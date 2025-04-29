# Project Setup

## Preliminaries

- Install the following Python versions:
  - Python 3.10.11
  - Python 3.12.10
- Ensure `pip` is installed.

## Create Virtual Environments for Both

### Whisper Environment

Create the virtual environment for Whisper:

```bash
python3.10 -m venv venv_whisper
```

Activate the environment:

```bash
source venv_whisper/scripts/activate
# On Windows:
# venv_whisper\Scripts\activate
```

Install the requirements:

```bash
pip install -r requirements-whisper.txt
```

Use the `venv_whisper` environment for the following scripts:

- `whisper.py`
- `mp4_to_mp3.py`
- `combine_whisper_diarization.py`

### Diarization Environment

Create the virtual environment for Diarization:

```bash
python3.10 -m venv venv_diarization
```

Activate the environment:

```bash
source venv_diarization/scripts/activate
# On Windows:
# venv_diarization\Scripts\activate
```

Install the requirements:

```bash
pip install --extra-index-url https://download.pytorch.org/whl/cu118 -r requirements-diarization.txt
```

Use the `venv_diarization` environment for the following script:

- `diarization.py`

## Folder Structure

Create the following folders before proceeding:

```bash
mkdir video_mp4 audio_mp3
```


- Place your `.mp4` video files in the `video_mp4/` folder.
- Place your `.mp3` audio files in the `audio_mp3/` folder.

## Hugging Face Token

Each user should create their own `.env` file, as the Hugging Face token is personal and must have read rights.

To prevent accidental exposure, make sure to add `.env` to your `.gitignore` file:

```bash
echo .env >> .gitignore
```

Create the `.env` file and add your token:

```env
HUGGINGFACE_TOKEN=your_token_here
```

Create a `.env` file and add your Hugging Face token (must have read rights):

```env
HUGGINGFACE_TOKEN=your_token_here
```

