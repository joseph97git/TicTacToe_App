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


# set window size
Config.set("graphics", "width", "446")
Config.set("graphics", "height", "600")
Config.set("graphics", "resizable", False)


class TicTacToeApp(App):
	def build(self):
		return Board()



class Board(FloatLayout):
	state = ListProperty([0, 0, 0, 0, 0, 0, 0, 0, 0])
	player = ListProperty(["O", "X"])
	color = ListProperty([[1, 0.843, 0, 1], [0.753, 0.753, 0.753, 1]])
	turn = NumericProperty(1)
	turn_label = Label(text="[color=000000]Player O to Move[/color]",
					   font_size="20", pos_hint={"x": 0, "center_y": 0.95},
					   markup=True)

	def __init__(self, *args, **kwargs):
		super(Board, self).__init__(*args, **kwargs)

		# background color
		with self.canvas.before:
			Color(1, 1, 1, 1)
			Rectangle(pos=(0, 0), size=(450, 600))
			Color(0, 0, 0, 1)
			Rectangle(pos=(0, 98), size=(450, 452))

		# add turn label 
		self.add_widget(self.turn_label)

		# individual board squares
		square_id = 1
		for col in [400, 248, 96]:
			for row in [0, 150, 300]:
				square = Square(pos=(row, col), size_hint=(0.33, 0.25),
								name=square_id, font_size="150",
								background_color=(0, 1, 1, 1))
				square.bind(on_release=self.square_press)
				self.add_widget(square)
				square_id = square_id + 1

		# play computer button
		self.add_widget(Button(text="[color=000000]Play Computer[/color]",
							   font_size="20", pos=(0, 45),
							   size_hint=(1, 0.084), markup=True))

		# reset button
		self.add_widget(Button(text="[color=000000]Reset[/color]",
							   font_size="20", pos=(0, 0),
							   size_hint=(1, 0.075), markup=True))


	def square_press(self, square):
		if square.status == 0:
			square.status = 1
			self.turn = -1 * self.turn
			index = int((self.turn + 1) / 2)
			square.text = self.player[index]
			square.color = self.color[index]
			self.turn_label.text = "[color=000000]Player " + \
								   self.player[-1 *index + 1] + \
								   " to Move[/color]"
			self.state[square.name - 1] = square.status
			print(self.state)



class Square(Button):
	name = NumericProperty(0)
	status = NumericProperty(0)


if __name__ == '__main__':
	TicTacToeApp().run()