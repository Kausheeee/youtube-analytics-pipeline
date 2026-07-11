import json
from pathlib import Path


def save_json(
    data,
    entity: str,
    filename: str,
    snapshot_date: str
):
    """
    Saves extracted data into the raw data directory.

    Example:
    data/raw/videos/2026-07-04/ankit_bansal.json
    """

    output_dir = Path(f"data/raw/{entity}/{snapshot_date}")

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = output_dir / f"{filename}.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(f"Saved {len(data)} records -> {output_file}")