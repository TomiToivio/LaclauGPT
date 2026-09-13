# -*- coding: utf-8 -*-
"""Compatibility project presets for the current paper pipeline.

The canonical package configuration lives under ``config/``.  This module is a
small compatibility layer for utilities that still expect Python project
metadata.  Research vocabulary may be richer than the six canonical AI26
formation labels used for computational aggregation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from laclaugpt.formations import CANONICAL_FORMATIONS

PROJECTS_DIR = Path(__file__).resolve().parent / "config" / "projects"


@dataclass(frozen=True)
class ProjectPreset:
    name: str
    topic_key: str
    title: str
    default_sources: list[dict[str, str]]
    seed_signifiers: list[str] = field(default_factory=list)
    seed_actors: list[str] = field(default_factory=list)
    seed_formations: list[str] = field(default_factory=list)
    languages: tuple[str, ...] = ()
    memory_subdir: str = ""
    notes: str = ""

    def memory_dir(self, base: Path | None = None) -> Path:
        base = base or Path("./data/memory")
        return base / (self.memory_subdir or self.name)


PROJECTS: dict[str, ProjectPreset] = {
    "ai26": ProjectPreset(
        name="ai26",
        topic_key="ai-contestation",
        title="Ideological contestation over AI (paper project, 3 arenas)",
        default_sources=[
            {"platform": "web", "country": "us", "language": "en",
             "query": "elite blogs / substacks / forums (Goertzel round)"},
            {"platform": "tiktok", "country": "fi", "language": "fi",
             "query": "grassroots: data centres, jobs, surveillance"},
            {"platform": "x", "country": "eu", "language": "en",
             "query": "elite + grassroots X discourse"},
        ],
        seed_signifiers=[
            "artificial intelligence", "existential risk", "abundance",
            "stagnation", "innovation", "data centre", "job displacement",
        ],
        seed_actors=[
            "Machine Intelligence Research Institute",
            "Distributed AI Research Institute",
            "Effective Accelerationism", "PauseAI",
        ],
        seed_formations=list(CANONICAL_FORMATIONS),
        languages=("en", "fi"),
        memory_subdir="ai26",
        notes="Arena runs live in run_configs/arena_*.yaml. Formation labels "
              "are canonical aggregation labels, not a closed ontology. No "
              "publication deadline is encoded here.",
    ),
}


def get_project(name: str) -> ProjectPreset:
    if name not in PROJECTS:
        raise KeyError(f"unknown project: {name!r} (known: {sorted(PROJECTS)})")
    return PROJECTS[name]


def project_yaml_path(name: str) -> Path:
    return PROJECTS_DIR / f"{name}.yaml"


def list_projects() -> list[str]:
    return sorted(PROJECTS)
