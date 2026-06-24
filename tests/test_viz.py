"""set_style applies cleanly; PALETTE is the right length and colourblind-safe."""
import re

import matplotlib as mpl

from info521.viz import PALETTE, set_style

HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
# The canonical Okabe-Ito colourblind-safe palette (8 colours).
OKABE_ITO = {
    "#000000", "#E69F00", "#56B4E9", "#009E73",
    "#F0E442", "#0072B2", "#D55E00", "#CC79A7",
}


def test_palette_length_is_eight():
    assert len(PALETTE) == 8


def test_palette_values_are_valid_unique_hex():
    values = list(PALETTE.values())
    assert all(HEX.match(v) for v in values)
    assert len(set(values)) == 8                       # all distinct


def test_palette_is_okabe_ito_colorblind_safe():
    assert set(PALETTE.values()) == OKABE_ITO


def test_set_style_applies_rcparams():
    mpl.rcParams["axes.spines.top"] = True             # dirty it first
    set_style()
    assert tuple(mpl.rcParams["figure.figsize"]) == (5.0, 3.0)
    assert mpl.rcParams["axes.spines.top"] is False
    cycle_colors = mpl.rcParams["axes.prop_cycle"].by_key()["color"]
    assert cycle_colors == list(PALETTE.values())


def test_set_style_is_idempotent():
    set_style()
    set_style()
    assert mpl.rcParams["axes.prop_cycle"].by_key()["color"] == list(PALETTE.values())
