import os
import sys
import datetime

# 将当前目录添加到系统路径，以便导入 media_sensor
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from media_sensor import get_video_metadata
except ImportError:
    print("Error: Could not import media_sensor.py. Ensure it is in the same directory.")
    sys.exit(1)

def generate_video_inventory(target_dir, output_file):
    video_extensions = ('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv')
    inventory = []
    
    if not os.path.exists(target_dir):
        print(f"错误: 目标目录不存在: {target_dir}")
        return

    print(f"开始扫描目录: {target_dir}")
    count = 0
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.lower().endswith(video_extensions):
                full_path = os.path.join(root, file)
                print(f"处理中: {file}")
                metadata = get_video_metadata(full_path)
                inventory.append(metadata)
                count += 1
    
    print(f"扫描完成，共发现 {count} 个视频文件。")
    
    # 按照创建时间排序（如果存在）
    def get_sort_key(item):
        # 尝试从元数据中获取创建日期
        for key in ['Creation date', 'CreationTime', 'Date']:
            if key in item and item[key] != 'Unknown':
                return item[key]
        return '9999-99-99'

    inventory.sort(key=get_sort_key, reverse=True)
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# 视频文件库清单 (Video Inventory)\n\n")
        f.write(f"生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"扫描目录: `{target_dir}`\n\n")
        
        f.write("| 文件名 | 时长 | 创建时间 | 分辨率 | 路径 |\n")
        f.write("| --- | --- | --- | --- | --- |\n")
        
        for item in inventory:
            name = item.get('Filename', 'Unknown')
            duration = item.get('Duration', 'Unknown')
            # 兼容不同格式的创建时间字段
            creation = item.get('Creation date', item.get('CreationTime', item.get('Date', 'Unknown')))
            
            width = item.get('Image width', item.get('Width', '0'))
            height = item.get('Image height', item.get('Height', '0'))
            resolution = f"{width}x{height}" if width != '0' else "Unknown"
            
            path = item.get('Path', 'Unknown')
            
            f.write(f"| {name} | {duration} | {creation} | {resolution} | {path} |\n")
            
    print(f"清单已生成至: {output_file}")

if __name__ == "__main__":
    # 默认配置
    target = r"I:\我的记录"
    output = r"d:\个人记录\obsidian-file\wjmber\tasks\需求\人生OS\2_DAO\VIDEO_INVENTORY.md"
    
    # 允许通过命令行参数覆盖
    if len(sys.argv) > 1:
        target = sys.argv[1]
    if len(sys.argv) > 2:
        output = sys.argv[2]
        
    generate_video_inventory(target, output)
