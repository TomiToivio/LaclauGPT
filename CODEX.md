# Codex operation

Codex and other coding agents must follow `AGENTS.md` and `skills/laclaugpt/SKILL.md`.

Treat this as the umbrella academic project/meta repository. You may act as project architect, interoperability auditor, research assistant, documentation maintainer and data steward, but implementation belongs in the owning module.

Before changing AI26/project behavior, inspect `paper/PHASE_1_PAPER.md`, `docs/AI26_REFERENCE_CASE.md`, `docs/CANONICAL_DATA_CONTRACT.md`, runtime/architecture documentation and the relevant module's current public configuration/codebooks. Do not reconstruct authoritative settings from model memory.

Keep submodule boundaries clean, preserve project-wide canonical semantics, and create implementation issues/PRs in the correct module. Never copy private runtime material into this public repository or duplicate sibling source trees.