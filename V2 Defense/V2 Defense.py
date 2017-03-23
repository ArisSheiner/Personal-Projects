#
# 				                  ____________
# _______________________________/ V2 Defense \__________________________________ 

#					Aris Sheiner
#					CSCI 1300
#					TA: Dana Hughes
#					Level: Beginner --- Bumped to intermediate



############# Note: For me all files by the .py must be in the home folder unless you open with Geany! If that doesn't work, try Geany!!###########################


#####	Preamble	####
import pygame, sys, pygame.mixer, random, _thread, math #import lots of stuff
from pygame.locals import *
from random import randint
pygame.init() #Initialize pygame



## Game Screen ##
screen_width = 980
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height)) ##Make me a screen
background=pygame.image.load("Resources/Sky.png").convert()	##Load the background and convert it
background=pygame.transform.scale(background, (1200,800))	#Resize the background



## Cursor & Keyboard Settings ##
pygame.mouse.set_visible(0) #invisible mouse
pygame.key.set_repeat(10,10) # Allow repeating for key-press events on key hold

###		Creating Sound		###
music = pygame.mixer.Sound("Resources/music.wav") #Background music
tank = pygame.mixer.Sound("Resources/tank.wav") #plane sound
fire_sound = pygame.mixer.Sound("Resources/fire.wav") #firing sound
explode = pygame.mixer.Sound("Resources/explode.wav") #explosion sound
sad = pygame.mixer.Sound("Resources/sad.wav") #game over sound


# Setting volume #
music.set_volume(0.5)
fire_sound.set_volume(0.3)
explode.set_volume(0.3)
tank.set_volume(0.5)
sad.set_volume(0.5)


####		Classes		####

###		System Classes		###

##	Game Clock ##
class clock:
	fps = None ## Game optimized frames per second
	clock = None ## clock variable
	def __init__(self): 
		self.clock = pygame.time.Clock() #pygame built-in clock function
		self.fps = 60 ##Asign 60 frames per second
	def clock_tick(self):
		clock_tick = self.clock.tick(self.fps) #return clock ticking at self.fps fps
		return clock_tick 
	
	

###		Sprite Classes		###

##	Player Sprite	##
class Player:
	
	##		Player Settings		##
	image = None
	health = None
	p_x = None
	p_y = None
	score = None
	
	##		Shot Settings		##
	s_x = None	#Shot x
	s_y = None	#Shot y
	s_dir_y = None #Shot direction
	s_dir_x = None
	shot_image = None
	fired = None
	
	##	Initialization Function	##
	def __init__(self):
		
		### Loading Images	###
		self.image = pygame.image.load("Resources/player_up.png") #load ship image
		self.image = pygame.transform.scale(self.image, (80,80)) #shrink player image
		self.shot_image = pygame.image.load("Resources/shot.png") #load shot image
		
		### Display Values	###
		self.fired = False
		
		
		##	Starting Values ##
		self.health = 100 #Set player health at 100%
		self.p_x = screen.get_width()/2 #Player starting x
		self.p_y = screen.get_height()-self.image.get_height()/1.3 #Player starting y
		self.score = 0
		self.s_x = self.p_x-40
		self.s_y = self.p_y
		self.s_dir_y = 1 #make shot go up/down
		self.s_dir_x = 0 #make shot not go left/right
		
	### Player Image Flipping	###
	def flip_left(self):
		self.image = pygame.image.load("Resources/player_left.png")	#rotate 
		self.image = pygame.transform.scale(self.image, (80,80)) #shrink player image
		
	def flip_right(self):
		self.image = pygame.image.load("Resources/player_right.png")	#rotate 
		self.image = pygame.transform.scale(self.image, (80,80)) #shrink player image	
		
	def flip_down(self):
		self.image = pygame.image.load("Resources/player_down.png")	#rotate 
		self.image = pygame.transform.scale(self.image, (80,80)) #shrink player image	
	
	def flip_up(self):
		self.image = pygame.image.load("Resources/player_up.png")	#rotate 
		self.image = pygame.transform.scale(self.image, (80,80)) #shrink player image
		
		
				
		##	Player Movement	##
	def move_left(self): 	#move left
		self.p_x -= 5
	def move_right(self):	#move right
		self.p_x += 5
	def move_up(self):		#move up
		self.p_y -= 5 
	def move_down(self):	#move down
		self.p_y += 5
		
	
		
