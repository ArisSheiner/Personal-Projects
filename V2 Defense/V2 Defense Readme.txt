
This is a game that I entered into the Intro-to-Computer-Science game-design competition at the University of Colorado at Boulder in 2013 when I was beginning to learn Python.
It won the intermediate category. 

I've come a long way since then, but this represents my early learning experience with Python. The game isn't perfect, but it's still fun to play -- even though there is a way to never lose. 

                              ___________________
_____________________________/ V2 Defense Readme \_____________________________________________________

Author: 	Aris Sheiner
Date: 		10/16/2013
Class: 		CSCI 1300
TA:			Dana Hughes
Level:		Beginner -- No prior programming experience



-------------------- Note: If python can't find the game files, try putting them in the home folder or opening the .py with Geany -----------------------------------------------------------------------------



			--------- Credits ---------
	

Main Music -------------------- unknown author
Imperial March 8bit ----------- unkown author
Other Sounds ------------------ SoundBible.com



			--------- Game Summary ---------


	V2 Defense is a game where the player controls a fighter craft sprite and uses its guns to destroy incoming enemy V2 rockets. 
	The rockets enter from both the left and right side of the screen and traverse it accordingly. The player must stear the aircraft into position using the arrow keys and then use the space bar to fire the plane's guns and kil the rockets before they reach the opposite side of the screen from which they entered.
	The player gains 100 points for every rocket killed. If 20 rockets cross the screen, the game is over. The player cannot win, only exceed his or her high score.

	



			--------- Controls ---------

	---- Main Menu ----
space bar:	 Start the game
escape key:	 Quit the game
s key:		 Take a screen shot

	---- Playing the Game ----
Arrow keys:	 Move the aircraft
Space bar:	 Fire aircraft guns
s key:		 Take a screen shot
escape key:	 Quit the game


	---- Game Over Menu ----
Enter key:	 Return to main menu
escape key:	 Quit the game
s key:		 Take a screen shot




			--------- Code Run-Through ---------


	First I import important packages and initialize the pygame package.  I then set the screen size and create a screen. Then I import a background image and resize it. Then I set important cursor and keyboard settings such as making the mouse invisible and allowing key holds to repeat inputs.
	Next comes the music -- imported and volume set.

	Now I make the classes.

	The first one is the clock. It's important because it keeps the game running at a good speed regardless of hardware.

	Next is the player and "gun bullet" class. Initial settings make sure that all variables are blank. This isn't super important but I wanted to make sure that I didn't reuse anything in this monstrous code. I define a "constructor" or "initialization function" to set all the variables to what I want them to be, such as giving the player sprite an image and setting the health to 100%. I also define a whole bunch of important functions that are vital to the functioning of the player -- like telling python how to draw it, how it moves and how it behaves when it shoots a missile.

	One of the biggest mistakes that I made while programming this was having the player missile class be part of the player class. This leads to a really annoying problem that I had to solve by using a thread and two separate functions -- one for firing the missile and the other for the missile while it's flying.

	Now here's where I started to get the hang of this whole class-thing. The enemy class was actually the last thing to get made. I had another one that didn't work very well and wouldn't spawn multiple enemies on screen at a time...  So, I decided to take a lesson on object-oriented programming and remake my enemy class from scratch about fifteen times while marathoning YouTube tutorials. I basically do the same thing as I did with the player -- set variables and define important functions that describe enemy behavior.

	The classes have all been made so now it's important to define some more variables that will help us make everything work how we want it to. Of note are the enemy variables where we lay the groundwork for being able to spawn multiple ones by creating a list to put them in. I also created some variables to govern the enemy spawn rate based on the current game clock time. The game state variables are what determine whether we're playing the game or on a menu screen.

	Now for the main game loop. It's a while loop that just runs until we quit the game -- as is standard for pygame stuff and presumably other programs as well. Because menu is true and game is false, we start on the main menu screen. It gives instructions etc. Key press events are defined in a for loop. 

	Next, the player hits space and game is set to true and menu to false so that the game begins. This takes the player to a screen governed by a while loop that will last for 15 seconds and tells the player the game story... Which is more or less just some bad historical fiction.

	After 15 seconds is up, the game begins. Key press events are defined (arrow keys etc.) and enemies enter from the left and right sides of the screen. The enemy spawn rate is governed by an if loop in which a spawn timer will psudeo-randomly be exceeded by the game clock. In this event, the enemy list is appended to add in a new enemy, the enemy class is called and an enemy is 'made.' Next the constant that determines the enemy spawn rate is increased according to player score. 
	
	Enemies are drawn and given movement using another if loop that cycles through the list of enemies and assigns them each behavior according to the enemy move and draw functions that we made in the enemy class above.


	Now for the enemy destroy loop. This guy was nothing but trouble. First a hit_box is determined for the player's missile. Next the code goes through yet another if loop to check each enemy. If the missile's box is detected to collide with an enemy's, that enemy is removed from the list of enemies and thus deleted from the game. Next the player score is increased and a sound is played.

	All of the vitally important game code is done and the rest is just the player health display, player score display, and game over displays. All of which are just simple pygame text displays. In the event that the player score is 0, the game ends by setting game and menu equal to false. The game over mechanic then starts and displays a "Game over" message and defines key presses such that the player may restart the game. In the event that the player chooses to do so, health is set to 100%, the score to 0, other variables to defaults and the game returns to the main menu. 


I hope that was clear enough.





			--------- Known Bugs ---------

 ----- Missile/Bullet follows player movement while spawned. Semi-fixed by just making it go super fast but I really should have made it its own class.

 ----- Screen shot doesn't capture enemies or counters.

 ----- Player can fly off the screen. This is an easy bug to fix but I didn't think it was of immediate concern.

 ----- Undestroyed rockets do not always cause a score hit.


