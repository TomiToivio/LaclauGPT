import unittest

from laclaugpt.synthesis import (
    SynthesisConfig,
    group_annotations,
    synthesize_annotations,
    synthesize_group,
)
from laclaugpt_interchange import (
    Articulation,
    DocumentAnnotation,
    FormationAssessment,
    MemoryRef,
)


def ref(obj_id: str, label: str, kind: str = "signifier") -> MemoryRef:
    return MemoryRef(obj_id=obj_id, label=label, kind=kind, raw=label)


def annotation(
    document_id: str,
    *,
    date: str,
    author: str,
    platform: str,
    signifier: str,
    formation: str,
) -> DocumentAnnotation:
    sig = ref(f"S-{signifier}", signifier)
    target = ref("T-target", "target")
    return DocumentAnnotation(
        document_id=document_id,
        source_timestamp=f"{date}T12:00:00Z",
        source_author=author,
        source_platform=platform,
        signifiers=[sig],
        formation_candidates=[
            FormationAssessment(
                formation=ref(f"F-{formation}", formation, "formation"),
                evidence="source evidence",
                evidence_verified=True,
            )
        ],
        articulations=[
            Articulation(
                signifier=sig,
                related_to=[target],
                evidence="source evidence",
                evidence_verified=True,
            )
        ],
        relevance="relevant",
    )


class CorpusSynthesisTests(unittest.TestCase):
    def test_composable_grouping(self) -> None:
        docs = [
            annotation("d1", date="2026-09-14", author="alice", platform="x", signifier="AI", formation="accel"),
            annotation("d2", date="2026-09-14", author="bob", platform="x", signifier="AI", formation="critical"),
        ]
        groups = group_annotations(docs, ["date", "signifier"])
        self.assertIn((("date", "2026-09-14"), ("signifier", "AI")), groups)
        self.assertEqual(len(groups[(("date", "2026-09-14"), ("signifier", "AI"))]), 2)

    def test_configurable_minimum_and_grouping(self) -> None:
        docs = [
            annotation("d1", date="2026-09-14", author="alice", platform="x", signifier="AI", formation="accel"),
            annotation("d2", date="2026-09-14", author="bob", platform="x", signifier="AI", formation="critical"),
        ]
        config = SynthesisConfig(group_by=["source_platform"], minimum_documents=2)
        result = synthesize_annotations(docs, config=config)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].grouping, {"source_platform": "x"})
        self.assertEqual(result[0].document_count, 2)
        self.assertEqual(result[0].document_ids, ["d1", "d2"])

    def test_explicit_change_fields(self) -> None:
        previous = [
            annotation("old", date="2026-09-13", author="alice", platform="x", signifier="safety", formation="doomer"),
        ]
        current = [
            annotation("new", date="2026-09-14", author="alice", platform="x", signifier="abundance", formation="accel"),
        ]
        result = synthesize_group(
            current,
            grouping={"author": "alice"},
            previous_annotations=previous,
            config=SynthesisConfig(minimum_documents=1),
        )
        self.assertIn("abundance", result.detected_changes.emerging_signifiers)
        self.assertIn("safety", result.detected_changes.declining_signifiers)
        self.assertIn("accel", result.detected_changes.emerging_formations)
        self.assertEqual(result.detected_changes.continuity_or_drift, "meaningful drift")
        self.assertIsNotNone(result.previous_window_reference)
        self.assertTrue(result.provenance["human_in_the_loop"])
        self.assertTrue(result.provenance["frequency_is_not_hegemony"])

    def test_irrelevant_documents_are_excluded(self) -> None:
        kept = annotation("kept", date="2026-09-14", author="alice", platform="x", signifier="AI", formation="accel")
        dropped = annotation("marked", date="2026-09-14", author="bob", platform="x", signifier="AI", formation="accel")
        dropped.relevance = "irrelevant"
        result = synthesize_annotations(
            [kept, dropped],
            config=SynthesisConfig(group_by=["date"], minimum_documents=1),
        )
        self.assertEqual(result[0].document_ids, ["kept"])


if __name__ == "__main__":
    unittest.main()
