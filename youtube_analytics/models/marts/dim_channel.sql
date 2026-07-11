
{{
    config (
        alias = "dim_channel",
        materialized = "table"
    )
}}

WITH latest_channel AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY channel_id
            ORDER BY snapshot_date DESC
        ) AS row_num
    FROM {{ ref('stg_channel') }}
)

SELECT
 channel_id,
 channel_title,
 custom_url,
 published_at,
 subscriber_count,
 view_count_total,
 video_count
FROM latest_channel
WHERE row_num = 1