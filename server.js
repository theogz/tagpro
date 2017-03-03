var _ = require('underscore');

var express = require('express');
var app = express();
app.set('view engine', 'pug');

// var dotenv = require('dotenv');
// dotenv.load();
require('dotenv').config();

var PythonShell = require('python-shell');
var port = Number(process.env.PORT) || 3000;

var exec = require('child_process').exec;
var pg = require('pg');

var async = require('async');

var basicAuth = require('basic-auth');

var config = {
    host: process.env.PG_HOST || 'localhost',
    user: process.env.PG_USER || 'postgres',
    password: process.env.PG_PASSWORD || 'psql',
    database: process.env.PG_DB || 'tagpro',
    port: process.env.PG_PORT || 5432,
    max: 16,
    idleTiemoutMillis: 12000,
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
    },
    {
        index_username: process.env.USERNAME_4,
        index_password: process.env.PASSWORD_4
    },
    {
        index_username: process.env.USERNAME_5,
        index_password: process.env.PASSWORD_5
    }
];



var season = 5;

// needed to parse JSON data from client
var bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(express.static('public'));

var pg_string = process.env.DATABASE_URL || 'postgres://' + config.user + ':' + config.password + '@' + config.host + '/' + config.database;
var pg_pool = new pg.Pool(config); // Setup our Postgres Client


app.get('/players/:id', function(req, res) {
    pg_pool.connect(function(err, client, done) {
        if(err) return console.error('cant connect to pg', err);

        var player_id = req.params.id;
        var query = "SELECT a.*, b.rank FROM players a INNER JOIN (Select id,rank() over (order by mmr-3*sigma desc) as rank from players) b "+
        "on (a.id = b.id) WHERE a.id="+player_id+";"

        client.query(query, function (err, result) {
            if(err) return console.error('random error db', err);
            if(!result.rows || result.rows.length === 0) {res.status(404).send('Erard 404 : ce joueur n\'existe pas'); return console.log('Player ID not found', player_id)};

            var player = result.rows[0];

            var query = "SELECT * FROM matchs m INNER JOIN (SELECT match_id, team FROM players_in_team WHERE player_id="+player_id+") t ON m.id = t.match_id ORDER BY added_at DESC LIMIT 25;"
            client.query(query, function (err, result) {
                done();
                if(err) return console.error('random error db', err);

                if(!result.rows || result.rows.length === 0) {var matchs=[];res.render('players_template', {title: player.name, player_stats: player, matchs_table:matchs}); return console.log('No match found', player_id);};
                var matchs = result.rows;
                res.render('players_template', {
                    title: player.name,
                    player_stats: player,
                    matchs_table: matchs
                });
            });
        });
    });
});

app.get('/matchs/:id', function(req, res) {
    pg_pool.connect(function(err, client, done) {
        if(err) return console.error('cant connect to pg', err);
        var match_id = req.params.id;
        var query = `SELECT pit.player_id, pit.team, pl.name
        FROM players_in_team pit 
        INNER JOIN (SELECT id, name FROM players) pl 
        ON (pit.player_id = pl.id)
        WHERE pit.match_id=`+match_id+`;`


        client.query(query, function (err, result) {
            if(err) return console.error('random error db', err);
            if(!result.rows || result.rows.length === 0) {res.status(404).send('Erard 404 : ce match n\'existe pas'); return console.log('Match ID not found', match_id)};
            
            var match_compo = result.rows;

            var query = `SELECT id, score1, score2, added_by, added_at
            FROM matchs
            WHERE id=`+match_id+`;`
            client.query(query, function(err, result) {
                done();
                if(err) return console.error('db error', err);
                var match_info = result.rows[0];
                res.render('matchs_template', {
                    title: 'Match n°'+match_info.id,
                    match_info: match_info,
                    match_compo: match_compo
                });
            });
        });
    });
});

app.get('/playerList', function (req, res) {
    pg_pool.connect(function(err, client, done) {
        if(err) return console.error('could not connect to pool', err);

        client.query('SELECT * FROM players ORDER by (mmr-3*sigma) desc', function (err, result) {
            done();
            if(err) return console.error('could not query db', err);
            var players = result.rows;
            res.send(players);
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

app.post('/addplayer', auth, function(req, res){
    var player_name = req.body.player_name;
    pg_pool.connect(function(err, client, done) {
        if(err) return console.error('could not connect to pool', err);

        client.query("INSERT INTO players (name) SELECT ($1) WHERE NOT EXISTS (SELECT 1 from players where name = '"+player_name+"' ) RETURNING id", [player_name], function (err, result) {
            done();
            if(err) return console.error('could not connect to poolish', err);
            if (result.rows[0]) {
                console.log('Added player with id', result.rows[0]['id']);
                return res.send({"message": "OK"});
            } else return res.status(403).send('Player already in database');
        });
    });
});

app.post('/trueskill', auth, function (req, res) {
    var team1 = req.body.teams['1'];
    var team2 = req.body.teams['2'];
    var scoreTeam1 = req.body.score['1'];
    var scoreTeam2 = req.body.score['2'];
    var matchComputed = 0;

    var team1ids = _.map(team1, function (player) { return {id: player.id, team: '1'}; });
    var team2ids = _.map(team2, function (player) { return {id: player.id, team: '2'}; });
    var concat_teams = team1ids.concat(team2ids);

    pg_pool.connect(function(err, client, done) {
        if(err) return console.error('could not connect to pool', err);


        client.query('INSERT INTO matchs (team1, team2, score1, score2, computed, season, added_by) VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING id', [_.map(team1ids, el => el.id), _.map(team2ids, el => el.id), scoreTeam1, scoreTeam2, matchComputed, season, user_logged], function (err, result) {
            if(err) return console.error('could not query db', err);

            var match_id = result.rows[0]['id'];

            console.log('Added match with id', match_id);
            res.send({"message": "OK"});

            async.each(concat_teams, function(element, cb) {
                client.query('INSERT INTO players_in_team (player_id, team, match_id) VALUES ($1, $2, $3) RETURNING id', [element.id, element.team, match_id], function (err, result) {
                    if(err) return cb(err);

                    return cb(null);
                });
            }, function (err) {
                done();
                if (err) return console.log(err);

                return console.log('All players_in_team updated.');
            });

            PythonShell.run('main.py', function (err, results) {
                if (err) throw err;
                console.log('Score updated');

                PythonShell.run('graphs_plotly.py', function(err, results){
                    if (err) throw err;                
                    console.log('Graph updated');
                });
            });
        });
    });
});

app.post('/matchmaking', function(req, res) {
    var ids = req.body.ids;
    var options = {args: ids, mode: 'json'};
    PythonShell.run('matchmaking.py', options, function(err, results) {
        if (err) throw err;
        console.log('results: %j', results);
        res.send(results);
    });
});

app.get('/matchList', function(req, res) {
    pg_pool.connect(function(err, client, done) {
        if(err) return console.error('could not connect to postgres', err);

        client.query('SELECT * FROM matchs ORDER BY id desc limit 100', function (err, result) {
            done();
            if(err) return console.error('could not query db', err);

            var matchs = result.rows;
            res.send(matchs);
        });
    });
});

app.get('*', function (req, res) { res.status(404).send('The flag has been captured.'); });

app.listen(port, function () { console.log('Tagpro Trueskill app running on port', port); });
