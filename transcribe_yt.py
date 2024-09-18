import os
import yt_dlp
from pathlib import Path
from groq import Groq
from pydub import AudioSegment

DOWNLOADS_DIR = Path(__file__).parent / "downloads"
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
        ydl.download([url])
        video_info = ydl.extract_info(url, download=False)
        return Path(f"{video_info['id']}.wav")

def split_audio(file_path, chunk_length_ms=10000):
    audio = AudioSegment.from_wav(file_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    chunk_paths = []
    for i, chunk in enumerate(chunks):
        chunk_path = file_path.parent / f"{file_path.stem}_part{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunk_paths.append(chunk_path)
    return chunk_paths

def transcribe_audio(file_path, client):
    chunk_paths = split_audio(file_path)
    for chunk_path in chunk_paths:
        with open(chunk_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(chunk_path.name, file.read()),
                model="whisper-large-v3",
                prompt="Specify context or spelling",
                response_format="json",
                language="zh",
                temperature=0.0
            )
            print(transcription.text)

def clean_downloads(directory):
    for file in directory.glob("*"):
        try:
            os.remove(file)
        except Exception as e:
            print(f"Error deleting file {file}: {e}")

def main():
    clean_downloads(DOWNLOADS_DIR)

    URL = input("Enter the URL of the YouTube video: ")

    video_path_local = download_and_extract_audio(URL)
    
    client = Groq(api_key="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")
    
    first_file = next(DOWNLOADS_DIR.glob("*"), None)
    if first_file:
        transcribe_audio(first_file, client)
    else:
        raise FileNotFoundError("No files found in the downloads directory.")
    
    clean_downloads(DOWNLOADS_DIR)

if __name__ == "__main__":
    main()