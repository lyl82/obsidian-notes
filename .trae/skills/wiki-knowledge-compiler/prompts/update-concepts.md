# Prompt: Update Concepts

你现在负责从本次 raw 与新生成的 summary 中抽取核心概念，并决定 concept 页面如何增量更新。

## 目标

- 判断哪些概念需要新建
- 判断哪些概念只需要更新
- 判断哪些信息不应提升为 concept

## 输入

- 本次 raw 文件内容
- 本次新生成的 summary
- 已有相关 concept 页面
- `templates/concept.template.md`

## 输出要求

- 对每个概念给出判断：
  - 新建
  - 更新
  - 不处理
- 若新建或更新，输出完整可保存的 concept Markdown 内容
- concept 输出结构必须遵守 `concept.template.md`

## 概念筛选原则

优先抽取：
- 可复用
- 可抽象
- 可跨文件链接
- 对未来检索有价值

通常不提升为 concept 的内容：
- 单次招聘信息
- 纯情绪表达
- 页面碎片
- 无法抽象的一次性细节

## 更新原则

1. 已存在页面优先最小更新
2. 不重写与本次 raw 无关的部分
3. 尽量追加新定义、新案例、新来源链接
4. 链接格式统一使用 `[[ @链接]]`

## 输出格式

- 概念判断清单
- 需要新建/更新的目标文件路径
- 对应完整 Markdown 内容
- 若需要脚本落盘，则额外输出一个 manifest（遵守 `docs/manifest-contract.md`）
