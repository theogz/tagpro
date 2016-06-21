var express = require("express");
var app = express();
var PythonShell = require('python-shell');
var port = Number(process.env.PORT) || 3000;



app.use(express.static('public'));


app.get('/trueskill', function (req, res) {
/*    var team1 = tableau de la team 1
    var team2 = tableau de la team 2
    var resultat = score du match (1 vs 2)*/

    PythonShell.run('main.py', options, function (err, results) {
        if (err) throw err;
        // results is an array consisting of messages collected during execution
        console.log('results: %j', results);
    });

    res.send("kikou");

});

app.get('*', function (req, res) {
    res.status(404).send('404');
});

app.listen(port, function () {
  console.log('Tagpro Trueskill app');
});