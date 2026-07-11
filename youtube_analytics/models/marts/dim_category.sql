{{ config(materialized='table') }}

SELECT
    category_id,
    category_title
FROM {{ ref('stg_category') }}