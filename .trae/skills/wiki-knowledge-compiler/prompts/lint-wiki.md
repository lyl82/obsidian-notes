# Prompt: Lint Wiki

你现在负责对本次改动后的 wiki 做一次健康检查。

## 目标

检查本次变更是否满足结构、链接、最小更新和反 hallucination 约束。

## 检查项

### 1. Summary 完整性
- 每篇 raw 是否对应一个 summary
- summary 是否完整可保存

### 2. Concept 合理性
- concept 是否只在必要时创建
- 已有 concept 是否遵守最小更新原则

### 3. Link 完整性
- summary 是否回链相关 concept
- concept 是否回链相关 summary
- index 是否包含本次新增入口

### 4. 命名合法性
- 文件名是否包含 Windows 非法字符
- 标题与文件名是否存在明显冲突

### 5. 内容边界
- 是否出现超出 raw 的推断
- 是否有不必要扩写

### 6. 模板一致性
- summary 是否符合 `summary.template.md`
- concept 是否符合 `concept.template.md`
- index 是否符合 `index.template.md`

## 输出要求

- 输出 lint 报告
- 若发现问题，列出需要修复的文件
- 若可直接修复，则输出修复后的完整 Markdown 内容
- 不负责决定 raw 是否跳过；跳过逻辑由脚本依据元数据处理
- 若需要给脚本落盘，则额外输出一个 manifest（遵守 `docs/manifest-contract.md`）
