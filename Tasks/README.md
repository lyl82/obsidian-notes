# 任务管理系统

## 快速开始

### 1. 选择 Base 文件
- **完整功能版**: [task-management-formulas.base](file:///d:/个人记录/obsidian-file/wjmber/LifeOS/Tasks/task-management-formulas.base) - 包含高级公式和多个视图
- **简化版**: [simple-task-management.base](file:///d:/个人记录/obsidian-file/wjmber/LifeOS/Tasks/simple-task-management.base) - 基础功能，适合新手

### 2. 创建任务笔记
在笔记中添加以下前置属性：

```yaml
---
type: task
status: todo | in-progress | done
priority: 1 | 2 | 3  # 1=高, 2=中, 3=低
due_date: YYYY-MM-DD  # 可选
project: 项目名称  # 可选
time_estimate: 数字  # 小时，可选
time_spent: 数字  # 小时，可选
---
```

### 3. 查看任务
在 Obsidian 中打开 base 文件，或嵌入到笔记中：

```markdown
![[task-management-formulas.base]]
```

## 文件说明

### Base 文件
- `task-management-formulas.base` - 完整功能任务管理
- `simple-task-management.base` - 简化版任务管理
- `tasks-视图.base` - 现有任务视图（已存在）

### 文档文件
- [任务管理Base使用说明.md](file:///d:/个人记录/obsidian-file/wjmber/LifeOS/Tasks/任务管理Base使用说明.md) - 详细使用指南
- `README.md` - 本快速入门指南

### 示例文件
- `示例任务-工作设计系统.md` - 进行中的高优先级任务
- `示例任务-文档整理.md` - 待办的中优先级任务
- `示例任务-会议准备.md` - 已完成的低优先级任务

## 功能特性

### 完整功能版包含：
- ✅ 8个智能计算公式
- ✅ 6个不同视图（表格、卡片等）
- ✅ 时间跟踪和进度计算
- ✅ 紧急程度自动评分
- ✅ 过期任务自动识别
- ✅ 优先级可视化（红黄绿图标）

### 简化版包含：
- ✅ 4个基本公式
- ✅ 4个简洁视图
- ✅ 优先级和状态图标
- ✅ 日期计算
- ✅ 任务筛选

## 使用场景

### 个人任务管理
1. 创建个人待办事项
2. 设置优先级和截止日期
3. 跟踪任务进度
4. 查看已完成任务

### 项目管理
1. 按项目分组任务
2. 分配时间预算
3. 监控项目进度
4. 生成时间报告

### 团队协作
1. 共享任务视图
2. 统一任务状态
3. 协调截止日期
4. 跟踪完成情况

## 下一步

1. **查看示例**: 打开示例任务文件了解格式
2. **尝试嵌入**: 在笔记中嵌入 base 文件查看效果
3. **创建任务**: 按照格式创建自己的任务
4. **自定义**: 根据需要修改 base 文件

## 获取帮助

详细说明请查看：[任务管理Base使用说明.md](file:///d:/个人记录/obsidian-file/wjmber/LifeOS/Tasks/任务管理Base使用说明.md)

如有问题，可以：
1. 参考示例任务文件
2. 检查前置属性格式
3. 验证日期格式是否正确
4. 确保文件扩展名为 `.md`