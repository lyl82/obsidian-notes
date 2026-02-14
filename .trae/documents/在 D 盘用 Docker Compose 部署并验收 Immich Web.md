## 目标

* 在 `D:\Documents\04_GitRepos` 下完成 Immich 的本地部署与启动，并在 Web 端验收“页面正常显示”（访问 `http://localhost:2283`）。

## 前置条件

* 任何的前置，中间间下载安装不要按默认在c盘，而是D:\Documents\04\_GitRepos。

- 安装并启动 Docker Desktop（启用 Docker Compose v2；命令应为 `docker compose` 而不是 `docker-compose`）。

- 机器资源建议至少 6GB 内存、2 核 CPU（官方 quick start 要求）。

## 目录与文件落点（不使用 C 盘）

* 运行目录：`D:\Documents\04_GitRepos\immich-app\`

* 媒体库目录（持久化上传文件）：`D:\Documents\04_GitRepos\immich-app\library\`

* 数据库目录（持久化 Postgres）：`D:\Documents\04_GitRepos\immich-app\postgres\`

## 部署步骤（推荐 Docker Compose）

1. 在 `D:\Documents\04_GitRepos\immich-app\` 创建 `docker-compose.yml` 与 `.env`：

   * 从 Immich release “latest” 下载 `docker-compose.yml` 与 `example.env`（重命名为 `.env`）。
2. 编辑 `.env`：

   * 设置 `UPLOAD_LOCATION` 指向 `D:\Documents\04_GitRepos\immich-app\library`。

   * 设置 `DB_DATA_LOCATION` 指向 `D:\Documents\04_GitRepos\immich-app\postgres`。

   * 将 `DB_PASSWORD` 改为随机值（建议仅用 `A-Za-z0-9` 以避免 Docker 解析问题）。

   * 需要的话设置 `TZ`。
3. 启动：在该目录执行 `docker compose up -d`。
4. 验收：

   * 浏览器打开 `http://localhost:2283`，确认登录/注册页可正常加载。

   * 注册第一个用户作为管理员，登录后尝试上传 1 张图片验证基本链路。

## 常见问题处理

* 如果遇到 `unknown shorthand flag: 'd' in -d` 或提示 `.env` 权限问题：通常是 Docker/Compose 版本不对，需确保使用 Docker Desktop/官方 Docker Engine，并使用 `docker compose`。

* 如果遇到 `can't set healthcheck.start_interval ... require Docker Engine v25 or later`：临时注释 compose 里数据库的 `start_interval` 行，再重启。

* 拉取镜像失败：可能需要对 GitHub Container Registry 登录（`ghcr.io`）。

## 可选：源码方式（仅当你要二次开发）

* 另行在 `D:\Documents\04_GitRepos\immich\` 克隆源码仓库，用于阅读/修改；运行生产推荐仍用上面的 release compose 文件。

## 我需要你确认的 2 个点（其余我按默认执行）

* 端口 `2283` 在你机器上是否可用（若冲突我会改映射端口）。

* 你希望 `library` 实际存储位置是否仍放在 `D:\Documents\04_GitRepos\immich-app\library`（或你有更大的磁盘路径）。

