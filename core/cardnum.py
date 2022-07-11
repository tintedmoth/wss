from kivy.graphics import Rectangle

from core.button import Button
from core.label import CoreLabel
from core.datapath import *


class CardNum(Button):
	def __init__(self, card, size, **kwargs):
		super(CardNum, self).__init__(**kwargs)
		self.font_name = f"{font_in}/{font}"
		self.cid = card
		self.back = False
		self.size_hint = (None, None)
		self.size = size
		self.center = (self.size[0] / 2, self.size[1] / 2)
		self.height = self.size[1]
		self.width = self.size[0]
		self.img_card = f"atlas://{img_in}/other/grey"
		self.img_back = f"atlas://{img_in}/other/back"

		with self.canvas.after:
			self.rect = Rectangle(source=self.img_card, pos=(0, 0), size=self.size)
			self.text_l = CoreLabel(text="", text_size=self.size, color=(1, 1, 1, 1), outline_width=2, halign='center', valign='middle', font_size=self.size[0] * .6)
			self.text_l.refresh()
			self.text_r = Rectangle(texture=self.text_l.texture, size=self.size, pos=(0, 0))

		self.bind(size=self._update_rect, pos=self._update_rect)
		self.update_text(t=card)

	def _update_rect(self, inst, lue):
		self.rect.pos = inst.pos
		self.rect.size = inst.size
		self.text_r.pos = inst.pos
		self.height = inst.size[1]

	def show_back(self):
		self.back = True
		with self.canvas:
			self.rect.source = self.img_back

	def show_front(self):
		self.back = False
		with self.canvas:
			self.rect.source = self.img_card

	def update_text(self, t="", f=.6):
		with self.canvas:
			self.text_l = CoreLabel(text=f"{t}", text_size=self.size, color=(1, 1, 1, 1), outline_width=2, halign='center', valign='middle', font_size=self.size[0] * f)
			# self.text_l.text = f"{t}"
			# self.text_l.font_size = self.size[0] * f
			self.text_l.refresh()
			self.text_r.texture = self.text_l.texture

	def selected_c(self, s=True):
		pass
