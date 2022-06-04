from kivy.animation import Animation
from kivy.graphics import Rectangle
from kivy.graphics import Rotate
from kivy.uix.relativelayout import RelativeLayout

from core.button import Button
from core.datapath import *
from core.label import CoreLabel
from os.path import exists

l_c_size = 0.3  # 0.264  # multiplier for changing size of level and cost image
p_size = 0.45  # multiplier for changing size of power bar image
i_size = 0.236  # multiplier for changing size of icon image
s_size = 0.55  # multiplier for changing size of soul image
a_size = 0.55  # multiplier for changing size of ability image
t_size = 0.27  # multiplier for changing size of trigger image
m_size = 0.25  # multiplier for changing size of marker image

img_l = (50, 60)  # Level image size in px used for card layout
img_c = (50, 42)  # Cost image size in px used for card layout
img_p = (81, 28)  # Power image size in px used for card layout
img_t = (49, 58)  # Trigger Icon image size in px
img_w = (66, 47)  # Trigger Icon image size in px
img_i = (56, 56)  # Icon image size in px
img_s = (16, 16)  # Soul image size in px
img_a = (24, 12)  # Ability image size in px

level_pos = (0.015, 0.015)  # Level and Cost image position from top left
power_bar = (0.015, 0.015)  # Power bar image position on card from bottom left
power_text = (0.12, 0.010)  # Power bar text position on card from bottom left
icon_pos = (0.035, 0.010)  # Power bar text position on card from bottom left
soul_pos = (0.015, 0.010)  # Power bar text position on card from bottom left
trigger_pos = (0.015, 0.015)  # trigger icon position on card from top right
colour_pos = (0.015, 0.015)  # Power bar text position on card from bottom right
ability_pos = (0.015, 0.015)  # ability image position on card from bottom right
marker_pos = (0.015, 0.015)  # marker image position on card from bottom right

move_dt = 0.35

cont_ability = "[CONT]"
auto_ability = "[AUTO]"
act_ability = "[ACT]"

card_annex = ["ws01v",
      "MK/S11-E101",
      "MK/S11-E103",
      "MK/S11-E105",
      "MK/S11-TE02",
      "MK/S11-TE03",
      "MK/S11-TE04",
      "MK/S11-TE05",
      "MK/S11-TE08",
      "MK/S11-TE09",
      "MK/S11-TE10",
              "MK/S11-TE11",
              "MK/S11-TE14",
              "MK/S11-TE15",
              "CGS/WS01-T01",
              "CGS/WS01-T02",
              "CGS/WS01-T03",
              "CGS/WS01-T04",
              "CGS/WS01-T05",
              "CGS/WS01-T06",
              "CGS/WS01-T07",
              "CGS/WS01-T08",
              "CGS/WS01-T09",
              "CGS/WS01-T10",
              "CGS/WS01-T11",
              "CGS/WS01-T12",
              "CGS/WS01-T13",
              "CGS/WS01-T14",
              "CGS/WS01-T15",
              "CGS/WS01-T16",
              "CGS/WS01-T17",
              "CGS/WS01-T18",
              "CGS/WS01-T19",
              "CGS/WS01-T20",
              "CGS/WS01-T21"
              ]


