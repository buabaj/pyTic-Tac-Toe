import kivy
import numpy
kivy.require("1.10.0")
from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.image import Image
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.config import Config
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.uix.behaviors import ButtonBehavior
import time
import random

#TODO get rid of globals where possible
global toe_box
global toe_box_ids
global glob

class globject():
	player1	    = "x"
	player1_img = "x.gif"
	cpu = "o"
	cpu_img = "o.gif"
	difficulty  = "random"
	opponent = "CPU"
	current_turn = "x"
	current_turn_img = "x.gif"
	gameOver = False

glob = globject()

def startup():
	Config.set('graphics', 'resizable', False)
	#Config.set('graphics', 'borderless', 1)
	Config.set('graphics', 'width', 800)
	Config.set('graphics', 'height', 800)
	Config.set('graphics', 'top', 50)

# Main
# Builds the kv file instead of having it separate
class Main(App):
	def build(self):
		startup()
		Builder.load_string(
"""
Container:
#Container holds all the other layouts
<Container>:
	id: contain
	orientation: "vertical"
	#pos_hint: {'center_y': 0.5, 'center_x': 0.5}
	#size_hint_y: None
	#height: 0.5625 * root.width
	StartMenu
	
#Custom Image class to prevent blurring on all images
<CustomImage>:
	Image:
		id: img
        source: root.source
        pos: root.pos
        size: root.size
		allow_stretch: True
		
#Custom class for buttons that have images
<ImageButton>:
	id: imgbtn
    source: None
    on_press: root.change_color()
    #on_press: root.click_box()
    on_release: root.reset_color()
    always_release: True
    allow_stretch: True
    
    #Helps the button on_press
    tint: 0,0,0,0
	canvas.after:
		Color:
			rgba: self.tint
		Rectangle:
			size: self.size
			pos: self.pos
    
    CustomImage:
		id: img
        source: root.source
        pos: root.pos
        size: root.size
		allow_stretch: True
	
<StartMenu>:
	orientation: "vertical"
	Label:
		text: "Tic Tac Toe"
	BoxLayout:
		orientation: "horizontal"
		Button:
			text: "CPU : Impossible"
			on_press: root.goto_xoro("impossible")
		Button:
			text: "CPU : Good"
			on_press: root.goto_xoro("good")
	BoxLayout:
		orientation: "horizontal"
		Button:
			text: "CPU : Plays Randomly"
			on_press: root.goto_xoro("random")
		Button:
			text: "CPU : Trying to Lose"
			on_press: root.goto_xoro("loser")
	Button:
		text: "2 Player"
		on_press: root.goto_2player("2player")
	Button:
		text: "Exit"
		on_press: root.quit_game()
		
<TicTacToe>:
	id: tictactoe
	BoxLayout:
		orientation: "vertical"
		BoxLayout:
			orientation: "horizontal"
			ImageButton:
				id: A1
				source: "blank.gif"	
				on_press: root.clicked([0,0], "A1")
			ImageButton:
				id: A2
				source: "blank.gif"	
				on_press: root.clicked([0,1], "A2")
			ImageButton:
				id: A3
				source: "blank.gif"
				on_press: root.clicked([0,2], "A3")
					
		BoxLayout:
			orientation: "horizontal"
			ImageButton:
				id: B1
				source: "blank.gif"
				on_press: root.clicked([1,0], "B1")	
			ImageButton:
				id: B2
				source: "blank.gif"
				on_press: root.clicked([1,1], "B2")
			ImageButton:
				id: B3
				source: "blank.gif"
				on_press: root.clicked([1,2], "B3")
					
		BoxLayout:
			orientation: "horizontal"
			ImageButton:
				id: C1
				source: "blank.gif"
				on_press: root.clicked([2,0], "C1")		
			ImageButton:
				id: C2
				source: "blank.gif"
				on_press: root.clicked([2,1], "C2")
			ImageButton:
				id: C3
				source: "blank.gif"	
				on_press: root.clicked([2,2], "C3")
				
<XorOScreen>:
	id: xoroscreen
	orientation: "vertical"
	BoxLayout:
		ImageButton:
			id: x
			source: "x.gif"
			on_press: root.choose_x()
		ImageButton:
			id: o
			source: "o.gif"	
			on_press: root.choose_o()
	Label:
		text: "Would you like to play as X's or O's?"
				
<EndGameScreen>:
	id: endgamescreen
	Label:
		id: backgroundcolorbox
		size_hint_y: 0.2
		pos_hint: {'x': 0, 'center_y': 0.5}
		bcolor: 0,0,0,1
		canvas.before:
			Color:
				rgba: self.bcolor
			Rectangle:
				pos: self.pos
				size: self.size
				
	BoxLayout:
		orientation: "vertical"
		size_hint_y: 0.2
		pos_hint:{'x':0, 'center_y':.5}
		Label:
			id: winlosetext
			bcolor: 0,0,0,1
			canvas.before:
				Color:
					rgba: self.bcolor
				Rectangle:
					pos: self.pos
					size: self.size
			text: "Game over"
		BoxLayout:
			orientation: "horizontal"
			Button:
				text: "Main Menu"
				on_press: root.goto_start_menu()
			Button:
				text: "Restart"
				on_press: root.restart_game()
""")
		global root
		root = Container()
		return root

