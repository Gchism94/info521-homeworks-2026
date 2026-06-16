"""Tests for hw17."""

import math
import numpy as np
from pytest import approx
from hw import (
    estimate_pi_using_circle,
    estimate_pi_using_sphere,
    estimate_pi_using_n_ball,
)

def test_estimate_pi_using_circle_converges():
    assert estimate_pi_using_circle(100000) == approx(math.pi, rel=0.01)


def test_estimate_pi_using_sphere_converges():
    assert estimate_pi_using_sphere(100000) == approx(math.pi, rel=0.01)

def test_estimate_pi_using_n_ball_converges():
    for (dim, samples) in [(2, 1000), (3, 1000), (4, 1000)]:
        assert estimate_pi_using_n_ball(dim, samples)[-1] == approx(math.pi, rel=0.05)
