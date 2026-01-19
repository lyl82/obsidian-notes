# ExifTool 视频元数据提取使用说明

## 一、ExifTool 简介

ExifTool 是一个强大的跨平台命令行工具，用于读取、写入和编辑各种文件格式的元数据信息，包括图片、视频、音频等。

### 主要特点
- 支持超过 200 种文件格式
- 可读取、写入和编辑元数据
- 支持多种元数据标准（EXIF、GPS、IPTC、XMP、JFIF等）
- 完全免费、开源
- 跨平台（Windows、macOS、Linux）

---

## 二、安装配置步骤

### Windows 系统安装

#### 方法1：下载独立可执行文件（推荐）

1. **下载 ExifTool**
   - 访问官网：https://exiftool.org/
   - 下载 Windows 版本：https://exiftool.org/exiftool-12.70.zip
   - 当前最新版本通常在首页显示

2. **解压并重命名**
   ```
   - 解压下载的 ZIP 文件
   - 找到 "exiftool(-k).exe"
   - 重命名为 "exiftool.exe"
   ```

3. **配置系统 PATH（可选但推荐）**
   
   **方法 A：放到已有 PATH 目录**
   ```
   将 exiftool.exe 复制到：
   C:\Windows\System32\
   ```
   
   **方法 B：添加新的 PATH 路径**
   ```
   1. 创建目录：C:\Tools\exiftool\
   2. 将 exiftool.exe 放入该目录
   3. 右键"此电脑" → 属性 → 高级系统设置
   4. 环境变量 → 系统变量 → 找到 Path → 编辑
   5. 新建 → 输入：C:\Tools\exiftool\
   6. 确定保存
   ```

4. **验证安装**
   ```powershell
   # 打开 PowerShell 或 CMD
   exiftool -ver
   ```
   显示版本号即为安装成功

#### 方法2：使用包管理器

```powershell
# 使用 Chocolatey
choco install exiftool

# 使用 Scoop
scoop install exiftool
```

### macOS 系统安装

```bash
# 使用 Homebrew
brew install exiftool

# 验证安装
exiftool -ver
```

### Linux 系统安装

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install libimage-exiftool-perl

# CentOS/RHEL
sudo yum install perl-Image-ExifTool

# Arch Linux
sudo pacman -S perl-image-exiftool

# 验证安装
exiftool -ver
```

---

## 三、基本命令行使用

### 3.1 查看完整元数据

```bash
# 查看单个文件的所有元数据
exiftool video.mp4

# 查看时带分组标签（推荐）
exiftool -G video.mp4

# 查看时带详细分组
exiftool -G1 video.mp4
```

### 3.2 输出 JSON 格式

```bash
# JSON 格式输出（便于程序解析）
exiftool -json video.mp4

# JSON + 分组标签
exiftool -json -G video.mp4

# 输出到文件
exiftool -json video.mp4 > metadata.json
```

### 3.3 提取特定字段

```bash
# 提取创建时间
exiftool -CreateDate video.mp4

# 提取 GPS 信息
exiftool -GPS* video.mp4

# 提取多个字段
exiftool -CreateDate -GPSLatitude -GPSLongitude video.mp4

# 只显示值，不显示字段名
exiftool -s -s -s -CreateDate video.mp4
```

### 3.4 批量处理

```bash
# 处理目录下所有 MP4 文件
exiftool *.mp4

# 递归处理子目录
exiftool -r D:\个人记录\

# 只处理特定格式
exiftool -ext mp4 -ext mov -r D:\个人记录\

# 批量输出到 CSV
exiftool -csv -r D:\个人记录\ > video_metadata.csv
```

### 3.5 常用参数说明

| 参数 | 说明 |
|------|------|
| `-a` | 显示重复的标签 |
| `-G` | 显示标签的分组名称 |
| `-G1` | 显示标签的分组名称（简化） |
| `-s` | 短格式输出（只显示字段名） |
| `-s -s -s` | 只输出值 |
| `-json` | JSON 格式输出 |
| `-csv` | CSV 格式输出 |
| `-r` | 递归处理子目录 |
| `-ext <扩展名>` | 指定文件扩展名 |
| `-n` | 显示原始数值（不转换） |
| `-b` | 以二进制形式输出 |
| `-charset utf8` | 指定字符编码 |

---

## 四、时间戳信息提取

### 4.1 视频文件常见时间字段

#### QuickTime/MP4 格式
```bash
# 查看所有时间相关字段
exiftool -time:all video.mp4