class Card(RelativeLayout):
	def __init__(self, code="", card=(100, 100), owner="", per=1, data="", **kwargs):
		super(Card, self).__init__(**kwargs)
		self.size_hint = (None, None)
		self.move_dt = move_dt
		self.ind = code
		self.per = per
		self.cid = ""
		self.name = ""
		self.jname = ""
		self.rarity = ""
		self.colour = []
		self.mcolour = ""
		self.colour_c = []
		self.card = ""
		self.trigger = ()
		self.text_o = ()
		self.jtext_o = ()
		self.level = 0
		self.cost = 0
		self.icon = ""
		self.power = 0
		self.soul = 0
		self.turn = 0
		self.trait = ()
		self.flavour = ""
		self.jflavour = ""
		self.jtrait = ()
		self.back = True
		self.movable = False
		self.status = ""
		self.pos_old = ""
		self.pos_new = ""
		self.owner = owner
		self.dx = 0
		self.dy = 0
		self.select = False
		self.cost_c = []
		self.cost_t = 0
		self.power_c = []
		self.power_t = 0
		self.level_c = []
		self.level_t = 0
		self.soul_c = []
		self.soul_t = 0
		self.soul_i = {}
		self.text_c = []
		self.trait_c = []
		self.trait_t = []
		self.name_t = ""
		self.name_c = []
		self.mat = ""
		self.img = {}
		self.img_file = ""
		self.max_soul = 4
		self.max_ability = 6
		self.max_trigger = 2
		self.ability_i = {}
		self.trigger_i = {}
		self.size = card
		self.marker = False
		self.wmarker = False

		self.img_blank = f"atlas://{img_in}/other/blank"
		self.img_none = f"atlas://{img_in}/other/none"
		self.img_back = f"atlas://{img_in}/other/back"
		self.img_power = f"atlas://{img_in}/other/power"
		self.img_soul = f"atlas://{img_in}/other/soul_s"
		self.img_auto = f"atlas://{img_in}/other/auto"
		self.img_act = f"atlas://{img_in}/other/act"
		self.img_cont = f"atlas://{img_in}/other/cont"
		self.img_select = f"atlas://{img_in}/other/select"
		self.img_selectable = f"atlas://{img_in}/other/movable"

		self.angle = 0
		self.height = card[1]
		self.width = card[0]
		self.center = (self.size[0] / 2, self.size[1] / 2)
		self.sep = abs(card[1] - card[0])

		with self.canvas.before:
			self.rotation = Rotate(angle=self.angle, origin=self.center)

		with self.canvas:
			soul_size = (img_s[0] * s_size * self.per, img_s[1] * s_size * self.per)
			ability_size = (img_a[0] * a_size * self.per, img_a[1] * a_size * self.per)
			marker_size = (self.size[0] * m_size, self.size[1] * m_size)
			pos_soul = (soul_pos[0] * self.size[0], soul_pos[1] * self.size[1])
			pos_level = (level_pos[0] * self.size[0],self.size[1] - img_l[1] * l_c_size * self.per - level_pos[1] * self.size[1])
			pos_cost = (pos_level[0], pos_level[1] - img_c[1] * l_c_size * self.per)
			pos_icon = (icon_pos[0] * self.size[0], pos_cost[1] - img_i[1] * i_size * self.per)
			pos_power = (power_bar[0] * self.size[0], power_bar[1] * self.size[1])
			pos_colour = (colour_pos[0] * self.size[0], colour_pos[1] * self.size[1])
			power_b = (img_p[0] * p_size * self.per, img_p[1] * p_size * self.per)

			self.slc = Rectangle(source=self.img_blank,pos=(self.pos[0] - self.size[1] / 20, self.pos[1] - self.size[1] / 20),size=(self.size[0] + self.size[1] / 10, self.size[1] * 1.1))
			self.front = Rectangle(source=self.img_blank, pos=self.pos, size=self.size)

			self.level_i = Rectangle(source=self.img_blank, pos=pos_level,size=(img_l[0] * l_c_size * self.per,img_l[1] * l_c_size * self.per))
			self.cost_i = Rectangle(source=self.img_blank, pos=pos_cost,size=(img_c[0] * l_c_size * self.per,img_c[1] * l_c_size * self.per))
			self.icon_i = Rectangle(source=self.img_blank, pos=pos_icon,size=(img_i[0] * i_size * self.per,img_i[1] * i_size * self.per))
			self.colour_i = Rectangle(source=self.img_blank, size=(power_b[1], power_b[1]),pos=(self.size[0] - power_b[1] - pos_colour[0], pos_colour[1]))

			for x in range(self.max_ability):
				self.ability_i[str(x)] = Rectangle(source=self.img_blank, size=ability_size, pos=(self.size[0] - ability_pos[0] * self.size[0] - ability_size[0],ability_pos[1] * self.size[1] + self.colour_i.pos[1] + self.colour_i.size[1] + x * (ability_size[1] + ability_pos[1] * self.size[1] / 2.)))

			self.power_b = Rectangle(source=self.img_blank, size=power_b, pos=pos_power)

			for x in range(self.max_soul):
				self.soul_i[str(x)] = Rectangle(source=self.img_blank, size=soul_size,pos=(self.power_b.pos[0] + x * soul_size[0],pos_soul[1] + self.power_b.pos[1] + self.power_b.size[1]))

			# self.soul_l = CoreLabel(text="", text_size=soul_size, color=(1, 1, 1, 1),
			self.soul_l = CoreLabel(text="", text_size=(soul_size[0] * 1.5, self.power_b.size[1]), color=(1, 1, 1, 1), outline_width=1.9, halign='center', valign='middle', font_size=self.power_b.size[1] * 0.8)
			self.soul_l.refresh()
			self.soul_r = Rectangle(texture=self.soul_l.texture, size=self.soul_l.texture.size, pos=(self.power_b.pos[0] + pos_soul[0] / 4. + soul_size[0],pos_soul[1] + self.power_b.pos[1] + self.power_b.size[1]))

			for n in range(self.max_trigger):
				self.trigger_i[str(n)] = Rectangle(source=self.img_blank,pos=(self.size[0] - trigger_pos[0] * self.size[0] - (img_t[0] * t_size * self.per) * (n + 1),self.size[1] - img_t[1] * t_size * self.per - trigger_pos[1] *self.size[1]),size=(img_t[0] * t_size * self.per, img_t[1] * t_size * self.per))

			self.trigger_i["0"].source = self.img_none
			self.level_l = CoreLabel(text="0", color=(1, 1, 1, 1), halign='center',font_size=self.level_i.size[1] * 0.55)
			self.level_l.refresh()
			self.level_r = Rectangle(texture=self.level_l.texture, size=self.level_l.texture.size,pos=(self.level_i.pos[0] * 1.6, self.level_i.pos[1] - self.level_i.size[1] * 0.03))

			self.power_l = CoreLabel(text="", text_size=self.power_b.size, color=(1, 1, 1, 1),halign='center', font_size=self.power_b.size[1] * 0.8, valign='middle')
			self.power_l.refresh()
			self.power_r = Rectangle(texture=self.power_l.texture, size=self.power_l.texture.size,pos=(power_text[0] * self.size[0], power_text[1] * self.size[1]))

			self.marker_i = Rectangle(source=self.img_blank, size=marker_size,pos=self.ability_i["0"].pos)
			# pos=(self.ability_i["0"].pos[0] - ability_size[0]-marker_pos[0] * self.card_size[0],self.ability_i["0"].pos[1]))

			self.marker_l = CoreLabel(text="", text_size=self.marker_i.size, color=(1, 1, 1, 1), outline_width=1.9,font_size=marker_size[1] * .8, halign='center', valign='middle', size=marker_size)
			self.marker_l.refresh()
			self.marker_r = Rectangle(texture=self.marker_l.texture, size=self.marker_l.texture.size,pos=(self.marker_i.pos[0], self.marker_i.pos[1]))
			self.cover = Rectangle(source=self.img_back, pos=self.pos, size=self.size)
			self.text_l = CoreLabel(text="", text_size=self.size, color=(1, 1, 1, 1),outline_width=2, halign='center', valign='middle', font_size=self.size[0] * .6)
			self.text_l.refresh()
			self.text_r = Rectangle(texture=self.text_l.texture, size=self.size, pos=(0, 0))

		if self.ind == "1" or self.ind == "2":
			self.cid = "player"
		if data:
			self.import_data(data)

	def import_mat(self, mat=""):
		self.mat = mat

	def import_data(self, card):
		if card != "" and card != "player":
			self.cid = str(card["id"])
			self.name = str(card["name"])
			self.update_name()
			self.jname = str(card["jap"])
			self.mcolour = str(card["colour"])
			self.colour.append(self.mcolour.lower())
			self.colour_c = []
			self.card = str(card["type"])
			if card["id"] in card_annex:
				self.img_file = str(card["img"][:-4])
			else:
				self.img_file = str(card["img"])
			self.update_image()

			self.rarity = str(card["rarity"])
			self.trigger = list(card["trigger"])
			self.update_trigger()
			self.text_o = list(card["text"])
			self.jtext_o = list(card["textj"])
			self.trait = list(card["trait"])
			self.status = "Stand"
			self.pos_old = "Library"
			self.pos_new = "Library"
			try:
				self.flavour = str(card["flavour"])
			except KeyError:
				self.flavour = ""
			try:
				self.jflavour = str(card["flavourj"])
			except KeyError:
				self.jflavour = ""
			try:
				self.jtrait = list(card["traitj"])
			except KeyError:
				self.jtrait = []
			try:
				self.jname = str(card["jap"])
			except KeyError:
				self.jname = ""
			try:
				self.jtext_o = list(card["textj"])
			except KeyError:
				self.jtext_o = []
			self.update_colour()
			self.level = int(card["level"])
			self.cost = int(card["cost"])
			self.update_cost()
			self.update_level()
			self.power = int(card["power"])
			self.soul = int(card["soul"])
			self.update_power()
			self.update_soul()

			self.trait_c = []
			self.update_trait()

			self.text_c = []
			for item in self.text_o:
				if item != "":
					self.text_c.append([item, -1])
			self.update_ability()
			self.icon = ""
			try:
				self.icon = str(card["icon"])
			except KeyError:
				for item in self.text_o:
					if "[counter]" in item.lower():
						self.icon = "Counter"
					elif "[clock]" in item.lower() or "] alarm" in item.lower() or "] shift" in item.lower():
						self.icon = "Clock"
			self.update_icon()

			if self.marker:
				self.update_marker()

		elif card == "player":
			self.card = "Climax"
			self.soul = 0
			self.soul_c = []
			self.update_soul()
			self.update_power()
			self.update_icon()
			self.update_image()
			self.update_colour()
			self.update_level()
			self.text_c = []
			self.update_marker()
			self.show_front()
			self.update_trigger()

	def stand(self, a=True):
		self.status = "Stand"
		angle = 0
		if self.rotation.angle > 180:
			angle = 360
		if a:
			mov = Animation(angle=angle, d=self.move_dt / 2.)
			mov.start(self.rotation)
		else:
			self.rotation.angle = angle

	# self.playmat_fix()

	def rest(self, a=True):
		self.status = "Rest"
		if self.rotation.angle < 90:
			angle = -90
		elif self.rotation.angle >= 90:
			angle = 270
		if a:
			mov = Animation(angle=angle, d=self.move_dt / 2.)
			mov.start(self.rotation)
		else:
			self.rotation.angle = angle
		if angle > 360:
			self.rotation.angle = 90

	# self.playmat_fix()

	def climax(self, a=True):
		self.status = ""
		if self.rotation.angle < 270:
			angle = 90
		elif self.rotation.angle >= 270:
			angle = 450
		if a:
			mov = Animation(angle=angle, d=self.move_dt / 2.)
			mov.start(self.rotation)
		else:
			self.rotation.angle = angle

	def reverse(self, a=True):
		self.status = "Reverse"
		angle = -180
		if self.rotation.angle >= 0:
			angle = 180

		if a:
			mov = Animation(angle=angle, d=self.move_dt / 2.)
			mov.start(self.rotation)
		else:
			self.rotation.angle = angle

	def show_back(self):
		self.back = True
		with self.canvas:
			self.cover.source = self.img_back

	def show_front(self):
		self.back = False
		with self.canvas:
			self.cover.source = self.img_blank

	def setPos(self, xpos=0, ypos=0, field=None, a=True, t="", d=False):
		if a:
			mdt = self.move_dt
		else:
			mdt = 0
		if field:
			# self.playmat_fix(field=field)
			# field = (field[0]-self.size[0]/2,field[1]-self.size[1]/2)

			# if a:
			move = Animation(x=field[0] + self.dx, y=field[1] + self.dy, d=mdt)
			move.start(self)
			# else:
			# 	self.x = field[0] + self.dx
			# 	self.y = field[1] + self.dy
		else:
			# if a:
			move = Animation(x=xpos, y=ypos, d=mdt)
			move.start(self)
			# else:
			# 	self.x = xpos
			# 	self.y = ypos

		# update and track position
		if t != "":
			self.pos_old = self.pos_new
			self.pos_new = t

			if t == "Library" or t == "Stock":
				# self.show_front()
				self.show_back()  # @@
			else:
				if d:
					self.show_back()
				else:
					self.show_front()

			if self.owner == "2" and self.pos_new == "Hand":
				# self.show_front()
				self.show_back()  # @@

			if self.pos_new == "Stock" and self.status != "Rest":
				self.rest()
			elif self.pos_new in ("Climax", "Level", "Memory") and self.status != "":
				self.climax()
			elif self.pos_new in ("Library", "Waiting", "Clock", "Hand") and self.status != "Stand":
				self.stand()
			elif self.pos_new in ("Center0", "Center1", "Center2", "Back0", "Back1") and self.pos_old in ("Memory","Stock"):
				self.stand()

			if self.pos_old == "Marker":
				self.wmarker = True
			if self.pos_new == "Marker":
				self.wmarker = False

			if self.pos_new in ("Waiting", "Hand", "Clock", "Stock", "Level", "Library", "Memory"):
				self.power_c = []
				self.soul_c = []
				self.name_c = []
				if not (self.pos_old == "Hand" and self.pos_new == "Hand"):
					self.level_c = []
				self.colour_c = []
				self.cost_c = []
				self.trait_c = []
				self.text_c = []
				self.wmarker = False
				for item in self.text_o:
					if item != "":
						self.text_c.append([item, -1])
				self.update_trait()
				self.update_name()
				self.update_power()
				self.update_cost()
				self.update_soul()
				self.update_ability()
				self.update_colour()
				self.update_level()

	def update_trait(self):
		self.trait_t = []
		if self.card == "Character":
			for item in self.trait:
				if item != "":
					self.trait_t.append(item)
			for item in self.trait_c:
				if item[1] != 0:
					self.trait_t.append(item[0])

	def update_power(self):
		if self.card == "Character":
			self.clean_c("power")
			self.power_t = int(self.power)

			for item in self.power_c:
				if item[1] != 0:
					self.power_t += item[0]

			with self.canvas:
				if self.power_t > self.power:
					color = (0, 1, 0, 1)
				elif self.power_t < self.power:
					color = (1, 0, 0, 1)
				else:
					color = (1, 1, 1, 1)

				if self.power_t > 0:
					self.power_b.source = self.img_power
					self.power_l = CoreLabel(text=f"{self.power_t:={len(str(self.power_t)) + 1}}", text_size=self.power_b.size, color=color, halign='center', font_size=self.power_b.size[1] * 0.8, valign='middle')

					# self.power_l.text = f"{self.power_t:={len(str(self.power_t))+1}}"
					# self.power_l.text_size = self.power_b.size
					# self.power_l.color = color
					self.power_l.refresh()
					self.power_r.texture = self.power_l.texture
					self.power_r.size = self.power_l.texture.size
					self.power_r.pos = (self.power_b.pos[0] + (self.power_b.size[0] - self.power_r.size[0]) / 2, power_text[1] * self.size[1])
		else:
			with self.canvas:
				self.power_b.source = self.img_blank
				self.power_l.text = ""
				self.power_l.refresh()
				self.power_r.texture = self.power_l.texture
				self.power_r.size = self.power_l.texture.size

	def update_text(self, t="", f=.6):
		self.text_l.text = f"{t}"
		self.text_l.font_size = self.size[0] * f
		self.text_l.refresh()
		self.text_r.texture = self.text_l.texture

	# self.text_r.size = self.text_l.texture.size

	def update_icon(self):
		if self.icon != "":
			self.icon_i.source = f"atlas://{img_in}/other/{self.icon.lower()}"
		else:
			self.icon_i.source = self.img_blank

	def update_image(self):
		if self.cid != "" and self.cid != "player":
			try:
				if "dc_w00_00.gif" in self.img_file:
					self.img_file = self.img_file.replace(".gif", "")
				self.front.source = f"atlas://{img_in}/annex/{self.img_file}"
			except KeyError:
				if exists(f"{cache}/{self.img_file}"):
					self.front.source = f"{cache}/{self.img_file}"
				else:
					self.front.source = f"atlas://{img_in}/other/grey"
		else:
			self.front.source = self.img_blank

	def update_colour(self):
		self.clean_c("colour")
		self.colour = []
		self.colour.append(self.mcolour.lower())
		for item in self.colour_c:
			if item[1] != 0 and item[0].lower() not in self.colour:
				self.colour.append(item[0].lower())
		with self.canvas:
			if self.cid != "" and self.cid != "player":
				self.colour_i.source = f"atlas://{img_in}/other/{''.join(s[0].lower() for s in self.colour)}"
			else:
				self.colour_i.source = self.img_blank

	def update_cost(self):
		if self.card != "Climax":
			self.clean_c("cost")
			self.cost_t = int(self.cost)
			for item in self.cost_c:
				if item[1] != 0:
					self.cost_t += item[0]

			with self.canvas:
				self.cost_i.source = f"atlas://{img_in}/other/C{self.cost_t}"
		else:
			with self.canvas:
				self.cost_i.source = self.img_blank

	def update_level(self):
		if self.card != "Climax":
			self.clean_c("level")
			self.level_t = int(self.level)
			for item in self.level_c:
				if item[1] != 0:
					self.level_t += item[0]

			with self.canvas:
				if self.level_t > 0:
					img = f"{self.mcolour[0].upper()}L"  # {self.level_t}"
				else:
					img = "L0"
				self.level_i.source = f"atlas://{img_in}/other/{img}"

				if self.level_t > self.level and ("Center" in self.pos_new or "Back" in self.pos_new):
					color = (0, 1, 0, 1)
				elif self.level_t < self.level and ("Center" in self.pos_new or "Back" in self.pos_new):
					color = (1, 0, 0, 1)
				elif self.level_t > self.level:
					color = (1, 0, 0, 1)
				elif self.level_t < self.level:
					color = (0, 1, 0, 1)
				else:
					color = (1, 1, 1, 1)

				self.level_l = CoreLabel(text=f"{self.level_t}", color=color, halign='center', font_size=self.level_i.size[1] * 0.55)
				self.level_l.refresh()
				self.level_r.texture = self.level_l.texture
				self.level_r.size = self.level_l.texture.size
				self.level_r.pos = (self.level_i.pos[0] + (self.level_i.size[0] - self.level_r.size[0]) / 2, self.level_i.pos[1] + self.level_i.size[1] * 0.08)
		else:
			self.level_i.source = self.img_blank

			self.level_l.text = ""
			self.level_l.refresh()
			self.level_r.texture = self.level_l.texture
			self.level_r.size = self.level_l.texture.size

	def update_ability(self):
		self.clean_c("text")
		with self.canvas:
			ability = []
			atext = []
			for text in self.text_c:
				tt = True
				if text[1] != 0 and text[1] != -3 and text[1] != -2 and len(ability) < self.max_ability and text[1] > -9:
					if text[0] not in atext:
						atext.append(text[0])
					else:
						if text[0].startswith(auto_ability):
							if text[0].lower().startswith(auto_ability.lower() + " encore ["):
								tt = False
						# elif text[0].startswith(cont_ability):
						# 	tt = False
					if tt:
						if text[0].startswith(cont_ability):
							ability.append(self.img_cont)
						elif text[0].startswith(auto_ability):
							ability.append(self.img_auto)
						elif text[0].startswith(act_ability):
							ability.append(self.img_act)
			for inx in range(self.max_ability):
				if inx < len(ability):
					self.ability_i[str(inx)].source = ability[inx]
					ability_size = (img_a[0] * a_size * self.per, img_a[1] * a_size * self.per)
					if self.marker:
						self.ability_i[str(inx)].pos = (self.ability_i[str(inx)].pos[0],ability_pos[1] * self.size[1] + self.colour_i.pos[1] +self.colour_i.size[1] + inx * (ability_size[1] + ability_pos[1] * self.size[1] / 2.) + self.marker_i.size[1])
					else:
						self.ability_i[str(inx)].pos = (self.size[0] - ability_pos[0] * self.size[0] - ability_size[0],ability_pos[1] * self.size[1] + self.colour_i.pos[1] + self.colour_i.size[1] + inx * (ability_size[1] + ability_pos[1] * self.size[1] / 2.))

				elif inx >= len(ability):
					self.ability_i[str(inx)].source = self.img_blank

	def update_trigger(self):
		with self.canvas:
			tr = [1, 0]
			for inx in range(self.max_trigger):
				if inx < len(self.trigger) and self.cid != "player":
					if self.trigger[inx] == "":
						self.trigger_i[str(inx)].source = self.img_none
					else:
						if len(self.trigger) > 1:
							self.trigger_i[str(tr[inx])].source = f"atlas://{img_in}/other/{self.trigger[inx]}"
						else:
							self.trigger_i[str(inx)].source = f"atlas://{img_in}/other/{self.trigger[inx]}"
				else:
					if inx == 0 and self.cid != "player":
						self.trigger_i[str(inx)].source = self.img_none
					else:
						self.trigger_i[str(inx)].source = self.img_blank

	def update_soul(self):
		self.clean_c("soul")
		with self.canvas:
			self.soul_t = int(self.soul)

			for item in self.soul_c:
				if item[1] != 0:
					self.soul_t += item[0]

			if self.soul_t<0:
				self.soul_t = 0

			if self.soul_t > self.max_soul:
				for inx in range(self.max_soul):
					self.soul_i[str(inx)].source = self.img_blank

				self.soul_i["0"].source = self.img_soul
				self.soul_l.text = f"x{self.soul_t}"
			elif self.soul_t <= self.max_soul:
				for x in range(self.max_soul):
					if x + 1 <= self.soul_t:
						self.soul_i[str(x)].source = self.img_soul
					else:
						self.soul_i[str(x)].source = self.img_blank
				self.soul_l.text = ""
			else:
				for x in range(self.max_soul):
					self.soul_i[str(x)].source = self.img_blank
				self.soul_l.text = ""
			self.soul_l.refresh()
			self.soul_r.texture = self.soul_l.texture
			self.soul_r.size = self.soul_l.texture.size

	def playmat_fix(self, field=""):
		self.dx = self.dy = 0
		# if self.owner == "2":
		# 	m = -1
		# elif self.owner == "1":
		# 	m = 1
		m = 1
		if field == "":
			field = self.pos_new

		if "Center" in field and self.status == "Rest":
			if "0" in field:
				if "mat" in self.mat and "2" in self.owner:
					self.dx = m * (self.size[0] - self.size[1]) / 2.
				elif "mat" in self.mat:
					self.dx = m * (self.size[0] - self.size[1]) / 2.
				elif self.mat in ("mk", "fz", "fs", "sfe", "dis", "ns", "zm", "dc", "p3", "lb"):
					self.dx = m * (self.size[0] - self.size[1])
				else:
					self.dx = m * (self.size[0] - self.size[1]) / 2.
			elif "1" in field:
				if "mat" in self.mat:
					self.dx = m * (self.size[0] - self.size[1]) / 2.
				else:
					self.dx = m * (self.size[0] - self.size[1]) / 2.
			elif "2" in field:
				if "mat" in self.mat:
					self.dx = m * (self.size[0] - self.size[1]) / 4.
				elif self.mat in ("mk", "fz", "fs", "sfe", "dis", "ns", "zm", "dc", "p3", "lb"):
					self.dx = m * 0.001
				else:
					self.dx = m * (self.size[0] - self.size[1]) / 2.
			else:
				self.dx = 0
		elif "Back" in field and self.status == "Rest":
			self.dx = (self.size[0] - self.size[1]) / 2.
		else:
			self.dx = 0

		if self.status == "Rest" and ("Back" in field or "Center" in field):
			self.dy = (self.size[1] - self.size[0]) / 2.

	def rot(self, i):
		rot = Animation(angle=i, d=0.01)
		rot.start(self.rotation)

	def update_name(self):
		self.clean_c("name")
		self.name_t = str(self.name)
		if self.card == "Character":
			for item in self.name_c:
				if item[1] != 0:
					self.name_t += f" - {item[0]}"

	def update_marker(self, m=0):
		if m > 0:
			self.marker = True
			self.marker_l.text = f"{m}"
			self.marker_i.source = self.img_back
		else:
			self.marker = False
			self.marker_l.text = ""
			self.marker_i.source = self.img_blank
		with self.canvas:
			self.marker_l.refresh()
			self.marker_r.texture = self.marker_l.texture
			self.marker_r.size = self.marker_l.texture.size
		self.update_ability()

	def clean_c(self, t=""):
		to_remove = []
		if t == "power":
			text = self.power_c
		elif t == "cost":
			text = self.cost_c
		elif t == "level":
			text = self.level_c
		elif t == "soul":
			text = self.soul_c
		elif t == "name":
			text = self.name_c
		elif t == "text":
			text = self.text_c
		elif t == "colour":
			text = self.colour_c
		elif t == "trait":
			text = self.trait_c
		else:
			text = []
			texts = (self.power_c, self.cost_c, self.level_c, self.soul_c, self.text_c, self.colour_c, self.trait_c, self.name_c)

		if t == "":
			for item in texts:
				for item1 in item:
					if item1[1] == 0:
						to_remove.append((item, item1))

			for itemr in to_remove:
				itemr[0].remove(itemr[1])
		else:
			for item in text:
				if item[1] == 0:
					to_remove.append(item)
			for itemr in to_remove:
				text.remove(itemr)

	def reduce_c(self, text="", waiting=False):
		if text == "":
			c = (self.power_c, self.cost_c, self.level_c, self.soul_c, self.text_c, self.colour_c, self.trait_c, self.name_c)
		else:
			if text == "power":
				text = self.power_c
			elif text == "cost":
				text = self.cost_c
			elif text == "level":
				text = self.level_c
			elif text == "soul":
				text = self.soul_c
			elif text == "text":
				text = self.text_c
			elif text == "name":
				text = self.name_c
			elif text == "colour":
				text = self.colour_c
			elif text == "trait":
				text = self.trait_c

			c = (text,)

		for tt in c:
			for item in tt:
				if not waiting and item[1] > 0:
					item[1] -= 1
				elif waiting and item[1] >= 0:
					item[1] = 0

	def selected(self, s=True):
		if s:
			self.select = True
			self.slc.source = self.img_select
		else:
			self.select = False
			self.slc.source = self.img_blank

	def selectable(self, s=True):
		if s:
			self.select = True
			self.slc.pos = (-self.size[1] / 10, -self.size[1] / 10)
			self.slc.size = (self.size[0] + self.size[1] / 5, self.size[1] * 1.2)
			self.slc.source = self.img_selectable
		else:
			self.select = False
			self.slc.pos = (-self.size[1] / 20, -self.size[1] / 20)
			self.slc.size = (self.size[0] + self.size[1] / 10, self.size[1] * 1.1)
			self.slc.source = self.img_blank


