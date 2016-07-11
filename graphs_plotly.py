import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import psycopg2
import psycopg2.extras
import numpy as np
from scipy.stats import norm
import os


py.sign_in(os.getenv('plotly_api_key'), os.getenv('plotly_username'))

x_min = 0
x_max = 59.9
stepz = 600

conn = psycopg2.connect(host=os.getenv('PG_HOST', 'localhost'), port=os.getenv('PG_PORT', 5432), user=os.getenv('PG_USER', 'postgres'), password=os.getenv('PG_PASSWORD', 'psql'), dbname=os.getenv('PG_DB', 'tagpro'))
# conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


sql_joueurs = "SELECT * FROM players;"
table_joueurs = pd.read_sql(sql_joueurs, conn, coerce_float=True, params=None)

table_joueurs = table_joueurs.loc[:, table_joueurs.columns !='id']
table_joueurs.columns = ["Joueur", "Niveau", "Confiance"]
table_joueurs[["Niveau", "Confiance"]] = table_joueurs[["Niveau", "Confiance"]].div(100)

nb_joueurs = table_joueurs.shape[0]
table_joueurs = table_joueurs.sort_values(by="Niveau", ascending=False)

scope = np.linspace(x_min,x_max, stepz)

data_for_graph = pd.DataFrame(scope)


for i in xrange(0, nb_joueurs):
    data_for_graph.loc[:,i+1]=[norm.pdf(x, loc=table_joueurs.iloc[i, 1], scale=table_joueurs.iloc[i, 2]) for 
    x in scope]

data_for_graph.columns = ["Abscisse"]+[joueur for joueur in table_joueurs["Joueur"]]


traces = [go.Scatter(
    x = data_for_graph["Abscisse"],
    y = data_for_graph[col],
    name = col,
    fill = 'tozerox',
    hoverinfo = 'text+name',
    text=[table_joueurs[table_joueurs["Joueur"]==col]["Niveau"] for i in xrange(0,data_for_graph.shape[0])]
) for col in data_for_graph.iloc[:,1:].columns]

layout = go.Layout(title='Ranking tagpro')
donnees=traces
fig = go.Figure(data=donnees, layout=layout )
py.plot(fig, filename='ranking-tag', auto_open=False)
