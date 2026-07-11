from pathlib import Path

from src.load.readers import read_json
from src.load.bigquery import (
    ensure_table,
    load_stage_table,
    merge_table
)


def load_entity(
    client,
    json_path,
    transformer,
    schema,
    stage_table,
    target_table,
    merge_keys,
    snapshot_date,
):
    """
    Generic Loader
    """

    raw_data = read_json(json_path)

    if snapshot_date is None:
        rows = [
            transformer(record)
            for record in raw_data
        ]
    else:
        rows = [
        transformer(record, snapshot_date)
        for record in raw_data
        ]

    ensure_table(
        client,
        stage_table,
        schema
    )

    ensure_table(
        client,
        target_table,
        schema
    )

    load_stage_table(
        client,
        stage_table,
        rows
    )

    merge_table(
        client=client,
        target_table=target_table,
        stage_table=stage_table,
        merge_keys=merge_keys,
        update_columns=list(rows[0].keys()),
        insert_columns=list(rows[0].keys())
    )