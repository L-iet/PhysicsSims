class Vec2D:
	def __init__(self,x,y):
		self.x = x; self.y = y
	def __add__(self,other):
		return Vec2D(self.x+other.x,self.y+other.y)
	def __sub__(self,other):
		return Vec2D(self.x-other.x,self.y-other.y)
	def __neg__(self):
		return Vec2D(-self.x,-self.y)
	def __mul__(self,other):
		if type(other) in [int, float]:
			return Vec2D(self.x*other,self.y*other)
		elif type(other) is Vec2D:
			return self.x*other.x + self.y*other.y
	def __truediv__(self,other):
		if type(other) in [int, float]:
			return Vec2D(self.x/other,self.y/other)
	def __rmul__(self,other):
		return self.__mul__(other)
	def __eq__(self,other):
		return self.x==other.x and self.y==other.y
	def __ne__(self,other):
		return not(self==other)
	def __round__(self,n=0):
		return Vec2D(round(self.x, n), round(self.y, n))
	def __str__(self):
		return f'Vec2D({self.x}, {self.y})'
	def __repr__(self):
		return f'Vec2D({self.x}, {self.y})'
	def tup(self):
		return self.x,self.y
	def mag(self):
		return (self.x*self.x + self.y*self.y)**0.5
	def mag2(self):
		return self.x*self.x + self.y*self.y
	def slope(self):
		return self.y/self.x
	def unit(self):
		m = self.mag()
		return Vec2D(self.x/m, self.y/m)


class Ball:
	def __init__(self,posx,posy,velx,vely,radius=10,color=None,mass=1):
		self.vel = Vec2D(velx,vely)
		self.pos = Vec2D(posx,posy)
		self.mass = mass
		if not color: color = tuple(random.randrange(50,255) for x in range(3))
		self.color = color
		self.radius = radius
		self.density = self.mass / (self.radius*self.radius)
		x = self.pos_tup()
		self.l20pos = [(int(x[0]),int(x[1]))]
	def __str__(self):
		return f'Ball(r={self.radius},m={self.mass})'
	def __repr__(self):
		return f'Ball(r={self.radius},m={self.mass})'
	def pos_tup(self):
		return (self.pos + V(640,376.5)).tup()

