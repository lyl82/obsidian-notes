# Raw 元数据契约

## 目的

为了提高 AI 使用效率，raw 文件的“是否需要处理”应优先由脚本根据元数据判断，而不是让 AI 用 token 逐篇理解后再猜测。

## 推荐字段

建议在 raw 文件 frontmatter 中逐步引入以下字段：

```yaml
wiki_status: pending
wiki_summary: false
wiki_concepts: []
wiki_last_compiled:
wiki_content_hash:
```

兼容字段：

```yaml
wiki-tags: pending
```

当前兼容策略：
- 脚本优先读取 `wiki_status`
- 若不存在 `wiki_status`，则回退读取 `wiki-tags`
- `wiki-tags` 的值会做 trim 和小写归一化，因此 `" pending"` 也会被识别为 `pending`

## 字段说明

### wiki_status
- `pending`：从未处理
- `done`：已处理且当前版本有效
- `stale`：曾处理过，但 raw 内容已变化，需要重新编译
- `skipped`：明确跳过，不进入编译
- 推荐作为长期主字段

### wiki-tags
- 兼容字段，可暂时承载与处理状态相关的单值
- 当前脚本会把它当作 `wiki_status` 的回退来源
- 若未来需要真正的多标签语义，建议把处理状态迁移回 `wiki_status`

### wiki_summary
- 是否已生成 summary

### wiki_concepts
- 当前 raw 已关联的 concept 名称列表

### wiki_last_compiled
- 最近一次编译时间

### wiki_content_hash
- 记录 raw 内容摘要，用于脚本判断是否变更
- 计算时应忽略所有 `wiki_*` 字段以及 `wiki-tags`，避免因状态回写导致 hash 自我变化

## 判定逻辑

- 若归一化后的状态为 `done` 且 `wiki_content_hash` 未变化 → 跳过
- 若 hash 变化 → 标记为 `stale`
- 若状态为 `pending` 或 `stale` → 进入本次编译队列

## 责任边界

- 脚本负责：
  - 读取元数据
  - 比对 hash
  - 决定是否跳过
- AI 负责：
  - 只处理脚本筛选后的输入
  - 不自行猜测跳过状态

## 注意

- v0.1 先定义契约，不强制立即改所有 raw
- 后续可从新增 raw 开始逐步引入这些字段
