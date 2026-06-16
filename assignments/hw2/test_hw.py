"""Tests for the lab."""

import numpy as np
from pytest import approx
from hw import w, winning_time_for_2012, w_second_order


def test_model_params():
    """Test model parameters found using least-squares approach."""
    assert w[0] == approx(36.4164559)
    assert w[1] == approx(-0.0133308857)

def test_prediction():
    """Test winning time prediction for 2012."""
    assert winning_time_for_2012 == approx(9.594713852048779)

def test_second_order_fit():
    """Test the second order polynomial fit."""
    assert w_second_order[0] == approx(455.597856)
    assert w_second_order[1] == approx(-0.443160486)
    assert w_second_order[2] == approx(0.000110151552)
