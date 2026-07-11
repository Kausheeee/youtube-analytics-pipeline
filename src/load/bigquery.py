import os

from google.cloud import bigquery
from google.api_core.exceptions import NotFound


PROJECT_ID = os.getenv("GCP_PROJECT_ID", "coral-balancer-501316-e6")
DATASET_ID = os.getenv("BQ_DATASET", "raw_youtube")
LOCATION = os.getenv("BQ_LOCATION", "asia-south1")


def get_client():
    """
    Returns an authenticated BigQuery client.
    """
    return bigquery.Client(project=PROJECT_ID)


def get_table_id(table_name: str) -> str:
    """
    Returns fully-qualified table name.

    Example:
    coral-balancer-501316-e6.raw_youtube.videos_raw
    """
    return f"{PROJECT_ID}.{DATASET_ID}.{table_name}"


def ensure_dataset(client):
    """
    Creates the dataset if it does not exist.
    """

    dataset_id = f"{PROJECT_ID}.{DATASET_ID}"

    dataset = bigquery.Dataset(dataset_id)
    dataset.location = LOCATION

    client.create_dataset(
        dataset,
        exists_ok=True
    )

    print(f"Dataset ready : {dataset_id}")


def ensure_table(
    client,
    table_name,
    schema
):
    """
    Creates a table if it does not exist.
    """

    table_id = get_table_id(table_name)

    table = bigquery.Table(
        table_id,
        schema=schema
    )

    client.create_table(
        table,
        exists_ok=True
    )

    print(f"Table ready : {table_id}")

    return table_id


def delete_snapshot(
    client,
    table_name,
    snapshot_date
):
    """
    Deletes rows for today's snapshot.

    Makes snapshot loads idempotent.
    """

    table_id = get_table_id(table_name)

    query = f"""
    DELETE
    FROM `{table_id}`
    WHERE snapshot_date = @snapshot_date
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "snapshot_date",
                "DATE",
                snapshot_date
            )
        ]
    )

    job = client.query(
        query,
        job_config=job_config
    )

    job.result()

    print(
        f"Deleted existing rows from {table_name} "
        f"for {snapshot_date}"
    )


def truncate_table(
    client,
    table_name
):
    """
    Removes all rows from a table.
    Used for lookup tables.
    """

    table_id = get_table_id(table_name)

    query = f"""
    TRUNCATE TABLE `{table_id}`
    """

    job = client.query(query)

    job.result()

    print(f"Truncated {table_name}")


def load_rows(
    client,
    table_name,
    rows
):
    """
    Loads rows into BigQuery.
    """

    if not rows:

        print(f"No rows to load into {table_name}")

        return

    table_id = get_table_id(table_name)

    job_config = bigquery.LoadJobConfig(

        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,

        write_disposition=bigquery.WriteDisposition.WRITE_APPEND

    )

    job = client.load_table_from_json(

        rows,

        table_id,

        job_config=job_config

    )

    job.result()

    if job.errors:

        raise Exception(job.errors)

    print(

        f"Loaded {len(rows)} rows into {table_name}"

    )

def load_stage_table(
    client,
    table_name,
    rows
):
    """
    Loads rows into a staging table.

    Every run replaces the previous stage data.
    """

    table_id = get_table_id(table_name)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )

    job = client.load_table_from_json(
        rows,
        table_id,
        job_config=job_config
    )

    job.result()

    print(f"Loaded {len(rows)} rows into {table_name}")

def merge_table(client, target_table, stage_table, merge_keys, **kwargs):
    target_id = get_table_id(target_table)
    stage_id = get_table_id(stage_table)

    stage_table_ref = client.get_table(stage_id)
    columns = [field.name for field in stage_table_ref.schema]
    column_list = ", ".join(columns)

    partition_cols = ", ".join(merge_keys)

    query = f"""
    CREATE OR REPLACE TABLE `{target_id}` AS
    SELECT {column_list} FROM (
        SELECT *,
            ROW_NUMBER() OVER (
                PARTITION BY {partition_cols}
                ORDER BY loaded_at DESC
            ) AS row_num
        FROM (
            SELECT {column_list} FROM `{target_id}`
            UNION ALL
            SELECT {column_list} FROM `{stage_id}`
        )
    )
    WHERE row_num = 1
    """

    print("GENERATED QUERY:")
    print(query)

    job = client.query(query)
    job.result()
    print(f"Merged (dedup) into {target_id}")