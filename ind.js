
'use strict'
import http from 'http';
import { Server } from 'socket.io';
import path from 'path';
import cors from  'cors';
import  express  from 'express';
//const express = require('express');
const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(cors())

// test
app.get('/', function (req, res) {
 res.send('hello world!');
});


import { join } from 'path'
import { Low, JSONFile } from 'lowdb'

// Use JSON file for storage

const __dirname = path.resolve();
const file = join(__dirname, 'db.json')
const adapter = new JSONFile(file)
const db = new Low(adapter)

// Read data from JSON file, this will set db.data content
await db.read()

//api endpoint
app.get('/posts', (req, res) => {
 let data = db.data.posts
 res.send(data);
});

app.get('/name',(req,res) => {
  let data = db.data.name
  res.send(data)
});
// If file.json doesn't exist, db.data will be null
// Set default data
db.data = { posts: [] , name:[], msg:[] }
// Create and query items using plain JS
db.data.posts.push('hello world')
db.data.posts[0]
db.data.posts.push('yoo')
// You can also use this syntax if you prefer
const { posts } = db.data
posts.push('hello world')
const { name } =  db.data
name.push('fuck')
name.push('this')
posts.push('easy')
// Write db.data content to db.json
await db.write()


import  mqtt from 'mqtt'
//var mqtt = require('mqtt')
var client  = mqtt.connect('mqtt://localhost:1883')

client.on('connect', function () {
  client.subscribe('testTopic', function (err) {
    if (!err) {
      client.publish('presence', 'Hello mqtt')
    }
  })
})

let mqttmsg;
const { msg } = db.data


client.on('message', function (topic, message) {
  // message is Buffer
  msg.push(message.toString())
  console.log(message.toString())
  client.end()
})

console.log('mqttmsg',mqttmsg)
msg.push(mqttmsg)

app.get('/mqtt',(req,res) => {
  let data = db.data.msg
  res.send(data)
});

io.on('connection', (socket) => {
    // eslint-disable-next-line no-console
    console.log('a user connected, server received connecting-event',socket);
});


server.listen(3200, () => console.log('Server listening on port ', 3200));
