window.onload = function() {

        var game = new Phaser.Game(1280, 720, Phaser.AUTO, '', { preload: preload, create: create, update: update});
}
	var socket = new io.Socket();
	var player;
	var cursors;
	var boundaries;

	function preload() {
		game.load.image('logo', 'phaser.png');
		game.load.image('block', 'block.jpg');
		game.load.image('bound', 'boundary.jpg');
	}

	function create() {
		socket = io.connect();
		game.physics.startSystem(Phaser.Physics.ARCADE);
		
		game.world.setBounds(0,0,1280,720);
		
		player = game.add.sprite(180,520, 'block');
		player.anchor.setTo(0.5,0.5);
		player.scale.setTo(.1, .1);
		game.physics.arcade.enable(player);
//		player.body.collideWorldBounds = true;
		player.body.bounce.setTo(1,1);
		createBoundaries();		
		cursors = game.input.keyboard.createCursorKeys();
		
		setEventHandlers();
	}
	
	function createBoundaries() {
		boundaries = game.add.group();
		boundaries.enableBody = true;	
		
		var boundary1 = boundaries.create(100,100, 'bound');
		boundary1.anchor.setTo(0,0);
		boundary1.width = 50;
		boundary1.height = 500;
		boundary1.body.immovable = true;
		
		var boundary2 = boundaries.create(150,100, 'bound');
		boundary2.anchor.setTo(0,0);
		boundary2.width = 940;
		boundary2.height = 50;
		boundary2.immovable = true;
		
		var boundary3 = boundaries.create(150,400, 'bound');
                boundary3.anchor.setTo(0,0);
                boundary3.width = 730;
                boundary3.height = 50;
                boundary3.immovable = true;

		var boundary4 = boundaries.create(150,550, 'bound');
                boundary4.anchor.setTo(0,0);
                boundary4.width = 980;
                boundary4.height = 50;
                boundary4.immovable = true;

		var boundary5 = boundaries.create(250, 250, 'bound');
                boundary5.anchor.setTo(0,0);
                boundary5.width = 880 ;
                boundary5.height = 50;
                boundary5.immovable = true;

		var boundary6 = boundaries.create(1130,100, 'bound');
                boundary6.anchor.setTo(0,0);
                boundary6.width = 50;
                boundary6.height = 500;
                boundary6.immovable = true;

	
	}
		
	function setEventHandlers() {
		socket.on('newPlayer', onNewPlayer);//new player
		socket.on('connect', onSocketConnected);//new connection
		socket.on('disconnect', onSocketDisconnect);//one of the players has moved
		socket.on('victory', function(data) {
			console.log("You Won!\nHere is your flag: ", data.f);
		});
		socket.on('playerID', function(data) {
			player.id = data.id;
		});
	}

	function onSocketConnected() {
		console.log('Connected to socket server');
		
		socket.emit('newPlayer', { x: player.x, y: player.y});	//send server info to create new player
	}
	
	function onSocketDisconnect () {
 		console.log('Disconnected from socket server');
	}

	function onNewPlayer (data) {
		console.log('New player connected:', data.id);

		// Avoid possible duplicate players
		var duplicate = playerById(data.id);
		if (duplicate) {
			console.log('Duplicate player!');
			return;
		}
		if (player.id == data.id){
			return;
		}
		
		// Add new player to the remote players array
		otherPlayers.push(new OtherPlayer(data.id, game, player, data.x, data.y, data.angle));	//create new player and put it into list of current players
			
		console.log(otherPlayers);	//debugging
	}

	function update() {
		var hitObstacle = game.physics.arcade.collide(player, boundaries);
		var x, y;
		
		if(hitObstacle == false) {
			if (cursors.up.isDown) { 
				player.body.y -= 1;
			}
			else if (cursors.down.isDown) {
		       		player.body.y += 1;
			} 
			if (cursors.left.isDown)
				player.body.x -= 1;
			else if (cursors.right.isDown)
				player.body.x += 1;
		}
		
		socket.emit('movePlayer', { x: player.x, y: player.y});	
	}

	function playerById (id) {								//returns player from given id
		for (var i = 0; i < otherPlayers.length; i++) {
			if (otherPlayers[i].player.id === id) {
				return otherPlayers[i];
			}
		}
		return false;
	}


