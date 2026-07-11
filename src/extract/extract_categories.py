import os
from typing import List, Dict
from dotenv import load_dotenv
from googleapiclient.discovery import build
from src.utils.youtube import get_youtube_client

load_dotenv()


def fetch_video_categories(
    youtube,
    region_code: str = "US"
) -> List[Dict]:
    """
    Fetches all YouTube video categories for a region.
    """
    response = youtube.videoCategories().list(
        part="snippet",
        regionCode=region_code
    ).execute()

    return response.get("items", [])


def extract_categories(
    region_code: str = "US"
) -> List[Dict]:
    """
    Main extraction function.

    Returns
    -------
    List[Dict]
        Raw category objects returned by the YouTube API.
    """

    youtube = get_youtube_client()
    print(f"Fetching video categories ({region_code})...")
    categories = fetch_video_categories(
        youtube,
        region_code
    )
    print(f"Fetched {len(categories)} categories.")
    return categories