##### Firing Functions	#####
	
	
		
	###		Fire Missile	###
	def fire(self): ## Miss
		if self.fired == False:
			self.s_x = self.p_x - 40  ##Where to shoot from
			self.s_y = self.p_y	##Where to shoot from
			
			self.fired = True ## FIRE ZE MISSILES
			_thread.start_new_thread(self.firing,()) #Start a new thread for the fired shot.
													#I admit that I'm not an expert on what a thread does 
													#does but after furiously Googling the problem,
													#I just decided to blindly take its advice.
													
	### Flying Missile	###
	def firing(self):
		
		fps = clock()
		
		while self.fired == True and screen.get_height() > self.s_y > 0 and screen.get_width() > self.s_x > 0 : ## While the missile has been fired and on the screen,

			self.s_y -= 50*self.s_dir_y # Make missile go continue up
			self.s_x -=50*self.s_dir_x
			fps.clock_tick() #Tick make missile obey the game clock. It doesn't like to. I assume because it's so small.

		##	Reset to initial values	##
		self.fired = False #shot not fired
		self.s_x = self.p_x - 40 ##Where to shoot from
		self.s_y = self.p_y ##Where to shoot from
		

	##render player	##
	def draw(self):  
		screen.blit(self.image, (self.p_x, self.p_y))
		if self.fired == True:
			screen.blit(self.shot_image, (self.s_x, self.s_y))
	## shot hit box ##
	def shot_box(self):
		shot_box = Rect( (self.s_x, self.s_y), self.shot_image.get_size()) #Alien hit box			
		return shot_box
	
	
################## New Stuff ################	
######		Enemy Class		######
class Enemy:
	
	def __init__(self):
		
		
		## Set enemy image ##
		
		self.image = pygame.image.load("Resources/enemy_left.png")
		self.image = pygame.transform.scale(self.image, (120,100))
		
		### get a rectangle for the enemy ##
		self.rect = self.image.get_rect()
		### random constant to determine direction of travel and spawn location ###
		self.enemy_dir = randint(0,1)
		#### Enemy Speed ###
		self.speed = randint(1,6)
		
			
	#### Make an enemy object ###		
	def make(self):
		if self.enemy_dir == 1: ### Enemy Left
			self.rect.x = screen.get_width()  #enemy x
			self.rect.y = random.randrange(screen_height)-self.image.get_height()/2	#enemy y
		elif self.enemy_dir == 0: ### Enemy Right
			self.rect.x = 0  #enemy x
			self.rect.y = random.randrange(screen_height)-self.image.get_height()/2	#enemy y
			
	#### Enemy Movement	###
	def move(self):
		if self.enemy_dir == 1: ### Enemy left
			self.rect.x -= self.speed
			self.image = pygame.image.load("Resources/enemy_left.png") #Flip image on movement
			self.image = pygame.transform.scale(self.image, (120,100))
			if -1<=self.rect.x <= 0: #If enemies leave screen reduce player health
				player.health -= 5
				
		elif self.enemy_dir == 0:	### Enemy Right
			self.rect.x += self.speed
			self.image = pygame.image.load("Resources/enemy_right.png")
			self.image = pygame.transform.scale(self.image, (120,100)) #Flip and scale image on movement
			if screen.get_width()+1>=self.rect.x >= screen.get_width():
				player.health -= 5
				
				
	## Draw Enemy	##
	def draw(self):  
		screen.blit(self.image, (self.rect.x, self.rect.y))
	
	## Enemy Hit Box ##
	def enemy_box(self):
		enemy_box = Rect( (self.rect.x, self.rect.y), self.image.get_size()) 	
		return enemy_box

################### Enemy Spawning Information ###############
#enemy_list = pygame.sprite.Group() # Create a list of the enemies
enemy_list = [] ## Empty Enemy List
enemyindex = 0	## Enemy liser index (list quantity) is zero
spawntimer = pygame.time.get_ticks() + randint(1,3)*1000 ## Timer dictating when the enemies spawn.
spawn_constant = 1 ### Variable determining enemy spawn rate
##############################################################

###		Class Asignment		###
fps = clock() ## Calling game clock fps
player = Player() ##player 
enemy = Enemy()



### Game State	###
game = False
menu = True
music.play(loops=5) ### Play music


