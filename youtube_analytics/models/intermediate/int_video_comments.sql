

{{
config(
    alias = "int_video_comments",
    materialized = "view"
)
}}

SELECT
    video_id,
    COUNT(*) AS total_comments_fetched,
    SUM(like_count) AS total_comment_likes,
    SUM(reply_count) AS total_replies,
    ROUND(AVG(LENGTH(comment_text)), 2) AS avg_comment_length
FROM {{ ref('stg_comment') }}
GROUP BY video_id