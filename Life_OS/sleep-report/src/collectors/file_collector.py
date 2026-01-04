from __future__ import annotations

from pathlib import Path
from typing import Iterable, List


def iter_markdown_files(root: Path) -> Iterable[Path]:
    root = root.expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Directory not found: {root}")
    for path in sorted(root.glob("**/*.md")):
        if path.is_file():
            yield path


def read_entry(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def collect_entries(root: Path) -> List[tuple[Path, str]]:
    return [(path, read_entry(path)) for path in iter_markdown_files(root)]
