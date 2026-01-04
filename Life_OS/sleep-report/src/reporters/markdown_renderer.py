from __future__ import annotations

from pathlib import Path
from typing import Iterable

from ..models import InsightSummary, SleepEntry
from .templates import ENTRY_CARD_TEMPLATE, SUMMARY_TEMPLATE


def _join_list(items: Iterable[str]) -> str:
    filtered = [item.strip() for item in items if item.strip()]
    return "；".join(filtered) if filtered else "-"


def render_entry(entry: SleepEntry) -> str:
    return ENTRY_CARD_TEMPLATE.format(
        title=entry.title,
        path=entry.path,
        date=entry.date or "-",
        background=_join_list(entry.background),
        symptoms=_join_list(entry.symptoms),
        triggers=_join_list(entry.triggers),
        strategies=_join_list(entry.strategies),
        notes=_join_list(entry.notes),
    )


def render_report(entries: list[SleepEntry], insights: InsightSummary) -> str:
    cards = "\n\n".join(render_entry(entry) for entry in entries)
    return SUMMARY_TEMPLATE.format(
        symptoms=_join_dict(insights.frequent_symptoms),
        triggers=_join_dict(insights.common_triggers),
        strategies=_join_dict(insights.effective_strategies),
        backgrounds=_join_dict(insights.recurring_backgrounds),
        recommendations=_join_list(insights.recommendations),
        cards=cards,
    )


def save_report(content: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")


def _join_dict(data: dict[str, int]) -> str:
    if not data:
        return "-"
    return "；".join(f"{key}×{value}" for key, value in data.items())
