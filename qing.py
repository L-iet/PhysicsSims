#air, cohesion(friction), vibration
import pygame
from MyVec2D import Vec2D, Ball
import random

pygame.init()
WIDTH = 245; HEIGHT = 400
surface = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pixarr = pygame.PixelArray(surface)
surface.fill((0,0,0))

RED = (200,0,0); GREEN = (0,200,0); BLUE = (0,0,200); WHITE = (200,200,200); YELLOW = (200,200,0); PINK = (200,0,200); CYAN = (0,200,200); BLACK = (0,0,0)
ORANGE = (255,165,0)
COLORS = [RED,GREEN,BLUE,WHITE,YELLOW,PINK,CYAN]
LEN_TRAIL = n = 40
d1 = 255/(n-1); d2 = 165/(n-1)
OrangeGrad = [(round(255-d1*i),round(165-d2*i),0) for i in range(n)]

g = Vec2D(0,0.1)

#####################################################

def collidegrad(ball,grad=None,vert=0,hor=0):
	u1 = ball.vel
	if grad is not None:
		twoth = 2*np.arctan(grad)
		c2th = np.cos(twoth); s2th = np.sin(twoth)
		m1 = Vec2D(c2th,s2th); m2 = Vec2D(s2th,-c2th)
		ball.vel = Vec2D(m1*ball.vel, m2*ball.vel)
	elif vert:
		ball.vel = Vec2D(-ball.vel.x,ball.vel.y)
	elif hor:
		ball.vel = Vec2D(ball.vel.x,-ball.vel.y)
	
	ball.vel = (0.9*ball.vel)
	ball.pos += ball.vel
	return ball


def collidewalls(b):
	bxl = b.pos.x - b.radius; bxr = b.pos.x + b.radius
	byu = b.pos.y - b.radius; byd = b.pos.y + b.radius
	if not (0< bxl and bxr < WIDTH):
		if bxl < 0: d = bxl
		else: d = bxr - WIDTH
		b.pos -= Vec2D(d, 0)
		b = collidegrad(b,vert=1)
	if not (0 < byu and byd < HEIGHT):
		if byu < 0: d = byu
		else: d = byd - HEIGHT
		b.pos -= Vec2D(0, d)
		b.vel -= g #added to correct
		b = collidegrad(b,hor=1)
	return b

####################################################

def drawtrail(b):
	if (-int(WIDTH/2)< b.pos.x < int(WIDTH/2)) and (-int(HEIGHT/2 - 1) < b.pos.y < int(HEIGHT/2)):
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
			
			if (r.mag2() <= (b.radius + ba.radius)**2) and b.vel != ba.vel != Vec2D(0,0):
				x = rad_b + rad_ba - r
				b.pos += (-0.5*x)
				ba.pos += 0.5*x
				
				m1 = b.mass; m2 = ba.mass
				rb = b.pos - ba.pos
				rb_u = rb.unit()
				u1costh1 = (b.vel*r_u)*r_u ; perp_r = (-u1costh1+b.vel)
				if perp_r != Vec2D(0,0): perp_r_u = perp_r.unit()
				else: perp_r_u = Vec2D(0,0)
				u1sinth1 = (b.vel*perp_r_u) * perp_r_u
				
				u2costh2 = (ba.vel*rb_u)*rb_u; perp_rb = (-u2costh2+ba.vel)
				if perp_rb != Vec2D(0,0): perp_rb_u = perp_rb.unit()
				else: perp_rb_u = Vec2D(0,0)
				u2sinth2 = (ba.vel*perp_rb_u) * perp_rb_u
				u1 = u1costh1; u2 = u2costh2
				v2 = (m1*(2*u1 - u2)+m2*u2)/(m2+m1)
				v1 = (m2*(2*u2 - u1)+m1*u1)/(m1+m2)
				ba.vel = v2+u2sinth2
				b.vel = v1+u1sinth1
				
				b.pos += b.vel; ba.pos += ba.vel
	return b


def simulate_balls_colliding(i,b,cs=None):
	b = collidewalls(b)
	#if ct > 1:
	
	if cs:
		for c in cs:
			if c[0] != Vec2D(0,0) and c[1] != Vec2D(360,0):
				b = collideCircle(b,c[1],c[0],inner=False)
			else:
				b = collideCircle(b,c[1],c[0])
	world[i] = collideBalls(i,b,world)
	b = world[i]
	if b.pos.y + b.radius < HEIGHT:
		b.vel += g
	b.pos += b.vel
	
	#drawtrail(b)	
	drawball(b)
	
	if cs:
		for c in cs:
			pygame.draw.circle(surface,GREEN,(c[0]+Vec2D(WIDTH/2,HEIGHT/2)).tup(),c[1].x,5)

world = []; cs = []

def f(a,b):
	return random.randint(a,b)
def randomcolor():
	return f(0,255), f(0,255), f(0,255)
for i in range(24):
	for diff in range(7):
		world.append(Ball((i)*10,HEIGHT-(10*diff+5),0,0,color=randomcolor(),radius=5,mass=1))
	

def vib(i,b,ct):
	R = b.pos - Vec2D(120, HEIGHT-5)
	if R != Vec2D(0,0):
		for instant in range(ct,0,-period):
			if round(R.mag()) == round((wave_speed*instant)):
				b.vel = (10/(wave_speed*instant))*R.unit()




wave_speed = 0.5
period = 10 #freq = 1/period
cts = []

ct = 0
while True:
	surface.fill((0,0,0))
	for ev in pygame.event.get():
		if ev.type == pygame.QUIT:
			pygame.quit()
			quit()


	for i,b in enumerate(world):
		vib(i,b,ct)
		simulate_balls_colliding(i,b)

	for t in range(ct,0,-period):
		pygame.draw.circle(surface, GREEN, (120,HEIGHT-5),wave_speed*t,3)

		
	
	pygame.display.update()
	#print(ct)
	ct += 1

