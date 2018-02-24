const pg = require('pg');
const fs = require('fs');
const argv = require('yargs').argv;

require('dotenv').config();

const config = {
    host: process.env.PG_HOST || 'localhost',
    user: process.env.PG_USER || 'postgres',
    password: process.env.PG_PASSWORD || 'psql',
    database: process.env.PG_DB || 'tagpro',
    port: process.env.PG_PORT || 5432,
    max: 16,
    idleTiemoutMillis: 12000,
};

const season = argv.season;

const query = fs.readFileSync('./scripts/sql/new_season.sql').toString().replace('${season}', season);
const pg_pool = new pg.Pool(config);

if (!season) {
  console.log('No --season argument given')
  process.exit();
}

pg_pool.connect(function(err, client, done) {
    if(err) return console.error('could not connect to pool', err);

    client.query(query, function (err, result) {
        done();
        
        if(err) 
          return console.error('could not query db', err);

        console.log(`Players stats reset for season ${season}`);
        console.log(`Please type: dokku config:set tagpro SEASON=${season}  /// it should automatically restart as well`);
        process.exit();
    });
});
