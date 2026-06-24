"""Data loaders — parse-only.

Each loader takes an **explicit path** (no bundled CSVs; the data lives in each
unit's own ``data/`` directory). These functions only read and shape the file
exactly as the units' current ``load_data`` does — they perform **no modelling**.

Mirrors the existing per-unit loaders so adoption is drop-in:
  * U1  Olympic-100m : ``np.loadtxt(delimiter=",", skiprows=1, unpack=True)``
  * U5  FCML         : two headerless CSVs (X has 2 columns, t is 1-D labels)
  * Cap Capstone     : ``np.loadtxt(delimiter=",", skiprows=1)`` -> columns (x, t)
"""
from __future__ import annotations

import numpy as np


def load_olympic_100m(path: str) -> tuple[np.ndarray, np.ndarray]:
    """Load the Olympic-100m data as ``(year, winning_time)``.

    CSV with a header row and two columns (``Year``, ``Time``).
    """
    return np.loadtxt(path, delimiter=",", skiprows=1, unpack=True)


def load_fcml_classification(x_path: str, t_path: str) -> tuple[np.ndarray, np.ndarray]:
    """Load the FCML binary-classification data as ``(X, t)``.

    The dataset is two headerless CSVs: ``x_path`` holds the ``(N, 2)`` feature
    matrix, ``t_path`` holds the ``(N,)`` labels in ``{0, 1}``. Two explicit paths
    are taken because the data is genuinely two files (see the proposal's Flag B).
    """
    X = np.loadtxt(x_path, delimiter=",")
    t = np.loadtxt(t_path)
    return X, t


def load_capstone(path: str) -> tuple[np.ndarray, np.ndarray]:
    """Load the Capstone data as ``(x, t)``.

    CSV with a header row and two columns (``x``, ``t``).
    """
    d = np.loadtxt(path, delimiter=",", skiprows=1)
    return d[:, 0], d[:, 1]
