import re
from os import PathLike
from pathlib import Path
from platform import system


def libmf6_version(mf6) -> tuple[int, int, int]:
    """Return the libmf6 version as a tuple of integers. Ex. (6, 8, 2)"""
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", mf6.get_version())
    return tuple(int(i) for i in match.groups())


def amend_libmf6_path(path: str | PathLike) -> str:
    ext = Path(path).suffix
    path = str(path)
    os = system().lower()
    if os == "windows":
        if not ext:
            path += ".dll"
        path = str(Path(path).absolute())
    elif os == "linux":
        if not ext:
            path += ".so"
        if not path.startswith("./"):
            if not path.startswith("/"):
                path = "./" + path
    elif os == "darwin" and not ext:
        path += ".dylib"
    return path


def is_exg(pkg_type: str):
    parts = pkg_type.split("-")
    return len(parts) == 2 and parts[0] == parts[1]
