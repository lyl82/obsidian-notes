# 人生OS 1.0 系统架构背景

此文档整理了 人生OS 1.0 系统的整体架构、文件结构、核心原则和控制机制，作为 AI 可以理解和参考的背景知识。

## 1. 系统概述
人生OS 1.0 是一个个人生活操作系统，旨在通过结构化的文件夹和文件管理健康、关系、工作等领域。架构分为多个层级：
- **治理层 (1_ControlPlane)**：包含宪法、核心控制逻辑和系统态管理。
- **领域层 (3_Domains)**：具体的业务领域（健康、关系、工作）。
- **探索层 (4_Exploration)**：沙盒实验区。
- **信息流层 (0_Inbox/2_DAO/7_Archive)**：数据的输入、记录与归档。
- **工具层 (5_Tools)** & **资源层 (6_Resources)**：支持系统运行的组件。

关键概念：
- **三件套模板**：Service (服务目标)、Control (决策规则)、DAO (数据支持)。
- **SERVICE-E 元原则**：能量第一性，作为系统存在论基础。
- **系统态 (System State)**：如“睡眠”，不是功能模块，而是底层运行时边界。

## 2. 文件结构
以下是 人生OS 1.0 目录的核心结构：

```
人生OS 1.0
+---0_Inbox
+---1_ControlPlane
|   |   📜_Service_Constitution.md (总宪法)
|   |   🚦_Control_IF-THEN.md
|   |   🔍_Control_Questions.md
|   \---SystemState (系统态管理)
|       \---Sleep (睡眠：系统边界)
|               📜_Service_Sleep.md
|               🚦_Control_Sleep.md
|               睡眠-非结构dao/
+---CodeLibrary (系统自动化脚本库)
|   |   📜_Code_Index.md (脚本索引)
|   |   archive_sleep_logs.py (归档工具 - 睡眠)
|   |   general_archiver.py (归档工具 - 通用)
|   |   workout_archiver.py (归档工具 - 锻炼专项)
+---2_DAO (注意力时间线)
+---3_Domains
|   +---Health
|   +---Relationships
|   \---Work
+---4_Exploration
+---5_Tools
+---6_Resources
\---7_Archive
```

## 3. 核心原则 (Service Constitution)
重点原则摘要：
- **能量第一性**：一切决策受制于能量供应水平。
- **稳定优先于表现**：不为短期爆发牺牲系统稳定性。
- **睡眠全局互斥锁**：睡眠是系统级红线，到点必须强制降级，剥夺应用层 Service 执行权。

## 4. 关键控制机制 (Control)

### 系统态：睡眠 (System State: Sleep)
- **触发**：节律驱动（固定时间锚点）。
- **逻辑**：三段式窗口（预降级 -> 意识撤出 -> 恢复运行）。
- **特殊处理**：已知破坏事件 (KDE) 触发“降级模式”，防止扰动放大。

### 领域控制 (Domain Control)
- **Health**：睡眠红线、生理预警、执行/延迟/丢弃。
- **Relationships**：成本红线、价值评估、保护个人节奏。
- **Work**：ROI 红线、专注匹配、高杠杆优先。

## 5. AI 协作指南
当 AI 处理 人生OS 1.0 相关任务时，应：
1. **优先检查能量状态**：参考 SERVICE-E 和睡眠状态。
2. **遵循互斥锁原则**：在睡眠窗口或降级模式下，停止推荐高强度任务。
3. **维护系统完整性**：所有新功能必须适配 Service/Control/DAO 三件套架构。

此文档作为 人生OS 1.0 的“元数据”，定义了系统的运行边界。
