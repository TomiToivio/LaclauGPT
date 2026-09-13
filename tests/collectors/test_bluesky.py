"""Offline tests for the recycled public Bluesky collector."""
from __future__ import annotations

import json

import pytest

from collector.bluesky import collect, iter_pages, normalize_post


def _post(identifier: str = "3abc") -> dict:
    return {
        "uri": f"at://did:plc:synthetic/app.bsky.feed.post/{identifier}",
        "author": {"handle": "researcher.test", "displayName": "Synthetic Researcher"},
        "record": {
            "text": "AI futures are contested #synthetic",
            "createdAt": "2026-09-13T08:00:00Z",
            "langs": ["en"],
            "tags": ["synthetic"],
            "facets": [{"features": [
                {"uri": "https://example.invalid/source"},
                {"did": "did:plc:mentioned"},
            ]}],
        },
        "likeCount": 4,
        "repostCount": 2,
        "replyCount": 1,
    }


def test_normalize_post_preserves_identity_evidence_and_provenance():
    record = normalize_post(_post(), raw_ref="raw/bluesky/page.ndjson")
    assert record["document_id"].startswith("at://")
    assert record["source_url"] == "https://bsky.app/profile/researcher.test/post/3abc"
    assert record["text"] == "AI futures are contested #synthetic"
    assert record["engagement"] == {"likes": 4, "reposts": 2, "replies": 1, "quotes": 0}
    assert record["collection_provenance"]["raw_ref"] == "raw/bluesky/page.ndjson"


def test_iter_pages_requires_exactly_one_collection_mode():
    with pytest.raises(ValueError, match="exactly one"):
        list(iter_pages())
    with pytest.raises(ValueError, match="exactly one"):
        list(iter_pages(query="ai", actor="researcher.test"))


def test_collect_stores_raw_normalized_manifest_and_deduplicates(tmp_path):
    calls = []

    def fake_fetch(endpoint, params):
        calls.append((endpoint, params))
        return {"posts": [_post()]}

    first = collect(data_root=tmp_path, query="AI", fetch_json=fake_fetch)
    second = collect(data_root=tmp_path, query="AI", fetch_json=fake_fetch)
    assert first["new_posts"] == 1
    assert second["new_posts"] == 0
    assert calls[0][0] == "app.bsky.feed.searchPosts"
    normalized = [
        json.loads(line)
        for line in (tmp_path / "normalized" / "bluesky.jsonl")
        .read_text(encoding="utf-8").splitlines()
    ]
    assert len(normalized) == 1
    assert normalized[0]["platform"] == "bluesky"
    assert list((tmp_path / "raw" / "bluesky").rglob("*.ndjson"))
    assert len(list((tmp_path / "manifests").glob("run-*.json"))) == 2


def test_author_feed_unwraps_post_views():
    def fake_fetch(endpoint, params):
        assert endpoint == "app.bsky.feed.getAuthorFeed"
        assert params["actor"] == "researcher.test"
        return {"feed": [{"post": _post()}]}

    pages = list(iter_pages(actor="researcher.test", fetch_json=fake_fetch))
    assert pages[0][1][0]["uri"].endswith("/3abc")
