"""Each assert helper PASSES valid input and RAISES on the degenerate case
(mutation-guard discipline). Thresholds are passed in, never hardcoded here."""
import numpy as np
import pytest

from info521.testing import (
    assert_psd,
    assert_beats_baseline,
    assert_converges,
    assert_stochastic,
    REL_TOL,
    ABS_TOL,
    approx,
)


# ---------- assert_psd ----------
def test_psd_passes_on_psd_matrix():
    assert_psd(np.array([[2.0, 0.5], [0.5, 2.0]]))


def test_psd_raises_on_asymmetric():
    with pytest.raises(AssertionError):
        assert_psd(np.array([[1.0, 2.0], [0.0, 1.0]]))


def test_psd_raises_on_negative_eigenvalue():
    with pytest.raises(AssertionError):
        assert_psd(np.array([[1.0, 0.0], [0.0, -1.0]]))


# ---------- assert_beats_baseline ----------
def test_beats_baseline_passes_for_good_fit():
    target = np.array([1.0, 2.0, 3.0, 4.0])
    assert_beats_baseline(target + 0.01, target, frac=0.7)     # near-perfect prediction


def test_beats_baseline_raises_for_mean_predictor():
    target = np.array([1.0, 2.0, 3.0, 4.0])
    mean_pred = np.full_like(target, target.mean())            # no improvement on baseline
    with pytest.raises(AssertionError):
        assert_beats_baseline(mean_pred, target, frac=0.7)


# ---------- assert_converges ----------
def test_converges_passes_when_error_shrinks():
    assert_converges(err_small_n=1.0, err_large_n=0.1, ceiling=0.5)


def test_converges_raises_when_not_shrinking():
    with pytest.raises(AssertionError):
        assert_converges(err_small_n=0.1, err_large_n=0.2)


def test_converges_raises_above_ceiling():
    with pytest.raises(AssertionError):
        assert_converges(err_small_n=1.0, err_large_n=0.4, ceiling=0.3)


# ---------- assert_stochastic ----------
def test_stochastic_passes_on_differing_draws():
    assert_stochastic(np.array([1, 2, 3]), np.array([1, 2, 4]))


def test_stochastic_raises_on_identical():
    with pytest.raises(AssertionError):
        assert_stochastic(np.array([1, 2, 3]), np.array([1, 2, 3]))


# ---------- re-exports ----------
def test_tolerances_and_approx_reexported():
    assert REL_TOL == 1e-3 and ABS_TOL == 1e-6
    assert 1.0 == approx(1.0 + 1e-9)