class CustomImage(Image):
	def __init__(self, *args, **kwargs):
		Image.__init__(self, *args, **kwargs)
		self.bind(texture=self._update_texture_filters)

	def _update_texture_filters(self, image, texture):
		texture.mag_filter = 'nearest'
	
class ImageButton(ButtonBehavior, Image):	
	#def __init__(self, *args, **kwargs):
	#	super(ImageButton, self).__init__(**kwargs)

	def change_color(self):
		self.tint = 0,0,0,0.2
		
	def reset_color(self):
		self.tint = 0,0,0,0

# The primary gui container that holds all the other gui pieces
class Container(BoxLayout):
	pass
	
class CPU():
	def __init__(self, *args, **kwargs):
		global toe_box
		global toe_box_ids

# The first menu the user sees
class StartMenu(BoxLayout):
	def __init__(self, **kwargs):
		super(StartMenu, self).__init__(**kwargs)
	def goto_xoro(self, difficulty):
		glob.difficulty = difficulty
		root.clear_widgets()
		root.add_widget(XorOScreen())
	def quit_game(self):
		App.get_running_app().stop()
		
class EndGameScreen(FloatLayout):
	def goto_start_menu(self):
		root.clear_widgets()
		root.add_widget(StartMenu())
	def restart_game(self):
		root.clear_widgets()
		root.add_widget(TicTacToe())

