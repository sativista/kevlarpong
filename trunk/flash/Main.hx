import flash.display.Sprite;
import flash.events.KeyboardEvent;
import haxe.Timer;
import Collision;

enum Direcao
{
	UP;
	DOWN;
	STAY;
}

class AbstractCorpse extends Sprite
{
	public var pos:Vector;
	public var vel:Vector;

	public function new() {
		super();
		pos = new Vector();
		vel = new Vector();
	}

	public function draw();
	public function update(?time:Float);
}

class Ball extends AbstractCorpse
{
	static var VELOCITY = 5;

	public var radius:Float;

	public function new(?r = 10.0) {
		super();
		radius = r;
		gen_velocity();
		graphics.beginFill(0);
		graphics.drawCircle(0, 0, r);
	}

	function gen_velocity() {
		vel.x = Math.random();
		vel.y = Math.random();
		vel.normEq();
	}

	public override function update(?time:Float) {
		pos.addEq(vel.mult(time*VELOCITY));
	}

	public override function draw() {
		x = pos.x;
		y = pos.y;
	}
}

class Racket extends AbstractCorpse
{
	static var WIDTH = 20;
	static var HEIGHT = 80;
	static var VEL = 80;

	public var dir:Direcao;

	public function new() {
		super();
		dir = STAY;
		graphics.beginFill(0);
		graphics.drawRect(0, 0, WIDTH, HEIGHT);
	}

	public override function update(?time:Float) {
		switch(dir) {
			case UP:
				pos.y += VEL;
			case DOWN:
				pos.y -= VEL;
			case STAY:
				trace("stay");
		}
	}

	public override function draw() {
		y = pos.y;
	}
}

class Game
{
	public var rackets:List<Racket>;

	public function new() {
		rackets = new List();
	}
}

class Main
{
	public static function main() {
		var s = new Sprite();
		var seg = {v1:new Vector(), v2:new Vector(100, 100)};
		var ball = new Ball();
		ball.pos.x = 200;
		ball.pos.y = 108;
		ball.vel.y = 0;
		ball.vel.x = -1;

		s.graphics.lineStyle(0);
		s.graphics.moveTo(seg.v1.x, seg.v1.y);
		s.graphics.lineTo(seg.v2.x, seg.v2.y);
		
		var W = flash.Lib.current.stage.stageWidth;
		var H = flash.Lib.current.stage.stageHeight;
		var w1 = {v1:new Vector(), v2:new Vector(W, 0)};
		var w2 = {v1:w1.v2, v2:new Vector(W, H)};
		var w3 = {v1:w2.v2, v2:new Vector(0, H)};
		var w4 = {v1:w3.v2, v2:new Vector()};

		var g = flash.Lib.current.graphics;
		g.lineStyle(0);

		var l = new List();
		for (i in 0...10) {
			var v1 = new Vector((W-100)*i/9+Math.random()*100, (H-100)*i/9+Math.random()*100);
			var v2 = new Vector((W-100)*i/9+Math.random()*100, (H-100)*i/9+Math.random()*100);
			g.moveTo(v1.x, v1.y);
			g.lineTo(v2.x, v2.y);
			l.add({v1:v1, v2:v2});
		}

		var t = new Timer(30);
		t.run = function() {
			ball.vel.y += 0.01;
			ball.update(1);
			ball.draw();
			Collision.checkBallSeg(ball, seg);
			Collision.checkBallSeg(ball, w1);
			Collision.checkBallSeg(ball, w2);
			Collision.checkBallSeg(ball, w3);
			Collision.checkBallSeg(ball, w4);
			for (seg in l)
				Collision.checkBallSeg(ball, seg);
		}

		flash.Lib.current.addChild(s);
		flash.Lib.current.addChild(ball);
		flash.Lib.current.stage.addEventListener(KeyboardEvent.KEY_DOWN, onKeyDown);
		flash.Lib.current.stage.addEventListener(KeyboardEvent.KEY_UP, onKeyUp);
	}

	static var direcao = STAY;

	static function onKeyDown(e) {
		direcao = switch(e.keyCode) {
			case 38:
				UP;
			case 40:
				DOWN;
			default:
				STAY;
		}
		trace(direcao);
	}

	static function onKeyUp(e) {
		direcao = switch(direcao) {
			case UP:
				if (e.keyCode == 38)
					STAY;
			case DOWN:
				if (e.keyCode == 40)
					STAY;
			default:
				null;
		}
		trace(direcao);
	}
}
