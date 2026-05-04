---
type: task
title: ""
action: ""
scheduled_time: ""
done_time:
estimated_duration: 0
actual_duration: 0
status:
  - done
value:
urgency:
cost:
priority_score: 1
purpose_tags: []
project: ""
date: 2026-05-01
---
 - [x] 接入 MiniMax TTS 并完成一次语音播放验收 📅 2026-05-01 ✅ 2026-05-03
来源：[](https://www.bilibili.com/video/BV19aM2zxErG/?spm_id_from=333.1387.favlist.content.click&vd_source=516478c1b7e0b5401d392cbaedc16d7c)
**目标（可交付结果）​**

SillyTavern 已接入 MiniMax TTS，并能让至少 1 张角色卡完成一次文字转语音播放，形成可复用的接入路径记录。

**完成标准（可判断）​**

- [x] 已在 SillyTavern 中配置 MiniMax TTS 所需的接口信息
- [x] 已让至少 1 张角色卡绑定可用语音
- 能在一次实际聊天中播放角色回复语音，并记录接入过程中的痛点或注意事项

**现实动作（按阶段触发，拆分任务步骤）​**

**阶段 1：确认入口**（触发：开始处理该任务）

- 打开 SillyTavern 的 TTS / Extensions 相关设置，确认MiniMax TTS 的配置参数，在音色库选择音色id

**阶段 2：填写配置**（触发：已确认 MiniMax TTS 配置入口）

- 填入 MiniMax TTS 所需的 API 信息，保存配置，并刷新或测试语音列表

**阶段 3：绑定角色语音**（触发：MiniMax TTS 配置已保存且可用）

- 打开任意 1 张已创建角色卡的聊天
- 为该角色选择一个可用语音，并应用 voice map / 语音映射设置

**阶段 4：完成播放验收**（触发：角色已绑定语音）

- 发送一条测试消息，触发角色回复
- 点击语音播放按钮，或开启自动朗读，确认能听到角色语音

**阶段 5：记录痛点笔记**（触发：已完成一次语音播放）

- 记录本次接入中遇到的问题、卡住的位置、有效配置和下次复现步骤



|                |            |
| -------------- | ---------- |
| 非常真实的asmr的日本女声 | 2026-05-03 |
