from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass(slots=True)
class SleepEntry:
    title: str
    path: Path
    date: Optional[str]
    background: List[str] = field(default_factory=list)
    symptoms: List[str] = field(default_factory=list)
    triggers: List[str] = field(default_factory=list)
    strategies: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)


@dataclass(slots=True)
class InsightSummary:
    frequent_symptoms: Dict[str, int]
    common_triggers: Dict[str, int]
    effective_strategies: Dict[str, int]
    recurring_backgrounds: Dict[str, int]
    recommendations: List[str]
