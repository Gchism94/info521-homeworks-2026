"""Unit 2a autograder — Part A (Poisson) Correctness specifications.

Parts B/C (Bernoulli MLE, Fisher information) are written derivations graded per-step by
a human (specs.md) — they have no autograded tests here. Closed-form scalars keep exact
checks with rel headroom; the rest are distribution-property / guard checks.
"""

import math
from pytest import approx
from hw import poisson, calculate_poisson_pmf_a, calculate_poisson_pmf_b


def test_poisson_pmf_values():
    """Spec A-pmf: the Poisson pmf matches the closed form at several x (not a pasted constant)."""
    assert poisson(0, 3) == approx(math.exp(-3))
    assert poisson(1, 3) == approx(3 * math.exp(-3))
    assert poisson(4, 3) == approx(3 ** 4 / 24 * math.exp(-3))


def test_poisson_is_valid_distribution():
    """Spec A-dist: pmf in [0,1] and sums to ~1 over a wide range (normalization)."""
    probs = [poisson(x, 3) for x in range(0, 60)]
    assert all(0.0 <= p <= 1.0 for p in probs)
    assert sum(probs) == approx(1.0, abs=1e-9)


def test_pmf_a_closed_form():
    """Spec A1 (MUST-MEET): P(2<=X<=6) closed-form value."""
    assert calculate_poisson_pmf_a() == approx(0.7673431912197031, rel=1e-6)


def test_pmf_a_is_range_sum_not_constant():
    """Spec A2 (MUST-MEET guard): (a) equals the actual sum of the pmf over [LOW,HIGH]."""
    assert calculate_poisson_pmf_a() == approx(sum(poisson(y, 3) for y in range(2, 7)))


def test_complement():
    """Spec A3 (MUST-MEET): (a)+(b)=1 (total probability)."""
    assert calculate_poisson_pmf_a() + calculate_poisson_pmf_b() == approx(1.0)
    assert calculate_poisson_pmf_b() == approx(0.23265680878029693, rel=1e-6)
