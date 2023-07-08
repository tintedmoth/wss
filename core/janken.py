from kivy.graphics import PopMatrix
from kivy.graphics import PushMatrix
from kivy.graphics import Rectangle
from kivy.graphics import Rotate

from core.button import Button
from core.datapath import *


class Janken(Button):
	def __init__(self, ncard, size, **kwargs):
		super(Janken, self).__init__(**kwargs)
		self.font_name = f"{font_in}/{font}"
		self.cid = ncard
		self.card = ncard
		self.back = False
		self.size_hint = (None, None)
		self.size = size
		self.center = (self.size[0] / 2, self.size[1] / 2)
		self.height = self.size[1]
		self.width = self.size[0]
		self.img_card = f"atlas://{img_in}/other/{self.card}"
		self.img_back = f"atlas://{img_in}/other/back"
		self.angle = 0

		with self.canvas.after:
			PushMatrix()
			self.rotation = Rotate(angle=self.angle, origin=self.center)
			self.rect = Rectangle(source=self.img_back, pos=self.pos, size=self.size)
			PopMatrix()
		self.bind(size=self._update_rect, pos=self._update_rect)

	def _update_rect(self, inst, value):
		self.rect.pos = inst.pos
		self.rect.size = inst.size
		self.rotation.origin = (self.rect.pos[0] + self.rect.size[0] / 2, self.rect.pos[1] + self.rect.size[1] / 2)
		self.height = inst.size[1]

	def show_back(self):
		self.back = True
		with self.canvas:
			self.rect.source = self.img_back

	def show_front(self):
		self.back = False
		with self.canvas:
			self.rect.source = self.img_card

	def reverse(self):
		self.rotation.angle = 180

	def stand(self):
		self.rotation.angle = 0
