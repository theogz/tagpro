DELETE FROM matchs where id >= ${match_id};

DELETE FROM players_in_team where match_id >= ${match_id};

DELETE FROM mmr_variations where updated_at >= ${date_of_match};


with last_mmr as (
select
	mmr_variations.player_id
	, mmr_variations.mmr
	, mmr_variations.sigma
from 
	mmr_variations
inner join
(select player_id, max(updated_at) as latest_update from mmr_variations group by 1) latest_mmr
on (latest_mmr.player_id = mmr_variations.player_id and latest_mmr.latest_update = mmr_variations.updated_at)
)
update 
	players 
set mmr = last_mmr.mmr, sigma  = last_mmr.sigma
from last_mmr
where players.id = last_mmr.player_id;


