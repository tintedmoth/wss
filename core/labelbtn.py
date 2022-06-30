from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout

from core.button import Button
from core.datapath import *
from core.label import Label


class Labelbtn(RelativeLayout):
	a = ""
	def __init__(self, size=(0, 0), cid="", **kwargs):
		super(Labelbtn, self).__init__(**kwargs)
		self.size_hint = (None, None)
		self.cid = cid
		self.size = size
		self.test = {}
		self.ian = {}
		self.inx = 0

		for n in range(1, 5):
			self.test[str(n)] = Label(text="　" * n, valign='middle')
			self.test[str(n)].texture_update()
		for n in range(2):
			self.ian[str(n)] = Image(source=f"atlas://{img_in}/other/blank", allow_stretch=True, size_hint=(None, None), size=(self.test["1"].texture.size[0] * 1.05, self.test["1"].texture.size[1] * 1.05))

		self.btn = Button(size=self.size, pos=self.pos, size_hint=(None, None), halign='left', valign='top', text_size=(self.size[0] * 0.95, self.size[1] * 0.95), markup=True, height=self.size[1])
		self.add_widget(self.btn)
		for img in self.ian:
			self.add_widget(self.ian[img])

	def replaceImage(self,p=False):
		for n in self.ian:
			self.ian[str(n)].source = f"atlas://{img_in}/other/blank"

		for n in range(len(self.ian), len(self.btn.anchors)):
			self.ian[str(n)] = Image(source=f"atlas://{img_in}/other/blank", allow_stretch=True, size_hint=(None, None), size=(self.test["1"].texture.size[0] * 1.05, self.test["1"].texture.size[1] * 1.05))
			self.add_widget(self.ian[str(n)])

		self.inx = 0
		for item in self.btn.anchors:
			self.ian[str(self.inx)].size = (self.test[item[-1]].texture.size[0] * 1.05, self.test[item[-1]].texture.size[1] * 1.05)
			self.ian[str(self.inx)].source = f"atlas://{img_in}/other/{item[:-3]}"
			if p:
				self.ian[str(self.inx)].pos = (self.size[1] / 17 + self.btn.anchors[item][0] + self.btn.x, self.btn.size[1] - self.size[1] / 19 - self.btn.anchors[item][1] - self.test[item[-1]].texture.size[1] + self.btn.y)
			else:
				self.ian[str(self.inx)].pos = (self.size[1] / 9 + self.btn.anchors[item][0] + self.btn.x, self.btn.size[1] - self.size[1] / 15 - self.btn.anchors[item][1] - self.test[item[-1]].texture.size[1] + self.btn.y)
			self.inx += 1
