import yaml
from typing import Dict, List

from dotenv import load_dotenv
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


def get_all_playlists(
    youtube,
    channel_id: str
) -> List[Dict]:
    """
    Fetch all playlists for a channel.
    """

    playlists = []
    next_page_token = None

    while True:

        response = youtube.playlists().list(
            part="snippet,contentDetails",
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        playlists.extend(
            response.get("items", [])
        )

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return playlists


def get_playlist_items(
    youtube,
    playlist_id: str
) -> List[Dict]:
    """
    Fetch all videos from a playlist.
    """

    playlist_items = []

    next_page_token = None

    while True:

        response = youtube.playlistItems().list(
            part="contentDetails,snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in response.get("items", []):

            playlist_items.append({

                "playlist_id": playlist_id,
                "video_id": item["contentDetails"]["videoId"],
                "position": item["snippet"]["position"],
                "added_at": item["snippet"]["publishedAt"]

            })

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return playlist_items


def extract_playlists(
    config_path: str = "config/channels.yml"
):
    """
    Extract playlists and playlist items.

    Returns
    -------
    {
        "ankit_bansal": {
            "playlists": [...],
            "playlist_items": [...]
        },
        ...
    }
    """

    youtube = get_youtube_client()

    channels = load_channels(config_path)

    extracted_data = {}

    for channel in channels:

        channel_name = channel["name"]

        print(f"Fetching playlists for {channel_name}...")

        playlists = get_all_playlists(
            youtube,
            channel["channel_id"]
        )

        playlist_items = []

        for playlist in playlists:

            print(
                f"   Fetching playlist items: {playlist['snippet']['title']}"
            )

            playlist_items.extend(

                get_playlist_items(
                    youtube,
                    playlist["id"]
                )

            )

        safe_name = channel_name.lower().replace(" ", "_")

        extracted_data[safe_name] = {

            "playlists": playlists,
            "playlist_items": playlist_items

        }

        print(
            f"Fetched {len(playlists)} playlists and "
            f"{len(playlist_items)} playlist items."
        )

    return extracted_data