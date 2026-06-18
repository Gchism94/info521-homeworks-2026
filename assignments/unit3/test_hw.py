"""Unit 3 autograder — Monte Carlo recovery / convergence / floor-AND-guard specs (seeded).

Stochastic: distributional/convergence checks (within X% of truth), never pinned draws. The
analytic E[f(X)]=18.61 and the 2-D/3-D/n-D pi formulas are written derivations graded per-step
(specs.md).
"""
import math
import numpy as np
from pytest import approx
from hw import (f, monte_carlo_expectation, estimate_pi_using_circle,
                estimate_pi_using_sphere, estimate_pi_using_n_ball, number_of_orthants)


def _rng(seed=0):
    return np.random.default_rng(seed)


# ---------- Part A: Monte Carlo expectation ----------
def test_f_values():
    """Spec A-f: f matches the polynomial at sample points (not a constant)."""
    assert f(0) == approx(35) and f(2) == approx(35 + 6 - 12 + 1.6 + 0.16)

def test_mc_recovers_analytic_expectation():
    """Recovery: MC estimate -> analytic E[f(X)] = 18.61 (seeded, distributional)."""
    assert monte_carlo_expectation(200000, _rng(0)) == approx(18.61, rel=0.02)

def test_mc_convergence_improves():
    """FLOOR-AND-GUARD: mean |error| shrinks with N (a constant estimator can't)."""
    small = np.mean([abs(monte_carlo_expectation(100, _rng(s)) - 18.61) for s in range(12)])
    large = np.mean([abs(monte_carlo_expectation(50000, _rng(s)) - 18.61) for s in range(12)])
    assert large < small and large < 0.5


# ---------- Part B: estimating pi ----------
def test_number_of_orthants():
    assert [number_of_orthants(n) for n in range(1, 6)] == [2, 4, 8, 16, 32]

def test_circle_converges():
    assert estimate_pi_using_circle(200000, _rng(0)) == approx(math.pi, rel=0.02)

def test_circle_is_stochastic_not_constant():
    """GUARD: a hardcoded constant cannot pass — two seeded draws differ, both plausible."""
    a, b = estimate_pi_using_circle(20000, _rng(1)), estimate_pi_using_circle(20000, _rng(2))
    assert a != b and 3.0 < a < 3.3 and 3.0 < b < 3.3

def test_sphere_converges():
    assert estimate_pi_using_sphere(200000, _rng(0)) == approx(math.pi, rel=0.02)

def test_n_ball_running_contract_and_converges():
    est = estimate_pi_using_n_ball(3, 2000, _rng(0))
    assert len(est) == 1999
    assert est[-1] == approx(math.pi, rel=0.1)

def test_pi_convergence_improves_with_n():
    """FLOOR-AND-GUARD: mean |error| shrinks with N for the circle estimator."""
    small = np.mean([abs(estimate_pi_using_circle(50, _rng(s)) - math.pi) for s in range(15)])
    large = np.mean([abs(estimate_pi_using_circle(50000, _rng(s)) - math.pi) for s in range(15)])
    assert large < small and large < 0.05
