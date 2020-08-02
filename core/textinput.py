from kivy.uix.textinput import TextInput as Ti

from core.datapath import *


class TextInput(Ti):
	cid = ""

	def __init__(self, cid="", **kwargs):
		super(TextInput, self).__init__(**kwargs)
		self.cid = cid
		self.font_name = f"{font_in}/{font}"
