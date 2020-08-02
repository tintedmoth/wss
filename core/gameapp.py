from kivy.app import App
from kivy.loader import Loader
from kivy.uix.widget import Widget
# import cProfile
# from plyer import email
# import pstats

from core.datapath import *
from core.gamemech import GameMech


class GameApp(App):
	netroom = ""
	version = ""

	def build(self):
		# self.title = ""
		Loader.loading_image = f"atlas://{img_in}/other/grey"
		parent = Widget()  # this is an empty holder for buttons, etc
		app = GameMech()
		parent.add_widget(app)  # use this hierarchy to make it easy to deal w/buttons
		return parent

	def on_keyboard(self, window, key, scancode=None, codepoint=None, modifier=None):
		"""
		used to manage the effect of the escape key
		"""
		# to implement at a later time
		if key == 27:
			#
			# 	if self.gm.current == 'main':
			# 		return False
			# 	# elif self.gm.current == 'host_game':
			# 	# 	self.gm.current = 'main'
			# 	# elif self.gm.current == 'host_wait':
			# 	# 	self.gm.stop_server();
			# 	# 	self.gm.current = 'main'
			# 	# elif self.gm.current == 'join_game':
			# 	# 	self.gm.stop_server();
			# 	# 	self.gm.current = 'main'
			# 	elif self.gm.current == 'game':
			# 		self.gm.current = 'pause'
			# 	elif self.gm.current == 'pause':
			# 		self.gm.current = 'game'
			return True
		return False

	def on_pause(self):
		"""
		trap on_pause to keep the app alive on android
		"""
		return True

	def on_resume(self):
		pass

	# def on_start(self):
		# self.profile = cProfile.Profile()
		# self.profile.enable()

	def on_stop(self):
		pass
		# self.profile.disable()
		# self.profile.dump_stats('myapp.profile')
		#
		# with open('myapp.profile.txt', 'w') as stream:
		# 	stats = pstats.Stats('myapp.profile', stream=stream)
		# 	stats.print_stats()
		#
		# with open("myapp.profile.txt", "r") as stream:
		# 	pp = ""
		# 	for line in stream.readlines():
		# 		pp += line
		# email.send(recipient="tsws@totuccio.com", subject="", text=pp, create_chooser=False)