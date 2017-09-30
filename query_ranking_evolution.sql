with last_2_mmrs as (
	select
		player_id
		, mmr
		, sigma
		, updated_at
		, 2-row_number() OVER (partition by player_id order by updated_at desc) as period
		, last.latest_update
	from
		mmr_variations
	inner join (select max(updated_at) as latest_update from mmr_variations) last
	on TRUE
), player_played_last_game as (
	select
		player_id
		, max(case when updated_at = latest_update then 1 else 0 end) as played_last_game
	from
		last_2_mmrs
	where
		period >= 0
	group by
		player_id

), period_comparison as (
	select 
		last_2_mmrs.player_id
		, sum(case when player_played_last_game.played_last_game = 1 then (1-last_2_mmrs.period)*last_2_mmrs.mmr 
			else last_2_mmrs.period*last_2_mmrs.mmr end) as mmr_0
		, sum(case when player_played_last_game.played_last_game = 1 then (1-last_2_mmrs.period)*last_2_mmrs.sigma 
			else last_2_mmrs.period*last_2_mmrs.sigma end) as sigma_0		
		, sum(last_2_mmrs.period*last_2_mmrs.mmr) as mmr_1
		, sum(last_2_mmrs.period*last_2_mmrs.sigma) as sigma_1		
		from
			last_2_mmrs
		inner join
			player_played_last_game
		on
			player_played_last_game.player_id = last_2_mmrs.player_id
		where
			last_2_mmrs.period >= 0
		group by
			last_2_mmrs.player_id
), ranks as (
	select
		player_id
		, RANK() over (order by mmr_0-3*sigma_0 DESC) as rank_0
		, RANK() over (order by mmr_1-3*sigma_1 DESC) as rank_1
		, mmr_1 as mmr
		, sigma_1 as sigma
	from
		period_comparison
)
select
	ranks.player_id
	, players.name
	, ranks.mmr
	, ranks.sigma
	, case when (ranks.rank_0 - ranks.rank_1 > 0) then 1
	when (ranks.rank_0 - ranks.rank_1 < 0) then -1
	else 0 end as rank_improved
	, COALESCE(pit.nb_matchs, 0) as nb_matchs
from
	ranks
inner join
	players
on
	players.id = ranks.player_id
left join
	(SELECT player_id, count(*) nb_matchs FROM players_in_team WHERE season = ${season} GROUP BY player_id) pit
on pit.player_id = ranks.player_id
order by ranks.mmr-3*ranks.sigma desc;