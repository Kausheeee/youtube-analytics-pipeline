
{{
config(
    alias = "stg_video",
    materialized = "view"
)
}}

SELECT 
    loaded_at,
    video_id,
    title AS video_title,
    channel_id,
    published_at,
    like_count,
    view_count,
    comment_count,
    tags,
    ROUND(
    (
        COALESCE(CAST(REGEXP_EXTRACT(duration_iso, r'(\d+)H') AS INT64), 0) * 3600 +
        COALESCE(CAST(REGEXP_EXTRACT(duration_iso, r'(\d+)M') AS INT64), 0) * 60 +
        COALESCE(CAST(REGEXP_EXTRACT(duration_iso, r'(\d+)S') AS INT64), 0)
    )/ 60 ,2) AS duration_in_minutes,
    category_id,
    snapshot_date
FROM {{ source('raw_youtube', 'videos_raw') }}