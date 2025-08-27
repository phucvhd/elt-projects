{{ config(
    materialized='incremental',
    unique_key='video_id',
    incremental_strategy='merge'
) }}

select video_id, count(*) as day_streak from video_stats vs group by video_id having count(*) > 1 order by day_streak desc