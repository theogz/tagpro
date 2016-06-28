# -*- coding: utf-8 -*-
import pandas as pd
import trueskill as ts
# import sys
# import os


#Convention : team 1 = winner (if no draw) 
# ==> TODO :need to reorder scores from table_matchs if needed


# try:
#     table_matchs = list(sys.argv[1])
#     table_joueurs = list(sys.argv[2])
# except IndexError:
#     print "nope"

table_joueurs = pd.read_json('http://localhost:3000/playerList')
liste_joueurs = table_joueurs["id"].tolist()
niveau_joueurs = [x/100 for x in table_joueurs["mmr"].tolist()]
confiance_joueurs = [x/100 for x in table_joueurs["sigma"].tolist()]
rating_joueurs = [ts.Rating(x,y) for x,y in zip(niveau_joueurs, confiance_joueurs)]

table_matchs = pd.read_json('http://localhost:3000/test-algo')

table_matchs["Nul"] = (table_matchs["score1"]==table_matchs["score2"])+0

Caracteristiques = dict(zip(liste_joueurs, rating_joueurs))


for i in xrange(0,table_matchs.shape[0]):
    Joueurs_team_1 = table_matchs.loc[i,"team1"]
    Ratings_team_1 = [Caracteristiques[x] for x in Joueurs_team_1]
    Joueurs_team_2 = table_matchs.loc[i,"team2"]
    Ratings_team_2 = [Caracteristiques[x] for x in Joueurs_team_2]
    Victoire_1 = int((table_matchs.loc[i,"score1"]>table_matchs.loc[i,"score2"])+0)
    Victoire_2 = int((table_matchs.loc[i,"score1"]<table_matchs.loc[i,"score2"])+0)
    # We update ratings
    New_ratings_team_1, New_ratings_team_2 = ts.rate([Ratings_team_1, Ratings_team_2], ranks=[Victoire_2,Victoire_1])

    for k in xrange(0,len(Joueurs_team_1)):
        Caracteristiques[Joueurs_team_1[k]] = New_ratings_team_1[k]
    for k in xrange(0, len(Joueurs_team_2)):
        Caracteristiques[Joueurs_team_2[k]] = New_ratings_team_2[k]

liste_joueurs_nv = Caracteristiques.keys()
ratings_joueurs_nv = [int(x.mu*100) for x in Caracteristiques.values()]
confiance_joueurs_nv = [int(x.sigma*100) for x in Caracteristiques.values()]

print Caracteristiques
# output = pd.DataFrame({"id":liste_joueurs_nv, "mmr":ratings_joueurs_nv, "name": table_joueurs["name"], "sigma":confiance_joueurs_nv})

# output.to_json