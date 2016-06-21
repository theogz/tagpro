import psycopg2
import psycopg2.extras


# Connect to root database to create tagpro database
conn = psycopg2.connect(dbname="postgres", user="cyril", host="localhost", port=5432)
conn.set_isolation_level(0)

# Open a cursor to perform database operations
cur = conn.cursor()

# Drop the databse if exists
cur.execute("DROP DATABASE IF EXISTS tagpro")
# Create the database
cur.execute("CREATE DATABASE tagpro")

# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()

# Connect to tagpro database and seed it
conn = psycopg2.connect(dbname="tagpro", user="cyril", host="localhost")

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Create the table of players and the first players
cur.execute("CREATE TABLE players (id serial PRIMARY KEY, name varchar, mmr integer default 0);")
cur.execute("INSERT INTO players (name) VALUES (%s);", ["HashtagYolo"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["R0xx0r"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["Batamanq"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["CousinVic"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["EkiLouly"])
cur.execute("INSERT INTO players (name) VALUES (%s);", ["DataArtist"])

# Make sure we have all the players
cur.execute("SELECT count(*) FROM players;")
print '%d players added to database' % cur.fetchone()['count']

# Create the table of matchs and the first match
cur.execute("CREATE TABLE matchs (id serial PRIMARY KEY, team1 integer[], team2 integer[], score1 integer, score2 integer);")
cur.execute("INSERT INTO matchs (team1, team2, score1, score2) VALUES (%s, %s, %s, %s);", [[1,2], [3,4], 7, 4])

# Make sure we have the match
cur.execute("SELECT * FROM matchs;")
match = cur.fetchone()
print 'match ID %d: team %s vs team %s, score %d-%d' % (match['id'], match['team1'], match['team2'], match['score1'],  match['score2'])

conn.commit()

cur.close()
conn.close()
