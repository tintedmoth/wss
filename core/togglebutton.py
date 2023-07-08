from kivy.uix.togglebutton import ToggleButton as Bu

from core.datapath import *


class ToggleButton(Bu):
	cid = ""

	def __init__(self, cid="", **kwargs):
		super(ToggleButton, self).__init__(**kwargs)
		self.cid = cid
		self.font_name = f"{font_in}/{font}"
