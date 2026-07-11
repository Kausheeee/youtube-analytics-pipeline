
{{
    config(
        alias = "int_video_engagement_metrics",
        materialized = "view"
    )
}}



SELECT
    video_id,
    snapshot_date,
    view_count,
    like_count,
    comment_count,
    ROUND(SAFE_DIVIDE(like_count, view_count) * 100,2) AS like_rate_pct,
    ROUND(SAFE_DIVIDE(comment_count, view_count) * 100,2) AS comment_rate_pct,
    ROUND(SAFE_DIVIDE(like_count + comment_count, view_count) * 100,2) AS engagement_rate_pct
FROM {{ ref('stg_video') }}
