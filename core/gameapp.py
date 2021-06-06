from kivy.app import App
from kivy.loader import Loader
from kivy.uix.widget import Widget

from core.datapath import *
from core.gamemech import GameMech

class GameApp(App):
	netroom = ""
	version = ""

	def build(self):
		Loader.loading_image = f"atlas://{img_in}/other/grey"
		parent = Widget()
		app = GameMech()
		parent.add_widget(app)
		return parent

	def on_keyboard(self, window, key, scancode=None, codepoint=None, modifier=None):
		if key == 27:
			return True
		return False

	def on_pause(self):
		return True

	def on_resume(self):
		pass

	def on_stop(self):
		pass
