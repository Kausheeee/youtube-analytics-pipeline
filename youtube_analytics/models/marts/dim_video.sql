
{{ config(materialized='table') }}

WITH latest_video AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY video_id
            ORDER BY snapshot_date DESC
        ) AS row_num
    FROM {{ ref('stg_video') }}
)

SELECT
    vlatest_video.video_id,
    vlatest_video.channel_id,
    vlatest_video.video_title,
    vlatest_video.published_at,
    vlatest_video.category_id,
    vlatest_video.view_count,
    vlatest_video.like_count,
    vlatest_video.comment_count,
    vlatest_video.duration_in_minutes,
    vlatest_video.tags,

    dchannel.channel_title
FROM latest_video AS vlatest_video
LEFT JOIN {{ ref('dim_channel') }} AS dchannel
    ON vlatest_video.channel_id = dchannel.channel_id
WHERE row_num = 1