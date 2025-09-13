{{ config(
    materialized='incremental',
    unique_key='channel_id',
    incremental_strategy='merge'
) }}

select DISTINCT vs.channel_id, ci.channel_title
from
	(select ts.video_id, ts.day_streak from trending_streak ts limit 10) as top_10_videos
left join video_stats vs on top_10_videos.video_id = vs.video_id
left join channel_infos ci on vs.channel_id = ci.channel_id