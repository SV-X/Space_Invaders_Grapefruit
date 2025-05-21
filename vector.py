from point import Point
import math

class Vector:
	@classmethod
	def from_point(cls, point): return cls(point.x, point.y)
	def __init__(self, x=0, y=0): self.x, self.y = x, y
	def __str__(self): return f"Vector({self.x}, {self.y})"
	def __add__(self, other): return Vector(self.x + other.x, self.y + other.y)     # + operator (e.g., x + y)
	def __sub__(self, other): return Vector(self.x - other.x, self.y - other.y)     # -  op      (e.g., x - y)
	def __iadd__(self, other): self.x += other.x;  self.y += other.y; return self   # += op      (e.g., x += y)
	def __isub__(self, other): self.x -= other.x;  self.y -= other.y; return self   # -= op      (e.g., x -= y)
	def __imul__(self, k: float): self.x *= k;  self.y *= k;  return self
	def __itruedev__(self, k: float): 
		if abs(k) < 1e-10: raise ZeroDivisionError('Cannot divide by zero')
		self.x /= k;  self.y /= k;  return self;
	def __mul__(self, k: float): return Vector(self.x * k, self.y * k)              # *  op      (e.g., x * k)
	def __rmul__(self, k: float): return self * k                                  # *  op      (e.g., k * x)
	def __truediv__(self, k: float):                                               # /  op      (e.g., x / k)
		if abs(k) < 1e-5: raise ZeroDivisionError('Cannot divide by zero')
		return Vector(self.x / k, self.y / k)  # call __mul__ using 1.0 / k
	def __eq__(self, other): return self.x == other.x and self.y == other.y       # logic equal (e.g., u == v)
	def __ne__(self, other): return not self == other
	def __neg__(self): return Vector(-self.x, -self.y)                            # unary neg (e.g., -v)
	
	def magnitude(self):
		return math.sqrt(self.x**2 + self.y**2)
	
	def normal(self):
		return Vector(self.x, self.y) / self.magnitude() if self.magnitude() != 0 else Vector(0, 0)

	def angle(self):
		angle_rad = math.atan2(self.y, self.x)   # returns angle in radians from -π to π
		angle_deg = math.degrees(angle_rad)      # convert to degrees
		return angle_deg % 360