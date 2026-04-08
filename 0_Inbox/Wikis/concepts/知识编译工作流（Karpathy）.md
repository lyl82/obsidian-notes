---
title: 知识编译工作流（Karpathy）
created: 2026-04-03
tags:
  - wiki
  - concept
  - knowledge-management
  - llm
---

## 核心想法（材料内）
把 LLM 从“聊天工具”升级为“知识编译器 + 维护者 + 查询引擎”：对原始资料做增量编译，产出结构化 Markdown wiki，并用 linting 做健康检查与自我修复。

## 工作流结构（raw → wiki → query → artifacts → feedback）
- raw/：存放权威原始资料（不改动）。
- wiki/：由 LLM 生成的派生结构（summary、concept、双向链接、index）。
- query：提问时由 LLM 自行查阅 wiki 并研究。
- artifacts：输出可复用文件（.md、幻灯片、图表等）。
- feedback：输出回流 + linting，让知识库“越查越厚、越用越一致”。

## LLM linting（材料内定义）
类比代码 lint 工具：对 wiki 做健康检查，找不一致、缺失、可新增链接与概念页，并输出需要修复/新增的完整 .md 文件内容。

## 相关概念
- [[AI代理（Agents）]]
- [[OpenClaw]]
- [[智能体安全：权限与Prompt Injection]]

## 来源（指向 summaries）
- [[summaries/Andrej Karpathy 是如何用 LLM 管理知识]]
