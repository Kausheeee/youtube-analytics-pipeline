{{
config(
    alias = "stg_playlist_item",
    materialized = "view"
)
}}

SELECT
    loaded_at,
    playlist_id,
    video_id,
    position AS playlist_item_position,
    added_at
FROM {{ source('raw_youtube', 'playlist_items_raw') }}
