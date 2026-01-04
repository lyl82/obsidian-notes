ENTRY_CARD_TEMPLATE = """
### {title}
- **路径**: {path}
- **日期**: {date}
- **背景**: {background}
- **症状**: {symptoms}
- **触发因素**: {triggers}
- **策略**: {strategies}
- **备注**: {notes}
""".strip()

SUMMARY_TEMPLATE = """
## 睡眠记录整合摘要

### 统计洞察
- **高频症状**: {symptoms}
- **共通触发**: {triggers}
- **有效策略**: {strategies}
- **重复背景**: {backgrounds}
- **建议**: {recommendations}

### 记录卡片
{cards}
""".strip()
