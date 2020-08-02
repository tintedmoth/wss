from kivy.uix.spinner import Spinner as Sp

from core.datapath import *


class Spinner(Sp):
	cid = ""

	def __init__(self, cid="", **kwargs):
		super(Spinner, self).__init__(**kwargs)
		self.cid = cid
		self.font_name = f"{font_in}/{font}"
