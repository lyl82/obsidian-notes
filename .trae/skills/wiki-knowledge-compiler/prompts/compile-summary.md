# Prompt: Compile Summary

你现在负责为本次提供的 raw 文件生成 summary 页面。

## 目标

为每个 raw 文件生成一篇完整的 Markdown summary，放入 `wiki/summaries/`。

## 输入

- raw 文件路径
- raw 文件完整内容
- 相关已有 wiki 页面（若存在）
- `templates/summary.template.md`

## 输出要求

- 输出完整可保存的 `.md` 文件内容
- 文件名默认与 raw 同名
- 输出结构必须遵守 `summary.template.md`
- summary 必须包含：
  - frontmatter
  - 核心内容
  - 关键点
  - 关联概念

## 硬规则

1. 只基于本次提供的 raw 内容
2. 不编造缺失信息
3. raw 内容过少时，输出最小 summary
4. 不直接修改 raw
5. 链接格式统一使用 `[[ @链接]]`

## 判断原则

- 若 raw 是长文：提炼主题、结构、关键判断
- 若 raw 是短帖：只保留可确认信息
- 若 raw 主要是图片或页面碎片：说明“信息有限”，不要强行总结

## 输出格式

- 直接输出目标文件路径
- 然后输出完整 Markdown 文件内容
- 若需要脚本落盘，则额外输出一个 manifest（遵守 `docs/manifest-contract.md`）
