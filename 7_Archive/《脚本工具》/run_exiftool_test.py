"""
ExifTool 视频元数据提取 - 简化执行版本
处理中文路径，直接使用已安装的 ExifTool
"""

import subprocess
import json
import os
from pathlib import Path
from datetime import datetime


class VideoAnalyzer:
    """视频元数据分析器"""
    
    def __init__(self):
        self.exiftool_path = r"F:\downloadforsetup\exiftool-13.45_64\exiftool.exe"
        print(f"✓ 使用 ExifTool: {self.exiftool_path}")
        self._check_version()
    
    def _check_version(self):
        """检查版本"""
        result = subprocess.run(
            [self.exiftool_path, "-ver"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✓ ExifTool 版本: {result.stdout.strip()}\n")
    
    def extract_metadata(self, video_path):
        """提取元数据"""
        try:
            # 使用 -charset 参数处理中文路径
            result = subprocess.run(
                [
                    self.exiftool_path,
                    "-json",
                    "-G",
                    "-charset", "filename=utf8",
                    video_path
                ],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=30
            )
            
            if result.returncode == 0:
                metadata = json.loads(result.stdout)
                return metadata[0] if metadata else {}
            else:
                print(f"错误: {result.stderr}")
                return {}
        except Exception as e:
            print(f"提取失败: {e}")
            return {}
    
    def format_gps(self, gps_str):
        """格式化GPS坐标为十进制度数"""
        if not gps_str:
            return None
        
        try:
            # 解析如: "26 deg 53' 2.76" N"
            import re
            match = re.search(r'(\d+)\s+deg\s+(\d+)\'\s+([\d.]+)"?\s*([NSEW])?', gps_str)
            if match:
                deg, min_, sec, direction = match.groups()
                decimal = float(deg) + float(min_)/60 + float(sec)/3600
                if direction in ['S', 'W']:
                    decimal = -decimal
                return round(decimal, 6)
        except:
            pass
        return gps_str
    
    def print_report(self, video_path):
        """打印分析报告"""
        print("=" * 80)
        print(f"📹 视频文件: {os.path.basename(video_path)}")
        print("=" * 80)
        
        if not os.path.exists(video_path):
            print(f"❌ 文件不存在: {video_path}\n")
            return
        
        metadata = self.extract_metadata(video_path)
        
        if not metadata:
            print("❌ 无法提取元数据\n")
            return
        
        # 基本信息
        print("\n【📊 基本信息】")
        print(f"  文件格式: {metadata.get('File:FileType', 'Unknown')}")
        print(f"  文件大小: {metadata.get('File:FileSize', 'Unknown')}")
        print(f"  分辨率: {metadata.get('QuickTime:ImageWidth', '?')} x {metadata.get('QuickTime:ImageHeight', '?')}")
        print(f"  时长: {metadata.get('QuickTime:Duration', 'Unknown')}")
        print(f"  帧率: {metadata.get('QuickTime:VideoFrameRate', 'Unknown')} fps")
        print(f"  比特率: {metadata.get('Composite:AvgBitrate', 'Unknown')}")
        
        # 时间信息
        print("\n【⏰ 时间信息】")
        create_date = metadata.get('QuickTime:CreateDate')
        modify_date = metadata.get('QuickTime:ModifyDate')
        file_date = metadata.get('File:FileModifyDate')
        
        if create_date:
            print(f"  拍摄时间: {create_date}")
        if modify_date:
            print(f"  修改时间: {modify_date}")
        if file_date:
            print(f"  文件时间: {file_date}")
        
        if not (create_date or modify_date):
            print("  ⚠️  未找到拍摄时间")
        
        # GPS信息
        print("\n【🌍 地理位置】")
        gps_position = metadata.get('Composite:GPSPosition') or metadata.get('QuickTime:GPSCoordinates')
        gps_lat = metadata.get('Composite:GPSLatitude')
        gps_lon = metadata.get('Composite:GPSLongitude')
        
        if gps_position:
            print(f"  GPS坐标: {gps_position}")
            if gps_lat and gps_lon:
                lat_decimal = self.format_gps(gps_lat)
                lon_decimal = self.format_gps(gps_lon)
                print(f"  十进制: {lat_decimal}, {lon_decimal}")
                # 生成地图链接
                if lat_decimal and lon_decimal:
                    map_url = f"https://www.google.com/maps?q={lat_decimal},{lon_decimal}"
                    print(f"  地图: {map_url}")
        else:
            print("  ⚠️  未找到GPS信息")
        
        # 设备信息
        print("\n【📱 设备信息】")
        make = metadata.get('QuickTime:AndroidMake') or metadata.get('QuickTime:Make')
        model = metadata.get('QuickTime:AndroidModel') or metadata.get('QuickTime:Model')
        market_name = metadata.get('QuickTime:XiaomiProductMarketname')
        
        if make:
            print(f"  制造商: {make}")
        if model:
            print(f"  设备型号: {model}")
        if market_name:
            print(f"  产品名称: {market_name}")
        
        if not (make or model):
            print("  ⚠️  未找到设备信息")
        
        print("\n" + "=" * 80 + "\n")
    
    def batch_analyze(self, directory, extensions=['.mp4', '.mov']):
        """批量分析"""
        print(f"\n🔍 扫描目录: {directory}")
        print("-" * 80)
        
        directory_path = Path(directory)
        if not directory_path.exists():
            print(f"❌ 目录不存在: {directory}\n")
            return
        
        # 查找视频文件
        video_files = []
        for ext in extensions:
            video_files.extend(list(directory_path.glob(f"*{ext}")))
            video_files.extend(list(directory_path.glob(f"*{ext.upper()}")))
        
        video_files = sorted(set(video_files))
        
        print(f"✓ 找到 {len(video_files)} 个视频文件\n")
        
        if not video_files:
            print("⚠️  没有找到视频文件\n")
            return
        
        # 分析每个文件
        stats = {
            'total': len(video_files),
            'with_gps': 0,
            'with_time': 0,
            'with_device': 0
        }
        
        for video_file in video_files:
            self.print_report(str(video_file))
            
            # 统计
            metadata = self.extract_metadata(str(video_file))
            if metadata.get('Composite:GPSPosition') or metadata.get('QuickTime:GPSCoordinates'):
                stats['with_gps'] += 1
            if metadata.get('QuickTime:CreateDate'):
                stats['with_time'] += 1
            if metadata.get('QuickTime:AndroidMake') or metadata.get('QuickTime:Make'):
                stats['with_device'] += 1
        
        # 打印统计
        print("=" * 80)
        print("📈 统计报告")
        print("=" * 80)
        print(f"总文件数: {stats['total']}")
        print(f"包含GPS信息: {stats['with_gps']} ({stats['with_gps']/stats['total']*100:.1f}%)")
        print(f"包含时间信息: {stats['with_time']} ({stats['with_time']/stats['total']*100:.1f}%)")
        print(f"包含设备信息: {stats['with_device']} ({stats['with_device']/stats['total']*100:.1f}%)")
        print("=" * 80 + "\n")


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("🎬 ExifTool 视频元数据分析工具")
    print("=" * 80 + "\n")
    
    analyzer = VideoAnalyzer()
    
    # 测试1: 分析单个文件
    print("\n【测试1：单个文件分析】")
    test_file = r"D:\个人记录\VID_20240905_141626.mp4"
    analyzer.print_report(test_file)
    
    # 测试2: 分析"锻炼"文件夹
    print("\n【测试2：批量分析 - 锻炼文件夹】")
    analyzer.batch_analyze(r"D:\个人记录\锻炼", extensions=['.mp4'])
    
    # 测试3: 分析根目录的视频
    print("\n【测试3：批量分析 - 根目录视频】")
    analyzer.batch_analyze(r"D:\个人记录", extensions=['.mp4', '.mov'])
    
    print("✅ 所有测试完成！")


if __name__ == "__main__":
    main()
