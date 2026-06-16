"""Tests for the hw."""

import numpy as np
from pytest import approx
from hw import SimpleLinearModel


def test_model_params():
    """Test model parameters found using least-squares approach."""
    x, t = np.loadtxt("data100m.csv", delimiter=",", skiprows=1, unpack=True)
    model = SimpleLinearModel()
    model.train(x, t)
    assert model.w0 == approx(36.41645590250286)
    assert model.w1 == approx(-0.013330885710960602)
