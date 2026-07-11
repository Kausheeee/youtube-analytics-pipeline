{{
    config(
        alias="mart_channel_performance",
        materialized="table"
    )
}}

SELECT

    f.snapshot_date,

    dc.channel_id,
    dc.channel_title,

    f.subscriber_count,
    f.view_count_total,
    f.video_count,

    f.subscribers_gained,
    f.views_gained

FROM {{ ref('fct_channel_daily') }} f

INNER JOIN {{ ref('dim_channel') }} dc
ON f.channel_id = dc.channel_id