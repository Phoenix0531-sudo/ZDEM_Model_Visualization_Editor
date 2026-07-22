"""Smoke tests for ZDEM parser (real pytest, no sample DSL scripts)."""

from __future__ import annotations

import os
import tempfile

from zdem_editor.core.parser import ZDEMParser


def _parse_line(line: str):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".zdem", delete=False, encoding="utf-8") as f:
        f.write(line + "\n")
        path = f.name
    try:
        parser = ZDEMParser()
        return parser.parse_file(path)
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def test_parse_wall_numeric_color():
    model = _parse_line(
        "WALL id 0 nodes ( 1000.0, 14250.0 )   ( 1000.0, 18500.0 ) kn=2e3 ks=2e3 fric=0.00 color=1"
    )
    assert model is not None


def test_parse_gline_p1_p2():
    model = _parse_line(
        "GLINE P1 (  10000.0,  10000.0 ) P2 (  10000.0, 30000.0 ) r 80.0 color blue GROUP bom_wall"
    )
    assert model is not None


def test_parse_prop_p4():
    model = _parse_line(
        "prop group presturct range P4 (10500.0, 12125.0) (10600.0, 12225.0) "
        "(19980.0, 14375.0) (19980.0, 14475.0)"
    )
    assert model is not None
