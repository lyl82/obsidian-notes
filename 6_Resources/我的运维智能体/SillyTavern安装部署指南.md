# SillyTavern（酒馆）安装部署指南

## 🎯 项目简介

**SillyTavern**（俗称"酒馆"）是一个本地运行的AI聊天和角色扮演界面。它允许您与各种AI语言模型进行对话，创建角色，进行沉浸式角色扮演。类似于一个本地版的AI聊天应用，但功能更强大，完全由您自己控制。

## ⚡ 快速开始（5分钟速览）

如果您已经熟悉命令行操作，可以按以下步骤快速启动：

1. **安装Node.js和Git**（如未安装）
   - 从 https://nodejs.org/ 下载Node.js LTS版本
   - 从 https://git-scm.com/download/win 下载Git

2. **克隆项目**：
   ```cmd
   cd /d F:\downloadforsetup
   git clone https://github.com/SillyTavern/SillyTavern.git --branch release
   ```

3. **安装依赖**：
   ```cmd
   cd SillyTavern
   npm install
   ```

4. **启动服务器**：
   ```cmd
   node server.js
   ```

5. **打开浏览器**：
   访问 http://localhost:8000

**注意**：第一次使用需要配置AI API密钥才能开始聊天。

## 📋 系统要求

### 最低要求
- **操作系统**：Windows 10/11（本指南针对Windows）
- **存储空间**：至少2GB可用空间
- **内存**：4GB RAM或更多
- **网络**：需要联网下载依赖（安装后可以离线使用）

### 必要软件（必须先安装）
1. **Node.js** - 运行SillyTavern的"发动机"
2. **Git** - 下载SillyTavern代码的工具

## 🔧 准备工作

### 1. 检查是否已安装必要软件

#### 检查Node.js
1. 按 `Win + R` 键，输入 `cmd`，按回车
2. 在黑色窗口中输入：`node --version`
3. 如果显示版本号（如 `v24.14.0`），说明已安装
4. 如果显示"不是内部或外部命令"，则需要安装

#### 检查Git
1. 同样在命令提示符中输入：`git --version`
2. 如果显示版本号，说明已安装
3. 如果显示错误，则需要安装

### 2. 下载和安装必要软件（如未安装）

#### 安装Node.js（Windows版）
1. 访问官网：https://nodejs.org/
2. 点击绿色的"LTS"版本下载按钮
3. 运行下载的安装程序（.msi文件）
4. 一直点击"下一步"直到完成
5. **重要**：安装过程中确保勾选"Add to PATH"选项

#### 安装Git（Windows版）
1. 访问官网：https://git-scm.com/download/win
2. 下载64位版本
3. 运行安装程序，使用默认设置即可

## 🚀 安装部署步骤

