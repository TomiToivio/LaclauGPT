#!/usr/bin/env python3
"""Offline guard for the AI26 two-machine runtime policy (Laskin + NooPunk).

Issue #71 built a second AI26 Phase 2 node. Its policy lives in
`docs/AI26_EXECUTION_ARCHITECTURE.md`, which until now nothing checked: the
document could have its model options deleted, or acquire a machine-specific
namespace, and CI would stay green.

This guard checks the things that would silently stop the two machines being *one
system*, in four groups:

1. **Roles** — the policy table assigns each machine what the issue specifies, and
   keeps the deliberately asymmetric browser duty.
2. **Model options** — NooPunk's on-demand models are both named, and the local one
   is the default. Deleting either, or making cloud the default, fails here.
3. **One namespace** — no machine-specific database, bucket, project id or run id.
   This is the rule that prevents two corpora, so it is checked in the doc text.
4. **Agreement with the schema** — the doc's cloud claims must match
   `schemas/distributed-run.schema.json`, where `cloud_fallback` is pinned `false`.
   A doc and a schema that disagree about whether cloud fallback exists is exactly
   the drift this file exists to catch.

Offline and dependency-free, like its sibling `verify_cross_module_fixture.py`.
Run: python3 scripts/verify_two_machine_policy.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHITECTURE = ROOT / "docs" / "AI26_EXECUTION_ARCHITECTURE.md"
DISTRIBUTED_SCHEMA = ROOT / "schemas" / "distributed-run.schema.json"
PROFILE_DIR = ROOT / "deploy" / "ai26-distributed"

#: The two nodes and the stages the issue assigns them. `continuous` / `on demand`
#: are the policy values; the absence of a browser duty for Laskin is the
#: intentionally asymmetric part.
EXPECTED_ROLES = {
    "Laskin": {
        "non_browser": "continuous",
        "browser": "never",
        "analysis": "continuous",
        "visualization": "continuous",
    },
    "NooPunk": {
        "non_browser": "supported",
        "browser": "continuous",
        "analysis": "on demand",
        "visualization": "on demand",
    },
}

#: NooPunk's two explicit model modes. The local one is the default.
NOOPUNK_LOCAL_MODEL = "gemma4:e2b"
NOOPUNK_CLOUD_MODEL = "gemma4:31b-cloud"
LASKIN_MODEL = "gemma4:12b"

#: Machine-suffixed namespace values. None may appear, because both nodes write one
#: `ai26` namespace. Only hyphenated forms are listed: the underscore forms
#: (`ai26_laskin`, `ai26_noopunk`) collide with legitimate documentation filenames
#: such as `AI26_LASKIN_DASHBOARD.md`, so matching them would fail on the runbook
#: links rather than on a real namespace.
MACHINE_SPECIFIC_NAMESPACES = (
    "ai26-laskin",
    "ai26-noopunk",
    "ai26-laskin-",
    "ai26-noopunk-",
    "laskin-ai26",
    "noopunk-ai26",
    "laskin__",
    "noopunk__",
)


def _text() -> str:
    return ARCHITECTURE.read_text(encoding="utf-8")


def _flat() -> str:
    return " ".join(_text().split())


def _role_table() -> dict[str, dict[str, str]]:
    """Parse the roles table into {machine: {stage: value}}.

    Returns lowercase cells with markdown emphasis stripped, so `**continuous**`
    and `continuous` compare equal.
    """
    text = _text()
    start = text.index("## Roles")
    end = text.index("```text", start)
    table_lines = [
        line for line in text[start:end].splitlines() if line.strip().startswith("|")
    ]
    rows: dict[str, dict[str, str]] = {}
    for line in table_lines:
        cells = [c.strip().replace("*", "") for c in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        machine = cells[0].strip()
        if machine.lower() in ("machine", "") or set(machine) <= set("-: "):
            continue
        rows[machine] = {
            "non_browser": cells[1].lower(),
            "browser": cells[2].lower(),
            "analysis": cells[3].lower(),
            "visualization": cells[4].lower(),
        }
    return rows


def check_roles() -> None:
    rows = _role_table()
    for machine, expected in EXPECTED_ROLES.items():
        assert machine in rows, (
            f"the roles table no longer lists {machine}; the two-machine policy must "
            f"name both nodes"
        )
        actual = rows[machine]
        for stage, want in expected.items():
            assert actual[stage] == want, (
                f"{machine}.{stage} is {actual[stage]!r}, expected {want!r}. "
                f"Changing a node's role changes which machine runs what; update "
                f"issue #71's policy and this guard together."
            )
    print("Roles: Laskin continuous analysis/visualization, NooPunk continuous browser.")


def check_model_options() -> None:
    flat = _flat()
    for model in (NOOPUNK_LOCAL_MODEL, NOOPUNK_CLOUD_MODEL, LASKIN_MODEL):
        assert model in flat, (
            f"{model!r} is no longer documented. NooPunk offers "
            f"{NOOPUNK_LOCAL_MODEL!r} (local, default) and {NOOPUNK_CLOUD_MODEL!r} "
            f"(cloud, explicit opt-in); Laskin runs {LASKIN_MODEL!r}."
        )

    # The mode table must mark local as the default and cloud as opt-in. Parsing the
    # table (rather than scanning a character window after the model name) matters:
    # a window search passed while "default" appeared in the *cloud* row's prose
    # ("defaulted"), so it could not tell which mode was the default.
    rows = [
        line for line in _text().splitlines()
        if line.strip().startswith("|") and "gemma4:" in line
    ]
    local_rows = [r for r in rows if "local" in r.lower()]
    cloud_rows = [r for r in rows if "cloud" in r.lower()]
    assert local_rows, "no table row presents NooPunk's local analysis mode"
    assert cloud_rows, "no table row presents NooPunk's cloud analysis mode"

    assert any("default" in r.lower() for r in local_rows), (
        f"the local mode row no longer marks {NOOPUNK_LOCAL_MODEL!r} as the default"
    )
    assert any(NOOPUNK_LOCAL_MODEL in r for r in local_rows), (
        f"the local mode row does not name {NOOPUNK_LOCAL_MODEL!r}"
    )

    for row in cloud_rows:
        assert NOOPUNK_CLOUD_MODEL in row, (
            f"the cloud mode row does not name {NOOPUNK_CLOUD_MODEL!r}: {row.strip()!r}"
        )
        assert "default" not in row.lower().replace("defaulted", ""), (
            f"the cloud mode row presents {NOOPUNK_CLOUD_MODEL!r} as a default; "
            f"cloud is opt-in only"
        )
        assert "explicit" in row.lower() or "opt-in" in row.lower(), (
            f"the cloud mode row does not mark cloud as explicit/opt-in: "
            f"{row.strip()!r}"
        )

    cloud_positions = [m.start() for m in re.finditer(re.escape(NOOPUNK_CLOUD_MODEL), flat)]
    cloud_context = flat[max(0, cloud_positions[0] - 260):cloud_positions[0] + 260].lower()
    assert "explicit" in cloud_context or "opt-in" in cloud_context, (
        f"{NOOPUNK_CLOUD_MODEL!r} is not documented as explicit/opt-in. Cloud use "
        f"must never be silent (issue #71)."
    )

    lower = flat.lower()
    for phrase in ("never silent", "rejected"):
        assert phrase in lower, (
            f"the architecture no longer states that cloud use is {phrase!r}; "
            f"NooPunk's cloud mode is opt-in only and an unknown model option is "
            f"rejected rather than defaulted"
        )
    print(
        f"Models: NooPunk local {NOOPUNK_LOCAL_MODEL} (default), cloud "
        f"{NOOPUNK_CLOUD_MODEL} (explicit); Laskin {LASKIN_MODEL}."
    )


def check_one_namespace() -> None:
    text = _text()
    lower = text.lower()
    for marker in MACHINE_SPECIFIC_NAMESPACES:
        assert marker not in lower, (
            f"the architecture names a machine-specific namespace {marker!r}. A "
            f"machine is execution provenance, never study identity: both nodes "
            f"write one `ai26` namespace."
        )
    # the doc must still state the single project id explicitly
    assert re.search(r"one value, `ai26`", _flat()), (
        "the architecture no longer states that the project id is one value, `ai26`, "
        "on both machines"
    )
    for phrase in ("execution provenance, never study", "one `ai26` namespace"):
        assert phrase in lower, (
            f"the architecture no longer states {phrase!r}; that rule is what keeps "
            f"the two nodes one system rather than two corpora"
        )
    print("Namespace: no machine-specific database, bucket, project id or run id.")


def check_schema_agreement() -> None:
    """The doc's cloud claims and the schema's cloud contract must agree."""
    schema = json.loads(DISTRIBUTED_SCHEMA.read_text(encoding="utf-8"))
    cloud_fallback = schema["properties"]["analysis"]["properties"]["cloud_fallback"]
    assert cloud_fallback["const"] is False, (
        "distributed-run.schema.json no longer pins analysis.cloud_fallback to "
        "false; the architecture doc claims no silent local-to-cloud fallback and "
        "the two must not disagree"
    )
    schema_model = schema["properties"]["analysis"]["properties"]["model"]
    assert schema_model["const"] == LASKIN_MODEL, (
        f"the schema's pinned analysis model is {schema_model['const']!r}, but the "
        f"architecture documents Laskin at {LASKIN_MODEL!r}"
    )

    # every public profile must still be secret-free and keep cloud fallback off
    forbidden = ("mongodb://", "mongodb+srv://", "redis://", "rediss://", "AKIA")
    profiles = sorted(PROFILE_DIR.glob("*.example.json"))
    assert profiles, f"no public AI26 profiles found under {PROFILE_DIR}"
    for path in profiles:
        raw = path.read_text(encoding="utf-8")
        for marker in forbidden:
            assert marker not in raw, f"{path.name} contains a live value {marker!r}"
        data = json.loads(raw)
        assert data["analysis"]["cloud_fallback"] is False, (
            f"{path.name} enables cloud fallback; it must be opt-in only"
        )
        assert data["project_id"] == "ai26", f"{path.name} is not on the ai26 project"
    print(
        f"Schema agreement: cloud_fallback pinned false, model {LASKIN_MODEL}, "
        f"{len(profiles)} secret-free profiles."
    )


def main() -> int:
    assert ARCHITECTURE.is_file(), f"missing {ARCHITECTURE}"
    check_roles()
    check_model_options()
    check_one_namespace()
    check_schema_agreement()
    print("AI26 two-machine runtime policy is consistent and secret-free.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
