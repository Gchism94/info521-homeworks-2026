"""Unit 0 autograder — onboarding completion + the seed policy (kept light)."""
import numpy as np
from pytest import approx
from hw import add, seeded_draw


def test_add():
    assert add(1, 1) == 2

def test_add_properties():
    """Light cases so a constant stub can't pass: identity, negatives, commutativity, floats."""
    assert add(0, 5) == 5 and add(-3, 3) == 0
    assert add(2, 7) == add(7, 2)
    assert add(0.5, 0.25) == 0.75

def test_seed_policy_reproducible():
    """The seed policy (graded Process spec): same seed -> identical draw; it is stochastic."""
    a, b = seeded_draw(0, 100), seeded_draw(0, 100)
    assert np.array_equal(a, b)                 # reproducible
    assert a.shape == (100,) and not np.array_equal(seeded_draw(1, 100), a)  # seed actually matters
