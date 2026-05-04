# 任务管理 Base 文件使用说明

## 已创建的 Base 文件

### 1. 完整功能版：`task-management-formulas.base`
**位置**: [Tasks/task-management-formulas.base](file:///d:/个人记录/obsidian-file/wjmber/LifeOS/Tasks/task-management-formulas.base)

**功能特点**:
- 8个计算公式
- 6个不同视图
- 时间跟踪功能
- 紧急程度评分系统
- 完成百分比计算

**包含的公式**:
1. `days_until_due` - 距离截止日期天数
2. `is_overdue` - 是否过期
3. `priority_label` - 优先级标签（带图标）
4. `status_icon` - 状态图标
5. `time_remaining` - 剩余时间
6. `completion_percentage` - 完成百分比
7. `days_since_created` - 创建天数
8. `urgency_score` - 紧急程度评分

**包含的视图**:
1. **Active Tasks by Urgency** - 按紧急程度排序的活动任务
2. **Tasks by Project** - 按项目分组显示
3. **Overdue Tasks** - 过期任务
4. **Completed Tasks** - 已完成任务（限制50条）
5. **Task Cards** - 任务卡片视图
6. **Time Tracking** - 时间跟踪视图

### 2. 简化版：`simple-task-management.base`
**位置**: [Tasks/simple-task-management.base](file:///d:/个人记录/obsidian-file/wjmber/LifeOS/Tasks/simple-task-management.base)

**功能特点**:
- 4个基本公式
- 4个简洁视图
- 适合初学者使用
- 界面简洁明了

**包含的公式**:
1. `days_until_due` - 距离截止日期天数
2. `is_overdue` - 是否过期
3. `priority_label` - 优先级标签（带图标）
4. `status_icon` - 状态图标

**包含的视图**:
1. **All Tasks** - 所有任务
2. **Active Tasks** - 活动任务
3. **Completed Tasks** - 已完成任务（限制30条）
4. **Task Cards** - 任务卡片视图

## 如何在笔记中使用这些 Base 文件

### 嵌入 Base 文件

在 Markdown 笔记中嵌入整个 base 文件：

```markdown
![[task-management-formulas.base]]
```

嵌入特定视图：

```markdown
![[task-management-formulas.base#Active Tasks by Urgency]]
```

### 任务笔记的前置属性要求

为了让 base 文件正确显示任务，您的任务笔记需要包含以下前置属性：

```yaml
---
type: task
status: todo | in-progress | done
priority: 1 | 2 | 3  # 1=高, 2=中, 3=低
due_date: YYYY-MM-DD  # 可选
project: 项目名称  # 可选
time_estimate: 5  # 小时，可选
time_spent: 2  # 小时，可选
---
```

### 示例任务笔记

```markdown
---
type: task
status: in-progress
priority: 1
due_date: 2026-04-20
project: 工作设计系统
time_estimate: 8
time_spent: 3
---

# 完成工作设计系统原型

## 任务描述
创建工作设计系统的原型界面和基本功能。

## 进度
- [x] 需求分析
- [x] 界面设计
- [ ] 功能实现
- [ ] 测试验证
```

## 公式详解

### 1. 日期计算
- `days_until_due`: 计算距离截止日期还有多少天
- `days_since_created`: 计算任务创建了多少天

### 2. 状态判断
- `is_overdue`: 自动判断任务是否过期（截止日期已过且状态不是"done"）

### 3. 可视化标签
- `priority_label`: 将数字优先级转换为带颜色的图标标签
  - 🔴 High (优先级1)
  - 🟡 Medium (优先级2)
  - 🟢 Low (优先级3)
  - ⚪ None (无优先级)

- `status_icon`: 将状态转换为图标
  - ✅ done (已完成)
  - 🔄 in-progress (进行中)
  - 📝 todo (待办)
  - ❓ unknown (未知)

### 4. 时间管理
- `time_remaining`: 计算剩余时间（时间估计 - 已花费时间）
- `completion_percentage`: 计算完成百分比

### 5. 智能评分
- `urgency_score`: 综合评分系统，考虑：
  - 优先级（高=3分，中=2分，低=1分）
  - 是否过期（过期+2分）
  - 距离截止日期≤3天（+1分）

## 视图功能说明

### 表格视图功能
1. **排序**: 支持多列排序
2. **分组**: 可按项目分组显示
3. **筛选**: 每个视图都有独立的筛选条件
4. **汇总**: 显示统计信息（平均值、总和等）
5. **列宽调整**: 可自定义列宽度

### 卡片视图功能
1. **视觉化展示**: 适合快速浏览
2. **卡片大小**: 可调整卡片尺寸
3. **图片比例**: 支持设置图片宽高比

## 使用建议

### 新手建议
1. 从 `simple-task-management.base` 开始
2. 先掌握基本的前置属性设置
3. 逐步尝试不同的视图

### 进阶使用
1. 使用 `task-management-formulas.base` 的完整功能
2. 利用时间跟踪功能管理工时
3. 根据紧急程度评分安排任务优先级

### 自定义调整
1. 可以修改 base 文件中的公式
2. 可以调整视图的筛选条件
3. 可以添加新的视图

## 常见问题

### Q: 为什么我的任务没有显示在 base 中？
A: 请检查：
1. 笔记是否包含 `type: task` 前置属性
2. 笔记文件扩展名是否为 `.md`
3. 是否在 base 文件的筛选范围内

### Q: 日期计算不正确怎么办？
A: 请确保 `due_date` 属性的格式为 `YYYY-MM-DD`

### Q: 如何添加新的计算公式？
A: 在 `formulas` 部分添加新的公式，例如：
```yaml
formulas:
  我的新公式: 'if(priority == 1, "紧急", "普通")'
```

## 更新日志

### 2026-04-17
- 创建了两个任务管理 base 文件
- 完整功能版包含8个公式和6个视图
- 简化版包含4个公式和4个视图
- 编写了详细的使用说明文档