---
title: 飞书 CLI (lark-cli) 安装配置笔记
date: 2026-05-03
tags:
  - 飞书
  - CLI
  - 自动化
created: 2026-05-03
status: done
---

# 飞书 CLI (lark-cli) 安装配置笔记

## 环境信息

- Node.js: v24.14.0
- npm: 11.9.0
- lark-cli: 1.0.23
- 安装路径: `D:\Documents\04_GitRepos\npm-global\node_modules`
- Node.js 路径: `F:\downloadforsetup\nodejs\node-v24.14.0-win-x64`

## 一、安装步骤

### 1.1 安装 Node.js（如未安装）

从 [Node.js 官网](https://nodejs.org/) 下载安装，推荐 v18+ 版本。

### 1.2 安装 lark-cli

```powershell
npm install -g @larksuite/cli
```

### 1.3 安装 CLI SKILL（可选，用于 AI Agent）

```powershell
npx skills add larksuite/cli -y -g
```

> 注意：此步骤需要访问 GitHub，网络不畅时可能失败。不影响 CLI 核心功能使用。

### 1.4 验证安装

```powershell
lark-cli --version
# 输出: lark-cli version 1.0.23
```

## 二、配置认证

### 2.1 创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 App ID 和 App Secret

### 2.2 配置 App 凭证

```powershell
lark-cli config init --app-id <你的App ID> --app-secret-stdin
# 按提示输入 App Secret
```

### 2.3 用户授权登录

```powershell
lark-cli auth login --recommend --no-wait
# 会输出验证 URL 和验证码
```

1. 访问输出的验证 URL
2. 输入验证码完成授权
3. 执行以下命令完成登录：

```powershell
lark-cli auth login --device-code <device_code>
```

### 2.4 查看认证状态

```powershell
lark-cli auth status
```

## 三、常用命令

### 3.1 多维表格（Base）

```powershell
# 查看表字段
lark-cli base +field-list --base-token <base_token> --table-id <table_id>

# 查看记录
lark-cli base +record-list --base-token <base_token> --table-id <table_id>

# 批量添加记录
lark-cli base +record-batch-create --base-token <base_token> --table-id <table_id> --json "{\"fields\":[\"字段名\"],\"rows\":[[\"值\"]]}"
```

### 3.2 文档（Docs）

```powershell
# 读取文档
lark-cli docs +fetch --doc <文档URL或token>

# 搜索文档
lark-cli docs +search --query "关键词"
```

### 3.3 电子表格（Sheets）

```powershell
# 读取表格
lark-cli sheets +read --spreadsheet-token <token>

# 写入单元格
lark-cli sheets +write --spreadsheet-token <token> --range <范围> --values <值>
```

### 3.4 通用 API 调用

```powershell
lark-cli api <METHOD> <PATH> --data <JSON>
```

## 四、关键参数说明

### 4.1 Base token 和 Table ID

从飞书多维表格 URL 中提取：
```
https://xxx.feishu.cn/base/XXX?table=YYY
# XXX = base token
# YYY = table ID（以 tbl 开头）
```

### 4.2 日期时间字段格式

多维表格日期字段支持时间戳格式（毫秒）：
```
1746256200000  # 对应 2026-05-03 11:10:00
```

## 五、权限配置

飞书应用需要开通相应权限才能操作数据：

### 必开权限（多维表格）

- `base:field:read` - 读取字段
- `base:field:write` - 写入字段
- `base:record:read` - 读取记录
- `base:record:write` - 写入记录
- `base:table:read` - 读取表格
- `base:table:write` - 写入表格

### 权限申请步骤

1. 开放平台 → 应用管理 → 选择应用
2. 权限管理 → 开通所需权限
3. 版本管理与发布 → 创建版本 → 发布

## 六、换机器复现步骤

1. 安装 Node.js
2. 执行 `npm install -g @larksuite/cli`
3. 配置环境变量（PATH 包含 Node.js 和 npm global 路径）
4. 执行 `lark-cli config init` 配置 App 凭证
5. 执行 `lark-cli auth login --recommend --no-wait` 完成用户授权

## 七、踩坑记录

### 7.1 中文编码问题

PowerShell 传递中文 JSON 可能出现乱码。建议使用 `@file.json` 方式读取文件。

### 7.2 时间字段格式

日期时间字段需要使用时间戳（毫秒）格式，而非字符串格式。

### 7.3 GitHub 访问失败

安装 skills 时可能因网络问题失败，可跳过，不影响核心功能。

## 八、配置文件位置

- Windows: `C:\Users\<用户名>\.lark-cli\config.json`
- macOS/Linux: `~/.lark-cli/config.json`

---

配置完成时间: 2026-05-03
