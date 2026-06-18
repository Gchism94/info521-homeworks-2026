"""Unit 4 autograder — predictive-variance (hw10) + coin-game conjugacy (hw11) specs.

Closed-form/relationship checks (no brittle 100-element array pins). The Inverse-Gamma
conjugacy derivation (hw12) is a written, human-graded spec (specs.md).
"""
import numpy as np
from pytest import approx
from scipy.special import gamma as _g
from hw import (PolynomialRegressionModel, generate_synthetic_data, sample_dataset,
                B, Beta, posterior, calculate_marginal_likelihood,
                calculate_probability_of_winning)


def _model(order=2):
    rng = np.random.default_rng(0)
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]); t = sample_dataset(x, 6, rng)
    return PolynomialRegressionModel(order, x, t)


# ---------- Part A: predictive variance ----------
def test_cov_w_definition_psd():
    m = _model(); X = m.X_train
    assert m.compute_cov_w() == approx(m.sigma_sq * np.linalg.inv(X.T @ X))
    cov = m.compute_cov_w()
    assert cov == approx(cov.T) and np.all(np.linalg.eigvalsh(cov) >= -1e-10)

def test_predictive_variance_matches_cov_w():
    m = _model(); cov = m.compute_cov_w()
    xq = np.array([0.5, 1.5, 4.0]); Xn = m.get_design_matrix(xq)
    assert m.predictive_variance(xq) == approx(np.diag(Xn @ cov @ Xn.T))
    assert np.all(m.predictive_variance(np.linspace(-2, 7, 20)) >= 0)

def test_variance_larger_in_gap():
    """FLOOR-AND-GUARD: predictive variance is larger in the data gap than where data is dense."""
    rng = np.random.default_rng(0)
    x, t = generate_synthetic_data(rng, 40, -2, 7, 6, 2.5, 4.5)
    m = PolynomialRegressionModel(3, x, t)
    assert m.predictive_variance(np.array([3.5]))[0] > m.predictive_variance(np.array([0.0]))[0]


# ---------- Part B: Beta-Binomial conjugacy (the coin game) ----------
def test_B_function():
    assert B(2, 3) == approx(_g(2) * _g(3) / _g(5))

def test_beta_normalizes():
    r = np.linspace(0, 1, 100001)
    assert np.trapezoid(Beta(r, 2, 5), r) == approx(1.0, abs=1e-3)

def test_posterior_is_conjugate_beta():
    """The defining identity: posterior(r) == Beta(r | a+y_N, b+N-y_N) (replaces the array pins)."""
    r = np.linspace(0.01, 0.99, 50)
    assert posterior(r, 20, 13, 2.0, 3.0) == approx(Beta(r, 2.0 + 13, 3.0 + 20 - 13))

def test_posterior_mean_is_conjugate():
    """Beta posterior mean = (a+y_N)/(a+b+N) (pseudo-counts; ties to U2b Beta moments)."""
    r = np.linspace(0, 1, 200001)
    post = posterior(r, 20, 13, 2.0, 3.0)
    mean = np.trapezoid(r * post, r)
    assert mean == approx((2 + 13) / (2 + 3 + 20), abs=1e-3)

def test_marginal_likelihood_and_prob_win_are_probabilities():
    ml = calculate_marginal_likelihood(20, 13, 2.0, 3.0)
    pw = calculate_probability_of_winning(20, 13, 2.0, 3.0)
    assert 0.0 < ml < 1.0
    assert 0.0 <= pw <= 1.0
