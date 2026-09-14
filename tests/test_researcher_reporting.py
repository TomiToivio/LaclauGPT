import json
import tempfile
import unittest
from pathlib import Path

from laclaugpt.researcher_reporting import (
    humanize_summary,
    render_researcher_report,
    write_researcher_report,
)
from laclaugpt_interchange import DocumentAnnotation


class ResearcherReportingTests(unittest.TestCase):
    def test_humanize_summary_renders_structured_json(self) -> None:
        summary = json.dumps({
            "narrative_construction": "A reform narrative",
            "political_entities": ["actor-a", "actor-b"],
            "grievances": {"issue": "cost", "status": "absent"},
        })
        rendered = humanize_summary(summary)
        self.assertIn("**Narrative**: A reform narrative", rendered)
        self.assertIn("**Political entities**: actor-a; actor-b", rendered)
        self.assertIn("**Grievances**: issue: cost", rendered)
        self.assertNotIn('"narrative_construction"', rendered)

    def test_humanize_summary_preserves_plain_text(self) -> None:
        self.assertEqual(humanize_summary("plain-language summary"), "plain-language summary")

    def test_report_keeps_machine_summary_separate_from_human_view(self) -> None:
        raw = json.dumps({"political_classification": "contested"})
        ann = DocumentAnnotation(document_id="doc-1", summary=raw)
        report = render_researcher_report([ann], project_label="Synthetic")
        self.assertEqual(ann.summary, raw)
        self.assertIn("# Synthetic analysis report", report)
        self.assertIn("**Political classification**: contested", report)
        self.assertNotIn('"political_classification"', report)

    def test_write_report(self) -> None:
        ann = DocumentAnnotation(document_id="doc-1", summary="Readable")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.md"
            returned = write_researcher_report([ann], path)
            self.assertEqual(returned, str(path))
            self.assertIn("Readable", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
