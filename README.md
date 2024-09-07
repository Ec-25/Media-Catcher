# Media Catcher - Version 1.0

Media Catcher is a multimedia downloading tool. It allows users to download and manage audio and video files from various sources, supporting different formats and offering customizable download options.

## Features

- **Download Video & Audio**: Supports downloading videos and audio from online sources with ease.
- **Format Options**: Choose between various formats such as MP4, MKV, MP3, FLAC, and more for your media.
- **Subtitles**: Option to download subtitles in multiple languages.
- **Metadata and Thumbnails**: Automatically adds metadata and embeds thumbnails to audio and video files.
- **Progress Tracking**: Real-time download progress with detailed information on speed, ETA, and file size.
- **Queue and Threading**: Manage multiple downloads at once with a queue system, powered by PySide6's QThreadPool for efficient processing.

## Supported Formats

### Video Formats
- MP4
- WEBM
- MKV
- AVI
- FLV
- MOV

### Audio Formats
- MP3
- AAC
- OPUS
- FLAC
- M4A
- WAV
- OGG
- WEBM

## Installation

### Prerequisites
- Python 3.x
- [PySide6](https://pypi.org/project/PySide6/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [TQDM](https://pypi.org/project/tqdm/)
- [requests](https://pypi.org/project/requests/)

### Clone the repository
```bash
git clone https://github.com/yourusername/media-catcher.git
cd media-catcher
```

### Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

1. Launch the application:
    ```bash
    python main.py
    ```
2. In the UI, enter the download link, choose your desired format, and start downloading.
3. Monitor your downloads in the queue with detailed progress for each task.

## Customization

You can customize:

- **Download path**: Set your preferred folder for media downloads.
- **Quality settings**: Choose between high or low-quality media downloads.
- **Subtitle options**: Enable subtitles in your preferred languages.

## Contributing

Feel free to contribute to MEDIA-CATCHER by submitting pull requests or reporting issues on the GitHub repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
