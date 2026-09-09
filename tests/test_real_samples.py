"""Integration tests: the parser must handle the real ZDEM DSL samples in Test/."""

from __future__ import annotations

from pathlib import Path

from zdem_editor.core.parser import ZDEMParser

ROOT = Path(__file__).resolve().parents[1]
TEST_DIR = ROOT / "Test"

SAMPLES = {
    "gen0.py": dict(walls=2, glines=6, p4=0),
    "shear0.py": dict(walls=1, glines=4, p4=0),
    "shear1.py": dict(walls=1, glines=0, p4=3),
    "test_prop_p4.py": dict(walls=1, glines=1, p4=1),
}


def test_parser_handles_real_dsl_samples():
    for name, expected in SAMPLES.items():
        path = TEST_DIR / name
        assert path.exists(), f"sample {name} missing"
        model = ZDEMParser().parse_file(str(path))
        assert len(model.walls) == expected["walls"], name
        assert len(model.glines) == expected["glines"], name
        assert len(model.prop_p4s) == expected["p4"], name


def test_gen0_glines_carry_groups():
    """Strike-slip sample: geometry lines are grouped (bom_wall / top_wall...)."""
    model = ZDEMParser().parse_file(str(TEST_DIR / "gen0.py"))
    groups = {g.group for g in model.glines}
    assert "bom_wall" in groups and "top_wall" in groups


def test_shear1_p4_polygons_are_quads():
    model = ZDEMParser().parse_file(str(TEST_DIR / "shear1.py"))
    assert len(model.prop_p4s) == 3
    for poly in model.prop_p4s:
        assert len(poly.points) == 4
