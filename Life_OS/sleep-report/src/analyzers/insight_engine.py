from __future__ import annotations

from collections import Counter
from typing import Iterable

from ..models import InsightSummary, SleepEntry


def summarize(entries: Iterable[SleepEntry]) -> InsightSummary:
    symptom_counter: Counter[str] = Counter()
    trigger_counter: Counter[str] = Counter()
    strategy_counter: Counter[str] = Counter()
    background_counter: Counter[str] = Counter()

    for entry in entries:
        symptom_counter.update(entry.symptoms)
        trigger_counter.update(entry.triggers)
        strategy_counter.update(entry.strategies)
        background_counter.update(entry.background)

    recommendations = _build_recommendations(symptom_counter, trigger_counter, strategy_counter)

    return InsightSummary(
        frequent_symptoms=dict(symptom_counter.most_common(10)),
        common_triggers=dict(trigger_counter.most_common(10)),
        effective_strategies=dict(strategy_counter.most_common(10)),
        recurring_backgrounds=dict(background_counter.most_common(10)),
        recommendations=recommendations,
    )


def _build_recommendations(
    symptoms: Counter[str],
    triggers: Counter[str],
    strategies: Counter[str],
) -> list[str]:
    recommendations: list[str] = []
    if symptoms:
        top_symptom, _ = symptoms.most_common(1)[0]
        recommendations.append(f"优先聚焦高频症状：{top_symptom}")
    if triggers:
        top_trigger, _ = triggers.most_common(1)[0]
        recommendations.append(f"排查常见触发因素：{top_trigger}")
    if strategies:
        top_strategy, _ = strategies.most_common(1)[0]
        recommendations.append(f"首选有效策略：{top_strategy}")
    return recommendations
