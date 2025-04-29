# diarization.py

import os
import sys
import time
import torch
import torchaudio
from tqdm import tqdm
from dotenv import load_dotenv
from pyannote.audio import Pipeline
from pathlib import Path
import threading

# Load environment variables
load_dotenv()
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Configuration
AUDIO_MP3_FOLDER = Path("audio_mp3")
AUDIO_WAV_FOLDER = Path("audio_wav")
OUTPUT_FOLDER = Path("diarization_results")
MODEL_ID = "pyannote/speaker-diarization"

def load_pipeline():
    print("\n🧠 Loading diarization pipeline...")
    try:
        pipeline = Pipeline.from_pretrained(MODEL_ID, use_auth_token=HUGGINGFACE_TOKEN)
    except Exception as e:
        print(f"❌ Error loading diarization pipeline: {e}")
        sys.exit(1)
    print("✅ Diarization pipeline loaded.")
    return pipeline

def get_files():
    mp3_files = list(AUDIO_MP3_FOLDER.glob("*.mp3"))
    wav_files = list(AUDIO_WAV_FOLDER.glob("*.wav"))
    wav_stems = {f.stem for f in wav_files}
    files = mp3_files + [f for f in wav_files if f.stem not in wav_stems]
    return files

def live_timer(start_time, stop_event, filename):
    while not stop_event.is_set():
        elapsed = time.time() - start_time
        sys.stdout.write(f"\r⏳ [{filename}] Running for {elapsed:.1f} seconds...")
        sys.stdout.flush()
        time.sleep(1)

def process_file(pipeline, file_path, output_folder):
    filename = file_path.stem
    output_path = output_folder / f"{filename}_diarization.txt"
    if output_path.exists():
        print(f"✅ Diarization for {file_path.name} already exists. Skipping...")
        return

    start_time = time.time()
    stop_event = threading.Event()
    timer_thread = threading.Thread(target=live_timer, args=(start_time, stop_event, file_path.name))
    timer_thread.start()

    diarization_start = None
    diarization_end = 0

    try:
        if file_path.suffix.lower() == ".mp3":
            print(f"\n🔄 Converting {file_path.name} to WAV...")
            wav_path = AUDIO_WAV_FOLDER / f"{filename}.wav"
            waveform, sr = torchaudio.load(file_path)
            torchaudio.save(wav_path, waveform, sr)
            file_to_use = wav_path
        else:
            file_to_use = file_path

        print(f"\n🧍 Diarizing {file_to_use.name}...")
        diarization_start = time.time()
        annotation = pipeline({"audio": str(file_to_use)})
        diarization_end = time.time()

        with open(output_path, "w") as f:
            for segment, _, speaker in annotation.itertracks(yield_label=True):
                f.write(f"{segment.start:.2f} --> {segment.end:.2f}: {speaker}\n")
        print(f"\n✅ Saved diarization to {output_path.name}")

    except Exception as e:
        print(f"\n❌ Error processing {file_path.name}: {e}")
        diarization_end = time.time()

    finally:
        stop_event.set()
        timer_thread.join()

    total_time = time.time() - start_time
    diarization_time = (diarization_end - diarization_start) if diarization_start else 0
    print(f"\n⏱️ [{file_path.name}] Total time: {total_time:.2f} sec | Diarization time: {diarization_time:.2f} sec")

def main():
    print("\n🚀 Starting Diarization only...")
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    AUDIO_WAV_FOLDER.mkdir(parents=True, exist_ok=True)

    files = get_files()
    if not files:
        print(f"⚠️ No audio files found in {AUDIO_MP3_FOLDER}")
        sys.exit(1)

    print(f"🎵 Found {len(files)} audio file(s).")

    pipeline = load_pipeline()

    for file_path in tqdm(files, desc="🧍 Processing", unit="file"):
        process_file(pipeline, file_path, OUTPUT_FOLDER)

    print("\n🏁 All done! Diarization results saved to:", OUTPUT_FOLDER)

if __name__ == "__main__":
    main()
