import logging
from datetime import date
from functools import partial
from math import ceil
from random import shuffle, choice, sample
from urllib.parse import urlencode

import certifi as cfi
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image, AsyncImage
from kivy.uix.progressbar import ProgressBar
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.switch import Switch
from kivy.uix.widget import Widget
from kivy.uix.widget import WidgetException
from plyer import email

from core.ai import AI
from core.bar import Bar
from core.button import Button
from core.card import Card, CardImg, CardEmpty
from core.imgbutton import ImgButton
from core.info import Info
from core.janken import Janken
from core.label import Label
from core.joke import Joketext
from core.labelbtn import Labelbtn
from core.mat import Mat
from core.popup import Popup
from core.recycle import RV
from core.spinner import Spinner
from core.stackspacer import StackSpacer
from core.textinput import TextInput
from core.togglebutton import ToggleButton
from core.var import *

# from android.permissions import check_permission, Permission #@android

logging.basicConfig(filename=f"{data_ex}/log", level=logging.DEBUG)
__author__ = "totuccio"
__copyright__ = "Copyright © 2020 totuccio"
__version__ = "0.24.0"


class GameMech(Widget):
	fields = (
		"Library", "Memory", "Waiting", "Center0", "Center1", "Center2", "Back0", "Back1", "Climax", "Clock", "Level",
		"Stock", "Res")
	labelfield = ("Library", "Memory", "Stock", "Waiting")
	stage = ("Center", "Back")
	m = (2, 1, 0)

	def __init__(self, **kwargs):
		super(GameMech, self).__init__(**kwargs)
		self.size = (Window.width, Window.height)
		self.c = 0
		self.anx = 0
		self.room = None
		self.infob = None
		self.infot = None
		self.req = {}
		self.download = False
		self.btn_clear = None
		self.event_move = False
		self.network = {}
		self.sd = {}
		self.gd = {}
		self.cd = {}
		self.cpop = {}
		self.dpop = {}
		self.mpop = {}
		self.iach = {}
		self.test = {}
		self.temp = []
		self.mat = {"1": {"mat": None, "field": {}, "id": "mat", "per": 1},
		            "2": {"mat": None, "field": {}, "id": "mat", "per": 1}}
		self.net = network_init()
		self.poptext = False
		self.pd = pdata_init()
		self.gd = gdata_init()
		self.emptycards = ("", "00", "sspace")

		with self.canvas:
			self.rect = Rectangle(source=f"atlas://{img_in}/other/blank", pos=(-Window.width * 2, -Window.height * 2))
			self.rect1 = Rectangle(source=f"atlas://{img_in}/annex/dc_w00_00",
			                       pos=(-Window.width * 2, -Window.height * 2))
			if exists(f"{img_ex}/main.atlas"):
				try:
					self.rect2 = Rectangle(
							source=f"atlas://{img_ex}/main/{next(iter(se['main']['a'][next(iter(se['main']['a']))]))}",
							pos=(-Window.width * 2, -Window.height * 2))
				except StopIteration:
					pass
		Clock.schedule_once(self.main_menu)

	def start_setting(self, *args):
		self.parent.parent.version = __version__
		self.scale_mat()
		self.mat["1"]["mat"] = Mat("1", self.mat["1"]["per"])
		self.mat["2"]["mat"] = Mat("2", self.mat["2"]["per"])
		self.mat["1"]["mat"].import_mat(sp[self.mat["1"]["id"]], self.mat["1"]["per"])
		self.mat["2"]["mat"].import_mat(sp[self.mat["2"]["id"]], self.mat["2"]["per"])

		self.cd["00"] = Card("", self.sd["card"], "0", self.mat["1"]["per"])
		# self.cd["00"].import_data(sc["MK/S11-E101"])
		# Clock.schedule_once(self.popup_deck_start)
		# Clock.schedule_once(self.popup_multi_info_start)
		# Clock.schedule_once(self.start_setting1, ability_dt)

		self.start_setting1()

	def start_setting1(self, *args):
		self.gd["eng_card"] = [s for s in sorted(se["main"]["c"]) if any(end in s for end in (
			"EN", "-E", "-TE", "-PE", "/WX", "/SX")) and "DC/W01" not in s and "LB/W02" not in s]
		self.gd["jap_card"] = [s for s in sorted(se["main"]["c"]) if s not in self.gd["eng_card"]]

		self.sd["touch_down"] = None
		self.rect1.source = f"atlas://{img_in}/other/blank"
		self.icon = {}
		self.sd["popup"] = {}
		self.sd["popup"]["popup"] = Popup()
		self.sd["popup"]["sspace"] = StackSpacer(o=self.sd["card"])
		self.sd["popup"]["icon"] = ImgButton(source=f"atlas://{img_in}/other/arrow", size=self.sd["card"],
		                                     card=self.sd["card"], cid="icon")
		self.sd["popup"]["p_sct"] = RelativeLayout()

		self.sd["popup"]["stack"] = StackLayout(size_hint_y=None, orientation="lr-tb", padding=self.sd["padding"] / 2,
		                                        spacing=self.sd["padding"])
		self.sd["popup"]["stack"].bind(minimum_height=self.sd["popup"]["stack"].setter('height'))
		self.sd["popup"]["p_scv"] = ScrollView(do_scroll_x=False, size_hint=(1, None))
		self.sd["popup"]["popup"].bind(on_dismiss=self.show_continue_btn, on_open=self.show_popup)

		self.sd["debug"] = {}
		self.sd["debug"]["switch"] = Switch(active=False)
		self.sd["debug"]["switch"].bind(active=self.debug)
		self.sd["debug"]["label"] = Label(text="Debug")
		self.sd["debug"]["box"] = BoxLayout(orientation='horizontal')
		self.sd["debug"]["box"].add_widget(self.sd["debug"]["label"])
		self.sd["debug"]["box"].add_widget(self.sd["debug"]["switch"])
		self.sd["debug"]["btn"] = {}

		self.sd["joke"] = {}
		self.sd["joke"]["1"] = Joketext()
		self.sd["joke"]["2"] = Joketext()

		self.field_btn = {}
		self.field_label = {}

		self.gd["inx"] = 0
		self.sd["label"] = {}

		for label in phases:
			xpos = Window.width / float(len(phases))
			self.sd["label"][label] = Label(text=label, color=(.5, .5, .5, 1.), font_size=self.sd["card"][1] / 6)
			self.sd["label"][label].center_y = Window.height / 2
			self.sd["label"][label].center_x = -Window.width
			# self.sd["label"][label].center_x = xpos / 2. + xpos * self.gd["inx"]
			self.add_widget(self.sd["label"][label])
		# self.gd["inx"] += 1

		# add steps labels
		self.gd["inx"] = 0
		for label in steps:
			self.sd["label"][label] = Label(text=label, color=(.5, .5, .5, 1.), font_size=self.sd["card"][1] / 6)
			self.sd["label"][label].center_y = Window.height / 2
			self.sd["label"][label].center_x = -Window.width
			self.add_widget(self.sd["label"][label])
		# self.gd["inx"] += 1

		# add bar
		self.sd["t_bar"] = Bar(size=(Window.width, self.sd["card"][1] / 2))
		self.sd["b_bar"] = Bar(size=(Window.width, self.sd["card"][1] / 2))

		self.add_widget(self.mat["2"]["mat"])
		self.add_widget(self.mat["1"]["mat"])

		self.add_widget(self.sd["t_bar"])
		self.add_widget(self.sd["b_bar"])

		self.sd["t_bar"].y = Window.height - self.sd["t_bar"].size[1]
		self.sd["b_bar"].x = -Window.width * 2
		self.sd["t_bar"].x = -Window.width * 2

		self.mat["1"]["mat"].x = -Window.width * 2
		self.mat["1"]["mat"].y = -Window.height * 2

		self.mat["2"]["mat"].y = -Window.height * 2
		self.mat["2"]["mat"].x = -Window.width * 2
		self.mat["2"]["mat"].reverse()

		for player in list(self.pd.keys()):
			self.sd["joke"][player].size = (self.mat[player]["mat"].size[0], self.mat[player]["mat"].size[1])
			# self.sd["joke"][player].joke.size = self.sd["joke"][player].size
			# self.sd["joke"][player].joke.text_size = (self.sd["joke"][player].size[0]*0.95,self.sd["joke"][player].size[1]*0.95)
			self.sd["joke"][player].x = -Window.width
			self.sd["joke"][player].y = -Window.height

			self.mat[player]["mat"].add_widget(self.sd["joke"][player])

		self.popup_text_start()

		self.sd["btn"] = {}
		self.sd["sbtn"] = {}
		self.sd["sbact"] = {}
		self.sd["menu"] = {}
		self.sd["btn"]["end"] = Button(size_hint=(None, None), text="End ",  # line_height=0.95,
		                               on_release=self.end_current_phase, halign='center')
		self.sd["btn"]["end_eff"] = Button(size_hint=(None, None), text="Continue Effect",  # line_height=0.95,
		                                   on_release=self.end_current_ability, halign='center')
		self.sd["btn"]["end_attack"] = Button(size_hint=(None, None), text="Attack Phase",  # line_height=0.95,
		                                      on_release=self.end_to_attack, halign='center')
		self.sd["btn"]["end_phase"] = Button(size_hint=(None, None), text="Skip Attack", on_release=self.end_to_end,
		                                     halign='center')  # line_height=0.95)
		self.sd["btn"]["continue"] = Button(size_hint=(None, None), text="Continue", on_release=self.show_popup,
		                                    cid="cont", halign='center')  # line_height=0.95)
		self.sd["btn"]["yes_btn"] = Button(size_hint=(None, None), text="Yes", on_release=self.confirm_result, cid="1")
		self.sd["btn"]["no_btn"] = Button(size_hint=(None, None), text="No", on_release=self.confirm_result, cid="0")
		self.sd["btn"]["close_btn"] = Button(size_hint=(None, None), text="Close", on_release=self.close_popup)
		self.sd["btn"]["field_btn"] = Button(size_hint=(None, None), text="Show Field", on_release=self.show_field)
		self.sd["btn"]["down_again"] = Button(size_hint=(None, None), text="Download", on_release=self.down_open)
		self.sd["btn"]["effect_btn"] = Button(size_hint=(None, None), text="End Effect", on_release=self.end_effect)

		self.sd["btn"]["top_btn"] = Button(size_hint=(None, None), text="Top deck", on_release=self.look_top, cid="t")
		self.sd["btn"]["bottom_btn"] = Button(size_hint=(None, None), text="Bottom", on_release=self.look_top,
		                                      cid="b")
		self.sd["btn"]["check_btn"] = Button(size_hint=(None, None), text="Close", on_release=self.look_top, cid="t")
		self.sd["btn"]["draw_btn"] = Button(size_hint=(None, None), text="Look next", on_release=self.look_draw,
		                                    cid="d")
		# self.sd["btn"]["reorder_btn"] = Button(size_hint=(None, None), text="Look Next", on_release=self.look_draw,
		#                                     cid="r")
		self.sd["btn"]["Look_btn"] = Button(size_hint=(None, None), text="End Effect", on_release=self.look_top,
		                                    cid="l")
		self.sd["btn"]["reshuffle_btn"] = Button(size_hint=(None, None), text="Reshuffle", on_release=self.reflev,
		                                         cid="ref")
		self.sd["btn"]["levelup_btn"] = Button(size_hint=(None, None), text="Level up", on_release=self.reflev,
		                                       cid="lev")
		self.sd["btn"]["encore_Stock3"] = Button(size_hint=(None, None), text="③", on_release=self.encore, cid="Stock3")
		self.sd["btn"]["encore_Stock2"] = Button(size_hint=(None, None), text="②", on_release=self.encore, cid="Stock2")
		self.sd["btn"]["encore_Stock1"] = Button(size_hint=(None, None), text="①", on_release=self.encore, cid="Stock1")
		self.sd["btn"]["encore_Character"] = Button(size_hint=(None, None), text="Character Encore",
		                                            on_release=self.encore, cid="Character")
		self.sd["btn"]["encore_Trait"] = Button(size_hint=(None, None), text="Trait Encore",
		                                        on_release=self.encore, cid="Trait")
		self.sd["btn"]["encore_Clock"] = Button(size_hint=(None, None), text="Clock Encore",
		                                        on_release=self.encore, cid="Clock")
		self.sd["btn"]["label"] = Label(text="test", text_size=(
			(self.sd["card"][0] + self.sd["padding"]) * 0.9 * starting_hand, None), font_size=self.sd["card"][1] / 5,
		                                size_hint=(1, None), markup=True)  # ,valign="middle")
		# self.sd["btn"]["label"].bind(texture_size=self.sd["btn"]["label"].setter('texture_size'))
		self.sd["btn"]["Mulligan_btn"] = Button(size_hint=(None, None), text="End Mulligan",
		                                        on_release=self.mulligan_done)
		self.sd["btn"]["M_all_btn"] = Button(size_hint=(None, None), text="Discard All",
		                                     on_release=self.mulligan_all)
		self.sd["btn"]["Clock_btn"] = Button(size_hint=(None, None), text="End Clock",
		                                     on_release=self.clock_phase_done)
		self.sd["btn"]["Discard_btn"] = Button(size_hint=(None, None), text="End Effect", on_release=self.discard)
		self.sd["btn"]["Levelup_btn"] = Button(size_hint=(None, None), text="Level Up", on_release=self.level_up_done)
		self.sd["btn"]["Hand_btn"] = Button(size_hint=(None, None), text="0 card left",
		                                    on_release=self.hand_limit_done)
		self.sd["btn"]["Search_btn"] = Button(size_hint=(None, None), text="End Search", on_release=self.search)
		self.sd["btn"]["Salvage_btn"] = Button(size_hint=(None, None), text="End Salvage", on_release=self.salvage)
		self.sd["btn"]["Change_btn"] = Button(size_hint=(None, None), text="End Chnage", on_release=self.change)
		self.sd["btn"]["Shuffle_btn"] = Button(size_hint=(None, None), text="End Effect",
		                                       on_release=self.shuffle_ability)
		self.sd["btn"]["Counter_btn"] = Button(size_hint=(None, None), text="End Counter",
		                                       on_release=self.counter_done)
		self.sd["btn"]["Marker_btn"] = Button(size_hint=(None, None), text="End Effect", on_release=self.marker)
		self.sd["btn"]["Add_btn"] = Button(size_hint=(None, None), text="Add", on_release=self.building_btn,
		                                   cid="adding")
		self.sd["btn"]["Addcls_btn"] = Button(size_hint=(None, None), text="Close", on_release=self.building_btn,
		                                      cid="close")
		self.sd["btn"]["cstock_btn"] = Button(size_hint=(None, None), text="End Effect", on_release=self.cstock)
		self.sd["btn"]["revive_btn"] = Button(size_hint=(None, None), text="End Effect", on_release=self.revive)
		self.sd["btn"]["Encore_btn"] = Button(size_hint=(None, None), text="End Encore", on_release=self.encore_done)
		self.sd["btn"]["show_all_btn"] = Button(size_hint=(None, None), text="Show All",
		                                        on_release=self.popup_filter)
		self.sd["btn"]["show_info_btn"] = Button(size_hint=(None, None), text="i", on_press=self.show_info_btn,
		                                         cid="info_btn")

		self.sd["btn"]["filter_add"] = BoxLayout(orientation="vertical", size_hint=(1, None))
		self.sd["btn"]["filter_add"].size = (Window.width, self.sd["card"][1])
		self.sd["menu"]["btn"] = Button(size_hint=(None, None), text="Menu", on_release=self.show_menu,
		                                cid="menu", halign='center')
		self.sd["menu"]["restart"] = Button(size_hint=(1, 1), text="Restart Game", on_release=self.start_game)
		self.sd["menu"]["change"] = Button(size_hint=(1, 1), text="Change Decks",
		                                   on_release=self.popup_network_slc, cid="single")
		self.sd["menu"]["main"] = Button(size_hint=(1, 1), text="Main Menu", on_release=self.gotomainmenu)
		self.sd["menu"]["close"] = Button(size_hint=(1, 1), text="Close", on_release=self.menu_dismiss)
		self.sd["menu"]["space"] = Label(text="", size_hint=(1, 0.3))
		self.sd["btn"]["draw_upto"] = Button(size_hint=(None, None), text="Draw card", on_release=self.draw_upto_btn)
		self.sd["btn"]["ablt_info"] = Button(size_hint=(None, None), text="Info", on_release=self.info_ability_pop)

		for item in list(self.sd["btn"].keys()):
			if any(item == btn for btn in
			       ("end", "continue", "end_attack", "end_phase", "ablt_info", "draw_upto", "end_eff")):
				self.sd["btn"]["end"].y = -Window.height * 2
			else:
				self.sd["popup"]["p_sct"].add_widget(self.sd["btn"][item])

		self.sd["btn"]["end"].size = (Window.width / 5., self.sd["b_bar"].size[1])
		self.sd["btn"]["end"].text_size = (Window.width / 5. * 0.9, None)  # self.sd["b_bar"].size[1]*0.9)
		# self.sd["btn"]["end"].font_size = self.sd["btn"]["end"].size[1]/2*0.75
		self.sd["btn"]["end_eff"].size = self.sd["btn"]["end"].size
		self.sd["btn"]["end_eff"].x = Window.width - self.sd["btn"]["end"].size[0]
		self.sd["btn"]["end_eff"].text_size = self.sd["btn"]["end"].text_size
		# self.sd["btn"]["end_eff"].font_size = self.sd["btn"]["end"].size[1]/2
		self.sd["btn"]["ablt_info"].size = self.sd["btn"]["end"].size
		self.sd["btn"]["end_attack"].size = self.sd["btn"]["end"].size
		self.sd["btn"]["end_attack"].text_size = self.sd["btn"]["end"].text_size
		# self.sd["btn"]["end_attack"].font_size = self.sd["btn"]["end"].size[1]/2
		self.sd["btn"]["end_phase"].size = self.sd["btn"]["end"].size
		self.sd["btn"]["end_phase"].text_size = self.sd["btn"]["end"].text_size
		# self.sd["btn"]["end_phase"].font_size = self.sd["btn"]["end"].size[1]/2
		self.sd["btn"]["draw_upto"].size = (Window.width / 5. * 2.5, self.sd["b_bar"].size[1])
		self.sd["btn"]["draw_upto"].x = Window.width / 5. * 1.25
		self.sd["btn"]["close_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
		self.sd["btn"]["field_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)

		self.sd["popup"]["popup"].content = self.sd["popup"]["p_sct"]
		self.sd["popup"]["p_sct"].add_widget(self.sd["popup"]["p_scv"])
		self.sd["popup"]["p_scv"].add_widget(self.sd["popup"]["stack"])

		self.sd["btn"]["flvl"] = Spinner(text="Lvl -", values=("Lvl -", "Lvl 0", "Lvl 1", "Lvl 2", "Lvl 3"),
		                                 size_hint=(1, 1))
		self.sd["btn"]["fcolour"] = Spinner(text="Colour", values=("Colour", "Yellow", "Green", "Red", "Blue"),
		                                    size_hint=(1, 1))
		self.sd["btn"]["ftype"] = Spinner(text="Type", values=("Type", "Character", "Event", "Climax"),
		                                  size_hint=(1, 1))
		self.sd["btn"]["ftrait"] = Spinner(text="Trait", values=("Trait",), size_hint=(1, 1))
		self.fav = BoxLayout(orientation="horizontal")
		for item in ("lvl", "colour", "type", "trait"):
			self.fav.add_widget(self.sd["btn"][f"f{item}"])
			self.sd["btn"][f"f{item}"].bind(text=self.popup_filter_add)

		self.sd["btn"]["filter_add"].add_widget(self.fav)
		self.sd["btn"]["ftext"] = TextInput(text="", size_hint=(4, 1.2))  # ,focus=True)
		self.sd["btn"]["ftextl"] = Label(text="Name")
		self.fav1 = BoxLayout(orientation="horizontal")
		self.fav1.add_widget(self.sd["btn"]["ftextl"])
		self.fav1.add_widget(self.sd["btn"]["ftext"])
		self.sd["btn"]["ftext"].bind(text=self.popup_filter_add)
		self.sd["btn"]["filter_add"].add_widget(self.fav1)

		for n in range(3):
			for t in ("d", "f", "s"):
				if t == "d":
					text = "Direct"
				elif t == "f":
					text = "Frontal"
				elif t == "s":
					text = "Side"

				self.sd["btn"][f"a{t}{n}"] = Button(text=text, cid=f"{t}{n}",
				                                    on_release=self.attack_declaration)
				self.sd["btn"][f"a{t}{n}"].size = (self.sd["card"][0], self.sd["card"][1] / 4.)
				self.sd["btn"][f"a{t}{n}"].pos = (-Window.width, -Window.height)
				self.sd["btn"][f"a{t}{n}"].disabled = False

				try:
					self.parent.add_widget(self.sd["btn"][f"a{t}{n}"])
				except WidgetException:
					continue

		for item in list(self.sd["btn"].keys()):
			self.sd["btn"][item].y = -Window.height

		self.sd["menu"]["wl"] = Label(text="You ", size_hint=(1, 0.8))
		self.sd["menu"]["wl_box"] = BoxLayout(orientation="vertical", spacing=self.sd["padding"])
		self.sd["menu"]["wl_box1"] = BoxLayout(orientation="vertical", spacing=self.sd["padding"])
		# self.sd["menu"]["wl_box"].add_widget(self.sd["menu"]["wl"])
		self.sd["menu"]["wl_box1"].add_widget(self.sd["menu"]["restart"])
		self.sd["menu"]["wl_box1"].add_widget(self.sd["menu"]["change"])
		self.sd["menu"]["wl_box1"].add_widget(self.sd["menu"]["main"])
		self.sd["menu"]["wl_box1"].add_widget(self.sd["menu"]["space"])
		self.sd["menu"]["wl_box1"].add_widget(self.sd["menu"]["close"])
		self.sd["menu"]["wl_box"].add_widget(self.sd["menu"]["wl_box1"])

		self.sd["cpop_slc"] = ""
		self.sd["cpop_press"] = []
		self.sd["cpop_pressing"] = None
		# add popup variables
		# self.janken = (False, "")
		self.ai = AI("2")

		self.sd["menu"]["popup"] = Popup(size=(Window.width * 0.6, Window.height * 0.4))
		self.sd["menu"]["popup"].title = "Menu"
		self.sd["menu"]["popup"].auto_dismiss = False
		self.sd["menu"]["popup"].content = self.sd["menu"]["wl_box"]

		self.sd["other"]["popup"] = Popup()
		self.sd["other"]["sct"] = RelativeLayout(size_hint=(1, 1))
		self.sd["other"]["scv"] = ScrollView(do_scroll_x=False, size_hint=(1, None))
		self.sd["other"]["about"] = Label(text="", valign="middle", halign="center",
		                                  text_size=(Window.width * 0.7, None), size_hint=(1, None), markup=True)
		self.sd["other"]["about"].bind(on_ref_press=self.ref_press)
		self.sd["other"]["close"] = Button(size_hint=(None, None), text="Close", on_release=self.other_dismiss)
		self.sd["other"]["copy"] = Button(size_hint=(None, None), text="Copyright", on_release=self.copy_open)

		self.sd["other"]["copy_box"] = BoxLayout(orientation="vertical")
		self.sd["other"]["copy_scv"] = ScrollView(do_scroll_x=False, size_hint=(1, 1))
		self.sd["other"]["copy_btn"] = Button(size_hint=(1, 0.05), text="Close", on_release=self.copy_dismiss)
		self.sd["other"]["copy_lb"] = Label(text="", valign="middle", halign="center",
		                                    text_size=(Window.width * 0.9, None), size_hint=(1, None))

		self.sd["other"]["copy_box"].add_widget(self.sd["other"]["copy_scv"])
		self.sd["other"]["copy_scv"].add_widget(self.sd["other"]["copy_lb"])
		self.sd["other"]["copy_box"].add_widget(self.sd["other"]["copy_btn"])
		self.sd["other"]["sct"].add_widget(self.sd["other"]["scv"])
		self.sd["other"]["scv"].add_widget(self.sd["other"]["about"])
		self.sd["other"]["sct"].add_widget(self.sd["other"]["close"])
		self.sd["other"]["sct"].add_widget(self.sd["other"]["copy"])
		# self.sd["other"]["sct"].add_widget(self.sd["other"]["down"])

		self.sd["other"]["popup"].content = self.sd["other"]["sct"]
		self.sd["other"]["popup"].title = "About"
		self.cardinfo = Info(pad=self.sd["padding"], card=self.sd["card"])
		self.cardinfo.bind(on_dismiss=self.info_pop_close)
		self.cardinfo.bind(on_open=self.info_pop_open)
		self.popup_deck_start()
		self.popup_network_start()
		self.deck_create()
		self.popup_multi_info_start()
		self.field_btn_fill()
		self.act_ability_create()
		self.janken_setting()
		self.hand_btn_create()
		self.replaceImage_test()
		self.create_field_label()
		self.stack_btn_ability(5)
		self.stack_btn_act(3)

	def ref_press(self, inst, value):
		if value == "email":
			email.send(recipient="tsws@totuccio.com", subject="", text="", create_chooser=False)

	def copy_dismiss(self, *args):
		self.decks["sets"].dismiss()

	def copy_open(self, *args):
		self.decks["sets"].size = (Window.width, Window.height)
		self.decks["sets"].content = self.sd["other"]["copy_box"]
		self.sd["other"]["copy_btn"].size = (Window.width, self.sd["card"][1] / 2)
		self.sd["other"]["copy_lb"].text = ""
		for text in se["copyright"]:
			self.sd["other"]["copy_lb"].text += f"{text}\n"
		self.sd["other"]["copy_lb"].texture_update()
		self.sd["other"]["copy_lb"].height = self.sd["other"]["copy_lb"].texture.size[1]
		self.sd["other"]["copy_scv"].scroll_y = 1
		self.decks["sets"].title = "Copyright"
		self.decks["sets"].open()

	def down_open(self, *args):
		self.sd["popup"]["popup"].dismiss()
		self.popup_clr()
		# for btn in self.sd["main_btn"]:
		# 	btn.disabled = True
		self.down_popup()

	# self.deck_title_pop("down")

	def down_popup(self, *args):
		self.multi_info["popup"].title = "Download"

		yscv = self.sd["card"][1] * 4 + self.sd["padding"] * 1.5
		yscatm = yscv + self.sd["card"][1] * 1.6
		ypop = yscatm + self.multi_info["popup"].title_size + self.multi_info["popup"].separator_height

		if ypop > Window.height:
			ypop = Window.height * 0.9
			yscatm = ypop - self.multi_info["popup"].title_size - self.multi_info["popup"].separator_height
			yscv = yscatm - self.sd["card"][1] * 0.75

		self.multi_info["download"].size = (self.sd["card"][0] * 6 + self.sd["padding"] * 2, yscv)
		self.multi_info["popup"].size = (self.sd["card"][0] * 6 + self.sd["padding"] * 2, ypop)

		self.multi_info["close"].center_x = self.multi_info["popup"].size[0] / 2. - self.sd["card"][0] / 2 + self.sd[
			"padding"] * 2
		self.multi_info["close"].y = self.sd["padding"] * 1.5
		self.multi_info["scv"].y = -Window.height * 2
		self.multi_info["download"].y = self.sd["padding"] * 3 + self.sd["card"][1] / 2
		self.multi_info["t"] = True
		self.multi_info["popup"].open()

	def down_popup_btn(self, btn):
		self.deck_title_pop(f"down_{btn.cid}")

	def down_data(self, request, *args):
		self.mcancel_create_bar1.value += 10
		item = request.url.split("/")[-2]
		temp = request.url.split("/")[-1]
		to_remove = []

		if "-d" in temp:
			ftemp = f"{data_ex}/{temp}"
			with open(ftemp, "wb") as write:
				write.write(request.result)
		elif "-" in temp:
			ftemp = f"{img_ex}/{temp}"
			with open(ftemp, "wb") as write:
				write.write(request.result)

		with open(ftemp, "rb") as f:
			hash_md5 = md5()
			for chunk in iter(lambda: f.read(4096), b""):
				hash_md5.update(chunk)

			if hash_md5.hexdigest() != se["check"][item][temp]:
				# print(item, temp, hash_md5.hexdigest())
				to_remove.append(ftemp)

		for item in to_remove:
			remove(item)

		self.mcancel_create_bar1.value += 1
		# for item in self.req:
		# 	if not self.req[item].is_finished:
		# if all(self.req[item].is_finished for item in self.req):
		if self.mcancel_create_bar1.value == self.mcancel_create_bar1.max and not self.gd["confirm_trigger"] and not \
				self.gd["cancel_down"]:
			self.mcreate_popup.dismiss()
			self.download = True
			self.gd["confirm_trigger"] = "Restart"
			self.gd["confirm_var"] = {"c": "Restart"}
			Clock.schedule_once(self.confirm_popup, popup_dt)

	def down_data_cnc(self, request, *args):
		# self.mcancel_create_bar1.value += 10
		item = request.url.split("/")[-2]
		temp = request.url.split("/")[-1]
		to_remove = []

		if "-d" in temp:
			ftemp = f"{data_ex}/{temp}"
		elif "-" in temp:
			ftemp = f"{img_ex}/{temp}"

		if exists(ftemp):
			with open(ftemp, "rb") as f:
				hash_md5 = md5()
				for chunk in iter(lambda: f.read(4096), b""):
					hash_md5.update(chunk)

				if hash_md5.hexdigest() != se["check"][item][temp]:
					# print(item, temp, hash_md5.hexdigest())
					to_remove.append(ftemp)

		for item in to_remove:
			remove(item)

		# self.mcancel_create_bar1.value += 1
		# for item in self.req:
		# 	if not self.req[item].is_finished:
		# if all(self.req[item].is_finished for item in self.req):

		if self.mcancel_create_bar1.value == self.mcancel_create_bar1.max and self.gd["cancel_down"]:
			self.sd["text"]["popup"].dismiss()
		# for btn in self.sd["main_btn"]:
		# 	btn.disabled = False

	def reset(self, *args):
		App.get_running_app().stop()
		Window.close()

	# def atlas_make_init(self,*args):
	# 	atlas_make()

	def other_open(self, *args):
		self.sd["other"]["popup"].size = (Window.width * 0.8, Window.height * 0.8)
		self.sd["other"]["close"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2)
		self.sd["other"]["copy"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2)
		# self.sd["other"]["down"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2)
		self.sd["other"]["scv"].size = (
			Window.width * 0.8, Window.height * 0.7 - self.sd["padding"] * 6 - self.sd["card"][1] * 1)

		self.sd["other"]["close"].center_x = Window.width * 0.8 / 2 - self.sd["padding"]
		self.sd["other"]["copy"].center_x = Window.width * 0.8 / 2 - self.sd["padding"]
		# self.sd["other"]["down"].center_x = Window.width * 0.8 / 2 - self.sd["padding"]
		self.sd["other"]["close"].y = self.sd["padding"] * 1.5
		self.sd["other"]["copy"].y = self.sd["padding"] * 3 + self.sd["card"][1] / 2
		# self.sd["other"]["down"].y = self.sd["padding"] * 4.5 + self.sd["card"][1]
		self.sd["other"]["scv"].y = self.sd["padding"] * 4.5 + self.sd["card"][1]
		self.sd["other"]["about"].text = f"Version {__version__}\n\nCreated by\n{__author__}\n\n"
		for text in se["about"]:
			self.sd["other"]["about"].text += f"{text}\n"
		self.sd["other"]["about"].texture_update()
		self.sd["other"]["about"].height = self.sd["other"]["about"].texture.size[1]
		self.sd["other"]["scv"].scroll_y = 1
		self.sd["other"]["popup"].open()

	def other_dismiss(self, *args):
		self.sd["other"]["popup"].dismiss()

	def info_pop_close(self, *args):
		self.gd["info_p"] = False

	def info_pop_open(self, *args):
		self.gd["info_p"] = True

	def janken_setting(self):
		width = self.sd["padding"] * 2 + self.sd["card"][0]
		height = self.sd["padding"] * 2 + self.sd["card"][1]
		self.sd["janken"] = {}
		self.sd["janken"]["popup"] = Popup()
		self.sd["janken"]["popup"].title = "Rock Paper Scissor"
		self.sd["janken"]["stack"] = StackLayout(orientation="lr-tb", padding=self.sd["padding"] * 2,
		                                         spacing=self.sd["padding"] * 2)  # ,size_hint_y=None)
		self.sd["janken"]["stack"].size = (self.sd["padding"] * 6 + width * 3, height * 3 + self.sd["padding"] * 6)
		self.sd["janken"]["popup"].content = self.sd["janken"]["stack"]
		self.sd["janken"]["button"] = Button(size_hint=(1, None), text="Choose one", on_press=self.janken_done,
		                                     size=(width * 3, self.sd["card"][1]))
		self.sd["janken"]["button"].disabled = True

		for i in reversed(range(2)):
			for card in self.gd["janken_choice"]:
				self.sd["janken"][f"j{card}{i}"] = Janken(card, self.sd["card"])
				self.sd["janken"][f"j{card}{i}"].bind(on_release=self.janken_pick)

				if i > 0:
					self.sd["janken"][f"j{card}{i}"].reverse()
					self.sd["janken"][f"j{card}{i}"].show_back()
					self.sd["janken"][f"j{card}{i}"].disabled = True

		for item in ("jk1", "jp1", "js1", "button", "jk0", "jp0", "js0"):
			self.sd["janken"]["stack"].add_widget(self.sd["janken"][item])

		self.sd["janken"]["popup"].size = (self.sd["janken"]["stack"].size[0] + self.sd["padding"],
		                                   self.sd["janken"]["stack"].size[1] + self.sd["card"][1] / 2 + self.sd[
			                                   "padding"] + self.sd["janken"]["popup"].title_size + self.sd["janken"][
			                                   "popup"].separator_height)

	def gotomainmenu(self, *args):
		self.restart()
		self.gd["gg"] = False
		self.mat["1"]["mat"].x = -Window.width * 2
		self.mat["2"]["mat"].x = -Window.width * 2
		self.sd["b_bar"].x = -Window.width * 2
		self.sd["t_bar"].x = -Window.width * 2
		self.sd["debug"]["box"].x = -Window.width * 2
		self.sd["menu"]["btn"].x = -Window.width * 2
		# for label in phases + steps:
		# 	self.sd["label"][label].y = -Window.height * 2
		self.main_scrn.pos = (0, 0)
		self.main_scrn.disabled = False
		if self.gd["debug"]:
			self.sd["debug"]["switch"].active = False
		self.sd["menu"]["popup"].dismiss()

	def hand_btn_create(self):
		self.sd["hbtn_press"] = []
		for nx in range(1, 51):
			self.field_btn[f"Hand{nx}1"] = Button(text=f"{nx}1", cid=f"{nx}1", opacity=0, size=self.sd["card"],
			                                      pos=(-Window.width, -Window.height), on_press=self.hand_btn_info,
			                                      on_release=self.hand_btn_info_re)
			self.parent.add_widget(self.field_btn[f"Hand{nx}1"])

	def hand_btn_show(self, t=True):
		self.sd["hbtn_press"] = []
		if t:
			for inx in self.pd["1"]["Hand"]:
				self.field_btn[f"Hand{inx}"].pos = (
					self.cd[inx].x + self.mat["1"]["mat"].x, self.cd[inx].y + self.mat["1"]["mat"].y)
		else:
			for item in self.field_btn:
				if item.startswith("Hand"):
					self.field_btn[item].y = -Window.height * 2
					self.field_btn[item].size = self.sd["card"]

	def hand_btn_info_re(self, btn):
		self.gd["btn_release"] = True
		self.gd["btn_id"] = ""
		if self.infob is not None:
			self.infob.cancel()
			self.infob = None

	def hand_btn_info(self, btn):
		self.gd["btn_id"] = btn.cid
		self.gd["btn_release"] = False

		if self.decks["dbuilding"]:
			self.cardinfo.import_data(self.cd[btn.cid], annex_img)
		else:
			self.gd["btn_id"] = btn.cid
			self.sd["hbtn_press"].append(btn.cid)
			if len(self.sd["hbtn_press"]) >= info_popup_press:
				if all(prs == btn.cid for prs in self.sd["hbtn_press"][-info_popup_press:]):
					self.infob = Clock.schedule_once(self.info_start)
			else:
				self.infob = Clock.schedule_once(self.info_start, info_popup_dt)

	def act_ability_create(self, *args):
		self.gd["act"] = {}
		for player in list(self.pd.keys()):
			for i in ("b", "c"):
				for j in range(3):
					if i == "b" and j == 2:
						continue
					self.gd["act"][f"{i}{j}{player}"] = []
					self.gd["act"][f"x{i}{j}{player}"] = Button(size_hint=(None, None), cid=f"{i}{j}{player}",
					                                            on_release=self.act_ability_btn, text="ACT",
					                                            background_normal=f"atlas://{img_in}/other/action_bar",
					                                            size=(self.sd["card"][0], self.sd["card"][1] / 4.))
					self.parent.add_widget(self.gd["act"][f"x{i}{j}{player}"])
					self.gd["act"][f"x{i}{j}{player}"].x = -Window.width
					self.gd["act"][f"x{i}{j}{player}"].y = -Window.height

	def act_ability_fill(self, player):
		for ind in self.pd[player]["Center"] + self.pd[player]["Back"]:
			if ind != "":
				self.gd["act"][f"{self.cd[ind].pos_new[0].lower()}{self.cd[ind].pos_new[-1]}{ind[-1]}"] = []
				for item in self.cd[ind].text_c:
					if item[0].startswith(act_aility) and item[1] != 0 and "[counter]" not in item[0].lower() and item[
						1] > -9:
						self.gd["act"][f"{self.cd[ind].pos_new[0].lower()}{self.cd[ind].pos_new[-1]}{ind[-1]}"].append(
								item[0])

	def act_ability_show(self, hide=False, *args):
		for btn in self.gd["act"]:
			if btn.startswith("x"):
				self.gd["act"][btn].x = -Window.width
		if not hide and self.gd["phase"] == "Main" and self.gd["noact"][self.gd["active"]]:
			if "ACT" not in self.gd["ability_trigger"]:
				self.act_ability_fill(self.gd["active"])
				ss = []
				h = []
				my = []
				wr = []
				stage = self.pd[self.gd["active"]]["Center"] + self.pd[self.gd["active"]]["Back"]
				for cc in stage:
					ass = False
					for item in self.cd[cc].text_c:
						if item[0].startswith(cont_ability) and item[1] != 0 and item[1] > -9:
							if "[cont] assist" in item[0].lower():
								ass = True
								break
					ss.append((self.cd[cc].status, self.cd[cc].name, self.cd[cc].trait_t, ass))
				for indy in self.pd[self.gd["active"]]["Hand"]:
					h.append((self.cd[indy].card, self.cd[indy].name, self.cd[indy].trait_t))
				for indmy in self.pd[self.gd["active"]]["Memory"]:
					my.append((self.cd[indmy].card, self.cd[indmy].name, self.cd[indmy].trait_t))
				for indwr in self.pd[self.gd["active"]]["Waiting"]:
					wr.append((self.cd[indwr].card, self.cd[indwr].name, self.cd[indwr].trait_t))
				for ind in stage:
					if ind != "":
						self.gd["act_pop"][ind] = []
						key = f"{self.cd[ind].pos_new[0].lower()}{self.cd[ind].pos_new[-1]}{ind[-1]}"
						nn = stage.index(ind)
						m = 0
						if ind in self.pd[ind[-1]]["marker"]:
							m = len(self.pd[ind[-1]]["marker"][ind])

						for item1 in self.gd["act"][key]:
							if ab.req(a=item1, ss=ss, h=h, m=m, my=my, nn=nn, wr=wr,
							          x=len(self.pd[ind[-1]]["Stock"]) + len(self.gd["astock"][ind[-1]])):
								self.gd["act_pop"][ind].append(item1)
								self.gd["act"][f"x{key}"].disabled = False
								if self.gd["act"][f"x{key}"].x < 0:
									self.gd["act"][f"x{key}"].x = self.mat[ind[-1]]["field"][self.cd[ind].pos_new][0] + \
									                              self.mat[ind[-1]]["mat"].x
									self.gd["act"][f"x{key}"].y = self.mat[ind[-1]]["field"][self.cd[ind].pos_new][1] - \
									                              self.gd["act"][f"x{key}"].size[1] + self.mat[ind[-1]][
										                              "mat"].y

	def act_ability_btn(self, btn):
		self.gd["moveable"] = []
		self.gd["act"][f"x{btn.cid}"].disabled = True
		if btn.cid[0] == "b":
			field = "Back"
		elif btn.cid[0] == "c":
			field = "Center"
		ind = self.pd[f"{btn.cid[2]}"][field][int(btn.cid[1])]
		if len(self.gd["act_pop"][ind]) > 1:
			self.gd["act_poped"] = ind
			self.act_popup(ind)
		else:
			self.act_ability(ind, 0)

	def act_popup_btn(self, btn):
		self.act_ability(btn.cid[:-1], int(btn.cid[-1]))

	def act_ability(self, ind, n):
		self.sd["popup"]["popup"].dismiss()
		# card = self.cd[ind]
		# key = f"{card.pos_new[0].lower()}{card.pos_new[-1]}{ind[-1]}"
		self.gd["act_poped"] = ""
		self.gd["ability"] = self.gd["act_pop"][ind][n]
		self.gd["ability_trigger"] = f"ACT_{ind}"
		self.gd["confirm_trigger"] = str(self.gd["ability_trigger"])
		# self.gd["play_card"] = ""
		self.gd["choose"] = False
		self.gd["pay"] = ab.pay(a=self.gd["ability"])
		if self.gd["pay"]:
			self.gd["payed"] = False
		else:
			self.gd["payed"] = True

		if self.net["game"] and self.gd["active"] == "2":
			if self.net["act"][5]:
				Clock.schedule_once(self.pay_condition, ability_dt)
			else:
				Clock.schedule_once(self.play_card_done, ability_dt)
		else:
			if self.net["game"]:
				self.net["act"] = ["t", ind, n, [], [], 0]
			self.gd["astock_pop"] = False
			self.gd["confirm_var"] = {"ind": ind, "c": "ability"}
			Clock.schedule_once(self.confirm_popup, popup_dt)

	def act_popup(self, idm, *args):
		# self.gd["p_ind"] = ind
		self.popup_clr_button()
		self.gd["p_over"] = False
		self.gd["p_c"] = "auto"
		self.gd["popup_done"] = (True, False)
		self.sd["popup"]["popup"].title = "Available ACT abilities"
		self.sd["popup"]["stack"].do_scroll_y = False
		self.sd["popup"]["stack"].clear_widgets()

		height = self.sd["card"][1] + self.sd["padding"] * 0.75
		xscat = (self.sd["padding"] + self.sd["card"][0]) * (starting_hand + 1) + self.sd["padding"] * 2

		self.sd["btn"]["label"].text = "Choose which ACT ability to activate."
		self.sd["btn"]["label"].text_size = (xscat * 0.9, None)
		self.sd["btn"]["label"].texture_update()

		r = len(self.gd["act_pop"][idm])

		if r > 6:
			self.sd["popup"]["stack"].do_scroll_y = True
			yscv = height * (r - 0.5)
		elif r > 0:
			yscv = height * r
		else:
			yscv = height
		yscv += self.sd["padding"]

		yscat = yscv + self.sd["card"][1]
		title = self.sd["popup"]["popup"].title_size + self.sd["popup"]["popup"].separator_height + \
		        self.sd["btn"]["label"].texture.size[1] + self.sd["card"][1]
		ypop = yscat + title

		if ypop > Window.height:
			self.gd["p_over"] = True
			ypop = Window.height * 0.9
			yscat = ypop - title
			yscv = yscat - self.sd["card"][1] * 0.75

		self.sd["popup"]["p_scv"].size = (xscat, yscv)
		self.sd["popup"]["popup"].size = (xscat, ypop)

		self.stack_btn_act(len(self.gd["act_pop"][idm]))
		self.cardinfo.inx = 10
		inx = 0
		for item in self.gd["act_pop"][idm]:
			self.cpop[idm].selected(False)
			self.cpop[idm].update_text()
			if self.cpop[idm] in self.sd["popup"]["stack"].children:
				for xx in list(self.cpop.keys()):
					if xx.endswith("0") and self.cpop[xx] not in self.sd["popup"]["stack"].children:
						self.sd["popup"]["stack"].add_widget(self.cpop[xx])
						if self.cd[idm].cid == "player":
							self.cpop[xx].import_data("player")
						else:
							self.cpop[xx].import_data(sc[self.cd[idm].cid])
						break
			else:
				self.sd["popup"]["stack"].add_widget(self.cpop[idm])

			self.sd["sbact"][f"{inx}"].btn.text = self.cardinfo.replaceMultiple(item)
			self.sd["sbact"][f"{inx}"].btn.cid = f"{idm}{self.gd['act_pop'][idm].index(item)}"
			self.sd["sbact"][f"{inx}"].btn.texture_update()
			self.sd["sbact"][f"{inx}"].replaceImage()
			self.sd["popup"]["stack"].add_widget(self.sd["sbact"][f"{inx}"])
			inx += 1

		self.sd["btn"]["field_btn"].center_x = xscat / 2. - self.sd["card"][0] / 2 + self.sd["padding"] * 0.75
		self.sd["btn"]["field_btn"].y = self.sd["padding"] * 1.5

		# self.sd["btn"]["close_btn"].center_x = xscat / 2. - self.sd["card"][0] / 2 + self.sd["padding"] * 0.75
		# self.sd["btn"]["close_btn"].y = self.sd["padding"] * 1.5

		self.sd["popup"]["p_scv"].y = self.sd["btn"]["field_btn"].y * 2.5 + self.sd["btn"]["field_btn"].size[1]
		self.sd["popup"]["p_scv"].scroll_y = 1

		self.sd["btn"]["label"].pos = (
			self.sd["padding"] / 2.,
			self.sd["popup"]["p_scv"].y + self.sd["popup"]["p_scv"].size[1])  # -self.sd["padding"]*5)

		self.sd["popup"]["popup"].open()

	def pay_mstock(self, s="", *args):
		idm = self.gd["ability_trigger"].split("_")[1]

		if not self.gd["target"] and idm[-1] == "1" and not self.gd["mstock"]:
			f = []
			for asm in self.gd[f"{s}tock"][idm[-1]]:
				if asm[0] not in f:
					f.append(asm[0])
			self.gd["mstock"] = s
			self.gd["chosen"] = []
			self.gd["choose"] = False
			self.select_card(f=f)
			Clock.schedule_once(partial(self.popup_text, "mstock"))
		elif self.gd["target"]:
			if "as" in self.gd["target"] or "es" in self.gd["target"]:
				s = self.gd["target"].pop(0)
				ind = self.gd["target"].pop(0)
				if self.net["game"] and idm[-1] == "1":
					self.net["act"][3].append(s)
					self.net["act"][3].append(ind)
				self.remove_marker(ind, q=1, s=s)
				self.gd["pay"][self.gd["pay"].index("Stock") + 1] -= 1
				self.update_marker()
				self.check_cont_ability()
				Clock.schedule_once(self.pay_condition)

	def pay_stock(self, qty):
		if self.gd["rev"] and self.gd["rev_counter"] and "Counter" not in self.gd["phase"]:
			player = self.gd["active"]
		elif self.gd["rev"] or self.gd["rev_counter"]:
			player = self.gd["opp"]
		else:
			player = self.gd["active"]

		if self.gd["dismay"]:
			self.gd["dismay"] = False

		for stock in range(qty):
			if len(self.pd[player]["Stock"]) > 0:
				temp = self.pd[player]["Stock"].pop()
				self.mat[temp[-1]]["mat"].remove_widget(self.cd[temp])
				self.mat[temp[-1]]["mat"].add_widget(self.cd[temp])
				self.pd[temp[-1]]["Waiting"].append(temp)
				self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Waiting"], t="Waiting")
				self.stock_size(temp[-1])
				self.update_field_label()
		self.check_cont_ability()

	def pay_condition(self, *args):
		if not self.gd["payed"]:
			if self.gd["rev"] and self.gd["rev_counter"] and "Counter" not in self.gd["phase"]:
				player = self.gd["active"]
			elif self.gd["rev"] or self.gd["rev_counter"]:
				player = self.gd["opp"]
			else:
				player = self.gd["active"]

			card = self.cd[self.gd["ability_trigger"].split("_")[1]]
			if not self.gd["pay"]:
				self.gd["pay"] = ab.pay(a=self.gd["ability"])

			if self.net["game"] and self.gd["active"] == "2":
				self.gd["choose"] = True
				self.gd["target"] = self.net["act"][3]

			if "Stock" in self.gd["pay"]:
				ind = self.gd["pay"].index("Stock")
				if "ACT" in self.gd["ability_trigger"]:
					ss = "as"
				elif "Event" in self.gd["ability_trigger"]:
					ss = "es"
				else:
					ss = ""
				if ss != "" and len(self.gd[f"{ss}tock"][card.ind[-1]]) > 0:
					if card.ind[-1] == "1" and not self.gd["astock_pop"]:
						self.gd["astock_pop"] = True
						self.gd["confirm_trigger"] = f"{ss}tock_{self.gd['ability_trigger']}"
						self.gd["confirm_var"] = {"c": f"{ss}tock"}
						Clock.schedule_once(self.confirm_popup, popup_dt)
						return False
					elif self.gd["com"] and card.ind[-1] == "2":
						if len(self.gd[f"{ss}tock"][card.ind[-1]]) >= self.gd["pay"][ind + 1]:
							qty = self.gd["pay"][ind + 1]
						else:
							qty = len(self.gd[f"{ss}tock"][card.ind[-1]])
						for sm in range(qty):
							self.gd["target"].append(ss)
							self.gd["target"].append(self.gd[f"{ss}tock"][card.ind[-1]][sm][0])

					if self.gd["target"]:
						Clock.schedule_once(self.pay_mstock)
						return False
				self.pay_stock(self.gd["pay"][ind + 1])
				self.gd["mstock"] = ""
				self.gd["pay"].remove("Stock")
				Clock.schedule_once(self.pay_condition, move_dt_btw)
				return False
			if "Discard" in self.gd["pay"] or "MDiscard" in self.gd["pay"] or "HMemory" in self.gd["pay"]:
				if "Discard" in self.gd["pay"]:
					ind = self.gd["pay"].index("Discard")
				elif "MDiscard" in self.gd["pay"]:
					ind = self.gd["pay"].index("MDiscard")
				elif "HMemory" in self.gd["pay"]:
					ind = self.gd["pay"].index("HMemory")

				if self.gd["pay"][ind + 1] == 0:
					self.gd["target"] = [card.ind]
					self.gd["discard"] = 1
				elif self.gd["pay"][ind + 1] == -10:
					self.gd["target"] = [choice(self.pd[card.ind[-1]]["Hand"])]
					self.gd["discard"] = 1
				elif "any" in self.gd["pay"]:
					self.gd["discard"] = self.gd["pay"][ind + 1]
				elif self.gd["pay"][ind + 1] > 0:
					self.gd["discard"] = self.gd["pay"][ind + 1]
					if "Trait" in self.gd["pay"]:
						self.gd["search_type"] = f"Trait_{self.gd['pay'][self.gd['pay'].index('Trait') + 1]}"
					elif "Name=" in self.gd["pay"]:
						self.gd["search_type"] = f"Name=_{self.gd['pay'][self.gd['pay'].index('Name=') + 1]}"
					elif "Name" in self.gd["pay"]:
						self.gd["search_type"] = f"Name_{self.gd['pay'][self.gd['pay'].index('Name') + 1]}"
					# elif "Climax" in self.gd["pay"]:
					# 	self.gd["search_type"] = "Climax"
					else:
						self.gd["search_type"] = self.gd["pay"][ind + 2]
					self.gd["p_c"] = ""
				if "Discard" in self.gd["pay"]:
					self.gd["pay"].remove("Discard")
				elif "MDiscard" in self.gd["pay"]:
					self.gd["effect"].append("mdiscard")
					self.gd["pay"].remove("MDiscard")
				elif "HMemory" in self.gd["pay"]:
					self.gd["effect"].append("hmemory")
					self.gd["pay"].remove("HMemory")
				Clock.schedule_once(self.discard)
				return False

			if "Rest" in self.gd["pay"]:
				ind = self.gd["pay"].index("Rest")
				if self.gd["pay"][ind + 1] == 0:
					self.rest_card(card.ind)
					self.gd["pay"].remove("Rest")
					Clock.schedule_once(self.pay_condition, move_dt_btw)
					return False
				elif self.gd["pay"][ind + 1] >= 1:
					if card.ind[-1] == "2":
						self.pay_opponent()
						self.gd["pay"].remove("Rest")
						Clock.schedule_once(self.pay_condition, move_dt_btw)
						return False
					elif not self.gd["choose"]:
						Clock.schedule_once(self.pay_choose)
						return False
					else:
						for inx in range(len(self.gd["target"])):
							inm = self.gd["target"].pop()
							self.gd["targetpay"].append(inm)
							self.rest_card(inm)
						self.gd["choose"] = False
						self.gd["pay"].remove("Rest")
						Clock.schedule_once(self.pay_condition, move_dt_btw)
						return False

			if "RevealStock" in self.gd["pay"]:
				if not self.gd["resonance"][0]:
					self.gd["discard"] = 1
					self.gd["search_type"] = f"Name=_{self.gd['pay'][self.gd['pay'].index('RevealStock') + 1]}"
					self.gd["p_c"] = ""
					self.gd["resonance"][0] = True
					Clock.schedule_once(self.discard)
					return False
				elif self.gd["resonance"][0]:
					for rr in self.gd["resonance"][1]:
						self.send_to_stock(rr)
					self.gd["resonance"] = [False, []]
					self.gd["pay"].remove("RevealStock")
					Clock.schedule_once(self.pay_condition, move_dt_btw)
					return False
			if "Reveal" in self.gd["pay"]:
				self.gd["discard"] = 1
				self.gd["search_type"] = f"Name=_{self.gd['pay'][self.gd['pay'].index('Reveal') + 1]}"
				self.gd["p_c"] = ""
				self.gd["resonance"][0] = True
				self.gd["pay"].remove("Reveal")
				Clock.schedule_once(self.discard)
				return False
			if "ClockH" in self.gd["pay"]:
				ind = self.gd["pay"].index("ClockH")
				if self.gd["pay"][ind + 1] > 0:
					self.gd["discard"] = self.gd["pay"][ind + 1]
					if "Trait" in self.gd["pay"]:
						self.gd["search_type"] = f"Trait_{self.gd['pay'][self.gd['pay'].index('Trait') + 1]}"
					elif "Name=" in self.gd["pay"]:
						self.gd["search_type"] = f"Name=_{self.gd['pay'][self.gd['pay'].index('Name=') + 1]}"
					elif "Name" in self.gd["pay"]:
						self.gd["search_type"] = f"Name_{self.gd['pay'][self.gd['pay'].index('Name') + 1]}"
					elif "Climax" in self.gd["pay"]:
						self.gd["search_type"] = "Climax"
					else:
						self.gd["search_type"] = ""
					self.gd["p_c"] = ""
					self.gd["effect"].append("Clock")
					self.gd["pay"].remove("ClockH")
					Clock.schedule_once(self.discard)
					return False
			if "ClockS" in self.gd["pay"]:
				qty = self.gd["pay"][self.gd["pay"].index("ClockS") + 1]
				if qty == 0:
					self.send_to_clock(card.ind)
					self.gd["pay"].remove("ClockS")
					Clock.schedule_once(self.pay_condition, move_dt_btw)
					return False
				elif qty > 0:
					if not self.gd["choose"]:
						self.gd["pay_status"] = f"Select{qty}"
						Clock.schedule_once(self.pay_choose)
						return False
					else:
						for inx in range(len(self.gd["target"])):
							inm = self.gd["target"].pop()
							self.gd["targetpay"].append(inm)
							self.send_to_clock(inm)
						self.gd["choose"] = False
						self.gd["pay"].remove("ClockS")
						Clock.schedule_once(self.pay_condition, move_dt_btw)
						return False
			if "Hander" in self.gd["pay"]:
				if self.gd["pay"][self.gd["pay"].index("Hander") + 1] == 0:
					self.send_to_hand(card.ind)
				self.gd["pay"].remove("Hander")
				Clock.schedule_once(self.pay_condition, move_dt_btw)
				return False
			if "WDecker" in self.gd["pay"] or "Decker" in self.gd["pay"]:
				if "WDecker" in self.gd["pay"]:
					ind = self.gd["pay"].index("WDecker")
				elif "Decker" in self.gd["pay"]:
					ind = self.gd["pay"].index("Decker")
				if self.gd["pay"][ind + 1] > 0:
					self.gd["salvage"] = self.gd["pay"][ind + 1]
					if "Trait" in self.gd["pay"]:
						self.gd["search_type"] = f"Trait_{self.gd['pay'][self.gd['pay'].index('Trait') + 1]}"
					elif "Name=" in self.gd["pay"]:
						self.gd["search_type"] = f"Name=_{self.gd['pay'][self.gd['pay'].index('Name=') + 1]}"
					elif "Name" in self.gd["pay"]:
						self.gd["search_type"] = f"Name_{self.gd['pay'][self.gd['pay'].index('Name') + 1]}"
					# elif "Climax" in self.gd["pay"]:
					# 	self.gd["search_type"] = "Climax"
					else:
						self.gd["search_type"] = self.gd["pay"][ind + 2]
					self.gd["p_c"] = ""
				if "Decker" in self.gd["pay"]:
					self.gd["pay"].remove("Decker")
				elif "WDecker" in self.gd["pay"]:
					self.gd["effect"].append("wdecker")
					self.gd["pay"].remove("WDecker")
				Clock.schedule_once(self.salvage)
				return False

			if "Memory" in self.gd["pay"]:
				if self.gd["pay"][self.gd["pay"].index("Memory") + 1] == 0:
					self.send_to_memory(card.ind)
				self.gd["pay"].remove("Memory")
				Clock.schedule_once(self.pay_condition, move_dt_btw)
				return False
			if "Waiting" in self.gd["pay"]:
				if self.gd["pay"][self.gd["pay"].index("Waiting") + 1] == 0:
					self.send_to_waiting(card.ind)
					self.gd["pay"].remove("Waiting")
				elif self.gd["pay"][self.gd["pay"].index("Waiting") + 1] > 0:
					if not self.gd["choose"]:
						self.gd["pay_status"] = f"Select{self.gd['pay'][self.gd['pay'].index('Waiting') + 1]}"
						Clock.schedule_once(self.pay_choose)
						return False
					else:
						for inx in range(len(self.gd["target"])):
							inm = self.gd["target"].pop()
							self.gd["targetpay"].append(inm)
							self.send_to_waiting(inm)
						self.gd["choose"] = False
						self.gd["pay"].remove("Waiting")
						Clock.schedule_once(self.pay_condition, move_dt_btw)
						return False
			if "ClockL" in self.gd["pay"]:
				self.gd["damage_refresh"] = self.gd["pay"][self.gd["pay"].index("ClockL") + 1]
				self.gd["damageref"] = True
				self.gd["reshuffle_trigger"] = "pay"
				self.gd["pay"].remove("ClockL")
				Clock.schedule_once(self.damage)
				return False
			if "Marker" in self.gd["pay"]:
				self.remove_marker(card.ind, self.gd["pay"][self.gd["pay"].index("Marker") + 1])
				self.gd["pay"].remove("Marker")
				Clock.schedule_once(self.pay_condition, move_dt_btw)
				return False

			self.pay_condition_done()
		else:
			self.pay_condition_done()

	def pay_condition_done(self, dt=0):
		if self.net["game"] and self.gd["active"] == "1" and self.gd["targetpay"]:
			for ing in self.gd["targetpay"]:
				self.net["act"][3].append(ing)

		self.gd["targetpay"] = []
		self.gd["payed"] = True
		self.gd["pay"] = ""
		self.check_cont_ability()

		if "ACT" in self.gd["ability_trigger"]:
			if "Counter" in self.gd["ability_trigger"]:
				effect = ab.act(self.gd["ability"])

				if "backup" in effect:
					if "C" in self.gd["attacking"]:
						ind = self.pd[self.gd["counter_id"][-1]]["Center"][self.gd["attacking"][3]]
					elif "B" in self.gd["attacking"]:
						ind = self.pd[self.gd["counter_id"][-1]]["Back"][self.gd["attacking"][3]]

					if ind != "":
						self.cd[ind].power_c.append([effect[1], 1, "Backup", self.gd["turn"]])
						self.cd[ind].update_power()
					self.gd["check_ctr"] = True
				Clock.schedule_once(self.counter_step_done)
			else:
				ind = self.gd["ability_trigger"].split("_")[1]
				self.check_auto_ability(act=ind, stacks=False)
				self.gd["effect"] = ab.act(self.gd["ability"])
				Clock.schedule_once(self.ability_event)
		else:
			Clock.schedule_once(self.ability_effect)

	def pay_opponent(self):
		pick = self.ai.ability(self.pd, self.cd, self.gd)
		pay = self.gd["pay"]
		if "AI_pay" in pick and "Rest" in pick:
			self.cd[self.gd["pay"][pick.index("AI_pay") + 1]].rest()
			self.gd["payed"] = True
		elif "AI_pay" in pick and "Clock" in pick:
			ind = self.gd["pay"][pick.index("AI_pay") + 1]
			self.hand_clock(ind)
			self.gd["payed"] = True

			if not self.gd["both"] and self.check_lose():
				return False

			if self.gd["both"]:
				self.gd["both"] = False

			if len(self.pd[self.gd["active"]]["Clock"]) >= 7:
				self.gd["level_up_trigger"] = "pay_choose"
				Clock.schedule_once(self.level_up, move_dt_btw)
				return False

	def pay_choose(self, *args):
		self.gd["chosen"] = []
		if "Rest" in self.gd["pay"]:
			ind = self.gd["pay"].index("Rest")
			if "BTrait" in self.gd["pay"]:
				inm = self.gd["ability_trigger"].split("_")[1]
				self.gd["btrait"][1] = self.gd["pay"][ind + 3].split("_")
				self.gd["btrait"][2] = [s for s in self.pd[inm[-1]]["Center"] + self.pd[inm[-1]]["Back"] if
				                       self.cd[s].status == "Stand"]
				# for br in self.gd["btrait"][2]:
				# 	if self.gd["btrait"][1][0] in self.cd[br].trait_t:
				# 		self.gd["btrait"][3].append(br)
				# 	if self.gd["btrait"][1][1] in self.cd[br].trait_t:
				# 		self.gd["btrait"][4].append(br)
			self.gd["pay_status"] = f"StandSelect{self.gd['pay'][ind + 1]}"
			if len(self.gd["pay"]) > 2 and (sel in self.gd["pay"][ind + 2] for sel in ("Name", "Trait", "Other")):
				self.gd["pay_status"] = self.add_to_status(self.gd["pay_status"], self.gd["pay"][ind:ind + 4])
				if "BTrait" in self.gd["pay"]:
					self.gd["btrait"][0] = str(self.gd["pay_status"])
			self.select_card(s="Stand", p=True)
		else:
			if "WOther" in self.gd["pay"]:
				self.gd["pay_status"] = self.add_to_status(self.gd["pay_status"], ["Other"])
			else:
				self.gd["pay_status"] = self.add_to_status(self.gd["pay_status"], self.gd["pay"])
			self.select_card(p=True)
		Clock.schedule_once(partial(self.popup_text, "Main"))
		return False

	def check_auto_ability(self, dt=.0, rev=[""], atk="", play="", wait="", revive="", trigger="", cnc=("", False),
	                       refr="", lvup="", stacks=True, act="", change="", batt=False, dis="", sav="", dmg=0, rst="",
	                       brt=("", 0), lvc=""):
		# st = []
		# for player in list(self.pd.keys()):
		# 	for indx in self.pd[player]["Center"] + self.pd[player]["Back"]:
		# 		st.append(self.cd[indx].name)
		for r in rev:
			for player in list(self.pd.keys()):
				sxx = []
				inds = []
				tr = []

				stage = self.pd[player]["Center"] + self.pd[player]["Back"]

				for indx in stage:
					sxx.append(self.cd[indx].status)
					inds.append(self.cd[indx].ind)
					tr.append(self.cd[indx].trait_t)

				# h = [self.cd[indy].card for indy in self.pd[player]["Hand"]]

				if len(self.pd[self.gd["active"]]["Climax"]) > 0:
					cxx = self.pd[self.gd["active"]]["Climax"][0]
					cx = (self.cd[cxx].name, self.cd[cxx].ind, self.cd[cxx].mcolour)
				else:
					cx = ("", "9", "")
				# sx = len(self.pd[player]["Stock"])
				if "Main" in self.gd["phase"] and self.gd["pp"] < 0:
					cards = list(stage + self.pd[player]["Memory"])
				else:
					cards = list(stage)

				for ind in cards + [player]:
					if ind in self.emptycards:
						continue
					card = self.cd[ind]
					# s = card.status
					encore = []
					pos = ("", "", "", "")
					if ind == wait:  # and player in wait[-1]:
						encore = [0, "encore"]
						if len(self.pd[wait[-1]]["Stock"]) >= 3:
							encore.append("Stock3")

					for item in card.text_c:
						if item[0].startswith(auto_ability) and item[1] != 0 and item[1] > -9:
							baind = ("", "")
							lvop = (0, 0)
							csop = (0, 0)
							suop = ("", "")
							nmop = ("", "")
							ty = ("", [])
							ch = False
							diss = (dis, self.cd[dis].card)
							savs = (sav, self.cd[sav].card)

							if self.gd["phase"] in ("Battle", "Counter", "Trigger", "Damage", "Declaration"):
								datk = self.gd["attacking"][0]
								deff = ""
								if self.gd["attacking"][0][-1] == "1":
									op = "2"
								elif self.gd["attacking"][0][-1] == "2":
									op = "1"
								if "C" in self.gd["attacking"][4]:
									deff = self.pd[op]["Center"][self.gd["attacking"][3]]
								elif "B" in self.gd["attacking"][4]:
									deff = self.pd[op]["Back"][self.gd["attacking"][3]]

								# if ind == deff:
								# 	baind = (deff, datk)
								# else:
								baind = (datk, deff)

								if deff != "":
									suop = (self.cd[baind[0]].status, self.cd[baind[1]].status)
									lvop = (self.cd[baind[0]].level_t, self.cd[baind[1]].level_t)
									csop = (self.cd[baind[0]].cost_t, self.cd[baind[1]].cost_t)
									nmop = (self.cd[baind[0]].name, self.cd[baind[1]].name)

							if rev != [""]:
								if self.gd["phase"] == "Trigger":
									ty = (self.cd[r].card, self.cd[r].trigger, self.gd["attacking"][0])
							elif atk:
								r = atk
							elif play:
								r = play
							elif wait:
								r = wait
							elif act:
								r = act
							elif rst:
								r = rst
							elif change:
								r = change
								ch = True

							v = (self.cd[ind].status, self.cd[r].status)
							nr = (self.cd[ind].name, self.cd[r].name)
							if wait and ind in wait:
								pos = (card.pos_new, "Waiting", self.cd[wait].pos_new, "Waiting")
							elif wait:
								pos = (card.pos_old, card.pos_new, self.cd[wait].pos_new, "Waiting")
							else:
								pos = (card.pos_old, card.pos_new, self.cd[r].pos_old, self.cd[r].pos_new)

							# if ab.req(a=item[0], s=s, x=sx, ss=sxx, h=h,tr=tr):
							# print(item[0])
							# print(ind, r, pos, v, self.gd["active"], cx, play, rev, atk)
							ability = ab.auto(a=item[0], p=self.gd["phase"], r=(ind, r, self.cd[r].card), v=v, cx=cx,
							                  ty=ty, suop=suop, lr=(self.cd[r].level_t, self.cd[r].level_t),
							                  pos=pos, n=self.gd["active"], sx=sxx, inds=inds, act=act, baind=baind,
							                  nr=nr, dis=diss, csop=csop, atk=self.gd["attacking"][1], nmop=nmop,
							                  lvup=lvup, refr=refr, sav=savs, rst=rst, lvc=(lvc, self.cd[lvc].card),
							                  z=(card.turn, self.gd['turn']), cnc=cnc, dmg=dmg, pp=self.gd["pp"], ch=ch,
							                  tr=(self.cd[ind].trait_t, self.cd[r].trait_t), lvop=lvop, batt=batt,
							                  brt=brt)

							# print(ability)
							if ability:
								if "pay" in ability:
									ability.insert(1, ab.pay(item[0]))
								elif "do" in ability:
									inx1 = ability.index("do") + 1
									if "pay" in ability[inx1]:
										ability[inx1].insert(1, ab.pay(item[0]))
									elif "do" in ability[inx1]:
										inx2 = ability[inx1].index("do") + 1
										if "pay" in ability[inx1][inx2]:
											ability[inx1][inx2].insert(1, ab.pay(item[0]))

								if "played" in ability:
									self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -9
								elif "at" in ability:
									if item[1] == -1:
										self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -31
								elif "a1" in ability:
									if item[1] == -1:
										self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -10
									elif item[1] > 0:
										self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -15
								elif "a2" in ability:
									if item[1] == -1:
										self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -5
									elif item[1] > 0:
										self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -7
									elif item[1] == -5:
										self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -11
									elif item[1] == -7:
										self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -16
								elif "a3" in ability:
									if item[1] == -1:
										self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -5
									elif item[1] > 0:
										self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -7
									elif item[1] == -5:
										self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -6
									elif item[1] == -7:
										self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -8
									elif item[1] == -6:
										self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -11
									elif item[1] == -8:
										self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -16
								if ability[0] == -38 and "pass" in item:
									ability[0] = int(item[item.index("pass") + 1])
									ability[2] = str(item[item.index("pass") + 2])
									ability.append("passed")

							if ind == wait and ability and "encore" in ability:
								if "Character" in ability:
									if len([s for s in self.pd[wait[-1]]["Hand"] if
									        self.cd[s].card == "Character"]) > 0 and "Character" not in encore:
										encore.append("Character")
								if "Trait" in ability:
									traits = ability[ability.index("Trait") + 1].split("_")
									if len([s for s in self.pd[wait[-1]]["Hand"] if
									        any(trait in self.cd[s].trait_t for trait in traits)]) > 0:
										if "Trait" not in encore:
											encore.append("Trait")
											encore.append("Trait_")

										for trait in traits:
											if trait not in encore[encore.index("Trait") + 1]:
												encore[encore.index("Trait") + 1] += f"_{trait}"
								if "Clock" in ability and "Clock" not in encore:
									encore.append("Clock")
								if "Stock" in ability and f"Stock{ability[0]}" not in encore:
									encore.append(f"Stock{ability[0]}")
							# elif ind != wait and ability and "encore" not in ability:
							if ability and "encore" not in ability:
								stack = [ind, ability, item[0], r, pos, self.gd["phase"], card.text_c.index(item),
								         self.gd["pp"]]
								if ability and stack not in self.gd["stack"][player]:
									self.gd["stack"][player].append(stack)

					if wait and player in wait[-1] and ind == wait and len(encore) > 2:
						stack = [wait, encore, "[AUTO] Encore", wait, pos, self.gd["phase"], 0, self.gd["pp"]]
						if stack not in self.gd["stack"][player]:
							self.gd["stack"][player].append(stack)
		if stacks:
			Clock.schedule_once(self.stack_ability)

	def stack_ability(self, *args):
		if self.gd["active"] == "1":
			self.gd["moveable"] = []
		if self.gd["rev"]:
			player = self.gd["opp"]
		else:
			player = self.gd["active"]
		if self.gd["auto_effect"] in self.gd["stack"][player]:
			self.gd["stack"][player].remove(self.gd["auto_effect"])
			if self.net["game"] and player == "1" and self.gd["ability_doing"] != "confirm" and not self.gd[
				"oppchoose"]:
				self.net["var"] = self.net["act"]
				self.net["var1"] = "auto"
				self.gd["oppchoose"] = False
				self.mconnect("act")
				return False

		if self.net["game"] and player == "1" and self.gd["oppchoose"]:
			self.gd["oppchoose"] = False

		if self.net["game"] and player == "1" and self.net["varlvl"] and not self.net["lvlsend"]:
			self.net["var"] = list(self.net["varlvl"])
			self.net["var1"] = "lvl"
			if not self.poptext:
				Clock.schedule_once(partial(self.popup_text, "waitingser"))
			self.mconnect("lvl")
			return False

		if self.gd["resonance"][0]:
			self.gd["resonance"] = [False, []]
			self.hand_size(player)

		if len(self.pd[player]["Res"]) > 0:
			self.event_done()

		# print("before",self.gd["stack"]["1"])
		self.auto_check(player)
		# print("after",self.gd["stack"]["1"])

		if "do" in self.gd["ability_effect"]:
			if self.gd["do"][0] > 0:
				self.gd["done"] = True
				Clock.schedule_once(self.ability_effect)
				return
			else:
				self.gd["ability_effect"].remove("do")

		if self.gd["reshuffle"] and "do" not in self.gd["ability_effect"] and self.gd["trigger"] <= 0:
			self.gd["reshuffle"] = False
			self.gd["damage_refresh"] = 1
			self.gd["damageref"] = True
			self.gd["reshuffle_trigger"] = "damage"
			Clock.schedule_once(self.damage, move_dt_btw)
			return False

		if len(self.gd["stack"][player]) > 1 and "1" in player:
			for item in self.gd["stack"]["1"]:
				if item[0] == "1":
					# self.stack_resolve(self.gd["stack"]["1"].index(item))
					Clock.schedule_once(partial(self.stack_resolve, self.gd["stack"]["1"].index(item)))
					return False
			self.gd["stack_pop"] = True
			Clock.schedule_once(self.stack_popup, popup_dt)
		elif len(self.gd["stack"][player]) > 0 and "2" in player:
			if self.net["game"]:
				if self.gd["show_wait_popup"]:
					Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
				self.mconnect("phase")
			elif self.gd["com"]:
				self.stack_resolve("0")
		##### add opponent com choice
		elif len(self.gd["stack"][player]) > 0:
			self.stack_resolve("0")
		elif len(self.gd["stack"][player]) <= 0 and not self.gd["rev"]:
			if not self.gd["check_reserve"]:
				self.gd["check_reserve"] = True
			else:
				self.gd["check_reserve"] = False
				self.gd["rev"] = True
			Clock.schedule_once(self.stack_ability)
		elif len(self.gd["stack"][player]) <= 0 and self.gd["rev"]:
			if not self.gd["check_reserve"]:
				self.gd["check_reserve"] = True
				Clock.schedule_once(self.stack_ability)
			else:
				self.gd["check_reserve"] = False
				self.gd["rev"] = False
				self.clear_ability()
				# if self.gd["level_up_trigger"]:
				# 	Clock.schedule_once(self.level_up_done)
				if "Draw" in self.gd["phase"]:
					Clock.schedule_once(self.draw_phase)
				elif "Battle" in self.gd["phase"]:
					Clock.schedule_once(self.attack_phase_done)
				elif "Damage" in self.gd["phase"]:
					self.gd["phase"] = "Battle"
					if self.gd["attacking"][1] == "f":
						Clock.schedule_once(self.battle_step)
					else:
						Clock.schedule_once(self.attack_phase_done)
				elif "Attack" in self.gd["phase"]:
					Clock.schedule_once(self.attack_phase_main)
				elif "Declaration" in self.gd["phase"]:
					Clock.schedule_once(self.attack_declaration_done)
				elif "Counter" in self.gd["phase"]:
					if self.gd["pp"] <= 0:
						Clock.schedule_once(self.counter_step)
					else:
						Clock.schedule_once(self.counter_step_done)
				elif "Trigger" in self.gd["phase"]:
					if self.gd["trigger"] > 0:
						Clock.schedule_once(self.trigger_effect)
					else:
						Clock.schedule_once(self.trigger_step_done)
				elif "Climax" in self.gd["phase"]:
					if self.gd["pp"] <= 0:
						Clock.schedule_once(self.climax_phase_beginning)
					else:
						Clock.schedule_once(self.climax_phase_done)
				elif "Main" in self.gd["phase"]:
					if self.gd["pp"] < 0:
						Clock.schedule_once(self.main_phase)
					else:
						Clock.schedule_once(self.play_card_done)
				elif "Draw" in self.gd["phase"]:
					Clock.schedule_once(self.draw_phase)
				elif "Encore" in self.gd["phase"]:
					Clock.schedule_once(self.encore_phase)
				elif "End" in self.gd["phase"]:
					if self.gd["pp"] < 0:
						Clock.schedule_once(self.end_phase_start)
					elif self.gd["pp"] > 0:
						Clock.schedule_once(self.end_phase_end)

	def stack_resolve(self, btn, *args):
		self.gd["stack_pop"] = False
		if self.gd["popup_done"][0]:
			self.sd["popup"]["popup"].dismiss()
			self.popup_clr()

		for nx in self.gd["sn"]:
			for ax in self.gd["sn"][nx]:
				for nnx in range(len(self.gd["sn"][nx][ax])):
					self.cd[self.gd["sn"][nx][ax][nnx][0]].update_text()
					self.cpop[self.gd["sn"][nx][ax][nnx][1]].update_text()
		for item in self.gd["so"]:
			self.cpop[item].update_text()
		self.gd["so"] = []
		self.gd["sn"] = {}

		self.gd["payed"] = False

		if self.gd["rev"]:
			player = self.gd["opp"]
		else:
			player = self.gd["active"]

		try:
			auto = int(btn.cid)
		except AttributeError:
			auto = int(btn)

		self.gd["auto_effect"] = list(self.gd["stack"][player][auto])

		if "TriggerIcon" in self.gd["auto_effect"]:
			self.gd["ability_trigger"] = f"AUTO_{self.gd['auto_effect'][0]}_Trigger"
		else:
			self.gd["ability_trigger"] = f"AUTO_{self.gd['auto_effect'][0]}"
		self.gd["ability"] = str(self.gd["auto_effect"][2])
		self.gd["effect"] = list(self.gd["auto_effect"][1])

		if "TriggerIcon" not in self.gd["auto_effect"]:
			self.gd["pay"] = ab.pay(a=self.gd["ability"])
			if self.gd["pay"]:
				self.gd["payed"] = False
			else:
				self.gd["payed"] = True
		else:
			self.gd["pay"] = []
			self.gd["payed"] = True

		if self.net["game"] and player == "1":
			self.net["send"] = False
			self.net["act"] = ["a", str(self.gd["auto_effect"][0]), auto, [], [], 0]

		if self.net["game"] and player == "2" and not self.net["act"][5] and "encore" in self.gd["effect"]:
			# 	Clock.schedule_once(self.pay_condition)
			# 	return False
			Clock.schedule_once(self.ability_effect)
		else:
			Clock.schedule_once(self.ability_event)

	def auto_reserve(self, p, auto, reserve=True):
		if auto in self.gd["stack"][p]:
			self.gd["stack"][p].remove(auto)
			if reserve and not self.gd["check_reserve"]:
				self.gd["reserve"][p].append(auto)

	def auto_check(self, p):
		self.gd["auto_recheck"] = False
		if len(self.gd["reserve"][p]) > 0:
			for autor in range(len(self.gd["reserve"][p])):
				temp = self.gd["reserve"][p].pop(0)
				if temp not in self.gd["stack"][p]:
					self.gd["stack"][p].append(temp)

		stack = list(self.gd["stack"][p])
		for auto in stack:
			if "pay" in auto[1] and "oppmay" in auto[1]:
				if p == "1":
					o = "2"
				elif "p" == "2":
					o = "1"
				auto1 = list(auto)
				auto1[1].remove("oppmay")
				self.gd["stack"][p].remove(auto)
				self.gd["stack"][o].append(auto1)
				continue

			if "Trigger" in auto[3]:
				continue

			if auto[5] != self.gd["phase"]:
				self.auto_reserve(p, auto, False)
			# if auto in self.gd["stack"][p]:
			# 	self.gd["stack"][p].remove(auto)

			# if "phase" in auto[1]:
			# 	if auto[5] in phases and auto[-1] != self.gd["phase"]:
			# 		self.gd["stack"][p].remove(auto)
			# 	elif auto[-1] in steps and auto[-1] != self.gd["pahse"]:
			# 		self.gd["stack"][p].remove(auto)
			if auto[7] != self.gd["pp"]:
				self.auto_reserve(p, auto, False)
			# if auto in self.gd["stack"][p]:
			# 	self.gd["stack"][p].remove(auto)

			stage = list(self.pd[p]["Center"] + self.pd[p]["Back"])
			stock = len(self.pd[p]["Stock"])
			# stand = len([s for s in stage if s!="" and self.cd[s].status == "Stand"])
			if "do" in auto[1]:
				do = auto[1][auto[1].index("do") + 1]
			else:
				do = []

			if self.gd["nomay"] and "may" in auto[1]:
				self.auto_reserve(p, auto, False)
			# if auto in self.gd["stack"][p]:
			# 	self.gd["stack"][p].remove(auto)
			elif "rescue" in auto[1]:
				if "Waiting" not in self.cd[auto[3]].pos_new:
					self.auto_reserve(p, auto)
			elif "revive" in auto[1]:
				if "Waiting" not in self.cd[auto[3]].pos_new:
					self.auto_reserve(p, auto)
			elif "encore" in auto[1]:
				if self.gd["noencore"][p]:
					self.gd["stack"][p].remove(auto)
				elif "Waiting" not in self.cd[auto[0]].pos_new and "Waiting" in auto[4][1]:
					self.auto_reserve(p, auto)
				else:
					if "Stock1" in auto[1] and stock < 1:
						self.auto_reserve(p, auto)
					if "Stock2" in auto[1] and stock < 2:
						self.auto_reserve(p, auto)
					if "Stock3" in auto[1] and stock < 3:
						self.auto_reserve(p, auto)
					if ("Character" in auto[1] or "Trait" in auto[1]) and len(self.pd[p]["Hand"]) < 1:
						self.auto_reserve(p, auto)
			elif ("power" in auto[1] or "soul" in auto[1] or "level" in auto[1] or "cost" in auto[1]) and auto[1][
				0] == 0 and auto[0] not in stage:
				self.auto_reserve(p, auto)
			elif any(stat in auto[1] for stat in ("Rest", "Stand", "Reversed")):
				if "Center" in auto[1]:
					stage1 = list(self.pd[p]["Center"])
				else:
					stage1 = list(self.pd[p]["Center"] + self.pd[p]["Back"])

				status = [self.cd[s].status for s in stage]

				if "other" in auto[1]:
					if auto[0] in stage1:
						status[stage1.index(auto[0])] = ""
				if "Rest" in auto[1]:
					if auto[1] == 0 and "Rest" in status:
						self.auto_reserve(p, auto)
			# elif auto[1][0] > 0 and "Stand" in auto[1] and "Stand" not in status:
			# 	self.gd["stack"][p].remove(auto)
			elif ("pay" in auto[1] and "this" in auto[1][auto[1].index("do") + 1]) or "this" in auto[1]:
				if "Center" not in self.cd[auto[0]].pos_new and "Back" not in self.cd[auto[0]].pos_new:
					self.auto_reserve(p, auto)
			elif "hander" in auto[1] or (
					"do" in auto[1] and "pay" in auto[1] and "hander" in auto[1][auto[1].index("do") + 1]):
				hh = False
				if "Climax" in auto[1] or (
						"do" in auto[1] and "pay" in auto[1] and "Climax" in auto[1][auto[1].index("do") + 1]) and len(
						self.pd[p]["Climax"]) < 1:
					hh = True
				elif "hander" in auto[1] and auto[1][0] == 0:
					if self.cd[auto[0]].pos_new != auto[4][1]:
						hh = True
					elif "Memory" in auto[1] and "Memory" not in self.cd[auto[0]].pos_new:
						hh = True
					elif "Memory" not in auto[1] and auto[0] not in stage:
						hh = True
				elif "do" in auto[1] and "pay" in auto[1] and "hander" in auto[1][auto[1].index("do") + 1] and \
						auto[1][auto[1].index("do") + 1][0] == 0:
					if self.cd[auto[0]].pos_new != auto[4][1]:
						hh = True
					elif "Memory" in auto[1][auto[1].index("do") + 1] and "Memory" not in self.cd[auto[0]].pos_new:
						hh = True
					elif "Memory" not in auto[1][auto[1].index("do") + 1] and auto[0] not in stage:
						hh = True
				if hh:
					self.auto_reserve(p, auto)
			elif "memorier" in auto[1] or (
					"do" in auto[1] and "pay" in auto[1] and "memorier" in auto[1][auto[1].index("do") + 1]):
				hh = False
				if "memorier" in auto[1] and auto[1][0] == 0:
					if self.cd[auto[0]].pos_new != auto[4][1]:
						hh = True
				elif "do" in auto[1] and "pay" in auto[1] and "memorier" in auto[1][auto[1].index("do") + 1] and \
						auto[1][auto[1].index("do") + 1][0] == 0:
					if self.cd[auto[0]].pos_new != auto[4][1]:
						hh = True
				if hh:
					self.auto_reserve(p, auto)
			elif "heal" in auto[1] or (
					"do" in auto[1] and "pay" in auto[1] and "heal" in auto[1][auto[1].index("do") + 1]):
				if len(self.pd[auto[0][-1]]["Clock"]) <= 0:
					self.auto_reserve(p, auto)
			elif "pay" in auto[1] and "change" in auto[1][-1]:
				if auto[0] not in self.gd["stage-1"]:
					self.auto_reserve(p, auto)
			elif "pay" in auto[1] and auto[1][-1][0] == -3 and any(
					abl in auto[1][-1] for abl in ("decker", "reverser", "stocker", "memorier", "clocker")):
				opp = auto[1][-1][auto[1][-1].index("target") + 1]
				if opp != "" and self.cd[opp].pos_new[:-1] in (
						"Center", "Back"):  # and self.cd[opp].pos_old != "Waiting":
					pass
				else:
					self.auto_reserve(p, auto)
			elif "turn" in auto[1]:
				tt = False
				if self.gd["turn"] == auto[1][1]:
					tt = True
				if tt:
					self.gd["stack"][p].remove(auto)
					auto[1] = do
					self.gd["stack"][p].append(auto)
					self.gd["auto_recheck"] = True
					break
				elif not tt:
					self.auto_reserve(p, auto)
			elif "more" in auto[1]:
				target = auto[1][2].split("_")
				mm = True
				if "lower" not in auto[1] and len(
						self.cont_times(auto[1], self.cont_cards(auto[1], auto[0]), self.cd)) < auto[1][0]:
					mm = False
				elif "lower" in auto[1] and len(self.cont_times(auto[1], self.cont_cards(auto[1], auto[0]), self.cd)) > \
						auto[1][0]:
					mm = False
				if mm:
					self.gd["stack"][p].remove(auto)
					auto[1] = do
					self.gd["stack"][p].append(auto)
					self.gd["auto_recheck"] = True
					break
				elif not mm:
					self.auto_reserve(p, auto)
			elif "atkpwrdif" in auto[1]:
				att = False
				if auto[1][2] == self.gd["attacking"][0]:
					attk = self.gd["attacking"][0]
					if attk[-1] == "1":
						opp = "2"
					elif attk[-1] == "2":
						opp = "1"
					if "C" in self.gd["attacking"][4]:
						deff = self.pd[opp]["Center"][self.gd["attacking"][3]]
					elif "B" in self.gd["attacking"][4]:
						deff = self.pd[opp]["Back"][self.gd["attacking"][3]]
					if self.cd[attk].power_t >= self.cd[deff].power_t + auto[1][0]:
						att = True
				if att:
					self.gd["stack"][p].remove(auto)
					auto[1] = do
					self.gd["stack"][p].append(auto)
					self.gd["auto_recheck"] = True
					break
				elif not att:
					self.auto_reserve(p, auto)
			elif "atkpwrchk" in auto[1]:
				att = False
				if "self" in auto[1]:
					if auto[1][0] == -2:
						stage1 = [s for s in stage if s != ""]
						if auto[0] in stage1:
							stage1.remove(auto[0])
						if "lower" in auto[1] and all(
								self.cd[ind].power_t < self.cd[auto[0]].power_t for ind in stage1):
							att = True
						elif "lower" not in auto[1] and all(
								self.cd[ind].power_t > self.cd[auto[0]].power_t for ind in stage1):
							att = True

				if att:
					self.gd["stack"][p].remove(auto)
					auto[1] = do
					self.gd["stack"][p].append(auto)
					self.gd["auto_recheck"] = True
					break
				elif not att:
					self.auto_reserve(p, auto)
			elif "name" in auto[1]:
				# if "opp" in auto[1] and (self.gd["rev"] or self.gd["rev_counter"]) and p == "1":
				# 	player = "1"
				# elif "opp" in auto[1] and (self.gd["rev"] or self.gd["rev_counter"]) and p == "2":
				# 	player = "2"
				# elif ("opp" in auto[1] or self.gd["rev"] or self.gd["rev_counter"]) and p == "1":
				# 	player = "2"
				# elif ("opp" in auto[1] or self.gd["rev"] or self.gd["rev_counter"]) and p == "2":
				# 	player = "1"
				# else:
				# 	player = p
				if "opp" in auto[1]:
					if auto[0][-1] == "1":
						player = "2"
					elif auto[0][-1] == "2":
						player = "1"
				else:
					player = auto[0][-1]

				if "Center" in auto[1]:
					stage1 = list(self.pd[player]["Center"])
				elif "Memory" in auto[1]:
					stage1 = list(self.pd[player]["Memory"])
				else:
					stage1 = list(self.pd[player]["Center"] + self.pd[player]["Back"])
				name = auto[1][auto[1].index("name") + 1]

				if "other" in auto[1] and auto[0] in stage1:
					stage1.remove(auto[0])

				if any(name in self.cd[s].name for s in stage1):
					self.gd["stack"][p].remove(auto)
					auto[1] = do
					self.gd["stack"][p].append(auto)
					self.gd["auto_recheck"] = True
					break
				else:
					self.auto_reserve(p, auto)
			elif "cards" in auto[1]:
				if "opp" in auto[1] and auto[0][-1] == "1":
					pl = "2"
				elif "opp" in auto[1] and auto[0][-1] == "2":
					pl = "1"
				else:
					pl = auto[0][-1]
				cc = True
				if "HandvsOpp" in auto[1]:
					if auto[0][-1] == "1":
						op = "2"
					elif auto[0][-1] == "2":
						op = "1"
					if "lower" in auto[1] and len(self.pd[auto[0][-1]]["Hand"]) >= len(self.pd[op]["Hand"]):
						cc = False
					elif "lower" not in auto[1] and len(self.pd[auto[0][-1]]["Hand"]) <= len(self.pd[op]["Hand"]):
						cc = False
				elif "Hand" in auto[1]:
					if len(self.pd[pl]["Hand"]) < auto[1][0]:
						cc = False
				elif "Stock" in auto[1]:
					if "lower" in auto[1] and len(self.pd[pl]["Stock"]) > auto[1][0]:
						cc = False
				elif "Library" in auto[1]:
					if "lower" in auto[1] and len(self.pd[pl]["Library"]) > auto[1][0]:
						cc = False
				elif "Clock" in auto[1]:
					if "lower" in auto[1] and len(self.pd[pl]["Clock"]) > auto[1][0]:
						cc = False
				elif "Memory" in auto[1]:
					if len(self.pd[pl]["Memory"]) < auto[1][0]:
						cc = False
				elif "Waiting" in auto[1]:
					if "Climax" in auto[1] and len([s for s in self.pd[pl]["Waiting"] if "Climax" in self.cd[s].card]) < \
							auto[1][0]:
						cc = False
					elif "lower" in auto[1] and len(self.pd[pl]["Waiting"]) > auto[1][0]:
						cc = False
					elif "lower" not in auto[1] and len(self.pd[pl]["Waiting"]) < auto[1][0]:
						cc = False

				if cc:
					self.gd["stack"][p].remove(auto)
					auto[1] = do
					self.gd["stack"][p].append(auto)
					self.gd["auto_recheck"] = True
					break
				else:
					self.auto_reserve(p, auto)
			elif "experience" in auto[1]:
				if sum([self.cd[lv].level for lv in self.pd[p]["Level"] if lv != ""]) >= auto[1][
					auto[1].index("experience") + 1]:
					self.gd["stack"][p].remove(auto)
					auto[1] = do
					self.gd["stack"][p].append(auto)
					self.gd["auto_recheck"] = True
					break
				else:
					self.auto_reserve(p, auto)
			elif "markers" in auto[1]:
				mk = True
				if auto[0] in self.pd[auto[0][-1]]["marker"]:
					markers = len(self.pd[auto[0][-1]]["marker"][auto[0]])
				else:
					markers = 0
				if "lower" in auto[1] and markers > auto[1][0]:
					mk = False
				elif "lower" not in auto[1] and markers < auto[1][0]:
					mk = False
				if mk:
					self.gd["stack"][p].remove(auto)
					auto[1] = do
					self.gd["stack"][p].append(auto)
					self.gd["auto_recheck"] = True
					break
				else:
					self.auto_reserve(p, auto)
			elif "opposite" in auto[1]:
				oo = True

				if "Center" not in self.cd[auto[0]].pos_new:
					oo = False
				else:
					if auto[0][-1] == "1":
						op = "2"
					elif auto[0][-1] == "2":
						op = "1"
					opp = self.pd[op]["Center"][self.m[int(self.cd[auto[0]].pos_new[-1])]]
					if opp == "":
						oo = False
					elif "olevel" in auto[1]:
						if "lower" in auto[1] and self.cd[opp].level_t > auto[1][auto[1].index("olevel") + 1]:
							oo = False
						elif "lower" not in auto[1] and self.cd[opp].level_t < auto[1][auto[1].index("olevel") + 1]:
							oo = False
					elif "#traits" in auto[1]:
						if "#lower" in auto[1] and len([t for t in self.cd[opp].trait_t if t != ""]) > auto[1][
							auto[1].index("#traits") + 1]:
							oo = False
						elif "#lower" not in auto[1] and len([t for t in self.cd[opp].trait_t if t != ""]) < auto[1][
							auto[1].index("#traits") + 1]:
							oo = False
				if oo:
					self.gd["stack"][p].remove(auto)
					auto[1] = do
					self.gd["stack"][p].append(auto)
					self.gd["auto_recheck"] = True
					break
				else:
					self.auto_reserve(p, auto)
			elif "stage" in auto[1]:
				aa = True
				if "Center" in auto[1] and "Center" not in self.cd[auto[0]].pos_new:
					aa = False
				elif "Memory" in auto[1] and "Memory" not in self.cd[auto[0]].pos_new:
					aa = False
				if aa:
					self.gd["stack"][p].remove(auto)
					auto[1] = do
					self.gd["stack"][p].append(auto)
					self.gd["auto_recheck"] = True
					break
				elif not aa:
					self.auto_reserve(p, auto)
			elif "plevel" in auto[1]:
				if "antilvl" in auto[1]:
					if "opp" in auto[1] and (self.gd["rev"] or self.gd["rev_counter"]) and p == "1":
						player = "1"
					elif "opp" in auto[1] and (self.gd["rev"] or self.gd["rev_counter"]) and p == "2":
						player = "2"
					elif ("opp" in auto[1] or self.gd["rev"] or self.gd["rev_counter"]) and p == "1":
						player = "2"
					elif ("opp" in auto[1] or self.gd["rev"] or self.gd["rev_counter"]) and p == "2":
						player = "1"
					else:
						player = p

					if self.cd[auto[1][2]].level_t > len(self.pd[player]["Level"]):
						self.gd["stack"][p].remove(auto)
						auto[1] = do
						self.gd["stack"][p].append(auto)
						self.gd["auto_recheck"] = True
						break
					else:
						self.auto_reserve(p, auto)
			if not self.auto_check_pay(auto, s="auto"):
				self.auto_reserve(p, auto)
		#
		# if "played" in auto[1]:
		# 	if "trait" in auto[1] and auto[1][0] not in self.cd[auto[3]].trait_t:
		# 		self.auto_reserve(p, auto)

		if self.gd["auto_recheck"]:
			self.auto_check(p)

	def auto_check_pay(self, auto, s=""):
		if s == "auto":
			lst = auto[1]
			ind = auto[0]
		else:
			lst = auto
			ind = self.gd["ability_trigger"].split("_")[1]

		if "pay" in lst and isinstance(lst[1], list):
			p = ind[-1]
			stock = len(self.pd[p]["Stock"])
			stage = list(self.pd[p]["Center"] + self.pd[p]["Back"])
			if "Stock" in lst[1] and stock < lst[1][lst[1].index("Stock") + 1]:
				return False

			if "Discard" in lst[1]:
				qty = lst[1][lst[1].index("Discard") + 1]

				if qty == 0 and ind not in self.pd[p]["Hand"]:
					return False
				elif qty == -10 and len(self.pd[p]["Hand"]) < 1:
					return False
				elif qty > 0:
					if len(self.pd[p]["Hand"]) < qty:
						return False
					elif "Rest" in lst[1] and len(
							self.cont_times(lst[1][:lst[1].index("Rest")], self.pd[p]["Hand"], self.cd)) < qty:
						return False
					elif "Rest" not in lst[1] and len(self.cont_times(lst[1], self.pd[p]["Hand"], self.cd)) < qty:
						return False
			if "MDiscard" in lst[1]:
				qty = lst[1][lst[1].index("MDiscard") + 1]
				if qty == 0 and ind not in self.pd[p]["Memory"]:
					return False
				elif qty > 0:
					if len(self.pd[p]["Memory"]) < qty:
						return False
					elif len(self.cont_times(lst[1], self.pd[p]["Memory"], self.cd)) < qty:
						return False
			if "HMemory" in lst[1]:
				qty = lst[1][lst[1].index("HMemory") + 1]
				if qty > 0:
					if len(self.pd[p]["Hand"]) < qty:
						return False
					elif len(self.cont_times(lst[1], self.pd[p]["Hand"], self.cd)) < qty:
						return False
			if "WDecker" in lst[1]:
				qty = lst[1][lst[1].index("WDecker") + 1]
				if qty > 0:
					if len(self.pd[p]["Waiting"]) < qty:
						return False
					elif len(self.cont_times(lst[1], self.pd[p]["Waiting"], self.cd)) < qty:
						return False
			if "RevealStock" in lst[1]:
				name = lst[1][lst[1].index("RevealStock") + 1]
				if all(name not in self.cd[nn].name for nn in self.pd[p]["Hand"]):
					return False
			elif "Reveal" in lst[1]:
				name = lst[1][lst[1].index("Reveal") + 1]
				if all(name not in self.cd[nn].name for nn in self.pd[p]["Hand"]):
					return False
			elif "ClockH" in lst[1]:
				if len(self.pd[p]["Hand"]) < lst[1][lst[1].index("ClockH") + 1]:
					return False
			elif "ClockS" in lst[1]:
				if lst[1][lst[1].index("ClockS") + 1] == 0 and ind not in stage:
					return False
				elif lst[1][lst[1].index("ClockS") + 1] > 0 and len(self.cont_times(lst[1], stage, self.cd)) < lst[1][
					lst[1].index("ClockS") + 1]:
					return False
			elif "Rest" in lst[1]:
				qty = lst[1][lst[1].index("Rest") + 1]
				if qty == 0 and self.cd[ind].status == "Rest":
					return False
				elif qty > 0:
					stage1 = list(stage)
					if "Other" in lst[1] and ind in stage1:
						stage1.remove(ind)

					if len([s for s in stage1 if s != "" and self.cd[s].status == "Stand"]) < qty:
						return False
					if "Trait" in lst[1]:
						trait = lst[1][lst[1].index("Trait") + 1]
						if len([s for s in stage1 if
						        s != "" and self.cd[s].status == "Stand" and trait in self.cd[s].trait_t]) < qty:
							return False
			elif "Marker" in lst[1]:
				qty = lst[1][lst[1].index("Marker") + 1]
				if ind in self.pd[ind[-1]]["marker"]:
					if len(self.pd[ind[-1]]["marker"]) < qty:
						return False
				else:
					return False
			if "Waiting" in lst[1]:
				if lst[1][lst[1].index("Waiting") + 1] == 0 and ind not in stage:
					return False
				elif lst[1][lst[1].index("Waiting") + 1] > 0 and len([s for s in stage if s != ""]) < lst[1][
					lst[1].index("Waiting") + 1]:
					return False
			elif "Memory" in lst[1]:
				if lst[1][lst[1].index("Memory") + 1] == 0 and ind not in stage:
					return False
			elif "Hander" in lst[1]:
				if lst[1][lst[1].index("Hander") + 1] == 0 and ind not in stage:
					return False
		return True

	def stack_popup(self, *args):
		# self.gd["p_ind"] = ind
		self.popup_clr_button()
		self.gd["p_over"] = False
		self.gd["p_c"] = "auto"
		self.gd["popup_done"] = (True, False)
		self.sd["popup"]["popup"].title = "Triggered AUTO abilities"
		self.sd["popup"]["stack"].do_scroll_y = False
		self.sd["popup"]["stack"].clear_widgets()
		self.gd["sn"] = {}

		height = self.sd["card"][1] + self.sd["padding"] * 0.75
		xscat = (self.sd["padding"] + self.sd["card"][0]) * (starting_hand + 1) + self.sd["padding"] * 2

		self.sd["btn"]["label"].text = "Choose which AUTO ability to activate first."
		self.sd["btn"]["label"].text_size = (xscat * 0.9, None)
		self.sd["btn"]["label"].texture_update()

		r = len(self.gd["stack"]["1"])

		if r > 6:
			self.sd["popup"]["stack"].do_scroll_y = True
			yscv = height * (r - 0.5)
		elif r > 0:
			yscv = height * r
		else:
			yscv = height
		yscv += self.sd["padding"]

		yscat = yscv + self.sd["card"][1]
		title = self.sd["popup"]["popup"].title_size + self.sd["popup"]["popup"].separator_height + \
		        self.sd["btn"]["label"].texture.size[1] + self.sd["card"][1]
		ypop = yscat + title

		if ypop > Window.height:
			self.gd["p_over"] = True
			ypop = Window.height * 0.9
			yscat = ypop - title
			yscv = yscat - self.sd["card"][1] * 0.75

		self.sd["popup"]["p_scv"].size = (xscat, yscv)
		self.sd["popup"]["popup"].size = (xscat, ypop)

		self.stack_btn_ability(len(self.gd["stack"]["1"]))
		self.cardinfo.inx = 10
		inx = 0
		for item in self.gd["stack"]["1"]:
			self.cpop[item[0]].selected(False)
			self.cpop[item[0]].update_text()
			repl = ""
			if self.cpop[item[0]] in self.sd["popup"]["stack"].children:
				for xx in self.cpop.keys():
					if xx.endswith("0") and self.cpop[xx] not in self.sd["popup"]["stack"].children:
						self.sd["popup"]["stack"].add_widget(self.cpop[xx])
						if self.cd[item[0]].cid == "player":
							self.cpop[xx].import_data("player")
						else:
							self.cpop[xx].import_data(sc[self.cd[item[0]].cid])
						self.gd["so"].append(xx)
						repl = xx
						break
			else:
				repl = item[0]
				self.sd["popup"]["stack"].add_widget(self.cpop[item[0]])

			if self.cd[item[0]].name in self.gd["sn"] and item[2] in self.gd["sn"][self.cd[item[0]].name]:
				if item[0] not in self.gd["sn"][self.cd[item[0]].name][item[2]]:
					self.gd["sn"][self.cd[item[0]].name][item[2]].append((item[0], repl))
			elif self.cd[item[0]].name in self.gd["sn"] and item[2] not in self.gd["sn"][self.cd[item[0]].name]:
				self.gd["sn"][self.cd[item[0]].name][item[2]] = [(item[0], repl)]
			else:
				self.gd["sn"][self.cd[item[0]].name] = {}
				self.gd["sn"][self.cd[item[0]].name][item[2]] = [(item[0], repl)]

			if ("do" in item[1] and "revive" in item[1][-1]) or "revive" in item[1]:
				if item[3] == item[0]:
					self.sd["sbtn"][
						f"{inx}"].btn.text = f"Target:\tThis card\n{self.cardinfo.replaceMultiple(item[2], True)}"
				else:
					self.sd["sbtn"][
						f"{inx}"].btn.text = f"Target:\t\"{self.cd[item[3]].name}\"\n{self.cardinfo.replaceMultiple(item[2], True)}"
			else:
				self.sd["sbtn"][f"{inx}"].btn.text = self.cardinfo.replaceMultiple(item[2], True)
			self.sd["sbtn"][f"{inx}"].btn.cid = str(self.gd["stack"]["1"].index(item))
			self.sd["sbtn"][f"{inx}"].btn.texture_update()
			self.sd["sbtn"][f"{inx}"].replaceImage()
			self.sd["popup"]["stack"].add_widget(self.sd["sbtn"][f"{inx}"])
			inx += 1

		nn = {}

		for nx in self.gd["sn"]:
			for ax in self.gd["sn"][nx]:
				if len(self.gd["sn"][nx][ax]) > 1:
					for nnx in range(len(self.gd["sn"][nx][ax])):
						if self.gd["sn"][nx][ax][nnx][0] not in nn:
							self.cd[self.gd["sn"][nx][ax][nnx][0]].update_text(nnx + 1)
							self.cpop[self.gd["sn"][nx][ax][nnx][1]].update_text(nnx + 1)
							nn[self.gd["sn"][nx][ax][nnx][0]] = nnx + 1
						elif self.gd["sn"][nx][ax][nnx][0] in nn:
							self.cd[self.gd["sn"][nx][ax][nnx][0]].update_text(nn[self.gd["sn"][nx][ax][nnx][0]])
							self.cpop[self.gd["sn"][nx][ax][nnx][1]].update_text(nn[self.gd["sn"][nx][ax][nnx][0]])

		self.sd["btn"]["field_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
		self.sd["btn"]["field_btn"].center_x = xscat / 2. - self.sd["card"][0] / 2 + self.sd["padding"] * 0.75
		self.sd["btn"]["field_btn"].y = self.sd["padding"] * 1.5

		self.sd["popup"]["p_scv"].y = self.sd["btn"]["field_btn"].y * 2.5 + self.sd["btn"]["field_btn"].size[1]
		self.sd["popup"]["p_scv"].scroll_y = 1

		self.sd["btn"]["label"].pos = (
			self.sd["padding"] / 2.,
			self.sd["popup"]["p_scv"].y + self.sd["popup"]["p_scv"].size[1])  # -self.sd["padding"]*5)

		self.sd["popup"]["popup"].open()

	def level(self, *args):
		if "power" in self.gd["effect"]:
			inx = self.gd["effect"].index("power") + 1
		else:
			inx = 0
		idm = self.gd["ability_trigger"].split("_")[1]
		if self.gd["effect"][inx] > 0:
			# if self.gd["effect"][0] == 1:
			for r in range(len(self.gd["target"])):
				temp = self.gd["target"].pop(0)
				if temp != "":
					self.cd[temp].level_c.append(
							[self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"],
							 self.gd["turn"]])
					self.cd[temp].update_level()
					if "extra" in self.gd["effect"]:
						self.gd["extra"].append(temp)
				if self.net["game"]:  # @@
					self.net["act"][4].append(temp)
				if "power" in self.gd["effect"]:
					self.gd["target"].append(temp)
					if self.net["game"]:  # @@
						self.net["act"][4].remove(temp)
		elif self.gd["effect"][inx] == 0:
			self.cd[idm].level_c.append(
					[self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"],
					 self.gd["turn"]])
			self.cd[idm].update_level()
		elif self.gd["effect"][inx] < 0:
			if self.gd["effect"][inx] == -1:
				for ind in self.pd[idm[-1]]["Center"] + self.pd[idm[-1]]["Back"]:
					if ind != "":
						self.cd[ind].level_c.append(
								[self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"],
								 self.gd["turn"]])
						self.cd[ind].update_level()
			elif self.gd["effect"][inx] == -2:
				for ind in self.pd[idm[-1]]["Center"] + self.pd[idm[-1]]["Back"]:
					if ind != "" and ind != idm:
						self.cd[ind].level_c.append(
								[self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"],
								 self.gd["turn"]])
						self.cd[ind].update_level()

		if "level" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("level")

		self.do_check(True)

	def power(self, dt=0, *args):
		idm = self.gd["ability_trigger"].split("_")[1]
		power_zero = []
		if self.gd["effect"][0] > 0:
			if self.gd["effect"][0] == 1:
				if "X" in self.gd["effect"][3]:
					stage = list(self.pd[idm[-1]]["Center"] + self.pd[idm[-1]]["Back"])
					tx = 0
					if "xName" in self.gd["effect"]:
						tx = len(self.cont_times(self.gd["effect"], stage, self.cd))
					elif "xlevel" in self.gd["effect"]:
						tx = self.cd[self.gd["target"][0]].level_t
					elif "xplevel" in self.gd["effect"]:
						tx = len(self.pd[idm[-1]]["Level"])
					self.gd["effect"][1] = tx * self.gd["effect"][self.gd["effect"].index("x") + 1]
				elif "#" in self.gd["effect"][3]:
					tx = 0
					if "Center" in self.gd["effect"]:
						stage = list(self.pd[idm[-1]]["Center"])
					elif "Back" in self.gd["effect"]:
						stage = list(self.pd[idm[-1]]["Back"])
					else:
						stage = list(self.pd[idm[-1]]["Center"] + self.pd[idm[-1]]["Back"])

					if "#other" in self.gd["effect"] and idm in stage:
						stage.remove(idm)
					if "#trait" in self.gd["effect"]:
						trr = self.gd["effect"][self.gd["effect"].index("#trait") + 1].split("_")
						tx = len([s for s in stage if any(tr in self.cd[s].trait_t for tr in trr)])
					elif "#stock" in self.gd["effect"]:
						tx = len(self.pd[idm[-1]]["Stock"])
					if "negative" in self.gd["effect"]:
						tx = -tx
					self.gd["effect"][1] = tx * self.gd["effect"][1]

				temp = self.gd["target"].pop(0)
				if "extra" in self.gd["effect"]:
					self.gd["extra"].append(temp)
				if temp != "" and self.gd["effect"][1] != 0:
					self.cd[temp].power_c.append(
							[self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"], self.gd["turn"]])
					self.cd[temp].update_power()
					if self.cd[temp].power_t <= 0:
						power_zero.append(temp)
				if self.net["game"]:  # @@
					self.net["act"][4].append(temp)
			else:
				for r in range(len(self.gd["target"])):
					temp = self.gd["target"].pop(0)
					if "extra" in self.gd["effect"]:
						self.gd["extra"].append(temp)
					if temp != "" and self.gd["effect"][1] != 0:
						self.cd[temp].power_c.append(
								[self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"],
								 self.gd["turn"]])
						self.cd[temp].update_power()
						if self.cd[temp].power_t <= 0:
							power_zero.append(temp)
					if self.net["game"]:  # @@
						self.net["act"][4].append(temp)
		elif self.gd["effect"][0] == 0:
			card = self.cd[idm]
			if any(st in card.pos_new for st in self.stage):
				if "random" in self.gd["effect"]:
					self.gd["effect"][1] = choice([s for s in range(self.gd["effect"][1], self.gd["effect"][
						self.gd["effect"].index("random") + 1] + 500, 500)])

				if "lvl" in self.gd["effect"]:
					if "opp" in self.gd["effect"]:
						if card.ind[-1] == "1":
							op = "2"
						else:
							op = "1"
						m = [2, 1, 0]
						opp = self.pd[op]["Center"][m[int(card.pos_new[-1])]]
						if opp != "" and self.cd[opp].level >= self.gd["effect"][self.gd["effect"].index("lvl") + 1]:
							card.power_c.append([self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"],
							                     self.gd["turn"]])
				elif "X" in self.gd["effect"]:
					times = 0
					if "xsoul" in self.gd["effect"]:
						times = card.soul_t
					card.power_c.append(
							[self.gd["effect"][1] * times, self.gd["effect"][2], self.gd["ability_trigger"],
							 self.gd["turn"]])
				elif "#" in self.gd["effect"]:
					ind = self.gd["ability_trigger"].split("_")[1]
					times = 0

					if "Center" in self.gd["effect"]:
						stage = list(self.pd[ind[-1]]["Center"])
					elif "Back" in self.gd["effect"]:
						stage = list(self.pd[ind[-1]]["Back"])
					else:
						stage = list(self.pd[ind[-1]]["Center"] + self.pd[ind[-1]]["Back"])

					if "other" in self.gd["effect"] and ind in stage:
						stage.remove(ind)

					if "Stock" in self.gd["effect"]:
						times = len(self.pd[idm[-1]]["Stock"])
					elif "Traits" in self.gd["effect"]:
						times = []
						for t in stage:
							for tr in self.cd[t].trait_t:
								if tr not in times:
									times.append(tr)
						times = len(times)
					else:
						times = len(self.cont_times(self.gd["effect"], stage, self.cd))

					card.power_c.append(
							[self.gd["effect"][1] * times, self.gd["effect"][2], self.gd["ability_trigger"],
							 self.gd["turn"]])

				else:
					card.power_c.append(
							[self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"], self.gd["turn"]])
				card.update_power()
				if card.power_t <= 0:
					power_zero.append(card.ind)
		elif self.gd["effect"][0] < 0:
			if self.gd["effect"][0] == -1:
				for ind in self.cont_times(self.gd["effect"], self.cont_cards(self.gd["effect"], idm), self.cd):
					if ind != "":
						self.cd[ind].power_c.append(
								[self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"],
								 self.gd["turn"]])
						self.cd[ind].update_power()
						if self.cd[ind].power_t <= 0:
							power_zero.append(ind)
			elif self.gd["effect"][0] == -2:
				for ind in self.pd[idm[-1]]["Center"] + self.pd[idm[-1]]["Back"]:
					if ind != "" and ind != idm:
						self.cd[ind].power_c.append(
								[self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"],
								 self.gd["turn"]])
						self.cd[ind].update_power()
						if self.cd[ind].power_t <= 0:
							power_zero.append(ind)
			elif self.gd["effect"][0] == -3:
				ind = self.gd["effect"][self.gd["effect"].index("target") + 1]
				if "extra" in self.gd["effect"]:
					self.gd["extra"].append(ind)
				self.cd[ind].power_c.append(
						[self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"], self.gd["turn"]])
				self.cd[ind].update_power()
				if self.cd[ind].power_t <= 0:
					power_zero.append(ind)
			elif self.gd["effect"][0] == -10:
				ind = choice([s for s in self.pd[idm[-1]]["Center"] + self.pd[idm[-1]]["Back"] if s != ""])
				self.cd[ind].power_c.append(
						[self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"], self.gd["turn"]])
				self.cd[ind].update_power()
				if self.cd[ind].power_t <= 0:
					power_zero.append(ind)
			elif self.gd["effect"][0] == -11:
				if idm[-1] == "1":
					opp = "2"
				elif idm[-1] == "2":
					opp = "1"
				ind = choice([s for s in self.pd[opp]["Center"] + self.pd[opp]["Back"] if s != ""])
				self.cd[ind].power_c.append(
						[self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"], self.gd["turn"]])
				self.cd[ind].update_power()
				if self.cd[ind].power_t <= 0:
					power_zero.append(ind)
			elif self.gd["effect"][0] == -16:
				for ind in list(self.gd["extra"]):
					if "extra" not in self.gd["effect"]:
						self.gd["extra"].remove(ind)
					self.cd[ind].power_c.append(
							[self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"], self.gd["turn"]])
					self.cd[ind].update_power()
					if self.cd[ind].power_t <= 0:
						power_zero.append(ind)

		if "power" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("power")

		for pind in reversed(power_zero):
			self.gd["no_cont_check"] = True
			self.send_to_waiting(pind)

		self.do_check(True)

	def reverser(self, *args):
		idm = self.gd["ability_trigger"].split("_")[1]
		ss = True
		if self.gd["effect"][0] == -3:
			if idm[-1] == "1" or (idm[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(self.gd["effect"][self.gd["effect"].index("target") + 1])
			self.gd["effect"][0] = 1
			ss = False
		for r in range(self.gd["effect"][0]):
			ind = self.gd["target"].pop(0)
			if self.net["game"] and idm[-1] == "1" and ss:
				self.net["act"][4].append(ind)
			if ind in self.emptycards:
				continue
			# if "Stock" in self.gd["effect"]:
			# 	self.send_to_stock(ind)
			# 	self.do_check()
			# elif "top" in self.gd["effect"]:
			# 	self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
			# 	self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])
			# 	self.pd[ind[-1]][self.cd[ind].pos_new[:-1]][self.cd[ind].pos_new[-1]] = ""
			# 	self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Library"], t="Library")
			# 	self.pd[ind[-1]]["Library"].append(ind)
			# 	self.update_field_label()
			# 	self.check_cont_ability()
			# 	self.auto_check()
			# else:
			rev = True
			for text in self.cd[ind].text_c:
				if text[0].startswith(cont_ability) and text[1] != 0 and text[1] > -9:
					eff = ab.cont(text[0])
					if "no_reverse_auto" in eff:
						rev = False
						break
			if rev:
				self.cd[ind].reverse()
			self.check_bodyguard()
			self.check_auto_ability(rev=[ind], stacks=False)

		if "reverser" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("reverser")

		self.gd["confirm_result"] = ""
		self.ability_effect()

	def soul(self, *args):
		if "power" in self.gd["effect"]:
			inx = self.gd["effect"].index("power") + 1
		else:
			inx = 0

		idm = self.gd["ability_trigger"].split("_")[1]
		if self.gd["effect"][inx] == -12:
			self.gd["effect"][inx] = 0
			idm = self.gd["attacking"][0]

		if self.gd["effect"][inx] > 0:
			# if self.gd["effect"][0] == 1:
			for r in range(len(self.gd["target"])):
				temp = self.gd["target"].pop(0)
				if temp != "":
					if "extra" in self.gd["effect"]:
						self.gd["extra"].append(temp)
					self.cd[temp].soul_c.append(
							[self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"],
							 self.gd["turn"]])
					self.cd[temp].update_soul()
				if self.net["game"]:  # @@
					self.net["act"][4].append(temp)
				if "power" in self.gd["effect"]:
					self.gd["target"].append(temp)
					if self.net["game"]:  # @@
						self.net["act"][4].remove(temp)

		elif self.gd["effect"][inx] == 0:
			if any(st in self.cd[idm].pos_new for st in self.stage):
				self.cd[idm].soul_c.append(
						[self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"],
						 self.gd["turn"]])
				self.cd[idm].update_soul()
		elif self.gd["effect"][inx] < 0:
			if self.gd["effect"][inx] == -1:
				if "random" in self.gd["effect"]:
					self.gd["effect"][1 + inx] = choice([s for s in range(self.gd["effect"][1 + inx], self.gd["effect"][
						self.gd["effect"].index("random") + 1 + inx] + 1)])
				# for ind in self.pd[idm[-1]]["Center"] + self.pd[idm[-1]]["Back"]:

				for ind in self.cont_times(self.gd["effect"], self.cont_cards(self.gd["effect"], idm), self.cd):
					if ind != "":
						self.cd[ind].soul_c.append(
								[self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"],
								 self.gd["turn"]])
						self.cd[ind].update_soul()
			elif self.gd["effect"][inx] == -18:
				cc = self.gd["effect"][self.gd["effect"].index("player") + 1]
				for ind in self.pd[cc]["Center"] + self.pd[cc]["Back"]:
					if ind != "":
						self.cd[ind].soul_c.append(
								[self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"],
								 self.gd["turn"]])
						self.cd[ind].update_soul()
			elif self.gd["effect"][0] == -16:
				for ind in list(self.gd["extra"]):
					if "extra" not in self.gd["effect"]:
						self.gd["extra"].remove(ind)
					self.cd[ind].soul_c.append(
							[self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"], self.gd["turn"]])
					self.cd[ind].update_soul()

		if "soul" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("soul")

		self.do_check(True)

	# self.ability_effect()

	def trait(self, *args):
		if "power" in self.gd["effect"]:
			inx = self.gd["effect"].index("power") + 1
		else:
			inx = 0

		idm = self.gd["ability_trigger"].split("_")[1]
		if self.gd["effect"][inx] == -12:
			self.gd["effect"][inx] = 0
			idm = self.gd["attacking"][0]

		if self.gd["effect"][inx] > 0:
			# if self.gd["effect"][0] == 1:
			for r in range(len(self.gd["target"])):
				temp = self.gd["target"].pop(0)
				if temp != "":
					if "extra" in self.gd["effect"]:
						self.gd["extra"].append(temp)
					self.cd[temp].trait_c.append(
							[self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"],
							 self.gd["turn"]])
					self.cd[temp].update_trait()
				if self.net["game"]:  # @@
					self.net["act"][4].append(temp)
				if "power" in self.gd["effect"]:
					self.gd["target"].append(temp)
					if self.net["game"]:  # @@
						self.net["act"][4].remove(temp)

		elif self.gd["effect"][inx] == 0:
			if any(st in self.cd[idm].pos_new for st in self.stage):
				self.cd[idm].trait_c.append(
						[self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"],
						 self.gd["turn"]])
				self.cd[idm].update_trait()
		elif self.gd["effect"][inx] < 0:
			if self.gd["effect"][inx] == -1:
				for ind in self.cont_times(self.gd["effect"], self.cont_cards(self.gd["effect"], idm), self.cd):
					if ind != "":
						self.cd[ind].trait_c.append(
								[self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"],
								 self.gd["turn"]])
						self.cd[ind].update_trait()
			elif self.gd["effect"][0] == -16:
				for ind in list(self.gd["extra"]):
					if "extra" not in self.gd["effect"]:
						self.gd["extra"].remove(ind)
					self.cd[ind].trait_c.append(
							[self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"],
							 self.gd["turn"]])
					self.cd[ind].update_trait()

		if "trait" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("trait")

		self.do_check(True)

	def rest_card(self, ind, rested=False):
		self.cd[ind].rest()
		self.gd["check_atk"] = True
		self.rested_card_update()
		self.check_cont_ability()
		if not rested:
			self.check_auto_ability(rst=ind, stacks=False)

	def restart(self):
		self.rect.source = f"atlas://{img_in}/other/blank"
		self.rect.pos = (-Window.width * 2, -Window.height * 2)
		self.rect1.source = f"atlas://{img_in}/other/blank"
		self.rect1.pos = (-Window.width * 2, -Window.height * 2)
		self.gd["starting_player"] = ""
		self.gd["second_player"] = ""
		self.gd["active"] = ""
		self.gd["opp"] = ""
		self.gd["phase"] = ""
		self.clear_ability()

		for ind in self.cd:
			if ind in self.emptycards or ind == "1" or ind == "2":
				continue
			self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Library"], t="Library")

		self.sd["menu"]["popup"].size = (Window.width * 0.6, Window.height * 0.4)
		self.sd["menu"]["wl_box"].remove_widget(self.sd["menu"]["wl"])

		for label in phases + steps:
			self.sd["label"][label].center_y = Window.height / 2
			self.sd["label"][label].x = -Window.width * 2

		# self.net = network_init()
		for player in list(self.pd.keys()):
			for key in self.pd[player]:
				# if key in ("dict", "deck"):
				if key in "deck":
					self.pd[player][key] = {}
				elif key in ("phase", "done"):
					for item in self.pd[player][key]:
						self.pd[player][key][item] = False
				elif key in ("deck_id", "deck_name", "name", "janken"):
					self.pd[player][key] = ""
				elif key in (
						"Hand", "Res", "Clock", "Level", "Climax", "Stock", "Memory", "Waiting"):
					for inx in range(len(self.pd[player][key])):
						temp = self.pd[player][key].pop()
						self.pd[player]["Library"].append(temp)
				elif key in "colour":
					self.pd[player][key] = []
				elif key in "marker":
					for ind in self.pd[player][key]:
						for item in self.pd[player][key][ind]:
							self.pd[player]["Library"].append(item[0])
						self.pd[player][key][ind] = []
				elif key in ("Center", "Back"):
					for inx in range(len(self.pd[player][key])):
						if self.pd[player][key][inx] != "":
							self.pd[player]["Library"].append(self.pd[player][key][inx])
							self.pd[player][key][inx] = ""

		for field in self.field_label:
			self.field_label[field].x -= Window.width * 2

		for field in self.field_btn:
			self.field_btn[field].x = -Window.width * 2
		for label in phases + steps:
			self.sd["label"][label].color = (.5, .5, .5, 1.)

		for ss in ("Clock",):
			self.sd["btn"][f"{ss}_btn"].text = f"End {ss}"

		for fields in self.gd["select_btns"]:
			if "Clock" in fields:
				for ind in self.pd[fields[-1]]["Clock"]:
					self.cd[ind].selectable(False)
			elif ("Stage" in self.gd["status"] or self.gd["move"]) and fields[:-1] in self.gd["stage"]:
				self.field_btn[f"{fields}s"].x = -Window.width * 3
			else:
				if "Climax" in fields:
					self.cd[self.pd[fields[-1]][fields[:-1]][0]].selectable(False)
				else:
					self.cd[self.pd[fields[-1]][fields[:-2]][int(fields[-2])]].selectable(False)

		self.gd["select_btns"] = []
		self.gd["mstock"] = ""
		self.sd["btn"]["end"].y = -Window.height
		self.sd["btn"]["end_attack"].y = -Window.height
		self.sd["btn"]["end_phase"].y = -Window.height
		self.sd["btn"]["continue"].y = -Window.height
		self.sd["btn"]["draw_upto"].y = -Window.height
		self.sd["btn"]["ablt_info"].y = -Window.height
		self.gd["rev"] = False
		self.act_ability_show(hide=True)
		self.hand_btn_show(False)
		self.popup_clr()

	def start_game(self, *args):
		self.sd["menu"]["popup"].dismiss()
		self.main_scrn.pos = (-Window.width, -Window.height)
		self.main_scrn.disabled = False
		self.network["m_connect"].disabled = False
		self.network["popup"].dismiss()

		if self.gd["gg"] or self.gd["menu"]:
			self.gd["gg"] = False
			self.gd["menu"] = False
			self.restart()

		self.sd["menu"]["btn"].size = (Window.width * 2 / 15., self.sd["b_bar"].size[1])
		self.sd["menu"]["btn"].x = Window.width - self.sd["menu"]["btn"].size[0]
		self.sd["menu"]["btn"].y = Window.height - self.sd["menu"]["btn"].size[1]
		self.sd["menu"]["btn"].disabled = True
		try:
			self.parent.add_widget(self.sd["menu"]["btn"])
		except WidgetException:
			pass

		self.sd["btn"]["label"].text = ""
		self.sd["btn"]["label"].texture_update()
		self.gd["shuffle_trigger"] = "turn0"
		self.gd["turn"] = 0

		if self.gd["debug"] and not self.net["game"]:
			try:
				self.parent.add_widget(self.sd["debug"]["box"])
			except WidgetException:
				pass
			self.sd["debug"]["box"].size = (self.sd["card"][0] * 3, self.sd["b_bar"].size[1])
			self.sd["debug"]["box"].x = 0
			self.sd["debug"]["box"].y = Window.height - self.sd["debug"]["box"].size[1]

		if self.net["game"]:
			self.sd["text"]["popup"].dismiss()

		for player in list(self.pd.keys()):
			if self.decks[player][3]:
				mat = choice([s for s in sp.keys() if sp[s]["c"]])
				self.import_mat(player, mat)
			else:
				self.import_mat(player, self.decks[player][1])

			self.scale_mat(t=False, player=player)
			# self.mat[player].import_mat(sd[self.mat[player]["id"]],self.mat[player]["per"])

			if player == "2" and self.net["game"]:
				self.import_deck(player, self.decks[player][0])
			elif self.decks[player][2]:
				deck = choice([s for s in sd.keys() if sd[s]["c"]])
				self.import_deck(player, deck)
			else:
				self.import_deck(player, self.decks[player][0])

		self.sd["b_bar"].x = 0
		self.sd["t_bar"].x = 0
		self.sd["t_bar"].y = Window.height - self.sd["menu"]["btn"].size[1]
		self.sd["b_bar"].y = 0
		self.mat["1"]["mat"].x = (Window.width - self.mat["1"]["mat"].size[0]) / 2
		self.mat["1"]["mat"].y = Window.height / 2 - self.sd["padding"] - self.sd["card"][1] / 6 - self.mat["1"][
			"mat"].height
		self.mat["2"]["mat"].reverse()

		self.mat["2"]["mat"].x = (Window.width - self.mat["2"]["mat"].size[0]) / 2
		self.mat["2"]["mat"].y = Window.height / 2 + self.sd["padding"] + self.sd["card"][1] / 6
		self.rect.size = (
			Window.width + self.sd["card"][0],
			Window.height / 2 - self.sd["padding"] - self.sd["card"][1] / 6)  # - self.sd["menu"]["btn"].size[1])

		self.field_btn_pos()

		self.change_label()
		for label in phases:
			self.sd["label"][label].center_y = Window.height / 2

		try:
			self.parent.add_widget(self.sd["btn"]["end"])
		except WidgetException:
			pass
		try:
			self.parent.add_widget(self.sd["btn"]["end_attack"])
		except WidgetException:
			pass
		try:
			self.parent.add_widget(self.sd["btn"]["end_phase"])
		except WidgetException:
			pass
		try:
			self.parent.add_widget(self.sd["btn"]["ablt_info"])
		except WidgetException:
			pass
		try:
			self.parent.add_widget(self.sd["btn"]["draw_upto"])
		except WidgetException:
			pass
		try:
			self.parent.add_widget(self.sd["btn"]["continue"])
		except WidgetException:
			pass
		try:
			self.parent.add_widget(self.sd["btn"]["end_eff"])
		except WidgetException:
			pass

		self.deck_fill()
		self.gd["game_start"] = True  # @@@@
		self.add_field_label()
		self.update_field_label()
		self.shuffle("0")

	# self.gd["p_width"] = self.sd["padding"] + self.sd["card"][0]
	# self.check_condition("11")

	def str_dict(self, deck):
		temp = {}
		for ind in deck.split("~")[1].split(","):
			i, j = ind.split(":")
			temp[i] = int(j)
		return temp

	def import_deck(self, owner, deck):
		# import deck data from database
		if owner == "2" and deck.startswith("CEJ") and self.net["game"]:
			self.pd[owner]["deck"] = self.str_dict(deck)
			self.pd[owner]["deck_name"] = "Custom"
			self.pd[owner]["deck_id"] = deck.split("!")[0]
		else:
			self.pd[owner]["deck"] = sd[deck]["deck"]
			self.pd[owner]["deck_name"] = sd[deck]["name"]
			self.pd[owner]["deck_id"] = deck

	def import_mat(self, player, mat="mat"):
		self.mat[player]["id"] = mat
		self.mat[player]["mat"].import_mat(sp[mat], self.mat[player]["per"])

	def clear_deck_pop(self, *args):
		self.decks["stack"].clear_widgets()

	def popup_deck_start(self, *args):
		self.decks = {}
		self.decks["1"] = ["S11E000", "mat", False, False]
		self.decks["2"] = ["S11E000", "mat", False, False]
		self.decks["popup"] = Popup()
		self.decks["popup"].bind(on_dismiss=self.clear_deck_pop)
		self.decks["sctm"] = RelativeLayout(size_hint=(1, 1))
		self.decks["stack"] = StackLayout(orientation="lr-tb", size_hint_y=None, padding=self.sd["padding"] / 2,
		                                  spacing=self.sd["padding"])
		self.decks["stack"].bind(minimum_height=self.decks["stack"].setter('height'))
		self.decks["sspaced"] = StackSpacer(o=(self.sd["card"][0] * 1.5, self.sd["card"][1] * 1.5))
		self.decks["scv"] = ScrollView(do_scroll_x=False, size_hint=(1, None))
		self.decks["p_info"] = None
		self.decks["selected"] = ""
		self.decks["dbuilding"] = ""
		self.decks["build_pop"] = False
		self.decks["dbuild"] = {}
		self.decks["dbtn"] = {}
		self.decks["imgs"] = []
		self.decks["add_chosen"] = []
		self.decks["img_pop"] = False
		self.decks["sets"] = Popup()
		self.decks["sets"].size = (self.sd["card"][0] * 6, self.sd["card"][1])
		self.decks["rv_rel"] = RelativeLayout(size_hint=(1, None))
		self.decks["rv_all"] = Button(size_hint=(None, None), text="Download All", on_release=self.deck_set_title_btn,
		                              size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.), cid="all")
		self.decks["rv_close"] = Button(size_hint=(None, None), text="Close", on_release=self.deck_set_title_btn,
		                                size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.), cid="close")
		self.decks["rv"] = RV()
		self.decks["rv"].bind(set_title=self.deck_set_title)
		self.decks["rv"].box.padding = self.sd["padding"]
		self.decks["rv"].box.spacing = self.sd["padding"]

		self.decks["close"] = Button(size_hint=(None, None), text="Close", on_release=self.popup_deck_slc,
		                             size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.), cid="")
		self.decks["confirm"] = Button(cid="1", size_hint=(None, None), text="Confirm", on_release=self.popup_deck_slc,
		                               size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.))

		self.decks["dismantle"] = Button(size_hint=(None, None), text="Dismantle", on_release=self.popup_deck_slc,
		                                 size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.), cid="z")
		self.decks["dismantle"].disabled = True
		self.decks["create"] = Button(cid="c", size_hint=(None, None), text="Create new",
		                              on_release=self.popup_deck_slc,
		                              size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.))
		self.decks["save"] = Button(cid="done", size_hint=(None, None), text="Save & Exit",
		                            on_release=self.building_btn,
		                            size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.))

		self.decks["rearrange"] = Button(cid="r", size_hint=(None, None), text="Confirm",
		                                 on_release=self.popup_deck_slc,
		                                 size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.))
		self.decks["back"] = Button(cid="b", size_hint=(None, None), text="Back", on_release=self.popup_deck_slc,
		                            size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.))

		self.decks["setting_pop"] = False
		self.decks["st"] = {}
		self.decks["st"]["name"] = Label(text="Deck Name", halign='center', valign='middle', outline_width=1.9)
		self.decks["st"]["name_btn"] = TextInput(text="", cid="name")
		self.decks["st"]["name_btn"].bind(text=self.deck_set_slc)
		self.decks["st"]["name_box"] = BoxLayout(orientation="vertical", size_hint=(1, None))
		self.decks["st"]["format"] = Label(text="Format", halign='center', valign='middle', outline_width=1.9)
		self.decks["st"]["lang"] = Label(text="Language", halign='center', valign='middle', outline_width=1.9)
		self.decks["st"]["lang_spn"] = Spinner(text="Both", values=("Both", "Jap", "Eng"), cid="lang")
		self.decks["st"]["lang_spn"].bind(text=self.deck_set_slc)
		self.decks["st"]["lang_box"] = BoxLayout(orientation="horizontal", size_hint=(1, None))
		self.decks["st"]["format_spn"] = Spinner(text="-",
		                                         values=("Standard", "Side", "Neo-Standard", "Title-Specific"),
		                                         cid="format")
		self.decks["st"]["format_spn"].bind(text=self.deck_set_slc)
		self.decks["st"]["format_btn"] = Button(text="", on_press=self.deck_set_slc, cid="title", disabled=True,
		                                        halign='center', valign='middle', max_lines=1)
		self.decks["st"]["format_box"] = BoxLayout(orientation="vertical", size_hint=(1, None))
		self.decks["st"]["format_box1"] = BoxLayout(orientation="horizontal", size_hint=(1, 1))
		self.decks["st"]["image"] = Label(text="Default Image", halign='center', valign='middle',
		                                  outline_width=1.9, max_lines=1)
		self.decks["st"]["image_btn"] = ImgButton(self.sd["card"], self.sd["card"], cid="image",
		                                          source=f"atlas://{img_in}/other/empty")
		self.decks["st"]["image_btn"].btn.bind(on_press=self.deck_set_slc)
		self.decks["st"]["image_box"] = BoxLayout(orientation="vertical", size_hint=(1, None))

		self.decks["st"]["name_box"].add_widget(self.decks["st"]["name"])
		self.decks["st"]["name_box"].add_widget(self.decks["st"]["name_btn"])
		self.decks["st"]["format_box1"].add_widget(self.decks["st"]["format"])
		self.decks["st"]["format_box1"].add_widget(self.decks["st"]["format_spn"])
		self.decks["st"]["format_box"].add_widget(self.decks["st"]["format_box1"])
		self.decks["st"]["format_box"].add_widget(self.decks["st"]["format_btn"])
		self.decks["st"]["image_box"].add_widget(self.decks["st"]["image"])
		self.decks["st"]["image_box"].add_widget(self.decks["st"]["image_btn"])
		self.decks["st"]["lang_box"].add_widget(self.decks["st"]["lang"])
		self.decks["st"]["lang_box"].add_widget(self.decks["st"]["lang_spn"])

		self.decks["add_btn"] = Button(size_hint=(0.3, 1), text="Add Card", cid="add",
		                               on_press=self.building_btn)
		self.decks["name_btn"] = Button(size_hint=(0.2, 1), text="Setting", cid="name",
		                                on_press=self.building_btn)
		self.decks["done_btn"] = Button(size_hint=(0.2, 1), text="Done", cid="done",
		                                on_press=self.building_btn)

		self.decks["50"] = Label(text="00/50", halign='center', valign='middle', outline_width=1.9, size_hint=(0.15, 1))
		self.decks["8"] = Label(text="0/8", halign='center', valign='middle', outline_width=1.9, size_hint=(0.15, 1))
		self.decks["dbuild_btn"] = BoxLayout(orientation="horizontal", size=(Window.width, self.sd["card"][1] / 2),
		                                     size_hint=(None, None))

		for item in ("done_btn", "50", "add_btn", "8", "name_btn"):
			self.decks["dbuild_btn"].add_widget(self.decks[item])

		self.decks["popup"].content = self.decks["sctm"]
		self.decks["sctm"].add_widget(self.decks["scv"])
		self.decks["sctm"].add_widget(self.decks["close"])
		self.decks["sctm"].add_widget(self.decks["confirm"])
		self.decks["scv"].add_widget(self.decks["stack"])

		self.decks["rv_rel"].add_widget(self.decks["rv_all"])
		self.decks["rv_rel"].add_widget(self.decks["rv_close"])
		self.decks["rv_rel"].add_widget(self.decks["rv"])

		self.decks["dbtn"] = {}
		pos = (-Window.width * 3, -Window.height * 3)
		size = (self.sd["card"][1], self.sd["card"][0] / 2)
		size1 = (self.sd["card"][1] / 2, self.sd["card"][0] / 2)
		for nx in range(1, 51):
			if f"{nx}1bb" in self.decks["dbtn"]:
				continue
			self.decks["dbtn"][f"{nx}1bb"] = BoxLayout(orientation="horizontal", pos=pos, size=size,
			                                           size_hint=(None, None))
			self.decks["dbtn"][f"{nx}1+"] = Button(text="+", size_hint=(0.38, 1), cid=f"{nx}1+")
			self.decks["dbtn"][f"{nx}1-"] = Button(text="-", size_hint=(0.38, 1), cid=f"{nx}1-")
			self.decks["dbtn"][f"{nx}1t"] = Label(text="0", halign='center', size_hint=(0.24, 1), valign="middle")

			self.decks["dbtn"][f"{nx}1bb"].add_widget(self.decks["dbtn"][f"{nx}1-"])
			self.decks["dbtn"][f"{nx}1bb"].add_widget(self.decks["dbtn"][f"{nx}1t"])
			self.decks["dbtn"][f"{nx}1bb"].add_widget(self.decks["dbtn"][f"{nx}1+"])

			self.decks["dbtn"][f"{nx}1b+"] = Button(text="", size_hint=(None, None), opacity=0, cid=f"{nx}1+",
			                                        on_release=self.add_card, pos=pos, size=size1)
			self.decks["dbtn"][f"{nx}1b-"] = Button(text="", size_hint=(None, None), opacity=0, cid=f"{nx}1-",
			                                        on_release=self.remove_card, pos=pos, size=size1)

			self.parent.add_widget(self.decks["dbtn"][f"{nx}1b+"])
			self.parent.add_widget(self.decks["dbtn"][f"{nx}1b-"])

		self.sd["dpop_press"] = []
		self.popup_deck(t="start")

	def deck_set_slc(self, inst, value=""):
		if self.decks["setting_pop"]:
			if inst.cid == "image":
				if len(self.decks["dbuild"]["deck"]) > 0:
					self.sd["popup"]["popup"].title = "Choose an Image"
					self.popup_start(c="Image")
			elif inst.cid == "format":
				self.decks["dbuild"]["n"] = value.split("-")[0]
				self.decks["close"].disabled = False
				if value == "Standard":
					self.decks["st"]["format_btn"].disabled = True
					self.decks["st"]["format_btn"].text = ""
					self.decks["dbuild"]["t"] = ""
				else:
					self.decks["st"]["format_btn"].disabled = False
					self.deck_title_pop()
			elif inst.cid == "name":
				self.decks["name"] = value
				self.decks["dbuild"]["name"] = value
			elif inst.cid == "lang":
				self.decks["lang"] = value
				if value == "Both":
					self.decks["dbuild"]["l"] = ""
				else:
					self.decks["dbuild"]["l"] = value.lower()[0]
			elif inst.cid == "title":
				self.decks["rv"].set_title = ""
				self.deck_title_pop("title")
			elif inst.cid == "sets":
				pass

	def deck_set_title_btn(self, btn):
		self.deck_set_title(btn, btn.cid)

	def deck_set_title(self, inst, val):
		if val != "":
			if val != "close":
				# for btn in self.sd["main_btn"]:
				# 	btn.disabled = True
				if val == "all":
					self.net["var"] = [str(val), 0]
					self.temp = []
					for var in se["check"].keys():
						if any(var == self.decks["rv"].data[ids]["id"] for ids in range(len(self.decks["rv"].data))):
							temp = str(var)
							temp1 = [str(var), 0]
							for item in se["check"][var]:
								if "-d" in item and exists(f"{data_ex}/{item}"):
									temp += "~d"
									temp1.append("d")
								elif "-" in item and "-d" not in item and exists(f"{img_ex}/{item}"):
									temp += f"~{item[-1]}"
									temp1.append(f"{item[-1]}")
							self.net["var"].append(temp)
							self.temp.append(temp1)
					self.net["var1"] = f"down_{val}"
					self.mconnect("down")
				elif val in se["check"]:
					self.net["var"] = [str(val), 0]
					for item in se["check"][val]:
						if "-d" in item and exists(f"{data_ex}/{item}"):
							self.net["var"].append("d")
						elif "-" in item and "-d" not in item and exists(f"{img_ex}/{item}"):
							self.net["var"].append(f"{item[-1]}")
					self.net["var1"] = f"down_{val}"
					self.mconnect("down")
				else:
					self.decks["dbuild"]["t"] = val
					self.decks["st"]["format_btn"].text = val
					self.decks["sets"].dismiss()
			else:
				self.decks["sets"].dismiss()
			self.decks["rv"].set_title = ""
		# for btn in self.sd["main_btn"]:
		# 	btn.disabled = False

	def deck_title_pop(self, t=""):
		self.decks["rv"].data = []
		data = []
		self.decks["rv"].do_scroll_y = False
		size = (self.sd["card"][0] * 5.6, self.sd['card'][1] / 1.25)
		text = (self.sd["card"][0] * 5.4, self.sd['card'][1] / 1.25)
		if "down" in t:
			self.decks["sets"].title = f"Choose a package to download"
			if "B" in t[-1] or "E" in t[-1] or "T" in t[-1]:
				sets = [s for s in se["check"].keys() if s.startswith(t[-1].lower())]
			else:
				sets = [s for s in se["check"].keys() if all(not s.startswith(ss) for ss in ("b", "e", "t"))]

			for set in sets:
				down = False
				for item in se["check"][set]:
					if "-d" in item and not exists(f"{data_ex}/{item}"):
						down = True
					elif "-" in item and not "-d" in item and not exists(f"{img_ex}/{item}"):
						down = True
				if down:
					data.append({"text": se["check"][set]["e"], "size": size, "size_hint": (1, None), "text_size": text,
					             "id": set, "disabled": False})

			for var in sorted(data, key=lambda x: x["text"]):
				self.decks["rv"].data.append(var)

		# self.decks["rv"].data.append(
		# 		{"text": "", "size": (self.sd["card"][0] * 5.8, self.sd['card'][1] / 3), "size_hint": (1, None),
		# 		 "disabled": True, "id": "space"})
		# if len(self.decks["rv"].data) > 1:
		# 	self.decks["rv"].data.append(
		# 			{"text": "Download All", "size": size, "size_hint": (1, None), "text_size": text, "id": "all",
		# 			 "disabled": False})
		#
		# self.decks["rv"].data.append(
		# 		{"text": "Close", "size": size, "size_hint": (1, None), "text_size": text, "id": "close",
		# 		 "disabled": False})
		else:
			if "Neo" in self.decks["dbuild"]["n"]:
				key = "Title"
			else:
				key = self.decks["dbuild"]["n"]

			self.decks["sets"].title = f"Choose a {key}"

			for name in sorted(se["main"]["s"][key]):
				self.decks["rv"].data.append(
						{"text": name, "size": size, "size_hint": (1, None), "disabled": False,
						 "text_size": text, "id": name}, )

		yscv = (self.sd["card"][1] / 1.25 + self.sd["padding"]) * len(self.decks["rv"].data)
		ybtn = self.sd["padding"] * 2.5 + self.sd["card"][1] / 2.
		ypop = yscv + ybtn + self.decks["sets"].title_size + self.decks["sets"].separator_height + self.sd["card"][
			1] * 0.75
		# ypop = self.decks["sets"].title_size + self.decks["sets"].separator_height
		# ypop += (self.sd["card"][1] / 2 + self.sd["padding"]) * len(self.decks["rv"].data) + self.sd["card"][1] * 0.75

		if ypop > Window.height:
			self.decks["rv"].do_scroll_y = True
			ypop = Window.height * 0.9
			yscv = ypop - self.sd["card"][1] * 0.75 - self.decks["sets"].title_size - self.decks[
				"sets"].separator_height - (self.sd["card"][1] / 1.25 + self.sd["padding"] * 0)

		self.decks["sets"].content = self.decks["rv_rel"]
		if "down" in t:
			self.decks["sets"].size = (self.sd["card"][0] * 6 + self.sd["padding"] * 2, ypop)
			self.decks["rv_all"].center_x = self.decks["sets"].size[0] / 4. - self.sd["padding"]
			self.decks["rv_all"].y = self.sd["padding"] * 1
			self.decks["rv_close"].center_x = self.decks["sets"].size[0] / 4. * 3 - self.sd["padding"] * 3
			self.decks["rv_close"].y = self.sd["padding"] * 1
			self.decks["rv"].y = ybtn
			self.decks["rv_rel"].size = (self.decks["sets"].size[0], yscv)
		else:
			self.decks["sets"].size = (self.sd["card"][0] * 6 + self.sd["padding"] * 2, ypop - ybtn)
			self.decks["rv_all"].y = -Window.height * 2
			self.decks["rv_close"].y = -Window.height * 2
			self.decks["rv_rel"].size = (self.decks["sets"].size[0], yscv)
			self.decks["rv"].y = self.sd["padding"] * 1

		self.decks["sets"].open()

	def popup_deck(self, t="start", dt=.0, *args):
		self.decks["c"] = t
		self.decks["selected"] = ""
		deck_size = (self.sd["card"][0] * 1.5, self.sd["card"][1] * 1.5)
		mat_size = (self.sd["card"][1] * 1.9, self.sd["card"][0] * 1.9)
		if t == "start":
			self.dpop["idadd"] = ImgButton(source=f"atlas://{img_in}/other/add", size=deck_size, cid="a",
			                               card=self.sd["card"])
			self.dpop["idadd"].btn.bind(on_press=self.popup_deck_slc)

			self.add_deckpop_btn()

			for mat in sorted(se["main"]["m"]):
				if not sp[mat]["c"]:
					continue
				img = sp[mat]["img"]
				if "." in img:
					img = img[:-4]
				if img in ("mat_mat", "demo"):
					source = "other"
				else:
					source = "main"
				self.decks["sspacem"] = StackSpacer(o=mat_size)

				if "main" in source:
					self.dpop[f"im{mat}"] = ImgButton(source=f"atlas://{img_ex}/main/{img}", size=mat_size,
					                                  cid=f"m{mat}",
					                                  card=self.sd["card"])
				else:
					self.dpop[f"im{mat}"] = ImgButton(source=f"atlas://{img_in}/{source}/{img}", size=mat_size,
					                                  cid=f"m{mat}",
					                                  card=self.sd["card"])
				self.dpop[f"im{mat}"].btn.bind(on_release=self.popup_deck_slc, on_press=self.popup_deck_info)
		elif t.startswith("x") or t.startswith("d"):
			self.decks["stack"].clear_widgets()
			self.sd["dpop_press"] = []
			if t == "ddd":
				self.decks["build_pop"] = True
			if "d" in t:
				if "dd" in t:
					self.decks["popup"].title = "Deck Building"
					decks = [s for s in sorted(sd.keys()) if s.startswith("CEJ")]
					decks.append("add")
					self.add_deckpop_btn()
					for key in ("create", "dismantle"):
						try:
							self.decks["sctm"].add_widget(self.decks[key])
						except WidgetException:
							pass
				else:
					self.decks["popup"].title = "Decks"
					decks = [s for s in sorted(sd.keys()) if sd[s]["c"]]
				self.decks["max_col"] = 4

				nx, ns = self.get_index_stack(decks, self.decks["max_col"])
				if nx:
					decks.insert(nx, "sspaced")
					self.decks["sspaced"].size = (self.decks["sspaced"].size_o[0] * ns, self.decks["sspaced"].size[1])

				width = deck_size[0] + self.sd["padding"]
				height = deck_size[1] + self.sd["padding"]
				for ind in decks:
					if "sspace" in ind:
						self.decks["stack"].add_widget(self.decks[ind])
					else:
						self.dpop[f"id{ind}"].selected(False)
						self.decks["stack"].add_widget(self.dpop[f"id{ind}"])
			elif "m" in t:
				self.decks["popup"].title = "Playmats"
				decks = [s for s in sorted(sp.keys()) if sp[s]["c"]]
				if len(decks) < 3:
					self.decks["max_col"] = 2
				else:
					self.decks["max_col"] = 3
				if "mat" in decks:
					temp = decks.pop(decks.index("mat"))
					decks.insert(0, "mat")

				nx, ns = self.get_index_stack(decks, self.decks["max_col"])
				if nx:
					decks.insert(nx, "sspacem")
					self.decks["sspacem"].size = (self.decks["sspacem"].size_o[0] * ns, self.decks["sspacem"].size[1])
				width = mat_size[0] + self.sd["padding"]
				height = mat_size[1] + self.sd["padding"]
				for ind in decks:
					if "sspace" in ind:
						self.decks["stack"].add_widget(self.decks[ind])
					else:
						self.dpop[f"im{ind}"].selected(False)
						self.decks["stack"].add_widget(self.dpop[f"im{ind}"])

			self.decks["scv"].do_scroll_y = False

			r = int(ceil(len(decks) / float(self.decks["max_col"]))) - 1

			if r > 3:
				yscv = height * (r - 0.5)
				self.decks["scv"].do_scroll_y = True
			elif r > 0:
				yscv = height * (r + 1)
			else:
				yscv = height + self.sd["padding"] / 2

			if "dd" in t:
				yscatm = yscv + self.sd["card"][1] * 2.5
			else:
				yscatm = yscv + self.sd["card"][1] * 1.6

			ypop = yscatm + self.decks["popup"].title_size + self.decks["popup"].separator_height

			if ypop > Window.height:
				ypop = Window.height * 0.9
				yscatm = ypop - self.decks["popup"].title_size - self.decks["popup"].separator_height
				yscv = yscatm - self.sd["card"][1] * 1.9 * 0.75

			self.decks["scv"].size = (width * self.decks["max_col"] + self.sd["padding"] * 4, yscv)
			self.decks["popup"].size = (width * self.decks["max_col"] + self.sd["padding"] * 4, ypop)

			self.decks["close"].y = self.sd["padding"] * 1.5

			if "dd" in t:
				self.decks["close"].center_x = self.decks["popup"].size[0] / 2 * 1 - self.sd["padding"]
				self.decks["confirm"].y = -Window.height
				self.decks["dismantle"].disabled = True
				self.decks["dismantle"].center_x = self.decks["popup"].size[0] / 4. * 1 - self.sd["padding"]
				self.decks["dismantle"].y = self.decks["close"].y * 2.5 + self.decks["close"].size[1]
				self.decks["create"].text = "Create new"
				self.decks["create"].center_x = self.decks["popup"].size[0] / 4. * 3 - self.sd["padding"]
				self.decks["create"].y = self.decks["close"].y * 2.5 + self.decks["close"].size[1]
				self.decks["scv"].y = (self.decks["close"].y * 2 + self.decks["close"].size[1]) * 2
			else:
				self.decks["create"].y = -Window.height * 2
				self.decks["dismantle"].y = -Window.height * 2
				self.decks["close"].center_x = self.decks["popup"].size[0] / 4. * 1 - self.sd["padding"]
				self.decks["confirm"].center_x = self.decks["popup"].size[0] / 4. * 3 - self.sd["padding"]
				self.decks["confirm"].y = self.sd["padding"] * 1.5
				self.decks["confirm"].disabled = True
				self.decks["scv"].y = self.decks["close"].size[1] + self.decks["close"].y * 2

			self.decks["scv"].scroll_y = 1
			self.sd["text"]["popup"].dismiss()
			self.decks["popup"].open()
		elif "setting" in t:
			self.decks["scv"].y = -Window.height * 2
			self.decks["popup"].title = "Deck Settings"

			for key in ("create", "dismantle"):
				self.decks["sctm"].remove_widget(self.decks[key])

			xscat = self.sd["card"][0] * 6
			ypop = self.decks["popup"].title_size + self.decks["popup"].separator_height

			self.decks["close"].y = self.sd["padding"] * 1.5
			self.decks["close"].center_x = xscat / 2 - self.sd["padding"] * 0.75

			ypos = self.sd["padding"] * 4.5 + self.sd["card"][1] / 2

			for item in ("image", "format", "lang", "name"):
				if item == "image" and "img" in t:
					self.decks["st"][f"{item}_box"].pos = (0, ypos)
					self.decks["st"][f"{item}_box"].size = (xscat, self.sd["card"][1] * 1.5)
					self.decks["st"][item].size = (xscat, self.sd["card"][1] / 2)
					# self.decks["st"][item].size = (xscat, self.sd["card"][1]/2)
					self.decks["st"][f"{item}_btn"].size = (xscat - self.sd["card"][0] / 2, self.sd["card"][1])
					# self.decks["st"][f"{item}_btn"].center_x = self.decks["st"][f"{item}_box"].center_x -self.sd["card"][0]/2
					self.decks["save"].y = self.sd["padding"] * 1.5
					self.decks["save"].center_x = xscat / 4 * 3 - self.sd["card"][0] / 2
					self.decks["close"].center_x = xscat / 4 - self.sd["padding"] / 2
					ypos += self.sd["card"][1] * 1.5 + self.sd["padding"] * 1
				elif item == "image" and "img" not in t:
					self.decks["st"][f"{item}_box"].y = -Window.height * 2
					self.decks["save"].y = -Window.height * 2
				else:
					self.decks["st"][f"{item}_box"].pos = (0, ypos)
					if item == "lang":
						self.decks["st"][f"{item}_box"].size = (xscat, self.sd["card"][1] / 2)
						# self.decks["st"][item].size =(xscat/2, self.sd["card"][1] / 2)
						ypos += self.sd["card"][1] / 2 + self.sd["padding"] * 3
					else:
						self.decks["st"][f"{item}_box"].size = (xscat, self.sd["card"][1])
						ypos += self.sd["card"][1] + self.sd["padding"] * 3
					if item == "format":
						self.decks["st"][f"{item}_btn"].text_size = (xscat * 0.9, self.sd["card"][1] / 2)
			# self.decks["st"][item].size =(xscat/2, self.sd["card"][1] / 2)

			ypop += ypos + self.sd["padding"] * 5
			if self.decks["dbuild"]["n"]:
				self.decks["close"].disabled = False
			else:
				self.decks["close"].disabled = True
			# self.decks["st"]["format_btn"].text_size = (xscat,self.sd["card"][1]/2)
			self.decks["st"]["image"].text_size = (xscat / 2, self.sd["card"][1])
			self.decks["popup"].size = (xscat, ypop)
			self.decks["popup"].open()
		elif "download" in t:
			self.decks["popup"].title = "Download"

			self.decks["popup"].open()

	def popup_deck_slc(self, btn):
		if self.decks["p_info"] is not None:
			self.decks["p_info"].cancel()
			self.decks["p_info"] = None
		if not btn.cid:
			if self.decks["setting_pop"]:
				self.decks["setting_pop"] = False
				self.deck_building_cards()
			elif self.decks["dbuilding"]:
				self.decks["dbuilding"] = ""
				self.main_scrn.pos = (0, 0)
				self.main_scrn.disabled = False
			elif self.decks["build_pop"]:
				self.decks["build_pop"] = False
				for key in ("create", "dismantle"):
					self.decks["sctm"].remove_widget(self.decks[key])
				self.decks["dismantle"].disabled = True
				self.decks["create"].text = "Create new"
			self.decks["selected"] = ""
			self.sd["dpop_press"] = []
			self.decks["popup"].dismiss()
		elif btn.cid == "a":
			self.decks["selected"] = ""
			self.decks["popup"].dismiss()
			Clock.schedule_once(partial(self.popup_text, "Loading"), ability_dt)
			Clock.schedule_once(self.gotodeckedit, move_dt_btw)
		elif btn.cid == "c":
			self.decks["popup"].dismiss()
			Clock.schedule_once(partial(self.popup_text, "Loading"), ability_dt)
			Clock.schedule_once(self.gotodeckedit, move_dt_btw)
		elif btn.cid == "z" and self.decks["selected"]:
			self.popup_text("Loading")
			del sd[self.decks["selected"][1:]]
			del scej[self.decks["selected"][1:]]
			# Clock.schedule_once(self.update_edata,move_dt_btw)
			self.gd["update_edata"] = False
			self.update_edata()
			Clock.schedule_once(self.update_edata)
			Clock.schedule_once(self.wait_update, move_dt_btw)
		# self.update_deckpop_btn()
		# self.popup_deck("ddd")
		elif btn.cid == "1":
			if "d" in self.decks["c"]:
				self.decks[self.decks["c"][1]][0] = self.decks["selected"][1:]
				self.decks[self.decks["c"][1]][2] = False
				img = sd[self.decks[self.decks["c"][1]][0]]["img"]
				if "." in img:
					img = img[:-4]
				if img in other_img:
					source = "other"
				elif img in annex_img:
					source = "annex"
				else:
					source = "main"

				if source == "main" and self.decks[self.decks["c"][1]][0].startswith("CEJ"):
					if (img in se["main"]["a"][set] for set in se["main"]["a"]):
						pass
					else:
						source = "other"
						img = "grey"

				if "main" in source:
					self.network[f"{self.decks['c'][1]}{self.decks['c'][2]}"].source = f"atlas://{img_ex}/main/{img}"
				else:
					self.network[
						f"{self.decks['c'][1]}{self.decks['c'][2]}"].source = f"atlas://{img_in}/{source}/{img}"
			elif "m" in self.decks["c"]:
				self.decks[self.decks["c"][1]][1] = self.decks["selected"][1:]
				self.decks[self.decks["c"][1]][3] = False
				img = sp[self.decks[self.decks["c"][1]][1]]["img"]
				if "." in img:
					img = img[:-4]
				if img in ("mat_mat", "demo"):
					source = "other"
				else:
					source = "main"

				if "main" in source:
					self.network[f"{self.decks['c'][1]}{self.decks['c'][2]}"].source = f"atlas://{img_ex}/main/{img}"
				else:
					self.network[
						f"{self.decks['c'][1]}{self.decks['c'][2]}"].source = f"atlas://{img_in}/{source}/{img}"
			self.network[f"{self.decks['c'][1]}{self.decks['c'][2]}_ran"].state = "normal"
			self.popup_network_slc(self.network[f"{self.decks['c'][1]}{self.decks['c'][2]}_ran"])
			self.decks["popup"].dismiss()
		elif self.decks["selected"] == btn.cid:
			self.dpop[f"i{btn.cid}"].selected(False)
			self.decks["selected"] = ""
			self.decks["confirm"].disabled = True
			self.decks["dismantle"].disabled = True
			self.decks["create"].text = "Create new"
		elif self.decks["selected"] != btn.cid:
			if self.decks["selected"] != "":
				self.dpop[f"i{self.decks['selected']}"].selected(False)
			self.decks["selected"] = btn.cid
			self.decks["confirm"].disabled = False
			self.dpop[f"i{btn.cid}"].selected()
			self.decks["dismantle"].disabled = False
			self.decks["create"].text = "Edit deck"

	def popup_deck_info(self, btn):
		if btn.cid.startswith("m"):
			pass
		elif btn.cid.startswith("d"):
			self.sd["dpop_press"].append(btn.cid)
			if len(self.sd["dpop_press"]) >= info_popup_press:
				if all(prs == btn.cid for prs in self.sd["dpop_press"][-info_popup_press:]):
					self.sd["dpop_press"] = []
					self.popup_multi_info(deck=btn.cid)
			else:
				self.decks["p_info"] = Clock.schedule_once(partial(self.popup_multi_info, deck=btn.cid), info_popup_dt)

	def popup_multi_info_start(self, *args):
		self.multi_info = {}
		self.multi_info["t"] = False
		self.multi_info["deck"] = AsyncImage(source=f"atlas://{img_in}/other/empty", allow_stretch=True,
		                                     height=self.sd["card"][1] * 3,
		                                     size=(self.sd["card"][0] * 3, self.sd["card"][1] * 3),
		                                     size_hint=(None, None))

		self.multi_info["popup"] = Popup()  # size=(100, 100))
		self.multi_info["popup"].bind(on_open=self.multi_info_open, on_dismiss=self.multi_info_dismiss)
		self.multi_info["close"] = Button(size_hint=(None, None), text="Close", on_release=self.popup_multi_info_slc,
		                                  size=(self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.), cid="close")
		self.multi_info["stack"] = StackLayout(orientation="lr-tb", size_hint_y=None, padding=self.sd["padding"] / 2,
		                                       spacing=self.sd["padding"])
		self.multi_info["stack"].bind(minimum_height=self.multi_info["stack"].setter('height'))
		self.multi_info["sctm"] = RelativeLayout(size_hint=(1, 1))
		self.multi_info["scv"] = ScrollView(do_scroll_x=False, size_hint=(1, None))
		self.multi_info["sctm"].add_widget(self.multi_info["scv"])
		self.multi_info["sctm"].add_widget(self.multi_info["close"])
		self.multi_info["scv"].add_widget(self.multi_info["stack"])
		self.multi_info["popup"].content = self.multi_info["sctm"]
		self.multi_info["sspace"] = StackSpacer(o=self.sd["card"])

		self.multi_info["download"] = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=self.sd["padding"])
		self.multi_info["sctm"].add_widget(self.multi_info["download"])
		for ind in ("Booster Pack", "Extra Booster", "Trial Deck", "Other"):
			rr = Button(text=ind, on_release=self.down_popup_btn, cid=ind[0])
			self.multi_info["download"].add_widget(rr)

		for x in range(1, 3):
			self.cpop[f"{x}"] = CardImg(f"{x}", self.sd["card"], f"{x}", self.mat[f"{x}"]["per"])
			self.cpop[f"{x}"].btn.bind(on_press=self.card_btn_press, on_release=self.card_btn_release)
		for x in range(1, 51):
			self.cpop[f"{x}0"] = CardImg(f"{x}0", self.sd["card"], "1", self.mat["1"]["per"])
			self.cpop[f"{x}0"].btn.bind(on_press=self.card_btn_press, on_release=self.card_btn_release)
			self.cpop[f"{x}1"] = CardImg(f"{x}1", self.sd["card"], "1", self.mat["1"]["per"])
			self.cpop[f"{x}1"].btn.bind(on_press=self.card_btn_press, on_release=self.card_btn_release)
			self.cpop[f"{x}2"] = CardImg(f"{x}2", self.sd["card"], "2", self.mat["1"]["per"])
			self.cpop[f"{x}2"].btn.bind(on_press=self.card_btn_press, on_release=self.card_btn_release)

	# self.multi_info["stack"].add_widget(self.cpop[f"{x}0"])

	def multi_info_open(self, *args):
		self.multi_info["t"] = True

	def multi_info_dismiss(self, *args):
		self.multi_info["t"] = False
		self.multi_info["stack"].clear_widgets()

	def popup_multi_info_slc(self, btn, *args):
		if btn.cid == "close":
			self.multi_info["popup"].dismiss()
			self.multi_info["t"] = False

			if "marker" in self.gd["ability_doing"]:
				self.marker()
			elif self.gd["popup_done"][1]:
				if "search" in self.gd["ability_doing"]:  # self.multi_info["t"]:
					if "Reveal" in self.gd["effect"]:
						Clock.schedule_once(self.ability_effect)
					else:
						self.gd["shuffle_trigger"] = "ability"
						self.shuffle(self.multi_info["owner"])
				elif "salvage" in self.gd["ability_doing"]:
					if "Library" in self.gd["effect"] and "top" not in self.gd["effect"] and "bottom" not in self.gd[
						"effect"]:
						self.gd["shuffle_trigger"] = "ability"
						self.shuffle(self.multi_info["owner"])
					else:
						Clock.schedule_once(self.ability_effect)
				elif self.gd["random_reveal"]:
					self.gd["random_reveal"] = []
					Clock.schedule_once(self.ability_effect)
				elif self.gd["ability_doing"] in ("looktop", "look"):
					if self.gd["ability_doing"] in self.gd["ability_effect"]:
						self.gd["ability_effect"].remove("ability_doing")
					if len(self.gd["show"]) > 0:
						self.gd["show"] = []
					Clock.schedule_once(self.ability_effect)
		else:
			if self.gd["turn"] <= 0:
				self.cardinfo.import_data(self.multi_info[f"c_{btn.cid}"], annex_img)
			else:
				self.cardinfo.import_data(self.multi_info[f"c_{btn.cid}"], annex_img)

	def popup_multi_info(self, field="", owner="", deck="", cards="", t="", *args):
		self.multi_info["download"].y = -Window.height * 2
		if deck != "":
			self.multi_info["popup"].title = sd[deck[1:]]["name"]
			self.multi_info["owner"] = "deck"
			self.multi_info["cards"] = []
			self.multi_info["deck_list"] = ["", ]
			c = 1
			for mcards in sorted(sd[deck[1:]]["deck"].keys()):
				for card in range(sd[deck[1:]]["deck"][mcards]):
					self.multi_info["cards"].append(f"{c}0")
					self.cpop[f"{c}0"].import_data(sc[mcards])
					self.multi_info["deck_list"].append(mcards)
					c += 1
		else:
			if owner == "2":
				own = "Opponent"
			elif owner == "1":
				own = "Player"
			if field:
				self.multi_info["cards"] = list(self.pd[owner][field])
				t = field
			elif cards:
				self.multi_info["cards"] = cards
			if t == "OChoose":
				self.multi_info["popup"].title = "Opponent choices"
			elif t == "Random":
				self.multi_info["popup"].title = f"{own} Random choices"
			else:
				if "Waiting" in t:
					t += " room"
				self.multi_info["popup"].title = f"{own} {t.lower()}"
			self.multi_info["owner"] = owner

		self.multi_info["stack"].clear_widgets()
		self.multi_info["scv"].do_scroll_y = False
		width = self.sd["card"][0] + self.sd["padding"]
		height = self.sd["card"][1] + self.sd["padding"]

		r = 0
		if starting_hand < len(self.multi_info["cards"]) < 7:
			ncards = len(self.multi_info["cards"])
		elif len(self.multi_info["cards"]) > starting_hand:
			ncards = int(popup_max_cards)
			r = int(ceil(len(self.multi_info["cards"]) / float(ncards))) - 1
		else:
			ncards = int(starting_hand)

		if deck != "":
			img = sd[deck[1:]]['img']
			if "." in img:
				img = img[:-4]

			if not deck[1:].startswith("CJ") and not deck[1:].startswith("CE") and sd[deck[1:]]["img"] not in other_img:
				if img in annex_img:
					self.multi_info["deck"].source = f"atlas://{img_in}/annex/{img}"
				else:
					self.multi_info["deck"].source = f"atlas://{img_ex}/main/{img}"
				self.multi_info["deck"].size = (width * ncards, self.sd["card"][1] * 3)
				self.multi_info["deck"].height = self.sd["card"][1] * 3
				self.multi_info["stack"].add_widget(self.multi_info["deck"])

		nx, ns = self.get_index_stack(self.multi_info["cards"], ncards)
		if nx:
			self.multi_info["cards"].insert(nx, "sspace")
			if ns > 1:
				if ns % 1 > 0:
					nss = int(ns)
				else:
					nss = int(ns) - 1
			else:
				nss = 0
			self.multi_info["sspace"].size = (self.sd["card"][0] * ns + self.sd["padding"] * nss, self.sd["card"][1])

		for ind in self.multi_info["cards"]:
			if "sspace" in ind:
				try:
					self.multi_info["stack"].add_widget(self.multi_info[ind])
				except WidgetException:
					pass
			else:
				self.cpop[ind].selected(False)
				self.cpop[ind].update_text()
				self.multi_info["stack"].add_widget(self.cpop[ind])

		if r > 4:
			yscv = height * (r - 0.5)
			self.multi_info["scv"].do_scroll_y = True
		elif r > 0:
			yscv = height * (r + 1)
		else:
			yscv = height + self.sd["padding"] / 2

		yscatm = yscv + self.sd["card"][1] * 1.6
		ypop = yscatm + self.multi_info["popup"].title_size + self.multi_info["popup"].separator_height

		if ypop > Window.height:
			ypop = Window.height * 0.9
			yscatm = ypop - self.multi_info["popup"].title_size - self.multi_info["popup"].separator_height
			yscv = yscatm - self.sd["card"][1] * 0.75

		self.multi_info["scv"].size = (width * ncards + self.sd["padding"] * 4, yscv)
		self.multi_info["popup"].size = (width * ncards + self.sd["padding"] * 4, ypop)

		self.multi_info["close"].center_x = self.multi_info["popup"].size[0] / 2. - self.sd["card"][0] / 2 + self.sd[
			"padding"]
		self.multi_info["close"].y = self.sd["padding"] * 1.5
		self.multi_info["scv"].y = self.multi_info["close"].y * 2 + self.multi_info["close"].size[1]
		self.multi_info["scv"].scroll_y = 1
		self.multi_info["t"] = True
		self.multi_info["popup"].open()

	def popup_network_start(self, *args):
		self.network["m_connect"] = Button(text="Connect", on_release=self.mconnect, cid="connect",
		                                   size_hint=(None, None),
		                                   size=(self.sd["card"][0] * 4, self.sd["card"][1] * 2))
		self.network["sctm"] = RelativeLayout(size_hint=(1, 1), pos=(0, 0))

		self.network["m_close"] = Button(size_hint=(None, None), text="Back", on_release=self.popup_network_slc,
		                                 cid="back", size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.))
		self.network["m_confirm"] = Button(size_hint=(None, None), on_release=self.popup_network_slc, cid="confirm",
		                                   text="Start", size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.))

		self.network["1d"] = ImgButton(source=f"atlas://{img_in}/other/demo", card=self.sd["card"], cid="x1d",
		                               size=(self.sd["card"][1] * 1.5, self.sd["card"][1] * 1.5))
		self.network["1m"] = ImgButton(source=f"atlas://{img_in}/other/mat_mat", cid="x1m", card=self.sd["card"],
		                               size=(self.sd["card"][1] * 1.5, self.sd["card"][1] * 1.5))
		self.network["2d"] = ImgButton(source=f"atlas://{img_in}/other/demo", card=self.sd["card"], cid="x2d",
		                               size=(self.sd["card"][1] * 1.5, self.sd["card"][1] * 1.5))
		self.network["2m"] = ImgButton(source=f"atlas://{img_in}/other/mat_mat", card=self.sd["card"], cid="x2m",
		                               size=(self.sd["card"][1] * 1.5, self.sd["card"][1] * 1.5))

		self.network["1d"].btn.bind(on_press=self.popup_network_slc)
		self.network["1m"].btn.bind(on_press=self.popup_network_slc)
		self.network["2d"].btn.bind(on_press=self.popup_network_slc)
		self.network["2m"].btn.bind(on_press=self.popup_network_slc)
		self.network["1d_ran"] = ToggleButton(text="Random", on_release=self.popup_network_slc, size_hint=(None, None),
		                                      cid="r1d", size=(self.sd["card"][1] * 1.5, self.sd["card"][1] / 3))
		self.network["1m_ran"] = ToggleButton(text="Random", on_release=self.popup_network_slc, size_hint=(None, None),
		                                      cid="r1m", size=(self.sd["card"][1] * 1.5, self.sd["card"][1] / 3))
		self.network["2d_ran"] = ToggleButton(text="Random", on_release=self.popup_network_slc, size_hint=(None, None),
		                                      cid="r2d", size=(self.sd["card"][1] * 1.5, self.sd["card"][1] / 3))
		self.network["2m_ran"] = ToggleButton(text="Random", on_release=self.popup_network_slc, size_hint=(None, None),
		                                      cid="r2m", size=(self.sd["card"][1] * 1.5, self.sd["card"][1] / 3))
		self.network["1text"] = Label(text="P1", size_hint=(None, None))
		self.network["2text"] = Label(text="P2", size_hint=(None, None))
		for x in range(1, 3):
			self.network[f"{x}text"].color = (1, 1, 1, 1)
			self.network[f"{x}text"].outline_width = 2
			self.network[f"{x}text"].halign = "center"
			self.network[f"{x}text"].valing = "middle"
			self.network[f"{x}text"].size = (self.sd["card"][1], self.sd["card"][1] * 2)

		self.network["popup"] = Popup(size=(self.sd["card"][1] * 5, self.sd["card"][1] * 7.25))

		for item in self.network:
			if item.startswith("1") or item.startswith("2") or item.startswith("m_"):
				self.network["sctm"].add_widget(self.network[item])

		# self.boxv2 = BoxLayout(orientation='vertical')
		# self.boxh1 = BoxLayout(orientation='horizontal')
		#
		# self.boxv2.add_widget(self.network["text_input"])
		# self.boxh1.add_widget(self.network["b_create"])
		# self.boxh1.add_widget(self.network["b_join"])
		# self.boxv2.add_widget(self.boxh1)

		self.network["popup"].content = self.network["sctm"]
		self.multiplay_popup_create()

	def popup_network(self, t="", *args):
		self.network["popup"].open()

	def popup_network_slc(self, btn, *args):
		if btn.cid == "":
			pass
		elif btn.cid.startswith("r"):
			if btn.state == "normal":
				if "d" in btn.cid:
					img = sd[self.decks[btn.cid[1]][0]]["img"]
					if "." in img:
						img = img[:-4]
					if img in other_img:
						source = "other"
					elif img in annex_img:
						source = "annex"
					else:
						source = "main"

					if "main" in source:
						self.network[f"{btn.cid[1]}{btn.cid[2]}"].source = f"atlas://{img_ex}/main/{img}"
					else:
						self.network[f"{btn.cid[1]}{btn.cid[2]}"].source = f"atlas://{img_in}/{source}/{img}"
					self.decks[f"{btn.cid[1]}"][2] = False
				elif "m" in btn.cid:
					img = sp[self.decks[btn.cid[1]][1]]["img"]
					if "." in img:
						img = img[:-4]
					if img in ("mat_mat", "demo"):
						source = "other"
					else:
						source = "main"

					if "main" in source:
						self.network[f"{btn.cid[1]}{btn.cid[2]}"].source = f"atlas://{img_ex}/main/{img}"
					else:
						self.network[f"{btn.cid[1]}{btn.cid[2]}"].source = f"atlas://{img_in}/{source}/{img}"
					self.decks[btn.cid[1]][3] = False
			elif btn.state == "down":
				self.network[f"{btn.cid[1]}{btn.cid[2]}"].source = f"atlas://{img_in}/other/random"
				if "d" in btn.cid:
					self.decks[btn.cid[1]][2] = True
				elif "m" in btn.cid:
					self.decks[btn.cid[1]][3] = True
		elif btn.cid == "back":
			self.network["popup"].dismiss()
		elif btn.cid == "confirm":
			self.main_scrn.disabled = True
			self.network["popup"].dismiss()
			Clock.schedule_once(self.start_game, move_dt)
		elif btn.cid.startswith("x") or btn.cid.startswith("d"):
			self.popup_deck(t=btn.cid)
		elif btn.cid == "single" or btn.cid == "multi":
			if self.gd["gg"]:
				self.gd["gg"] = False
				self.restart()
			if btn.cid == "single":
				self.network["popup"].title = f"Game Settings - {btn.cid[:1].upper()}{btn.cid[1:]}-player"
			else:
				self.network["popup"].title = f"Game Settings - {btn.cid[:1].upper()}{btn.cid[1:]}player"

			for item in self.network:
				if item.startswith("m_"):
					self.network[item].y = self.sd["padding"] * 1.5
					if "close" in item:
						if btn.cid == "multi":
							self.network[item].center_x = self.network["popup"].size[0] / 2. - self.sd["padding"]
						else:
							self.network[item].center_x = self.network["popup"].size[0] / 4. - self.sd["padding"]
					elif "confirm" in item:
						if btn.cid == "multi":
							self.network[item].center_x = -Window.width * 2
						else:
							self.network[item].center_x = self.network["popup"].size[0] / 4. * 3 - self.sd["padding"]
					elif "connect" in item:
						if btn.cid == "multi":
							self.network[item].center_x = self.network["popup"].size[0] / 2. - self.sd["padding"]
							self.network[item].y = self.sd["card"][1] * 1.25
						else:
							self.network[item].center_x = -Window.width * 2
				elif item.startswith("1") or item.startswith("2"):
					if item.startswith("1"):
						self.network[item].y = self.sd["card"][1] * 3.75
					elif item.startswith("2") and btn.cid == "single":
						self.network[item].y = self.sd["card"][1] * 1.25
					else:
						self.network[item].y = -Window.height

					if "text" in item:
						self.network[item].x = self.sd["padding"] * 1.5
						self.network[item].y += self.sd["padding"] * 1.5
					elif "d" in item:
						self.network[item].x = (self.sd["padding"] * 1.5) * 1 + self.sd["card"][1] * 1
						if "d" in item and "ran" not in item:
							self.network[item].y += self.sd["card"][1] * 0.5
					elif "m" in item:
						self.network[item].x = (self.sd["padding"] * 1.5) * 2 + self.sd["card"][1] * 2.5
						if "m" in item and "ran" not in item:
							self.network[item].y += self.sd["card"][1] * 0.5

			self.sd["menu"]["popup"].dismiss()
			self.network["popup"].open()

	def play(self, lst):
		self.play_to_stage(lst[0], f"{lst[1]}{lst[2]}")

		if self.gd["active"] == "1":
			if self.net["game"]:
				self.net["send"] = False

		self.hand_size(self.gd["active"])
		self.gd["play_card"] = lst[0]
		Clock.schedule_once(self.play_card, ability_dt)

	def multiplay_popup_create(self, *args):
		self.mcreate_popup = Popup()
		self.mcreate_popup.bind(on_open=self.update_time)

		xscat = self.sd["padding"] * 2 + (self.sd["card"][0] + self.sd["padding"]) * starting_hand
		yscat = (self.sd["card"][1] + self.sd["padding"]) + self.sd["card"][1] + self.sd[
			"padding"] * 5 + self.mcreate_popup.title_size + self.mcreate_popup.separator_height

		self.mcreate_popup.size = (xscat + self.sd["padding"] * 2, yscat + self.sd["padding"] * 1)
		self.mcreate_sct = RelativeLayout()
		self.mcreate_popup.content = self.mcreate_sct

		self.mcancel_create_btn = Button(text="Cancel", on_release=self.mcancel_room, size_hint=(None, None))
		self.mcancel_create_time = Label(text="0s", halign="center", text_size=(xscat, None), size_hint=(1, None))
		self.mcancel_create_text = Label(text=".", halign="center", text_size=(xscat, None), size_hint=(1, None))
		self.mcancel_create_bar = ProgressBar(size_hint=(1, None), size=(xscat, self.sd["card"][1] / 3.))
		self.mcancel_create_bar1 = ProgressBar(size_hint=(1, None), size=(xscat, self.sd["card"][1] / 3.))
		self.mcreate_sct.add_widget(self.mcancel_create_btn)
		self.mcreate_sct.add_widget(self.mcancel_create_text)
		self.mcreate_sct.add_widget(self.mcancel_create_time)
		self.mcreate_sct.add_widget(self.mcancel_create_bar)

		self.mcancel_create_bar.y = self.sd["padding"] * 3.5 + self.sd["card"][1] / 2
		self.mcancel_create_bar.x = - Window.width * 2

		self.mcancel_create_btn.size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
		self.mcancel_create_btn.center_x = xscat / 2 - self.sd["padding"] * 0.75
		self.mcancel_create_btn.y = self.sd["padding"] * 1.5

		self.mcancel_create_time.texture_update()
		self.mcancel_create_time.pos = (0, self.sd["padding"] * 3.5 + self.sd["card"][1] / 2.)

		self.mcancel_create_text.texture_update()
		self.mcancel_create_text.pos = (0, self.mcancel_create_time.y + self.sd["padding"] + \
		                                self.mcancel_create_time.texture.size[1])

	def failure_message(self, request, result):
		# print("failure on multiplay", result)
		# print(self.net["url"])
		logging.exception(f'Got exception on main handler\nFailure\n{[request]}\n{request.url}\n{[result]}')
		Clock.schedule_once(partial(self.popup_text, "no_internet"))

	def error_message(self, request, result):
		# print("error on multiplay", result)
		logging.exception(f'Got exception on main handler\nError\n{[request]}\n{request.url}\n{[result]}')
		Clock.schedule_once(partial(self.popup_text, "no_internet"))

	def progress_message(self, request, current_size, total_size):
		item = request.url.split("/")[-1]
		self.downloads[item][1] = current_size
		# self.downloads[item][2] = total_size
		# total = 0
		current = 0
		for key in self.downloads.keys():
			current += self.downloads[key][1]
		# total +=self.downloads[key][2]
		# print(total)

		self.mcancel_create_bar.value = current
		# self.mcancel_create_bar.max = total
		# print(self.mcancel_create_bar.value, self.mcancel_create_bar.max)
		# self.mcancel_create_text.text = f"{round(total,1)}%"
		self.mcancel_create_text.text = f"{round(self.mcancel_create_bar.value_normalized * 100, 1)}%"

	# logging.exception(f'Got exception on main handler\nProgress\n{[request]}\n{[current_size]}\n{[total_size]}')
	# print("progress on multiplay", current_size, total_size)

	def multiplay_cjpopup(self, *args):
		if self.net["status"] == "join":
			self.mcreate_popup.title = "Joining Room"
			self.mcancel_create_text.text = "Looking for open room"
			self.mcancel_create_btn.text = "Cancel Join"
			self.mcancel_create_btn.cid = self.net["status"]
		elif self.net["status"] == "create":
			self.mcreate_popup.title = "Room Created"
			self.mcancel_create_text.text = "Waiting Opponent to join room"
			self.mcancel_create_btn.text = "Cancel Room"
			self.mcancel_create_time.x = 0
			self.mcancel_create_bar.x = -Window.width * 2
			self.mcancel_create_btn.cid = self.net["status"]
		elif self.net["status"] == "roomdis":
			self.mcreate_popup.title = "Room Created"
			self.mcancel_create_text.text = "There was an error joining the room.\nPlease try again later."
			self.mcancel_create_btn.text = "Close"
			self.mcancel_create_btn.cid = self.net["status"]
		elif self.net["status"] == "down":
			self.gd["cancel_down"] = False
			self.mcreate_popup.title = "Download progress"
			self.mcancel_create_text.text = "0.0 %"
			self.mcancel_create_bar.value = 0
			self.mcancel_create_time.x = -Window.width * 2
			self.mcancel_create_bar.x = 0
			self.mcancel_create_btn.text = "Cancel"
			self.mcancel_create_btn.cid = self.net["status"]

	def update_time(self, *args):
		if self.net["time"] >= 0:
			self.net["time"] += 1
			m, s = divmod(self.net["time"], 60)
			h, m = divmod(m, 60)

			if h > 0:
				self.mcancel_create_time.text = f"{h}h {m}m {s}s"
			elif m > 0:
				self.mcancel_create_time.text = f"{m}m {s}s"
			else:
				self.mcancel_create_time.text = f"{s}s"
			# self.mcancel_create_time.texture_update()
			# self.mcancel_create_time.y = self.sd["card"][1] / 2. + self.sd["padding"] * 3.5
			Clock.schedule_once(self.update_time, 1)
		else:
			self.mcancel_create_time.text = " "

	# self.mcancel_create_time.texture_update()
	# self.mcancel_create_time.y = self.sd["card"][1] / 2. + self.sd["padding"] * 3.5

	# def check_internet(self):
	# 	try:
	# 		req = urllib.request.urlopen(self.net["test"])
	# 		# req = UrlRequest(self.net["url"], req_body=data, req_headers=headers, on_success=self.mcheck_data, debug=True
	# 		# on_failure = self.failure_message,
	# 		#              on_error = self.error_message, on_progress = self.progress_message
	# 		# )
	# 		# req.wait()
	# 		return True
	# 	except URLError:
	# 		Clock.schedule_once(partial(self.popup_text, "no_internet"))
	# 		return False

	def mconnect(self, btn, dt=0):
		# if self.check_internet():
		try:
			var = btn.cid
		except AttributeError:
			var = btn
		self.net["wait"] = True
		dat = {}
		headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
		if "connect" in var:
			# if not check_permission('Permission.INTERNET'):
			# 	Clock.schedule_once(partial(self.popup_text, "no_internet"))
			# 	return False #@android

			self.network["m_connect"].disabled = True
			Clock.schedule_once(partial(self.popup_text, "making"))
			if self.decks["1"][2]:
				deck = choice([s for s in sd.keys() if sd[s]["c"]])

				self.decks["1"][0] = deck
				self.decks["1"][2] = False
			else:
				deck = self.decks["1"][0]
			deck1 = self.decks["1"][0]

			if deck.startswith("CEJ"):
				s1 = "'"
				s2 = '"'
				deck1 = f"{deck}~{str(sd[deck]['deck'])[1:-1].replace(s1, '').replace(s2, '').replace(' ', '')}"

			if self.decks["1"][3]:
				mat = choice([s for s in sp.keys() if sp[s]["c"]])
				self.decks["1"][1] = mat
				self.decks["1"][3] = False
			else:
				mat = self.decks["1"][1]

			if sd[deck]['l'] == "":
				dset = f"0b{sd[deck]['n'][:2]}{sd[deck]['t']}"
			else:
				dset = f"0{sd[deck]['l']}{sd[deck]['n'][:2]}{sd[deck]['t']}"

			dat = {"0": "c0", "1": deck1, "2": mat, "3": dset}
		elif "disconn" in var:
			dat = {"0": "dc", "1": self.net["room"]}
		elif "room" in var:
			dat = {"0": f"r{self.net['player']}", "1": self.net["room"], "2": self.net["ready"]}
		elif "winlose" in var:
			self.net["status"] = "winlose"
			dat = {"0": f"w{self.net['player']}", "1": self.net["room"], "2": f"{self.net['var']}"}
		elif "shuffleplr" in var:
			self.net["status"] = "shuffleplr"
			library = self.list_str(self.pd["1"]["Library"])
			dat = {"0": f"s{self.net['player']}", "1": self.net["room"], "2": library, "8": self.net["select"],
			       "9": self.gd["turn"]}
		elif "shuffleopp" in var:
			self.net["status"] = "shuffleopp"
			dat = {"0": f"z{self.net['player']}", "1": self.net["room"], "8": self.net["select"], "9": self.gd["turn"]}
		elif "janken" in var:
			self.net["status"] = "janken"
			dat = {"0": f"j{self.net['player']}", "1": self.net["room"], "2": self.gd["j_hand"],
			       "8": self.net["select"], "9": self.gd["turn"]}
		elif "mulligan" in var:
			self.net["status"] = "mulligan"
			mulligan = self.list_str(self.gd["mulligan"][0])
			dat = {"0": f"m{self.net['player']}", "1": self.net["room"], "2": mulligan, "8": self.net["select"],
			       "9": self.gd["turn"]}
		elif "act" in var:
			self.net["status"] = "act"
			if len(self.net["var"][3]) >= 0:
				self.net["var"][3] = f"{self.list_str(self.net['var'][3], '~')}"
			if len(self.net["var"][4]) >= 0:
				self.net["var"][4] = f"{self.list_str(self.net['var'][4], '~')}"
			temp = f"{self.gd['phase'][:3]}_{self.list_str(self.net['var'])}"  # + "_" + self.gd["ability_doing"]
			dat = {"0": f"p{self.net['player']}", "1": self.net["room"], "2": temp, "8": self.net["select"],
			       "9": self.gd["turn"]}
		elif "phase" in var:
			self.net["status"] = "phase"
			if (self.gd["active"] == "2" and not self.gd["rev"]) or (self.gd["rev"] and self.gd["active"] == "1"):
				self.gd["popup_on"] = True
				dat = {"0": f"o{self.net['player']}", "1": self.net["room"], "8": self.net["select"],
				       "9": self.gd["turn"]}
			elif (self.gd["active"] == "1" and not self.gd["rev"]) or (self.gd["rev"] and self.gd["active"] == "2"):
				temp = f"{self.gd['phase'][:3]}_{self.list_str(self.net['var'])}"  # + "_" + self.gd["ability_doing"]
				dat = {"0": f"p{self.net['player']}", "1": self.net["room"], "2": temp, "8": self.net["select"],
				       "9": self.gd["turn"]}
		elif "oppchoose" in var:
			self.net["status"] = "oppchoose"
			ind = self.gd["ability_trigger"].split("_")[1]
			if ind[-1] == "1":
				self.gd["popup_on"] = True
				dat = {"0": f"o{self.net['player']}", "1": self.net["room"], "8": self.net["select"],
				       "9": self.gd["turn"]}
			elif ind[-1] == "2":
				temp = f"och_{self.list_str(self.net['var'])}"  # + "_" + self.gd["ability_doing"]
				dat = {"0": f"p{self.net['player']}", "1": self.net["room"], "2": temp, "8": self.net["select"],
				       "9": self.gd["turn"]}
		elif "plchoose" in var:
			self.net["status"] = "plchoose"
			ind = self.gd["ability_trigger"].split("_")[1]
			if ind[-1] == "1":
				temp = f"pch_{self.list_str(self.net['var'])}"  # + "_" + self.gd["ability_doing"]
				dat = {"0": f"p{self.net['player']}", "1": self.net["room"], "2": temp, "8": self.net["select"],
			       "9": self.gd["turn"]}
			elif ind[-1] == "2":
				self.gd["popup_on"] = True
				dat = {"0": f"o{self.net['player']}", "1": self.net["room"], "8": self.net["select"],
				       "9": self.gd["turn"]}
		elif "confirm" in var:
			self.net["status"] = "confirm"
			self.gd["popup_on"] = True
			dat = {"0": f"c{self.net['player']}", "1": self.net["room"], "8": self.net["select"],
			       "9": self.gd["turn"]}
		elif "lvl" in var:
			self.net["status"] = "lvl"
			temp = f"lvu_{self.list_str(self.net['var'])}"
			dat = {"0": f"p{self.net['player']}", "1": self.net["room"], "2": temp, "8": self.net["select"],
			       "9": self.gd["turn"]}
		elif "counter" in var:
			self.net["status"] = "counter"
			if self.gd["active"] == "1":
				dat = {"0": f"o{self.net['player']}", "1": self.net["room"], "8": self.net["select"],
				       "9": self.gd["turn"]}
			else:
				temp = f"{self.gd['phase'][:3]}_{self.list_str(self.net['var'])}_{self.gd['ability_doing']}"
				dat = {"0": f"p{self.net['player']}", "1": self.net["room"], "2": temp, "8": self.net["select"],
				       "9": self.gd["turn"]}
		elif "down" in var:
			self.net["status"] = "down"
			if "all" in self.net["var"][0]:
				dat = {"0": "w", "1": f"{self.list_str(self.net['var'])}"}
			else:
				dat = {"0": "w", "1": f"{self.list_str(self.net['var'])}"}
		if "down" in var and self.net["var"][1] > 0:
			self.downloads = {}
			self.mcancel_create_bar1.max = 0
			if "all" in self.net["var"][0]:
				for item in self.temp:
					for item1 in se["check"][item[0]]:
						if item1 == "e" or item1 == "j" or item1 == "d" or any(s in item1[-2:] for s in item[2:]):
							continue
						self.downloads[item1] = [f"{self.net['data']}{item[0]}", 0, 0]
			else:
				for item in se["check"][self.net["var"][0]]:
					if item == "e" or item == "j" or item == "d" or any(s in item[-2:] for s in self.net["var"][2:]):
						continue
					self.downloads[item] = [f"{self.net['data']}{self.net['var'][0]}", 0, 0]

			self.mcancel_create_bar1.max = len(self.downloads) * 10

			for down in list(self.downloads.keys()):
				self.req[down] = UrlRequest(f"{self.downloads[down][0]}/{down}", on_success=self.down_data,
				                            verify=True, on_cancel=self.down_data_cnc,
				                            ca_file=cfi.where(), on_failure=self.failure_message,
				                            on_error=self.error_message, on_progress=self.progress_message)
		else:
			# print("urlencode",urlencode(dat))
			data = urlencode(dat)
			UrlRequest(self.net["url"], req_body=data, req_headers=headers, on_success=self.mcheck_data, timeout=10,
			           ca_file=cfi.where(), on_failure=self.failure_message, on_error=self.error_message, verify=True)

	# , debug=True, on_progress=self.progress_message)
	# 	print("_" * 5)    #@@@
	# 	print(urlencode(dat)) #@@@

	def list_str(self, lst, sep=".",sh=False):
		temp = ""
		for inx in range(len(lst)):
			ind = str(lst[inx])
			if len(lst) == 6 and (inx == 3 or inx == 4) and (lst[0] == "a" or lst[0] == "t"):
				temp += f"{ind}{sep}"
			elif len(ind) >= 2:
				try:
					# if sh:
					if sh:
						temp += f"{ind}{sep}"
					else:
						int(ind)
						temp += f"{ind[:-1]}{sep}"
					# elif "Center" in ind or "Back" in ind:
					# 	temp += f"{ind[0]}{sep}"

				except ValueError:
					if "Center" in ind:
						temp += f"{ind.replace('Center','C')}{sep}"
					elif "Back" in ind:
						temp += f"{ind.replace('Back','B')}{sep}"
					else:
						temp += f"{ind}{sep}"
			else:
				temp += f"{ind}{sep}"
		if temp.endswith(f"{sep}"):
			temp = temp[:-1]
		if not temp:
			temp = "x"
		return temp

	def mcancel_room(self, btn, *args):
		self.mcreate_popup.dismiss()
		self.net["time"] = -1
		self.update_time()
		if self.net["status"] == "create":
			self.net["status"] = "disconn"
			self.mconnect("disconn")
		elif self.net["status"] == "down":
			self.gd["cancel_down"] = True
			for item in self.req:
				if not self.req[item].is_finished:
					self.req[item].cancel()
		# self.popup_text("Loading")

	def mping_data(self):
		if "create" in self.net["status"] or "join" in self.net["status"]:
			self.room = Clock.schedule_once(partial(self.mconnect, "room"), 2)
		elif any(s in self.net["status"] for s in
		         ("shuffle", "janken", "mulligan", "phase", "counter", "oppchoose","plchoose", "winlose")):
			Clock.schedule_once(partial(self.mconnect, self.net["status"]), 2)

	def mcheck_data(self, request, result):
		# var = result.decode('UTF-8')
		var = str(result)
		# print(var) #@@@
		if var.startswith("w"):
			# for btn in self.sd["main_btn"]:
			# 	btn.disabled = False
			self.gd["confirm_trigger"] = "Download"
			self.mcancel_create_bar.max = float(var.split("_")[1]) * 1024
			self.gd["confirm_var"] = {"c": "Download", "ind": var.split("_")[1]}
			Clock.schedule_once(self.confirm_popup)
		elif var.startswith("1c"):
			self.sd["text"]["popup"].dismiss()
			self.net["time"] = 0
			self.net["status"] = "create"
			self.multiplay_cjpopup()
			self.mcreate_popup.open()
			self.net["room"] = int(result[2:])
			self.net["player"] = 1
			self.mping_data()
		elif var.startswith("2j"):
			Clock.schedule_once(partial(self.popup_text, "waitingopp"))
			var = var.split("_")
			self.net["player"] = 2
			self.net["room"] = int(var[0][2:])
			self.net["status"] = "join"
			self.decks["2"] = [var[1], var[2], False, False]
			self.net["ready"] = 1
			self.mping_data()
		elif var.startswith("r"):
			if "r12" in var:
				self.net["status"] = "shuffle"
				self.net["game"] = "online"
				self.gd["com"] = False
				global netroom
				netroom = self.net["room"]
				self.start_game()
			elif "r1_" in var and self.net["player"] == 1 and self.net["ready"] == 0:
				self.mcreate_popup.dismiss()
				Clock.schedule_once(partial(self.popup_text, "waitingopp"))
				self.net["ready"] = 1
				var = var.split("_")
				self.decks["2"] = [var[2], var[3], False, False]
				self.mping_data()
			else:
				self.mping_data()
		elif var.startswith("dc"):
			self.room.cancel()
			self.sd["text"]["popup"].dismiss()
			if self.net["player"] == 2:
				Clock.schedule_once(partial(self.popup_text, "roomdis"), move_dt)
			else:
				self.net = network_init()
				self.network["m_connect"].disabled = False
		elif var.startswith("v"):
			if var.startswith(f"v{self.net['player']}"):
				return
			else:
				self.mping_data()
		elif any(var.startswith(v) for v in ("s", "p")):
			if var.startswith("s") and len(var) > 1:
				self.net["wait"] = False
				if len(self.gd["shuffle"]) <= 0:
					self.sd["text"]["popup"].dismiss()
					self.net["select"] += 1
				self.shuffle_animation()
			elif var.startswith("p") and len(var) > 1:
				self.net["wait"] = False
				self.net["send"] = True
				self.net["select"] += 1
				self.sd["text"]["popup"].dismiss()
				if "lvl" in self.net["var1"]:
					if self.net["varlvl"]:
						self.net["lvlsend"] = True
						self.net["varlvl"] = []
						self.stack_ability()
					else:
						self.level_up_done()
				elif "hand" in self.net["var1"]:
					self.hand_limit_done()
				elif "trigger" in self.net["var1"]:
					self.trigger_done()
				elif "act" in self.net["var1"]:
					Clock.schedule_once(self.play_card_done, ability_dt)
				elif "auto" in self.net["var1"]:
					Clock.schedule_once(self.stack_ability, ability_dt)
				elif "confirm" in self.net["var1"]:
					Clock.schedule_once(self.ability_effect, ability_dt)
				elif "stacked" in self.net["var1"]:
					self.look_top("l")
				elif "searchopp" in self.net["var1"] or "looktopopp" in self.net["var1"]:
					Clock.schedule_once(self.ability_effect, ability_dt)
				elif "plchoose" in self.net["var1"]:
					if "salvage" in  self.net["var1"]:
						self.net["send"] = False
						if self.net["act"][4]:
							self.net["act"][4] = []
						Clock.schedule_once(self.salvage)
					else:
						self.gd["oppchoose"]=True
						Clock.schedule_once(self.ability_effect)
				elif "oppchoose" in self.net["var1"]:
					if "search" in self.gd["ability_doing"]:
						Clock.schedule_once(self.search)
					elif "looktop" in self.gd["ability_doing"]:
						self.look_top("l")
					elif "confirm" in self.gd["ability_doing"]:
						Clock.schedule_once(self.ability_effect)
				elif "end current" in self.net["var1"]:
					self.pd[self.gd["active"]]["done"][self.gd["phase"]] = True
					self.sd["btn"]["end"].disabled = True
					if "Attack" in self.gd["phase"]:
						self.attack_phase_end()
					elif "Climax" in self.gd["phase"]:
						self.gd["phase"] = "Attack"
						Clock.schedule_once(self.attack_phase, move_dt_btw)
				elif "Clock" in self.gd["phase"]:
					self.clock_phase_done()
				elif "Main" in self.gd["phase"]:
					if "move" in self.net["var1"]:
						self.net["send"] = False
					elif "play" in self.net["var1"]:
						if "climax" in self.net["var1"]:
							self.sd["text"]["popup"].dismiss()
							self.gd["phase"] = "Climax"
							self.gd["nomay"] = True
							self.gd["climax_play"] = True
							Clock.schedule_once(self.climax_phase, ability_dt)
						else:
							self.play_card()
				elif "Climax" in self.gd["phase"]:
					if "skip" in self.net["var1"]:
						self.climax_phase()
					elif "no climax" in self.net["var1"]:
						self.climax_phase_done()
					else:
						self.climax_phase_play()
				# elif "Declaration" in self.gd["phase"] or "Encore" in self.gd["phase"]:
				# 	return
				elif "Attack" in self.gd["phase"]:
					if "no attack" in self.net["var1"]:
						self.attack_phase_done()
				elif "Counter" in self.gd["phase"]:
					if not self.gd["counter"]:
						self.counter_step_end()
					else:
						self.counter_done()
				elif "Declaration" in self.gd["phase"]:
					self.attack_declaration_beginning()
				elif "Encore" in self.gd["phase"]:
					self.encore_start()
				elif "Trigger" in self.gd["phase"]:
					self.trigger_effect()
				elif "End" in self.gd["phase"]:
					self.end_phase()
			else:
				self.mping_data()
		elif any(var.startswith(v) for v in ("z", "j", "m", "o")):
			var = var.split("_")
			if f"z{self.net['player']}" in var[0]:
				opp = var[1].split(".")
				if len(opp) == len(self.pd["2"]["Library"]):
					self.pd["2"]["Library"] = []
					for ind in opp:
						self.pd["2"]["Library"].append(f"{ind}2")
					if len(self.gd["shuffle"]) <= 0:
						self.sd["text"]["popup"].dismiss()
						self.net["select"] += 1
					self.shuffle_animation()
				else:
					self.net["status"] = "shuffleopp"
					self.mping_data()
			elif f"j{self.net['player']}" in var[0]:
				self.sd["text"]["popup"].dismiss()
				# print(var)
				self.gd["j_hand_opp"] = var[1]
				self.net["select"] += 1
				self.janken_results()
			elif f"m{self.net['player']}" in var[0]:
				self.sd["text"]["popup"].dismiss()
				self.cardinfo.dismiss()
				self.multi_info["popup"].dismiss()
				if "x" in var[1]:
					self.gd["mulligan"][1] = [""]
				else:
					self.gd["chosen"] = []
					for ind in var[1].split("."):
						# self.gd["chosen"].append(ind)
						self.gd["chosen"].append(f"{ind}2")
				self.pd["2"]["phase"]["Mulligan"] = True
				if self.gd["starting_player"] == "1":
					self.gd["rev"] = True
				self.gd["p_owner"] = "2"
				self.gd["mulligan"][1] = self.gd["chosen"]
				self.net["select"] += 1
				self.mulligan_done()
			elif f"o{self.net['player']}" in var[0]:
				self.gd["popup_on"] = False
				self.sd["text"]["popup"].dismiss()

				self.cardinfo.dismiss()
				self.multi_info["popup"].dismiss()
				self.net["select"] += 1
				self.net["wait"] = False
				cont = []
				if len(var) > 2:
					cont = var[2].split(".")
				# if "confirm" in var:
				# 	if "T" in var:
				# 		self.gd["confirm2"] = [True, True]
				# 	else:
				# 		self.gd["confirm2"] = [True, False]
				# 	self.ability_effect()
				if "lvu" in var[1]:
					# self.gd["chosen"] = [f"{var[2].replace('l', '')}"]
					self.gd["chosen"] = [f"{var[2].replace('l', '')}2"]
					self.level_up_done()
				elif any(var[2].startswith(s) for s in ("a", "t")):
					p = []
					c = []
					if "x" not in cont[3]:
						for ind in cont[3].split("~"):
							# p.append(ind)
							p.append(f"{ind}2")
					if "x" not in cont[4]:
						for ind in cont[4].split("~"):
							try:
								c.append(f"{int(ind)}2")
							except ValueError:
								if "C" in ind:
									c.append(f"{ind.replace('C','Center')}")
								elif "B" in ind:
									c.append(f"{ind.replace('B','Back')}")
								else:
									c.append(f"{ind}")
							# c.append(ind)
					self.net["act"] = [cont[0], f"{cont[1]}2", int(cont[2]), p, c, int(cont[5])]
					# self.net["act"] = [cont[0], cont[1], int(cont[2]), p, c, int(cont[5])]
					# if var[1] in "Trigger":
					# 	self.ability_effect()
					self.gd["confirm2"] = [True, int(cont[5])]
					if "t" in self.net["act"][0]:
						self.act_ability_fill("2")
						self.act_ability(self.net["act"][1], self.net["act"][2])
					elif "a" in self.net["act"][0]:
						self.stack_resolve(self.net["act"][2])
				elif "och" in var[1]:
					self.net["send"] = True
					self.gd["oppchoose"] = True
					if "confirm" in self.gd["ability_doing"]:
						self.gd["confirm2"] =[True, int(var[2])]
						self.ability_effect()
					else:
						if "x" not in var[2]:
							for ind in cont:
								# self.gd["chosen"].append(ind)
								self.gd["chosen"].append(f"{ind}1")
						if "search" in self.gd["ability_doing"]:
							self.gd["p_c"] = "Search"
							self.search()
						elif "looktop" in self.gd["ability_doing"]:
							if "stack" in self.gd["effect"]:
								self.gd["p_c"] = "Look_stack"
							self.look_top("l")
				elif "pch" in var[1]:
					self.net["send"] = True
					self.gd["oppchoose"] = True
					if "x" not in var[2]:
						self.gd["target"] = var[2].split(".")
						for rr in range(len(self.gd["target"])):
							try:
								if self.gd["effect"] and self.gd["ability_trigger"]:
									ind = self.gd["ability_trigger"].split("_")[1]
									if ("opp" in self.gd["effect"] or "Opp" in self.gd["effect"]) and ind[-1]=="1":
										self.gd["target"][rr] = f"{int(self.gd['target'][rr])}2"
									elif ("opp" in self.gd["effect"] or "Opp" in self.gd["effect"]) and ind[-1]=="2":
										self.gd["target"][rr] = f"{int(self.gd['target'][rr])}1"
									else:
										self.gd["target"][rr] = f"{int(self.gd['target'][rr])}{ind[-1]}"
								else:
									self.gd["target"][rr] = f"{int(self.gd['target'][rr])}2"
							except ValueError:
								if "C" in self.gd["target"][rr]:
									self.gd["target"][rr] = self.gd["target"][rr].replace("C","Center")
								elif "B" in self.gd["target"][rr]:
									self.gd["target"][rr] = self.gd["target"][rr].replace("B","Back")

					else:
						self.gd["chosen"] = []
					if "looktop" in self.gd["ability_doing"]:
						# self.gd["target"][1] = int(self.gd["target"][1])
						# self.gd["target"][2] = int(self.gd["target"][2])
						self.gd["target"][1] = int(self.gd["target"][1][:-1])
						self.gd["target"][2] = int(self.gd["target"][2][:-1])
						self.look_top("l")
					elif "salvage" in self.gd["ability_doing"]:
						self.gd["p_c"] = "Salvage"
						self.salvage()
				elif var[1] in "Clock":
					self.gd["p_owner"] = "2"
					self.gd["chosen"] = []
					if "x" not in var[2]:
						for ind in cont:
							self.gd["chosen"].append(f"{ind}2")
							# self.gd["chosen"].append(ind)
					self.clock_phase_done()
				elif var[1] in "Main":
					if "x" not in var[2]:
						if "." not in var[2]:
							# opp = str(var[2])
							opp = f"{var[2]}2"
							if self.cd[opp].card == "Climax":
								self.pd["2"]["Hand"].remove(opp)
								self.cd[opp].setPos(field=self.mat["2"]["field"]["Climax"], t="Climax")
								self.pd["2"]["Climax"].append(opp)
								self.hand_size(opp[-1])
								self.gd["play_card"] = str(opp)
								self.pd["2"]["done"]["Main"] = True
								self.check_cont_ability()
								self.gd["phase"] = "Climax"
								self.gd["nomay"] = True
								self.gd["climax_play"] = True
								Clock.schedule_once(self.climax_phase, ability_dt)
						else:
							if "C" in cont[1]:
								# opp = [cont[0], "Center", int(cont[2])]
								opp = [f"{cont[0]}2", "Center", int(cont[2])]
							elif "B" in cont[1]:
								# opp = [cont[0], "Back", int(cont[2])]
								opp = [f"{cont[0]}2", "Back", int(cont[2])]
							else:
								opp = [f"{cont[0]}2", "Res", cont[2]]
								# opp = [cont[0], "Res", cont[2]]
							if opp[0] in self.pd["2"]["Hand"]:
								self.gd["opp_play"] = [opp]
								self.opp_play()
							elif opp[0] in self.pd["2"]["Center"] + self.pd["2"]["Back"]:
								self.gd["opp_move"] = [opp]
								self.opp_move()
				elif var[1] in "Climax":
					if "k" in var[2]:
						if "ca" in var[2]:
							self.net["select"] += 1
							self.end_to_end()
						elif "c" in var[2]:
							self.end_to_attack()
					elif "x" not in var[2]:
						# self.opp_climax(var[2])
						self.opp_climax(f"{var[2]}2")
					else:
						self.end_current_phase()
				elif var[1] in "Declaration":
					if "x" not in var[2]:
						opp = [f"{cont[0]}2", cont[1], int(cont[2]), int(cont[3]), cont[4]]
						# opp = [cont[0], cont[1], int(cont[2]), int(cont[3]), cont[4]]
						self.gd["opp_attack"].append(opp)
					self.opp_attack()
				elif var[1] in "Attack":
					if "x" in var[2]:
						self.end_current_phase()
				elif var[1] in "Counter":
					if "x" not in var[2]:
						# self.gd["counter_id"] = str(cont[0])
						self.gd["counter_id"] = f"{cont[0]}2"
						self.gd["rev_counter"] = True
						self.counter_done()
					else:
						self.counter_step_done()
				elif var[1] in "Encore":
					if "ke" in var[2]:
						# self.gd["nomay"] = True
						# # self.move_field_btn(self.gd["phase"])
						# for cind in self.gd["encore"]["2"]:
						# 	self.gd["no_cont_check"] = True
						# 	self.cd[cind].selected(False)
						# 	self.send_to_waiting(cind)
						# self.check_cont_ability()
						# self.gd["nomay"] = False
						self.skip_encore()
						self.encore_start()
					else:
						# self.gd["encore_ind"] = str(cont[0])
						self.gd["encore_ind"] = f"{cont[0]}2"
						self.encore_middle()
				# self.gd["encore_type"] = cont[1]
				# if "Stock" not in self.gd["encore_type"]:
				# 	self.gd["chosen"].append(cont[2])
				# elif "Stock" in self.gd["encore_type"]:
				# 	self.pay_stock(int(self.gd["encore_type"][-1]))
				# self.encore_done()
				elif var[1] in "End":
					if "kn" in var[2]:
						self.gd["attack"] = 0
						self.attack_phase_main()
					else:
						if "x" not in var[2]:
							for ind in cont:
								# self.gd["chosen"].append(ind)
								self.gd["chosen"].append(f"{ind}2")
						self.hand_limit_done()
			else:
				self.mping_data()

	def add_deckpop_btn(self):
		deck_size = (self.sd["card"][0] * 1.5, self.sd["card"][1] * 1.5)
		for deck in se["main"]["t"]:
			# if not sd[deck]["c"]:
			# 	continue
			if f"id{deck}" in self.dpop:
				continue
			img = sd[deck]["img"]
			if "." in img:
				img = img[:-4]
			if img in other_img:
				source = "other"
			elif img in annex_img:
				source = "annex"
			else:
				source = "main"

			if deck.startswith("CE") or deck.startswith("CJ"):
				if img in annex_img or img in other_img:
					pass
				elif any(img in se["main"]["a"][set] for set in se["main"]["a"]):
					pass
				else:
					source = "other"
					img = "grey"

			if "main" in source:
				self.dpop[f"id{deck}"] = ImgButton(source=f"atlas://{img_ex}/main/{img}", size=deck_size,
				                                   cid=f"d{deck}",
				                                   card=self.sd["card"])
			else:
				self.dpop[f"id{deck}"] = ImgButton(source=f"atlas://{img_in}/{source}/{img}", size=deck_size,
				                                   cid=f"d{deck}", card=self.sd["card"])
			self.dpop[f"id{deck}"].btn.bind(on_release=self.popup_deck_slc, on_press=self.popup_deck_info)

	def update_deckpop_btn(self):
		self.decks["stack"].clear_widgets()
		temp = list(self.dpop.keys())
		for deck in temp:
			if "add" in deck:
				continue
			if deck[2:] not in sd:
				del self.dpop[deck]

	def get_index_stack(self, lst, max):
		n = len(lst) % max
		s = (max - n) / 2
		return -n, s

	def main_menu(self, *args):
		self.sd["single"] = Button(text="Start Game", on_release=self.popup_network_slc, cid="single")
		self.network["multi_btn"] = Button(text="Multiplayer (WIP)", on_release=self.popup_network_slc, cid="multi")
		self.network["deck_btn"] = Button(text="Deck Building", on_release=self.popup_network_slc, cid="ddd")
		self.network["other_btn"] = Button(text="Other", on_release=self.other_open, cid="other")
		self.sd["other"] = {}
		self.sd["other"]["down"] = Button(size_hint=(1, 1), text="Download", on_release=self.down_open)
		if self.gd["multiplay_btn"]:
			self.network["multi_btn"].disabled = False

		self.main_scrn = BoxLayout(orientation='vertical', size=(Window.width, Window.height))
		boxv2 = BoxLayout(orientation='vertical')
		boxv3 = BoxLayout(orientation='horizontal')

		img = Image(source=f"atlas://{img_in}/other/shiyoko", allow_stretch=True, size_hint=(1, 0.8))

		boxv3.add_widget(self.sd["other"]["down"])
		boxv3.add_widget(self.network["other_btn"])

		boxv2.add_widget(self.sd["single"])
		boxv2.add_widget(self.network["multi_btn"])
		boxv2.add_widget(self.network["deck_btn"])
		boxv2.add_widget(boxv3)
		self.sd["main_btn"] = [self.network["multi_btn"], self.network["deck_btn"], self.sd["other"]["down"],
		                       self.network["other_btn"], self.sd["single"]]
		self.main_scrn.add_widget(img)
		self.main_scrn.add_widget(boxv2)
		self.parent.add_widget(self.main_scrn)

		self.start_setting()

	def scale_mat(self, per=1.00, t=True, player=""):
		if t:
			mat = self.mat["1"]["id"]

			total_height = (sp[mat]["card"][1] / 10 * 8 + (
					sp[mat]["size"][1] + sp[mat]["card"][1] * 1.5) * 2) * per + sp[mat]["card"][1] / 6 * 2
			total_width = sp[mat]["size"][0] * per

			if total_height < Window.height and per == 1.00:
				per = 1.05
				self.scale_mat(per)
			elif total_height > Window.height and per == 1.00:
				per = 0.95
				self.scale_mat(per)
			elif total_height < Window.height and per > 1.00:
				per = per * 1.02
				self.scale_mat(per)
			elif total_height > Window.height and per < 1.00:
				per = per * 0.98
				self.scale_mat(per)
			else:
				if per != 1.00:
					if total_width > Window.width:
						per = per * 0.99
					self.sd["card"] = (sp[mat]["card"][0] * per, sp[mat]["card"][1] * per)
					self.sd["padding"] = sp[mat]["card"][1] * per / 10

					for player in list(self.pd.keys()):
						self.mat[player]["per"] = per
						self.scale_mat(t=False, player=player)
		else:
			mat = self.mat[player]["id"]
			sep = self.sd["card"][1] - self.sd["card"][0] / 2
			for field in sp[mat].keys():
				if field in ("card", "pos", "size", "actual", "name", "img", "c"):
					continue
				if field in ("Level", "Stock", "Climax", "Memory"):
					# card = (self.sd["card"][1]-sep, self.sd["card"][0]+sep)
					card = (self.sd["card"][1], self.sd["card"][0])
				else:
					card = self.sd["card"]
				card = self.sd["card"]

				xm = sp[mat][field][0] * self.mat[player]["per"] - card[0] / 2
				ym = sp[mat][field][1] * self.mat[player]["per"] - card[1] / 2

				if field == "Clock" or field == "Level" or field == "Stock" or field == "Res":
					am = sp[mat][field][2] * self.mat[player]["per"] - card[0] / 2
					bm = sp[mat][field][3] * self.mat[player]["per"] - card[1] / 2
					if field == "Stock":
						self.mat[player]["field"][field] = (xm, ym, am, bm)
					else:
						self.mat[player]["field"][field] = (xm, ym, am, bm)
				else:
					self.mat[player]["field"][field] = (xm, ym)

	def gotodeckedit(self, *args):
		self.main_scrn.pos = (-Window.width, -Window.height)
		self.main_scrn.disabled = False
		self.sd["t_bar"].x = -Window.width * 2
		self.sd["b_bar"].x = 0
		self.sd["debug"]["box"].x = -Window.width * 2
		self.sd["menu"]["btn"].x = -Window.width * 2
		self.mat["1"]["mat"].x = 0
		self.mat["1"]["mat"].y = -self.mat["1"]["mat"].size[1]
		self.mat["2"]["mat"].stand()
		self.mat["2"]["mat"].x = 0
		self.mat["2"]["mat"].y = -self.mat["2"]["mat"].size[1]
		self.parent.add_widget(self.decks["dbuild_btn"])
		self.decks["dbuild_btn"].pos = (0, 0)
		self.decks["sctm"].add_widget(self.decks["save"])

		for item in ("name", "format", "image", "lang"):
			self.decks["sctm"].add_widget(self.decks["st"][f"{item}_box"])

		self.decks["dbuild"] = {"l": "", "qty": {}, "names": {}, "neo": {}, "ns": [], "c": True, "n": "", "t": "",
		                        "img": "", "jap": "", "name": "", "date": "", "deck": {}, "pos": {}}
		self.decks["dbuild"]["qty"]["inds"] = list(self.pd["2"]["Library"])

		if self.decks["selected"]:
			self.decks["dbuilding"] = self.decks["selected"][1:]
			for key in sd[self.decks["selected"][1:]]:
				if key == "c":
					self.decks["dbuild"][key] = bool(sd[self.decks["selected"][1:]][key])
				elif key in ("img", "name", "jap", "date", "n", "t", "l"):
					self.decks["dbuild"][key] = str(sd[self.decks["selected"][1:]][key])
				elif key == "deck":
					self.decks["dbuild"][key] = dict(sd[self.decks["selected"][1:]][key])

			self.decks["st"]["name_btn"].text = self.decks["dbuild"]["name"]
			if self.decks["dbuild"]["l"] == "j":
				self.decks["st"]["lang_spn"].text = "Jap"
			elif self.decks["dbuild"]["l"] == "e":
				self.decks["st"]["lang_spn"].text = "Eng"
			else:
				self.decks["st"]["lang_spn"].text = "Both"

			if self.decks['dbuild']['img'] in other_img:
				self.decks["st"]["image_btn"].source = f"atlas://{img_in}/other/{self.decks['dbuild']['img']}"
			elif self.decks['dbuild']['img'] in annex_img:
				self.decks["st"]["image_btn"].source = f"atlas://{img_in}/annex/{self.decks['dbuild']['img']}"
			else:
				self.decks["st"]["image_btn"].source = f"atlas://{img_ex}/main/{self.decks['dbuild']['img']}"

			for ind in list(self.decks["dbuild"]["deck"].keys()):
				if self.decks["dbuild"]["deck"][ind] <= 0:
					del self.decks["dbuild"]["deck"][ind]
					continue
				self.decks["dbuild"]["qty"][sc[ind]["name"]] = 4
				for item in sc[ind]["text"]:
					eff = ab.cont(item)
					if "limit" in eff:
						self.decks["dbuild"]["qty"][sc[ind]["name"]] = eff[0]
						break
				self.decks["dbuild"]["qty"][ind] = []
				self.decks["dbuild"]["names"][sc[ind]["name"]] = 0
				for nx in range(self.decks["dbuild"]["deck"][ind]):
					if nx == 0:
						continue
					if nx > 4:
						break
					temp = self.decks["dbuild"]["qty"]["inds"].pop()
					self.decks["dbuild"]["qty"][ind].append(temp)
				self.check_card_neo(ind)
		else:
			for nx in range(1, 1000):
				if f"CEJ{str(nx).zfill(3)}" not in sd:
					self.decks["dbuilding"] = f"CEJ{str(nx).zfill(3)}"
					d = date.today()
					self.decks["dbuild"]["date"] = d.strftime("%Y/%m/%d")
					self.decks["dbuild"]["img"] = "empty"
					self.decks["dbuild"]["c"] = False
					break

		for nx in range(1, 51):
			self.mat["1"]["mat"].add_widget(self.decks["dbtn"][f"{nx}1bb"])

		self.decks["name_btn"].disabled = False
		self.decks["done_btn"].disabled = True

		if not self.decks["dbuild"]["n"]:
			self.decks["setting_pop"] = True
			self.popup_deck(t="setting")
		else:
			self.deck_building_cards()

	def check_card_neo(self, ind):
		# if "LB/W02" in ind:
		# 	self.decks["dbuild"]["neo"][ind] = False
		if self.decks["dbuild"]["n"] and any(set in ind for set in self.decks["dbuild"]["ns"]):
			if "KS/" in ind or "Sks/" in ind:
				if ind in (
						"KS/W49-T20", "KS/W49-T10", "KS/W49-066", "KS/W49-071", "KS/W49-056", "KS/W49-082",
						"KS/W49-075", "KS/W49-053", "KS/W49-057"):
					self.decks["dbuild"]["neo"][ind] = True
				else:
					self.decks["dbuild"]["neo"][ind] = False
			else:
				self.decks["dbuild"]["neo"][ind] = True
		else:
			self.decks["dbuild"]["neo"][ind] = False

	def update_deck_label(self):
		cards = self.decks["dbuild"]["deck"].keys()
		d = 0
		c = 0
		for card in cards:
			t = sc[card]["type"]

			d += self.decks["dbuild"]["deck"][card]
			if t == "Climax":
				c += self.decks["dbuild"]["deck"][card]

		self.decks["50"].text = f"{str(d).zfill(2)}/50"
		self.decks["8"].text = f"{c}/8"

		if c > 8:
			self.decks["done_btn"].disabled = True
		elif d < 50 or d > 50:
			self.decks["done_btn"].disabled = True
		else:
			self.decks["done_btn"].disabled = False

	def deck_building_cards(self):
		if self.decks["dbuild"]["n"]:
			self.decks["st"]["format_btn"].text = self.decks["dbuild"]["t"]
			if "Title" in self.decks["dbuild"]["n"]:
				self.decks["st"]["format_spn"].text = "Title-Specific"
			elif "Neo" in self.decks["dbuild"]["n"]:
				self.decks["st"]["format_spn"].text = "Neo-Standard"
			else:
				self.decks["st"]["format_spn"].text = self.decks["dbuild"]["n"]
			self.decks["st"]["format_btn"].disabled = False
			if self.decks["dbuild"]["n"] == "Standard":
				self.decks["dbuild"]["ns"] = ["-"]
				self.decks["st"]["format_btn"].disabled = True
			elif self.decks["dbuild"]["n"] == "Side":
				self.decks["dbuild"]["ns"] = sn["Side"][self.decks["dbuild"]["t"]]
			else:
				try:
					self.decks["dbuild"]["ns"] = sn["Title"][self.decks["dbuild"]["t"]] + \
					                             sn["Exception"][self.decks["dbuild"]["n"]][self.decks["dbuild"]["t"]]
				except KeyError:
					self.decks["dbuild"]["ns"] = sn["Title"][self.decks["dbuild"]["t"]]
		else:
			self.decks["dbuild"]["n"] = "Standard"
			self.decks["dbuild"]["ns"] = ["-"]

		if self.decks["dbuild"]["l"]:
			if self.decks["dbuild"]["l"] == "e":
				self.gd["p_cards"] = list(self.gd["eng_card"])
			elif self.decks["dbuild"]["l"] == "j":
				self.gd["p_cards"] = list(self.gd["jap_card"])
			else:
				self.gd["p_cards"] = list(sorted(se["main"]["c"]))
		else:
			self.gd["p_cards"] = list(sorted(se["main"]["c"]))

		if self.decks["dbuild"]["n"]:
			self.gd["p_cards"] = [s for s in self.gd["p_cards"] if any(ns in s for ns in self.decks["dbuild"]["ns"])]

		if self.decks["dbuild"]["n"] == "Side" and "Schwarz" in self.decks["dbuild"]["t"]:
			self.gd["p_cards"] = [s for s in self.gd["p_cards"] if "CGS/" in s or sc[s]["side"] == "Schwarz"]
		elif self.decks["dbuild"]["n"] == "Side" and "Weiβ" in self.decks["dbuild"]["t"]:
			self.gd["p_cards"] = [s for s in self.gd["p_cards"] if
			                      "CGS/" in s or sc[s]["side"] == "Weiβ" or sc[s]["side"] == "Weiss"]

		trait = ["Trait"]
		for ind in self.gd["p_cards"]:
			for trt in sc[ind]["trait"]:
				if trt and trt not in trait:
					trait.append(trt)
		self.sd["btn"]["ftrait"].values = trait

		self.gd["p_ld"] = list(sorted(self.cd.keys()))
		if "" in self.gd["p_ld"]:
			self.gd["p_ld"].remove("")
		if "00" in self.gd["p_ld"]:
			self.gd["p_ld"].remove("00")
		if "sspace" in self.gd["p_ld"]:
			self.gd["p_ld"].remove("sspace")

		for rr in range(20):
			if len(self.gd["p_cards"]) > len(self.gd["p_ld"]):
				for inx in range(1, len(self.gd["p_cards"]) - len(self.gd["p_ld"]) + 1):
					ind = f"{inx}{rr}"
					self.gd["p_ld"].append(ind)
					if ind not in self.cpop:
						self.cpop[ind] = CardImg(ind, self.sd["card"], "1", self.mat["1"]["per"])
						self.cpop[ind].btn.bind(on_press=self.card_btn_press, on_release=self.card_btn_release)
			else:
				break
		Clock.schedule_once(self.deck_building_layout, ability_dt)

	def deck_building_layout(self, *args):
		self.sd["popup"]["stack"].clear_widgets()
		for ind in self.cd:
			if ind in self.emptycards or ind == "1" or ind == "2":
				continue
			self.cd[ind].stand(a=False)
			self.cd[ind].pos = (0, 0)
			if ind.endswith("1"):
				self.decks["dbtn"][f"{ind}bb"].pos = (0, 0)
				self.decks["dbtn"][f"{ind}b-"].pos = (-Window.width, 0)
				self.decks["dbtn"][f"{ind}b+"].pos = (-Window.width, 0)

		self.hand_btn_show(False)

		d_width = self.sd["card"][1] + self.sd["padding"] * 1.3
		d_height = self.sd["card"][0] / 2 + self.sd["card"][1] + self.sd["padding"] * 1.1

		d_0 = []
		d_1 = []
		d_2 = []
		d_3 = []
		d_cx = []

		for ind in self.decks["dbuild"]["deck"]:
			if sc[ind]["type"] == "Climax":
				d_cx.append(ind)
			elif sc[ind]["level"] == 1:
				d_1.append(ind)
			elif sc[ind]["level"] == 2:
				d_2.append(ind)
			elif sc[ind]["level"] >= 3:
				d_3.append(ind)
			elif sc[ind]["level"] == 0:
				d_0.append(ind)

		d_r = 0
		for it in (d_0, d_1, d_2, d_3, d_cx):
			d_r += int(ceil(len(it) / dbuild_limit))
		if d_r > 0:
			d_r -= 1
		inx = 1
		ypos = self.mat["1"]["mat"].size[1] + self.sd["b_bar"].size[1]  # + self.sd["padding"]
		for item in (d_0, d_1, d_2, d_3, d_cx):
			xpos = 0
			c = 0

			if len(item) % dbuild_limit == 0:
				d_j = int(dbuild_limit)
			else:
				d_j = len(item) % dbuild_limit

			for ind in sorted(item):
				self.cd[f"{inx}1"].import_data(sc[ind])
				self.cd[f"{inx}1"].show_front()

				if len(item) > dbuild_limit and dbuild_limit % 2 == 0 and d_r > 0:
					xpos = Window.width / 2. - self.sd["padding"] / 2 * 0 - dbuild_limit / 2. * d_width + d_width * c
				elif len(item) > dbuild_limit and dbuild_limit % 2 != 0 and d_r > 0:
					xpos = Window.width / 2. - self.sd["padding"] / 2 * 0 - (dbuild_limit - 1) / 2. * d_width - \
					       self.sd["card"][1] / 2. + d_width * c
				elif d_j % 2 != 0:
					xpos = Window.width / 2. - self.sd["padding"] / 2 * 0 - (d_j - 1) / 2. * d_width - self.sd["card"][
						1] / 2. + d_width * c
				elif d_j % 2 == 0:
					xpos = Window.width / 2. - self.sd["padding"] / 2. * 0 - d_j / 2. * d_width + d_width * c

				self.decks["dbtn"][f"{inx}1bb"].x = xpos
				self.decks["dbtn"][f"{inx}1bb"].y = ypos + d_height * d_r + self.sd["padding"] / 3
				ybar = self.decks["dbtn"][f"{inx}1bb"].y + self.decks["dbtn"][f"{inx}1bb"].size[1] + self.sd[
					"padding"] * 0.25
				self.decks["dbtn"][f"{inx}1b-"].x = xpos
				self.decks["dbtn"][f"{inx}1b-"].y = self.sd["b_bar"].size[1] + d_height * d_r + self.sd["padding"] / 3

				self.decks["dbtn"][f"{inx}1b+"].x = xpos + self.decks["dbtn"][f"{inx}1bb"].size[0] - \
				                                    self.decks["dbtn"][f"{inx}1b+"].size[0]
				self.decks["dbtn"][f"{inx}1b+"].y = self.sd["b_bar"].size[1] + d_height * d_r + self.sd["padding"] / 3

				self.cd[f"{inx}1"].y = ybar
				self.decks["dbuild"]["pos"][f"{inx}1"] = (xpos, ybar, self.mat["1"]["mat"].size[1])

				self.update_qty_card(f"{inx}1")

				self.decks["dbtn"][f"{inx}1t"].text = str(self.decks["dbuild"]["deck"][ind])
				inx += 1
				c += 1
				if c >= dbuild_limit:
					# if len(item) > dbuild_limit:
					# 	d_r -= 1
					# if len(item) % dbuild_limit==0:
					d_r -= 1
					c = 0
			if len(item) > 0 and len(item) % dbuild_limit != 0:
				d_r -= 1

		self.update_deck_label()
		self.update_deck_names()
		self.sd["text"]["popup"].dismiss()

	def update_deck_names(self):
		self.decks["dbuild"]["names"] = {}
		for ind in self.decks["dbuild"]["deck"]:
			name = sc[ind]["name"]
			for x in range(self.decks["dbuild"]["deck"][ind]):
				if name in self.decks["dbuild"]["names"]:
					self.decks["dbuild"]["names"][name] += 1
				else:
					self.decks["dbuild"]["names"][name] = 1

	def remove_card(self, btn):
		ind = btn.cid[:-1]
		card = self.cd[ind].cid
		name = self.cd[ind].name
		if self.decks["dbuild"]["deck"][card] > 0:
			if self.decks["dbuild"]["deck"][card] <= 5:
				if len(self.decks["dbuild"]["qty"][card]) > 0:
					temp = self.decks["dbuild"]["qty"][card].pop()
					self.decks["dbuild"]["qty"]["inds"].append(temp)
			self.decks["dbuild"]["deck"][card] -= 1
			self.decks["dbuild"]["names"][name] -= 1
			self.decks["dbtn"][f"{ind}t"].text = str(self.decks["dbuild"]["deck"][card])
			if self.decks["dbuild"]["deck"][card] <= 0:
				self.decks["dbtn"][f"{ind}bb"].x = -Window.width * 2
				self.decks["dbtn"][f"{ind}b-"].x = -Window.width * 2
				self.decks["dbtn"][f"{ind}b+"].x = -Window.width * 2
				del self.decks["dbuild"]["deck"][card]
				del self.decks["dbuild"]["neo"][card]
				Clock.schedule_once(self.deck_building_layout, ability_dt)
			else:
				self.update_qty_card(ind)
				self.update_deck_label()

	def update_edata(self, *arg):
		with open(f"{data_ex}/cej.db", "w") as w_d:
			jdump(json_zip(scej), w_d, separators=(',', ':'))
		self.gd["update_edata"] = True

	def wait_update(self, *args):
		if self.gd["update_edata"]:
			Clock.schedule_once(partial(self.popup_deck, "ddd"))
		else:
			Clock.schedule_once(self.wait_update, move_dt_btw)

	def add_card(self, btn):
		ind = btn.cid[:-1]
		card = self.cd[ind].cid
		name = self.cd[ind].name
		limit = self.decks["dbuild"]["qty"][name]
		if self.decks["dbuild"]["names"][name] < limit:
			if self.decks["dbuild"]["deck"][card] < 5:
				if len(self.decks["dbuild"]["qty"]["inds"]) > 0:
					temp = self.decks["dbuild"]["qty"]["inds"].pop()
					self.decks["dbuild"]["qty"][card].append(temp)
			self.decks["dbuild"]["names"][name] += 1
			self.decks["dbuild"]["deck"][card] += 1
			self.decks["dbtn"][f"{ind}t"].text = str(self.decks["dbuild"]["deck"][card])
			self.update_qty_card(ind)
			self.update_deck_label()

	def update_qty_card(self, ind):
		inx = self.cd[ind].cid
		sep = (self.sd["card"][1] - self.sd["card"][0]) / 2
		if self.cd[ind].card == "Climax":
			self.cd[ind].climax(a=False)
			self.cd[ind].x = self.decks["dbuild"]["pos"][ind][0]
			self.field_btn[f"Hand{ind}"].size = (self.sd["card"][1], self.sd["card"][0])
			if self.decks["dbuild"]["deck"][inx] == 1:
				self.cd[ind].y = self.decks["dbuild"]["pos"][ind][1] + sep
				self.field_btn[f"Hand{ind}"].pos = (
					self.cd[ind].pos[0],
					self.cd[ind].pos[1] - self.decks["dbuild"]["pos"][ind][2])
			else:
				if self.decks["dbuild"]["deck"][inx] == 2:
					self.cd[ind].y = self.decks["dbuild"]["pos"][ind][1] + sep / 3 * 2
				elif self.decks["dbuild"]["deck"][inx] == 3:
					self.cd[ind].y = self.decks["dbuild"]["pos"][ind][1] + sep / 3
				elif self.decks["dbuild"]["deck"][inx] >= 4:
					self.cd[ind].y = self.decks["dbuild"]["pos"][ind][1]
				for nx in range(len(self.decks["dbuild"]["qty"][inx])):
					# if nx>3:
					# 	continue
					inq = self.decks["dbuild"]["qty"][inx][nx]

					self.cd[inq].y = self.cd[ind].y - sep + sep / 3 * 2 * (nx + 1)
					self.cd[inq].x = self.cd[ind].x + sep
					self.cd[inq].climax(a=False)
					self.cd[inq].show_back()
				self.field_btn[f"Hand{ind}"].pos = (
					self.cd[ind].pos[0], self.cd[ind].pos[1] - self.decks["dbuild"]["pos"][ind][2])
			self.cd[ind].x += sep
			self.cd[ind].y -= sep
		else:
			self.cd[ind].y = self.decks["dbuild"]["pos"][ind][1]
			if self.decks["dbuild"]["deck"][inx] == 1:
				self.cd[ind].x = self.decks["dbuild"]["pos"][ind][0] + sep
			else:
				if self.decks["dbuild"]["deck"][inx] == 2:
					self.cd[ind].x = self.decks["dbuild"]["pos"][ind][0] + sep / 3 * 2
				elif self.decks["dbuild"]["deck"][inx] == 3:
					self.cd[ind].x = self.decks["dbuild"]["pos"][ind][0] + sep / 3
				elif self.decks["dbuild"]["deck"][inx] >= 4:
					self.cd[ind].x = self.decks["dbuild"]["pos"][ind][0]
				for nx in range(len(self.decks["dbuild"]["qty"][inx])):
					# if nx>3:
					# 	continue
					inq = self.decks["dbuild"]["qty"][inx][nx]
					self.cd[inq].x = self.cd[ind].x + sep / 3 * 2 * (nx + 1)
					self.cd[inq].y = self.cd[ind].y
					self.cd[inq].show_back()
			self.field_btn[f"Hand{ind}"].pos = (
				self.cd[ind].pos[0], self.cd[ind].pos[1] - self.decks["dbuild"]["pos"][ind][2])

		if self.decks["dbuild"]["deck"][inx] > 1:
			for nx in reversed(range(len(self.decks["dbuild"]["qty"][inx]))):
				# if nx > 3:
				# 	continue
				inq = self.decks["dbuild"]["qty"][inx][nx]
				self.mat["2"]["mat"].remove_widget(self.cd[inq])
				self.mat["2"]["mat"].add_widget(self.cd[inq])

		for ind in self.decks["dbuild"]["qty"]["inds"]:
			self.cd[ind].stand(a=False)
			self.cd[ind].pos = (0, 0)

	def clear_building(self, *args):
		self.mat["1"]["mat"].pos = (
			-Window.width * 2,
			Window.height / 2 - self.sd["padding"] - self.sd["card"][1] / 6 - self.mat["1"]["mat"].height)
		self.mat["2"]["mat"].pos = (-Window.width * 2, Window.height / 2 + self.sd["padding"] + self.sd["card"][1] / 6)
		self.mat["2"]["mat"].reverse()
		self.sd["b_bar"].x = -Window.width * 2

		for ind in self.cd:
			if ind in self.emptycards or ind == "1" or ind == "2":
				continue
			self.cd[ind].stand(a=False)
			self.cd[ind].pos = (0, 0)

		self.hand_btn_show(False)
		for inx in range(1, 51):
			self.mat["1"]["mat"].remove_widget(self.decks["dbtn"][f"{inx}1bb"])
			self.decks["dbtn"][f"{inx}1bb"].x = -Window.width * 2
			self.decks["dbtn"][f"{inx}1b-"].x = -Window.width * 2
			self.decks["dbtn"][f"{inx}1b+"].x = -Window.width * 2

		for item in ("name", "format", "image", "lang"):
			self.decks["sctm"].remove_widget(self.decks["st"][f"{item}_box"])

		self.decks["sctm"].remove_widget(self.decks["save"])
		self.decks["st"]["name_btn"].text = ""
		self.decks["st"]["format_spn"].text = "-"
		self.decks["st"]["format_btn"].text = ""
		self.decks["st"]["format_btn"].disabled = True
		self.decks["st"]["image_btn"].source = f"atlas://{img_in}/other/empty"
		self.decks["st"]["lang_spn"].text = "Both"
		self.sd["btn"]["Addcls_btn"].y = -Window.height * 2
		self.decks["rv"].set_title = ""
		self.parent.remove_widget(self.decks["dbuild_btn"])
		self.decks["dbuild"] = {}
		self.sd["btn"]["filter_add"].y = -Window.height
		self.sd["btn"]["Add_btn"].y = -Window.height
		self.sd["popup"]["stack"].clear_widgets()

	def building_btn_done(self, *args):
		if self.decks["setting_pop"]:
			self.decks["setting_pop"] = False

		if len(self.decks["dbuild"]["deck"]) > 0:
			if self.decks["dbuilding"] not in sd:
				sd[self.decks["dbuilding"]] = {}

			if self.decks["50"].text[:2] == "50" and self.decks["8"].text[0] == "8":
				self.decks["dbuild"]["c"] = True

			if any(not indx for indx in self.decks["dbuild"]["neo"]):
				self.decks["dbuild"]["c"] = False

			for key in ("n", "t", "img", "date", "name", "jap", "deck", "c", "l"):
				if key == "c":
					sd[self.decks["dbuilding"]][key] = bool(self.decks["dbuild"][key])
				elif key == "deck":
					sd[self.decks["dbuilding"]][key] = dict(self.decks["dbuild"][key])
				else:
					sd[self.decks["dbuilding"]][key] = str(self.decks["dbuild"][key])
			scej[self.decks["dbuilding"]] = dict(sd[self.decks["dbuilding"]])
			self.add_deckpop_btn()

		self.gd["update_edata"] = False
		Clock.schedule_once(self.clear_building)
		# self.update_edata()
		# self.clear_building()
		Clock.schedule_once(self.update_edata)
		Clock.schedule_once(self.wait_update, move_dt_btw)

	def building_btn(self, btn):
		if btn.cid == "done":
			# Clock.schedule_once(partial(self.popup_text, "Loading"), ability_dt)
			self.decks["popup"].dismiss()
			self.popup_text("Loading")
			Clock.schedule_once(self.building_btn_done)
		elif btn.cid == "name":
			self.decks["setting_pop"] = True
			self.popup_deck(t="setting_img")
		elif btn.cid == "close":
			self.sd["popup"]["popup"].dismiss()
		elif btn.cid == "add":
			self.popup_text("Loading")
			Clock.schedule_once(self.add_building_popup)
		elif btn.cid == "adding":
			self.popup_text("Loading")
			self.sd["popup"]["popup"].dismiss()
			self.sd["cpop_press"] = []
			if self.sd["cpop_pressing"] is not None:
				self.sd["cpop_pressing"].cancel()
				self.sd["cpop_pressing"] = None
			for ind in sorted(self.decks["add_chosen"]):
				name = sc[ind]["name"]
				if name in self.decks["dbuild"]["names"]:
					limit = self.decks["dbuild"]["qty"][name]
					if self.decks["dbuild"]["names"][name] < limit:
						if ind not in self.decks["dbuild"]["deck"]:
							self.decks["dbuild"]["deck"][ind] = 1
							self.decks["dbuild"]["qty"][ind] = []
						else:
							if self.decks["dbuild"]["deck"][ind] < 5:
								temp = self.decks["dbuild"]["qty"]["inds"].pop()
								self.decks["dbuild"]["qty"][ind].append(temp)
							self.decks["dbuild"]["deck"][ind] += 1
						self.decks["dbuild"]["names"][name] += 1
				else:
					self.decks["dbuild"]["deck"][ind] = 1
					self.decks["dbuild"]["names"][name] = 1
					self.decks["dbuild"]["qty"][name] = 4
					for item in sc[ind]["text"]:
						eff = ab.cont(item)
						if "limit" in eff:
							self.decks["dbuild"]["qty"][name] = eff[0]
							break

					self.decks["dbuild"]["qty"][ind] = []

				self.check_card_neo(ind)
			self.decks["add_chosen"] = []
			self.deck_building_layout()

	# Clock.schedule_once(self.deck_building_layout, ability_dt)
	# self.sd["popup"]["popup"].dismiss()

	def add_building_popup(self, *args):
		self.sd["popup"]["popup"].title = "Add a card to deck"
		self.gd["confirm_var"] = {"o": "1", "c": "Add", "m": 1}
		Clock.schedule_once(self.popup_start, popup_dt)

	def popup_filter_add(self, spinner, text):
		if "Lvl" in text:
			self.gd["p_flvl"] = text
		elif any(text == s for s in self.sd["btn"]["fcolour"].values):
			self.gd["p_fcolour"] = text
		elif any(text == s for s in self.sd["btn"]["ftype"].values):
			self.gd["p_ftype"] = text
		elif any(text == s for s in self.sd["btn"]["ftrait"].values):
			self.gd["p_ftrait"] = text
		elif text != "":
			self.gd["p_ftext"] = text
		else:
			self.gd["p_ftext"] = ""

		if self.gd["p_c"] == "Add":
			self.popup_filter()

	def filter_deck_add(self):
		self.gd["p_fcards"] = self.gd["p_cards"]
		if self.gd["remove_cards_in_deck"]:
			for ind in self.decks["dbuild"]["deck"]:
				if ind in self.gd["p_fcards"]:
					self.gd["p_fcards"].remove(ind)
		if self.gd["p_flvl"] != "Lvl -":
			if self.gd["p_flvl"][-1] == "3":
				self.gd["p_fcards"] = [s for s in self.gd["p_fcards"] if sc[s]["level"] >= int(self.gd["p_flvl"][-1])]
			elif self.gd["p_flvl"][-1] == "0":
				self.gd["p_fcards"] = [s for s in self.gd["p_fcards"] if
				                       sc[s]["level"] == int(self.gd["p_flvl"][-1]) and sc[s]["type"] != "Climax"]
			else:
				self.gd["p_fcards"] = [s for s in self.gd["p_fcards"] if sc[s]["level"] == int(self.gd["p_flvl"][-1])]
		if self.gd["p_fcolour"] != "Colour":
			self.gd["p_fcards"] = [s for s in self.gd["p_fcards"] if sc[s]["colour"] == self.gd["p_fcolour"]]
		if self.gd["p_ftype"] != "Type":
			self.gd["p_fcards"] = [s for s in self.gd["p_fcards"] if sc[s]["type"] == self.gd["p_ftype"]]
		if self.gd["p_ftrait"] != "Trait":
			self.gd["p_fcards"] = [s for s in self.gd["p_fcards"] if self.gd["p_ftrait"] in sc[s]["trait"]]
		if self.gd["p_ftext"] != "":
			self.gd["p_fcards"] = [s for s in self.gd["p_fcards"] if
			                       self.gd["p_ftext"].lower() in sc[s]["name"].lower()]
		self.gd["p_l"] = self.gd["p_ld"][:len(self.gd["p_fcards"])]

	def deck_create(self, *args):
		self.cd[""] = CardEmpty()
		self.cd["1"] = Card(code="1", card=self.sd["card"], owner="1", per=self.mat["1"]["per"])
		self.cd["2"] = Card(code="2", card=self.sd["card"], owner="2", per=self.mat["2"]["per"])
		self.cd["sspace"] = CardEmpty()
		for player in list(self.pd.keys()):
			for inx in range(1, 51):
				ind = f"{inx}{player}"
				self.pd[player]["Library"].append(ind)
				self.cd[ind] = Card(code=ind, card=self.sd["card"], owner=player, per=self.mat[player]["per"])
				# self.cd[ind].import_data(sc["MK/S11-E101"])
				self.cd[ind].setPos(xpos=-Window.width, ypos=-Window.height, a=False, t="Library")
				self.cd[ind].show_back()
				self.mat[player]["mat"].add_widget(self.cd[ind])

	def deck_fill(self, *args):
		for player in list(self.pd.keys()):
			self.gd["inx"] = 1
			for card in sorted(self.pd[player]["deck"].keys()):
				for nx in range(self.pd[player]["deck"][card]):
					ind = f"{self.gd['inx']}{player}"
					self.cd[ind].import_data(sc[card])
					self.cd[ind].setPos(field=self.mat[player]["field"]["Library"], a=False, t="Library")
					self.cpop[ind].import_data(sc[card])
					self.gd["inx"] += 1

	def on_touch_down(self, touch):
		self.sd["touch_down"] = touch.pos
		if self.gd["active"] != "" and self.gd["active"] is not None:
			# if not self.gd["popup_done"][0] and not self.gd["popup_done"][1]:
			# 	self.sd["popup"]["popup"].open()

			if self.gd["phase"] not in ("Draw", "Janken", "Stand Up", ""):  # ""
				# self.sd["touch_down"] = touch.pos
				if self.gd["popup_on"] or self.gd["active"] == "1":
					for field in self.gd["fields"]:
						for card in self.pd[self.gd["active"]][field]:
							if card == "":
								continue

							width = (self.mat[self.gd["active"]]["mat"].x + self.cd[card].x,
							         self.mat[self.gd["active"]]["mat"].x + self.cd[card].x + self.sd["card"][0])
							height = (self.mat[self.gd["active"]]["mat"].y + self.cd[card].y,
							          self.mat[self.gd["active"]]["mat"].y + self.cd[card].y + self.sd["card"][1])

							if width[0] < touch.pos[0] < width[1] and height[0] < touch.pos[1] < height[1]:
								self.gd["selected"] = card
								self.gd["last"] = card

								self.gd["btn_id"] = self.gd["selected"]
								self.gd["btn_release"] = False
								self.gd["moving"] = False
								if touch.is_triple_tap:
									self.infot = Clock.schedule_once(self.info_start, ability_dt)
								else:
									self.infot = Clock.schedule_once(self.info_start, info_popup_dt)

								self.gd["old_pos"] = (self.cd[card].x, self.cd[card].y)

								self.mat[self.gd["active"]]["mat"].remove_widget(self.cd[self.gd["selected"]])
								self.mat[self.gd["active"]]["mat"].add_widget(self.cd[self.gd["selected"]])
								break
		return True

	def on_touch_move(self, touch):
		if (self.gd["phase"] == "Main" or self.gd["phase"] == "Climax") and self.gd["active"] == "1":
			if self.sd["touch_down"] and (
					touch.pos[0] / self.sd["touch_down"][0] >= 1.33 or touch.pos[0] / self.sd["touch_down"][
				0] <= 0.67) and (
					touch.pos[1] / self.sd["touch_down"][1] >= 1.33 or touch.pos[1] / self.sd["touch_down"][1] <= 0.67):
				self.gd["moving"] = True
			if self.infot is not None:
				self.infot.cancel()
				self.infot = None

			if self.gd["selected"] in self.gd["moveable"] and self.gd["selected"] != "":
				self.gd["touch_move_x"] = touch.pos[0] - self.sd["touch_down"][0]

				card = self.cd[self.gd["selected"]]
				self.mat[self.gd["selected"][-1]]["mat"].remove_widget(card)
				self.mat[self.gd["selected"][-1]]["mat"].add_widget(card)
				width = (self.mat[self.gd["active"]]["field"]["Climax"][0] - self.sd["card"][1] / 2.,
				         self.mat[self.gd["active"]]["field"]["Climax"][0] + self.sd["card"][1] + self.sd["card"][
					         1] / 2.)
				height = (self.mat[self.gd["active"]]["field"]["Climax"][1] - self.sd["card"][0] / 2.,
				          self.mat[self.gd["active"]]["field"]["Climax"][1] + self.sd["card"][0] + self.sd["card"][
					          0] / 2.)

				if card.card == "Climax" and width[0] < card.center_x < width[1] and height[0] < card.center_y < height[
					1]:
					card.climax()
				elif card.card == "Climax" and card.status == "":
					card.stand()

				if not self.gd["confirm_requirement"]:
					if card.card == "Climax" and card.mcolour not in self.pd[self.gd["active"]]["colour"] and touch.pos[
						1] >= self.mat[self.gd["active"]]["mat"].y:
						self.gd["touch_move_y"] = self.mat[self.gd["active"]]["mat"].y - self.sd["touch_down"][1]
					elif card.card != "Climax" and card.level != 0 and len(
							self.pd[self.gd["active"]]["Level"]) < card.level and touch.pos[1] >= \
							self.mat[self.gd["active"]][
								"mat"].y:
						self.gd["touch_move_y"] = self.mat[self.gd["active"]]["mat"].y - self.sd["touch_down"][1]
					elif card.card != "Climax" and card.level != 0 and len(
							self.pd[self.gd["active"]]["Level"]) >= card.level and card.mcolour not in \
							self.pd[self.gd["active"]]["colour"] and touch.pos[1] >= self.mat[self.gd["active"]][
						"mat"].y:
						self.gd["touch_move_y"] = self.mat[self.gd["active"]]["mat"].y - self.sd["touch_down"][1]
					elif card.card != "Climax" and card.level != 0 and len(
							self.pd[self.gd["active"]]["Level"]) >= card.level and card.mcolour in \
							self.pd[self.gd["active"]][
								"colour"] and len(self.pd[self.gd["active"]]["Stock"]) < card.cost and touch.pos[1] >= \
							self.mat[self.gd["active"]]["mat"].y:
						self.gd["touch_move_y"] = self.mat[self.gd["active"]]["mat"].y - self.sd["touch_down"][1]
					else:
						self.gd["touch_move_y"] = touch.pos[1] - self.sd["touch_down"][1]
				else:
					self.gd["touch_move_y"] = touch.pos[1] - self.sd["touch_down"][1]

				card.center_y = self.gd["old_pos"][1] + self.gd["touch_move_y"] + self.sd["card"][1] / 2.
				card.center_x = self.gd["old_pos"][0] + self.gd["touch_move_x"] + self.sd["card"][0] / 2.

		return True

	def on_touch_up(self, touch):
		if self.infot is not None:
			self.infot.cancel()
			self.infot = None
		self.sd["touch_down"] = None
		if self.gd["phase"] == "Main":
			if self.gd["selected"] != "":
				card = self.cd[self.gd["selected"]]

				if self.gd["selected"] in self.pd[self.gd["active"]]["Hand"]:
					fields = list(self.gd["stage"]) + ["Climax"]

					if touch.pos[1] <= self.mat[self.gd["active"]]["mat"].y:
						for ncard in self.pd[self.gd["active"]]["Hand"]:
							width = (self.cd[ncard].x, self.cd[ncard].x + self.sd["card"][0])
							height = (self.cd[ncard].y, self.cd[ncard].y + self.sd["card"][1])

							if width[0] < self.cd[self.gd["selected"]].center_x < width[1] and height[0] < \
									self.cd[self.gd["selected"]].center_y < height[1] and ncard != self.gd["selected"]:
								self.gd["swap_card"][0] = True
								self.gd["swap_card"][1] = ncard
								self.gd["swap_card"][2] = self.pd[self.gd["active"]]["Hand"].index(ncard)
								self.gd["swap_card"][3] = self.pd[self.gd["active"]]["Hand"].index(self.gd["selected"])
								break

						if self.gd["swap_card"][0]:
							self.pd[self.gd["active"]]["Hand"][self.gd["swap_card"][2]] = self.gd["selected"]
							self.pd[self.gd["active"]]["Hand"][self.gd["swap_card"][3]] = self.gd["swap_card"][1]
							self.gd["swap_card"][0] = False
						self.check_cont_hand("1")
						self.hand_size(self.gd["active"])
						self.gd["selected"] = ""
						self.hand_size(self.gd["active"], move=False)
					else:
						if card.card == "Event":
							if touch.pos[1] > self.mat[self.gd["active"]]["mat"].y:
								# if self.gd["confirm_requirement"]:
								if not self.check_condition(self.gd["selected"]):
									Clock.schedule_once(self.check_cont_ability, ability_dt)
									self.gd["selected"] = ""
									self.hand_size(self.gd["active"])
									return True

								self.gd["moveable"] = []
								self.play([self.gd["selected"],"Res",""])
								# self.pd[self.gd["active"]]["Hand"].remove(self.gd["selected"])
								# res = self.mat[self.gd["active"]]["field"]["Res"]
								# card.setPos(field=((res[2] - res[0]) / 2 + res[0], (res[3] - res[1]) / 2 + res[1]),
								#             t="Res")

								# self.pd[self.gd["active"]]["Res"].append(self.gd["selected"])
								# if self.net["game"]:
								# 	self.net["send"] = False
								# self.gd["play_card"] = self.gd["selected"]
								# Clock.schedule_once(self.play_card, ability_dt)
						else:
							for field in fields:
								width = (self.mat[self.gd["active"]]["field"][field][0],
								         self.mat[self.gd["active"]]["field"][field][0] + self.sd["card"][0])
								height = (self.mat[self.gd["active"]]["field"][field][1],
								          self.mat[self.gd["active"]]["field"][field][1] + self.sd["card"][1])

								if width[0] < card.center_x < width[1] and height[0] < card.center_y < height[1]:
									if not self.check_condition(self.gd["selected"]):
										break
									self.gd["moveable"] = []
									if field == "Climax" and card.card == "Climax":
										self.gd["playable_climax"] = []
										self.pd[self.gd["active"]]["Hand"].remove(self.gd["selected"])
										card.setPos(field=self.mat[self.gd["active"]]["field"][field], t=field)
										self.pd[self.gd["active"]][field].append(self.gd["selected"])
										self.gd["play_card"] = str(self.gd["selected"])
										self.pd[self.gd["active"]]["done"]["Main"] = True
										self.check_cont_ability()
										self.gd["selected"] = ""
										self.hand_size(self.gd["active"])
										if self.net["game"] and self.gd["active"] == "1":
											self.net["var"] = [self.gd["play_card"]]
											self.net["var1"] = "play_climax"
											if not self.poptext:
												Clock.schedule_once(partial(self.popup_text, "waitingser"))
											self.mconnect("phase")
											return True
										else:
											self.gd["phase"] = "Climax"
											self.gd["nomay"] = True
											Clock.schedule_once(self.climax_phase, ability_dt)

									elif field != "Climax" and card.card != "Climax":
										ind = self.pd[self.gd["active"]][field[:-1]][int(field[-1])]
										self.gd["play"] = [card.ind, field[:-1], int(field[-1])]
										if ind != "":
											if self.gd["overlap_confirm"]:
												self.gd["confirm_trigger"] = "Overplay"
												self.gd["confirm_var"] = {"ind": f"{card.ind}_{ind}", "c": "Overplay"}
												Clock.schedule_once(self.confirm_popup, popup_dt)
												return False
											else:
												self.play(self.gd["play"])
										else:
											self.play(self.gd["play"])
									break
				elif any(self.gd["selected"] in self.pd[self.gd["active"]][field] for field in ("Center", "Back")):
					for field in self.gd["stage"]:
						width = (self.mat[self.gd["active"]]["field"][field][0],
						         self.mat[self.gd["active"]]["field"][field][0] + self.sd["card"][0])
						height = (self.mat[self.gd["active"]]["field"][field][1],
						          self.mat[self.gd["active"]]["field"][field][1] + self.sd["card"][1])

						if width[0] < card.center_x < width[1] and height[0] < card.center_y < height[1]:
							if field != card.pos_new:
								if self.pd[self.gd["active"]][field[:-1]][int(field[-1])] != "":
									temp = self.pd[self.gd["active"]][field[:-1]][int(field[-1])]
									self.cd[temp].setPos(field=self.mat[temp[-1]]["field"][card.pos_new],
									                     t=card.pos_new)
									self.pd[self.gd["active"]][card.pos_new[:-1]][int(card.pos_new[-1])] = temp
								else:
									self.pd[self.gd["active"]][card.pos_new[:-1]][int(card.pos_new[-1])] = ""

								card.setPos(field=self.mat[card.owner]["field"][field], t=field)
								self.pd[self.gd["active"]][field[:-1]][int(field[-1])] = self.gd["selected"]

							if self.net["game"] and self.gd["active"] == "1":
								self.net["var"] = [card.ind, card.pos_new[:-1], card.pos_new[-1]]
								self.net["var1"] = "move_card"
								self.update_marker()
								self.check_cont_ability()
								self.gd["selected"] = ""
								self.hand_size(self.gd["active"])
								if not self.poptext:
									Clock.schedule_once(partial(self.popup_text, "waitingser"))
								self.mconnect("phase")
								return True
							break

					card.setPos(field=self.mat[card.owner]["field"][card.pos_new], t=card.pos_new)
					self.update_marker()
					self.check_cont_ability()

				self.gd["selected"] = ""
				self.hand_size(self.gd["active"])

		if self.gd["phase"] == "Climax":
			if self.gd["selected"] != "":
				card = self.cd[self.gd["selected"]]
				width = (
					self.mat[self.gd["active"]]["field"]["Climax"][0],
					self.mat[self.gd["active"]]["field"]["Climax"][0] + self.sd["card"][0])
				height = (
					self.mat[self.gd["active"]]["field"]["Climax"][1],
					self.mat[self.gd["active"]]["field"]["Climax"][1] + self.sd["card"][1])

				if width[0] < card.center_x < width[1] and height[0] < card.center_y < height[1]:
					if self.check_condition(self.gd["selected"]):
						self.gd["moveable"] = self.gd["playable_climax"] = []
						self.pd[self.gd["active"]]["Hand"].remove(self.gd["selected"])
						card.setPos(field=self.mat[self.gd["active"]]["field"]["Climax"], t="Climax")
						self.pd[self.gd["active"]]["Climax"].append(self.gd["selected"])
						self.gd["play_card"] = str(self.gd["selected"])
						Clock.schedule_once(self.climax_phase_play, ability_dt)

			self.gd["selected"] = ""
			self.hand_size(self.gd["active"])
			Clock.schedule_once(self.check_cont_ability, ability_dt)

		if self.gd["phase"] == "End":
			self.hand_size(self.gd["active"])

		return True

	def field_btn_fill(self, dt=0):
		pos = (-Window.width * 2, -Window.height * 2)
		for player in list(self.pd.keys()):
			for field in self.mat[player]["field"]:
				if field == "Level":
					size = (
						self.sd["card"][1],
						abs(self.mat[player]["field"][field][3] - self.mat[player]["field"][field][1]) +
						self.sd["card"][0])
				elif field == "Stock":
					size = (self.sd["card"][1],
					        abs(self.mat[player]["field"][field][3] - self.mat[player]["field"][field][1]) +
					        self.sd["card"][0])
				elif field == "Climax" or field == "Memory":
					size = (self.sd["card"][1], self.sd["card"][0])
				elif field == "Clock":
					size = (
						abs(self.mat[player]["field"][field][2] - self.mat[player]["field"][field][0]) +
						self.sd["card"][0],
						self.sd["card"][1])
				elif field == "Res":
					size = (
						abs(self.mat[player]["field"][field][2] - self.mat[player]["field"][field][0] + self.sd["card"][
							0]),
						abs(self.mat[player]["field"][field][3] - self.mat[player]["field"][field][1] + self.sd["card"][
							1]))

					size1 = (self.sd["card"][0],
					         abs(self.mat[player]["field"]["Library"][1] + self.sd["card"][1] -
					             self.mat[player]["mat"].pos_mat[1]))

					self.field_btn[f"{field}1{player}"] = Button(text=f"{field}1", cid=field + player, pos=pos,
					                                             opacity=0, on_press=self.show_info_btn,
					                                             size=size1, on_release=self.show_info_re)
					self.parent.add_widget(self.field_btn[f"{field}1{player}"])
				else:
					size = self.sd["card"]

				self.field_btn[f"{field}{player}"] = Button(text=field, cid=field + player[-1], opacity=0,
				                                            pos=pos, size=size, on_press=self.show_info_btn,
				                                            on_release=self.show_info_re)
				self.parent.add_widget(self.field_btn[f"{field}{player}"])

			for field in self.gd["stage"]:
				size = (self.sd["card"][0] + self.sd["padding"] * 2, self.sd["card"][1] + self.sd["padding"] * 2)
				pos = (
					-Window.width * 3,
					self.mat[player]["field"][field][1] - self.sd["padding"] + self.mat[player]["mat"].y)
				self.field_btn[f"{field}{player}s"] = Image(source=f"atlas://{img_in}/other/movable", size=size,
				                                            pos=pos,
				                                            size_hint=(None, None), allow_stretch=True,
				                                            keep_ratio=False)
				self.mat[player]["mat"].add_widget(self.field_btn[f"{field}{player}s"])
			for r in range(select2cards):
				self.field_btn[f"stage{r}{player}s"] = Image(source=f"atlas://{img_in}/other/select2", size=(
					self.sd["card"][0] + self.sd["padding"] * 2, self.sd["card"][1] + self.sd["padding"] * 2), pos=pos,
				                                     size_hint=(None, None), allow_stretch=True, keep_ratio=False)
				self.mat[f"{player}"]["mat"].add_widget(self.field_btn[f"stage{r}{player}s"])

	def field_btn_pos(self, dt=0):
		sep = (self.sd["card"][1] - self.sd["card"][0]) / 2
		for player in list(self.pd.keys()):
			for field in self.mat[player]["field"]:
				if field == "Res":
					if player == "1":
						pos1 = (self.mat[player]["field"]["Library"][0] - self.sd["padding"] / 4 - self.sd["card"][0] +
						        self.mat[player]["mat"].x,
						        self.mat[player]["mat"].y + self.mat[player]["field"]["Library"][1] + self.sd["card"][
							        1] - self.field_btn[f"{field}1{player}"].size[1])
					elif player == "2":
						pos1 = (
							self.mat[player]["mat"].x + self.mat[player]["mat"].size[0] + self.sd["card"][0] + self.sd[
								"padding"] / 4 - self.sd["card"][0] - self.mat[player]["field"]["Library"][0],
							self.mat[player]["mat"].y + self.mat[player]["mat"].size[1] -
							self.mat[player]["field"]["Library"][1] - self.sd["card"][1])

					self.field_btn[f"{field}1{player}"].x -= Window.width * 2
				if player == "1":
					pos = (self.mat[player]["field"][field][0] + self.mat[player]["mat"].x,
					       self.mat[player]["field"][field][1] + self.mat[player]["mat"].y)

					if field == "Climax" or field == "Memory" or field == "Level":
						pos = (pos[0] - sep, pos[1] + sep)

					if field == "Stock":
						pos = (self.mat[player]["field"][field][0] + self.mat[player]["mat"].x - sep,
						       self.mat[player]["field"][field][3] + self.mat[player]["mat"].y + sep)
				elif player == "2":
					pos = (
						self.mat[player]["mat"].x + self.mat[player]["mat"].size[0] - self.sd["card"][0] -
						self.mat[player]["field"][field][0],
						self.mat[player]["mat"].y + self.mat[player]["mat"].size[1] - self.sd["card"][1] -
						self.mat[player]["field"][field][1])
					if field == "Level":
						pos = (self.mat[player]["mat"].x + self.mat[player]["mat"].size[0] - self.sd["card"][1] -
						       self.mat[player]["field"][field][0] + sep,
						       self.mat[player]["mat"].y + self.mat[player]["mat"].size[1] -
						       self.mat[player]["field"][field][1] - self.field_btn[f"{field}{player}"].size[1] - sep)
					elif field == "Stock":
						pos = (self.mat[player]["mat"].x + self.mat[player]["mat"].size[0] - self.sd["card"][1] -
						       self.mat[player]["field"][field][0] + sep,
						       self.mat[player]["mat"].y + self.mat[player]["mat"].size[1] -
						       self.mat[player]["field"][field][
							       1] - self.sd["card"][0] - sep)

					elif field == "Climax" or field == "Memory":
						pos = (self.mat[player]["mat"].x + self.mat[player]["mat"].size[0] - self.sd["card"][1] -
						       self.mat[player]["field"][field][0] + sep,
						       self.mat[player]["mat"].y + self.mat[player]["mat"].size[1] - self.sd["card"][0] -
						       self.mat[player]["field"][field][1] - sep)
					elif field == "Clock":
						pos = (
							self.mat[player]["mat"].x + self.mat[player]["mat"].size[0] -
							self.mat[player]["field"][field][
								0] - self.field_btn[f"{field}{player}"].size[0],
							self.mat[player]["mat"].y + self.mat[player]["mat"].size[1] - self.sd["card"][1] -
							self.mat[player]["field"][field][1])
					elif field == "Res":
						pos = (
							self.mat[player]["mat"].x + self.mat[player]["mat"].size[0] -
							self.mat[player]["field"][field][
								0] - self.field_btn[f"{field}{player}"].size[0], self.mat[player]["mat"].y)

				self.field_btn[f"{field}{player}"].pos = pos

	def move_field_btn(self, p="", y=False):
		for fields in self.gd["select_btns"]:
			if "Clock" in fields:
				for ind in self.pd[fields[-1]]["Clock"]:
					self.cd[ind].selectable(False)
			elif not y and ("Stage" in self.gd["status"] or self.gd["move"]) and fields[:-1] in self.gd["stage"]:
				self.field_btn[f"{fields}s"].x = -Window.width * 3
			elif y and ("Stage" in self.gd["pay_status"] or self.gd["move"]) and fields[:-1] in self.gd["stage"]:
				self.field_btn[f"{fields}s"].x = -Window.width * 3
			else:
				if "Climax" in fields:
					self.cd[self.pd[fields[-1]][fields[:-1]][0]].selectable(False)
				else:
					self.cd[self.pd[fields[-1]][fields[:-2]][int(fields[-2])]].selectable(False)

		self.gd["select_btns"] = []
		self.gd["mstock"] = ""
		if (p == "Main" and self.gd["active"] == "1") or p == "restart":
			for field in self.gd["stage"]:
				self.field_btn[f"{field}1"].x = -Window.width
		else:
			for field in self.gd["stage"]:
				self.field_btn[f"{field}1"].x = self.mat["1"]["mat"].x + self.mat["1"]["field"][field][0]

	def enable_field_btn(self, b=True):
		for btn in self.field_btn:
			if b:
				self.field_btn[btn].disabled = False
			else:
				self.field_btn[btn].disabled = True

	def opp_play(self, dt=0):
		if len(self.gd["opp_play"]) > 0:
			play = self.gd["opp_play"].pop(0)
			if play[0] in self.pd[self.gd["active"]]["Hand"]:
				self.play(play)
		else:
			self.gd["opp_play"] = []
			move = self.ai.main_move(self.pd, self.cd)
			if move != "pass":
				self.gd["opp_move"] = list(move)

			if len(self.gd["opp_move"]) > 0:
				Clock.schedule_once(self.opp_move, move_dt_btw)
			else:
				Clock.schedule_once(self.end_current_phase)
			return False

	def opp_move(self, dt=0):
		if len(self.gd["opp_move"]) > 0:
			move = self.gd["opp_move"].pop(0)

			self.mat[move[0][-1]]["mat"].remove_widget(self.cd[move[0]])
			self.mat[move[0][-1]]["mat"].add_widget(self.cd[move[0]])

			old = self.cd[move[0]].pos_new

			if self.pd[move[0][-1]][move[1]][move[2]] != "":
				temp = self.pd[move[0][-1]][move[1]][move[2]]
				self.cd[temp].setPos(field=self.mat[temp[-1]]["field"][old], t=old)
				self.pd[move[0][-1]][old[:-1]][int(old[-1])] = temp
			else:
				self.pd[move[0][-1]][old[:-1]][int(old[-1])] = ""

			self.cd[move[0]].setPos(field=self.mat[move[0][-1]]["field"][f"{move[1]}{move[2]}"],
			                        t=f"{move[1]}{move[2]}")
			self.pd[move[0][-1]][move[1]][move[2]] = move[0]
			self.check_cont_ability()

			if self.net["game"] and self.gd["active"] == "2":
				if self.gd["show_wait_popup"]:
					Clock.schedule_once(partial(self.popup_text, "waiting"), move_dt_btw)
				self.mconnect("phase")
			else:
				Clock.schedule_once(self.opp_move, move_dt_btw)
		else:
			self.gd["opp_move"] = []
			Clock.schedule_once(self.end_current_phase)

	def main_phase(self, *args):
		self.dismiss_all()
		self.change_label()
		self.clear_ability()

		if self.gd["pp"] < 0:
			Clock.schedule_once(self.check_auto_ability)
			return False
		else:
			self.main_phase_main()

	def main_phase_main(self, *args):
		self.sd["btn"]["end"].text = "Climax Phase"  # f"End {self.gd["phase"]}"
		self.move_field_btn(self.gd["phase"])

		if self.gd["active"] == "1":
			self.hand_btn_show(False)
			self.sd["menu"]["btn"].disabled = False

		if self.net["game"] and self.gd["active"] == "1":
			self.net["send"] = False

		if self.net["game"] and self.gd["active"] == "2":
			if self.gd["show_wait_popup"]:
				Clock.schedule_once(partial(self.popup_text, "waiting"))
			self.mconnect("phase")
		elif self.gd["com"] and self.gd["active"] == "2":
			play = self.ai.main_play(self.pd, self.cd, self.gd)
			if play != "pass":
				self.gd["opp_play"] = list(play)
			Clock.schedule_once(self.opp_play, move_dt_btw)
		else:
			# self.sd["btn"]["end"] = Button(text=f"End {self.gd["phase"]}", on_release=self.end_current_phase)
			# self.sd["btn"]["end"].size = (self.sd["btn"]["end"].size[0], self.sd["b_bar"].size[1])
			self.sd["btn"]["end"].x = Window.width - self.sd["btn"]["end"].size[0]
			self.sd["btn"]["end"].y = 0
			self.sd["btn"]["end"].disabled = False

			self.sd["btn"]["end_attack"].x = Window.width - self.sd["btn"]["end"].size[0] - \
			                                 self.sd["btn"]["end_attack"].size[0]
			self.sd["btn"]["end_attack"].y = 0
			self.sd["btn"]["end_attack"].disabled = False

			self.sd["btn"]["end_phase"].x = Window.width - self.sd["btn"]["end"].size[0] - \
			                                self.sd["btn"]["end_attack"].size[0] - \
			                                self.sd["btn"]["end_phase"].size[0]
			self.sd["btn"]["end_phase"].y = 0
			self.sd["btn"]["end_phase"].disabled = False
			self.sd["btn"]["ablt_info"].y = -Window.height
			self.sd["btn"]["draw_upto"].y = -Window.height

			self.update_movable(self.gd["active"])

	# debug function
	def debug(self, instance, value):
		if value:
			self.debug_btn()
		else:
			for btn in self.sd["debug"]["btn"]:
				self.sd["debug"]["btn"][btn].y = -Window.height

	def debug_btn(self, dt=0):
		# debug button
		debug_btn_size = self.sd["card"][0] * 0.9

		self.gd["d_btn_list"] = ["3", "Draw_Me", "Draw_Opp", "Stock_Me", "Stock_Opp", "Damage_Me", "Damage_Opp",
		                         "Level_Me", "Level_Opp", "RRev_Me", "RRev_Opp", "Wall_Me", "Wall_Opp", "Mill_Me",
		                         "Mill_Opp", "RKill_Me", "RKill_Opp", "ULevel_Me", "ULevel_Opp"]
		self.gd["inx"] = 0

		for item in self.gd["d_btn_list"]:
			if len(item) == 1:
				self.sd["debug"]["btn"][f"d{item}"] = TextInput(text=item, input_filter="int")
			else:
				id = f"{item.split('_')[0][:2]}{item.split('_')[1][:1]}"
				if len(item) > 5:
					short = id
				else:
					short = item
				self.sd["debug"]["btn"][f"d{item}"] = Button(text=short, on_release=self.debug_effect, cid=id)

			if len(item) == 1:
				self.sd["debug"]["btn"][f"d{item}"].size = (debug_btn_size / 3. * 2, self.sd["b_bar"].size[1])
			else:
				self.sd["debug"]["btn"][f"d{item}"].size = (debug_btn_size, self.sd["b_bar"].size[1])

			if "Opp" in item:
				if len(item) == 1:
					self.sd["debug"]["btn"][f"d{item}"].x = self.sd["debug"]["btn"][f"d{item}"].size[0] * (
							self.gd["inx"] - 1)
				else:
					self.sd["debug"]["btn"][f"d{item}"].x = self.sd["debug"]["btn"][f"d{item}"].size[0] * (
							self.gd["inx"] - 1) - debug_btn_size / 3
				self.sd["debug"]["btn"][f"d{item}"].y = self.sd["debug"]["btn"][f"d{item}"].size[1]
			else:
				if len(item) == 1:
					self.sd["debug"]["btn"][f"d{item}"].x = self.sd["debug"]["btn"][f"d{item}"].size[0] * self.gd["inx"]
				else:
					self.sd["debug"]["btn"][f"d{item}"].x = self.sd["debug"]["btn"][f"d{item}"].size[0] * self.gd[
						"inx"] - debug_btn_size / 3
				self.sd["debug"]["btn"][f"d{item}"].y = 0
				self.gd["inx"] += 1
			self.sd["debug"]["btn"][f"d{item}"].disabled = False

			try:
				self.parent.add_widget(self.sd["debug"]["btn"][f"d{item}"])
			except WidgetException:
				pass

	def debug_rotation_btn(self, dt=0):
		# debug button
		debug_btn_size = self.sd["card"][0] * 0.85
		self.gd["d_btn_list"] = ["3", "L90", "R90", "L180", "R180", "C", "O", "A"]
		self.gd["inx"] = 0

		for item in self.gd["d_btn_list"]:
			if item.isdigit():
				self.sd["debug"]["btn"][f"d{item}"] = TextInput(text=item)
				self.sd["debug"]["btn"][f"d{item}"].size = (debug_btn_size, self.sd["b_bar"].size[1])
			else:
				self.sd["debug"]["btn"][f"d{item}"] = Button(on_release=self.gd["d_rotation"], cid=item, text=item)
				self.sd["debug"]["btn"][f"d{item}"].size = (debug_btn_size, self.sd["b_bar"].size[1])

			self.sd["debug"]["btn"][f"d{item}"].x = self.sd["debug"]["btn"][f"d{item}"].size[0] * self.gd["inx"]
			self.sd["debug"]["btn"][f"d{item}"].y = 0
			if item == "O":
				self.sd["debug"]["btn"][f"d{item}"].disabled = True

			try:
				self.parent.add_widget(self.sd["debug"]["btn"][f"d{item}"])
			except WidgetException:
				pass

			self.gd["inx"] += 1

	def debug_rotation(self, btn):
		if self.gd["last"] != "":
			card = self.cd[self.gd["last"]]
			self.sd["debug"]["btn"][f"d{'O'}"].text = str(card.rotation)
			rot = card.rotation
			n = 0

			if btn.cid == "A":
				self.sd["debug"]["btn"]["dA"].text = str(rot)
			elif btn.cid != "C":
				n = int(btn.cid[1:])
				if "L" in btn.cid:
					n = n * (-1)
				rot += n
				card.rot(rot)
				self.sd["debug"]["btn"]["dA"].text = str(rot)
			else:
				if "a" in self.sd["debug"]["btn"]["d3"].text:
					n = int(self.sd["debug"]["btn"]["d3"].text[1:])
					rot += n
				elif "s" in self.sd["debug"]["btn"]["d3"].text:
					n = int(self.sd["debug"]["btn"]["d3"].text[1:])
					rot -= n
				else:
					rot = int(self.sd["debug"]["btn"]["d3"].text)

				card.rot(rot)
				self.sd["debug"]["btn"]["dA"].text = str(rot)

	def debug_effect(self, btn):
		logging.warning(f'Pressed debug button:\t{btn.cid}')
		if self.gd["active"] == "1":
			self.gd["moveable"] = []
		if "M" in btn.cid[-1]:
			player = self.gd["active"]
		elif "O" in btn.cid[-1]:
			player = self.gd["opp"]

		if "Da" in btn.cid:
			if "O" in btn.cid[-1]:
				self.gd["rev"] = True
			self.gd["damage"] = int(self.sd["debug"]["btn"][f"d{self.gd['d_btn_list'][0]}"].text)
			self.gd["dmg"] = int(self.gd["damage"])
			Clock.schedule_once(self.damage, move_dt_btw)
		elif "Dr" in btn.cid:
			if "O" in btn.cid[-1]:
				self.gd["rev"] = True
			self.gd["draw"] = int(self.sd["debug"]["btn"][f"d{self.gd['d_btn_list'][0]}"].text)
			self.gd["ability_trigger"] = f"debug_{btn.cid}"
			Clock.schedule_once(self.draw, move_dt_btw)
		elif "St" in btn.cid:
			if "O" in btn.cid[-1]:
				self.gd["rev"] = True
			self.gd["stock"] = int(self.sd["debug"]["btn"][f"d{self.gd['d_btn_list'][0]}"].text)
			Clock.schedule_once(self.stock, move_dt_btw)
		elif "Le" in btn.cid:
			temp = self.pd[player]["Library"].pop(-1)
			self.pd[player]["Level"].append(temp)
			self.level_size(player)
			self.update_colour(player)
			self.check_cont_ability()
			if self.gd["active"] == "1":
				self.update_movable(self.gd["active"])
		elif "UL" in btn.cid:
			if len(self.pd[player]["Level"]) > 0:
				temp = self.pd[player]["Level"].pop(-1)
				self.cd[temp].setPos(field=self.mat[player]["field"]["Waiting"], t="Waiting")
				self.pd[player]["Waiting"].append(temp)
				self.update_field_label()
				self.level_size(player)
				self.update_colour(player)
				self.check_cont_ability()
			if self.gd["active"] == "1":
				self.update_movable(self.gd["active"])
		elif "Wa" in btn.cid:
			inxs = int(self.sd["debug"]["btn"][f"d{self.gd['d_btn_list'][0]}"].text)
			if inxs > 3:
				inxs = 3

			for inx in range(inxs):
				ind = ""
				a = 0
				pos = -1
				if len(self.pd[player]["Library"]) <= 1:
					continue
				for item in self.pd[player]["Library"]:
					if self.cd[item].card == "Character":
						ind = item
						break
				if ind != "":
					if self.pd[player]["Center"][inx] == "":
						pos = inx
					else:
						if inx != 2:
							a = 1
						else:
							continue

						if self.pd[player]["Center"][inx + a] == "":
							pos = inx + a
						else:
							if inx != 2:
								a = 1
							else:
								continue
							if self.pd[player]["Center"][inx + a] == "":
								pos = inx + a

					if pos >= 0:
						self.pd[player]["Library"].remove(ind)
						self.cd[ind].setPos(field=self.mat[ind[-1]]["field"][f"Center{pos}"], t=f"Center{pos}")
						self.pd[player]["Center"][pos] = ind
						self.update_field_label()
			if self.gd["active"] == "1":
				self.update_movable(self.gd["active"])
		elif "Mi" in btn.cid:
			for mill in range(int(self.sd["debug"]["btn"][f"d{self.gd['d_btn_list'][0]}"].text)):
				if len(self.pd[player]["Library"]) >= 1:
					temp = self.pd[player]["Library"].pop(-1)
					self.mat[player]["mat"].remove_widget(self.cd[temp])
					self.mat[player]["mat"].add_widget(self.cd[temp])

					self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Waiting"], t="Waiting")
					self.pd[player]["Waiting"].append(temp)
					self.update_field_label()
			if self.gd["active"] == "1":
				self.update_movable(self.gd["active"])
		elif "RR" in btn.cid:
			inds = [s for s in self.pd[player]["Center"] + self.pd[player]["Back"] if
			        s != "" and self.cd[s].status != "Reverse"]
			if len(inds) > 0:
				ind = choice(inds)
				card = self.cd[ind]
				if card.status != "Reverse":
					card.reverse()
					self.check_auto_ability(rev=(card.ind,))
		elif "RK" in btn.cid:
			inds = [s for s in self.pd[player]["Center"] + self.pd[player]["Back"] if s != ""]
			if len(inds) > 0:
				ind = choice(inds)
				self.send_to_waiting(ind)
				self.stack_ability()

	def update_movable(self, player):
		self.sd["menu"]["btn"].disabled = False
		self.gd["moveable"] = []
		for field in self.gd["fields"]:
			for ind in self.pd[player][field]:
				if ind in self.emptycards:
					continue
				aa = True
				for item in self.cd[ind].text_c:
					if item[0].startswith(cont_ability) and item[1] != 0 and item[1] > -9:
						eff = ab.cont(item[0])
						if "no_move" in eff:
							aa = False
							break
				if aa:
					self.gd["moveable"].append(ind)
		self.act_ability_show()

	def update_playable_climax(self, player):
		self.gd["moveable"] = []
		self.gd["playable_climax"] = []
		for ind in self.pd[self.gd["active"]]["Hand"]:
			self.gd["moveable"].append(ind)
			# add colour req
			if self.cd[ind].card == "Climax" and self.cd[ind].mcolour in self.pd[self.gd["active"]]["colour"]:
				self.gd["playable_climax"].append(ind)
		if len(self.gd["playable_climax"]) > 1:
			self.sd["btn"]["end"].disabled = False

	def end_effect(self, *args):
		self.sd["popup"]["popup"].dismiss()
		if self.gd["confirm_pop"]:
			self.gd["confirm_pop"] = False
		self.popup_clr()
		if self.gd["ability_doing"] in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove(self.gd["ability_doing"])
		self.gd["encore_ind"] = ""
		self.gd["p_c"] = ""
		self.gd["encore_type"] = ""

		# if self.net["game"]:
		# 	self.net["send"] = False
		# 	self.net["act"][4].append(str(btn.cid))

		self.ability_effect()

	def end_current_ability(self, *args):
		self.gd["end_stage"] = True
		self.move_field_btn(self.gd["phase"])
		self.sd["btn"]["end"].y = -Window.height * 2
		self.sd["btn"]["end"].x = Window.width - self.sd["btn"]["end"].size[0]
		self.sd["btn"]["end_eff"].y = -Window.height * 2
		for player in list(self.pd.keys()):
			for r in range(select2cards):
				self.field_btn[f"stage{r}{player}s"].pos = (-Window.width * 2, -Window.height * 2)

		if "salvage" in self.gd["ability_doing"]:
			Clock.schedule_once(self.salvage)
		elif self.gd["ability_doing"] in (
		"give", "power", "trait", "soul", "hander", "waitinger", "clocker", "memorier"):
			if len(self.gd["chosen"]) < self.gd["effect"][0]:
				for r in range(self.gd["effect"][0] - len(self.gd["chosen"])):
					self.gd["chosen"].append("")
			for ind in self.gd["chosen"]:
				self.gd["target"].append(ind)
				if ind != "":
					self.cd[ind].update_text()
			if "give" in self.gd["ability_doing"]:
				Clock.schedule_once(self.give)
			elif "power" in self.gd["ability_doing"]:
				Clock.schedule_once(self.power)
			elif "trait" in self.gd["ability_doing"]:
				Clock.schedule_once(self.trait)
			elif "soul" in self.gd["ability_doing"]:
				Clock.schedule_once(self.soul)
			elif "level" in self.gd["ability_doing"]:
				Clock.schedule_once(self.level)
			elif "hander" in self.gd["ability_doing"]:
				Clock.schedule_once(self.wind)
			elif "waitinger" in self.gd["ability_doing"]:
				Clock.schedule_once(self.waitinger)
			elif "clocker" in self.gd["ability_doing"]:
				Clock.schedule_once(self.clocker)
			elif "memorier" in self.gd["ability_doing"]:
				Clock.schedule_once(self.memorier)

	def end_current_phase(self, *args):
		if "Effect" in self.sd["btn"]["end"].text or "Reveal" in self.sd["btn"]["end"].text or "Heal" in self.sd["btn"][
			"end"].text or "Stock" in self.sd["btn"]["end"].text:
			if self.gd["ability_doing"] in self.gd["ability_effect"]:
				if self.gd["ability_doing"] == "drawupto":
					self.sd["btn"]["ablt_info"].y = -Window.height * 2
					self.sd["btn"]["draw_upto"].y = -Window.height * 2
					self.gd["draw_upto"] = 0
				if "heal" in self.gd["ability_doing"] and "Clock" in self.gd["status"]:
					self.gd["move"] = "none"
				elif "search" in self.gd["ability_doing"] and "Stage" in self.gd["status"]:
					self.gd["move"] = "none"
				elif "move" in self.gd["ability_doing"]:
					self.gd["move"] = "none"
				else:
					if self.gd["ability_doing"] in ("give", "power", "level", "trait", "soul") and len(
							self.gd["chosen"]) > 0:
						for ind in self.gd["chosen"]:
							self.cd[ind].update_text()
						self.gd["chosen"] = []
					self.gd["ability_effect"].remove(self.gd["ability_doing"])
			self.move_field_btn(self.gd["phase"])
			if "Reveal" in self.gd["effect"] and "if" in self.gd["effect"]:
				if len(self.pd[self.gd["ability_trigger"].split("_")[1][-1]]["Res"]) >= self.gd["effect"][
					self.gd["effect"].index("if") + 1]:
					self.gd["done"] = True
			elif "if" in self.gd["effect"]:
				self.gd["done"] = False
			elif "do" in self.gd["effect"]:
				self.gd["done"] = True
			if "do" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("do")
			for player in list(self.pd.keys()):
				for r in range(select2cards):
					self.field_btn[f"stage{r}{player}s"].pos = (-Window.width * 2, -Window.height * 2)
			self.sd["btn"]["end"].y = -Window.height * 2
			self.sd["btn"]["end"].disabled = True
			if self.gd["phase"] == "Main":
				self.sd["btn"]["end"].text = "Climax\nPhase"
			else:
				self.sd["btn"]["end"].text = f"End {self.gd['phase']}"
			self.sd["btn"]["end"].x = Window.width - self.sd["btn"]["end"].size[0]
			self.sd["btn"]["end_eff"].y = -Window.height * 2
			self.ability_effect()
		elif self.gd["phase"] == "Clock":
			self.pd[self.gd["active"]]["done"]["Clock"] = True
			self.sd["btn"]["end"].disabled = True
			self.gd["phase"] = "Main"
			Clock.schedule_once(self.main_phase)
		elif self.gd["phase"] == "Main":
			self.pd[self.gd["active"]]["done"]["Main"] = True
			self.sd["btn"]["end_attack"].disabled = True
			self.sd["btn"]["end_phase"].disabled = True
			self.sd["btn"]["end"].disabled = True
			self.gd["phase"] = "Climax"
			Clock.schedule_once(self.climax_phase, move_dt_btw)
		elif self.gd["phase"] == "Climax":
			if self.net["game"] and self.gd["active"] == "1":
				self.net["var"] = ["x"]
				self.net["var1"] = "end current"
				self.mconnect("phase")
			else:
				self.pd[self.gd["active"]]["done"]["Climax"] = True
				self.sd["btn"]["end"].disabled = True
				self.gd["phase"] = "Attack"
				Clock.schedule_once(self.attack_phase, move_dt_btw)
		elif (self.gd["phase"] == "Attack" or self.gd["phase"] == "Declaration") and "AUTO" in self.gd[
			"ability_trigger"]:
			self.pd[self.gd["active"]]["done"]["Attack"] = True
			self.sd["btn"]["end"].disabled = True
			self.gd["phase"] = "Trigger"
			Clock.schedule_once(self.trigger_step, move_dt_btw)
		elif self.gd["phase"] == "Attack" or self.gd["phase"] == "Declaration":
			self.sd["btn"]["end"].disabled = True
			self.gd["attack"] = 0
			if self.gd["turn"] == 1:
				self.gd["d_atk"] = [0, []]
			if self.net["game"] and self.gd["active"] == "1":
				self.net["var"] = ["x"]
				self.net["var1"] = "end current"
				self.mconnect("phase")
			else:
				Clock.schedule_once(self.attack_phase_end)
		elif self.gd["phase"] == "Encore":
			self.skip_encore()
			if self.net["game"] and (self.gd["active"] == "1" or (self.gd["rev"] and self.gd["active"] == "2")):
				self.net["var"] = ["ke"]
				self.net["var1"] = "skip_encore"
				self.mconnect("phase")
			else:
				Clock.schedule_once(self.encore_start)

	# self.pd[self.gd["active"]]["done"]["Encore"] = True
	# self.sd["btn"]["end"].disabled = True
	# self.gd["phase"] = "End"
	# Clock.schedule_once(self.end_phase, move_dt_btw)

	def skip_encore(self,*args):
		self.gd["nomay"] = True
		self.move_field_btn(self.gd["phase"])
		for cind in self.gd["encore"]["1"]:
			self.gd["no_cont_check"] = True
			self.cd[cind].selected(False)
			self.send_to_waiting(cind)
		self.check_cont_ability()
		self.gd["nomay"] = False

	def end_to_attack(self, *args):
		self.sd["btn"]["end"].disabled = True
		self.sd["btn"]["end"].y = -Window.height
		self.sd["btn"]["end_attack"].disabled = True
		self.sd["btn"]["end_attack"].y = -Window.height
		self.sd["btn"]["end_phase"].disabled = True
		self.sd["btn"]["end_phase"].y = -Window.height
		self.sd["btn"]["ablt_info"].y = -Window.height
		self.sd["btn"]["draw_upto"].y = -Window.height
		self.pd[self.gd["active"]]["done"]["Main"] = True
		self.gd["phase"] = "Climax"
		self.gd["skip"].append("Climax")
		self.gd["nomay"] = True
		if self.net["game"] and self.gd["active"] == "1":
			self.net["var"] = ["kc"]
			self.net["var1"] = "skip_climax"
			self.mconnect("phase")
		else:
			Clock.schedule_once(self.climax_phase)

	def end_to_end(self, *args):
		self.sd["btn"]["end"].disabled = True
		self.sd["btn"]["end"].y = -Window.height
		self.sd["btn"]["end_attack"].disabled = True
		self.sd["btn"]["end_attack"].y = -Window.height
		self.sd["btn"]["end_phase"].disabled = True
		self.sd["btn"]["end_phase"].y = -Window.height
		self.sd["btn"]["ablt_info"].y = -Window.height
		self.sd["btn"]["draw_upto"].y = -Window.height
		self.pd[self.gd["active"]]["done"]["Main"] = True
		self.gd["phase"] = "Climax"
		self.gd["skip"].append("Climax")
		self.gd["skip"].append("Attack")
		self.gd["nomay"] = True
		if self.net["game"] and self.gd["active"] == "1":
			self.net["var"] = ["kca"]
			self.net["var1"] = "skip_climax_attack"
			self.mconnect("phase")
		else:
			Clock.schedule_once(self.climax_phase)

	def create_field_label(self):
		for player in list(self.pd.keys()):
			for field in self.labelfield:
				self.field_label[f"{field}{player}"] = Label(text="50", halign="center",
				                                             font_size=self.sd["card"][1] / 4,
				                                             text_size=self.sd["card"], color=(1, 1, 1, 1),
				                                             outline_width=2, size_hint=(None, None),
				                                             pos_hint=(None, None), size=self.sd["card"],
				                                             pos=(-Window.width * 2, 0))
				self.parent.add_widget(self.field_label[f"{field}{player}"])
				self.field_label[f"{field}{player}"].texture_update()
				self.field_label[f"{field}{player}"].size = self.field_label[f"{field}{player}"].texture.size
				if field == "Stock":
					if player == "1":
						self.field_label[f"{field}{player}"].halign = "right"
					else:
						self.field_label[f"{field}{player}"].halign = "left"
		# yp = (self.sd["card"][1] - text_size) / 2.
		# if field == "Memory" or field == "Stock":
		# 	yp = self.sd["card"][0] / 2. + text_size / 4.

	def add_field_label(self, *args):
		for player in list(self.pd.keys()):
			for field in self.labelfield:
				self.field_label[f"{field}{player}"].center = self.field_btn[f"{field}{player}"].center
				# self.field_label[f"{field}{player}"].x = self.field_btn[f"{field}{player}"].center_x - Window.width
				# self.field_label[f"{field}{player}"].y = self.field_btn[f"{field}{player}"].center_y + yp
				self.field_label[f"{field}{player}"].y += self.sd["card"][0] / 2
				self.field_label[f"{field}{player}"].x -= Window.width

	def show_field_label(self, field):
		self.update_field_label()
		if field[:-1] in self.labelfield:
			if self.field_label[field].x >= 0:
				self.field_label[field].x -= Window.width
			else:
				self.field_label[field].x += Window.width

	def update_field_label(self, *args):
		for player in list(self.pd.keys()):
			for label in self.labelfield:
				self.field_label[f"{label}{player}"].text = str(len(self.pd[player][label]))

	def shuffle(self, player, *args):
		if player == "0":
			for player in list(self.pd.keys()):
				for n in range(shuffle_n * 1):
					shuffle(self.pd[player]["Library"])
				self.gd["shuffle"].append(player)
		else:
			for n in range(shuffle_n * 1):
				shuffle(self.pd[player]["Library"])
			self.gd["shuffle"].append(player)

		Clock.schedule_once(self.shuffle_animation, shuffle_dt * shuffle_n)

	# self.shuffle_event = Clock.schedule_once(self.shuffle_animation, shuffle_dt * shuffle_n)

	def shuffle_animation(self, dt=0):
		if self.gd["shuffle_rep"] > 0:
			for player in self.gd["shuffle"]:
				library = self.mat[player]["field"]["Library"]
				card = self.pd[player]["Library"]

				if len(library) > 0:
					def front(*args):
						f = self.cd[self.pd[player]["Library"][0]]

						self.mat[player]["mat"].remove_widget(f)
						self.mat[player]["mat"].add_widget(f)

					def top(*args):
						t = self.cd[self.pd[player]["Library"][-1]]
						self.mat[player]["mat"].remove_widget(t)
						self.mat[player]["mat"].add_widget(t)

					a1 = Animation(x=library[0], y=library[1] - self.sd["card"][1], d=shuffle_dt)
					a2 = Animation(x=library[0], y=library[1], d=shuffle_dt)
					a1.bind(on_complete=front)
					a2.bind(on_complete=top)

					animation = a1 + a2
					animation.start(self.cd[card[0]])

			self.gd["shuffle_rep"] -= 1
			# self.shuffle_event = Clock.schedule_once(self.shuffle_animation, shuffle_dt * shuffle_n)
			Clock.schedule_once(self.shuffle_animation, shuffle_dt * shuffle_n)
		else:
			# self.shuffle_event.cancel()
			if len(self.gd["shuffle"]) > 0 and self.net["game"]:
				if "1" in self.gd["shuffle"]:
					self.gd["shuffle"].remove("1")
					self.stack("1")
					self.mconnect("shuffleplr")
				elif "2" in self.gd["shuffle"]:
					self.gd["shuffle"].remove("2")
					if self.gd["show_wait_popup"]:
						Clock.schedule_once(partial(self.popup_text, "waiting"))
					self.mconnect("shuffleopp")
			else:
				self.gd["shuffle_rep"] = shuffle_n

				if not self.net["game"]:
					for player in self.gd["shuffle"]:
						self.stack(player)
					self.gd["shuffle"] = []

				if self.gd["shuffle_trigger"] == "refresh":
					self.gd["shuffle_trigger"] = ""
					Clock.schedule_once(self.refresh)
				elif self.gd["shuffle_trigger"] == "turn0" and self.gd["turn"] == 0:
					self.gd["shuffle_trigger"] = ""
					for player in list(self.pd.keys()):
						self.pd[player]["phase"][self.gd["phase"]] = True
					self.gd["phase"] = "Janken"
					Clock.schedule_once(self.janken_start, move_dt_btw)
				elif self.gd["shuffle_trigger"] == "ability":
					self.gd["shuffle_trigger"] = ""
					if self.gd["pay"] and not self.gd["payed"]:
						Clock.schedule_once(self.pay_condition, move_dt_btw)
					else:
						Clock.schedule_once(self.ability_effect)
				elif self.gd["shuffle_trigger"] == "looktop":
					self.gd["shuffle_trigger"] = ""
					Clock.schedule_once(self.look_top_done)

	def draw_both(self, dt=0):
		if self.gd["draw_both"][0] > 0:
			self.gd["draw"] = self.gd["draw_both"][0]
			if not self.gd["draw_both"][1]:
				Clock.schedule_once(self.draw, move_dt_btw)
			elif not self.gd["draw_both"][2]:
				self.gd["rev"] = True
				Clock.schedule_once(self.draw, move_dt_btw)
			if self.gd["draw_both"][1] and self.gd["draw_both"][2]:
				self.gd["draw_both"][0] = 0
				self.draw_both()
		# for player in list(self.pd.keys()):
		# 	temp = self.pd[player]["Library"].pop()
		# 	self.pd[player]["Hand"].append(temp)
		# 	self.hand_size(player)
		# self.gd["draw_both"][0] -= 1
		# self.update_field_label()
		# Clock.schedule_once(self.draw_both, move_dt_btw)
		else:
			if self.gd["phase"] == "Janken":
				self.gd["draw_both"] = [starting_hand, False, False]
				self.gd["phase"] = "Mulligan"
				Clock.schedule_once(self.mulligan_start)  # , phase_dt)

	def mulligan_start(self, *args):
		if self.gd["rev"]:
			player = self.gd["opp"]
		else:
			player = self.gd["active"]

		self.pd[player]["phase"]["Mulligan"] = True

		if self.net["game"] and player == "2":
			self.gd["rev"] = True
			Clock.schedule_once(self.mulligan_start)
		elif self.gd["com"] and player == "2":
			self.gd["chosen"] = self.ai.mulligan(self.pd, self.cd)
			self.gd["p_owner"] = player
			# self.gd["trev"] = player
			self.mulligan_done()
		else:
			self.sd["popup"]["popup"].title = self.gd["phase"]
			self.gd["uptomay"] = True
			self.popup_start(o=player, c="Mulligan", m=starting_hand)

	def hand_waiting(self, dt=0, chosen=[]):
		for ind in chosen:
			if ind in self.emptycards:
				continue
			self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
			self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])
			if "Hand" in self.cd[ind].pos_new:
				if "Mulligan" not in self.gd["phase"]:
					self.check_auto_ability(dis=ind, stacks=False)
				self.pd[ind[-1]]["Hand"].remove(ind)
				self.hand_size(ind[-1])
			elif "Clock" in self.cd[ind].pos_new:
				self.pd[ind[-1]]["Clock"].remove(ind)
				self.clock_size(ind[-1])
			elif "Memory" in self.cd[ind].pos_new:
				self.pd[ind[-1]]["Memory"].remove(ind)
			self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Waiting"], t="Waiting")
			self.pd[ind[-1]]["Waiting"].append(ind)
			self.update_field_label()

	def hand_clock(self, ind, *args):
		self.pd[ind[-1]]["Hand"].remove(ind)
		self.pd[ind[-1]]["Clock"].append(ind)

		self.clock_size(ind[-1])
		self.hand_size(ind[-1])
		self.check_cont_ability()

	def mulligan_all(self, bt):
		self.gd["chosen"] = []
		for ind in self.pd[self.gd["p_owner"]]["Hand"]:
			self.gd["chosen"].append(ind)
			self.cpop[ind].update_text()
		self.mulligan_done()

	def mulligan_done(self, *args):
		self.sd["popup"]["popup"].dismiss()
		if self.net["game"] and self.gd["p_owner"] == "1":
			self.gd["mulligan"][0] = self.gd["chosen"]

		self.hand_waiting(chosen=self.gd["chosen"])

		self.gd["draw"] = len(self.gd["chosen"])
		self.popup_clr()
		self.hand_btn_show(False)
		Clock.schedule_once(self.draw, move_dt_btw)

	def rescue(self, *args):
		temp = self.gd["effect"][self.gd["effect"].index("rescue") + 1]
		if "Waiting" in self.cd[temp[0]].pos_new:
			if "Hand" in temp:
				self.pd[temp[0][-1]]["Waiting"].remove(temp[0])
				self.pd[temp[0][-1]]["Hand"].append(temp[0])
				self.hand_size(temp[0][-1])
				self.update_field_label()
				self.check_cont_ability()

		if "rescue" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("rescue")
		self.ability_effect()

	def stocker(self, *args):
		ind = self.gd["ability_trigger"].split("_")[-1]

		if self.gd["effect"][0] == 0:
			if ind[-1] == "1":
				self.gd["target"].append(ind)
			self.gd["effect"][0] = 1
		elif self.gd["effect"][0] == -3:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(self.gd["effect"][self.gd["effect"].index("target") + 1])
			self.gd["effect"][0] = 1
		elif self.gd["effect"][0] == -15:
			if "Opp" in self.gd["effect"] and ind[-1] == "1":
				op = "2"
			elif "Opp" in self.gd["effect"] and ind[-1] == "2":
				op = "1"
			else:
				op = ind[-1]
			fop = []
			if "Level" in self.gd["effect"]:
				lvl = self.gd["effect"][self.gd["effect"].index("Level") + 1]
				if "<=" in lvl:
					fop = [o for o in self.pd[op]["Center"] if self.cd[o].level <= int(lvl[-1])]
			if ind[-1] == "1":
				for ond in fop:
					self.gd["target"].append(ond)
			self.gd["effect"][0] = len(fop)

		lif = []
		for r in range(self.gd["effect"][0]):
			temp = self.gd["target"].pop(0)
			if self.net["game"] and ind[-1] == "1":
				self.net["act"][4].append(temp)
			if temp == "":
				self.gd["notarget"] = True
				continue
			if "if" in self.gd["effect"]:
				lif.append(temp)
			self.send_to_stock(temp)

		if self.gd["notarget"]:
			self.gd["notarget"] = False

		if "stocker" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("stocker")

		if "if" in self.gd["effect"]:
			if len(lif) >= self.gd["effect"][self.gd["effect"].index("if") + 1]:
				self.gd["done"] = True
		elif "do" in self.gd["effect"] and self.gd["do"][0] > 0:
			self.gd["done"] = True

		if "do" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("do")

		self.ability_effect()

	def clock_to_level(self, ind):
		self.pd[ind[-1]]["Clock"].remove(ind)
		self.pd[ind[-1]]["Level"].append(ind)
		self.level_size(ind[-1])
		self.gd["levelup"][ind[-1]] = True
		self.check_auto_ability(lvup=ind[-1], stacks=False)

	def clocker(self, *args):
		ind = self.gd["ability_trigger"].split("_")[1]
		if not self.gd["clocker"]:
			self.gd["clocker"] = True
			if self.gd["effect"][0] == 0:  # and not self.gd["target"]:
				if ind[-1] == "1":
					self.gd["target"].append(ind)
				self.gd["effect"][0] = 1
			elif self.gd["effect"][0] == -3:
				if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
					self.gd["target"].append(self.gd["effect"][self.gd["effect"].index("target") + 1])
				self.gd["effect"][0] = 1

		if len(self.gd["target"]) > 0 and self.gd["clocker"]:
			player = ""
			for r in range(self.gd["effect"][0]):
				temp = self.gd["target"].pop(0)
				if self.net["game"] and ind[-1] == "1":
					self.net["act"][4].append(temp)
				if temp == "":
					self.gd["notarget"] = True
					continue
				player = temp[-1]
				if "Res" in self.cd[temp].pos_new:
					self.pd[temp[-1]]["Res"].remove(temp)
					self.pd[temp[-1]]["Clock"].append(temp)
					self.clock_size(temp[-1])
					self.check_cont_ability()
				else:
					self.send_to_clock(temp)

				if not self.gd["both"] and self.check_lose():
					return False

				if self.gd["both"]:
					self.gd["both"] = False

				if player and len(self.pd[player]["Clock"]) >= 7:
					if player == "2" and ind[-1] != player:
						self.gd["clocker_rev"] = True
					self.popup_clr()
					self.gd["level_up_trigger"] = "clocker"
					Clock.schedule_once(self.level_up)
					return False

		if self.gd["notarget"]:
			self.gd["notarget"] = False

		if "clocker" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("clocker")
			self.gd["choose"] = False

		if self.gd["clocker"]:
			self.gd["clocker"] = False

		self.ability_effect()

	def decker(self, *args):
		ind = self.gd["ability_trigger"].split("_")[1]
		ss = True
		if "Opp" in self.gd["effect"] and ind[-1] == "1":
			player = "2"
		elif "Opp" in self.gd["effect"] and ind[-1] == "2":
			player = "1"
		else:
			player = ind[-1]

		if self.gd["effect"][0] == 0:
			if ind[-1] == "1":
				self.gd["target"].append(ind)
			self.gd["effect"][0] = 1
		elif self.gd["effect"][0] == -1:
			if ind[-1] == "1":
				self.gd["target"].append("all")
			self.gd["effect"][0] = 1
		elif self.gd["effect"][0] == -3:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(self.gd["effect"][self.gd["effect"].index("target") + 1])
			self.gd["effect"][0] = 1
			ss = False
		# elif self.gd["effect"][0] == -13:
		# 	# if ind[-1] == "1":
		# 	self.gd["target"].append(self.gd["effect"][self.gd["effect"].index("decker") + 1])
		# 	self.gd["effect"][0] = 1
		# 	ss = False
		elif self.gd["effect"][0] == -20:
			self.gd["effect"][0] = len(self.gd["extra1"])
			for r in range(len(self.gd["extra1"])):
				ex = self.gd["extra1"].pop(0)
				if ind[-1] == "1":
					self.gd["target"].append(ex)

		deck = ""
		for r in range(self.gd["effect"][0]):
			temp = self.gd["target"].pop(0)
			if self.net["game"] and ind[-1] == "1" and ss:
				self.net["act"][4].append(temp)
			if temp == "":
				self.gd["notarget"] = True
				continue
			if "extra" in self.gd["effect"]:
				self.gd["extra"].append(temp)
			if "save_name" in self.gd["effect"]:
				self.gd["save_name"] = self.cd[temp].name
			if temp == "all":
				self.send_to_deck(all=True)
			else:
				if "bottom" in self.gd["effect"]:
					self.send_to_deck(temp, pos="bottom")
				else:
					self.send_to_deck(temp)
					deck = temp

		if self.gd["notarget"]:
			self.gd["notarget"] = False

		if "decker" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("decker")
			self.gd["choose"] = False

		if "do" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("do")

		if "if" in self.gd["effect"]:
			if deck:
				self.gd["done"] = True
		elif "do" in self.gd["effect"] and self.gd["do"][0] > 0:
			self.gd["done"] = True

		if self.gd["decker"] and not ("bottom" in self.gd["effect"] or "top" in self.gd["effect"]):
			self.gd["shuffle_trigger"] = "ability"
			self.shuffle(player)
		else:
			self.ability_effect()

	def waitinger(self, *args):
		ind = self.gd["ability_trigger"].split("_")[1]
		if "Opp" in self.gd["effect"] and ind[-1] == "1":
			player = "2"
		elif "Opp" in self.gd["effect"] and ind[-1] == "2":
			player = "1"
		else:
			player = ind[-1]

		if self.gd["effect"][0] == 0:
			if ind[-1] == "1":
				self.gd["target"].append(ind)
			self.gd["effect"][0] = 1
		elif self.gd["effect"][0] == -1:
			if ind[-1] == "1":
				self.gd["status"] = self.add_to_status("", self.gd["effect"])
				for rr in self.select_card(filter=True):
					self.gd["target"].append(rr)
				self.gd["status"] = ""
			self.gd["effect"][0] = len(self.gd["target"])
		elif self.gd["effect"][0] == -3:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(self.gd["effect"][self.gd["effect"].index("target") + 1])
			self.gd["effect"][0] = 1
		# elif self.gd["effect"][0] == -13:
		# 	if ind[-1] == "1":
		# 		self.gd["target"].append(self.gd["effect"][self.gd["effect"].index("decker") + 1])
		# 	self.gd["effect"][0] = 1

		wait = []
		for r in range(self.gd["effect"][0]):
			temp = self.gd["target"].pop(0)
			if self.net["game"] and ind[-1] == "1":
				self.net["act"][4].append(temp)
			if temp == "":
				self.gd["notarget"] = True
				continue
			if "extra" in self.gd["effect"]:
				self.gd["extra"].append(temp)
			if "if" in self.gd["effect"]:
				wait.append(temp)
			self.send_to_waiting(temp)

		if self.gd["notarget"]:
			self.gd["notarget"] = False

		if "waitinger" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("waitinger")
			self.gd["choose"] = False

		if "do" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("do")

		if "if" in self.gd["effect"]:
			if wait:
				self.gd["done"] = True
		elif "do" in self.gd["effect"] and self.gd["do"][0] > 0:
			self.gd["done"] = True

		if self.gd["pay"] and not self.gd["payed"]:
			self.pay_condition()
		else:
			self.ability_effect()

	def memorier(self, *args):
		ind = self.gd["ability_trigger"].split("_")[1]
		if ("Opp" in self.gd["effect"] or "opp" in self.gd["effect"]) and ind[-1] == "1":
			pl = "2"
		elif ("Opp" in self.gd["effect"] or "opp" in self.gd["effect"]) and ind[-1] == "2":
			pl = "1"
		else:
			pl = ind[-1]

		if self.gd["effect"][0] == 0:
			if ind[-1] == "1":
				self.gd["target"].append(ind)
			self.gd["effect"][0] = 1
		elif self.gd["effect"][0] == -1:
			if ind[-1] == "1":
				for rr in self.cont_cards(self.gd["effect"],ind):
					self.gd["target"].append(rr)
			self.gd["effect"][0]=len(self.gd["target"])
		elif self.gd["effect"][0] == -3:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(self.gd["effect"][self.gd["effect"].index("target") + 1])
			self.gd["effect"][0] = 1

		if "this" in self.gd["effect"] and self.gd["effect"][0] > 0:
			if ind[-1] == "1":
				self.gd["target"].append(ind)
			self.gd["effect"][0] += 1

		if self.net["game"] and pl!=ind[-1]:
			for rr in range(len(self.gd["target"])):
				if self.gd["target"][rr][-1] == ind[-1]:
					self.gd["target"][rr] = f"{self.gd['target'][rr][:-1]}{pl}"

		# elif "top-down" in self.gd["effect"] and self.gd["effect"][0] > 0:
		# 	if "Library" in self.gd["effect"]:
		# 		if len(self.pd[ind[-1]]["Library"])<self.gd["effect"][0]:
		# 			self.gd["effect"][0] =len(self.pd[ind[-1]]["Library"])
		# 		if ind[-1] == "1":
		# 			for rr in range(self.gd["effect"][0]):
		# 				self.gd["target"].append(self.pd[ind[-1]]["Library"][-(1 + rr)])

		lif = []
		for r in range(self.gd["effect"][0]):
			temp = self.gd["target"].pop(0)
			if self.net["game"] and ind[-1] == "1":
				self.net["act"][4].append(temp)
			if temp == "":
				self.gd["notarget"] = True
				continue
			if "if" in self.gd["effect"]:
				lif.append(ind)
			if "extra" in self.gd["effect"]:
				self.gd["extra"].append(temp)
			self.send_to_memory(temp)

		if self.gd["notarget"]:
			self.gd["notarget"] = False

		if "memorier" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("memorier")
			self.gd["choose"] = False

		if "if" in self.gd["effect"]:
			if lif:
				self.gd["done"] = True
			else:
				if "extra" in self.gd["effect"]:
					self.gd["extra"] = []
		elif "do" in self.gd["effect"] and self.gd["do"][0] > 0:
			self.gd["done"] = True

		if "do" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("do")

		self.ability_effect()

	def wind(self, *args):
		ind = self.gd["ability_trigger"].split("_")[1]
		if self.gd["effect"][0] == 0:
			if ind[-1] == "1":
				self.gd["target"].append(ind)
			self.gd["effect"][0] = 1
		elif self.gd["effect"][0] == -1:
			if ind[-1] == "1":
				self.gd["status"] = self.add_to_status("", self.gd["effect"])
				for rr in self.select_card(filter=True):
					self.gd["target"].append(rr)
				self.gd["status"] = ""
			self.gd["effect"][0] = len(self.gd["target"])

		if "this" in self.gd["effect"] and self.gd["effect"][0] > 0:
			if ind[-1] == "1":
				self.gd["target"].append(ind)
			self.gd["effect"][0] += 1

		if len(self.gd["target"]) < self.gd["effect"][0]:
			for r in range(self.gd["effect"][0] - len(self.gd["target"])):
				self.gd["target"].append("")

		retr = []
		for r in range(self.gd["effect"][0]):
			temp = self.gd["target"].pop(0)
			if self.net["game"] and ind[-1] == "1":
				self.net["act"][4].append(temp)
			if temp == "":
				self.gd["notarget"] = True
				continue
			self.send_to_hand(temp)
			retr.append(temp)

		if "wind" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("wind")
			self.gd["choose"] = False

		if "hander" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("hander")
			self.gd["choose"] = False

		if "if" in self.gd["effect"] and "do" in self.gd["ability_effect"]:
			if len(retr) >= self.gd["effect"][self.gd["effect"].index("if") + 1]:
				self.gd["done"] = True
		elif "do" in self.gd["ability_effect"] and not self.gd["notarget"]:
			self.gd["done"] = True

		if "do" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("do")

		if self.gd["notarget"]:
			self.gd["notarget"] = False

		self.ability_effect()

	def play_to_stage(self, ind, st, *args):
		old = str(self.cd[ind].pos_new)
		if "Library" in old:
			self.pd[ind[-1]]["Library"].remove(ind)
		elif "Clock" in old:
			self.pd[ind[-1]]["Clock"].remove(ind)
			self.clock_size(ind[-1])
		elif "Waiting" in old:
			self.pd[ind[-1]]["Waiting"].remove(ind)
		elif "Memory" in old:
			self.pd[ind[-1]]["Memory"].remove(ind)
			self.cd[ind].stand()
		elif "Hand" in old:
			self.pd[ind[-1]]["Hand"].remove(ind)
			self.hand_size(ind[-1])

		self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
		self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])

		if "Center" in st or "Back" in st:
			if self.pd[ind[-1]][st[:-1]][int(st[-1])] != "":
				temp = self.pd[ind[-1]][st[:-1]][int(st[-1])]
				self.send_to_waiting(temp)
			self.cd[ind].setPos(field=self.mat[ind[-1]]["field"][st], t=st)
			self.pd[ind[-1]][st[:-1]][int(st[-1])] = ind
		elif "Res" in st:
			res = self.mat[ind[-1]]["field"][st]
			self.cd[ind].setPos(field=((res[2] - res[0]) / 2 + res[0], (res[3] - res[1]) / 2 + res[1]), t="Res")
			self.pd[ind[-1]]["Res"].append(ind)

		# self.cd[ind].setPos(field=self.mat[ind[-1]]["field"][st], t=st)

		self.update_field_label()
		self.check_cont_ability()
		# if "Hand" in old:
		if self.gd["pp"] >= 0 or ("Hand" in old or "Memory" in old or "Waiting" in old):
			self.check_auto_ability(play=ind, stacks=False)

	def send_to_hand(self, ind, *args):
		if ind in self.pd[ind[-1]]["Res"]:
			self.pd[ind[-1]]["Res"].remove(ind)
		elif ind in self.pd[ind[-1]]["Climax"]:
			self.pd[ind[-1]]["Climax"].remove(ind)
		elif ind in self.pd[ind[-1]]["Memory"]:
			self.pd[ind[-1]]["Memory"].remove(ind)
		else:
			self.pd[ind[-1]][self.cd[ind].pos_new[:-1]][int(self.cd[ind].pos_new[-1])] = ""
			self.remove_marker(ind)
		self.pd[ind[-1]]["Hand"].append(ind)
		self.hand_size(ind[-1])
		self.update_field_label()
		self.check_cont_ability()

	def send_to_stock(self, ind, *args):
		if ind in self.pd[ind[-1]]["Res"]:
			self.pd[ind[-1]]["Res"].remove(ind)
		elif ind in self.pd[ind[-1]]["Hand"]:
			self.pd[ind[-1]]["Hand"].remove(ind)
			self.hand_size(ind[-1])
		elif ind in self.pd[ind[-1]]["Memory"]:
			self.pd[ind[-1]]["Memory"].remove(ind)
		elif ind in self.pd[ind[-1]]["Climax"]:
			self.pd[ind[-1]]["Climax"].remove(ind)
		else:
			self.pd[ind[-1]][self.cd[ind].pos_new[:-1]][int(self.cd[ind].pos_new[-1])] = ""
			self.remove_marker(ind)

		self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
		self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])
		self.pd[ind[-1]]["Stock"].append(ind)
		self.stock_size(ind[-1])
		self.update_field_label()
		self.check_cont_ability()

	def send_to_clock(self, ind, *args):
		if ind in self.pd[ind[-1]]["Res"]:
			self.pd[ind[-1]]["Res"].remove(ind)
		else:
			self.pd[ind[-1]][self.cd[ind].pos_new[:-1]][int(self.cd[ind].pos_new[-1])] = ""
			self.remove_marker(ind)
		self.pd[ind[-1]]["Clock"].append(ind)
		self.clock_size(ind[-1])
		self.update_field_label()
		self.check_cont_ability()

	def send_to_memory(self, ind,*args):
		self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
		self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])
		if ind in self.pd[ind[-1]]["Res"]:
			self.pd[ind[-1]]["Res"].remove(ind)
		elif ind in self.pd[ind[-1]]["Library"]:
			self.pd[ind[-1]]["Library"].remove(ind)
		elif ind in self.pd[ind[-1]]["Waiting"]:
			self.pd[ind[-1]]["Waiting"].remove(ind)
		elif ind in self.pd[ind[-1]]["Hand"]:
			self.pd[ind[-1]]["Hand"].remove(ind)
			self.hand_size(ind[-1])
		else:
			self.pd[ind[-1]][self.cd[ind].pos_new[:-1]][int(self.cd[ind].pos_new[-1])] = ""
			self.remove_marker(ind)
		self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Memory"], t="Memory")
		self.pd[ind[-1]]["Memory"].append(ind)
		self.update_field_label()
		self.check_cont_ability()

	def send_to_deck(self, ind="", all=False, pos="", *args):
		if all:
			if "Opp" in self.gd["effect"] and self.gd["ability_trigger"].split("_")[1][-1] == "1":
				player = "2"
			elif "Opp" in self.gd["effect"] and self.gd["ability_trigger"].split("_")[1][-1] == "2":
				player = "2"
			else:
				player = self.gd["ability_trigger"].split("_")[1][-1]

			for inx in self.pd[player]["Center"] + self.pd[player]["Back"]:
				if inx != "":
					if not self.gd["decker"]:
						self.gd["decker"] = True
					self.pd[player][self.cd[inx].pos_new[:-1]][int(self.cd[inx].pos_new[-1])] = ""
					self.cd[inx].setPos(field=self.mat[inx[-1]]["field"]["Library"], t="Library")
					self.pd[player]["Library"].append(inx)
					self.remove_marker(inx)
		else:
			if not self.gd["decker"]:
				self.gd["decker"] = True
			self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
			self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])
			if ind in self.pd[ind[-1]]["Res"]:
				self.pd[ind[-1]]["Res"].remove(ind)
			else:
				self.pd[ind[-1]][self.cd[ind].pos_new[:-1]][int(self.cd[ind].pos_new[-1])] = ""
			if pos == "bottom":
				self.stack(ind[-1])
				self.pd[ind[-1]]["Library"].insert(0, ind)
			else:
				self.pd[ind[-1]]["Library"].append(ind)

			self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Library"], t="Library")

			self.remove_marker(ind)
		self.update_field_label()
		self.check_cont_ability()

	def damage(self, *args):
		if self.gd["trev"]:
			player = self.gd["trev"]
		else:
			if self.gd["rev"]:
				player = self.gd["opp"]
			else:
				player = self.gd["active"]

		if self.gd["damage"] > 0 or self.gd["damage_refresh"] > 0:
			if len(self.pd[player]["Library"]) > 0:

				temp = self.pd[player]["Library"].pop()
				card = self.cd[temp]

				self.mat[player]["mat"].remove_widget(card)
				self.mat[player]["mat"].add_widget(card)

				library = self.mat[player]["field"]["Library"]
				card.show_front()
				if self.gd["damageref"]:
					self.pd[player]["Clock"].append(temp)
					self.clock_size(temp[-1])
				else:
					card.setPos(library[0] - self.sd["padding"] / 4 - self.sd["card"][0],
					            library[1] - self.sd["card"][1] / 3. * len(self.pd[player]["Res"]), t="Res")
					self.pd[player]["Res"].append(temp)

					if not self.gd["Res1_move"]:
						self.field_btn[f"Res1{player}"].x += Window.width * 2
						self.gd["Res1_move"] = True

				self.update_field_label()

				if self.gd["damage"] <= 0 < self.gd["damage_refresh"]:
					self.gd["reshuffle"] = False
					self.gd["damage_refresh"] -= 1
				elif card.card == "Climax" and self.gd["damage"] > 0:
					self.gd["cancel_dmg"] = True
					self.gd["damage"] = 0
				else:
					self.gd["damage"] -= 1

			if self.gd["damageref"] and len(self.pd[player]["Library"]) <= 0 and len(
					self.pd[player]["Clock"]) == 7 and len(self.pd[player]["Level"]) >= 3:
				if player == "1":
					self.gd["wl"] = False
				else:
					self.gd["wl"] = True
				self.gd["gg"] = True
				Clock.schedule_once(self.winlose, move_dt_btw)
				return False
			elif self.gd["damageref"] and self.gd["damage_refresh"] > 0 and len(
					self.pd[player]["Library"]) <= 0 and len(self.pd[player]["Clock"]) == 7:
				self.gd["reflev"] = ["ref", "lev"]
				Clock.schedule_once(partial(self.reflev, "ref"))
				return False
			elif self.gd["damageref"] and self.gd["damage_refresh"] == 0 and len(
					self.pd[player]["Library"]) <= 0 and len(self.pd[player]["Clock"]) == 7:
				self.gd["reflev"] = ["ref", "lev"]
				if player == "1":
					self.gd["confirm_var"] = {"c": "reflev"}
					Clock.schedule_once(self.confirm_popup, popup_dt)
				elif self.net["game"] and player == "2":
					rule = self.gd["target"].pop(0)
					Clock.schedule_once(partial(self.reflev, rule))
				elif self.gd["com"] and player == "2":
					Clock.schedule_once(partial(self.reflev, choice(("ref", "lev"))))
				return False
			elif len(self.pd[player]["Library"]) <= 0:
				if self.gd["reshuffle_trigger"]:
					self.gd["reshuffle_trigger_temp"] = str(self.gd["reshuffle_trigger"])
				self.gd["reshuffle_trigger"] = "damage"
				Clock.schedule_once(self.refresh, move_dt_btw)
				return False

			Clock.schedule_once(self.damage, move_dt_btw)
		else:
			# if len(self.pd[player]["Level"]) >= 3 and len(self.pd[player]["Clock"]) + len(
			# 		self.pd[player]["Res"]) >= 7 and not self.gd["cancel_dmg"]:
			# 	if player == "1":
			# 		self.gd["wl"] = False
			# 	else:
			# 		self.gd["wl"] = True
			#   self.gd["gg"] = True
			# 	Clock.schedule_once(self.winlose, move_dt_btw)
			# 	return False

			for inx in range(len(self.pd[player]["Res"])):
				temp = self.pd[player]["Res"].pop(0)
				if "Event" in self.gd["ability_trigger"] and temp in self.gd["ability_trigger"]:
					self.pd[player]["Res"].append(temp)
					continue
				if self.gd["cancel_dmg"]:
					self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Waiting"], t="Waiting")
					self.pd[player]["Waiting"].append(temp)
				else:
					self.pd[player]["Clock"].append(temp)

			self.clock_size(player)
			self.update_field_label()

			if self.gd["Res1_move"]:
				self.field_btn[f"Res1{player}"].x -= Window.width * 2
				self.gd["Res1_move"] = False
			self.gd["level_up_trigger"] = ""

			self.check_cont_ability()
			self.check_auto_ability(atk=self.gd["attacking"][0], cnc=(player, self.gd["cancel_dmg"]),
			                        dmg=self.gd["dmg"], stacks=False)
			if self.gd["cancel_dmg"]:
				self.gd["cancel_dmg"] = False
			self.gd["dmg"] = 0

			if len(self.gd["reflev"]) > 0:
				Clock.schedule_once(partial(self.reflev, self.gd["reflev"][0]))
				return False

			if not self.gd["both"] and self.check_lose():
				return False

			if self.gd["both"]:
				self.gd["both"] = False

			if len(self.pd[player]["Clock"]) >= 7:
				self.gd["level_up_trigger"] = "damage"
				self.check_cont_ability()
				Clock.schedule_once(self.level_up, move_dt_btw)
				return False

			if self.gd["reshuffle"]:
				self.gd["reshuffle"] = False
				self.gd["damage_refresh"] = 1
				self.gd["damageref"] = True
				self.gd["reshuffle_trigger"] = "damage"
				Clock.schedule_once(self.damage, move_dt_btw)
				return True

			self.gd["rev"] = False

			if self.gd["damageref"]:
				self.gd["damageref"] = False

			if self.gd["reshuffle_trigger_temp"]:
				self.gd["reshuffle_trigger"] = str(self.gd["reshuffle_trigger_temp"])
				self.gd["reshuffle_trigger_temp"] = ""

			if "draw" in self.gd["reshuffle_trigger"]:
				self.gd["reshuffle_trigger"] = ""
				Clock.schedule_once(self.draw, move_dt_btw)
			elif "pay" in self.gd["reshuffle_trigger"]:
				self.gd["reshuffle_trigger"] = ""
				Clock.schedule_once(self.pay_condition_done, move_dt_btw)
			elif "stock" in self.gd["reshuffle_trigger"]:
				self.gd["reshuffle_trigger"] = ""
				Clock.schedule_once(self.stock, move_dt_btw)
			elif "looktop" in self.gd["reshuffle_trigger"]:
				self.gd["reshuffle_trigger"] = ""
				Clock.schedule_once(self.look_top_done, move_dt_btw)
			elif "mill" in self.gd["reshuffle_trigger"]:
				self.gd["reshuffle_trigger"] = ""
				Clock.schedule_once(self.mill, move_dt_btw)
			elif "trigger" in self.gd["reshuffle_trigger"]:
				self.gd["reshuffle_trigger"] = ""
				Clock.schedule_once(self.trigger_done, move_dt_btw)
			elif "encore" in self.gd["reshuffle_trigger"]:
				self.gd["reshuffle_trigger"] = ""
				Clock.schedule_once(self.encore_done, move_dt_btw)
			elif "reveal" in self.gd["reshuffle_trigger"]:
				self.gd["reshuffle_trigger"] = ""
				Clock.schedule_once(self.reveal_done, move_dt_btw)
			elif "marker" in self.gd["reshuffle_trigger"]:
				self.gd["reshuffle_trigger"] = ""
				Clock.schedule_once(self.marker, move_dt_btw)
			elif "Damage" in self.gd["target"] and "encore" in self.gd["effect"]:
				Clock.schedule_once(self.encore_done)
			elif "damage" in self.gd["ability_effect"]:
				Clock.schedule_once(self.ability_effect, move_dt_btw)
			elif len(self.gd["attacking"]) >= 3:
				if self.gd["attacking"][1] == "f" and self.gd["phase"] == "Damage":
					self.pd[self.gd["active"]]["done"]["Damage"] = True
				elif self.gd["attacking"][1] != "f" and self.gd["phase"] == "Damage":
					self.pd[self.gd["active"]]["phase"]["Battle"] = True
					self.pd[self.gd["active"]]["done"]["Damage"] = True
					self.pd[self.gd["active"]]["done"]["Battle"] = True
				Clock.schedule_once(self.stack_ability)

	def dismiss_all(self):
		self.multi_info["popup"].dismiss()
		self.cardinfo.dismiss()
		self.sd["popup"]["popup"].dismiss()
		self.sd["text"]["popup"].dismiss()

	def change_active_background(self, *args):
		if self.gd["active"] == "1":
			self.rect.pos = (-self.sd["card"][0] / 2, 0)  # self.sd["menu"]["btn"].size[1])
			self.rect.source = f"atlas://{img_in}/other/bar_b"
			self.rect1.source = f"atlas://{img_in}/other/bar_b"
		elif self.gd["active"] == "2":
			self.rect.pos = (-self.sd["card"][0] / 2, self.mat["2"]["mat"].y)
			self.rect.source = f"atlas://{img_in}/other/bar_r"
			self.rect1.source = f"atlas://{img_in}/other/bar_r"

	def change_active_phase(self, step, *args):
		if step == "Encore":
			self.rect1.source = f"atlas://{img_in}/other/bar_g"
		elif self.gd["active"] == "1":
			if step == "Counter":
				self.rect1.source = f"atlas://{img_in}/other/bar_r"
			else:
				self.rect1.source = f"atlas://{img_in}/other/bar_b"
		elif self.gd["active"] == "2":
			if step == "Counter":
				self.rect1.source = f"atlas://{img_in}/other/bar_b"
			else:
				self.rect1.source = f"atlas://{img_in}/other/bar_r"

	def stand_phase(self, *args):
		self.dismiss_all()
		self.change_label()
		self.gd["pp"] = -1

		self.change_active_background()
		for card in self.pd[self.gd["active"]]["Center"] + self.pd[self.gd["active"]]["Back"]:
			if card != "":
				stand = True
				for item in self.cd[card].text_c:
					if item[0].startswith(cont_ability) and item[1] != 0 and item[1] > -9:
						eff = ab.cont(item[0])
						if "no_stand" in eff:
							stand = False
							if item[1] == 1:
								self.cd[card].text_c[self.cd[card].text_c.index(item)][1] = 0
							break
				if stand:
					self.cd[card].stand()

		self.check_cont_ability()
		self.hand_btn_show(False)
		self.pd[self.gd["active"]]["done"]["Stand Up"] = True
		self.gd["phase"] = "Draw"
		Clock.schedule_once(self.draw_phase, phase_dt)

	def draw_phase(self, *args):
		self.dismiss_all()
		self.change_label()
		self.clear_ability()
		if self.gd["pp"] < 0:
			Clock.schedule_once(self.check_auto_ability)
			return False
		else:
			self.draw_phase_ending()

	def draw_phase_ending(self):
		self.gd["draw"] = 1
		Clock.schedule_once(self.draw, move_dt_btw)

	def effect_to_stage(self, s):
		self.gd["move"] = ""
		self.gd["choose"] = True
		# if self.gd["uptomay"]:
		# 	self.gd["uptomay"] = False
		self.gd["status"] = f"{s}1"
		self.gd["status"] = self.add_to_status(self.gd["status"], self.gd["effect"])
		self.select_field()
		Clock.schedule_once(partial(self.popup_text, "Move"))

	def search(self, dt=0):
		if self.gd["p_c"] != "" and (not self.gd["target"] or self.gd["p_again"]):
			self.gd["p_again"] = False
			self.sd["popup"]["popup"].dismiss()
			if self.net["game"] and "searchopp" in self.gd["effect"] and not self.net["send"]:
				self.net["var"] = self.gd["chosen"]
				self.net["var1"] = "oppchoose"
				if not self.poptext:
					Clock.schedule_once(partial(self.popup_text, "waitingser"))
				self.mconnect("oppchoose")
				return False
			else:
				if self.gd["p_stage"] <= 0:
					if len(self.gd["chosen"]) < self.gd["effect"][0]:
						for r in range(self.gd["effect"][0] - len(self.gd["chosen"])):
							self.gd["chosen"].append("")
					self.gd["target"] = list(self.gd["chosen"])
				else:
					if len(self.gd["chosen"]) > 0:
						self.gd["target"].append(self.gd["chosen"][0])
					else:
						self.gd["target"].append("")
				if "Stage" in self.gd["effect"]:
					if len([c for c in self.gd["chosen"] if c != ""]) > 0:
						self.effect_to_stage("Stage")
					else:
						self.gd["target"].append("")
						Clock.schedule_once(self.search)
				else:
					Clock.schedule_once(self.search)
		elif self.gd["p_c"] == "" and not self.gd["target"]:
			if self.gd["uptomay"]:
				uptomay = "up to "
			else:
				uptomay = ""

			ind = self.gd["ability_trigger"].split("_")[1]

			search = ""
			if "NameSet" in self.gd["search_type"]:
				name = self.gd["search_type"].split("_")[1:]
				if len(name) / 2 == 1:
					search = f"character with\"{name}\" in its card name"
				else:
					search = f"character with\"{name}\" or \"{name}\" in its card name"
			elif "Level" in self.gd["search_type"]:  # and "Character" in self.gd["effect"]:
				lvl = self.gd["search_type"].split("_")[1]
				if "<=" in lvl:
					level = f"{lvl[-1]} or lower"
				elif ">=" in lvl:
					level = f"{lvl[-1]} or higher"
				search = f"level {level} character"
			elif "LevCost" in self.gd["search_type"]:
				lc = self.gd["search_type"].split("_")
				search = "level "
				if lc[1] == "<=p":
					search += f"{len(self.pd[ind[-1]]['Level'])} or lower"
				search += f" and cost {lc[2][-1]} or lower character"
			elif "TraitL" in self.gd["search_type"]:
				trait = self.gd['search_type'].split('_')[1:-1]
				if "_<=p" in self.gd["search_type"]:
					search = f"level {len(self.pd[ind[-1]]['Level'])} or lower"
				elif "_<=" in self.gd["search_type"]:
					search = f"level {self.gd['search_type'][-1]} or lower"
				elif "_>=" in self.gd["search_type"]:
					search = f"level {self.gd['search_type'][-1]} or higher"
				elif "_=" in self.gd["search_type"]:
					search = f"level {self.gd['search_type'][-1]}"
				for rr in range(len(trait)):
					if rr == 0:
						search += f" with «{trait[rr]}»"
					else:
						search += f" or «{trait[rr]}»"
				search += " character"
			elif "Trait" in self.gd["search_type"]:
				if len(self.gd["search_type"].split("_")) == 3:
					search = f"«{self.gd['search_type'].split('_')[1]}» or «{self.gd['search_type'].split('_')[2]}» character"
				elif self.gd["search_type"].split("_")[1:] == [""]:
					search = f"character with no traits"
				else:
					search = f"«{self.gd['search_type'].split('_')[1]}» character"
			elif "Text" in self.gd["search_type"]:
				text = self.gd['search_type'].split('_')[1]
				if len(text) < 15:
					search = f"character with \"{text.replace('] ', '')}\""
				else:
					search = f"character with \"{text}\""
			elif "Name" in self.gd["search_type"]:
				if len(self.gd["search_type"].split("_")) == 3:
					search = f"\"{self.gd['search_type'].split('_')[1]}\" or \"{self.gd['search_type'].split('_')[2]}\" character"
				else:
					search = f"\"{self.gd['search_type'].split('_')[1]}\" character"
			else:
				search = self.gd["search_type"]

			c = "Search"
			if "Reveal" in self.gd["effect"]:
				c += "_Reveal"

			if "Reveal" in self.gd["effect"]:
				self.sd["popup"]["popup"].title = f"Choose {uptomay}{self.gd['search']} {search}"
			else:
				self.sd["popup"]["popup"].title = f"Search {uptomay}{self.gd['search']} {search}"
			self.gd["confirm_var"] = {"o": ind[-1], "c": c, "m": self.gd["search"]}
			Clock.schedule_once(self.popup_start, popup_dt)
		else:
			imd = self.gd["ability_trigger"].split("_")[1]
			if self.gd["end_stage"]:
				self.gd["end_stage"] = False
				self.gd["target"][-1] = ""
				self.gd["target"].append("")
				self.gd["p_stage"] -= 1
			elif "Stage" in self.gd["effect"] and self.gd["move"] and imd[-1] == "1":
				if self.gd["uptomay"] and (not self.gd["move"] or self.gd["move"] == "none"):
					self.gd["target"].append("")
				else:
					self.gd["target"].append(self.gd["move"])
				self.gd["move"] = ""
				self.gd["p_stage"] -= 1

			if "Stage" in self.gd["effect"] and self.gd["p_stage"] > 0 and len(
					[c for c in self.gd["target"] if c == ""]) < 2:
				self.gd["p_again"] = True
				self.gd["confirm_var"] = dict(self.gd["confirm_temp"])
				self.gd["confirm_var"]["m"] = self.gd["p_stage"]
				Clock.schedule_once(self.popup_start, popup_dt)
				return False
			if "Stage" in self.gd["effect"] and len(self.gd["target"]) < self.gd["effect"][0] * 2:
				for r in range(self.gd["search"] * 2 - len(self.gd["target"])):
					self.gd["target"].append("")

			idm = []
			player = ""
			st = ""
			wait = []
			for r in range(self.gd["effect"][0]):
				ind = self.gd["target"].pop(0)
				if "Stage" in self.gd["effect"]:
					st = self.gd["target"].pop(0)
				if self.net["game"] and self.gd["p_owner"] == "1" and not self.gd["oppchoose"]:  # @@
					self.net["act"][4].append(ind)
					if "Stage" in self.gd["effect"]:
						self.net["act"][4].append(st)
				if ind in self.emptycards:
					continue
				if "Stage" in self.gd["effect"]:
					if st:
						self.cpop[ind].stage_slc(False)
						for r in range(select2cards):
							self.field_btn[f"stage{r}{ind[-1]}s"].pos = (-Window.width * 2, -Window.height * 2)
						self.play_to_stage(ind, st)
				elif "Waiting" in self.gd["effect"]:
					self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
					self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])
					self.pd[ind[-1]]["Library"].remove(ind)
					self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Waiting"], t="Waiting")
					self.pd[ind[-1]]["Waiting"].append(ind)
					wait.append(ind)
				else:
					if "Reveal" in self.gd["effect"]:
						self.pd[ind[-1]]["Res"].remove(ind)
					else:
						self.pd[ind[-1]]["Library"].remove(ind)
					self.pd[ind[-1]]["Hand"].append(ind)

				player = ind[-1]
				if player == "2":
					idm.append(ind)

			if self.gd["notarget"]:
				self.gd["notarget"] = False

			self.hand_size(imd[-1])

			if "Reveal" in self.gd["effect"]:
				for inx in range(len(self.pd[imd[-1]]["Res"])):
					temp = self.pd[imd[-1]]["Res"].pop(0)
					self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Waiting"], t="Waiting")
					self.pd[player]["Waiting"].append(temp)
					self.update_field_label()

			self.update_field_label()
			self.check_cont_ability()
			self.popup_clr()

			if "if" in self.gd["effect"]:
				if wait:
					self.gd["done"] = True
			elif "do" in self.gd["effect"] and self.gd["do"][0] > 0:
				self.gd["done"] = True

			if "search" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("search")

			self.gd["search_type"] = ""
			if player == "2" and "show" in self.gd["effect"] and len(idm) > 0:
				self.popup_multi_info(cards=idm, owner=player, t="Search")
			elif "Reveal" in self.gd["effect"] or "topdeck" in self.gd["effect"]:
				self.ability_effect()
			else:
				self.gd["shuffle_trigger"] = "ability"
				self.shuffle(imd[-1])

	def revive(self, dt=0):
		if not self.gd["move"] and not self.gd["target"]:
			self.sd["popup"]["popup"].dismiss()

			if len(self.gd["chosen"]) > 0:
				for ind in self.gd["chosen"]:
					self.gd["revive"].append(ind)
				if "may" in self.gd["ability_effect"]:
					self.gd["uptomay"] = False
			else:
				if "revive" in self.gd["ability_effect"]:
					self.gd["ability_effect"].remove("revive")

			self.gd["search_type"] = ""
			self.gd["salvage"] = 0
			self.gd["ability"] = ""

			self.popup_clr()
			self.ability_effect()
		else:
			ind = self.gd["ability_trigger"].split("_")[1]
			if "revive" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("revive")
			if self.gd["revive"] and self.gd["move"] and ind[-1] == "1" and not self.gd["target"]:
				c = self.gd["revive"].pop(0)
				m = self.gd["move"]
				self.gd["target"].append(c)
				self.gd["target"].append(m)
				if self.net["game"] and c[-1] == "1":
					self.net["act"][4].append(c)
					self.net["act"][4].append(m)
				self.gd["choose"] = False
				self.gd["move"] = ""

			if self.gd["target"]:
				card = self.gd["target"].pop(0)
				move = self.gd["target"].pop(0)
				if card != "":
					if "extra" in self.gd["effect"]:
						self.gd["extra"].append(card)
					if self.pd[card[-1]][move[:-1]][int(move[-1])] != "":
						temp = self.pd[card[-1]][move[:-1]][int(move[-1])]
						self.send_to_waiting(temp)
					self.pd[card[-1]]["Waiting"].remove(card)
					self.cd[card].setPos(field=self.mat[card[-1]]["field"][self.gd["move"]], t=self.gd["move"])
					self.pd[card[-1]][move[:-1]][int(move[-1])] = card

				self.update_field_label()
				self.check_cont_ability()
				self.popup_clr()

			self.do_check(True)

	# self.ability_effect()
	# self.check_auto_ability(play=card)

	def cstock(self, dt=0):
		idm = self.gd["ability_trigger"].split("_")[1]
		if idm[-1] == "1" and self.gd["p_c"] != "" and not self.gd["target"]:
			self.sd["popup"]["popup"].dismiss()
			if len(self.gd["chosen"]) < self.gd["effect"][0]:
				for r in range(self.gd["effect"][0] - len(self.gd["chosen"])):
					self.gd["chosen"].append("")
			self.gd["target"] = list(self.gd["chosen"])
			self.cstock()
		elif idm[-1] == "1" and self.gd["p_c"] == "" and not self.gd["target"]:
			if self.gd["uptomay"]:
				uptomay = "up to "
			else:
				uptomay = ""

			if "Card" in self.gd["search_type"]:
				search = f"{self.gd['search_type'].split('_')[0].upper()} {self.gd['search_type'].split('_')[1]}"
			elif "Trait" in self.gd["search_type"]:
				if len(self.gd["search_type"].split("_")) == 3:
					search = f"«{self.gd['search_type'].split('_')[1]}» or «{self.gd['search_type'].split('_')[2]}»"
				else:
					search = f"«{self.gd['search_type'].split('_')[1]}»"
			elif len(self.gd["search_type"].split("_")) == 3:
				search = f"{self.gd['search_type'].split('_')[1]} or {self.gd['search_type'].split('_')[2]}"
			else:
				search = self.gd["search_type"]

			self.sd["popup"]["popup"].title = f"Choose {uptomay}{self.gd['salvage']} {search}"
			c = "cstock_"
			if "Waiting" in self.gd["effect"]:
				c += "Salvage"
			elif "Library" in self.gd["effect"]:
				c += "Search"
			elif "Clock" in self.gd["effect"]:
				c += "Level"
			self.gd["confirm_var"] = {"o": self.gd["active"], "c": c, "m": self.gd["salvage"]}
			Clock.schedule_once(self.popup_start, popup_dt)
		else:
			if "cstock" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("cstock")

			for r in range(self.gd["effect"][0]):
				ind = self.gd["target"].pop(0)
				if self.net["game"] and self.gd["p_owner"] == "1":  # @@
					self.net["act"][4].append(ind)
				if ind in self.emptycards:
					continue
				self.pd[ind[-1]][self.gd["effect"][self.gd["effect"].index("cstock") + 2]].remove(ind)
				self.pd[ind[-1]]["Stock"].append(ind)
				self.update_field_label()
				self.stock_size(ind[-1])
			if "Hand" in self.gd["effect"]:
				self.hand_size(idm[-1])

			if self.gd["notarget"]:
				self.gd["notarget"] = False

			self.check_cont_ability()
			self.popup_clr()
			self.gd["search_type"] = ""
			self.gd["salvage"] = 0
			self.do_check(True)

	def shuffle_ability(self, *args):
		ind = self.gd["ability_trigger"].split("_")[1]
		if "opp" in self.gd["effect"] and ind[-1] == "1":
			player = "2"
		elif "opp" in self.gd["effect"] and ind[-1] == "2":
			player = "1"
		else:
			player = str(ind[-1])

		if self.gd["effect"][0] == -1:
			if "both" in self.gd["effect"]:
				players = ["1", "2"]
			else:
				players = [player]
			for player in players:
				for n in range(len(self.pd[player]["Waiting"])):
					temp = self.pd[player]["Waiting"].pop()
					self.pd[player]["Library"].append(temp)
					self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Library"], t="Library")
				self.update_field_label()

			self.gd["shuffle_trigger"] = "ability"
			self.gd["ability_effect"].remove("shuffle")
			self.do_check()
			if "both" in self.gd["effect"]:
				self.shuffle("0")
			else:
				self.shuffle(player)
		elif self.gd["effect"][0] > 0:
			if self.gd["p_c"] != "" and not self.gd["target"]:
				self.sd["popup"]["popup"].dismiss()
				if len(self.gd["chosen"]) < self.gd["effect"][0]:
					for r in range(self.gd["effect"][0] - len(self.gd["chosen"])):
						self.gd["chosen"].append("")
				self.gd["target"] = list(self.gd["chosen"])
				if self.gd["notarget"]:
					self.gd["notarget"] = False
				self.shuffle_ability()
			elif self.gd["p_c"] == "" and not self.gd["target"]:
				if len(self.pd[player]["Waiting"]) > 0:
					if self.gd["uptomay"]:
						uptomay = "up to "
					else:
						uptomay = ""

					if self.gd["effect"][0] > 1:
						word = "cards"
					else:
						word = "card"

					if len(self.pd[player]["Waiting"]) < self.gd['effect'][0]:
						m = len(self.pd[player]["Waiting"])
					else:
						m = self.gd['effect'][0]

					self.sd["popup"]["popup"].title = f"Choose {uptomay}{self.gd['effect'][0]} {word}"

					self.gd["confirm_var"] = {"c": "Shuffle", "m": m, "o": player}
					Clock.schedule_once(self.popup_start, popup_dt)
				else:
					self.gd["p_c"] = "Shuffle_"
					self.gd["chosen"] = []
					self.shuffle_ability()
			else:
				if "shuffle" in self.gd["ability_effect"]:
					self.gd["ability_effect"].remove("shuffle")

				for r in range(self.gd["effect"][0]):
					temp = self.gd["target"].pop(0)
					if self.net["game"] and self.gd["p_owner"] == "1":  # @@
						self.net["act"][4].append(temp)
					if temp in self.emptycards:
						continue
					self.pd[temp[-1]]["Waiting"].remove(temp)
					self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Library"], t="Library")
					self.pd[temp[-1]]["Library"].append(temp)
				self.update_field_label()

				self.check_cont_ability()
				self.popup_clr()

				self.gd["shuffle_trigger"] = "ability"
				self.do_check()

				self.shuffle(player)

	def change(self, *args):
		if self.gd["p_c"] != "" and not self.gd["target"]:
			self.sd["popup"]["popup"].dismiss()
			if len(self.gd["chosen"]) < self.gd["effect"][1]:
				for r in range(self.gd["effect"][1] - len(self.gd["chosen"])):
					self.gd["chosen"].append("")
			self.gd["target"] = list(self.gd["chosen"])
			if self.gd["notarget"]:
				self.gd["notarget"] = False
			self.change()
		elif self.gd["p_c"] == "" and not self.gd["target"]:
			idm = self.gd["ability_trigger"].split("_")[1]
			if self.gd["uptomay"]:
				self.sd["btn"]["Change_btn"].disabled = False
				upto = "up to "
			else:
				self.sd["btn"]["Change_btn"].disabled = True
				upto = ""

			search = ""
			if "NCost" in self.gd["search_type"]:
				nc = self.gd['search_type'].split('_')
				if "<=" in nc[2]:
					search += f"cost {nc[2][-1]} or lower"
				search += f" character with \"{nc[1]}\" in name"
			elif "TraitL" in self.gd["search_type"]:
				trait = self.gd['search_type'].split('_')[1:-1]
				if "_<=p" in self.gd["search_type"]:
					search = f"level {len(self.pd[idm[-1]]['Level'])} or lower"
				elif "_<=" in self.gd["search_type"]:
					search = f"level {self.gd['search_type'][-1]} or lower"
				elif "_>=" in self.gd["search_type"]:
					search = f"level {self.gd['search_type'][-1]} or higher"
				elif "_=" in self.gd["search_type"]:
					search = f"level {self.gd['search_type'][-1]}"
				for rr in range(len(trait)):
					if rr == 0:
						search += f" with «{trait[rr]}»"
					else:
						search += f" or «{trait[rr]}»"
				search += " character"
			else:
				search = self.gd['search_type'].split('_')[1]

			c = "Change_Salvage"
			if "mchange" in self.gd["effect"]:
				c += "_Memory"
			elif "lchange" in self.gd["effect"]:
				c = "Change_Search"

			self.sd["popup"]["popup"].title = f"Choose {upto}{self.gd['salvage']} {search}"

			self.gd["confirm_var"] = {"o": self.gd["ability_trigger"].split("_")[1][-1], "c": c,
			                          "m": self.gd["salvage"]}
			Clock.schedule_once(self.popup_start, popup_dt)
		else:
			if "change" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("change")

			card = self.cd[self.gd["ability_trigger"].split("_")[1]]
			for r in range(self.gd["effect"][1]):
				ind = self.gd["target"].pop(0)
				if self.net["game"] and self.gd["p_owner"] == "1":  # @@
					self.net["act"][4].append(ind)
				if ind in self.emptycards:
					continue
				if "extra" in self.gd["effect"]:
					self.gd["extra"].append(ind)
				if "mchange" in self.gd["effect"]:
					self.pd[ind[-1]]["Memory"].remove(ind)
					self.cd[ind].stand()
				elif "lchange" in self.gd["effect"]:
					self.pd[ind[-1]]["Library"].remove(ind)
				else:
					self.pd[ind[-1]]["Waiting"].remove(ind)

				self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
				self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])
				self.cd[ind].setPos(field=self.mat[ind[-1]]["field"][card.pos_old], t=card.pos_old)

				if self.pd[ind[-1]][self.cd[ind].pos_new[:-1]][int(self.cd[ind].pos_new[-1])] != "":
					temp = self.pd[ind[-1]][self.cd[ind].pos_new[:-1]][int(self.cd[ind].pos_new[-1])]
					self.send_to_waiting(temp)
				self.pd[ind[-1]][self.cd[ind].pos_new[:-1]][int(self.cd[ind].pos_new[-1])] = ind

				self.check_auto_ability(change=ind, stacks=False)

			self.update_field_label()
			self.check_cont_ability()
			self.popup_clr()

			self.gd["search_type"] = ""

			self.do_check()
			if "lchange" in self.gd["effect"]:
				self.gd["shuffle_trigger"] = "ability"
				self.shuffle(card.ind[-1])
			else:
				self.gd["salvage"] = 0
				Clock.schedule_once(self.ability_effect)

	def salvage(self, dt=0):
		if self.gd["p_c"] != "" and (not self.gd["target"] or self.gd["p_again"]):
			self.gd["p_again"] = False
			self.sd["popup"]["popup"].dismiss()
			if self.gd["p_stage"] <= 0:
				if len(self.gd["chosen"]) < self.gd["salvage"]:
					for r in range(self.gd["effect"][0] - len(self.gd["chosen"])):
						self.gd["chosen"].append("")
				self.gd["target"] = list(self.gd["chosen"])
			else:
				if len(self.gd["chosen"]) > 0:
					self.gd["target"].append(self.gd["chosen"][0])
				else:
					self.gd["target"].append("")
			if self.gd["notarget"]:
				self.gd["notarget"] = False
			if "Stage" in self.gd["effect"]:
				if len([c for c in self.gd["chosen"] if c != ""]) > 0:
					self.effect_to_stage("Stage")
				else:
					self.gd["move"] = "none"
					Clock.schedule_once(self.salvage)
			elif "levswap" in self.gd["effect"]:
				if len([s for s in self.gd["target"] if s != ""]) > 0:
					for rr in self.gd["target_temp"]:
						self.gd["target"].append(rr)
					self.gd["target_temp"] = []
				Clock.schedule_once(self.salvage)
			else:
				Clock.schedule_once(self.salvage)
		elif self.gd["p_c"] == "" and not self.gd["target"]:
			# if self.gd["salvage_cost"]:
			# 	self.pay_condition()

			if self.gd["uptomay"]:
				uptomay = "up to "
			else:
				uptomay = ""
			ind = self.gd["ability_trigger"].split("_")[1]
			if "opp" in self.gd["effect"] and ind[-1] == "1":
				opp = "2"
			elif "opp" in self.gd["effect"] and ind[-1] == "2":
				opp = "1"
			else:
				opp = ind[-1]

			if "x#" in self.gd["effect"]:
				tx = 0
				if "xmemory" in self.gd["effect"]:
					tx = len(self.pd[opp]["Memory"])
				self.gd["effect"][2] = f"{self.gd['effect'][2][:-1]}{tx}"
				self.gd["search_type"] = self.gd["effect"][2]

			search = ""
			if "_standby" in self.gd["search_type"]:
				search = f"level {len(self.pd[opp]['Level']) + 1} or lower character"
			elif "Cost" in self.gd["search_type"]:
				if "<=" in self.gd["search_type"]:
					search = f"cost {self.gd['search_type'][-1]} or lower character"
			elif "TraitL" in self.gd["search_type"]:
				if "_<=" in self.gd["search_type"]:
					search = f"level {self.gd['search_type'][-1]} or lower «{self.gd['search_type'].split('_')[1]}» character"
				elif "_=" in self.gd["search_type"]:
					search = f"level {self.gd['search_type'][-1]} «{self.gd['search_type'].split('_')[1]}» character"
			elif "TraitN" in self.gd["search_type"]:
				search = f"«{self.gd['search_type'].split('_')[1]}» or {self.gd['search_type'].split('_')[-1]} in its card name "
			elif "BTrait" in self.gd["search_type"]:
				pass
			elif "Trait" in self.gd["search_type"]:
				if len(self.gd["search_type"].split("_")) == 3:
					search = f"«{self.gd['search_type'].split('_')[1]}» or «{self.gd['search_type'].split('_')[2]}» character"
				else:
					search = f"«{self.gd['search_type'].split('_')[1]}» character"
			elif "CLevel" in self.gd["search_type"]:
				if "<=" in self.gd["search_type"]:
					search = f"level {self.gd['search_type'][-1]} or lower character"
			elif len(self.gd["search_type"].split("_")) == 3:
				search = f"{self.gd['search_type'].split('_')[1]} or {self.gd['search_type'].split('_')[2]}"
			elif "_" in self.gd["search_type"]:
				search = self.gd['search_type'].split('_')[1]
			else:
				search = self.gd["search_type"]
			if search == "":
				search = "card"

			c = "Salvage"
			if "revive" in self.gd["effect"]:
				c = f"revive_{c}"
			elif "marker" in self.gd["effect"]:
				c = f"Marker_{c}"
			elif "csalvage" in self.gd["effect"]:
				c += "_Clock"
			elif "msalvage" in self.gd["effect"]:
				c += "_Memory"

			if "ID=" in self.gd["search_type"] and "passed" in self.gd["effect"]:
				self.sd["popup"][
					"popup"].title = f"Choose characters from previous effect to continue."
			elif "Name=" in self.gd["search_type"]:
				name = self.gd['search_type'].split('_')[1:]
				if "passed" in self.gd["effect"]:
					self.sd["popup"][
						"popup"].title = f"Choose characters from previous effect to continue."
				else:
					self.sd["popup"][
						"popup"].title = f"Choose {uptomay}{self.gd['salvage']} \"{name[0]}\""
			elif "Name" in self.gd["search_type"]:
				name = self.gd['search_type'].split('_')[1:]
				if len(name) == 1:
					self.sd["popup"]["popup"].title = f"Choose a character with \"{name[0]}\" in its card name"
				elif len(name) == 2:
					self.sd["popup"][
						"popup"].title = f"Choose a character with \"{name[0]}\" or \"{name[1]}\" in its card name"
			elif "BTrait" in self.gd["search_type"]:
				self.gd["btrait"][1] = self.gd["search_type"].split("_")[1:]
				self.gd["btrait"][3] = list(self.gd["btrait"][1])
				if self.gd["salvage"] == len(self.gd["btrait"][1]):
					for nx in range(len(self.gd["btrait"][1])):
						if nx == 0:
							self.sd["popup"]["popup"].title = f"Choose {uptomay}1 «{self.gd['btrait'][1][nx]}» character"
						elif nx == len(self.gd["btrait"][1])-1:
							self.sd["popup"]["popup"].title += f", and {uptomay}1 «{self.gd['btrait'][1][nx]}» character"
						else:
							self.sd["popup"]["popup"].title += f", {uptomay}1 «{self.gd['btrait'][1][nx]}» character"
			else:
				self.sd["popup"]["popup"].title = f"Choose {uptomay}{self.gd['salvage']} {search}"

			self.gd["confirm_var"] = {"o": opp, "c": c, "m": self.gd["salvage"]}
			Clock.schedule_once(self.popup_start, popup_dt)
		else:
			imd = self.gd["ability_trigger"].split("_")[1]
			if self.gd["end_stage"]:
				self.gd["end_stage"] = False
				self.gd["target"][-1] = ""
				self.gd["target"].append("")
				self.gd["p_stage"] -= 1
			elif "Stage" in self.gd["effect"] and self.gd["move"] and imd[-1] == "1":
				if not self.gd["move"] or self.gd["move"] == "none":
					self.gd["target"].append("")
				else:
					self.gd["target"].append(self.gd["move"])
				self.gd["move"] = ""
				self.gd["p_stage"] -= 1

			if "Stage" in self.gd["effect"] and self.gd["p_stage"] > 0 and len(
					[c for c in self.gd["target"] if c == ""]) < 2:
				self.gd["p_again"] = True
				self.gd["confirm_var"] = dict(self.gd["confirm_temp"])
				self.gd["confirm_var"]["m"] = self.gd["p_stage"]
				Clock.schedule_once(self.popup_start, popup_dt)
				return False
			if "Stage" in self.gd["effect"] and len(self.gd["target"]) < self.gd["effect"][0] * 2:
				for r in range(self.gd["salvage"] * 2 - len(self.gd["target"])):
					self.gd["target"].append("")

			idm = []
			player = ""
			st = ""
			ss = ""
			lif = []

			for r in range(self.gd["salvage"]):
				ind = self.gd["target"].pop(0)
				st = ""
				if "Stage" in self.gd["effect"]:
					st = self.gd["target"].pop(0)
				if self.net["game"] and imd[-1] == "1":  # @@
					self.net["act"][4].append(ind)
					if "Stage" in self.gd["effect"]:
						self.net["act"][4].append(st)
				if ind in self.emptycards:
					continue
				if "if" in self.gd["effect"]:
					lif.append(ind)
				if "extra1" in self.gd["effect"]:
					self.gd["extra1"].append(ind)
				elif "extra" in self.gd["effect"]:
					self.gd["extra"].append(ind)
				if "Stage" in self.gd["effect"]:
					if st:
						self.cpop[ind].stage_slc(False)
						for r in range(select2cards):
							self.field_btn[f"stage{r}{ind[-1]}s"].pos = (-Window.width * 2, -Window.height * 2)
						self.play_to_stage(ind, st)
				elif "levswap" in self.gd["effect"]:
					lv = self.gd["target"].pop(0)
					self.mat[ind[-1]]["mat"].remove_widget(self.cd[lv])
					self.mat[ind[-1]]["mat"].add_widget(self.cd[lv])
					self.pd[ind[-1]]["Level"].remove(lv)
					self.cd[lv].setPos(field=self.mat[ind[-1]]["field"]["Waiting"], t="Waiting")
					self.pd[ind[-1]]["Waiting"].append(lv)
					self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
					self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])
					self.pd[ind[-1]]["Waiting"].remove(ind)
					self.pd[ind[-1]]["Level"].append(ind)
					self.level_size(ind[-1])
					self.update_colour(ind[-1])
					self.check_auto_ability(lvc=ind, stacks=False)
				else:
					if "csalvage" in self.gd["effect"]:
						self.pd[ind[-1]]["Clock"].remove(ind)
					else:
						self.pd[ind[-1]]["Waiting"].remove(ind)
					self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
					self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])
					if "Library" in self.gd["effect"] or "wdecker" in self.gd["effect"]:
						self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Library"], t="Library")
						if "top" in self.gd["effect"]:
							self.pd[ind[-1]]["Library"].append(ind)
							ss = ""
						elif "bottom" in self.gd["effect"]:
							self.pd[ind[-1]]["Library"].insert(0, ind)
							ss = ""
						else:
							ss = ind[-1]
					elif "Memory" in self.gd["effect"]:
						self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Memory"], t="Memory")
						self.pd[ind[-1]]["Memory"].append(ind)
					elif "Stock" in self.gd["effect"]:
						self.pd[ind[-1]]["Stock"].append(ind)
						self.stock_size(ind[-1])
					else:
						self.pd[ind[-1]]["Hand"].append(ind)
						if "csalvage" not in self.gd["effect"] and "msalvage" not in self.gd["effect"]:
							self.check_auto_ability(sav=ind, stacks=False)

				player = ind[-1]
				if player == "2" or (player == "1" and imd[-1] == "2"):
					idm.append(ind)

			self.hand_size(imd[-1])
			if "csalvage" in self.gd["effect"]:
				self.clock_size(imd[-1])
			self.update_field_label()
			self.check_cont_ability()

			if "salvage" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("salvage")
			if "bond" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("bond")
			if "revive" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("revive")
			self.popup_clr()
			if self.gd["notarget"]:
				self.gd["notarget"] = False
			self.gd["search_type"] = ""
			self.gd["salvage"] = 0
			if "BTrait" in self.gd["search_type"]:
				self.gd["btrait"] = ["", [], [], [],[], []]

			if "levswap" in self.gd["effect"] and len(self.gd["target_temp"]) > 0:
				self.gd["target_temp"] = []

			if "wdecker" in self.gd["effect"]:
				self.gd["effect"].remove("wdecker")

			if "if" in self.gd["effect"]:
				if lif:
					self.gd["done"] = True
			elif "do" in self.gd["effect"] and self.gd["do"][0] > 0:
				self.gd["done"] = True

			if "do" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("do")
			if player == "1" and imd[-1] == "2" and "show" in self.gd["effect"] and len(idm) > 0:
				self.popup_multi_info(cards=idm, owner=player, t="OChoose")
			elif player == "2" and imd[-1] == "2" and "show" in self.gd["effect"] and len(idm) > 0:
				self.popup_multi_info(cards=idm, owner=player, t="Salvage")
			else:
				if ss:
					self.gd["shuffle_trigger"] = "ability"
					self.shuffle(ss)
				else:
					if self.net["game"] and "plchoose" in self.gd["effect"] and not self.net["send"]:
						self.net["var"] = list(self.net["act"][4])
						self.net["var1"] = "plchoose"
						if not self.poptext:
							Clock.schedule_once(partial(self.popup_text, "waitingser"))
						self.mconnect("plchoose")
					else:
						Clock.schedule_once(self.ability_effect)

	def select_filter_check(self, ind):
		if ind in self.gd["target"]:
			return False

		if "Character" in self.gd["search_type"] and self.cd[ind].card in self.gd["search_type"]:
			return True
		elif "ID=" in self.gd["search_type"]:
			if any(name == ind for name in self.gd["search_type"].split("_")[1:]):
				return True
		elif "TraitL" in self.gd["search_type"]:
			if "_<=p" in self.gd["search_type"] and any(
					tr in self.cd[ind].trait_t for tr in self.gd["search_type"].split("_")[1:-1]) and self.cd[
				ind].level <= len(self.pd[ind[-1]]["Level"]):
				return True
			elif "_<=" in self.gd["search_type"] and "p" not in self.gd["search_type"][-1] and self.gd[
				"search_type"] and any(
					tr in self.cd[ind].trait_t for tr in self.gd["search_type"].split("_")[1:-1]) and self.cd[
				ind].level <= int(self.gd["search_type"][-1]):
				return True
			elif "_>=" in self.gd["search_type"] and "p" not in self.gd["search_type"][-1] and self.gd[
				"search_type"] and any(
					tr in self.cd[ind].trait_t for tr in self.gd["search_type"].split("_")[1:-1]) and self.cd[
				ind].level >= int(self.gd["search_type"][-1]):
				return True
			elif "_=" in self.gd["search_type"] and "p" not in self.gd["search_type"][-1] and self.gd[
				"search_type"] and any(
					tr in self.cd[ind].trait_t for tr in self.gd["search_type"].split("_")[1:-1]) and self.cd[
				ind].level == int(self.gd["search_type"][-1]):
				return True
		elif "TraitN" in self.gd["search_type"]:
			if "or" in self.gd["effect"] and self.gd["search_type"].split("_")[1] in self.cd[ind].trait_t or \
					self.gd["search_type"].split("_")[-1] in self.cd[ind].name:
				return True
			elif "or" not in self.gd["effect"] and self.gd["search_type"].split("_")[1] in self.cd[ind].trait_t and \
					self.gd["search_type"].split("_")[-1] in self.cd[ind].name:
				return True
		elif "BTrait" in self.gd["search_type"]:
			if self.cd[ind].card == "Character" and self.gd["btrait"][3]:
				b = 0
				t =[]
				for tr in self.cd[ind].trait_t:
					if tr in self.gd["btrait"][3]:
						b+=1
						t.append(tr)

				if b == 0:
					return False
				elif not self.gd["btrait"][4]:
					if b == 1:
						self.gd["btrait"][3].remove(t[0])
						self.gd["btrait"][5].append((ind,t[0]))
					elif b>1:
						self.gd["btrait"][4].append(ind)
					return True
				elif self.gd["btrait"][4]:
					ind1 = self.gd["btrait"][4].pop()
					b1 = 0
					t1 = []
					for tr in self.cd[ind1].trait_t:
						if tr in self.gd["btrait"][3]:
							b1 += 1
							t1.append(tr)
					if b == 1 and b1>1 and t[0] in t1:
						self.gd["btrait"][3].remove(t[0])
						self.gd["btrait"][5].append((ind, t[0]))
						t1.remove(t[0])
						if len(t1)==1:
							self.gd["btrait"][3].remove(t1[0])
							self.gd["btrait"][5].append((ind1,t1[0]))
						else:
							self.gd["btrait"][4].append(ind1)
						return True
					elif b>1 and b1>1:
						if set(t)==set(t1):
							if b==2 and b1==2:
								self.gd["btrait"][3].remove(t[0])
								self.gd["btrait"][5].append((ind, t[0]))
								t1.remove(t[0])
								self.gd["btrait"][3].remove(t1[0])
								self.gd["btrait"][5].append((ind1, t1[0]))
								return True

			# self.gd["btrait"][3] = {}
			# self.gd["btrait"][3]["b"] = 0
			# self.gd["btrait"][3]["c"] = 0
			# self.gd["btrait"][3]["0"] = []
			#
			# for nx in self.gd["chosen"]:
			# 	for tr in self.gd["btrait"][1]:
			# 		if tr!="" and tr in self.cd[self.gd["chosen"][nx]].trait_t:
			# 			self.gd["btrait"][3]["b"]+=1
			# 		elif tr=="" and len(self.cd[self.gd["chosen"][nx]].trait_t) == 0:
			# 			self.gd["btrait"][3]["b"]+=1
			# 	if self.gd["btrait"][3]["b"] >= len(self.gd["btrait"][1]):
			# 		if self.gd["btrait"][3]["c"]<len(self.gd["btrait"][1]):
			# 			self.gd["btrait"][3]["c"]+=1
			# 		else:
			# 			return False
			# 	elif self.gd["btrait"][3]["b"]==0:
			# 		return False
			# 	elif self.gd["btrait"][3]["b"] == 1:
			# 		if nx not self.gd["btrait"][3]["0"]:

		elif "Trait" in self.gd["search_type"]:
			if self.gd["search_type"].split("_")[1:] == [""] and len(self.cd[ind].trait_t) <= 0 and "Character" in \
					self.cd[ind].card:
				return True
			elif self.gd["search_type"].split("_")[1:] != [""] and any(
					trait in self.cd[ind].trait_t for trait in self.gd["search_type"].split("_")[1:]):
				return True
		elif "Name=" in self.gd["search_type"] or "Bond_" in self.gd["search_type"]:
			# if self.cd[ind].name in self.gd["search_type"]:
			if any(name == self.cd[ind].name for name in self.gd["search_type"].split("_")[1:]):
				return True
		elif "Name" in self.gd["search_type"] and any(
				name in self.cd[ind].name for name in self.gd["search_type"].split("_")[1:]):
			return True
		elif "Text" in self.gd["search_type"] and any(
				any(txt.lower() in text.lower() for txt in self.gd["search_type"].split("_")[1:]) for text in
				self.cd[ind].text_o):
			return True
		elif "Climax" in self.gd["search_type"] and self.cd[ind].card in self.gd["search_type"]:
			return True
		elif "Card" in self.gd["search_type"] and self.cd[ind].mcolour.lower() in self.gd["search_type"]:
			return True
		elif "NCost" in self.gd["search_type"]:
			if "Character" in self.cd[ind].card and "<=" in self.gd["search_type"] and self.cd[ind].cost <= int(
					self.gd["search_type"][-1]) and self.gd["search_type"].split("_")[1] in self.cd[ind].name:
				return True
		elif "LevCost" in self.gd["search_type"] and "<=p" in self.gd["search_type"] and "Character" in self.cd[
			ind].card and self.cd[ind].level <= len(self.pd[ind[-1]]["Level"]) and self.cd[ind].cost <= int(
				self.gd["search_type"][-1]):
			return True
		elif "Cost_<=" in self.gd["search_type"] and self.cd[ind].cost <= int(
				self.gd["search_type"][-1]) and "Character" in self.cd[ind].card:
			return True
		elif "Cost_>=" in self.gd["search_type"] and self.cd[ind].cost >= int(
				self.gd["search_type"][-1]) and "Character" in self.cd[ind].card:
			return True
		elif "CLevelN" in self.gd["search_type"] and "Character" in self.cd[ind].card:
			if "Character" in self.cd[ind].card and "_standby" in self.gd["search_type"] and self.cd[ind].level <= len(
					self.pd[ind[-1]]["Level"]) + 1 and \
					self.gd["search_type"].split("_")[-1] in self.cd[ind].name:
				return True
			else:
				return False
		elif "CLevel" in self.gd["search_type"]:
			if "_standby" in self.gd["search_type"] and self.cd[ind].level <= len(
					self.pd[ind[-1]]["Level"]) + 1 and "Character" in self.cd[ind].card:
				return True
			elif "_<=" in self.gd["search_type"] and "Character" in self.cd[ind].card and self.cd[ind].level <= int(
					self.gd["search_type"][-1]):
				return True
			elif "_>=" in self.gd["search_type"] and "Character" in self.cd[ind].card and self.cd[ind].level >= int(
					self.gd["search_type"][-1]):
				return True
			else:
				return False
		elif "stacked" in self.gd["search_type"]:
			if self.cpop[ind].back:
				return True
		elif self.gd["search_type"] == "":
			return True
		return False

	def close_popup(self, *args):
		self.sd["popup"]["popup"].dismiss()
		Clock.schedule_once(self.popup_clr)
		if self.gd["act_poped"]:
			self.gd["act_poped"] = ""
		if len(self.gd["select_btns"]) <= 0 and ("Main" in self.gd["phase"] or "Climax" in self.gd["phase"]):
			Clock.schedule_once(self.play_card_done)

	def info_start(self, *args):
		self.sd["hbtn_press"] = []
		if self.infot is not None:
			self.infot.cancel()
			self.infot = None
		if self.infob is not None:
			self.infob.cancel()
			self.infob = None
		if self.gd["phase"] in ("", "Janken", "Mulligan") and self.gd["popup_done"][
			1]:  # @End , "Draw", "Standby", "Stand Up"
			pass
		elif self.gd["btn_release"]:
			pass
		elif self.gd["moving"]:
			pass
		else:
			if self.gd["btn_id"][:-1] in self.fields:
				if self.gd["btn_id"][:-1] in self.gd["stage"]:
					card = self.pd[str(self.gd["btn_id"][-1])][self.gd["btn_id"][:-2]][int(self.gd["btn_id"][-2])]
					if card:
						self.cardinfo.import_data(self.cd[card], annex_img)
				elif "Climax" in self.gd["btn_id"]:
					try:
						card = self.pd[str(self.gd["btn_id"][-1])][self.gd["btn_id"][:-1]][0]
						if card:
							self.cardinfo.import_data(self.cd[card], annex_img)
					except IndexError:
						pass
				elif self.gd["btn_id"][:-1] in ("Memory", "Clock", "Level", "Waiting", "Res"):
					if self.pd[str(self.gd["btn_id"][-1])][self.gd["btn_id"][:-1]]:
						self.sd["popup"]["stack"].clear_widgets()
						self.popup_multi_info(field=self.gd["btn_id"][:-1], owner=self.gd["btn_id"][-1])
			else:
				if self.gd["btn_id"]:
					self.gd["info_p"] = True
					self.cardinfo.import_data(self.cd[self.gd["btn_id"]], annex_img)
					self.hand_size(self.gd["btn_id"][-1])

	def popup_text_start(self):
		self.sd["text"] = {}
		self.sd["text"]["popup"] = Popup(title="", separator_height=0)
		self.sd["text"]["popup"].bind(on_dismiss=self.popup_text_check_open)
		self.sd["text"]["c"] = ""
		self.sd["text"]["close"] = Button(size_hint=(None, None), text="Close", on_release=self.popup_text_close)
		self.sd["text"]["label"] = Label(text="", text_size=(self.sd["card"][0] * 0.9 * starting_hand, None),
		                                 halign='center', valign="middle")
		self.sd["text"]["sct"] = RelativeLayout()
		self.sd["text"]["popup"].content = self.sd["text"]["sct"]
		self.sd["text"]["sct"].add_widget(self.sd["text"]["label"])
		self.sd["text"]["sct"].add_widget(self.sd["text"]["close"])

	def popup_text_check_open(self, *args):
		self.poptext = False
		self.gd["text_popup"] = False

	def popup_text_close(self, btn):
		self.sd["text"]["popup"].dismiss()
		self.gd["text_popup"] = False
		if self.decks["dbuilding"]:
			pass
		elif self.gd["ability_doing"] == "look":
			self.gd["ability_doing"].remove("look")
			self.ability_effect()
		elif "Counter" in self.sd["text"]["c"]:
			Clock.schedule_once(self.counter_step_done)
		elif "Climax" in self.sd["text"]["c"]:
			self.gd["phase"] = "Attack"
			Clock.schedule_once(self.attack_phase, phase_dt)
		elif self.gd["notargetfield"]:
			self.gd["move"] = "none"
			self.ability_effect()
		elif self.gd["notarget"]:
			self.gd["choose"] = True
			self.gd["chosen"] = []
			if len(self.gd["chosen"]) < self.gd["effect"][0]:
				for r in range(self.gd["effect"][0] - len(self.gd["chosen"])):
					self.gd["chosen"].append("")
			self.gd["target"] = list(self.gd["chosen"])
			self.ability_effect()
		elif "roomdis" in self.sd["text"]["c"] or "no_internet" in self.sd["text"]["c"]:
			self.net = network_init()
			self.network["m_connect"].disabled = False
		elif self.net["game"] and self.sd["text"]["c"] == "waiting":
			self.gd["popup_on"] = True

	def popup_text(self, c="", dt=0):
		self.poptext = True
		self.gd["text_popup"] = True
		self.sd["text"]["c"] = c
		text = "　"

		xscat = self.sd["card"][0] * starting_hand
		yscat = self.sd["padding"] * 1.5 + self.sd["card"][1] / 4. + self.sd["padding"] * 8  # + self.sd["card"][1]

		self.sd["text"]["close"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
		yscat += self.sd["card"][1] / 4. + self.sd["padding"] * 2
		self.sd["text"]["close"].text = "Close"

		if c in ("Attack", "Declaration"):
			text = "Select a Character and choose the attack type"
		elif "Counter" in c:
			text = "There are no playable counter cards in your hand."
		elif "Climax" in c:
			text = "There are no playable Climax cards in your hand."
		elif "Encore" in c:
			text = "Select a reversed Character and put it into the waiting room.\n(Repeate this step until there are no reversed character remaining.)"
		elif c == "connect":
			text = "Waiting for Opponent to join."
			self.sd["text"]["close"].text = "Disconnect"
		elif "no_internet" in c:
			text = "Cannot connect to serve.\nPlease try again later."
		elif "roomdis" in c:
			text = "There was an error joining the room.\nPlease try again later."
		elif "waiting" in c:
			if "opp" in c:
				text = "Found a room.\n Waiting for Opponent..."
			elif "ser" in c:
				text = "Connecting to server..."
			else:
				text = "Waiting for Opponent..."
		elif "LookOpp" in c:
			text = "Opponent is looking at your hand"
		elif "making" in c:
			text = "Waiting for to create room..."
		elif "Loading" in c:
			text = "Loading..."
		elif "mstock" in c:
			text = "Choose a card with markers to pay the cost."
		elif "Main" in c or "do" in c:
			if not self.gd["payed"]:
				status = self.gd["pay_status"]
			else:
				status = self.gd["status"]
			if "Select" in status:
				if len(self.gd["select_btns"]) > 0:
					if self.gd["uptomay"]:
						upto = "up to "
					else:
						upto = ""

					e = ""
					n = ""
					o = ""
					if "Opp" in status:
						e += " opponent's"
					if "Other" in status:
						o += "other "

					if "NameSet" in status:
						names = status.split("_")[1:-1]
						n = " with "
						for nn in range(int(len(names) / 2)):
							if nn == 0:
								n += f"\"{names[nn]}\""
							else:
								n += f" or \"{names[nn]}\""
						n += " in it's card name"
					elif "Name=" in status:
						e += f" \"{status.split('_')[-2]}\""
					elif "Name" in status:
						n += f" with \"{status.split('_')[-2]}\" in it's card name"
					elif "Text" in status:
						names = status.split("_")[1:-1]
						if len(names[0]) < 15:
							n += f" with \"{names[0].replace('] ', '')}\""
						else:
							n += f" with \"{names[0]}\""

					if "Stand" in status:
						e += " STAND"
					if "Trait" in status:
						trs = status.split("_")[1:-1]
						status = status.split("_")[-1]
						if self.gd["btrait"][0]:
							e = f" «{trs[0]}»"
							e1 = f" «{trs[1]}»"
						else:
							if len(trs) == 1 and trs[0] == "":
								n += " with no traits"
							else:
								for tr in range(len(trs)):
									if tr > 0:
										e += f" or «{trs[tr]}»"
									else:
										e += f" «{trs[tr]}»"
					if "Level" in status:
						if "Level<=" in status:
							e += f" level {status[status.index('Level<=') + 7]} or lower"
						elif "Level>=" in status:
							e += f" level {status[status.index('Level>=') + 7]} or higher"
					if "Cost" in status:
						if "Cost<=" in status:
							e += f" cost {status[status.index('Cost<=') + 6]} or lower"
						elif "Cost>=" in status:
							e += f" cost {status[status.index('Cost>=') + 6]} or higher"

					if "Center" in status:
						e += " center stage"
					elif "Back" in status:
						e += " back stage"
					if "Opposite" in status:
						text = f"Choose the character opposite this cards."
					elif "revive" in self.gd["effect"]:
						text = f"Choose {upto}{status[-1]} positions of your stage."
					elif "backatk" in self.gd["effect"]:
						text = f"Choose {upto}{status[-1]} of your{e} {o}characters to attack."
					elif "Climax" in status:
						text = f"Choose {upto}{status[-1]} climax in your{e} climax area."
					else:
						if self.gd["btrait"][0]:
							text = f"Choose 1 of your{e} characters{n} and 1 of your{e1} {o}characters{n}."
						else:
							text = f"Choose {upto}{status[-1]} of your{e} {o}characters{n}."
				else:
					text = "There are no target to choose."
					self.gd["notarget"] = True
		elif "Move" in c:
			if len(self.gd["select_btns"]) > 0:
				d = ""
				e = ""
				s = ""
				if "seperate" in self.gd["effect"]:
					s = "seperate "
				if "Opp" in self.gd["status"] and self.gd["rev"]:
					e += ""
				elif "Opp" in self.gd["status"]:
					e += " opponent's"
				if "Center" in self.gd["status"]:
					e += " center"
				elif "Back" in self.gd["status"]:
					e += " back"
				if "Open" in self.gd["status"]:
					d = "n open"
				if "Clock" in self.gd["status"]:
					text = f"Put up to {self.gd['status'][-1]} card from the top of your clock into your waiting room"
				else:
					text = f"Choose a{d} {s}position in your{e} stage."
			else:
				if "Clock" in self.gd["status"]:
					text = "There are no cards in your clock."
				else:
					text = "There are no position in stage to choose."
				self.gd["notargetfield"] = True

		# pos = (self.sd["padding"] / 2., self.sd["padding"] * 1.5 + self.sd["card"][1] / 2. + self.sd["padding"] * 5)

		self.sd["text"]["label"].text = text
		self.sd["text"]["label"].texture_update()

		yscat += self.sd["text"]["label"].texture.size[1]

		# self.sd["text"]["sct"].size = (xscat, yscat)
		self.sd["text"]["popup"].size = (xscat + self.sd["padding"] * 2, yscat + self.sd["padding"] * 2)
		# self.sd["text"]["popup"].size = (xscat*1.05, yscat*1.05)

		# self.sd["text"]["sct"].center = self.sd["text"]["popup"].center

		if "waiting" not in c and "making" not in c and "Loading" not in c:
			self.sd["text"]["close"].center_x = xscat / 2.
			self.sd["text"]["close"].y = self.sd["padding"] * 1.5
			self.sd["text"]["label"].y = self.sd["padding"] * 3.5 + self.sd["card"][1] / 2.
		else:
			self.sd["text"]["label"].y = self.sd["padding"] * 3
			self.sd["text"]["close"].y = -Window.height

		# if self.net["game"] and c == "waiting":
		# 	if self.gd["turn"] > 0 and not any(p in self.gd["phase"] for p in ("Mulligan", "Janken")):
		# 		self.sd["text"]["close"].center_x = xscat / 2.
		# 		self.sd["text"]["close"].y = self.sd["padding"] * 1.5
		# 		self.sd["text"]["close"].text = "Show Field"
		# 		self.sd["text"]["label"].y = self.sd["padding"] * 3.5 + self.sd["card"][1] / 2.
		self.sd["text"]["label"].x = self.sd["padding"] / 2

		self.sd["text"]["popup"].open()

	def popup_start(self, dt=0, o="1", c="", m="", l="", t=None):
		self.multi_info["popup"].dismiss()
		self.sd["text"]["popup"].dismiss()
		self.cardinfo.dismiss()
		self.popup_clr_button()
		if self.infob is not None:
			self.infob.cancel()
			self.infob = None
		if self.infot is not None:
			self.infot.cancel()
			self.infot = None
		# self.sd["popup"]["popup"].dismiss()
		if self.gd["confirm_var"]:
			self.gd["confirm_temp"] = dict(self.gd["confirm_var"])
			for key in self.gd["confirm_var"]:
				if "o" in key:
					o = self.gd["confirm_var"][key]
				elif "c" in key:
					c = self.gd["confirm_var"][key]
				elif "m" in key:
					m = self.gd["confirm_var"][key]
				elif "l" in key:
					l = self.gd["confirm_var"][key]
				elif "t" in key:
					t = self.gd["confirm_var"][key]
			self.gd["confirm_var"] = {}

		self.gd["p_c"] = c
		self.gd["p_t"] = t
		self.gd["p_owner"] = o
		self.gd["popup_done"] = (True, False)
		self.gd["popup_on"] = True
		self.sd["popup"]["popup"].auto_dismiss = False
		self.gd["chosen"] = []
		self.gd["p_select"] = []
		self.gd["p_over"] = False
		self.gd["p_f"] = True
		self.gd["p_min_s"] = -1

		if not m:
			# set max cards selectable
			if self.gd["p_c"] == "Clock" or self.gd["p_c"] == "Level":
				self.gd["p_max_s"] = 1
			elif self.gd["p_c"] == "Hand":
				self.gd["p_max_s"] = len(self.pd[self.gd["active"]]["Hand"]) - hand_limit
			else:
				self.gd["p_max_s"] = hand_limit
		elif isinstance(m,list):
			if "stack" in self.gd["p_c"] and "stacked" not in self.gd["p_c"]:
				self.gd["p_max_s"] = sorted(m, reverse=True)[0]
				self.gd["p_min_s"] = sorted(m, reverse=False)[0]
		else:
			self.gd["p_max_s"] = m

		if "Stage" in self.gd["effect"] and self.gd["p_max_s"] > 1:
			self.gd["p_stage"] = int(self.gd["p_max_s"])
			self.gd["p_max_s"] = 1

		if not l:
			self.gd["p_look"] = 1
		else:
			self.gd["p_look"] = l

		if "Levelup" in self.gd["p_c"]:
			self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Clock"][:7])
		elif "Search" in self.gd["p_c"]:
			if "Reveal" in self.gd["p_c"]:
				self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Res"])
			else:
				self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Library"])
		elif "Salvage" in self.gd["p_c"]:
			if "Memory" in self.gd["p_c"]:
				self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Memory"])
			elif "Clock" in self.gd["p_c"]:
				self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Clock"])
			else:
				self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Waiting"])
		elif "Shuffle" in self.gd["p_c"]:
			self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Waiting"])
		elif "Counter" in self.gd["p_c"]:
			self.gd["p_l"] = list(self.gd["counter"])
		elif "Look" in self.gd["p_c"]:
			if "fix" in self.gd["p_c"]:
				if len(self.gd["p_l"]) > 0:
					pass
				else:
					self.gd["p_l"] = self.pd[self.gd["p_owner"]]["Library"][-self.gd["p_look"]:]
			elif self.gd["uptomay"]:
				if self.gd["p_t"]:
					self.gd["p_l"] = list(self.gd["p_t"])
					self.gd["p_t"] = []
				else:
					self.gd["p_l"] = []
			else:
				self.gd["p_l"] = self.pd[self.gd["p_owner"]]["Library"][-self.gd["p_look"]:]
		elif "Add" in self.gd["p_c"]:
			self.decks["add_chosen"] = []
		elif "Image" in self.gd["p_c"]:
			self.sd["btn"]["Addcls_btn"].y = -Window.height * 2
			self.decks["imgs"] = []
			for card in self.decks["dbuild"]["deck"].keys():
				self.decks["imgs"].append(card)
			# self.decks["imgs"] = [sc[d]["img"] for d in self.decks["dbuild"]["deck"]]
			# # self.decks["imgs"].append("empty")
			# for i in range(len(self.decks["imgs"])):
			# 	if "." in self.decks["imgs"][i]:
			# 		self.decks["imgs"][i] = self.decks["imgs"][:-4]
			self.gd["p_l"] = self.gd["p_ld"][:len(self.decks["imgs"])]
			self.decks["img_pop"] = True
		elif "Clock" in self.gd["p_c"] and "Discard" in self.gd["phase"]:
			self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Clock"])
		elif "Level" in self.gd["p_c"]:
			self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Level"])
		elif "Memory" in self.gd["p_c"]:
			self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Memory"])
		else:
			self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Hand"])

		self.gd["p_width"] = self.sd["card"][0] + self.sd["padding"]  # * self.gd["p_pad"]
		self.gd["p_height"] = self.sd["card"][1] + self.sd["padding"]  # * 1.25

		self.gd["p_title"] = self.sd["popup"]["popup"].title_size + self.sd["popup"]["popup"].separator_height + \
		                     self.sd["card"][1] / 3 + \
		                     self.sd["padding"] * 2

		self.popup_filter()
		if self.gd["p_c"] == "Hand" or self.gd["p_c"] == "Levelup":
			self.sd["btn"][f"{self.gd['p_c']}_btn"].disabled = True
		self.sd["popup"]["popup"].open()

	def popup_pl(self, phase):
		p_l = []
		if self.gd["p_f"] and any(s in self.gd["p_c"] for s in ("Search", "Salvage", "Encore", "Discard")):
			self.gd["p_f"] = False
			if "Search" in self.gd["p_c"]:
				if "Reveal" in self.gd["p_c"]:
					p_l = list(self.pd[self.gd["p_owner"]]["Res"])
				else:
					p_l = list(self.pd[self.gd["p_owner"]]["Library"])
			elif "Salvage" in self.gd["p_c"]:
				if "Memory" in self.gd["p_c"]:
					p_l = list(self.pd[self.gd["p_owner"]]["Memory"])
				elif "Clock" in self.gd["p_c"]:
					p_l = list(self.pd[self.gd["p_owner"]]["Clock"])
				else:
					p_l = list(self.pd[self.gd["p_owner"]]["Waiting"])
			elif "Encore" in self.gd["p_c"]:
				p_l = list(self.pd[self.gd["p_owner"]]["Hand"])
			elif "Discard" in self.gd["p_c"]:
				if "Memory" in self.gd["p_c"]:
					p_l = list(self.pd[self.gd["p_owner"]]["Memory"])
				elif "Level" in self.gd["p_c"]:
					p_l = list(self.pd[self.gd["p_owner"]]["Level"])
				elif "Clock" in self.gd["p_c"]:
					p_l = list(self.pd[self.gd["p_owner"]]["Clock"])
				else:
					p_l = list(self.pd[self.gd["p_owner"]]["Hand"])

			if "Character" in self.gd["search_type"] or "Climax" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if self.cd[s].card in self.gd["search_type"]]
			elif "ID=" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if any(name == s for name in self.gd["search_type"].split("_")[1:])]
			elif "Bond" in self.gd["search_type"] or "Name=" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if
				                  any(name == self.cd[s].name for name in self.gd["search_type"].split("_")[1:])]
			elif "Card" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if self.cd[s].mcolour.lower() in self.gd["search_type"].split("_")]
			elif "NameSet" in self.gd["search_type"]:
				names = self.gd["search_type"].split("_")[1:]
				sets = names[int(len(names) / 2):]
				for setn in sets:
					if setn in names:
						names.remove(setn)
				self.gd["p_l"] = [s for s in p_l if
				                  any(name in self.cd[s].name and any(
						                  setid in s for setid in se["neo"]["Title"][setn[names.index(name)]]) for name
				                      in names)]
			elif "Name" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if
				                  any(name in self.cd[s].name for name in self.gd["search_type"].split("_")[1:])]
			elif "Text" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if any(
						any(txt.lower() in text.lower() for txt in self.gd["search_type"].split("_")[1:]) for text in
						self.cd[s].text_o)]
			elif "NCost" in self.gd["search_type"]:
				nc = self.gd["search_type"].split("_")
				if "<=" in nc[2]:
					self.gd["p_l"] = [s for s in p_l if
					                  "Character" in self.cd[s].card and self.cd[s].cost_t <= int(nc[2][-1]) and nc[
						                  1] in self.cd[s].name]
			elif "LevCost" in self.gd["search_type"]:
				lc = self.gd["search_type"].split("_")
				if lc[1] == "<=p":
					self.gd["p_l"] = [s for s in p_l if
					                  "Character" in self.cd[s].card and self.cd[s].level_t <= len(
							                  self.pd[self.gd["p_owner"]]["Level"]) and self.cd[s].cost_t <= int(
							                  lc[2][-1])]
			elif "Cost" in self.gd["search_type"]:
				if "<=" in self.gd["search_type"]:
					self.gd["p_l"] = [s for s in p_l if
					                  self.cd[s].cost_t <= int(self.gd["search_type"][-1]) and "Character" in
					                  self.cd[s].card]
				elif ">=" in self.gd["search_type"]:
					self.gd["p_l"] = [s for s in p_l if
					                  self.cd[s].cost_t >= int(self.gd["search_type"][-1]) and "Character" in
					                  self.cd[s].card]
			elif "TraitL" in self.gd["search_type"]:
				level = self.gd["search_type"].split("_")[-1]
				trait = self.gd["search_type"].split("_")[1:-1]
				if "<=p" in level:
					self.gd["p_l"] = [s for s in p_l if
					                  self.cd[s].level_t <= len(self.pd[self.gd["p_owner"]]["Level"]) and any(
							                  tr in self.cd[s].trait_t for tr in trait)]
				elif "<=" in level:
					self.gd["p_l"] = [s for s in p_l if
					                  self.cd[s].level_t <= int(level[-1]) and any(
							                  tr in self.cd[s].trait_t for tr in trait)]
				elif ">=" in level:
					self.gd["p_l"] = [s for s in p_l if
					                  self.cd[s].level_t >= int(level[-1]) and any(
							                  tr in self.cd[s].trait_t for tr in trait)]
				elif "=" in level:
					self.gd["p_l"] = [s for s in p_l if
					                  self.cd[s].level_t == int(level[-1]) and any(
							                  tr in self.cd[s].trait_t for tr in trait)]
			elif "TraitN" in self.gd["search_type"]:
				name = self.gd["search_type"].split("_")[-1]
				trait = self.gd["search_type"].split("_")[1]
				if "or" in self.gd["effect"]:
					self.gd["p_l"] = [s for s in p_l if trait in self.cd[s].trait_t or name in self.cd[s].name]
				else:
					self.gd["p_l"] = [s for s in p_l if trait in self.cd[s].trait_t and name in self.cd[s].name]
			elif "Trait" in self.gd["search_type"]:
				if self.gd["search_type"].split("_")[1:] == [""]:
					self.gd["p_l"] = [s for s in p_l if len(self.cd[s].trait_t) <= 0 and "Character" in self.cd[s].card]
				else:
					self.gd["p_l"] = [s for s in p_l if any(
							trait in self.cd[s].trait_t for trait in self.gd["search_type"].split("_")[1:])]
			elif "CLevelN" in self.gd["search_type"]:
				name = self.gd["search_type"].split("_")[-1]
				level = self.gd["search_type"].split("_")[1]
				if "_standby" in level:
					self.gd["p_l"] = [s for s in p_l if
					                  "Character" in self.cd[s].card and name in self.cd[s].name and self.cd[
						                  s].level <= len(self.pd[self.gd["p_owner"]]["Level"]) + 1]
			elif "CLevel" in self.gd["search_type"]:
				if "_standby" in self.gd["search_type"]:
					self.gd["p_l"] = [s for s in p_l if
					                  "Character" in self.cd[s].card and self.cd[s].level_t <= len(
							                  self.pd[self.gd["p_owner"]]["Level"]) + 1]
				elif "<=" in self.gd["search_type"]:
					self.gd["p_l"] = [s for s in p_l if
					                  self.cd[s].level_t <= int(self.gd["search_type"][-1]) and "Character" in
					                  self.cd[s].card]
				elif ">=" in self.gd["search_type"]:
					self.gd["p_l"] = [s for s in p_l if
					                  self.cd[s].level_t >= int(self.gd["search_type"][-1]) and "Character" in
					                  self.cd[s].card]
			else:
				self.gd["p_l"] = p_l

			self.sd["btn"]["show_all_btn"].text = "Show All"

			if len(self.gd["p_l"]) <= 0:
				self.gd["notarget"] = True
				# self.gd["p_f"] = True
				# self.sd["btn"]["show_all_btn"].text = self.gd["search_type"].split("_")[0].upper()
				self.sd["btn"][f"{phase}_btn"].disabled = False
			else:
				self.gd["notarget"] = False
		elif not self.gd["p_f"] and any(s in self.gd["p_c"] for s in ("Search", "Salvage", "Encore", "Discard")):
			self.gd["p_f"] = True
			self.sd["btn"][
				"show_all_btn"].text = "Filter"  # self.gd["search_type"].split("_")[0].upper().replace("=","")
			if "Search" in self.gd["p_c"]:
				if "Reveal" in self.gd["p_c"]:
					self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Res"])
				else:
					self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Library"])
			elif "Salvage" in self.gd["p_c"]:
				if "Memory" in self.gd["p_c"]:
					self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Memory"])
				elif "Clock" in self.gd["p_c"]:
					self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Clock"])
				else:
					self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Waiting"])
			elif "Encore" in self.gd["p_c"]:
				self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Hand"])
			elif "Discard" in self.gd["p_c"]:
				if "Memory" in self.gd["p_c"]:
					self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Memory"])
				elif "Level" in self.gd["p_c"]:
					self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Level"])
				elif "Clock" in self.gd["p_c"]:
					self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Clock"])
				else:
					self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Hand"])

	def popup_filter(self, *args):
		self.sd["popup"]["p_scv"].do_scroll_y = False
		self.gd["chosen"] = []
		self.gd["p_select"] = []

		self.sd["popup"]["stack"].clear_widgets()
		if "_" in self.gd["p_c"]:
			phase = self.gd["p_c"].split("_")[0]
		else:
			phase = self.gd["p_c"]

		if "Image" not in self.gd["p_c"]:
			self.pop_btn_disable(phase)

			if "Add" in self.gd["p_c"]:
				self.filter_deck_add()
				if len(self.decks["add_chosen"]) > 0:
					self.sd["btn"]["Add_btn"].disabled = False
				else:
					self.sd["btn"]["Add_btn"].disabled = True
			else:
				self.popup_pl(phase)
		self.gd["p_rows"] = 0
		if starting_hand < len(self.gd["p_l"]) <= 7:
			self.gd["p_hand"] = len(self.gd["p_l"])
		elif len(self.gd["p_l"]) > starting_hand:
			self.gd["p_hand"] = int(popup_max_cards)
			self.gd["p_rows"] = int(ceil(len(self.gd["p_l"]) / float(popup_max_cards)))
		else:
			self.gd["p_hand"] = int(starting_hand)

		if self.gd["p_rows"] > 6:
			self.sd["popup"]["p_scv"].do_scroll_y = True
			self.gd["p_yscv"] = self.gd["p_height"] * (self.gd["p_rows"] - 0.5)
			self.gd["p_yssct"] = self.gd["p_height"] * (self.gd["p_rows"] + 0)
		elif self.gd["p_rows"] > 0:
			self.gd["p_yscv"] = self.gd["p_height"] * (self.gd["p_rows"] + 0)
			self.gd["p_yssct"] = self.gd["p_height"] * (self.gd["p_rows"] + 0)
		else:
			self.gd["p_yscv"] = self.gd["p_height"] + self.sd["padding"]
			self.gd["p_yssct"] = self.gd["p_height"]

		self.gd["p_title"] = self.sd["popup"]["popup"].title_size + self.sd["popup"]["popup"].separator_height

		if "Add" in self.gd["p_c"]:
			self.gd["p_title"] += self.sd["card"][1] + self.sd["padding"]
		elif any(s in self.gd["p_c"] for s in ("Search", "Salvage", "Encore")) or (
				"Discard" in self.gd["p_c"] and self.gd["search_type"]):
			self.gd["p_title"] += self.sd["card"][1] / 3 + self.sd["padding"] * 2

		self.gd["p_yscat"] = self.gd["p_yscv"] + self.sd["card"][1] / 2. + self.gd["p_title"] + self.gd["p_height"]

		if "Add" in self.gd["p_c"]:
			self.gd["p_xscat"] = self.sd["padding"] * 4 + self.gd["p_width"] * popup_max_cards
		else:
			self.gd["p_xscat"] = self.sd["padding"] * 4 + self.gd["p_width"] * self.gd["p_hand"]

		self.sd["btn"]["label"].text = ""
		self.sd["btn"]["label"].halign = "left"
		pos = (0, 0)

		if self.gd["notarget"] and not self.gd["p_f"]:
			self.sd["btn"]["label"].halign = "center"
			self.sd["btn"]["label"].text = "There are no target to choose from."

			pos = (self.sd["padding"] * 1,
			       self.sd["padding"] * 6.5 + self.sd["card"][1] / 2)
		# self.sd["btn"][f"{phase}_btn"].y + self.sd["btn"][f"{phase}_btn"].size[1] +
		# self.sd["padding"] * 5)

		elif "Look" in self.gd["p_c"] and "top" in self.gd["effect"] and (
				"bottom" in self.gd["effect"] or "Waiting" in self.gd["effect"]):
			# if  and "bottom" in self.gd["effect"]:
			if "opp" in self.gd["effect"]:
				self.sd["btn"]["label"].text = "Choose where to put the top card of your opponent's deck."
			else:
				self.sd["btn"]["label"].text = "Choose where to put the top card of your deck."
			pos = (self.sd["padding"] * 1.5, self.sd["padding"] * 5.5 + self.sd["card"][1] * 2)
		# self.gd["p_yscat"] += self.sd["padding"] * 1.5 + self.sd["card"][1] / 2. + \
		#                       self.sd["btn"]["label"].size[1]
		elif "Look" in self.gd["p_c"] and self.gd["p_look"] >= 1 and self.gd["p_max_s"] >= 1:
			if self.gd["uptomay"]:
				upto = "up to "
			else:
				upto = ""
			if "hand" in self.gd["p_c"]:
				if "fix" in self.gd["p_c"]:
					fix = ""
				else:
					fix = "up to "

				if "show" in self.gd["effect"]:
					tr = self.gd["effect"][self.gd["effect"].index("hand") + 2].split("_")
					c = ""

					if "TraitN" in tr:
						c = f"«{tr[1]}» or \"{tr[2]}\" in its card name"
					elif "Trait" in tr:
						if len(tr) == 3:
							c = f"«{tr[1]}» or «{tr[2]}» character"
						else:
							c = f"«{tr[1]}» character"
					else:
						c = "card"
					if self.gd['p_max_s'] > 1:
						cc = "them"
					else:
						cc = "it"
					self.sd["btn"][
						"label"].text = f"Look at {fix}{self.gd['p_look']} cards from top of your deck. Choose {upto}{self.gd['p_max_s']} {c}, reveal {cc}, and put it in your hand, and put the rest in the waiting room."
				else:
					if "stacked" in self.gd["effect"]:
						self.sd["btn"][
							"label"].text = f"Choose {upto}{self.gd['p_max_s']} face down stack of cards and put them in your hand. Return the rest into your deck, and shuffle your deck."
					else:
						self.sd["btn"][
						"label"].text = f"Look at {fix}{self.gd['p_look']} cards from top of your deck. Choose {upto}{self.gd['p_max_s']} of them and put it in your hand, and put the rest in the waiting room."
			elif "waiting" in self.gd["p_c"]:
				if "all" in self.gd["effect"]:
					upto = ""
				opp = ""
				if "opp" in self.gd["effect"]:
					opp = "opponets's "
				self.sd["btn"][
					"label"].text = f"Look at up to {self.gd['p_look']} cards from top of your {opp}deck. Choose {upto}{self.gd['p_max_s']} of them and put it in your {opp}waiting room."
			elif "bdeck" in self.gd["p_c"]:
				opp = ""
				if "opp" in self.gd["effect"]:
					opp = "opponets's "
				self.sd["btn"][
					"label"].text = f"Look at the top {self.gd['p_look']} cards of your {opp}deck. Choose {upto}{self.gd['p_max_s']} of them and put it on the bottom your {opp}deck."
			elif "reorder" in self.gd["p_c"] and "fix" in self.gd["p_c"]:
				self.sd["btn"][
					"label"].text = f"Look at the top {(self.gd['p_look'])} cards of your deck, and put them on the top of your deck in any order."
			elif "reorder" in self.gd["p_c"]:
				self.sd["btn"][
					"label"].text = f"Look at up to {self.gd['p_look']} cards from top of your deck, and put them on the top of your deck in any order."
			elif "stack" in self.gd["p_c"]:
				# if len(self.gd["effect"][self.gd["effect"].index("stack")+1])
				self.sd["btn"]["label"].text = f"Choose {self.gd['p_min_s']} or {self.gd['p_max_s']} cards to add into the first stacks of cards. The rest will make the other stack of cards."
			elif "look" in self.gd["p_c"]:
				self.sd["btn"][
					"label"].text = f"Look at up to {self.gd['p_look']} cards from top of your deck, and put them back in the same order."
			else:
				self.sd["btn"][
					"label"].text = f"Look at up to {self.gd['p_look']} cards from top of your deck. Choose {upto}{self.gd['p_max_s']} of them and put it on top of the deck, and put the rest in the waiting room."
			if "fix" in self.gd["p_c"] and ("top" in self.gd["effect"] or "stack" in self.gd["effect"] or "stacked" in self.gd["effect"]) and self.gd["p_look"] >= 1 and self.gd["p_max_s"] > 0:
				pos = (self.sd["padding"] * 0.5, self.sd["padding"] * 2 + self.sd["card"][1] * 2)
				self.gd["p_yscat"] -= self.sd["card"][1] / 2.
			else:
				pos = (self.sd["padding"] * 0.5, self.sd["padding"] * 7 + self.sd["card"][1] * 2)
		# self.gd["p_yscat"] += self.sd["padding"] * 1.5 + self.sd["card"][1] / 2. + \
		#                       self.sd["btn"]["label"].size[1]

		if self.sd["btn"]["label"].text != "":
			self.sd["btn"]["label"].text_size = (self.gd["p_xscat"] * 0.9, None)
			self.sd["btn"]["label"].texture_update()
			self.sd["btn"]["label"].size = self.sd["btn"]["label"].texture.size
			self.sd["btn"]["label"].pos = pos

			if not self.gd["notarget"]:
				self.gd["p_yscat"] += self.sd["padding"] * 2 + self.sd["card"][1] / 2. + \
				                      self.sd["btn"]["label"].size[1]
		else:
			self.sd["btn"]["label"].x = -Window.width

		if "Image" in self.gd["p_c"]:
			self.gd["p_ypop"] = self.gd["p_title"] + self.gd["p_height"] + self.gd["p_yscv"]
		else:
			self.gd["p_ypop"] = self.gd["p_yscat"]

		if self.gd["p_ypop"] > Window.height:
			self.gd["p_over"] = True
			self.gd["p_ypop"] = Window.height * 0.9
			self.gd["p_yscat"] = self.gd["p_ypop"] - self.gd["p_title"]
			self.gd["p_yscv"] = self.gd["p_yscat"] - self.sd["card"][1] * 0.75 - self.sd["padding"]
			if "Add" in self.gd["p_c"]:
				r = (self.gd["p_yscv"] - self.sd["card"][1]) % self.gd["p_height"] / self.gd["p_height"]
				if r > 0.25:
					r = 0.25
					self.sd["p_over"] = r
				self.gd["p_rows"] = int(self.gd["p_yscv"] / self.gd["p_height"]) + r
				self.gd["p_yscv"] -= self.sd["card"][1] - self.gd["p_height"] * r

		# self.sd["popup"]["p_sct"].size = (self.gd["p_xscat"], self.gd["p_yscat"])
		self.sd["popup"]["p_scv"].size = (self.gd["p_xscat"], self.gd["p_yscv"])
		self.sd["popup"]["popup"].size = (self.gd["p_xscat"], self.gd["p_ypop"])

		if "sspace" in self.gd["p_l"]:
			self.gd["p_l"].remove("sspace")

		if "Add" in self.gd["p_c"]:
			nx, ns = self.get_index_stack(self.gd["p_l"], popup_max_cards)
		elif "stacked" in self.gd["p_c"]:
			nx, ns = self.get_index_stack(self.gd["stacked"]["0"], self.gd["p_hand"])
		else:
			nx, ns = self.get_index_stack(self.gd["p_l"], self.gd["p_hand"])
		if nx:
			if "stacked" in self.gd["p_c"]:
				self.gd["p_l"].insert(0, "sspace")
			else:
				self.gd["p_l"].insert(nx, "sspace")
			if ns > 1:
				if ns % 1 > 0:
					nss = int(ns)
				else:
					nss = int(ns) - 1
			else:
				nss = 0
			self.sd["popup"]["sspace"].size = (self.sd["card"][0] * ns + self.sd["padding"] * nss, self.sd["card"][1])
		c = 0
		for inx in range(len(self.gd["p_l"])):
			ind = self.gd["p_l"][inx]
			if "sspace" in ind:
				try:
					self.sd["popup"]["stack"].add_widget(self.sd["popup"][ind])
				except WidgetException:
					pass
				c += 1
			else:
				if c:
					inx -= 1
				if "Add" in self.gd["p_c"]:
					self.cpop[ind].import_data(sc[self.gd["p_fcards"][inx]])
					if self.gd["p_fcards"][inx] in self.decks["add_chosen"]:
						self.cpop[ind].selected()
					else:
						self.cpop[ind].selected(False)
				elif "Image" in self.gd["p_c"]:
					self.cpop[ind].import_data(sc[self.decks["imgs"][inx]])
					self.cpop[ind].selected(False)
				else:
					if "Stage" in self.gd["effect"] and ind in self.gd["target"]:
						self.cpop[ind].stage_slc()
						for r in range(select2cards):
							if self.field_btn[f"stage{r}{ind[-1]}s"].x < 0 and self.field_btn[
									f"stage{r}{ind[-1]}s"].y < 0:  # (-Window.width * 2, -Window.height * 2):
								self.field_btn[f"stage{r}{ind[-1]}s"].pos = (
								self.mat[ind[-1]]["field"][self.gd["target"][self.gd["target"].index(ind) + 1]][0] -
								self.sd["padding"],
								self.mat[ind[-1]]["field"][self.gd["target"][self.gd["target"].index(ind) + 1]][1] -
								self.sd["padding"])
								break
					else:
						self.cpop[ind].selected(False)
				if "_look" in self.gd["p_c"]:
					if inx == 0:
						self.cpop[ind].update_text("Top", .5)
					elif (inx + 1) % 10 == 1:
						self.cpop[ind].update_text(f"{inx + 1}st", .5)
					elif (inx + 1) % 10 == 2:
						self.cpop[ind].update_text(f"{inx + 1}nd", .5)
					elif (inx + 1) % 10 == 3:
						self.cpop[ind].update_text(f"{inx + 1}rd", .5)
					else:
						self.cpop[ind].update_text(f"{inx + 1}th", .5)
				else:
					self.cpop[ind].update_text()

				if "stacked" in self.gd["p_c"]:
					if any(self.cpop[sind] in self.sd["popup"]["stack"].children for sind in self.gd["stacked"]["0"][self.gd["stacked"][ind]]):
						continue
					else:
						self.sd["popup"]["stack"].add_widget(self.cpop[ind])
						self.cpop[ind].update_text(f"{len(self.gd['stacked']['0'][self.gd['stacked'][ind]])}")
						self.cpop[ind].show_back()
				else:
					self.sd["popup"]["stack"].add_widget(self.cpop[ind])

		if "Image" not in self.gd["p_c"]:
			self.sd["popup"]["p_scv"].y = self.sd["padding"] * 3 + self.sd["card"][1] / 2
			if "Look" in self.gd["p_c"] and "top" in self.gd["effect"] and "fix" not in self.gd["p_c"]:
				self.sd["popup"]["p_scv"].y += self.sd["padding"] * 1.5 + self.sd["btn"]["top_btn"].size[1]

			if self.gd["ability_trigger"]:
				self.sd["btn"]["show_info_btn"].size = (self.sd["card"][1] / 3, self.sd["card"][1] / 3)
				self.sd["btn"]["show_info_btn"].y = self.gd["p_ypop"] - self.sd["btn"]["show_info_btn"].size[1] * 2 - \
				                                    self.sd["padding"] * 1.5
				# self.sd["btn"]["show_info_btn"].y = self.gd["p_yscat"] - self.sd["padding"] * 2
				self.sd["btn"]["show_info_btn"].x = self.gd["p_xscat"] - self.sd["card"][1] / 3 * 2 - self.sd["padding"]

			if any(item in self.gd["p_c"] for item in ("Search", "Salvage", "Encore")) or (
					"Discard" in self.gd["p_c"] and self.gd["search_type"]):
				self.sd["btn"]["show_all_btn"].size = (self.sd["card"][0] * 2, self.sd["card"][1] / 3.)
				self.sd["btn"]["show_all_btn"].y = self.sd["popup"]["p_scv"].y + self.sd["popup"]["p_scv"].size[1] + \
				                                   self.sd["padding"]
				self.sd["btn"]["show_all_btn"].center_x = self.gd["p_xscat"] / 2 - self.sd["card"][0] / 2 + self.sd[
					"padding"] * 0.75
		else:
			self.sd["popup"]["p_scv"].y = self.sd["padding"] * 1.5
			self.sd["btn"]["filter_add"].y = -Window.height * 2
			self.sd["btn"]["Add_btn"].y = -Window.height * 2

		self.sd["popup"]["p_scv"].scroll_y = 1

		if "Image" not in self.gd["p_c"]:
			self.sd["btn"][f"{phase}_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
			self.sd["btn"][f"{phase}_btn"].y = self.sd["padding"] * 1.5
			if phase in phases:
				self.sd["btn"][f"{phase}_btn"].text = f"End {phase}"
			else:
				self.sd["btn"][f"{phase}_btn"].text = "End Effect"  # f"End {phase}" #phase

			if self.gd["p_c"] == "Add":
				self.sd["btn"]["filter_add"].y = self.gd["p_yscv"] + self.sd["padding"] * 1 + self.sd["popup"][
					"p_scv"].y
				if len(self.gd["p_l"]) > 1:
					self.sd["btn"][f"{phase}_btn"].text = f"Add cards"
				else:
					self.sd["btn"][f"{phase}_btn"].text = f"Add card"
				self.sd["btn"][f"{phase}_btn"].center_x = self.gd["p_xscat"] / 4 * 3 - self.sd["card"][0] / 2 + \
				                                          self.sd["padding"]
				self.sd["btn"][f"{phase}cls_btn"].center_x = self.gd["p_xscat"] / 4 - self.sd["card"][0] / 2 + \
				                                             self.sd["padding"]
				self.sd["btn"][f"{phase}cls_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
				self.sd["btn"][f"{phase}cls_btn"].y = self.sd["padding"] * 1.5
			else:
				self.sd["btn"][f"{phase}_btn"].center_x = self.gd["p_xscat"] / 4. * 3 - self.sd["card"][0] / 2 + \
				                                          self.sd["padding"]

			if any(item in self.gd["p_c"] for item in
			       ("Clock", "Level", "Hand", "Search", "Salvage", "Counter", "Encore", "Discard", "Marker")):
				self.sd["btn"]["field_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
				self.sd["btn"]["field_btn"].y = self.sd["padding"] * 1.5
				self.sd["btn"]["field_btn"].center_x = self.gd["p_xscat"] / 4. - self.sd["card"][0] / 2 + self.sd[
					"padding"]
			elif self.gd["p_c"] == "Mulligan":
				self.sd["btn"][f"{phase}_btn"].text = f"End {phase}"
				self.sd["btn"]["M_all_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
				self.sd["btn"]["M_all_btn"].y = self.sd["padding"] * 1.5
				self.sd["btn"]["M_all_btn"].center_x = self.gd["p_xscat"] / 4. - self.sd["card"][0] / 2 + self.sd[
					"padding"]
			elif "Look" in self.gd["p_c"]:
				self.sd["btn"]["field_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
				self.sd["btn"]["field_btn"].y = self.sd["padding"] * 1.5
				self.sd["btn"]["field_btn"].center_x = self.gd["p_xscat"] / 4. - self.sd["card"][0] / 2 + \
				                                       self.sd["padding"]
				# self.sd["popup"]["p_scv"].y = self.sd["padding"] * 2 + self.sd["btn"]["field_btn"].size[1]
				if "top" in self.gd["effect"] and ("bottom" in self.gd["effect"] or "Waiting" in self.gd[
					"effect"]):  # and "bottom" in self.gd["effect"]
					self.sd["btn"][f"{self.gd['p_c']}_btn"].y = -Window.height
					self.sd["btn"]["field_btn"].center_x = self.gd["p_xscat"] / 2. - self.sd["card"][0] / 2 + \
					                                       self.sd["padding"]
					self.sd["btn"]["top_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
					self.sd["btn"]["top_btn"].center_x = self.gd["p_xscat"] / 4. - self.sd["card"][0] / 2 + self.sd[
						"padding"]
					self.sd["btn"]["top_btn"].y = self.sd["padding"] * 3 + self.sd["card"][1] / 2.
					self.sd["btn"]["top_btn"].text = "Top deck"
					if "bottom" in self.gd["effect"]:
						self.sd["btn"]["bottom_btn"].text = "Bottom deck"
					elif "Waiting" in self.gd["effect"]:
						self.sd["btn"]["bottom_btn"].text = "Waiting room"
					self.sd["btn"]["bottom_btn"].size = self.sd["btn"]["top_btn"].size
					self.sd["btn"]["bottom_btn"].center_x = self.gd["p_xscat"] / 4. * 3 - self.sd["card"][0] / 2 + \
					                                        self.sd["padding"]
					self.sd["btn"]["bottom_btn"].y = self.sd["btn"]["top_btn"].y
					self.sd["popup"]["p_scv"].y = self.sd["padding"] * 3.5 + self.sd["btn"]["top_btn"].size[1] * 2
					self.gd["p_c"] += "_auto"
				elif "top" in self.gd["effect"] and "look" in self.gd["effect"]:
					self.sd["btn"][f"{phase}_btn"].y = -Window.height
					self.sd["btn"]["top_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
					self.sd["btn"]["top_btn"].center_x = self.gd["p_xscat"] * 3 / 4. - self.sd["card"][0] / 2 + self.sd[
						"padding"]
					self.sd["btn"]["top_btn"].y = self.sd["padding"] * 1.5
					self.sd["btn"]["top_btn"].text = "End Effect"
					self.sd["btn"]["draw_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
					self.sd["btn"]["draw_btn"].center_x = self.gd["p_xscat"] / 2. - self.sd["card"][0] / 2 + self.sd[
						"padding"]
					self.sd["btn"]["draw_btn"].y = self.sd["padding"] * 3 + self.sd["card"][1] / 2.
					self.sd["popup"]["p_scv"].y = self.sd["padding"] * 3.5 + self.sd["btn"]["top_btn"].size[1] * 2
				elif "top" in self.gd["effect"] and self.gd["p_look"] >= 1 and self.gd["p_max_s"] > 0 and "fix" not in \
						self.gd["p_c"]:
					self.sd["btn"]["draw_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
					self.sd["btn"]["draw_btn"].center_x = self.gd["p_xscat"] / 2. - self.sd["card"][0] / 2 + self.sd[
						"padding"]
					self.sd["btn"]["draw_btn"].y = self.sd["padding"] * 3 + self.sd["card"][1] / 2.
					self.sd["popup"]["p_scv"].y = self.sd["padding"] * 3.5 + self.sd["btn"]["draw_btn"].size[1] * 2
				# elif "stack" in self.gd["effect"] or "stacked" in self.gd["effect"]:
				#
				elif "check" in self.gd["effect"]:
					self.sd["btn"]["check_btn"].center_x = self.gd["p_xscat"] / 2. - self.sd["card"][0] / 2 + \
					                                       self.sd["padding"]
					self.sd["btn"]["check_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
					self.sd["btn"]["check_btn"].y = self.sd["padding"] * 1.5
					self.sd["btn"][f"{phase}_btn"].y = -Window.height
					self.sd["btn"]["field_btn"].y = -Window.height

	def popup_slc_move(self, ind):
		if self.gd["p_max_s"] > 0:
			self.cpop[ind].selected()
			self.gd["chosen"].append(ind)

			if len(self.gd["chosen"]) > self.gd["p_max_s"] and ind not in self.gd["p_select"]:
				temp = self.gd["p_select"].pop(0)
				self.gd["chosen"].remove(temp)
				self.cpop[temp].selected(False)

			self.gd["p_select"].append(ind)
			if "stacked" not in self.gd["p_c"]:
				self.update_text_selected()

	def update_text_selected(self):
		for i in range(len(self.gd["p_l"])):
			if self.gd["p_l"][i] != "sspace":
				self.cpop[self.gd["p_l"][i]].update_text()

		for i in range(len(self.gd["chosen"])):
			if "Look" in self.gd["p_c"] and "order" in self.gd["p_c"]:
				if i == 0:
					self.cpop[self.gd["chosen"][i]].update_text("Top", .5)
				elif (i + 1) % 10 == 1:
					self.cpop[self.gd["chosen"][i]].update_text(f"{i + 1}st", .5)
				elif (i + 1) % 10 == 2:
					self.cpop[self.gd["chosen"][i]].update_text(f"{i + 1}nd", .5)
				elif (i + 1) % 10 == 3:
					self.cpop[self.gd["chosen"][i]].update_text(f"{i + 1}rd", .5)
				else:
					self.cpop[self.gd["chosen"][i]].update_text(f"{i + 1}th", .5)
			else:
				self.cpop[self.gd["chosen"][i]].update_text(i + 1)

	def popup_clr_button(self):
		for btn in self.sd["btn"].keys():
			if btn.startswith("a"):
				continue
			elif "filter_add" in btn:
				continue
			self.sd["btn"][btn].y = -Window.height * 2
		for nx in self.iach:
			self.iach[nx].y = -Window.height * 2
		self.sd["btn"]["label"].x = -Window.width * 2
		self.sd["cpop_press"] = []

	def popup_clr(self, *args):
		self.gd["popup_done"] = (False, True)
		self.gd["popup_on"] = False
		self.gd["uptomay"] = False
		self.gd["chosen"] = []
		self.gd["p_c"] = ""
		self.sd["popup"]["stack"].clear_widgets()

		if not self.decks["dbuilding"]:
			self.popup_clr_button()

			# for icon in self.icon.keys():
			# 	self.icon[icon].y = -Window.height

			# if self.gd["debug"]:
			# 	for item2 in self.gd["d_btn_list"]:
			# 		self.sd["btn"][f"d{item2}"].y = 0

			if self.gd["phase"] == "Main" and self.gd["active"] == "1" and "ACT" in self.gd["ability_trigger"]:
				self.act_ability_show(hide=True)
				self.sd["btn"]["end"].y = -Window.height
				self.sd["btn"]["end_attack"].y = -Window.height
				self.sd["btn"]["end_phase"].y = -Window.height
			elif any(self.gd["phase"] == phase for phase in ("Main", "Attack", "Declaration", "Climax", "Encore")):
				if "Main" in self.gd["phase"]:
					self.sd["btn"]["end"].text = "Climax Phase"  # @\n
				else:
					self.sd["btn"]["end"].text = f"End {self.gd['phase']}"
				if self.gd["active"] == "1":
					if len(self.gd["select_btns"]) > 0:
						self.act_ability_show(hide=True)
					else:
						self.act_ability_show()

	def card_btn_release(self, btn):
		self.sd["cpop_slc"] = ""

	def card_btn_press(self, btn):
		if self.multi_info["t"]:
			self.cardinfo.import_data(self.cpop[btn.cid], annex_img)
		elif self.decks["dbuilding"]:
			if self.decks["img_pop"]:
				self.decks["img_pop"] = False
				self.decks["dbuild"]["img"] = str(self.cpop[btn.cid].img_file)
				if self.decks['dbuild']['img'] in other_img:
					self.decks["st"]["image_btn"].source = f"atlas://{img_in}/other/{self.decks['dbuild']['img']}"
				elif self.decks['dbuild']['img'] in annex_img:
					self.decks["st"]["image_btn"].source = f"atlas://{img_in}/annex/{self.decks['dbuild']['img']}"
				else:
					self.decks["st"]["image_btn"].source = f"atlas://{img_ex}/main/{self.decks['dbuild']['img']}"

				if f"id{self.decks['dbuilding']}" in self.dpop:
					self.dpop[f"id{self.decks['dbuilding']}"].source = str(self.decks["st"]["image_btn"].source)

				self.popup_clr()
				self.sd["popup"]["popup"].dismiss()
			else:
				ind = self.cpop[btn.cid].cid
				self.sd["cpop_slc"] = ind
				self.sd["cpop_press"].append(ind)
				if len(self.sd["cpop_press"]) >= info_popup_press:
					if all(prs == self.sd["cpop_press"][-1] for prs in self.sd["cpop_press"][-info_popup_press:]):
						self.cd["00"].import_data(sc[self.sd["cpop_press"][-1]])
						self.sd["cpop_press"] = []
						self.cardinfo.import_data(self.cd["00"], annex_img)
				else:
					self.sd["cpop_pressing"] = Clock.schedule_once(self.card_btn_info, info_popup_dt)
				if ind not in self.decks["add_chosen"]:
					self.decks["add_chosen"].append(ind)
					self.cpop[btn.cid].selected()
					self.sd["btn"]["Add_btn"].disabled = False
				elif ind in self.decks["add_chosen"]:
					self.decks["add_chosen"].remove(ind)
					self.cpop[btn.cid].selected(False)
					if len(self.decks["add_chosen"]) == 0:
						self.sd["btn"]["Add_btn"].disabled = True
		else:
			if not self.cpop[btn.cid]:
				self.sd["cpop_slc"] = btn.cid
				self.sd["cpop_press"].append(btn.cid)
				if len(self.sd["cpop_press"]) >= info_popup_press:
					if all(prs == btn.cid for prs in self.sd["cpop_press"][-info_popup_press:]):
						self.sd["cpop_press"] = []
						self.cardinfo.import_data(self.cpop[btn.cid], annex_img)
				else:
					self.sd["cpop_pressing"] = Clock.schedule_once(self.card_btn_info, info_popup_dt)

			if not self.multi_info["t"]:
				if "_" in self.gd["p_c"]:
					phase = self.gd["p_c"].split("_")[0]
				else:
					phase = self.gd["p_c"]

				if "auto" in self.gd["p_c"]:
					if "stock" not in self.gd["p_c"] and not self.cd[btn.cid].back:
						try:
							if (btn.cid != "1" or btn.cid != "2"):
								self.cardinfo.import_data(self.cd[btn.cid], annex_img)
						except KeyError:
							if self.cpop[btn.cid].cid != "player":
								self.cardinfo.import_data(self.cpop[btn.cid], annex_img)
				else:
					# add select background on the card selected
					if (any(s in self.gd["p_c"] for s in ("Salvage", "Search", "Encore", "Discard")) or (
							"Look" in self.gd["p_c"] and "hand" in self.gd["effect"])) and btn.cid not in self.gd[
						"chosen"]:
						if self.select_filter_check(btn.cid):
							self.popup_slc_move(btn.cid)
					elif btn.cid not in self.gd["chosen"]:
						self.popup_slc_move(btn.cid)
					else:
						self.cpop[btn.cid].selected(False)
						if btn.cid in self.gd["chosen"]:
							self.gd["chosen"].remove(btn.cid)
							if "stacked" not in self.gd["p_c"]:
								self.update_text_selected()
							if self.gd["btrait"][1]:
								for tr in list(self.gd["btrait"][5]):
									if btn.cid in tr[0]:
										self.gd["btrait"][3].append(tr[1])
										self.gd["btrait"][5].remove(tr)
										break
						if btn.cid in self.gd["p_select"]:
							self.gd["p_select"].remove(btn.cid)

					# change button text
					if self.gd["p_c"] == "Hand" or self.gd["p_c"] == "Levelup":
						if self.gd["p_max_s"] - len(self.gd["chosen"]) > 1:
							word = "cards"
							card = self.gd["p_max_s"] - len(self.gd["chosen"])
						else:
							word = "card"
							card = 1

						if self.gd["p_max_s"] == len(self.gd["chosen"]):
							self.sd["btn"][f"{self.gd['p_c']}_btn"].disabled = False
							if self.gd["p_c"] == "Hand":
								self.sd["btn"][f"{self.gd['p_c']}_btn"].text = "Discard selected"
							elif self.gd["p_c"] == "Levelup":
								self.sd["btn"][f"{self.gd['p_c']}_btn"].text = "Level Up"
						else:
							self.sd["btn"][f"{self.gd['p_c']}_btn"].disabled = True
							self.sd["btn"][f"{self.gd['p_c']}_btn"].text = f"{card} {word} left"
					elif len(self.gd["chosen"]) > 0:
						if len(self.gd["chosen"]) > 1:
							word = "cards"
						else:
							word = "card"

						if "Mulligan" in self.gd["p_c"]:
							self.sd["btn"]["Mulligan_btn"].text = f"Discard {len(self.gd['chosen'])} {word}"
						elif "cstock" in self.gd["p_c"]:
							self.sd["btn"]["cstock_btn"].text = f"Put {len(self.gd['chosen'])} {word} to Stock"
						elif "revive" in self.gd["p_c"]:
							self.sd["btn"]["revive_btn"].text = f"Choose selected {word}"
						elif any(s in self.gd["p_c"] for s in ("Clock", "Search", "Salvage", "Discard")):
							if "Bond" in self.gd["search_type"]:
								self.sd["btn"][f"{phase}_btn"].text = f"Bond {word}"
							elif "Stage" in self.gd["effect"] or "Library" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = "Continue Effect"
							elif "Memory" in self.gd["effect"] or "hmemory" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = "Put into Memory"
							elif "Stock" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = "Put into Stock"
							elif "Clock" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = "Put into Clock"
							elif "Clock" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = "Put into Clock"
							elif "Reveal" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = f"Take {word}"
							elif "Change" in self.gd["p_c"]:
								self.sd["btn"][f"{phase}_btn"].text = "Continue Effect"
							elif "levswap" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = f"Swap cards"
							elif "csalvage" in self.gd["effect"] or "wdecker" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = f"Return {word}"
							else:
								self.sd["btn"][f"{phase}_btn"].text = f"{phase} {word}"
						elif "Counter" in self.gd["p_c"]:
							self.sd["btn"]["Counter_btn"].text = f"Play Counter {word}"
						elif "Shuffle" in self.gd["p_c"]:
							self.sd["btn"]["Shuffle_btn"].text = f"Shuffle {word}"
						elif "Look" in self.gd["p_c"]:
							if "hand" in self.gd["p_c"]:
								if "stacked" in self.gd["p_c"]:
									self.sd["btn"]["Look_btn"].text = f"Take selected stack"
								else:
									self.sd["btn"]["Look_btn"].text = f"Take selected {word}"
							elif "stack" in self.gd["p_c"] and "stacked" not in self.gd["p_c"]:
								self.sd["btn"]["Look_btn"].text = f"Create Stack"
							elif "waiting" in self.gd["p_c"] and "reorder" in self.gd["effect"]:
								self.sd["btn"]["Look_btn"].text = "Continue Effect"
							elif "bdeck" in self.gd["p_c"] and "reorder" in self.gd["effect"]:
								self.sd["btn"]["Look_btn"].text = "Continue Effect"
							elif "waiting" in self.gd["p_c"]:
								self.sd["btn"]["Look_btn"].text = f"Discard {word}"
							elif "reorder" in self.gd["p_c"]:
								self.sd["btn"]["Look_btn"].text = f"Reorder {word}"
							else:
								self.sd["btn"]["Look_btn"].text = f"Return selected {word}"
						elif "Stage" in self.gd["effect"]:
							self.sd["btn"][f"{phase}_btn"].text = "Play selected"
						elif "encore" not in phase:
							if self.gd["resonance"][0]:
								self.sd["btn"][f"{phase}_btn"].text = "Reveal selected"
							elif "Level" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = "Put to Level"
							elif "levswap" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = "Continue Effect"
							else:
								self.sd["btn"][f"{phase}_btn"].text = "Discard selected"
					else:
						if "_" in self.gd["p_c"]:
							self.sd["btn"][f"{phase}_btn"].text = "End Effect"
						if "Stage" in self.gd["effect"]:
							self.sd["btn"][f"{phase}_btn"].text = "End Effect"
						elif "cstock" in self.gd["p_c"]:
							self.sd["btn"]["cstock_btn"].text = "End Effect"
						elif "Counter" in self.gd["p_c"]:
							self.sd["btn"]["cstock_btn"].text = "End Counter"
						elif phase in phases:
							self.sd["btn"][f"{phase}_btn"].text = f"End {phase}"
						else:
							self.sd["btn"][f"{phase}_btn"].text = "End Effect"

					if "encore" not in phase:
						self.pop_btn_disable(phase)

	def card_btn_info(self, *args):
		if self.sd["cpop_slc"] != "":
			self.sd["cpop_press"] = []
			if self.decks["dbuilding"]:
				self.cd["00"].import_data(sc[self.sd["cpop_slc"]])
				self.cardinfo.import_data(self.cd["00"], annex_img)
			else:
				self.cardinfo.import_data(self.cpop[self.sd["cpop_slc"]], annex_img)
		else:
			if self.sd["cpop_pressing"] is not None:
				self.sd["cpop_pressing"].cancel()
				self.sd["cpop_pressing"] = None

	def show_info_btn(self, btn):
		self.gd["moving"] = False
		self.gd["btn_release"] = False
		if "info_btn" in btn.cid:
			self.gd["btn_id"] = self.gd["ability_trigger"].split("_")[-1]
			self.infob = Clock.schedule_once(self.info_start)
		else:
			self.gd["btn_id"] = btn.cid
			self.sd["hbtn_press"].append(btn.cid)
			if len(self.sd["hbtn_press"]) >= info_popup_press:
				if all(prs == btn.cid for prs in self.sd["hbtn_press"][-info_popup_press:]):
					self.infob = Clock.schedule_once(self.info_start)
			else:
				self.infob = Clock.schedule_once(self.info_start, info_popup_dt)

	def pop_btn_disable(self, phase):
		if self.gd["notarget"]:
			self.sd["btn"][f"{phase}_btn"].disabled = False
		elif self.gd["dismay"]:
			self.sd["btn"][f"{phase}_btn"].disabled = False
		elif self.gd["p_min_s"] >= 0:
			if len(self.gd["chosen"]) > self.gd["p_max_s"]:
				self.sd["btn"][f"{phase}_btn"].disabled = True
			elif len(self.gd["chosen"]) < self.gd["p_min_s"]:
				self.sd["btn"][f"{phase}_btn"].disabled = True
			else:
				self.sd["btn"][f"{phase}_btn"].disabled = False
		elif len(self.gd["chosen"]) < self.gd["p_max_s"] and "fix" in self.gd["p_c"]:
			max = list(self.gd["p_l"])
			if "sspace" in max:
				max.remove("sspace")

			if len(max) < self.gd["p_max_s"]:
				if len(self.gd["chosen"]) < len(max):
					self.sd["btn"][f"{phase}_btn"].disabled = True
				else:
					self.sd["btn"][f"{phase}_btn"].disabled = False
			else:
				self.sd["btn"][f"{phase}_btn"].disabled = True
		elif len(self.gd["chosen"]) < self.gd["p_max_s"] and not self.gd["uptomay"]:
			if self.gd["btrait"][1]:
				max = list(self.gd["p_l"])
				if self.gd["btrait"][4]:
					 for ind in self.gd["btrait"][4]:
						 if ind in max:
							 max.remove(ind)
				if len([s for s in max if any(tr in self.cd[s].trait_t for tr in self.gd["btrait"][3])])>0:
					self.sd["btn"][f"{phase}_btn"].disabled = True
				else:
					self.sd["btn"][f"{phase}_btn"].disabled = False
			else:
				self.sd["btn"][f"{phase}_btn"].disabled = True
		elif len(self.gd["chosen"]) < self.gd["p_max_s"] and self.gd["uptomay"] and "all" in self.gd["effect"]:
			max = list(self.gd["p_l"])
			if "sspace" in max:
				max.remove("sspace")

			if len(max) < self.gd["p_max_s"]:
				if len(self.gd["chosen"]) < len(max):
					self.sd["btn"][f"{phase}_btn"].disabled = True
				else:
					self.sd["btn"][f"{phase}_btn"].disabled = False
			else:
				self.sd["btn"][f"{phase}_btn"].disabled = True
		elif "reorder" in self.gd["p_c"]:
			max = len(self.gd["p_l"])
			if "sspace" in self.gd["p_l"]:
				max -= 1
			if len(self.gd["chosen"]) < max:
				self.sd["btn"][f"{phase}_btn"].disabled = True
			elif len(self.gd["chosen"]) >= max:
				self.sd["btn"][f"{phase}_btn"].disabled = False
		else:
			self.sd["btn"][f"{phase}_btn"].disabled = False

	def selected_card(self, *args):
		if "Clock" in self.gd["status"] and "Clock" in self.gd["btn_id"] and self.gd["btn_id"] in self.gd[
			"select_btns"]:
			if not self.gd["move"]:
				self.gd["move"] = "clock"
				self.move_field_btn(self.gd["phase"])
				return True
		elif ("Center" in self.gd["btn_id"] or "Back" in self.gd["btn_id"] or "Climax" in self.gd["btn_id"]) and \
				self.gd["btn_id"] in self.gd[
			"select_btns"]:
			if (self.gd["choose"] or self.gd["revive"]) and not self.gd["move"]:
				# if self.gd["btn_id"] not in self.gd["chosen"]:
				# self.gd["chosen"].append(self.gd["btn_id"])
				self.gd["move"] = self.gd["btn_id"][:-1]
			else:
				if "Climax" in self.gd["btn_id"]:
					ind = self.pd[self.gd["btn_id"][-1]][self.gd["btn_id"][:-1]][0]
				else:
					ind = self.pd[self.gd["btn_id"][-1]][self.gd["btn_id"][:-2]][int(self.gd["btn_id"][-2])]
				if ind not in self.gd["chosen"]:
					self.gd["chosen"].append(ind)
					if self.gd["btrait"][0] and len(self.gd["chosen"]) > 1:
						tr = [[], []]
						for sx in self.gd["chosen"]:
							for inx in range(len(self.gd["btrait"][1])):
								if self.gd["btrait"][1][inx] in self.cd[sx].trait_t:
									tr[inx].append(sx)
						if (len(tr[0]) >= 2 and len(tr[1]) < 1) or (len(tr[0]) < 1 and len(tr[1]) >= 2):
							temp = self.gd["chosen"].pop(0)
							self.cd[temp].update_text()
				elif ind in self.gd["chosen"]:
					self.cd[ind].update_text()
					self.gd["chosen"].remove(ind)

			if not self.gd["payed"] and self.gd["pay"]:
				if self.gd["mstock"]:
					status = "1"
				else:
					status = self.gd["pay_status"]
			else:
				status = self.gd["status"]

			if "Encore" in self.gd["phase"] and self.gd["pp"] >= 0 and len(self.gd["chosen"]) == 1:
				self.gd["encore_ind"] = str(self.gd["chosen"][0])
				self.move_field_btn(self.gd["phase"])
				return True
			elif len(self.gd["chosen"]) == int(status[-1]) or self.gd["move"] or (
					len(self.gd["chosen"]) == len(self.gd["select_btns"]) and len(self.gd["select_btns"]) < int(
					status[-1])):
				# if "Encore" in self.gd["phase"]:
				# 	self.gd["encore_ind"] = str(self.gd["chosen"][0])
				# if (self.gd["choose"] or self.gd["revive"]) and not self.gd["move"]:
				# 	self.gd["move"] = self.gd["chosen"][0][:-1]
				if not self.gd["choose"]:
					if len(self.gd["chosen"]) < int(status[-1]):
						for r in range(int(status[-1]) - len(self.gd["chosen"])):
							self.gd["chosen"].append("")
					for inx in self.gd["chosen"]:
						if self.gd["mstock"]:
							self.gd["target"].append(self.gd["mstock"])
						self.gd["target"].append(inx)
						if inx != "" and inx in self.cd:
							self.cd[inx].selectable(False)
							self.cd[inx].update_text()

				if self.gd["btrait"][1]:
					self.gd["btrait"] = ["", [], [],[],[],[]]
				self.gd["choose"] = True
				if not self.gd["payed"] and self.gd["pay"]:
					self.move_field_btn(self.gd["phase"], y=True)
				else:
					self.move_field_btn(self.gd["phase"])
				return True
			else:
				if "move" not in self.gd["ability_doing"]:
					for tt in range(len(self.gd["chosen"])):
						self.cd[self.gd["chosen"][tt]].update_text(tt + 1)
				if self.gd["btrait"][1]:
					if len(self.gd["chosen"]) > 0:
						if all(tr in self.cd[self.gd["chosen"][0]].trait_t for tr in self.gd["btrait"][1]):
							self.gd["pay_status"] = str(self.gd["btrait"][0])
						else:
							for inx in range(len(self.gd["btrait"][1])):
								if self.gd["btrait"][1][inx] in self.cd[self.gd["chosen"][0]].trait_t:
									self.gd["pay_status"] = str(self.gd["btrait"][0]).replace(
										f"_{self.gd['btrait'][1][inx]}", "")
					elif len(self.gd["chosen"]) <= 0:
						self.gd["pay_status"] = str(self.gd["btrait"][0])
					self.move_field_btn(self.gd["phase"])
					self.select_card(s="Stand", p=True)
		return False

	def show_info_re(self, btn):
		self.gd["btn_release"] = True
		# self.gd["btn_id"] = ""

		if self.infob is not None:
			self.infob.cancel()
			self.infob = None
		if btn.cid[:-1] in self.fields:
			self.show_field_label(btn.cid)

		if not self.gd["info_p"]:
			if not self.gd["payed"] and self.gd["pay"]:
				if self.selected_card():
					if self.gd["mstock"]:
						self.pay_mstock(self.gd["mstock"])
					else:
						self.pay_condition()
			elif not self.gd["text_popup"]:  # and not self.gd["info_p"]:
				if self.selected_card():
					if "Encore" in self.gd["phase"] and self.gd["pp"] >= 0:
						self.encore_start()
					else:
						self.ability_effect()

	def event_done(self, *args):
		if self.gd["ability_trigger"]:
			ind = self.gd["ability_trigger"].split("_")[1]
			if ind in self.pd[ind[-1]]["Res"] and ind != self.gd["trigger_card"]:
				self.pd[ind[-1]]["Res"].remove(ind)
				self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
				self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])
				self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Waiting"], t="Waiting")
				self.pd[ind[-1]]["Waiting"].append(ind)
				self.update_field_label()
				self.event_move = True

	def check_event(self, ind):
		for item in self.cd[ind].text_c:
			play = ab.play(item[0])
			if "play" in play:
				# stage = [s for s in self.pd[ind[-1]]["Center"] + self.pd[ind[-1]]["Back"] if s != ""]
				# if "Trait" in play:
				# 	if "lower" in play and len([s for s in stage if
				# 	        any(tr in self.cd[s].trait_t for tr in play[play.index("Trait") + 1].split("_"))]) <= play[
				# 		0]:
				# 		return False
				# 	elif "lower" not in play and len([s for s in stage if
				# 	        any(tr in self.cd[s].trait_t for tr in play[play.index("Trait") + 1].split("_"))]) >= play[
				# 		0]:
				# 		return False
				if "lower" in play and len(self.cont_times(play, self.cont_cards(play, ind), self.cd)) <= play[0]:
					return False
				elif "lower" not in play and len(self.cont_times(play, self.cont_cards(play, ind), self.cd)) >= play[0]:
					return False
		return True

	def check_condition(self, ind):
		card = self.cd[ind]
		check = False
		effect = True
		text = ""
		if card.card == "Climax":
			if card.mcolour in self.pd[ind[-1]]["colour"]:
				check = True
			else:
				text = "Colour"
		else:
			if card.level_t == 0:
				if len(self.pd[ind[-1]]["Stock"]) >= card.cost:
					check = True
				else:
					text = "Cost"
			elif len(self.pd[ind[-1]]["Level"]) >= card.level_t:
				if card.mcolour in self.pd[ind[-1]]["colour"]:
					if len(self.pd[ind[-1]]["Stock"]) >= card.cost:
						check = True
					else:
						text = "Cost"
				else:
					text = "Colour"
			else:
				text = "Level"

		if card.card == "Event" and (not self.gd["event"][ind[-1]] or not self.check_event(ind)):
			effect = False
			text = "Effect"
		elif card.card == "Climax" and not self.gd["climax"][ind[-1]]:
			effect = False
			text = "Effect"

		if check and effect:
			return True
		else:
			if self.gd["confirm_requirement"]:
				self.popup_clr_button()
				self.sd["popup"]["popup"].title = "Play Condition"
				self.gd["p_c"] = "auto"
				self.gd["p_xscat"] = self.sd["padding"] * 2 + self.gd["p_width"] * starting_hand
				self.gd["p_hand"] = starting_hand
				self.sd["popup"]["p_scv"].do_scroll_y = False
				self.sd["popup"]["stack"].clear_widgets()

				self.sd["btn"]["close_btn"].center_x = self.gd["p_xscat"] / 2. - self.sd["card"][0] / 2 + self.sd[
					"padding"]
				self.sd["btn"]["close_btn"].y = self.sd["padding"] * 1.5

				# self.sd["btn"]["label"].text_size = (self.gd["p_xscat"] * 0.9, None)
				if card.card == "Event" and not self.gd["event"][ind[-1]]:
					self.sd["btn"][
						"label"].text = f"The card \"{card.name}\" cannot be played because you cannot play event cards from hand this turn."
				elif card.card == "Climax" and not self.gd["climax"][ind[-1]]:
					self.sd["btn"][
						"label"].text = f"The card \"{card.name}\" cannot be played because you cannot play climax cards from hand during your climax phase."
				else:
					self.sd["btn"][
						"label"].text = f"The card \"{card.name}\" cannot be played because it does not meet the required {text} condition."
				self.sd["btn"]["label"].text_size = (self.gd["p_xscat"] * 0.9, None)
				self.sd["btn"]["label"].texture_update()
				self.sd["btn"]["label"].height = self.sd["btn"]["label"].texture.size[1]
				self.sd["btn"]["label"].pos = (
					self.sd["padding"] / 2, self.sd["card"][1] / 2. + self.sd["padding"] * 3.5)  # -self.sd["padding"])

				self.sd["popup"]["popup"].size = (self.gd["p_xscat"],
				                                  self.sd["btn"]["label"].texture.size[1] + self.sd["card"][1] * 2 +
				                                  self.sd["padding"] * 9.5 + self.sd["popup"]["popup"].title_size +
				                                  self.sd["popup"]["popup"].separator_height)

				self.sd["popup"]["p_scv"].size = (self.gd["p_xscat"], self.gd["p_height"])
				self.sd["popup"]["p_scv"].y = self.sd["card"][1] / 2. + self.sd["padding"] * 3.5 + \
				                              self.sd["btn"]["label"].size[1] + self.sd["padding"] * 2

				self.sd["popup"]["stack"].size = (self.sd["popup"]["p_scv"].size[0], self.gd["p_height"])

				self.gd["p_l"] = [ind]
				nx, ns = self.get_index_stack(self.gd["p_l"], self.gd["p_hand"])
				if nx:
					self.gd["p_l"].insert(nx, "sspace")
					self.sd["popup"]["sspace"].size = (
						self.sd["popup"]["sspace"].size_o[0] * ns, self.sd["popup"]["sspace"].size[1])

				for inx in self.gd["p_l"]:
					if "sspace" in inx:
						try:
							self.sd["popup"]["stack"].add_widget(self.sd["popup"][inx])
						except WidgetException:
							pass
					else:
						self.sd["popup"]["stack"].add_widget(self.cpop[inx])
						self.cpop[inx].selected(False)
						self.cpop[inx].update_text()

				self.sd["popup"]["popup"].open()
			return False

	def move(self, *args):
		# if not self.gd["notarget"] and not self.gd["notargetfield"]:
		ind = self.gd["ability_trigger"].split("_")[1]
		if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
			if "this" in self.gd["effect"]:
				self.gd["target"].append(ind)
			elif self.gd["effect"][0] == -16:
				for r in range(len(self.gd["extra"])):
					self.gd["target"].append(self.gd["extra"][r])

			if not self.gd["move"] or self.gd["move"] == "none":
				self.gd["target"].append("")
			else:
				self.gd["target"].append(self.gd["move"])
			self.gd["move"] = ""
		# elif not self.gd["move"] and ind[-1] == "1":
		# 	self.gd["target"].append("")
		if self.gd["effect"][0] == 0:
			self.gd["effect"][0] = 1
		elif self.gd["effect"][0] == -16:
			self.gd["effect"][0] = len(self.gd["extra"])
			self.gd["extra"] = []

		for r in range(self.gd["effect"][0]):
			idm = self.gd["target"].pop(0)
			move = self.gd["target"].pop(0)
			if self.net["game"] and ind[-1] == "1":
				self.net["act"][4].append(idm)
				self.net["act"][4].append(move)

			if idm == "":
				continue
			if move == "none" or move == "":
				continue
			card = self.cd[idm]
			self.mat[ind[-1]]["mat"].remove_widget(self.cd[idm])
			self.mat[ind[-1]]["mat"].add_widget(self.cd[idm])
			if self.pd[idm[-1]][move[:-1]][int(move[-1])] != "":
				temp = self.pd[idm[-1]][move[:-1]][int(move[-1])]
				self.cd[temp].setPos(field=self.mat[card.owner]["field"][card.pos_new], t=card.pos_new)
				self.pd[idm[-1]][card.pos_new[:-1]][int(card.pos_new[-1])] = temp
			else:
				self.pd[idm[-1]][card.pos_new[:-1]][int(card.pos_new[-1])] = ""
			card.setPos(field=self.mat[card.owner]["field"][move], t=move)
			self.pd[idm[-1]][move[:-1]][int(move[-1])] = card.ind
			self.check_cont_ability()

		if "move" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("move")
			self.gd["choose"] = False

		if self.gd["notarget"]:
			self.gd["notarget"] = False

		if self.gd["notargetfield"]:
			self.gd["notargetfield"] = False

		self.do_check()
		self.ability_effect()

	def select_card(self, s="", p=False, f=None, filter=False):
		self.gd["moveable"] = []
		if not filter:
			self.gd["select_btns"] = []
			self.act_ability_show(hide=True)
		if p:
			status = self.gd["pay_status"]
		else:
			status = self.gd["status"]

		if "Opp" in status and (self.gd["rev"] or self.gd["rev_counter"]):
			player = self.gd["active"]
		elif "Opp" in status or self.gd["rev"] or self.gd["rev_counter"]:
			player = self.gd["opp"]
		else:
			player = self.gd["active"]

		if f is None:
			fields = []
			inm = self.gd["ability_trigger"].split("_")[1]

			if "Opposite" in status:
				if "Center" in self.cd[inm].pos_new:
					if inm[-1] == "1":
						p = "2"
					elif inm[-1] == "2":
						p = "1"
					fields = [self.pd[p]["Center"][self.m[int(self.cd[inm].pos_new[-1])]]]

			elif "Battle" in status:
				atk = self.gd["attacking"][0]
				deff = "0"
				if self.gd["attacking"][0][-1] == "1":
					opp = "2"
				elif self.gd["attacking"][0][-1] == "2":
					opp = "1"
				if "C" in self.gd["attacking"][4]:
					deff = self.pd[opp]["Center"][self.gd["attacking"][3]]
				elif "B" in self.gd["attacking"][4]:
					deff = self.pd[opp]["Back"][self.gd["attacking"][3]]

				battle = [atk, deff]

				if "Both" in status:
					fields = list(battle)
				elif "Batk" in status:
					fields = [s for s in self.pd[player]["Back"] if s != ""]
				elif "Bopp" in status:
					if player == "1":
						fields = [s for s in battle if s[-1] == "2"]
					elif player == "2":
						fields = [s for s in battle if s[-1] == "1"]
				else:
					if player == "1":
						fields = [s for s in battle if s[-1] == "1"]
					elif player == "2":
						fields = [s for s in battle if s[-1] == "2"]
			elif "Climax" in status:
				fields = self.pd[player]["Climax"]
			elif "Center" in status:
				fields = self.pd[player]["Center"]
			elif "Back" in status:
				fields = self.pd[player]["Back"]
			elif "Any" in status:
				fields = self.pd[self.gd["active"]]["Center"] + self.pd[self.gd["active"]]["Back"] + \
				         self.pd[self.gd["opp"]]["Center"] + \
				         self.pd[self.gd["opp"]]["Back"]
			elif "Another" in status:
				fields = self.pd[player]["Center"] + self.pd[player]["Back"]
				inx = 0
				for j in range(len(status)):
					if "Another" in status:
						inx = j
				fields.remove(status[inx].split("_")[1])
			else:
				fields = self.pd[player]["Center"] + self.pd[player]["Back"]

			if "Antilvl" in status:
				fields = [s for s in fields if self.cd[s].level_t > len(self.pd[player]["Level"])]

			if "Trait" in status:
				traits = status.split("_")[1:-1]
				status = status.split("_")[-1]
				if traits == [""]:
					fields = [s for s in fields if len(self.cd[s].trait_t) <= 0 and "Character" in self.cd[s].card]
				else:
					fields = [s for s in fields if any(trait in self.cd[s].trait_t for trait in traits)]
			elif "NameSet" in status:
				names = status.split("_")[1:-1]
				status = status.split("_")[-1]
				temp = list(fields)
				fields = []
				for n in temp:
					if n != "":
						for nx in range(int(len(names) / 2)):
							if names[nx] in self.cd[n].name_t:
								if names[nx + int(len(names) / 2)] != "":
									for ss in sn["Title"][names[nx + int(len(names) / 2)]]:
										if ss in self.cd[n].cid:
											fields.append(n)
								else:
									fields.append(n)
			elif "Name=" in status:
				names = status.split("_")[1:-1]
				status = status.split("_")[-1]
				fields = [s for s in fields if self.cd[s].name_t in names]
			elif "Name" in status:
				names = status.split("_")[1:-1]
				status = status.split("_")[-1]
				fields = [s for s in fields if any(name in self.cd[s].name_t for name in names)]
			elif "Text" in status:
				names = status.split("_")[1:-1]
				status = status.split("_")[-1]
				fields = [s for s in fields if
				          any(any(text1.lower() in tx[0].lower() and f"\"{text1.lower()}\"" not in tx[0].lower() for
				                  text1 in names) for tx in self.cd[s].text_c)]

			if "Cost<=" in status:
				fields = [s for s in fields if self.cd[s].cost_t <= int(status[status.index("Cost<=") + 6])]
			elif "Cost>=" in status:
				fields = [s for s in fields if self.cd[s].cost_t >= int(status[status.index("Cost>=") + 6])]

			if "Level<=" in status:
				fields = [s for s in fields if self.cd[s].level_t <= int(status[status.index("Level<=") + 7])]
			elif "Level>=" in status:
				fields = [s for s in fields if self.cd[s].level_t >= int(status[status.index("Level>=") + 7])]

			if "Standing" in status:
				fields = [s for s in fields if self.cd[s].status == "Stand"]
			# elif "Rest" in status:
			# 	fields = [s for s in fields if self.cd[s].status == "Rest"]
			# elif "Reversed" in status:
			# 	fields = [s for s in fields if self.cd[s].status == "Reversed"]

			if "Other" in status and inm in fields:
				fields.remove(inm)
			elif "This" in status and inm not in fields:
				fields.append(inm)

			opptar = list(fields)
			if "Opp" in status:
				for idc in opptar:
					for text in self.cd[idc].text_c:
						if text[0].startswith(cont_ability) and text[1] != 0 and text[1] > -9:
							eff = ab.cont(text[0])
							if eff and "no_target" in eff:
								fields.remove(idc)
								break
			if "BattleBatk" in status and "May" in status:
				fields.append(self.pd[self.gd["opp"]]["Center"][self.gd["attacking"][3]])
			if self.gd["btrait"][0] and len(self.gd["chosen"]) >= 1:
				for ii in self.gd["chosen"]:
					fields.append(ii)
		else:
			fields = f

		if filter:
			return fields

		for ind in fields:
			if ind == "":
				continue
			if s == "":
				pass
			elif self.cd[ind].status != s:
				continue

			field = self.cd[ind].pos_new
			self.cd[ind].selectable()
			if "Opp" in status:
				self.field_btn[f"{field}{player}"].x = self.mat[player]["mat"].x + self.mat[player]["mat"].size[0] - \
				                                       self.sd["card"][0] - self.mat[player]["field"][field][0]
			else:
				self.field_btn[f"{field}{player}"].x = self.mat[player]["mat"].x + self.mat[player]["field"][field][0]
			self.gd["select_btns"].append(f"{field}{player}")

		if self.gd["uptomay"]:
			if "Encore" in self.gd["phase"]:
				self.sd["btn"]["end"].text = "End Encore"
			else:
				# if "do" in self.gd["effect"]:
				# 	self.sd["btn"]["end"].text = "Continue Effect"
				# else:
				self.sd["btn"]["end"].text = "End Effect"
				if isinstance(self.gd["effect"][0], int) and self.gd["effect"][0] > 1:
					self.sd["btn"]["end"].x = Window.width - self.sd["btn"]["end"].size[0] * 2
					self.sd["btn"]["end_eff"].y = 0
			self.sd["btn"]["end"].disabled = False
			self.sd["btn"]["end"].y = 0
			self.sd["btn"]["end_attack"].y = -Window.height
			self.sd["btn"]["end_phase"].y = -Window.height

	def select_field(self, p=False, *args):
		self.gd["moveable"] = []
		self.gd["select_btns"] = []
		self.act_ability_show(hide=True)
		if p:
			status = self.gd["pay_status"]
		else:
			status = self.gd["status"]

		if "Opp" in status and self.gd["rev"]:
			player = self.gd["active"]
		elif "Opp" in status or self.gd["rev"]:
			player = self.gd["opp"]
		else:
			player = self.gd["active"]

		if "Clock" in status:
			if len(self.pd[player]["Clock"]) > 0:
				self.gd["select_btns"].append(f"Clock{player}")
				if "Top" in status:
					self.cd[self.pd[player]["Clock"][-1]].selectable()
		else:
			fields = []
			if "Change" in status:
				fields = [self.cd[self.gd["ability_trigger"].split("_")[1]].pos_old]
			elif "Center" in status:
				fields = list(self.gd["stage"][:3])
			elif "Back" in status:
				fields = list(self.gd["stage"][3:])
			else:
				fields = list(self.gd["stage"])

			if "Open" in status:
				fields = [f for f in fields if self.pd[player][f[:-1]][int(f[-1])] == ""]
			if "seperate" in self.gd["effect"]:
				for field in list(fields):
					if any(d for d in self.gd["target"] if field in d):
						fields.remove(field)
			for field in fields:
				self.field_btn[f"{field}{player}s"].x = self.mat[player]["field"][field][0] - self.sd["padding"]
				self.field_btn[f"{field}{player}s"].y = self.mat[player]["field"][field][1] - self.sd["padding"]

				if "Opp" in status:
					self.field_btn[f"{field}{player}"].x = self.mat[player]["mat"].x + self.mat[player]["mat"].size[0] - \
					                                       self.sd["card"][0] - self.mat[player]["field"][field][0]
				else:
					self.field_btn[f"{field}{player}"].x = self.mat[player]["field"][field][0] + self.mat[player][
						"mat"].x
				self.gd["select_btns"].append(f"{field}{player}")

		if self.gd["uptomay"]:
			self.sd["btn"]["end"].text = "End Effect"
			self.sd["btn"]["end"].disabled = False
			self.sd["btn"]["end"].y = 0
			self.sd["btn"]["end_attack"].y = -Window.height
			self.sd["btn"]["end_phase"].y = -Window.height
			if isinstance(self.gd["effect"][0], int) and self.gd["effect"][0] > 1 and len(self.gd["target"]) % \
					self.gd["effect"][0] != 0 and len(self.gd["target"]) > 2:
				self.sd["btn"]["end"].x = Window.width - self.sd["btn"]["end"].size[0] * 2
				self.sd["btn"]["end_eff"].y = 0

	def janken(self, *args):
		if self.gd["janken_result"] == 0:
			Clock.schedule_once(self.janken_start, move_dt_btw)
		elif self.gd["janken_result"] != 0:
			if "winner" in self.gd["effect"]:
				if self.gd["janken_result"] < 0 and self.gd["active"] == "1":
					self.gd["rev"] = True
				elif self.gd["janken_result"] > 0 and self.gd["active"] == "2":
					self.gd["rev"] = True
				self.gd["done"] = True

			self.gd["janken_result"] = 0

			if "janken" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("janken")

			self.ability_effect()

	# if "draw" in self.gd["effect"]:
	# 	self.gd["draw"] += self.gd["effect"][0]
	# 	Clock.schedule_once(self.draw, move_dt_btw)
	def replaceImage_test(self):
		for nx in range(1, 5):
			self.test[str(nx)] = Label(text="　" * nx, font_size=self.sd["btn"]["label"].font_size, valign='middle')
			self.test[str(nx)].texture_update()
		for nx in range(5):
			self.iach[str(nx)] = Image(source=f"atlas://{img_in}/other/blank", size=(
				self.test["1"].texture.size[0] * 1.05, self.test["1"].texture.size[1] * 1.05),
			                           allow_stretch=True, size_hint=(None, None))
			self.sd["popup"]["p_sct"].add_widget(self.iach[str(nx)])

	def stack_btn_ability(self, qty):
		for inx in range(len(self.sd["sbtn"]), qty - len(self.sd["sbtn"]) + 1):
			self.sd["sbtn"][f"{inx}"] = Labelbtn(size=(self.sd["card"][0] * 5 + self.sd["padding"], self.sd["card"][1]))
			self.sd["sbtn"][f"{inx}"].btn.bind(on_release=self.stack_resolve)

	def stack_btn_act(self, qty):
		for inx in range(len(self.sd["sbact"]), qty - len(self.sd["sbact"]) + 1):
			self.sd["sbact"][f"{inx}"] = Labelbtn(
					size=(self.sd["card"][0] * 5 + self.sd["padding"], self.sd["card"][1]))
			self.sd["sbact"][f"{inx}"].btn.bind(on_release=self.act_popup_btn)

	def replaceImage(self):
		for nx in range(len(self.iach), len(self.sd["btn"]["label"].anchors)):
			self.iach[str(nx)] = Image(source=f"atlas://{img_in}/other/blank", size=(
				self.test["1"].texture.size[0] * 1.05, self.test["1"].texture.size[1] * 1.05),
			                           allow_stretch=True, size_hint=(None, None))
			self.sd["popup"]["p_sct"].add_widget(self.iach[str(nx)])

		self.gd["inx"] = 0
		for item in self.sd["btn"]["label"].anchors:
			self.iach[str(self.gd["inx"])].size = (
				self.test[item[-1]].texture.size[0] * 1.05, self.test[item[-1]].texture.size[1] * 1.05)
			self.iach[str(self.gd["inx"])].source = f"atlas://{img_in}/other/{item[:-3]}"
			self.iach[str(self.gd["inx"])].pos = (
				self.sd["padding"] * 1.5 + self.sd["btn"]["label"].anchors[item][0] + self.sd["btn"]["label"].x,
				self.sd["btn"]["label"].size[1] - self.sd["padding"] / 4.5 - self.sd["btn"]["label"].anchors[item][1] -
				self.test[item[-1]].texture.size[1] + self.sd["btn"]["label"].y)
			self.gd["inx"] += 1

	def confirm_popup(self, dt=.0, ind="", c="", icon="", a="", o=""):
		self.popup_clr_button()
		self.gd["confirm_pop"] = True
		if self.gd["confirm_var"]:
			self.gd["confirm_temp"] = dict(self.gd["confirm_var"])
			for key in self.gd["confirm_var"]:
				if key == "ind":
					ind = self.gd["confirm_var"][key]
				elif key == "c":
					c = self.gd["confirm_var"][key]
				elif key == "icon":
					icon = self.gd["confirm_var"][key]
				elif key == "a":
					a = self.gd["confirm_var"][key]
				elif key == "o":
					o = self.gd["confirm_var"][key]
			self.gd["confirm_var"] = {}
		self.gd["p_ind"] = ind
		self.gd["p_l"] = []
		self.gd["p_c"] = f"{c}_auto"
		self.gd["popup_done"] = (True, False)
		self.sd["popup"]["popup"].title = f"Confirm {c}"
		self.sd["popup"]["p_scv"].do_scroll_y = False
		self.sd["popup"]["stack"].clear_widgets()
		if a != "":
			self.gd["ability"] = a

		xscat = (self.sd["padding"] + self.sd["card"][0]) * starting_hand
		self.gd["p_hand"] = starting_hand

		if self.gd["rev"]:
			player = self.gd["opp"]
		else:
			player = self.gd["active"]

		self.gd["p_yscat"] = self.sd["padding"] * 3 + self.sd["card"][1] * 3 + self.sd["padding"] * 4 + \
		                     self.sd["popup"]["popup"].title_size + self.sd["popup"]["popup"].separator_height

		self.sd["btn"]["down_again"].y = -Window.height * 2
		for btn in ("yes_btn", "no_btn", "field_btn"):
			if btn[0] == "f":
				self.sd["btn"][btn].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
				self.sd["btn"][btn].center_x = xscat / 2. - self.sd["padding"] * 0.75
				self.sd["btn"][btn].y = self.sd["padding"] * 3 + self.sd["card"][1] / 2.
			else:
				self.sd["btn"][btn].size = (self.sd["card"][0] * 1.5, self.sd["card"][1] / 2.)
				self.sd["btn"][btn].y = self.sd["padding"] * 1.5
				if btn[0] == "y" and "encore" not in self.gd["p_c"]:
					self.sd["btn"][btn].center_x = xscat / 4. - self.sd["padding"] * 0.75
				elif btn[0] == "n" and "encore" not in self.gd["p_c"]:
					self.sd["btn"][btn].center_x = xscat / 4. * 3 - self.sd["padding"] * 0.75

		if "encore" in self.gd["p_c"]:
			self.sd["btn"]["yes_btn"].x = -Window.width * 2
			self.sd["btn"]["no_btn"].x = -Window.width * 2
			self.sd["btn"]["effect_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
			self.sd["btn"]["effect_btn"].center_x = xscat / 4. * 3 - self.sd[
				"padding"] * 0.75  # - self.sd["card"][0] / 2 + self.sd["padding"]
			self.sd["btn"]["effect_btn"].y = self.sd["padding"] * 1.5

			self.sd["btn"]["field_btn"].center_x = xscat / 4. - self.sd["padding"]
			self.sd["btn"]["field_btn"].y = self.sd["padding"] * 1.5
			self.gd["p_yscat"] = self.sd["padding"] * 3.5 + self.sd["card"][1] * 1.5 + self.sd["padding"] * 4 + \
			                     self.sd["popup"]["popup"].title_size + self.sd["popup"]["popup"].separator_height
		elif "reflev" in self.gd["p_c"]:
			self.sd["btn"]["yes_btn"].x = -Window.width * 2
			self.sd["btn"]["no_btn"].x = -Window.width * 2
			self.sd["btn"]["effect_btn"].x = -Window.width * 2
			self.sd["btn"]["field_btn"].center_x = xscat / 2. - self.sd["padding"]
			self.sd["btn"]["field_btn"].y = self.sd["padding"] * 1.5
			self.gd["p_yscat"] = self.sd["padding"] * 3.5 + self.sd["card"][1] * 1 + self.sd["padding"] * 4 + \
			                     self.sd["popup"]["popup"].title_size + self.sd["popup"]["popup"].separator_height
		pos = (self.sd["padding"] / 4, self.sd["padding"] * 5 + self.sd["card"][1])
		confirm_text = "　"
		self.sd["btn"]["label"].halign = "left"
		if "Overplay" in self.gd["p_c"]:
			idm = self.gd["p_ind"].split("_")
			confirm_text = f"Do you want to play \"{self.cd[idm[0]].name}\" over \"{self.cd[idm[1]].name}\"?"
			self.gd["p_l"] = [idm[0], "arrow", idm[1]]
		elif "Restart" in self.gd["p_c"]:
			self.sd["btn"]["down_again"].size = self.sd["btn"]["field_btn"].size
			self.sd["btn"]["down_again"].pos = self.sd["btn"]["field_btn"].pos
			self.sd["btn"]["field_btn"].y = -Window.height * 2
			self.sd["btn"]["label"].halign = "center"
			self.gd["p_yscat"] = self.sd["padding"] * 7.5 + self.sd["card"][1] * 1.5 + self.sd["popup"][
				"popup"].title_size + self.sd["popup"]["popup"].separator_height
			confirm_text = "Would you like to close the app?\n\n*Downloaded files will only be loaded after a restart."
		elif "Download" in self.gd["p_c"]:
			# for btn in self.sd["main_btn"]:
			# 	btn.disabled = True
			self.sd["popup"]["popup"].title = "Confirm download"
			self.gd["p_ind"] = float(self.gd["p_ind"])
			if self.gd["p_ind"] < 102:
				mb = f"{round(self.gd['p_ind'], 2)} KB"
			else:
				mb = f"{round(self.gd['p_ind'] / 1024, 2)} MB"
			confirm_text = f"Would you like to download the selected game data?\n\nDownload size:\t{mb}\n\n*It is recommended connecting to WI-FI before downloading."
			self.gd["p_yscat"] = self.sd["padding"] * 7.5 + self.sd["card"][1] * 1 + self.sd["popup"][
				"popup"].title_size + self.sd["popup"]["popup"].separator_height
			self.sd["btn"]["field_btn"].y = -Window.height * 2
			self.sd["btn"]["label"].halign = "center"
			pos = (self.sd["padding"] / 4, self.sd["padding"] * 3.5 + self.sd["card"][1] / 2)
		elif "astock" in self.gd["p_c"]:
			self.sd["popup"]["popup"].title = f"Confirm cost"
			confirm_text = f"Do you want to pay the [ACT] cost using markers of one of your character on stage?\n \n{self.gd['ability']}"
			self.gd["p_yscat"] -= self.sd["card"][1] * 1.5
		elif "confirm" in self.gd["p_c"] or "ability" in self.gd["p_c"]:
			ability = self.cardinfo.replaceMultiple(self.gd["ability"])
			confirm_text = f"Do you agree to activate the following ability?\n \n{ability}"
			self.gd["p_l"] = [self.gd["p_ind"]]
		elif "trigger" in self.gd["p_c"]:
			confirm_text = f"Do you want to activate the following trigger?\n \n{self.gd['ability']}"
		elif "counter" in self.gd["p_c"]:
			confirm_text = "Do you want to play a card which has a Counter Icon on it?\n "
		elif "encore" in self.gd["p_c"]:
			self.gd['encore_ind'] = ind
			self.sd["popup"]["popup"].title = "Confirm Encore ability"
			self.gd["inx"] = 0
			# xpos = xscat / float(len(self.gd["effect"]) - 1)
			for item in ("Stock3", "Stock2", "Stock1", "Character", "Trait", "Clock"):
				if item in self.gd["effect"]:
					self.sd["btn"][f"encore_{item}"].size = (
						self.sd["card"][0] * 5 + self.sd["padding"], self.sd["card"][1] / 1.5)
					self.sd["btn"][f"encore_{item}"].y = self.sd["padding"] * 3 + self.sd["card"][1] / 2. + \
					                                     (self.sd["padding"] * 1.5 + self.sd["card"][1] / 1.5) * \
					                                     self.gd["inx"]
					# self.sd["btn"][f"encore_{item}"].center_x = xscat / 2. - self.sd["padding"]
					self.sd["btn"][f"encore_{item}"].x = self.sd["padding"]
					self.gd["inx"] += 1

			confirm_text = f"Do you want to encore \"{self.cd[self.gd['encore_ind']].name}\"?\n \n "

			self.gd["p_yscat"] += (self.sd["card"][1] / 1.5 + self.sd["padding"] * 1.5) * self.gd["inx"]
			pos = (self.sd["padding"] / 4, (
					self.sd["padding"] * 1.5 + self.sd["card"][1] / 1.5) * (self.gd["inx"]) + self.sd["padding"] * 2)
			self.gd["p_l"] = [self.gd["encore_ind"]]
		elif "reflev" in self.gd["p_c"]:
			self.sd["popup"]["popup"].title = "Confirm rule action"
			self.gd["inx"] = 0
			for item in ("reshuffle", "levelup"):
				self.sd["btn"][f"{item}_btn"].size = (
					self.sd["card"][0] * 5 + self.sd["padding"], self.sd["card"][1] / 1.5)
				self.sd["btn"][f"{item}_btn"].y = self.sd["padding"] * 3 + self.sd["card"][1] / 2. + \
				                                  (self.sd["padding"] * 1.5 + self.sd["card"][1] / 1.5) * \
				                                  self.gd["inx"]
				# self.sd["btn"][f"encore_{item}"].center_x = xscat / 2. - self.sd["padding"]
				self.sd["btn"][f"{item}_btn"].x = self.sd["padding"]
				self.gd["inx"] += 1
			confirm_text = f"Choose which rule action to perform first."
			self.gd["p_yscat"] += (self.sd["card"][1] / 1.5 + self.sd["padding"] * 1.5) * self.gd["inx"]
			pos = (self.sd["padding"] / 4, self.sd["padding"] * 3.5 + self.sd["card"][1] / 3 + (
					self.sd["padding"] * 1.5 + self.sd["card"][1] / 1.5) * (self.gd["inx"]) + self.sd["padding"] * 2)

		self.sd["btn"]["label"].text_size = (xscat * 0.9, None)
		self.sd["btn"]["label"].text = confirm_text
		self.sd["btn"]["label"].texture_update()
		self.sd["btn"]["label"].height = self.sd["btn"]["label"].texture.size[1]
		self.sd["btn"]["label"].pos = pos
		self.replaceImage()
		if icon != "":
			self.gd["p_l"] = [icon]

		self.sd["popup"]["popup"].size = (
			xscat + self.sd["padding"] * 2, self.gd["p_yscat"] + self.sd["btn"]["label"].texture.size[1])

		self.sd["popup"]["p_scv"].y = self.sd["btn"]["label"].y + self.sd["btn"]["label"].texture.size[1] + \
		                              self.sd["padding"] * 1.5
		self.sd["popup"]["p_scv"].size = (xscat, self.gd["p_height"])
		self.sd["popup"]["stack"].size = self.sd["popup"]["p_scv"].size

		if "Restart" not in self.gd["p_c"] or "Download" not in self.gd["p_c"]:
			if "sspace" in self.gd["p_l"]:
				self.gd["p_l"].remove("sspace")
			nx, ns = self.get_index_stack(self.gd["p_l"], self.gd["p_hand"])
			if nx:
				self.gd["p_l"].insert(nx, "sspace")
				self.sd["popup"]["sspace"].size = (
					self.sd["popup"]["sspace"].size_o[0] * ns, self.sd["popup"]["sspace"].size[1])
			for inx in self.gd["p_l"]:
				if "sspace" in inx:
					self.sd["popup"]["stack"].add_widget(self.sd["popup"][inx])
				elif inx == "arrow":
					self.sd["popup"]["stack"].add_widget(self.sd["popup"]["icon"])
					self.sd["popup"]["icon"].source = f"atlas://{img_in}/other/arrow"
				elif inx in icon:
					self.sd["popup"]["stack"].add_widget(self.sd["popup"]["icon"])
					self.sd["popup"]["icon"].source = f"atlas://{img_in}/other/{inx}"
				else:
					self.cpop[inx].selected(False)
					self.cpop[inx].update_text()
					self.sd["popup"]["stack"].add_widget(self.cpop[inx])

		self.sd["popup"]["popup"].open()

	def joke(self, player,a=""):
		if "d" in a:
			self.sd["joke"][player].center_x = self.mat[player]["mat"].size[0] / 2.

			anim = Animation(d=joke_dt, y=0) + Animation(d=joke_dt * 8) + Animation(d=joke_dt, x=-Window.width)
			self.mat[player]["mat"].remove_widget(self.sd["joke"][player])
			self.mat[player]["mat"].add_widget(self.sd["joke"][player])
			anim.start(self.sd["joke"][player])
		elif "f" in a:
			self.sd["joke"][player].center_x = self.mat[player]["mat"].size[0]

			anim = Animation(d=joke_dt, y=0) + Animation(d=joke_dt * 8) + Animation(d=joke_dt, x=-Window.width)
			self.mat[player]["mat"].remove_widget(self.sd["joke"][player])
			self.mat[player]["mat"].add_widget(self.sd["joke"][player])
			anim.start(self.sd["joke"][player])

	def confirm_result(self, btn):
		self.sd["popup"]["popup"].dismiss()
		self.popup_clr()
		self.gd["confirm_pop"] = False
		if self.gd["rev"]:
			player = self.gd["opp"]
		else:
			player = self.gd["active"]

		if "pay" in self.gd["ability_doing"]:
			self.gd["paypop"] = True

		# if self.download:
		# 	self.download = False
		# 	Clock.schedule_once(self.atlas_make_init)

		if btn.cid == "" or btn.cid == "0":
			# if "Download" in self.gd["confirm_trigger"] or "Restart" in self.gd["confirm_trigger"]:
			# for btn in self.sd["main_btn"]:
			# 	btn.disabled = False
			if self.gd["ability_doing"] in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove(self.gd["ability_doing"])
			if "do" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("do")
			if "Overplay" in self.gd["confirm_trigger"]:
				self.hand_size(self.gd["active"])
				self.gd["selected"] = ""
				self.play_card_done()
			elif "astock" in self.gd["confirm_trigger"]:
				ind = self.gd["pay"].index("Stock")
				if len(self.pd[self.gd["ability_trigger"].split("_")[1][-1]]["Stock"]) >= self.gd["pay"][ind + 1]:
					if self.net["game"] and self.gd["active"] == "1":
						self.net["act"][5] = 1
						self.net["send"] = False
					self.gd["confirm_trigger"] = ""
					Clock.schedule_once(self.pay_condition)
				else:
					if self.net["game"] and self.gd["active"] == "1":
						self.net["act"][0] = ""
					Clock.schedule_once(self.play_card_done)
			elif "AUTO" in self.gd["confirm_trigger"]:
				self.gd["confirm1"] = [True, 0]
				if self.net["game"]:
					self.net["act"][5] = 0
				Clock.schedule_once(self.ability_effect)
			elif "ACT" in self.gd["confirm_trigger"] or "Character" in self.gd["confirm_trigger"]:
				if self.net["game"] and self.gd["active"] == "1":
					self.net["act"][0] = ""
				Clock.schedule_once(self.play_card_done)
			# Clock.schedule_once(self.ability_effect, ability_dt)
			# elif "Character" in self.gd["confirm_trigger"]:
			# 	Clock.schedule_once(self.play_card_done, ability_dt)

			# elif "Trigger" in self.gd["confirm_trigger"]:
			# 	self.gd["confirm1"] =[True,0]
			# 	Clock.schedule_once(self.ability_effect, move_dt_btw)
			elif "Counter" in self.gd["confirm_trigger"]:
				Clock.schedule_once(self.counter_step_done)

		elif btn.cid == "1":
			if "Overplay" in self.gd["confirm_trigger"]:
				self.play(self.gd["play"])
			elif "Restart" in self.gd["confirm_trigger"]:
				self.reset()
			elif "Download" in self.gd["confirm_trigger"]:
				self.net["var"][1] = 1
				# Clock.schedule_once(partial(self.popup_text, "Download"))
				self.decks["sets"].dismiss()
				self.multiplay_cjpopup()
				self.mcreate_popup.open()
				Clock.schedule_once(partial(self.mconnect, "down"), move_dt_btw)
			elif "astock" in self.gd["confirm_trigger"]:
				self.gd["mstock"] = ""
				Clock.schedule_once(partial(self.pay_mstock, "as"))
			elif "AUTO" in self.gd["confirm_trigger"]:
				self.gd["confirm_result"] = btn.cid
				self.gd["confirm1"] = [True, 1]
				if self.net["game"]:
					self.net["act"][5] = 1
				Clock.schedule_once(self.pay_condition)
			elif "Character" in self.gd["confirm_trigger"]:
				if "janken" in self.gd["effect"]:
					Clock.schedule_once(self.janken)
			elif "ACT" in self.gd["confirm_trigger"]:
				if self.net["game"] and self.gd["active"] == "1":
					self.net["act"][5] = 1
					self.net["send"] = False
				self.gd["confirm_trigger"] = ""
				Clock.schedule_once(self.pay_condition)
			# elif "Trigger" in self.gd["confirm_trigger"]:
			# 	# self.gd["confirm_result"] = btn.cid
			# 	# if "door" in self.gd["confirm_trigger"] or "gate" in self.gd["confirm_trigger"]:
			# 	# 	self.gd["p_c"] = ""
			# 	# 	Clock.schedule_once(self.salvage, move_dt_btw)
			# 	self.gd["confirm_result"] = btn.cid
			# 	Clock.schedule_once(self.ability_effect, move_dt_btw)
			elif "Counter" in self.gd["confirm_trigger"]:
				Clock.schedule_once(self.counter, move_dt_btw)

		self.gd["confirm_trigger"] = ""

	def janken_start(self, *args):
		if self.net["game"]:
			self.net["status"] = "janken"

		self.gd["j_result"] = 0

		self.janken_reset()

		self.sd["janken"]["popup"].open()

	def janken_done(self, *args):
		if self.gd["j_result"] != 0 and self.gd["turn"] == 0:
			if self.gd["j_result"] > 0:
				self.gd["starting_player"] = "1"
				self.gd["second_player"] = "2"
			elif self.gd["j_result"] < 0:
				self.gd["starting_player"] = "2"
				self.gd["second_player"] = "1"

			if self.gd["debug"] and not self.net["game"]:
				if self.gd["d_opp_first"]:
					self.gd["starting_player"] = "2"
					self.gd["second_player"] = "1"
				elif self.gd["d_pl_first"]:
					self.gd["starting_player"] = "1"
					self.gd["second_player"] = "2"
					##### starting setup ####
					player = "1"
					# Level me
					for rr in range(3):
						temp = self.pd[player]["Library"].pop(-1)
						self.pd[player]["Level"].append(temp)
						self.level_size(player)
						self.update_colour(player)
						self.check_cont_ability()
					# Stock me
					for rr in range(3):
						temp = self.pd[player]["Library"].pop()
						self.pd[player]["Stock"].append(temp)
						self.stock_size(player)
						self.update_field_label()


			self.gd["active"] = str(self.gd["starting_player"])
			self.gd["opp"] = str(self.gd["second_player"])

			self.change_active_background()

			for var in self.pd[self.gd["second_player"]]["done"]:
				self.pd[self.gd["second_player"]]["done"][var] = True
			self.pd[self.gd["second_player"]]["done"]["Mulligan"] = False
			self.pd[self.gd["starting_player"]]["done"]["Janken"] = True

			Clock.schedule_once(self.draw_both, ability_dt)
			self.sd["janken"]["popup"].dismiss()
		elif self.gd["j_result"] != 0:
			self.gd["janken_result"] = int(self.gd["j_result"])
			self.sd["janken"]["popup"].dismiss()
			Clock.schedule_once(self.janken)
		else:
			self.janken_reset()

	def janken_reset(self, *args):
		for card in self.gd["janken_choice"][1:]:
			self.sd["janken"][f"j{card}1"].show_back()
			self.sd["janken"][f"j{card}0"].show_front()
			self.sd["janken"][f"j{card}0"].disabled = False

		self.gd["j_hand"] = ""
		self.gd["j_hand_opp"] = ""

		self.sd["janken"]["button"].disabled = True
		self.sd["janken"]["button"].text = "Choose One"

	def janken_pick(self, btn):
		self.gd["j_hand"] = str(btn.cid)

		for card in self.gd["janken_choice"]:
			self.sd["janken"][f"j{card}0"].disabled = True
			if card != self.gd["j_hand"]:
				self.sd["janken"][f"j{card}0"].show_back()

		if self.net["game"]:
			Clock.schedule_once(partial(self.popup_text, "waiting"), ability_dt)
			self.mconnect("janken")
		else:
			Clock.schedule_once(self.janken_results)

	def janken_results(self, *args):
		if not self.net["game"]:  # if self.gd["com"]:
			# randomise opponent choice
			# r = randint(0, 2)
			self.gd["j_hand_opp"] = choice(self.gd["janken_choice"][1:])

		# show opponent choice
		self.sd["janken"][f"j{self.gd['j_hand_opp']}1"].show_front()

		# compare choices and decide if win/loose/tie
		if self.gd["j_hand"] == self.gd["j_hand_opp"]:
			self.sd["janken"]["button"].text = "Tie"
		elif self.gd["j_hand"] == "p" and self.gd["j_hand_opp"] == "k":
			self.sd["janken"]["button"].text = "Win"
			self.gd["j_result"] += 1
		elif self.gd["j_hand"] == "s" and self.gd["j_hand_opp"] == "p":
			self.sd["janken"]["button"].text = "Win"
			self.gd["j_result"] += 1
		elif self.gd["j_hand"] == "k" and self.gd["j_hand_opp"] == "s":
			self.sd["janken"]["button"].text = "Win"
			self.gd["j_result"] += 1
		else:
			self.sd["janken"]["button"].text = "Lose"
			self.gd["j_result"] -= 1

		# enable button
		self.sd["janken"]["button"].disabled = False

	def look_top(self, btn):
		if btn is not None:
			try:
				btn = str(btn.cid)
			except AttributeError:
				btn = str(btn)
		self.sd["popup"]["popup"].dismiss()
		idm = self.gd["ability_trigger"].split("_")[1]
		if btn is not None and btn == "s":
			if "opp" in self.gd["effect"] and idm[-1] == "1":
				opp = "2"
			elif "opp" in self.gd["effect"] and idm[-1] == "2":
				opp = "1"
			else:
				opp = idm[-1]

			if self.gd["effect"][0] == -14:
				if "Stage" in self.gd["effect"]:
					stage = [s for s in self.pd[opp]["Center"] + self.pd[opp]["Back"] if s != ""]

				if "Trait" in self.gd["effect"]:
					traits = self.gd["effect"][self.gd["effect"].index("Trait") + 1].split("_")
					times = len([t for t in stage if any(tr in self.cd[t].trait_t for tr in traits)])
				self.gd["effect"][0] = int(times)

			c = "Look"
			self.sd["btn"]["draw_btn"].disabled = False
			qty = 0
			if "top" in self.gd["effect"] and isinstance(self.gd["effect"][self.gd["effect"].index("top") + 1], int):
				qty = self.gd["effect"][self.gd["effect"].index("top") + 1]
			elif "hand" in self.gd["effect"]:
				qty = self.gd["effect"][self.gd["effect"].index("hand") + 1]
				self.gd["search_type"] = self.gd["effect"][self.gd["effect"].index("hand") + 2]
				c += "_hand"
				if "stacked" in self.gd["effect"]:
					# if self.net["game"] and self.gd["oppchoose"]:
					# 	self.gd["oppchoose"] = False
					c += "_stacked"
			elif "bdeck" in self.gd["effect"]:
				qty = self.gd["effect"][self.gd["effect"].index("bdeck") + 1]
				c += "_bdeck"
			elif "waiting" in self.gd["effect"]:
				qty = self.gd["effect"][self.gd["effect"].index("waiting") + 1]
				c += "_waiting"
			elif "reorder" in self.gd["effect"] and "waiting" not in self.gd["effect"] and "bdeck" not in self.gd[
				"effect"]:
				qty = self.gd["effect"][0]
				c += "_reorder"
			elif "look" in self.gd["effect"]:
				c += "_look_auto"
			elif "stack" in self.gd["effect"]:
				c += "_stack"
				qty = list(self.gd["effect"][self.gd["effect"].index("stack") + 1])

			if "fix" in self.gd["effect"]:
				c += "_fix"
			if self.gd["clear"]:
				self.gd["p_l"] = []
			self.sd["popup"]["popup"].title = f"{self.gd['ability_trigger'].split('_')[0]} Effect"
			self.gd["confirm_var"] = {"o": opp, "c": c, "m": qty, "l": self.gd["effect"][0]}
			Clock.schedule_once(self.popup_start, popup_dt)
		elif not self.gd["target"]:# and idm[-1] == "1":
			if self.net["game"] and "looktopopp" in self.gd["effect"] and not self.net["send"]:
				self.net["var"] = self.gd["chosen"]
				self.net["var1"] = "oppchoose"
				if not self.poptext:
					Clock.schedule_once(partial(self.popup_text, "waitingser"))
				self.mconnect("oppchoose")
				return False
			else:
				if "reorder" in self.gd["p_c"]:
					self.gd["target_temp"].append("r")
				# elif "stack" in self.gd["p_c"]:
				# 	self.gd["target_temp"].append("s")
				else:
					self.gd["target_temp"].append(btn)
				if "sspace" in self.gd["p_l"]:
					self.gd["p_l"].remove("sspace")
				if btn is not None and btn == "l":
					self.gd["target_temp"].append(len(self.gd["p_l"]))
					self.gd["target_temp"].append(len(self.gd["chosen"]))
					chosen = list(self.gd["chosen"])
					if len(chosen) < len(self.gd["p_l"]):
						for r in range(len(self.gd["p_l"]) - len(chosen)):
							if "reorder" in self.gd["effect"] and (
									"waiting" in self.gd["effect"] or "bdeck" in self.gd["effect"]):
								chosen.append("R")
							elif "shuff" in self.gd["effect"]:
								chosen.append("D")
							elif "stacked" in self.gd["effect"]:
								chosen.append("D")
							elif "stack" in self.gd["effect"]:
								chosen.append("S")
							else:
								chosen.append("W")
					for ind in chosen:
						self.gd["target_temp"].append(ind)
				if "reorder" in self.gd["effect"] and (
						"waiting" in self.gd["effect"] or "bdeck" in self.gd["effect"]) and "reorder" not in self.gd["p_c"]:
					if len(self.gd["p_l"]) > len(self.gd["chosen"]):
						for inx in self.gd["chosen"]:
							if inx in self.gd["p_l"]:
								self.gd["p_l"].remove(inx)
						if "opp" in self.gd["effect"] and idm[-1] == "1":
							opp = "2"
						elif "opp" in self.gd["effect"] and idm[-1] == "2":
							opp = "1"
						else:
							opp = idm[-1]
						self.gd["uptomay"] = False
						self.sd["btn"]["draw_btn"].disabled = True
						self.sd["btn"]["Look_btn"].disabled = True
						self.gd["confirm_var"] = {"o": opp, "c": "Look_reorder_fix", "m": len(self.gd["p_l"]),
						                          "l": len(self.gd["p_l"])}
						Clock.schedule_once(self.popup_start, popup_dt)
						return False
				else:
					self.gd["p_c"] = "Look_"
					for xx in range(len(self.gd["target_temp"])):
						xx = self.gd["target_temp"].pop(0)
						self.gd["target"].append(xx)
				if self.net["game"] and self.gd["p_owner"] == "1" and not self.gd["oppchoose"]:
					for ind in self.gd["target"]:
						self.net["act"][4].append(ind)
				if self.net["game"] and "stacked" in self.gd["effect"] and self.gd["oppchoose"]:
					self.gd["oppchoose"] = False
					self.net["var"] = list(self.gd["target"])
					self.net["var1"] = "stacked"
					self.mconnect("plchoose")
					return False
				else:
					self.look_top(btn)
		else:
			item = self.gd["target"].pop(0)
			if "t" in item:
				self.look_top_done()
			elif "b" in item:
				if "opp" in self.gd["effect"]:
					if idm[-1] == "1":
						top = self.pd["2"]["Library"].pop(-1)
					elif idm[-1] == "2":
						top = self.pd["1"]["Library"].pop(-1)
				else:
					top = self.pd[idm[-1]]["Library"].pop(-1)
				if "bottom" in self.gd["effect"]:
					self.pd[top[-1]]["Library"].insert(0, top)
					self.stack(top[-1])
				elif "Waiting" in self.gd["effect"]:
					self.mat[top[-1]]["mat"].remove_widget(self.cd[top])
					self.mat[top[-1]]["mat"].add_widget(self.cd[top])
					self.cd[top].setPos(field=self.mat[top[-1]]["field"]["Waiting"], t="Waiting")
					self.pd[top[-1]]["Waiting"].append(top)
				self.look_top_done()
			elif "r" in item:
				d = self.gd["target"].pop(0)
				c = self.gd["target"].pop(0)
				for n in reversed(range(d)):
					ind = self.gd["target"].pop(n)
					if ind in self.emptycards:
						continue
					self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
					self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])
					self.pd[ind[-1]]["Library"].remove(ind)
					self.pd[ind[-1]]["Library"].append(ind)
					self.update_field_label()

				self.look_top_done()
			elif "l" in item:
				d = self.gd["target"].pop(0)
				c = self.gd["target"].pop(0)
				s = []
				for n in range(d):
					ind = self.gd["target"].pop(0)
					if ind in self.emptycards:
						continue
					if ind == "W":
						ind = str(self.pd[self.gd["p_owner"]]["Library"][-1])
						self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
						self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])
						self.pd[ind[-1]]["Library"].remove(ind)
						self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Waiting"], t="Waiting")
						self.pd[ind[-1]]["Waiting"].append(ind)
						self.update_field_label()
					elif ind == "R" or ind == "D":
						continue
					elif ind == "S":
						if len(self.gd["stacked"]["0"]) <= 1:
							s = list(self.gd["p_l"])
							for r in list(s):
								if r in self.gd["stacked"]["0"][0]:
									s.remove(r)
							self.gd["stacked"]["0"].append([])
						if len(s)>0:
							ind = s.pop()
						self.gd["stacked"]["0"][1].append(ind)
						self.gd["stacked"][ind] = 1
					else:
						if "stacked" in self.gd["effect"] and "hand" in self.gd["effect"]:
							for rr in self.gd["stacked"]["0"][self.gd["stacked"][ind]]:
								if rr in self.pd[rr[-1]]["Memory"]:
									self.pd[rr[-1]]["Memory"].remove(rr)
								else:
									self.pd[rr[-1]]["Library"].remove(rr)
								self.pd[rr[-1]]["Hand"].append(rr)
								self.cpop[rr].show_front()
								del self.gd["stacked"][rr]

							self.hand_size(ind[-1])
							self.gd["search_type"] = ""
							for rr in list(self.gd["stacked"].keys()):
								if rr == "0":
									continue
								if rr in self.pd[rr[-1]]["Memory"]:
									self.pd[rr[-1]]["Memory"].remove(rr)
								if "deck" in self.gd["effect"]:
									self.cd[rr].setPos(field=self.mat[rr[-1]]["field"]["Library"], t="Library")
									self.pd[rr[-1]]["Library"].append(rr)
								else:
									self.cd[rr].setPos(field=self.mat[rr[-1]]["field"]["Waiting"], t="Waiting")
									self.pd[rr[-1]]["Waiting"].append(rr)
								self.cpop[rr].show_front()
								del self.gd["stacked"][rr]
							self.gd["stacked"]["0"] = []
							self.update_field_label()
						else:
							self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
							self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])
							if "hand" in self.gd["effect"]:
								self.pd[ind[-1]]["Library"].remove(ind)
								self.pd[ind[-1]]["Hand"].append(ind)
								self.update_field_label()
								self.hand_size(ind[-1])
								self.gd["search_type"] = ""
								if "show" in self.gd["effect"]:
									self.gd["show"].append(ind)
							elif "waiting" in self.gd["effect"]:
								self.pd[ind[-1]]["Library"].remove(ind)
								self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Waiting"], t="Waiting")
								self.pd[ind[-1]]["Waiting"].append(ind)
								self.update_field_label()
							elif "bdeck" in self.gd["effect"]:
								self.pd[ind[-1]]["Library"].remove(ind)
								self.pd[ind[-1]]["Library"].insert(0, ind)
								self.stack(ind[-1])
							elif "stack" in self.gd["effect"]:
								if len(self.gd["stacked"]["0"])<=0:
									self.gd["stacked"]["0"].append([])
								self.gd["stacked"]["0"][0].append(ind)
								self.gd["stacked"][ind] = 0
				if len(self.gd["target"]) > 0:
					self.look_top(btn)
				elif "shuff" in self.gd["effect"]:
					self.gd["shuffle_trigger"] = "looktop"
					if "opp" in self.gd["effect"] and idm[-1] == "1":
						self.shuffle("2")
					elif "opp" in self.gd["effect"] and idm[-1] == "2":
						self.shuffle("1")
					else:
						self.shuffle(idm[-1])
				elif len(self.pd[idm[-1]]["Library"]) <= 0:
					self.gd["reshuffle_trigger"] = "looktop"
					Clock.schedule_once(self.refresh, move_dt_btw)
					return False
				else:
					self.look_top_done()

	def look_top_done(self, dt=0):
		self.check_cont_ability()
		if self.gd["reshuffle"]:
			self.gd["reshuffle"] = False
			self.gd["damage_refresh"] += 1
			self.gd["damageref"] = True
			self.gd["reshuffle_trigger"] = "looktop"
			Clock.schedule_once(self.damage, move_dt_btw)
			return False

		if "looktop" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("looktop")

		self.popup_clr()
		player = ""
		if "show" in self.gd["effect"] and len(self.gd["show"]) > 0:
			for p in self.gd["show"]:
				player = p[-1]

		self.do_check()

		ind = self.gd["ability_trigger"].split("_")[1]
		if "check" in self.gd["effect"] and ind[-1] == "1":
			self.popup_multi_info(cards=[self.pd[ind[-1]]["Library"][-1]], owner=ind[-1], t="top card")
		elif player == "2" and "show" in self.gd["effect"] and len(self.gd["show"]) > 0:
			self.popup_multi_info(cards=self.gd["show"], owner=player, t="Search")
		else:
			if "deck" in self.gd["effect"]:
				self.gd["shuffle_trigger"] = "ability"
				self.shuffle(ind[-1])
			else:
				self.ability_effect()

	def look_draw(self, btn):
		if "d" in btn.cid:
			pl = len(self.gd["p_l"])
			if "sspace" in self.gd["p_l"]:
				pl -= 1
			if pl <= self.gd["p_look"]:
				if pl >= self.gd["p_look"]:
					self.sd["btn"]["draw_btn"].disabled = True
				elif pl >= len(self.pd[self.gd["p_owner"]]["Library"]):
					self.sd["btn"]["draw_btn"].disabled = True
				else:
					self.gd["p_l"].append(self.pd[self.gd["p_owner"]]["Library"][-(pl + 1)])
					pl += 1
					if pl >= self.gd["p_look"]:
						self.sd["btn"]["draw_btn"].disabled = True
					if pl >= len(self.pd[self.gd["p_owner"]]["Library"]):
						self.sd["btn"]["draw_btn"].disabled = True

					if "_" in self.gd["p_c"]:
						phase = self.gd["p_c"].split("_")[0]
					else:
						phase = self.gd["p_c"]
					self.sd["btn"][f"{phase}_btn"].text = f"End Effect"
					self.popup_filter()

	def info_ability_pop(self, btn):
		self.cardinfo.import_data(self.cd[self.gd["ability_trigger"].split("_")[1]], annex_img)

	def play_card(self, *args):
		self.sd["btn"]["end"].disabled = True
		self.sd["btn"]["end_attack"].disabled = True
		self.sd["btn"]["end_phase"].disabled = True
		self.act_ability_show(hide=True)
		card = self.cd[self.gd["play_card"]]

		if self.net["game"] and not self.net["send"] and self.gd["active"] == "1":
			if card.card == "Event":
				self.net["var"] = [card.ind, card.pos_new,""]
			else:
				self.net["var"] = [card.ind, card.pos_new[:-1], card.pos_new[-1]]
			self.net["var1"] = "play_card"
			if not self.poptext:
				Clock.schedule_once(partial(self.popup_text, "waitingser"))
			self.mconnect("phase")
		else:
			card.turn = int(self.gd["turn"])

			if len(self.pd[self.gd["active"]]["Stock"]) >= card.cost and card.card != "Climax":
				self.pay_stock(card.cost)
				self.gd["payed"] = True

			if card.card == "Character":
				self.gd["ability_trigger"] = f"Character_{card.ind}"
				Clock.schedule_once(self.stack_ability)
			elif card.card == "Event":
				self.gd["ability_trigger"] = f"Event_{card.ind}"
				self.gd["effect"] = ab.event(card.text_c[0][0])
				self.gd["ability"] = card.text_c[0][0]
				# self.gd["auto_effect"] = [card.ind, self.gd["effect"], self.gd["ability"]]
				# self.gd["stack"][card.ind[-1]].append(self.gd["auto_effect"])
				self.check_auto_ability(play=card.ind, stacks=False)
				if "cards" in self.gd["effect"]:
					aa = False
					if "Hand" in self.gd["effect"]:
						if "lower" not in self.gd["effect"] and len(self.pd[card.ind[-1]]["Hand"]) >= self.gd["effect"][
							0]:
							aa = True
						elif "lower" in self.gd["effect"] and len(self.pd[card.ind[-1]]["Hand"]) <= self.gd["effect"][
							0]:
							aa = True
					if aa:
						self.gd["effect"] = self.gd["effect"][self.gd["effect"].index("do") + 1]
					else:
						self.gd["effect"] = []
				self.ability_event()

	def add_to_status(self, stat, eff):
		if "Opp" in eff:
			stat = f"Opp{stat}"
		if "top" in eff and "heal" in eff:
			stat = f"Top{stat}"
		if "Opposite" in eff:
			stat = f"Opposite{stat}"
		if "Change" in eff:
			stat = f"Change{stat}"
		if "Center" in eff:
			stat = f"Center{stat}"
		if "Back" in eff:
			stat = f"Back{stat}"
		if "Climax" in eff:
			stat = f"Climax{stat}"
		if "This" in eff:
			stat = f"This{stat}"
		if "Standing" in eff:
			stat = f"Standing{stat}"
		# if "Rest" in eff:
		# 	stat = f"Rest{stat}"
		# if "Reversed" in eff:
		# 	stat = f"Reversed{stat}"
		if "Antilvl" in eff:
			stat = f"Antilvl{stat}"
		if "Open" in eff:
			stat = f"Open{stat}"
		if "Other" in eff:
			stat = f"Other{stat}"
		if "Battle" in eff:
			if "both" in eff:
				stat = f"BattleBoth{stat}"
			elif "opp" in eff:
				stat = f"BattleBopp{stat}"
			else:
				stat = f"Battle{stat}"
		if "Cost" in eff:
			stat = f"Cost{eff[eff.index('Cost') + 1]}{stat}"
		if "Level" in eff:
			stat = f"Level{eff[eff.index('Level') + 1]}{stat}"
		if "BTrait" in eff:
			stat = f"BTrait_{eff[eff.index('BTrait') + 1]}_{stat}"
		elif "Trait" in eff:
			stat = f"Trait_{eff[eff.index('Trait') + 1]}_{stat}"
		elif "NameSet" in eff:
			stat = f"NameSet_{eff[eff.index('NameSet') + 1]}_{stat}"
		elif "Name=" in eff:
			stat = f"Name=_{eff[eff.index('Name=') + 1]}_{stat}"
		elif "Name" in eff:
			stat = f"Name_{eff[eff.index('Name') + 1]}_{stat}"
		elif "Text" in eff:
			stat = f"Text_{eff[eff.index('Text') + 1]}_{stat}"

		return stat

	def ability_event(self, dt=0, m=""):
		if self.gd["rev_counter"]:
			player = self.gd["opp"]
		else:
			player = self.gd["active"]

		# stage = self.pd[player]["Center"] + self.pd[player]["Back"]
		# stock = len(self.pd[player]["Stock"])
		# stand = len([s for s in stage if self.cd[s].status == "Stand"])
		self.gd["chosen"] = []
		self.gd["target"] = []
		self.gd["choose"] = False

		if self.gd["effect"] and isinstance(self.gd["effect"][0], int):
			if self.gd["effect"][0] > 0 and not self.gd["choose"]:
				self.gd["status"] = f"Select{self.gd['effect'][0]}"
				self.gd["status"] = self.add_to_status(self.gd["status"], self.gd["effect"])

		self.gd["uptomay"] = False
		if "may" in self.gd["effect"] or "upto" in self.gd["effect"]:
			self.gd["uptomay"] = True
			self.gd["confirm1"] = [False, 0]
			self.gd["confirm_result"] = ""
		if not self.gd["payed"]:
			self.gd["confirm1"] = [False, 0]
			self.gd["confirm_result"] = ""
		# if self.net["game"] and self.gd["active"]=="1":
		# 	self.net["act"][0] = ""

		# if "played" in self.gd["effect"]:
		# 	self.gd["ability_effect"].append("played")
		if "stock" in self.gd["effect"]:
			self.gd["stock"] = self.gd["effect"][self.gd["effect"].index("stock") + 1]
			self.gd["ability_effect"].append("stock")

		if "draw" in self.gd["effect"]:
			self.gd["ability_effect"].append("draw")
		if "pay" in self.gd["effect"] and not m:
			self.gd["paypop"] = False
			self.gd["ability_effect"].append("pay")
		elif "d_atk" in self.gd["effect"]:
			self.gd["d_atk"][0] = self.gd["effect"][1]
		elif "drawupto" in self.gd["effect"]:
			self.gd["draw_upto"] = self.gd["effect"][self.gd["effect"].index("drawupto") + 1]
			if self.gd["draw_upto"] > 0:
				self.gd["ability_effect"].append("drawupto")
		elif "confirm" in self.gd["effect"]:
			self.gd["confirm1"] = [False, 0]
			if self.net["game"]:
				self.net["send"] = False
			self.gd["ability_effect"].append("confirm")
		# elif "levelrev" in self.gd["effect"]:
		# 	self.gd["ability_effect"].append("levelrev")
		elif "stand" in self.gd["effect"]:
			self.gd["ability_effect"].append("stand")
		elif "mill" in self.gd["effect"]:
			self.gd["mill"] = self.gd["effect"][1]
			self.gd["mill_check"] = []
			self.gd["ability_effect"].append("mill")
		elif "rest" in self.gd["effect"] or "rested" in self.gd["effect"]:
			self.gd["ability_effect"].append("rest")
		elif "stand" in self.gd["effect"]:
			self.gd["ability_effect"].append("stand")
		elif "damageref" in self.gd["effect"]:
			self.gd["ability_effect"].append("damage")
			self.gd["damage_refresh"] = self.gd["effect"][self.gd["effect"].index("damageref") + 1]
			self.gd["damageref"] = True
		elif "damage" in self.gd["effect"]:
			self.gd["ability_effect"].append("damage")
			self.gd["damage"] = self.gd["effect"][self.gd["effect"].index("damage") + 1]
		elif "encore" in self.gd["effect"]:
			self.gd["ability_effect"].append("encore")
		elif "looktop" in self.gd["effect"] or "looktopopp" in self.gd["effect"]:
			if self.net["game"] and "looktopopp" in self.gd["effect"]:
				self.net["send"] = False
			self.gd["ability_effect"].append("looktop")
		elif "discard" in self.gd["effect"] or "ldiscard" in self.gd["effect"] or "cdiscard" in self.gd[
			"effect"] or "mdiscard" in self.gd["effect"]:
			self.gd["discard"] = self.gd["effect"][1]
			self.gd["search_type"] = self.gd["effect"][2]
			self.gd["ability_effect"].append("discard")
		elif "brainstorm" in self.gd["effect"]:
			self.gd["ability_effect"].append("brainstorm")
		elif "rescue" in self.gd["effect"]:
			self.gd["ability_effect"].append("rescue")
		elif "reveal" in self.gd["effect"]:
			self.gd["ability_effect"].append("reveal")
		elif "look" in self.gd["effect"]:
			self.gd["ability_effect"].append("look")
		elif "janken" in self.gd["effect"]:
			self.gd["ability_effect"].append("janken")
			self.gd["janken_result"] = 0
		elif "move" in self.gd["effect"]:  # and ab.req(a=self.gd["ability"], x=stock, ss=stand):
			self.gd["move"] = ""
			self.gd["ability_effect"].append("move")
		# elif "runner" in self.gd["effect"]:  # and ab.req(a=self.gd["ability"], x=stock, ss=stand):
		# 	if "self" in self.gd["effect"]:
		# 		self.gd["choose"] = True
		# 		self.gd["effect"].append(self.gd["auto_effect"][0])
		# 		self.gd["notarget"] = False
		# 	self.gd["ability_effect"].append("runner")
		elif "wind" in self.gd["effect"]:
			self.gd["ability_effect"].append("wind")
		elif "hander" in self.gd["effect"]:
			self.gd["ability_effect"].append("hander")
		elif "stocker" in self.gd["effect"]:
			self.gd["ability_effect"].append("stocker")
		elif "decker" in self.gd["effect"]:
			if "same_name" in self.gd["effect"]:
				if self.gd["save_name"] != "":
					self.gd["effect"][self.gd["effect"].index("Name=") + 1] = str(self.gd["save_name"])
					self.gd["save_name"] = ""
				Clock.schedule_once(self.ability_event)
				return False
			self.gd["ability_effect"].append("decker")
		elif "waitinger" in self.gd["effect"]:
			self.gd["ability_effect"].append("waitinger")
		elif "clocker" in self.gd["effect"]:
			self.gd["ability_effect"].append("clocker")
		elif "memorier" in self.gd["effect"]:
			self.gd["ability_effect"].append("memorier")
		elif "shuffle" in self.gd["effect"]:
			self.gd["ability_effect"].append("shuffle")
		elif "change" in self.gd["effect"] or "mchange" in self.gd["effect"] or "lchange" in self.gd[
			"effect"] or "changew" in self.gd["effect"]:
			self.gd["ability_effect"].append("change")
			self.gd["search_type"] = self.gd["effect"][2]
			self.gd["salvage"] = self.gd["effect"][1]
		elif "salvage" in self.gd["effect"] or "csalvage" in self.gd["effect"] or "msalvage" in self.gd["effect"]:
			self.gd["search_type"] = self.gd["effect"][2]
			self.gd["salvage"] = self.gd["effect"][0]
			self.gd["ability_effect"].append("salvage")
		elif "cstock" in self.gd["effect"]:
			self.gd["search_type"] = self.gd["effect"][2]
			self.gd["salvage"] = self.gd["effect"][0]
			# self.gd["salvage_cost"] = ab.pay(a=self.gd["ability"])
			self.gd["ability_effect"].append("cstock")
		elif "search" in self.gd["effect"] or "searchopp" in self.gd["effect"]:
			if "EName=" in self.gd["effect"][2] and len(self.gd["extra"]) > 0:
				temp = self.gd["extra"].pop(0)
				self.gd["search_type"] = f"{self.gd['effect'][2][1:]}_{self.cd[temp].name}"
			else:
				self.gd["search_type"] = self.gd["effect"][2]
			if self.net["game"] and "searchopp" in self.gd["effect"]:
				self.net["send"] = False
			self.gd["search"] = self.gd["effect"][0]
			self.gd["ability_effect"].append("search")
		elif "declare" in self.gd["effect"]:
			self.gd["ability_effect"].append("declare")
		elif "revive" in self.gd["effect"]:
			# self.gd["revive"] = []
			# self.gd["search_type"] = f"{self.gd['effect'][2]}_{self.gd['effect'][3]}"
			# self.gd["salvage"] = self.gd["effect"][0]
			self.gd["ability_effect"].append("revive")
		elif "give" in self.gd["effect"]:
			self.gd["ability_effect"].append("give")
		elif "reverser" in self.gd["effect"]:
			self.gd["ability_effect"].append("reverser")
		elif "heal" in self.gd["effect"]:
			self.gd["ability_effect"].append("heal")
		elif "marker" in self.gd["effect"]:
			self.gd["p_c"] = ""
			self.gd["ability_effect"].append("marker")
		if "power" in self.gd["effect"]:
			self.gd["ability_effect"].append("power")
		if "soul" in self.gd["effect"]:
			self.gd["ability_effect"].append("soul")
		if "trait" in self.gd["effect"]:
			self.gd["ability_effect"].append("trait")
		if "level" in self.gd["effect"]:
			self.gd["ability_effect"].append("level")
		if "distock" in self.gd["effect"]:
			self.gd["ability_effect"].append("distock")
		if "do" in self.gd["effect"]:
			if not m:
				if "do" not in self.gd["ability_effect"]:
					self.gd["ability_effect"].append("do")
				self.gd["done"] = False
			self.gd["do"][1] = list(self.gd["effect"][self.gd["effect"].index("do") + 1])
			self.gd["do"][0] = 1

		self.ability_effect()

	def do_check(self, effect=False, r=False):
		if "do" in self.gd["ability_effect"]:
			# self.gd["ability_effect"].remove("do")
			if r:
				self.gd["done"] = False
				self.gd["ability_effect"].remove("do")
			elif self.gd["do"][0] > 0:
				self.gd["done"] = True
			else:
				self.gd["done"] = False
				self.gd["ability_effect"].remove("do")
		if effect:
			self.ability_effect()

	def ability_effect(self, *args):
		if self.net["game"] and self.gd["ability_trigger"] and self.gd["ability_trigger"].split("_")[1][-1] == "2":
			self.gd["choose"] = True
			self.gd["p_owner"] = "2"
			self.gd["target"] = self.net["act"][4]

		if self.gd["phase"] != "Encore":
			self.gd["confirm_trigger"] = self.gd["ability_trigger"]

		if self.gd["done"] and self.gd["do"][0] > 0:
			if "do" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("do")
			self.gd["effect"] = list(self.gd["do"][1])
			self.gd["done"] = False
			if self.gd["do"][0] > 0:
				self.gd["do"][0] -= 1
				self.gd["ability_effect"].append("do")
				self.ability_event()
			else:
				self.ability_effect()
		elif "pay" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "pay"
			ind = self.gd["ability_trigger"].split("_")[1]
			if self.net["game"] and (ind[-1] == "2" or ("opp" in self.gd["effect"] and ind[-1] == "1")):
				self.gd["ability_effect"].remove("pay")
				if not self.net["act"][5]:
					self.gd["ability_effect"].remove("do")
					self.gd["done"] = False
					self.ability_effect()
				else:
					self.gd["paypop"] = True
					self.gd["done"] = True
					if not self.gd["payed"]:
						self.pay_condition()
					else:
						self.ability_event(m=self.net["game"])
			elif self.gd["com"] and (ind[-1] == "2" or ("opp" in self.gd["effect"] and ind[-1] == "1")):
				pick = self.ai.ability(self.pd, self.cd, self.gd)
				if pick != "pass":
					# inx = pick.index("AI_pay")
					self.pay_condition()
					self.gd["ability_effect"].remove("pay")
					self.gd["done"] = True
					self.gd["p_owner"] = ind[-1]
				else:
					self.gd["ability_effect"].remove("pay")
					self.gd["ability_effect"].remove("do")
					self.ability_effect()
			elif ind[-1] == "1" and "opp" not in self.gd["effect"] and not self.gd["payed"] and self.gd["paypop"]:
				self.gd["ability_effect"].remove("pay")
				self.gd["ability_effect"].remove("do")
				self.gd["confirm_result"] = ""
				self.ability_effect()
			elif ind[-1] == "1" and "opp" not in self.gd["effect"] and self.gd["payed"] and self.gd["paypop"]:
				self.gd["ability_effect"].remove("pay")
				self.gd["ability_effect"].remove("do")
				self.gd["done"] = True
				self.gd["confirm_result"] = ""
				self.ability_effect()
			elif ind[-1] == "1" and "opp" not in self.gd["effect"] and (
					not self.gd["payed"] or self.gd["uptomay"]) and not self.gd["paypop"]:
				if self.auto_check_pay(self.gd["effect"]):
					if "may" in self.gd["effect"]:
						self.gd["effect"].remove("may")
						if "Discard" in self.gd["pay"]:
							if "Rest" in self.gd["pay"]:
								self.gd["dismay"] = False
							else:
								self.gd["dismay"] = True
							self.gd["uptomay"] = False
					self.gd["confirm_trigger"] = self.gd["ability_trigger"]
					self.gd["confirm_var"] = {"ind": ind, "c": "ability"}
					Clock.schedule_once(self.confirm_popup, popup_dt)
					return False
				else:
					self.gd["ability_effect"].remove("pay")
					self.gd["ability_effect"].remove("do")
					self.ability_effect()

		elif "stand" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "stand"
			ind = self.gd["ability_trigger"].split("_")[1]
			# if ind[-1] == "1" and not self.gd["payed"]:
			# 	self.gd["confirm_var"] = {"ind": ind, "c": "ability"}
			# 	Clock.schedule_once(self.confirm_popup, popup_dt)
			# 	return False
			# else:
			self.stand()
		elif "rest" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "rest"
			ind = self.gd["ability_trigger"].split("_")[1]
			# if (not self.gd["payed"] or self.gd["uptomay"]) and ind[-1] == "1" and self.gd["confirm_result"] != "1":
			# 	self.gd["confirm_trigger"] = self.gd["ability_trigger"]
			# 	self.gd["confirm_var"] = {"ind": ind, "c": "ability"}
			# 	Clock.schedule_once(self.confirm_popup, popup_dt)
			# 	return False
			if self.gd["target"]:
				self.rest()
			elif self.gd["effect"][0] > 0 and not self.gd["choose"]:
				if ind[-1] == "1":
					if "Stand" in self.gd["effect"]:
						self.select_card(s="Stand")
					else:
						self.select_card()
					Clock.schedule_once(partial(self.popup_text, "Main"))
				elif ind[-1] == "2" and self.gd["com"]:
					pick = self.ai.ability(self.pd, self.cd, self.gd)
					self.gd["choose"] = True
					if pick != "pass":
						self.gd["target"].append(pick[pick.index("AI_target") + 1])
					else:
						self.gd["notarget"] = True
					self.ability_effect()
			else:
				self.gd["confirm_result"] = ""
				self.rest()
		elif "backatk" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("backatk")

			if not self.gd["bodyguard"]:
				temp = self.gd["target"].pop(0)
				self.gd["attacking"][3] = int(self.cd[temp].pos_new[-1])
				self.gd["attacking"][4] = str(self.cd[temp].pos_new[0])

			for fields in self.gd["select_btns"]:
				self.cd[self.pd[fields[-1]][fields[:-2]][int(fields[-2])]].selectable(False)

			self.gd["chosen"] = []
			self.gd["choose"] = False
			self.clear_ability()
			self.attack_declaration_beginning()
		elif "shuffle" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "shuffle"
			self.gd["p_c"] = ""
			self.shuffle_ability()
		elif "confirm" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "confirm"
			ind = self.gd["ability_trigger"].split("_")[1]

			if self.gd["rev"] and self.gd["active"] == "1":
				player = "2"
			elif self.gd["rev"] and self.gd["active"] == "2":
				player = "1"
			else:
				player = self.gd["active"]

			if self.net["game"] and not self.gd["confirm2"][0]:
				if ind[-1] == "1":
					if not self.gd["confirm1"][0]:
						self.net["send"] = False
					elif not self.net["send"]:
						# self.net["act"][4] = self.gd["confirm1"][1][0]
						self.net["var"] = list(self.net["act"])
						self.net["var1"] = "confirm"
						if not self.poptext:
							Clock.schedule_once(partial(self.popup_text, "waitingser"))
						self.mconnect("act")
						return
					else:
						if self.gd["show_wait_popup"]:
							Clock.schedule_once(partial(self.popup_text, "waiting"),popup_dt)
						self.mconnect("counter")
						return
			elif self.net["game"] and self.gd["confirm2"][0]:
				if ind[-1] == "2":
					if not self.gd["confirm1"][0]:
						self.net["send"] = False
					elif not self.net["send"]:
						self.net["var"] = [self.gd["confirm1"][1]]
						self.net["var1"] = "confirm"
						if not self.poptext:
							Clock.schedule_once(partial(self.popup_text, "waitingser"))
						self.mconnect("oppchoose")
						return
			elif self.gd["com"] and not self.gd["confirm2"][0] and (
					"opp" in self.gd["effect"] or "both" in self.gd["effect"]):
				pick = self.ai.ability(self.pd, self.cd, self.gd)
				if pick != "pass" or not pick:
					if "y" in pick:
						self.gd["confirm2"][1] = True
					elif "n" in pick:
						self.gd["confirm2"][1] = False
				else:
					self.gd["confirm2"][1] = False
				self.gd["confirm2"][0] = True


			# if self.net["game"] and self.gd["confirm1"][0] and ind[-1] == "1" and not self.net["send"] and not \
			# 		self.gd["confirm2"][0]:
			# 	self.net["var"] = ["a", str(self.gd["auto_effect"][0]),
			# 	                   self.gd["stack"][player].index(self.gd["auto_effect"]), [],
			# 	                   [], 1]
			#
			# elif self.net["game"] and self.gd["confirm1"][0] and ind[-1] == "1" and self.net["send"] and not \
			# 		self.gd["confirm2"][0]:
			# 	if self.gd["show_wait_popup"]:
			# 		Clock.schedule_once(partial(self.popup_text, "waiting"))
			# 	self.mconnect("counter")
			# elif self.net["game"] and self.gd["confirm1"][0] and ind[-1] == "2" and not self.net["send"] and not \
			# 		self.gd["confirm2"][0]:
			# 	if "True" in self.gd["target"]:
			# 		self.gd["confirm2"] = [True, True]
			# 	else:
			# 		self.gd["confirm2"] = [True, False]
			# 	self.net["var"] = self.gd["confirm1"][1]
			# 	self.net["var1"] = "confirm"
			# 	if not self.poptext:
			# 		Clock.schedule_once(partial(self.popup_text, "waitingser"))
			# 	self.mconnect("counter")

			if not self.gd["confirm1"][0] and "both" in self.gd["effect"]:
				self.gd["confirm_var"] = {"ind": ind, "c": "confirm"}
				Clock.schedule_once(self.confirm_popup, popup_dt)
				return False
			elif not self.gd["confirm1"][0] and self.gd["active"] == "2" and ind[-1] == "2" and "opp" in self.gd[
				"effect"]:
				self.gd["confirm_var"] = {"ind": ind, "c": "confirm"}
				Clock.schedule_once(self.confirm_popup, popup_dt)
				return False
			elif not self.gd["confirm1"][0] and self.gd["active"] == "1" and ind[-1] == "1" and "opp" in self.gd[
				"effect"]:
				self.gd["confirm_var"] = {"ind": ind, "c": "confirm"}
				Clock.schedule_once(self.confirm_popup, popup_dt)
				return False
			elif self.gd["confirm1"][0] and self.gd["confirm2"][0]:
				if self.gd["confirm1"][1] and self.gd["confirm2"][1]:
					self.gd["done"] = True
				self.gd["confirm1"] = [False, 0]
				self.gd["confirm2"] = [False, 0]
				if "confirm" in self.gd["ability_effect"]:
					self.gd["ability_effect"].remove("confirm")
				if "do" in self.gd["ability_effect"]:
					self.gd["ability_effect"].remove("do")
				self.ability_effect()
		elif "declare" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "declare"
			if "text" in self.gd["effect"]:
				if "all" in self.gd["effect"]:
					for player in list(self.pd.keys()):
						self.sd["joke"][player].change_texture(self.gd["effect"][self.gd["effect"].index("text")+1])
						self.sd["joke"][player].center_x = self.mat[player]["mat"].size[0] / 2.
						self.sd["joke"][player].x = self.mat[player]["mat"].x
						self.sd["joke"][player].y = -Window.height

						self.joke(player,"d")
			elif "five" in self.gd["effect"]:
				for player in list(self.pd.keys()):
					if player == "1":
						self.sd["joke"][player].img_src = f"atlas://{img_in}/other/random"
						self.sd["joke"][player].rect.source = f"atlas://{img_in}/other/random"
						# self.sd["joke"][player].source = f"atlas://{img_in}/other/handb"
					elif player == "2":
						self.sd["joke"][player].img_src = f"atlas://{img_in}/other/handf"
						self.sd["joke"][player].rect.source = f"atlas://{img_in}/other/handf"

					self.sd["joke"][player].center_x = self.mat[player]["mat"].size[0] / 2.
					self.sd["joke"][player].x = self.mat[player]["mat"].x
					self.sd["joke"][player].y = -Window.height

					self.joke(player, "d")
			if "declare" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("declare")

			if "do" in self.gd["effect"] and self.gd["do"][0] > 0:
				self.gd["done"] = True
			if "do" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("do")

			Clock.schedule_once(self.ability_effect, joke_dt * 10)
		elif "distock" in self.gd["ability_effect"]:
			ind = self.gd["ability_trigger"].split("_")[1]
			if "opp" in self.gd["effect"]:
				if ind[-1] == "1":
					p = "2"
				elif ind[-1] == "2":
					p = "1"
			else:
				p = ind[-1]
			if self.gd["effect"][1] == -1:
				self.gd["effect"][1] = len(self.pd[p]["Stock"])
				if "count" in self.gd["effect"] and "stock" in self.gd["effect"][self.gd["effect"].index("do") + 1]:
					self.gd["effect"][self.gd["effect"].index("do") + 1][1] = len(self.pd[p]["Stock"])
					self.gd["do"][1] = self.gd["effect"][self.gd["effect"].index("do") + 1]
			wait = []
			for r in range(self.gd["effect"][1]):
				if len(self.pd[p]["Stock"]) > 0:
					if "bottom" in self.gd["effect"]:
						temp = self.pd[p]["Stock"].pop(0)
					else:
						temp = self.pd[p]["Stock"].pop(-1)
					self.mat[p]["mat"].remove_widget(self.cd[temp])
					self.mat[p]["mat"].add_widget(self.cd[temp])
					self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Waiting"], t="Waiting")
					self.pd[p]["Waiting"].append(temp)
					wait.append(temp)
					self.update_field_label()
					self.stock_size(p)
			self.check_cont_ability()
			self.gd["ability_effect"].remove("distock")
			if "if" in self.gd["effect"]:
				if wait:
					self.gd["done"] = True
			elif "do" in self.gd["effect"] and self.gd["do"][0] > 0:
				self.gd["done"] = True
			if "do" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("do")
			self.ability_effect()
		elif "heal" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "heal"
			if self.gd["target"] or self.gd["move"]:
				self.heal()
			elif self.gd["uptomay"]:
				self.effect_to_stage("Clock")
			else:
				self.heal()
		elif "brainstorm" in self.gd["ability_effect"]:
			self.gd["brainstorm_c"] = [0, []]
			self.gd["brainstorm"] = int(self.gd["effect"][self.gd["effect"].index("brainstorm") + 1])
			self.brainstorm()
		# elif "levelrev" in self.gd["ability_effect"]:
		# 	lev = self.gd["effect"].index("levelrev")+1
		# 	oind  = self.gd["effect"].index("levelrev")+1
		# 	if ">=" in lev:
		# 		if self.cd[oind].level >=int(lev[-1]):
		# 			self.gd["done"] = True
		# 	elif "<=" in lev:
		# 		if self.cd[oind].level <= int(lev[-1]):
		# 			self.gd["done"] = True
		#
		# 	if "do" in self.gd["ability_effect"] and not self.gd["done"]:
		# 		self.gd["ability_effect"].remove("do")
		# 	self.gd["ability_effect"].remove("levelrev")
		# 	self.ability_effect()
		elif "look" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "look"
			ind = self.gd["ability_trigger"].split("_")[1]
			if "opp" in self.gd["effect"] and ind[-1] == "1":
				opp = "2"
			elif "opp" in self.gd["effect"] and ind[-1] == "2":
				opp = "1"
			else:
				opp = ind[-1]
			if ind[-1] == self.gd["active"]:
				self.popup_multi_info(field=self.gd["effect"][0], owner=opp)
			elif ind[-1] != self.gd["active"]:
				Clock.schedule_once(partial(self.popup_text, "LookOpp"))
		elif "looktop" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "looktop"
			ind = self.gd["ability_trigger"].split("_")[1]

			if self.gd["effect"][0] == -16:
				self.gd["effect"][0] = len(self.gd["extra"])
				self.gd["p_l"] = list(self.gd["extra"])
				if "extra" not in self.gd["effect"]:
					self.gd["extra"] = []
				self.gd["clear"] = False

			if self.net["game"] and "looktopopp" in self.gd["effect"]:
				if ind[-1] == "1":
					# if not self.net["send"]:
					# 	self.net["act"][5] = 1
					# 	self.net["var"] = self.net["act"]
					# 	self.net["var1"] = "looktopopp"
					# 	if not self.poptext:
					# 		Clock.schedule_once(partial(self.popup_text, "waitingser"))
					# 	self.mconnect("act")
					# else:
					if self.gd["show_wait_popup"]:
						Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
					self.mconnect("oppchoose")
				elif ind[-1] == "2":
					if not self.net["send"]:
					# self.net["send"] = False
						self.gd["oppchoose"] = True
						self.look_top("s")
					else:
						if self.gd["show_wait_popup"]:
							Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
						self.mconnect("plchoose")
			# elif self.net["game"] and "looktop" in self.gd["effect"] and "stacked" in self.gd["effect"] and ind[-1] != f"{self.net['player']+1}":
			# 	if self.gd["show_wait_popup"]:
			# 		Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
			# 	self.mconnect("plchoose")
			elif self.gd["com"] and (ind[-1] == "2" or ("looktopopp" in self.gd["effect"] and ind[-1] == "1")):
				if "stack" in self.gd["effect"]:
					self.gd["p_c"] = "Look_stack"
				if self.gd["effect"][0] == -16:
					self.gd["effect"][0] = len(self.gd["extra"])
					self.gd["p_l"] = list(self.gd["extra"])
					if "extra" not in self.gd["effect"]:
						self.gd["extra"] = []
				pick = self.ai.ability(self.pd, self.cd, self.gd)
				if "AI_looktop" in pick:
					inx = pick.index("AI_looktop")
					self.gd["chosen"] = list(pick[inx+1])
				else:
					self.gd["chosen"] = []
				self.look_top("l")
			# need ai choice/action
			elif self.gd["target"]:
				self.look_top(None)
			elif "check" in self.gd["effect"]:
				self.gd["target"].append("t")
				self.look_top(None)
			else:
				if self.net["game"] and self.gd["oppchoose"] and ind[-1] == "2":
					if self.gd["show_wait_popup"]:
						Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
					self.mconnect("plchoose")
				else:
					self.look_top("s")
		elif "marker" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "marker"
			self.marker()
		elif "drawupto" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "drawupto"
			ind = self.gd["ability_trigger"].split("_")[1]
			if "if" in self.gd["effect"]:
				self.gd["drawed"] = []
			if ind[-1] == "1":
				if "Reveal" in self.gd["effect"]:
					self.sd["btn"]["end"].text = "End Reveal"
					self.sd["btn"]["draw_upto"].text = "Reveal card"
				elif "Stock" in self.gd["effect"]:
					self.sd["btn"]["end"].text = "End Stock"
					self.sd["btn"]["draw_upto"].text = "Add Stock"
				elif "heal" in self.gd["effect"]:
					self.sd["btn"]["end"].text = "End Heal"
					self.sd["btn"]["draw_upto"].text = "Heal"
				else:
					self.sd["btn"]["draw_upto"].text = "Draw card"
					self.sd["btn"]["end"].text = "End Effect"

				if "heal" in self.gd["effect"] and len(self.pd[ind[-1]]["Clock"]) <= 0:
					self.gd["draw_upto"] = 0
					self.gd["draw"] = 0
					self.draw()
				else:
					self.sd["btn"]["ablt_info"].y = 0
					self.sd["btn"]["ablt_info"].x = 0
					self.sd["btn"]["draw_upto"].y = 0
					self.sd["btn"]["end"].y = 0
					self.sd["btn"]["end"].disabled = False
					self.sd["btn"]["end_attack"].y = -Window.height * 2
					self.sd["btn"]["end_phase"].y = -Window.height * 2
			elif self.net["game"] and ind[-1] == "2":
				self.gd["draw"] = self.gd["target"].count("d")
				for d in range(self.gd["draw_upto"]):
					if "d" in self.gd["target"]:
						self.gd["target"].remove("d")
				self.gd["draw_upto"] = 0
				self.draw()
			elif self.gd["com"] and ind[-1] == "2":
				self.gd["draw"] = int(self.gd["draw_upto"])
				self.gd["draw_upto"] = 0
				self.draw()
		elif "draw" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "draw"
			ind = self.gd["ability_trigger"].split("_")[1]
			if "opp" in self.gd["effect"] and ind[-1] == self.gd["active"]:
				self.gd["rev"] = True
			elif "opp" in self.gd["effect"] and ind[-1] != self.gd["active"]:
				self.gd["rev"] = False
			elif "opp" not in self.gd["effect"] and ind[-1] == self.gd["active"]:
				self.gd["rev"] = False
			elif "opp" not in self.gd["effect"] and ind[-1] != self.gd["active"]:
				self.gd["rev"] = True

			if "xrlevel+1" in self.gd["effect"] and self.gd["effect"][1] == "x":
				self.gd["effect"][1] = self.cd[self.gd["resonance"][1][0]].level + 1
			if "More" in self.gd["effect"]:
				if "lower" in self.gd["effect"] and len(
						self.cont_times(self.gd["effect"], self.cont_cards(self.gd["effect"], ind), self.cd)) > \
						self.gd["effect"][self.gd["effect"].index("More") + 1]:
					self.gd["effect"][1] = 0
				elif "lower" not in self.gd["effect"] and len(
						self.cont_times(self.gd["effect"], self.cont_cards(self.gd["effect"], ind), self.cd)) < \
						self.gd["effect"][self.gd["effect"].index("More") + 1]:
					self.gd["effect"][1] = 0
			self.gd["draw"] = self.gd["effect"][1]
			self.draw()
		elif "discard" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "discard"
			ind = self.gd["ability_trigger"].split("_")[1]
			if "cdiscard" in self.gd["effect"] and self.gd["effect"][1] == -17:
				self.gd["discard"] = 1
				if "opp" in self.gd["effect"]:
					if ind[-1] == "1":
						p = "2"
					elif ind[-1] == "2":
						p = "1"
				else:
					p = ind[-1]
				if len(self.pd[p]["Clock"]) > 0:
					self.gd["target"].append(self.pd[p]["Clock"][-1])
				else:
					self.gd["target"].append("")

			if "random" in self.gd["effect"]:
				dd = sample(self.pd[ind[-1]]["Hand"], self.gd["discard"])
				for d in dd:
					self.gd["target"].append(d)
					self.gd["random_reveal"].append(d)
				self.gd["effect"].remove("random")
			if "Reveal" in self.gd["effect"]:
				self.gd["resonance"][0] = True

			if self.gd["com"] and ind[-1] == "2":
				pick = self.ai.ability(self.pd, self.cd, self.gd)
				self.gd["target"] = list(pick[pick.index("AI_discard") + 1])
			self.discard()
		elif "encore" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "encore"
			# if self.gd["encore_ind"] == "":
			self.gd["encore_ind"] = str(self.gd["auto_effect"][0])
			if self.gd["target"]:
				self.encore_pay()
			elif self.gd["com"] and self.gd["encore_ind"][-1] == "2":
				if "Clock" in self.gd["effect"] and len(self.pd[self.gd["encore_ind"][-1]]["Level"]) <= 2:
					self.gd["target"].append("Clock")
				elif "Stock3" in self.gd["effect"] and len(self.pd[self.gd["encore_ind"][-1]]["Stock"]) >= 3:
					self.gd["target"].append("Stock3")
				self.encore_pay()
			else:
				self.gd["confirm_trigger"] = str(self.gd["ability_trigger"])
				self.gd["confirm_trigger"] = "Encore_" + self.gd["ability_trigger"]
				self.gd["confirm_var"] = {"ind": self.gd["encore_ind"], "c": "encore"}
				Clock.schedule_once(self.confirm_popup, popup_dt)
				return False
		# Clock.schedule_once(self.encore_popup)
		elif "give" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "give"
			ind = self.gd["ability_trigger"].split("_")[1]
			# if not self.gd["payed"] and ind[-1] == "1":
			# 	self.gd["confirm_var"] = {"ind": ind, "c": "ability"}
			# 	Clock.schedule_once(self.confirm_popup, popup_dt)
			# 	return False
			if self.gd["target"]:
				self.give()
			elif ind[-1] == "1" and self.gd["effect"][0] > 0 and not self.gd["target"]:
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"))
			# elif self.net["game"] and ind[-1] == "2":
			# 	if (not self.gd["payed"] or self.gd["uptomay"]) and not self.net["act"][5]:
			# 		self.gd["ability_effect"].remove("give")
			# 		self.ability_effect()
			# 	else:
			# 		self.give()
			else:
				self.give()
		elif "rescue" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "rescue"
			ind = self.gd["ability_trigger"].split("_")[1]
			# if not self.gd["payed"] and ind[-1] == "1":
			# 	self.gd["confirm_trigger"] = str(self.gd["ability_trigger"])
			# 	self.gd["confirm_var"] = {"ind": ind, "c": "ability"}
			# 	Clock.schedule_once(self.confirm_popup, popup_dt)
			# 	return False
			if self.net["game"] and ind[-1] == "2":
				if not self.net["act"][5]:
					self.gd["ability_effect"].remove("rescue")
					self.ability_effect()
				else:
					self.rescue()
			else:
				self.rescue()
		elif "stock" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "stock"
			ind = self.gd["ability_trigger"].split("_")[1]
			if "opp" in self.gd["effect"] and ind[-1] == self.gd["active"]:
				self.gd["rev"] = True
			elif "opp" in self.gd["effect"] and ind[-1] != self.gd["active"]:
				self.gd["rev"] = False
			elif "opp" not in self.gd["effect"] and ind[-1] == self.gd["active"]:
				self.gd["rev"] = False
			elif "opp" not in self.gd["effect"] and ind[-1] != self.gd["active"]:
				self.gd["rev"] = True

			self.stock()
		elif "janken" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "janken"
			self.janken()
		elif "reveal" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "reveal"
			self.reveal()
		elif "hander" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "hander"
			ind = self.gd["ability_trigger"].split("_")[1]
			if ind[-1] == "1" and self.gd["effect"][0] > 0 and not self.gd["choose"]:
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"))
			else:
				self.wind()
		elif "wind" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "wind"
			ind = self.gd["ability_trigger"].split("_")[1]
			if ind[-1] == "1" and self.gd["effect"][0] > 0 and not self.gd["target"]:
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"))
			else:
				self.gd["confirm_result"] = ""
				self.wind()
		elif "stocker" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "stocker"
			ind = self.gd["ability_trigger"].split("_")[1]
			if ind[-1] == "1" and self.gd["effect"][0] > 0 and not self.gd["target"]:
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"))
			# elif ind[-1] == "1" and self.gd["effect"][0] == 0 and (self.gd["uptomay"] or not self.gd["payed"]):
			# 	if not self.gd["confirm1"][0]:
			# 		self.gd["confirm_var"] = {"ind": ind, "c": "ability"}
			# 		Clock.schedule_once(self.confirm_popup, popup_dt)
			# 		return False
			# 	elif not self.gd["confirm1"][1]:
			# 		self.gd["notarget"] = True
			# 	if self.gd["confirm1"][0]:
			# 		self.stocker()
			else:
				self.stocker()
		elif "clocker" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "clocker"
			ind = self.gd["ability_trigger"].split("_")[1]
			if ind[-1] == "1" and self.gd["effect"][0] > 0 and not self.gd["choose"]:
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"))
			else:
				self.clocker()
		elif "decker" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "decker"
			ind = self.gd["ability_trigger"].split("_")[1]
			if ind[-1] == "1" and self.gd["effect"][0] > 0 and not self.gd["choose"]:
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"))
			else:
				self.decker()
		elif "waitinger" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "waitinger"
			ind = self.gd["ability_trigger"].split("_")[1]
			if ind[-1] == "1" and self.gd["effect"][0] > 0 and not self.gd["choose"]:
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"))
			else:
				self.waitinger()
		elif "memorier" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "memorier"
			ind = self.gd["ability_trigger"].split("_")[1]
			if ind[-1] == "1" and self.gd["effect"][0] > 0 and not self.gd["choose"]:# and "top-down" not in self.gd["effect"]:
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"))
			else:
				self.memorier()
		elif "reverser" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "reverser"
			ind = self.gd["ability_trigger"].split("_")[1]
			if self.gd["com"] and ind[-1] == "2":
				pick = self.ai.ability(self.pd, self.cd, self.gd)
				if pick != "pass":
					self.cd[ind].reverse()

				if "do" in self.gd["ability_effect"]:
					self.gd["ability_effect"].remove("do")
				self.gd["ability_effect"].remove("reverser")
				self.ability_effect()
			else:
				self.reverser()
		# elif "runner" in self.gd["ability_effect"]:
		# 	self.gd["ability_doing"] = "move"
		# 	ind = self.gd["ability_trigger"].split("_")[1]
		# 	if "runner" in self.gd["ability_effect"]:
		# 		self.gd["ability_effect"].remove("runner")
		# 	if ind[-1] == "1" and self.gd["active"] == "2":
		# 		self.gd["confirm_trigger"] = self.gd["ability_trigger"]
		# 		self.gd["confirm_var"] = {"ind": ind, "c": "ability"}
		# 		Clock.schedule_once(self.confirm_popup, popup_dt)
		# 	else:
		# 		self.ability_effect()
		elif "revive" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "revive"
			ind = self.gd["ability_trigger"].split("_")[1]
			if self.gd["effect"][0] == 0:
				if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
					if "Waiting" in self.cd[ind].pos_new:
						self.gd["target"].append(ind)
					else:
						self.gd["target"].append("")
				self.gd["effect"][0] = 1
				if "Stage" in self.gd["effect"]:
					self.gd["target"].append(self.cd[ind].pos_old)
			elif self.gd["effect"][0] == -7:
				if ind[-1] == "1":
					if "Waiting" in self.cd[self.gd["effect"][2][0]].pos_new:
						self.gd["target"].append(self.gd["effect"][2][0])
					else:
						self.gd["target"].append("")
				self.gd["effect"][0] = 1
				if "Stage" in self.gd["effect"][2][1]:
					self.gd["effect"].append("Stage")
					if ind[-1] == "1" or (self.gd["com"] and ind[-1] == "2"):
						self.gd["target"].append(self.cd[self.gd["effect"][2][0]].pos_old)
			self.gd["salvage"] = int(self.gd["effect"][0])
			self.salvage()
		elif "move" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "move"
			ind = self.gd["ability_trigger"].split("_")[1]
			if "this" in self.gd["effect"]:
				self.gd["choose"] = True
				self.gd["notarget"] = False
			if self.gd["effect"][0] == -16:
				self.gd["choose"] = True
				self.gd["notarget"] = False
				self.gd["status"] = self.add_to_status("Select1", self.gd["effect"])

			if self.gd["target"]:
				self.move()
			# if not self.gd["payed"] and ind[-1] == "1" and not self.gd["confirm1"][0]:
			# 	self.gd["confirm_trigger"] = self.gd["ability_trigger"]
			# 	self.gd["confirm_var"] = {"ind": ind, "c": "ability"}
			# 	Clock.schedule_once(self.confirm_popup, popup_dt)
			# 	return False
			# elif self.net["game"] and ind[-1] == "2":
			# 	if self.net["act"][5]:
			# 		self.gd["notarget"] = False
			# 	else:
			# 		self.gd["notarget"] = True
			# 	self.move()
			elif self.gd["effect"][0] > 0 and not self.gd["choose"]:
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"))
			elif self.gd["choose"] and not self.gd["notarget"] and not self.gd["move"]:
				# self.gd["chosen"] = []
				self.select_field()
				Clock.schedule_once(partial(self.popup_text, "Move"))
			else:
				self.move()
		elif "change" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "change"
			ind = self.gd["ability_trigger"].split("_")[1]
			if self.gd["com"] and ind[-1] == "2":
				pick = self.ai.ability(self.pd, self.cd, self.gd)
				if pick != "pass":
					inx = pick.index("AI_change")
					self.gd["chosen"].append(pick[inx + 1])
					self.gd["p_c"] = "Change"
					self.gd["p_owner"] = ind[-1]
					self.change()
				else:
					self.gd["ability_effect"].remove("change")
					self.do_check(True, r=True)
			else:
				self.gd["p_c"] = ""
				self.change()
		elif "damage" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "damage"
			if "both" in self.gd["effect"]:
				self.gd["both"] = True
			if self.gd["damage"] == "x":
				ind = self.gd["ability_trigger"].split("_")[1]
				tx = 0
				if "Waiting" in self.gd["effect"]:
					tx = len(self.cont_times(self.gd["effect"],
					                         self.pd[ind[-1]]["Waiting"], self.cd))
				elif "xlvlhigh" in self.gd["effect"]:
					tx = sorted([self.cd[s].level_t for s in self.pd[ind[-1]]["Center"] + self.pd[ind[-1]]["Back"] if
					             s != ""], reverse=True)[0]
				self.gd["damage"] = tx
			elif self.gd["damage"] == -16:
				self.gd["damage"] = len(self.gd["extra"])
				self.gd["extra"] = []
			elif self.gd["damage"] == -36:
				if len(self.gd["extra"]) > 0:
					self.gd["damage"] = self.cd[self.gd["extra"][0]].level
				else:
					self.gd["damage"] = 0
				self.gd["extra"] = []
			elif self.gd["damage"] == -37:
				if len(self.gd["extra"]) > 0:
					self.gd["damage"] = self.cd[self.gd["extra"][0]].level + 1
				else:
					self.gd["damage"] = 0 + 1
				self.gd["extra"] = []

			if self.gd["damage"] > 0 or self.gd["damage_refresh"] > 0:
				ind = self.gd["ability_trigger"].split("_")[1]
				if "opp" in self.gd["effect"] and ind[-1] == self.gd["active"]:
					self.gd["rev"] = True
				elif "opp" in self.gd["effect"] and ind[-1] != self.gd["active"]:
					self.gd["rev"] = False
				elif "opp" not in self.gd["effect"] and ind[-1] == self.gd["active"]:
					self.gd["rev"] = False
				elif "opp" not in self.gd["effect"] and ind[-1] != self.gd["active"]:
					self.gd["rev"] = True

				self.gd["dmg"] = int(self.gd["damage"])
				self.damage()
			else:
				self.gd["dmg"] = 0
				self.gd["ability_effect"].remove("damage")
				self.do_check(True)
		elif "mill" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "mill"
			self.mill()
		elif "salvage" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "salvage"
			ind = self.gd["ability_trigger"].split("_")[1]

			if "xrlevel+1" in self.gd["effect"] and self.gd["effect"][2][-1] == "x":
				self.gd["effect"][2] = f"{self.gd['effect'][2][:-1]}{self.cd[self.gd['resonance'][1][0]].level + 1}"
				self.gd["search_type"] = self.gd["effect"][2]
			elif "ID_x" in self.gd["effect"] and self.gd["effect"][0] == -16:
				self.gd["effect"][0] = len(self.gd["extra"])
				self.gd["salvage"] = int(self.gd["effect"][0])
				self.gd["effect"][2] = "_".join(["ID="] + [n for n in self.gd["extra"] if n != ""])
				self.gd["effect"].append("passed")
				self.gd["search_type"] = str(self.gd["effect"][2])
				self.gd["extra"] = []

				if self.net["game"] and "plchoose" in self.gd["effect"]:
					if ind[-1] == "1":
						self.gd["p_c"] = ""
						self.net["send"] = False
						self.net["var"] = list(self.net["act"])
						self.net["var1"] = "plchoose_salvage"
						if not self.poptext:
							Clock.schedule_once(partial(self.popup_text, "waitingser"))
						self.mconnect("act")
						return False
					elif ind[-1] == "2":
						if self.gd["effect"][0]>0:
							if self.gd["show_wait_popup"]:
								Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
							self.mconnect("plchoose")
							return False

			if self.gd["effect"][0] == -16:
				self.gd["effect"][0] = len(self.gd["extra"])
				self.gd["salvage"] = int(self.gd["effect"][0])
				for r in range(len(self.gd["extra"])):
					ex = self.gd["extra"].pop(0)
					if ind[-1] == "1":
						self.gd["target"].append(ex)
				if "Stage" in self.gd["effect"] and self.gd["effect"][0] == 1:
					if len([c for c in self.gd["target"] if c != ""]) > 0:
						self.effect_to_stage("Stage")
						return False
					else:
						self.gd["move"] = "none"

			if self.gd["com"] and ind[-1] == "2":
				self.gd["p_c"] = "Salvage"
				self.gd["p_owner"] = ind[-1]

				self.gd["p_f"] = True
				self.popup_pl("Search")
				pick = self.ai.ability(self.pd, self.cd, self.gd)
				if "AI_salvage" in pick:
					inx = pick.index("AI_salvage")
					self.gd["chosen"] = pick[inx + 1]
				else:
					self.gd["chosen"] = []
				self.salvage()
			else:
				self.gd["p_c"] = ""
				self.salvage()
		elif "cstock" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "cstock"
			ind = self.gd["ability_trigger"].split("_")[1]
			if self.gd["target"]:
				self.cstock()
			elif self.gd["com"] and ind[-1] == "2":
				pick = self.ai.ability(self.pd, self.cd, self.gd)
				if pick != "pass":
					inx = pick.index("AI_cstock")
					self.gd["chosen"].append(pick[inx + 1])
					self.gd["p_c"] = "Stock"
					self.gd["p_owner"] = self.gd["active"]
					self.salvage()
				else:
					self.gd["ability_effect"].remove("salvage")
					self.ability_effect()
			else:
				self.gd["p_c"] = ""
				self.cstock()
		elif "search" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "search"
			ind = self.gd["ability_trigger"].split("_")[1]
			if self.gd["effect"][0] == -9:
				self.gd["effect"][0] = 1
				if "Stage" in self.gd["effect"]:
					self.gd["chosen"].append(self.pd[ind[-1]]["Library"][-1])
				else:
					self.gd["target"].append(self.pd[ind[-1]]["Library"][-1])
				if ind[-1] == "1":
					self.gd["p_c"] = "Search_Stage"

			if self.net["game"] and "searchopp" in self.gd["effect"]:
				if ind[-1] == "1":
					if not self.net["send"]:
						self.net["act"][5] = 1
						self.net["var"] = self.net["act"]
						self.net["var1"] = "searchopp"
						if not self.poptext:
							Clock.schedule_once(partial(self.popup_text, "waitingser"))
						self.mconnect("act")
					else:
						if self.gd["show_wait_popup"]:
							Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
						self.mconnect("oppchoose")
				elif ind[-1] == "2":
					self.net["send"] = False
					self.gd["oppchoose"] = True
					self.gd["p_c"] = ""
					self.search()
			elif self.gd["com"] and (ind[-1] == "2" or ("searchopp" in self.gd["effect"] and ind[-1] == "1")):
				self.gd["p_c"] = "Search"
				if ind[-1] == "2":
					self.gd["p_owner"] = "2"
				elif ("searchopp" in self.gd["effect"] and ind[-1] == "1"):
					self.gd["p_owner"] = "1"
				if "Reveal" in self.gd["effect"]:
					self.gd["p_c"] += "_Reveal"
				self.gd["p_f"] = True
				self.popup_pl("Search")
				pick = self.ai.ability(self.pd, self.cd, self.gd)
				if "AI_search" in pick:
					inx = pick.index("AI_search")
					self.gd["chosen"] = list(pick[inx + 1])
				else:
					self.gd["chosen"] = []
				self.search()
			else:
				self.search()
		elif "level" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "level"
			ind = self.gd["ability_trigger"].split("_")[1]

			if self.gd["effect"][0] > 0 and not self.gd["target"] and ind[-1] == "1":
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"))
			else:
				self.level()
		elif "soul" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "soul"
			ind = self.gd["ability_trigger"].split("_")[1]
			if self.gd["effect"][0] > 0 and not self.gd["target"] and ind[-1] == "1":
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"))
			else:
				self.soul()
		elif "trait" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "trait"
			ind = self.gd["ability_trigger"].split("_")[1]
			if self.gd["effect"][0] > 0 and not self.gd["target"] and ind[-1] == "1":
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"))
			else:
				self.trait()
		elif "power" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "power"
			ind = self.gd["ability_trigger"].split("_")[1]
			if "xrlevel+1" in self.gd["effect"] and self.gd["effect"][0] == "x":
				self.gd["effect"][0] = self.cd[self.gd["resonance"][1][0]].level + 1
				if self.gd["effect"][0] > 0 and not self.gd["choose"]:
					self.gd["status"] = f"Select{self.gd['effect'][0]}"
					self.gd["status"] = self.add_to_status(self.gd["status"], self.gd["effect"])
			elif "xrlevel" in self.gd["effect"] and self.gd["effect"][1] == "x":
				self.gd["effect"][1] = self.gd["effect"][self.gd["effect"].index("xrlevel") + 1] * self.cd[
					self.gd["resonance"][1][0]].level

			if self.gd["effect"][0] > 0 and not self.gd["target"] and ind[-1] == "1":
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"), popup_dt)
			elif self.gd["effect"][0] > 0 and not self.gd["target"] and ind[-1] == "2":
				cards = [s for s in self.pd[ind[-1]]["Center"] + self.pd[ind[-1]]["Back"] if s != ""]
				if "other" in self.gd["effect"] and ind in cards:
					cards.remove(ind)
				for cc in range(len(cards)):
					self.gd["target"].append(cards[cc])
				self.power()
			else:
				self.power()

		# elif "Trigger" in self.gd["ability_trigger"] and len(self.gd["ability_effect"]) <= 0:
		# 	Clock.schedule_once(self.trigger_effect)
		elif len(self.gd["stack"][self.gd["active"]]) > 0 or len(self.gd["stack"][self.gd["opp"]]) > 0:
			Clock.schedule_once(self.stack_ability)
		elif len(self.gd["ability_effect"]) <= 0 and (
				"Climax" in self.gd["ability_trigger"] or "Climax" in self.gd["phase"]):
			Clock.schedule_once(self.climax_phase_play)
		elif len(self.gd["ability_effect"]) <= 0 and "Counter" in self.gd["ability_trigger"]:
			Clock.schedule_once(self.counter_step_done)
		elif len(self.gd["ability_effect"]) <= 0 and "Battle" in self.gd["ability_trigger"]:
			pass
		# elif len(self.gd["ability_effect"]) <= 0 and self.pd[self.gd["active"]]["done"]["Battle"]:
		# 	Clock.schedule_once(self.attack_phase_done)
		elif len(self.gd["ability_effect"]) <= 0 and (
				"Character" in self.gd["ability_trigger"] or "Event" in self.gd["ability_trigger"] or "ACT" in self.gd[
			"ability_trigger"]):
			Clock.schedule_once(self.play_card_done)
		elif "debug" in self.gd["ability_trigger"] and "Main" in self.gd["phase"]:
			self.update_movable(self.gd["active"])
		# elif len(self.gd["ability_effect"]) <= 0 and "Encore" in self.gd["phase"]:
		# 	self.gd["encore_ind"] = ""
		# 	Clock.schedule_once(self.encore_start)
		# elif len(self.gd["ability_effect"]) <= 0 and "Attack" in self.gd["phase"]:
		# 	self.gd["encore_ind"] = ""
		# 	Clock.schedule_once(self.attack_phase_main)
		else:
			# print("ability else")
			# print(self.gd["ability_effect"])
			# print(self.gd["ability_trigger"])
			Clock.schedule_once(self.stack_ability)

	def heal(self, dt=0):
		ind = self.gd["ability_trigger"].split("_")[1]
		if ind[-1] == "1":
			if len(self.pd[ind[-1]]["Clock"]) > 0:
				if "top" in self.gd["effect"]:
					cind = self.pd[ind[-1]]["Clock"][-1]
					if self.gd["uptomay"] and (not self.gd["move"] or self.gd["move"] == "none"):
						self.gd["target"].append("")
					else:
						self.gd["target"].append(cind)
			else:
				self.gd["target"].append("")

		for inx in range(self.gd["effect"][1]):
			temp = self.gd["target"].pop(0)
			if self.net["game"] and ind[-1] == "1":
				self.net["act"][4].append(temp)
			if temp in self.emptycards:
				continue
			self.mat[ind[-1]]["mat"].remove_widget(self.cd[temp])
			self.mat[ind[-1]]["mat"].add_widget(self.cd[temp])
			self.pd[ind[-1]]["Clock"].remove(temp)
			self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Waiting"], t="Waiting")
			self.pd[ind[-1]]["Waiting"].append(temp)
			self.update_field_label()
		self.clock_size(ind[-1])
		self.check_cont_ability()
		if "heal" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("heal")

		self.do_check(True)

	def rest(self, dt=0):
		ind = self.gd["ability_trigger"].split("_")[1]
		if self.gd["effect"][0] == 0:
			if ind[-1] == "1":
				if self.cd[ind].status != "Rest" and (
						"Center" in self.cd[ind].pos_new or "Back" in self.cd[ind].pos_new):
					self.gd["target"].append(ind)
				else:
					self.gd["target"].append("")
			self.gd["effect"][0] = 1
		elif self.gd["effect"][0] == -1:
			if ind[-1] == "1":
				if "Opp" in self.gd["effect"]:
					if ind[-1] == "1":
						p = "2"
					elif ind[-1] == "2":
						p = "1"
				else:
					p = ind[-1]

				for r in self.pd[p]["Center"] + self.pd[p]["Back"]:
					if r != "":
						if "Other" in self.gd["effect"] and r == ind:
							continue
						if "Stand" in self.gd["effect"] and self.cd[r].status == "Stand":
							self.gd["target"].append(r)

			self.gd["effect"][0] = len(self.gd["target"])
		elif self.gd["effect"][0] == -16:
			self.gd["effect"][0] = len(self.gd["extra"])
			for r in range(len(self.gd["extra"])):
				ex = self.gd["extra"].pop(0)
				if ind[-1] == "1":
					if self.cd[ex].status != "Rest" and (
							"Center" in self.cd[ex].pos_new or "Back" in self.cd[ex].pos_new):
						self.gd["target"].append(ex)
					else:
						self.gd["target"].append("")

		if len(self.gd["target"]) < self.gd["effect"][0]:
			for r in range(self.gd["effect"][0] - len(self.gd["target"])):
				self.gd["target"].append("")

		rest = []
		for r in range(self.gd["effect"][0]):
			temp = self.gd["target"].pop(0)
			if self.net["game"] and ind[-1] == "1":
				self.net["act"][4].append(temp)
			if temp in self.emptycards:
				continue
			if "extra" in self.gd["effect"]:
				self.gd["extra"].append(temp)
			if self.cd[temp].status != "Rest":
				rest.append(temp)
				if "rested" in self.gd["effect"]:
					self.rest_card(temp, True)
				else:
					self.rest_card(temp)

		if "rest" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("rest")

		if "do" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("do")
			if "if" in self.gd["effect"]:
				if len(rest) >= self.gd["effect"][self.gd["effect"].index("if") + 1]:
					self.gd["done"] = True
			else:
				self.gd["done"] = True

		if self.gd["notarget"]:
			self.gd["notarget"] = False

		self.check_cont_ability()
		self.check_auto_ability(stacks=False)
		self.ability_effect()

	def stand(self, *args):
		ind = self.gd["ability_trigger"].split("_")[1]
		if ind[-1] == "1" and self.gd["effect"][0] == 0:
			self.gd["target"].append(ind)
			self.gd["effect"][0] = 1

		for r in range(self.gd["effect"][0]):
			temp = self.gd["target"].pop(0)
			if self.net["game"] and ind[-1] == "1":
				self.net["act"][4].append(temp)
			if temp == "":
				self.gd["notarget"] = True
				continue
			if self.cd[temp].status != "Stand":
				self.cd[temp].stand()
				self.gd["check_atk"] = True

		if "stand" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("stand")

		self.check_cont_ability()
		self.check_auto_ability(stacks=False)
		self.ability_effect()

	def brainstorm(self, dt=0):
		if self.gd["rev"]:
			player = self.gd["opp"]
		else:
			player = self.gd["active"]

		if self.gd["brainstorm"] > 0:
			if len(self.pd[player]["Library"]) > 0:
				temp = self.pd[player]["Library"].pop()
				card = self.cd[temp]

				self.mat[player]["mat"].remove_widget(card)
				self.mat[player]["mat"].add_widget(card)

				library = self.mat[player]["field"]["Library"]

				card.setPos(library[0] - self.sd["padding"] - self.sd["card"][0],
				            library[1] - self.sd["card"][1] / 3. * len(self.pd[player]["Res"]), t="Res")
				card.show_front()
				if "Climax" in self.gd["effect"] and card.card == "Climax":
					self.gd["brainstorm_c"][0] += 1
				self.pd[player]["Res"].append(temp)

				if not self.gd["Res1_move"]:
					self.field_btn[f"Res1{player}"].x += Window.width
					self.gd["Res1_move"] = True

				self.update_field_label()
				self.gd["brainstorm"] -= 1

			if len(self.pd[player]["Library"]) <= 0:
				self.gd["reshuffle_trigger"] = "brainstorm"
				Clock.schedule_once(self.refresh, move_dt_btw)
				return False
			Clock.schedule_once(self.brainstorm, move_dt_btw)
		else:
			cany = []
			if "any" in self.gd["effect"]:
				if "Name=" in self.gd["effect"] or "Trait" in self.gd["effect"]:
					cany = self.cont_times(self.gd["effect"], self.pd[player]["Res"], self.cd)
				elif "Climax" in self.gd["effect"]:
					cany = [c for c in range(self.gd["brainstorm_c"][0])]
			elif "each" in self.gd["effect"]:
				if "Name=" in self.gd["effect"] or "Trait" in self.gd["effect"]:
					self.gd["brainstorm_c"][0] = len(
						self.cont_times(self.gd["effect"], self.pd[player]["Res"], self.cd))

			for r in range(len(self.pd[player]["Res"])):
				temp = self.pd[player]["Res"].pop(0)
				if "Event" in self.gd["ability_trigger"] and temp in self.gd["ability_trigger"]:
					self.pd[player]["Res"].append(temp)
					continue
				self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Waiting"], t="Waiting")
				self.pd[player]["Waiting"].append(temp)
				self.update_field_label()

			if self.gd["Res1_move"]:
				self.field_btn[f"Res1{player}"].x -= Window.width
				self.gd["Res1_move"] = False

			self.check_cont_ability()
			self.check_auto_ability(brt=(self.gd["ability_trigger"].split("_")[1], self.gd["brainstorm_c"][0]),
			                        stacks=False)
			self.gd["rev"] = False

			if "brainstorm" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("brainstorm")

			if "do" in self.gd["ability_effect"] and "any" in self.gd["effect"] and len(cany) >= self.gd["effect"][
				self.gd["effect"].index("any") + 1]:
				if "#" in self.gd["do"][1]:
					if "_<=#" in self.gd["do"][1][2] and "#trait" in self.gd["do"][1]:
						self.gd["do"][1][2] = self.gd["do"][1][2].replace("_<=#", f"_<={len(cany)}")
						self.gd["effect"][self.gd["effect"].index("do") + 1] = list(self.gd["do"][1])
					elif "_=#" in self.gd["do"][1][2] and "#trait" in self.gd["do"][1]:
						self.gd["do"][1][2] = self.gd["do"][1][2].replace("_=#", f"_={len(cany)}")
						self.gd["effect"][self.gd["effect"].index("do") + 1] = list(self.gd["do"][1])
				self.gd["done"] = True
			elif "do" in self.gd["ability_effect"] and self.gd["brainstorm_c"][0] > 0:
				self.gd["done"] = True
				if "draw" in self.gd["do"][1]:
					self.gd["do"][1][1] = self.gd["do"][1][1] * self.gd["brainstorm_c"][0]
				elif "stocker" in self.gd["do"][1]:
					self.gd["do"][0] = 1
				elif any(eff in self.gd["do"][1] for eff in ("search", "salvage", "waitinger")):
					if isinstance(self.gd["do"][1][0], str) and "x" in self.gd["do"][1][0]:
						if self.gd["brainstorm_c"][0] <= 0:
							self.gd["done"] = False
						else:
							self.gd["do"][1][0] = int(self.gd["brainstorm_c"][0])
							if "do" in self.gd["do"][1] and self.gd["do"][1][self.gd["do"][1].index("do") + 1][
								1] == "x":
								self.gd["do"][1][self.gd["do"][1].index("do") + 1][1] = int(self.gd["brainstorm_c"][0])
					elif isinstance(self.gd["do"][1][-1], list) and "discard" in self.gd["do"][1][-1]:
						self.gd["brainstorm_c"][1] = list(self.gd["do"][1])
						self.gd["brainstorm_c"][0] -= 1
					else:
						self.gd["do"][1][0] = self.gd["do"][1][0] * self.gd["brainstorm_c"][0]
				else:
					self.gd["do"][0] = int(self.gd["brainstorm_c"][0])
			else:
				self.gd["ability_effect"].remove("do")

			Clock.schedule_once(self.ability_effect, ability_dt)

	def clear_ability(self):
		self.gd["ability_trigger"] = ""
		self.gd["choose"] = False
		self.gd["clear"] = True
		self.gd["move"] = ""
		self.gd["ability"] = ""
		self.gd["effect"] = []
		self.gd["chosen"] = []
		self.gd["target"] = []
		self.gd["status"] = ""
		self.gd["mstock"] = ""

		if self.gd["uptomay"]:
			self.gd["uptomay"] = False
			self.sd["btn"]["end"].y = -Window.height * 2
			self.sd["btn"]["end_eff"].y = -Window.height * 2

		self.gd["pay"] = []
		self.gd["payed"] = True
		self.gd["paypop"] = False
		self.gd["pay_status"] = ""
		self.gd["brainstorm_c"] = [0, []]
		self.gd["notarget"] = False
		self.gd["notargetfield"] = False
		self.gd["draw_upto"] = 0
		self.gd["dmg"] = 0
		# act
		self.gd["auto_effect"] = ""
		self.gd["rev"] = False
		self.gd["ability_doing"] = ""
		self.gd["confirm_result"] = ""

		if self.net["game"]:
			# self.net["send"] = False
			self.net["act"] = ["", "", 0, [], [], 0]

	def play_card_done(self, dt=0):
		if self.net["game"] and self.net["act"][5] and not self.net["send"] and self.gd["active"] == "1":
			if "ACT" in self.gd["ability_trigger"]:
				self.net["var1"] = "act"
			elif "AUTO" in self.gd["ability_trigger"]:
				self.net["var1"] = "auto"
			self.net["var"] = self.net["act"]
			self.mconnect("act")
		else:
			if "Event" in self.gd["ability_trigger"]:
				self.event_done()

			if self.gd["reshuffle"] and "do" not in self.gd["ability_effect"] and self.gd["trigger"] <= 0:
				self.gd["reshuffle"] = False
				self.gd["damage_refresh"] = 1
				self.gd["damageref"] = True
				self.gd["reshuffle_trigger"] = "act"
				Clock.schedule_once(self.damage, move_dt_btw)
				return False

			self.gd["play_card"] = ""
			self.clear_ability()
			self.check_cont_ability()
			# Clock.schedule_once(self.check_cont_ability, ability_dt)

			if "1" in self.gd["active"]:
				self.move_field_btn(self.gd["phase"])
				self.sd["btn"]["end"].x = Window.width - self.sd["btn"]["end"].size[0]
				self.sd["btn"]["end"].y = 0
				self.sd["btn"]["end_eff"].y = -Window.height * 2
				self.sd["btn"]["ablt_info"].y = -Window.height * 2
				self.sd["btn"]["draw_upto"].y = -Window.height * 2
				self.sd["btn"]["end_attack"].disabled = False
				self.sd["btn"]["end_phase"].disabled = False
				if "Climax" in self.gd["phase"]:
					self.sd["btn"]["end"].text = "Attack\nPhase"
					self.sd["btn"]["end_attack"].y = -Window.height
					self.sd["btn"]["end_phase"].y = -Window.height
				else:
					self.sd["btn"]["end"].disabled = False
					self.sd["btn"]["end"].text = "Climax\nPhase"
					self.sd["btn"]["end_attack"].y = 0
					self.sd["btn"]["end_phase"].y = 0

			if self.gd["resonance"][0]:
				self.gd["resonance"] = [False, []]
				self.hand_size(self.gd["active"])

			if self.net["game"] and self.gd["active"] == "2":
				if self.gd["show_wait_popup"]:
					Clock.schedule_once(partial(self.popup_text, "waiting"), move_dt_btw)
				self.mconnect("phase")
			elif self.gd["com"] and self.gd["active"] == "2":
				Clock.schedule_once(self.opp_play, move_dt_btw)
			elif "Counter" in self.gd["phase"]:
				Clock.scheduke_once(self.counter_step_done)
			else:
				if "Climax" in self.gd["phase"]:
					self.update_playable_climax(self.gd["active"])
				else:
					self.update_movable(self.gd["active"])
				self.hand_btn_show(False)

	def cont_cards(self, eff, ind):
		if "opp" in eff:
			if ind[-1] == "1":
				p = "2"
			elif ind[-1] == "2":
				p = "1"
		else:
			p = ind[-1]
		if "Memory" in eff:
			cards = [s for s in self.pd[p]["Memory"] if s != ""]
		elif "Waiting" in eff:
			cards = [s for s in self.pd[p]["Waiting"] if s != ""]
		elif "Clock" in eff:
			cards = [s for s in self.pd[p]["Clock"] if s != ""]
		elif "Back" in eff:
			cards = [s for s in self.pd[p]["Back"] if s != ""]
		elif "Center" in eff:
			cards = [s for s in self.pd[p]["Center"] if s != ""]
		else:
			cards = [s for s in self.pd[p]["Center"] + self.pd[p]["Back"] if s != ""]
		if "other" in eff and ind in cards:
			cards.remove(ind)
		return cards

	def cont_times(self, eff, cs, cd):
		if "NameSet" in eff:
			names = eff[eff.index("NameSet") + 1].split("_")
			nc = []
			for n in cs:
				if n != "":
					for nx in range(int(len(names) / 2)):
						if names[nx] in cd[n].name_t:
							if names[nx + int(len(names) / 2)] != "":
								for ss in sn["Title"][names[nx + int(len(names) / 2)]]:
									if ss in cd[n].cid:
										nc.append(n)
							else:
								nc.append(n)
		elif "xName" in eff:
			names = eff[eff.index("xName") + 1].split("_")
			nc = [n for n in cs if any(name in cd[n].name_t for name in names)]
		elif "Name=" in eff:
			names = eff[eff.index("Name=") + 1]
			nc = [n for n in cs if names in cd[n].name_t]
		elif "Name" in eff:
			names = eff[eff.index("Name") + 1].split("_")
			nc = [n for n in cs if any(name in cd[n].name_t for name in names)]
		elif "Trait" in eff:
			traits = eff[eff.index("Trait") + 1].split("_")
			if traits == [""]:
				nc = [n for n in cs if len(cd[n].trait_t) <= 0 and "Character" in self.cd[n].card]
			else:
				nc = [n for n in cs if any(trait in cd[n].trait_t for trait in traits)]
		elif "Colour" in eff:
			colours = eff[eff.index("Colour") + 1].split("_")
			nc = [n for n in cs if any(colour in cd[n].colour for colour in colours)]
		elif "LevelC" in eff:
			if "lower" in eff:
				nc = [n for n in cs if cd[n].level_t <= eff[eff.index("LevelC") + 1]]
			elif "lower" not in eff:
				nc = [n for n in cs if cd[n].level_t >= eff[eff.index("LevelC") + 1]]
		elif "Text" in eff:
			text = eff[eff.index("Text") + 1].split("_")
			# if "[AUTO] Encore [Put a character from your hand into your waiting room]" in text or"[AUTO] Encore [Put 1 character from your hand into your waiting room]" in text:
			# 	text = ["[AUTO] Encore [Put 1 character from your hand into your waiting room]","[AUTO] Encore [Put a character from your hand into your waiting room]"]
			# nc = [n for n in cs if any(text in tx[0] and f"\"{text}\"" not in tx[0] for tx in cd[n].text_c)]
			nc = [n for n in cs if any(any(
					text1.lower() in tx[0].lower() and f"\"{text1.lower()}\"" not in tx[0].lower() for text1 in text)
			                           for tx in cd[n].text_c)]
		elif "Character" in eff:
			nc = [n for n in cs if cd[n].card == "Character"]
		elif "Climax" in eff:
			nc = [n for n in cs if cd[n].card == "Climax"]
		elif "Rest" in eff:
			nc = [n for n in cs if cd[n].status == "Rest"]
		else:
			nc = cs
		return nc

	def check_cont_ability(self, *args):
		self.gd["backup"] = {"1": True, "2": True}
		self.gd["event"] = {"1": True, "2": True}
		self.gd["climax"] = {"1": True, "2": True}
		self.gd["clock"] = {"1": True, "2": True}
		self.gd["noact"] = {"1": True, "2": True}

		self.check_cont_hand("1")
		# self.rested_card_update()
		for player in list(self.pd.keys()):
			power_zero = []
			stage = list(self.pd[player]["Center"] + self.pd[player]["Back"])
			# for field in ("Center", "Back"):
			for ind in stage + [player]:
				if ind in self.emptycards:
					continue
				card = self.cd[ind]
				to_remove_p = []
				to_remove_s = []
				to_remove_t = []
				to_remove_l = []
				to_remove_n = []
				to_remove_tr = []
				# remove cont ability
				for power in card.power_c:
					if power[1] < 0:
						pp = False
						if "Turn" in power[2]:
							otd = power[2].split("_")[1]
							if "sMemory" in power and "Memory" not in self.cd[otd].pos_new:
								pp = True
							elif "Topp" in power and self.gd["active"] == otd[-1]:
								pp = True
							elif "Topp" not in power and self.gd["active"] != otd[-1]:
								pp = True
							if "Experience" in power:
								if sum([self.cd[lv].level for lv in self.pd[ind[-1]]["Level"]]) < power[
									power.index("Experience") + 1]:
									pp = True
							if otd != ind and otd not in stage:
								pp = True
						elif "Battle" in power[2]:
							deff = ""
							if self.gd["attacking"][0] != "":
								if self.gd["attacking"][0][-1] == "1":
									opp = "2"
								elif self.gd["attacking"][0][-1] == "2":
									opp = "1"
								if "C" in self.gd["attacking"][4]:
									deff = self.pd[opp]["Center"][self.gd["attacking"][3]]
								elif "B" in self.gd["attacking"][4]:
									deff = self.pd[opp]["Back"][self.gd["attacking"][3]]
								if ind == self.gd["attacking"][0]:
									if "xolevel" in power or "xlevel" in power:
										pp = True
									elif "olevel" in power and self.cd[deff].level < power[power.index("olevel") + 1]:
										pp = True
									elif "otrait" in power and all(otr not in self.cd[deff].trait_t for otr in
									                               power[power.index("otrait") + 1].split("_")):
										pp = True
								elif deff != "" and deff == ind:
									if "xolevel" in power or "xlevel" in power:
										pp = True
									elif "olevel" in power and self.cd[self.gd["attacking"][0]].level < power[
										power.index("olevel") + 1]:
										pp = True
									elif "otrait" in power and all(
											otr not in self.cd[self.gd["attacking"][0]].trait_t for otr in
											power[power.index("otrait") + 1].split("_")):
										pp = True
								else:
									pp = True
							else:
								pp = True
						elif "Assist" in power[2]:
							if "Center" in card.pos_new:
								if "1" in card.pos_new:
									if power[2].split("_")[-1] not in self.pd[player]["Back"]:
										pp = True
								else:
									if power[2].split("_")[-1] not in self.pd[player]["Back"][
										int(int(card.pos_new[-1]) / 2)]:
										pp = True
							elif "Back" in card.pos_new:
								pp = True
							if "Turn" in power:
								otd = power[2].split("_")[1]
								if "Topp" in power and self.gd["active"] == otd[-1]:
									pp = True
								elif "Topp" not in power and self.gd["active"] != otd[-1]:
									pp = True
						elif "X" in power[2]:
							e = True
							if "Experience" in power and sum([self.cd[lv].level for lv in self.pd[ind[-1]]["Level"]]) < \
									power[power.index("Experience") + 1]:
								e = False
							if "opposite" in power:
								if ind[-1] == "1":
									op = "2"
								else:
									op = "1"
								opp = self.pd[op]["Center"][self.m[int(card.pos_new[-1])]]
								if (opp == "" or (opp != "" and opp not in power[2]) or not e):
									pp = True
							elif "xhighlevel" in power:
								pp = True
						elif "Alarm" in power[2]:
							if len(self.pd[ind[-1]]["Clock"]) <= 0:
								pp = True
							elif power[2].split("_")[1] != self.pd[ind[-1]]["Clock"][-1]:
								pp = True
						elif "Climax" in power[2]:
							if power[2].split("_")[1] not in self.pd[player]["Climax"]:
								pp = True
						elif "Marker#" in power[2]:
							if ind in self.pd[ind[-1]]["marker"] and len(self.pd[ind[-1]]["marker"][ind]) < power[3]:
								pp = True
							elif ind not in self.pd[ind[-1]]["marker"]:
								pp = True
						elif "Each" in power[2]:
							idm = power[2].split("_")[1]
							if idm == ind:
								pp = True
							elif idm not in stage:
								pp = True
						elif "All" in power[2]:
							cards = [s for s in stage if s != ""]
							if len(self.cont_times(power, cards, self.cd)) != len(cards):
								pp = True
						elif "Another" in power[2]:
							cards = [s for s in stage if s != "" and s != ind]
							if len(self.cont_times(power, cards, self.cd)) < 1:
								pp = True
						elif "Experience" in power[2]:
							if "Name=" in power and len(self.cont_times(power, self.pd[ind[-1]]["Level"], self.cd)) < \
									power[3]:
								pp = True
							elif power[2].split("_")[-1] not in stage or sum(
									[self.cd[lv].level for lv in self.pd[ind[-1]]["Level"]]) < power[3]:
								pp = True
							else:
								if "fm" in power and card.pos_new != "Center1":
									pp = True
						elif "More" in power[2]:
							cards = self.cont_cards(power, ind)
							if "lower" in power and len(self.cont_times(power, cards, self.cd)) > power[3]:
								pp = True
							elif "lower" not in power and len(self.cont_times(power, cards, self.cd)) < power[3]:
								pp = True
							if "Turn" in power:
								otd = power[2].split("_")[1]
								if "Topp" in power and self.gd["active"] == otd[-1]:
									pp = True
								elif "Topp" not in power and self.gd["active"] != otd[-1]:
									pp = True
						elif "Other" in power[2]:
							idm = power[2].split("_")[1]
							if "Hand" in power and len(self.pd[player]["Hand"]) < power[power.index("Hand") + 1]:
								pp = True
							elif "Stock" in power and len(self.pd[player]["Stock"]) < power[power.index("Stock") + 1]:
								pp = True
							elif "OMore" in power and idm in stage:
								if "OMemory" in power:
									estage = [s for s in self.pd[idm[-1]]["Memory"] if s != ""]
								else:
									estage = [s for s in self.pd[idm[-1]]["Center"] + self.pd[idm[-1]]["Back"] if
									          s != ""]
								if "Oother" in power and idm in estage:
									estage.remove(idm)
								if "OName=" in power:
									meff = ["Name=", power[power.index("OName=") + 1]]
								emore = self.cont_times(meff, estage, self.cd)
								if len(emore) < power[power.index("OMore") + 1]:
									pp = True
							elif "Marker#" in power and idm in stage:
								if idm not in self.pd[idm[-1]]["marker"]:
									pp = True
								elif idm in self.pd[idm[-1]]["marker"] and len(self.pd[idm[-1]]["marker"][idm]) < power[
									power.index("Marker#") + 1]:
									pp = True
							elif idm in stage and "Experience" in power:
								if sum([self.cd[lv].level for lv in self.pd[idm[-1]]["Level"]]) < power[4]:
									pp = True
							elif power[2].split("_")[1] not in stage:
								pp = True
						elif "Hand" in power[2]:
							if "HandvsOpp" in power:
								if ind[-1] == "1":
									op = "2"
								elif ind[-1] == "2":
									op = "1"
								if len(self.pd[ind[-1]]["Hand"]) <= len(self.pd[op]["Hand"]):
									pp = True
							elif "lower" in power and len(self.pd[ind[-1]]["Hand"]) > power[3]:
								pp = True
							elif "lower" not in power and len(self.pd[ind[-1]]["Hand"]) < power[3]:
								pp = True
						elif "sMemory" in power[2]:
							otd = power[2].split("_")[1]
							if "Memory" not in self.cd[otd].pos_new:
								pp = True
						elif "Stock" in power[2]:
							if "lower" in power and len(self.pd[player]["Stock"]) > power[3]:
								pp = True
							elif "lower" not in power and len(self.pd[player]["Stock"]) < power[3]:
								pp = True
						elif "Middle" in power[2]:
							if ind in power[2] and card.pos_new == "Center1" and "other" in power:
								pp = True
							elif ind in power[2] and card.pos_new != "Center1":
								pp = True
							elif power[2].split("_")[1] not in stage or card.pos_new != "Center1":
								pp = True
						elif "Clock" in power[2]:
							if "opp" in power and ind[-1] == "1":
								opp = "2"
							elif "opp" in power and ind[-1] == "2":
								opp = "1"
							else:
								opp = ind[-1]
							if len(self.pd[opp]["Clock"]) < int(power[3]):
								pp = True
						elif "NoCH" in power[2]:
							if "Center" in power:
								nst = list(self.pd[ind[-1]]["Center"])
							else:
								nst = list(self.pd[ind[-1]]["Center"] + self.pd[ind[-1]["Back"]])
							if "other" in power and ind in nst:
								nst.remove(ind)
							if any(p != "" for p in nst):
								pp = True
						elif "LevelP" in power[2]:
							if "lower" not in power:
								if self.cd[ind].level_t <= len(self.pd[ind[-1]]["Level"]):
									pp = True
						if pp and power not in to_remove_p:
							to_remove_p.append(power)

				for soul in card.soul_c:
					if soul[1] < 0:
						ss = False
						if "Climax" in soul[2]:
							if soul[2].split("_")[1] not in self.pd[player]["Climax"]:
								ss = True
						elif "Assist" in soul[2]:
							if "Center" in card.pos_new:
								if "1" in card.pos_new:
									if soul[2].split("_")[-1] not in self.pd[player]["Back"]:
										ss = True
								else:
									if soul[2].split("_")[-1] not in self.pd[player]["Back"][
										int(int(card.pos_new[-1]) / 2)]:
										ss = True
							elif "Back" in card.pos_new:
								ss = True
						elif "Experience" in soul[2]:
							if "Name=" in soul and len(self.cont_times(soul, self.pd[ind[-1]]["Level"], self.cd)) < \
									soul[3]:
								ss = True
							elif soul[2].split("_")[-1] not in stage or sum(
									[self.cd[lv].level for lv in self.pd[ind[-1]]["Level"]]) < soul[3]:
								ss = True
							else:
								if "fm" in soul and card.pos_new != "Center1":
									ss = True
						elif "More" in soul[2]:
							cards = self.cont_cards(soul, ind)
							if "lower" in soul and len(self.cont_times(soul, cards, self.cd)) > soul[3]:
								ss = True
							elif "lower" not in soul and len(self.cont_times(soul, cards, self.cd)) < soul[3]:
								ss = True
							if "Turn" in soul:
								otd = soul[2].split("_")[1]
								if "Topp" in soul and self.gd["active"] == otd[-1]:
									ss = True
								elif "Topp" not in soul and self.gd["active"] != otd[-1]:
									ss = True
						elif "Opposite" in soul[2]:
							if card.ind[-1] == "1":
								op = "2"
							else:
								op = "1"
							opp = self.pd[op]["Center"][self.m[int(card.pos_new[-1])]]
							if opp == "" or (opp != "" and opp not in soul[2]):
								ss = True
						if ss and soul not in to_remove_s:
							to_remove_s.append(soul)

				for text in card.text_c:
					if len(text) > 2 and text[1] > -9 and text[1] < 0:
						tt = False
						if "Middle" in text[2]:
							if ind in text[2] and card.pos_new == "Center1" and "other" in text:
								tt = True
							if ind in text[2] and card.pos_new != "Center1":
								tt = True
								to_remove_t.append(text)
							elif (text[2].split("_")[1] not in stage or card.pos_new != "Center1"):
								tt = True
						elif "Marker#" in text[2]:
							if ind in self.pd[ind[-1]]["marker"] and len(self.pd[ind[-1]]["marker"][ind]) < text[3]:
								tt = True
							elif ind not in self.pd[ind[-1]]["marker"]:
								tt = True
						elif "Assist" in text[2]:
							if "Center" in card.pos_new:
								if "1" in card.pos_new:
									if text[2].split("_")[-1] not in self.pd[player]["Back"]:
										tt = True
								else:
									if text[2].split("_")[-1] not in self.pd[player]["Back"][
										int(int(card.pos_new[-1]) / 2)]:
										tt = True
							elif "Back" in card.pos_new:
								tt = True
						elif "Opposite" in text[2]:
							if card.ind[-1] == "1":
								op = "2"
							else:
								op = "1"
							opp = self.pd[op]["Center"][self.m[int(card.pos_new[-1])]]
							if "#traits" in text:
								if "#lower" not in text and len(
										[t for t in self.cd[opp].trait_t if t != ""]) < text[
									text.index("#traits") + 1]:
									tt = True
								elif "#lower" in text and len(
										[t for t in self.cd[opp].trait_t if t != ""]) > text[
									text.index("#traits") + 1]:
									tt = True

							if opp == "" or (opp != "" and opp not in text[2]):
								tt = True
							elif "Center" not in card.pos_new:
								tt = True

						elif "Stock" in text[2]:
							if "lower" in text and len(self.pd[ind[-1]]["Stock"]) > text[3]:
								tt = True
							elif "lower" not in text and len(self.pd[ind[-1]]["Stock"]) < text[3]:
								tt = True
						elif "Other" in text[2]:
							idm = text[2].split("_")[1]
							if idm in stage and "Experience" in text:
								if sum([self.cd[lv].level for lv in self.pd[idm[-1]]["Level"]]) < text[4]:
									tt = True
							elif "OMore" in text and idm in stage:
								if "OMemory" in text:
									estage = [s for s in self.pd[idm[-1]]["Memory"] if s != ""]
								else:
									estage = [s for s in self.pd[idm[-1]]["Center"] + self.pd[idm[-1]]["Back"] if
									          s != ""]
								if "Oother" in text and idm in estage:
									estage.remove(idm)
								if "OName=" in text:
									meff = ["Name=", text[text.index("OName=") + 1]]
								else:
									meff = []
								emore = self.cont_times(meff, estage, self.cd)
								if len(emore) < text[text.index("OMore") + 1]:
									tt = True
							elif idm not in stage:
								tt = True
						elif "Alarm" in text[2]:
							if len(self.pd[ind[-1]]["Clock"]) <= 0:
								tt = True
							elif text[2].split("_")[1] != self.pd[ind[-1]]["Clock"][-1]:
								tt = True
							elif "plevel" in text:
								if len(self.pd[ind[-1]]["Level"]) < text[text.index("plevel") + 1]:
									tt = True
						# elif "Colour" in text and text[text.index("Colour") + 1] not in self.cd[
						# 	ind[-1]].mcolour and text not in to_remove_t:
						# 	to_remove_t.append(text)
						# elif "LevelC" in text and len(self.pd[ind[-1]]["Level"]) < text[
						# 	text.index("Level") + 1] and text not in to_remove_t:
						# 	to_remove_t.append(text)
						elif "Hand" in text[2]:
							if "lower" in text and len(self.pd[ind[-1]]["Hand"]) > text[3]:
								tt = True
							elif "lower" not in text and len(self.pd[ind[-1]]["Hand"]) < text[3]:
								tt = True
						elif "More" in text[2]:
							cards = self.cont_cards(text, ind)
							if "lower" in text and len(self.cont_times(text, cards, self.cd)) > text[3]:
								tt = True
							elif "lower" not in text and len(self.cont_times(text, cards, self.cd)) < text[3]:
								tt = True
						elif "Middle" in text[2]:
							if ind in text[2] and card.pos_new == "Center1" and "other" in text:
								tt = True
							elif ind in text[2] and card.pos_new != "Center1":
								tt = True
							elif text[2].split("_")[1] not in stage or card.pos_new != "Center1":
								tt = True
						elif "NoCH" in text[2]:
							if "Center" in text:
								nst = list(self.pd[ind[-1]]["Center"])
							else:
								nst = list(self.pd[ind[-1]]["Center"] + self.pd[ind[-1]["Back"]])
							if "other" in text and ind in nst:
								nst.remove(ind)
							if any(t != "" for t in nst):
								tt = True
						elif "Experience" in text[2]:
							if "Name=" in text and len(self.cont_times(text, self.pd[ind[-1]]["Level"], self.cd)) < \
									text[3]:
								tt = True
							elif text[2].split("_")[-1] not in stage or sum(
									[self.cd[lv].level for lv in self.pd[ind[-1]]["Level"]]) < text[3]:
								tt = True
							else:
								if "fm" in text and card.pos_new != "Center1":
									tt = True
						if tt and text not in to_remove_t:
							to_remove_t.append(text)

				for level in card.level_c:
					if level[1] < 0:
						ll = False
						otd = level[2].split("_")[1]
						if "Turn" in level[2]:
							if "Topp" in level and self.gd["active"] == otd[-1]:
								ll = True
							elif "Topp" not in level and self.gd["active"] != otd[-1]:
								ll = True
							if otd != ind and otd not in stage:
								ll = True
						elif "Each" in level[2]:
							if level[2].split("_")[1] == ind:
								ll = True
							elif level[2].split("_")[1] not in stage:
								ll = True
						elif "pHand" in level:
							ll = True
						elif "Stock" in level[2]:
							if "lower" in level and len(self.pd[player]["Stock"]) > level[3]:
								ll = True
							elif "lower" not in level and len(self.pd[player]["Stock"]) < level[3]:
								ll = True
						elif "Stage" in level[2]:
							if otd not in stage:
								ll = True
						elif "Other" in level[2]:
							if otd not in stage:
								ll = True
						elif "Assist" in level[2]:
							if "Center" in card.pos_new:
								if "1" in card.pos_new:
									if otd not in self.pd[player]["Back"]:
										ll = True
								else:
									if otd not in self.pd[player]["Back"][int(int(card.pos_new[-1]) / 2)]:
										ll = True
							elif "Back" in card.pos_new:
								ll = True
						elif "More" in level[2]:
							cards = self.cont_cards(level, ind)
							if "lower" in level and len(self.cont_times(level, cards, self.cd)) > level[3]:
								ll = True
							elif "lower" not in level and len(self.cont_times(level, cards, self.cd)) < level[3]:
								ll = True
							if "Turn" in level:
								if "Topp" in level and self.gd["active"] == otd[-1]:
									ll = True
								elif "Topp" not in level and self.gd["active"] != otd[-1]:
									ll = True
						if ll and level not in to_remove_l:
							to_remove_l.append(level)

				for trait in card.trait_c:
					if trait[1] < 0:
						pp = False
						if "Opposite" in trait[2]:
							if card.ind[-1] == "1":
								op = "2"
							else:
								op = "1"
							opp = self.pd[op]["Center"][self.m[int(card.pos_new[-1])]]
							if opp == "" or (opp != "" and opp not in trait[2]):
								pp = True
						elif "Battle" in trait[2]:
							deff = ""
							if self.gd["attacking"][0] != "":
								if self.gd["attacking"][0][-1] == "1":
									opp = "2"
								elif self.gd["attacking"][0][-1] == "2":
									opp = "1"
								if "C" in self.gd["attacking"][4]:
									deff = self.pd[opp]["Center"][self.gd["attacking"][3]]
								elif "B" in self.gd["attacking"][4]:
									deff = self.pd[opp]["Back"][self.gd["attacking"][3]]
								if ind == self.gd["attacking"][0]:
									if "olevel" in trait and self.cd[deff].level < trait[trait.index("olevel") + 1]:
										pp = True
									elif "otrait" in trait and all(otr not in self.cd[deff].trait_t for otr in
									                               trait[trait.index("otrait") + 1].spit("_")):
										pp = True
								elif deff != "" and deff == ind:
									if "olevel" in trait and self.cd[self.gd["attacking"][0]].level < trait[
										trait.index("olevel") + 1]:
										pp = True
									elif "otrait" in trait and all(
											otr not in self.cd[self.gd["attacking"][0]].trait_t for otr in
											trait[trait.index("otrait") + 1].split("_")):
										pp = True
								else:
									pp = True
							else:
								pp = True
						elif "More" in trait[2]:
							cards = self.cont_cards(trait, ind)
							if "lower" in trait and len(self.cont_times(trait, cards, self.cd)) > trait[3]:
								pp = True
							elif "lower" not in trait and len(self.cont_times(trait, cards, self.cd)) < trait[3]:
								pp = True

						if pp and trait not in to_remove_tr:
							to_remove_tr.append(trait)

				for name in card.name_c:
					if name[1] < 0:
						pp = False
						if "More" in name[2]:
							cards = self.cont_cards(name, ind)
							if "lower" in name and len(self.cont_times(name, cards, self.cd)) > name[3]:
								pp = True
							elif "lower" not in name and len(self.cont_times(name, cards, self.cd)) < name[3]:
								pp = True
						elif "Stage" in name[2]:
							if "Center" not in card.pos_new and "Back" not in card.pos_new:
								pp = True
						if pp and name not in to_remove_n:
							to_remove_n.append(name)

				for itemp in to_remove_p:
					card.power_c.remove(itemp)
				for items in to_remove_s:
					card.soul_c.remove(items)
				for itemt in to_remove_t:
					card.text_c.remove(itemt)
				for iteml in to_remove_l:
					card.level_c.remove(iteml)
				for itemtr in to_remove_tr:
					card.trait_c.remove(itemtr)
				for itemn in to_remove_n:
					card.name_c.remove(itemn)

				# cards = [s for s in self.pd[player]["Center"] + self.pd[player]["Back"] if s != ""]
				for item in card.text_c:
					if item[0].startswith(cont_ability) and item[1] > -9 and item[1] != 0:
						effect = ab.cont(a=item[0])
						if len(effect) < 4 and "marker#" not in effect:
							continue
						if "no_encore" in effect:
							e = player
							if "opp" in effect:
								if player == "1":
									e = "2"
								elif player == "2":
									e = "1"
							self.gd["noencore"][e] = True
							continue
						if "pHand" in effect:
							continue
						if "no_backup" in effect:
							e = player
							if "opp" in effect:
								if player == "1":
									e = "2"
								elif player == "2":
									e = "1"
							if "battle" not in effect:
								self.gd["backup"][e] = False
						if "no_event" in effect:
							e = player
							if "opp" in effect:
								if player == "1":
									e = "2"
								elif player == "2":
									e = "1"
							if "battle" not in effect:
								self.gd["event"][e] = False
						if "no_climax" in effect:
							e = player
							if "opp" in effect:
								if player == "1":
									e = "2"
								elif player == "2":
									e = "1"
							self.gd["climax"][e] = False
						if "no_clock" in effect:
							e = player
							if "opp" in effect:
								if player == "1":
									e = "2"
								elif player == "2":
									e = "1"
							self.gd["clock"][e] = False
						if "no_act" in effect:
							e = player
							if "opp" in effect:
								if player == "1":
									e = "2"
								elif player == "2":
									e = "1"
							self.gd["noact"][e] = False

						if "marker#" in effect:
							effect = effect[1]
						else:
							effect = [effect]

						for effs in effect:
							seff = []
							peff = []
							aeff = []
							leff = []
							teff = []
							neff = []

							if "soul" in effs and "ability" in effs:
								enx = effs.index("ability") + 1
								seff = effs[enx:]
								aeff = effs[:enx]
							elif "ability" in effs and "power" in effs:
								enx = effs.index("power") + 1
								aeff = effs[enx:]
								peff = effs[:enx]
							elif "trait" in effs and "name" in effs:
								enx = effs.index("trait") + 1
								neff = effs[enx:]
								teff = effs[:enx]
							elif "level" in effs and "power" in effs:
								enx = effs.index("power") + 1
								leff = effs[enx:]
								peff = effs[:enx]
							elif "soul" in effs and "power" in effs:
								enx = effs.index("power") + 1
								seff = effs[enx:]
								peff = effs[:enx]
							elif "ability" in effs:
								aeff = list(effs)
							elif "power" in effs:
								peff = list(effs)
							elif "soul" in effs:
								seff = list(effs)
							elif "level" in effs:
								leff = list(effs)
							elif "trait" in effs:
								teff = list(effs)
							elif "name" in effs:
								neff = list(effs)

							if peff:
								if ind not in peff[3]:
									peff[3] += f"_{ind}"
								if "opp" in peff:
									if player == "1":
										p = "2"
									elif player == "2":
										p = "1"
								else:
									p = player
								pcards = self.cont_cards(peff, ind)
								ptimes = self.cont_times(peff, pcards, self.cd)
								if peff[0] == 0:
									pp = False
									if "All" in peff[3]:
										if len(ptimes) == len(pcards):
											pp = True
									elif "Hand" in peff[3]:
										if "HandvsOpp" in peff:
											if ind[-1] == "1":
												op = "2"
											elif ind[-1] == "2":
												op = "1"
											if len(self.pd[ind[-1]]["Hand"]) > len(self.pd[op]["Hand"]):
												pp = True

										elif "lower" not in peff and len(self.pd[p]["Hand"]) >= peff[4]:
											pp = True
										elif "lower" in peff and len(self.pd[p]["Hand"]) <= peff[4]:
											pp = True
									elif "Stock" in peff[3]:
										if "lower" in peff and len(self.pd[p]["Stock"]) <= peff[4]:
											pp = True
										elif "lower" not in peff and len(self.pd[p]["Stock"]) >= peff[4]:
											pp = True
									elif "Stock" in peff[3]:
										if "lower" not in peff and len(self.pd[p]["Stock"]) >= peff[4]:
											pp = True
									elif "Clock" in peff[3]:
										if len(self.pd[p]["Clock"]) >= peff[4]:
											pp = True
									elif "Marker#" in peff[3]:
										if ind in self.pd[p]["marker"] and len(self.pd[p]["marker"][ind]) >= peff[4]:
											pp = True
									elif "Each" in peff[3]:
										if "marker" in peff:
											if ind in self.pd[p]["marker"]:
												for mnx in range(len(self.pd[player]["marker"][ind])):
													card.power_c.append(peff[1:] + [mnx])
										else:
											if "markers" in peff and ind not in self.pd[p]["marker"]:
												continue
											if "OMore" in peff:
												if "OMemory" in peff:
													estage = [s for s in self.pd[ind[-1]]["Memory"] if s != ""]
												else:
													estage = [s for s in
													          self.pd[ind[-1]]["Center"] + self.pd[ind[-1]]["Back"] if
													          s != ""]
												opeff = []
												if "OTrait" in peff:
													opeff.append("Trait")
													opeff.append(peff[peff.index("OTrait") + 1])
												emore = self.cont_times(opeff, estage, self.cd)
												if len(emore) < peff[peff.index("OMore") + 1]:
													ptimes = []
											if "Turn" in peff:
												if "Topp" not in peff and self.gd["active"] not in ind[-1]:
													ptimes = []
												elif "Topp" in peff and self.gd["active"] in ind[-1]:
													ptimes = []
											if "Rest" in peff:
												ptimes = [s for s in ptimes if self.cd[s].status == "Rest"]
											elif "Traits" in peff:
												ptimes = []
												for t in pcards:
													for tr in self.cd[t].trait_t:
														if tr not in ptimes:
															ptimes.append(tr)
											for mnx in range(len(ptimes)):
												card.power_c.append(peff[1:] + [mnx])
									elif "X" in peff[3]:
										tip = 0
										e = True
										if "opposite" in peff and "xlevel" in peff:
											if ind[-1] == "1":
												op = "2"
											else:
												op = "1"
											opp = self.pd[op]["Center"][self.m[int(card.pos_new[-1])]]
											if opp != "":
												tip = self.cd[opp].level
										elif "xhighlevel" in peff:
											if len(ptimes) > 0:
												tip = self.cd[
													sorted(ptimes, key=lambda x: self.cd[x].level_t)[-1]].level_t

										peff[1] = tip * peff[peff.index("x") + 1]

										if "Experience" in peff and sum(
												[self.cd[lv].level for lv in self.pd[p]["Level"]]) < \
												peff[peff.index("Experience") + 1]:
											e = False

										if e and peff[1] != 0 and peff[1:] not in card.power_c:
											card.power_c.append(peff[1:])
									elif "Another" in peff[3]:
										if len(ptimes) <= 1:
											pp = True
									elif "Battle" in peff[3]:
										deff = ""
										if self.gd["attacking"][0] != "":
											if self.gd["attacking"][0][-1] == "1":
												opp = "2"
											elif self.gd["attacking"][0][-1] == "2":
												opp = "1"
											if "C" in self.gd["attacking"][4]:
												deff = self.pd[opp]["Center"][self.gd["attacking"][3]]
											elif "B" in self.gd["attacking"][4]:
												deff = self.pd[opp]["Back"][self.gd["attacking"][3]]

											if ind == self.gd["attacking"][0]:
												if "xolevel" in peff:
													peff[1] = peff[1] * self.cd[deff].level_t
												if "olevel" in peff and self.cd[deff].level >= peff[
													peff.index("olevel") + 1]:
													pp = True
												elif "otrait" in peff and any(otr in self.cd[
													deff].trait_t for otr in peff[peff.index("otrait") + 1].split("_")):
													pp = True
												elif "olevel" not in peff and "otrait" not in peff:
													pp = True
											elif deff != "" and deff == ind:
												if "xolevel" in peff:
													peff[1] = peff[1] * self.cd[self.gd["attacking"][0]].level_t
												if "olevel" in peff and self.cd[self.gd["attacking"][0]].level >= peff[
													peff.index("olevel") + 1]:
													pp = True
												elif "otrait" in peff and any(otr in self.cd[
													self.gd["attacking"][0]].trait_t for otr in
												                              peff[peff.index("otrait") + 1].split(
														                              "_")):
													pp = True
												elif "olevel" not in peff and "otrait" not in peff:
													pp = True
									elif "More" in peff[3]:
										if "lower" in peff and len(ptimes) <= peff[4]:
											pp = True
										elif "lower" not in peff and len(ptimes) >= peff[4]:
											pp = True
										if "Turn" in peff:
											if "Topp" in peff and self.gd["active"] in ind[-1]:
												pp = False
											elif "Topp" not in peff and self.gd["active"] not in ind[-1]:
												pp = False
									elif "Middle" in peff[3]:
										if card.pos_new == "Center1":
											pp = True
									elif "Turn" in peff[3]:
										if "Topp" in peff and self.gd["active"] not in ind[-1]:
											pp = True
										elif "Topp" not in peff and self.gd["active"] in ind[-1]:
											pp = True
									elif "Experience" in peff[3]:
										if "Name=" in peff:
											if len(self.cont_times(peff, self.pd[p]["Level"], self.cd)) >= peff[4]:
												pp = True
										elif sum([self.cd[lv].level for lv in self.pd[p]["Level"]]) >= peff[4]:
											pp = True
									elif "NoCH" in peff[3]:
										if "Center" in peff:
											nst = list(self.pd[ind[-1]]["Center"])
										else:
											nst = list(self.pd[ind[-1]]["Center"] + self.pd[ind[-1]["Back"]])
										if "other" in peff and ind in nst:
											nst.remove(ind)
										if any(p == "" for p in nst):
											pp = True
									if pp and peff[1:] not in card.power_c:
										card.power_c.append(peff[1:])
								elif peff[0] == -1:
									pp = True
									if "sMemory" in peff and "Memory" not in self.cd[ind].pos_new:
										pp = False
									if "Alarm" in peff[3] or "Alarm" in peff:
										pp = False
									if "Turn" in peff[3]:
										if "Topp" in peff and self.gd["active"] in ind[-1]:
											pp = False
										elif "Topp" not in peff and self.gd["active"] not in ind[-1]:
											pp = False

									for pinx in ptimes:
										if pp and peff[1:] not in self.cd[pinx].power_c:
											if "LevelP" in peff[3]:
												if "lower" not in peff:
													if self.cd[pinx].level_t > len(self.pd[pinx[-1]]["Level"]):
														self.cd[pinx].power_c.append(peff[1:])
											else:
												self.cd[pinx].power_c.append(peff[1:])

											self.cd[pinx].update_power()
											if self.cd[pinx].power_t <= 0:
												power_zero.append(pinx)
								elif peff[0] == -2:
									if ind in ptimes:
										ptimes.remove(ind)
									if "OMore" in peff:
										if "OMemory" in peff:
											estage = [s for s in self.pd[ind[-1]]["Memory"] if s != ""]
										else:
											estage = [s for s in self.pd[ind[-1]]["Center"] + self.pd[ind[-1]]["Back"]
											          if
											          s != ""]
										if "Oother" in peff and ind in estage:
											estage.remove(ind)
										meff = []
										if "OName=" in peff:
											meff = ["Name=", peff[peff.index("OName=") + 1]]
										emore = self.cont_times(meff, estage, self.cd)
										if len(emore) < peff[peff.index("OMore") + 1]:
											ptimes = []
									elif "Marker#" in peff:
										if ind in self.pd[p]["marker"] and len(self.pd[p]["marker"][ind]) < peff[
											peff.index("Marker#") + 1]:
											ptimes = []
										elif ind not in self.pd[p]["marker"]:
											ptimes = []
									if "Alarm" in peff[3] or "Alarm" in peff:
										ptimes = []
									if "Turn" in peff[3]:
										if "Topp" not in peff and self.gd["active"] not in ind[-1]:
											ptimes = []
										elif "Topp" in peff and self.gd["active"] in ind[-1]:
											ptimes = []
									if "Experience" in peff and sum([self.cd[lv].level for lv in self.pd[p]["Level"]]) < \
											peff[peff.index("Experience") + 1]:
										ptimes = []
									elif "Hand" in peff and len(self.pd[ind[-1]]["Hand"]) < peff[
										peff.index("Hand") + 1]:
										ptimes = []
									elif "Stock" in peff and len(self.pd[ind[-1]]["Stock"]) < peff[
										peff.index("Stock") + 1]:
										ptimes = []
									for pnx in ptimes:
										if "xlevel" in peff:
											peff[1] = peff[peff.index("x") + 1] * self.cd[pnx].level_t
										if peff[1:] not in self.cd[pnx].power_c:
											self.cd[pnx].power_c.append(peff[1:])
											self.cd[pnx].update_power()
											if self.cd[pnx].power_t <= 0:
												power_zero.append(pnx)
								elif peff[0] == -5:
									cind = ""
									if "Experience" in peff[3] and sum(
											[self.cd[lv].level for lv in self.pd[p]["Level"]]) >= peff[4]:
										cind = self.pd[p]["Center"][1]
									elif "Middle" in peff[3]:
										cind = self.pd[p]["Center"][1]

									if "other" in peff and ind == cind:
										cind = ""

									if cind != "" and peff[1:] not in self.cd[cind].power_c:
										self.cd[cind].power_c.append(peff[1:])
										self.cd[cind].update_power()
										if self.cd[cind].power_t <= 0:
											power_zero.append(cind)
								elif peff[0] == "front" and "Assist" in peff[3] and "Back" in card.pos_new:
									for finx in range(int(card.pos_new[-1]), int(card.pos_new[-1]) + 2):
										if self.pd[p]["Center"][finx] != "":
											pp = True
											front = self.cd[self.pd[p]["Center"][finx]]
											if "x" in peff and "flevel" in peff:
												peff[1] = front.level_t * peff[peff.index("x") + 1]
											elif "x" in peff and "Level" in peff:
												asst = 0
												if "LevTrait" in peff:
													trait = peff[peff.index("LevTrait") + 1].split("_")
													asst = len([lv for lv in self.pd[ind[-1]]["Level"] if
													            any(tr in self.cd[lv].trait_t for tr in trait)])
												peff[1] = asst * peff[peff.index("x") + 1]
											elif "lower" not in peff and "flevel" in peff and front.level < peff[
												peff.index("flevel") + 1]:
												pp = False
											elif "lower" in peff and "flevel" in peff and front.level > peff[
												peff.index("flevel") + 1]:
												pp = False
											if "Trait" in peff and all(tr not in front.trait_t for tr in
											                           peff[peff.index("Trait") + 1].split("_")):
												pp = False
											elif "Text" in peff:
												if any(peff[peff.index("Text") + 1] in txt[
													0] and f"\"{peff[peff.index('Text') + 1]}" not in txt[0] for txt in
												       front.text_c):
													pass
												else:
													pp = False
											if "Turn" in peff:
												if "Topp" not in peff and self.gd["active"] not in ind[-1]:
													pp = False
												elif "Topp" in peff and self.gd["active"] in ind[-1]:
													pp = False
											if pp and peff[1:] not in front.power_c:
												front.power_c.append(peff[1:])
												front.update_power()
												if front.power_t <= 0:
													power_zero.append(front.ind)

							if seff:
								if ind not in seff[3]:
									seff[3] += f"_{ind}"
								if "opp" in seff:
									if player == "1":
										p = "2"
									elif player == "2":
										p = "1"
								else:
									p = player
								scards = self.cont_cards(seff, ind)
								stimes = self.cont_times(seff, scards, self.cd)
								if seff[0] == 0:
									ss = False
									if "Experience" in seff[3]:
										if "Name=" in seff:
											if len(self.cont_times(seff, self.pd[p]["Level"], self.cd)) >= peff[4]:
												ss = True
										elif sum([self.cd[lv].level for lv in self.pd[p]["Level"]]) >= seff[4]:
											ss = True
									elif "More" in seff[3]:
										if "lower" in seff and len(stimes) <= seff[4]:
											ss = True
										elif "lower" not in peff and len(stimes) >= seff[4]:
											ss = True
										if "Turn" in seff:
											if "Topp" in seff and self.gd["active"] in ind[-1]:
												ss = False
											elif "Topp" not in seff and self.gd["active"] not in ind[-1]:
												ss = False

									if ss and seff[1:] not in card.soul_c:
										card.soul_c.append(seff[1:])
								elif seff[0] == -6 and "Center" in card.pos_new:
									if ind[-1] == "1":
										op = "2"
									else:
										op = "1"
									opp = self.pd[op]["Center"][self.m[int(card.pos_new[-1])]]
									if opp != "" and seff[1:] not in self.cd[opp].soul_c:
										self.cd[opp].soul_c.append(seff[1:])
										self.cd[opp].update_soul()
								elif seff[0] == "front" and "Assist" in seff[3] and "Back" in card.pos_new:
									for finx in range(int(card.pos_new[-1]), int(card.pos_new[-1]) + 2):
										if self.pd[p]["Center"][finx] != "":
											ss = True
											front = self.cd[self.pd[p]["Center"][finx]]
											if "flevel" in seff and front.level < seff[seff.index("flevel") + 1]:
												ss = False
											if "Trait" in seff and all(tr not in front.trait_t for tr in
											                           seff[seff.index("Trait") + 1].split("_")):
												ss = False

											if ss and seff[1:] not in front.soul_c:
												front.soul_c.append(seff[1:])
												front.update_soul()

							if leff:
								if ind not in leff[3]:
									leff[3] += f"_{ind}"
								if "opp" in leff:
									if player == "1":
										p = "2"
									elif player == "2":
										p = "1"
								else:
									p = player
								lcards = self.cont_cards(leff, ind)
								ltimes = self.cont_times(leff, lcards, self.cd)
								if leff[0] == 0:
									ll = False
									if "Each" in leff[3]:
										if "marker" in leff:
											if ind in self.pd[p]["marker"]:
												for mnx in range(len(self.pd[player]["marker"][ind])):
													card.level_c.append(leff[1:] + [mnx])
										else:
											if "markers" in leff and ind not in self.pd[p]["marker"]:
												continue
											for mnx in range(len(ltimes)):
												card.level_c.append(leff[1:] + [mnx])
									elif "Stock" in leff[3]:
										if "lower" in leff and len(self.pd[p]["Stock"]) <= leff[4]:
											ll = True
										elif "lower" not in leff and len(self.pd[p]["Stock"]) >= leff[4]:
											ll = True
									elif "More" in leff[3]:
										if "lower" in leff and len(ltimes) <= leff[4]:
											ll = True
										elif "lower" not in leff and len(ltimes) >= leff[4]:
											ll = True
										if "Turn" in leff:
											if "Topp" in leff and self.gd["active"] in ind[-1]:
												ll = False
											elif "Topp" not in leff and self.gd["active"] not in ind[-1]:
												ll = False
									elif "Stage" in leff[3]:
										if "Center" in card.pos_new or "Back" in card.pos_new:
											ll = True
									if ll and leff[1:] not in card.level_c:
										card.level_c.append(leff[1:])
								elif leff[0] == -2:
									if ind in ltimes:
										ltimes.remove(ind)
									if "Turn" in leff[3]:
										if "Topp" not in leff and self.gd["active"] not in ind[-1]:
											ltimes = []
										elif "Topp" in leff and self.gd["active"] in ind[-1]:
											ltimes = []

									for lnx in ltimes:
										if leff[1:] not in self.cd[lnx].level_c:
											self.cd[lnx].level_c.append(leff[1:])
											self.cd[lnx].update_level()
								elif leff[0] == "front" and "Assist" in leff[3] and "Back" in card.pos_new:
									for finx in range(int(card.pos_new[-1]), int(card.pos_new[-1]) + 2):
										if self.pd[p]["Center"][finx] != "":
											ll = False
											front = self.cd[self.pd[p]["Center"][finx]]

											if "Trait" in leff and any(tr in front.trait_t for tr in
											                           leff[leff.index("Trait") + 1].split("_")):
												ll = True
											if ll and leff[1:] not in front.level_c:
												front.level_c.append(leff[1:])
												front.update_level()

							if teff:
								if ind not in teff[3]:
									teff[3] += f"_{ind}"
								if "opp" in teff:
									if player == "1":
										p = "2"
									elif player == "2":
										p = "1"
								else:
									p = player
								tcards = self.cont_cards(teff, ind)
								ttimes = self.cont_times(teff, tcards, self.cd)

								if teff[0] == 0:
									pp = True
									if "Battle" in teff[3]:
										pp = False
										deff = ""
										if self.gd["attacking"][0] != "":
											if self.gd["attacking"][0][-1] == "1":
												opp = "2"
											elif self.gd["attacking"][0][-1] == "2":
												opp = "1"
											if "C" in self.gd["attacking"][4]:
												deff = self.pd[opp]["Center"][self.gd["attacking"][3]]
											elif "B" in self.gd["attacking"][4]:
												deff = self.pd[opp]["Back"][self.gd["attacking"][3]]
											if ind == self.gd["attacking"][0]:
												if "olevel" in teff and self.cd[deff].level >= teff[
													teff.index("olevel") + 1]:
													pp = True
												elif "otrait" in teff and any(otr in self.cd[deff].trait_t for otr in
												                              teff[teff.index("otrait") + 1].split(
														                              "_")):
													pp = True
												elif "olevel" not in teff and "otrait" not in teff:
													pp = True
											elif deff != "" and deff == ind:
												if "olevel" in teff and self.cd[self.gd["attacking"][0]].level >= teff[
													teff.index("olevel") + 1]:
													pp = True
												elif "otrait" in peff and any(
														otr in self.cd[self.gd["attacking"][0]].trait_t for otr in
														teff[teff.index("otrait") + 1].split("_")):
													pp = True
												elif "olevel" not in teff and "otrait" not in teff:
													pp = True
									elif "More" in teff[3]:
										if "lower" not in teff and len(ttimes) < teff[4]:
											pp = False
										elif "lower" in teff and len(ttimes) > teff[4]:
											pp = False
									if pp and teff[1:] not in card.trait_c:
										card.trait_c.append(teff[1:])
								if teff[0] == -6 and "Center" in card.pos_new:
									if ind[-1] == "1":
										op = "2"
									else:
										op = "1"
									opp = self.pd[op]["Center"][self.m[int(card.pos_new[-1])]]
									if opp != "" and teff[1:] not in self.cd[opp].trait_c:
										self.cd[opp].trait_c.append(teff[1:])
										self.cd[opp].update_trait()

							if aeff:
								if ind not in aeff[3]:
									aeff[3] += f"_{ind}"
								if "opp" in aeff:
									if player == "1":
										p = "2"
									elif player == "2":
										p = "1"
								else:
									p = player
								acards = self.cont_cards(aeff, ind)
								atimes = self.cont_times(aeff, acards, self.cd)

								if aeff[0] == 0:
									aa = False
									if "More" in aeff[3]:
										if "lower" in aeff and len(atimes) <= aeff[4]:
											aa = True
										elif "lower" not in aeff and len(atimes) >= aeff[4]:
											aa = True
										if "Turn" in aeff:
											if "Topp" in aeff and self.gd["active"] in ind[-1]:
												aa = False
											elif "Topp" not in aeff and self.gd["active"] not in ind[-1]:
												aa = False
									elif "Hand" in aeff[3]:
										if "lower" not in aeff and len(self.pd[p]["Hand"]) >= aeff[4]:
											aa = True
										elif "lower" in aeff and len(self.pd[p]["Hand"]) <= aeff[4]:
											aa = True
									elif "Middle" in aeff[3]:
										if card.pos_new == "Center1":
											aa = True
									elif "NoCH" in aeff[3]:
										if "Center" in aeff:
											nst = list(self.pd[ind[-1]]["Center"])
										else:
											nst = list(self.pd[ind[-1]]["Center"] + self.pd[ind[-1]["Back"]])
										if "other" in aeff and ind in nst:
											nst.remove(ind)
										if any(p == "" for p in nst):
											aa = True
									elif "Marker#" in aeff[3]:
										if ind in self.pd[p]["marker"] and len(self.pd[p]["marker"][ind]) >= aeff[4]:
											aa = True
									elif "Stock" in aeff[3]:
										if "lower" not in aeff and len(self.pd[p]["Stock"]) >= aeff[4]:
											aa = True
									elif "Experience" in aeff[3]:
										if "Name=" in aeff:
											if len(self.cont_times(aeff, self.pd[p]["Level"], self.cd)) >= aeff[4]:
												aa = True
										elif sum([self.cd[lv].level for lv in self.pd[p]["Level"]]) >= aeff[4]:
											aa = True
									elif "Opposite" in aeff[3]:
										if ind[-1] == "1":
											op = "2"
										else:
											op = "1"
										opp = self.pd[op]["Center"][self.m[int(card.pos_new[-1])]]
										if "#traits" in aeff and opp!="":
											if "#lower" not in aeff and len(
													[t for t in self.cd[opp].trait_t if t != ""]) >= aeff[
												aeff.index("#traits") + 1]:
												aa = True
											elif "#lower" in aeff and len(
													[t for t in self.cd[opp].trait_t if t != ""]) <= aeff[
												aeff.index("#traits") + 1]:
												aa = True
										if "Center" not in card.pos_new:
											aa = False
									if aa and aeff[1:] not in card.text_c:
										card.text_c.append(aeff[1:])
								# elif aeff[0] == -1:
								# 	aa = False
								# 	if "Alarm" in aeff[3]:
								# 		if "Level" in aeff and len(self.pd[p]["Level"]) >= aeff[
								# 			aeff.index("Level") + 1]:
								#
								# 	for anx in atimes:
								# 		if aa and aeff[1:] not in self.cd[anx].text_c:
								# 			self.cd[anx].text_c.append(aeff[1:])
								# 			self.cd[anx].update_ability()
								elif aeff[0] == -2:
									if ind in atimes:
										atimes.remove(ind)
									if "Turn" in aeff:
										if "Topp" not in aeff and ind[-1] != self.gd["active"]:
											atimes = []
										elif "Topp" in aeff and ind[-1] == self.gd["active"]:
											atimes = []
									elif "Experience" in aeff and sum(
											[self.cd[lv].level for lv in self.pd[p]["Level"]]) < aeff[5]:
										atimes = []

									for anx in atimes:
										if aeff[1:] not in self.cd[anx].text_c:
											self.cd[anx].text_c.append(aeff[1:])
											self.cd[anx].update_ability()
								elif aeff[0] == -32:
									if ind not in atimes:
										atimes.append(ind)
									if "OMore" in aeff:
										if "OMemory" in aeff:
											estage = [s for s in self.pd[ind[-1]]["Memory"] if s != ""]
										else:
											estage = [s for s in self.pd[ind[-1]]["Center"] + self.pd[ind[-1]]["Back"]
											          if
											          s != ""]
										if "Oother" in aeff and ind in estage:
											estage.remove(ind)
										if "OName=" in aeff:
											meff = ["Name=", aeff[aeff.index("OName=") + 1]]
										else:
											meff = []
										emore = self.cont_times(meff, estage, self.cd)
										if len(emore) < aeff[aeff.index("OMore") + 1]:
											atimes = []
									if "Turn" in aeff:
										if "Topp" not in aeff and ind[-1] != self.gd["active"]:
											atimes = []
										elif "Topp" in aeff and ind[-1] == self.gd["active"]:
											atimes = []
									elif "Experience" in aeff and sum(
											[self.cd[lv].level for lv in self.pd[p]["Level"]]) < aeff[5]:
										atimes = []
									for anx in atimes:
										if aeff[1:] not in self.cd[anx].text_c:
											self.cd[anx].text_c.append(aeff[1:])
											self.cd[anx].update_ability()
								elif aeff[0] == -5:
									cm = self.pd[p]["Center"][1]
									if "other" in aeff and ind == cm:
										cm = ""
									if cm != "":
										if aeff[1:] not in self.cd[cm].text_c:
											self.cd[cm].text_c.append(aeff[1:])
											self.cd[cm].update_ability()
								elif aeff[0] == -6 and "Center" in card.pos_new:
									if ind[-1] == "1":
										op = "2"
									else:
										op = "1"
									opp = self.pd[op]["Center"][self.m[int(card.pos_new[-1])]]
									if opp != "" and aeff[1:] not in self.cd[opp].text_c:
										self.cd[opp].text_c.append(aeff[1:])
										self.cd[opp].update_ability()
								elif aeff[0] == "front" and "Assist" in aeff[3] and "Back" in card.pos_new:
									for finx in range(int(card.pos_new[-1]), int(card.pos_new[-1]) + 2):
										if self.pd[p]["Center"][finx] != "":
											front = self.cd[self.pd[p]["Center"][finx]]
											if aeff[1:] not in front.text_c:
												front.text_c.append(aeff[1:])
												front.update_ability()

							if neff:
								if ind not in neff[3]:
									neff[3] += f"_{ind}"
								if "opp" in neff:
									if player == "1":
										p = "2"
									elif player == "2":
										p = "1"
								else:
									p = player
								ncards = self.cont_cards(neff, ind)
								ntimes = self.cont_times(neff, ncards, self.cd)

								if neff[0] == 0:
									neff0 = True
									if "More" in neff[3]:
										if "lower" not in neff and len(ntimes) < neff[4]:
											neff0 = False
										elif "lower" in neff and len(ntimes) > neff[4]:
											neff0 = False
									elif "Stage" in neff[3]:
										if "Center" not in card.pos_new and "Back" not in card.pos_new:
											neff0 = False
									if neff0 and neff[1:] not in card.name_c:
										card.name_c.append(neff[1:])

				if ind != "1" and ind != "2":
					card.update_power()
					card.update_soul()
					card.update_level()
					card.update_trait()
					card.update_name()
					card.update_ability()
					if card.power_t <= 0:
						power_zero.append(ind)

			for field in ("Clock", "Memory", "Climax"):
				for ind in self.pd[player][field]:
					if ind in self.emptycards:
						continue
					card = self.cd[ind]
					if card.card == "Climax" and field != "Climax":
						continue
					for item in card.text_c:
						if item[0].startswith(cont_ability) and item[1] > -9 and item[1] != 0:
							effect = ab.cont(a=item[0])
							if len(effect) < 4:
								continue
							seff = []
							peff = []
							aeff = []

							if "soul" in effect and "power" in effect:
								enx = effect.index("power") + 1
								seff = effect[enx:]
								peff = effect[:enx]
							elif "ability" in effect:
								aeff = list(effect)
							elif "power" in effect:
								peff = list(effect)
							elif "soul" in effect:
								seff = list(effect)

							cards = [s for s in stage if s != ""]

							if peff:
								if ind not in peff[3]:
									peff[3] += f"_{ind}"
								if card.card == "Climax":
									peff[3] += f"_Climax"
								pcards = self.cont_cards(peff, ind)
								ptimes = self.cont_times(peff, pcards, self.cd)
								if peff[0] == -1:
									pp = True
									if "sMemory" in peff and "Memory" not in self.cd[ind].pos_new:
										pp = False

									if "Alarm" in peff[3]:
										if len(self.pd[ind[-1]]["Clock"]) <= 0:
											pp = False
										elif self.pd[ind[-1]]["Clock"][-1] != ind:
											pp = False
									elif "Turn" in peff[3]:
										if "Topp" in peff and self.gd["active"] in ind[-1]:
											pp = False
										elif "Topp" not in peff and self.gd["active"] not in ind[-1]:
											pp = False
									hid = list(peff[1:])
									hid[1] = -3
									for pinx in ptimes:
										if pp and peff[1:] not in self.cd[pinx].power_c:
											if hid in self.cd[pinx].power_c:
												continue
											self.cd[pinx].power_c.append(peff[1:])
											self.cd[pinx].update_power()
											if self.cd[pinx].power_t <= 0:
												power_zero.append(pnx)

							if seff:
								if ind not in seff[3]:
									seff[3] += f"_{ind}"
								if card.card == "Climax":
									seff[3] += f"_Climax"
								scards = self.cont_cards(seff, ind)
								stimes = self.cont_times(seff, scards, self.cd)
								if seff[0] == -1:
									for sinx in stimes:
										if seff[1:] not in self.cd[sinx].soul_c:
											self.cd[sinx].soul_c.append(seff[1:])
											self.cd[sinx].update_soul()
							if aeff:
								if ind not in aeff[3]:
									aeff[3] += f"_{ind}"
								acards = self.cont_cards(aeff, ind)
								atimes = self.cont_times(aeff, acards, self.cd)
								if aeff[0] == -1:
									aa = True
									if "Alarm" in aeff[3]:
										if len(self.pd[ind[-1]]["Clock"][-1]) <= 0:
											aa = False
										elif self.pd[ind[-1]]["Clock"][-1] == ind:
											if "plevel" in aeff and len(self.pd[ind[-1]]["Level"]) < aeff[
												aeff.index("plevel") + 1]:
												aa = False
										elif self.pd[ind[-1]]["Clock"][-1] != ind:
											aa = False

									for ainx in atimes:
										if aa and aeff[1:] not in self.cd[ainx].text_c:
											self.cd[ainx].text_c.append(aeff[1:])
											self.cd[ainx].update_ability()

			for pind in reversed(power_zero):
				self.gd["no_cont_check"] = True
				self.send_to_waiting(pind)
		if "1" in self.gd["active"]:
			self.act_ability_show()

	def check_cont_hand(self, player):
		for ind in self.pd[player]["Hand"]:
			if ind in self.emptycards:
				continue
			if self.cd[ind].card != "Character":
				continue
			card = self.cd[ind]

			to_remove_l = []
			for level in card.level_c:
				if level[1] < 0 and len(level) > 2:
					if "pHand" in level and level[2].split("_")[1] == ind:
						cx = []
						if "ClimaxWR" in level[2]:
							cx = [s for s in self.pd[ind[-1]]["Waiting"] if "Climax" in self.cd[s].card]
						elif "NameWR" in level[2]:
							cx = self.cont_times(level, self.pd[ind[-1]]["Waiting"], self.cd)
						elif "NameCL" in level[2]:
							cx = self.cont_times(level, self.pd[ind[-1]]["Clock"], self.cd)
						elif "Deck" in level[2]:
							cx = self.pd[player]["Library"]
						elif "More" in level[2]:
							cards = self.cont_cards(level, ind)
							cx = self.cont_times(level, cards, self.cd)

						if "lower" in level and len(cx) > level[3] and level not in to_remove_l:
							to_remove_l.append(level)
						elif "lower" not in level and len(cx) < level[3] and level not in to_remove_l:
							to_remove_l.append(level)

			# elif level not in to_remove_l:
			# 	to_remove_l.append(level)

			for iteml in to_remove_l:
				card.level_c.remove(iteml)

			for item in card.text_c:
				if item[0].startswith(cont_ability) and item[1] > -9 and item[1] != 0:
					effect = ab.cont(a=item[0])
					if len(effect) < 4:
						continue
					leff = []
					if "level" in effect:
						leff = list(effect)

					if leff:
						if ind not in leff[3]:
							leff[3] += f"_{ind}"
						if leff[0] == 0:
							if "pHand" in leff:
								cx = []
								if "ClimaxWR" in leff[3]:
									cx = [s for s in self.pd[ind[-1]]["Waiting"] if "Climax" in self.cd[s].card]
								elif "NameWR" in leff[3]:
									cx = self.cont_times(leff, self.pd[ind[-1]]["Waiting"], self.cd)
								elif "NameCL" in leff[3]:
									cx = self.cont_times(leff, self.pd[ind[-1]]["Clock"], self.cd)
								elif "Deck" in leff[3]:
									cx = self.pd[player]["Library"]
								elif "More" in leff[3]:
									cards = self.cont_cards(leff, ind)
									cx = self.cont_times(leff, cards, self.cd)

								if "lower" in leff and len(cx) <= leff[4] and leff[1:] not in card.level_c:
									card.level_c.append(leff[1:])
								elif "lower" not in leff and len(cx) >= leff[4] and leff[1:] not in card.level_c:
									card.level_c.append(leff[1:])
			card.update_level()

	def reveal(self, dt=0):
		ind = self.gd["ability_trigger"].split("_")[1]
		card = self.cd[self.pd[ind[-1]]["Library"][-1]]
		if card.back:
			self.mat[ind[-1]]["mat"].remove_widget(card)
			self.mat[ind[-1]]["mat"].add_widget(card)
			card.show_front()
			Clock.schedule_once(self.reveal, reveal_dt)

		elif not card.back:
			if "not" in self.gd["effect"]:
				traits = self.gd["effect"][self.gd["effect"].index("Trait") + 1].split("_")
				if all(trait not in card.trait_t for trait in traits):
					if "clock" in self.gd["effect"]:
						self.pd[ind[-1]]["Library"].remove(card.ind)
						self.pd[ind[-1]]["Clock"].append(card.ind)
						self.clock_size(ind[-1])
						self.update_field_label()

						if len(self.pd[self.gd["active"]]["Library"]) <= 0:
							self.gd["reshuffle_trigger"] = "reveal"
							Clock.schedule_once(self.refresh, move_dt_btw)
							return False
					else:
						if "if" in self.gd["effect"]:
							self.gd["done"] = True
						card.show_back()
					self.reveal_done()
				else:
					card.show_back()
					self.reveal_done()
			else:
				rr = False
				if "Name=" in self.gd["effect"]:
					if card.name in self.gd["effect"][self.gd["effect"].index("Name=") + 1]:
						rr = True
				elif "Name" in self.gd["effect"]:
					names = self.gd["effect"][self.gd["effect"].index("Name") + 1].split("_")
					if any(name in card.name for name in names):
						rr = True

				if "TraitEv" in self.gd["effect"]:
					traits = self.gd["effect"][self.gd["effect"].index("TraitEv") + 1].split("_")
					if any(tr in card.trait_t for tr in traits) or "Event" in card.card:
						rr = True
				elif "TraitL" in self.gd["effect"]:
					traits = self.gd["effect"][self.gd["effect"].index("TraitL") + 1].split("_")
					lvl = traits.pop(-1)
					if "<=p" in lvl:
						if any(tr in card.trait_t for tr in traits) and card.level_t <= len(
								self.pd[card.ind[-1]]["Level"]):
							rr = True
				elif "Trait" in self.gd["effect"]:
					traits = self.gd["effect"][self.gd["effect"].index("Trait") + 1].split("_")
					if any(tr in card.trait_t for tr in traits):
						rr = True
				elif "Level" in self.gd["effect"]:
					if "lower" in self.gd["effect"]:
						if card.level <= self.gd["effect"][self.gd["effect"].index("Level") + 1]:
							rr = True
					elif card.level >= self.gd["effect"][self.gd["effect"].index("Level") + 1]:
						rr = True
				elif "Climax" in self.gd["effect"]:
					if card.card == "Climax":
						rr = True

				if "do" in self.gd["ability_effect"]:
					if rr:
						self.gd["done"] = True

				card.show_back()
				self.reveal_done()

	def reveal_done(self, *args):
		if len(self.pd[self.gd["active"]]["Clock"]) >= 7:
			self.gd["level_up_trigger"] = "reveal"
			Clock.schedule_once(self.level_up, move_dt_btw)
			return False

		if self.gd["reshuffle"]:
			self.gd["reshuffle"] = False
			self.gd["damage_refresh"] += 1
			self.gd["damageref"] = True
			self.gd["reshuffle_trigger"] = "reveal"
			Clock.schedule_once(self.damage, move_dt_btw)
			return False
		if "do" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("do")

		if "reveal" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("reveal")

		self.ability_effect()

	def mill(self, dt=0):
		ind = self.gd["ability_trigger"].split("_")[1]
		if "opp" in self.gd["effect"] and ind[-1] == "1":
			player = "2"
		elif "opp" in self.gd["effect"] and ind[-1] == "2":
			player = "1"
		else:
			player = ind[-1]
		if self.gd["trev"] and player != self.gd["trev"]:
			player = self.gd["trev"]

		if self.gd["mill"] > 0:
			if len(self.pd[player]["Library"]) > 0:
				if "bottom" in self.gd["effect"]:
					temp = self.pd[player]["Library"].pop(0)
				else:
					temp = self.pd[player]["Library"].pop(-1)
				self.mat[player]["mat"].remove_widget(self.cd[temp])
				self.mat[player]["mat"].add_widget(self.cd[temp])

				if "Memory" in self.gd["effect"]:
					if "top-down" in self.gd["effect"]:
						self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Memory"], t="Memory",d=True)
					else:
						self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Memory"], t="Memory")
					self.pd[player]["Memory"].append(temp)
				else:
					self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Waiting"], t="Waiting")
					self.pd[player]["Waiting"].append(temp)
				self.gd["mill_check"].append(temp)
				self.update_field_label()
				self.gd["mill"] -= 1

			if self.gd["mill"] > 0 and "upto" in self.gd["effect"] and len(self.pd[player]["Library"]) <= 0:
				self.gd["mill"] = 0

			if len(self.pd[player]["Library"]) <= 0:
				self.gd["trev"] = player
				self.gd["reshuffle_trigger"] = "mill"
				Clock.schedule_once(self.refresh, move_dt_btw)
				return False
			Clock.schedule_once(self.mill, move_dt_btw)
		else:
			self.check_cont_ability()

			if self.gd["reshuffle"]:
				self.gd["reshuffle"] = False
				self.gd["damage_refresh"] += 1
				self.gd["damageref"] = True
				self.gd["reshuffle_trigger"] = "mill"
				Clock.schedule_once(self.damage, move_dt_btw)
				return False

			self.gd["trev"] = ""

			if "mill" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("mill")

			if self.gd["effect"][1] > 0 and "if" in self.gd["effect"]:
				self.gd["done"] = False
				if "x#" in self.gd["effect"]:
					txt = 0
					if "pwr" in self.gd["effect"]:
						if "ctrait" in self.gd["effect"]:
							trt = self.gd["effect"][self.gd["effect"].index("ctrait") + 1].split("_")
							txt = len([s for s in self.gd["mill_check"] if any(tr in self.cd[s].trait_t for tr in trt)])
					elif "Climax" in self.gd["effect"]:
						txt = len([s for s in self.gd["mill_check"] if self.cd[s].card == "Climax"])
					if txt > 0:
						self.gd["done"] = True
						self.gd["effect"][self.gd["effect"].index("do") + 1][1] = \
							self.gd["effect"][self.gd["effect"].index("do") + 1][1] * txt
						self.gd["do"][1] = list(self.gd["effect"][self.gd["effect"].index("do") + 1])
				elif "lvl" in self.gd["effect"]:
					lvl = self.gd["effect"][self.gd["effect"].index("lvl") + 1]
					if "lower" in self.gd["effect"]:
						if "Character" in self.gd["effect"]:
							nlv = len([s for s in self.gd["mill_check"] if
							           self.cd[s].level_t <= lvl and "Character" in self.cd[s].card])
						else:
							nlv = len([s for s in self.gd["mill_check"] if self.cd[s].level_t <= lvl])
					else:
						nlv = len([s for s in self.gd["mill_check"] if self.cd[s].level_t >= lvl])

					if "any" in self.gd["effect"] and nlv >= 1:
						if "extra" in self.gd["effect"]:
							for temp in self.gd["mill_check"]:
								self.gd["extra"].append(temp)
						self.gd["done"] = True
				elif "Trait" in self.gd["effect"]:
					trt = self.gd["effect"][self.gd["effect"].index("Trait") + 1].split("_")
					ntr = len([s for s in self.gd["mill_check"] if any(tr in self.cd[s].trait_t for tr in trt)])
					if "any" in self.gd["effect"] and ntr >= 1:
						self.gd["done"] = True
					elif "all" in self.gd["effect"] and ntr == self.gd["effect"][1]:
						self.gd["done"] = True
				elif "Climax" in self.gd["effect"]:
					cx = self.gd["effect"][self.gd["effect"].index("Climax") + 1]
					ncx = len([s for s in self.gd["mill_check"] if "Climax" in self.cd[s].card])
					if self.gd["effect"] and ncx >= cx:
						self.gd["done"] = True
				elif "extra" in self.gd["effect"]:
					for temp in self.gd["mill_check"]:
						self.gd["extra"].append(temp)
					self.gd["done"] = True

			if "do" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("do")

			self.ability_effect()

	def give(self, dt=0):
		idm = self.gd["ability_trigger"].split("_")[1]
		gt = 10
		if "if" in self.gd["effect"]:
			extra = len(self.gd["extra"])

		if self.gd["effect"][0] == 0:
			if idm[-1] == "1":
				self.gd["target"].append(idm)
			self.gd["effect"][0] = 1
		elif self.gd["effect"][0] == -12:
			if idm[-1] == "1":
				self.gd["target"].append(self.gd["attacking"][0])
			self.gd["effect"][0] = 1
		elif self.gd["effect"][0] == -16:
			self.gd["effect"][0] = len(self.gd["extra"])
			for r in range(len(self.gd["extra"])):
				ex = self.gd["extra"].pop(0)
				if idm[-1] == "1":
					self.gd["target"].append(ex)
		elif self.gd["effect"][0] == -21:
			self.gd["effect"][0] = 1
			if idm[-1] == "1":
				self.gd["target"].append("P")
		# elif self.gd["effect"][0] == -22:
		# 	self.gd["effect"][0] = 1
		# 	if idm[-1] == "1":
		# 		self.gd["target"].append("2")
		elif self.gd["effect"][0] == -1:
			# tar = [s for s in self.pd[idm[-1]]["Center"] + self.pd[idm[-1]]["Back"] if s != ""]
			if idm[-1] == "1":
				for ta in self.cont_times(self.gd["effect"], self.cont_cards(self.gd["effect"], idm), self.cd):
					self.gd["target"].append(ta)
			self.gd["effect"][0] = len(self.gd["target"])
		if "this" in self.gd["effect"] and self.gd["effect"][0] > 0:
			if idm[-1] == "1":
				self.gd["target"].append(idm)
			self.gd["effect"][0] += 1

		if len(self.gd["target"]) < self.gd["effect"][0]:
			for r in range(self.gd["effect"][0] - len(self.gd["target"])):
				self.gd["target"].append("")

		for r in range(self.gd["effect"][0]):
			ind = self.gd["target"].pop(0)
			if self.net["game"] and self.gd["ability_trigger"].split("_")[1][-1] == "1":  # @@
				self.net["act"][4].append(ind)
			if ind in self.emptycards:
				continue
			if ind == "P":
				ind = idm[-1]
			gg = 99
			if "give" in self.gd["effect"]:
				gg = self.gd["effect"].index("give")
				self.gd["effect"][gg] = f"{self.gd['effect'][gg]}_{idm}"
				# if self.gd["effect"][1].startswith(auto_ability):
				self.anx += 1
				self.gd["effect"].insert(gg + 1, self.anx)
				if "expass" in self.gd["effect"]:
					self.gd["effect"].insert(gg + 2, "pass")
					if len([n for n in self.gd["extra"] if n != ""]) < self.gd["effect"][
						self.gd["effect"].index("expass") + 1]:
						self.gd["effect"].insert(gg + 3, len([n for n in self.gd["extra"] if n != ""]))
					else:
						self.gd["effect"].insert(gg + 3, self.gd["effect"][self.gd["effect"].index("expass") + 1])

					if "ex_ID=" in self.gd["effect"]:
						self.gd["effect"].insert(gg + 4, "_".join(["ID="] + [n for n in self.gd["extra"] if n != ""]))
					elif "ex_Name=" in self.gd["effect"]:
						self.gd["effect"].insert(gg + 4, "_".join(
							["Name="] + [self.cd[n].name for n in self.gd["extra"] if n != ""]))
					if "extra" not in self.gd["effect"]:
						self.gd["extra"] = []
					gg += 5
				else:
					gg += 2
			if self.gd["effect"][1:gg] not in self.cd[ind].text_c:
				self.cd[ind].text_c.append(self.gd["effect"][1:gg])
				if ind != "1" and ind != "2":
					self.cd[ind].update_ability()

		if self.gd["end_stage"]:
			self.gd["end_stage"] = False

		if "give" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("give")

		if "do" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("do")
			if "if" in self.gd["effect"]:
				if isinstance(self.gd["effect"][self.gd["effect"].index("if") + 1], int) and extra >= self.gd["effect"][
					self.gd["effect"].index("if") + 1]:
					self.gd["done"] = True
			else:
				self.gd["done"] = True

		self.check_cont_ability()
		self.ability_effect()

	def draw_upto_btn(self, btn):
		self.sd["btn"]["draw_upto"].disabled = True
		self.sd["btn"]["end"].disabled = True
		self.gd["draw"] += 1
		self.gd["draw_upto"] -= 1
		if self.gd["draw_upto"] <= 0:
			self.sd["btn"]["ablt_info"].y = -Window.height * 2
			self.sd["btn"]["draw_upto"].y = -Window.height * 2
			self.sd["btn"]["end"].y = -Window.height * 2
			self.sd["btn"]["draw_upto"].disabled = False
			self.sd["btn"]["end"].disabled = False
		if self.net["game"]:
			self.net["act"][4].append("d")
		self.draw()

	def draw(self, dt=0):
		# if self.gd["trev"]:
		# 	player = self.gd["trev"]
		# else:
		if self.gd["rev"] and self.gd["rev_counter"] and "Counter" not in self.gd["phase"]:
			player = self.gd["active"]
		elif self.gd["rev"] or self.gd["rev_counter"]:
			player = self.gd["opp"]
		else:
			player = self.gd["active"]
		# self.update_marker()  # @@@@
		self.sd["menu"]["btn"].disabled = True
		if self.gd["draw"] > 0:
			if "drawupto" in self.gd["effect"] and "heal" in self.gd["effect"]:
				if len(self.pd[player]["Clock"]) > 0:
					temp = self.pd[player]["Clock"].pop()
					self.gd["drawed"].append(temp)
					self.mat[player]["mat"].remove_widget(self.cd[temp])
					self.mat[player]["mat"].add_widget(self.cd[temp])
					self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Waiting"], t="Waiting")
					self.pd[player]["Waiting"].append(temp)

			elif len(self.pd[player]["Library"]) > 0:
				temp = self.pd[player]["Library"].pop()
				self.gd["drawed"].append(temp)

				if "Reveal" in self.gd["effect"]:
					self.mat[player]["mat"].remove_widget(self.cd[temp])
					self.mat[player]["mat"].add_widget(self.cd[temp])
					library = self.mat[player]["field"]["Library"]
					self.cd[temp].setPos(library[0] - self.sd["padding"] / 4 - self.sd["card"][0],
					                     library[1] - self.sd["card"][1] / 3. * len(self.pd[player]["Res"]), t="Res")
					self.cd[temp].show_front()
					self.pd[player]["Res"].append(temp)
					if not self.gd["Res1_move"]:
						self.field_btn[f"Res1{player}"].x += Window.width * 2
						self.gd["Res1_move"] = True
				elif "Stock" in self.gd["effect"]:
					self.pd[player]["Stock"].append(temp)
					self.stock_size(player)
				else:
					self.pd[player]["Hand"].append(temp)
					self.hand_size(player)

			self.gd["draw"] -= 1
			self.update_field_label()

			if len(self.pd[player]["Library"]) <= 0:
				self.gd["reshuffle_trigger"] = "draw"
				Clock.schedule_once(self.refresh, move_dt_btw)
			else:
				Clock.schedule_once(self.draw, move_dt_btw)
		else:
			self.check_cont_ability()

			if self.gd["reshuffle"]:
				self.gd["reshuffle"] = False
				self.gd["damage_refresh"] += 1
				self.gd["damageref"] = True
				self.gd["reshuffle_trigger"] = "draw"
				Clock.schedule_once(self.damage, move_dt_btw)
				return False

			if self.gd["active"] == "1" and self.gd["phase"] in ("", "Main", "Climax", "Mulligan", "Janken"):
				self.hand_btn_show(False)

			if self.gd["draw_upto"] <= 0:
				if "drawupto" in self.gd["ability_effect"]:
					self.gd["ability_effect"].remove("drawupto")

				if "draw" in self.gd["ability_effect"]:
					self.gd["ability_effect"].remove("draw")

				if "Reveal" in self.gd["effect"] and "if" in self.gd["effect"]:
					if len(self.pd[player]["Res"]) >= self.gd["effect"][self.gd["effect"].index("if") + 1]:
						self.gd["done"] = True
				elif "if" in self.gd["effect"]:
					if len(self.gd["drawed"]) >= self.gd["effect"][self.gd["effect"].index("if") + 1]:
						self.gd["done"] = True
					self.gd["drawed"] = []
				elif "do" in self.gd["effect"] and self.gd["do"][0] > 0:
					self.gd["done"] = True
				if "do" in self.gd["ability_effect"]:
					self.gd["ability_effect"].remove("do")

				# if self.gd["brainstorm_c"][0] > 1:
				# 	self.gd["brainstorm_c"][0] -= 1
				# 	self.gd["done"] = True
				self.gd["rev"] = False
				if "AUTO" in self.gd["ability_trigger"] or "ACT" in self.gd["ability_trigger"] or "Event" in self.gd[
					"ability_trigger"]:
					Clock.schedule_once(self.ability_effect)
				elif self.gd["phase"] == "Main":
					Clock.schedule_once(self.ability_effect, move_dt_btw)
				elif self.gd["phase"] == "Draw":
					self.pd[self.gd["active"]]["done"]["Draw"] = True
					self.gd["phase"] = "Clock"
					if self.gd["active"] == "1":
						Clock.schedule_once(self.clock_phase)
					else:
						Clock.schedule_once(self.clock_phase, phase_dt)
				elif self.gd["phase"] == "Clock":
					self.pd[self.gd["active"]]["done"]["Clock"] = True
					self.gd["phase"] = "Main"
					Clock.schedule_once(self.main_phase)
				elif self.gd["phase"] == "Mulligan":
					self.pd[player]["done"]["Mulligan"] = True
					if all(self.pd[p]["done"]["Mulligan"] for p in list(self.pd.keys())):
						self.gd["turn"] += 1
						self.gd["rev"] = False
						self.gd["phase"] = "Stand Up"
						Clock.schedule_once(self.stand_phase, phase_dt)
					else:
						if self.net["game"] and not self.gd["mulligan"][1]:
							if self.gd["show_wait_popup"]:
								Clock.schedule_once(partial(self.popup_text, "waiting"))
							self.mconnect("mulligan")
						elif self.pd[self.gd["starting_player"]]["done"]["Mulligan"]:
							self.gd["rev"] = True
							Clock.schedule_once(self.mulligan_start)  # , phase_dt)
				elif self.gd["turn"] == 0:
					if not self.gd["draw_both"][1]:
						self.gd["draw_both"][1] = True
					elif not self.gd["draw_both"][2]:
						self.gd["draw_both"][2] = True
					Clock.schedule_once(self.draw_both, move_dt_btw)
			else:
				self.sd["btn"]["draw_upto"].disabled = False
				self.sd["btn"]["end"].disabled = False

	def add_marker(self, ind, var, face):
		if ind not in self.pd[ind[-1]]["marker"]:
			self.pd[ind[-1]]["marker"][ind] = []
		if var not in self.pd[ind[-1]]["marker"][ind]:
			self.pd[ind[-1]]["marker"][ind].append([var, face])
		for text in self.cd[ind].text_c:
			if text[0].startswith(cont_ability) and text[1] != 0 and text[1] > -9:
				ef = ab.cont(text[0])
				if ef and "astock" in ef:
					self.gd["astock"][ind[-1]].append((ind, var))
					break

	def update_marker(self):
		for player in self.pd:
			space = self.sd["card"][0] * 0.1
			for ind in self.pd[player]["marker"]:
				card = self.cd[ind]
				for inx in range(len(self.pd[player]["marker"][ind])):
					inm = self.pd[player]["marker"][ind][inx]
					marker = self.cd[inm[0]]
					self.mat[player]["mat"].remove_widget(marker)
					self.mat[player]["mat"].add_widget(marker)
					xpos = self.mat[player]["field"][card.pos_new][0] + space * (
							len(self.pd[player]["marker"][ind]) - inx)
					ypos = self.mat[player]["field"][card.pos_new][1] - space * (
							len(self.pd[player]["marker"][ind]) - inx)
					marker.setPos(xpos, ypos, t="Marker")
					if not inm[1]:
						marker.show_back()
					else:
						marker.show_front()
				self.mat[player]["mat"].remove_widget(card)
				self.mat[player]["mat"].add_widget(card)
				card.update_marker(len(self.pd[player]["marker"][ind]))

	def remove_marker(self, ind="", q=0, s=None):
		if ind in self.pd[ind[-1]]["marker"]:
			remove = []
			if q <= 0:
				q = len(self.pd[ind[-1]]["marker"][ind])

			for inx in range(1, q + 1):
				inm = self.pd[ind[-1]]["marker"][ind][-inx]
				remove.append(inm)
				self.mat[ind[-1]]["mat"].remove_widget(self.cd[inm[0]])
				self.mat[ind[-1]]["mat"].add_widget(self.cd[inm[0]])

				self.cd[inm[0]].setPos(field=self.mat[ind[-1]]["field"]["Waiting"], t="Waiting")
				self.pd[ind[-1]]["Waiting"].append(inm[0])
			for item in remove:
				self.pd[ind[-1]]["marker"][ind].remove(item)
				if s is None:
					sx = ["as", "es"]
				else:
					sx = [s]
				for m in sx:
					if (ind, item[0]) in self.gd[f"{m}tock"][ind[-1]]:
						self.gd[f"{m}tock"][ind[-1]].remove((ind, item[0]))
			self.cd[ind].update_marker(len(self.pd[ind[-1]]["marker"][ind]))
			if len(self.pd[ind[-1]]["marker"][ind]) <= 0:
				del self.pd[ind[-1]]["marker"][ind]

	def marker(self, *args):
		# if self.gd["rev"]:
		# 	player = self.gd["opp"]
		# else:
		# 	player = self.gd["active"]
		#
		# stage = self.pd[player]["Center"] + self.pd[player]["Back"]
		if "face-up" in self.gd["effect"]:
			face = True
		else:
			face = False

		card = self.gd["ability_trigger"].split("_")[1]

		if "Return" in self.gd["effect"]:
			if len(self.pd[card[-1]]["marker"][card]) >= self.gd["effect"][0]:
				for inx in range(1, self.gd["effect"][0] + 1):
					inm = self.pd[card[-1]]["marker"][card].pop()

					if "Hand" in self.gd["effect"]:
						self.pd[card[-1]]["Hand"].append(inm[0])
						self.hand_size(card[-1])

				self.update_marker()
				self.check_cont_ability()
			self.gd["effect"].remove("Return")
			if "Hand" in self.gd["effect"]:
				self.gd["effect"].remove("Hand")
			self.marker()
		elif "top" in self.gd["effect"]:
			if "Stock" in self.gd["effect"]:
				if len(self.pd[card[-1]]["Stock"]) > 0:
					temp = self.pd[card[-1]]["Stock"].pop()
					self.cd[temp].stand()
					self.add_marker(card, temp, face)
					self.update_marker()
					self.update_field_label()
					self.check_cont_ability()
				self.gd["effect"].remove("top")
				self.gd["effect"].remove("Stock")
				self.marker()
			else:
				if len(self.pd[card[-1]]["Library"]) > 0:
					temp = self.pd[card[-1]]["Library"].pop()
					self.add_marker(card, temp, face)
					self.update_marker()
					self.update_field_label()
					self.check_cont_ability()
				self.gd["effect"].remove("top")

				if len(self.pd[card[-1]]["Library"]) <= 0:
					self.gd["reshuffle_trigger"] = "marker"
					Clock.schedule_once(self.refresh)
					return False
				else:
					self.marker()
		elif "Hand" in self.gd["effect"]:
			if card[-1] == "1" and self.gd["p_c"] != "" and not self.gd["target"]:
				self.sd["popup"]["popup"].dismiss()
				if len(self.gd["chosen"]) < self.gd["effect"][0]:
					for r in range(self.gd["effect"][0] - len(self.gd["chosen"])):
						self.gd["chosen"].append("")
				self.gd["target"] = list(self.gd["chosen"])
				self.gd["choose"] = False
				self.gd["chosen"] = []
				self.marker()
			elif self.gd["target"]:
				idm = []
				for r in range(self.gd["effect"][0]):
					ind = self.gd["target"].pop(0)
					if self.net["game"] and self.gd["p_owner"] == "1":  # @@
						self.net["act"][4].append(ind)
					if ind in self.emptycards:
						continue
					self.pd[ind[-1]]["Hand"].remove(ind)
					self.add_marker(card, ind, face)
					if card[-1] == "2":
						idm.append(ind)
				self.update_marker()
				self.hand_size(card[-1])
				self.check_cont_ability()
				self.gd["effect"].remove("Hand")
				if card[-1] == "2" and "show" in self.gd["effect"]:
					self.popup_multi_info(cards=idm, owner=card[-1], t="Marker")
				else:
					self.marker()
			else:
				self.gd["search_type"] = self.gd["effect"][2]
				self.gd["discard"] = self.gd["effect"][0]
				self.gd["p_c"] = ""
				Clock.schedule_once(self.discard)
				return False
		elif "Waiting" in self.gd["effect"]:
			if card[-1] == "1" and self.gd["p_c"] != "" and not self.gd["target"]:
				self.sd["popup"]["popup"].dismiss()
				if len(self.gd["chosen"]) < self.gd["effect"][0]:
					for r in range(self.gd["effect"][0] - len(self.gd["chosen"])):
						self.gd["chosen"].append("")
				self.gd["target"] = list(self.gd["chosen"])
				self.gd["choose"] = False
				self.gd["chosen"] = []
				self.marker()
			elif self.gd["target"]:
				for r in range(self.gd["effect"][0]):
					ind = self.gd["target"].pop(0)
					if self.net["game"] and self.gd["p_owner"] == "1":  # @@
						self.net["act"][4].append(ind)
					if ind in self.emptycards:
						continue
					self.pd[self.gd["p_owner"]]["Waiting"].remove(ind)
					self.add_marker(card, ind, face)
				self.update_marker()
				self.update_field_label()
				self.check_cont_ability()
				self.gd["effect"].remove("Waiting")
				self.marker()
			else:
				if "none" in self.gd["effect"] and (
						card in self.pd[card[-1]]["marker"] and len(self.pd[card[-1]]["marker"][card]) > 0):
					self.gd["effect"].remove("Waiting")
					Clock.schedule_once(self.marker)
					return False

				self.gd["search_type"] = self.gd["effect"][2]
				self.gd["salvage"] = self.gd["effect"][0]
				self.gd["p_c"] = ""
				Clock.schedule_once(self.salvage)
				return False
		else:
			if self.gd["reshuffle"]:
				self.gd["reshuffle"] = False
				self.gd["damage_refresh"] += 1
				self.gd["damageref"] = True
				self.gd["reshuffle_trigger"] = "marker"
				Clock.schedule_once(self.damage, move_dt_btw)
				return False

			self.popup_clr()

			if self.gd["rev"]:
				self.gd["rev"] = False

			if self.gd["notarget"]:
				self.gd["notarget"] = False

			if "marker" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("marker")
			self.check_cont_ability()
			Clock.schedule_once(self.ability_effect)
			return False

	def stock(self, dt=0):
		if self.gd["rev"]:
			player = self.gd["opp"]
		else:
			player = self.gd["active"]

		if self.gd["stock"] > 0:
			if len(self.pd[player]["Library"]) > 0:
				temp = self.pd[player]["Library"].pop()
				self.pd[player]["Stock"].append(temp)
				self.stock_size(player)
				self.update_field_label()
				self.gd["stock"] -= 1

			if len(self.pd[player]["Library"]) <= 0:
				self.gd["reshuffle_trigger"] = "stock"
				Clock.schedule_once(self.refresh)
				return False
			Clock.schedule_once(self.stock, move_dt_btw)
		else:
			if self.gd["reshuffle"]:
				self.gd["reshuffle"] = False
				self.gd["damage_refresh"] += 1
				self.gd["damageref"] = True
				self.gd["reshuffle_trigger"] = "stock"
				Clock.schedule_once(self.damage)
				return False

			if self.gd["rev"]:
				self.gd["rev"] = False
			self.check_cont_ability()
			if "stock" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("stock")

			# if "stock" in self.gd["effect"]:
			# 	self.gd["effect"] = self.gd["effect"][2:].
			self.do_check()
			self.ability_effect()

	def change_label(self):
		self.gd["inx"] = 0
		if any(step in self.gd["phase"] for step in steps):
			xpos = Window.width / float(len(steps))
			self.rect1.size = (xpos, (self.sd["padding"] + self.sd["card"][1] / 6) * 2)
			for label in phases:
				self.sd["label"][label].center_x = -Window.width

			for label in steps:
				self.sd["label"][label].center_x = xpos / 2. + xpos * self.gd["inx"]
				if label == self.gd["phase"]:
					self.change_active_phase(label)
					self.sd["label"][label].color = (1., 1., 1., 1.)
					self.rect1.pos = (
						xpos * self.gd["inx"], Window.height / 2 - self.sd["padding"] - self.sd["card"][1] / 6)
				else:
					self.sd["label"][label].color = (.5, .5, .5, 1.)
				self.gd["inx"] += 1
		else:
			xpos = Window.width / float(len(phases))
			self.rect1.size = (xpos, (self.sd["padding"] + self.sd["card"][1] / 6) * 2)
			for label in steps:
				self.sd["label"][label].center_x = -Window.width
			for label in phases:
				self.sd["label"][label].center_x = xpos / 2. + xpos * self.gd["inx"]

				if label == self.gd["phase"]:
					self.change_active_phase(label)
					self.sd["label"][label].color = (1., 1., 1., 1.)
					self.rect1.pos = (
						xpos * self.gd["inx"], Window.height / 2 - self.sd["padding"] - self.sd["card"][1] / 6)
				else:
					self.sd["label"][label].color = (.5, .5, .5, 1.)
				self.gd["inx"] += 1

		if self.gd["phase"] != "":
			if not self.pd[self.gd["active"]]["phase"][self.gd["phase"]]:
				self.pd[self.gd["active"]]["phase"][self.gd["phase"]] = True
				self.gd["pp"] = -1
				self.gd["stage-1"] = list(self.pd[self.gd["active"]]["Center"] + self.pd[self.gd["active"]]["Back"])
			else:
				if self.gd["pp"] < 0:
					self.gd["pp"] = 0  # @@
				elif self.gd["pp"] == 0:
					self.gd["pp"] = 1
				elif self.gd["pp"] >= 1:
					self.gd["pp"] += 1

	def battle_step(self, *args):
		self.change_label()
		if self.gd["attacking"][0] and self.gd["attacking"][1] == "f" and self.gd["attack_t"][self.gd["attacking"][1]][
			self.gd["attacking"][2]] and \
				self.gd["attacking"][4] != "":
			# compare power
			reverse = [True, True]
			card = self.cd[self.gd["attacking"][0]]
			opp_ind = ""
			if self.gd["attacking"][4] == "C":
				opp_ind = self.pd[self.gd["opp"]]["Center"][self.gd["attacking"][3]]
			elif self.gd["attacking"][4] == "B":
				opp_ind = self.pd[self.gd["opp"]]["Back"][self.gd["attacking"][3]]

			revlist = []
			if opp_ind != "":
				card_opp = self.cd[opp_ind]
				for text in card.text_c:
					effect = ab.cont(text[0])
					if "no_reverse" in effect:
						if "cost" in effect and card_opp.cost <= effect[effect.index("cost") + 1]:
							reverse[0] = False
						elif "event" in effect:
							reverse[0] = False

				for text in card_opp.text_c:
					effect = ab.cont(text[0])
					if "no_reverse" in effect:
						if "cost" in effect and card.cost <= effect[effect.index("cost") + 1]:
							reverse[1] = False
						elif "event" in effect:
							reverse[0] = False

				if card.power_t > card_opp.power_t:
					if reverse[1]:
						if card_opp.status != "Reverse":
							card_opp.reverse()
							revlist.append(card_opp.ind)
							self.check_bodyguard(self.gd["phase"])
				elif card.power_t < card_opp.power_t:
					if reverse[0]:
						if card.status != "Reverse":
							card.reverse()
							revlist.append(card.ind)
				elif card.power_t == card_opp.power_t:
					if reverse[0]:
						if card.status != "Reverse":
							card.reverse()
							revlist.append(card.ind)
					if reverse[1]:
						if card_opp.status != "Reverse":
							card_opp.reverse()
							self.check_bodyguard(self.gd["phase"])
							revlist.append(card_opp.ind)
			self.pd[self.gd["active"]]["done"]["Battle"] = True
			self.check_auto_ability(rev=revlist, batt=True)
		else:
			self.pd[self.gd["active"]]["done"]["Battle"] = True
			Clock.schedule_once(self.attack_phase_done)

	def check_atk_type(self, inx=""):
		if inx:
			lst = [inx]
		else:
			lst = self.pd[self.gd["active"]]["Center"]

		for ind in lst:
			for text in self.cd[ind].text_c:
				if text[0].startswith(cont_ability) and text[1] > -9 and text[1] != 0:
					effect = ab.cont(text[0])
					aa = True
					if "no_attack" in effect:
						if "Clock" in effect:
							if "lower" in effect and len(self.pd[ind[-1]]["Clock"]) > effect[effect.index("Clock") + 1]:
								aa = False
							elif "lower" not in effect and len(self.pd[ind[-1]]["Clock"]) < effect[
								effect.index("Clock") + 1]:
								aa = False
						elif "Stage" in effect:
							if "Back" in effect:
								stage = len([s for s in self.pd[ind[-1]]["Back"] if s != ""])
							else:
								stage = len(
										[s for s in self.pd[ind[-1]]["Center"] + self.pd[ind[-1]]["Back"] if s != ""])

							if "lower" in effect and stage > effect[effect.index("Stage") + 1]:
								aa = False
							elif "lower" not in effect and stage < effect[effect.index("Stage") + 1]:
								aa = False
						elif "Olevel" in effect:
							op = self.pd[self.gd["opp"]]["Center"][self.m[self.pd[ind[-1]["Center"].index(ind)]]]
							if "lower" not in effect and self.cd[ind].level_t >= self.cd[op].level_t:
								aa = False
							elif "lower" in effect and self.cd[ind].level_t <= self.cd[op].level_t:
								aa = False
						if aa:
							self.gd["attack_t"]["s"][int(self.cd[ind].pos_new[-1])] = False
							self.gd["attack_t"]["f"][int(self.cd[ind].pos_new[-1])] = False
							self.gd["attack_t"]["d"][int(self.cd[ind].pos_new[-1])] = False
					else:
						if "olevel" in effect:
							if ind[-1] == "1":
								op = "2"
							else:
								op = "1"
							opp = self.pd[op]["Center"][self.m[int(self.cd[ind].pos_new[-1])]]
							if opp != "":
								if "higher" in effect and self.cd[opp].level_t <= self.cd[ind].level_t:
									aa = False
						if aa and "no_side" in effect:
							self.gd["attack_t"]["s"][int(self.cd[ind].pos_new[-1])] = False
						if aa and "no_front" in effect:
							self.gd["attack_t"]["f"][int(self.cd[ind].pos_new[-1])] = False
						if aa and "no_direct" in effect:
							self.gd["attack_t"]["d"][int(self.cd[ind].pos_new[-1])] = False

	def attack_phase_done(self, *args):
		self.gd["popup_attack"] -= 1
		self.gd["attacking"] = ["", "", 0, 0, ""]
		self.check_cont_ability()
		if self.gd["check_atk"]:
			self.gd["attack"] = len([s for s in self.pd[self.gd["active"]]["Center"] if self.cd[s].status == "Stand"])
		else:
			self.gd["attack"] -= 1
		Clock.schedule_once(self.attack_phase_end)

	def attack_phase_end(self, *args):
		if self.gd["turn"] == 1 and self.gd["d_atk"][0] > 0 and len(self.gd["d_atk"][1]) >= self.gd["d_atk"][0]:
			self.gd["attack"] = 0
			self.gd["d_atk"] = [0, []]
			Clock.schedule_once(self.attack_phase_end)
		elif self.gd["attack"] > 0:
			self.pd[self.gd["active"]]["phase"]["Attack"] = False
			self.reset_auto()
			for step in ("Trigger", "Counter", "Damage", "Battle"):
				self.pd[self.gd["active"]]["done"][step] = False
				self.pd[self.gd["active"]]["phase"][step] = False

			self.gd["phase"] = "Attack"

			if self.net["game"] and self.gd["active"] == "2":
				if self.gd["show_wait_popup"]:
					Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
				self.mconnect("phase")
			elif self.gd["com"] and self.gd["active"] == "2":
				Clock.schedule_once(self.opp_attack, move_dt_btw)
			else:
				Clock.schedule_once(self.attack_phase_main, phase_dt / 2)
		else:
			self.hand_btn_show(False)
			self.hide_attack_btn()
			for t in self.gd["attack_t"]:
				for i in self.gd["attack_t"][t]:
					self.gd["attack_t"][t][i] = True
			self.gd["attack"] = 0
			self.gd["popup_attack"] = 1
			self.pd[self.gd["active"]]["done"]["Attack"] = True
			self.gd["bodyguard"] = False
			if self.gd["nomay"]:
				self.gd["nomay"] = False
			self.gd["phase"] = "Encore"
			self.gd["check_ctr"] = False
			if "Attack" in self.gd["skip"]:
				Clock.schedule_once(self.encore_phase)  # , phase_dt)
			else:
				Clock.schedule_once(self.encore_phase, phase_dt)

	def damage_step(self, *args):
		self.change_label()
		card = self.cd[self.gd["attacking"][0]]
		if self.gd["attack_t"][self.gd["attacking"][1]][self.gd["attacking"][2]] and card.soul_t > 0:
			self.gd["damage"] = card.soul_t
			self.gd["rev"] = True
			self.gd["dmg"] = int(self.gd["damage"])

		Clock.schedule_once(self.damage, move_dt_btw)

	def rested_card_update(self):
		if len(self.pd[self.gd["active"]]["Res"]) < 1 and not self.event_move:
			c = (0, 1, 2)
			b = (0, 1)
			# if self.gd["active"] == "2":
			# 	c = sorted(c, reverse=True)
			# 	b = sorted(b, reverse=True)
			for inx in c:
				if self.pd[self.gd["active"]]["Center"][inx] != "":
					card = self.cd[self.pd[self.gd["active"]]["Center"][inx]]
					self.mat[self.gd["active"]]["mat"].remove_widget(card)
					self.mat[self.gd["active"]]["mat"].add_widget(card)

			for inx in b:
				if self.pd[self.gd["active"]]["Back"][inx] != "":
					card = self.cd[self.pd[self.gd["active"]]["Back"][inx]]
					self.mat[self.gd["active"]]["mat"].remove_widget(card)
					self.mat[self.gd["active"]]["mat"].add_widget(card)
		elif self.event_move:
			self.event_move = False

	def trigger_step(self, *args):
		self.change_label()
		self.sd["btn"]["end"].y = -Window.height

		self.rested_card_update()

		self.gd["trigger"] = 1
		self.gd["mtrigger"] -= 1
		Clock.schedule_once(self.trigger, move_dt_btw)

	def trigger_effect(self, *args):
		if len(self.gd["trigger_icon"]) > 0:
			trigger = self.gd["trigger_icon"].pop(0)
			if not trigger:
				self.trigger_effect()
			else:
				self.gd["effect"] = ab.trigger(a=trigger)
				ind = self.pd[self.gd['attacking'][0][-1]]['Res'][0]
				# self.gd["ability_trigger"] = f"AUTO_{ind}_{trigger.lower()}_Trigger"
				# self.gd["payed"] = True
				self.gd["ability"] = self.gd["effect"][self.gd["effect"].index("text") + 1]
				if self.gd["effect"][0] != -12:
					self.gd["stack"][ind[-1]].append(
							[ind, self.gd["effect"], self.gd["ability"], "Trigger", 1, self.gd["pp"], "TriggerIcon"])
					if self.net["game"] and self.gd['attacking'][0][-1] == "1":
						self.net["act"] = ["a", ind, 0, [], [], 0]
						self.net["send"] = False
					Clock.schedule_once(self.stack_ability)
				else:
					self.gd["ability_trigger"] = f"AUTO_{ind}_{trigger.lower()}_Trigger"
					self.gd["payed"] = True
					self.ability_event()
		# if self.net["game"] and self.gd['attacking'][0][-1] == "1" and self.gd["effect"][0] != -12:
		# 	self.net["act"] = ["a", ind, 0, [], [], 0]
		# 	self.net["send"] = False

		# Clock.schedule_once(self.stack_ability)
		# if self.net["game"] and self.gd['attacking'][0][-1] == "2" and self.gd["effect"][0] != -12:
		# 	if self.gd["show_wait_popup"]:
		# 		Clock.schedule_once(partial(self.popup_text, "waiting"))
		# 	self.mconnect("phase")
		# else:
		# 	self.ability_event()
		else:
			# if self.net["game"] and self.gd["active"] == "1" and not self.net["send"]:
			# 	print("trigger_effect endpart1")
			# 	# self.net["var1"] = "trigger"
			# 	# self.net["var"] = self.net["act"]
			# 	# self.mconnect("act")
			# 	# return
			# 	Clock.schedule_once(self.stack_ability)
			# else:
			# 	print("trigger_effect endpart2")
			# 	Clock.schedule_once(self.trigger_done, move_dt_btw)
			Clock.schedule_once(self.trigger_done, move_dt_btw)

	def trigger_done(self, dt=0):
		self.change_label()
		if self.gd["trigger"] > 0:
			if len(self.pd[self.gd["active"]]["Res"]) > 0:
				temp = self.pd[self.gd["active"]]["Res"].pop(0)
				self.pd[self.gd["active"]]["Stock"].append(temp)
				self.update_field_label()
				self.stock_size(self.gd["active"])
				self.gd["trigger_card"] = ""
			self.gd["trigger"] -= 1

			if self.gd["mtrigger"] > 0:
				self.gd["mtrigger"] -= 1
				Clock.schedule_once(self.trigger, move_dt_btw)
			elif self.gd["trigger"] >= 0:
				Clock.schedule_once(self.trigger_done)
		else:
			if self.gd["reshuffle"]:
				self.gd["reshuffle"] = False
				self.gd["damage_refresh"] += 1
				self.gd["damageref"] = True
				self.gd["reshuffle_trigger"] = "trigger"
				Clock.schedule_once(self.damage, move_dt_btw)
				return False
			self.check_auto_ability(rev=self.gd["triggers"])

	def trigger_step_done(self, *args):
		self.gd["mtrigger"] = 1
		self.gd["triggers"] = []
		if self.gd["attacking"][1] == "f":
			self.pd[self.gd["active"]]["done"]["Trigger"] = True
			self.gd["phase"] = "Counter"
			Clock.schedule_once(self.counter_step, phase_dt)
		else:
			self.pd[self.gd["active"]]["done"]["Trigger"] = True
			self.pd[self.gd["active"]]["phase"]["Counter"] = True
			self.pd[self.gd["active"]]["done"]["Counter"] = True
			self.gd["phase"] = "Damage"
			Clock.schedule_once(self.damage_step, phase_dt)

	def trigger(self, *args):
		self.gd["inx"] = 0
		if self.gd["trigger"] > 0:
			if len(self.pd[self.gd["active"]]["Library"]) > 0:
				temp = self.pd[self.gd["active"]]["Library"].pop()
				card = self.cd[temp]
				library = self.mat[self.gd["active"]]["field"]["Library"]
				self.pd[self.gd["active"]]["Res"].append(temp)
				self.update_field_label()

				self.mat[self.gd["active"]]["mat"].remove_widget(card)
				self.mat[self.gd["active"]]["mat"].add_widget(card)

				card.show_front()
				card.setPos(library[0] - self.sd["padding"] - self.sd["card"][0], library[1], t="Res")

				self.gd["trigger_icon"] = list(card.trigger)
				self.gd["triggers"].append(temp)
				self.gd["trigger_card"] = temp
				self.gd["trigger"] -= 1

			if len(self.pd[self.gd["active"]]["Library"]) <= 0:
				self.gd["reshuffle_trigger"] = "trigger"
				Clock.schedule_once(self.refresh, move_dt_btw)
			elif self.gd["trigger"] >= 0:
				Clock.schedule_once(self.trigger, move_dt_btw)
		else:
			self.gd["trigger"] = 1
			Clock.schedule_once(self.trigger_effect, move_dt_btw)

	def counter_step(self, *args):
		self.dismiss_all()
		self.change_label()
		self.clear_ability()
		if self.gd["pp"] < 0:
			Clock.schedule_once(self.check_auto_ability)
			return False
		else:
			self.counter_step_main()

	def counter_step_main(self, *args):
		self.change_label()
		self.gd["counter"] = []
		cards = [self.gd["attacking"][0]]
		if self.gd["attacking"][0][-1] == "1":
			opp = "2"
		elif self.gd["attacking"][0][-1] == "2":
			opp = "1"
		if "C" in self.gd["attacking"][4]:
			cards.append(self.pd[opp]["Center"][self.gd["attacking"][3]])
		elif "B" in self.gd["attacking"][4]:
			cards.append(self.pd[opp]["Back"][self.gd["attacking"][3]])

		if self.gd["backup"][self.gd["opp"]] or self.gd["event"][self.gd["opp"]]:
			for c in cards:
				if c != "":
					for item in self.cd[c].text_c:
						if item[0].startswith(cont_ability) and item[1] != 0 and item[1] > -9:
							eff = ab.cont(item[0])
							if eff:
								if "opp" in eff and c[-1] == "1":
									pl = "2"
								elif "opp" and c[-1] == "2":
									pl = "1"
								else:
									pl = c[-1]

								if "no_backup" in eff:
									if "both" in eff:
										self.gd["counter_icon"]["1"][0] = False
										self.gd["counter_icon"]["2"][0] = False
									else:
										self.gd["counter_icon"][pl][0] = False
								if "no_event" in eff:
									if "both" in eff:
										self.gd["counter_icon"]["1"][1] = False
										self.gd["counter_icon"]["2"][1] = False
									else:
										self.gd["counter_icon"][pl][1] = False

		if self.gd["active"] == "2":
			for s in self.pd[self.gd["opp"]]["Hand"]:
				card = self.cd[s]
				if card.icon == "Counter":
					if card.card == "Character" and self.gd["backup"][self.gd["opp"]] and \
							self.gd["counter_icon"][self.gd["opp"]][0]:
						for text in card.text_c:
							if text[0].startswith(act_aility) and text[1] != 0 and text[1] > -9:
								act = ab.act(a=text[0])
								if act and ab.req(a=text[0],
								                  x=len(self.pd[opp]["Stock"])) and "backup" in act and len(
										self.pd[opp]["Level"]) >= act[act.index("backup") + 1]:
									if s not in self.gd["counter"]:
										self.gd["counter"].append(s)
					elif card.card == "Event" and "[counter]" in card.text_c[0][0].lower() and self.gd["event"][
						self.gd["opp"]] and \
							self.gd["counter_icon"][opp][1] and len(
							self.pd[opp]["Level"]) >= card.level and card.mcolour in \
							self.pd[opp]["colour"] and len(self.pd[opp]["Stock"]) >= card.cost:

						if self.check_event(s) and s not in self.gd["counter"]:
							self.gd["counter"].append(s)

			if self.net["game"]:
				self.net["send"] = False

			if len(self.gd["counter"]) > 0:
				self.gd["confirm_trigger"] = "Counter"
				self.gd["confirm_var"] = {"icon": "counter", "c": "counter", "ind": self.gd["counter"][0]}
				Clock.schedule_once(self.confirm_popup, popup_dt)
			else:
				Clock.schedule_once(partial(self.popup_text, self.gd["phase"]), popup_dt)
			return False
		elif self.net["game"] and self.gd["active"] == "1":
			if self.gd["show_wait_popup"]:
				Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
			self.mconnect("counter")
		elif self.gd["com"] and self.gd["active"] == "1":
			counter = self.ai.counter_step(self.pd, self.cd, self.gd, str(self.gd["attacking"][0]),
			                               str(self.pd[self.gd["opp"]]["Center"][self.gd["attacking"][3]]))
			if counter == "pass":
				Clock.schedule_once(self.counter_step_done, ability_dt)
			else:
				self.gd["chosen"].append(counter[0])
				self.gd["p_owner"] = self.gd["opp"]
				self.gd["p_c"] = "Counter"
				Clock.schedule_once(self.counter_step_done)

	def counter(self, *args):
		# if self.gd["p_c"] == "":
		self.gd["uptomay"] = True
		self.gd["payed"] = False
		self.sd["popup"]["popup"].title = "Choose a card"
		self.gd["confirm_var"] = {"o": self.gd["opp"], "c": "Counter", "m": 1}
		Clock.schedule_once(self.popup_start, popup_dt)

	def counter_done(self, dt=0):
		if not self.gd["counter_id"]:
			self.sd["popup"]["popup"].dismiss()

			for ind in self.gd["chosen"]:
				if ind in self.emptycards:
					continue
				self.gd["counter_id"] = ind
				self.gd["rev_counter"] = True

			if not self.gd["counter_id"]:
				self.counter_step_done()
			else:
				self.popup_clr()
				self.counter_done()
		elif self.net["game"] and not self.net["send"] and self.gd["active"] == "2":
			self.net["var"] = [self.gd["counter_id"]]
			self.net["var1"] = "counter"
			if not self.poptext:
				Clock.schedule_once(partial(self.popup_text, "waitingser"))
			self.mconnect("counter")
		else:
			counter = self.cd[self.gd["counter_id"]]
			for item in counter.text_c:
				if counter.card == "Event" and item[0].lower().startswith("[counter]") and item[1] > -9 and item[
					1] != 0:
					self.mat[self.gd["counter_id"][-1]]["mat"].remove_widget(counter)
					self.mat[self.gd["counter_id"][-1]]["mat"].add_widget(counter)
					self.pd[self.gd["counter_id"][-1]]["Hand"].remove(self.gd["counter_id"])
					res = self.mat[self.gd["counter_id"][-1]]["field"]["Res"]
					counter.setPos(field=((res[2] - res[0]) / 2 + res[0], (res[3] - res[1]) / 2 + res[1]), t="Res")
					self.pd[self.gd["counter_id"][-1]]["Res"].append(self.gd["counter_id"])
					self.hand_size(counter.ind[-1])
					self.pay_stock(counter.cost)
					self.gd["payed"] = True
					self.gd["effect"] = ab.event(item[0])
					self.gd["ability_trigger"] = f"Event_{self.gd['counter_id']}_Counter"
					Clock.schedule_once(self.ability_event)
					return False
				elif counter.card == "Character" and item[0].lower().startswith("[act] [counter]") and item[1] != 0 and \
						item[1] > -9:
					self.gd["ability_trigger"] = f"ACT_{self.gd['counter_id']}_Counter"
					self.gd["ability"] = item[0]

					self.gd["pay"] = ab.pay(item[0])
					if self.gd["pay"]:
						self.gd["payed"] = False
					else:
						self.gd["payed"] = True

					Clock.schedule_once(self.pay_condition)
					return False

			Clock.schedule_once(self.counter_step_done)

	def counter_step_done(self, dt=0):
		self.popup_clr()
		if self.gd["counter_id"] != "" and self.cd[self.gd["counter_id"]].card == "Event":
			self.event_done()

		if self.gd["check_ctr"]:
			self.gd["check_ctr"] = False
			counter = self.cd[self.gd["counter_id"]]
			if counter.card == "Character":
				for text in counter.text_c:
					if text[0].startswith(auto_ability) and text[1] != 0 and text[1] > -9:
						ability = ab.auto(a=text[0], p=self.gd["phase"], r=(counter.ind, counter.ind), act=counter.ind)
						stack = [self.gd["counter_id"], ability, text[0], self.gd["counter_id"],
						         (counter.pos_old, counter.pos_new, "", ""), self.gd["phase"], 0, self.gd["pp"]]
						if ability and stack not in self.gd["stack"][self.gd["counter_id"][-1]]:
							self.gd["stack"][self.gd["counter_id"][-1]].append(stack)
				self.check_auto_ability(act=self.gd["counter_id"])
			else:
				Clock.schedule_once(self.counter_step_done)
		else:
			if self.net["game"] and self.gd["active"] == "2" and not self.gd["counter_id"]:
				self.net["var"] = []
				self.net["var1"] = "counter"
				self.mconnect("counter")
			else:
				self.counter_step_end()

	def counter_step_end(self, dt=0):
		self.gd["rev_counter"] = False
		self.gd["counter_id"] = ""
		self.gd["check_atk"] = True
		self.gd["counter"] = []
		self.pd[self.gd["active"]]["done"]["Counter"] = True
		self.gd["phase"] = "Damage"
		Clock.schedule_once(self.damage_step, phase_dt)

	def show_attack_btn(self):
		self.sd["btn"]["end"].disabled = False
		self.sd["btn"]["end"].y = 0
		if self.gd["popup_attack"] > 0:
			Clock.schedule_once(partial(self.popup_text, "Attack"))

		if self.gd["com"] and self.gd["active"] == "2":
			pass
		else:
			for n in range(3):
				if self.pd[self.gd["active"]]["Center"][n] != "" and self.cd[
					self.pd[self.gd["active"]]["Center"][n]].status == "Stand":
					btns = []
					if self.pd[self.gd["opp"]]["Center"][self.m[n]] != "":
						if self.gd["attack_t"]["f"][n]:
							self.sd["btn"][f"af{n}"].y = self.cd[self.pd[self.gd["active"]]["Center"][n]].y + \
							                             self.sd["card"][1] + self.mat[self.gd["active"]]["mat"].y
							btns.append("f")

						if self.gd["attack_t"]["s"][n]:
							self.sd["btn"][f"as{n}"].y = self.cd[self.pd[self.gd["active"]]["Center"][n]].y - \
							                             self.sd["btn"][f"as{n}"].size[1] + \
							                             self.mat[self.gd["active"]]["mat"].y
							btns.append("s")
					else:
						if self.gd["attack_t"]["d"][n]:
							self.sd["btn"][f"ad{n}"].y = self.cd[self.pd[self.gd["active"]]["Center"][n]].y + \
							                             self.sd["card"][1] + self.mat[self.gd["active"]]["mat"].y
							btns.append("d")
						for text in self.cd[self.pd[self.gd["active"]]["Center"][n]].text_c:
							if text[0].startswith(cont_ability) and text[1] != 0 and text[1] > -9:
								self.gd["effect"] = ab.cont(text[0])
								if "backatk" in self.gd["effect"]:
									self.sd["btn"][f"af{n}"].y = self.cd[self.pd[self.gd["active"]]["Center"][n]].y - \
									                             self.sd["btn"][f"af{n}"].size[1] + \
									                             self.mat[self.gd["active"]]["mat"].y
									btns.append("f")
									break

					for btn in btns:
						self.sd["btn"][f"a{btn}{n}"].x = self.mat["1"]["mat"].x + self.cd[
							self.pd[self.gd["active"]]["Center"][n]].x

	def hide_attack_btn(self):
		for item in self.sd["btn"]:
			if item.startswith("a"):
				self.sd["btn"][item].pos = (-Window.width, -Window.height)

	# self.sd["btn"][item].disabled = True

	def attack_phase(self, *args):
		self.sd["btn"]["end"].text = "End Attack"
		self.sd["btn"]["end"].disabled = True
		self.sd["btn"]["end_attack"].y = -Window.height
		self.sd["btn"]["end_phase"].y = -Window.height
		self.act_ability_show(hide=True)
		self.dismiss_all()
		self.change_label()
		self.clear_ability()
		self.gd["check_atk"] = False
		if self.gd["active"] == "1":
			self.hand_btn_show()
		for t in self.gd["attack_t"]:
			for i in self.gd["attack_t"][t]:
				self.gd["attack_t"][t][i] = True
		if "Attack" in self.gd["skip"]:
			self.gd["nomay"] = True
			self.gd["attack"] = 0
		else:
			self.gd["nomay"] = False
			if self.gd["turn"] == 1:
				if self.gd["d_3atk_1turn"] and not self.net["game"]:
					self.gd["d_atk"][0] = 3
				else:
					self.gd["d_atk"][0] = 1
			self.gd["attack"] = len([s for s in self.pd[self.gd["active"]]["Center"] if self.cd[s].status == "Stand"])
		self.check_auto_ability()

	def attack_phase_main(self, dt=0):
		self.sd["btn"]["end"].disabled = True
		self.sd["btn"]["end"].text = "End Attack"
		self.sd["btn"]["end"].x = Window.width - self.sd["btn"]["end"].size[0]
		self.change_label()
		self.clear_ability()

		if self.gd["attack"] > 0:
			self.sd["btn"]["end"].disabled = False
			self.check_atk_type()
			if self.net["game"] and self.gd["active"] == "2":
				if self.gd["show_wait_popup"]:
					Clock.schedule_once(partial(self.popup_text, "waiting"))
				self.mconnect("phase")
			elif self.gd["com"] and self.gd["active"] == "2":
				self.check_bodyguard()
				discard = self.ai.attack(self.pd, self.cd, self.gd)
				self.gd["attack"] = len(discard)
				if discard == "pass":
					self.end_current_phase()
				else:
					self.gd["opp_attack"] = list(discard)
					Clock.schedule_once(self.opp_attack, move_dt_btw)
			else:
				if self.net["game"]:
					self.net["send"] = False
				self.show_attack_btn()
		else:
			# if "Attack" in self.gd["skip"]:
			# 	Clock.schedule_once(self.attack_phase_done)
			# else:
			if self.net["game"] and self.gd["active"] == "1":
				self.net["var"] = ["x"]
				self.net["var1"] = "no attack"
				self.mconnect("phase")
			else:
				Clock.schedule_once(self.attack_phase_done)  # , move_dt_btw)

	def opp_attack(self, dt=0):
		if len(self.gd["opp_attack"]) > 0:
			self.gd["phase"] = "Declaration"
			self.change_label()
			temp = self.gd["opp_attack"].pop(0)
			self.gd["attacking"] = list(temp)
			self.attack_declaration_middle()
		else:
			self.end_current_phase()

	def check_bodyguard(self, p=""):
		if self.pd[self.gd["opp"]]["Center"][1] != "":
			card_opp = self.cd[self.pd[self.gd["opp"]]["Center"][1]]
		else:
			card_opp = False
		if card_opp and "Declaration" in p and not self.gd["bodyguard"]:
			for text in card_opp.text_c:
				if text[0].startswith(cont_ability) and text[1] > -9 and text[1] != 0:
					effect = ab.cont(text[0])
					if effect and card_opp.status != "Reverse" and "bodyguard" in effect:
						self.gd["bodyguard"] = True
						break
		elif card_opp and "Battle" in p and card_opp.status == "Reverse":
			self.gd["bodyguard"] = False

	def attack_declaration_middle(self):
		card = self.cd[self.gd["attacking"][0]]
		self.rest_card(self.gd["attacking"][0])

		self.mat[self.gd["active"]]["mat"].remove_widget(card)
		self.mat[self.gd["active"]]["mat"].add_widget(card)
		if self.gd["bodyguard"] and self.gd["attacking"][1] != "f" and self.gd["attacking"][3] != 1:
			self.gd["attacking"][3] = 1
			self.gd["attacking"][1] = "f"
			self.gd["attacking"][4] = "C"
		elif self.gd["attacking"][1] == "d":
			card.soul_c.append([1, 1, "Direct", self.gd["turn"]])
		elif self.gd["attacking"][1] == "s":
			aa = True
			for text in card.text_c:
				if text[0].startswith(cont_ability) and text[1] > -9 and text[1] != 0:
					eff = ab.cont(text[0])
					if "no_decrease" in eff:
						aa = False
						break
			if aa:
				card.soul_c.append(
						[-self.cd[self.pd[self.gd["opp"]]["Center"][self.gd["attacking"][3]]].level_t, 1, "Side",
						 self.gd["turn"]])
				card.update_soul()

		if self.gd["d_atk"][0] > 0 and len(self.gd["d_atk"][1]) < self.gd["d_atk"][0]:
			self.gd["d_atk"][1].append(self.gd["attacking"][0])

		self.check_cont_ability()
		self.check_auto_ability(atk=self.gd["attacking"][0])

	def attack_declaration(self, btn):
		self.sd["btn"]["end"].disabled = True
		self.sd["btn"]["end"].y = -Window.height
		self.hide_attack_btn()
		self.gd["phase"] = "Declaration"
		self.change_label()
		ind = self.pd[self.gd["active"]]["Center"][int(btn.cid[-1])]
		self.check_bodyguard(self.gd["phase"])

		if self.gd["bodyguard"]:
			m = 1
		else:
			m = self.m[int(btn.cid[-1])]

		if "d" in btn.cid[0]:
			p = ""
		else:
			p = "C"

		self.gd["attacking"] = [ind, btn.cid[0], int(btn.cid[-1]), m, p]
		# id , direct/front , position in center, opp position in center,opp center/back stage

		if len([b for b in self.pd[self.gd["opp"]]["Back"] if b != ""]) >= 1 and btn.cid[0] == "f":
			for text in self.cd[ind].text_c:
				if text[0].startswith(cont_ability) and text[1] != 0 and text[1] > -9:
					self.gd["effect"] = ab.cont(text[0])
					if "backatk" in self.gd["effect"]:
						self.gd["chosen"] = []
						self.gd["choose"] = False
						self.gd["ability_trigger"] = f"BattleBatk_{ind}"
						self.gd["ability_effect"].append("backatk")
						self.gd["status"] = "BattleBatkOppSelect1"
						if "may" in self.gd["effect"]:
							self.gd["status"] = f"May{self.gd['status']}"
						self.select_card()
						Clock.schedule_once(partial(self.popup_text, "Main"))
						return False

		self.attack_declaration_beginning()

	def attack_declaration_beginning(self, dt=0):
		if self.net["game"] and not self.net["send"] and self.gd["active"] == "1":
			self.net["var"] = list(self.gd["attacking"])
			self.net["var1"] = "atk_decla"
			if not self.poptext:
				Clock.schedule_once(partial(self.popup_text, "waitingser"))
			self.mconnect("phase")
		else:
			self.attack_declaration_middle()

	def attack_declaration_done(self, dt=0):
		if self.gd["attacking"][0] != "":
			self.gd["phase"] = "Trigger"
			Clock.schedule_once(self.trigger_step, phase_dt)
		else:
			self.pd[self.gd["active"]]["phase"]["Battle"] = True
			self.pd[self.gd["active"]]["phase"]["Trigger"] = True
			self.pd[self.gd["active"]]["phase"]["Counter"] = True
			self.pd[self.gd["active"]]["phase"]["Damage"] = True
			self.pd[self.gd["active"]]["done"]["Damage"] = True
			self.pd[self.gd["active"]]["done"]["Battle"] = True
			self.pd[self.gd["active"]]["done"]["Trigger"] = True
			self.pd[self.gd["active"]]["done"]["Counter"] = True
			self.pd[self.gd["active"]]["done"]["Declaration"] = True
			Clock.schedule_once(self.attack_phase_done)

	def climax_phase_beginning(self, dt=0):
		self.sd["btn"]["end"].text = f"End {self.gd['phase']}"
		self.change_label()
		self.clear_ability()
		if self.gd["pp"] < 0:
			Clock.schedule_once(self.check_auto_ability)
			return False
		else:
			if "Climax" in self.gd["skip"]:
				self.climax_phase_done()
			else:
				# self.sd["btn"]["end"].disabled = False
				self.climax_phase_play()

	def climax_phase(self, dt=0):
		self.sd["btn"]["end"].disabled = True
		self.act_ability_show(hide=True)
		self.dismiss_all()
		self.sd["btn"]["end_attack"].y = -Window.height
		self.sd["btn"]["end_phase"].y = -Window.height
		if self.net["game"] and self.gd["active"] == "1":
			self.net["send"] = False
		self.climax_phase_beginning()

	def climax_phase_play(self, dt=0):
		self.gd["nomay"] = False
		if self.net["game"] and self.gd["active"] == "2" and len(self.pd[self.gd["active"]]["Climax"]) <= 0:

			if self.gd["show_wait_popup"]:
				Clock.schedule_once(partial(self.popup_text, "waiting"))
			self.mconnect("phase")
		elif self.net["game"] and self.gd["active"] == "1" and not self.net["send"] and self.gd["play_card"] and not \
				self.gd["climax_play"]:
			if len(self.pd[self.gd["active"]]["Climax"]) > 0:
				self.net["var"] = [self.pd[self.gd["active"]]["Climax"][0]]
				self.net["var1"] = "play_climax"
				if not self.poptext:
					Clock.schedule_once(partial(self.popup_text, "waitingser"))
				self.mconnect("phase")
		elif self.gd["play_card"] and len(self.pd[self.gd["active"]]["Climax"]) > 0:
			self.gd["play_card"] = ""
			card = self.cd[self.pd[self.gd["active"]]["Climax"][0]]
			self.gd["ability"] = str(card.text_c[0][0])

			if auto_ability in self.gd["ability"]:
				self.gd["stack"][card.ind[-1]].append(
						[card.ind, ab.climax(self.gd["ability"]), str(self.gd["ability"]), card.ind,
						 (card.pos_old, card.pos_new, "", ""), self.gd["phase"], 0, self.gd["pp"]])
			self.check_auto_ability(play=card.ind)
		elif not self.gd["play_card"] and len(self.pd[self.gd["active"]]["Climax"]) > 0:
			self.gd["ability_trigger"] = ""
			self.climax_phase_done()
		elif self.gd["com"] and self.gd["active"] == "2":
			climax = self.ai.climax(self.pd, self.cd)
			if climax == "pass":
				self.end_current_phase()
			else:
				self.opp_climax(climax)
		else:
			# self.sd["btn"]["end"].disabled = False
			self.sd["btn"]["end"].y = 0
			self.update_playable_climax(self.gd["active"])
			if len(self.gd["playable_climax"]) < 1 or not self.gd["climax"][self.gd["active"]]:
				if self.net["game"] and self.gd["active"] == "1":
					self.net["var"] = ["x"]
					self.net["var1"] = "no climax"
					self.mconnect("phase")
				else:
					self.climax_phase_done()


	def opp_climax(self, climax):
		self.pd[climax[-1]]["Hand"].remove(climax)
		self.cd[climax].setPos(field=self.mat[climax[-1]]["field"]["Climax"], t="Climax")
		self.pd[climax[-1]]["Climax"].append(climax)
		self.hand_size(climax[-1])
		self.update_field_label()
		self.check_cont_ability()
		self.gd["play_card"] = climax
		Clock.schedule_once(self.climax_phase_play)

	def climax_phase_done(self):
		self.sd["btn"]["end"].disabled = True
		self.pd[self.gd["active"]]["done"]["Climax"] = True
		self.gd["phase"] = "Attack"
		if "Climax" in self.gd["skip"]:
			self.gd["nomay"] = True
			Clock.schedule_once(self.attack_phase)
		else:
			Clock.schedule_once(self.attack_phase, phase_dt)

	def level_up(self, *args):
		if self.gd["clocker_rev"]:
			ind = self.gd["ability_trigger"].split("_")[1]
			if ind[-1] == "1":
				player = "2"
			elif ind[-1] == "2":
				player = "1"
		else:
			if self.gd["rev"]:
				player = self.gd["opp"]
			else:
				player = self.gd["active"]

		if self.net["game"] and player == "2":
			if self.gd["show_wait_popup"]:
				Clock.schedule_once(partial(self.popup_text, "waiting"))
			self.mconnect("phase")
		elif self.gd["com"] and player == "2":
			self.gd["p_owner"] = player
			self.gd["chosen"] = []
			self.gd["chosen"].append(self.ai.level_up(self.pd, self.cd))
			self.level_up_done()
		else:
			self.sd["popup"]["popup"].title = "Level Up"
			self.gd["confirm_var"] = {"o": player, "c": "Levelup", "m": 1}
			Clock.schedule_once(self.popup_start, popup_dt)

	def level_up_done(self, *args):
		self.sd["popup"]["popup"].dismiss()
		if self.net["game"] and self.net["lvlsend"] and self.gd["chosen"][0][
			-1] == "1":  # and self.gd["active"] == "1":
			self.net["lvlsend"] = False
			if not self.net["send"]:
				self.net["varlvl"] = list(self.gd["chosen"])
				self.level_up_done()
			else:
				self.net["var"] = list(self.gd["chosen"])
				self.net["var1"] = "lvl"
				if not self.poptext:
					Clock.schedule_once(partial(self.popup_text, "waitingser"))
				self.mconnect("lvl")
		else:
			if self.net["send"] and not self.net["lvlsend"]:
				self.net["lvlsend"] = True
			card = ""
			if self.gd["chosen"]:
				card = self.gd["chosen"].pop(0)
				self.clock_to_level(card)

			if len(self.pd[card[-1]]["Clock"]) > 0:
				# discard all cards in clock
				for n in range(len(self.pd[card[-1]]["Clock"][:6])):
					ind = self.pd[card[-1]]["Clock"].pop(0)
					self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
					self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])
					self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Waiting"], t="Waiting")
					self.pd[ind[-1]]["Waiting"].append(ind)

				self.update_field_label()
				self.clock_size(card[-1])

			self.check_cont_ability()

			self.popup_clr()
			if self.gd["active"] == "1":
				if self.gd["phase"] == "Main":
					self.update_movable(self.gd["active"])
				elif self.gd["phase"] == "Climax":
					self.update_playable_climax(self.gd["active"])

			if "damage" in self.gd["level_up_trigger"]:
				Clock.schedule_once(self.damage, move_dt_btw)
			elif "draw" in self.gd["level_up_trigger"]:
				Clock.schedule_once(self.draw, move_dt_btw)
			elif "clocker" in self.gd["level_up_trigger"]:
				if self.gd["clocker_rev"]:
					self.gd["clocker_rev"] = False
				Clock.schedule_once(self.clocker, move_dt_btw)
			elif "clock" in self.gd["level_up_trigger"]:
				Clock.schedule_once(self.clock_phase_done, move_dt_btw)
			elif "reveal" in self.gd["level_up_trigger"]:
				Clock.schedule_once(self.reveal_done, move_dt_btw)
			elif "pay_choose" in self.gd["level_up_trigger"]:
				Clock.schedule_once(self.pay_condition_done, move_dt_btw)
			self.gd["level_up_trigger"] = ""

	def clock_phase(self, *args):
		self.change_label()
		# if self.net["game"]:
		# 	self.net["wait"] = True
		self.gd["clock_done"] = False
		if self.net["game"]:
			self.net["send"] = False

		if self.net["game"] and self.gd["active"] == "2":
			if self.gd["show_wait_popup"]:
				Clock.schedule_once(partial(self.popup_text, "waiting"))
			self.mconnect("phase")
		elif self.gd["com"] and self.gd["active"] == "2":
			discard = self.ai.clock(self.pd, self.cd)
			if discard == "pass" or not self.gd["clock"][self.gd["active"]]:
				self.end_current_phase()
			else:
				self.gd["p_owner"] = self.gd["active"]
				self.gd["chosen"] = []
				self.gd["chosen"].append(discard)
				self.clock_phase_done()
		else:
			if not self.gd["clock"][self.gd["active"]]:
				Clock.schedule_once(self.clock_phase_done, phase_dt)
			else:
				self.sd["popup"]["popup"].title = self.gd["phase"]
				self.gd["uptomay"] = True
				self.gd["confirm_var"] = {"o": self.gd["active"], "c": "Clock", "m": 1}
				Clock.schedule_once(self.popup_start, popup_dt)

	def clock_phase_done(self, *args):
		self.sd["popup"]["popup"].dismiss()
		if self.gd["chosen"] and self.gd["level_up_trigger"] == "":
			self.gd["target"] = list(self.gd["chosen"])
		if self.gd["clock_temp"]:
			self.gd["target"] = self.gd["clock_temp"]
			self.gd["clock_temp"] = None
		if self.net["game"] and not self.net["send"] and self.gd["active"] == "1" and "Clock" in self.gd["phase"]:
			self.net["var"] = self.gd["chosen"]
			self.net["var1"] = "Clock"
			if not self.poptext:
				Clock.schedule_once(partial(self.popup_text, "waitingser"))
			self.mconnect("phase")
		elif self.gd["target"] and not self.gd["clock_done"]:
			if self.gd["level_up_trigger"] == "":
				ind = self.gd["target"].pop(0)
				self.hand_clock(ind)

				if not self.gd["both"] and self.check_lose():
					return False

				if self.gd["both"]:
					self.gd["both"] = False

				self.gd["clock_done"] = True
				if len(self.pd[self.gd["active"]]["Clock"]) >= 7:
					self.gd["clock_temp"] = self.gd["target"]
					self.popup_clr()
					self.gd["level_up_trigger"] = "clock"
					Clock.schedule_once(self.level_up)
				else:
					Clock.schedule_once(self.clock_phase_done)
		elif self.gd["clock_done"] and self.gd["level_up_trigger"] == "" and "Clock" in self.gd["phase"]:
			self.gd["clock_done"] = False
			self.gd["draw"] = 2
			self.popup_clr()
			Clock.schedule_once(self.draw, move_dt_btw)
		else:
			self.popup_clr()
			if "Clock" in self.gd["phase"]:
				self.pd[self.gd["p_owner"]]["done"]["Clock"] = True
				self.gd["phase"] = "Main"
				self.gd["clock_done"] = False
				Clock.schedule_once(self.main_phase)
			elif not self.gd["payed"] and ("AUTO" in self.gd["ability_trigger"] or "ACT" in self.gd["ability_trigger"]):
				self.pay_condition_done()

	def check_lose(self, *args):
		if self.gd["trev"]:
			player = self.gd["trev"]
		else:
			if self.gd["rev"]:
				player = self.gd["opp"]
			else:
				player = self.gd["active"]

		if len(self.pd[player]["Level"]) >= 3 and len(self.pd[player]["Clock"]) >= 7:
			if player == "1":
				self.gd["wl"] = False
			else:
				self.gd["wl"] = True
			self.gd["gg"] = True
			Clock.schedule_once(self.winlose, move_dt_btw)
			return True

	def show_continue_btn(self, *args):
		# show a continue btn when dismissing the clock popup
		# if self.gd["popup_done"][0] and not self.gd["popup_done"][1] and not self.decks["dbuilding"]:
		# 	self.gd["popup_done"] = (False, False)
		# 	self.sd["btn"]["end"].y = -Window.height
		# 	self.sd["btn"]["end_attack"].y = -Window.height
		# 	self.sd["btn"]["end_phase"].y = -Window.height
		#
		# 	self.sd["btn"]["continue"].size = (Window.width / 5., self.sd["b_bar"].size[1])
		# 	self.sd["btn"]["continue"].x = Window.width - self.sd["btn"]["continue"].size[0]
		# 	self.sd["btn"]["continue"].y = 0
		# 	self.sd["btn"]["continue"].disabled = False
		# 	self.sd["cpop_press"] = []
		# 	self.hand_btn_show()
		#
		# 	self.act_ability_show(True)
		# 	self.sd["menu"]["btn"].disabled = False
		self.sd["popup"]["stack"].clear_widgets()
		self.sd["btn"]["filter_add"].y = -Window.height * 2

	# else:
	# 	self.hand_btn_show(False)

	def show_popup(self, btn):
		# show the clock popup and continue when pressing the continue btn
		if not self.gd["popup_done"][0] and not self.gd["popup_done"][1]:
			self.hand_btn_show(False)
			self.sd["menu"]["btn"].disabled = True
			self.gd["popup_done"] = (True, False)
			self.sd["btn"]["continue"].y = -Window.height
			self.hand_btn_show(False)

			if self.infot is not None:
				self.infot.cancel()
				self.infot = None

			if btn.cid == "cont":
				if self.gd["stack_pop"]:
					self.stack_popup()
				elif self.gd["act_poped"]:
					self.act_popup(self.gd["act_poped"])
				else:
					self.gd["confirm_var"] = dict(self.gd["confirm_temp"])
					if self.gd["confirm_pop"]:
						self.confirm_popup()
					else:
						self.popup_start()

	def show_menu(self, *args):
		self.gd["menu"] = True
		if self.net["game"]:
			self.sd["menu"]["restart"].disabled = True
			self.sd["menu"]["change"].disabled = True
		else:
			self.sd["menu"]["restart"].disabled = False
			self.sd["menu"]["change"].disabled = False
		self.sd["menu"]["main"].disabled = False

		self.sd["menu"]["popup"].open()

	def menu_dismiss(self, *args):
		self.gd["menu"] = False
		self.sd["menu"]["popup"].dismiss()

	def show_field(self, btn):
		# dismiss the popup and show the field
		self.sd["popup"]["popup"].dismiss()
		if self.gd["ability_doing"] == "looktop" and "hand" in self.gd["p_c"]:
			self.gd["confirm_temp"]["t"] = list(self.gd["p_l"])
		self.sd["cpop_press"] = []
		self.gd["popup_done"] = (False, False)
		if self.gd["act_poped"]:
			self.gd["act_poped"] = ""
			Clock.schedule_once(self.play_card_done)
		else:
			self.sd["btn"]["end"].y = -Window.height
			self.sd["btn"]["end_eff"].y = -Window.height
			self.sd["btn"]["end_attack"].y = -Window.height
			self.sd["btn"]["end_phase"].y = -Window.height

			self.sd["btn"]["continue"].size = (Window.width / 5., self.sd["b_bar"].size[1])
			self.sd["btn"]["continue"].x = Window.width - self.sd["btn"]["continue"].size[0]
			self.sd["btn"]["continue"].y = 0
			self.sd["btn"]["continue"].disabled = False
			self.sd["cpop_press"] = []
			self.hand_btn_show()
			self.act_ability_show(hide=True)
		self.sd["menu"]["btn"].disabled = False

	def refresh(self, dt=0):
		if self.gd["trev"]:
			player = self.gd["trev"]
		else:
			if self.gd["rev"]:
				player = self.gd["opp"]
			else:
				player = self.gd["active"]

		if not self.gd["reshuffle"]:
			self.check_cont_ability()
			self.gd["reshuffle"] = True
			if len(self.pd[player]["Waiting"]) <= 0 and not self.gd["cancel_dmg"]:
				if player == "1":
					self.gd["wl"] = False
				else:
					self.gd["wl"] = True
				self.gd["gg"] = True
				Clock.schedule_once(self.winlose, popup_dt)
				return
			else:
				if len(self.pd[player]["Waiting"]) <= 0 and self.gd["cancel_dmg"]:
					for inx in range(len(self.pd[player]["Res"])):
						temp = self.pd[player]["Res"].pop(0)
						self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Waiting"], t="Waiting")
						self.pd[player]["Waiting"].append(temp)

				for n in range(len(self.pd[player]["Waiting"])):
					temp = self.pd[player]["Waiting"].pop()
					self.pd[player]["Library"].append(temp)
					self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Library"], t="Library")
				self.update_field_label()
				self.check_auto_ability(refr=player, stacks=False)
				self.gd["shuffle_trigger"] = "refresh"
				self.shuffle(player)
		else:
			if self.gd["reshuffle_trigger"] == "damage":
				Clock.schedule_once(self.damage)
			elif self.gd["reshuffle_trigger"] == "draw":
				Clock.schedule_once(self.draw)
			elif self.gd["reshuffle_trigger"] == "trigger":
				Clock.schedule_once(self.trigger)
			elif self.gd["reshuffle_trigger"] == "looktop":
				Clock.schedule_once(self.look_top_done)
			elif self.gd["reshuffle_trigger"] == "stock":
				Clock.schedule_once(self.stock)
			elif self.gd["reshuffle_trigger"] == "reveal":
				Clock.schedule_once(self.reveal)
			elif self.gd["reshuffle_trigger"] == "mill":
				Clock.schedule_once(self.mill)
			elif self.gd["reshuffle_trigger"] == "marker":
				Clock.schedule_once(self.marker)
			elif self.gd["reshuffle_trigger"] == "brainstorm":
				Clock.schedule_once(self.brainstorm)

	def send_to_waiting(self, ind, *args):
		if not self.gd["no_cont_check"]:
			self.check_cont_ability()
		if "Waiting" not in self.cd[ind].pos_new:
			self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
			self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])

			if ind in self.pd[ind[-1]]["Climax"]:
				self.pd[ind[-1]]["Climax"].remove(ind)
			else:
				if ind in self.gd["stage-1"]:
					self.gd["stage-1"].remove(ind)
				self.check_auto_ability(wait=ind, stacks=False)
				self.pd[ind[-1]][self.cd[ind].pos_new[:-1]][int(self.cd[ind].pos_new[-1])] = ""
				self.remove_marker(ind)

			self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Waiting"], t="Waiting")
			self.pd[ind[-1]]["Waiting"].append(ind)

			self.update_field_label()
			if ind in self.gd["attacking"][0]:  # "Declaration" in self.gd["phase"] and
				self.gd["attacking"][0] = ""
			if self.gd["no_cont_check"]:
				self.gd["no_cont_check"] = False
			else:
				self.check_cont_ability()

	def encore_card(self, ind, *args):
		card = self.cd[ind]
		self.pd[ind[-1]]["Waiting"].remove(ind)

		card.setPos(field=self.mat[ind[-1]]["field"][card.pos_old], t=card.pos_old)
		card.rest()

		if self.pd[ind[-1]][card.pos_new[:-1]][int(card.pos_new[-1])] != "":
			temp = self.pd[ind[-1]][card.pos_new[:-1]][int(card.pos_new[-1])]
			self.send_to_waiting(temp)
		self.pd[ind[-1]][card.pos_new[:-1]][int(card.pos_new[-1])] = ind
		self.update_field_label()
		self.check_auto_ability(play=ind, stacks=False)
		self.check_cont_ability()

	def encore_middle(self):
		self.send_to_waiting(self.gd["encore_ind"])
		Clock.schedule_once(self.stack_ability)

	def encore_start(self, dt=0):
		if self.gd["rev"]:
			player = self.gd["opp"]
		else:
			player = self.gd["active"]
		self.check_reversed()
		if len(self.gd["encore"][player]) > 0:
			if player == "1":
				if self.gd["encore_ind"]:
					self.gd["uptomay"] = False
					self.sd["btn"]["end"].disabled = True
					if self.net["game"] and not self.net["send"]:
						self.net["var"] = [self.gd["encore_ind"]]
						self.net["var1"] = "encore"
						if not self.poptext:
							Clock.schedule_once(partial(self.popup_text, "waitingser"))
						self.mconnect("phase")
					else:
						self.encore_middle()
				else:
					if self.net["game"]:
						self.net["send"] = False
					self.gd["status"] = "Select1"
					self.gd["chosen"] = []
					self.gd["uptomay"] = True
					# self.gd["choose"] = True
					if not self.gd["ability_trigger"]:
						self.gd["ability_trigger"] = "_0"
					self.select_card(s="Reverse")
					if self.gd["popup_encore"]:
						self.gd["popup_encore"] = False
						Clock.schedule_once(partial(self.popup_text, "Encore"), popup_dt)
			elif player == "2":
				if self.net["game"]:
					if self.gd["show_wait_popup"]:
						Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
					self.mconnect("phase")
				elif self.gd["com"]:
					ind = ""
					if len(self.gd["opp_encore"]) > 0:
						ind = self.gd["opp_encore"].pop(0)

					if ind and ind in self.gd["encore"][player]:
						self.gd["encore_ind"] = ind
						self.encore_middle()
					else:
						self.gd["encore_ind"] = self.gd["encore"][player].pop(0)
						self.encore_middle()
		else:
			if not self.gd["rev"]:
				self.gd["rev"] = True
				self.gd["encore_ind"] = ""
				Clock.schedule_once(self.encore_start)
			else:
				self.gd["rev"] = False
				self.gd["encore_ind"] = ""
				self.pd[self.gd["active"]]["done"]["Encore"] = True
				self.gd["phase"] = "End"
				Clock.schedule_once(self.end_phase, move_dt_btw)

	def encore(self, btn):
		self.sd["popup"]["popup"].dismiss()
		if self.gd["confirm_pop"]:
			self.gd["confirm_pop"] = False

		if self.net["game"]:
			self.net["send"] = False
			self.net["act"][4].append(str(btn.cid))
			self.net["act"][5] = 1

		self.gd["target"] = [str(btn.cid)]
		self.encore_pay()

	def reflev(self, btn, *args):
		self.sd["popup"]["popup"].dismiss()
		if self.gd["confirm_pop"] and len(self.gd["reflev"]) >= 2:
			self.gd["confirm_pop"] = False
		try:
			rule = str(btn.cid)
			if self.net["game"]:
				self.net["act"][4].append(btn.cid)
		except AttributeError:
			rule = btn

		if rule == "ref":
			self.gd["reflev"].remove("ref")
			if self.gd["reshuffle_trigger"]:
				self.gd["reshuffle_trigger_temp"] = str(self.gd["reshuffle_trigger"])
			self.gd["reshuffle_trigger"] = "damage"
			Clock.schedule_once(self.refresh, move_dt_btw)
			return False
		elif rule == "lev":
			self.gd["reflev"].remove("lev")
			self.gd["level_up_trigger"] = "damage"
			self.check_cont_ability()
			Clock.schedule_once(self.level_up, move_dt_btw)
			return False

	def encore_pay(self):
		if "Character" in self.gd["target"]:
			self.gd["search_type"] = "Character"
			Clock.schedule_once(self.encore_popup)
		elif "Trait" in self.gd["target"]:
			self.gd["search_type"] = self.gd["effect"][self.gd["effect"].index("Trait") + 1]
			Clock.schedule_once(self.encore_popup)
		elif "Clock" in self.gd["target"]:
			self.gd["reshuffle_trigger"] = "encore"
			self.gd["damage_refresh"] = 1
			self.gd["damageref"] = True
			Clock.schedule_once(self.damage, move_dt_btw)
		elif any("Stock" in encore for encore in self.gd["target"]):
			for encore in self.gd["target"]:
				if "Stock" in encore:
					self.pay_stock(int(self.gd["target"][self.gd["target"].index(encore)][-1]))
					self.gd["payed"] = True
					Clock.schedule_once(self.encore_done)
					return False
		else:
			self.encore_done()

	def encore_done(self, *args):
		self.sd["popup"]["popup"].dismiss()
		if self.gd["rev"]:
			player = self.gd["opp"]
		else:
			player = self.gd["active"]

		if self.gd["chosen"]:
			for ind in self.gd["chosen"]:
				self.gd["target"].append(ind)

		if any("Stock" in trg for trg in self.gd["target"]) or "Clock" in self.gd["target"]:
			if "Waiting" in self.cd[self.gd["encore_ind"]].pos_new:
				self.encore_card(self.gd["encore_ind"])
		elif len(self.gd["target"]) > 1 and ("Character" in self.gd["target"] or "Trait" in self.gd["target"]):
			temp = self.gd["target"].pop(-1)
			self.hand_waiting(chosen=[temp])
			self.encore_card(self.gd["encore_ind"])
			if self.net["game"] and (
					self.gd["active"] == "1" and not self.gd["rev"] or self.gd["active"] == "2" and self.gd["rev"]):
				self.net["act"][4].append(temp)

		self.popup_clr()
		self.check_cont_ability()

		if "encore" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("encore")

		self.gd["encore_ind"] = ""
		self.gd["p_c"] = ""
		Clock.schedule_once(self.ability_effect, move_dt_btw)

	def encore_popup(self, *args):
		self.popup_clr()
		self.sd["popup"]["popup"].title = f"Encore {self.cd[self.gd['encore_ind']].name}"
		self.gd["uptomay"] = True
		self.gd["confirm_var"] = {"o": self.gd["encore_ind"][-1], "c": "Encore", "m": 1}
		Clock.schedule_once(self.popup_start, popup_dt)

	def check_reversed(self):
		self.gd["encore"]["1"] = [s for s in self.pd["1"]["Center"] + self.pd["1"]["Back"] if
		                          s != "" and self.cd[s].status == "Reverse"]
		self.gd["encore"]["2"] = [s for s in self.pd["2"]["Center"] + self.pd["2"]["Back"] if
		                          s != "" and self.cd[s].status == "Reverse"]

	def encore_phase(self, dt=0):
		self.dismiss_all()
		self.change_label()
		self.clear_ability()
		if self.gd["pp"] < 0:
			self.gd["popup_encore"] = True
			Clock.schedule_once(self.check_auto_ability)
			return False
		else:
			self.encore_phase_start()

	def encore_phase_start(self, *args):
		self.gd["encore_ind"] = ""
		self.check_reversed()
		if len(self.gd["encore"]["1"]) + len(self.gd["encore"]["2"]) <= 0:
			self.pd[self.gd["active"]]["phase"]["Encore"] = True
			self.pd[self.gd["active"]]["done"]["Encore"] = True
			self.gd["phase"] = "End"
			# if self.net["game"] and self.gd["turn"] > 1 and self.gd["active"] == "1":
			# 	self.net["var"] = ["kn"]
			# 	self.net["var1"] = "end_encore"
			# 	self.mconnect("phase")
			# else:
			Clock.schedule_once(self.end_phase, move_dt_btw)
			return False

		if self.gd["com"] and len(self.gd["encore"]["2"]) > 0:
			encore = self.ai.encore(self.pd, self.cd, self.gd)
			self.gd["opp_encore"] = encore
		self.hand_btn_show()
		Clock.schedule_once(self.encore_start)

	def end_phase(self, *args):
		self.dismiss_all()
		self.sd["menu"]["btn"].disabled = True
		self.sd["btn"]["end"].y = -Window.height
		self.sd["btn"]["end_attack"].y = -Window.height
		self.sd["btn"]["end_phase"].y = -Window.height
		self.sd["btn"]["ablt_info"].y = -Window.height
		self.sd["btn"]["draw_upto"].y = -Window.height
		self.gd["nomay"] = False
		self.gd["skip"] = []
		self.gd["climax_play"] = False
		self.end_phase_start()

	def end_phase_start(self, *args):
		self.clear_ability()
		self.change_label()
		if self.gd["pp"] < 0:
			Clock.schedule_once(self.check_auto_ability)
			return False
		else:
			self.end_phase_main()

	def end_phase_main(self, *args):
		self.hand_btn_show(False)
		# remove climax
		if len(self.pd[self.gd["active"]]["Climax"]) > 0:
			ind = self.pd[self.gd["active"]]["Climax"].pop()
			self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
			self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])
			self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Waiting"], t="Waiting")
			self.pd[ind[-1]]["Waiting"].append(ind)
			self.update_field_label()
		for key in self.pd[self.gd["opp"]]["phase"].keys():
			if any(key != phase for phase in ("Janken", "Mulligan")):
				self.pd[self.gd["opp"]]["phase"][key] = False
				self.pd[self.gd["opp"]]["done"][key] = False
		self.check_cont_ability()
		self.hand_limit_start()

	def reset_auto(self):
		for player in list(self.pd.keys()):
			for ind in self.pd[player]["Center"] + self.pd[player]["Back"] + self.pd[player]["Memory"]:
				if ind != "":
					for item in self.cd[ind].text_c:
						if item[1] == -31:
							self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -1

						if self.gd["phase"] == "End":
							if item[1] == -2:
								self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = 1
							elif item[1] == -5:
								self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -1
							elif item[1] == -7:
								self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = 1
							elif item[1] == -6:
								self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -1
							elif item[1] == -8:
								self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = 1
							elif item[1] == -10:
								self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -1
							elif item[1] == -11:
								self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -1
							elif item[1] == -15:
								self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = 1
							elif item[1] == -16:
								self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = 1
							elif item[1] == -30:
								self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -3

	def reduce_c_counter(self, *args):
		for player in list(self.pd.keys()):
			for ind in self.pd[player]["Center"] + self.pd[player]["Back"] + [player]:
				if ind != "":
					self.cd[ind].reduce_c()
					self.cd[ind].clean_c()

	def winlose(self, dt=0):
		if self.gd["gg"]:
			if self.gd["wl"]:
				wl = "Win"
			else:
				wl = "Lose"
			self.sd["menu"]["wl"].text = f"You {wl}"
			if self.net["game"]:
				self.net["var"] = wl[0]
				self.net["var1"] = "winlose"
				self.mconnect("winlose")

		self.sd["menu"]["popup"].title = "End of Game"
		self.sd["menu"]["popup"].size = (Window.width * 0.6, Window.height * 0.6)
		self.sd["menu"]["wl_box"].remove_widget(self.sd["menu"]["wl_box1"])
		self.sd["menu"]["wl_box"].add_widget(self.sd["menu"]["wl"])
		self.sd["menu"]["wl_box"].add_widget(self.sd["menu"]["wl_box1"])
		# self.sd["btn"]["restart"].pos = (0, 0)
		# self.sd["btn"]["change"].pos = (0, 0)
		# self.sd["btn"]["main"].pos = (0, 0)
		self.sd["btn"]["end"].disabled = True
		self.sd["btn"]["end_attack"].disabled = True
		self.sd["btn"]["end_phase"].disabled = True
		self.sd["btn"]["continue"].disabled = True
		self.sd["menu"]["btn"].disabled = False

		if self.net["game"]:
			self.net["var"] = wl[0]
			self.net["var1"] = "winlose"
			self.mconnect("act")

		self.show_menu()

	def discard(self, dt=0):
		imd = self.gd["ability_trigger"].split("_")[1]
		if self.gd["p_c"] != "" and not self.gd["target"]:
			self.sd["popup"]["popup"].dismiss()

			if len(self.gd["chosen"]) < self.gd["discard"] and self.gd["dismay"]:
				self.gd["dismay"] = False
				self.gd["confirm1"] = [True, 0]
				if self.net["game"]:
					self.net["act"][5] = 0
				Clock.schedule_once(self.ability_effect)
				return False
			elif len(self.gd["chosen"]) < self.gd["discard"]:
				for r in range(self.gd["discard"] - len(self.gd["chosen"])):
					self.gd["chosen"].append("")

			for ix in self.gd["chosen"]:
				self.gd["target"].append(ix)

			if "Stage" in self.gd["effect"]:
				if len([c for c in self.gd["chosen"] if c != ""]) > 0:
					self.effect_to_stage("Stage")
				else:
					self.gd["target"].append("")
					Clock.schedule_once(self.discard)
			elif "levswap" in self.gd["effect"]:
				if len([s for s in self.gd["target"] if s != ""]) > 0 and len(self.pd[imd[-1]]["Waiting"]) > 0:
					for rr in self.gd["target"]:
						self.gd["target_temp"].append(rr)
					self.gd["target"] = []
					if "discard" in self.gd["ability_effect"]:
						self.gd["ability_effect"].remove("discard")
					self.gd["done"] = True
					self.gd["discard"] = 0
					if self.gd["dismay"]:
						self.gd["dismay"] = False
					Clock.schedule_once(self.ability_effect)
					return False
				else:
					Clock.schedule_once(self.discard)
			else:
				Clock.schedule_once(self.discard)
		elif self.gd["p_c"] == "" and not self.gd["target"]:
			self.gd["chosen"] = []

			if self.gd["uptomay"]:
				uptomay = "up to "
			else:
				uptomay = ""

			if self.gd["discard"] > 1:
				word = "cards"
			else:
				word = "card"

			if "opp" in self.gd["effect"] and imd[-1] == "1":
				player = "2"
			elif "opp" in self.gd["effect"] and imd[-1] == "2":
				player = "1"
			else:
				player = imd[-1]

			disc = ""
			if "Climax" in self.gd["search_type"] or "Character" in self.gd["search_type"]:
				disc = f"{self.gd['search_type'].lower()} "
			elif "Cost" in self.gd["search_type"]:
				disc = f"cost {self.gd['search_type'][-1]} or "
				if "<=" in self.gd["search_type"]:
					disc += "lower"
				elif ">=" in self.gd["search_type"]:
					disc += "higher"
				disc += " character "
			elif "Trait" in self.gd["search_type"]:
				if len(self.gd["search_type"].split("_")) == 3:
					disc = f"«{self.gd['search_type'].split('_')[1]}» or «{self.gd['search_type'].split('_')[2]}»"
				else:
					disc = f"«{self.gd['search_type'].split('_')[1]}»"
			elif "Name=" in self.gd["search_type"]:
				disc = f"\"{self.gd['search_type'].split('_')[1]}\" "
			elif "CLevel" in self.gd["search_type"]:
				disc = f"level {self.gd['search_type'][-1]} or "
				if "<=" in self.gd["search_type"]:
					disc += "lower"
				elif ">=" in self.gd["search_type"]:
					disc += "higher"
				disc += " character "

			if "marker" in self.gd["effect"] and isinstance(self.gd["effect"][0], str) and "discard" in \
					self.gd["effect"][0]:
				c = "Marker_Discard"
			elif "Stage" in self.gd["effect"] and isinstance(self.gd["effect"][0], str) and "discard" in \
					self.gd["effect"][0]:
				c = "Discard_stage"
			else:
				c = "Discard"

			if "cdiscard" in self.gd["effect"]:
				c += "_Clock"
			elif "ldiscard" in self.gd["effect"]:
				c += "_Level"
			elif "mdiscard" in self.gd["effect"]:
				c += "_Memory"

			if self.gd["resonance"][0]:
				self.sd["popup"]["popup"].title = f"Reveal {self.gd['discard']} {disc}{word}"
			elif "_" in c or "Clock" in self.gd["effect"]:
				self.sd["popup"]["popup"].title = f"Choose {uptomay}{self.gd['discard']} {disc}{word}"
			else:
				if "Name=" in self.gd["effect"] or "Name=" in self.gd["pay"]:
					self.sd["popup"]["popup"].title = f"Discard {self.gd['discard']} {disc}{word}"
				elif "hmemory" in self.gd["effect"]:
					self.sd["popup"]["popup"].title = f"Put {self.gd['discard']} {disc}{word} into your memory"
				else:
					self.sd["popup"]["popup"].title = f"Discard {self.gd['discard']} {disc}{word}"
			self.gd["confirm_var"] = {"o": player, "c": c, "m": self.gd["discard"]}
			Clock.schedule_once(self.popup_start, popup_dt)
		else:
			if "discard" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("discard")
			# if "do" in self.gd["ability_effect"]:
			# 	self.gd["ability_effect"].remove("do")

			if "Stage" in self.gd["effect"] and self.gd["move"] and imd[-1] == "1":
				if self.gd["uptomay"] and (not self.gd["move"] or self.gd["move"] == "none"):
					self.gd["target"].append("")
				else:
					self.gd["target"].append(self.gd["move"])
				self.gd["move"] = ""

			idm = []
			player = ""
			discard = []
			st = ""
			lif = []
			for r in range(self.gd["discard"]):
				ind = self.gd["target"].pop(0)
				if "Stage" in self.gd["effect"]:
					st = self.gd["target"].pop(0)
				if self.net["game"] and self.gd["p_owner"] == "1":  # @@
					if self.gd["pay"] and not self.gd["payed"]:
						self.net["act"][3].append(ind)
					else:
						self.net["act"][4].append(ind)
						if "Stage" in self.gd["effect"]:
							self.net["act"][4].append(st)
				if ind in self.emptycards:
					continue
				if "extra" in self.gd["effect"]:
					self.gd["extra"].append(ind)
				if self.gd["resonance"][0]:
					self.gd["resonance"][1].append(ind)
				elif "Stage" in self.gd["effect"]:
					if "if" in self.gd["effect"]:
						lif.append(ind)
					if st:
						self.play_to_stage(ind, st)
				elif "Level" in self.gd["effect"]:
					if "if" in self.gd["effect"]:
						lif.append(ind)
					self.clock_to_level(ind)
				elif "Clock" in self.gd["effect"]:
					self.hand_clock(ind)
				elif "Stock" in self.gd["effect"]:
					self.send_to_stock(ind)
				elif "Memory" in self.gd["effect"] or "hmemory" in self.gd["effect"]:
					self.send_to_memory(ind)
				else:
					lif.append(ind)
					discard.append(ind)
				player = ind[-1]
				if player == "2":
					idm.append(ind)

			self.hand_waiting(chosen=discard)

			self.gd["discard"] = 0
			if self.gd["notarget"]:
				self.gd["notarget"] = False
			self.check_cont_ability()
			self.popup_clr()
			if self.gd["dismay"]:
				self.gd["dismay"] = False

			if self.gd["resonance"][0]:
				for r in range(len(idm)):
					if self.cd[idm[r]].back:
						self.cd[idm[r]].show_front()
			if "mdiscard" in self.gd["effect"]:
				self.gd["effect"].remove("mdiscard")
			elif "hmemory" in self.gd["effect"]:
				self.gd["effect"].remove("hmemory")

			if self.gd["pay"] and not self.gd["payed"]:
				Clock.schedule_once(self.pay_condition, move_dt_btw)
			else:
				if "if" in self.gd["effect"]:
					if lif:
						self.gd["done"] = True
				elif "do" in self.gd["effect"] and self.gd["do"][0] > 0:
					self.gd["done"] = True
				elif self.gd["brainstorm_c"][1] and self.gd["brainstorm_c"][0] > 0:
					self.gd["brainstorm_c"][0] -= 1
					self.gd["do"][0] = 1
					self.gd["do"][1] = list(self.gd["brainstorm_c"][1])
					self.gd["done"] = True
				elif self.gd["brainstorm_c"][1] and self.gd["brainstorm_c"][0] <= 0:
					self.gd["brainstorm_c"][1] = []

				if "do" in self.gd["ability_effect"]:
					self.gd["ability_effect"].remove("do")

				if self.gd["random_reveal"]:
					self.popup_multi_info(cards=self.gd["random_reveal"], owner=imd[-1], t="Random")
				else:
					self.ability_effect()

	def hand_limit_start(self, *args):
		# set cards container
		self.gd["chosen"] = []
		self.gd["choose"] = False
		self.gd["uptomay"] = False

		# hand limit check
		if len(self.pd[self.gd["active"]]["Hand"]) > hand_limit:
			if self.net["game"] and self.gd["active"] == "2":
				if self.gd["show_wait_popup"]:
					Clock.schedule_once(partial(self.popup_text, "waiting"))
				self.mconnect("phase")
			elif self.gd["com"] and self.gd["active"] == "2":
				discard = self.ai.hand_limit(self.pd, self.cd)
				for ind in discard:
					self.gd["chosen"].append(ind)
				self.hand_limit_done()
			else:
				self.sd["popup"]["popup"].title = "Hand Limit"

				if len(self.pd[self.gd["active"]]["Hand"]) > hand_limit + 1:
					word = "cards"
					card = len(self.pd[self.gd["active"]]["Hand"]) - hand_limit
				else:
					word = "card"
					card = 1
				self.sd["btn"]["Hand_btn"].text = f"{card} {word} left"
				self.sd["btn"]["Hand_btn"].disabled = True

				if self.net["game"]:
					self.net["send"] = False
				# populate the popup

				self.gd["confirm_var"] = {"o": self.gd["active"], "c": "Hand"}
				Clock.schedule_once(self.popup_start, popup_dt)
		else:
			self.hand_limit_done()

	def hand_limit_done(self, *args):
		self.sd["popup"]["popup"].dismiss()

		if len(self.pd[self.gd["active"]]["Hand"]) > hand_limit and self.net["game"] and self.gd[
			"active"] == "1" and not self.net["send"]:
			self.net["var"] = self.gd["chosen"]
			self.net["var1"] = "hand_limit"
			if not self.poptext:
				Clock.schedule_once(partial(self.popup_text, "waitingser"))
			self.mconnect("phase")
		else:
			self.hand_waiting(chosen=self.gd["chosen"])
			self.check_cont_ability()
			self.popup_clr()
			self.end_phase_end()

	def end_phase_end(self, *args):
		self.clear_ability()
		self.change_label()
		if self.gd["pp"] < 2:
			Clock.schedule_once(self.check_auto_ability)
			return False
		else:
			self.reset_auto()
			self.reduce_c_counter()
			self.check_cont_ability()
			self.gd["counter_icon"] = {"1": [True, True], "2": [True, True]}
			self.gd["noencore"] = {"1": False, "2": False}
			self.pd[self.gd["active"]]["done"]["End"] = True
			self.gd["turn"] += 1
			if self.gd["turn"] % 2 == 0 and self.gd["turn"] > 0:
				self.gd["active"] = str(self.gd["second_player"])
				self.gd["opp"] = str(self.gd["starting_player"])
			else:
				self.gd["active"] = str(self.gd["starting_player"])
				self.gd["opp"] = str(self.gd["second_player"])
			# if self.net["game"]:
			# 	if self.gd["active"] == "2":
			# 		self.net["select"] += 2
			# else:
			# 	self.net["select"] += 1
			# self.reset_auto()
			self.gd["phase"] = "Stand Up"
			Clock.schedule_once(self.stand_phase)

	# Clock.schedule_once(self.stand_phase, phase_dt)

	def stock_size(self, owner):
		pos = self.mat[owner]["field"]["Stock"]
		sep = self.sd["card"][1] - self.sd["card"][0]

		if len(self.pd[owner]["Stock"]) > 2:
			space = abs(pos[3] - pos[1]) / (len(self.pd[owner]["Stock"]) - 1)
		else:
			space = sep

		self.gd["inx"] = 0
		for card in self.pd[owner]["Stock"]:
			self.mat[owner]["mat"].remove_widget(self.cd[card])
			self.mat[owner]["mat"].add_widget(self.cd[card])
			if space < sep:
				posy = pos[1] - space * self.gd["inx"]
			else:
				posy = pos[1] - sep * self.gd["inx"]

			self.cd[card].setPos(pos[0], posy, t="Stock")
			self.gd["inx"] += 1

	# self.act_ability_show()

	def clock_size(self, owner):
		pos = self.mat[owner]["field"]["Clock"]

		self.gd["inx"] = 0
		for card in self.pd[owner]["Clock"]:
			self.mat[owner]["mat"].remove_widget(self.cd[card])
			self.mat[owner]["mat"].add_widget(self.cd[card])

			posx = pos[0] + self.gd["inx"] * (pos[2] - pos[0]) / 5
			self.cd[card].setPos(posx, pos[1], t="Clock")

			self.gd["inx"] += 1

		self.update_colour(owner)

	def level_size(self, owner):
		pos = self.mat[owner]["field"]["Level"]

		self.gd["inx"] = 0
		for card in self.pd[owner]["Level"]:
			self.mat[owner]["mat"].remove_widget(self.cd[card])
			self.mat[owner]["mat"].add_widget(self.cd[card])

			y = pos[1] + self.gd["inx"] * (pos[3] - pos[1]) / 2
			self.cd[card].setPos(pos[0], y, t="Level")

			self.gd["inx"] += 1

	def update_colour(self, player):
		self.pd[player]["colour"] = []
		for card in self.pd[player]["Level"] + self.pd[player]["Clock"]:
			if self.cd[card].mcolour not in self.pd[player]["colour"]:
				self.pd[player]["colour"].append(self.cd[card].mcolour)

	def stack(self, player, field="Library"):
		if len(self.pd[player][field]) > 0:
			for ind in self.pd[player][field]:
				self.mat[player]["mat"].remove_widget(self.cd[ind])
				self.mat[player]["mat"].add_widget(self.cd[ind])

	def hand_size(self, owner, move=True):
		# if owner == "2":
		# 	shuffle(self.pd[owner]["Hand"])
		cards = self.pd[owner]["Hand"]
		width = self.sd["card"][0] + self.sd["padding"]
		height = self.sd["card"][1] + self.sd["padding"] * 1.5
		many = False

		if self.mat[owner]["mat"].size[0] - (len(cards) * width + self.sd["padding"]) < 0:
			width = (self.mat[owner]["mat"].size[0] - self.sd["padding"] * 2 - self.sd["card"][
				0]) / (len(cards) - 1)
			many = True

		self.gd["inx"] = 0
		for card in cards:
			if owner == "3":
				self.cd[card].show_back() #@@@
			else:
				self.cd[card].show_front()

			self.mat[owner]["mat"].remove_widget(self.cd[card])
			self.mat[owner]["mat"].add_widget(self.cd[card])

			# if self.gd["selected"] != "" and self.gd["selected"] != card:
			# 	self.mat[owner]["mat"].remove_widget(self.cd[self.gd["selected"]])
			# 	self.mat[owner]["mat"].add_widget(self.cd[self.gd["selected"]])

			if self.gd["swap_card"][0] and self.gd["selected"] != "" and self.gd["inx"] < self.gd["swap_card"][2]:
				self.mat[owner]["mat"].remove_widget(self.cd[self.gd["swap_card"][1]])
				self.mat[owner]["mat"].add_widget(self.cd[self.gd["swap_card"][1]])
				self.gd["swap_card"][0] = False

			if move:
				if many:
					xpos = self.sd["padding"] + width * self.gd["inx"]
				elif len(cards) % 2 == 0:
					xpos = self.mat[owner]["mat"].size[0] / 2. - len(
							cards) / 2. * width + self.sd["padding"] / 2. + width * self.gd["inx"]
				elif len(cards) % 2 != 0:
					xpos = self.mat[owner]["mat"].size[0] / 2. - (len(cards) - 1) / 2. * width - self.sd["card"][
						0] / 2. + width * self.gd["inx"]

				self.cd[card].setPos(xpos, -height, t="Hand")
			self.gd["inx"] += 1

	def sort_by_level(self, owner):
		self.pd[owner]["Hand"] = sorted(self.pd[owner]["Hand"], key=lambda x: self.cd[x].level)
