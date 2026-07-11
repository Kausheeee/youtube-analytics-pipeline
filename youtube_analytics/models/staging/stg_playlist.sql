
{{
config(
    alias = "stg_playlist",
    materialized = "view"
)
}}


SELECT
    loaded_at,
    playlist_id,
    title AS playlist_title,
    description AS playlist_description,
    channel_id,
    item_count,
    published_at
FROM {{ source('raw_youtube', 'playlists_raw') }}