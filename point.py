class Point:
	def __init__(self, x=0, y=0): self.x, self.y = x, y
	def __str__(self): return f"({self.x}, {self.y})"
	def move_to(self, x, y): self.x, self.y = x, y 
	def move_by(self, dx, dy): 
		self.x += dx;    
		self.y += dy;
	def as_tuple(self): return self.x, self.y  
	@staticmethod
	def run_tests():  # no self here
		a = Point();  b = Point(2, 2);  print('first: ', a, b);  
		a.move_to(1, 1);  b.move_by(1, 1); print('after: ', a, b)
