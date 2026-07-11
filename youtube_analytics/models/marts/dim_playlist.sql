

{{
    config (
        alias = "dim_playlist",
        materialized = "table"
    )
}}


SELECT 
    playlist_id,
    playlist_title,
    playlist_description,
    channel_id,
    published_at,
    item_count,
    video_id,
    playlist_item_position
FROM {{ ref('int_playlist_details') }}