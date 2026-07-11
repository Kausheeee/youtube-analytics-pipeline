{{
    config(
        alias="mart_playlist_performance",
        materialized="table"
    )
}}

WITH latest_video_stats AS (
    SELECT *
    FROM {{ ref('fct_video_daily') }}
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY video_id ORDER BY snapshot_date DESC
    ) = 1
)

SELECT
    dp.playlist_id,
    dp.playlist_title,
    dc.channel_title,
    COUNT(DISTINCT dv.video_id) AS total_videos,
    SUM(f.view_count) AS total_views,
    SUM(f.like_count) AS total_likes,
    SUM(f.comment_count) AS total_comments,
    ROUND(AVG(f.engagement_rate_pct), 2) AS avg_engagement_rate
FROM {{ ref('dim_playlist') }} dp
LEFT JOIN {{ ref('dim_video') }} dv ON dp.video_id = dv.video_id
LEFT JOIN latest_video_stats f ON dv.video_id = f.video_id
LEFT JOIN {{ ref('dim_channel') }} dc ON dp.channel_id = dc.channel_id
GROUP BY dp.playlist_id, dp.playlist_title, dc.channel_title