#Aliisa Roe
#Project 1 -- pygame
#Oct 5, 2015

"""This is a simple game where the user moves a pangolin image with 
arrow keys to get to the top of the screen without colliding with moving 
snake sprites--- an experiment with pygame."""

#I used pygame tutorial videos @ Kris Occhipinti
#spritesheet from #colorado.edu/StudentGroups/uchc/trips.html creative commons
# help on spriteCode from http://pygame.org/wiki/Spritesheet
#sound from SoundBible.com creative commons
	#win from Mr Smith
	#lose from DavinCammas
	#hit from Mark DiAngelo
#pangolin.png from https://pixabay.com/en/animal-pangolin-wild-157578/ openSource vectors


import pygame, random, time, pygame.mixer
from pygame.locals import *


pygame.init()
clock = pygame.time.Clock() #will monitor frames per second for consistent speed on different hardware
size = width, height = 400, 430
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))#black
hitSound = pygame.mixer.Sound('hit.wav')
winSound = pygame.mixer.Sound('meow.wav')
loseSound = pygame.mixer.Sound('siren.wav')

class Spritesheet(object): #edited code from _____
    def __init__(self, filename):
		self.sheet = pygame.image.load(filename).convert()
    def image_at(self, rectangle): 
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        image = pygame.transform.flip(image, True, False)
        return image
        
class Sprite(object):
	def __init__(self, sprite, y):
		self.startingX = random.randrange(370)
		self.x = self.startingX
		self.y = y
		self.direction = "right"
		self.goingRight = True
		screen.blit(sprite, (self.x, self.y))
	def get_y(self):
		return self.y
	def update_x(self, newX):
		self.x = newX
	def get_x(self):
		return self.x
	def get_rect(self):
		return (pygame.Rect((self.x, self.y), (50, 30)))
	def hit_side(self):
		x = self.x
		if x >= 360 or x <= 0 :
			return True
		else:
			return False
	def newDirection(self):
		if self.direction == "left":
			self.direction = "right"
		elif self.direction == "right":
			self.direction = "left"
			
def introPrint():
	print ("Welcome, to the pangolin hustle!")
	time.sleep(2)
	print ("Freddy the pangolin is trying to get to the other side of the screen, but he is very allergic to snakes.")
	time.sleep(3)
	print "Won't you help Freddy get accross?"
	print "Let's get started! Use your arrow keys to get Freddy to the top of the screen."
	time.sleep(3)
	print "And DON'T TOUCH ANY SNAKES!!"
	print "Press 'q' to quit."
	print "GO!"
	time.sleep(3)
	
			
def main():
	introPrint()

	ss = Spritesheet('char2.png')
	
	snakes = [] #enemy
	snakes.append(ss.image_at((0, 44, 44, 33)))
	snakes.append(ss.image_at((63, 44, 50, 33)))
	snakes.append(ss.image_at((130, 44, 50, 33)))
	snakes.append(ss.image_at((190, 44, 50, 33)))
	
	snakeRowList = []
	yVal = 0
	for i in range(13): #makes 13 rows of enemy snakes
		snakeRowList.append(Sprite(snakes[0], yVal))
		yVal += 30
	
	pangolin = pygame.image.load("pangolin.png").convert() #player
	pangolin = pygame.transform.scale(pangolin, (50, 50))
	
	#initialize values
	x = 0
	y = 0
	snakeSprite = 0
	hit = 0
	arrowY = 400
	arrowX = 200
	beenHit = False
	
	#GAME LOOP
	running = True
	while running:
		
		screen.blit(pangolin, (arrowX,arrowY))
		pangolinPos = pygame.Rect((arrowX, arrowY), (50, 50))
		
		for event in pygame.event.get():
			#QUIT types
			if event.type == pygame.QUIT:
				running = False
			elif event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q):
				running = False
				
			elif event.type == KEYDOWN and (event.key == K_UP):
				if 0 < arrowY <= 400:
					arrowY -= 10
			elif event.type == KEYDOWN and (event.key == K_DOWN):
				if 0 < arrowY < 400:
					arrowY += 10
			elif event.type == KEYDOWN and (event.key == K_LEFT):
				if 0 < arrowX < 400:
					arrowX -= 10
			elif event.type == KEYDOWN and (event.key == K_RIGHT):
				if 0 < arrowX < 400:
					arrowX += 10
		"""	#screenshots	
			elif event.type == KEYDOWN and event.key == K_SPACE:
				pygame.image.save(screen, "screenshot1.png")""" #here for screenshots that didn't capture my snake sprites :(
		
		#choose sprite image from snakeRowList
		if snakeSprite >= 3:
			snakeSprite -= 1
		else:
			snakeSprite += 1
		
		#animate Sprites, check for pangolin collision
		for row in snakeRowList:
			if row.hit_side():
				row.newDirection()
			if row.direction == "right":
				row.update_x((row.get_x() + 8))
			elif row.direction == "left":
				row.update_x((row.get_x() - 8))
			screen.blit(snakes[snakeSprite], (row.get_x(), row.get_y()))
			if (pangolinPos).colliderect(row.get_rect()): #is there a better way?
				beenHit = True
		if beenHit == True:
			hit += 1
			print "OW! only", (10-hit), "more lives!"
			hitSound.play()
			beenHit = False
			screen.fill((250, 0, 0))
		
		#game scores
		if hit >= 9:
			loseSound.play()
			print "You died..."
			running = False
		elif hit <= 10 and arrowY <= 0: 
			screen.fill((0, 250, 0))
			print "YOU WIN!"
			winSound.play()
			running = False
					
		pygame.display.flip()
		screen.fill((0,0,0))
		clock.tick(5)
		
	time.sleep(2)
	pygame.quit()

main()
