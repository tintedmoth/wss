from kivy.uix.image import Image
from kivy.graphics import Rectangle

from core.datapath import *
from core.label import Label


class Joketext(Image):
	def __init__(self, **kwargs):
		super(Image, self).__init__(**kwargs)
		self.size_hint = (None, None)
		self.blank = f"atlas://{img_in}/other/blank"
		self.img_src = f"atlas://{img_in}/other/blank"

		self.joke = Label(text="")
		self.joke.color=(1,1,1,1)
		self.joke.outline_width=5
		self.joke.halign="center"
		self.joke.valing="center"

		with self.canvas.before:
			self.rect = Rectangle(source=self.img_src, pos=self.pos, size=self.size)
		self.bind(size=self._update_rect, pos=self._update_rect)

	def _update_rect(self, inst, value):
		self.rect.pos = inst.pos
		self.rect.size = inst.size
		self.height = inst.size[1]


	def change_texture(self,text):
		self.joke.text = text
		self.joke.font_size = int(self.joke.size[1]/2)
		self.joke.texture_update()
		self.texture = self.joke.texture
