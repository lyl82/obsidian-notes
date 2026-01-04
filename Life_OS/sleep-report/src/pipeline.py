from __future__ import annotations

from pathlib import Path
from typing import List

from .collectors.file_collector import collect_entries
from .models import SleepEntry
from .parsers.sleep_parser import SleepParser
from .analyzers.insight_engine import summarize
from .reporters.markdown_renderer import render_report, save_report


def run_pipeline(source_dir: Path, output_path: Path) -> str:
    parser = SleepParser()
    entries: List[SleepEntry] = []
    for path, raw_text in collect_entries(source_dir):
        entries.append(parser.parse(raw_text, path))
    insights = summarize(entries)
    content = render_report(entries, insights)
    save_report(content, output_path)
    return content
