//Some ideas on how to run a game server taken from:
//https://github.com/xicombd/phaser-multiplayer-game

//stores all the info needed for the client to display the other players that are connected

var OtherPlayer = function(id, game, player, startX, startY, startAngle) {
	//initialize the other player
	var x = startX;
	var y = startY;
	var angle = startAngle;
	this.player = player;
	this.game = game;

	this.alive = true;	
		
	this.player = game.add.sprite(x, y, 'block');		//add sprite to game in starting position based on its number
	this.player.id = id.toString();	
	
	game.physics.enable(this.player, Phaser.Physics.ARCADE)
	
	this.player.anchor.setTo(0.5, 0.5);
	this.player.scale.setTo(0.5, 0.5);
	this.player.angle = angle;
	this.lastPosition = { x: x, y: y, angle: angle };	//store where it last was when updated
	this.player.bringToTop();
}

OtherPlayer.prototype.update = function() {			//function to update the stored location
	this.lastPosition.x = this.player.x;
	this.lastPosition.y = this.player.y;
	this.lastPosition.angle = this.player.angle;
}

window.OtherPlayer = OtherPlayer;
