DELETE FROM matchs where id = 605;

DELETE FROM players_in_team where match_id = 605;

DELETE FROM mmr_variations where updated_at = '2017-10-03 15:21:23.37692';


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


