"""M11 — diagrams + docs presence and basic validity (T363, T474–T476)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DIAGRAM_HEADERS = {
    "class_diagram.mmd": "classDiagram",
    "block_diagram.mmd": "flowchart",
    "sequence_diagram.mmd": "sequenceDiagram",
}


def test_diagrams_exist_with_valid_headers():
    for name, header in DIAGRAM_HEADERS.items():
        text = (ROOT / "diagrams" / name).read_text()
        assert text.lstrip().startswith(header), f"{name} must start with {header}"


def test_all_ten_adrs_present_and_indexed():
    adr_dir = ROOT / "docs" / "adr"
    files = sorted(adr_dir.glob("ADR-*.md"))
    assert len(files) == 10
    index = (adr_dir / "README.md").read_text()
    for f in files:
        assert f.name in index, f"{f.name} missing from ADR index"


def test_six_mechanism_prds_present_and_indexed():
    prd_dir = ROOT / "docs" / "prd"
    files = sorted(prd_dir.glob("mech-*.md"))
    assert len(files) == 6
    index = (prd_dir / "README.md").read_text()
    for f in files:
        assert f.name in index


def test_root_docs_present():
    for name in ("prd.md", "Plan.md", "Todo.md", "CHANGELOG.md"):
        assert (ROOT / name).exists()


def test_readme_figures_exist():
    """Every image the README embeds must be committed (no 404s)."""
    figures = ROOT / "docs" / "figures"
    for name in ("chase_filmstrip.png", "board_hero.png", "architecture.png",
                 "sequence.png", "class_diagram.png"):
        assert (figures / name).exists(), f"missing README figure: {name}"
