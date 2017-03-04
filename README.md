#Tagpro Trueskill

##Database init

Make sure you have postgresql installed and running.

Edit the config in `pg_init.py` to your desired environment.

Run `python pg_init.py` to create the database, tables, and insert some values in them (edit `pg_init.py` accordingly).

**NOTE: every time your run `python pg_init.py` the database will be DROPPED. Don't do that on the production server.**

##Web server

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
