from kivy.app import App
from kivy.loader import Loader
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
# from kivy.core.window import Window, Keyboard

from core.datapath import *
from core.gamemech import GameMech
from core.label import Label
from core.button import Button
from core.popup import Popup


# import cProfile
# from plyer import email
# import pstats


class GameApp(App):
	netroom = ""
	version = ""
	dialog = None  # Used to get user confirmation
	app = None
	tpopup = None

	def build(self):
		# self.title = ""
		Window.bind(on_request_close=self.on_request_close)
		Window.bind(on_keyboard=self.on_keyboard)
		self.tpopup = Popup(title="Exit", content=None, size_hint=(None, None), size=(100, 100))
		Loader.loading_image = f"atlas://{img_in}/other/grey"
		parent = Widget()  # this is an empty holder for buttons, etc
		self.app = GameMech()
		parent.add_widget(self.app)  # use this hierarchy to make it easy to deal w/buttons
		return parent

	def on_keyboard(self, window, key, *args):
		"""
		used to manage the effect of the escape key
		"""
		# to implement at a later time
		if key in ["escape", 27, 1001]:  # if keycode[1] in ["escape", 27]:
			self.textpopup()
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
	def on_request_close(self, *args):
		self.textpopup()
		return True

	def textpopup(self, title='', text=''):
		"""Open the pop-up with the name.

		:param title: title of the pop-up to open
		:type title: str
		:param text: main text of the pop-up to open
		:type text: str
		:rtype: None
		"""
		xscat = self.app.sd["card"][0] * 5
		yscat = self.app.sd["card"][1] * 2.5
		box = BoxLayout(orientation='vertical')
		box1 = BoxLayout(orientation='horizontal',size_hint=(1, 0.5))
		box.add_widget(Label(text="Are you sure?",size_hint=(1, 0.5)))
		box.add_widget(box1)
		mybutton = Button(text='Yes', size_hint=(1, 1))
		mybutton1 = Button(text='No', size_hint=(1, 1))
		box1.add_widget(mybutton)
		box1.add_widget(mybutton1)
		mybutton.bind(on_release=self.stop)
		mybutton1.bind(on_release=self.textpopup_close)
		self.tpopup.content = box
		self.tpopup.size = (xscat, yscat)
		self.tpopup.open()

	def textpopup_close(self,*args):
		self.tpopup.dismiss()