# The first menu the user sees
class TicTacToe(FloatLayout):	
	def __init__(self, **kwargs):
		super(TicTacToe, self).__init__(**kwargs)
		global toe_box
		global toe_box_ids
		global difficulty
		toe_box = [ ["","",""],
					["","",""],
					["","",""]] # The array of the tic tac toe box
		toe_box_ids = [ ["A1","A2","A3"],
						["B1","B2","B3"],
						["C1","C2","C3"]] #The ids of the tic tac toe squares
		self.turn = 1
		glob.current_turn = "x"
		glob.current_turn_img = "x.gif"
		glob.gameOver = False
	
	def run_random(self):
		open_spaces = []
		for i in range(3):
			for j in range(3):
				if toe_box[i][j] == "":
					open_spaces.append([i,j])
		if open_spaces != []:
			rando = random.randint(0,len(open_spaces)-1)
			self.play(open_spaces[rando])
		
	#Runs the cpu by difficulty, if 2 player mode is selected then the cpu does not make a move
	def run_cpu_turn(self):
		if glob.difficulty == "impossible":
			self.run_impossible()
		elif glob.difficulty == "good":
			self.run_good()
		elif glob.difficulty == "random":
			self.run_random()
		elif glob.difficulty == "loser":
			self.run_loser()
	
	def change_turn(self):
		if glob.current_turn == "x":
			glob.current_turn = "o"
			glob.current_turn_img = "o.gif"
		else:
			glob.current_turn = "x"
			glob.current_turn_img = "x.gif"
	
	#TODO Fix the location so it looks like [i][j] instead of (i,j), you'll have to scour the code for this
	def play(self, location): #loc = location, imgid = image id
		a = location[0]
		b = location[1]
		img_id = toe_box_ids[a][b]
		toe_box[a][b] = glob.current_turn
		self.ids[img_id].source = glob.current_turn_img
		self.turn += 1
		if self.checkIfWon() == True:
			pass
		elif self.checkIfWon() == False:
			if self.turn == 10:
				self.endGame("It's a tie!")
			else:
				self.change_turn()
				if glob.opponent == "CPU" and glob.current_turn != glob.player1:
						self.run_cpu_turn()

	def clicked(self, location, box_id):
		x = location[0]
		y = location[1]
		if toe_box[x][y] == "" and glob.gameOver == False: #if the square is empty and the game hasn't ended
			self.play(location)
	
	#Checks to see if either player has won the game
	def checkIfWon(self):
		who = "x"
		z = 2
		
		while z > 0:
			#Check for horizontal wins
			for i in range(3):
				if toe_box[i][0] == who and toe_box[i][1] == who and toe_box[i][2] == who:
					self.endGame(who.upper() + " Wins!" )
					glob.gameOver = True
					return True
			
			#Check for vertical wins
			for j in range(3):
				if toe_box[0][j] == who and toe_box[1][j] == who and toe_box[2][j] == who:
					self.endGame(who.upper() + " Wins!" )
					glob.gameOver = True
					return True
					
			#Check for Top to Bottom diagonal wins
			if toe_box[0][0] == who and toe_box[1][1] == who and toe_box[2][2] == who:
				self.endGame(who.upper() + " Wins!" )
				glob.gameOver = True
				return True
				
			#Check for Bottom to Top diagonal wins
			if toe_box[0][2] == who and toe_box[1][1] == who and toe_box[2][0] == who:
				self.endGame(who.upper() + " Wins!" )
				glob.gameOver = True
				return True
			
			who = "o"
			z -= 1
		return False
	
	def endGame(self, outcome):
		e = EndGameScreen()
		e.ids["winlosetext"].text = outcome
		self.add_widget(e)
	
	def goto_start_menu(self):
		root.clear_widgets()
		root.add_widget(StartMenu())
	
	def check_if_row_closed(self, row):
		if player1 in ([row][0],[row][1],[row][2]):
			return True
		else:
			return False
		
	def check_if_col_closed(self, col):
		if player1 in ([0][col],[1][col],[2][col]):
			return True
		else:
			return False
	
	#start_pos is the left most square to test from, 0 tests from top to bottom, 2 tests from bottom to top
	def check_if_diag_closed(self, start_pos):
		if start_pos == 0:
			if player1 in ([0][0], [1][1], [2][2]):
				return True
			else:
				return False
		elif start_pos == 2:
			if player1 in ([2][0], [1][1], [0][2]):
				return True
			else:
				return False


	# TODO FIX THIS MESS!!!!!!!!!!!!!!!!!!!!
	def test_for_wins(self, test_locs): #test_locs must have 3 locations for this to work
		blank_spots = 0
		blank_loc = [0][0]
		a = [0,0,0]
		a[0] = toe_box[test_locs[0][0]] [test_locs[0][1]]
		a[1] = toe_box[test_locs[1][0]] [test_locs[1][1]]
		a[2] = toe_box[test_locs[2][0]] [test_locs[2][1]]
		
		if glob.player1 not in (a[0],a[1],a[2]): #if the player is not blocking
			blank_spots = 0
			for i in range(3):
				if a[i] == "":
					blank_spots += 1
					blank_loc = (test_locs[i])
				
		if blank_spots == 1:
			self.play(blank_loc)
			return True
					
	#The CPU looks to see if it can play any moves to win the game
	def look_for_winning_moves(self):
		if glob.gameOver == False:
			#look for wins in the rows
			for i in range(3):
				if self.test_for_wins( ((i,0),(i,1),(i,2)) ) == True:
					return True
					
			#look for wins in the columns
			for i in range(3):
				if self.test_for_wins( ((0,i),(1,i),(2,i)) ) == True:
					return True
			
			#look for wins in the top to bottom diagonal
			for i in range(3):
				if self.test_for_wins( ((0,0),(1,1),(2,2)) ) == True:
					return True

			#look for wins in the bottom to top diagonal
			for i in range(3):
				if self.test_for_wins( ((2,0),(1,1),(0,2)) ) == True:
					return True
			return False
				
	#TODO Create the good CPU
	def run_good(self):
		if self.look_for_winning_moves() == False:
			self.run_random()
	
	# TODO Create the impossible CPU
	def run_impossible(self):
		self.run_random()
		self.check_if_diags_closed([0][0])
	
class XorOScreen(BoxLayout):
	def choose_x(self):
		glob.player1 = "x"
		glob.player1_img = "x.gif"
		glob.cpu = "o"
		root.clear_widgets()
		root.add_widget(TicTacToe())
	def choose_o(self):
		glob.player1 = "o"
		glob.player1_img = "o.gif"
		glob.cpu = "x"
		root.clear_widgets()
		root.add_widget(TicTacToe())

# Runs the program	
if __name__ == '__main__':
	Main().run()