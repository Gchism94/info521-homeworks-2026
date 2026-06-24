"""Loaders parse tiny fixtures with the correct header/dtype/columns."""
import numpy as np

from info521.data import load_olympic_100m, load_fcml_classification, load_capstone


def test_load_olympic_100m(tmp_path):
    p = tmp_path / "olympic.csv"
    p.write_text("Year,Time (seconds)\n1896,12\n1900,11\n1904,11\n")
    year, time = load_olympic_100m(str(p))
    assert year.shape == (3,) and time.shape == (3,)        # header skipped, unpacked
    assert np.array_equal(year, [1896, 1900, 1904])
    assert np.array_equal(time, [12, 11, 11])


def test_load_fcml_classification(tmp_path):
    xp = tmp_path / "X.csv"
    tp = tmp_path / "t.csv"
    xp.write_text("-2.5,-2.8\n1.0,0.5\n3.1,-1.2\n")          # headerless, 2 columns
    tp.write_text("0\n1\n0\n")                                # headerless labels
    X, t = load_fcml_classification(str(xp), str(tp))
    assert X.shape == (3, 2) and t.shape == (3,)
    assert np.array_equal(t, [0, 1, 0])
    assert X[1, 0] == 1.0 and X[1, 1] == 0.5


def test_load_capstone(tmp_path):
    p = tmp_path / "capstone.csv"
    p.write_text("x,t\n-2.0,0.16\n0.0,1.5\n2.5,-0.3\n")      # header skipped
    x, t = load_capstone(str(p))
    assert x.shape == (3,) and t.shape == (3,)
    assert np.array_equal(x, [-2.0, 0.0, 2.5])
    assert t[1] == 1.5
