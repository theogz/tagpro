#Tagpro Trueskill

##Database init

Make sure you have postgresql installed and running.

Edit the config in `pg_init.py` to your desired environment.

Run `python pg_init.py` to create the database, tables, and insert some values in them (edit `pg_init.py` accordingly).

**NOTE: every time your run `python pg_init.py` the database will be DROPPED. Don't do that on the production server.**

##Web server

The web pages are served by Express running on NodeJS. The entire project is built to be deployed on Heroku.

Create/edit a `.env` file at the root of the project, containing the PostgreSQL config info:
```
PG_HOST="localhost"
PG_USER="user"
PG_PASSWORD="password"
PG_DB="tagpro"
PG_PORT=5432
```

Create/edit a `.Rprofile` file at the root of the project, containing the PostgreSQL and plotly config info:
```
Sys.setenv("plotly_api_key"="plotly_key")
Sys.setenv("plotly_username"="plotly_user")
Sys.setenv("PG_HOST"="localhost")
Sys.setenv("PG_PORT"=5432)
Sys.setenv("PG_USER"="user")
Sys.setenv("PG_PASSWORD"="password")
Sys.setenv("PG_DB"="tagpro")
 
```

Run `heroku local` to start the server (default port is 5000, edit according to your needs).

Static resources (HTML pages, css, scripts, images) can be found in `/public`.

##Trueskill score update

TODO: After each match is inserted in database, a Python script is run to update each player's Trueskill score.