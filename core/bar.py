from kivy.graphics import Rectangle
from kivy.uix.relativelayout import RelativeLayout

from core.datapath import *


class Bar(RelativeLayout):
	def __init__(self, **kwargs):
		super(Bar, self).__init__(**kwargs)
		self.size_hint = (None, None)

		with self.canvas:
			self.img = f"atlas://{img_in}/other/bar_k"
			self.rect = Rectangle(source=self.img, pos=self.pos, size=self.size)
