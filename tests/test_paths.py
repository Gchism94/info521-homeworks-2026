"""data_path resolves relative to the CALLER (or explicit base), not the package."""
import os

import info521
from info521.paths import data_path

HERE = os.path.dirname(os.path.abspath(__file__))


def test_resolves_relative_to_caller():
    # Called from THIS file -> resolves against this file's directory (tests/).
    resolved = data_path("fixtures/sample.csv")
    assert resolved == os.path.join(HERE, "fixtures", "sample.csv")
    assert os.path.isfile(resolved)


def test_not_relative_to_package():
    resolved = data_path("fixtures/sample.csv")
    pkg_dir = os.path.dirname(os.path.abspath(info521.__file__))
    assert not resolved.startswith(pkg_dir)


def test_explicit_base_overrides_caller(tmp_path):
    resolved = data_path("X.csv", base=str(tmp_path))
    assert resolved == os.path.join(str(tmp_path), "X.csv")


def test_returns_absolute_path():
    assert os.path.isabs(data_path("data/anything.csv"))
