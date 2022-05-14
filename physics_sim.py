import pygame
import numpy as np
import random

pygame.init()
surface = pygame.display.set_mode((1280, 753))
#s2 = pygame.Surface((50,50)); s2.fill((0,0,0))
clock = pygame.time.Clock()
pixarr = pygame.PixelArray(surface)


surface.fill((0,0,0))
RED = (200,0,0); GREEN = (0,200,0); BLUE = (0,0,200); WHITE = (200,200,200); YELLOW = (200,200,0); PINK = (200,0,200); CYAN = (0,200,200); BLACK = (0,0,0)
ORANGE = (255,165,0)
COLORS = [RED,GREEN,BLUE,WHITE,YELLOW,PINK,CYAN]
LEN_TRAIL = n = 40
d1 = 255/(n-1); d2 = 165/(n-1)
OrangeGrad = [(round(255-d1*i),round(165-d2*i),0) for i in range(n)]

def getDMV(var,d=1,m=1,l=1):
	if var == 'd':
		return m/(l*l)
	elif var == 'm':
		return d*l*l
	else:
		return (m/d)**0.5
	




def simpson(f,a,b,n=10):
	delx = (b-a)/n
	s = f(a)
	for i in range(1,n):
		s += ((i%2)*2 + 2) * f(a+i*delx)
	s += f(b)
	return delx * s /3


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
	def __str__(self):
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
		if m:
			return Vec2D(self.x/m, self.y/m)
		else: return Vec2D(0,0)
	def orthvector(self):
		return Vec2D(self.y, -self.x).unit()


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
	


V = Vec2D
P = V(640,376.5)


Bc = V(0,0); Br = V(360,0)
Bc2 = V(300,0); Br2 = V(100,0)
cs = [(Bc,Br),(Bc2,Br2)]
g = V(0,0)
#surface.blit(ball)

world = []

r = random.sample; r2 = random.randrange
b1 = Ball(-600,350,0,0,color=RED,radius=5,mass=1)
b2 = Ball(50,-200,0,2.2,color=GREEN,radius=5,mass=2)
b3 = Ball(111,-208,4,2,color= WHITE, radius=20,mass=300)
b4 = Ball(300,-310,-1,0,color=YELLOW,radius=5,mass=2)

def mass_propor_rad(rad):
	return rad * 15

def f(a,b):
	return random.randint(a,b)
def randomcolor():
	return f(0,255), f(0,255), f(0,255)
for i in range(8):
	rad = f(5,25)
	world.append(Ball(f(-300,300),f(-400,400),f(-3,3),f(-3,3),color=randomcolor(),radius=rad,mass=mass_propor_rad(rad)))
for i in range(4):
	cs.append((V(f(-320,321), f(-320,321)), V(f(5,100), 0)))




world.append(b3)

#####################################################

def collidegrad(ball,grad=None,vert=0,hor=0):
	u1 = ball.vel
	if grad is not None:
		twoth = 2*np.arctan(grad)
		c2th = np.cos(twoth); s2th = np.sin(twoth)
		m1 = V(c2th,s2th); m2 = V(s2th,-c2th)
		ball.vel = V(m1*ball.vel, m2*ball.vel)
	elif vert:
		ball.vel = V(-ball.vel.x,ball.vel.y)
	elif hor:
		ball.vel = V(ball.vel.x,-ball.vel.y)
	#ball.vel = (0.9*ball.vel)
	#ball.pos += ball.vel
	return ball


def collidewalls(b):
	if not (-640+b.radius< b.pos.x < 640-b.radius):
		b = collidegrad(b,vert=1)
	if not (-375+b.radius < b.pos.y < 376-b.radius):
		b.vel -= g #added to correct
		b = collidegrad(b,hor=1)
	#print(b.vel.mag2())
	return b

####################################################

def drawtrail(b):
	if (-640< b.pos.x < 640) and (-375 < b.pos.y < 376):
			if len(b.l20pos) >= LEN_TRAIL:
				b.l20pos = b.l20pos[1:]
			x = b.pos_tup()
			b.l20pos.append((int(x[0]),int(x[1])))
			try:
				for j,p in enumerate(reversed(b.l20pos)):
					pixarr[p[0]][p[1]] = OrangeGrad[j]
			except IndexError:
				pass 