####		Main Game Loop		####
while True:
	##### Game Start menu ####
	
	if menu == True and game == False:
		sad_playing = True # Ready game over music
		screen.blit(background,(0,0) ) #make screen background
		fps.clock_tick() ## Begin game at assigned FPS
		
		
		##### Game Start Instructions and logo ####
		
		font3 = pygame.font.SysFont("monospace", 60)
		logo = font3.render("________V2 Defense________", 1, (255,255,255))
		screen.blit(logo, (20, 60))
		
		font2 = pygame.font.SysFont("monospace", 20)
		instructions = font2.render("Press the arrow keys to steer and the space bar to fire.", 1, (255,255,255))
		screen.blit(instructions, (instructions.get_width()/4, screen.get_height()/2+instructions.get_height()))	
		
		instructions2 = font2.render("The _s_ key will take a screenshot and escape will quit.", 1, (255,255,255))
		screen.blit(instructions2, (instructions.get_width()/4, screen.get_height()/2+2*instructions.get_height()))	
		
		instructions3 = font2.render("Press the Spacebar to begin...", 1, (255,255,255))
		screen.blit(instructions3, (instructions.get_width()/2, screen.get_height()/2+8*instructions.get_height()))	
		
		pygame.display.update()
			
			
		####	 Game Menu Events	####
		for event in pygame.event.get():
			##		Quit Event		##
			if event.type == pygame.QUIT: #click on x-button to exit
				sys.exit()
			elif event.type == KEYDOWN and event.key == K_ESCAPE: #Escape key exit
				sys.exit()
			elif event.type == KEYDOWN and event.key == K_SPACE: ## Begin Game
				menu = False
				game = True
				timer = pygame.time.get_ticks() #timer for story
			elif event.type == KEYDOWN and event.key == K_s:
					pygame.image.save(screen, "screenshot.jpg")
		
		pygame.display.update()

		
	
	elif game == True and menu == False:
		
			
				
		screen.blit(background,(0,0) ) #make screen background
		fps.clock_tick() ## Begin game at assigned FPS
		
		#### Story Loop ####
		while pygame.time.get_ticks() - timer < 8000:  ### Display for 8 seconds:
			story1 = font2.render("In early September 1945, a desperate Adolf Hitler gave the order to launch", 1, (255,255,255))
			screen.blit(story1, (10, screen.get_height()/3))	
			story2 = font2.render("an unprecendented V2 rocket attack on London... ", 1, (255,255,255))
			screen.blit(story2, (10, screen.get_height()/3+story1.get_height()))
			story3 = font2.render("High over the English Channel, The 19th Squadron has been tasked with", 1, (255,255,255))
			screen.blit(story3, (10, screen.get_height()/3+4*story1.get_height()))
			story4 = font2.render("intercepting these deadly bombs and saving the people of England...", 1, (255,255,255))
			screen.blit(story4, (10, screen.get_height()/3+5*story1.get_height()))
			story5 =font2.render("Go get 'em, Ace!", 1, (255,255,255))
			screen.blit(story5, (400, screen.get_height()/3+12*story1.get_height()))
			pygame.display.update()
			
			###	Event For Loop	###
			for event in pygame.event.get():
	
				##		Quit Event		##
				if event.type == pygame.QUIT: #click on x-button to exit
					sys.exit()
				elif event.type == KEYDOWN and event.key == K_ESCAPE: #Escape key exit
					sys.exit()
				elif event.type == KEYDOWN and event.key == K_s:
					pygame.image.save(screen, "screenshot.jpg")
		
		
		
	################ Begin Game ############	
					
		###		Calling Draw Function		##
		player.draw() ## Draw player every time through while-loop
		

		###	Event For Loop	###
		for event in pygame.event.get():
	
			##		Quit Event		##
			if event.type == pygame.QUIT: #click on x-button to exit
				sys.exit()
			elif event.type == KEYDOWN and event.key == K_ESCAPE: #Escape key exit
				sys.exit()
			
			###		Player Movement		###
			
			if event.type==KEYDOWN: #key press events -- start moving
				if event.key == K_LEFT: #left key
					player.move_left()
					player.s_dir_y = 0 #Set y shot direction to 0
					player.s_dir_x = 1 #Set x shot direction to 1
					player.flip_left() #rotate player image
					
				elif event.key == K_RIGHT: #right key
					player.move_right()
					player.s_dir_y = 0 #Set y shot direction to 0
					player.s_dir_x = -1 #Set x shot direction to -1
					player.flip_right()

				elif event.key == K_UP: #up key
					player.move_up()
					player.s_dir_y = 1	#Set y shot direction to -1
					player.s_dir_x = 0 #Set x shot direction to 0
					player.flip_up()

					
				elif event.key == K_DOWN: #down key
					player.move_down()
					player.s_dir_y = -1 #Set y shot direction to 1
					player.s_dir_x = 0 #Set x shot direction to 0
					player.flip_down()
		
			#### Screen Shots	###
				elif event.key == K_s:
					pygame.image.save(screen, "screenshot.jpg")
			
			
		
			
			###		Player Missile Firing	### 
			if event.type==KEYDOWN and event.key == K_SPACE:
				player.fire()
				fire_sound.play() #play firing sound
				
				
			if event.type == KEYUP and event.key == K_SPACE:
				fire_sound.stop() ## Stop firing sound
				
				
		
		####	Enemy Spawn		###
		if pygame.time.get_ticks() >= spawntimer: ## System time exceeds the random spawn timer
			enemy_list.append(Enemy())	## Add an enemey
			enemy_list[enemyindex] = Enemy() ##Call the class
			enemy_list[enemyindex].make() 	## Make an enemy
			enemyindex = enemyindex + 1		## Add enemy to index
			spawn_constant = spawn_constant+(player.score)/1000		#reset spawn constant so it changes with score
			spawntimer = pygame.time.get_ticks() + random.uniform(0,1+10/spawn_constant)*1000 ## Reset spawn timer
			
			
	##### Drawing Enemies ####	
		i=0
		while i< len(enemy_list):		#Run through the enemy list
			if enemy_list[i] is not None: ## Check if there are enemies
				enemy_list[i].move()	#Move enemies
				enemy_list[i].draw()	#Draw
				i=i+1					#Check next member of list
		
		
		
		
		###################### 	Enemy Destroy	#####################
		shot_box = player.shot_box()	## Asign shot hot-box based on current position
		##### While loop for object collision ####
		i=0
		while i < len(enemy_list):
			#if enemy_list[i] is not None:
			if shot_box.colliderect(enemy_list[i]) and player.fired == True: #Check for collision and shots fired
				del enemy_list[i]	#Delete member of enemy list
				explode.play()
				enemyindex = len(enemy_list) #Change number of enemies in enemy index
				player.score = player.score + 100	##Increase player score
			i=i+1	#next member of enemy list
			
		
			
		####	Player Health Display	###	
		font = pygame.font.SysFont("monospace", 40)
		health = "Health: " + str(player.health)
		h_display = font.render(health, 1, (255,255,255))
		screen.blit(h_display, (h_display.get_width()/6, screen.get_height()-h_display.get_height()))
	
		
		####	Player Score Display	###	
		font = pygame.font.SysFont("monospace", 40)
		score = "Score: " + str(player.score)
		s_display = font.render(score, 1, (255,255,255))
		screen.blit(s_display, (screen.get_width()-1.5*s_display.get_width(), screen.get_height()-h_display.get_height()))
	
	
	
		### Game Over	###
		if player.health <= 0:
			game = False
			menu = False
			music.stop() ##Stop Music
		pygame.display.update()
			
