import Main;

typedef Segment = {
	var v1:Vector;
	var v2:Vector;
}

class Collision
{
	public static function checkBallSeg(ball:Ball, seg:Segment) {
		var dir = seg.v2.sub(seg.v1);
		var aux = ball.pos.sub(seg.v1);
		var base;
		if (aux.dot(dir) <= 0)
			base = seg.v1;
		else {
			aux = ball.pos.sub(seg.v2);
			base = if (aux.dot(dir) >= 0)
				seg.v2;
			else
				aux.proj(dir).addEq(seg.v2);
		}

		var norm = ball.pos.sub(base);
		var proj = ball.vel.proj(norm);
		var diff = proj.sub(ball.vel);
		var vnew = ball.vel.add(diff.mult(2));

		if (norm.mag2() <= ball.radius*ball.radius)
			ball.vel = vnew.mult(-1);
	}
}

