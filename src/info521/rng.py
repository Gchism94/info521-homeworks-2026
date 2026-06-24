"""Reproducibility: the one canonical seeded-RNG construction surface.

Every unit should build its generator with ``make_rng(seed)`` instead of calling
``np.random.default_rng`` directly. Centralizing it here means the numpy RNG-stream
pin (``numpy==2.1.*``) is guarded in exactly one place: if numpy is bumped, this is
the only function whose stream behaviour needs re-checking.
"""
from __future__ import annotations

import numpy as np

#: Default seed used across the course when a caller does not specify one.
DEFAULT_SEED: int = 0


def make_rng(seed: int | None = DEFAULT_SEED) -> np.random.Generator:
    """Return a seeded NumPy ``Generator`` (``np.random.default_rng(seed)``).

    Parameters
    ----------
    seed:
        Integer seed for reproducibility (default ``DEFAULT_SEED`` = 0). Passing
        ``None`` yields an unseeded generator — allowed, but not reproducible.
    """
    return np.random.default_rng(seed)