### Game Over Mechanic	###
	elif game == False and menu == False:
		pygame.display.update()
		###	Event For Loop	###
		sad.play() #play game over sound
		sad_playing = True 
		for event in pygame.event.get():
	
			##		Quit Event		##
			if event.type == pygame.QUIT: #click on x-button to exit
				sys.exit()
			elif event.type == KEYDOWN and event.key == K_ESCAPE: #Escape key exit
				sys.exit()
			elif event.type == KEYDOWN and event.key == K_s:
					pygame.image.save(screen, "screenshot.jpg")
			
			##		Restart Game	##	
			elif event.type == KEYDOWN and event.key == K_RETURN: #Enter Key Restart Game
				menu = True
				game = False
				player.health = 100 #Reset Player Health
				spawntimer = pygame.time.get_ticks() + randint(1,3)*1000 ## Timer dictating when the enemies spawn.
				spawn_constant = 1 ### Variable determining enemy spawn rate
				enemy.e_modifier = 0.5 #Reset enemy speed modifer
				player.score = 0	#Reset Player Score
				sad.stop()
				sad_playing = False
				music.play() #Play music
				
				### Game Over Display	###
		font = pygame.font.SysFont("monospace", 50)
		game_over = font.render("Game Over!", 1, (255,255,255))
		screen.blit(game_over, (h_display.get_width()/2+game_over.get_height()/2, screen.get_height()/2))	
		
		font2 = pygame.font.SysFont("monospace", 20)
		continue_playing = font2.render("Press Enter to return to the main menu...", 1, (255,255,255))
		screen.blit(continue_playing, (h_display.get_width()/2+game_over.get_height()/2, screen.get_height()/2+game_over.get_height()))	
		pygame.display.update()
