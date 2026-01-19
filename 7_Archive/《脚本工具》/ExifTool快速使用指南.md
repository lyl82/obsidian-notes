# 🚀 ExifTool 快速使用指南

## 📦 你的安装信息

- **ExifTool 路径**: `F:\downloadforsetup\exiftool-13.45_64\exiftool.exe`
- **版本**: 13.45
- **状态**: ✅ 已安装并可用

---

## 🎯 最常用的5个命令

### 1️⃣ 查看单个视频的所有信息
```bash
F:\downloadforsetup\exiftool-13.45_64\exiftool.exe -G1 "D:\个人记录\VID_20240905_141626.mp4"
```

### 2️⃣ 只看时间和GPS
```bash
F:\downloadforsetup\exiftool-13.45_64\exiftool.exe -CreateDate -GPSLatitude -GPSLongitude "D:\个人记录\VID_20240905_141626.mp4"
```

### 3️⃣ 批量导出所有视频到CSV
```bash
F:\downloadforsetup\exiftool-13.45_64\exiftool.exe -csv -r -ext mp4 -ext mov "D:\个人记录" > metadata.csv
```

### 4️⃣ 查找有GPS的视频
```bash
F:\downloadforsetup\exiftool-13.45_64\exiftool.exe -if "$GPSLatitude" -FileName -GPSPosition -r "D:\个人记录"
```

### 5️⃣ JSON格式输出（给程序用）
```bash
F:\downloadforsetup\exiftool-13.45_64\exiftool.exe -json -G "D:\个人记录\VID_20240905_141626.mp4"
```

---

## 🖱️ 更简单的方式：使用批处理脚本

我已经为你创建了一个图形化菜单脚本：

### 📝 使用方法
1. 双击运行：`exiftool_常用命令.bat`
2. 根据菜单提示选择操作
3. 输入视频路径或目录
4. 查看结果

### 菜单选项
```
1. 查看单个视频的完整元数据
2. 提取单个视频的时间和GPS信息
3. 批量导出所有视频元数据到CSV
4. 查找包含GPS信息的视频
5. 查找缺少时间戳的视频
6. 导出JSON格式（便于程序处理）
7. 退出
```

---

## 📊 你的视频分析结果摘要

### 统计数据
- ✅ **有GPS的视频**: 8个 → 可以看到拍摄地点
- ⏰ **有时间戳的视频**: 8个 → 知道具体拍摄时间
- ⚠️ **缺少元数据的视频**: 16个 → 在"锻炼"文件夹里

### 主要拍摄地点
1. **湖南省衡阳市** (26.88°N, 112.54°E) - 5个视频
2. **广东省中山市** (22.93°N, 113.28°E) - 1个视频
3. **广东省深圳市** (22.62°N, 114.11°E) - 1个视频

### 设备信息
从元数据中识别到的拍摄设备：
- **品牌**: Xiaomi (小米)
- **型号**: Redmi K70
- **系统**: Android 14

---

## 🔍 实用案例

### 案例1：查找2024年10月的所有视频
```bash
F:\downloadforsetup\exiftool-13.45_64\exiftool.exe -if "$CreateDate =~ /2024:10/" -FileName -CreateDate -r "D:\个人记录"
```

### 案例2：查找在衡阳拍摄的视频
```bash
F:\downloadforsetup\exiftool-13.45_64\exiftool.exe -if "$GPSLatitude =~ /26 deg 53/" -FileName -GPSPosition -CreateDate -r "D:\个人记录"
```

### 案例3：查找4K视频
```bash
F:\downloadforsetup\exiftool-13.45_64\exiftool.exe -if "$ImageWidth >= 3840" -FileName -ImageWidth -ImageHeight -FileSize -r "D:\个人记录"
```

### 案例4：查找超过10分钟的长视频
```bash
F:\downloadforsetup\exiftool-13.45_64\exiftool.exe -if "$Duration# > 600" -FileName -Duration -FileSize -r "D:\个人记录"
```

