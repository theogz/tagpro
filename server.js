var _ = require('underscore');

var express = require('express');
var app = express();
var PythonShell = require('python-shell');
var port = Number(process.env.PORT) || 3000;

var exec = require('child_process').exec;



var pg = require('pg');
var config = {
    host: 'localhost',
    user: 'postgres',
    password: 'psql',
    database: 'tagpro',
    port: 5432
};
var pg_string = 'postgres://' + config.user + ':' + config.password + '@' + config.host + '/' + config.database 

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

app.post('/trueskill', function (req, res) {
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

        pg_client.query('INSERT INTO matchs (team1, team2, score1, score2, computed) VALUES ($1, $2, $3, $4, $5) RETURNING id', [team1ids, team2ids, scoreTeam1, scoreTeam2, matchComputed], function (err, result) {
            if(err) return console.error('could not query db', err);

            console.log('Added match with id', result.rows[0]['id']);
            res.send({"message": "OK"});

            PythonShell.run('main_postgres.py', function (err, results) {
                if (err) throw err;
                exec('Rscript trueplots.R', function(error, stdout, stderr) {
                    console.log('stdout: ',stdout);
                    console.log('stderr: ',stderr);
                    if (error !=null) {
                        console.log('exec error: ', error);
                    }
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