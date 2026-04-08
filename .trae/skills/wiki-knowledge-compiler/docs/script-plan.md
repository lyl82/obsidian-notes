# 脚本职责规划

当前版本已实现第一批脚本原型，并继续定义后续脚本模块的职责边界。

## 目标

把机械重复、容易出错、适合程序处理的工作，从 AI 判断中拆出来，交给脚本。

## 计划中的脚本模块

### 1. scan-inputs
- 扫描本次用户指定的 raw 文件
- 读取文件路径、扩展名、基础元信息
- 生成本次任务的输入清单
- 解析 raw frontmatter 中的处理状态字段
- 当前状态：已实现原型

### 2. detect-existing-pages
- 检查 `Wikis/summaries/` 是否已有同名 summary
- 检查 `Wikis/concepts/` 是否已有候选 concept
- 检查 `index.md` 是否已有入口
- 结合 raw 状态字段判断是否需要跳过
- 当前状态：已实现原型

### 3. normalize-names
- 把概念标题转换成 Windows 安全文件名
- 解决非法字符问题
- 建立“标题名 ↔ 文件名”的映射
- 当前状态：已实现原型

### 4. plan-changes
- 生成本次待创建/待更新文件列表
- 标记哪些是新建，哪些是局部更新
- 为 AI 输出提供结构化变更计划
- 为每个文件指定使用的模板类型

### 5. apply-changes
- 把 AI 产出的完整 Markdown 内容写入目标路径
- 在写入前做备份或差异检查
- 尽量避免误覆盖已有人工内容
- 当前状态：已实现原型

### 6. validate-wiki
- 检查 summary 是否齐全
- 检查 concept 链接是否存在
- 检查 index 是否已补入口
- 检查文件名是否合法
- 检查输出是否符合模板结构
- 当前状态：已实现原型

## 推荐的 raw 元数据字段

建议未来 raw frontmatter 支持：

- `wiki_status`
- `wiki_summary`
- `wiki_concepts`
- `wiki_last_compiled`
- `wiki_content_hash`

建议语义：
- `wiki_status: pending | done | skipped | stale`
- `wiki_summary: true | false`
- `wiki_concepts: [概念1, 概念2]`

## 推荐的脚本判定顺序

1. 读取 raw frontmatter
2. 计算当前内容 hash
3. 比对 `wiki_content_hash`
4. 若 `wiki_status=done` 且 hash 未变化，则跳过
5. 若 hash 变化，则标记为 `stale`
6. 只有 `pending` 或 `stale` 文件进入 AI 编译阶段

## 脚本与 AI 的职责边界

### AI 负责
- 理解 raw 内容
- 抽取概念
- 生成 Markdown 内容
- 决定链接关系

### 脚本负责
- 扫描与定位文件
- 命名规范化
- 变更计划结构化
- 文件写入与校验
- 状态判断与跳过逻辑

## 下一步接入顺序

1. 把 `apply-changes` 接入变更 manifest 生成链路
2. 把 `validate-wiki` 结果接入回写保护
3. 加入 raw 状态自动回写
4. 形成完整批处理闭环
