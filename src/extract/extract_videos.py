import os
import yaml
from typing import Dict, List

from dotenv import load_dotenv
from googleapiclient.discovery import build
from src.utils.youtube import get_youtube_client

load_dotenv()

def load_channels(
    config_path: str = "config/channels.yml"
) -> List[Dict]:
    """
    Load configured channels.
    """

    with open(config_path, "r") as file:
        return yaml.safe_load(file)["channels"]


def get_all_video_ids(
    youtube,
    uploads_playlist_id: str
) -> List[str]:
    """
    Fetch all video IDs from a channel's uploads playlist.
    """

    video_ids = []

    next_page_token = None

    while True:

        response = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in response.get("items", []):

            video_ids.append(
                item["contentDetails"]["videoId"]
            )

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return video_ids


def get_video_details(
    youtube,
    video_ids: List[str]
) -> List[Dict]:
    """
    Fetch detailed metadata for videos.

    videos.list supports a maximum of 50 IDs per request.
    """

    all_videos = []

    for i in range(0, len(video_ids), 50):

        batch = video_ids[i:i + 50]

        response = youtube.videos().list(
            part="snippet,statistics,contentDetails,topicDetails,status",
            id=",".join(batch)
        ).execute()

        all_videos.extend(
            response.get("items", [])
        )

    return all_videos


def extract_videos(
    config_path: str = "config/channels.yml"
):
    """
    Extract videos for all configured channels.

    Returns
    -------
    {
        "ankit_bansal": [...],
        "techtfq": [...],
        "ansh_lamba": [...]
    }
    """

    youtube = get_youtube_client()

    channels = load_channels(config_path)

    extracted_data = {}

    for channel in channels:

        channel_name = channel["name"]

        print(f"Fetching videos for {channel_name}...")

        video_ids = get_all_video_ids(
            youtube,
            channel["uploads_playlist_id"]
        )

        print(f"Found {len(video_ids)} videos.")

        videos = get_video_details(
            youtube,
            video_ids
        )

        safe_name = channel_name.lower().replace(" ", "_")

        extracted_data[safe_name] = videos

        print(f"Fetched {len(videos)} videos.")

    return extracted_data