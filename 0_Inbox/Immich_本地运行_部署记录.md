# Immich 本地运行/部署记录（Windows）

## 当前环境结论

- **Immich 服务已成功部署并运行** ✅
- **所有数据均在 D 盘**（不占用 C 盘），路径：`D:\Documents\04_GitRepos\immich-app`
- 访问方式：`http://localhost:2283`

## 落盘位置（按 D 盘约束）

- Docker Compose 运行目录（已准备文件）：`D:\Documents\04_GitRepos\immich-app\`
  - `docker-compose.yml`
  - `.env`（已改为 D 盘持久化路径；`DB_PASSWORD` 已随机化；未在此文档重复展示）
  - `library\`、`postgres\`（持久化目录）
- 源码目录（用于二次开发/本地运行 web）：`D:\Documents\04_GitRepos\immich\`

## 部署与验证记录

- 虚拟化开启：用户已开启 BIOS 虚拟化及 Windows 功能。
- 网络配置：通过 VPN 解决 ghcr.io 访问问题。
- Docker 状态：容器正常启动，Health Check 通过。
- 首次使用：访问 `http://localhost:2283`，创建管理员账号即可开始使用。

## 为什么现在“不能直接用”

- 你目前打开的是 Immich 的 Web 前端开发服务器。它只负责界面渲染，本身不包含相册系统的核心能力。
- Immich 的核心能力（登录、上传、相册、检索、人脸/机器学习等）需要后端服务 + 数据库（Postgres）+ 缓存/队列（Redis）等组件协同运行。
- 官方最简单的“可用系统”运行方式是 Docker Compose 一键拉起这些组件；但你这台机器目前 Docker/WSL2 无法工作（报 `HCS_E_HYPERV_NOT_INSTALLED`），所以后端起不来，就无法使用完整功能。

## 你需要做什么，才能用上完整功能（推荐路径，尽量不用 C 盘）

1. 让 Windows 具备运行 WSL2 / Linux 容器的能力
   - BIOS/UEFI 打开虚拟化：Intel VT-x / AMD-V / SVM（不同主板名字不同）
   - Windows 功能开启（需要管理员权限，启用后通常要重启）
     - “虚拟机平台 (Virtual Machine Platform)”
     - “适用于 Linux 的 Windows 子系统 (Windows Subsystem for Linux)”
     - 视机型/系统版本可能还需要 “Hyper-V”
2. 安装一个 WSL 发行版（例如 Ubuntu），确保 `wsl -l -v` 能看到已安装发行版且版本为 2
   - 为了避免把发行版的数据放在 C 盘，可以不用 `wsl --install -d Ubuntu-22.04`，改用：
     - 在 `D:\Documents\04_GitRepos\wsl\Ubuntu-22.04\` 作为发行版家目录
     - 在 `D:\Documents\04_GitRepos\wsl\` 下下载 rootfs（例如 `ubuntu-22.04.rootfs.tar.gz`）
     - 使用：`wsl --import Ubuntu-22.04 D:\Documents\04_GitRepos\wsl\Ubuntu-22.04 D:\Documents\04_GitRepos\wsl\ubuntu-22.04.rootfs.tar.gz --version 2`
   - 目前已验证：rootfs 已成功下载到 D 盘，但由于物理机 BIOS 未启用虚拟化，`wsl --import` 报 `HCS_E_HYPERV_NOT_INSTALLED`，即：**WSL2 仍然无法真正创建虚拟机环境**，这一步必须在 BIOS 开启虚拟化后由你重新执行。
3. 安装并启动 Docker Desktop（选择 WSL2 backend）
4. 在 `D:\Documents\04_GitRepos\immich-app\` 执行 `docker compose up -d`
5. 浏览器访问 `http://localhost:2283`，注册第一个用户并上传照片验收

## 如果你没法开虚拟化（公司电脑/BIOS锁/无管理员权限）

- 方案 A：换一台能跑 Docker 的机器（或 NAS、Linux 主机）部署 Immich，然后手机/电脑访问它
- 方案 B：只做“UI/代码阅读/二次开发”，继续用 `pnpm dev` 看页面，但这不等于可用相册系统
- 方案 C：用在线演示环境进行功能体验（适合快速验收交互，但不适合存你自己的照片）

## 生产部署（Docker Compose 推荐）需要满足的条件

- 安装并启动 Docker（需支持 `docker compose`，Compose v2）
- Windows 需要启用虚拟化相关能力（Virtual Machine Platform/BIOS 虚拟化等），否则无法运行 Linux 容器
- 启动后默认访问：`http://localhost:2283`

## 常见问题速查

- `TLS handshake timeout`：Docker 拉取镜像超时，请检查是否开启 VPN 全局代理或 TUN 模式。
- `docker : 无法将“docker”项识别为 ...`：未安装 Docker 或未加入 PATH
- WSL2 报 `HCS_E_HYPERV_NOT_INSTALLED`：虚拟化/Hyper-V 平台不可用；需启用系统组件并在 BIOS 打开虚拟化
- `can't set healthcheck.start_interval ... require Docker Engine v25 or later`：Docker Engine 版本偏低；可临时注释 compose 中数据库 healthcheck 的 `start_interval`
- `unknown shorthand flag: 'd' in -d`：使用了错误的 Docker/Compose 版本；应使用 `docker compose`（v2），不是 `docker-compose`（v1）

