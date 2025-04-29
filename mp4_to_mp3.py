import os
from moviepy.editor import VideoFileClip
from pathlib import Path

# Define directories for the video and audio files
VIDEO_MP4_FOLDER = Path("video_mp4")
AUDIO_MP3_FOLDER = Path("audio_mp3")

# Ensure output folder exists
AUDIO_MP3_FOLDER.mkdir(parents=True, exist_ok=True)

def convert_mp4_to_mp3(mp4_path):
    # Extract filename without extension
    mp3_path = AUDIO_MP3_FOLDER / f"{mp4_path.stem}.mp3"
    
    # Skip if MP3 file already exists
    if mp3_path.exists():
        print(f"✅ {mp4_path.name} already converted. Skipping...")
        return  # Skip processing
    
    try:
        # Load the video file
        video = VideoFileClip(str(mp4_path))
        
        # Extract audio and save as mp3
        audio = video.audio
        audio.write_audiofile(str(mp3_path))
        print(f"✅ Converted {mp4_path.name} to {mp3_path.name}")
        
    except Exception as e:
        print(f"❌ Error during conversion of {mp4_path}: {e}")

def process_mp4_files():
    # Find all .mp4 files in the VIDEO_MP4_FOLDER
    mp4_files = list(VIDEO_MP4_FOLDER.glob("*.mp4"))
    
    if not mp4_files:
        print(f"⚠️ No MP4 files found in folder: {VIDEO_MP4_FOLDER}")
        return

    print(f"Found {len(mp4_files)} MP4 file(s). Converting to MP3...")
    
    # Loop over each file and convert
    for mp4_file in mp4_files:
        try:
            convert_mp4_to_mp3(mp4_file)
        except Exception as e:
            print(f"❌ Error processing {mp4_file.name}: {e}")

if __name__ == "__main__":
    process_mp4_files()
