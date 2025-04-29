import json
from pathlib import Path

# Input folders
TRANSCRIPTS_FOLDER = Path("transcripts_whisper")
DIARIZATION_FOLDER = Path("diarization_results")
# Output folder
COMBINED_FOLDER = Path("combined_transcripts")
COMBINED_FOLDER.mkdir(exist_ok=True)


def load_diarization(diarization_path):
    diarization = []
    with open(diarization_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 4:
                start = float(parts[0])
                end = float(parts[2].replace("-->", "").replace(":", ""))  # <--- remove ":" here!
                speaker = parts[3]
                diarization.append((start, end, speaker))
    return diarization



def load_transcript(transcript_file):
    with transcript_file.open("r", encoding="utf-8") as f:
        return json.load(f)


def find_speaker(diarization, start, end, last_speaker):
    overlaps = []
    for dia_start, dia_end, speaker in diarization:
        overlap = max(0, min(end, dia_end) - max(start, dia_start))
        if overlap > 0:
            overlaps.append((overlap, speaker))

    if overlaps:
        overlaps.sort(reverse=True)  # Largest overlap first
        return overlaps[0][1]
    else:
        return last_speaker  # Fallback to previous speaker


def combine_files(transcript_path, diarization_path, output_path):
    transcript = load_transcript(transcript_path)
    diarization = load_diarization(diarization_path)

    output_lines = []
    last_speaker = "@Unknown"

    for segment in transcript:
        start = segment["start"]
        end = segment["end"]
        text = segment["text"].strip()

        speaker = find_speaker(diarization, start, end, last_speaker)

        if speaker != last_speaker:
            output_lines.append(f"\n@{speaker}")
            last_speaker = speaker

        output_lines.append(text)

    output_text = "\n".join(output_lines)

    with output_path.open("w", encoding="utf-8") as f:
        f.write(output_text)

    print(f"✅ Combined file saved: {output_path.name}")


def main():
    transcript_files = list(TRANSCRIPTS_FOLDER.glob("*.json"))

    for transcript_file in transcript_files:
        filename_stem = transcript_file.stem
        diarization_file = DIARIZATION_FOLDER / f"{filename_stem}_diarization.txt"

        if diarization_file.exists():
            output_file = COMBINED_FOLDER / f"{filename_stem}_combined.txt"
            combine_files(transcript_file, diarization_file, output_file)
        else:
            print(f"⚠️ Diarization file missing for {filename_stem}, skipping.")


if __name__ == "__main__":
    main()
