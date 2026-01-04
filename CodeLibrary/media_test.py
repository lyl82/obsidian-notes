import os
import sys
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from hachoir.core import config

# Disable warnings to keep output clean
config.quiet = True

def get_video_metadata(file_path):
    print(f"\n--- Analyzing: {os.path.basename(file_path)} ---")
    try:
        parser = createParser(file_path)
        if not parser:
            print("Unable to parse file.")
            return

        with parser:
            metadata = extractMetadata(parser)
            if not metadata:
                print("No metadata found.")
                return

            for line in metadata.exportPlaintext():
                print(line)
            
            # Specifically look for creation date and duration
            creation_date = metadata.get('creation_date')
            duration = metadata.get('duration')
            print(f"\n[Summary]")
            print(f"Creation Date: {creation_date}")
            print(f"Duration: {duration}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    target_file = r"H:\视频_归档\2022-2023_视频存储\2023\03\20230330_224151.mp4"
    if os.path.exists(target_file):
        get_video_metadata(target_file)
    else:
        print(f"File not found: {target_file}")
