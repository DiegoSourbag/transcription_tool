import os
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

import sys
import json
import time
import threading
from pathlib import Path
from tqdm import tqdm
from faster_whisper import WhisperModel

# Configuration
AUDIO_FOLDER = Path("audio_mp3")
OUTPUT_FOLDER = Path("transcripts_whisper")
MODEL_SIZE = "large-v2"
BEAM_SIZE = 5 
LANGUAGE = "nl"


def load_whisper_model():
    print("\n📦 Loading Whisper model (large)...")
    try:
        model = WhisperModel(MODEL_SIZE, device="cuda", compute_type="float16")
    except Exception as e:
        print(f"❌ Error loading Whisper model: {e}")
        sys.exit(1)
    print("✅ Whisper model loaded.")
    return model


def get_audio_files(audio_folder):
    return list(audio_folder.glob("*.mp3")) + list(audio_folder.glob("*.m4a"))


# Helper function for live timer with filename
def live_timer(start_time, stop_event, filename):
    while not stop_event.is_set():
        elapsed = time.time() - start_time
        sys.stdout.write(f"\r⏳ [{filename}] Running for {elapsed:.1f} seconds...")
        sys.stdout.flush()
        time.sleep(1)  # update every second

def process_audio_file(audio_path, whisper_model, output_folder):
    filename = audio_path.stem
    json_path = output_folder / f"{filename}.json"

    # Check if the transcript already exists
    if json_path.exists():
        print(f"✅ Transcript already exists for {audio_path.name}. Skipping...")
        return  # Skip processing

    start_time = time.time()

    # Start live timer thread
    stop_event = threading.Event()
    timer_thread = threading.Thread(target=live_timer, args=(start_time, stop_event, audio_path.name))
    timer_thread.start()

    try:
        print(f"\n🎙️ Processing file: {audio_path.name}")
        segments_gen, _ = whisper_model.transcribe(
            str(audio_path), language=LANGUAGE, beam_size=BEAM_SIZE
        )
        segments = [
            {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            }
            for segment in segments_gen
        ]

        with json_path.open("w", encoding="utf-8") as f_json:
            json.dump(segments, f_json, indent=2, ensure_ascii=False)
        print(f"✅ Transcript saved to {json_path.name}.")

    except Exception as e:
        print(f"❌ Error processing {audio_path.name}: {e}")

    finally:
        # Stop live timer
        stop_event.set()
        timer_thread.join()

    total_time = time.time() - start_time
    print(f"\n⏱️ [{audio_path.name}] Total time: {total_time:.2f} sec")


def main():
    print("\n🚀 Starting Whisper transcription only...")
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    audio_files = get_audio_files(AUDIO_FOLDER)
    if not audio_files:
        print(f"⚠️ No audio files found in folder: {AUDIO_FOLDER}")
        sys.exit(1)

    print(f"🎵 Found {len(audio_files)} audio file(s).")

    whisper_model = load_whisper_model()

    # Process each file one by one, and skip to next if a file has an error
    for audio_path in tqdm(audio_files, desc="🔊 Processing", unit="file"):
        try:
            process_audio_file(audio_path, whisper_model, OUTPUT_FOLDER)
        except Exception as e:
            print(f"❌ Error processing {audio_path.name}: {e}")
            continue  # Skip to next file in case of an error

    print("\n🏁 All done! Transcripts saved to:", OUTPUT_FOLDER)


if __name__ == "__main__":
    main()
