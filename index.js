const express = require('express');
const app = express();
// test
app.get('/', function (req, res) {
 res.send('hello world!');
});
app.listen(3000, () => console.log('App listening on port ', 3000));const low = require('lowdb');
const FileSync = require('lowdb/adapters/FileSync')
const adapter = new FileSync('db.json');
const db = low(adapter);
db.defaults({ posts: [] })
 .write()
