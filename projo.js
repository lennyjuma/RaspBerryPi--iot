import  express  from 'express';
import  http  from 'http';
import  { Server }  from 'socket.io';
import path from 'path';


const app = express();
const server = http.createServer(app);
const io = new Server(server, {
    cors: {
        origin: "http://localhost:3000",
        methods: ["GET", "POST"],
        allowedHeaders: ["my-custom-header"],
        credentials: true
    }
});
let __dirname = path.resolve(path.dirname(''));


import  mqtt from 'mqtt'
const topicArray = ['Temperature-bulb-middle','Temperature-bulb-front','Temperature-bulb-back','fan']
// client, user and device details
const serverUrl   = "mqtt://172.16.32.81:1883";
const clientId    = "my_mqtt_nodejs_client";
const device_name = "My Node.js MQTT device";
const tenant      = "<<tenant_ID>>";
const username    = "emqx";
const password    = "public";

var temperature   = 25;

// connect the client to mqtt server on raspberry pi
const client = mqtt.connect(serverUrl, {
    username: username,
    password: password,
    clientId: clientId
});

//let mqtt = require('mqtt')
// let client  = mqtt.connect('mqtt://172.16.33.43:1883')

client.on('connect', function () {
    client.subscribe('testTopic', function (err) {
        if (!err) {
            client.publish('presence', 'Hello mqtt')
        }
    })
})


client.on('message', function (topic, message) {
    // message is Buffer
    io.emit('line message', message.toString());
    io.emit('bar message', message.toString());
    console.log('data from mqqt',message.toString())
    // client.end()

})
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

io.on('connection', (socket) => {
    console.log('a user connected');

    socket.on('chat message', (msg) => {
        // io.emit('some event', { someProperty: 'some value', otherProperty: 'other value' }); // This will emit the event to all connected sockets
        io.emit('chat message', msg);
        console.log('message: ' + msg);
    });
    // send  activate mqtt msg to raspberry pi based on msg from vuejs using sockets
    socket.on('device/activate', (msg) => {
        // io.emit('some event', { someProperty: 'some value', otherProperty: 'other value' }); // This will emit the event to all connected sockets
        io.emit('chat message', msg);
        // for (let topic in topicArray){
        //     console.log(topic)
        // }
        client.publish('device/activate', msg)
        console.log('device/activate: ' + msg);
    });
    // send deactivate mqtt msg to raspberry pi based on msg from vuejs using sockets
    socket.on('device/deactivate', (msg) => {
        // io.emit('some event', { someProperty: 'some value', otherProperty: 'other value' }); // This will emit the event to all connected sockets
        io.emit('chat message', msg);
        // for (let topic in topicArray){
        //     console.log(topic)
        // }
        client.publish('device/deactivate', msg)
        console.log('device/deactivate: ' + msg);
    });

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
});

server.listen(3200, () => {
    console.log('listening on *:3200');
});