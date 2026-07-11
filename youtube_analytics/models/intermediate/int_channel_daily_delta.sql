
{{
config(
    alias = "int_channel_daily_delta",
    materialized = "view"
)
}}


SELECT
    channel_id,
    channel_title,
    snapshot_date,
    subscriber_count,
    view_count_total,
    video_count,
    subscriber_count - LAG(subscriber_count) OVER (
        PARTITION BY channel_id ORDER BY snapshot_date
    ) AS subscribers_gained,
    view_count_total - LAG(view_count_total) OVER (
        PARTITION BY channel_id ORDER BY snapshot_date
    ) AS views_gained
FROM {{ ref('stg_channel') }}