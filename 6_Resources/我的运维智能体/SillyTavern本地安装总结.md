# SillyTavern本地安装总结报告

## 📍 安装位置总览（核心信息）

### 🎯 主安装位置
```
F:\downloadforsetup\SillyTavern\
```
**包含**：所有SillyTavern文件、启动脚本、配置文件、用户数据

### 🔧 备用Node.js位置
```
F:\downloadforsetup\nodejs\node-v24.14.0-win-x64\
```
**用途**：当系统Node.js损坏时使用

### 📁 关键文件位置速查
| 文件/文件夹 | 位置                                              | 用途       |
| ------ | ----------------------------------------------- | -------- |
| 启动脚本   | `F:\downloadforsetup\SillyTavern\Start.bat`     | 一键启动     |
| 配置文件   | `F:\downloadforsetup\SillyTavern\config.yaml`   | 服务器设置    |
| 用户数据   | `F:\downloadforsetup\SillyTavern\data\`         | 角色、对话等   |
| 依赖包    | `F:\downloadforsetup\SillyTavern\node_modules\` | 798个必要组件 |
| 主程序    | `F:\downloadforsetup\SillyTavern\server.js`     | 服务器核心    |
| 项目定义   | `F:\downloadforsetup\SillyTavern\package.json`  | 依赖列表     |

### 🗺️ 目录结构图
```
F:\downloadforsetup\
├── SillyTavern\          # 主项目（已安装）
│   ├── Start.bat         # 启动脚本
│   ├── server.js         # 服务器文件
│   ├── config.yaml       # 配置文件
│   ├── package.json      # 依赖定义
│   ├── node_modules\     # 依赖包（798个）
│   └── data\             # 用户数据（运行时生成）
└── nodejs\               # 备用Node.js
    └── node-v24.14.0-win-x64\
        ├── node.exe      # Node.js主程序
        └── npm.cmd       # npm包管理器
```

## 🔧 实际安装经验总结（从聊天记录提取）

### 🚨 遇到的真实问题

#### 问题1：Node.js安装损坏（最严重）
**发现过程**：
- 检查Node.js：`node --version` 正常显示v24.12.0
- 但 `npm --version` 报错：找不到 `D:\Documents\01_Projects\node_modules\npm\bin\npm-prefix.js`

**根本原因**：
- Node.js安装路径混乱，指向了错误的用户文档目录
- 可能是之前安装时选择了自定义路径或移动了文件

**实际解决方案**：
1. **不修复原有安装**，而是下载独立版本
2. 从 https://nodejs.org/dist/v24.14.0/ 下载 `node-v24.14.0-win-x64.zip`
3. 解压到干净位置：`F:\downloadforsetup\nodejs\node-v24.14.0-win-x64\`
4. 使用完整路径：`"F:\downloadforsetup\nodejs\node-v24.14.0-win-x64\node.exe"`

#### 问题2：命令行环境混淆
**用户操作**：在PowerShell中执行 `cd /d F:\downloadforsetup\SillyTavern`

**错误信息**：PowerShell不认识 `/d` 参数

**原因分析**：
- `cd /d` 是**CMD（命令提示符）**的语法
- PowerShell使用不同的命令系统
- 这是Windows用户常见混淆点

**正确做法**：
- **在CMD中**：`cd /d F:\downloadforsetup\SillyTavern` ✓
- **在PowerShell中**：`Set-Location "F:\downloadforsetup\SillyTavern"` ✓
- 或直接 `cd "F:\downloadforsetup\SillyTavern"` ✓

#### 问题3：开发工具沙盒限制
**症状**：在Trae IDE中启动时无法创建 `data/cookie-secret.txt`

**原因**：安全沙盒限制文件创建权限

**解决方案**：在**常规Windows命令提示符**中运行，而不是在IDE或特殊工具中

### ✅ 成功的关键因素
1. **使用独立Node.js**：绕过系统安装问题
2. **正确命令行环境**：使用CMD而非PowerShell执行特定命令
3. **常规命令提示符**：避免沙盒权限限制
4. **耐心等待依赖安装**：798个包需要时间下载

## 🚀 核心安装步骤（精简版）

### 第1步：准备环境
```cmd
# 检查Node.js
node --version

