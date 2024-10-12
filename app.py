from flask import Flask, request, jsonify, render_template
import os
from pathlib import Path
from openai import OpenAI
from pydub import AudioSegment
import yt_dlp
import sys

app = Flask(__name__)

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

def transcribe_audio(file_path, client):
    chunk_paths = split_audio(file_path)
    total_chunks = len(chunk_paths)
    transcription_text = ""
    
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
            transcription_text += transcription + "\n"
            print(transcription)  # Print each transcription on a new line
    print()  # Move to the next line after the progress is complete
    return transcription_text

def clean_downloads(directory):
    for file in directory.glob("*"):
        try:
            os.remove(file)
        except Exception as e:
            print(f"Error deleting file {file}: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        url = request.form['url']
        clean_downloads(DOWNLOADS_DIR)
        TRANSCRIPTIONS_DIR.mkdir(exist_ok=True)

        video_id, video_path_local = download_and_extract_audio(url)
        
        client = OpenAI(api_key="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")
        
        transcription_text = transcribe_audio(video_path_local, client)
        
        clean_downloads(DOWNLOADS_DIR)
        
        return jsonify({'transcription': transcription_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
