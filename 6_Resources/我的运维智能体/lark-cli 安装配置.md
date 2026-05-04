# lark-cli 安装配置与验证总结

## 任务目标

本地环境安装 `lark-cli`，能通过命令行成功读取飞书文档内容、写入飞书表格单元格，并留存一份换机器可复现的安装配置笔记。

## 完成情况

| 任务 | 状态 |
|------|------|
| 安装 lark-cli v1.0.23 | ✅ 完成 |
| 配置飞书 App 凭证 | ✅ 完成 |
| 用户授权登录 | ✅ 完成 |
| 写入多维表格记录 | ✅ 完成 |
| 编写安装配置笔记 | ✅ 完成 |

## 详细过程

### 1. 安装 lark-cli

使用 npm 全局安装飞书官方 CLI 工具：

```powershell
npm install -g @larksuite/cli
```

- 安装版本：1.0.23
- 安装路径：D:\Documents\04_GitRepos\npm-global\node_modules

### 2. 配置认证

#### 2.1 配置 App 凭证

```powershell
lark-cli config init --app-id <App ID> --app-secret-stdin
```

#### 2.2 用户授权登录

```powershell
# 获取授权码
lark-cli auth login --recommend --no-wait

# 完成授权
lark-cli auth login --device-code <device_code>
```

### 3. 功能验证

#### 3.1 写入多维表格记录

成功向用户的 stream_log_时间实际表 添加了一条记录：

- **Base Token**: OLFqbMUCNaKNKEslF9VcYVHpnKc
- **Table ID**: tblNHgT3WA2bHti5
- **新增数据**: 起始时间 → 2026-05-03 11:10:00
- **记录 ID**: recviwzneEUNBj

```powershell
# 添加记录命令
lark-cli base +record-batch-create --base-token OLFqbMUCNaKNKEslF9VcYVHpnKc --table-id tblNHgT3WA2bHti5 --json "{\"fields\":[\"fld0ewjpju\"],\"rows\":[[1777777800000]]}"
```

**注意**：日期时间字段需要使用时间戳（毫秒）格式

### 4. 配置文件位置

- Windows: C:\Users\<用户名>\.lark-cli\config.json

## 生成的文档

- 📄 安装配置笔记：[飞书CLI安装配置笔记.md](d:/个人记录/obsidian-file/wjmber/LifeOS/4_Exploration/电子信息设备/飞书CLI安装配置笔记.md)

## 踩坑记录

### 中文编码问题

PowerShell 传递中文 JSON 可能出现乱码，建议使用 `@file.json` 方式读取文件。

### 时间字段格式

日期时间字段需要使用时间戳（毫秒）格式，而非字符串格式。

### GitHub 访问失败

安装 skills 时可能因网络问题失败，可跳过，不影响 CLI 核心功能。

## 换机器复现步骤

1. 安装 Node.js (v18+)
2. 执行 `npm install -g @larksuite/cli`
3. 配置 PATH 环境变量（Node.js 和 npm global 路径）
4. 执行 `lark-cli config init` 配置 App 凭证
5. 执行 `lark-cli auth login --recommend --no-wait` 完成用户授权

---

完成时间：2026-05-03
