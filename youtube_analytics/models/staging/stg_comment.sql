{{
config(
    alias = "stg_comment",
    materialized = "view"
)
}}

SELECT
    loaded_at,
    comment_id,
    video_id,
    author AS comment_author,
    comment_text,
    like_count,
    reply_count,
    published_at
FROM {{ source('raw_youtube', 'comments_raw') }}
