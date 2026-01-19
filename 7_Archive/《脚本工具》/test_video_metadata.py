import sys
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from hachoir.core import config

def get_video_metadata(filename):
    # Disable config error messages
    config.quiet = True
    
    parser = createParser(filename)
    if not parser:
        print(f"Unable to parse file: {filename}")
        return

    try:
        metadata = extractMetadata(parser)
    except Exception as err:
        print(f"Metadata extraction error: {err}")
        metadata = None

    if not metadata:
        print("No metadata could be extracted.")
        return

    # Print all available metadata
    for line in metadata.exportPlaintext():
        print(line)

if __name__ == "__main__":
    video_path = r"D:\个人记录\锻炼\171949c926fbecdffa89cc2dcae43a20.mp4"
    print(f"--- Metadata for: {video_path} ---")
    get_video_metadata(video_path)
