# Media Catcher - Version 2.0
*A fast, powerful, and customizable tool for downloading videos and audio from the web.*

Media Catcher lets you download and manage multimedia content from various websites with ease:

- 🎥 Download video & audio from online sources  
- 📁 Convert to multiple formats (MP4, MP3, FLAC...)  
- 💬 Download subtitles  
- 🧠 Embed metadata and thumbnails automatically  
- ⚙️ Multithreaded queue system for fast parallel downloads

![media-catcher-image](https://github.com/user-attachments/assets/1dd08057-1d75-4d8e-b3bc-1408145c26db)

## Features

- **Download Video & Audio**: Easily download videos and audio from online sources.
- **Format Options**: Choose from a variety of formats like MP4, MKV, MP3, FLAC, and more.
- **Subtitles**: Option to download subtitles in multiple languages.
- **Metadata and Thumbnails**: Automatically embeds metadata and thumbnails into media files.
- **Progress Tracking**: Real-time download progress with speed, ETA, and file size details.
- **Proxy Support**: Supports downloading through a specified proxy — useful for hiding your IP or bypassing geo-restrictions.
- **Use of Cookies**: Allows specifying a cookies file (e.g., cookies.txt) to manage sessions for sites that require authentication.
- **Queue and Threading**: Handle multiple downloads simultaneously using a queue system, powered by PySide6's QThreadPool for efficient processing.

## Supported Formats

### Video Formats
- MP4
- MKV
- MOV
- WEBM
- AVI
- FLV

### Audio Formats
- AAC
- M4A
- MP3
- FLAC
- OGG
- OPUS
- WAV
- WEBM

## Supported Sites

Media Catcher uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) under the hood, meaning it supports hundreds of websites.

🔗 **Full list of supported sites:**  
👉 [https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)  
> **ℹ️ Note:** yt-dlp is actively maintained and regularly updates its supported sites list and internal features.  
> To ensure continued compatibility, keep yt-dlp updated to its latest version.

## Getting Started

* [`Portable`](#portable) ~ *Windows*
* [`Manual`](#manual-cross-platform) ~ *Cross-platform*

## Portable
Download the latest portable version from the [releases](https://github.com/Ec-25/Media-Catcher/releases/latest) section. 
This will download a ZIP file containing the program files.

## Manual (Cross-platform)

### Prerequisites
You **must** have [Python](https://www.python.org/downloads/) 3.9+ installed.

### Clone the repository
```bash
git clone https://github.com/Ec-25/Media-Catcher
cd Media-Catcher
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Usage

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
