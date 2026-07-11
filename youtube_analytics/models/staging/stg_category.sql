{{
config(
    alias = "stg_category",
    materialized = "view"
)
}}

SELECT
    loaded_at,
    category_id,
    title AS category_title,
    assignable
FROM {{ source('raw_youtube', 'categories_raw') }}
