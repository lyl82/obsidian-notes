---
name: "wiki-knowledge-compiler"
description: "Compiles provided raw knowledge files into incremental wiki summaries, concepts, links, and index updates. Invoke when user provides new source files and asks to compile or maintain the wiki."
---

# Wiki Knowledge Compiler

- 作用：把用户本次提供的 raw 资料，增量编译到 `0_Inbox/Wikis/`
- 调用时机：当用户提供新的 Clippings/raw 文件，并要求生成或更新 summary、concept、双向链接、index 时调用
- 当前版本：v0.4（260404）
- 当前边界：已完成模板化输出、manifest 契约、scan/apply/validate、log 追加与 raw 状态回写原型；尚未实现基于 AI 自动产出 manifest 的完整闭环与回写保护策略

## 目标

- 基于用户本次提供的 raw 文件，增量维护结构化 wiki
- 同时兼顾：
  - 人类可复盘
  - 弱 AI 可执行
  - 后续可持续迭代

## 输入契约

- 用户明确提供的 raw 文件路径、文件内容，或指定的本次处理范围
- raw 目录默认是：`d:\个人记录\obsidian-file\wjmber\LifeOS\0_Inbox\Clippings`
- wiki 目录默认是：`d:\个人记录\obsidian-file\wjmber\LifeOS\0_Inbox\Wikis`
- 未来脚本应优先基于 raw 的 frontmatter 元数据判断是否需要处理，而不是让 AI 用 token 逐篇猜测状态
- 当前元数据状态字段优先使用 `wiki_status`，同时兼容你新增的 `wiki-tags`

## 输出契约

- 为每篇 raw 生成或更新一篇 `summaries/<raw同名>.md`
- 创建或最小更新相关 `concepts/<概念名>.md`
- 在相关页面之间添加双向链接 `[[ @链接]]`
- 更新 `index.md`
- 输出必须是完整、可直接保存的 Markdown 文件内容
- summary 与 concept 必须遵守固定模板，便于后续统一调整

## 硬规则

1. 不修改 raw 文件
2. 每次只处理用户本次提供的文件
3. 不编造未在 raw 中出现的信息
4. 已存在页面优先最小修改，不做无边界重写
5. 文件名必须兼容 Windows 非法字符规则
6. 旧页面若有用户手工修改痕迹，优先追加与局部修正，不整体覆盖
7. 未来若 raw frontmatter 明确标记“已处理且未变更”，脚本应跳过，不再调用 AI 编译

## 标准流程

1. 确认本次 raw 输入范围
2. 读取相关 raw 与现有 wiki 页面
3. 生成或更新 summary
4. 抽取核心概念并判断：
   - 新建 concept
   - 更新已有 concept
   - 仅保留在 summary，不升级为 concept
5. 补充双向链接
6. 更新 index
7. 运行一次 lint/校验
8. 输出本次需要创建或更新的完整 Markdown 文件

## Prompt 组件

- `prompts/compile-summary.md`
- `prompts/update-concepts.md`
- `prompts/update-index.md`
- `prompts/lint-wiki.md`

## 脚本组件

- `scripts/common.ps1`
- `scripts/normalize-names.ps1`
- `scripts/scan-inputs.ps1`
- `scripts/detect-existing-pages.ps1`
- `scripts/apply-changes.ps1`
- `scripts/validate-wiki.ps1`
- `scripts/append-log.ps1`
- `scripts/run-ingest.ps1`
- `scripts/update-raw-status.ps1`

## 模板组件

- `templates/summary.template.md`
- `templates/concept.template.md`
- `templates/index.template.md`
- `templates/log.template.md`

## 流程文档

- `docs/design-v0.1.md`
- `docs/workflow.md`
- `docs/script-plan.md`
- `docs/metadata-contract.md`
- `docs/log-contract.md`
- `docs/manifest-contract.md`

## 使用原则

- 若用户只是讨论规则、结构、规范，则优先读取并遵循本技能文档，不直接写 wiki
- 若用户明确给出新 raw 并要求“已编译”，则按流程产出 summary / concept / index 变更
- 若遇到信息不足、主要为图片、或无法可靠抽象概念时，降级为最小 summary，不强行扩展