### 第1步：创建项目文件夹
1. 打开"文件资源管理器"
2. 进入 `F:\` 驱动器
3. 创建新文件夹：`downloadforsetup`
4. 进入这个新文件夹

### 第2步：下载SillyTavern代码
使用**命令提示符（CMD）**执行以下操作：

1. 按 `Win + R`，输入 `cmd`，按回车
2. 切换到项目文件夹：
   ```
   cd /d F:\downloadforsetup
   ```
3. 下载SillyTavern代码：
   ```
   git clone https://github.com/SillyTavern/SillyTavern.git --branch release
   ```
4. 完成后，进入SillyTavern文件夹：
   ```
   cd SillyTavern
   ```

**注意**：如果git命令失败，可能需要重启电脑让环境变量生效。

### 第3步：安装项目依赖
在SillyTavern文件夹中继续执行：

1. 安装依赖包（这需要一些时间）：
   ```
   npm install
   ```
2. 等待安装完成，看到"added X packages"表示成功

**可能出现的情况**：
- 如果看到黄色"warning"可以忽略
- 如果看到红色"error"需要解决问题
- 如果卡住，按 `Ctrl + C` 中断，然后重试

### 第4步：准备Node.js环境（备用方案）

如果您的Node.js有问题，可以下载独立版本：

1. 在浏览器中访问：https://nodejs.org/dist/v24.14.0/
2. 下载 `node-v24.14.0-win-x64.zip`
3. 解压到 `F:\downloadforsetup\nodejs\` 文件夹
4. 使用时需要指定路径（见下文）

## 💻 启动和使用

### 方法一：使用启动脚本（最简单）
1. 在SillyTavern文件夹中，双击 `Start.bat` 文件
2. 或使用命令提示符：
   ```
   cd /d F:\downloadforsetup\SillyTavern
   Start.bat
   ```

### 方法二：手动启动
1. 打开命令提示符
2. 切换到SillyTavern目录：
   ```
   cd /d F:\downloadforsetup\SillyTavern
   ```
3. 启动服务器：
   ```
   node server.js
   ```

### 访问SillyTavern
1. 服务器启动后，打开浏览器
2. 访问地址：http://localhost:8000
3. 如果浏览器没有自动打开，手动输入上述地址

## 🛠️ 故障排除

### 常见问题1：Node.js命令找不到
**症状**：`node --version` 显示"不是内部或外部命令"

**解决方案**：
1. 重启电脑（让环境变量生效）
2. 或使用完整路径：
   ```
   "C:\Program Files\nodejs\node.exe" --version
   ```
3. 或重新安装Node.js，确保勾选"Add to PATH"

### 常见问题2：npm install失败
**症状**：安装过程中出现红色错误信息

**解决方案**：
1. 清除npm缓存：
   ```
   npm cache clean --force
   ```
2. 删除node_modules文件夹（如果有）
3. 重新运行 `npm install`

### 常见问题3：端口被占用
**症状**：启动时显示端口8000已被使用

**解决方案**：
1. 修改配置文件 `config.yaml` 中的端口号
2. 或关闭占用8000端口的程序

### 常见问题4：无法创建文件
**症状**：在沙盒环境或受限环境中启动失败

**解决方案**：
在**常规的命令提示符**中运行，而不是在特殊开发工具中。

### 常见问题5：PowerShell与CMD命令混淆
**症状**：`cd /d F:\downloadforsetup\SillyTavern` 在PowerShell中报错

**原因**：
- `cd /d` 是CMD（命令提示符）的语法
- PowerShell使用不同的命令：`Set-Location` 或直接 `cd`

**解决方案**：
1. **在CMD中使用**：
   ```
   cd /d F:\downloadforsetup\SillyTavern
   ```
2. **在PowerShell中使用**：
   ```
   Set-Location "F:\downloadforsetup\SillyTavern"
   ```
   或
   ```
   cd "F:\downloadforsetup\SillyTavern"
   ```

### 常见问题6：Node.js路径问题
**症状**：已安装Node.js但命令找不到

**解决方案**：
1. **检查安装路径**：
   - Node.js默认安装到：`C:\Program Files\nodejs\`
   - 或：`C:\Program Files (x86)\nodejs\`
2. **手动指定路径**：
   ```
   "C:\Program Files\nodejs\node.exe" server.js
   ```
3. **添加环境变量**：
   - 右键"此电脑" → 属性 → 高级系统设置
   - 环境变量 → 系统变量Path → 编辑
   - 添加Node.js安装路径

### 常见问题7：npm权限问题
**症状**：npm安装时出现权限错误

**解决方案**：
1. **以管理员身份运行命令提示符**
2. **修改npm全局安装路径**：
   ```
   npm config set prefix "C:\npm-global"
   ```
3. **添加新路径到环境变量**

### 常见问题8：依赖安装缓慢或失败
**症状**：`npm install` 卡住或下载失败

**解决方案**：
1. **使用淘宝镜像（国内用户）**：
   ```
   npm config set registry https://registry.npmmirror.com
   ```
2. **设置代理（如有需要）**：
   ```
   npm config set proxy http://proxy.example.com:8080
   ```
3. **重试并跳过可选依赖**：
   ```
   npm install --no-optional
   ```

### 常见问题9：启动后无法访问页面
**症状**：服务器启动成功，但浏览器无法打开

**解决方案**：
1. **检查防火墙**：允许Node.js通过防火墙
2. **检查端口**：确认8000端口未被其他程序占用
3. **使用IP地址访问**：`http://127.0.0.1:8000`
4. **检查服务器日志**：查看是否有错误信息

### 常见问题10：数据丢失或损坏
**症状**：角色数据丢失或配置文件损坏