def drawball(b,color=None):
	pygame.draw.circle(surface,b.color,b.pos_tup(),b.radius,0)

#################################################


def adjust_ball(ball,vtoball,small_r,R,inner):
	if inner:
		x = vtoball + small_r - R
		ball.pos += (-x)
	else:
		x = small_r + R - vtoball
		ball.pos += x
	return ball



def collideCircle(ball,Br,Bc,inner=True):
	rs = Br.x-ball.radius; rl = Br.x+ball.radius
	vtoball = ball.pos - Bc
	vtoball_u = vtoball.unit()
	small_r = ball.radius*vtoball_u
	R = Br.x * vtoball_u
	
	
	if inner and (ball.pos.x <= (Bc.x-rs) or ball.pos.x >= (Bc.x+rs)):
		#if ball.pos == Bc-Br or ball.pos == Bc+Br:
		ball = adjust_ball(ball,vtoball,small_r,R,inner)
		ball = collidegrad(ball,vert=1)
		
	elif not inner and (( Bc.x-rl <= ball.pos.x <= Bc.x+rl) and ball.pos.y==Bc.y):
		ball = adjust_ball(ball,vtoball,small_r,R,inner)
		ball = collidegrad(ball,vert=1)
		
	elif inner and vtoball.mag2() >= rs*rs:
		ball = adjust_ball(ball,vtoball,small_r,R,inner)
		dydx = (vtoball.x)/(-vtoball.y)
		ball = collidegrad(ball,grad=dydx)
		
		#ball.pos -= (0.05*(ball.pos-Bc))
	elif not inner and vtoball.mag2() <= rl*rl:
		ball = adjust_ball(ball,vtoball,small_r,R,inner)
		dydx = (vtoball.x)/(-vtoball.y)
		ball = collidegrad(ball,grad=dydx)
		
		#ball.pos += (0.05*(ball.pos-Bc))
	return ball

def collide2balls(b,ba):
			r = ba.pos - b.pos
			r_u = r.unit();
			rad_b = b.radius * r_u
			rad_ba = ba.radius * r_u
			
			if r.mag2() <= (b.radius + ba.radius)**2:
				x = rad_b + rad_ba - r
				b.pos += (-0.5*x)
				ba.pos += 0.5*x
				
				m1 = b.mass; m2 = ba.mass
				rb = b.pos - ba.pos
				rb_u = rb.unit()
				u1costh1 = (b.vel*r_u)*r_u ; perp_r_u = (-u1costh1+b.vel).unit()
				u1sinth1 = (b.vel*perp_r_u) * perp_r_u
				
				u2costh2 = (ba.vel*rb_u)*rb_u; perp_rb_u = (-u2costh2+ba.vel).unit()
				u2sinth2 = (ba.vel*perp_rb_u) * perp_rb_u
				u1 = u1costh1; u2 = u2costh2
				v2 = (m1*(2*u1 - u2)+m2*u2)/(m2+m1)
				v1 = (m2*(2*u2 - u1)+m1*u1)/(m1+m2)
				ba.vel = v2+u2sinth2
				b.vel = v1+u1sinth1
				
				b.pos += b.vel; ba.pos += ba.vel


