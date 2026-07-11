{{ config(materialized='table') }}

SELECT

    v.video_id,

    v.snapshot_date,

    v.view_count,
    v.like_count,
    v.comment_count,

    e.engagement_rate_pct,
    e.like_rate_pct,
    e.comment_rate_pct,

    d.views_gained,
    d.likes_gained,
    d.comments_gained

FROM {{ ref('stg_video') }} v

LEFT JOIN {{ ref('int_video_engagement_metrics') }} e
USING(video_id, snapshot_date)

LEFT JOIN {{ ref('int_video_daily_delta') }} d
USING(video_id, snapshot_date)