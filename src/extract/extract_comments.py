import json
import os
import yaml
from pathlib import Path
from typing import Dict, List
from googleapiclient.discovery import build
from src.utils.youtube import get_youtube_client


def load_channels(config_path: str = "config/channels.yml") -> List[Dict]:
    """
    Load channel configuration.
    """

    with open(config_path, "r") as file:
        return yaml.safe_load(file)["channels"]


def load_video_ids(
    channel_name: str,
    snapshot_date: str
) -> List[str]:
    """
    Reads extracted videos from the raw JSON files and returns
    only the video IDs.
    """

    safe_name = channel_name.lower().replace(" ", "_")

    file_path = Path(
        f"data/raw/videos/{snapshot_date}/{safe_name}.json"
    )

    with open(file_path, "r") as file:
        videos = json.load(file)

    return [
        video["id"]
        for video in videos
    ]


def fetch_comments(
    youtube,
    video_id: str,
    max_results: int = 20
) -> List[Dict]:

    try:

        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            order="relevance"
        ).execute()

        comments = []

        for item in response.get("items", []):

            snippet = item["snippet"]["topLevelComment"]["snippet"]

            comments.append({

                "comment_id": item["id"],
                "video_id": video_id,
                "author": snippet["authorDisplayName"],
                "text": snippet["textDisplay"],
                "like_count": snippet["likeCount"],
                "published_at": snippet["publishedAt"],
                "reply_count": item["snippet"]["totalReplyCount"]

            })

        return comments

    except Exception as e:

        error = str(e)

        if "commentsDisabled" in error:
            return []

        if "videoNotFound" in error:
            print(f"Video not found: {video_id}")
            return []

        print(f"Error fetching comments for {video_id}: {e}")

        return []


def extract_comments(
    snapshot_date: str,
    config_path: str = "config/channels.yml"
) -> Dict[str, List[Dict]]:
    """
    Extract comments for every configured channel.

    Returns
    -------
    {
        "ankit_bansal": [...],
        "techtfq": [...],
        ...
    }
    """

    youtube = get_youtube_client()

    channels = load_channels(config_path)

    comments_by_channel = {}

    for channel in channels:

        channel_name = channel["name"]

        print(f"Fetching comments for {channel_name}...")

        video_ids = load_video_ids(
            channel_name,
            snapshot_date
        )

        all_comments = []

        for video_id in video_ids:
            all_comments.extend(
                fetch_comments(
                    youtube,
                    video_id
                )
            )

        safe_name = channel_name.lower().replace(" ", "_")

        comments_by_channel[safe_name] = all_comments

        print(f"Fetched {len(all_comments)} comments.")

    return comments_by_channel