class CardImg(RelativeLayout):
	def __init__(self, code="", card=(100, 100), owner="", per=1, data="", **kwargs):
		super(CardImg, self).__init__(**kwargs)
		self.size_hint = (None, None)
		self.ind = code
		self.per = per
		self.cid = ""
		self.name = ""
		self.jname = ""
		self.rarity = ""
		self.colour = []
		self.mcolour = ""
		self.colour_c = []
		self.card = ""
		self.trigger = ()
		self.text_o = ()
		self.jtext_o = ()
		self.level = 0
		self.cost = 0
		self.icon = ""
		self.power = 0
		self.soul = 0
		self.turn = 0
		self.trait = ()
		self.flavour = ""
		self.jflavour = ""
		self.jtrait = ()
		self.back = False
		self.status = ""
		self.pos_old = ""
		self.pos_new = ""
		self.owner = owner
		self.select = False
		self.cost_c = []
		self.cost_t = 0
		self.power_c = []
		self.power_t = 0
		self.level_c = []
		self.level_t = 0
		self.soul_c = []
		self.soul_t = 0
		self.soul_i = {}
		self.text_c = []
		self.trait_c = []
		self.trait_t = []
		self.name_c = []
		self.name_t = ""
		self.img = {}
		self.img_file = ""
		self.soul_i = {}
		self.max_soul = 4
		self.max_ability = 6
		self.max_trigger = 2
		self.ability_i = {}
		self.trigger_i = {}
		self.size = card
		self.stage = False

		self.img_blank = f"atlas://{img_in}/other/blank"
		self.img_none = f"atlas://{img_in}/other/none"
		self.img_back = f"atlas://{img_in}/other/back"
		self.img_power = f"atlas://{img_in}/other/power"
		self.img_soul = f"atlas://{img_in}/other/soul_s"
		self.img_auto = f"atlas://{img_in}/other/auto"
		self.img_act = f"atlas://{img_in}/other/act"
		self.img_cont = f"atlas://{img_in}/other/cont"
		self.img_select = f"atlas://{img_in}/other/select"

		self.height = card[1]
		self.width = card[0]

		with self.canvas:
			self.btn = Button(size=self.size, pos=self.pos, cid=self.ind, opacity=0, size_hint=(None, None), height=card[1])
			self.add_widget(self.btn)
			soul_size = (img_s[0] * s_size * self.per, img_s[1] * s_size * self.per)
			ability_size = (img_a[0] * a_size * self.per, img_a[1] * a_size * self.per)
			pos_soul = (soul_pos[0] * self.size[0], soul_pos[1] * self.size[1])
			pos_level = (level_pos[0] * self.size[0], self.size[1] - img_l[1] * l_c_size * self.per - level_pos[1])
			pos_cost = (pos_level[0], pos_level[1] - img_c[1] * l_c_size * self.per)
			pos_icon = (icon_pos[0] * self.size[0], pos_cost[1] - img_i[1] * i_size * self.per)
			pos_power = (power_bar[0] * self.size[0], power_bar[1] * self.size[1])
			pos_colour = (colour_pos[0] * self.size[0], colour_pos[1] * self.size[1])
			power_b = (img_p[0] * p_size * self.per, img_p[1] * p_size * self.per)

			self.slc = Rectangle(source=self.img_blank, pos=(self.pos[0] - self.size[1] / 20, self.pos[1] - self.size[1] / 20), size=(self.size[0] + self.size[1] / 10, self.size[1] * 1.1))
			self.front = Rectangle(source=self.img_blank, pos=self.pos, size=self.size)

			self.level_i = Rectangle(source=self.img_blank, pos=pos_level, size=(img_l[0] * l_c_size * self.per, img_l[1] * l_c_size * self.per))
			self.cost_i = Rectangle(source=self.img_blank, pos=pos_cost, size=(img_c[0] * l_c_size * self.per, img_c[1] * l_c_size * self.per))
			self.icon_i = Rectangle(source=self.img_blank, pos=pos_icon, size=(img_i[0] * i_size * self.per,img_i[1] * i_size * self.per))
			self.colour_i = Rectangle(source=self.img_blank, size=(power_b[1], power_b[1]), pos=(self.size[0] - power_b[1] - pos_colour[0], pos_colour[1]))

			for x in range(self.max_ability):
				self.ability_i[str(x)] = Rectangle(source=self.img_blank, size=ability_size, pos=(self.size[0] - ability_pos[0] * self.size[0] - ability_size[0], ability_pos[1] * self.size[1] + self.colour_i.pos[1] + self.colour_i.size[1] + x * (ability_size[1] + ability_pos[1] * self.size[1] / 2.)))

			self.power_b = Rectangle(source=self.img_blank, size=power_b, pos=pos_power)

			for x in range(self.max_soul):
				self.soul_i[str(x)] = Rectangle(source=self.img_blank, size=soul_size, pos=(self.power_b.pos[0] + x * soul_size[0], pos_soul[1] + self.power_b.pos[1] + self.power_b.size[1]))

			self.soul_l = CoreLabel(text="", text_size=(soul_size[0] * 1.5, self.power_b.size[1]), color=(1, 1, 1, 1), outline_width=1.9, halign='center', valign='middle', font_size=self.power_b.size[1] * 0.8)
			self.soul_l.refresh()
			self.soul_r = Rectangle(texture=self.soul_l.texture, size=self.soul_l.texture.size, pos=(self.power_b.pos[0] + pos_soul[0] / 4 + soul_size[0], pos_soul[1] + self.power_b.pos[1] + self.power_b.size[1]))

			self.level_l = CoreLabel(text="0", color=(1, 1, 1, 1), halign='center', font_size=self.level_i.size[1] * 0.55)
			self.level_l.refresh()
			self.level_r = Rectangle(texture=self.level_l.texture, size=self.level_l.texture.size, pos=(self.level_i.pos[0] * 1.6, self.level_i.pos[1] - self.level_i.size[1] * 0.03))

			self.power_l = CoreLabel(text="", text_size=self.power_b.size, color=(1, 1, 1, 1), halign='center', font_size=self.power_b.size[1] * 0.8, valign='middle')
			self.power_l.refresh()
			self.power_r = Rectangle(texture=self.power_l.texture, size=self.power_l.texture.size, pos=(power_text[0] * self.size[0], power_text[1] * self.size[1]))
			for n in range(self.max_trigger):
				self.trigger_i[str(n)] = Rectangle(source=self.img_blank, pos=(self.size[0] - trigger_pos[0] * self.size[0] - (img_t[0] * t_size * self.per) * (n + 1), self.size[1] - img_t[1] * t_size * self.per - trigger_pos[1] * self.size[1]), size=(img_t[0] * t_size * self.per, img_t[1] * t_size * self.per))
			self.trigger_i["0"].source = self.img_none
			self.cover = Rectangle(source=self.img_blank, pos=self.pos, size=self.size)
			self.text_l = CoreLabel(text="", text_size=self.size, color=(1, 1, 1, 1), outline_width=2, halign='center', valign='middle', font_size=self.size[0] * .6)
			self.text_l.refresh()
			self.text_r = Rectangle(texture=self.text_l.texture, size=self.size, pos=(0, 0))

		# self.text_r.center = self.center
		if data:
			self.import_data(data)

	def import_data(self, card):
		if card != "" and card != "player":
			self.cid = str(card["id"])
			self.name = str(card["name"])
			self.update_name()
			self.mcolour = str(card["colour"])
			self.colour.append(self.mcolour.lower())
			self.colour_c = []
			self.card = str(card["type"])
			if card["id"] in card_annex:
				self.img_file = str(card["img"][:-4])
			else:
				self.img_file = str(card["img"])
			self.update_image()

			self.rarity = str(card["rarity"])
			self.trigger = list(card["trigger"])
			self.update_trigger()
			self.text_o = list(card["text"])
			self.trait = list(card["trait"])
			self.status = "Stand"
			self.pos_old = "Library"
			self.pos_new = "Library"
			try:
				self.flavour = str(card["flavour"])
			except KeyError:
				self.flavour = ""
			try:
				self.jflavour = str(card["flavourj"])
			except KeyError:
				self.jflavour = ""
			try:
				self.jtrait = list(card["traitj"])
			except KeyError:
				self.jtrait = []
			try:
				self.jtext_o = list(card["textj"])
			except KeyError:
				self.jtext_o = []
			try:
				self.jname = str(card["jap"])
			except KeyError:
				self.jname = ""
			self.update_colour()
			self.level = int(card["level"])
			self.cost = int(card["cost"])
			self.update_cost()
			self.update_level()
			self.power = int(card["power"])
			self.soul = int(card["soul"])
			self.update_power()
			self.update_soul()

			self.trait_c = []
			self.update_trait()

			self.text_c = []
			for item in self.text_o:
				if item != "":
					self.text_c.append([item, -1])
			self.update_ability()
			self.icon = ""
			try:
				self.icon = str(card["icon"])
			except KeyError:
				for item in self.text_o:
					if "[counter]" in item.lower():
						self.icon = "Counter"
					elif "[clock]" in item.lower() or "[alarm]" in item.lower() or "] alarm" in item.lower() or "] shift" in item.lower():
						self.icon = "Clock"
			self.update_icon()
		elif card == "player":
			self.card = "Climax"
			self.soul = 0
			self.soul_c = []
			self.update_soul()
			self.update_power()
			self.update_icon()
			self.update_image()
			self.update_colour()
			self.update_level()
			self.text_c = []
			self.update_ability()
			self.update_trigger()

	def stand(self):
		self.status = "Stand"

	def rest(self):
		self.status = "Rest"

	def climax(self):
		self.status = ""

	def reverse(self):
		self.status = "Reverse"

	def show_back(self):
		self.back = True
		with self.canvas:
			self.cover.source = self.img_back

	def show_front(self):
		self.back = False
		with self.canvas:
			self.cover.source = self.img_blank

	def update_text(self, t="", f=.6):
		with self.canvas:
			self.text_l.text = f"{t}"
			self.text_l.font_size = self.size[0] * f
			self.text_l.refresh()
			self.text_r.texture = self.text_l.texture

	# self.text_r.size = self.text_l.texture.size

	def update_trait(self):
		self.trait_t = []
		if self.card == "Character":
			for item in self.trait:
				if item != "":
					self.trait_t.append(item)
			for item in self.trait_c:
				if item[1] != 0:
					self.trait_t.append(item[0])

	def update_name(self):
		self.clean_c("name")
		self.name_t = str(self.name)
		if self.card == "Character":
			for item in self.name_c:
				if item[1] != 0:
					self.name_t += f" {item[0]}"

	def update_power(self):
		if self.card == "Character":
			self.clean_c("power")
			self.power_t = self.power

			for item in self.power_c:
				if item[1] != 0:
					self.power_t += item[0]

			with self.canvas:
				if self.power_t > self.power:
					color = (0, 1, 0, 1)
				elif self.power_t < self.power:
					color = (1, 0, 0, 1)
				else:
					color = (1, 1, 1, 1)

				self.power_b.source = self.img_power
				self.power_l.text = f"{self.power_t:=6}"
				self.power_l.text_size = self.power_b.size
				self.power_l.color = color
				self.power_l.refresh()
				self.power_r.texture = self.power_l.texture
				self.power_r.size = self.power_l.texture.size
				self.power_r.pos = (self.power_b.pos[0] + (self.power_b.size[0] - self.power_r.size[0]) / 2, power_text[1] * self.size[1])
		else:
			with self.canvas:
				self.power_b.source = self.img_blank
				self.power_l.text = ""
				self.power_l.refresh()
				self.power_r.texture = self.power_l.texture
				self.power_r.size = self.power_l.texture.size

	def update_icon(self):
		with self.canvas:
			if self.icon != "":
				self.icon_i.source = f"atlas://{img_in}/other/{self.icon.lower()}"
			else:
				self.icon_i.source = self.img_blank

	def update_image(self):
		with self.canvas:
			if self.cid != "" and self.cid != "player":
				try:
					if "dc_w00_00.gif" in self.img_file:
						self.img_file = self.img_file.replace(".gif","")
					self.front.source = f"atlas://{img_in}/annex/{self.img_file}"
				except KeyError:
					if exists(f"{cache}/{self.img_file}"):
						self.front.source = f"{cache}/{self.img_file}"
					else:
						self.front.source = f"atlas://{img_in}/other/grey"
			else:
				self.front.source = self.img_blank

	def update_colour(self):
		self.clean_c("colour")
		self.colour = []
		self.colour.append(self.mcolour.lower())
		for item in self.colour_c:
			if item[1] != 0 and item[0].lower() not in self.colour:
				self.colour.append(item[0].lower())
		with self.canvas:
			if self.cid != "" and self.cid != "player":
				self.colour_i.source = f"atlas://{img_in}/other/{''.join(s[0].lower() for s in self.colour)}"
			else:
				self.colour_i.source = self.img_blank

	def update_cost(self):
		if self.card != "Climax":
			self.clean_c("cost")
			self.cost_t = self.cost
			for item in self.cost_c:
				if item[1] != 0:
					self.cost_t += item[0]

			with self.canvas:
				self.cost_i.source = f"atlas://{img_in}/other/C{self.cost_t}"
		else:
			with self.canvas:
				self.cost_i.source = self.img_blank

	def update_level(self):
		if self.card != "Climax":
			self.clean_c("level")
			self.level_t = int(self.level)
			for item in self.level_c:
				if item[1] != 0:
					self.level_t += item[0]

			with self.canvas:
				if self.level_t > 0:
					img = f"{self.mcolour[0].upper()}L"  # {self.level_t}"
				else:
					img = "L0"
				self.level_i.source = f"atlas://{img_in}/other/{img}"

				if self.level_t > self.level and ("Center" in self.pos_new or "Back" in self.pos_new):
					color = (0, 1, 0, 1)
				elif self.level_t < self.level and ("Center" in self.pos_new or "Back" in self.pos_new):
					color = (1, 0, 0, 1)
				elif self.level_t > self.level:
					color = (1, 0, 0, 1)
				elif self.level_t < self.level:
					color = (0, 1, 0, 1)
				else:
					color = (1, 1, 1, 1)

				self.level_l = CoreLabel(text=f"{self.level_t}", color=color, halign='center',font_size=self.level_i.size[1] * 0.55)
				self.level_l.refresh()
				self.level_r.texture = self.level_l.texture
				self.level_r.size = self.level_l.texture.size
				self.level_r.pos = (self.level_i.pos[0] + (self.level_i.size[0] - self.level_r.size[0]) / 2, self.level_i.pos[1] + self.level_i.size[1] * 0.08)
		else:
			self.level_i.source = self.img_blank

			self.level_l.text = ""
			self.level_l.refresh()
			self.level_r.texture = self.level_l.texture
			self.level_r.size = self.level_l.texture.size

	def update_ability(self):
		self.clean_c("text")
		with self.canvas:
			ability = []

			for text in self.text_c:
				if text[1] != 0 and text[1] != -3 and text[1] != -2 and len(ability) < self.max_ability:  # text[1] > -9
					if text[0].startswith(cont_ability):
						ability.append(self.img_cont)
					elif text[0].startswith(auto_ability):
						ability.append(self.img_auto)
					elif text[0].startswith(act_ability):
						ability.append(self.img_act)
			for inx in range(self.max_ability):
				if inx < len(ability):
					self.ability_i[str(inx)].source = ability[inx]
					ability_size = (img_a[0] * a_size * self.per, img_a[1] * a_size * self.per)
					self.ability_i[str(inx)].pos = (self.size[0] - ability_pos[0] * self.size[0] - ability_size[0],ability_pos[1] * self.size[1] + self.colour_i.pos[1] + self.colour_i.size[1] + inx * (ability_size[1] + ability_pos[1] * self.size[1] / 2.))

				elif inx >= len(ability):
					self.ability_i[str(inx)].source = self.img_blank

	def update_trigger(self):
		tr = [1, 0]
		for inx in reversed(range(self.max_trigger)):
			if inx < len(self.trigger) and self.cid != "player":
				if self.trigger[inx] == "":
					self.trigger_i[str(inx)].source = self.img_none
				else:
					if len(self.trigger) > 1:
						self.trigger_i[str(tr[inx])].source = f"atlas://{img_in}/other/{self.trigger[inx]}"
					else:
						self.trigger_i[str(inx)].source = f"atlas://{img_in}/other/{self.trigger[inx]}"
			else:
				if inx == 0 and self.cid != "player":
					self.trigger_i[str(inx)].source = self.img_none
				else:
					self.trigger_i[str(inx)].source = self.img_blank

	def update_soul(self):
		self.clean_c("soul")
		with self.canvas:
			self.soul_t = self.soul
			for item in self.soul_c:
				if item[1] != 0:
					self.soul_t += item[0]

			if self.soul_t<0:
				self.soul_t = 0

			if self.soul_t > self.max_soul:
				for inx in range(self.max_soul):
					self.soul_i[str(inx)].source = self.img_blank

				self.soul_i["0"].source = self.img_soul
				self.soul_l.text = f"x{self.soul_t}"
			elif self.soul_t <= self.max_soul:
				for x in range(self.max_soul):
					if x + 1 <= self.soul_t:
						self.soul_i[str(x)].source = self.img_soul
					else:
						self.soul_i[str(x)].source = self.img_blank
				self.soul_l.text = ""
			else:
				for x in range(self.max_soul):
					self.soul_i[str(x)].source = self.img_blank
				self.soul_l.text = ""
			self.soul_l.refresh()
			self.soul_r.texture = self.soul_l.texture
			self.soul_r.size = self.soul_l.texture.size

	def clean_c(self, t=""):
		to_remove = []
		if t == "power":
			text = self.power_c
		elif t == "cost":
			text = self.cost_c
		elif t == "level":
			text = self.level_c
		elif t == "soul":
			text = self.soul_c
		elif t == "text":
			text = self.text_c
		elif t == "name":
			text = self.name_c
		elif t == "colour":
			text = self.colour_c
		elif t == "trait":
			text = self.trait_c
		else:
			text = []
			texts = (self.power_c, self.cost_c, self.level_c, self.soul_c, self.text_c, self.colour_c, self.trait_c, self.name_c)

		if t == "":
			for item in texts:
				for item1 in item:
					if item1[1] == 0:
						to_remove.append((item, item1))

			for itemr in to_remove:
				itemr[0].remove(itemr[1])
		else:
			for item in text:
				if item[1] == 0:
					to_remove.append(item)
			for itemr in to_remove:
				text.remove(itemr)

	def selected(self, s=True):
		if s:
			self.select = True
			self.slc.source = self.img_select
		else:
			self.select = False
			self.slc.source = self.img_blank

	def stage_slc(self, s=True):
		if s:
			self.stage = True
			self.slc.source = f"atlas://{img_in}/other/select2"
		else:
			self.stage = False
			self.slc.source = self.img_blank


