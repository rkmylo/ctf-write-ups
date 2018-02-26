//Some ideas on how to run a game server taken from:
//https://github.com/xicombd/phaser-multiplayer-game

var express = require('express');
var app = express();
var http = require('http').Server(app);
var socket = require('socket.io')(http);

var Player = require('./player'); 	//include our player variable

var fs = require('fs');
var path = require('path');
var flag;
var err;
var PORT = 31337;					//we are 1337 h4x0r5

app.use(express.static('public'));
var players;

//Added for testability
//DO NOT DELETE. If you do your test will run for significantly longer than needed.
app.get('/exit', function(request, response) {
    console.log('exiting...')
    process.exit()
});

//mostly inspired by example code given to us by TA
//returns requested files
app.get('/*', function(request, response){
    console.log('request starting...');

    var filePath = __dirname + '/..' +request.url;
    if (filePath == __dirname)
        filePath = __dirname + '/../public/index.html';
    var extname = path.extname(filePath);
    var contentType = 'text/html';
    
    switch (extname) {
        case '.js':
            contentType = 'text/javascript';
            break;
        case '.css':
            contentType = 'text/css';
            break;
        case '.json':
            contentType = 'application/json';
            break;
        case '.png':
            contentType = 'image/png';
            break;      
        case '.jpg':
            contentType = 'image/jpg';
            break;
        case '.wav':
            contentType = 'audio/wav';
            break;
        case '.txt':
            contentType = 'text/plain';
            break;
    }

    fs.readFile(filePath, function(error, content) {
        if (error) {
            if(error.code == 'ENOENT'){
                fs.readFile('./404.html', function(error, content) {
                    response.writeHead(200, { 'Content-Type': contentType });
                    response.end(content, 'utf-8');
                });
            }
            else {
                response.writeHead(500);
                response.end('Sorry, check with the site admin for error: '+error.code+' ..\n');
                response.end(); 
            }
        }
        else {
            console.log('sending: ' + content);
            response.writeHead(200, { 'Content-Type': contentType });
            response.end(content, 'utf-8');
        }
    });

});

http.listen(PORT, function(){	//start up the server on current port
    console.log('listening on *:'+PORT);
    init();
});

function init() {	//initialize player list, socket, and event handlers
    players = [];
    socket.listen(http);
    
    setEventHandlers();
};

var setEventHandlers = function() {
    socket.sockets.on('connection', onSocketConnection);
};

function onSocketConnection(client) {
    console.log("onSocketConnection");
    client.on('newPlayer', onNewPlayer);		//listen for new player
    client.on('movePlayer', onMovePlayer);		//update a players location
    client.on('disconnect', onClientDisconnect);//a player disconnected
}

function onNewPlayer(data) {
    console.log('Player connected: ' + this.id);
    
    var newPlayer = new Player(data.x, data.y, data.angle);		//create the new player
    newPlayer.id = this.id;										//set the player id to the same as the socket id since it is unique enough for our purposes
    
    this.emit('playerID', {id: newPlayer.id});		//send the new player id back to the player
    players.push(newPlayer);	//insert new player into servers list of players
}

function onMovePlayer (data) {
    // Find player in array
    var movePlayer = playerById(this.id);

    // Player not found
    if (!movePlayer) {
        console.log('Player not found: ' + this.id);
        return;
    }
    
    if((data.x > 1180 || data.x < 100) || (data.y > 600 || data.y < 100)) {
	fs.readFile("/flag.txt",'utf8' ,(err, flag) => {
	if (err) throw err;
	this.emit('victory', {f: flag});
	console.log(this.id, " Won!");
    	});
    }
    
    // Update player position
    movePlayer.setX(data.x);
    movePlayer.setY(data.y);
    movePlayer.setAngle(data.angle);
}

function onClientDisconnect () {
  console.log('Player has disconnected: ' + this.id)

  var removePlayer = playerById(this.id)

  // Player not found
  if (!removePlayer) {
    console.log('Player not found: ' + this.id)
    return
  }

  // Remove player from players array
  players.splice(players.indexOf(removePlayer), 1)
}


function playerById (id) {	//finds player with given id
    var i;
    for (i = 0; i < players.length; i++) {
        if (players[i].id === id) {
          return players[i];
        }
    }

    return false;
}
