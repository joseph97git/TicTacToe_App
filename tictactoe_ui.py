"""
	File name: tictactoe_ui.py
	Author: Joseph Kim
	Date created: 6/15/18
	Date last modified: 7/4/18
	Python Version: 3.6.6
"""

# import packages
from kivy.app import App 
from kivy.uix.button import Button 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout   
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from kivy.config import Config
from kivy.clock import Clock


# set window size
Config.set("graphics", "width", "446")
Config.set("graphics", "height", "600")
Config.set("graphics", "resizable", False) # prevent resizing 


class TicTacToeApp(App):
	"""This class defines the user interface for the game of Tic-tac-toe. \
	It also includes the functionality to play against the computer."""
	

	def build(self):
		"""Initializes the application."""
		return Board()



class Board(FloatLayout):
	"""This class defines the board to play Tic-tac-toe and also includes \
	the additional features of reseting the board and playing against the \
	computer."""

	# initialize board attributes
	state = ListProperty([0, 0, 0, 0, 0, 0, 0, 0, 0])
	player = ListProperty(["O", "X"])
	color = ListProperty([[1, 0.843, 0, 1], [0.753, 0.753, 0.753, 1]])
	turn = NumericProperty(1)
	turn_label = Label(text="[color=000000]Player O to Move[/color]",
					   font_size="30", pos_hint={"x": 0, "center_y": 0.95},
					   markup=True)

	def __init__(self, *args, **kwargs):
		"""Initialize the GUI that the user interacts with in order to play \
		a game of Tic-tac-toe."""

		super(Board, self).__init__(*args, **kwargs)

		# background colors
		with self.canvas.before:
			Color(1, 1, 1, 1) # white for root background  
			Rectangle(pos=(0, 0), size=(450, 600))
			Color(0, 0, 0, 1) # black for board lines
			Rectangle(pos=(0, 98), size=(450, 452))

		# turn label 
		self.add_widget(self.turn_label)

		# add individual board squares
		square_id = 1 # id board squares
		for col in [400, 248, 96]:
			for row in [0, 150, 300]:
				square = Square(pos=(row, col), size_hint=(0.33, 0.25),
								name=square_id, font_size="150",
								background_color=(0, 1, 1, 1))
				square.bind(on_press=self.square_press) 
				self.add_widget(square)
				square_id = square_id + 1 # update id

		# add computer button
		comp_button = Button(text="[color=000000]Play Computer[/color]",
							   font_size="20", pos=(0, 45),
							   size_hint=(1, 0.084), markup=True)
		self.add_widget(comp_button)

		# add reset button
		reset_button = Button(text="[color=000000]Reset[/color]",
							   font_size="20", pos=(0, 0),
							   size_hint=(1, 0.075), markup=True)
		reset_button.bind(on_release=self.reset)
		self.add_widget(reset_button)


	def is_winner(self):
		"""Determines if there is a winner of the game.
		Returns: 
			True, if there is a winner and False if not.
		"""
		sums_state = [sum(self.state[0:3]), sum(self.state[3:6]), 
					  sum(self.state[6:9]), sum(self.state[0::3]), 
					  sum(self.state[1::3]), sum(self.state[2::3]), 
					  sum(self.state[0::4]), sum(self.state[6::-2])]
		if 3 in sums_state or -3 in sums_state:
			return True
		return False


	def is_tie(self):
		"""Determines if the game is a tie.
		Returns:
			True, if there is a tie and False if not
		"""
		if 0 not in self.state:
			return True
		return False


	def square_press(self, square):
		"""Updates the board state, sqaure status, turn, and turn_label
		based on the square that was pressed.
		Args:
			square: the board square that was just clicked on.
		"""
		if square.status == 0:
			square.status = 1
			self.turn = -1 * self.turn
			index = int((self.turn + 1) / 2)
			square.text = self.player[index]
			square.color = self.color[index]
			self.state[square.name - 1] = self.turn	
			if self.is_winner():
				self.turn_label.text = "[color=000000]Player " + \
										self.player[index] + " Wins![/color]"
				for child in list(self.children):
					if type(child) == Square:
						child.disabled = True
				Clock.schedule_once(self.reset, 3)
			elif self.is_tie():
				self.turn_label.text = "[color=000000]It's a Tie![/color]"
				Clock.schedule_once(self.reset, 3)
			else:
				self.turn_label.text = "[color=000000]Player " + \
								   		self.player[-1 *index + 1] + \
								   		" to Move[/color]"
			print(self.state)


	def reset(self, *args):
		"""Resets the state of the game to the inital state.
		Args: 
			*args: accepts more than one argument.
		"""

		# reset attributes
		self.state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.turn = 1
		self.win = 0
		self.turn_label.text= "[color=000000]Player O to Move[/color]"
		# reset squares
		for child in list(self.children):
			if type(child) == Square:
				child.disabled = False
				child.text = ""
				child.status = 0


class Square(Button):
	"""This class defines a board square and has data fields to help keep \
	track of the board state.
	"""
	name = NumericProperty(0)
	status = NumericProperty(0)


if __name__ == '__main__':
	TicTacToeApp().run()