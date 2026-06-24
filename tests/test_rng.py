"""make_rng: returns the documented Generator and is reproducible."""
import numpy as np

from info521 import make_rng
from info521.rng import DEFAULT_SEED


def test_returns_numpy_generator():
    assert isinstance(make_rng(0), np.random.Generator)


def test_same_seed_same_draw():
    a = make_rng(0).random(100)
    b = make_rng(0).random(100)
    assert np.array_equal(a, b)


def test_different_seed_differs():
    a = make_rng(0).random(100)
    c = make_rng(1).random(100)
    assert not np.array_equal(a, c)


def test_default_seed_is_reproducible():
    assert DEFAULT_SEED == 0
    assert np.array_equal(make_rng().random(10), make_rng().random(10))


def test_none_seed_is_unseeded():
    # Allowed but not reproducible: two None-seeded generators should differ.
    assert not np.array_equal(make_rng(None).random(50), make_rng(None).random(50))
