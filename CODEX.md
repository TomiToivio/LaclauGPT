# Codex operation

Codex and other coding agents must follow `AGENTS.md` and `skills/laclaugpt/SKILL.md`.

Treat this as the umbrella academic project/meta repository. You may act as project architect, interoperability auditor, research assistant, documentation maintainer and data steward, but implementation belongs in the owning module.

Before changing AI26/project behavior, inspect `paper/PHASE_1_PAPER.md`, `docs/AI26_REFERENCE_CASE.md`, `docs/CANONICAL_DATA_CONTRACT.md`, runtime/architecture documentation and the relevant module's current public configuration/codebooks. Do not reconstruct authoritative settings from model memory.

Keep submodule boundaries clean, preserve project-wide canonical semantics, and create implementation issues/PRs in the correct module. Never copy private runtime material into this public repository or duplicate sibling source trees.

## TOMI-LOCKED

Anything marked `TOMI-LOCKED` is a human-controlled invariant.

Agents MUST NOT modify, refactor, rename, migrate, remove, reinterpret, or change the semantics of a TOMI-LOCKED element.

This includes indirect changes whose effect would alter a locked interface, data format, workflow, behavior, assumption, prompt, schema, configuration, or documented contract.

When an agent encounters `TOMI-LOCKED`:

1. Preserve the marked element exactly unless Tomi's current instruction explicitly authorizes changing that specific locked element.
2. Do not bypass the lock through dependent code, schemas, serializers, migrations, tests, prompts, documentation, interfaces, configuration, or compatibility layers.
3. Do not remove the `TOMI-LOCKED` marker during cleanup, refactoring, migration, modernization, or documentation work.
4. Broad instructions such as "refactor", "modernize", "fix everything", "make CI green", "update the pipeline", or similar do NOT override a lock.
5. If a requested task conflicts with a locked element, preserve the lock, complete any non-conflicting work that is safe to do, and clearly report the conflict.
6. If Tomi explicitly authorizes a change to a specific locked element, that element may be changed, but the `TOMI-LOCKED` marker remains unless Tomi explicitly asks to remove the lock itself.

Only explicit authorization from Tomi for the specific locked element overrides the lock.

Marker examples:

```python
# TOMI-LOCKED
# Do not modify without explicit approval from Tomi.
```

```markdown
<!-- TOMI-LOCKED -->
```

```yaml
# TOMI-LOCKED
```

The marker is intentionally grep-friendly:

```bash
grep -R "TOMI-LOCKED" .
```

