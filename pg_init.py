import psycopg2
import psycopg2.extras
import os

# Connect to root database to create tagpro database
conn = psycopg2.connect(host=os.getenv('PG_HOST', 'localhost'), port=os.getenv('PG_PORT', 5432), user=os.getenv('PG_USER', 'postgres'), password=os.getenv('PG_PASSWORD', 'psql'), dbname=os.getenv('PG_DB', 'tagpro'))
# conn = psycopg2.connect(os.environ['DATABASE_URL'])
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
conn = psycopg2.connect(host=os.getenv('PG_HOST', 'localhost'), port=os.getenv('PG_PORT', 5432), user=os.getenv('PG_USER', 'postgres'), password=os.getenv('PG_PASSWORD', 'psql'), dbname=os.getenv('PG_DB', 'tagpro'))
# conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Create the table of players and the first players
cur.execute("DROP TABLE IF EXISTS players;")
cur.execute("CREATE TABLE players (id serial PRIMARY KEY, name varchar, mmr integer default 2500, sigma integer default 833);")
cur.execute("INSERT INTO players (name) VALUES (%s);", ["Hashtag_Yolo"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["R0xx0r"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["Ekisomox"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["Batamanq"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["Cousinvic"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["Nulos"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["FonkyNuma"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["Bouboule"])

# Make sure we have all the players
cur.execute("SELECT count(*) FROM players;")
print '%d players added to database' % cur.fetchone()['count']

# Create the table of matchs and the first match
cur.execute("DROP TABLE IF EXISTS matchs")
cur.execute("CREATE TABLE matchs (id serial PRIMARY KEY, team1 integer[], team2 integer[], score1 integer, score2 integer, computed integer, season integer, added_at timestamp DEFAULT current_timestamp, added_by varchar);")


# Create the table of players in matchs
cur.execute("DROP TABLE IF EXISTS players_in_team;")
cur.execute("CREATE TABLE players_in_team (id serial PRIMARY KEY, player_id integer, team integer, match_id integer, season integer);")

# Create the table of mmr historical variations
cur.execute("DROP TABLE IF EXISTS mmr_variations;")
cur.execute("CREATE TABLE mmr_variations (id serial PRIMARY KEY, player_id integer, last_update timestamp DEFAULT current_timestamp, mmr integer, sigma integer);")

# Make sure we have the match
# cur.execute("SELECT * FROM matchs;")
# match = cur.fetchone()
# print 'match ID %d: team %s vs team %s, score %d-%d' % (match['id'], match['team1'], match['team2'], match['score1'],  match['score2'])

conn.commit()

cur.close()
conn.close()
