from __future__ import annotations

import re
from dataclasses import asdict
from pathlib import Path
from typing import Iterable, List

from ..models import SleepEntry

DATE_PATTERN = re.compile(r"(?P<date>\d{1,2}[\-/]\d{1,2}|\d{4}[\-/]\d{1,2}[\-/]\d{1,2})")
SENTENCE_SPLIT = re.compile(r"[\n。！？!?]")

KEYWORDS = {
    "background": ["背景", "经历", "成长", "童年", "个人", "历史"],
    "symptoms": ["症状", "感受", "疲劳", "困", "衰弱", "不适", "状态", "脑雾"],
    "triggers": ["原因", "触发", "因为", "导致", "诱因", "偶尔"],
    "strategies": ["策略", "能做", "可以", "方案", "改善", "计划", "练习", "建议", "目标"],
}


class SleepParser:
    """将非结构化文本映射为 SleepEntry."""

    def __init__(self) -> None:
        self._compiled_keywords = {
            field: [re.compile(re.escape(word)) for word in words]
            for field, words in KEYWORDS.items()
        }

    def parse(self, text: str, source: Path) -> SleepEntry:
        sentences = self._tokenize(text)
        entry = SleepEntry(
            title=source.stem,
            path=source,
            date=self._extract_date(text),
        )
        for sentence in sentences:
            field = self._classify(sentence)
            if field:
                getattr(entry, field).append(sentence.strip())
            else:
                entry.notes.append(sentence.strip())
        entry.notes = [note for note in entry.notes if note]
        return entry

    def _tokenize(self, text: str) -> List[str]:
        raw_sentences = SENTENCE_SPLIT.split(text)
        cleaned = [sentence.strip() for sentence in raw_sentences if sentence.strip()]
        return cleaned

    def _classify(self, sentence: str) -> str | None:
        for field, patterns in self._compiled_keywords.items():
            if any(pattern.search(sentence) for pattern in patterns):
                return field
        return None

    def _extract_date(self, text: str) -> str | None:
        match = DATE_PATTERN.search(text)
        if match:
            return match.group("date")
        return None


def as_dict(entry: SleepEntry) -> dict:
    data = asdict(entry)
    data["path"] = str(data["path"])
    return data
