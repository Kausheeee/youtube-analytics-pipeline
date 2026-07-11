# resolve_channels.py
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

youtube = build("youtube", "v3", developerKey=os.environ["YOUTUBE_API_KEY"])

handles = ["@AnshLambaJSR", "@ankitbansal6", "@techTFQ"]

for handle in handles:
    response = youtube.channels().list(
        part="snippet,statistics,contentDetails",
        forHandle=handle
    ).execute()

    if response["items"]:
        item = response["items"][0]
        print(f"Handle: {handle}")
        print(f"  channel_id: {item['id']}")
        print(f"  title: {item['snippet']['title']}")
        print(f"  subscriber_count: {item['statistics'].get('subscriberCount')}")
        print(f"  video_count: {item['statistics'].get('videoCount')}")
        print(f"  uploads_playlist_id: {item['contentDetails']['relatedPlaylists']['uploads']}")
        print()
    else:
        print(f"Handle: {handle} — NOT FOUND")