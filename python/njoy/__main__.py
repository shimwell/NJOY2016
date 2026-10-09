"""Console-script entry point: exec the bundled njoy executable."""

import os
import sys

from . import executable


def main() -> int:
    exe = os.fspath(executable())
    if hasattr(os, "execv"):
        os.execv(exe, [exe, *sys.argv[1:]])
    import subprocess  # pragma: no cover - Windows fallback

    return subprocess.run([exe, *sys.argv[1:]]).returncode


if __name__ == "__main__":
    raise SystemExit(main())
