---
title: Summary - Andrej Karpathy 是如何用 LLM 管理知识
created: 2026-04-03
tags:
  - wiki
  - summary
source_file: "[[0_Inbox/Clippings/Andrej Karpathy 是如何用 LLM 管理知识]]"
source_url: "https://x.com/i/grok?conversation=2040056700896792789"
---

## 核心内容
围绕 Andrej Karpathy 分享的一套“用 LLM 作为知识编译器/维护者”的个人知识管理流程：把散乱资料落到 raw/ 目录，再由 LLM 增量编译为结构化 wiki（摘要/概念/双链/索引），用 Obsidian 作为浏览前端；提问时由 LLM 自行查阅 wiki 并输出可复用文件；并通过 linting/health checks 做一致性检查与补全，实现“越用越厚、可自我修复”的循环。

知识库的概念，关联rag，企业，客服知识库管理
## 7步工作流（材料内结构）
1. 数据采集：来源统一进入 raw/。
2. LLM 编译：生成 summaries、concepts、双链与 index。
3. Obsidian 查看：像浏览代码仓库一样浏览与跳转。
4. LLM 问答：对大规模 wiki 提复杂问题，LLM 自行查阅与研究。
5. 输出：产出 .md/幻灯片/图表等文件，而非仅聊天文本。
6. 归档回流：把每次探索输出沉淀回 wiki。
7. 校验（linting）：检查不一致、补缺失、发现新关联，实现自我修复。

## 关键点（材料内强调）
- “编译”是把 raw 输入转为结构化文件系统产物；可版本控制（Git）。
- linting 类比代码 lint：一致性检查、缺失标注、链接与索引修复。
- 可从“纯手动（chat复制粘贴）”起步，再逐步脚本化。

## 关联概念
- [[concepts/知识编译工作流（Karpathy）]]
- [[concepts/AI代理（Agents）]]
- [[concepts/OpenClaw]]
