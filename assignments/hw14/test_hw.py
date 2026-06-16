"""Tests for the homework."""

import numpy as np
from pytest import approx
from hw import logistic, hessian, gradient


def test_logistic_function():
    assert logistic(1) == approx(0.7310585786300049)


def test_gradient_function():
    X = np.loadtxt("data/X.csv", delimiter=",")
    t = np.loadtxt("data/t.csv")
    sig_sq = 10

    w = np.zeros(2)  # Initial guess
    all_w = []
    all_w.append(w.flatten())
    for _ in range(10):
        w = w - np.linalg.inv(hessian(w, X, sig_sq)) @ gradient(
            w, X, t, sig_sq
        )
        all_w.append(w.flatten())

    print(all_w[-1])
    assert all_w[-1] == approx([1.63985881, 1.99983755])
