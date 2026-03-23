#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A minimal sandbox-like guard demo for path access."""

from pathlib import Path


class PathAccessGuard:
    """Allow file access only under configured root directories."""

    def __init__(self, allowed_roots: list[Path]) -> None:
        self.allowed_roots = [p.resolve() for p in allowed_roots]

    def validate(self, path: Path) -> None:
        target = path.resolve()
        for root in self.allowed_roots:
            if target == root or root in target.parents:
                return
        raise PermissionError(f"Access denied for path: {target}")

    def safe_read_text(self, path: Path) -> str:
        self.validate(path)
        return path.read_text(encoding="utf-8")


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    data_dir = base / "data"
    data_dir.mkdir(exist_ok=True)
    ok_file = data_dir / "allowed.txt"
    ok_file.write_text("safe content", encoding="utf-8")

    guard = PathAccessGuard(allowed_roots=[data_dir])

    # 1) Allowed path
    content = guard.safe_read_text(ok_file)
    if content == "safe content":
        print("ALLOWED_READ_OK")

    # 2) Blocked path
    try:
        guard.safe_read_text(Path("/etc/hosts"))
    except PermissionError:
        print("BLOCKED_AS_EXPECTED")


if __name__ == "__main__":
    main()
