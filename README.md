# YouTube Video Downloader

A simple and elegant GUI application built with Python and `customtkinter` for downloading YouTube videos. This project provides two versions of the downloader: a lightweight basic version and a feature-rich advanced version.

## Features

  - **Basic Version (`youtube_downloader_basic.py`)**

      - Simple and fast.
      - Downloads videos that are available as a single "progressive" stream (up to 720p).
      - Supports audio-only downloads.

  - **Advanced Version (`youtube_downloader_high_quality.py`)**

      - Supports downloading videos in the highest available quality (1080p, 4K, etc.).
      - Automatically downloads separate video and audio streams and merges them using the `moviepy` library.
      - Supports audio-only downloads.

## Prerequisites

To run this application, you need to have the following installed on your system:

  - **Python 3.6+**
  - **pip** (Python package installer)
  - **ffmpeg** (required for the advanced version to merge video and audio)

You can download `ffmpeg` from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) and ensure it is added to your system's PATH.

## Installation

1.  Clone this repository to your local machine or download the files.

2.  Navigate to the project directory in your terminal.

3.  Install the required Python packages for the **basic version**:

    ```bash
    pip install customtkinter pytubefix
    ```

4.  If you want to run the **advanced version**, install `moviepy` as well:

    ```bash
    pip install moviepy
    ```

## How to Use

To launch either version of the application, simply run the corresponding Python script from your terminal:

**For the Basic Version:**

```bash
python youtubeDownloaderBasic.py
```

**For the Advanced Version:**

```bash
python youtubeDownloaderHighQuality.py
```

After the application window appears:

1.  Paste the URL of the YouTube video into the text box.
2.  Select your desired video quality from the dropdown menu.
3.  Choose your download path by clicking the "Browse" button.
4.  Click "Download" to start the process. The progress bar will show the download status.
