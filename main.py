import pygame
import math

pygame.init()

screen_x = 641
screen_y = 361

win = pygame.display.set_mode((screen_x, screen_y))
win_rect = pygame.Rect(0, 0, screen_x, screen_y)

invisible = pygame.Surface((screen_x, screen_y))
invisible_image = pygame.image.load("background.png")
invisible.set_colorkey("#123456")

visible = pygame.Surface((screen_x, screen_y))
visible_image = pygame.image.load("foreground.png")

pygame.display.set_caption("Ray Casting")


#####################################################################################
# This is a Python-Pygame translation from https://github.com/ncase/sight-and-light #
# Credits to https://github.com/ncase/ for the javascript implementation.           #
# Issue fixes from https://github.com/tomasiser are also implemented and translated #
#####################################################################################


# LINE SEGMENTS
segments = [

	# Border
	{"a":{"x":0,"y":0}, "b":{"x":640,"y":0}},
	{"a":{"x":640,"y":0}, "b":{"x":640,"y":360}},
	{"a":{"x":640,"y":360}, "b":{"x":0,"y":360}},
	{"a":{"x":0,"y":360}, "b":{"x":0,"y":0}},

	# Polygon #1
	{"a":{"x":100,"y":150}, "b":{"x":120,"y":50}},
	{"a":{"x":120,"y":50}, "b":{"x":200,"y":80}},
	{"a":{"x":200,"y":80}, "b":{"x":140,"y":210}},
	{"a":{"x":140,"y":210}, "b":{"x":100,"y":150}},

	# Polygon #2
	{"a":{"x":100,"y":200}, "b":{"x":120,"y":250}},
	{"a":{"x":120,"y":250}, "b":{"x":60,"y":300}},
	{"a":{"x":60,"y":300}, "b":{"x":100,"y":200}},

	# Polygon #3
	{"a":{"x":200,"y":260}, "b":{"x":220,"y":150}},
	{"a":{"x":220,"y":150}, "b":{"x":300,"y":200}},
	{"a":{"x":300,"y":200}, "b":{"x":350,"y":320}},
	{"a":{"x":350,"y":320}, "b":{"x":200,"y":260}},

	# Polygon #4
	{"a":{"x":340,"y":60}, "b":{"x":360,"y":40}},
	{"a":{"x":360,"y":40}, "b":{"x":370,"y":70}},
	{"a":{"x":370,"y":70}, "b":{"x":340,"y":60}},

	# Polygon #5
	{"a":{"x":450,"y":190}, "b":{"x":560,"y":170}},
	{"a":{"x":560,"y":170}, "b":{"x":540,"y":270}},
	{"a":{"x":540,"y":270}, "b":{"x":430,"y":290}},
	{"a":{"x":430,"y":290}, "b":{"x":450,"y":190}},

	# Polygon #6
	{"a":{"x":400,"y":95}, "b":{"x":580,"y":50}},
	{"a":{"x":580,"y":50}, "b":{"x":480,"y":150}},
	{"a":{"x":480,"y":150}, "b":{"x":400,"y":95}}

]

# Find intersection of RAY & SEGMENT
def getIntersection(ray, segment):
	# RAY in parametric: Point + Delta*T1
	r_px = ray['a']['x']
	r_py = ray['a']['y']
	r_dx = ray['b']['x'] - ray['a']['x']
	r_dy = ray['b']['y'] - ray['a']['y']

	# SEGMENT in parametric: Point + Delta*T2
	s_px = segment['a']['x']
	s_py = segment['a']['y']
	s_dx = segment['b']['x'] - segment['a']['x']
	s_dy = segment['b']['y'] - segment['a']['y']

	# Are they parallel? If so, no intersect
	if r_dx * s_dy == r_dy * s_dx:
		# Unit vectors are the same.
		return None

	# SOLVE FOR T1 & T2
	# r_px+r_dx*T1 = s_px+s_dx*T2 && r_py+r_dy*T1 = s_py+s_dy*T2
	# ==> T1 = (s_px+s_dx*T2-r_px)/r_dx = (s_py+s_dy*T2-r_py)/r_dy
	# ==> s_px*r_dy + s_dx*T2*r_dy - r_px*r_dy = s_py*r_dx + s_dy*T2*r_dx - r_py*r_dx
	# ==> T2 = (r_dx*(s_py-r_py) + r_dy*(r_px-s_px))/(s_dx*r_dy - s_dy*r_dx)
	T2 = (r_dx * (s_py - r_py) + r_dy * (r_px - s_px)) / (s_dx * r_dy - s_dy * r_dx)
	if r_dy == 0.0:
		T1 = (s_px + s_dx * T2 - r_px) / r_dx
	else:
		T1 = (s_py + s_dy * T2 - r_py) / r_dy

	# Must be within parametic whatevers for RAY/SEGMENT
	if T1 < 0: return None
	if T2 < 0 or T2 > 1: return None

	# Return the POINT OF INTERSECTION
	return {
		'x': r_px + r_dx * T1,
		'y': r_py + r_dy * T1,
		'param': T1
	}

