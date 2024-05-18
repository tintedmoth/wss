from kivy.graphics import Rectangle
from kivy.graphics import Rotate
from kivy.uix.relativelayout import RelativeLayout

from core.datapath import *
from os.path import exists


class Mat(RelativeLayout):
	def __init__(self, owner, data, per=1, **kwargs):
		super(Mat, self).__init__(**kwargs)
		self.size_hint = (None, None)
		self.owner = owner
		self.angle = 0
		self.data = data
		self.per = per
		self.yspace = 0
		self.size = (400 * self.per, 240 * self.per)
		self.center = (self.size[0] / 2, self.size[1] / 2)
		self.img_mat = f"atlas://{img_in}/other/blank"
		self.actual = self.size
		self.pos_mat = (0, 0)
		self.mat = self.size
		self.height = self.size[1]
		self.width = self.size[0]

		with self.canvas.before:
			self.rotation = Rotate(angle=self.angle, origin=self.center)
		with self.canvas:
			self.rect = Rectangle(source=self.img_mat, pos=self.pos_mat, size=self.actual)

	def import_mat(self, data, per=1):
		self.yspace = -data["card"][1] * per * 11 / 10
		self.mat = (data["size"][0] * per, data["size"][1] * per)
		self.size = (data["size"][0] * per, data["size"][1] * per)
		self.center = (self.size[0] / 2, self.size[1] / 2)
		self.rotation.origin = (self.pos[0] + self.center[0], self.pos[1] + self.center[1])
		if "mat_matj" in data["img"]:
			self.img_mat = f"atlas://{img_in}/other/mat_matj"
		elif "mat_mat" in data["img"]:
			self.img_mat = f"atlas://{img_in}/other/mat_mat"
		elif "mat_nodl" in data["img"]:
			self.img_mat = f"atlas://{img_in}/other/mat_nodl"
		else:
			if exists(f"{cache}/{data['img']}"):
				self.img_mat = f"{cache}/{data['img']}"
			else:
				self.img_mat = f"atlas://{img_in}/other/mat_mat"

		if "actual" in data:
			self.actual = (data["actual"][0] * per, data["actual"][1] * per)

		self.pos_mat = (data["pos"][0] * per, data["pos"][1] * per)

		self.rect.source = self.img_mat
		self.rect.size = self.actual
		self.rect.pos = self.pos_mat

	def reverse(self):
		self.rotation.angle = 180

	def stand(self):
		self.rotation.angle = 0
