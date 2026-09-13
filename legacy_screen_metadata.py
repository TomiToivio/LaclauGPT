# -*- coding: utf-8 -*-
"""Generic OCR-derived screen metadata helpers for legacy media imports."""
from __future__ import annotations

import re
from dataclasses import dataclass, field

HANDLE_RE = re.compile(r"@([A-Za-z0-9._]{2,30})")
PLATFORM_HINTS = {
    "instagram": "Instagram",
    "tiktok": "TikTok",
    "reels": "Instagram",
    "for you": "TikTok",
    "seuraa": "Instagram",
    "seuraat": "Instagram",
    "seuraamme": "TikTok",
    "following": None,
}


@dataclass
class ScreenMetadata:
    handle: str | None = None
    display_name: str | None = None
    platform: str | None = None
    engagement: dict = field(default_factory=dict)
    ocr_confidence: float | None = None
    source: str = "ocr"
    review_status: str = "proposed"


def lift_handle(ocr_text: str) -> str | None:
    match = HANDLE_RE.search(ocr_text or "")
    return match.group(1) if match else None


def lift_platform(ocr_text: str) -> str | None:
    low = (ocr_text or "").lower()
    for hint, platform in PLATFORM_HINTS.items():
        if hint in low and platform:
            return platform
    return None


def lift_engagement(ocr_text: str) -> dict:
    out: dict = {}
    low = (ocr_text or "").lower()
    m = re.search(r"([\d.,\s]+)\s*(?:tykk|like)", low)
    if m:
        out["likes_text"] = m.group(1).strip()
    m = re.search(r"([\d.,\s]+)\s*(?:komment|comment)", low)
    if m:
        out["comments_text"] = m.group(1).strip()
    m = re.search(r"([\d.,\s]+)\s*(?:jako|share)", low)
    if m:
        out["shares_text"] = m.group(1).strip()
    if not out:
        bare = re.findall(r"^\s*([\d.,]+[KkMk]?)\s*$", ocr_text or "", re.M)
        if bare:
            out["bare_counters"] = bare[:4]
    return out


def extract_screen_metadata(ocr_text: str, *, confidence: float | None = None) -> ScreenMetadata:
    handle = lift_handle(ocr_text)
    display_name = None
    if handle:
        for line in (ocr_text or "").splitlines():
            line = line.strip()
            if handle in line or not line:
                continue
            if line.startswith("@") or line.lower().startswith(("seuraa", "follow")):
                continue
            if 2 < len(line) <= 60 and not line.isdigit():
                display_name = line
                break
    return ScreenMetadata(
        handle=handle,
        display_name=display_name,
        platform=lift_platform(ocr_text),
        engagement=lift_engagement(ocr_text),
        ocr_confidence=confidence,
    )


def screen_metadata_record(meta: ScreenMetadata) -> dict:
    return {"screen_metadata": {
        "handle": meta.handle,
        "display_name": meta.display_name,
        "platform": meta.platform,
        "engagement": meta.engagement,
        "ocr_confidence": meta.ocr_confidence,
        "source": meta.source,
        "review_status": meta.review_status,
    }}


def merge_into_asr_record(record: dict, ocr_text: str, *, confidence: float | None = None) -> dict:
    record.update(screen_metadata_record(extract_screen_metadata(ocr_text, confidence=confidence)))
    return record
