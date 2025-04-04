from platform import system

_OS = system()
_REQUIRED_PACKAGES_INFO = {
    "Darwin": {
        "ffmpeg": "ffmpeg-osx64-v4.2.2",
        "ffprobe": "ffprobe-osx64-v4.1",
        "yt-dlp": "yt-dlp_macos",
    },
    "Linux": {
        "ffmpeg": "ffmpeg-linux64-v4.2.2",
        "ffprobe": "ffprobe-linux64-v4.1",
        "yt-dlp": "yt-dlp_linux",
    },
    "Windows": {
        "ffmpeg": "ffmpeg-win64-v4.2.2.exe",
        "ffprobe": "ffprobe-win64-v4.1.exe",
        "yt-dlp": "yt-dlp.exe",
    },
}
DOWNLOAD_PACKAGES_INFO = {
    'yt-dlp': f'https://github.com/yt-dlp/yt-dlp/releases/latest/download/{_REQUIRED_PACKAGES_INFO[_OS]['yt-dlp']}',
    'ffmpeg': f'https://github.com/imageio/imageio-binaries/raw/master/ffmpeg/{_REQUIRED_PACKAGES_INFO[_OS]['ffmpeg']}',
    'ffprobe': f'https://github.com/imageio/imageio-binaries/raw/master/ffmpeg/{_REQUIRED_PACKAGES_INFO[_OS]['ffprobe']}'
}