# 常见字段：
CreateDate              # 创建时间
ModifyDate             # 修改时间
TrackCreateDate        # 轨道创建时间
TrackModifyDate        # 轨道修改时间
MediaCreateDate        # 媒体创建时间
MediaModifyDate        # 媒体修改时间
```

#### 文件系统时间
```bash
FileModifyDate         # 文件修改日期
FileAccessDate         # 文件访问日期
FileCreateDate         # 文件创建日期（Windows）
```

### 4.2 提取时间示例

```bash
# 提取所有时间信息
exiftool -time:all -G1 video.mp4

# 提取创建时间
exiftool -CreateDate -MediaCreateDate video.mp4

# 批量提取并保存到 CSV
exiftool -csv -CreateDate -ModifyDate -FileModifyDate *.mp4 > times.csv
```

### 4.3 时间格式解析

ExifTool 输出的时间格式通常为：
```
2024:09:05 14:16:26
```

Python 解析示例：
```python
from datetime import datetime

# ExifTool 时间格式
time_str = "2024:09:05 14:16:26"
dt = datetime.strptime(time_str, "%Y:%m:%d %H:%M:%S")
print(dt)  # 2024-09-05 14:16:26
```

---

## 五、地理位置信息提取

### 5.1 GPS 相关字段

```bash
# 查看所有 GPS 信息
exiftool -GPS* video.mp4

# 常见字段：
GPSLatitude            # 纬度
GPSLongitude           # 经度
GPSAltitude            # 海拔高度
GPSLatitudeRef         # 纬度参考（N/S）
GPSLongitudeRef        # 经度参考（E/W）
GPSAltitudeRef         # 海拔参考
GPSTimeStamp           # GPS 时间戳
GPSDateStamp           # GPS 日期戳
GPSSpeed               # 速度
GPSTrack               # 移动方向
```

### 5.2 提取地理位置示例

```bash
# 提取 GPS 坐标
exiftool -GPSLatitude -GPSLongitude -GPSAltitude video.mp4

# 提取组合位置（自动计算十进制度数）
exiftool -GPSPosition video.mp4

# 批量提取地理位置
exiftool -csv -GPSLatitude -GPSLongitude -GPSAltitude *.mp4 > gps.csv
```

### 5.3 坐标格式转换

ExifTool 显示的坐标格式：
```
GPS Latitude  : 39 deg 54' 49.35" N
GPS Longitude : 116 deg 23' 30.69" E
GPS Position  : 39.9137083, 116.3918583
```

Python 转换示例：
```python
def dms_to_decimal(degrees, minutes, seconds, direction):
    """将度分秒转换为十进制度数"""
    decimal = degrees + minutes/60 + seconds/3600
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

# 示例
lat = dms_to_decimal(39, 54, 49.35, 'N')
lon = dms_to_decimal(116, 23, 30.69, 'E')
print(f"纬度: {lat}, 经度: {lon}")
```

---

## 六、不同格式兼容性测试

### 6.1 支持的视频格式

| 格式 | 扩展名 | 元数据支持 | GPS 支持 | 备注 |
|------|--------|-----------|---------|------|
| MP4 | .mp4 | ✅ 完整 | ✅ 支持 | 最常见格式，支持最好 |
| MOV | .mov | ✅ 完整 | ✅ 支持 | QuickTime 格式 |
| AVI | .avi | ⚠️ 有限 | ❌ 不支持 | 较老格式，元数据支持有限 |
| MKV | .mkv | ✅ 完整 | ⚠️ 部分 | Matroska 格式 |
| WMV | .wmv | ⚠️ 有限 | ❌ 不支持 | Windows Media 格式 |
| FLV | .flv | ⚠️ 有限 | ❌ 不支持 | Flash 视频格式 |
| 3GP | .3gp | ✅ 完整 | ⚠️ 部分 | 移动设备格式 |

### 6.2 兼容性测试脚本

```bash
# 测试目录下所有视频格式
exiftool -ext mp4 -ext mov -ext avi -ext mkv -r -csv D:\个人记录\ > format_test.csv

# 查看每个文件的格式信息
exiftool -FileType -MIMEType -r D:\个人记录\
```

### 6.3 常见问题

#### 问题1：中文路径乱码
```bash
# 使用 UTF-8 编码
exiftool -charset filename=utf8 视频.mp4
```

#### 问题2：某些字段无法读取
```bash
# 使用 -a 参数显示所有重复标签
exiftool -a -G1 video.mp4

