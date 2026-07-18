SELECT *
FROM {{ ref('fct_video_daily') }}
WHERE view_count < 0
AND like_count < 0
AND comment_count < 0