"""Unit 5 autograder — four-ways-to-one-posterior Correctness specifications.

MAP & Laplace are deterministic (closed-form scalars with rel headroom + properties); MCMC is
seeded and graded distributionally (recovery + floor-AND-guard), never on pinned draws. The
CROSS-METHOD specs check the four methods recover the *same* posterior. The PGM structural specs
(hw13) and the two written derivations (hw14 Poisson, hw15 Beta-Binomial) are human-graded
(specs.md) and have no autograded test here.
"""
import numpy as np
from pytest import approx
from hw import (logistic, gradient, hessian, newton_map, laplace_covariance,
                MetropolisSampler, load_data, SIG_SQ)

X, t = load_data()
W_MAP = np.array([1.63985881, 1.99983755])
# Laplace covariance at the MAP, pinned from the reference solution at authoring time
# (it IS the inverse negative Hessian of the log-posterior, computed under the numpy 2.1.x
# RNG/ABI pin). Pinned as a VALUE so the autograder checks correctness WITHOUT handing
# students the `inv(-hessian(...))` one-liner they are meant to derive.
G_COV = np.array([[3.50656249, -1.25041951], [-1.25041951, 3.17126848]])


def _chain(seed=0, n=8000, burn=2000, pv=0.5):
    s = MetropolisSampler(X, t, pv, SIG_SQ, seed=seed)
    return np.array(s.generate_samples(n))[burn:]


# ---------- Way 2: MAP via Newton-Raphson ----------
def test_map_recovery_floor():
    """Recovery floor: Newton reaches a stationary point of the log-posterior."""
    assert np.linalg.norm(gradient(newton_map(X, t), X, t)) < 1e-4

def test_map_matches_reference():
    assert newton_map(X, t) == approx(W_MAP, rel=1e-3)

def test_hessian_negative_definite():
    assert np.all(np.linalg.eigvalsh(hessian(W_MAP, X)) < 0)


# ---------- Way 3: Laplace approximation ----------
def test_laplace_is_inverse_neg_hessian_psd():
    """L1: the Laplace covariance equals the inverse negative Hessian of the log-posterior --
    verified by VALUE against the pinned G_COV fixture (NOT the `inv(-hessian(...))`
    expression students must derive) -- and is symmetric and positive-definite."""
    g = laplace_covariance(W_MAP, X)
    assert g == approx(G_COV, rel=1e-3)                              # correctness: value, not the one-liner
    assert g == approx(g.T) and np.all(np.linalg.eigvalsh(g) > 0)    # symmetric + positive-definite

def test_laplace_matches_reference():
    assert laplace_covariance(W_MAP, X) == approx(G_COV, rel=1e-3)


# ---------- Way 4: MCMC (properties + distributional recovery) ----------
def test_mcmc_log_prior():
    s = MetropolisSampler(X, t, 0.1, 0.25)
    assert s.log_prior(np.array([1.0, 2.0])) == approx(-(1**2 + 2**2) / (2 * 0.25))

def test_mcmc_log_likelihood_and_acceptance():
    s = MetropolisSampler(X, t, 0.1, 0.5)
    P = np.clip(logistic(X @ np.array([1.0, 2.0])), 1e-12, 1 - 1e-12)
    assert s.log_likelihood(np.array([1.0, 2.0])) == approx(
        (t @ np.log(P) + (1 - t) @ np.log(1 - P)).sum())
    w, wc = np.array([0.0, 0.0]), np.array([4.0, 3.0])
    lr = (s.log_prior(wc) + s.log_likelihood(wc) - s.log_prior(w) - s.log_likelihood(w))
    assert s.compute_acceptance_ratio(w, wc) == approx(np.exp(lr))

def test_mcmc_proposal_seeded_and_shaped():
    a = MetropolisSampler(X, t, 0.1, 0.5, seed=100).sample_from_proposal(np.array([1.0, 2.0]))
    b = MetropolisSampler(X, t, 0.1, 0.5, seed=100).sample_from_proposal(np.array([1.0, 2.0]))
    assert a.shape == (2,) and a == approx(b)

def test_mcmc_recovers_posterior_and_mixes():
    """Distributional recovery + FLOOR-AND-GUARD: plausible mean, PSD cov, and the chain
    actually mixes (a stuck/degenerate chain has ~0 variance and fails)."""
    c = _chain(seed=0)
    mean, cov = c.mean(0), np.cov(c.T)
    assert np.all((mean > 0.3) & (mean < 5.0))
    assert np.all(np.linalg.eigvalsh(cov) > 0)
    assert np.all(np.diag(cov) > 0.5)        # GUARD: mixes (not stuck at a point)


# ---------- CROSS-METHOD: four ways, one posterior ----------
def test_cross_method_map_mode_inside_mcmc_posterior():
    """The Newton MAP (mode) lies inside the MCMC posterior bulk (mode != mean, but consistent)."""
    c = _chain(seed=0)
    assert np.linalg.norm(W_MAP - c.mean(0)) < 2.5 * np.sqrt(max(np.linalg.eigvalsh(np.cov(c.T))))

def test_cross_method_laplace_matches_mcmc_spread():
    """Laplace and MCMC recover a similar posterior spread (std within a factor of 2)."""
    c = _chain(seed=0)
    ratio = np.sqrt(np.diag(np.cov(c.T))) / np.sqrt(np.diag(G_COV))
    assert np.all((ratio > 0.5) & (ratio < 2.0))
