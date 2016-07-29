# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Wed Jul 27 16:33:42 2016

@author: tgantzer
"""

import pandas as pd
import sys
import os
import trueskill as ts
import itertools
import psycopg2
import psycopg2.extras



#DB connections
conn = psycopg2.connect(host=os.getenv('PG_HOST', 'localhost'), port=os.getenv('PG_PORT', 5432), user=os.getenv('PG_USER', 'postgres'), password=os.getenv('PG_PASSWORD', 'psql'), dbname=os.getenv('PG_DB', 'tagpro'))
# conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

sql_joueurs = "SELECT * FROM players;"

table_joueurs = pd.read_sql(sql_joueurs, conn, coerce_float=True, params=None)
liste_joueurs = table_joueurs["id"].tolist()
niveau_joueurs = [float(x)/100 for x in table_joueurs["mmr"].tolist()]
confiance_joueurs = [float(x)/100 for x in table_joueurs["sigma"].tolist()]
rating_joueurs = [ts.Rating(x,y) for x,y in zip(niveau_joueurs, confiance_joueurs)]
Caracteristiques = dict(zip(liste_joueurs, rating_joueurs))


try:
    pool_joueurs = [int(ids) for ids in sys.argv[1:]]
except IndexError:
    pool_joueurs = liste_joueurs[7:]




#In tagpro, maximum of 924 combinations, computation is quick.

Best_quality = 0
Best_team_1 = []
Best_team_2 = []
for subset in itertools.combinations(pool_joueurs, len(pool_joueurs)/2):
    Joueurs_team_1 = list(subset)
    Joueurs_team_2 = [joueur for joueur in pool_joueurs if joueur not in subset]
    Ratings_team_1 = [Caracteristiques[x] for x in Joueurs_team_1]
    Ratings_team_2 = [Caracteristiques[x] for x in Joueurs_team_2]
    if ts.quality([Ratings_team_1, Ratings_team_2])>Best_quality:
        Best_quality = ts.quality([Ratings_team_1, Ratings_team_2])
        Best_team_1 = Joueurs_team_1
        Best_team_2 = Joueurs_team_2
        

conn.commit()
cur.close()
conn.close()


print Best_team_1
print Best_team_2