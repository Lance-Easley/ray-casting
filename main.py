import pygame
import math

pygame.init()

screen_x = 641
screen_y = 361

win = pygame.display.set_mode((screen_x, screen_y))
win_rect = pygame.Rect(0, 0, screen_x, screen_y)

invisible = pygame.Surface((screen_x, screen_y))
invisible_image = pygame.image.load("nonvisible_map.png").convert()
invisible.set_colorkey("#123456")

visible_image = pygame.image.load("visible_map.png").convert()

pygame.display.set_caption("Ray Casting")

pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])

#####################################################################################
# This is a Python-Pygame translation from https://github.com/ncase/sight-and-light #
# Credits to https://github.com/ncase/ for the javascript implementation.           #
# Issue fixes from https://github.com/tomasiser are also implemented and translated #
#####################################################################################


# LINE SEGMENTS
segments = [

	# Border
	{"a":{"x":0,"y":0}, "b":{"x":screen_x,"y":0}},
	{"a":{"x":screen_x,"y":0}, "b":{"x":screen_x,"y":screen_y}},
	{"a":{"x":screen_x,"y":screen_y}, "b":{"x":0,"y":screen_y}},
	{"a":{"x":0,"y":screen_y}, "b":{"x":0,"y":0}},

	# Outer walls (-x+y corner - counter-clockwise)
	{"a":{"x":24,"y":24}, "b":{"x":24,"y":248}},
	{"a":{"x":24,"y":248}, "b":{"x":87,"y":248}},
	{"a":{"x":87,"y":248}, "b":{"x":87,"y":241}},
	#opening
	{"a":{"x":120,"y":241}, "b":{"x":120,"y":248}},
	{"a":{"x":120,"y":248}, "b":{"x":160,"y":248}},
	{"a":{"x":160,"y":248}, "b":{"x":160,"y":337}},
	{"a":{"x":160,"y":337}, "b":{"x":520,"y":337}},
	{"a":{"x":520,"y":337}, "b":{"x":520,"y":257}},
	{"a":{"x":520,"y":257}, "b":{"x":505,"y":257}},
	{"a":{"x":505,"y":257}, "b":{"x":505,"y":264}},
	#opening
	{"a":{"x":480,"y":264}, "b":{"x":480,"y":257}},
	{"a":{"x":480,"y":257}, "b":{"x":448,"y":257}},
	{"a":{"x":448,"y":257}, "b":{"x":448,"y":249}},
	{"a":{"x":448,"y":249}, "b":{"x":441,"y":249}},
	#opening
	{"a":{"x":441,"y":240}, "b":{"x":448,"y":240}},
	{"a":{"x":448,"y":240}, "b":{"x":448,"y":233}},
	{"a":{"x":448,"y":233}, "b":{"x":441,"y":233}},
	#opening
	{"a":{"x":441,"y":224}, "b":{"x":448,"y":224}},
	{"a":{"x":448,"y":224}, "b":{"x":448,"y":217}},
	{"a":{"x":448,"y":217}, "b":{"x":441,"y":217}},
	#opening
	{"a":{"x":441,"y":208}, "b":{"x":448,"y":208}},
	{"a":{"x":448,"y":208}, "b":{"x":448,"y":201}},
	{"a":{"x":448,"y":201}, "b":{"x":441,"y":201}},
	#opening
	{"a":{"x":441,"y":192}, "b":{"x":448,"y":192}},
	{"a":{"x":448,"y":192}, "b":{"x":448,"y":185}},
	{"a":{"x":448,"y":185}, "b":{"x":441,"y":185}},
	#opening
	{"a":{"x":441,"y":176}, "b":{"x":448,"y":176}},
	{"a":{"x":448,"y":176}, "b":{"x":448,"y":168}},
	{"a":{"x":448,"y":168}, "b":{"x":608,"y":168}},
	{"a":{"x":608,"y":168}, "b":{"x":608,"y":24}},
	{"a":{"x":608,"y":24}, "b":{"x":24,"y":24}},

	# Inner walls (-x+y corner - counter-clockwise)
	{"a":{"x":31,"y":31}, "b":{"x":31,"y":88}},
	{"a":{"x":31,"y":88}, "b":{"x":71,"y":88}},
	{"a":{"x":71,"y":88}, "b":{"x":71,"y":96}},
	{"a":{"x":71,"y":96}, "b":{"x":31,"y":96}},
	{"a":{"x":31,"y":96}, "b":{"x":31,"y":241}},
	{"a":{"x":31,"y":241}, "b":{"x":87,"y":241}},
	#opening
	{"a":{"x":120,"y":241}, "b":{"x":160,"y":241}},
	{"a":{"x":160,"y":241}, "b":{"x":160,"y":129}},
	{"a":{"x":160,"y":129}, "b":{"x":167,"y":129}},
	{"a":{"x":167,"y":129}, "b":{"x":167,"y":137}},
	{"a":{"x":167,"y":137}, "b":{"x":240,"y":137}},
	{"a":{"x":240,"y":137}, "b":{"x":240,"y":129}},
	{"a":{"x":240,"y":129}, "b":{"x":247,"y":129}},
	{"a":{"x":247,"y":129}, "b":{"x":247,"y":160}},
	{"a":{"x":247,"y":160}, "b":{"x":240,"y":160}},
	{"a":{"x":240,"y":160}, "b":{"x":240,"y":144}},
	{"a":{"x":240,"y":144}, "b":{"x":167,"y":144}},
	{"a":{"x":167,"y":144}, "b":{"x":167,"y":185}},
	{"a":{"x":167,"y":185}, "b":{"x":240,"y":185}},
	{"a":{"x":240,"y":185}, "b":{"x":240,"y":177}},
	{"a":{"x":240,"y":177}, "b":{"x":247,"y":177}},
	{"a":{"x":247,"y":177}, "b":{"x":247,"y":208}},
	{"a":{"x":247,"y":208}, "b":{"x":240,"y":208}},
	{"a":{"x":240,"y":208}, "b":{"x":240,"y":192}},
	{"a":{"x":240,"y":192}, "b":{"x":167,"y":192}},
	{"a":{"x":167,"y":192}, "b":{"x":167,"y":330}},
	{"a":{"x":167,"y":330}, "b":{"x":240,"y":330}},
	{"a":{"x":240,"y":330}, "b":{"x":240,"y":233}},
	{"a":{"x":240,"y":233}, "b":{"x":247,"y":233}},
	{"a":{"x":247,"y":233}, "b":{"x":247,"y":257}},
	{"a":{"x":247,"y":257}, "b":{"x":255,"y":257}},
	{"a":{"x":255,"y":257}, "b":{"x":255,"y":264}},
	{"a":{"x":255,"y":264}, "b":{"x":247,"y":264}},
	{"a":{"x":247,"y":264}, "b":{"x":247,"y":330}},
	{"a":{"x":247,"y":330}, "b":{"x":337,"y":330}},
	{"a":{"x":337,"y":330}, "b":{"x":337,"y":264}},
	{"a":{"x":337,"y":264}, "b":{"x":280,"y":264}},
	{"a":{"x":280,"y":264}, "b":{"x":280,"y":257}},
	{"a":{"x":280,"y":257}, "b":{"x":344,"y":257}},
	{"a":{"x":344,"y":257}, "b":{"x":344,"y":330}},
	{"a":{"x":344,"y":330}, "b":{"x":441,"y":330}},
	{"a":{"x":441,"y":330}, "b":{"x":441,"y":322}},
	{"a":{"x":441,"y":322}, "b":{"x":448,"y":322}},
	{"a":{"x":448,"y":322}, "b":{"x":448,"y":330}},
	{"a":{"x":448,"y":330}, "b":{"x":513,"y":330}},
	{"a":{"x":513,"y":330}, "b":{"x":513,"y":264}},
	{"a":{"x":513,"y":264}, "b":{"x":505,"y":264}},
	{"a":{"x":480,"y":264}, "b":{"x":448,"y":264}},
	{"a":{"x":448,"y":264}, "b":{"x":448,"y":273}},
	{"a":{"x":448,"y":273}, "b":{"x":441,"y":273}},
	{"a":{"x":441,"y":273}, "b":{"x":441,"y":249}},
	{"a":{"x":441,"y":240}, "b":{"x":441,"y":233}},
	{"a":{"x":441,"y":224}, "b":{"x":441,"y":218}},
	{"a":{"x":441,"y":208}, "b":{"x":441,"y":201}},
	{"a":{"x":441,"y":192}, "b":{"x":441,"y":185}},
	{"a":{"x":441,"y":176}, "b":{"x":441,"y":145}},
	{"a":{"x":441,"y":145}, "b":{"x":448,"y":145}},
	{"a":{"x":448,"y":145}, "b":{"x":448,"y":161}},
	{"a":{"x":448,"y":161}, "b":{"x":601,"y":161}},
	{"a":{"x":601,"y":161}, "b":{"x":601,"y":31}},
	{"a":{"x":601,"y":31}, "b":{"x":504,"y":31}},
	{"a":{"x":504,"y":31}, "b":{"x":504,"y":47}},
	{"a":{"x":504,"y":47}, "b":{"x":497,"y":47}},
	{"a":{"x":497,"y":47}, "b":{"x":497,"y":31}},
	{"a":{"x":497,"y":31}, "b":{"x":448,"y":31}},
	{"a":{"x":448,"y":31}, "b":{"x":448,"y":88}},
	{"a":{"x":448,"y":88}, "b":{"x":497,"y":88}},
	{"a":{"x":497,"y":88}, "b":{"x":497,"y":72}},
	{"a":{"x":497,"y":72}, "b":{"x":504,"y":72}},
	{"a":{"x":504,"y":72}, "b":{"x":504,"y":96}},
	{"a":{"x":504,"y":96}, "b":{"x":448,"y":96}},
	{"a":{"x":448,"y":96}, "b":{"x":448,"y":120}},
	{"a":{"x":448,"y":120}, "b":{"x":441,"y":120}},
	{"a":{"x":441,"y":120}, "b":{"x":441,"y":96}},
	{"a":{"x":441,"y":96}, "b":{"x":377,"y":96}},
	{"a":{"x":377,"y":96}, "b":{"x":377,"y":88}},
	{"a":{"x":377,"y":88}, "b":{"x":441,"y":88}},
	{"a":{"x":441,"y":88}, "b":{"x":441,"y":31}},
	{"a":{"x":441,"y":31}, "b":{"x":344,"y":31}},
	{"a":{"x":344,"y":31}, "b":{"x":344,"y":88}},
	{"a":{"x":344,"y":88}, "b":{"x":352,"y":88}},
	{"a":{"x":352,"y":88}, "b":{"x":352,"y":96}},
	{"a":{"x":352,"y":96}, "b":{"x":329,"y":96}},
	{"a":{"x":329,"y":96}, "b":{"x":329,"y":88}},
	{"a":{"x":329,"y":88}, "b":{"x":337,"y":88}},
	{"a":{"x":337,"y":88}, "b":{"x":337,"y":31}},
	{"a":{"x":337,"y":31}, "b":{"x":247,"y":31}},
	{"a":{"x":247,"y":31}, "b":{"x":247,"y":88}},
	{"a":{"x":247,"y":88}, "b":{"x":303,"y":88}},
	{"a":{"x":303,"y":88}, "b":{"x":303,"y":96}},
	{"a":{"x":303,"y":96}, "b":{"x":247,"y":96}},
	{"a":{"x":247,"y":96}, "b":{"x":247,"y":104}},
	{"a":{"x":247,"y":104}, "b":{"x":240,"y":104}},
	{"a":{"x":240,"y":104}, "b":{"x":240,"y":96}},
	{"a":{"x":240,"y":96}, "b":{"x":232,"y":96}},
	{"a":{"x":232,"y":96}, "b":{"x":232,"y":88}},
	{"a":{"x":232,"y":88}, "b":{"x":240,"y":88}},
	{"a":{"x":240,"y":88}, "b":{"x":240,"y":31}},
	{"a":{"x":240,"y":31}, "b":{"x":207,"y":31}},
	{"a":{"x":207,"y":31}, "b":{"x":207,"y":88}},
	{"a":{"x":207,"y":88}, "b":{"x":215,"y":88}},
	{"a":{"x":215,"y":88}, "b":{"x":215,"y":96}},
	{"a":{"x":215,"y":96}, "b":{"x":167,"y":96}},
	{"a":{"x":167,"y":96}, "b":{"x":167,"y":104}},
	{"a":{"x":167,"y":104}, "b":{"x":160,"y":104}},
	{"a":{"x":160,"y":104}, "b":{"x":160,"y":96}},
	{"a":{"x":160,"y":96}, "b":{"x":120,"y":96}},
	{"a":{"x":120,"y":96}, "b":{"x":120,"y":88}},
	{"a":{"x":120,"y":96}, "b":{"x":120,"y":88}},
	{"a":{"x":120,"y":88}, "b":{"x":200,"y":88}},
	{"a":{"x":200,"y":88}, "b":{"x":200,"y":31}},
	{"a":{"x":200,"y":31}, "b":{"x":31,"y":31}},

]

