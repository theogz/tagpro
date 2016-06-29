# -*- coding: utf-8 -*-
import pandas as pd
import trueskill as ts
import psycopg2
import psycopg2.extras
import subprocess



#DB connections
conn = psycopg2.connect(dbname="tagpro", user="postgres", host="localhost", password="psql")
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


sql_matchs = "SELECT * FROM matchs;"
sql_joueurs = "SELECT * FROM players;"

#We get the tables from the database :
#players :
table_joueurs = pd.read_sql(sql_joueurs, conn, coerce_float=True, params=None)

liste_joueurs = table_joueurs["id"].tolist()
niveau_joueurs = [float(x)/100 for x in table_joueurs["mmr"].tolist()]
confiance_joueurs = [float(x)/100 for x in table_joueurs["sigma"].tolist()]
rating_joueurs = [ts.Rating(x,y) for x,y in zip(niveau_joueurs, confiance_joueurs)]

#matchs :
table_matchs = pd.read_sql(sql_matchs, conn, coerce_float=True, params=None)

#We create the dictionary based on players' current rating :
Caracteristiques = dict(zip(liste_joueurs, rating_joueurs))


#Loop that update ratings for every match played :
for i in xrange(0,table_matchs.shape[0]):
    if table_matchs.loc[i, "computed"]==0:

        #We recreate the teams, their ratings and the outcome (1,0, 0,1 or 0,0)
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


#We put everything into a new dataframe (for players) because it's simpler (the matchs dataframe has barely changed)
liste_joueurs = Caracteristiques.keys()
ratings_joueurs = [int(x.mu*100) for x in Caracteristiques.values()]
name_joueurs = table_joueurs["name"]
confiance_joueurs = [int(x.sigma*100) for x in Caracteristiques.values()]

table_joueurs_nv = pd.DataFrame({'id':liste_joueurs, 'name':name_joueurs, 'mmr':ratings_joueurs, 'sigma':confiance_joueurs})

for i in xrange(0,table_joueurs_nv.shape[0]):
    cur.execute("UPDATE players SET mmr = %s, sigma=%s WHERE id = %s;", [int(table_joueurs_nv.loc[i,"mmr"]), int(table_joueurs_nv.loc[i,"sigma"]), int(table_joueurs_nv.loc[i,"id"])])

for i in xrange(0, table_matchs.shape[0]):
    cur.execute("UPDATE matchs SET computed = %s WHERE id = %s;", [int(table_matchs.loc[i,"computed"]), int(table_matchs.loc[i,"id"])])


conn.commit()
cur.close()
conn.close()

subprocess.check_call(['Rscript', 'trueplots.R'], shell=False)