### 案例5：按拍摄时间重命名视频
```bash
# ⚠️ 会修改文件名，请先备份！
F:\downloadforsetup\exiftool-13.45_64\exiftool.exe "-FileName<CreateDate" -d "%Y%m%d_%H%M%S%%e" "D:\个人记录\*.mp4"
```

---

## 🛠️ 常用参数速查

| 参数 | 作用 | 示例 |
|------|------|------|
| `-G1` | 显示标签分组 | `-G1` |
| `-json` | JSON格式输出 | `-json` |
| `-csv` | CSV格式输出 | `-csv` |
| `-r` | 递归处理子目录 | `-r` |
| `-ext mp4` | 只处理mp4文件 | `-ext mp4` |
| `-if` | 条件过滤 | `-if "$GPSLatitude"` |
| `-CreateDate` | 只显示创建时间 | `-CreateDate` |
| `-GPS*` | 显示所有GPS字段 | `-GPS*` |
| `-time:all` | 显示所有时间字段 | `-time:all` |

---

## 📱 如何确保视频包含完整元数据

### ✅ 推荐做法
1. **使用手机原生相机录制**
   - 原生相机App会保留完整的GPS和时间信息
   - 确保开启"位置信息"权限

2. **直接从手机导出**
   - 使用USB数据线传输
   - 避免使用会压缩的云盘

3. **不要用第三方工具编辑**
   - 很多视频编辑软件会移除元数据
   - 如需编辑，选择"保留元数据"选项

### ⚠️ 避免做法
- ❌ 通过微信/QQ发送（会压缩并移除元数据）
- ❌ 使用某些视频编辑App
- ❌ 从视频网站下载
- ❌ 使用"视频转换器"转格式

---

## 🔧 故障排除

### 问题1：中文路径乱码
**解决方案**：
```bash
# 方法1：使用UTF-8编码
F:\downloadforsetup\exiftool-13.45_64\exiftool.exe -charset filename=utf8 "视频.mp4"

# 方法2：使用短文件名（Windows）
F:\downloadforsetup\exiftool-13.45_64\exiftool.exe "D:\GERENJ~1\VID_20240905_141626.mp4"
```

### 问题2：提示"找不到指定文件"
**检查清单**：
- ✅ 路径是否正确？
- ✅ 文件名是否包含特殊字符？
- ✅ 是否用引号包围路径？

### 问题3：GPS信息为空
**可能原因**：
1. 录制时未开启定位权限
2. 视频经过编辑或转码
3. 从社交平台下载的视频
4. 室内录制时GPS信号弱

---

## 📚 相关文档

- **详细分析报告**: `视频元数据分析报告.md`
- **完整使用说明**: `ExifTool使用说明.md`
- **Python脚本**: `run_exiftool_test.py`
- **批处理脚本**: `exiftool_常用命令.bat`
- **CSV报告**: `video_metadata_report.csv`

---

## 💡 高级技巧

### 1. 批量修改元数据
```bash
# 添加版权信息
F:\downloadforsetup\exiftool-13.45_64\exiftool.exe -Copyright="Your Name" *.mp4

# 修改GPS坐标（如果需要）
F:\downloadforsetup\exiftool-13.45_64\exiftool.exe -GPSLatitude=26.88 -GPSLongitude=112.54 video.mp4
```

### 2. 提取视频缩略图
```bash
F:\downloadforsetup\exiftool-13.45_64\exiftool.exe -b -PreviewImage video.mp4 > thumbnail.jpg
```

### 3. 对比两个视频的元数据差异
```bash
F:\downloadforsetup\exiftool-13.45_64\exiftool.exe -json video1.mp4 video2.mp4 > compare.json
```

### 4. 生成HTML报告
```bash
F:\downloadforsetup\exiftool-13.45_64\exiftool.exe -h -r "D:\个人记录" > report.html
```

---

**🎉 现在你已经掌握了ExifTool的使用方法！**

有任何问题，参考完整文档：https://exiftool.org/