segment_deltas = set()
uniquePoints = set()
for segment in segments:
	# s_px, s_py, s_dx, s_dy
	segment_deltas.add((segment['a']['x'], segment['a']['y'], segment['b']['x'] - segment['a']['x'], segment['b']['y'] - segment['a']['y']))

	if tuple(segment["a"].items()) not in uniquePoints:
		uniquePoints.add(tuple(segment["a"].items()))
	if tuple(segment["b"].items()) not in uniquePoints:
		uniquePoints.add(tuple(segment["b"].items()))

# Find intersection of RAY & SEGMENT
def getIntersection(ray, segment_delta):
	# RAY in parametric: Point + Delta*T1
	r_px = ray['a']['x']
	r_py = ray['a']['y']
	r_dx = ray['b']['x'] - ray['a']['x']
	r_dy = ray['b']['y'] - ray['a']['y']

	# SEGMENT in parametric: Point + Delta*T2
	s_px, s_py, s_dx, s_dy = segment_delta

	# Are they parallel? If so, no intersect
	if r_dx * s_dy == r_dy * s_dx:
		# Unit vectors are the same.
		return None

	# SOLVE FOR T1 & T2
	T2 = (r_dx * (s_py - r_py) + r_dy * (r_px - s_px)) / (s_dx * r_dy - s_dy * r_dx)
	if r_dy == 0:
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
	mouse_x, mouse_y = pygame.mouse.get_pos()

	# Draw segments
	# color = "#999999"
	# for seg in segments:
	# 	pygame.draw.line(win, color, (seg["a"]["x"], seg["a"]["y"]), (seg["b"]["x"], seg["b"]["y"]), 1)

	# Get all angles
	uniqueAngles = set()
	for uniquePoint in uniquePoints:
		points_dict = dict(uniquePoint)
		angle = math.atan2(points_dict['y'] - mouse_y, points_dict['x'] - mouse_x)
		points_dict['angle'] = angle
		uniqueAngles.update([angle-0.00001, angle+0.00001])

	uniqueAngles = sorted(uniqueAngles)

	# RAYS IN ALL DIRECTIONS
	intersects = []
	for angle in uniqueAngles:

		# Calculate dx & dy from angle
		dx = math.cos(angle)
		dy = math.sin(angle)

		# Ray from center of screen to mouse
		ray = {
			"a":{"x": mouse_x, "y": mouse_y},
			"b":{"x": mouse_x + dx, "y": mouse_y + dy}
		}

		# Find CLOSEST intersection
		closestIntersect = None
		for segment_delta in segment_deltas:
			intersect = getIntersection(ray,segment_delta)
			if not intersect: continue
			elif not closestIntersect or intersect["param"] < closestIntersect["param"]:
				closestIntersect = intersect

		# Intersect angle
		if not closestIntersect: continue
		# Add to list of intersects
		else:
			intersects.append(closestIntersect)

	# DRAW ALL RAYS
	points = [(intersect['x'], intersect['y']) for intersect in intersects]

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
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					run = False


		redrawGameWindow()

		clock.tick(60)
	pygame.quit()
