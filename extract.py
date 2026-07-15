import argparse
from datetime import datetime, timezone

from src.extract.extract_channels import extract_channels
from src.extract.extract_videos import extract_videos
from src.extract.extract_comments import extract_comments
from src.extract.extract_playlists import extract_playlists
from src.extract.extract_categories import extract_categories

from src.utils.save_json import save_json



def get_snapshot_date():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def run_extraction(snapshot_date):

    print("=" * 70)
    print("Starting Extraction Pipeline")
    print("=" * 70)

    channels = extract_channels()

    save_json(
        channels,
        "channels",
        "channels_snapshot",
        snapshot_date,
    )

    videos = extract_videos()

    for channel_name, data in videos.items():

        save_json(
            data,
            "videos",
            channel_name,
            snapshot_date,
        )

    comments = extract_comments(snapshot_date)

    for channel_name, data in comments.items():

        save_json(
            data,
            "comments",
            channel_name,
            snapshot_date,
        )

    playlists = extract_playlists()

    for channel_name, data in playlists.items():

        save_json(
            data["playlists"],
            "playlists",
            f"{channel_name}_playlists",
            snapshot_date,
        )

        save_json(
            data["playlist_items"],
            "playlists",
            f"{channel_name}_playlist_items",
            snapshot_date,
        )

    categories = extract_categories()

    save_json(
        categories,
        "categories",
        "video_categories",
        snapshot_date,
    )

    print("\nExtraction Completed Successfully")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--snapshot-date",
        required=False,
        help="Snapshot date in YYYY-MM-DD format",
    )

    args = parser.parse_args()

    snapshot = args.snapshot_date or get_snapshot_date()

    run_extraction(snapshot)