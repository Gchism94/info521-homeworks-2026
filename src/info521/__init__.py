"""info521 — shared *plumbing* for the INFO 521 homework units.

Scope (enforced): reproducibility (seeded RNG), data loaders, plotting style,
path resolution, and test helpers. This package contains **only what students may
see** — it never holds assessed/derivable content (no normal equations, no design
matrix, no estimators, no posterior/predictive math, nothing from inside
``### SOLUTION ###`` / ``%%% Answer %%%`` / ``#answer()`` markers).

The top level re-exports the cheapest, most-used helper (``make_rng``); the rest
live in submodules (``info521.data``, ``info521.viz``, ``info521.testing``,
``info521.paths``) so that ``import info521`` does not pull matplotlib.
"""
from .rng import DEFAULT_SEED, make_rng

__version__ = "0.1.0"
__all__ = ["make_rng", "DEFAULT_SEED", "__version__"]
