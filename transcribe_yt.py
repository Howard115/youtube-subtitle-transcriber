import os
import sys
import yt_dlp
from pathlib import Path
from groq import Groq
from pydub import AudioSegment
from openai import OpenAI  # Add this import

DOWNLOADS_DIR = Path(__file__).parent / "downloads"
TRANSCRIPTIONS_DIR = Path(__file__).parent / "transcriptions"
YDL_OPTS = {
    'format': 'm4a/bestaudio/best',
    'outtmpl': str(DOWNLOADS_DIR / '%(id)s.%(ext)s'),
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }]
}

def download_and_extract_audio(url):
    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        video_info = ydl.extract_info(url, download=True)
        return video_info['id'], Path(f"{DOWNLOADS_DIR}/{video_info['id']}.wav")

def split_audio(file_path, chunk_length_ms=10000):
    audio = AudioSegment.from_wav(file_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    chunk_paths = []
    for i, chunk in enumerate(chunks):
        chunk_path = file_path.parent / f"{file_path.stem}_part{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunk_paths.append(chunk_path)
    return chunk_paths

def transcribe_audio(file_path, client, transcription_file):
    chunk_paths = split_audio(file_path)
    total_chunks = len(chunk_paths)
    
    with open(transcription_file, "w", encoding="utf-8") as subtitle:
        for i, chunk_path in enumerate(chunk_paths):
            # Update progress
            progress = (i + 1) / total_chunks * 100
            sys.stdout.write(f"\rProgress: {progress:.2f}%")
            sys.stdout.flush()
            
            with open(chunk_path, "rb") as file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=file,
                    response_format="text",
                    language="zh"
                )
                subtitle.write(transcription + "\n")
                print(transcription)  # Print each transcription on a new line
    print()  # Move to the next line after the progress is complete

def clean_downloads(directory):
    for file in directory.glob("*"):
        try:
            os.remove(file)
        except Exception as e:
            print(f"Error deleting file {file}: {e}")

def main():
    clean_downloads(DOWNLOADS_DIR)
    TRANSCRIPTIONS_DIR.mkdir(exist_ok=True)

    URL = input("Enter the URL of the YouTube video: ")

    video_id, video_path_local = download_and_extract_audio(URL)
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    transcription_file = TRANSCRIPTIONS_DIR / f"{video_id}.txt"
    
    first_file = next(DOWNLOADS_DIR.glob("*.wav"), None)
    if first_file:
        transcribe_audio(first_file, client, transcription_file)
    else:
        raise FileNotFoundError("No files found in the downloads directory.")
    
    clean_downloads(DOWNLOADS_DIR)

if __name__ == "__main__":
    main()
