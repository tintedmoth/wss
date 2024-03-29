from kivy.core.text import Label as Ct
from kivy.uix.label import Label as Lo

from core.datapath import *


class Label(Lo):
	def __init__(self, **kwargs):
		super(Label, self).__init__(**kwargs)
		self.font_name = f"{font_in}/{font}"


class CoreLabel(Ct):
	def __init__(self, **kwargs):
		super(CoreLabel, self).__init__(**kwargs)
		self.font_name = f"{font_in}/{font}"
