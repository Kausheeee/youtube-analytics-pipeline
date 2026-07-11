
{{
config(
    alias = "int_video_with_channel",
    materialized = "view"
)
}}

SELECT
    v.video_id,
    v.channel_id,
    c.channel_title,
    v.video_title,
    v.published_at,
    v.category_id,
    v.duration_in_minutes,
    v.view_count,
    v.like_count,
    v.comment_count,
    v.tags,
    v.snapshot_date,
    c.subscriber_count,
    cat.category_title
FROM {{ ref('stg_video') }} v
LEFT JOIN {{ ref('stg_channel') }} c
    ON v.channel_id = c.channel_id
    AND v.snapshot_date = c.snapshot_date
LEFT JOIN {{ref('stg_category')}} cat
    ON v.category_id = cat.category_id