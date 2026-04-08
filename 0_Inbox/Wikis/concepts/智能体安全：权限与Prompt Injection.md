---
title: 智能体安全：权限与Prompt Injection
created: 2026-04-03
tags:
  - wiki
  - concept
  - security
  - ai
  - agent
---

## 问题定义（材料内）
当 Agent 获得文件/终端/邮箱/浏览器等高权限时，风险从“回答错”升级为“执行错/被诱导执行恶意动作”。

## 典型风险面（材料内提法）
- Prompt injection：恶意网页/文本诱导 Agent 泄露信息或执行危险操作。
- 不安全工具使用：权限边界过大、缺乏最小权限与隔离。
- 供应链风险：社区技能/插件可能包含恶意逻辑或敏感信息外泄。
- 数据泄露：Moltbook/Agent 生态被提及出现数据库/令牌/API key 暴露等案例型风险。

## 关键原则（材料内倾向）
- 最小权限、隔离运行、谨慎授予敏感目录/凭证。
- 对“把执行权交给模型”的后果做清晰责任归属与风险自担认知。

## 相关概念
- [[AI代理（Agents）]]
- [[OpenClaw]]
- [[Moltbook（Agent社交实验）]]

## 来源（指向 summaries）
- [[summaries/openclaw的分析报告]]
- [[summaries/Moltbook]]
- [[summaries/Claude Cowork引发SaaS末日恐慌 - Grok]]