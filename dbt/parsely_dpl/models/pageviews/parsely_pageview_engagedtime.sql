with pageview_events as (

    select * from {{ ref('parsely_match_hbs') }}

),

engaged_xf as (

  select
      pv.event_id,
      sum(hb.engaged_time_inc) as engaged_time
  from pageview_events hb
  left join {{ref('parsely_parent_pageview_keys')}} pv using (pageview_key)
  where hb.action = 'heartbeat' and
    hb.ts_action >= pv.ts_action and
    (case when pv.next_pageview_ts_action is not null
      then hb.ts_action < pv.next_pageview_ts_action
      else true end)
  group by pv.event_id
),

video_xf as (
  select
    pageview_key,
    sum(video_engaged_time) as video_engaged_time,
    sum(videostart_counter) as videoviews
  from {{ref('parsely_videoviews')}}
  group by pageview_key
)

select
  *
from pageview_events
left join engaged_xf using (event_id)
left join video_xf using (pageview_key)
where action = 'pageview'