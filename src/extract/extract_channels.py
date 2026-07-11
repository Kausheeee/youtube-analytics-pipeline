import os
import yaml
from typing import List, Dict
from dotenv import load_dotenv
from googleapiclient.discovery import build
from src.utils.youtube import get_youtube_client


load_dotenv()

def load_channel_ids(
    config_path: str = "config/channels.yml"
) -> List[str]:
    """
    Reads channel IDs from the configuration file.
    """
    with open(config_path, "r") as file:
        channels = yaml.safe_load(file)["channels"]
    return [
        channel["channel_id"]
        for channel in channels
    ]


def fetch_channel_data(
    youtube,
    channel_ids: List[str]
) -> List[Dict]:
    """
    Fetches channel metadata from YouTube.
    """
    response = youtube.channels().list(
        part="snippet,statistics,contentDetails,brandingSettings",
        id=",".join(channel_ids)
    ).execute()
    return response.get("items", [])


def extract_channels(
    config_path: str = "config/channels.yml"
) -> List[Dict]:
    """
    Extracts channel metadata.

    Returns
    -------
    List[Dict]
        Raw channel objects returned by the YouTube API.
    """

    youtube = get_youtube_client()
    channel_ids = load_channel_ids(config_path)
    print(f"Fetching {len(channel_ids)} channels...")
    channels = fetch_channel_data(
        youtube,
        channel_ids
    )
    print(f"Fetched {len(channels)} channels.")
    return channels