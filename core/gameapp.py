from kivy.app import App
from kivy.loader import Loader
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

from core.datapath import *
from core.gamemech import GameMech
from core.label import Label
from core.button import Button
from core.popup import Popup
from core.settings import ESettingsPanel




class GameApp(App):
	netroom = ""
	version = ""
	dialog = None  
	app = None
	tpopup = None
	settings_popup = None
	default_settings = {'show_wait_popup': True, 'overlap_confirm': True, "confirm_requirement": True, "show_counter_popup": True, "DLimg": False, "HDimg": False}

	def build(self):
		self.title = "WSS"
		self.settings_cls = ESettingsPanel

		Window.bind(on_request_close=self.on_request_close)
		Window.bind(on_keyboard=self.on_keyboard)
		self.tpopup = Popup(title="", separator_height=0, content=None, size_hint=(None, None), size=(100, 100))
		Loader.loading_image = f"atlas://{img_in}/other/grey"
		parent = Widget()  
		self.app = GameMech()
		parent.add_widget(self.app)  
		return parent

	def btn_open_settings(self, *args):
		self.open_settings()

	def build_config(self, config):
		"""
		Set the default values for the configs sections.
		"""
		config.setdefaults('Settings', self.default_settings)
		config.write()

	def build_settings(self, settings):
		"""
		Add our custom section to the default configuration object.
		"""
		settings.add_json_panel('Settings', self.config, join(data_in, "sdata.db"))

	def on_keyboard(self, window, key, *args):
		"""
		used to manage the effect of the escape key
		"""
		if key in ["escape", 27, 1001]:  
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


	def on_stop(self):
		pass


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
		box1 = BoxLayout(orientation='horizontal', size_hint=(1, 0.4), padding=self.app.sd["padding"])
		box.add_widget(Label(text="Close the application?\n ", size_hint=(1, 0.6), halign="center", valign="middle"))
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

	def textpopup_close(self, *args):
		self.tpopup.dismiss()

	def display_settings(self, settings):
		try:
			p = self.settings_popup
			if not p:
				raise AttributeError
		except AttributeError:
			self.settings_popup = Popup(content=settings, title="", separator_height=0, size_hint=(0.8, 0.8))
			p = self.settings_popup
		if not p or p.content is not settings:
			p.content = settings
		p.open()

	def close_settings(self, *args):
		self.app.update_gdata_config()
		try:
			p = self.settings_popup
			p.dismiss()
		except AttributeError:
			pass  
