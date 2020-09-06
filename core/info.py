from kivy.uix.image import AsyncImage
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView

from core.button import Button
from core.datapath import *
from core.label import Label
from core.markreplace import markreplace


class Info(Popup):
	pinfo_lst = ("id", "card", "colour", "level", "cost", "power", "soul", "trigger", "icon", "trait", "text",
	             "flavour")
	pinfo_c = {"text_o": "", "colour_o": "", "level_o": "", "cost_o": "", "power_o": "", "soul_o": "", "trait_o": "",
	           "text_c": "", "colour_c": "", "level_c": "", "cost_c": "", "power_c": "", "soul_c": "", "trait_c": ""}
	lang = {"nameE": "", "nameJ": "", "traitj": "", "traite": "", "texte": "", "textj": "", "flavoure": "",
	        "flavourj": "", "coloure": "", "colourj": "", "carde": "",
	        "cardj": ""}  # "triggere":"","triggerj":"","icone":"","iconj":""
	popdict = {"name": "Card Name", "id": "Card No.", "rarity": "Rarity", "card": "Type", "colour": "Colour",
	           "level": "Level", "cost": "Cost", "power": "Power", "soul": "Soul", "trigger": "Trigger",
	           "trait": "Attribute", "text": "Text", "flavour": "Flavor Text", "icon": "Card Icon", "stock": "Pool",
	           "door": "Door", "salvage": "Door", "gate": "Gate"}
	jap = {"Red": "赤", "Blue": "青", "Yellow": "黄", "Green": "緑", "Character": "キャラ", "Event": "イベント",
	       "Climax": "クライマックス", "Purple": "紫"}
	cgst06 = ["mf_s13_072", "im_se04_23", "im_s07_090", "im_s07_054", "mk_s11_076"]
	reverse_fix = ["im_se04_24"]
	reverse_fix_btn = ["im_s07_051"]

	def __init__(self, pad=1, card=(100, 100), **kwargs):
		super(Info, self).__init__(**kwargs)
		self.title_font = f"{font_in}/{font}"
		self.markreplace = markreplace["markreplace"]
		self.anchors_text = markreplace["anchors"]
		self.marksquare = markreplace["square"]
		self.set_only = markreplace["set_only"]
		self.inx = 10
		self.inx1 = 0
		self.pad = pad
		self.card = card
		self.auto_dismiss = False
		self.title_align = "center"
		self.size_hint = (None, None)
		self.cls_btn = Button(size_hint=(None, None), text="Close", on_release=self.close,
		                      size=(self.card[0] * 2.5, self.card[1] / 2.))
		self.jap_btn = Button(size_hint=(None, None), text="JAP", on_release=self.change_lang, cid="jp")
		self.eng_btn = Button(size_hint=(None, None), text="ENG", on_release=self.change_lang, cid="en")
		self.img_card = AsyncImage(source=f"atlas://{img_in}/other/back", size=(self.card[0] * 4, self.card[1] * 4),
		                           allow_stretch=True, size_hint=(None, None))
		self.fsize = self.card[1] / 3. * 0.6
		self.label = {}
		for item in self.pinfo_lst:
			if item in self.pinfo_lst[-2:]:
				sized = (self.card[0] * 7.2, self.card[1] / 3.)
				textsize = (self.card[0] * 7, None)
			else:
				if "trait" in item or "id" in item:
					sized = (self.card[0] * 3, self.card[1] / 3.)
					textsize = (self.card[0] * 3, None)
				else:
					sized = (self.card[0] * 1.5, self.card[1] / 3.)
					textsize = sized

			if item in self.pinfo_lst[:-2] or item[:-2] in self.pinfo_lst[-2:]:
				self.label[item] = Label(text="　", color=(1, 1, 1, 1), text_size=textsize, font_size=self.fsize,
				                         halign='center', valign='middle', markup=True, size=sized,
				                         size_hint=(None, None))
				self.label[f"{item}_btn"] = Button(text=self.popdict[item], size=sized, size_hint=(None, None),
				                                   cid=item, on_press=self.actual)
			else:
				self.label[f"{item}_btn"] = Button(text=self.popdict[item], size=sized, size_hint=(None, None),
				                                   cid=item, on_press=self.actual)
				self.label[item] = Label(text="　", color=(1, 1, 1, 1), text_size=textsize, font_size=self.fsize,
				                         valign='middle', markup=True, size_hint=(None, None), size=sized)

		self.jap_wrap = [False, []]
		self.wrap = self.card[0] * 7
		self.label["wrap"] = Label(text="", font_size=self.fsize, valign='middle', markup=True, size_hint=(None, None))
		self.sct_size = (self.card[0] * 7.1, self.card[1] * 7.7)
		self.sct = RelativeLayout(size_hint=(1, 1))
		self.sct1 = RelativeLayout(size_hint=(1, None), size=(self.card[0] * 7.1, self.card[1] * 7.1))  # ,  # 7
		self.scv = ScrollView(do_scroll_x=False, size_hint=(1, None), size=(self.card[0] * 7.1, self.card[1] * 7.1))
		self.lang_btn = Button(size_hint=(None, None), size=(self.card[1] / 2, self.card[1] / 2), text="E", cid="lang",
		                       on_press=self.change_lang)

		self.size = (self.sct_size[0] * 1.1, self.sct_size[1] + self.title_size + self.separator_height)
		self.content = self.sct
		self.sct.center = self.content.center
		self.pos_c = self.sct_size[0] / 2

		self.scv.size = (self.sct_size[0] + self.pad, self.card[1] * 6)
		self.sct.add_widget(self.scv)
		self.sct.add_widget(self.cls_btn)
		self.sct.add_widget(self.lang_btn)
		self.cls_btn.center_x = self.pos_c
		self.cls_btn.y = self.card[1] * 0.15
		self.lang_btn.y = self.card[1] * 0.15
		self.lang_btn.x = self.sct_size[0] - self.lang_btn.size[0]  # -self.card[1] * 0.15

		self.scv.y = self.cls_btn.y * 2 + self.cls_btn.size[1]
		self.scv.add_widget(self.sct1)

		self.sct1.add_widget(self.img_card)
		for item in reversed(self.pinfo_lst):
			self.sct1.add_widget(self.label[item])
			self.sct1.add_widget(self.label[f"{item}_btn"])
		self.test = {}
		for nx in range(1, 5):
			self.test[str(nx)] = Label(text="　" * nx, font_size=self.fsize, valign='middle')
			self.test[str(nx)].texture_update()

		self.img_anchors = {}
		for nx in range(10):
			self.img_anchors[str(nx)] = Image(source=f"atlas://{img_in}/other/blank", size=(
				self.test["1"].texture.size[0] * 1.05, self.test["1"].texture.size[1] * 1.05),
			                                  allow_stretch=True, size_hint=(None, None))
			self.sct1.add_widget(self.img_anchors[str(nx)])

	def close(self, *arg):
		self.dismiss()

	def change_lang(self, btn):
		if not self.jap_wrap[0]:
			self.jap_wrap[0] = True
			for nx in range(len(self.jap_wrap[1])):
				if self.jap_wrap[1][nx] == "" or self.jap_wrap[1][nx] == "None" or self.jap_wrap[1][nx] is None:
					continue
				else:
					text = self.jap_wrap[1][nx].replace("】 ", "】").replace("］ ", "］").replace(" 【", "【").replace(" ［",
					                                                                                             "［").replace(
							"） ", "）").replace(" （", "（")
					text = self.replaceMultiple(text)
					if nx > 0:
						self.lang["textj"] += f"\n[color=ffffff]{text}[/color]"
					else:
						self.lang["textj"] = f"[color=ffffff]{text}[/color]"

		if btn.cid == "lang":
			if btn.text == "E":
				self.lang_btn.text = "J"
			elif btn.text == "J":
				self.lang_btn.text = "E"
			self.title = self.lang[f"name{self.lang_btn.text.lower()}"]
			self.label["card"].text = self.lang[f"card{self.lang_btn.text.lower()}"]
			self.label["colour"].text = self.lang[f"colour{self.lang_btn.text.lower()}"]
			self.label["flavour"].text = self.lang[f"flavour{self.lang_btn.text.lower()}"]
			self.label["text"].text = self.lang[f"text{self.lang_btn.text.lower()}"]
			self.label["trait"].text = self.lang[f"trait{self.lang_btn.text.lower()}"]
			for item in self.label:
				if "_btn" not in item:
					self.label[item].texture_update()
					self.label[item].size = self.label[item].texture.size
			self.content_size()
			self.scv.scroll_y = 1

	def import_data(self, card, annex):
		self.inx = 10
		self.lang_btn.text = "E"
		ability = []
		for key in self.lang:
			self.lang[key] = "[color=ffffff]　[/color]"

		for label in self.pinfo_lst:
			self.label[label].text = "[color=ffffff]　[/color]"

		for label in self.pinfo_c:
			if "_c" in label:
				self.pinfo_c[label] = "[color=ffff00]　[/color]"
			else:
				self.pinfo_c[label] = "[color=ffffff]　[/color]"

		self.jap_wrap = [False, list(card.jtext_o)]
		self.title = card.name_t
		self.lang["namee"] = card.name_t
		self.lang["namej"] = card.jname

		if card.img_file in annex:
			self.img_card.source = f"atlas://{img_in}/annex/{card.img_file}"
		else:
			self.img_card.source = f"atlas://{img_ex}/main/{card.img_file}"

		self.label["id"].text = f"[color=ffffff]{card.cid} {card.rarity}[/color]"
		if any(end in card.cid for end in
		       ("EN", "-E", "-TE", "-PE", "/WX", "/SX")) and "DC/W01" not in card.cid and "LB/W02" not in card.cid:
			self.lang_btn.disabled = True
		else:
			self.lang_btn.disabled = False
		self.label["card"].text = f"[color=ffffff]{card.card}[/color]"
		self.lang["cardj"] = f"[color=ffffff]{self.jap[card.card]}[/color]"
		self.lang["carde"] = f"[color=ffffff]{card.card}[/color]"

		# self.pinfo_c["level_o"] = "[color=ffffff] [/color]"
		# self.pinfo_c["level_c"] = "[color=ffff00] [/color]"
		# self.pinfo_c["cost_o"] = "[color=ffffff] [/color]"
		# self.pinfo_c["cost_c"] = "[color=ffff00] [/color]"
		# self.pinfo_c["power_o"] = "[color=ffffff] [/color]"
		# self.pinfo_c["power_c"] = "[color=ffff00] [/color]"
		# self.pinfo_c["soul_o"] = "[color=ffffff] [/color]"
		# self.pinfo_c["soul_c"] = "[color=ffff00] [/color]"

		for item in range(len(card.colour)):
			if card.colour[item] == "" or card.colour[item] == "None" or card.colour[item] is None:
				continue
			else:
				colour = card.colour[item][0].upper() + card.colour[item][1:]
				if item == 0:
					self.pinfo_c["colour_o"] = f"[color=ffffff]{colour}[/color]"
					self.pinfo_c["colour_c"] = f"[color=ffff00]{colour}[/color]"
				elif not card.colour[item] in card.mcolour:
					self.pinfo_c["colour_c"] += f" - [color=ffff00]{colour}[/color]"
				elif card.colour[item] in card.mcolour:
					self.pinfo_c["colour_o"] += f" - [color=ffffff]{colour}[/color]"
					self.pinfo_c["colour_c"] += f" - [color=ffff00]{colour}[/color]"
		self.lang["coloure"] = str(self.pinfo_c["colour_o"])
		self.lang["colourj"] = f"[color=ffffff]{self.jap[card.mcolour]}[/color]"

		if "Climax" not in self.label["card"].text:
			self.pinfo_c["level_o"] = f"[color=ffffff]{card.level}[/color]"
			self.pinfo_c["level_c"] = f"[color=ffff00]{card.level_t}[/color]"
			self.pinfo_c["cost_o"] = f"[color=ffffff]{card.cost}[/color]"
			self.pinfo_c["cost_c"] = f"[color=ffff00]{card.cost_t}[/color]"
			if "Event" not in self.label["card"].text:
				self.pinfo_c["power_o"] = f"[color=ffffff]{card.power}[/color]"
				self.pinfo_c["power_c"] = f"[color=ffff00]{card.power_t}[/color]"
				self.pinfo_c["soul_o"] = f"[color=ffffff]{card.soul}[/color]"
				self.pinfo_c["soul_c"] = f"[color=ffff00]{card.soul_t}[/color]"

		# self.pinfo_c["trait_o"] = "[color=ffffff] [/color]"
		# self.pinfo_c["trait_c"] = "[color=ffff00] [/color]"
		for item in range(len(card.trait_t)):
			if card.trait_t[item] == "" or card.trait_t[item] == "None" or card.trait_t[item] is None:
				continue
			else:
				if item == 0:
					self.pinfo_c["trait_o"] = f"[color=ffffff]{card.trait_t[item]}[/color]"
					self.pinfo_c["trait_c"] = f"[color=ffff00]{card.trait_t[item]}[/color]"
				elif not card.trait_t[item] in card.trait:
					self.pinfo_c["trait_c"] += f" - [color=ffff00]{card.trait_t[item]}[/color]"
				elif card.trait_t[item] in card.trait:
					self.pinfo_c["trait_o"] += f" - [color=ffffff]{card.trait_t[item]}[/color]"
					self.pinfo_c["trait_c"] += f" - [color=ffff00]{card.trait_t[item]}[/color]"
		self.lang["traite"] = str(self.pinfo_c["trait_o"])

		for nx in range(len(card.jtrait)):
			if card.jtrait[nx] == "" or card.jtrait[nx] == "None" or card.jtrait[nx] is None:
				continue
			else:
				if nx > 0:
					self.lang["traitj"] += f" - [color=ffffff]{card.jtrait[nx]}[/color]"
				else:
					self.lang["traitj"] = f"[color=ffffff]{card.jtrait[nx]}[/color]"

		for item in range(len(card.trigger)):
			if card.trigger[item] == "" or card.trigger[item] == "None" or card.trigger[item] is None:
				continue
			else:
				if item == 0:
					self.label["trigger"].text = f"[color=ffffff][anchor=i{card.trigger[item]}{self.inx}1]　[/color]"
					self.inx += 1
				# self.lang["triggerj"] = f"[color=ffffff]{self.jap[card.trigger[item]]}[/color]"
				else:
					self.label["trigger"].text += f" [color=ffffff][anchor=i{card.trigger[item]}{self.inx}1]　[/color]"
					self.inx += 1
		# self.lang["triggerj"] = f" [color=ffffff]{self.jap[card.trigger[item]]}[/color]"

		# self.lang["triggere"] = str(self.label["trigger"].text)

		# self.pinfo_c["text_o"] = "[color=ffffff] [/color]"
		# self.pinfo_c["text_c"] = "[color=ffff00] [/color]"
		for item in range(len(card.text_c)):
			if card.text_c[item] == "" or card.text_c[item] == "None" or card.text_c[item] is None:
				continue
			else:
				text = self.replaceMultiple(card.text_c[item][0])
				if item == 0:
					if card.text_c[item][0] in card.text_o:
						self.pinfo_c["text_o"] = f"[color=ffffff]{text}[/color]"
						if not self.pinfo_c["text_o"]:
							self.pinfo_c["text_o"] = "[color=ffffff] [/color]"
						self.pinfo_c["text_c"] = self.pinfo_c["text_o"]
					else:
						self.pinfo_c["text_o"] = "[color=ffffff] [/color]"
						self.pinfo_c["text_c"] = f"[color=ffff00]{text}[/color]"
				elif card.text_c[item][1] == -3 or card.text_c[item][1] == -2:
					continue
				elif not card.text_c[item][0] in card.text_o:
					# if f"[color=ffff00]{text}[/color]" not in self.pinfo_c["text_c"]:
					if card.text_c[item][0] not in ability:
						ability.append(card.text_c[item][0])
						self.pinfo_c["text_c"] += f"\n[color=ffff00]{text}[/color]"
					elif card.text_c[item][0] in ability:
						if card.text_c[item][0].startswith("[AUTO]") and not card.text_c[item][0].lower().startswith(
								"[auto] encore ["):
							# elif f"[color=ffff00]{text}[/color]" in self.pinfo_c["text_c"] and "] encore [" not in card.text_c[item][0].lower() and "[AUTO]" in card.text_c[item][0]:
							self.pinfo_c["text_c"] += f"\n[color=ffff00]{text}[/color]"
				else:
					self.pinfo_c["text_o"] += f"\n[color=ffffff]{text}[/color]"
					self.pinfo_c["text_c"] += f"\n[color=ffffff]{text}[/color]"

		self.lang["texte"] = str(self.pinfo_c["text_o"])

		# self.label["flavour"].text = "[color=ffffff] [/color]"
		if not card.flavour == "" or "none" not in card.flavour.lower() or card.flavour is not None:
			self.label["flavour"].text = f"[color=ffffff]{card.flavour}[/color]"
			self.lang["flavoure"] = f"[color=ffffff]{card.flavour}[/color]"
			self.lang["flavourj"] = f"[color=ffffff]{card.jflavour}[/color]"

		# self.label["icon"].text = "[color=ffffff] [/color]"
		if card.icon:
			if card.icon == "Clock":
				cc = "alarm"
			else:
				cc = card.icon.lower()
			self.label["icon"].text = f"[color=ffffff][anchor=i{cc}{self.inx}1]　[/color]"
			self.inx += 1

		for item in self.pinfo_lst:
			if f"{item}_c" in self.pinfo_c:
				self.label[item].text = self.pinfo_c[f"{item}_o"]

			self.label[item].texture_update()
			self.label[item].size = self.label[item].texture.size

		self.content_size()
		self.scv.scroll_y = 1
		self.open()

	def replaceMultiple(self, mStr, btn=False):
		self.inx1 = 0
		for elem in self.marksquare:
			if elem in mStr:
				mStr = mStr.replace(elem, self.marksquare[elem])
		if "ISTAND phase" in mStr:
			mStr = mStr.replace("ISTAND phase", "stand phase")
		if "ISTAND Phase" in mStr:
			mStr = mStr.replace("ISTAND Phase", "stand phase")
		mStr = mStr.replace("&", "&amp;").replace("[", "&bl;").replace("]", "&br;")
		for elem in self.markreplace:
			if elem in mStr:
				mStr = mStr.replace(elem, self.markreplace[elem])

		for ss in self.set_only:
			if ss in mStr:
				mStr = mStr.replace(ss, f"{{{self.set_only[ss]}}}")
		if "(" in mStr:
			ita = f"({mStr.split('(')[-1]}"
			if ")\"" not in ita:
				mStr = mStr.replace(ita, f"[color=999999]{ita}[/color]")
		if "（" in mStr:
			ita = f"（{mStr.split('（')[-1]}"
			if "）」" not in ita:
				mStr = mStr.replace(ita, f"[color=999999]{ita}[/color]")

		if "{" in mStr:
			mStr = mStr.replace("{", "(").replace("}", ")")

		for item in self.anchors_text:
			if "[" in item:
				item1 = item[1:-1]
			else:
				item1 = item
			for nx in range(mStr.count(item)):
				if self.inx1 < 1 and f"\"{item}" in mStr and self.img_card.source.split("/")[-1] in self.cgst06:
					mStr = mStr.replace(f"\"{item}",
					                    f"\n\"[anchor={item1.lower()}{self.inx}{self.anchors_text[item]}]{'　' * self.anchors_text[item]} ",
					                    1)
					self.inx1 += 1
				# mStr = mStr.replace(f"\"{item}", f" [anchor=cgst06]\" [anchor={item1.lower()}{self.inx}{self.anchors_text[item]}]{'　' * self.anchors_text[item]} ",1)
				elif self.inx1 < 1 and not btn and "IREVERSE" in item and self.img_card.source.split("/")[
					-1] in self.reverse_fix:
					mStr = mStr.replace(item,
					                    f"\n[anchor={item1.lower()}{self.inx}{self.anchors_text[item]}]{'　' * self.anchors_text[item]} ",
					                    1)
					self.inx1 += 1
				# mStr = mStr.replace(f"\"{item}", f" [anchor=cgst06]\" [anchor={item1.lower()}{self.inx}{self.anchors_text[item]}]{'　' * self.anchors_text[item]} ",1)
				elif self.inx1 < 1 and btn and "IREVERSE" in item and self.img_card.source.split("/")[
					-1] in self.reverse_fix_btn:
					mStr = mStr.replace(item,
					                    f"\n[anchor={item1.lower()}{self.inx}{self.anchors_text[item]}]{'　' * self.anchors_text[item]} ",
					                    1)
					self.inx1 += 1
				# mStr = mStr.replace(f"\"{item}", f" [anchor=cgst06]\" [anchor={item1.lower()}{self.inx}{self.anchors_text[item]}]{'　' * self.anchors_text[item]} ",1)
				else:
					mStr = mStr.replace(item,
					                    f"[anchor={item1.lower()}{self.inx}{self.anchors_text[item]}]{'　' * self.anchors_text[item]} ",
					                    1)
				self.inx += 1
		if "の" in mStr:
			mStr = self.wrap_jap(mStr)
		# xx = 0
		# inx = -10
		# sk = False
		# jt = []
		# ss = 0
		# for tx in mainString:
		# 	inx +=10
		# 	ss+=10
		# 	if " " in tx:
		# 		xx+=5
		# 		continue
		# 	if "\"" in tx:
		# 		sk= True
		# 		ss = 0
		# 	elif "[" in tx:
		# 		sk = True
		# 	elif "]" in tx:
		# 		sk = False
		# 		continue
		# 	if sk and ss==10:
		# 		sk = False
		# 		continue
		#
		# 	if not sk:
		# 		if xx % 250 == 0:
		# 			if mainString[int(inx/10)-1] in "－＋+-0123456789":
		# 				for nx in reversed(range(int(inx/10)-1)):
		# 					if mainString[nx] not in "－＋+-0123456789":
		# 						jt.append(nx)
		# 						xx = nx*10
		# 						break
		# 			else:
		# 				jt.append(int(inx/10)-1)
		# 		if tx in "0123456789":
		# 			xx += 5
		# 		else:
		# 			xx += 10
		# for sx in reversed(jt):
		# 	if sx == 0:
		# 		continue
		# 	mainString = mainString[:sx] + "\n" + mainString[sx:]

		return mStr

	def replaceImage(self):
		qty = len(self.label["text"].anchors) + len(self.label["trigger"].anchors) + len(self.label["icon"].anchors)
		if qty < len(self.img_anchors):
			for nx in range(len(self.img_anchors), qty):
				self.img_anchors[str(nx)] = Image(source=f"atlas://{img_in}/other/blank", size_hint=(None, None), size=(
					self.test1.texture.size[0] * 1.05, self.test1.texture.size[1] * 1.05), allow_stretch=True)
				self.sct1.add_widget(self.img_anchors[str(nx)])

		for itt in self.img_anchors:
			self.img_anchors[itt].y = -self.card[1] * 20

		i1 = 0
		for item in self.label["text"].anchors:
			# if "cgst06" in item:
			# 	continue
			self.img_anchors[str(i1)].size = (
				self.test[item[-1]].texture.size[0] * 1.05, self.test[item[-1]].texture.size[1] * 1.05)
			self.img_anchors[str(i1)].source = f"atlas://{img_in}/other/{item[:-3]}"
			# if self.img_card.source in self.cgst06 and "auto" in item:
			# 	self.img_anchors[str(i1)].pos = (self.label["text"].anchors["cgst06"][0] + self.label["text"].x + self.card[1] / 10,
			#                                  self.label["text"].size[1] - self.card[1] / 45 -
			#                                  self.label["text"].anchors["cgst06"][1] - self.test[item[-1]].texture.size[1] +
			#                                  self.label["text"].y)
			# else:
			self.img_anchors[str(i1)].pos = (
			self.label["text"].anchors[item][0] + self.label["text"].x + self.card[1] / 30,
			self.label["text"].size[1] - self.card[1] / 45 -
			self.label["text"].anchors[item][1] - self.test[item[-1]].texture.size[1] +
			self.label["text"].y)
			i1 += 1

		for item in self.label["trigger"].anchors:
			self.img_anchors[str(i1)].size = (
				self.test[item[-1]].texture.size[0] * 1.05, self.test[item[-1]].texture.size[1] * 1.05)
			self.img_anchors[str(i1)].source = f"atlas://{img_in}/other/{item[:-3]}"
			self.img_anchors[str(i1)].pos = (self.label["trigger"].anchors[item][0] + self.label["trigger"].x,
			                                 self.label["trigger"].size[1] - self.card[1] / 45 -
			                                 self.label["trigger"].anchors[item][1] -
			                                 self.test[item[-1]].texture.size[1] + self.label["trigger"].y)
			i1 += 1
		for item in self.label["icon"].anchors:
			self.img_anchors[str(i1)].size = (
				self.test[item[-1]].texture.size[0] * 1.05, self.test[item[-1]].texture.size[1] * 1.05)
			self.img_anchors[str(i1)].source = f"atlas://{img_in}/other/{item[:-3]}"
			self.img_anchors[str(i1)].pos = (self.label["icon"].anchors[item][0] + self.label["icon"].x,
			                                 self.label["icon"].size[1] - self.card[1] / 45 -
			                                 self.label["icon"].anchors[item][1] -
			                                 self.test[item[-1]].texture.size[1] + self.label["icon"].y)
			i1 += 1

	def content_size(self):
		scty = 0
		col = 0
		x1 = 0
		x2 = 0
		y1 = 0
		for item in reversed(self.pinfo_lst):
			if item in self.pinfo_lst[-2:]:
				self.label[item].x = self.pad
				self.label[item].y = scty
				scty += self.label[item].size[1]
				self.label[f"{item}_btn"].x = 0
				self.label[f"{item}_btn"].y = scty
				scty += self.label[f"{item}_btn"].size[1]
				scty += self.pad
			elif item == "trait" or item == "id":
				if item == "trait":
					self.img_card.x = 0
					self.img_card.y = scty + self.pad / 2

					x1 = self.img_card.size[0] + self.card[0] / 10 * 2
					x2 = x1 + self.card[0] * 1.5
				elif item == "id":
					scty += self.pad / 2

				self.label[item].x = x1
				self.label[item].y = scty
				scty += self.label[item].size[1]
				self.label[f"{item}_btn"].x = x1
				self.label[f"{item}_btn"].y = scty
				scty += self.label[f"{item}_btn"].size[1]
			else:
				if col % 2 == 0:
					scty += self.pad / 2
					xpos = x2
					y1 = int(scty)
				else:
					xpos = x1
					scty += self.label[item].size[1]
					scty += self.label[f"{item}_btn"].size[1]

				self.label[f"{item}_btn"].x = xpos
				self.label[item].x = xpos
				self.label[item].y = y1
				self.label[f"{item}_btn"].y = self.label[item].size[1] + y1
				col += 1

		self.replaceImage()
		self.sct1.size = (self.sct.size[0], scty)
		self.scv.scroll_y = 1

	def actual(self, btn):
		if f"{btn.cid}_o" in self.pinfo_c and self.lang_btn.text == "E":
			if self.label[btn.cid].text == self.pinfo_c[f"{btn.cid}_o"]:
				self.label[btn.cid].text = self.pinfo_c[f"{btn.cid}_c"]
			else:
				self.label[btn.cid].text = self.pinfo_c[f"{btn.cid}_o"]

			self.label[btn.cid].texture_update()
			self.label[btn.cid].size = self.label[btn.cid].texture.size
			self.content_size()

	# self.scv.scroll_y = 1

	def wrap_jap(self, sttr):
		lines = []
		sttr = sttr.replace("\n", " ")
		sstr = ""
		for x in range(len(sttr)):
			if len(sttr) <= 0:
				break
			self.label["wrap"].text = sttr
			self.label["wrap"].texture_update()
			if self.label["wrap"].texture.size[0] > self.wrap:
				line = self.check_wrap(sttr)
			else:
				line = sttr
			lines.append(line)
			sttr = sttr.replace(line, "")

		for l in range(len(lines)):
			if l == 0:
				sstr = f"{lines[l]}"
			else:
				sstr += f"\n{lines[l]}"
		return sstr

	def check_wrap(self, sttr=""):
		for s in reversed(range(len(sttr))):
			if sttr[s] in "\\[\"]'abcdefghijklmnopqrstuvwxyz()0123456789+-;&":
				continue
			elif sttr[s] in ")]｝〕〉》」』】〙〗〟｠»＋－。.・、:;,‐゠–〜? ! ‼ ⁇ ⁈ ⁉":
				continue
			elif sttr[s] in "ヽヾーァィゥェォッャュョヮヵヶぁぃぅぇぉっゃゅょゎゕゖㇰㇱㇲㇳㇴㇵㇶㇷㇸㇹㇺㇻㇼㇽㇾㇿ々〻":
				continue
			self.label["wrap"].text = sttr[:s]
			self.label["wrap"].texture_update()
			if self.label["wrap"].texture.size[0] > self.wrap:
				continue
			else:
				return sttr[:s]