"""Seed example data for the 人生OS 1.0 database."""
from __future__ import annotations

import hashlib
from typing import Dict, Iterable, List, Tuple

from database import connect, init_db


EXAMPLE_LOGS: List[str] = [
    "早上 6:30 起床，跑步 3 公里，喝 500ml 水",
    "下午开了 2 小时产品评审会议，感觉能量下降",
    "晚上和父母视频聊天 20 分钟，心情变好",
    "查看余额宝收益 +25.3 元，计划下周调仓",
]

EXAMPLE_RULES: List[Tuple[str, str]] = [
    (
        "健康习惯",
        "'跑步' in content or '喝' in content and '水' in content",
    ),
    (
        "情绪波动",
        "'心情' in content or '能量' in content or '压力' in content",
    ),
    (
        "财务提醒",
        "'余额宝' in content or '收益' in content or '调仓' in content",
    ),
]

EXAMPLE_QUEUE: List[Tuple[str, str]] = [
    ("健康习惯", "new"),
    ("情绪波动", "pending"),
    ("财务提醒", "new"),
]


def _hash_content(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def seed_example() -> Dict[str, int]:
    """Insert deterministic example data and return basic counts."""
    init_db()
    with connect() as conn:
        # Insert logs
        log_hashes = [_hash_content(content) for content in EXAMPLE_LOGS]
        for content, content_hash in zip(EXAMPLE_LOGS, log_hashes):
            conn.execute(
                "INSERT OR IGNORE INTO logs (content, content_hash) VALUES (?, ?)",
                (content, content_hash),
            )

        # Insert rules
        for name, expression in EXAMPLE_RULES:
            conn.execute(
                "INSERT OR IGNORE INTO rules (name, expression) VALUES (?, ?)",
                (name, expression),
            )
        conn.commit()

        # Map content_hash -> log id
        placeholder = ",".join(["?"] * len(log_hashes))
        cursor = conn.execute(
            f"SELECT id, content_hash FROM logs WHERE content_hash IN ({placeholder})",
            log_hashes,
        )
        hash_to_id = {row[1]: row[0] for row in cursor.fetchall()}

        # Refresh queue for a clean MVP view
        conn.execute("DELETE FROM queue")

        # Insert queue rows using first matching log for each rule
        for rule_name, status in EXAMPLE_QUEUE:
            # Pick a deterministic log id for the rule: use the first log
            log_id = hash_to_id[log_hashes[0]]
            conn.execute(
                "INSERT INTO queue (log_id, rule_name, status) VALUES (?, ?, ?)",
                (log_id, rule_name, status),
            )


        conn.commit()

        # Counts for reporting
        log_count = conn.execute("SELECT COUNT(*) FROM logs").fetchone()[0]
        rule_count = conn.execute("SELECT COUNT(*) FROM rules").fetchone()[0]
        queue_count = conn.execute("SELECT COUNT(*) FROM queue").fetchone()[0]

    return {"logs": log_count, "rules": rule_count, "queue": queue_count}


if __name__ == "__main__":
    counts = seed_example()
    print(f"Seeded example data: logs={counts['logs']}, rules={counts['rules']}, queue={counts['queue']}")