# 检查Git
git --version

# 如未安装，从官网下载安装
```

### 第2步：克隆项目
```cmd
cd /d F:\downloadforsetup
git clone https://github.com/SillyTavern/SillyTavern.git --branch release
```

### 第3步：安装依赖
```cmd
cd SillyTavern
npm install
```

### 第4步：启动服务器
```cmd
node server.js
```

### 第5步：访问界面
浏览器打开：http://localhost:8000

## ⚠️ 关键注意事项

### 1. 环境变量问题
- Node.js安装时要勾选"Add to PATH"
- 如PATH有问题，重启电脑或使用完整路径

### 2. 依赖安装
- 第一次 `npm install` 会安装798个包
- 需要网络连接，国内用户可设置淘宝镜像

### 3. 启动位置
- 必须在 `F:\downloadforsetup\SillyTavern\` 目录中启动
- 使用 `Start.bat` 或 `node server.js`

## 📊 安装验证清单

| 检查项 | 命令/位置 | 预期结果 |
|--------|-----------|----------|
| Node.js | `node --version` | 显示版本号（如v24.14.0） |
| Git | `git --version` | 显示版本号 |
| 项目目录 | `F:\downloadforsetup\SillyTavern\` | 存在且包含文件 |
| 依赖包 | `node_modules\` 文件夹 | 存在且较大（约几百MB） |
| 配置文件 | `config.yaml` | 存在，端口默认8000 |
| 服务器启动 | `node server.js` | 显示"Server running on port 8000" |
| 浏览器访问 | http://localhost:8000 | 显示SillyTavern界面 |

## 🔄 重新安装流程

### 情况1：完全重新安装
1. 删除 `F:\downloadforsetup\SillyTavern\` 文件夹
2. 重新执行"核心安装步骤"

### 情况2：更新现有安装
```cmd
cd /d F:\downloadforsetup\SillyTavern
git pull
npm install
```

### 情况3：仅修复依赖
```cmd
cd /d F:\downloadforsetup\SillyTavern
npm cache clean --force
rmdir /s node_modules
npm install
```

## 💡 实用技巧

### 快速启动
创建快捷方式到桌面：
1. 右键 `Start.bat` → 发送到 → 桌面快捷方式
2. 双击桌面快捷方式启动

### 端口修改
如8000端口被占用，修改 `config.yaml`：
```yaml
port: 8001  # 改为其他端口
```

### 数据备份
- 备份 `data` 文件夹到安全位置
- 定期导出重要角色和对话

## 🆘 紧急恢复

### Node.js损坏时
```cmd
# 使用备用Node.js
"F:\downloadforsetup\nodejs\node-v24.14.0-win-x64\node.exe" server.js
```

### 项目文件损坏时
```cmd
# 备份数据
xcopy F:\downloadforsetup\SillyTavern\data F:\backup\sillytavern-data /E

# 重新克隆
cd /d F:\downloadforsetup
rmdir /s SillyTavern
git clone https://github.com/SillyTavern/SillyTavern.git --branch release

# 恢复数据
xcopy F:\backup\sillytavern-data F:\downloadforsetup\SillyTavern\data /E
```

## 📞 快速参考

### 常用命令
```cmd
# 进入项目
cd /d F:\downloadforsetup\SillyTavern

# 启动
node server.js

# 停止
Ctrl + C

# 更新
git pull && npm install
```

### 关键文件
- `Start.bat` - Windows启动脚本
- `server.js` - 主服务器文件
- `config.yaml` - 配置文件
- `package.json` - 依赖定义

---

**总结**：SillyTavern已成功安装在 `F:\downloadforsetup\SillyTavern\`，使用Node.js v24.14.0运行。主要问题是环境变量和命令行语法，已通过备用Node.js和正确命令解决。下次安装时注意使用CMD而非PowerShell执行 `cd /d` 命令。