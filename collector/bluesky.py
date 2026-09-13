"""Public Bluesky/XRPC collector with LaclauGPT provenance.

Clean-room adaptation of the useful public-API pattern in the legacy
LaclauGPT-Data-Collection repository. Credentials, MongoDB coupling, and
best-effort firehose decoding are deliberately excluded. Collection remains
separate from discourse-theoretical interpretation.
"""
from __future__ import annotations

import argparse
import json
import os
import urllib.parse
import urllib.request
from urllib.error import HTTPError
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterator

from . import COLLECTOR_VERSION
from .store import Store


PUBLIC_XRPC = "https://public.api.bsky.app/xrpc"
FetchJSON = Callable[[str, dict[str, Any]], dict[str, Any]]


def _fetch_json(endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
    query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    headers = {"Accept": "application/json", "User-Agent": "LaclauGPT/2.0"}
    token = os.getenv("BSKY_ACCESS_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(
        f"{PUBLIC_XRPC}/{endpoint}?{query}", headers=headers,
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except HTTPError as exc:
        if exc.code in {401, 403} and endpoint == "app.bsky.feed.searchPosts":
            raise RuntimeError(
                "Bluesky search is not anonymous for this AppView; set "
                "BSKY_ACCESS_TOKEN to a short-lived access JWT, or use --actor"
            ) from exc
        raise
    if not isinstance(payload, dict):
        raise ValueError("Bluesky XRPC response must be a JSON object")
    return payload


def normalize_post(post: dict[str, Any], *, raw_ref: str = "") -> dict[str, Any]:
    """Map an app.bsky.feed.defs#postView to the collector schema."""
    record = post.get("record") if isinstance(post.get("record"), dict) else {}
    author = post.get("author") if isinstance(post.get("author"), dict) else {}
    uri = str(post.get("uri") or "")
    post_id = uri.rsplit("/", 1)[-1] if uri else ""
    handle = str(author.get("handle") or "")
    facets = record.get("facets") if isinstance(record.get("facets"), list) else []
    links: list[str] = []
    mentions: list[str] = []
    for facet in facets:
        for feature in facet.get("features", []) if isinstance(facet, dict) else []:
            if not isinstance(feature, dict):
                continue
            if feature.get("uri"):
                links.append(str(feature["uri"]))
            if feature.get("did"):
                mentions.append(str(feature["did"]))
    labels = record.get("tags") if isinstance(record.get("tags"), list) else []
    source_url = (
        f"https://bsky.app/profile/{handle}/post/{post_id}"
        if handle and post_id else uri
    )
    captured_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return {
        "document_id": uri or post_id,
        "platform": "bluesky",
        "author": handle,
        "author_display": author.get("displayName"),
        "timestamp": str(record.get("createdAt") or post.get("indexedAt") or ""),
        "source_url": source_url,
        "text": str(record.get("text") or ""),
        "hashtags": [str(tag) for tag in labels],
        "mentions": list(dict.fromkeys(mentions)),
        "urls": list(dict.fromkeys(links)),
        "engagement": {
            "likes": int(post.get("likeCount") or 0),
            "reposts": int(post.get("repostCount") or 0),
            "replies": int(post.get("replyCount") or 0),
            "quotes": int(post.get("quoteCount") or 0),
        },
        "language": (record.get("langs") or [None])[0],
        "media_references": [],
        "collection_provenance": {
            "captured_at": captured_at,
            "captured_from_url": source_url,
            "captured_from_response": "public.api.bsky.app XRPC",
            "collector_version": COLLECTOR_VERSION,
            "transformations": ["bluesky-postView-normalise"],
            "raw_ref": raw_ref,
        },
    }


def iter_pages(
    *, query: str | None = None, actor: str | None = None,
    max_results: int = 500, cursor: str | None = None,
    fetch_json: FetchJSON = _fetch_json,
) -> Iterator[tuple[dict[str, Any], list[dict[str, Any]], str | None]]:
    """Yield raw pages and post views from search or author-feed XRPC."""
    if bool(query) == bool(actor):
        raise ValueError("provide exactly one of query or actor")
    if max_results < 1:
        raise ValueError("max_results must be positive")
    collected = 0
    while collected < max_results:
        limit = min(100, max_results - collected)
        if query:
            endpoint = "app.bsky.feed.searchPosts"
            params = {"q": query, "limit": limit, "sort": "latest", "cursor": cursor}
            raw = fetch_json(endpoint, params)
            posts = raw.get("posts") or []
        else:
            endpoint = "app.bsky.feed.getAuthorFeed"
            params = {"actor": actor, "limit": limit, "cursor": cursor}
            raw = fetch_json(endpoint, params)
            posts = [item.get("post", {}) for item in (raw.get("feed") or [])]
        valid = [post for post in posts if isinstance(post, dict)]
        cursor = raw.get("cursor")
        yield raw, valid, str(cursor) if cursor else None
        collected += len(valid)
        if not valid or not cursor:
            break


def collect(
    *, data_root: str | Path, query: str | None = None,
    actor: str | None = None, max_results: int = 500,
    fetch_json: FetchJSON = _fetch_json,
) -> dict[str, Any]:
    """Collect public Bluesky posts into the canonical durable store."""
    store = Store(Path(data_root))
    key = f"query:{query}" if query else f"actor:{actor}"
    pages = posts_seen = inserted = 0
    cursor = store.get_cursor(key, "bluesky")
    try:
        for raw, posts, cursor in iter_pages(
            query=query, actor=actor, max_results=max_results,
            cursor=cursor, fetch_json=fetch_json,
        ):
            pages += 1
            raw_ref = store.append_raw("bluesky", raw)
            for post in posts:
                posts_seen += 1
                normalized = normalize_post(post, raw_ref=raw_ref)
                if not normalized["document_id"]:
                    continue
                inserted += int(store.upsert_post(normalized, raw_ref))
            store.checkpoint(key, "bluesky", cursor=cursor, status="ok")
        manifest = {
            "schema": "laclaugpt.collection-run/1.0",
            "platform": "bluesky",
            "collection_mode": "search" if query else "author_feed",
            "target": query or actor,
            "pages": pages,
            "posts_seen": posts_seen,
            "new_posts": inserted,
            "collector_version": COLLECTOR_VERSION,
            "interpretation_status": "source collection only; no discourse coding",
        }
        store.write_manifest(manifest)
        return manifest
    except Exception as exc:
        store.checkpoint(key, "bluesky", cursor=cursor, status=f"error: {exc}")
        raise
    finally:
        store.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Collect public Bluesky posts via XRPC")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--query")
    target.add_argument("--actor", help="Bluesky handle or DID")
    parser.add_argument("--data-root", required=True)
    parser.add_argument("--max-results", type=int, default=500)
    args = parser.parse_args(argv)
    print(json.dumps(collect(
        data_root=args.data_root, query=args.query, actor=args.actor,
        max_results=args.max_results,
    ), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
