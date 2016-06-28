# -*- coding: utf-8 -*-
import pandas as pd
import trueskill as ts
import psycopg2
import psycopg2.extras
# import sys
# import os


# try:
#     table_matchs = list(sys.argv[1])
#     table_joueurs = list(sys.argv[2])
# except IndexError:
#     print "nope"

#DB connections
conn = psycopg2.connect(dbname="tagpro", user="postgres", host="localhost", password="psql")
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


sql_matchs = "SELECT * FROM matchs;"
sql_joueurs = "SELECT * FROM players;"


table_joueurs = pd.io.sql.read_sql(sql_joueurs, conn, coerce_float=True, params=None)
liste_joueurs = table_joueurs["id"].tolist()
niveau_joueurs = [x/100 for x in table_joueurs["mmr"].tolist()]
confiance_joueurs = [x/100 for x in table_joueurs["sigma"].tolist()]
rating_joueurs = [ts.Rating(x,y) for x,y in zip(niveau_joueurs, confiance_joueurs)]

table_matchs = pd.io.sql.read_sql(sql_matchs, conn, coerce_float=True, params=None)


Caracteristiques = dict(zip(liste_joueurs, rating_joueurs))


for i in xrange(0,table_matchs.shape[0]):
    if table_matchs.loc[i, "computed"]==0:
        Joueurs_team_1 = table_matchs.loc[i,"team1"]
        Ratings_team_1 = [Caracteristiques[x] for x in Joueurs_team_1]
        Joueurs_team_2 = table_matchs.loc[i,"team2"]
        Ratings_team_2 = [Caracteristiques[x] for x in Joueurs_team_2]
        Victoire_1 = int((table_matchs.loc[i,"score1"]>table_matchs.loc[i,"score2"])+0)
        Victoire_2 = int((table_matchs.loc[i,"score1"]<table_matchs.loc[i,"score2"])+0)
        #We "simulate" the match
        New_ratings_team_1, New_ratings_team_2 = ts.rate([Ratings_team_1, Ratings_team_2], ranks=[Victoire_2,Victoire_1])

        # We update ratings
        for k in xrange(0,len(Joueurs_team_1)):
            Caracteristiques[Joueurs_team_1[k]] = New_ratings_team_1[k]
        for k in xrange(0, len(Joueurs_team_2)):
            Caracteristiques[Joueurs_team_2[k]] = New_ratings_team_2[k]

        #We make sure not to take the match into the algorithm anymore
        table_matchs.loc[i, "computed"]=1

liste_joueurs_nv = Caracteristiques.keys()
ratings_joueurs_nv = [int(x.mu*100) for x in Caracteristiques.values()]
confiance_joueurs_nv = [int(x.sigma*100) for x in Caracteristiques.values()]

print Caracteristiques
print table_matchs
# output = pd.DataFrame({"id":liste_joueurs_nv, "mmr":ratings_joueurs_nv, "name": table_joueurs["name"], "sigma":confiance_joueurs_nv})

# output.to_json