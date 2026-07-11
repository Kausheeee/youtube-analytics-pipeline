# src/load/schemas.py

from google.cloud import bigquery


# -----------------------------
# Videos
# -----------------------------
VIDEO_SCHEMA = [
    bigquery.SchemaField("video_id", "STRING"),
    bigquery.SchemaField("channel_id", "STRING"),
    bigquery.SchemaField("title", "STRING"),
    bigquery.SchemaField("published_at", "TIMESTAMP"),
    bigquery.SchemaField("category_id", "INT64"),
    bigquery.SchemaField("duration_iso", "STRING"),
    bigquery.SchemaField("view_count", "INT64"),
    bigquery.SchemaField("like_count", "INT64"),
    bigquery.SchemaField("comment_count", "INT64"),
    bigquery.SchemaField("tags", "STRING", mode="REPEATED"),
    bigquery.SchemaField("snapshot_date", "DATE"),
    bigquery.SchemaField("raw_data", "STRING"),
    bigquery.SchemaField("loaded_at", "TIMESTAMP"),
]


# -----------------------------
# Comments
# -----------------------------
COMMENT_SCHEMA = [
    bigquery.SchemaField("comment_id", "STRING"),
    bigquery.SchemaField("video_id", "STRING"),
    bigquery.SchemaField("author", "STRING"),
    bigquery.SchemaField("comment_text", "STRING"),
    bigquery.SchemaField("like_count", "INT64"),
    bigquery.SchemaField("reply_count", "INT64"),
    bigquery.SchemaField("published_at", "TIMESTAMP"),
    bigquery.SchemaField("raw_data", "STRING"),
    bigquery.SchemaField("loaded_at", "TIMESTAMP"),
]


# -----------------------------
# Channels
# -----------------------------
CHANNEL_SCHEMA = [
    bigquery.SchemaField("channel_id", "STRING"),
    bigquery.SchemaField("title", "STRING"),
    bigquery.SchemaField("custom_url", "STRING"),
    bigquery.SchemaField("published_at", "TIMESTAMP"),
    bigquery.SchemaField("subscriber_count", "INT64"),
    bigquery.SchemaField("view_count_total", "INT64"),
    bigquery.SchemaField("video_count", "INT64"),
    bigquery.SchemaField("snapshot_date", "DATE"),
    bigquery.SchemaField("raw_data", "STRING"),
    bigquery.SchemaField("loaded_at", "TIMESTAMP"),
]


# -----------------------------
# Playlists
# -----------------------------
PLAYLIST_SCHEMA = [
    bigquery.SchemaField("playlist_id", "STRING"),
    bigquery.SchemaField("channel_id", "STRING"),
    bigquery.SchemaField("title", "STRING"),
    bigquery.SchemaField("description", "STRING"),
    bigquery.SchemaField("published_at", "TIMESTAMP"),
    bigquery.SchemaField("item_count", "INT64"),
    bigquery.SchemaField("loaded_at", "TIMESTAMP"),
    bigquery.SchemaField("raw_data", "STRING"),
]


# -----------------------------
# Playlist Items
# -----------------------------
PLAYLIST_ITEM_SCHEMA = [
    bigquery.SchemaField("playlist_id", "STRING"),
    bigquery.SchemaField("video_id", "STRING"),
    bigquery.SchemaField("position", "INT64"),
    bigquery.SchemaField("added_at", "TIMESTAMP"),
    bigquery.SchemaField("loaded_at", "TIMESTAMP"),
]


# -----------------------------
# Categories
# -----------------------------
CATEGORY_SCHEMA = [
    bigquery.SchemaField("category_id", "INT64"),
    bigquery.SchemaField("title", "STRING"),
    bigquery.SchemaField("assignable", "BOOL"),
    bigquery.SchemaField("loaded_at", "TIMESTAMP"),
    bigquery.SchemaField("raw_data", "STRING"),
]