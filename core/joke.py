from kivy.uix.image import Image
from kivy.graphics import Rectangle

from core.datapath import *
from core.label import Label


class Joketext(Image):
	def __init__(self, **kwargs):
		super(Image, self).__init__(**kwargs)
		# self.font_name = f"{font_in}/{font}"
		# self.joke = Label(text="", color=(1, 1, 1, 1), outline_width=5, halign="center", valing="center")
		self.size_hint = (None, None)
		self.blank = f"atlas://{img_in}/other/blank"
		self.img_src = f"atlas://{img_in}/other/blank"
		# self.source = self.img_src

		# self.allow_stretch = False
		# self.keep_ratio = True

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
		#
		# # self.label.bind(on_texture=self.change_font_size)
		# self.joke.bind(on_text=self.change_texture)


	# def on_text(self, instance, text):
	# 	# Just get large texture:
	# 	label = Label(text=self.text, color=(1, 1, 1, 1), outline_width=5, halign="center", valing="center",text_size=self.size)
	# 	label.font_size = "500dp"  # something that'll give texture bigger than phone's screen size
	# 	label.texture_update()
	# 	# Set it to image, it'll be scaled to image size automatically:
	# 	self.texture = label.texture


	def change_texture(self,text):
		# self.joke = Label()
		#
		# self.joke.color = (1, 1, 1, 1)
		# self.joke.outline_width = 5
		# self.joke.halign = "center"
		# self.joke.valing = "center"
		self.joke.text = text
		self.joke.font_size = int(self.joke.size[1]/2)
		print(self.joke.font_size)
		self.joke.texture_update()
		# for r in range(int(self.joke.size[1]/2)):
		# 	if self.joke.texture_size[0] >= self.width or self.joke.texture_size[1] >= self.height:
		# 		self.joke.font_size -= 1
		# 		self.joke.texture_update()
		# 	else:
		# 		print(self.joke.font_size)
		# 		self.texture = self.joke.texture
		# 		break
		self.texture = self.joke.texture
