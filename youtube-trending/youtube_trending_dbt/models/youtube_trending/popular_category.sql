{{ config(
    materialized='incremental',
    unique_key='category_id',
    incremental_strategy='merge'
) }}

with category_count as
	(select category_id, count(*) as video_count from video_stats vs group by category_id)
select vc.category_id, vc.category_name, cc.video_count from video_categories vc join category_count cc on cc.category_id = vc.category_id
order by video_count desc limit 10