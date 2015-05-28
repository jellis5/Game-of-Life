import pygame, sys
from pygame.locals import *

WINDOWSIZE = (1200, 1000)
FPS = 15
MINFPS, MAXFPS = 1, 60

BLACK = (0, 0, 0)
GREY = (40, 40, 40)
GREEN = (0, 100, 0)

BLOCKSIZE = (20, 20)

windowSurf = pygame.display.set_mode(WINDOWSIZE)
pygame.display.set_caption("Game of Life (PAUSED)")
fpsClock = pygame.time.Clock()

def drawGrid():
	"""Draw grid on top of window."""
	for x in range(BLOCKSIZE[0], WINDOWSIZE[0], BLOCKSIZE[0]):
		pygame.draw.line(windowSurf, GREY, (x, 0), (x, WINDOWSIZE[1]))
	for y in range(BLOCKSIZE[1], WINDOWSIZE[1], BLOCKSIZE[1]):
		pygame.draw.line(windowSurf, GREY, (0, y), (WINDOWSIZE[0], y))
		
def getNeighbors(coords):
	"""Returns tuple of top-left coordinates of neighbors (including diagonal) of coords.
		Coords is tuple containing top-left corner coordinates."""
	neighbors = []
	
	leftNeighborsX = coords[0] - BLOCKSIZE[0]
	rightNeighborsX = coords[0] + BLOCKSIZE[0]
	topNeighborsY = coords[1] - BLOCKSIZE[1]
	bottomNeighborsY = coords[1] + BLOCKSIZE[1]
	
	if leftNeighborsX < 0:
		leftNeighborsX = WINDOWSIZE[0] - BLOCKSIZE[0]
	if rightNeighborsX == WINDOWSIZE[0]:
		rightNeighborsX = 0
	if topNeighborsY < 0:
		topNeighborsY = WINDOWSIZE[1] - BLOCKSIZE[1]
	if bottomNeighborsY == WINDOWSIZE[1]:
		bottomNeighborsY = 0
	
	neighbors.append((leftNeighborsX, topNeighborsY))
	neighbors.append((leftNeighborsX, coords[1]))
	neighbors.append((leftNeighborsX, bottomNeighborsY))
	neighbors.append((coords[0], topNeighborsY))
	neighbors.append((coords[0], bottomNeighborsY))
	neighbors.append((rightNeighborsX, topNeighborsY))
	neighbors.append((rightNeighborsX, coords[1]))
	neighbors.append((rightNeighborsX, bottomNeighborsY))
	
	return tuple(neighbors)
		
def getBlocks():
	"""Returns dictionary of each block's values."""
	blocks = {}
	for x in range(0, WINDOWSIZE[0], BLOCKSIZE[0]):
		for y in range(0, WINDOWSIZE[1], BLOCKSIZE[1]):
			blocks['block'+str(x)+'_'+str(y)] = [Rect((x, y), BLOCKSIZE), getNeighbors((x, y)), False]
	return blocks

def main():
	global FPS
	blocks = getBlocks()
	grid = False
	paused = True
	
	while True:
		print(fpsClock.get_fps())
		windowSurf.fill(BLACK)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				elif event.key == K_g:
					grid = not grid
				elif event.key == K_UP:
					if FPS < MAXFPS:
						FPS += 1
				elif event.key == K_DOWN:
					if FPS > MINFPS:
						FPS -= 1
				elif event.key == K_SPACE:
					paused = not paused
					if paused:
						pygame.display.set_caption("Game of Life (PAUSED)")
					else:
						pygame.display.set_caption("Game of Life (RUNNING)")
		if paused:
			buttonsPressed = pygame.mouse.get_pressed()
			if buttonsPressed[0] or buttonsPressed[2]:
				for block in blocks:
					if blocks[block][0].collidepoint(pygame.mouse.get_pos()):
						if buttonsPressed[0]:
							blocks[block][2] = True
						else:
							blocks[block][2] = False
				
		else:
			newAlive = []
			newDead = []
			for block in blocks:
				numAlive = 0
				for neighborCoords in blocks[block][1]:
					if blocks['block'+str(neighborCoords[0])+'_'+str(neighborCoords[1])][2]:
						numAlive += 1
				if blocks[block][2] and (numAlive < 2 or numAlive > 3):
					newDead.append(block)
				if not blocks[block][2] and numAlive == 3:
					newAlive.append(block)
			for block in newAlive:
				blocks[block][2] = True
			for block in newDead:
				blocks[block][2] = False
		
		for block in blocks:
			if blocks[block][2]:
				pygame.draw.rect(windowSurf, GREEN, blocks[block][0])
		
		if grid:
			drawGrid()
		
		pygame.display.update()
		fpsClock.tick(FPS)
	
	return 0

main()
