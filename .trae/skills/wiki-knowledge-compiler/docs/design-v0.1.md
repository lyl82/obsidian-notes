# Wiki Knowledge Compiler 设计稿 v0.3

## 目标

构建一个可以被 AI 在对话中直接调用的技能，用于把 `Clippings/` 中本次提供的 raw 文件，增量编译到 `Wikis/` 中。

## 本版实现范围

- 已完成：
  - Skill 名称与职责边界
  - Skill 目录结构
  - Prompt 模板文件
  - 输出模板文件
  - 流程文档
  - 脚本职责规划
  - 第一批脚本原型
  - 第二批脚本原型
  - `SKILL.md`
- 未完成：
  - 状态回写保护
  - 全量 lint 自动化
  - 完整批处理闭环

## 适用对象

- 未来的自己
- 上下文理解有限的 AI
- 重复执行同类任务的执行者

## Skill 名称

- `wiki-knowledge-compiler`

## 目录结构

```text
.trae/skills/wiki-knowledge-compiler/
├─ SKILL.md
├─ docs/
│  ├─ design-v0.1.md
│  ├─ metadata-contract.md
│  ├─ workflow.md
│  └─ script-plan.md
├─ scripts/
│  ├─ common.ps1
│  ├─ normalize-names.ps1
│  ├─ scan-inputs.ps1
│  ├─ detect-existing-pages.ps1
│  ├─ apply-changes.ps1
│  └─ validate-wiki.ps1
├─ templates/
│  ├─ summary.template.md
│  ├─ concept.template.md
│  └─ index.template.md
└─ prompts/
   ├─ compile-summary.md
   ├─ update-concepts.md
   ├─ update-index.md
   └─ lint-wiki.md
```

## 模块职责

### SKILL.md
- 定义调用时机
- 规定输入输出契约
- 规定硬规则与主流程

### prompts/
- 把复杂任务拆成稳定子任务
- 降低 AI 对长上下文的依赖
- 保证不同批次编译的输出风格尽量一致

### templates/
- 固定 summary / concept / index 的输出格式
- 让后续格式调整只需改模板，不必重写所有 prompt
- 让 AI 输出更稳定，方便脚本落盘

### docs/
- 沉淀人类可复盘的设计说明
- 固定增量编译逻辑
- 明确未来脚本应承担的职责
- 明确 raw 元数据如何支持“已处理跳过”

### scripts/
- 用 PowerShell 实现第一批零依赖原型，适配当前 Windows 环境
- 在 AI 编译前完成状态筛选、命名规范化、已有页面探测
- 在 AI 输出后完成变更写入与 wiki 结构校验
- 输出 JSON，供后续 AI 或脚本链路继续消费

## v0.1 的工作假设

- 不追求一次做出最终版
- 先建立“稳定调用接口 + 明确工作流 + 可迭代文档”
- 脚本稍后接入，不阻塞技能定义
- 处理状态判断最终交给脚本，不交给 AI 用 token 逐篇判断
- 输出文档结构必须模板化，不能每次自由发挥

## 处理状态设计（预留给脚本）

raw 文件未来可通过 frontmatter 增加状态字段，例如：

```yaml
wiki_status: pending
wiki_summary: false
wiki_concepts: []
wiki_last_compiled:
wiki_content_hash:
```

设计意图：
- `wiki_status`：标识待处理、已处理、跳过等状态
- `wiki_summary`：是否已生成 summary
- `wiki_concepts`：本 raw 已关联的 concept 列表
- `wiki_last_compiled`：最后编译时间
- `wiki_content_hash`：用于判断内容是否变化

规则：
- 若脚本检测到 `wiki_status=done` 且 `wiki_content_hash` 未变化，则直接跳过
- AI 不负责判断“要不要跳过”，AI 只处理脚本交给它的输入
- 当前兼容 `wiki-tags` 作为回退状态字段，便于先从现有属性体系接入

## 未来迭代方向

- v0.4：加入自动 lint、变更检测与回写保护
- v0.5：加入状态回写与 manifest 串联
- v0.6：形成稳定的“用户给 raw → AI 调 Skill → 脚本辅助落盘”闭环