class CardEmpty:
	def __init__(self):
		self.ind = ""
		self.per = 1
		self.cid = ""
		self.name = ""
		self.jname = ""
		self.rarity = ""
		self.colour = []
		self.mcolour = ""
		self.colour_c = []
		self.card = ""
		self.trigger = ()
		self.text_o = ()
		self.jtext = ()
		self.level = 0
		self.cost = 0
		self.icon = ""
		self.power = 0
		self.soul = 0
		self.turn = 0
		self.trait = ()
		self.flavour = ""
		self.jflavour = ""
		self.jtrait = ()
		self.back = True
		self.movable = False
		self.status = ""
		self.pos_old = ""
		self.pos_new = ""
		self.owner = ""
		self.selected = False
		# self.selectable = False
		self.cost_c = []
		self.cost_t = 0
		self.power_c = []
		self.power_t = 0
		self.level_c = []
		self.level_t = 0
		self.soul_c = []
		self.soul_t = 0
		self.soul_i = {}
		self.text_c = []
		self.trait_c = []
		self.trait_t = []
		self.name_t = ""
		self.name_c = []

	def clean_c(self, t=""):
		to_remove = []
		if t == "power":
			text = self.power_c
		elif t == "cost":
			text = self.cost_c
		elif t == "level":
			text = self.level_c
		elif t == "soul":
			text = self.soul_c
		elif t == "text":
			text = self.text_c
		elif t == "colour":
			text = self.colour_c
		elif t == "name":
			text = self.name_c
		elif t == "trait":
			text = self.trait_c
		else:
			text = []
			texts = (self.power_c, self.cost_c, self.level_c, self.soul_c, self.text_c, self.colour_c, self.trait_c, self.name_c)

		if t == "":
			for item in texts:
				for item1 in item:
					if item1[1] == 0:
						to_remove.append((item, item1))

			for itemr in to_remove:
				itemr[0].remove(itemr[1])
		else:
			for item in text:
				if item[1] == 0:
					to_remove.append(item)
			for itemr in to_remove:
				text.remove(itemr)

	def reduce_c(self, text="", waiting=False):
		if text == "":
			c = (self.power_c, self.cost_c, self.level_c, self.soul_c, self.text_c, self.colour_c, self.trait_c, self.name_c)
		else:
			if text == "power":
				text = self.power_c
			elif text == "cost":
				text = self.cost_c
			elif text == "level":
				text = self.level_c
			elif text == "soul":
				text = self.soul_c
			elif text == "text":
				text = self.text_c
			elif text == "name":
				text = self.name_c
			elif text == "colour":
				text = self.colour_c
			elif text == "trait":
				text = self.trait_c

			c = (text,)

		for tt in c:
			for item in tt:
				if not waiting and item[1] > 0:
					item[1] -= 1
				elif waiting and item[1] >= 0:
					item[1] = 0
