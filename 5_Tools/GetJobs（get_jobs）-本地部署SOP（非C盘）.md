# GetJobs（get_jobs）-本地部署SOP（非C盘）

## 0. 目标与验收

**目标**

- 把 GitHub 项目 `https://github.com/loks666/get_jobs` 下载到 `D:\Documents\04_GitRepos`
- 所有下载/缓存/运行产物尽量落在 D 盘（不安装到 C 盘）
- 能看到 UI 页面

**验收**

- UI 可访问：`http://localhost:6866/`
- 后端 API（可选）可访问：`http://localhost:8888/`

## 1. 项目是什么（最少知识点）

- 这是一个“自动投简历/爬平台”的工具，后端是 Java（Spring Boot），前端是 Next.js（打包后是静态文件）。
- 启动后常见会出现两个端口：
  - `6866`：UI（静态前端）
  - `8888`：后端 API（业务逻辑、配置存储、调用 Playwright 等）
- 该项目后端启动时会初始化 Playwright（浏览器自动化），可能触发“自动下载浏览器”到用户目录（常见在 C 盘用户目录）。如果你的运行环境/沙盒限制访问 C 盘，会导致后端直接崩溃。

## 2. 目录约定（可复用、可回溯）

统一把“代码”和“环境”分开，便于迁移、复现、清理。

**代码目录**

- `D:\Documents\04_GitRepos\get_jobs`

**环境目录（非C盘）**

- `D:\Documents\04_GitRepos\env`
  - `jdk-21\`：免安装 JDK 21
  - `.gradle\`：Gradle 缓存（避免落到 `C:\Users\<你>\.gradle`）
  - `playwright\`：Playwright 浏览器目录（可选，用于避免落到 C 盘用户目录）

**前端静态产物目录**

- `D:\Documents\04_GitRepos\get_jobs\src\main\resources\dist`

## 3. 一次性初始化（只做一遍）

### 3.1 克隆代码到指定位置

在 PowerShell 执行：

```powershell
New-Item -ItemType Directory -Force -Path D:\Documents\04_GitRepos
cd D:\Documents\04_GitRepos
git clone https://github.com/loks666/get_jobs.git
```

### 3.2 准备免安装 JDK 21（放 D 盘）

建议使用 Microsoft OpenJDK 21 的 zip 包，解压到：

- `D:\Documents\04_GitRepos\env\jdk-21\jdk-21.x.x+xx\`

后续通过 `JAVA_HOME` 指向这个路径即可，不需要全局安装。

### 3.3 准备前端 dist（不依赖 Node 编译）

该项目 release 提供 `dist.zip`（前端已编译好的静态文件）。

下载并解压到：

- `D:\Documents\04_GitRepos\get_jobs\src\main\resources\dist`

如果解压后出现一层多余的 `dist\dist\...`，以最终能在目录下直接看到 `index.html` 为准。

目录检查要点：

- `src\main\resources\dist\index.html` 必须存在
- `_next\` 目录必须存在

## 4. 启动方式 A：完整启动（后端 + UI）

适用场景：真实 Windows 环境（非受限沙盒）、允许 Playwright 安装浏览器，或你已把 Playwright 浏览器安装到了 D 盘。

### 4.1 编译（首次或更新代码后）

在 `D:\Documents\04_GitRepos\get_jobs` 目录打开 PowerShell，执行：

```powershell
$env:JAVA_HOME='D:\Documents\04_GitRepos\env\jdk-21\jdk-21.0.10+7'
$env:GRADLE_USER_HOME='D:\Documents\04_GitRepos\env\.gradle'
.\gradlew build -x test
```

产物位置：

- `build\libs\get_jobs-0.0.1-SNAPSHOT.jar`

### 4.2 启动后端（会自动打开 UI 页面）

```powershell
$env:JAVA_HOME='D:\Documents\04_GitRepos\env\jdk-21\jdk-21.0.10+7'
$env:GRADLE_USER_HOME='D:\Documents\04_GitRepos\env\.gradle'

