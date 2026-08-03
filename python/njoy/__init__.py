"""Binary distribution of the NJOY2016 nuclear data processing system.

The compiled ``njoy`` executable is shipped inside this package. Use
:func:`executable` to get its path, or call the ``njoy`` console script that is
installed alongside the package.
"""

import os
import sys
from pathlib import Path

try:  # pragma: no cover - trivial
    from importlib.metadata import PackageNotFoundError, version

    __version__ = version("njoy2016")
except Exception:  # PackageNotFoundError or missing metadata
    __version__ = "unknown"

#: Directory containing the bundled executable.
BIN_DIR = Path(__file__).parent / "bin"

__all__ = ["BIN_DIR", "executable", "run", "__version__"]


def executable() -> Path:
    """Return the path to the bundled ``njoy`` executable."""
    name = "njoy.exe" if sys.platform == "win32" else "njoy"
    path = BIN_DIR / name
    if not path.exists():
        raise FileNotFoundError(
            f"the njoy executable was not found at {path}; the njoy2016 package "
            "may be an incomplete or source-only installation"
        )
    return path


def run(*args, **kwargs):
    """Run ``njoy`` via :func:`subprocess.run`, forwarding all arguments.

    NJOY reads its input from stdin, so a typical call looks like::

        njoy.run(stdin=open("input"), cwd="rundir", check=True)
    """
    import subprocess

    return subprocess.run([os.fspath(executable()), *args], **kwargs)
