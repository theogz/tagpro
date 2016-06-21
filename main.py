import pandas as pd
import trueskill as ts

matchs = pd.read_csv("3. resultat.csv", sep=";")




Caracteristiques = dict.fromkeys(Joueurs, ts.Rating())


# il y a matches.shape[0] matchs au total
# xrange(0,matchs.shape[0]) va de 0 a match.shape[0]-1

for i in xrange(0,matchs.shape[0]):
    Joueurs_team_1 = matchs.iloc[i,1].split("//")
    Ratings_team_1 = [Caracteristiques[x] for x in Joueurs_team_1]
    Joueurs_team_2 = matchs.iloc[i,2].split("//")
    Ratings_team_2 = [Caracteristiques[x] for x in Joueurs_team_2]

    New_ratings_team_1, New_ratings_team_2 = ts.rate([Ratings_team_1, Ratings_team_2], ranks=[0,1-matchs.iloc[i,3]])

    for k in xrange(0,len(Joueurs_team_1)):
        Caracteristiques[Joueurs_team_1[k]] = New_ratings_team_1[k]
    for k in xrange(0, len(Joueurs_team_2)):
        Caracteristiques[Joueurs_team_2[k]] = New_ratings_team_2[k]

Liste_joueurs = Caracteristiques.keys()
Liste_mus = [x.mu for x in Caracteristiques.values()]
Liste_sigmas = [x.sigma for x in Caracteristiques.values()]

output = pd.DataFrame({'Joueur':Liste_joueurs, 'Niveau':Liste_mus, 'Incertitude':Liste_sigmas})
colonnes = ['Joueur', 'Niveau', 'Incertitude']
output = output[colonnes]

output = output.sort_values(by='Niveau', ascending=False)

output.to_csv("5. Classement.csv", sep=";", decimal=",", index=False, index_label=False)
