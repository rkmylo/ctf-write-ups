//Some ideas on how to run a game server taken from:
//https://github.com/xicombd/phaser-multiplayer-game

//stores all the functions and info needed for the server to keep track of players who are connected

var Player = function (startX, startY, startAngle) {
	var x = startX;				//current x coordinate
	var y = startY;				//current y coordinate
	var angle = startAngle;		//current angle
	var id;						//unique id number
	
	var getX = function () {
		return x
	}

	var getY = function () {
		return y
	}
	var getAngle = function () {
		return angle
	}
		
	var setX = function (newX) {
		x = newX
	}

	var setY = function (newY) {
		y = newY
	}
	
	var setAngle = function (newAngle) {
		angle = newAngle
	}
	
	return {
		getX: getX,
		getY: getY,
		getAngle: getAngle,
		setX: setX,
		setY: setY,
		setAngle: setAngle,
		id: id,
	}
}

module.exports = Player;
