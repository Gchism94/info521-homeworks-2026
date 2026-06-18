"""Convergence/property tests for hw17 (Monte Carlo pi)."""

import math
import numpy as np
from pytest import approx
from hw import (
    estimate_pi_using_circle,
    estimate_pi_using_sphere,
    estimate_pi_using_n_ball,
    number_of_orthants,
)


def test_number_of_orthants():
    assert [number_of_orthants(n) for n in range(1, 6)] == [2, 4, 8, 16, 32]


def test_circle_converges():
    assert estimate_pi_using_circle(100000) == approx(math.pi, rel=0.02)


def test_circle_is_stochastic_not_constant():
    """GUARD: a hardcoded constant cannot pass -- two draws differ, both plausible."""
    a, b = estimate_pi_using_circle(20000), estimate_pi_using_circle(20000)
    assert a != b
    assert 3.0 < a < 3.3 and 3.0 < b < 3.3


def test_sphere_converges():
    assert estimate_pi_using_sphere(100000) == approx(math.pi, rel=0.02)


def test_n_ball_running_contract():
    est = estimate_pi_using_n_ball(3, 1000)
    assert len(est) == 999  # length n_samples - 1
    assert est[-1] == approx(math.pi, rel=0.1)


def test_convergence_improves_with_n():
    """FLOOR+GUARD: mean |error| shrinks with more samples (a constant estimator can't)."""
    small = np.mean([abs(estimate_pi_using_circle(50) - math.pi) for _ in range(15)])
    large = np.mean([abs(estimate_pi_using_circle(50000) - math.pi) for _ in range(15)])
    assert large < small
    assert large < 0.05
