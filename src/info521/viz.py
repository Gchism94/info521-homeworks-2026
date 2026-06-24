"""Shared plotting style — colorblind-safe palette + sane matplotlib defaults.

This is *style only*. It deliberately does **not** provide the ±2σ predictive-band
figure (that plots the student's own assessed results — see the proposal's EXCLUDE
list); it offers a palette and ``set_style`` so every unit's figures look
consistent and remain readable for colourblind viewers.

``PALETTE`` is the Okabe–Ito colourblind-safe qualitative palette (8 colours).
"""
from __future__ import annotations

import matplotlib as mpl

#: Okabe & Ito (2008) colourblind-safe qualitative palette — 8 named colours.
PALETTE: dict[str, str] = {
    "black": "#000000",
    "orange": "#E69F00",
    "sky_blue": "#56B4E9",
    "bluish_green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermillion": "#D55E00",
    "reddish_purple": "#CC79A7",
}


def set_style() -> None:
    """Apply the shared matplotlib rcParams: Okabe–Ito colour cycle + clean defaults.

    Idempotent; safe to call at the top of any unit notebook. Touches only
    ``matplotlib.rcParams`` (no backend selection, no figures created).
    """
    mpl.rcParams.update(
        {
            "figure.figsize": (5.0, 3.0),
            "figure.dpi": 110,
            "savefig.dpi": 150,
            "savefig.bbox": "tight",
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.3,
            "legend.frameon": False,
            "axes.prop_cycle": mpl.cycler(color=list(PALETTE.values())),
        }
    )