#######################################################

# DRAWING
def draw(segments):
	mouse = pygame.mouse.get_pos()

	# Draw segments
	# color = "#999999"
	# for seg in segments:
	# 	pygame.draw.line(canvas, color, (seg["a"]["x"], seg["a"]["y"]), (seg["b"]["x"], seg["b"]["y"]), 1)

	uniquePoints = []
	for seg in segments:
		if seg["a"] not in uniquePoints:
			uniquePoints.append(seg["a"])
		if seg["b"] not in uniquePoints:
			uniquePoints.append(seg["b"])
	

	# Get all angles
	uniqueAngles = []
	for uniquePoint in uniquePoints:
		angle = math.atan2(uniquePoint['y'] - mouse[1], uniquePoint['x'] - mouse[0])
		uniquePoint['angle'] = angle
		uniqueAngles.extend([angle-0.00001, angle+0.00001])

	uniqueAngles.sort()

	# RAYS IN ALL DIRECTIONS
	intersects = []
	for angle in uniqueAngles:

		# Calculate dx & dy from angle
		dx = math.cos(angle)
		dy = math.sin(angle)

		# Ray from center of screen to mouse
		ray = {
			"a":{"x": mouse[0], "y": mouse[1]},
			"b":{"x": mouse[0] + dx, "y": mouse[1] + dy}
		}

		# Find CLOSEST intersection
		closestIntersect = None
		for segment in segments:
			intersect = getIntersection(ray,segment)
			if not intersect: continue
			elif not closestIntersect or intersect["param"] < closestIntersect["param"]:
				closestIntersect = intersect

		# Intersect angle
		if not closestIntersect: continue

		# Add to list of intersects
		if closestIntersect:
			closestIntersect["angle"] = angle
			intersects.append(closestIntersect)

	# DRAW AS A GIANT POLYGON
	# ctx.fillStyle = "#dd3838";
	# ctx.beginPath();
	# ctx.moveTo(intersects[0].x,intersects[0].y);
	# for(var i=1;i<intersects.length;i++){
	# 	var intersect = intersects[i];
	# 	ctx.lineTo(intersect.x,intersect.y);
	# }
	# ctx.fill();

	# DRAW ALL RAYS
	color = "#dd3838"
	points = []
	for intersect in intersects:

		# Draw red laser
		# pygame.draw.line(canvas, color, mouse, (intersect["x"], intersect["y"]), 1)
		
		# Draw red dot
		# pygame.draw.circle(canvas, color, (intersect['x'], intersect['y']), 4)

		# Draw Polygon Shading
		points.append((intersect['x'], intersect['y']))
	# # print("\n", points, "\n")
	invisible.blit(invisible_image, win_rect)
	pygame.draw.polygon(invisible, "#123456", points)


#######################################################

def redrawGameWindow():
	win.blit(visible_image, win_rect)
	win.blit(invisible, win_rect)
	draw(segments)
	pygame.display.update()


#mainloop

if __name__ == '__main__':
	run = True
	clock = pygame.time.Clock()
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		
		keys = pygame.key.get_pressed()

		if keys[pygame.K_ESCAPE]:
			run = False

		redrawGameWindow()

		clock.tick(60)
	pygame.quit()
