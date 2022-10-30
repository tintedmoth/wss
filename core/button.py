from kivy.uix.button import Button as Bu
from core.datapath import *
class Button(Bu):
	cid = ""
	def __init__(self, cid="", **kwargs):
		super(Button, self).__init__(**kwargs)
		self.cid = cid
		self.font_name = f"{font_in}/{font}"
