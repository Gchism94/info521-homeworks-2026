"""Path resolution for unit data files.

The units load data with relative paths (``"data/X.csv"``, ``"data100m.csv"``),
which only works when the process CWD happens to be the unit directory.
``data_path`` resolves a file relative to the **caller's** location instead, so a
loader works no matter where pytest / quarto is invoked from.

Resolution is relative to the CALLER (or an explicit ``base``), **never** relative
to the installed ``info521`` package.
"""
from __future__ import annotations

import inspect
import os


def data_path(filename: str, base: str | None = None) -> str:
    """Return the absolute path to ``filename`` relative to the caller's directory.

    Parameters
    ----------
    filename:
        Path fragment to resolve, e.g. ``"data/X.csv"`` or ``"data100m.csv"``.
    base:
        If given, resolve relative to this directory instead of inferring the
        caller. If omitted, the directory of the file that *called* ``data_path``
        is used; if that cannot be determined (REPL/notebook), the current working
        directory is used as a fallback.
    """
    if base is None:
        caller_file = inspect.stack()[1].filename
        if caller_file and os.path.isfile(caller_file):
            base = os.path.dirname(os.path.abspath(caller_file))
        else:
            base = os.getcwd()
    return os.path.abspath(os.path.join(base, filename))
