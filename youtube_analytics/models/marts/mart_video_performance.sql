{{
    config(
        alias="mart_video_performance",
        materialized="table"
    )
}}

SELECT

    f.snapshot_date,

    dv.video_id,
    dv.video_title,
    dv.published_at,

    FORMAT_DATE('%A', DATE(dv.published_at)) AS weekday_name,

    dc.channel_id,
    dc.channel_title,

    dcat.category_id,
    dcat.category_title,

    dv.duration_in_minutes,

    f.view_count,
    f.like_count,
    f.comment_count,

    f.like_rate_pct,
    f.comment_rate_pct,
    f.engagement_rate_pct,

    f.views_gained,
    f.likes_gained,
    f.comments_gained

FROM {{ ref('fct_video_daily') }} f

INNER JOIN {{ ref('dim_video') }} dv
ON f.video_id = dv.video_id

INNER JOIN {{ ref('dim_channel') }} dc
ON dv.channel_id = dc.channel_id

LEFT JOIN {{ ref('dim_category') }} dcat
ON dv.category_id = dcat.category_id