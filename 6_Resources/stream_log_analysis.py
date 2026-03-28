import csv
import sys
from collections import defaultdict
from datetime import datetime


def parse_datetime(value):
    if not value:
        return None
    value = value.strip()
    if not value:
        return None
    for fmt in ("%Y/%m/%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def to_minutes(value):
    if value is None:
        return 0.0
    text = str(value).strip()
    if not text:
        return 0.0
    try:
        return float(text)
    except ValueError:
        return 0.0


def classify_record(title, log_text, done_text, doing_text, object_tag):
    text_parts = [title or "", log_text or "", done_text or "", doing_text or "", object_tag or ""]
    text = " ".join(text_parts)
    if any(key in text for key in ["投递简历", "投简历", "简历", "面试", "自我介绍", "口头表达"]):
        return "求职与面试"
    if any(key in text for key in ["锻炼", "引体", "深蹲", "骑行", "跑步", "拳击"]):
        return "锻炼与身体活动"
    if any(key in text for key in ["学习", "发散思考", "思维", "复盘", "蓝图", "管理"]):
        return "思考与学习"
    if any(key in text for key in ["游戏", "脱口秀", "看视频", "citywalk"]):
        return "娱乐与体验"
    if any(key in text for key in ["物理移动", "吃饭", "通勤"]):
        return "生活与物理移动"
    return "模糊或未定义"


def analyze(csv_path):
    records = []
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            start_raw = row.get("初时间")
            end_raw = row.get("完成时间")
            duration_raw = row.get("持续时间（整数）")
            title = row.get("标题")
            log_text = row.get("log描述")
            done_text = row.get("done描述")
            doing_text = row.get("doing 描述")
            object_tag = row.get("对象标签")
            start_time = parse_datetime(start_raw)
            end_time = parse_datetime(end_raw)
            duration_minutes = to_minutes(duration_raw)
            if duration_minutes <= 0 and start_time and end_time:
                delta = end_time - start_time
                duration_minutes = delta.total_seconds() / 60.0
            date = start_time.date() if start_time else None
            category = classify_record(title, log_text, done_text, doing_text, object_tag)
            records.append(
                {
                    "start_time": start_time,
                    "end_time": end_time,
                    "date": date,
                    "duration_minutes": max(duration_minutes, 0.0),
                    "title": title or "",
                    "log_text": log_text or "",
                    "done_text": done_text or "",
                    "doing_text": doing_text or "",
                    "object_tag": object_tag or "",
                    "category": category,
                }
            )
    if not records:
        print("没有读取到任何记录。")
        return
    total_minutes = sum(r["duration_minutes"] for r in records)
    dates = [r["date"] for r in records if r["date"] is not None]
    day_count = len(set(dates)) if dates else 0
    by_date = defaultdict(float)
    by_title = defaultdict(float)
    by_object_tag = defaultdict(float)
    by_category = defaultdict(float)
    empty_meaning_minutes = 0.0
    empty_meaning_count = 0
    for r in records:
        minutes = r["duration_minutes"]
        if r["date"]:
            by_date[r["date"]] += minutes
        if r["title"]:
            by_title[r["title"]] += minutes
        if r["object_tag"]:
            by_object_tag[r["object_tag"]] += minutes
        by_category[r["category"]] += minutes
        if not r["title"] and not r["log_text"] and not r["done_text"] and not r["doing_text"]:
            empty_meaning_minutes += minutes
            empty_meaning_count += 1
    print("=== 时间流日志分析结果 ===")
    print(f"记录条数: {len(records)}")
    print(f"总时长: {total_minutes:.1f} 分钟 ≈ {total_minutes/60.0:.2f} 小时")
    if day_count > 0:
        print(f"覆盖天数: {day_count} 天")
        print(f"平均每天记录时长: {total_minutes/day_count:.1f} 分钟 ≈ {total_minutes/60.0/day_count:.2f} 小时")
    print()
    print("按行动类别统计:")
    for category, minutes in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
        ratio = minutes / total_minutes * 100 if total_minutes > 0 else 0
        print(f"- {category}: {minutes:.1f} 分钟 ({ratio:.1f}%)")
    print()
    print("按对象标签统计（前 10 项）:")
    sorted_tags = sorted(by_object_tag.items(), key=lambda x: x[1], reverse=True)
    for tag, minutes in sorted_tags[:10]:
        print(f"- {tag or '（空）'}: {minutes:.1f} 分钟")
    print()
    print("按标题统计（前 10 项）:")
    sorted_titles = sorted(by_title.items(), key=lambda x: x[1], reverse=True)
    for title, minutes in sorted_titles[:10]:
        print(f"- {title or '（空）'}: {minutes:.1f} 分钟")
    print()
    print("记录质量概览:")
    print(f"- 描述完全为空的记录: {empty_meaning_count} 条, 合计 {empty_meaning_minutes:.1f} 分钟")


def main():
    if len(sys.argv) < 2:
        print("用法: python stream_log_analysis.py <csv文件路径>")
        return
    csv_path = sys.argv[1]
    analyze(csv_path)


if __name__ == "__main__":
    main()

