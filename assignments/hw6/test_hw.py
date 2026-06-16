"""Tests for the homework."""

from pytest import approx
from hw import expectations


def test_expectation_values():
    """Test model parameters found using least-squares approach."""
    assert expectations[0:10] == approx(
        [
            3.57855833,
            16.35364788,
            15.71438918,
            16.25004994,
            17.50904091,
            17.04557439,
            17.4767006,
            17.87095725,
            16.95103646,
            16.78459524,
        ]
    )

    assert expectations[-1] == approx(17.713951811257257)