def collideBalls(i,b,world):
	for ba in world:
		if world.index(ba) != i:
			r = ba.pos - b.pos
			r_u = r.unit();
			rad_b = b.radius * r_u
			rad_ba = ba.radius * r_u
			
			if r.mag2() <= (b.radius + ba.radius)**2:
				x = rad_b + rad_ba - r
				b.pos += (-0.5*x)
				ba.pos += 0.5*x
				
				m1 = b.mass; m2 = ba.mass
				rb = b.pos - ba.pos
				rb_u = rb.unit()
				u1costh1 = (b.vel*r_u)*r_u ; perp_r_u = (-u1costh1+b.vel).unit()
				u1sinth1 = (b.vel*perp_r_u) * perp_r_u
				
				u2costh2 = (ba.vel*rb_u)*rb_u; perp_rb_u = (-u2costh2+ba.vel).unit()
				u2sinth2 = (ba.vel*perp_rb_u) * perp_rb_u
				u1 = u1costh1; u2 = u2costh2
				v2 = (m1*(2*u1 - u2)+m2*u2)/(m2+m1)
				v1 = (m2*(2*u2 - u1)+m1*u1)/(m1+m2)
				ba.vel = v2+u2sinth2
				b.vel = v1+u1sinth1
				
				b.pos += b.vel; ba.pos += ba.vel
	return b


def simulate_balls_colliding(i,b,cs):
	b = collidewalls(b)
	#if ct > 1:
	
	for c in cs:
		if c[0] != V(0,0) and c[1] != V(360,0):
			b = collideCircle(b,c[1],c[0],inner=False)
		else:
			b = collideCircle(b,c[1],c[0])
	world[i] = collideBalls(i,b,world)
	b = world[i]
	b.vel += g
	b.pos += b.vel
	
	drawtrail(b)	
	drawball(b)
	
	for c in cs:
		pygame.draw.circle(surface,GREEN,(c[0]+V(640,376.5)).tup(),c[1].x,5)


##########################################################


def newballs(ball,r,n,m):
	momentum = ball.vel.mag()*ball.mass
	velmag = momentum/m
	l = []; vels = []
	a = np.sqrt( 4*r*r/( 2*(1-np.cos(2*np.pi/n)) ) )
	#a += 0.5
	for k in range(1,n+1):
		v =  Vec2D(round(a*np.cos(2*np.pi*k/n),4), round(a*np.sin(2*np.pi*k/n),4))
		l.append(v)
		
		vels.append(2*velmag*v.unit())
		
	nb = [Ball(*(ball.pos+x).tup(),*(vels[l.index(x)].tup()),mass=m,radius=r) for x in l]
	return nb


def spaceCollision(i,b,world):
	NSPLIT = 5
	for ba in world:
		if world.index(ba) != i:
			r = ba.pos - b.pos
			r_u = r.unit();
			rad_b = b.radius * r_u
			rad_ba = ba.radius * r_u
			
			if r.mag2() <= (b.radius + ba.radius)**2:
				if len(world) < 10:
					collide2balls(b,ba)
					'''nbv = int(NSPLIT*b.mass/(b.mass+ba.mass))
					nba_v = NSPLIT - nbv
					new_r = ((b.radius*b.radius + ba.radius*ba.radius)/NSPLIT)**0.5
					new_m = (b.mass+ba.mass)/NSPLIT
					if b in world:
						world.remove(b)
					if ba in world:
						world.remove(ba)
					if nbv >1:
						wb = newballs(b,new_r,nbv,new_m)
						world.extend(wb)
					if nba_v > 1:
						world.extend(newballs(ba,new_r,nba_v,new_m))
					for i in range(nba_v):
						c = random.choice([0.5,-0.5])
						displace = 0.5*i*(ba.pos.orthvector())
						nb = Ball(*(ba.pos+displace).tup(), 0,0, radius=new_r, mass=new_m)
						world.append(nb)
						w2.append(nb)'''
					
					break





def spacegravity(i,b,world):
		#if b.vel.mag2()> 15:
		#	world.remove(b)
		#	world[-1].mass += b.mass
			
		for b_2 in world:
			if world.index(b_2) != i:
				v = b_2.pos - b.pos
				r2 = v.mag2()
				if r2 > 0:
					#Here we're using F = Gm1m2/r^2, and finding the accelerations
					G = 1
					k = G/r2
					b_acc = k*b_2.mass
					b_2acc = k*b.mass
					b.vel += b_acc*(v.unit())
					b_2.vel += b_2acc *(-(v.unit()))
		return b

def simulate_space_gravity(i,b,world):
	b = spacegravity(i,b,world)
	b = collidewalls(b)
	collideBalls(i,b,world)
	return b


