import unittest

from laclaugpt.researcher_reporting import (
    render_human_readable_analysis,
    researcher_row,
    research_facing_payload,
)
from laclaugpt_interchange import DocumentAnnotation, MemoryRef


class ResearcherRowParityTests(unittest.TestCase):
    def test_complete_render_contains_every_populated_top_level_field(self) -> None:
        ann = DocumentAnnotation(
            document_id="doc-1",
            source_platform="x",
            source_author="researcher-visible-author",
            source_timestamp="2026-09-15T08:00:00Z",
            transformations={
                "source_text": "Original source text",
                "transcript": "Whisper transcript",
                "frame_analysis": {"frame": "public safety"},
                "stage_models": {"discourse": "model-a"},
                "stage_warnings": ["example warning"],
            },
            collection_provenance={
                "native_metadata": {
                    "conversation_id": "conv-1",
                    "engagement": {"likes": 4},
                }
            },
            topics=[MemoryRef(obj_id="T1", label="topic-a", kind="topic")],
            prompt_versions={"discourse": "v3"},
            evidence_quotes=["verbatim evidence"],
            uncertainties=["needs review"],
            relevance="relevant",
        )
        rendered = render_human_readable_analysis(ann)
        payload = research_facing_payload(ann)

        # The renderer is schema-driven: every populated top-level field must
        # have a visible heading. Adding a schema field without exposing it to
        # researchers therefore breaks this test.
        for field in payload:
            label = field.replace("_", " ").capitalize()
            self.assertIn(f"## {label}", rendered, field)

        self.assertIn("Original source text", rendered)
        self.assertIn("Whisper transcript", rendered)
        self.assertIn("public safety", rendered)
        self.assertIn("conversation_id", rendered)
        self.assertIn("model-a", rendered)
        self.assertIn("verbatim evidence", rendered)

    def test_researcher_row_keeps_machine_fields_and_adds_human_view(self) -> None:
        ann = DocumentAnnotation(
            document_id="doc-2",
            summary="machine-readable value",
            transformations={"source_text": "hello"},
        )
        row = researcher_row(ann)
        self.assertEqual(row["document_id"], "doc-2")
        self.assertEqual(row["summary"], "machine-readable value")
        self.assertIn("human_readable_analysis", row)
        self.assertIn("hello", row["human_readable_analysis"])


if __name__ == "__main__":
    unittest.main()
