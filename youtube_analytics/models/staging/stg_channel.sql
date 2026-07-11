{{
config(
    alias = "stg_channel",
    materialized = "view"
)
}}

SELECT
    loaded_at,
    channel_id,
    title AS channel_title,
    custom_url,
    published_at,
    subscriber_count,
    view_count_total,
    video_count,
    snapshot_date
FROM {{ source('raw_youtube', 'channels_raw') }}
