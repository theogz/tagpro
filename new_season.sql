with new_season as (
select
  player_id
  , now() as updated_at
  , 2500 as mmr
  , 833 as sigma
  , 10 as season
  from mmr_variations
  group by 1
)
INSERT INTO mmr_variations (player_id, updated_at, mmr, sigma, season) select * from new_season;


UPDATE players set mmr = 2500, sigma = 833;