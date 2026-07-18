
SELECT *
FROM {{ ref('fct_video_daily') }}
WHERE engagement_rate_pct < 0
   OR engagement_rate_pct > 100 