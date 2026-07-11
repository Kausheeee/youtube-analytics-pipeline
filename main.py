from datetime import datetime, timezone

from extract import run_extraction
from load import run_loading


def get_snapshot_date():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def main():

    snapshot = get_snapshot_date()

    print("=" * 70)
    print("YouTube Analytics Pipeline")
    print(f"Snapshot Date : {snapshot}")
    print("=" * 70)

    run_extraction(snapshot)

    run_loading(snapshot)

    print("=" * 70)
    print("Pipeline Completed Successfully")
    print("=" * 70)


if __name__ == "__main__":
    main()