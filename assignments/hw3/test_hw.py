"""Tests for the homework."""

import numpy as np
from pytest import approx
from hw import PolynomialRegressionModel, scale


def test_get_design_matrix_shape():
    model = PolynomialRegressionModel(3)
    x, t = np.loadtxt("data100m.csv", delimiter=",", skiprows=1, unpack=True)
    assert model.get_design_matrix_shape(x) == (27, 4)


def test_initialize_design_matrix():
    model = PolynomialRegressionModel(3)
    X = model.initialize_design_matrix((27, 4))
    assert X.shape == (27, 4)


def test_model_params():
    """Test model parameters found using least-squares approach."""
    x, t = np.loadtxt("data100m.csv", delimiter=",", skiprows=1, unpack=True)
    model = PolynomialRegressionModel(1)
    model.train(x, t)
    assert model.w[0] == approx(36.4164559)
    assert model.w[1] == approx(-0.0133308857)

    model = PolynomialRegressionModel(2)
    model.train(x, t)
    assert model.w[0] == approx(455.59785579660615)
    assert model.w[1] == approx(-0.4431604855345469)
    assert model.w[2] == approx(0.00011015155196387)


def test_first_order_prediction():
    """Test winning time prediction for 2012 with a first-order polynomial"""
    x, t = np.loadtxt("data100m.csv", delimiter=",", skiprows=1, unpack=True)
    model = PolynomialRegressionModel(1)
    model.train(x, t)
    winning_time_for_2012 = model.predict(np.array([2012]))[0]
    assert winning_time_for_2012 == approx(9.594713852048779)


def test_second_order_prediction():
    """Test winning time prediction for 2012 with a second-order polynomial"""
    x, t = np.loadtxt("data100m.csv", delimiter=",", skiprows=1, unpack=True)
    model = PolynomialRegressionModel(2)
    model.train(x, t)
    winning_time_for_2012 = model.predict(np.array([2012]))[0]
    assert winning_time_for_2012 == approx(9.868303074326368)


def test_scale():
    """Test scaling"""
    arr = np.array(
        [
            0.48558948,
            0.79734976,
            0.51286662,
            0.80593392,
            0.93484382,
            0.39261496,
            0.73133769,
            0.97869016,
            0.6799601,
            0.84983537,
        ]
    )
    arr_scaled, arr_min, arr_range = scale(arr)
    assert arr_scaled == approx(
        [
            0.15863923,
            0.69058509,
            0.20518128,
            0.70523196,
            0.9251865,
            0.0,
            0.57795098,
            1.0,
            0.49028714,
            0.78013949,
        ]
    )

    assert arr_min == approx(0.39261496406609664)
    assert arr_range == approx(0.5860751925305081)
