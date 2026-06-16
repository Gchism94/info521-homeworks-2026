"""Tests for the hw."""

import numpy as np
from pytest import approx
from hw import w_MAP, g_cov


def test_w_MAP():
    assert w_MAP == approx([1.63985881, 1.99983755])

def test_g_cov():
    assert g_cov[0] == approx([3.50656249, -1.25041951])
    assert g_cov[1] == approx([-1.25041951,  3.17126848])
