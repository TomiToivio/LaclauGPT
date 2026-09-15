from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from laclaugpt.canonical_pipeline import _apply_context_options
from laclaugpt.context_profiles import load_profile
from laclaugpt.context_runtime import build_context_block


class _Run:
    def __init__(self):
        self.previous_batch_summary = ""
        self.corpus_stats_path = ""

    def enabled(self, module: str) -> bool:
        return module == "context_memory"


class _Memory:
    def __init__(self, block: str = "Codebook suggestions for signifier:\n- S001 = AI"):
        self.block = block
        self.calls = []

    def context_prompt_block(self, text, top_k_per_kind=5, kinds=()):
        self.calls.append((text, top_k_per_kind, tuple(kinds)))
        return self.block


class _Stage:
    def __init__(self, name: str, memory=None):
        self.stage_name = name
        self.run = _Run()
        self.memory = memory or _Memory()


class ContextRuntimeTests(unittest.TestCase):
    def test_balanced_profile_controls_real_retrieval_depth(self):
        stage = _Stage("discourse")
        profile = load_profile("balanced")
        block, provenance = build_context_block(
            stage, "source text", ("signifier", "formation"), profile
        )
        self.assertIn("S001", block)
        self.assertEqual(stage.memory.calls[0][1], 5)
        self.assertEqual(provenance["profile"], "balanced")
        self.assertFalse(provenance["codebook_missing"])
        self.assertEqual(len(provenance["sha256"]), 64)

    def test_high_accuracy_can_inject_previous_daily_state_as_untrusted(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "previous-day.json"
            state.write_text(json.dumps({
                "major_actors": ["Example actor"],
                "emerging_frames": ["abundance"],
                "review_status": "model_proposed",
            }), encoding="utf-8")
            stage = _Stage("discourse")
            stage.run.previous_batch_summary = str(state)
            block, provenance = build_context_block(
                stage, "source text", ("signifier",), load_profile("high_accuracy")
            )
        self.assertIn("PREVIOUS BATCH / DAILY SITUATIONAL STATE", block)
        self.assertIn("UNTRUSTED PRIOR STATE", block)
        state_prov = provenance["previous_batch_summary"]
        self.assertEqual(state_prov["trust"], "model_proposed")
        self.assertEqual(state_prov["source"], "previous-day.json")
        self.assertEqual(len(state_prov["sha256"]), 64)

    def test_human_reviewed_previous_state_is_marked_but_not_source_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "previous-day.json"
            state.write_text(json.dumps({
                "review_status": "human_reviewed",
                "important_signifiers": ["AI"],
            }), encoding="utf-8")
            stage = _Stage("populism")
            stage.run.previous_batch_summary = str(state)
            block, provenance = build_context_block(
                stage, "source text", ("signifier", "target"),
                load_profile("high_accuracy"),
            )
        self.assertIn("HUMAN-REVIEWED SITUATIONAL STATE", block)
        self.assertIn("Source documents remain primary evidence", block)
        self.assertEqual(
            provenance["previous_batch_summary"]["trust"], "human_reviewed"
        )

    def test_validation_profile_fails_loudly_when_required_codebook_missing(self):
        stage = _Stage(
            "discourse",
            _Memory("(no established codebook entries match this chunk yet)"),
        )
        with self.assertRaisesRegex(RuntimeError, "required codebook context is missing"):
            build_context_block(
                stage, "source text", ("signifier",), load_profile("validation")
            )

    def test_validation_fails_when_context_memory_module_is_disabled(self):
        stage = _Stage("discourse")
        stage.run.enabled = lambda module: False
        with self.assertRaisesRegex(RuntimeError, "required codebook context is missing"):
            build_context_block(
                stage, "source text", ("signifier",), load_profile("validation")
            )
        self.assertEqual(stage.memory.calls, [])

    def test_balanced_profile_marks_missing_codebook_without_failing(self):
        stage = _Stage(
            "discourse",
            _Memory("(no established codebook entries match this chunk yet)"),
        )
        _, provenance = build_context_block(
            stage, "source text", ("signifier",), load_profile("balanced")
        )
        self.assertTrue(provenance["codebook_required"])
        self.assertTrue(provenance["codebook_missing"])

    def test_canonical_dataset_pipeline_options_are_explicit_opt_in(self):
        run = SimpleNamespace()
        selected = _apply_context_options(run, {
            "pipeline": {
                "context_profile": "high_accuracy",
                "previous_batch_summary": "/private/previous.json",
                "corpus_stats_path": "/private/stats.json",
            }
        })
        self.assertEqual(selected, "high_accuracy")
        self.assertEqual(run.context_profile, "high_accuracy")
        self.assertEqual(run.previous_batch_summary, "/private/previous.json")
        self.assertEqual(run.corpus_stats_path, "/private/stats.json")

    def test_no_profile_does_not_mutate_run(self):
        run = SimpleNamespace()
        self.assertEqual(_apply_context_options(run, {"pipeline": {}}), "")
        self.assertFalse(hasattr(run, "context_profile"))


if __name__ == "__main__":
    unittest.main()
