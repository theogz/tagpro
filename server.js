var express = require('express');
var app = express();
var PythonShell = require('python-shell');
var port = Number(process.env.PORT) || 3000;

// needed to parse JSON data from client
var bodyParser = require('body-parser');
app.use(bodyParser.json());


app.use(express.static('public'));

var players_temp = require('./players.json');
app.get('/playerList', function (req, res) {
    // FIXME: load list from database instead
    var players = players_temp;
    res.send(players);
});

app.post('/trueskill', function (req, res) {
    var team1 = req.body.teams['1'];
    var team2 = req.body.teams['2'];
    var scoreTeam1 = req.body.score['1'];
    var scoreTeam2 = req.body.score['2'];

    console.log(team1, team2, scoreTeam1, scoreTeam2);

    // PythonShell.run('main.py', options, function (err, results) {
    //     if (err) throw err;
    //     // results is an array consisting of messages collected during execution
    //     console.log('results: %j', results);
    // });

    res.send({"message": "OK"});
});

app.get('*', function (req, res) { res.status(404).send('The flag has been captured.'); });

app.listen(port, function () { console.log('Tagpro Trueskill app running on port', port); });