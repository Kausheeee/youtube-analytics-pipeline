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

    # ---------------- Channels ----------------

    load_entity(
        client=client,
        json_path=Path(
            f"data/raw/channels/{snapshot_date}/channels_snapshot.json"
        ),
        transformer=transform_channel,
        schema=CHANNEL_SCHEMA,
        stage_table="channels_stage",
        target_table="channels_raw",
        merge_keys=[
            "channel_id",
            "snapshot_date",
        ],
        snapshot_date=snapshot_date,
    )

    # Continue with Videos, Comments, Playlists,
    # Playlist Items and Categories...
    # (Exactly the same code you already have.)

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