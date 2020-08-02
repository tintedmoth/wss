from kivy.core.text import Label as CL
from kivy.uix.image import Image
from kivy.uix.label import Label as Lo

from core.datapath import *


class Label(Lo):
	def __init__(self, **kwargs):
		super(Label, self).__init__(**kwargs)
		self.font_name = f"{font_in}/{font}"


class CoreLabel(CL):
	def __init__(self, **kwargs):
		super(CoreLabel, self).__init__(**kwargs)
		self.font_name = f"{font_in}/{font}"


class Joketext(Image):
	text = ""

	def on_text(self, instance, text):
		# Just get large texture:
		l = Label(text=self.text, color=(1, 1, 1, 1), outline_width=5, halign="center", valing="center")
		l.font_size = "500dp"  # something that'll give texture bigger than phone's screen size
		l.texture_update()
		# Set it to image, it'll be scaled to image size automatically:
		self.texture = l.texture
