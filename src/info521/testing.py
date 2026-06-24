"""Generic, parameterized assertion helpers for the unit autograders.

INVARIANT — READ BEFORE ADDING ANYTHING HERE
============================================
This package holds **only what students may see**. There is **no hidden grading
logic** in this module, ever. Every threshold, tolerance, ratio, and ceiling is an
explicit **argument** supplied by the caller's ``test_hw.py`` — never baked in.
These helpers are *mechanics* (a PSD check, a baseline ratio, a convergence check,
a stochasticity guard), not *policy*. The numbers that decide pass/not-yet stay in
each unit's test file.
"""
from __future__ import annotations

import numpy as np
from pytest import approx  # re-exported so unit tests import tolerances + approx from one place

#: Suggested default tolerances. Callers may override per assertion.
REL_TOL: float = 1e-3
ABS_TOL: float = 1e-6

__all__ = [
    "approx",
    "REL_TOL",
    "ABS_TOL",
    "assert_psd",
    "assert_beats_baseline",
    "assert_converges",
    "assert_stochastic",
]


def assert_psd(matrix, tol: float = 1e-8) -> None:
    """Assert ``matrix`` is square, symmetric, and positive semidefinite.

    ``tol`` (an argument) is the allowed slack on the smallest eigenvalue.
    """
    M = np.asarray(matrix, dtype=float)
    assert M.ndim == 2 and M.shape[0] == M.shape[1], f"not a square matrix: shape {M.shape}"
    assert np.allclose(M, M.T), "matrix is not symmetric"
    min_eig = float(np.linalg.eigvalsh(M).min())
    assert min_eig >= -tol, f"matrix is not PSD: min eigenvalue {min_eig} < -{tol}"


def assert_beats_baseline(pred, target, frac: float, baseline_pred=None) -> None:
    """Assert ``rmse(pred, target) <= frac * rmse(baseline, target)``.

    ``frac`` (an argument, e.g. 0.7) is the required improvement ratio. ``baseline_pred``
    defaults to the constant-mean predictor (whose RMSE equals ``std(target)``).
    """
    pred = np.asarray(pred, dtype=float)
    target = np.asarray(target, dtype=float)
    if baseline_pred is None:
        baseline_pred = np.full_like(target, target.mean())
    else:
        baseline_pred = np.asarray(baseline_pred, dtype=float)
    model_rmse = float(np.sqrt(np.mean((target - pred) ** 2)))
    base_rmse = float(np.sqrt(np.mean((target - baseline_pred) ** 2)))
    assert model_rmse <= frac * base_rmse, (
        f"did not beat baseline: rmse {model_rmse:.6g} > {frac} * {base_rmse:.6g}"
    )


def assert_converges(err_small_n, err_large_n, ceiling: float | None = None) -> None:
    """Assert error shrank with more samples: ``err_large_n < err_small_n``.

    Optionally assert ``err_large_n < ceiling`` (an argument) so a hardcoded
    constant — whose error does not shrink — cannot pass.
    """
    err_small_n = float(err_small_n)
    err_large_n = float(err_large_n)
    assert err_large_n < err_small_n, (
        f"error did not shrink with N: {err_large_n:.6g} >= {err_small_n:.6g}"
    )
    if ceiling is not None:
        assert err_large_n < ceiling, f"large-N error {err_large_n:.6g} not below ceiling {ceiling}"


def assert_stochastic(a, b) -> None:
    """Assert two draws differ — a constant / hardcoded result cannot pass."""
    a = np.asarray(a)
    b = np.asarray(b)
    assert not np.array_equal(a, b), "values are identical — result is not stochastic"
