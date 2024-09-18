# youtube-subtitle-transcriber

`youtube-subtitle-transcriber` is a specialized tool designed to generate subtitles from YouTube videos, particularly useful for handling non-English content. This project aims to streamline the process of extracting and converting spoken content from YouTube videos into readable text subtitles, with a focus on accuracy and ease of use.

## Key Features

- **YouTube Video Downloading**: Download videos directly from YouTube with ease.
- **Audio Extraction**: Extract high-quality audio from the downloaded videos.
- **Speech-to-Text Conversion**: Convert the extracted audio into text using advanced speech recognition, supporting multiple languages.
- **Subtitle Formatting**: Format the transcribed text into subtitle files (e.g., SRT) for various use cases, including educational and accessibility purposes.

## Future Enhancements

- **User Interface**: Develop a front-end interface to make the tool more user-friendly and accessible. This interface will allow users to input YouTube URLs, monitor the transcription progress, and download the final subtitle files directly from their browser.
- **Improved Pronunciation Accuracy**: Implement advanced speech recognition models and techniques to enhance the accuracy of transcriptions, especially for non-English languages. This will involve continuous updates and training of the models to handle diverse accents and pronunciations more effectively.

## Getting Started

Follow these steps to get started with `youtube-subtitle-transcriber`:

### Prerequisites

Ensure you have the following installed on your system:
- Python 3.6 or higher
- `pip` (Python package installer)

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/youtube-subtitle-transcriber.git
    cd youtube-subtitle-transcriber
    ```

2. **Create a virtual environment** (optional but recommended):
    ```sh
    python -m venv myenv
    source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

### Usage

1. **Run the script**:
    ```sh
    python transcribe_yt.py
    ```

2. **Input the YouTube URL** when prompted:
    ```
    Enter the URL of the YouTube video: <paste_your_youtube_url_here>
    ```

3. **Wait for the process to complete**. The transcriptions will be saved in the `transcriptions` directory.
