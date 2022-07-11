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

# class DigitInput(TextInput):
# 	pat = re.compile('[^0-9]')
# 	def insert_text(self, substring, from_undo=False):
# 		pat = self.pat
# 		s = re.sub(pat, '', substring)
# 		return super().insert_text(s, from_undo=from_undo)
