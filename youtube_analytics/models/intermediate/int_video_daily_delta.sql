{{
config(
    alias = "int_video_daily_delta",
    materialized = "view"
)
}}


SELECT
    video_id,
    video_title,
    channel_id,
    snapshot_date,
    view_count,
    like_count,
    comment_count,
    view_count - LAG(view_count) OVER (
        PARTITION BY video_id ORDER BY snapshot_date
    ) AS views_gained,
    like_count - LAG(like_count) OVER (
        PARTITION BY video_id ORDER BY snapshot_date
    ) AS likes_gained,
    comment_count - LAG(comment_count) OVER (
        PARTITION BY video_id ORDER BY snapshot_date
    ) AS comments_gained
FROM {{ ref('stg_video') }}
