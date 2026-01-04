from pathlib import Path

from ..parsers.sleep_parser import SleepParser


def test_parser_extracts_fields(tmp_path: Path) -> None:
    content = """
    # 2025-02-18
    背景：过去长期熬夜。
    症状：白天衰弱。
    原因：咖啡过量。
    策略：减少屏幕时间。
    其他备注。
    """.strip()
    file_path = tmp_path / "sample.md"
    file_path.write_text(content, encoding="utf-8")

    parser = SleepParser()
    entry = parser.parse(content, file_path)

    assert "过去长期熬夜" in entry.background[0]
    assert "白天衰弱" in entry.symptoms[0]
    assert "咖啡过量" in entry.triggers[0]
    assert entry.date == "2025-02-18"
