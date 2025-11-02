import requests
import re
import os
from dotenv import load_dotenv
import yt_dlp

load_dotenv()

def extract_playlist_id(url: str) -> str | None:
    """Extract playlistId from YouTube URL."""
    match = re.search(r"[?&]list=([A-Za-z0-9_-]+)", url)
    return match.group(1) if match else None

def get_video_ids(playlist_id: str, api_key: str) -> list[str]:
    """Fetch all video IDs from a YouTube playlist using the Data API."""
    base_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        "part": "contentDetails",
        "playlistId": playlist_id,
        "maxResults": 50,
        "key": api_key
    }
    video_ids = []

    while True:
        resp = requests.get(base_url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        for item in data.get("items", []):
            vid = item["contentDetails"]["videoId"]
            video_ids.append(vid)

        if "nextPageToken" in data:
            params["pageToken"] = data["nextPageToken"]
        else:
            break

    return video_ids

def download_audio(url, output_path="downloads"):
    # Make sure output folder exists
    os.makedirs(output_path, exist_ok=True)

    # yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'writethumbnail': True,
        'embedthumbnail': True,
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Save using video title
        'postprocessors': [
            {  # Extract audio to mp3
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            {'key': 'FFmpegMetadata'},
            {'key': 'EmbedThumbnail'},
        ],
        'quiet': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading audio from: {url}")
        ydl.download([url])
        print("Download complete!")

if __name__ == "__main__":
    playlist_url = input("Enter YouTube playlist URL: ").strip()
    api_key = os.getenv('API_KEY')

    playlist_id = extract_playlist_id(playlist_url)
    if not playlist_id:
        print("Could not extract playlist ID from URL")
    else:
        ids = get_video_ids(playlist_id, api_key)
        print(f"Found {len(ids)} videos")
        start = int(input("From: "))-1
        end = int(input("To: "))
        ni = 1
        for i in range(start, end):
            download_audio("https://www.youtube.com/watch?v="+ids[i])
            print(f"\033[32mDownloaded {ni}/{end-start}\033[0m") # Text color green
            ni += 1
        print("\033[32mAll downloads complete!\033[0m") # Text color green