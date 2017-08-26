Tagpro Trueskill
=====

First time setup
-----

- Download and install [node.js](http://nodejs.org/).
- Install postgresql and have a database running.
- Clone the project in a folder somewhere.
- edit `pg_init.py` to match your own config (by default it has 2 players, MMR of 25 and sigma of 8.33)
- Open the terminal on the folder where the project is.
- run `npm install` once.
- run `python pg_init.py`
**WARNING! every time you execute this previous command, the database will be DROPPED. Don't do that on the production server.**
- run `node server.js` to start the server.

Web server
-----

The web pages are served by Express running on NodeJS. The entire project is built to be deployed on Heroku.

Create/edit a `.env` file at the root of the project, containing the PostgreSQL and plotly config info:
```
PG_HOST="localhost"
PG_USER="user"
PG_PASSWORD="password"
PG_DB="tagpro"
PG_PORT=5432
plotly_api_key="valid plotly key"
plotly_username="your plotly username"
```
You can also add usernames and password for the `simple-auth` : USERNAME, PASSWORD, USERNAME_2, PASSWORD_2 (up to 5)

Static resources (HTML pages, css, scripts, images) can be found in `/public`.

A Python script will compute the new rankings after each match.

Another Python script will plot the players' rankings through plotly.
