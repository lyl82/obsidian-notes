# 工作流

## 核心原则

- 增量处理，不全库重编译
- raw 是权威源，不可修改
- wiki 是派生产物，可增量维护
- 优先最小更新，避免覆盖用户手工整理内容
- 处理状态优先由脚本基于元数据判断，不由 AI 自由猜测
- summary / concept / index 输出格式必须遵守固定模板

## 预处理层（未来由脚本执行）

在 AI 读取 raw 之前，先由脚本做一层预处理：

- 读取 raw frontmatter
- 判断 `wiki_status`
- 比对 `wiki_content_hash`
- 筛选真正需要进入 AI 编译阶段的文件

如果脚本判断：
- 已处理
- 且内容无变化

则该 raw 直接跳过，不进入 AI 编译。

## 标准执行流程

### 1. 确认输入范围
- 明确本次处理的是哪几个 raw 文件
- 若用户未明确说明，不自动全量扫库

### 2. 读取上下文
- 读取本次 raw
- 读取相关已有 summary
- 读取相关 concept
- 读取 index 中对应条目
- 读取对应模板文件

### 3. 生成 summary
- 每篇 raw 必须对应一个 summary
- summary 只基于 raw 本身，不引入外部推断
- 若 raw 信息不足，则输出最小 summary
- summary 必须遵守固定模板

### 4. 抽取概念
- 从本次 raw 中抽取可复用、可抽象、可跨文档连接的核心概念
- 判断是：
  - 新建 concept
  - 更新旧 concept
  - 不建 concept，仅留在 summary

### 5. 更新 concept
- 已存在 concept 时优先补充，不优先重写
- 新增内容优先写入：
  - 新定义
  - 新案例
  - 新对比
  - 新来源链接
- concept 必须遵守固定模板

### 6. 补双向链接
- summary 指向相关 concept
- concept 回链相关 summary
- 链接格式统一使用 `[[ @链接]]`

### 7. 更新 index
- 追加新的 summary 入口
- 必要时补充新的 concept 入口
- 不做与本次任务无关的全局整理

### 8. 校验
- 是否每篇 raw 都有 summary
- 是否 concept 更新最小化
- 是否出现非法文件名
- 是否链接目标存在
- 是否存在明显 hallucination 风险

## 降级处理

- 图片型 raw：仅记录可确认元数据与可见主题
- 短引语 raw：通常只生成 summary，不强行新建 concept
- 招聘/通知类 raw：通常不提升为抽象 concept，除非用户明确要求

## 增量更新规则

- 只改动本次 raw 影响到的页面
- 不重写未命中的 concept
- 不主动改旧文件风格，除非本次更新必须触达
- 不因 AI 自己判断“像是处理过”而跳过；跳过逻辑只认脚本状态判断
