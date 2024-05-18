from kivy.graphics import Rectangle
from kivy.uix.image import Image

from core.button import Button
from core.datapath import *


class ImgButton(Image):
	cid = ""

	def __init__(self, card=(13, 18), size=(10, 10), cid="", **kwargs):
		super(ImgButton, self).__init__(**kwargs)
		self.dlimg = 0
		self.card = card
		self.cid = cid
		self.size = size
		self.size_hint = (None, None)
		self.height = self.size[1]
		self.width = self.size[0]
		self.select = False
		self.blank = f"atlas://{img_in}/other/blank"
		self.img_btn = str(self.source)
		self.img_btnn = f"atlas://{img_in}/other/grey"
		self.img_select = f"atlas://{img_in}/other/select"
		self.pos_select = (self.pos[0] - self.card[1] / 20, self.pos[1] - self.card[1] / 20)
		self.size_select = (self.size[0] + self.card[1] / 10, self.size[1] + self.card[1] / 10)
		self.allow_stretch = True

		with self.canvas.before:
			self.rect = Rectangle(source=self.blank, pos=self.pos_select, size=self.size_select)
		with self.canvas:
			self.btn = Button(size=self.size, pos=self.pos, size_hint=(None, None), cid=self.cid, opacity=0, height=self.height)
			self.add_widget(self.btn)
		self.bind(size=self._update_rect, pos=self._update_rect)

	def _update_rect(self, inst, value):
		self.rect.pos = (inst.pos[0] - self.card[1] / 20, inst.pos[1] - self.card[1] / 20)
		self.rect.size = (inst.size[0] + self.card[1] / 10, inst.size[1] + self.card[1] / 10)
		self.btn.pos = inst.pos
		self.btn.size = inst.size
		self.height = inst.size[1]
		self.btn.height = inst.size[1]

	def update_image(self, dlimg):
		self.dlimg = dlimg
		if not self.dlimg and "other/" not in self.img_btn:
			self.source = self.img_btnn
		else:
			self.source = self.img_btn

	def selected_c(self, s=True):
		if s:
			self.select = True
			self.rect.source = self.img_select
		else:
			self.select = False
			self.rect.source = self.blank