**预防措施**：
1. **定期备份** `data` 文件夹
2. **不要手动修改** `data` 文件夹中的文件（除非知道用途）
3. **使用导出功能**备份角色和对话

## 📁 项目结构说明

```
F:\downloadforsetup\SillyTavern\
├── public\          # 网页界面文件
├── src\            # 程序源代码
├── data\           # 用户数据（运行时生成）
├── config.yaml     # 配置文件
├── package.json    # 项目依赖列表
├── server.js       # 主服务器文件
└── Start.bat       # Windows启动脚本
```

## ⚙️ 配置文件说明

主要配置文件 `config.yaml` 中的重要设置：

```yaml
# 服务器端口（默认8000）
port: 8000

# 是否自动打开浏览器
browserLaunch:
  enabled: true
  browser: 'default'

# 数据存储位置
dataRoot: ./data
```

## 🔄 更新和升级

### 更新SillyTavern
1. 进入SillyTavern文件夹：
   ```
   cd /d F:\downloadforsetup\SillyTavern
   ```
2. 拉取最新代码：
   ```
   git pull
   ```
3. 更新依赖：
   ```
   npm install
   ```

### 更新Node.js
从Node.js官网下载最新LTS版本重新安装。

## 🧰 实用命令备忘

### 检查版本
```cmd
node --version      # 检查Node.js版本
npm --version       # 检查npm版本
git --version       # 检查Git版本
```

### 项目管理
```cmd
cd /d F:\downloadforsetup\SillyTavern  # 进入项目
npm install                            # 安装依赖
node server.js                         # 启动服务器
```

### 进程管理
- 按 `Ctrl + C` 停止服务器
- 在任务管理器中结束Node.js进程（如果卡死）

## 💡 使用技巧

### 1. AI模型配置（关键步骤）
首次启动后，需要配置AI API密钥才能开始聊天：

#### 支持的AI服务：
- **OpenAI**（ChatGPT）：最常用，需购买API密钥
- **Claude**（Anthropic）：功能强大
- **Google Gemini**：免费额度较大
- **本地模型**：需额外设置

#### 配置步骤：
1. 启动SillyTavern并打开浏览器界面
2. 点击左侧菜单的"设置"（齿轮图标）
3. 选择"API连接"选项卡
4. 选择您要使用的AI服务
5. 输入API密钥（从对应服务商获取）
6. 保存设置，开始聊天

#### 获取API密钥：
- **OpenAI**：访问 https://platform.openai.com/api-keys
- **Claude**：访问 https://console.anthropic.com/
- **Google Gemini**：访问 https://makersuite.google.com/

### 2. 角色创建与管理
- **导入角色**：下载角色卡（.json或.png文件）并导入
- **创建角色**：使用角色编辑器自定义名称、头像、性格等
- **角色市场**：在线查找和下载其他用户创建的角色

### 3. 扩展功能
- **插件系统**：支持多种功能扩展
- **主题定制**：更换界面主题
- **快捷键**：自定义操作快捷键

### 4. 数据安全
- **定期备份** `data` 文件夹
- **导出对话**：重要对话可以导出保存
- **角色备份**：导出自定义角色文件

## 📞 获取帮助

### 官方资源
- GitHub仓库：https://github.com/SillyTavern/SillyTavern
- 官方文档：在项目中查看README文件
- 社区支持：GitHub Issues或相关社区

### 本地帮助
项目中的文档文件：
- `README.md` - 基本介绍
- `docs/` 文件夹 - 详细文档

## ✅ 安装成功验证

完成安装后，请检查以下几点：

1. ✅ Node.js可以运行：`node --version` 显示版本号
2. ✅ Git可以运行：`git --version` 显示版本号  
3. ✅ 项目文件夹存在：`F:\downloadforsetup\SillyTavern\`
4. ✅ 依赖安装完成：`node_modules` 文件夹存在且较大
5. ✅ 服务器能启动：访问 http://localhost:8000 能看到界面

## 🎉 开始使用

一切就绪后，您可以：
1. 启动SillyTavern
2. 在浏览器中打开界面
3. 配置AI API密钥
4. 开始聊天或角色扮演

祝您使用愉快！