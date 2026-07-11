
{{
config(
    alias = "int_playlist_details",
    materialized = "view"
)
}}

SELECT 
    playlist.loaded_at,
    playlist.channel_id,
    playlist.playlist_id,
    playlist.playlist_title,
    playlist.playlist_description,
    playlist_item.video_id,
    playlist.item_count,
    playlist.published_at,
    playlist_item.playlist_item_position
FROM {{ref('stg_playlist')}} AS playlist 

LEFT JOIN {{ref('stg_playlist_item')}} AS playlist_item 
    ON playlist.playlist_id = playlist_item.playlist_id

ORDER BY playlist.playlist_id
