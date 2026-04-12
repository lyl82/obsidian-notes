---
type: task
title: ""
action: ""
scheduled_time: ""
done_time:
estimated_duration: 0
actual_duration: 0
status: pending
value: 0
urgency: 0
cost: 0
priority_score: 1
purpose_tags: []
project: ""
date: 2026-04-10
---
[[主流大模型API性价比调研任务]]- [ ] 完成 SillyTavern 本体安装、API 接入、角色卡创建与痛点记录 📅 2026-04-17

## 目标（可交付结果）

SillyTavern 在本地稳定运行，已接入可用 API，创建 2 张风格不同的角色卡并完成真实对话，Obsidian 中存有一份结构化的基准体验与痛点笔记。

## 完成标准（可判断）

- [x] 已在本地成功启动 SillyTavern，浏览器界面可正常访问 ✅ 2026-04-10
- [x] 已填入 API Key 并通过连接测试，能收到模型真实回复 ✅ 2026-04-10
- [x] 已创建 2 张角色卡，且两张卡在人格、风格、约束上有明显差异 ✅ 2026-04-10
- [ ] 每张角色卡已完成不少于 10 轮对话，能判断人设是否稳定
- [ ] 已在 Obsidian 记录痛点笔记，包含"顺手之处"与"不顺手之处"各至少 3 条

## 现实动作（下一步具体动作）

1. 打开终端，运行 `git clone https://github.com/SillyTavern/SillyTavern.git` 将项目拉到本地
2. 进入项目目录，Windows 执行 `start.bat`，Mac/Linux 执行 `bash start.sh`，等待依赖安装完成
3. 浏览器访问 `http://localhost:8000`，确认界面正常加载
4. 进入「API 连接」设置，选择提供商（OpenAI 兼容接口），填入已有 API Key，点击「测试连接」直至显示成功
5. 新建第 1 张角色卡：定位为「职业规划顾问」，写入人格描述、说话风格、至少 1 条行为约束，保存
6. 新建第 2 张角色卡：定位为「项目复盘伙伴」，风格与第 1 张明显不同（如更简短、更追问），保存
7. 分别与两张角色卡各对话 10 轮，期间主动测试边界（如话题跳跃、追问矛盾处），观察人设稳定性
8. 在 Obsidian 新建 `AI_System/SillyTavern/阶段0-基准体验.md`，按「顺手 / 不顺手 / 待解决问题」三栏记录真实感受

- [x] 卡在获取角色卡，12:09 ✅ 2026-04-10
- [x] 酒馆是否只是prompt+聊天嘛 ✅ 2026-04-10
更有性格，记忆的聊天，是否可以设置成真实的数字员工呢，角色+skill。
像龙虾那样？