# 使用 -ee 参数提取更多元数据
exiftool -ee -G1 video.mp4
```

#### 问题3：大文件处理慢
```bash
# 只提取需要的字段，避免处理全部数据
exiftool -fast -CreateDate -GPSLatitude -GPSLongitude video.mp4
```

---

## 七、Python 集成使用

### 7.1 使用 subprocess 调用

见 `exiftool_video_test.py` 脚本

### 7.2 使用 PyExifTool 库

```bash
# 安装
pip install PyExifTool
```

```python
import exiftool

with exiftool.ExifToolHelper() as et:
    # 读取元数据
    metadata = et.get_metadata("video.mp4")
    
    # 提取特定字段
    for d in metadata:
        print(f"创建时间: {d.get('QuickTime:CreateDate')}")
        print(f"GPS位置: {d.get('Composite:GPSPosition')}")
```

---

## 八、实际使用案例

### 8.1 提取视频拍摄时间

```bash
exiftool -CreateDate -MediaCreateDate -FileModifyDate -csv *.mp4 > video_times.csv
```

### 8.2 查找带 GPS 信息的视频

```bash
exiftool -if "$GPSLatitude" -FileName -GPSPosition -r D:\个人记录\
```

### 8.3 按拍摄时间重命名视频

```bash
# 将视频重命名为：2024-09-05_141626.mp4
exiftool "-FileName<CreateDate" -d "%Y-%m-%d_%H%M%S%%e" *.mp4
```

### 8.4 提取设备信息

```bash
exiftool -Make -Model -Software -csv *.mp4 > devices.csv
```

---

## 九、测试脚本使用

### 9.1 运行测试脚本

```bash
# 确保已安装 ExifTool
exiftool -ver

# 运行测试脚本
python exiftool_video_test.py
```

### 9.2 脚本功能

1. ✅ 自动检测 ExifTool 是否安装
2. ✅ 提供详细的安装指南
3. ✅ 单个视频文件分析
4. ✅ 批量目录分析
5. ✅ 提取时间戳信息
6. ✅ 提取地理位置信息
7. ✅ 提取设备信息
8. ✅ 生成格式化报告
9. ✅ 格式兼容性统计

### 9.3 自定义测试

修改 `exiftool_video_test.py` 中的路径：

```python
# 单个文件测试
test_video = r"D:\个人记录\VID_20240905_141626.mp4"

# 批量分析目录
target_directory = r"D:\个人记录"

# 指定文件格式
extensions = ['.mp4', '.mov', '.avi']
```

---

## 十、性能优化建议

### 10.1 快速模式

```bash
# 使用 -fast 参数跳过某些元数据
exiftool -fast video.mp4
```

### 10.2 并行处理

```bash
# Windows PowerShell 并行处理
Get-ChildItem *.mp4 | ForEach-Object -Parallel {
    exiftool $_.FullName
} -ThrottleLimit 4
```

### 10.3 缓存结果

```python
import json
import os

def get_metadata_cached(video_path, cache_file="metadata_cache.json"):
    """带缓存的元数据提取"""
    cache = {}
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache = json.load(f)
    
    if video_path in cache:
        return cache[video_path]
    
    # 提取元数据
    # ... (使用 exiftool)
    
    # 保存到缓存
    cache[video_path] = metadata
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
    
    return metadata
```

---

## 十一、参考资源

- **官方网站**: https://exiftool.org/
- **完整文档**: https://exiftool.org/exiftool_pod.html
- **标签名称**: https://exiftool.org/TagNames/
- **常见问题**: https://exiftool.org/faq.html
- **论坛支持**: https://exiftool.org/forum/

---

## 十二、总结

### 优点
- ✅ 功能强大，支持格式广泛
- ✅ 完全免费开源
- ✅ 跨平台支持
- ✅ 命令行接口便于自动化
- ✅ 输出格式多样（文本、JSON、CSV等）

### 局限性
- ⚠️ 依赖视频文件本身是否包含元数据
- ⚠️ 某些格式（如 AVI）元数据支持有限
- ⚠️ 大文件处理速度较慢
- ⚠️ 需要学习命令行参数

### 最佳实践
1. 优先使用 JSON 格式输出，便于程序解析
2. 使用 `-G1` 参数查看标签分组
3. 批量处理时使用 CSV 格式
4. 缓存元数据结果避免重复处理
5. 针对特定需求只提取必要字段

---

**更新时间**: 2024-12-29
