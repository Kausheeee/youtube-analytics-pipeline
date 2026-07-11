{{ config(materialized='table') }}

SELECT
    channel_id,
    snapshot_date,
    subscriber_count,
    view_count_total,
    video_count,
    subscribers_gained,
    views_gained
FROM {{ ref('int_channel_daily_delta') }}