& "$env:JAVA_HOME\bin\java.exe" -jar "build\libs\get_jobs-0.0.1-SNAPSHOT.jar"
```

验证：

- UI：`http://localhost:6866/`
- API：`http://localhost:8888/api/health`

注意：

- 如果你之前运行过“仅UI（6866）”模式，必须先关掉那个窗口/进程，否则完整启动会因为 `6866` 端口被占用而失败。

### 4.3 Playwright（避免写入 C 盘的策略）

如果你明确要求 Playwright 的浏览器下载/缓存也必须在 D 盘，优先尝试：

```powershell
$env:PLAYWRIGHT_BROWSERS_PATH='D:\Documents\04_GitRepos\env\playwright'
```

然后再启动后端。

注意：项目内部依赖 Playwright Java，会在首次运行时尝试安装 driver/browsers。不同环境下会有不同落盘目录，建议以日志为准。

## 5. 启动方式 B：只启动 UI（刻意体现“服务不可用”）

适用场景：

- 后端因 Playwright 权限/网络/沙盒限制无法启动
- 你只需要 UI 可见、可打开，并在 UI 操作时体现“接口不可用”

### 5.1 用 JDK 自带 `jwebserver` 托管 dist

在 `D:\Documents\04_GitRepos\get_jobs` 目录执行：

```powershell
$env:JAVA_HOME='D:\Documents\04_GitRepos\env\jdk-21\jdk-21.0.10+7'

& "$env:JAVA_HOME\bin\jwebserver.exe" `
  -d "D:\Documents\04_GitRepos\get_jobs\src\main\resources\dist" `
  -p 6866 `
  -b 0.0.0.0
```

打开：

- `http://localhost:6866/`

此时后端未运行：

- `http://localhost:8888/` 会连接失败
- UI 页面能打开，但点击“保存配置/启动任务/拉取数据”等动作会提示失败，这就是“只有服务不可用”的演示效果。

## 6. 常见问题与定位（按现象排查）

### 6.1 现象：`http://localhost:8888/` 无法连接

含义：后端没有在运行，或者启动后崩溃退出。

处理：

- 看启动日志中是否出现 Playwright 相关错误（例如 Failed to install browsers / create driver）
- 如果是权限/路径限制，走“启动方式 B：只启动 UI”可以先完成 UI 验收

### 6.2 现象：后端启动报 Playwright 安装失败

含义：Playwright 在安装 driver/browsers 时无法写入默认目录或网络不可达。

处理顺序：

1) 确保网络可访问 Playwright 下载源（有时需要能访问 GitHub/CDN）
2) 设定 `PLAYWRIGHT_BROWSERS_PATH` 指向 D 盘目录
3) 在真实环境运行（不要在受限沙盒/严格目录白名单环境中运行）

### 6.3 现象：日志提示无法创建 `.\target\logs\get-jobs.log` 目录

含义：程序想写日志文件，但 `target\logs` 不存在。

处理：

- 手动创建目录：`D:\Documents\04_GitRepos\get_jobs\target\logs`
- 或者只关注控制台日志（不影响核心功能）

### 6.4 现象：`Error: Unable to access jarfile build\libs\get_jobs-0.0.1-SNAPSHOT.jar`

含义：`java -jar ...` 这条命令执行时，当前所在目录里并不存在这个相对路径（或者还没编译生成 jar）。

处理（按顺序做）：

1) 确认你在项目根目录执行（必须先 `cd` 进去）

```powershell
cd D:\Documents\04_GitRepos\get_jobs
```

2) 确认 jar 是否存在

```powershell
dir build\libs
```

3) 若不存在，先编译生成 jar

```powershell
$env:JAVA_HOME='D:\Documents\04_GitRepos\env\jdk-21\jdk-21.0.10+7'
$env:GRADLE_USER_HOME='D:\Documents\04_GitRepos\env\.gradle'
.\gradlew build -x test
```

4) 再启动

```powershell
$env:JAVA_HOME='D:\Documents\04_GitRepos\env\jdk-21\jdk-21.0.10+7'
& "$env:JAVA_HOME\bin\java.exe" -jar "build\libs\get_jobs-0.0.1-SNAPSHOT.jar"
```

