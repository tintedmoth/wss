from kivy.uix.textinput import TextInput as Ti
import re
from core.datapath import *
class TextInput(Ti):
	cid = ""
	def __init__(self, cid="", **kwargs):
		super(TextInput, self).__init__(**kwargs)
		self.cid = cid
		self.font_name = f"{font_in}/{font}"
		self.multiline = False
		self.padding = [12,6,6,6]
		self.bind(size=self._update_rect)
	def _update_rect(self, inst, value):
		self.height = inst.size[1]
		self.width = inst.size[0]
