# -*- coding: utf-8 -*-
import pandas as pd
import trueskill as ts
import numpy as np
import sys
import os


#Convention : team 1 = winner (if no draw)

# try:
#     table_matchs = list(sys.argv[1])
#     table_joueurs = list(sys.argv[2])
# except IndexError:
#     print "nope"

table_joueurs = pd.read_json('http://localhost:3000/playerList')
liste_joueurs = table_joueurs["name"].tolist()
niveau_joueurs = [x/100 for x in table_joueurs["mmr"].tolist()]
confiance_joueurs = [x/100 for x in table_joueurs["sigma"].tolist()]
table_matchs = pd.read_json('http://localhost:3000/test-algo')

table_matchs["Nul"] = (table_matchs["score1"]==table_matchs["score2"])+0


print table_matchs
Caracteristiques = dict(zip(liste_joueurs, zip(niveau_joueurs, confiance_joueurs)))



# print jsone.tail(1)