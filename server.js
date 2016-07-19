var _ = require('underscore');

var express = require('express');
var app = express();

var dotenv = require('dotenv');
dotenv.load();

var PythonShell = require('python-shell');
var port = Number(process.env.PORT) || 3000;

var exec = require('child_process').exec;
var pg = require('pg');

var basicAuth = require('basic-auth');

var config = {
    host: process.env.PG_HOST || 'localhost',
    user: process.env.PG_USER || 'postgres',
    password: process.env.PG_PASSWORD || 'psql',
    database: process.env.PG_DB || 'tagpro',
    port: process.env.PG_PORT || 5432
};

var BASIC_AUTH = [
    {
        index_username: process.env.USERNAME,
        index_password: process.env.PASSWORD
    },
    {
        index_username: process.env.USERNAME_2,
        index_password: process.env.PASSWORD_2
    },
    {
        index_username: process.env.USERNAME_3,
        index_password: process.env.PASSWORD_3
    }
];


var pg_string = process.env.DATABASE_URL || 'postgres://' + config.user + ':' + config.password + '@' + config.host + '/' + config.database;



// needed to parse JSON data from client
var bodyParser = require('body-parser');
app.use(bodyParser.json());




app.use(express.static('public'));


app.get('/playerList', function (req, res) {
    var pg_client = new pg.Client(pg_string);
    pg_client.connect(function(err) {
        if(err) return console.error('could not connect to postgres', err);

        pg_client.query('SELECT * FROM players', function (err, result) {
            if(err) return console.error('could not query db', err);

            var players = result.rows;
            res.send(players);
            return pg_client.end();
        });
    });
});

var user_logged;

var auth = function (req,res,next){
    function unauthorized(res){
        res.set('WWW-Authenticate', 'Basic realm=Autorization Required');
        return res.sendStatus(401);
    };
    var user = basicAuth(req);
    if(!user || !user.name || !user.pass){
        return unauthorized(res);
    };
    user_logged = user.name;
    for (var i = 0; i<BASIC_AUTH.length; i++){
        if (user.name == BASIC_AUTH[i].index_username && user.pass == BASIC_AUTH[i].index_password){
            return next();
        };
    };
    return unauthorized(res);
};



app.post('/trueskill', auth, function (req, res) {
    var team1 = req.body.teams['1'];
    var team2 = req.body.teams['2'];
    var scoreTeam1 = req.body.score['1'];
    var scoreTeam2 = req.body.score['2'];
    var matchComputed = 0;

    team1ids = _.map(team1, function (player) { return player.id });
    team2ids = _.map(team2, function (player) { return player.id });

    var pg_client = new pg.Client(pg_string);
    pg_client.connect(function(err) {
        if(err) return console.error('could not connect to postgres', err);

        pg_client.query('INSERT INTO matchs (team1, team2, score1, score2, computed, added_by) VALUES ($1, $2, $3, $4, $5, $6) RETURNING id', [team1ids, team2ids, scoreTeam1, scoreTeam2, matchComputed, user_logged], function (err, result) {
            if(err) return console.error('could not query db', err);

            console.log('Added match with id', result.rows[0]['id']);
            res.send({"message": "OK"});

            PythonShell.run('main.py', function (err, results) {
                if (err) throw err;
                console.log('Score updated');

                PythonShell.run('graphs_plotly.py', function(err, results){
                    if (err) throw err;                
                    console.log('Graph updated');
                });
            });
            return pg_client.end();
        });
    });
});

app.get('/test-algo', function(req, res) {
    var pg_client = new pg.Client(pg_string);
    pg_client.connect(function(err) {
        if(err) return console.error('could not connect to postgres', err);

        pg_client.query('SELECT * FROM matchs', function (err, result) {
            if(err) return console.error('could not query db', err);

            var matchs = result.rows;
            res.send(matchs);
            return pg_client.end();
        });
    });
});

app.get('*', function (req, res) { res.status(404).send('The flag has been captured.'); });

app.listen(port, function () { console.log('Tagpro Trueskill app running on port', port); });