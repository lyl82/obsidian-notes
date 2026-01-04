from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pipeline import run_pipeline  # noqa: E402


def main() -> None:
    source_dir = Path("D:/个人记录/obsidian-file/wjmber/tasks/需求/人生OS/3_Domains/Health/睡眠-非结构dao")
    output_path = ROOT / "output" / "sleep_report.md"
    content = run_pipeline(source_dir, output_path)
    print(f"生成报告: {output_path}")
    print(content[:500])


if __name__ == "__main__":
    main()
