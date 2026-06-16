"""Tests for the homework."""

import numpy as np
from pytest import approx
from hw import PolynomialRegressionModel, sample_dataset


def test_predictive_variance_and_cov_w():
    """Test model parameters found using least-squares approach."""
    rng = np.random.default_rng(seed=100)
    x = np.array([1, 2, 3])
    t = sample_dataset(x, 6, rng)
    m = PolynomialRegressionModel(1, x, t)
    cov_w = m.compute_cov_w()
    assert m.predictive_variance(np.array([0.5]))[0] == approx(
        0.033335027248591345
    )
    assert m.compute_cov_w() == approx(
        np.array([[0.05333604, -0.0228583], [-0.0228583, 0.01142915]])
    )
