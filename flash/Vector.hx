
class Vector
{
	public var x:Float;
	public var y:Float;

	public function new(?x:Float = 0, ?y:Float = 0) {
		this.x = x;
		this.y = y;
	}

	public function mag2() {
		return x*x + y*y;
	}
	
	public function mag() {
		return Math.sqrt(mag2());
	}

	public function add(v:Vector) {
		return new Vector(x+v.x, y+v.y);
	}

	public function addEq(v:Vector) {
		x += v.x;
		y += v.y;
		return this;
	}

	public function mult(f:Float) {
		return new Vector(x*f, y*f);
	}

	public function multEq(f:Float) {
		x *= f;
		y *= f;
		return this;
	}

	public function norm(?len:Float = 1) {
		var m = mag();
		if (m != 0) {
			return new Vector(x/m, y/m);
		}
		return null;
	}

	public function normEq(?len:Float = 1) {
		var m = mag();
		if (m != 0) {
			x = x/m;
			y = y/m;
		}
		return this;
	}

	public function dot(v:Vector) {
		return x*v.x + y*v.y;
	}

	public function sub(v:Vector) {
		return new Vector(x-v.x, y-v.y);
	}

	public function subEq(v:Vector) {
		x -= v.x;
		y -= v.y;
		return this;
	}

	public function proj(v:Vector) {
		var dir = v.norm();
		var dp = dot(dir);
		return dir.multEq(dp);
	}

	public function toString() {
		return x+", "+y;
	}
}
