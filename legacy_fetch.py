# -*- coding: utf-8 -*-
"""Generic legacy media-fetch compatibility helpers.

Project-specific storage locations, identifiers and empirical mappings are not
published here. This module only retains reusable manifest/dedup/download logic.
"""
from __future__ import annotations

import csv
import hashlib
import os
import urllib.error
import urllib.request
from pathlib import Path

ID_COLUMN = "document_id"
URL_COLUMNS = ("source_url", "media_url", "allas_url")
DEFAULT_CHUNK = 1 << 20


def load_manifest(manifest_path: str | Path) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    with open(manifest_path, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            url = next((str(row.get(k, "")).strip() for k in URL_COLUMNS if row.get(k)), "")
            if not url:
                raise ValueError("manifest row has no supported media URL")
            pairs.append((str(row[ID_COLUMN]).strip(), url))
    return pairs


def unique_urls(pairs: list[tuple[str, str]]) -> list[str]:
    return list(dict.fromkeys(url for _, url in pairs))


def _dest_for(workdir: Path, url: str) -> Path:
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]
    suffix = Path(url.split("?", 1)[0]).suffix or ".bin"
    return workdir / f"{digest}{suffix}"


def fetch_video(url: str, workdir: Path, *, chunk: int = DEFAULT_CHUNK,
                timeout: float = 60.0, max_retries: int = 3) -> Path:
    dest = _dest_for(workdir, url)
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    workdir.mkdir(parents=True, exist_ok=True)
    for attempt in range(max_retries + 1):
        try:
            request = urllib.request.Request(url, method="GET", headers={"User-Agent": "LaclauGPT/1.0"})
            with urllib.request.urlopen(request, timeout=timeout) as response, open(dest, "wb") as fh:
                if response.status != 200:
                    raise RuntimeError(f"unexpected status {response.status}")
                while True:
                    block = response.read(chunk)
                    if not block:
                        break
                    fh.write(block)
            if dest.stat().st_size == 0:
                dest.unlink(missing_ok=True)
                raise RuntimeError("empty download")
            return dest
        except (urllib.error.URLError, TimeoutError, RuntimeError) as exc:
            if dest.exists() and dest.stat().st_size == 0:
                dest.unlink(missing_ok=True)
            if attempt >= max_retries:
                raise RuntimeError(f"fetch failed after {max_retries} retries") from exc
    raise RuntimeError("unreachable")


def fetch_all(manifest_path: str | Path, workdir: Path, *, max_retries: int = 3) -> dict[str, str]:
    return {url: str(fetch_video(url, workdir, max_retries=max_retries))
            for url in unique_urls(load_manifest(manifest_path))}


def _tmpdir() -> Path:
    return Path(os.environ.get("TMPDIR", "./tmp_legacy"))
