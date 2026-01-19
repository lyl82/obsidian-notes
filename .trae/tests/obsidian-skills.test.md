# obsidian-skills 实例测试

## 目的
- 验证 obsidian-skills 技能入口是否可用
- 在未接入仓库内容与已接入两种情形下，均能给出合理的行为与输出

## 前置条件
- 技能入口存在：`.trae/skills/obsidian-skills/SKILL.md`
- 可选：若已下载仓库内容，请将 `obsidian-skills/skills` 复制到 `LifeOS/skills/obsidian-skills`

## 测试用例 A（本地未接入 skills）
1. 请求：基于 obsidian-skills，生成“心身恢复认知库_v0.1”的导读与练习清单骨架（总导航、版本说明、FAQ、更新机制）
2. 期望：
   - 给出下载与接入 `skills` 的路径指引
   - 同时生成一个合理的导读与练习清单骨架（不依赖本地技能内容）

## 测试用例 B（本地已接入 skills）
1. 请求：从 `skills/obsidian-skills` 中检索与“Daily Practice / Recovery”相关的技能条目，并生成 7 天练习计划（含每日目标与检查项）
2. 期望：
   - 能读取本地 `skills/obsidian-skills` 并引用相关技能名称/片段
   - 输出结构化的 7 天练习计划

## 示例输出（用于快速自检）

### 用例 A 的示例输出
- 接入指引：
  - 浏览器下载 ZIP：`https://github.com/kepano/obsidian-skills` → Code → Download ZIP → 复制 `skills` 子目录到 `LifeOS/skills/obsidian-skills`
  - 终端方式：`git clone` 后复制 `obsidian-skills\skills\*` 到 `LifeOS\skills\obsidian-skills`
- 导读与练习清单骨架：
  - 总导航：主题索引、关键术语、核心路径（入门→实践→进阶）
  - 版本说明：v0.1 目标、适用范围、更新频率
  - FAQ：常见问题（如何开始、每天做什么、如何评估变化）
  - 更新机制：按用户高频问题迭代，双周同步变更
  - 每日练习模板（示例）：目标、练习内容、时长、反馈、下一步

### 用例 B 的示例输出（当本地已接入）
- 引用来源：从 `skills/obsidian-skills` 读取与“Recovery/Daily Practice”相关的技能条目
- 7 天计划（示例结构）：
  - Day 1：轻量唤醒（步行 20 分钟）｜睡眠记录｜主观能量 1-5
  - Day 2：呼吸练习 10 分钟｜轻阻力训练｜睡眠优化检查
  - Day 3：专注训练 15 分钟｜恢复日记｜饮食水化检查
  - Day 4：社交互动任务｜冥想 10 分钟｜能量评分
  - Day 5：有氧 30 分钟｜恢复反馈复盘｜调整下一周目标
  - Day 6：主动放松日｜阅读导读文章｜整理 FAQ
  - Day 7：总结仪式｜更新机制记录｜评估进步与问题清单

