"""Tests for the homework"""

from pytest import approx
from hw import calculate_poisson_pmf_a, calculate_poisson_pmf_b

def test_poisson_pmf_a():
    assert calculate_poisson_pmf_a() == approx(0.7673431912197031)

def test_poisson_pmf_b():
    assert calculate_poisson_pmf_b() == approx(0.23265680878029693)
