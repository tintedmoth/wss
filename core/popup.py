from kivy.uix.popup import Popup as Pop

from core.datapath import *


class Popup(Pop):
	cid = ""

	def __init__(self, **kwargs):
		super(Popup, self).__init__(**kwargs)
		self.title_font = f"{font_in}/{font}"
		self.title_align = "center"
		self.auto_dismiss = False
		self.size_hint = (None, None)
