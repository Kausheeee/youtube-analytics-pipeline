import argparse
from datetime import datetime, timezone
from pathlib import Path

from src.load.bigquery import (
    get_client,
    ensure_dataset,
)

from src.load.loader import load_entity

from src.load.schemas import *

from src.load.transformers import *

from src.load.readers import get_channel_file_names


def get_snapshot_date():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def run_loading(snapshot_date):

    print("=" * 70)
    print("Starting BigQuery Loading Pipeline")
    print("=" * 70)

    client = get_client()

    ensure_dataset(client)

    channel_names = get_channel_file_names()

    # -------------------------------------------------
    # Channels
    # -------------------------------------------------

    print("\nLoading Channels...")

    load_entity(
        client=client,
        json_path=Path(
            f"data/raw/channels/{snapshot_date}/channels_snapshot.json"
        ),
        transformer=transform_channel,
        schema=CHANNEL_SCHEMA,
        stage_table="channels_stage",
        target_table="channels_raw",
        merge_keys=["channel_id", "snapshot_date"],
        snapshot_date=snapshot_date,
    )

    # -------------------------------------------------
    # Videos
    # -------------------------------------------------

    print("\nLoading Videos...")

    for channel_name in channel_names:

        load_entity(
            client=client,
            json_path=Path(
                f"data/raw/videos/{snapshot_date}/{channel_name}.json"
            ),
            transformer=transform_video,
            schema=VIDEO_SCHEMA,
            stage_table="videos_stage",
            target_table="videos_raw",
            merge_keys=["video_id", "snapshot_date"],
            snapshot_date=snapshot_date,
        )

    # -------------------------------------------------
    # Comments
    # -------------------------------------------------

    print("\nLoading Comments...")

    for channel_name in channel_names:

        load_entity(
            client=client,
            json_path=Path(
                f"data/raw/comments/{snapshot_date}/{channel_name}.json"
            ),
            transformer=transform_comment,
            schema=COMMENT_SCHEMA,
            stage_table="comments_stage",
            target_table="comments_raw",
            merge_keys=["comment_id"],
            snapshot_date=None,
        )

    # -------------------------------------------------
    # Playlists
    # -------------------------------------------------

    print("\nLoading Playlists...")

    for channel_name in channel_names:

        load_entity(
            client=client,
            json_path=Path(
                f"data/raw/playlists/{snapshot_date}/{channel_name}_playlists.json"
            ),
            transformer=transform_playlist,
            schema=PLAYLIST_SCHEMA,
            stage_table="playlists_stage",
            target_table="playlists_raw",
            merge_keys=["playlist_id"],
            snapshot_date=None,
        )

    # -------------------------------------------------
    # Playlist Items
    # -------------------------------------------------

    print("\nLoading Playlist Items...")

    for channel_name in channel_names:

        load_entity(
            client=client,
            json_path=Path(
                f"data/raw/playlists/{snapshot_date}/{channel_name}_playlist_items.json"
            ),
            transformer=transform_playlist_item,
            schema=PLAYLIST_ITEM_SCHEMA,
            stage_table="playlist_items_stage",
            target_table="playlist_items_raw",
            merge_keys=["playlist_id", "video_id"],
            snapshot_date=None,
        )

    # -------------------------------------------------
    # Categories
    # -------------------------------------------------

    print("\nLoading Categories...")

    load_entity(
        client=client,
        json_path=Path(
            f"data/raw/categories/{snapshot_date}/video_categories.json"
        ),
        transformer=transform_category,
        schema=CATEGORY_SCHEMA,
        stage_table="categories_stage",
        target_table="categories_raw",
        merge_keys=["category_id"],
        snapshot_date=None,
    )

    print("\nLoading Completed Successfully")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--snapshot-date",
        required=False,
        help="Snapshot date in YYYY-MM-DD format",
    )

    args = parser.parse_args()

    snapshot = args.snapshot_date or get_snapshot_date()

    run_loading(snapshot)