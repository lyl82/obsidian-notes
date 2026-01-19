"""
ExifTool 视频元数据提取测试脚本

功能：
1. 使用 ExifTool 提取视频文件的元数据信息
2. 重点提取时间戳和地理位置数据
3. 测试不同格式视频文件的兼容性（MP4/MOV）
4. 生成结构化的元数据报告

使用前提：
- 需要先安装 ExifTool：https://exiftool.org/
- Windows 下载：https://exiftool.org/exiftool-12.70.zip
- 将 exiftool(-k).exe 重命名为 exiftool.exe 并添加到系统 PATH
"""

import subprocess
import json
import os
from pathlib import Path
from datetime import datetime
import re


class VideoMetadataExtractor:
    """视频元数据提取器"""
    
    def __init__(self, exiftool_path="exiftool"):
        """
        初始化提取器
        
        Args:
            exiftool_path: exiftool 可执行文件路径，默认为系统 PATH 中的 exiftool
        """
        self.exiftool_path = exiftool_path
        self._check_exiftool()
    
    def _check_exiftool(self):
        """检查 ExifTool 是否已安装"""
        try:
            result = subprocess.run(
                [self.exiftool_path, "-ver"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✓ ExifTool 已安装，版本: {version}")
            else:
                print("✗ ExifTool 未正确安装")
                self._print_install_guide()
        except FileNotFoundError:
            print("✗ ExifTool 未找到")
            self._print_install_guide()
        except Exception as e:
            print(f"✗ 检查 ExifTool 时出错: {e}")
            self._print_install_guide()
    
    def _print_install_guide(self):
        """打印安装指南"""
        print("\n" + "="*60)
        print("ExifTool 安装指南：")
        print("="*60)
        print("1. 访问: https://exiftool.org/")
        print("2. 下载 Windows 版本: https://exiftool.org/exiftool-12.70.zip")
        print("3. 解压后将 'exiftool(-k).exe' 重命名为 'exiftool.exe'")
        print("4. 将 exiftool.exe 放到以下任一位置：")
        print("   - 当前脚本目录")
        print("   - 或添加到系统 PATH 环境变量")
        print("5. 重新运行此脚本")
        print("="*60 + "\n")
    
    def extract_metadata_json(self, video_path):
        """
        提取视频元数据（JSON 格式）
        
        Args:
            video_path: 视频文件路径
            
        Returns:
            dict: 元数据字典
        """
        try:
            result = subprocess.run(
                [self.exiftool_path, "-json", "-G", video_path],
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                metadata = json.loads(result.stdout)
                return metadata[0] if metadata else {}
            else:
                print(f"错误: {result.stderr}")
                return {}
        except subprocess.TimeoutExpired:
            print(f"超时: 处理 {video_path} 超过 30 秒")
            return {}
        except json.JSONDecodeError as e:
            print(f"JSON 解析错误: {e}")
            return {}
        except Exception as e:
            print(f"提取元数据时出错: {e}")
            return {}
    
    def extract_metadata_text(self, video_path):
        """
        提取视频元数据（文本格式）
        
        Args:
            video_path: 视频文件路径
            
        Returns:
            str: 元数据文本
        """
        try:
            result = subprocess.run(
                [self.exiftool_path, "-a", "-G1", video_path],
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                return f"错误: {result.stderr}"
        except Exception as e:
            return f"提取元数据时出错: {e}"
    
    def extract_datetime_info(self, metadata):
        """
        提取时间相关信息
        
        Args:
            metadata: 元数据字典
            
        Returns:
            dict: 时间信息字典
        """
        datetime_info = {}
        
        # 常见的时间字段
        datetime_fields = [
            'File:FileModifyDate',
            'File:FileCreateDate',
            'QuickTime:CreateDate',
            'QuickTime:ModifyDate',
            'QuickTime:TrackCreateDate',
            'QuickTime:TrackModifyDate',
            'QuickTime:MediaCreateDate',
            'QuickTime:MediaModifyDate',
            'XMP:CreateDate',
            'XMP:ModifyDate',
            'EXIF:CreateDate',
            'EXIF:ModifyDate',
            'EXIF:DateTimeOriginal'
        ]
        
        for field in datetime_fields:
            if field in metadata:
                datetime_info[field] = metadata[field]
        
        return datetime_info
    
    def extract_location_info(self, metadata):
        """
        提取地理位置信息
        
        Args:
            metadata: 元数据字典
            
        Returns:
            dict: 地理位置信息字典
        """
        location_info = {}
        
        # 常见的地理位置字段
        location_fields = [
            'Composite:GPSLatitude',
            'Composite:GPSLongitude',
            'Composite:GPSAltitude',
            'Composite:GPSPosition',
            'XMP:GPSLatitude',
            'XMP:GPSLongitude',
            'EXIF:GPSLatitude',
            'EXIF:GPSLongitude',
            'EXIF:GPSAltitude',
            'QuickTime:GPSCoordinates',
            'Keys:GPSCoordinates'
        ]
        
        for field in location_fields:
            if field in metadata:
                location_info[field] = metadata[field]
        
        return location_info
    
    def extract_video_info(self, metadata):
        """
        提取视频基本信息
        
        Args:
            metadata: 元数据字典
            
        Returns:
            dict: 视频信息字典
        """
        video_info = {
            '文件格式': metadata.get('File:FileType', 'Unknown'),
            '文件大小': metadata.get('File:FileSize', 'Unknown'),
            '视频编码': metadata.get('QuickTime:VideoCodec') or metadata.get('QuickTime:CompressorID', 'Unknown'),
            '分辨率': f"{metadata.get('QuickTime:ImageWidth', '?')}x{metadata.get('QuickTime:ImageHeight', '?')}",
            '时长': metadata.get('QuickTime:Duration', 'Unknown'),
            '帧率': metadata.get('QuickTime:VideoFrameRate', 'Unknown'),
            '比特率': metadata.get('QuickTime:AvgBitrate', 'Unknown')
        }
        
        return video_info
    
    def generate_report(self, video_path):
        """
        生成完整的元数据报告
        
        Args:
            video_path: 视频文件路径
            
        Returns:
            str: 格式化的报告文本
        """
        print(f"\n正在分析: {video_path}")
        print("-" * 80)
        
        # 检查文件是否存在
        if not os.path.exists(video_path):
            return f"错误: 文件不存在 - {video_path}"
        
        # 提取元数据
        metadata = self.extract_metadata_json(video_path)
        
        if not metadata:
            return f"警告: 无法提取 {video_path} 的元数据"
        
        # 构建报告
        report = []
        report.append("="*80)
        report.append(f"视频文件: {os.path.basename(video_path)}")
        report.append(f"完整路径: {video_path}")
        report.append("="*80)
        
        # 视频基本信息
        report.append("\n【视频基本信息】")
        video_info = self.extract_video_info(metadata)
        for key, value in video_info.items():
            report.append(f"  {key}: {value}")
        
        # 时间信息
        report.append("\n【时间戳信息】")
        datetime_info = self.extract_datetime_info(metadata)
        if datetime_info:
            for key, value in datetime_info.items():
                report.append(f"  {key}: {value}")
        else:
            report.append("  未找到时间戳信息")
        
        # 地理位置信息
        report.append("\n【地理位置信息】")
        location_info = self.extract_location_info(metadata)
        if location_info:
            for key, value in location_info.items():
                report.append(f"  {key}: {value}")
        else:
            report.append("  未找到地理位置信息")
        
        # 其他重要元数据
        report.append("\n【设备信息】")
        device_fields = [
            ('QuickTime:Make', '制造商'),
            ('QuickTime:Model', '设备型号'),
            ('QuickTime:Software', '软件版本'),
            ('XMP:CreatorTool', '创建工具')
        ]
        
        device_found = False
        for field, label in device_fields:
            if field in metadata:
                report.append(f"  {label}: {metadata[field]}")
                device_found = True
        
        if not device_found:
            report.append("  未找到设备信息")
        
        report.append("\n" + "="*80)
        
        return "\n".join(report)
    
    def batch_analyze(self, directory, extensions=['.mp4', '.mov', '.avi', '.mkv']):
        """
        批量分析目录下的视频文件
        
        Args:
            directory: 目标目录
            extensions: 要分析的文件扩展名列表
            
        Returns:
            dict: 分析结果字典
        """
        results = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'reports': []
        }
        
        directory_path = Path(directory)
        
        if not directory_path.exists():
            print(f"错误: 目录不存在 - {directory}")
            return results
        
        # 查找所有视频文件
        video_files = []
        for ext in extensions:
            video_files.extend(directory_path.glob(f"**/*{ext}"))
            video_files.extend(directory_path.glob(f"**/*{ext.upper()}"))
        
        results['total'] = len(video_files)
        
        print(f"\n找到 {results['total']} 个视频文件")
        print("="*80)
        
        for video_file in video_files:
            try:
                report = self.generate_report(str(video_file))
                results['reports'].append({
                    'file': str(video_file),
                    'report': report
                })
                results['success'] += 1
                print(report)
            except Exception as e:
                print(f"处理 {video_file} 时出错: {e}")
                results['failed'] += 1
        
        return results


def main():
    """主函数"""
    print("="*80)
    print("ExifTool 视频元数据提取测试")
    print("="*80)
    
    # 创建提取器实例 - 使用指定的 ExifTool 路径
    exiftool_path = r"F:\downloadforsetup\exiftool-13.45_64\exiftool.exe"
    extractor = VideoMetadataExtractor(exiftool_path=exiftool_path)
    
    # 测试单个文件
    print("\n" + "="*80)
    print("【测试1：单个视频文件分析】")
    print("="*80)
    
    test_video = r"D:\个人记录\VID_20240905_141626.mp4"
    
    if os.path.exists(test_video):
        report = extractor.generate_report(test_video)
        print(report)
        
        # 同时输出文本格式的完整元数据（用于参考）
        print("\n" + "="*80)
        print("【完整元数据（文本格式）】")
        print("="*80)
        full_metadata = extractor.extract_metadata_text(test_video)
        print(full_metadata)
    else:
        print(f"测试文件不存在: {test_video}")
    
    # 批量分析
    print("\n" + "="*80)
    print("【测试2：批量分析目录】")
    print("="*80)
    
    target_directory = r"D:\个人记录"
    results = extractor.batch_analyze(target_directory, extensions=['.mp4', '.mov'])
    
    # 输出统计信息
    print("\n" + "="*80)
    print("【分析统计】")
    print("="*80)
    print(f"总文件数: {results['total']}")
    print(f"成功分析: {results['success']}")
    print(f"失败: {results['failed']}")
    
    # 生成兼容性报告
    print("\n" + "="*80)
    print("【格式兼容性报告】")
    print("="*80)
    
    format_stats = {}
    for item in results['reports']:
        metadata = extractor.extract_metadata_json(item['file'])
        file_type = metadata.get('File:FileType', 'Unknown')
        format_stats[file_type] = format_stats.get(file_type, 0) + 1
    
    for file_type, count in format_stats.items():
        print(f"  {file_type}: {count} 个文件")
    
    print("\n测试完成！")


if __name__ == "__main__":
    main()