## 7. 经验沉淀（反思与建议）

### 7.1 关键坑位

- **Playwright 在启动阶段就初始化**：即使你只是想看 UI，也可能导致后端因为“安装浏览器到默认目录”失败而崩溃。
- **端口行为**：项目会尝试同时跑 API（8888）和静态资源（6866），因此你可能会看到 UI 端口能开一会儿，但后端崩溃后 UI 也跟着消失。

### 7.2 最稳的“先验收 UI”策略

- 先用 `dist.zip + jwebserver` 把 UI 单独跑起来（不依赖 Node、不依赖后端）
- 后端问题（Playwright、网络、权限）单独处理，不阻塞 UI 验收

### 7.3 可选的工程化改进方向（如果要长期用）

- 增加一个“禁用 Playwright 的启动参数/环境变量”，使后端启动不强制初始化浏览器引擎（仅在真正执行投递任务时再初始化）。
- 增加“Playwright 安装路径”的可配置项，明确落盘到 D 盘。

## 8. 一键启动模板（复制即可用）

### 8.1 只看 UI（服务不可用演示）

```powershell
$env:JAVA_HOME='D:\Documents\04_GitRepos\env\jdk-21\jdk-21.0.10+7'
& "$env:JAVA_HOME\bin\jwebserver.exe" -d "D:\Documents\04_GitRepos\get_jobs\src\main\resources\dist" -p 6866 -b 0.0.0.0
```

### 8.2 完整启动（后端 + UI）

```powershell
cd D:\Documents\04_GitRepos\get_jobs
$env:JAVA_HOME='D:\Documents\04_GitRepos\env\jdk-21\jdk-21.0.10+7'
$env:GRADLE_USER_HOME='D:\Documents\04_GitRepos\env\.gradle'
$env:PLAYWRIGHT_BROWSERS_PATH='D:\Documents\04_GitRepos\env\playwright'
.\gradlew build -x test
& "$env:JAVA_HOME\bin\java.exe" -jar "build\libs\get_jobs-0.0.1-SNAPSHOT.jar"
```

## 9. 一键脚本（可直接运行）

- `d:\个人记录\obsidian-file\wjmber\LifeOS\5_Tools\GetJobs-启动-完整（后端+UI）.ps1`
- `d:\个人记录\obsidian-file\wjmber\LifeOS\5_Tools\GetJobs-启动-仅UI（服务不可用演示）.ps1`

运行方式（推荐，避免执行策略拦截）：

```powershell
powershell -ExecutionPolicy Bypass -File "d:\个人记录\obsidian-file\wjmber\LifeOS\5_Tools\GetJobs-启动-完整（后端+UI）.ps1"
```

如果提示端口被占用（6866/8888），用下面命令定位并结束进程（以 6866 为例）：

```powershell
$c = Get-NetTCPConnection -State Listen -LocalPort 6866
$pid = $c | Select-Object -First 1 -ExpandProperty OwningProcess
Get-Process -Id $pid
Stop-Process -Id $pid -Force
```

## 10. 功能点击无反应：日志排查SOP

先确认后端活着：

```powershell
Invoke-WebRequest -Uri "http://localhost:8888/api/health" -UseBasicParsing
```

如果这里失败，UI 再能打开也只能“看页面”，功能不会执行。

查看后端日志（推荐）：

```powershell
powershell -ExecutionPolicy Bypass -File "d:\个人记录\obsidian-file\wjmber\LifeOS\5_Tools\GetJobs-查看后端日志.ps1"
```

日志文件路径：

- `D:\Documents\04_GitRepos\get_jobs\target\logs\get-jobs.log`

快速筛错误：

```powershell
Select-String -Path "D:\Documents\04_GitRepos\get_jobs\target\logs\get-jobs.log" -Pattern "ERROR|Exception|Playwright|Failed" -CaseSensitive:$false
```

前端配合排查：

- 打开 UI 页面后按 `F12`。
- 在 `Network` 看点击按钮后是否真的发出了请求。
- 在 `Console` 看是否有 `500/404/CORS/timeout` 报错。
