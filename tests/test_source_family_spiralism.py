from pathlib import Path

from laclaugpt.config import load_source_family
from laclaugpt.formations import CANONICAL_FORMATIONS

ROOT = Path(__file__).resolve().parents[1]


def test_spiralism_is_source_family_not_canonical_formation():
    family = load_source_family("ai-spiralism")
    assert family["project"] == "ai26"
    assert family["category"] == "synthetic_spirituality"
    assert family["subcategory"] == "spiralism"
    assert family["status"] == "exploratory"
    assert family["collection_configuration"] == "private"
    assert set(family["must_not_absorb"]) == set(CANONICAL_FORMATIONS)
    assert "spiralism" not in CANONICAL_FORMATIONS
    assert "ai spiralism" not in CANONICAL_FORMATIONS


def test_paper_does_not_reintroduce_spiralism():
    paper = (ROOT / "paper" / "PAPER.md").read_text(encoding="utf-8").casefold()
    assert "ai spiralism" not in paper
    assert "synthetic spirituality" not in paper


def test_seed_codebook_keeps_spiral_terms_out_of_formations():
    from seed_codebook import SEEDS

    formations = {label for kind, label, _definition in SEEDS if kind == "formation"}
    assert formations == set(CANONICAL_FORMATIONS)
    assert "ai spiralism" not in formations
    signifiers = {label for kind, label, _definition in SEEDS if kind == "signifier"}
    assert {"spiral", "recursion", "synthetic spirituality"} <= signifiers