###############################################################
f = 6

def find_first_below(w_set,ncols,cell,right=True,n=1):
	j = cell[1]; i=cell[0]
	if right:
		for ind in range(j,ncols):
			if (i+1,ind) not in w_set:
				return ind-1
	else:
		for ind in range(j,-1,-1):
			if (i+1,ind) not in w_set:
				return ind+1
	return -1

def add_cell(nextgen,cell):
	nextgen.add(cell)
	pygame.draw.circle(surface, ORANGE, ((cell[1]*f), (cell[0]*f)), 3,0)
	return nextgen
	
	

def cellular_automata(surface, w_set):
	GRAD = 0
	#for i in range(-20,20):
	#	pixarr[i+640][376] = WHITE
	no_r = int(752/f)
	no_c = int(1280/f)
	
	nextgen = set()
	
	for cell in w_set:
		i = cell[0]; j = cell[1]
		if cell[0] != no_r - 1:
			if not (i+1,j) in w_set:
				#nextgen[i,j] = 0;
				nextgen = add_cell(nextgen,(i+1,j))
			else:
				if all([(x not in w_set) for x in ((i,j-1),(i,j+1),(i+1,j-1),(i+1,j+1))]):
					dir = random.choice((0,1))
				else:
					dir = 0 if not(((i,j+1) in w_set) or (i+1,j+1) in w_set) else (1 if not( ((i,j-1) in w_set) or (i+1,j-1) in w_set) else None) #random.choice((0,1))
				if dir:
					x = find_first_below(w_set,no_c,cell,right=False)
					if x == j:
						#nextgen[i,j] = 0; 
						nextgen = add_cell(nextgen,(i+1,j-1))
					else:
						grad = 1/(x-j)
						if grad > GRAD:
							#nextgen[i,j] = 0;
							nextgen = add_cell(nextgen,(i+1,x-1))
						else: nextgen = add_cell(nextgen,(i,j))
				elif dir is not None:
					x = find_first_below(w_set,no_c,cell)
					if x == j:
						#nextgen[i,j] = 0;
						nextgen = add_cell(nextgen,(i+1,j+1))
					else:
						grad = 1/(j-x)
						if grad > GRAD:
							#nextgen[i,j] = 0;
							nextgen = add_cell(nextgen,(i+1,x+1))
						else: nextgen = add_cell(nextgen,(i,j))
				else:
					nextgen = add_cell(nextgen,(i,j))
		else:
			nextgen = add_cell(nextgen,(i,j))
	#for cell in nextgen:
	#	pygame.draw.circle(surface, WHITE, ((cell[1]*f), (cell[0]*f)), 3,0)
	
	return nextgen


def create_set_for_sand():
	w_set = set()
	for i in range(2,3):
		for j in range(20, 30):
			choice = random.choice((0,1))
			if choice:
				w_set.add((i,j))
	return w_set

def simulate_sand(w_set):
	if 10 < ct < 900:
		for i in (2,3):
			for j in (30,31):
				if random.randint(0,1): w_set.add((i,j))
	if 90 < ct < 1200:
		for i in (2,3):
			for j in (60,61):
				if random.randint(0,1): w_set.add((i,j))
	
	w_set = cellular_automata(surface,w_set)
	return w_set

##One simulation at a time please, lol


#for the sand cellular automaton, uncomment the line below, and line 514
w_set = create_set_for_sand()


ct = 0
while True:
	surface.fill((0,0,0))
	for ev in pygame.event.get():
		if ev.type == pygame.QUIT:
			pygame.quit()
			quit()

	#for space_gravity or balls_colliding
	for i,b in enumerate(world):
		pass
		#uncomment one of the lines below for the relevant simulation
		#simulate_balls_colliding(i,b,cs)
		#simulate_space_gravity(i,b,world)

		#if one line above is uncommented, uncomment both lines below
		# b.pos += b.vel
		# drawball(b)
	
	w_set = simulate_sand(w_set) #uncomment this line for sand simulation

	pygame.display.update()
	clock.tick(60)
	ct += 1


	
	
