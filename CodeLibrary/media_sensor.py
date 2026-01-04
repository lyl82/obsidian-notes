import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

def get_gps_info(exif_data):
    """提取GPS信息并转换为经纬度"""
    if not exif_data:
        return None
    
    gps_info = {}
    for tag, value in exif_data.items():
        decoded = TAGS.get(tag, tag)
        if decoded == "GPSInfo":
            for t in value:
                sub_decoded = GPSTAGS.get(t, t)
                gps_info[sub_decoded] = value[t]
    
    if not gps_info:
        return None

    def convert_to_degrees(value):
        try:
            d = float(value[0])
            m = float(value[1])
            s = float(value[2])
            return d + (m / 60.0) + (s / 3600.0)
        except (TypeError, IndexError, ZeroDivisionError):
            return 0.0

    lat_ref = gps_info.get('GPSLatitudeRef')
    lat_val = gps_info.get('GPSLatitude')
    lon_ref = gps_info.get('GPSLongitudeRef')
    lon_val = gps_info.get('GPSLongitude')

    if not lat_val or not lon_val:
        return None

    lat = convert_to_degrees(lat_val)
    if lat_ref != 'N':
        lat = -lat
        
    lon = convert_to_degrees(lon_val)
    if lon_ref != 'E':
        lon = -lon
        
    return lat, lon

def get_photo_metadata(file_path):
    """获取照片元数据"""
    try:
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            metadata = {
                "Filename": os.path.basename(file_path),
                "Path": file_path,
                "Format": img.format,
                "Size": img.size,
            }
            
            if exif_data:
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    if tag_name == "DateTimeOriginal":
                        metadata["CreationTime"] = value
                
                gps = get_gps_info(exif_data)
                if gps:
                    metadata["GPS"] = gps
            
            return metadata
    except Exception as e:
        return {"Filename": os.path.basename(file_path), "Error": str(e)}

def get_video_metadata(file_path):
    """获取视频元数据 (MP4, MOV等)"""
    try:
        parser = createParser(file_path)
        if not parser:
            return {"Filename": os.path.basename(file_path), "Error": "Unable to parse file"}
            
        with parser:
            metadata = extractMetadata(parser)
            if not metadata:
                return {"Filename": os.path.basename(file_path), "Error": "No metadata found"}
            
            data = {
                "Filename": os.path.basename(file_path),
                "Path": file_path,
            }
            
            for line in metadata.exportPlaintext():
                if ":" in line:
                    key, val = line.split(":", 1)
                    data[key.strip()] = val.strip()
            
            return data
    except Exception as e:
        return {"Filename": os.path.basename(file_path), "Error": str(e)}

def scan_directory(directory, extensions=('.mp4', '.mov', '.jpg', '.jpeg', '.png')):
    """递归扫描目录中的媒体文件"""
    results = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extensions):
                full_path = os.path.join(root, file)
                if file.lower().endswith(('.mp4', '.mov')):
                    results.append(get_video_metadata(full_path))
                else:
                    results.append(get_photo_metadata(full_path))
    return results

if __name__ == "__main__":
    # 示例测试
    import sys
    test_path = sys.argv[1] if len(sys.argv) > 1 else r"H:\视频_归档\2022-2023_视频存储\2023\03"
    if os.path.exists(test_path):
        print(f"Scanning {test_path}...")
        results = scan_directory(test_path)
        for res in results:
            print(res)
    else:
        print(f"Path not found: {test_path}")
