# Youtube-playlist-mp3-downloader

Python program that automatically downloads the audio from Youtube videos in a playlist given the playlist url using yt-dlp.

---

## Dependencies

* Python versions 3.10+ (CPython) and 3.11+ (PyPy) are supported by yt-dlp.

* A js runtime is also required by yt-dlp, in this case i use Node, but Deno is also supported. To use Deno delete the line: ```"js_runtimes": {"node": {"path": None}},```.

* A YouTube Data API V3 Key. You can get one in [Google Cloud Console](https://console.cloud.google.com)

## Usage

1. Clone this repository:
```
git clone https://github.com/EricKohan/youtube-playlist-mp3-downloader.git
```
2. Run ```pip install -r requirements.txt``` to install dependencies.
3. Run ```python3 -m pip install -U --pre "yt-dlp[pin,pin-curl-cffi]"``` to update yt-dlp to its latest nightly version.
4. Create a .env file containing: ```API_KEY=<Your YouTube Data API V3 Key>```.
5. Run ```python3 playlist.py```.

Once you enter the playlist url and from which to which video to download the audio, the files will appear in ```/downloads```.