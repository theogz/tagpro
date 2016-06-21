#Tagpro Trueskill

##Database init

Make sure you have postgresql installed and running.

Edit the config in `pg_init.py` to your desired environment.

Run `python pg_init.py` to create the database, tables, and insert some values in them (edit `pg_init.py` accordingly).

**NOTE: every time your run `python pg_init.py` the database will be DROPPED. Don't do that on the production server.**

##Web server

The web pages are served by Express running on NodeJS.

Run `node server.js` to start the server (default port is 3000, edit according to your needs).

Static resources (HTML pages, css, scripts, images) can be found in `/public`.

##Trueskill score update

TODO: After each match is inserted in database, a Python script is run to update each player's Trueskill score.