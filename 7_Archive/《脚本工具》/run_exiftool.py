import subprocess
import os

exiftool_path = r"F:\downloadforsetup\exiftool-13.45_64\exiftool.exe"
video_path = r"D:\个人记录\锻炼\8-14.mp4"

if not os.path.exists(exiftool_path):
    print(f"ExifTool not found at: {exiftool_path}")
    # List files in the directory to help debug
    dir_path = os.path.dirname(exiftool_path)
    if os.path.exists(dir_path):
        print(f"Contents of {dir_path}:")
        print(os.listdir(dir_path))
    else:
        print(f"Directory not found: {dir_path}")
else:
    cmd = [exiftool_path, "-G1", "-a", "-s", "-time:all", "-gps:all", video_path]
    print(f"Running command: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        print("--- STDOUT ---")
        print(result.stdout)
        print("--- STDERR ---")
        print(result.stderr)
    except Exception as e:
        print(f"Error running subprocess: {e}")
