import psycopg2
import psycopg2.extras
import os

# Connect to root database to create tagpro database
# conn = psycopg2.connect(dbname="postgres", user="postgres", host="localhost", port=5432, password="psql")
conn = psycopg2.connect(os.environ['DATABASE_URL'])
conn.set_isolation_level(0)

# Open a cursor to perform database operations
# cur = conn.cursor()

# # Drop the databse if exists
# cur.execute("DROP DATABASE IF EXISTS tagpro")
# # Create the database
# cur.execute("CREATE DATABASE tagpro")

# # Make the changes to the database persistent
# conn.commit()

# # Close communication with the database
# cur.close()
# conn.close()

# Connect to tagpro database and seed it
# conn = psycopg2.connect(dbname="tagpro", user="postgres", host="localhost", password="psql")
conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Create the table of players and the first players
cur.execute("DROP TABLE players;")
cur.execute("CREATE TABLE players (id serial PRIMARY KEY, name varchar, mmr integer default 2500, sigma integer default 833);")
cur.execute("INSERT INTO players (name) VALUES (%s);", ["HashtagYolo"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["R0xx0r"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["Batamanq"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["CousinVic"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["EkiLouly"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["Ekisomox"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["Ancestro"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["FonkyNuma"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["Ironballs"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["Sniper"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["Nulos"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["Jisk"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["EkiBB"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["Bouboule"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["EkiPro"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["EDD"])

# Make sure we have all the players
cur.execute("SELECT count(*) FROM players;")
print '%d players added to database' % cur.fetchone()['count']

# Create the table of matchs and the first match
cur.execute("DROP TABLE matchs")
cur.execute("CREATE TABLE matchs (id serial PRIMARY KEY, team1 integer[], team2 integer[], score1 integer, score2 integer, computed integer);")
# cur.execute("INSERT INTO matchs (team1, team2, score1, score2, computed) VALUES (%s, %s, %s, %s, %s);", [[1,2], [3,4], 5, 2, 0])

# Make sure we have the match
# cur.execute("SELECT * FROM matchs;")
# match = cur.fetchone()
# print 'match ID %d: team %s vs team %s, score %d-%d' % (match['id'], match['team1'], match['team2'], match['score1'],  match['score2'])

conn.commit()

cur.close()
conn.close()
