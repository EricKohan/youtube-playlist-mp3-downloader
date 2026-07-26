import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()


def extract_playlist_id(url: str) -> str | None:
    """Extract playlistId from YouTube URL."""
    match = re.search(r"[?&]list=([A-Za-z0-9_-]+)", url)
    return match.group(1) if match else None


def get_video_ids(playlist_id: str, api_key: str) -> list[str]:
    """Fetch all video titles from a YouTube playlist using the Data API."""
    base_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        "part": "snippet",
        "playlistId": playlist_id,
        "maxResults": 50,
        "key": api_key,
    }
    video_titles = []

    while True:
        resp = requests.get(base_url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        for item in data.get("items", []):
            vid = item["snippet"]["title"]
            video_titles.append(vid)

        if "nextPageToken" in data:
            params["pageToken"] = data["nextPageToken"]
        else:
            break

    return video_titles


if __name__ == "__main__":
    playlist_url = input("Enter YouTube playlist URL: ").strip()
    api_key = os.getenv("API_KEY")

    playlist_id = extract_playlist_id(playlist_url)
    if not playlist_id:
        print("Could not extract playlist ID from URL")
    else:
        titles = get_video_ids(playlist_id, api_key)
        print(f"Found {len(titles)} videos")
        start = int(input("From: "))
        end = int(input("To: "))
        selected_titles = titles[start - 1 : end]
        for i in range(0, len(selected_titles)):
            print(selected_titles[i])
