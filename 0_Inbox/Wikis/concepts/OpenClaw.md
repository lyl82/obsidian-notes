---
title: OpenClaw
created: 2026-04-03
tags:
  - wiki
  - concept
  - ai
  - agent
---

## 定义（来自材料）
OpenClaw 被描述为“本地优先/可自托管的个人 AI 智能体平台”，通过常见聊天软件作为界面，驱动后台工具执行（文件、终端、浏览器、邮件、日历等），并具备技能（Skills）生态与长期运行能力。

## 关键结构
- 接入层：多聊天渠道（IM）作为前端。
- Agent/Reasoning：调用大模型规划与决定工具使用。
- 执行层：真实工具（shell、文件、浏览器等）。
- 记忆/会话：跨会话上下文与偏好沉淀。

## 关键差异（相对“AI编辑器”）
材料内的区分强调：AI 编辑器偏“你在电脑前同步协作”；OpenClaw偏“你把任务异步扔给后台，它自己跑，手机验收结果”。

## 主要风险（材料内）
- 权限过大与 prompt injection 风险被反复强调。
- 社区技能质量参差与潜在恶意技能。

## 相关概念
- [[AI代理（Agents）]]
- [[知识编译工作流（Karpathy）]]
- [[智能体安全：权限与Prompt Injection]]
- [[Moltbook（Agent社交实验）]]

## 来源（指向 summaries）
- [[summaries/openclaw的分析报告]]
- [[summaries/Moltbook]]
- [[summaries/Andrej Karpathy 是如何用 LLM 管理知识]]
