const http = require('http');
var ip = require("ip")
require('dotenv').config()

const socketio_port = 4000
const zeromq_server = process.env.API_SERVICE_HOST;
const zeromq_port   = 5456
const zeromq_topic  = "userdata"
const hostname      = ip.address();

const zmq = require("zeromq")
var io = require('socket.io')(socketio_port);

async function run() {
  const sock = new zmq.Subscriber
 
  sock.connect(`tcp://${zeromq_server}:${zeromq_port}`)
  sock.subscribe(zeromq_topic)
  console.log(`ZMQ sub connected to ${zeromq_server}:${zeromq_port}`);
 
  for await (const [topic, msg] of sock) {
    data = topic.toString().slice(zeromq_topic.length).trim()
    console.log(data)

    data = JSON.parse(data)
    io.emit(zeromq_topic, data)         // Send to socket.io
  }
}
 
//Connect to SocketIO 
io.on('connection', function(socket) {
    console.log('A user connected');
})

process.on('SIGINT', () => {
    process.exit(1);
})

run()
