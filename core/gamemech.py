import socket
import logging
import os
import shelve
import webbrowser
from datetime import date
from functools import partial
from math import ceil
from random import shuffle, choice, sample
from urllib.parse import urlencode
from zipfile import ZipFile

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
from core.cardnum import CardNum
from core.colour import Colours
from core.imgbutton import ImgButton
from core.info import Info
from core.janken import Janken
from core.joke import Joketext
from core.label import Label
from core.labelbtn import Labelbtn
from core.markreplace import markreplace
from core.mat import Mat
from core.mail import *
from core.popup import Popup
from core.recycle import RV, RVText
from core.spinner import Spinner
from core.stackspacer import StackSpacer
from core.textinput import TextInput, SuTextInput
from core.togglebutton import ToggleButton
from core.var import *

logging.basicConfig(filename=f"{data_ex}/log", level=logging.DEBUG, format="[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s")

__author__ = "tintedmoth"
__copyright__ = "Copyright © 2022 tintedmoth"
__version__ = "0.43.1"
app_package_name = 'com.totuccio.wss'

if platform == "android":
	from jnius import autoclass


	Context = autoclass('android.content.Context')
	PackageManager = autoclass('android.content.pm.PackageManager')
	PythonActivity = autoclass('org.kivy.android.PythonActivity').mActivity
	Intent = autoclass('android.content.Intent')
	Uri = autoclass('android.net.Uri')

	package_name = PythonActivity.getPackageName()
	package_manager = PythonActivity.getPackageManager()
	installer_info = package_manager.getInstallerPackageName(package_name)




if platform != "android":
	from requests_html import HTMLSession


def list_str(lst, sep=".", sh=False):
	temp = ""
	for inx in range(len(lst)):
		ind = str(lst[inx])
		if len(lst) == 7 and (inx == 3 or inx == 4) and any(lst[0] == _ for _ in ("a", "t", "e", "p")):
			temp += f"{ind}{sep}"
		elif len(ind) >= 2:
			try:
				if sh:
					temp += f"{ind}{sep}"
				else:
					int(ind)
					temp += f"{ind[:-1]}{sep}"
			except ValueError:
				if "Center" in ind:
					temp += f"{ind.replace('Center', 'C')}{sep}"
				elif "Back" in ind:
					temp += f"{ind.replace('Back', 'B')}{sep}"
				else:
					temp += f"{ind}{sep}"
		else:
			temp += f"{ind}{sep}"
	if temp.endswith(f"{sep}"):
		temp = temp[:-1]
	if not temp:
		temp = "x"
	return temp


def check_version(file_ver, app_ver,load=False):
	v1 = file_ver.split(".")
	v2 = app_ver.split(".")
	up = False
	if float(f"{v1[0]}.{v1[1]}") > float(f"{v2[0]}.{v2[1]}"):

		up = True
	elif float(f"{v1[0]}.{v1[1]}") >= float(f"{v2[0]}.{v2[1]}") and float(f"{v1[1]}.{v1[2]}") > float(f"{v2[1]}.{v2[2]}"):
		up = True
	if not up and load:
		if float(f"{v1[0]}.{v1[1]}") == float(f"{v2[0]}.{v2[1]}") and float(f"{v1[1]}.{v1[2]}") == float(f"{v2[1]}.{v2[2]}"):
			up = True
	return up


if "version" in scej and check_version(scej["version"], __version__):
	__version__ = scej["version"]
else:
	scej["version"] = __version__



def delete_load_file(dt=0):
	for _ in ("dat", "dir", "bak"):
		if exists(f"{data_ex}/sdata.{_}"):
			remove(f"{data_ex}/sdata.{_}")


class GameMech(Widget):
	fields = ("Library", "Memory", "Waiting", "Center0", "Center1", "Center2", "Back0", "Back1", "Climax", "Clock", "Level", "Stock", "Res")
	labelfield = ("Library", "Memory", "Stock", "Waiting")
	stage = ("Center", "Back")
	colour = ("Yellow", "Green", "Red", "Blue")
	battle = ("Declaration", "Trigger", "Counter", "Damage", "Battle")
	cc = ("ability", "power", "soul", "level", "trait", "name", "cost", "contadd", "astock", "estock")
	m = (2, 1, 0)
	no_attack = ("no_attack", "no_front", "no_side", "no_direct")
	deck_spinner = ("import", "image", "format", "lang", "name")
	check_cont_waiting = []
	check_waiting_cost = []


	def __init__(self, **kwargs):
		super(GameMech, self).__init__(**kwargs)
		self.ai = AI("2")
		self.icon = {}
		self.main_scrn = None
		self.size = (Window.width, Window.height)
		self.c = 0
		self.anx = 0
		self.sin = 0
		self.sim = 0
		self.room = None
		self.infob = None
		self.infot = None
		self.req = {}
		self.download = False
		self.btn_clear = None
		self.event_move = False
		self.cnet = None
		self.opp_choice = ""
		self.network = {}
		self.cdsh = {}
		self.sd = {"field_btn_fill": False,"alabel":""}
		self.gd = {}
		self.cd = {}
		self.cpop = {}
		self.dpop = {}
		self.mpop = {}
		self.iach = {}
		self.test = {}
		self.downloads = {}
		self.downloads_key = []
		self.multi_info = {}
		self.field_btn = {}
		self.field_label = {}
		self.decks = {}
		self.temp = []
		self.title_pack = {}
		self.power_zero = []
		self.cont_recheck = {}
		self.mat = {"1": {"mat": None, "field": {}, "id": "mat", "per": 1}, "2": {"mat": None, "field": {}, "id": "mat", "per": 1}}
		self.net = network_init()
		self.poptext = False
		self.pd = pdata_init()
		self.gd = gdata_init()
		self.update_gdata_config()
		self.emptycards = ("", "00", "sspace", "9", "09")
		self.skip_cpop = list(self.emptycards) + ["1", "2"]
		self.cardinfo = None
		self.fav = None
		self.fav1 = None
		self.hscv = [[], [], 0]

		if platform == "android":
			self.webview = ""

		with self.canvas:
			self.rect = Rectangle(source=f"atlas://{img_in}/other/blank", pos=(-Window.width * 2, -Window.height * 2))
			self.rect1 = Rectangle(source=f"atlas://{img_in}/annex/dc_w00_00", pos=(-Window.width * 2, -Window.height * 2))

		Clock.schedule_once(self.main_menu)

	def start_setting(self, *args):
		self.sd["touch_down"] = None
		self.sd["update"] = ""
		self.rect1.source = f"atlas://{img_in}/other/blank"

		Clock.schedule_once(self.start_setting1, move_dt_btw)

	def start_setting_game(self, *args):
		self.mat["1"]["mat"] = Mat("1", self.mat["1"]["per"])
		self.mat["2"]["mat"] = Mat("2", self.mat["2"]["per"])
		self.mat["1"]["mat"].import_mat(sp[self.mat["1"]["id"]], self.mat["1"]["per"])
		self.mat["2"]["mat"].import_mat(sp[self.mat["2"]["id"]], self.mat["2"]["per"])

		self.cd["00"] = Card("", self.sd["card"], "0", self.mat["1"]["per"])


		self.sd["joke"] = {}
		self.sd["joke"]["1"] = Joketext()
		self.sd["joke"]["2"] = Joketext()

		self.gd["inx"] = 0
		self.sd["label"] = {}

		for label in phases:
			self.sd["label"][label] = Label(text=label, color=(.5, .5, .5, 1.), font_size=self.sd["card"][1] / 6)
			self.sd["label"][label].center_y = Window.height / 2
			self.sd["label"][label].center_x = -Window.width
			self.add_widget(self.sd["label"][label])

		for label in steps:
			self.sd["label"][label] = Label(text=label, color=(.5, .5, .5, 1.), font_size=self.sd["card"][1] / 6)
			self.sd["label"][label].center_y = Window.height / 2
			self.sd["label"][label].center_x = -Window.width
			self.add_widget(self.sd["label"][label])

		self.sd["t_bar"] = Bar(size=(Window.width, self.sd["card"][1] / 2))
		self.sd["b_bar"] = Bar(size=(Window.width, self.sd["card"][1] / 2))

		self.sd["build_scv"] = ScrollView(do_scroll_x=False, do_scroll_y=True, size_hint=(1, None), size=(Window.width, Window.height - self.sd["b_bar"].size[1]))
		self.sd["build_layout"] = RelativeLayout(size_hint_y=None, size=self.sd["build_scv"].size)

		self.parent.add_widget(self.sd["build_scv"])
		self.sd["build_scv"].add_widget(self.sd["build_layout"])

		self.sd["colour1"] = Colours(self.sd["card"], "1", self.mat["1"]["per"])
		self.sd["colour2"] = Colours(self.sd["card"], "2", self.mat["2"]["per"])
		self.mat["1"]["mat"].add_widget(self.sd["colour1"])
		self.mat["2"]["mat"].add_widget(self.sd["colour2"])

		self.add_widget(self.mat["2"]["mat"])
		self.add_widget(self.mat["1"]["mat"])

		self.add_widget(self.sd["t_bar"])
		self.add_widget(self.sd["b_bar"])

		self.sd["t_bar"].y = Window.height - self.sd["t_bar"].size[1]
		self.sd["b_bar"].x = -Window.width * 2
		self.sd["t_bar"].x = -Window.width * 2

		self.sd["build_scv"].y = self.sd["b_bar"].size[1]
		self.sd["build_scv"].x = -Window.width * 2

		self.mat["1"]["mat"].x = -Window.width * 2
		self.mat["1"]["mat"].y = -Window.height * 2

		self.mat["2"]["mat"].y = -Window.height * 2
		self.mat["2"]["mat"].x = -Window.width * 2
		self.mat["2"]["mat"].reverse()

		for player in list(self.pd.keys()):
			self.sd["joke"][player].size = (self.mat[player]["mat"].size[0], self.mat[player]["mat"].size[1])
			self.sd["joke"][player].x = -Window.width
			self.sd["joke"][player].y = -Window.height

			self.mat[player]["mat"].add_widget(self.sd["joke"][player])

		Clock.schedule_once(self.start_setting_game0, move_dt_btw)

	def start_setting_game0(self, *args):
		self.sd["popup"] = {}
		self.sd["popup"]["popup"] = Popup(size_hint=(None, None))
		self.sd["popup"]["sspace"] = StackSpacer(o=self.sd["card"])
		self.sd["popup"]["digit"] = TextInput(text="0", input_filter="int", size_hint=(None, None))
		self.sd["popup"]["icon"] = ImgButton(source=f"atlas://{img_in}/other/arrow", size=self.sd["card"], card=self.sd["card"], cid="icon")
		self.sd["popup"]["p_sct"] = RelativeLayout()
		self.sd["popup"]["sutext"] = SuTextInput(text="", size_hint=(None, None), notes=all_traits)
		self.sd["popup"]["sutext"].bind(text=self.sd["popup"]["sutext"].filter_dropdown)

		self.sd["popup"]["stack"] = StackLayout(size_hint_y=None, orientation="lr-tb", padding=self.sd["padding"] / 2, spacing=self.sd["padding"])
		self.sd["popup"]["stack"].bind(minimum_height=self.sd["popup"]["stack"].setter('height'))
		self.sd["popup"]["p_scv"] = ScrollView(do_scroll_x=False, size_hint=(1, None), effect_cls="ScrollEffect")
		self.sd["popup"]["p_scv"].bind(scroll_y=self.moving_touch_down)
		self.sd["popup"]["popup"].bind(on_dismiss=self.show_continue_btn, on_open=self.show_popup)

		self.sd["btn"] = {}
		self.sd["sbtn"] = {}
		self.sd["sbact"] = {}
		self.sd["sbper"] = {}

		self.sd["btn"]["end"] = Button(size_hint=(None, None), text="End ", on_release=self.end_current_phase, halign='center', line_height=0.8)  
		self.sd["btn"]["end_eff"] = Button(size_hint=(None, None), text="Continue Effect", on_release=self.end_current_ability, halign='center', line_height=0.8)  
		self.sd["btn"]["end_attack"] = Button(size_hint=(None, None), text="Attack Phase", on_release=self.end_to_attack, halign='center', line_height=0.8)  
		self.sd["btn"]["end_phase"] = Button(size_hint=(None, None), text="Skip Attack", on_release=self.end_to_end, halign='center', line_height=0.8)  
		self.sd["btn"]["continue"] = Button(size_hint=(None, None), text="Continue", on_release=self.show_popup, cid="cont", halign='center', line_height=0.8)  
		self.sd["btn"]["return_btn"] = Button(size_hint=(None, None), text="Abilities stack", on_release=self.stack_return, cid="-1")
		self.sd["btn"]["declare_btn"] = Button(size_hint=(None, None), text="Declare", on_release=self.cardnum_pick, cid="-1")
		self.sd["btn"]["yes_btn"] = Button(size_hint=(None, None), text="Yes", on_release=self.confirm_result, cid="1")
		self.sd["btn"]["no_btn"] = Button(size_hint=(None, None), text="No", on_release=self.confirm_result, cid="0")
		self.sd["btn"]["close_btn"] = Button(size_hint=(None, None), text="Close", on_release=self.close_popup)
		self.sd["btn"]["field_btn"] = Button(size_hint=(None, None), text="Show Field", on_release=self.show_field)
		self.sd["btn"]["down_again"] = Button(size_hint=(None, None), text="Download", on_release=self.down_open)
		self.sd["btn"]["effect_btn"] = Button(size_hint=(None, None), text="End Effect", on_release=self.end_effect)

		self.sd["btn"]["top_btn"] = Button(size_hint=(None, None), text="Top deck", on_release=self.look_top, cid="t")
		self.sd["btn"]["bottom_btn"] = Button(size_hint=(None, None), text="Bottom", on_release=self.look_top, cid="b")
		self.sd["btn"]["check_btn"] = Button(size_hint=(None, None), text="Close", on_release=self.look_top, cid="t")
		self.sd["btn"]["draw_btn"] = Button(size_hint=(None, None), text="Look next", on_release=self.look_draw, cid="d")
		self.sd["btn"]["Look_btn"] = Button(size_hint=(None, None), text="End Effect", on_release=self.look_top, cid="l")
		self.sd["btn"]["reshuffle_btn"] = Button(size_hint=(None, None), text="Reshuffle", on_release=self.reflev, cid="ref")
		self.sd["btn"]["levelup_btn"] = Button(size_hint=(None, None), text="Level up", on_release=self.reflev, cid="lev1")
		self.sd["btn"]["encore_Stock3"] = Button(size_hint=(None, None), text="③", on_release=self.encore, cid="Stock3")
		self.sd["btn"]["encore_Stock2"] = Button(size_hint=(None, None), text="②", on_release=self.encore, cid="Stock2")
		self.sd["btn"]["encore_Stock1"] = Button(size_hint=(None, None), text="①", on_release=self.encore, cid="Stock1")
		self.sd["btn"]["encore_Character"] = Button(size_hint=(None, None), text="Character Encore", on_release=self.encore, cid="Character")
		self.sd["btn"]["encore_Climax"] = Button(size_hint=(None, None), text="Climax Encore", on_release=self.encore, cid="Climax")
		self.sd["btn"]["encore_TraitN"] = Button(size_hint=(None, None), text="Trait or Name Encore", on_release=self.encore, cid="TraitN")
		self.sd["btn"]["encore_Trait"] = Button(size_hint=(None, None), text="Trait Encore", on_release=self.encore, cid="Trait")
		self.sd["btn"]["encore_Clock"] = Button(size_hint=(None, None), text="Clock Encore", on_release=self.encore, cid="Clock")
		self.sd["btn"]["encore_SWaiting"] = Button(size_hint=(None, None), text="& Stage Encore", on_release=self.encore, cid="SWaiting")
		self.sd["btn"]["label"] = Label(text="test", text_size=((self.sd["card"][0] + self.sd["padding"]) * 0.9 * starting_hand, None), font_size=self.sd["card"][1] / 5, size_hint=(1, None), markup=True)  
		self.sd["btn"]["Mulligan_btn"] = Button(size_hint=(None, None), text="End Mulligan", on_release=self.mulligan_done)
		self.sd["btn"]["M_all_btn"] = Button(size_hint=(None, None), text="Discard All", on_release=self.mulligan_all)
		self.sd["btn"]["Clock_btn"] = Button(size_hint=(None, None), text="End Clock", on_release=self.clock_phase_done)
		self.sd["btn"]["Discard_btn"] = Button(size_hint=(None, None), text="End Effect", on_release=self.discard)
		self.sd["btn"]["Levelup_btn"] = Button(size_hint=(None, None), text="Level Up", on_release=self.level_up_done)
		self.sd["btn"]["Hand_btn"] = Button(size_hint=(None, None), text="0 card left", on_release=self.hand_limit_done)
		self.sd["btn"]["Search_btn"] = Button(size_hint=(None, None), text="End Search", on_release=self.search)
		self.sd["btn"]["Salvage_btn"] = Button(size_hint=(None, None), text="End Salvage", on_release=self.salvage)
		self.sd["btn"]["Shuffle_btn"] = Button(size_hint=(None, None), text="End Effect", on_release=self.shuffle_ability)
		self.sd["btn"]["Counter_btn"] = Button(size_hint=(None, None), text="End Counter", on_release=self.counter_done)
		self.sd["btn"]["Marker_btn"] = Button(size_hint=(None, None), text="End Effect", on_release=self.marker)
		self.sd["btn"]["Add_btn"] = Button(size_hint=(None, None), text="Add", on_release=self.building_btn, cid="adding")
		self.sd["btn"]["Addcls_btn"] = Button(size_hint=(None, None), text="Close", on_release=self.building_btn, cid="close")
		self.sd["btn"]["revive_btn"] = Button(size_hint=(None, None), text="End Effect", on_release=self.revive)
		self.sd["btn"]["Encore_btn"] = Button(size_hint=(None, None), text="End Encore", on_release=self.encore_done)
		self.sd["btn"]["show_all_btn"] = Button(size_hint=(None, None), text="Show All", on_release=self.popup_filter)
		self.sd["btn"]["show_info_btn"] = Button(size_hint=(None, None), text="info", on_press=self.show_info_btn, cid="info_btn")
		self.sd["btn"]["choose_trait_btn"] = Button(size_hint=(None, None), text="Confirm", on_release=self.choose_trait)

		self.sd["btn"]["filter_add"] = BoxLayout(orientation="vertical", size_hint=(1, None))
		self.sd["btn"]["filter_add"].size = (Window.width, self.sd["card"][1])
		self.sd["btn"]["draw_upto"] = Button(size_hint=(None, None), text="Draw card", on_release=self.draw_upto_btn)
		self.sd["btn"]["ablt_info"] = Button(size_hint=(None, None), text="Info", on_release=self.info_ability_pop)

		for item in list(self.sd["btn"].keys()):
			if any(item == btn for btn in ("end", "continue", "end_attack", "end_phase", "ablt_info", "draw_upto", "end_eff")):
				self.sd["btn"]["end"].y = -Window.height * 2
			else:
				self.sd["popup"]["p_sct"].add_widget(self.sd["btn"][item])
		self.sd["popup"]["p_sct"].add_widget(self.sd["popup"]["digit"])
		self.sd["popup"]["p_sct"].add_widget(self.sd["popup"]["sutext"])

		self.sd["btn"]["end"].size = (Window.width / 5., self.sd["b_bar"].size[1])
		self.sd["btn"]["end"].text_size = (Window.width / 5. * 0.9, None)
		self.sd["btn"]["end"].font_size = self.sd["btn"]["end"].size[1] * 0.4
		self.sd["btn"]["end_eff"].size = self.sd["btn"]["end"].size
		self.sd["btn"]["end_eff"].x = Window.width - self.sd["btn"]["end"].size[0]
		self.sd["btn"]["end_eff"].text_size = self.sd["btn"]["end"].text_size
		self.sd["btn"]["end_eff"].font_size = self.sd["btn"]["end"].font_size
		self.sd["btn"]["ablt_info"].size = self.sd["btn"]["end"].size
		self.sd["btn"]["end_attack"].size = self.sd["btn"]["end"].size
		self.sd["btn"]["end_attack"].text_size = self.sd["btn"]["end"].text_size
		self.sd["btn"]["end_attack"].font_size = self.sd["btn"]["end"].font_size
		self.sd["btn"]["end_phase"].size = self.sd["btn"]["end"].size
		self.sd["btn"]["end_phase"].text_size = self.sd["btn"]["end"].text_size
		self.sd["btn"]["end_phase"].font_size = self.sd["btn"]["end"].font_size
		self.sd["btn"]["draw_upto"].size = (Window.width / 5. * 2.5, self.sd["b_bar"].size[1])
		self.sd["btn"]["draw_upto"].x = Window.width / 5. * 1.25
		self.sd["btn"]["close_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
		self.sd["btn"]["field_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)

		self.sd["popup"]["popup"].content = self.sd["popup"]["p_sct"]
		self.sd["popup"]["p_sct"].add_widget(self.sd["popup"]["p_scv"])
		self.sd["popup"]["p_scv"].add_widget(self.sd["popup"]["stack"])

		self.sd["btn"]["flvl"] = Spinner(text="Lvl -", values=("Lvl -", "Lvl 0", "Lvl 1", "Lvl 2", "Lvl 3"), size_hint=(1, 1))
		self.sd["btn"]["fcolour"] = Spinner(text="Colour", values=("Colour", "Yellow", "Green", "Red", "Blue"), size_hint=(1, 1))
		self.sd["btn"]["ftype"] = Spinner(text="Type", values=("Type", "Character", "Event", "Climax"), size_hint=(1, 1))
		self.sd["btn"]["ftrait"] = Spinner(text="Trait", values=("Trait",), size_hint=(1, 1))
		self.fav = BoxLayout(orientation="horizontal")
		for item in ("lvl", "colour", "type", "trait"):
			self.fav.add_widget(self.sd["btn"][f"f{item}"])
			self.sd["btn"][f"f{item}"].bind(text=self.popup_filter_add)

		self.sd["btn"]["filter_add"].add_widget(self.fav)
		self.sd["btn"]["ftext"] = TextInput(text="", size_hint=(4, 1))  
		self.sd["btn"]["ftextl"] = Spinner(text="Name", values=("Name", "Card No", "Text"), size_hint=(1, 1))
		self.fav1 = BoxLayout(orientation="horizontal")
		self.fav1.add_widget(self.sd["btn"]["ftextl"])
		self.fav1.add_widget(self.sd["btn"]["ftext"])
		self.sd["btn"]["ftext"].bind(text=self.popup_filter_add)
		self.sd["btn"]["ftextl"].bind(text=self.popup_filter_add)
		self.sd["btn"]["filter_add"].add_widget(self.fav1)

		for item in list(self.sd["btn"].keys()):
			self.sd["btn"][item].y = -Window.height

		self.sd["menu"] = {}
		self.sd["menu"]["btn"] = Button(size_hint=(None, None), text="Menu", on_release=self.show_menu, cid="menu", halign='center')
		self.sd["menu"]["restart"] = Button(size_hint=(1, 1), text="Restart Game", on_release=self.start_game)
		self.sd["menu"]["change"] = Button(size_hint=(1, 1), text="Change Decks", on_release=self.popup_network_slc, cid="single")
		self.sd["menu"]["main"] = Button(size_hint=(1, 1), text="Main Menu", on_release=self.gotomainmenu)
		self.sd["menu"]["setting"] = Button(size_hint=(1, 1), text="Settings", on_release=App.get_running_app().btn_open_settings)
		self.sd["menu"]["close"] = Button(size_hint=(1, 1), text="Close", on_release=self.menu_dismiss)
		self.sd["menu"]["space"] = Label(text="", size_hint=(1, 0.3))
		self.sd["menu"]["wl"] = Label(text="You ", size_hint=(1, 0.5))
		self.sd["menu"]["wl_box"] = BoxLayout(orientation="vertical", spacing=self.sd["padding"])
		self.sd["menu"]["wl_box1"] = BoxLayout(orientation="vertical", spacing=self.sd["padding"])
		self.sd["menu"]["wl_box1"].add_widget(self.sd["menu"]["restart"])
		self.sd["menu"]["wl_box1"].add_widget(self.sd["menu"]["change"])
		self.sd["menu"]["wl_box1"].add_widget(self.sd["menu"]["main"])
		self.sd["menu"]["wl_box1"].add_widget(self.sd["menu"]["setting"])
		self.sd["menu"]["wl_box1"].add_widget(self.sd["menu"]["space"])
		self.sd["menu"]["wl_box1"].add_widget(self.sd["menu"]["close"])
		self.sd["menu"]["wl_box"].add_widget(self.sd["menu"]["wl_box1"])

		self.sd["menu"]["popup"] = Popup(size=(Window.width * 0.6, Window.height * 0.45), size_hint=(None, None))
		self.sd["menu"]["popup"].title = "Menu"
		self.sd["menu"]["popup"].content = self.sd["menu"]["wl_box"]

		Clock.schedule_once(self.start_setting_game1, move_dt_btw)

	def start_setting_game1(self, *args):
		self.deck_create()
		self.janken_setting()
		self.create_field_label()
		self.replaceImage_test()
		self.field_btn_fill()
		self.act_ability_create()
		self.hand_btn_create()

		Clock.schedule_once(self.start_setting_game2, move_dt)

	def start_setting_game2(self, *args):
		self.stack_btn_ability(5)
		self.stack_btn_act(3)
		self.stack_btn_perform(2)

		self.decks["dbtn"] = {}
		pos = (-Window.width * 3, -Window.height * 3)
		size = (self.sd["card"][1], self.sd["card"][0] / 2)
		size1 = (self.sd["card"][1] / 2, self.sd["card"][0] / 2)

		for nx in range(1, 51):
			if f"{nx}1bb" in self.decks["dbtn"]:
				continue
			self.decks["dbtn"][f"{nx}1bb"] = BoxLayout(orientation="horizontal", pos=pos, size=size, size_hint=(None, None))
			self.decks["dbtn"][f"{nx}1+"] = Button(text="+", size_hint=(0.38, 1), cid=f"{nx}1+", on_release=self.add_card)
			self.decks["dbtn"][f"{nx}1-"] = Button(text="-", size_hint=(0.38, 1), cid=f"{nx}1-", on_release=self.remove_card)
			self.decks["dbtn"][f"{nx}1t"] = Label(text="0", halign='center', size_hint=(0.24, 1), valign="middle")

			self.decks["dbtn"][f"{nx}1bb"].add_widget(self.decks["dbtn"][f"{nx}1-"])
			self.decks["dbtn"][f"{nx}1bb"].add_widget(self.decks["dbtn"][f"{nx}1t"])
			self.decks["dbtn"][f"{nx}1bb"].add_widget(self.decks["dbtn"][f"{nx}1+"])

			self.sd["build_layout"].add_widget(self.decks["dbtn"][f"{nx}1bb"])

		for n in range(3):
			for t in ("d", "f", "s"):
				if t == "d":
					text = "Direct"
				elif t == "f":
					text = "Frontal"
				elif t == "s":
					text = "Side"

				self.sd["btn"][f"a{t}{n}"] = Button(text=text, cid=f"{t}{n}", on_release=self.attack_declaration)
				self.sd["btn"][f"a{t}{n}"].size = (self.sd["card"][0], self.sd["card"][1] / 4.)
				self.sd["btn"][f"a{t}{n}"].pos = (-Window.width, -Window.height)
				self.sd["btn"][f"a{t}{n}"].disabled = False

				try:
					self.parent.add_widget(self.sd["btn"][f"a{t}{n}"])
				except WidgetException:
					continue

		for x in range(4):
			self.cpop[f"n{x}"] = CardNum(f"{x}", self.sd["card"])
			self.cpop[f"n{x}"].bind(on_release=self.cardnum_pick)
			self.skip_cpop.append(f"n{x}")

		for x in ("H", "W"):
			self.cpop[f"t{x}0"] = CardNum(f"t{x}0", self.sd["card"])
			self.skip_cpop.append(f"t{x}0")

		self.cpop["9"] = CardImg("9", self.sd["card"], "9", self.mat["1"]["per"])
		self.cpop["9"].btn.bind(on_press=self.card_btn_press, on_release=self.card_btn_release)
		self.cpop["09"] = CardImg("09", self.sd["card"], "09", self.mat["1"]["per"])
		self.cpop["09"].btn.bind(on_press=self.card_btn_press, on_release=self.card_btn_release)

		for x in range(1, 3):
			self.cpop[f"{x}"] = CardImg(f"{x}", self.sd["card"], f"{x}", self.mat[f"{x}"]["per"])
			self.cpop[f"{x}"].btn.bind(on_press=self.card_btn_press, on_release=self.card_btn_release)

		self.sd["field_btn_fill"] = True
		Clock.schedule_once(self.update_edata)

	def start_setting1(self, *args):
		self.popup_text_start()

		self.cardinfo = Info(pad=self.sd["padding"], card=self.sd["card"])
		self.cardinfo.bind(on_dismiss=self.info_pop_close)
		self.cardinfo.bind(on_open=self.info_pop_open)

		self.sd["cpop_slc"] = ""
		self.sd["cpop_press"] = []
		self.sd["cpop_pressing"] = None

		self.sd["other"]["popup"] = Popup(size_hint=(None, None))
		self.sd["other"]["sct"] = RelativeLayout(size_hint=(1, 1))
		self.sd["other"]["scv"] = ScrollView(do_scroll_x=False, size_hint=(1, None), effect_cls="ScrollEffect")
		self.sd["other"]["about"] = Label(text="", valign="middle", halign="center", text_size=(Window.width * 0.7, None), size_hint=(1, None), markup=True)
		self.sd["other"]["about"].bind(on_ref_press=self.ref_press)
		self.sd["other"]["close"] = Button(size_hint=(None, None), text="Close", on_release=self.other_dismiss)
		self.sd["other"]["copy"] = Button(size_hint=(None, None), text="Copyright", on_release=self.copy_open)

		self.sd["other"]["copy_rv"] = RVText()
		self.sd["other"]["copy_rv"].box.padding = self.sd["padding"]
		self.sd["other"]["copy_rv"].box.spacing = self.sd["padding"] / 2
		self.sd["other"]["copy_box"] = BoxLayout(orientation="vertical")
		self.sd["other"]["copy_btn"] = Button(size_hint=(1, 0.05), text="Close", on_release=self.copy_dismiss)

		self.sd["other"]["copy_box"].add_widget(self.sd["other"]["copy_rv"])
		self.sd["other"]["copy_box"].add_widget(self.sd["other"]["copy_btn"])
		self.sd["other"]["sct"].add_widget(self.sd["other"]["scv"])
		self.sd["other"]["scv"].add_widget(self.sd["other"]["about"])
		self.sd["other"]["sct"].add_widget(self.sd["other"]["close"])
		self.sd["other"]["sct"].add_widget(self.sd["other"]["copy"])

		self.sd["other"]["popup"].content = self.sd["other"]["sct"]
		self.sd["other"]["popup"].title = "About"

		Clock.schedule_once(self.popup_deck_start, move_dt_btw)
		Clock.schedule_once(self.popup_network_start, move_dt_btw * 1.25)
		Clock.schedule_once(self.popup_multi_info_start, move_dt_btw * 1.5)
		Clock.schedule_once(self.check_game)

	def check_game(self, dt=0):
		self.shelve_load()
		self.main_scrn.disabled = True
		Clock.schedule_once(self.start_setting_game, move_dt_btw * 2)
		if self.gd["game_start"] and "version" in self.gd and check_version(self.gd["version"], scej["version"],load=True):
			Clock.schedule_once(partial(self.popup_text, "LoadGame"))
		else:
			Clock.schedule_once(partial(self.popup_text, "ClearLoadGame"), popup_dt)
			self.clear_loaded_game()


	def load_pos(self):
		for card in list(self.cdsh.keys()):
			if card != "1" and card != "2" and not card.endswith("3"):
				self.cd[card].colour_c = list(self.cdsh[card]["colour_c"])
				if self.cdsh[card]["back"] and "back_info" in self.cdsh[card] and not self.cdsh[card]["back_info"]:
					self.cd[card].show_back(False)
				elif self.cdsh[card]["back"]:
					self.cd[card].show_back()
				else:
					self.cd[card].show_front()
				self.cd[card].movable = bool(self.cdsh[card]["movable"])

				self.mat[card[-1]]["mat"].remove_widget(self.cd[card])
				self.mat[card[-1]]["mat"].add_widget(self.cd[card])

				self.cd[card].pos_old = str(self.cdsh[card]["pos_old"])
				self.cd[card].pos_new = str(self.cdsh[card]["pos_new"])
				if card in self.pd[card[-1]]["Library"] and self.cd[card].pos_new != "Library":
					self.pd[card[-1]]["Library"].remove(card)

				if self.cd[card].pos_new != "" and self.cd[card].pos_new != "Hand" and self.cd[card].pos_new != "Marker":
					if "Center" in self.cd[card].pos_new or "Back" in self.cd[card].pos_new or self.cd[card].pos_new in ("Waiting", "Memory", "Climax"):  
						self.cd[card].setPos(field=self.mat[card[-1]]["field"][self.cd[card].pos_new], a=True)
					elif "Res" in self.cd[card].pos_new:
						if len(self.pd[card[-1]]["Res"]) == 1 and self.cd[card].card == "Event" and card in self.gd["ability_trigger"]:
							res = self.mat[card[-1]]["field"]["Res"]
							self.cd[card].setPos(field=((res[2] - res[0]) / 2 + res[0], (res[3] - res[1]) / 2 + res[1]), t="Res", a=True)
						else:
							library = self.mat[card[-1]]["field"]["Library"]
							self.cd[card].setPos(library[0] - self.sd["padding"] / 4 - self.sd["card"][0], library[1] - self.sd["card"][1] / 3. * len(self.pd[card[-1]]["Res"]), t="Res", a=True)
					else:
						self.cd[card].setPos(field=self.mat[card[-1]]["field"][self.cd[card].pos_new], a=False)

				self.cd[card].turn = list(self.cdsh[card]["turn"])

				if self.cdsh[card]["status"] == "Rest":
					self.cd[card].rest()
				elif self.cdsh[card]["status"] == "Reverse":
					self.cd[card].reverse()
				elif self.cdsh[card]["status"] == "Stand":
					self.cd[card].stand()
				elif self.cdsh[card]["status"] == "":
					self.cd[card].climax()

				if self.cdsh[card]["marker"]:
					self.cd[card].update_marker()

			self.cd[card].select = bool(self.cdsh[card]["select"])
			self.cd[card].wmarker = bool(self.cdsh[card]["wmarker"])
			self.cd[card].aselected = str(self.cdsh[card]["aselected"])

			self.cd[card].cost_c = list(self.cdsh[card]["cost_c"])
			self.cd[card].power_c = list(self.cdsh[card]["power_c"])
			self.cd[card].level_c = list(self.cdsh[card]["level_c"])
			self.cd[card].soul_c = list(self.cdsh[card]["soul_c"])
			self.cd[card].text_c = list(self.cdsh[card]["text_c"])
			self.cd[card].trait_c = list(self.cdsh[card]["trait_c"])
			self.cd[card].name_c = list(self.cdsh[card]["name_c"])

			if card != "1" and card != "2":
				self.cd[card].update_trait()
				self.cd[card].update_power()
				self.cd[card].update_cost()
				self.cd[card].update_soul()
				self.cd[card].update_ability()
				self.cd[card].update_colour()
				self.cd[card].update_level()
				self.cd[card].update_name()

		self.change_active_background()
		self.change_active_phase(self.gd["phase"])

		for p in list(self.pd.keys()):
			self.stack(p)
			self.stack(p, field="Waiting")
			self.stack(p, field="Memory")
			self.hand_size(p)
			self.clock_size(p)
			self.stock_size(p)
			self.level_size(p)

		self.update_marker()
		self.cdsh = {}
		self.hide_attack_btn()
		self.update_field_label()


	def ref_press(self, inst, value):
		if value == "email":
			email.send(recipient="tsws@totuccio.com", subject="", text="", create_chooser=False)
		elif value == "kofi":
			webbrowser.open('https://ko-fi.com/tintedmoth')

	def copy_dismiss(self, *args):
		self.decks["sets"].dismiss()

	def copy_open(self, *args):
		self.decks["sets"].title = "Copyright"
		self.decks["sets"].size = (Window.width, Window.height)
		self.decks["sets"].content = self.sd["other"]["copy_box"]
		self.sd["other"]["copy_btn"].size = (Window.width, self.sd["card"][1] / 2)
		size = (self.decks["sets"].size[0] * 0.90, None)
		text_size = (self.decks["sets"].size[0] * 0.85, None)
		font_size = self.sd["card"][1] / 6
		self.sd["other"]["copy_rv"].data = []

		for text in se["copyright"]:
			self.sd["other"]["copy_rv"].data.append({"text": text, "text_size": text_size, "size": size, "font_size": font_size})



		Clock.schedule_once(self.copy_open_delay_y0, ability_dt)

	def copy_open_delay_y0(self, *args):
		self.sd["other"]["copy_rv"].scroll_y = 0
		Clock.schedule_once(self.copy_open_delay_y1, ability_dt)

	def copy_open_delay_y1(self, *args):
		self.sd["other"]["copy_rv"].scroll_y = 1
		Clock.schedule_once(self.copy_open_delay, ability_dt)

	def copy_open_delay(self, *args):
		self.decks["sets"].open()

	def down_open(self, *args):
		self.sd["popup"]["popup"].dismiss()
		self.popup_clr()
		self.down_popup()

	def down_popup(self, *args):
		self.multi_info["popup"].title = "Download"

		yscv = self.sd["card"][1] * 5 + self.sd["padding"] * 1.5
		yscatm = yscv + self.sd["card"][1] * 1.6 + self.sd["card"][1] * 1.5
		ypop = yscatm + self.multi_info["popup"].title_size + self.multi_info["popup"].separator_height

		if ypop > Window.height:
			ypop = Window.height * 0.9
			yscatm = ypop - self.multi_info["popup"].title_size - self.multi_info["popup"].separator_height
			yscv = yscatm - self.sd["card"][1] * 0.75

		self.multi_info["download"].size = (self.sd["card"][0] * 6 + self.sd["padding"] * 2, yscv)
		self.multi_info["dw"]["v"].size = (self.sd["card"][0] * 5, self.sd["card"][0] * 1.5)
		self.multi_info["dw"]["h"].size = (self.sd["card"][0] * 5, self.sd["card"][0] * 1.5 / 2)
		self.multi_info["popup"].size = (self.sd["card"][0] * 6 + self.sd["padding"] * 2, ypop)

		self.multi_info["dw"]["v"].center_x = self.multi_info["popup"].size[0] / 2. - self.sd["card"][0] / 4  

		self.multi_info["close"].center_x = self.multi_info["popup"].size[0] / 2. - self.sd["card"][0] / 4  
		self.multi_info["close"].y = self.sd["padding"] * 1.5
		self.multi_info["scv"].y = -Window.height * 2
		self.multi_info["download"].y = self.sd["padding"] * 3 + self.sd["card"][1] / 2
		self.multi_info["dw"]["v"].y = self.sd["padding"] * 3 + self.sd["card"][1] / 2 + yscv + self.sd["padding"] * 4

		self.multi_info["t"] = True
		self.multi_info["popup"].open()

	def down_popup_btn(self, btn):
		self.deck_title_pop(f"down_{btn.cid}")

	def down_data(self, request, *args):
		self.mcancel_create_bar1.value += 10
		temp = request.url.split("/")[-1]
		item = temp[:-2]
		db = False

		to_remove = []

		if "-d" in temp:
			ftemp = f"{data_ex}/{temp}"
		elif "-i" in temp or "-h" in temp:
			ftemp = f"{cache}/{temp}"
		else:
			db = True
			ftemp = f"{data_in}/{temp}"

		if ftemp:
			with open(ftemp, "wb") as write:
				write.write(request.result)

		with open(ftemp, "rb") as ft:
			hash_md5 = md5()
			for chunk in iter(lambda: ft.read(4096 * 10), b""):
				hash_md5.update(chunk)

			if item in se["check"] and temp in se["check"][item] and hash_md5.hexdigest() != se["check"][item][temp]:
				to_remove.append(ftemp)
			elif db and temp in self.sd["update"] and hash_md5.hexdigest() != self.sd["update"].split(".")[-1]:
				to_remove.append(ftemp)

		for itemr in to_remove:
			remove(itemr)

		if not to_remove:
			if db:
				add_db(temp, db)
			else:
				if se["check"][item]["s"] != "" and se["check"][item]["s"] not in se["main"]["w"]:
					se["main"]["w"].append(se["check"][item]["s"])
				if "-i" in temp or "-h" in temp:
					with ZipFile(ftemp, 'r') as zipObj:
						zipObj.extractall(cache)
					remove(ftemp)
				if "-d" in temp:
					add_db(item)

		self.mcancel_create_bar1.value += 1
		if self.downloads_key:
			down = self.downloads_key.pop()
			self.req[down] = UrlRequest(f"{self.downloads[down][0]}{down}", timeout=10, on_success=self.down_data, on_cancel=self.down_data_cnc, on_failure=self.failure_message, on_error=self.error_message, on_progress=self.progress_message, ca_file=cfi.where(), verify=True)

		if self.mcancel_create_bar1.value >= self.mcancel_create_bar1.max and not self.gd["confirm_trigger"] and not self.gd["cancel_down"]:
			self.mcreate_popup.dismiss()
			self.download = True
			self.gd["filter_card"][0] = False
			self.add_deckpop_btn(True)


	def down_data_cnc(self, request, *args):
		temp = request.url.split("/")[-1]
		item = temp[:-2]
		db = False

		to_remove = []

		if "-d" in temp:
			ftemp = f"{data_ex}/{temp}"
		elif "-" in temp:
			ftemp = f"{cache}/{temp}"
		elif temp in self.sd["update"]:
			db = True
			ftemp = f"{data_in}/{temp}"

		if exists(ftemp):
			with open(ftemp, "rb") as ff:
				hash_md5 = md5()
				for chunk in iter(lambda: ff.read(4096), b""):
					hash_md5.update(chunk)

				if item in se["check"] and temp in se["check"][item] and hash_md5.hexdigest() != se["check"][item][temp]:
					to_remove.append(ftemp)
				elif db and temp in self.sd["update"] and hash_md5.hexdigest() != self.sd["update"].split(".")[-1]:
					to_remove.append(ftemp)

		for itemr in to_remove:
			remove(itemr)


		if self.mcancel_create_bar1.value >= self.mcancel_create_bar1.max and self.gd["cancel_down"]:
			self.sd["text"]["popup"].dismiss()


	@staticmethod
	def reset():
		if platform == "android":
			App.get_running_app().stop()
			Window.close()
		else:
			print(f'exec: {sys.executable} {["python"] + sys.argv}')
			os.execvp(sys.executable, ['python'] + sys.argv)

	def other_open(self, *args):
		self.sd["other"]["popup"].size = (Window.width * 0.8, Window.height * 0.8)
		self.sd["other"]["close"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2)
		self.sd["other"]["copy"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2)
		self.sd["other"]["scv"].size = (Window.width * 0.8, Window.height * 0.7 - self.sd["padding"] * 5 - self.sd["card"][1] * 1)

		self.sd["other"]["close"].center_x = Window.width * 0.8 / 2 - self.sd["padding"] * 2
		self.sd["other"]["copy"].center_x = Window.width * 0.8 / 2 - self.sd["padding"] * 2
		self.sd["other"]["close"].y = self.sd["padding"] * 1.5
		self.sd["other"]["copy"].y = self.sd["padding"] * 3 + self.sd["card"][1] / 2
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

	def shelve_load(self):
		if exists(f"{data_ex}/sdata.dat"):
			with shelve.open(f"{data_ex}/sdata", "c") as shdb:
				self.pd = shdb["pdata"]
				self.gd = shdb["gdata"]
				self.decks["1"] = shdb["decks1"]
				self.decks["2"] = shdb["decks2"]
				self.net = shdb["net"]
				self.cdsh = shdb["cdata"]

	def shelve_save(self,dt=0):
		if self.gd["shelve"] and dt!=0:
			return
		else:
			self.gd["shelve"] = True
		with shelve.open(f"{data_ex}/sdata", "c") as shdb:

			if self.gd["popup_done"][0]:
				self.gd["p_ltitle"] = self.sd["popup"]["popup"].title
				self.gd["p_t"] = self.gd["p_l"]
			self.gd["version"] = scej["version"]
			shdb["pdata"] = self.pd
			shdb["gdata"] = self.gd
			try:
				shdb["decks1"] = self.decks["1"]
			except KeyError:
				shdb["decks1"] = []
			try:
				shdb["decks2"] = self.decks["2"]
			except KeyError:
				shdb["decks2"] = []
			shdb["net"] = self.net

			ss = {}
			for cc in self.cd:
				if cc in self.emptycards:
					continue
				ss[cc] = {}
				ss[cc]["colour_c"] = self.cd[cc].colour_c
				ss[cc]["back"] = self.cd[cc].back
				ss[cc]["back_info"] = self.cd[cc].back_info
				ss[cc]["movable"] = self.cd[cc].movable
				ss[cc]["status"] = self.cd[cc].status
				ss[cc]["pos_old"] = self.cd[cc].pos_old
				ss[cc]["pos_new"] = self.cd[cc].pos_new
				ss[cc]["turn"] = self.cd[cc].turn
				ss[cc]["select"] = self.cd[cc].select
				ss[cc]["cost_c"] = self.cd[cc].cost_c
				ss[cc]["power_c"] = self.cd[cc].power_c
				ss[cc]["level_c"] = self.cd[cc].level_c
				ss[cc]["soul_c"] = self.cd[cc].soul_c
				ss[cc]["text_c"] = self.cd[cc].text_c
				ss[cc]["trait_c"] = self.cd[cc].trait_c
				ss[cc]["name_c"] = self.cd[cc].name_c
				ss[cc]["marker"] = self.cd[cc].marker
				ss[cc]["select"] = self.cd[cc].select
				ss[cc]["wmarker"] = self.cd[cc].wmarker
				ss[cc]["aselected"] = self.cd[cc].aselected
			shdb["cdata"] = ss
		self.gd["shelve"] = False


	def janken_setting(self):
		width = self.sd["padding"] * 2 + self.sd["card"][0]
		height = self.sd["padding"] * 2 + self.sd["card"][1]
		self.sd["janken"] = {}
		self.sd["janken"]["popup"] = Popup(size_hint=(None, None))
		self.sd["janken"]["popup"].title = "Rock Paper Scissor"
		self.sd["janken"]["stack"] = StackLayout(orientation="lr-tb", padding=self.sd["padding"] * 2, spacing=self.sd["padding"] * 2)  
		self.sd["janken"]["stack"].size = (self.sd["padding"] * 6 + width * 3, height * 3 + self.sd["padding"] * 6)
		self.sd["janken"]["popup"].content = self.sd["janken"]["stack"]
		self.sd["janken"]["button"] = Button(size_hint=(1, None), text="Choose one", on_release=self.janken_done, size=(width * 3, self.sd["card"][1]))
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

		self.sd["janken"]["popup"].size = (self.sd["janken"]["stack"].size[0] + self.sd["padding"], self.sd["janken"]["stack"].size[1] + self.sd["card"][1] / 2 + self.sd["padding"] + self.sd["janken"]["popup"].title_size + self.sd["janken"]["popup"].separator_height)

	def gotomainmenu(self, *args):
		self.sd["menu"]["popup"].dismiss()
		self.restart()
		self.gd["gg"] = False
		self.mat["1"]["mat"].x = -Window.width * 2
		self.mat["2"]["mat"].x = -Window.width * 2
		self.sd["b_bar"].x = -Window.width * 2
		self.sd["t_bar"].x = -Window.width * 2
		self.sd["menu"]["btn"].x = -Window.width * 2
		self.main_scrn.pos = (0, 0)
		self.main_scrn.disabled = False
		if self.net["game"]:
			self.net["game"] = ""
			self.gd["com"] = True
			self.decks["2"][0] = "S11E000"
			self.decks["2"][1] = "mat"
			if not self.gd["DLimg"]:
				self.decks["2"][1] = "nodl"
			self.decks["selected"] = "dS11E000"
			self.decks["c"] = "x2d"
			self.popup_deck_slc("1")
			self.decks["c"] = "x2m"
			self.decks["selected"] = "mmat"
			if not self.gd["DLimg"]:
				self.decks["selected"] = "mnodl"
			self.popup_deck_slc("1")

	def hand_btn_create(self):
		self.sd["hbtn_press"] = []
		self.sd["hbtn"] = False
		for nx in range(1, 51):
			self.field_btn[f"Hand{nx}1"] = Button(text=f"{nx}1", cid=f"{nx}1", opacity=0, size=self.sd["card"], pos=(-Window.width, -Window.height), on_press=self.hand_btn_info, on_release=self.hand_btn_info_re)
			self.parent.add_widget(self.field_btn[f"Hand{nx}1"])

	def hand_btn_show(self, t=True):
		self.sd["hbtn_press"] = []
		self.sd["hbtn"] = t
		if t:
			for _ in self.pd["1"]["Hand"]:
				self.field_btn[f"Hand{_}"].pos = (self.cd[_].x + self.mat["1"]["mat"].x, self.cd[_].y + self.mat["1"]["mat"].y)
		else:
			for _ in self.field_btn:
				if _.startswith("Hand"):
					self.field_btn[_].y = -Window.height * 2


	def hand_btn_info_re(self, btn):
		self.gd["btn_release"] = True
		self.gd["btn_id"] = ""
		if self.infob:
			self.infob.cancel()
			self.infob = None

	def hand_btn_info(self, btn):
		self.gd["btn_id"] = btn.cid
		self.gd["btn_release"] = False

		if self.decks["dbuilding"]:
			self.cardinfo.import_data(self.cd[btn.cid], annex_img,self.gd["DLimg"])
		else:
			self.gd["btn_id"] = btn.cid
			self.sd["hbtn_press"].append(btn.cid)
			if len(self.sd["hbtn_press"]) >= info_popup_press:
				if all(_ == btn.cid for _ in self.sd["hbtn_press"][-info_popup_press:]):
					self.infob = Clock.schedule_once(self.info_start)
			else:
				self.infob = Clock.schedule_once(self.info_start, info_popup_dt)

	def act_ability_create(self, *args):
		self.sd["act"] = {}
		for _ in self.pd:
			for i in ("b", "c"):
				for j in range(3):
					if i == "b" and j == 2:
						continue
					self.sd["act"][f"{i}{j}{_}"] = []
					self.sd["act"][f"x{i}{j}{_}"] = Button(size_hint=(None, None), cid=f"{i}{j}{_}", on_release=self.act_ability_btn, text="ACT", background_normal=f"atlas://{img_in}/other/action_bar", size=(self.sd["card"][0], self.sd["card"][1] / 4.))
					self.parent.add_widget(self.sd["act"][f"x{i}{j}{_}"])
					self.sd["act"][f"x{i}{j}{_}"].x = -Window.width
					self.sd["act"][f"x{i}{j}{_}"].y = -Window.height

	def act_ability_fill(self, player):
		for _ in self.pd[player]["Center"] + self.pd[player]["Back"]:
			if _ != "":
				self.sd["act"][f"{self.cd[_].pos_new[0].lower()}{self.cd[_].pos_new[-1]}{_[-1]}"] = []
				for item in self.cd[_].text_c:
					if item[0].startswith(act_ability) and item[1] != 0 and "[counter]" not in item[0].lower() and item[1] > -9:
						self.sd["act"][f"{self.cd[_].pos_new[0].lower()}{self.cd[_].pos_new[-1]}{_[-1]}"].append(item[0])

	def act_ability_show(self, hide=False, player="", *args):
		for _ in self.sd["act"]:
			if _.startswith("x"):
				self.sd["act"][_].x = -Window.width
		if player:
			pp = player
		else:
			pp = self.gd["active"]
		if not hide and self.gd["phase"] == "Main" and not self.gd["no_act"][pp] and self.gd["ability_doing"] != "drawupto":
			if "ACT" not in self.gd["ability_trigger"]:
				self.act_ability_fill(pp)
				ss = []
				h = []
				my = []
				wr = []
				stage = [_ for _ in self.pd[pp]["Center"] + self.pd[pp]["Back"] if _ != ""]
				for _ in stage:
					ass = False
					for item in self.cd[_].text_c:
						if item[0].startswith(cont_ability) and item[1] != 0 and item[1] > -9:
							if "[cont] assist" in item[0].lower():
								ass = True
								break
					mk = 0
					if _ in self.pd[_[-1]]["marker"]:
						mk = len(self.pd[_[-1]]["marker"][_])
					ss.append((self.cd[_].status, self.cd[_].name_t, self.cd[_].trait_t, ass, mk, self.cd[_].ind))
				for _ in self.pd[pp]["Hand"]:
					h.append((self.cd[_].card, self.cd[_].name_t, self.cd[_].trait_t, self.cd[_].colour, self.cd[_].trigger, self.cd[_].ind))
				for _ in self.pd[pp]["Memory"]:
					my.append((self.cd[_].card, self.cd[_].name_t, self.cd[_].trait_t, self.cd[_].back, self.cd[_].back_info, self.cd[_].ind))
				for _ in self.pd[pp]["Waiting"]:
					wr.append((self.cd[_].card, self.cd[_].name_t, self.cd[_].trait_t, self.cd[_].ind))
				for ind in stage:
					if ind != "":
						self.gd["act_pop"][ind] = []

						if "Library" in self.cd[ind].pos_new:
							continue
						key = f"{self.cd[ind].pos_new[0].lower()}{self.cd[ind].pos_new[-1]}{ind[-1]}"
						nn = stage.index(ind)
						m = 0
						if ind in self.pd[ind[-1]]["marker"]:
							m = len(self.pd[ind[-1]]["marker"][ind])
						astock = 0
						if self.gd["markerstock"]:
							if any(name in self.gd["astock"] for name in self.cd[ind].name_t.split("\n")):
								for name in self.cd[ind].name_t.split("\n"):
									if name in self.gd["astock"]:
										astock = len(self.gd["astock"][name][ind[-1]])
							else:
								astock = len(self.gd["astock"][ind[-1]])

						for item1 in self.sd["act"][key]:
							if ab.req(a=item1, ss=ss, h=h, m=m, my=my, nn=nn, wr=wr, x=len(self.pd[ind[-1]]["Stock"]) + astock):
								self.gd["act_pop"][ind].append(item1)
								if pp == "1":
									self.sd["act"][f"x{key}"].disabled = False
									if self.sd["act"][f"x{key}"].x < 0:
										self.sd["act"][f"x{key}"].x = self.mat[ind[-1]]["field"][self.cd[ind].pos_new][0] + self.mat[ind[-1]]["mat"].x
										self.sd["act"][f"x{key}"].y = self.mat[ind[-1]]["field"][self.cd[ind].pos_new][1] - self.sd["act"][f"x{key}"].size[1] + self.mat[ind[-1]]["mat"].y

	def act_ability_btn(self, btn):
		self.gd["movable"] = []
		self.sd["act"][f"x{btn.cid}"].disabled = True
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
		self.gd["act_poped"] = ""
		self.gd["ability"] = self.gd["act_pop"][ind][n]
		self.gd["ability_trigger"] = f"ACT_{ind}"
		self.gd["confirm_trigger"] = str(self.gd["ability_trigger"])
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
				self.net["act"] = ["t", ind, n, [], [], 0, -1]
				self.net["send"] = False
			self.gd["astock_pop"] = False
			self.gd["confirm_var"] = {"ind": ind, "c": "ability"}
			Clock.schedule_once(self.confirm_popup, popup_dt)

	def act_popup(self, idm, *args):
		self.popup_clr_button()
		self.gd["p_over"] = False
		self.gd["p_c"] = "auto"
		self.gd["popup_done"] = (True, False)
		self.sd["popup"]["popup"].title = "Available ACT abilities"
		self.sd["popup"]["p_scv"].do_scroll_y = False
		self.sd["popup"]["stack"].clear_widgets()

		height = self.sd["card"][1] + self.sd["padding"] * 0.75
		xscat = (self.sd["padding"] + self.sd["card"][0]) * (starting_hand + 1) + self.sd["padding"] * 2

		self.sd["btn"]["label"].text = "Choose which ACT ability to activate."
		self.sd["btn"]["label"].text_size = (xscat * 0.9, None)
		self.sd["btn"]["label"].texture_update()

		r = len(self.gd["act_pop"][idm])

		if r > 6:
			self.sd["popup"]["p_scv"].do_scroll_y = True
			yscv = height * (r - 0.5)
		elif r > 0:
			yscv = height * r
		else:
			yscv = height
		yscv += self.sd["padding"]

		yscat = yscv + self.sd["card"][1]
		title = self.sd["popup"]["popup"].title_size + self.sd["popup"]["popup"].separator_height + self.sd["btn"]["label"].texture.size[1] + self.sd["card"][1]
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
			self.cpop[idm].selected_c(False)
			self.cpop[idm].update_text()
			if self.cpop[idm] in self.sd["popup"]["stack"].children:
				for xx in list(self.cpop.keys()):
					if xx.endswith("0") and self.cpop[xx] not in self.sd["popup"]["stack"].children:
						self.sd["popup"]["stack"].add_widget(self.cpop[xx])
						if self.cd[idm].cid == "player":
							self.cpop[xx].import_data("player",self.gd["DLimg"])
						else:
							self.cpop[xx].import_data(sc[self.cd[idm].cid],self.gd["DLimg"])
						break
			else:
				self.sd["popup"]["stack"].add_widget(self.cpop[idm])

			self.sd["sbact"][f"{inx}"].btn.text = self.cardinfo.replaceMultiple(item)
			self.sd["sbact"][f"{inx}"].btn.cid = f"{idm}{self.gd['act_pop'][idm].index(item)}"
			self.sd["sbact"][f"{inx}"].btn.texture_update()
			self.sd["sbact"][f"{inx}"].replaceImage()
			self.sd["popup"]["stack"].add_widget(self.sd["sbact"][f"{inx}"])
			inx += 1

		self.sd["btn"]["field_btn"].center_x = xscat / 2. - self.sd["card"][0] / 4  
		self.sd["btn"]["field_btn"].y = self.sd["padding"] * 1.5


		self.sd["popup"]["p_scv"].y = self.sd["btn"]["field_btn"].y * 2.5 + self.sd["btn"]["field_btn"].size[1]
		self.sd["popup"]["p_scv"].scroll_y = 1

		self.sd["btn"]["label"].pos = (
			self.sd["padding"] / 2.,
			self.sd["popup"]["p_scv"].y + self.sd["popup"]["p_scv"].size[1])  

		self.sd["popup"]["popup"].open()

	def perform_popup_btn(self, btn, a="", net=False):
		self.sd["popup"]["popup"].dismiss()
		if btn is not None and a == "":
			a = btn.a
		if not net and "choice" in self.gd["per_poped"] and btn is not None:
			self.gd["per_poped"][3] = int(btn.cid[-1])
		if not "unli" in self.gd["per_poped"]:
			self.gd["per_poped"][1].remove(self.gd["per_poped"][1][self.gd["per_poped"][3]])
		self.gd["per_poped"][-1] -= 1
		if "giver" in self.gd["effect"]:
			self.gd["effect"] = [self.gd["effect"][self.gd["effect"].index("giver") + 1], a, self.gd["effect"][self.gd["effect"].index("giver") + 2], "give"]
		else:
			self.gd["effect"] = ab.event(a)
			self.gd["ability"] = a
			self.gd["pay"] = ab.pay(a=self.gd["ability"])
			if self.gd["pay"]:
				self.gd["payed"] = False
			else:
				self.gd["payed"] = True

		if self.gd["do"][0] > 1 and "do" not in self.gd["effect"]:
			self.gd["effect"].append("do")
			self.gd["effect"].append(self.gd["do"][1])
		self.gd["ability_effect"].remove("perform")

		ind = self.gd["ability_trigger"].split("_")[1]

		if self.net["game"] and ind[-1] == "1":
			self.net["act"][5] = 1
			self.net["act"][6] = int(self.gd["per_poped"][3])

		self.ability_event()

	def popup_delay(self, *args):
		self.sd["popup"]["popup"].open()

	def popup_multi_delay(self, *args):
		self.multi_info["popup"].open()

	def perform_popup(self, idm, *args):
		self.popup_clr_button()
		self.gd["p_over"] = False
		self.gd["p_c"] = "auto"
		self.gd["popup_done"] = (True, False)
		self.sd["popup"]["popup"].title = "Performable effects"
		self.sd["popup"]["p_scv"].do_scroll_y = False
		self.sd["popup"]["stack"].clear_widgets()

		height = self.sd["card"][1] * 2.25 + self.sd["padding"] * 0.75
		xscat = (self.sd["padding"] + self.sd["card"][0]) * (starting_hand + 1) + self.sd["padding"] * 2

		self.sd["btn"]["label"].text = "Choose which effect to perform."
		self.sd["btn"]["label"].text_size = (xscat * 0.9, None)
		self.sd["btn"]["label"].texture_update()

		r = len(idm[1])

		if r > 3:
			self.sd["popup"]["p_scv"].do_scroll_y = True
			yscv = height * (r - 0.5)
		elif r > 0:
			yscv = height * r
		else:
			yscv = height
		yscv += self.sd["padding"]

		yscat = yscv + self.sd["card"][1]
		title = self.sd["popup"]["popup"].title_size + self.sd["popup"]["popup"].separator_height + self.sd["btn"]["label"].texture.size[1] + self.sd["card"][1]
		ypop = yscat + title

		if ypop > Window.height:
			self.gd["p_over"] = True
			ypop = Window.height * 0.9
			yscat = ypop - title
			yscv = yscat - self.sd["card"][1] * 0.75

		self.sd["popup"]["p_scv"].size = (xscat, yscv)
		self.sd["popup"]["popup"].size = (xscat, ypop)

		self.stack_btn_perform(len(idm[1]))
		self.cardinfo.inx = 10
		inx = 0
		for item in idm[1]:
			self.sd["sbper"][f"{inx}"].btn.a = item
			self.sd["sbper"][f"{inx}"].btn.text = self.cardinfo.replaceMultiple(item)
			self.sd["sbper"][f"{inx}"].btn.cid = f"{idm[0]}{idm[1].index(item)}"
			self.sd["sbper"][f"{inx}"].btn.texture_update()
			self.sd["sbper"][f"{inx}"].replaceImage(p=True)
			self.sd["popup"]["stack"].add_widget(self.sd["sbper"][f"{inx}"])
			inx += 1

		self.sd["btn"]["field_btn"].center_x = xscat / 2. - self.sd["card"][0] / 4  
		self.sd["btn"]["field_btn"].y = self.sd["padding"] * 1.5


		self.sd["popup"]["p_scv"].x = xscat / 2. - self.sd["popup"]["p_scv"].size[0] / 2 + self.sd["padding"] * 0.75
		self.sd["popup"]["p_scv"].y = self.sd["btn"]["field_btn"].y * 2.5 + self.sd["btn"]["field_btn"].size[1]
		self.sd["popup"]["p_scv"].scroll_y = 1

		self.sd["btn"]["label"].pos = (self.sd["padding"] / 2., self.sd["popup"]["p_scv"].y + self.sd["popup"]["p_scv"].size[1])  

		self.sd["btn"]["show_info_btn"].size = (self.sd["card"][1] / 2, self.sd["card"][1] / 4.5)
		self.sd["btn"]["show_info_btn"].y = ypop - self.sd["btn"]["show_info_btn"].size[1] * 2 - self.sd["padding"]
		self.sd["btn"]["show_info_btn"].x = xscat - self.sd["btn"]["show_info_btn"].size[0] * 2 + self.sd["padding"] * 1.5
		self.sd["btn"]["show_info_btn"].font_size = self.sd["btn"]["show_info_btn"].size[1] * 0.85

		Clock.schedule_once(self.popup_delay, popup_dt)

	def pay_mstock(self, s="", *args):
		idm = self.gd["ability_trigger"].split("_")[1]

		if not self.gd["target"] and idm[-1] == "1" and not self.gd["mstock"][0]:
			a = []

			if any(name in self.gd[f"{s}tock"] for name in self.cd[idm].name_t.split("\n")):
				for name in self.cd[idm].name_t.split("\n"):
					if name in self.gd[f"{s}tock"]:
						astk = self.gd[f"{s}tock"][name][idm[-1]]
			else:
				astk = self.gd[f"{s}tock"][idm[-1]]

			for asm in astk:
				if asm[0] not in a:
					a.append(asm[0])
			if len(a) > len(self.pd[idm[-1]]["Stock"]):
				self.gd["mstock"][1] = len(self.pd[idm[-1]]["Stock"])
			else:
				self.gd["mstock"][1] = len(a)
			self.gd["mstock"][0] = s
			self.gd["chosen"] = []
			self.gd["choose"] = False
			self.gd["astock_select"] = True
			self.select_card(fd=a)
			Clock.schedule_once(partial(self.popup_text, "mstock"))
		elif self.gd["target"]:
			if self.gd["target"] == [""]:
				self.gd["target"].remove("")
			_=[]
			for r in range(int(len(self.gd["target"]) / 2)):
				if "as" in self.gd["target"] or "es" in self.gd["target"]:
					s = self.gd["target"].pop(0)
					ind = self.gd["target"].pop(0)
					if s == "as":
						if self.net["game"] and idm[-1] == "1":
							self.net["act"][3].append(s)
							self.net["act"][3].append(ind)
						self.gd["pay"][self.gd["pay"].index("Stock") + 1] -= 1
						self.gd["payed_mstock"] = True
					elif s == "es":
						self.gd["estock_payed"].append(ind)
					self.remove_marker(ind, q=1, s=s)
					_.append(ind)

			if _:
				self.update_marker()
				self.check_cont_ability()

			if "ACT" in self.gd["ability_trigger"]:
				Clock.schedule_once(self.pay_condition)
			elif "Event" in self.gd["ability_trigger"]:
				ind, st ,_= self.gd["estock_pop"].split("_")
				if "Counter" in self.gd["ability_trigger"]:
					self.play([ind, st, ""],cnt=True)
				else:
					self.play([ind, st, ""])

	def pay_stock(self, qty, player=""):
		if self.gd["dismay"]:
			self.gd["dismay"] = False

		if qty == -1:
			qty = len(self.pd[player]["Stock"])

		for stock in range(qty):
			if len(self.pd[player]["Stock"]) > 0:
				temp = self.pd[player]["Stock"].pop()
				self.mat[temp[-1]]["mat"].remove_widget(self.cd[temp])
				self.mat[temp[-1]]["mat"].add_widget(self.cd[temp])
				self.pd[temp[-1]]["Waiting"].append(temp)
				self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Waiting"], t="Waiting")
				self.stock_size(temp[-1])
				self.update_field_label()
		self.check_cont_ability(act="False")

	def pay_condition(self, *args):
		if not self.gd["payed"] and "confirmbefore" not in self.gd["effect"]:
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
				self.gd["target"] = list(self.net["act"][3])

			if "Stock" in self.gd["pay"]:
				ind = self.gd["pay"].index("Stock")
				if "ACT" in self.gd["ability_trigger"]:
					ss = "as"
				else:
					ss = ""
				if ss != "" and f"{ss}tock" in self.gd["markerstock"] and len(self.gd[f"{ss}tock"][card.ind[-1]]) > 0:
					if card.ind[-1] == "1" and not self.gd["astock_pop"]:
						self.gd["astock_pop"] = True
						self.gd["confirm_trigger"] = f"{ss}tock_{self.gd['ability_trigger']}"
						self.gd["confirm_var"] = {"c": f"{ss}tock"}
						Clock.schedule_once(self.confirm_popup, popup_dt)
						return False
					elif card.ind[-1] == "1" and self.gd["payed_mstock"] and len(self.pd[card.ind[-1]]["Stock"]) <= self.gd["pay"][self.gd["pay"].index("Stock") + 1] and len(self.gd[f"{ss}tock"][card.ind[-1]]) > 0:
						self.gd["mstock"][0] = ""
						Clock.schedule_once(partial(self.pay_mstock, "as"))
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
				self.pay_stock(self.gd["pay"][ind + 1], card.ind[-1])
				self.gd["mstock"][0] = ""
				self.gd["pay"].remove("Stock")
				Clock.schedule_once(self.pay_condition, move_dt_btw)
				return False
			if "Zwei" in self.gd["pay"]:
				if "Zwei" not in self.gd["effect"]:
					ind = self.gd["pay"].index("Zwei")
					if "Zthis" in self.gd["pay"]:
						self.gd["p_c"] = "Salvage"
						self.gd["choose"] = False
						self.gd["target"].append(card.ind)
					elif self.gd["pay"][ind + 1] > 0:
						self.gd["salvage"] = self.gd["pay"][ind + 1]
						if "ZName=" in self.gd["pay"]:
							self.gd["search_type"] = f"Name=_{self.gd['pay'][self.gd['pay'].index('ZName=') + 1]}"
						else:
							self.gd["search_type"] = self.gd["pay"][ind + 2]
						self.gd["p_c"] = ""
					if card.ind[-1] == "2":
						self.gd["p_c"] = "Salvage"
						if "Zthis" not in self.gd["pay"]:
							self.pay_opponent("Zwei")
					self.gd["effect"].append("Zwei")
					Clock.schedule_once(self.salvage)
					return False
				else:
					if not self.gd["choose"]:
						self.gd["pay_status"] = f"Select{self.gd['pay'][self.gd['pay'].index('ZM') + 1]}"
						Clock.schedule_once(self.pay_choose)
						return False
					else:
						inm = self.gd["target"].pop(0)
						inm1 = self.gd["target"].pop(0)
						self.gd["targetpay"].append(inm)
						self.gd["targetpay"].append(inm1)
						self.check_pos(inm)
						face = False
						if "Zface-up" in self.gd["pay"]:
							face = True
						self.add_marker(inm1, inm, face)

						self.update_marker()
						self.check_cont_ability()
						self.gd["choose"] = False
						self.gd["pay"].remove("Zwei")
						Clock.schedule_once(self.pay_condition, move_dt_btw)
						return False
			if "Swap" in self.gd["pay"]:
				ind = self.gd["pay"].index("Swap")
				if self.gd["pay"][ind + 1] >= 1:
					self.gd["effect"] = [self.gd["pay"][ind + 1],"stand","this","nostand","swap"]
					self.gd["pay_status"]=f'Select{self.gd["pay"][ind + 1]}'
					if card.ind[-1] == "2":
						self.pay_opponent("Swap")
						self.gd["choose"] = True

					if not self.gd["choose"]:
						Clock.schedule_once(self.pay_choose)
						return False
					else:
						if "Swap" in self.gd["pay"]:
							self.gd["pay"].remove("Swap")
						Clock.schedule_once(self.stand, move_dt_btw)
						return False
			if "Marker" in self.gd["pay"]:
				self.remove_marker(card.ind, self.gd["pay"][self.gd["pay"].index("Marker") + 1])
				self.gd["pay"].remove("Marker")
				Clock.schedule_once(self.pay_condition, move_dt_btw)
				return False
			if "Flip" in self.gd["pay"] or "MFlip" in self.gd["pay"]:
				if "Flip" in self.gd["pay"]:
					ind = self.gd["pay"].index("Flip")
				elif "MFlip" in self.gd["pay"]:
					ind = self.gd["pay"].index("MFlip")
				if self.gd["pay"][ind + 1] == 0:
					if self.gd["pay"][ind + 2] == "down" and not card.back:
						card.show_back()
					elif self.gd["pay"][ind + 2] == "up" and card.back:
						card.show_front()
					if "Flip" in self.gd["pay"]:
						self.gd["pay"].remove("Flip")
					elif "MFlip" in self.gd["pay"]:
						self.gd["pay"].remove("MFlip")
					Clock.schedule_once(self.pay_condition, move_dt_btw)
					return False
			if "ClockL" in self.gd["pay"]:
				self.gd["damage_refresh"] = self.gd["pay"][self.gd["pay"].index("ClockL") + 1]
				self.gd["damageref"] = True
				self.gd["reshuffle_trigger"] = "pay"
				self.gd["pay"].remove("ClockL")
				if card.ind[-1] != self.gd["active"]:
					self.gd["drev"] = True
				Clock.schedule_once(self.damage, move_dt_btw)
				return False
			if "RevealStock" in self.gd["pay"]:
				if not self.gd["resonance"][0]:
					self.gd["discard"] = 1
					self.gd["search_type"] = f"Name=_{self.gd['pay'][self.gd['pay'].index('RevealStock') + 1]}"
					self.gd["p_c"] = ""
					self.gd["resonance"][0] = True
					self.gd["resonance"][2] = self.gd["discard"]

					Clock.schedule_once(self.discard)
					return False
				elif self.gd["resonance"][0]:
					for rr in self.gd["resonance"][1]:
						self.send_to("Stock", rr)
					self.gd["resonance"] = [False, [], 0]
					self.gd["pay"].remove("RevealStock")
					Clock.schedule_once(self.pay_condition, move_dt_btw)
					return False
			if "RevealMarker" in self.gd["pay"]:
				if not self.gd["resonance"][0]:
					self.gd["discard"] = 1
					self.gd["search_type"] = f"Name=_{self.gd['pay'][self.gd['pay'].index('RevealMarker') + 1]}"
					self.gd["p_c"] = ""
					self.gd["resonance"][0] = True
					self.gd["resonance"][2] = self.gd["discard"]
					Clock.schedule_once(self.discard)
					return False
				elif self.gd["resonance"][0]:
					face = False
					if "face-up" in self.gd["pay"]:
						face = True
					for rr in self.gd["resonance"][1]:
						self.add_marker(card.ind, rr, face)
					self.gd["resonance"] = [False, [], 0]
					self.gd["pay"].remove("RevealMarker")
					self.update_marker(card.ind[-1])
					self.check_cont_ability()
					Clock.schedule_once(self.pay_condition, move_dt_btw)
					return False
			if "Reveal" in self.gd["pay"]:
				self.gd["search_type"] = f"Name=_{self.gd['pay'][self.gd['pay'].index('Reveal') + 1]}"
				if "any" in self.gd["pay"]:
					self.gd["pay"].remove("any")
					self.gd["uptomay"] = True
					self.gd["discard"] = len(self.cont_times(self.gd["search_type"].split("_"), self.cont_cards(['Hand'], card.ind), self.cd))
				else:
					self.gd["discard"] = 1

				self.gd["p_c"] = ""
				self.gd["resonance"][0] = True
				self.gd["resonance"][2] = self.gd["discard"]
				self.gd["pay"].remove("Reveal")
				Clock.schedule_once(self.discard)
				return False
			if "Discard" in self.gd["pay"] or "MDiscard" in self.gd["pay"] or "HMemory" in self.gd["pay"] or "CXDiscard" in self.gd["pay"]:
				disdo = ""
				if "Discard" in self.gd["pay"]:
					ind = self.gd["pay"].index("Discard")
					disdo = "Discard"
				elif "MDiscard" in self.gd["pay"]:
					ind = self.gd["pay"].index("MDiscard")
					disdo = "MDiscard"
				elif "CXDiscard" in self.gd["pay"]:
					ind = self.gd["pay"].index("CXDiscard")
					disdo = "CXDiscard"
				elif "HMemory" in self.gd["pay"]:
					ind = self.gd["pay"].index("HMemory")
					disdo = "HMemory"
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
					if disdo == "MDiscard" and "MTrait" in self.gd["pay"]:
						self.gd["search_type"] = f"Trait_{self.gd['pay'][self.gd['pay'].index('MTrait') + 1]}"
					elif disdo == "MDiscard" and "MName=" in self.gd["pay"]:
						self.gd["search_type"] = f"Name=_{self.gd['pay'][self.gd['pay'].index('MName=') + 1]}"
					elif disdo == "MDiscard" and "MCName" in self.gd["pay"]:
						self.gd["search_type"] = f"CName_{self.gd['pay'][self.gd['pay'].index('MCName') + 1]}"
					elif disdo == "CXDiscard" and "CXName=" in self.gd["pay"]:
						self.gd["search_type"] = f"Name=_{self.gd['pay'][self.gd['pay'].index('CXName=') + 1]}"
					elif disdo == "HMemory" and "Name=" in self.gd["pay"]:
						self.gd["search_type"] = f"Name=_{self.gd['pay'][self.gd['pay'].index('Name=') + 1]}"
					elif "CColourT" in self.gd["pay"]:
						self.gd["search_type"] = f"CColourT_{self.gd['pay'][self.gd['pay'].index('CColourT') + 1]}"
					elif "Trait" in self.gd["pay"]:
						self.gd["search_type"] = f"Trait_{self.gd['pay'][self.gd['pay'].index('Trait') + 1]}"
					elif "Name=" in self.gd["pay"]:
						self.gd["search_type"] = f"Name=_{self.gd['pay'][self.gd['pay'].index('Name=') + 1]}"
					elif "Name" in self.gd["pay"]:
						self.gd["search_type"] = f"Name_{self.gd['pay'][self.gd['pay'].index('Name') + 1]}"
					elif "TriggerCX" in self.gd["pay"]:
						self.gd["search_type"] = f"TriggerCX_{self.gd['pay'][self.gd['pay'].index('TriggerCX') + 1]}"
					elif "ColourCx" in self.gd["pay"]:
						self.gd["search_type"] = f"ColourCx_{self.gd['pay'][self.gd['pay'].index('ColourCx') + 1]}"

					else:
						self.gd["search_type"] = self.gd["pay"][ind + 2]
					self.gd["p_c"] = ""

				if card.ind[-1] == "2":
					self.gd["p_c"] = "Discard"
					self.pay_opponent(disdo)

				if "Discard" in self.gd["pay"]:
					self.gd["pay"].remove("Discard")
				elif "MDiscard" in self.gd["pay"]:
					self.gd["effect"].append("mdiscard")
					self.gd["pay"].remove("MDiscard")
				elif "CXDiscard" in self.gd["pay"]:
					self.gd["effect"].append("cxdiscard")
					self.gd["pay"].remove("CXDiscard")
				elif "HMemory" in self.gd["pay"]:
					self.gd["effect"].append("hmemory")
					self.gd["pay"].remove("HMemory")

				if self.gd["effect"] and "xdiscard" in self.gd["effect"][-1]:
					self.gd["effect"].append("xdiscard")

				Clock.schedule_once(self.discard)
				return False
			if "Salvage" in self.gd["pay"]:
				ind = self.gd["pay"].index("Salvage")
				if self.gd["pay"][ind + 1] > 0:
					self.gd["salvage"] = self.gd["pay"][ind + 1]
					if "Climax" in self.gd["pay"]:
						self.gd["search_type"] = "Climax"
					else:
						self.gd["search_type"] = self.gd["pay"][ind + 2]
					self.gd["p_c"] = ""

				if card.ind[-1] == "2":
					self.gd["p_c"] = "Salvage"
					self.pay_opponent("Salvage")

				if "Salvage" in self.gd["pay"]:
					self.gd["pay"].remove("Salvage")
				if "SMemory" in self.gd["pay"]:
					self.gd["effect"].append("Memory")

				Clock.schedule_once(self.salvage)
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
					self.send_to("Clock", card.ind)
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
							self.send_to("Clock", inm)
						self.gd["choose"] = False
						self.gd["pay"].remove("ClockS")
						Clock.schedule_once(self.pay_condition, move_dt_btw)
						return False
			if "ClockW" in self.gd["pay"]:
				ind = self.gd["pay"].index("ClockW")
				if self.gd["pay"][ind + 1] > 0:
					self.gd["salvage"] = self.gd["pay"][ind + 1]
					if "Trait" in self.gd["pay"]:
						self.gd["search_type"] = f"Trait_{self.gd['pay'][self.gd['pay'].index('Trait') + 1]}"
					else:
						self.gd["search_type"] = self.gd["pay"][ind + 2]
					self.gd["p_c"] = ""
				if card.ind[-1] == "2":
					self.gd["p_c"] = "Salvage"
					self.pay_opponent("ClockW")
				self.gd["effect"].append("Clock")
				if "Cbottom" in self.gd["pay"]:
					self.gd["effect"].append("bottom")

				Clock.schedule_once(self.salvage)
				return False
			if "Hander" in self.gd["pay"]:
				if self.gd["pay"][self.gd["pay"].index("Hander") + 1] == 0:
					self.send_to("Hand", card.ind)
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
					else:
						self.gd["search_type"] = self.gd["pay"][ind + 2]
					self.gd["p_c"] = ""
				if card.ind[-1] == "2":
					self.gd["p_c"] = "Salvage"
					self.pay_opponent("WDecker")

				if "Decker" in self.gd["pay"]:
					self.gd["pay"].remove("Decker")
				elif "WDecker" in self.gd["pay"]:
					self.gd["effect"].append("wdecker")
					self.gd["pay"].remove("WDecker")

				Clock.schedule_once(self.salvage)
				return False

			if "Waiting" in self.gd["pay"]:
				if self.gd["pay"][self.gd["pay"].index("Waiting") + 1] == 0:
					self.send_to("Waiting", card.ind)
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
							self.send_to("Waiting", inm)
						self.gd["choose"] = False
						self.gd["pay"].remove("Waiting")
						Clock.schedule_once(self.pay_condition, move_dt_btw)
						return False
			if "Stocker" in self.gd["pay"]:
				if self.gd["pay"][self.gd["pay"].index("Stocker") + 1] == 0:
					self.send_to("Stock", card.ind)
					self.gd["pay"].remove("Stocker")
				elif self.gd["pay"][self.gd["pay"].index("Stocker") + 1] > 0:
					if not self.gd["choose"]:
						self.gd["pay_status"] = f"Select{self.gd['pay'][self.gd['pay'].index('Stocker') + 1]}"
						Clock.schedule_once(self.pay_choose)
						return False
					else:
						for inx in range(len(self.gd["target"])):
							inm = self.gd["target"].pop()
							self.gd["targetpay"].append(inm)
							self.send_to("Stock", inm)
						self.gd["choose"] = False
						self.gd["pay"].remove("Stocker")
						Clock.schedule_once(self.pay_condition, move_dt_btw)
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
						self.pay_opponent("Rest")
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
			if "Memory" in self.gd["pay"]:
				if self.gd["pay"][self.gd["pay"].index("Memory") + 1] == 0:
					self.send_to("Memory", card.ind)
				self.gd["pay"].remove("Memory")
				Clock.schedule_once(self.pay_condition, move_dt_btw)
				return False

			self.pay_condition_done()
		else:
			self.pay_condition_done()

	def pay_condition_done(self, dt=0):
		if self.net["game"] and self.gd["active"] == "1" and self.gd["targetpay"] and "confirmbefore" not in self.gd["effect"]:
			for ing in self.gd["targetpay"]:
				self.net["act"][3].append(ing)

		self.gd["targetpay"] = []
		self.gd["payed_mstock"] = False
		self.gd["astock_pop"] = False
		if "confirmbefore" in self.gd["effect"]:
			if self.gd["pay"]:
				self.gd["payed"] = False
				self.gd["paypop"] = False
		else:
			self.gd["payed"] = True
			self.gd["pay"] = ""
			self.check_cont_ability()

		ind = self.gd["ability_trigger"].split("_")[1]
		if len(self.pd[ind[-1]]["Library"]) <= 0 and len(self.pd[ind[-1]]["Clock"]) >= 7:
			self.gd["level_up_trigger"] = "pay"
			self.gd["reshuffle_trigger"] = "pay"
			self.gd["confirm_var"] = {"c": "reflev"}
			Clock.schedule_once(self.confirm_popup, popup_dt)
			return False
		else:
			if len(self.pd[ind[-1]]["Library"]) <= 0:
				self.gd["reshuffle_trigger"] = "pay"
				self.gd["rrev"] = ind[-1]
				Clock.schedule_once(self.refresh, move_dt_btw)
				return False
			if len(self.pd[ind[-1]]["Clock"]) >= 7:
				self.gd["level_up_trigger"] = "pay"
				Clock.schedule_once(partial(self.level_up, ind[-1]), move_dt_btw)
				return False

		if "ACT" in self.gd["ability_trigger"]:
			self.gd["paypop"] = True
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
				check = True

				if "plevel" in self.gd["effect"]:
					if "lower" not in self.gd["effect"] and len(self.pd[ind[-1]]["Level"]) < self.gd["effect"][1]:
						check = False
					elif "lower" in self.gd["effect"] and len(self.pd[ind[-1]]["Level"]) > self.gd["effect"][1]:
						check = False
				elif "experience" in self.gd["effect"]:
					if "Name=" in self.gd["effect"]:
						if len([nn for nn in self.pd[ind[-1]]["Level"] if self.gd["effect"][self.gd["effect"].index("Name=") + 1] in self.cd[nn].name_t and nn != ""]) < self.gd["effect"][self.gd["effect"].index("experience") + 1]:
							check = False
					else:
						if sum([self.cd[lv].level_t for lv in self.pd[ind[-1]]["Level"] if lv != ""]) < self.gd["effect"][self.gd["effect"].index("experience") + 1]:
							check = False
				elif "markers" in self.gd["effect"]:
					if ind not in self.pd[ind[-1]]["marker"]:
						if self.gd["effect"][self.gd["effect"].index("markers") + 1] <= 0 and "lower" in self.gd["effect"]:
							check = True
						else:
							check = False
					else:
						if "lower" in self.gd["effect"] and len(self.pd[ind[-1]]["marker"][ind]) > self.gd["effect"][self.gd["effect"].index("markers") + 1]:
							check = False
						elif "lower" not in self.gd["effect"] and len(self.pd[ind[-1]]["marker"][ind]) < self.gd["effect"][self.gd["effect"].index("markers") + 1]:
							check = False
				if check:
					if "do" in self.gd["effect"] and any(cc in self.gd["effect"] for cc in ("plevel", "experience", "markers")):
						self.gd["effect"] = self.gd["effect"][self.gd["effect"].index("do") + 1]
				else:
					self.gd["effect"] = []

				Clock.schedule_once(self.ability_event)
		else:
			Clock.schedule_once(self.ability_effect)

	def pay_opponent(self, dtype=""):
		pick = self.ai.ability(self.pd, self.cd, self.gd)
		if "AI_pay" in pick and "Swap" in pick:
			ind = pick[pick.index("AI_pay") + 1]
			self.gd["target"].append(ind)
		if "AI_pay" in pick and "Rest" in pick:
			self.cd[self.gd["pay"][pick.index("AI_pay") + 1]].rest()
			self.check_auto_ability(rev=[self.gd["pay"][pick.index("AI_pay") + 1]], rst=[self.gd["pay"][pick.index("AI_pay") + 1]], stacks=False)
			self.gd["payed"] = True
		if "AI_pay" in pick and "Clock" in pick:
			ind = self.gd["pay"][pick.index("AI_pay") + 1]
			self.send_to("Clock", ind)
			self.gd["payed"] = True

			if self.check_lose(ind[-1]):
				return False

			if self.gd["both"]:
				self.gd["both"] = False

			if len(self.pd[self.gd["active"]]["Clock"]) >= 7:
				self.gd["level_up_trigger"] = "pay_choose"
				Clock.schedule_once(partial(self.level_up, self.gd["active"]), move_dt_btw)
				return False
		if "AI_pay" in pick and "Discard" in pick:
			inds = pick[pick.index("AI_pay") + 1]
			for ind in inds:
				self.gd["chosen"].append(ind)
			self.gd["discard"] = len(inds)
			for dis in self.gd["pay"]:
				if "Discard" in str(dis):
					self.gd["pay"].remove(dis)
		if "AI_pay" in pick and "Salvage" in pick:
			inds = pick[pick.index("AI_pay") + 1]
			for ind in inds:
				self.gd["chosen"].append(ind)
			self.gd["salvage"] = len(inds)
			if "Salvage" in self.gd["pay"]:
				self.gd["pay"].remove("Salvage")
		if "AI_pay" in pick and ("WDecker" in pick or "Zwei" in pick):
			if "WDecker" in pick:
				inds = pick[pick.index("WDecker") + 1]
			elif "Zwei" in pick:
				inds = pick[pick.index("Zwei") + 1]
			for ind in inds:
				self.gd["chosen"].append(ind)
			self.gd["choose"] = True
			self.gd["salvage"] = len(inds)

	def pay_choose(self, *args):
		self.gd["chosen"] = []
		inm = self.gd["ability_trigger"].split("_")[1]
		if self.gd["com"] and ((inm[-1] == "2" and "oppturn" not in self.gd["effect"]) or (inm[-1] == "1" and "oppturn" in self.gd["effect"])):
			pick = []
			if "Waiting" in self.gd["pay"]:
				pick = self.ai.choose_stage_target("Waiting", self.pd, self.cd, self.gd)
			elif "Marker" in self.gd["pay"]:
				pick = self.ai.choose_stage_target("Marker", self.pd, self.cd, self.gd)

			if "AI_Stage" in pick:
				inx = pick.index("AI_Stage")
				self.gd["choose"] = True
				for x in pick[inx + 1]:
					self.gd["target"].append(x)
			else:
				for x in range(self.gd["effect"][0]):
					self.gd["target"].append("")
			if not self.gd["payed"] and self.gd["pay"]:
				self.pay_condition()
		else:
			if "Rest" in self.gd["pay"] and self.gd["pay"][self.gd["pay"].index("Rest") + 1] >= 1 and "Waiting" not in self.gd["pay"]:
				ind = self.gd["pay"].index("Rest")
				if "BTrait" in self.gd["pay"]:
					self.gd["btrait"][1] = self.gd["pay"][ind + 3].split("_")
					self.gd["btrait"][2] = [s for s in self.pd[inm[-1]]["Center"] + self.pd[inm[-1]]["Back"] if self.cd[s].status == "Stand"]
				self.gd["pay_status"] = f"StandSelect{self.gd['pay'][ind + 1]}"
				if len(self.gd["pay"]) > 2 and (sel in self.gd["pay"][ind + 2] for sel in ("Name", "Trait", "Other", "Text")):
					self.gd["pay_status"] = self.add_to_status(self.gd["pay_status"], self.gd["pay"][ind:ind + 5])
					if "BTrait" in self.gd["pay"]:
						self.gd["btrait"][0] = str(self.gd["pay_status"])
				self.select_card(s="Stand", p=True)
			else:
				if "PStand" in self.gd["pay"] and "PCenter" in self.gd["pay"]:
					self.gd["pay_status"] = self.add_to_status(self.gd["pay_status"], ["Stand", "Center"])
				elif "WOther" in self.gd["pay"] and "WCenter" in self.gd["pay"]:
					self.gd["pay_status"] = self.add_to_status(self.gd["pay_status"], ["Other", "Center"])
				elif "WOther" in self.gd["pay"]:
					self.gd["pay_status"] = self.add_to_status(self.gd["pay_status"], ["Other"])
				else:
					self.gd["pay_status"] = self.add_to_status(self.gd["pay_status"], self.gd["pay"])
				self.select_card(p=True)
			Clock.schedule_once(partial(self.popup_text, "Main"))
			return False

	def check_auto_ability(self, dt=.0, rev=[""], atk="", play="", wait="", revive="", trigger="", cnc=("", False), refr="", lvup="", stacks=True, act="", dis="", sav="", dmg=0, rst=[], brt=("", 0), lvc="",chg=""):
		std = ("", "", "")
		if play and self.gd["standby"][0]:
			std = tuple(self.gd["standby"])
		for re in list(rev):
			r = re
			for player in self.pd:
				tr = []

				stage = self.pd[player]["Center"] + self.pd[player]["Back"]
				for indx in stage:
					tr.append(self.cd[indx].trait_t)


				if len(self.pd[self.gd["active"]]["Climax"]) > 0:
					cxx = self.pd[self.gd["active"]]["Climax"][0]
					cx2 = ""
					if len(self.pd[self.gd["opp"]]["Climax"]) > 0:
						cx2 = self.pd[self.gd["opp"]]["Climax"][0]
					cx = (self.cd[cxx].name_t, self.cd[cxx].ind, self.cd[cxx].mcolour, self.cd[cx2].name_t, self.cd[cx2].ind, self.cd[cx2].mcolour)
				else:
					cx = ("", "9", "", "", "", "")

				if self.gd["pp"] < 0 or self.gd["phase"] in ("Attack", "Declaration","Damage","Encore"):
					cards_s = stage + [s for s in self.pd[player]["Memory"] if not self.cd[s].back]
				else:
					cards_s = list(stage)

				alarm = []
				if len(self.pd[player]["Clock"]) > 0:
					for _ in self.pd[player]["Clock"]:
						if "Clock" in self.cd[_].icon:
							alarm.append(_)
				if player == "2":
					ss = []
					h = []
					my = []
					wr = []
					mm = 0

					for cc in stage:
						ass = False
						for item in self.cd[cc].text_c:
							if item[0].startswith(cont_ability) and item[1] != 0 and item[1] > -9:
								if "[cont] assist" in item[0].lower():
									ass = True
									break
						ss.append((self.cd[cc].status, self.cd[cc].name_t, self.cd[cc].trait_t, ass, self.cd[cc].ind))
					for indy in self.pd[player]["Hand"]:
						h.append((self.cd[indy].card, self.cd[indy].name_t, self.cd[indy].trait_t, self.cd[indy].colour, self.cd[indy].trigger, self.cd[indy].ind))
					for indmy in self.pd[player]["Memory"]:
						if not self.cd[indmy].back:
							my.append((self.cd[indmy].card, self.cd[indmy].name_t, self.cd[indmy].trait_t, self.cd[indmy].back, self.cd[indmy].back_info, self.cd[indmy].ind))
					for indwr in self.pd[player]["Waiting"]:
						wr.append((self.cd[indwr].card, self.cd[indwr].name_t, self.cd[indwr].trait_t, self.cd[indwr].ind))

				cards = cards_s + [player] + alarm
				if self.gd["pp"] < 0:
					if player not in self.gd["stage-1"]:
						for rr in cards:
							if rr not in self.gd["stage-1"]:
								self.gd["stage-1"].append(rr)
					else:
						if not chg:
							cards = []
				else:
					self.gd["stage-1"] = []

				if std and std[0] in self.gd["ability_trigger"]:
					if std[2] not in cards:
						cards.append(std[2])

				for ind in cards:
					if ind in self.emptycards:
						continue
					if chg and self.gd["pp"] < 0 and ind not in self.gd["stage-1"]:
						continue
					card = self.cd[ind]
					if card.back:
						continue
					encore = []
					pos = ("", "", "", "")
					if ind == wait:  
						encore = [0, "encore"]
						if len(self.pd[wait[-1]]["Stock"]) >= 3 and "Stock3" not in encore:
							encore.append("Stock3")

					for item in card.text_c:
						if item[0].startswith(auto_ability) and item[1] != 0 and item[1] > -9:
							if "Clock" in card.icon and "[clock]" not in item[0].lower() and "[alarm]" not in item[0].lower():
								continue
							baind = ("", "")
							lvop = (0, 0)
							csop = (0, 0)
							suop = ("", "")
							nmop = ("", "")
							trop = ([], [])
							ty = ("", [], "", "", "")

							passed = False
							diss = (dis, self.cd[dis].card)
							savs = (sav, self.cd[sav].card)
							if (ind == "1" or ind == "2") and "turn" in item:
								z = (item[item.index("turn") + 1], self.gd['turn'], "ability", "")
							else:
								z = (card.turn[0], self.gd['turn'], card.turn[1], card.turn[2])

							opp = ""
							if "Center" in card.pos_new:
								if ind[-1] == "1":
									op = "2"
								elif ind[-1] == "2":
									op = "1"
								opp = self.pd[op]["Center"][self.m[int(card.pos_new[-1])]]

							if self.gd["phase"] in ("Battle", "Counter", "Trigger", "Damage", "Declaration"):
								datk = self.gd["attacking"][0]
								deff = ""
								if datk and self.gd["attacking"][1] == "f":
									if self.gd["attacking"][0][-1] == "1":
										op = "2"
									elif self.gd["attacking"][0][-1] == "2":
										op = "1"
									if "C" in self.gd["attacking"][4]:
										deff = self.pd[op]["Center"][self.gd["attacking"][3]]
									elif "B" in self.gd["attacking"][4]:
										deff = self.pd[op]["Back"][self.gd["attacking"][3]]

								baind = (datk, deff)

								suop = (self.cd[datk].status, self.cd[deff].status)
								lvop = (self.cd[datk].level_t, self.cd[deff].level_t)
								csop = (self.cd[datk].cost_t, self.cd[deff].cost_t)
								nmop = (self.cd[datk].name_t, self.cd[deff].name_t)
								trop = (self.cd[datk].trait_t, self.cd[deff].trait_t)
							if self.gd["phase"] == "Trigger":
								ty = (self.cd[r].card, self.cd[r].trigger, self.gd["attacking"][0], self.cd[r].name_t, self.cd[r].mcolour, self.cd[r].level_t)
							elif atk:
								r = atk
							elif play:
								r = play
							elif wait:
								r = wait
							elif act:
								r = act
							elif chg:
								r = chg

							if "pass" in item:
								passed = True

							v = (self.cd[ind].status, self.cd[r].status)
							nr = (self.cd[ind].name_t, self.cd[r].name_t)
							if wait and ind in wait:
								pos = (card.pos_new, "Waiting", self.cd[wait].pos_new, "Waiting")
							elif wait:
								pos = (card.pos_old, card.pos_new, self.cd[wait].pos_new, "Waiting")
							else:
								pos = (card.pos_old, card.pos_new, self.cd[r].pos_old, self.cd[r].pos_new)

							ability = ab.auto(a=item[0], p=self.gd["phase"], r=(ind, r, self.cd[r].card, self.cd[r].colour, self.cd[r].aselected), text=(self.cd[ind].text_c, self.cd[r].text_c), begin=self.gd["stage-1"], v=v, cx=cx, ty=ty, suop=suop, lr=(self.cd[r].level_t, self.cd[r].level_t), pos=pos, n=self.gd["active"], act=act, baind=baind, nr=nr, dis=diss, csop=csop, atk=self.gd["attacking"][1], nmop=nmop, trop=trop, lvup=lvup, refr=refr, sav=savs, rst=rst, lvc=(lvc, self.cd[lvc].card), z=z, cnc=cnc, dmg=dmg, pp=self.gd["pp"], tr=(self.cd[ind].trait_t, self.cd[r].trait_t), lvop=lvop, brt=brt, std=std, passed=passed, opp=opp,chg=chg)
							if player == "2":
								if ind in self.pd[ind[-1]]["marker"]:
									mm = len(self.pd[ind[-1]]["marker"][ind])
								nn = -1
								if ind in stage:
									nn = stage.index(ind)
								astock = 0
								if self.gd["markerstock"]:
									if any(name in self.gd["astock"] for name in self.cd[ind].name_t.split("\n")):
										for name in self.cd[ind].name_t.splt("\n"):
											if name in self.gd["astock"]:
												astock = len(self.gd["astock"][name][player])
									else:
										astock = len(self.gd["astock"][player])
								if not ab.req(a=item[0], x=len(self.pd[player]["Stock"]) + astock, m=mm, ss=ss, nn=nn, h=h, my=my, wr=wr, cx=cx):
									ability = []
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

								if "a1" in ability:
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
								elif "played" in ability:
									self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -9
								elif "at" in ability:
									if item[1] == -1:
										self.cd[ind].text_c[self.cd[ind].text_c.index(item)][1] = -31

								if "pass" in item and ability[0] == -38:
									ability[0] = int(item[item.index("pass") + 1])
									ability[2] = str(item[item.index("pass") + 2])
									ability.append("passed")
								elif "pass" in item and "do" in ability:
									inx1 = ability.index("do") + 1
									if ability[inx1][0] == -38:
										ability[inx1][0] = int(item[item.index("pass") + 1])
										ability[inx1][2] = str(item[item.index("pass") + 2])
										ability[inx1].append("passed")
							if ind == wait and ability and "encore" in ability:
								if not self.gd["no_encore"][wait[-1]]:
									if "StockWaiting" in ability:
										wtar = ability[ability.index("StockWaiting") + 1].split("_")
										swtext = ""
										if len(self.pd[wait[-1]]["Stock"]) >= ability[0]:
											swtext += "S"
										if "Character" in wtar[1]:
											if len([s for s in self.pd[wait[-1]]["Center"] + self.pd[wait[-1]]["Back"] if s != ""]) > int(wtar[0]):
												swtext += "Waiting"
										if "SWaiting" in swtext and swtext not in encore:
											encore.append(swtext)
											self.gd["encore_effect"] = list(ability)
									if "Character" in ability:
										if len([s for s in self.pd[wait[-1]]["Hand"] if self.cd[s].card == "Character"]) > 0 and "Character" not in encore:
											encore.append("Character")
									if "Climax" in ability:
										if len([s for s in self.pd[wait[-1]]["Hand"] if self.cd[s].card == "Climax"]) > 0 and "Climax" not in encore:
											encore.append("Climax")
									if "TraitN" in ability:
										traits = ability[ability.index("TraitN") + 1].split("_")
										if len([s for s in self.pd[wait[-1]]["Hand"] if any(trait in self.cd[s].trait_t for trait in traits[:-1]) or traits[-1] in self.cd[s].name_t]) > 0:
											if "TraitN" not in encore:
												encore.append("TraitN")
												encore.append("TraitN")

											for trait in traits:
												if trait not in encore[encore.index("TraitN") + 1]:
													encore[encore.index("TraitN") + 1] += f"_{trait}"
									if "Trait" in ability:
										traits = ability[ability.index("Trait") + 1].split("_")
										if len([s for s in self.pd[wait[-1]]["Hand"] if any(trait in self.cd[s].trait_t for trait in traits)]) > 0:
											if "Trait" not in encore:
												encore.append("Trait")
												encore.append("Trait")

											for trait in traits:
												if trait not in encore[encore.index("Trait") + 1]:
													encore[encore.index("Trait") + 1] += f"_{trait}"
									if "Clock" in ability and "Clock" not in encore:
										encore.append("Clock")
									if "Stock" in ability and len(self.pd[wait[-1]]["Stock"]) >= ability[0] and f"Stock{ability[0]}" not in encore:
										encore.append(f"Stock{ability[0]}")
							if ability and "encore" not in ability:
								stack = [ind, ability, item[0], r, pos, self.gd["phase"], card.text_c.index(item), self.gd["pp"]]
								if ability and stack not in self.gd["stack"][ind[-1]]:
									self.gd["stack"][ind[-1]].append(stack)

					if len(encore) > 2:
						for item in self.cd[wait].text_c:
							if item[0].startswith(cont_ability) and item[1] != 0 and item[1] > -9:
								eff = ab.cont(item[0])
								if "no_encore_self" in eff:
									encore = []

					if wait and player in wait[-1] and ind == wait and len(encore) > 2:
						stack = [wait, encore, "[AUTO] Encore", wait, pos, self.gd["phase"], 0, self.gd["pp"]]
						if stack not in self.gd["stack"][wait[-1]]:
							self.gd["stack"][wait[-1]].append(stack)
		self.shelve_save()

		if stacks:
			Clock.schedule_once(self.stack_ability)

	def stack_ability(self, *args):
		if self.gd["reveal_ind"]:
			if not self.cd[self.gd["reveal_ind"]].back and self.pd[self.gd["reveal_ind"][-1]]["Library"][-1] == self.gd["reveal_ind"]:
				self.cd[self.gd["reveal_ind"]].show_back()
			self.gd["reveal_ind"] = ""
		self.shelve_save()
		if self.gd["active"] == "1":
			self.gd["movable"] = []

		if self.gd["rev"]:
			player = self.gd["opp"]
		else:
			player = self.gd["active"]

		if self.gd["auto_effect"] in self.gd["stack"][player]:
			if self.gd["perform_both"]:
				self.gd["perform_both"] = False

			if "change [" in self.gd["auto_effect"][2].lower() and self.gd["payed"]:
				self.check_auto_ability(chg=self.gd["auto_effect"][0],stacks=False)
			self.gd["stack"][player].remove(self.gd["auto_effect"])
			if self.net["game"] and player == "1" and self.gd["ability_doing"] != "confirm" and not self.gd["oppchoose"]:
				self.net["var"] = list(self.net["act"])
				self.net["var1"] = "auto"
				self.gd["oppchoose"] = False
				self.mconnect("act")
				return False
		elif self.net["game"] and ("ACT" in self.gd["ability_trigger"] or "Event" in self.gd["ability_trigger"] or "Play" in self.gd["ability_trigger"]) and self.gd["ability_trigger"] and player == "1" and player == self.gd["ability_trigger"].split("_")[1][-1] and not self.net["send"]:
			if "ACT" in self.gd["ability_trigger"]:
				self.net["var1"] = "act"
			elif "Event" in self.gd["ability_trigger"]:
				self.net["var1"] = "event"
			self.net["var"] = list(self.net["act"])
			if not self.poptext:
				Clock.schedule_once(partial(self.popup_text, "waitingser"))
			self.mconnect("act")
			return False

		if self.net["game"] and player == "1" and self.net["varlvl"] and not self.net["lvlsend"]:
			self.net["var"] = list(self.net["varlvl"])
			self.net["var1"] = "lvl"
			if not self.poptext:
				Clock.schedule_once(partial(self.popup_text, "waitingser"))
			self.mconnect("lvl")
			return False

		if self.gd["resonance"][0]:
			for _ in self.gd["resonance"][1]:
				if not self.cd[_].back:
					self.cd[_].show_back()
			self.gd["resonance"] = [False, [], 0]
			self.hand_size(player)

		if len(self.pd[player]["Res"]) > 0:
			if (self.gd["per_poped"][-1] and "Event" in self.gd["ability_trigger"]) or "Play" in self.gd["ability_trigger"]:
				pass
			else:
				self.event_done()

		self.auto_check(player)

		if self.net["game"] and player == "1" and self.gd["oppchoose"]:
			self.gd["oppchoose"] = False

		if "do" in self.gd["ability_effect"]:
			if self.gd["do"][0] > 0:
				self.gd["done"] = True
				Clock.schedule_once(self.ability_effect)
				return
			else:
				self.gd["ability_effect"].remove("do")

		if len(self.pd[player]["Clock"]) >= 7:
			self.gd["level_up_trigger"] = "stack"
			Clock.schedule_once(partial(self.level_up, player), move_dt_btw)
			return False

		if self.gd["per_poped"][-1]:
			self.gd["ability_effect"].append("perform")
			if self.net["game"] and "2" in player:
				if self.gd["show_wait_popup"]:
					Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
				self.mconnect("phase")
			else:
				Clock.schedule_once(self.ability_effect)
		elif len(self.gd["stack"][player]) > 1 and "1" in player:
			for item in self.gd["stack"]["1"]:
				if item[0] == "1":
					Clock.schedule_once(partial(self.stack_resolve, self.gd["stack"]["1"].index(item)))
					return False
			Clock.schedule_once(self.stack_popup, popup_dt)
			return False
		elif len(self.gd["stack"][player]) > 0 and "2" in player:
			if self.net["game"]:
				if self.gd["show_wait_popup"]:
					Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
				self.mconnect("phase")
			elif self.gd["com"]:
				self.stack_resolve("0", player)
		elif len(self.gd["stack"][player]) > 0:
			self.stack_resolve("0", player)
		elif len(self.gd["stack"][player]) <= 0 and not self.gd["rev"]:
			if not self.gd["check_reserve"] and len(self.gd["reserve"][player])>0:
				self.gd["check_reserve"] = True
				Clock.schedule_once(self.stack_ability)
			else:
				self.gd["check_reserve"] = False
				self.gd["rev"] = True
				Clock.schedule_once(self.stack_ability)
		elif len(self.gd["stack"][player]) <= 0 and self.gd["rev"]:
			if not self.gd["check_reserve"] and len(self.gd["reserve"][player])>0:
				self.gd["check_reserve"] = True
				Clock.schedule_once(self.stack_ability)
			else:
				self.gd["check_reserve"] = False
				self.gd["rev"] = False
				self.clear_ability()
				self.shelve_save()
				if self.gd["pp"] < 0:
					Clock.schedule_once(self.beginning_phase)
				elif "Battle" in self.gd["phase"]:
					Clock.schedule_once(self.attack_phase_done)
				elif "Damage" in self.gd["phase"]:
					self.gd["phase"] = "Battle"
					if self.gd["attacking"][1] == "f":
						Clock.schedule_once(self.beginning_phase)
					else:
						Clock.schedule_once(self.attack_phase_done)
				elif "Attack" in self.gd["phase"]:
					if "Attack" in self.gd["skip"]:
						self.gd["pp"] = 9
					if self.gd["pp"] >= 9:
						Clock.schedule_once(self.attack_phase_end)
					else:
						Clock.schedule_once(self.attack_phase)
				elif "Declaration" in self.gd["phase"]:
					Clock.schedule_once(self.attack_declaration_done)
				elif "Counter" in self.gd["phase"]:
					Clock.schedule_once(self.counter_step_done)
				elif "Trigger" in self.gd["phase"]:
					if self.gd["trigger"] >= 0:
						Clock.schedule_once(self.trigger_effect)
					else:
						Clock.schedule_once(self.trigger_step_done)
				elif "Climax" in self.gd["phase"]:
					Clock.schedule_once(self.climax_phase_done)
				elif "Main" in self.gd["phase"]:
					Clock.schedule_once(self.play_card_done)
				elif "Encore" in self.gd["phase"]:
					Clock.schedule_once(self.encore_start)
				elif "Clock" in self.gd["phase"]:
					if self.gd["clock_done"] and self.gd["chosen"]:
						Clock.schedule_once(self.clock_phase_end)
					elif not self.gd["clock_done"] and not self.gd["chosen"]:
						Clock.schedule_once(self.clock_phase)
					else:
						Clock.schedule_once(self.clock_phase_done)
				elif "End" in self.gd["phase"]:
					Clock.schedule_once(self.end_phase_end)

	def stack_return(self, btn, *args):
		self.sd["popup"]["popup"].dismiss()
		self.clear_ability()
		self.gd["ability_effect"] = []
		self.popup_clr()
		self.gd["stack_return"] = True
		Clock.schedule_once(self.stack_popup, popup_dt)

	def stack_resolve(self, btn, player="1", *args):
		self.gd["stack_pop"] = False
		if self.gd["popup_done"][0]:
			self.sd["popup"]["popup"].dismiss()
			self.popup_clr()

		for nx in self.gd["sn"]:
			for snx in self.gd["sn"][nx]:
				for nnx in range(len(self.gd["sn"][nx][snx])):
					self.cd[self.gd["sn"][nx][snx][nnx][0]].update_text()
					self.cpop[self.gd["sn"][nx][snx][nnx][1]].update_text()
		for item in self.gd["so"]:
			self.cpop[item].update_text()
		self.gd["so"] = []
		self.gd["sn"] = {}

		self.gd["payed"] = False


		try:
			auto = int(btn.cid)
		except AttributeError:
			auto = int(btn)

		self.gd["auto_effect"] = list(self.gd["stack"][player][auto])
		if self.gd["waiting_cost"][1]:
			self.gd["ability_trigger"] = f"Play_{self.gd['auto_effect'][0]}"
		elif "TriggerIcon" in self.gd["auto_effect"]:
			self.gd["ability_trigger"] = f"AUTO_{self.gd['auto_effect'][0]}_Trigger"
		else:
			self.gd["ability_trigger"] = f"AUTO_{self.gd['auto_effect'][0]}"
		self.gd["ability"] = str(self.gd["auto_effect"][2])
		self.gd["effect"] = list(self.gd["auto_effect"][1])

		if self.gd["waiting_cost"][1]:
			self.gd["pay"] = []
			self.gd["payed"] = False
		elif "TriggerIcon" not in self.gd["auto_effect"]:
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
			self.net["act"] = ["a", str(self.gd["auto_effect"][0]), auto, [], [], 0, -1]
			if self.gd["payed"]:
				self.net["act"][5] = 1
			if self.gd["waiting_cost"][1]:
				self.net["act"][0] = "p"

		if self.net["game"] and player == "2" and not self.net["act"][5] and "encore" in self.gd["effect"]:
			Clock.schedule_once(self.ability_effect)
		else:
			Clock.schedule_once(self.ability_event)

	def check_more(self, eff, ind, p=""):
		_ = True

		if not p:
			p = ind[-1]

		if "opp" in eff:
			if p == "1":
				p = "2"
			elif p == "2":
				p = "1"

		if eff[0] == -1:
			if "Center" in eff:
				eff[0] = len([r for r in self.pd[p]["Center"] if r!=""])
			elif "Back" in eff:
				eff[0] = len([r for r in self.pd[p]["Back"] if r!=""])
			else:
				eff[0] = len([r for r in self.pd[p]["Center"] + self.pd[p]["Back"] if r != ""])

		if "HandvsOpp" in eff:
			if ind[-1] == "1":
				op = "2"
			elif ind[-1] == "2":
				op = "1"
			vs = len(self.pd[op]["Hand"])
		else:
			vs = eff[0]

		if "=" in eff and len(self.cont_times(eff, self.cont_cards(eff, ind), self.cd)) != vs:
			_ = False
		elif "fewer" in eff and len(self.cont_times(eff, self.cont_cards(eff, ind), self.cd)) >= vs:
			_ = False
		elif "lower" in eff and len(self.cont_times(eff, self.cont_cards(eff, ind), self.cd)) > vs:
			_ = False
		elif "lower" not in eff and len(self.cont_times(eff, self.cont_cards(eff, ind), self.cd)) < vs:
			_ = False

		return _

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

		for auto in list(self.gd["stack"][p]):
			if "pay" in auto[1] and "oppmay" in auto[1]:
				if p == "1":
					o = "2"
				elif p == "2":
					o = "1"
				auto1 = list(auto)
				auto1[1].remove("oppmay")
				self.gd["stack"][p].remove(auto)
				self.gd["stack"][o].append(auto1)
				continue

			if "Trigger" in auto[3] or "Play" in auto[3]:
				continue

			if auto[5] != self.gd["phase"]:
				self.auto_reserve(p, auto, False)
				continue

			if auto[7] != self.gd["pp"]:
				self.auto_reserve(p, auto, False)
				continue

			stage = list(self.pd[p]["Center"] + self.pd[p]["Back"])
			autostock = len(self.pd[p]["Stock"])
			if "do" in auto[1]:
				do = auto[1][auto[1].index("do") + 1]
			else:
				do = []

			if "done" in auto[1]:
				done = auto[1][auto[1].index("done") + 1]
			else:
				done = []

			if "multicond" in auto[1]:
				multicond = auto[1][auto[1].index("multicond") + 1]
			else:
				multicond = []

			aa = 1
			if self.gd["nomay"] and "may" in auto[1] and auto[0][-1] == self.gd["active"]:
				aa = -1
			elif "shift" in auto[1]:
				aa = 0
				if len(self.pd[auto[0][-1]]["Level"]) >= auto[1][auto[1].indext("shift") + 1]:
					auto[1].extend("Hand", f"Colour_{self.cd[auto[0]].mcolour}")
					if len(self.cond_time(auto[1], self.cond_cards(auto[1], auto[0]), self.cd)) > 0:
						aa = 2
			elif "rescue" in auto[1] or "revive" in auto[1]:
				if "Waiting" not in self.cd[auto[3]].pos_new:
					aa = 0
			elif "encore" in auto[1]:
				if self.gd["no_encore"][p]:
					self.gd["stack"][p].remove(auto)
				elif "Waiting" not in self.cd[auto[0]].pos_new and "Waiting" in auto[4][1]:
					aa = 0
				else:
					if "Stock1" in auto[1] and autostock < 1:
						aa = 0
					if "Stock2" in auto[1] and autostock < 2:
						aa = 0
					if "Stock3" in auto[1] and autostock < 3:
						aa = 0
					if ("Character" in auto[1] or "Climax" in auto[1] or "Trait" in auto[1] or "TraitN" in auto[1]) and len(self.pd[p]["Hand"]) < 1:
						aa = 0
					if len(self.pd[p]["Hand"]) > 0:
						if "TraitN" in auto[1] and len([s for s in self.pd[p]["Hand"] if auto[1][auto[1].index("TraitN") + 1].split("_")[:-1] in self.cd[s].trait_t or auto[1][auto[1].index("TraitN") + 1].split("_")[-1] in self.cd[s].name_t]) < 1:
							aa = 0
						elif "Trait" in auto[1] and len([s for s in self.pd[p]["Hand"] if any(tt in self.cd[s].trait_t for tt in auto[1][auto[1].index("Trait") + 1].split("_"))]) < 1:
							aa = 0
						elif "Character" in auto[1] and len([s for s in self.pd[p]["Hand"] if self.cd[s].card == "Character"]) < 1:
							aa = 0
						elif "Climax" in auto[1] and len([s for s in self.pd[p]["Hand"] if self.cd[s].card == "Climax"]) < 1:
							aa = 0
					else:
						aa = 0
			elif ("power" in auto[1] or "soul" in auto[1] or "level" in auto[1] or "cost" in auto[1]) and auto[1][0] == 0 and auto[0] not in stage:
				aa = 0
			elif (("move" in auto[1] and auto[1][0] == 1) or ("do" in auto[1] and "move" in auto[1][-1] and auto[1][-1][0] == 1) or ("do" in auto[1] and "do" in auto[1][-1] and "move" in auto[1][-1][-1] and auto[1][-1][-1][0] == 1)) and auto[0] not in stage:
				aa = 0
			elif any(stat in auto[1] for stat in ("Rest", "Stand", "Reversed")) and "more" not in auto[1]:
				if "Center" in auto[1]:
					stage1 = list(self.pd[p]["Center"])
				else:
					stage1 = list(self.pd[p]["Center"] + self.pd[p]["Back"])

				status = [self.cd[s].status for s in stage1]

				if "other" in auto[1]:
					if auto[0] in stage1:
						status[stage1.index(auto[0])] = ""
				if "Rest" in auto[1]:
					if auto[1][0] == 0 and "Rest" in status:
						aa = 0
			elif ("pay" in auto[1] and "this" in auto[1][auto[1].index("do") + 1]) or "this" in auto[1]:
				if "alarmed" in auto[1]:
					if "Clock" not in self.cd[auto[0]].pos_new:
						aa = 0
				else:
					if "Center" not in self.cd[auto[0]].pos_new and "Back" not in self.cd[auto[0]].pos_new:
						aa = 0
			elif "hander" in auto[1] or ("do" in auto[1] and "pay" in auto[1] and "hander" in auto[1][auto[1].index("do") + 1]):
				if "Climax" in auto[1] or ("do" in auto[1] and "pay" in auto[1] and "Climax" in auto[1][auto[1].index("do") + 1]) and len(self.pd[p]["Climax"]) < 1:
					aa = 0
				elif "hander" in auto[1] and auto[1][0] == 0:
					if self.cd[auto[0]].pos_new != auto[4][1]:
						aa = 0
					elif "Memory" in auto[1] and "Memory" not in self.cd[auto[0]].pos_new:
						aa = 0
					elif "Memory" not in auto[1] and auto[0] not in stage:
						aa = 0
				elif "do" in auto[1] and "pay" in auto[1] and "hander" in auto[1][auto[1].index("do") + 1] and auto[1][auto[1].index("do") + 1][0] == 0:
					if self.cd[auto[0]].pos_new != auto[4][1]:
						aa = 0
					elif "Memory" in auto[1][auto[1].index("do") + 1] and "Memory" not in self.cd[auto[0]].pos_new:
						aa = 0
					elif "Memory" not in auto[1][auto[1].index("do") + 1] and auto[0] not in stage:
						aa = 0
			elif "memorier" in auto[1] or ("do" in auto[1] and "pay" in auto[1] and "memorier" in auto[1][auto[1].index("do") + 1]):
				if "memorier" in auto[1] and auto[1][0] == 0:
					if self.cd[auto[0]].pos_new != auto[4][1]:
						aa = 0
				elif "do" in auto[1] and "pay" in auto[1] and "memorier" in auto[1][auto[1].index("do") + 1] and auto[1][auto[1].index("do") + 1][0] == 0:
					if self.cd[auto[0]].pos_new != auto[4][1]:
						aa = 0
			elif "marker" in auto[1] or ("do" in auto[1] and "pay" in auto[1] and "marker" in auto[1][auto[1].index("do") + 1]):
				if "Center" not in self.cd[auto[0]].pos_new and "Back" not in self.cd[auto[0]].pos_new:
					aa = 0
				elif "marker" in auto[1] and "ID=" in auto[1][2]:
					if not self.cd[auto[1][2].split("_")[1]].wmarker:
						aa = 0
				elif "do" in auto[1] and "pay" in auto[1] and "marker" in auto[1][auto[1].index("do") + 1] and "ID=" in auto[1][auto[1].index("do") + 1][2]:
					if not self.cd[auto[1][auto[1].index("do") + 1][2].split("_")[1]].wmarker:
						aa = 0
			elif "heal" in auto[1] or ("do" in auto[1] and "pay" in auto[1] and "heal" in auto[1][auto[1].index("do") + 1]):
				if len(self.pd[auto[0][-1]]["Clock"]) <= 0:
					aa = 0
				if "may" in auto[1]:
					aa = 1
			elif "pay" in auto[1] and any(abl in auto[1][auto[1].index("do") + 1] for abl in ("decker", "reverser", "stocker", "memorier", "clocker")) and auto[1][-1][0] == -3:
				opp = auto[1][auto[1].index("do") + 1][auto[1][auto[1].index("do") + 1].index("target") + 1]
				if opp != "" and self.cd[opp].pos_new[:-1] in ("Center", "Back"):  
					aa = 1
				else:
					aa = 0
			elif "pay" in auto[1] and "discard" in auto[1][auto[1].index("do") + 1] and "upto" not in auto[1][auto[1].index("do") + 1]:
				if len(self.cont_times([auto[1][auto[1].index("do") + 1][2].split("_")[0], "_".join(auto[1][auto[1].index("do") + 1][2].split("_")[1:])], self.pd[p]["Hand"], self.cd)) < auto[1][auto[1].index("do") + 1][1]:
					aa = 0
			elif "Middle" in auto[1] or ("pay" in auto[1] and "do" in auto[1] and "Middle" in auto[1][auto[1].index("do") + 1]):
				if self.pd[auto[0][-1]]["Center"][1] == "":
					aa = 0
			elif "turn" in auto[1]:
				if self.gd["turn"] == auto[1][1]:
					aa = 2
				else:
					aa = 0
			elif "more" in auto[1]:
				aa = 2
				if not self.check_more(auto[1], auto[0], p):
					aa = 0
			elif "alarm" in auto[1]:
				aa = 0
				if len(self.pd[p]["Clock"]) > 0 and auto[0] == self.pd[p]["Clock"][-1]:
					aa = 4
			elif "battleopp" in auto[1]:
				aa = 2
				attk = self.gd["attacking"][0]
				if attk[-1] == "1":
					opp = "2"
				elif attk[-1] == "2":
					opp = "1"
				if "C" in self.gd["attacking"][4]:
					deff = self.pd[opp]["Center"][self.gd["attacking"][3]]
				elif "B" in self.gd["attacking"][4]:
					deff = self.pd[opp]["Back"][self.gd["attacking"][3]]

				if auto[0] == attk:
					bp = attk
					bo = deff
				else:
					bp = deff
					bo = attk

				if "Level" in auto[1]:
					lv = auto[1][auto[1].index("Level") + 1]
					if lv == "x":
						xeff = []
						if "xName=" in auto[1]:
							xeff.extend(["Name=", auto[1][auto[1].index("xName=") + 1]])
						if "xWaiting" in auto[1]:
							xeff.extend(["Waiting"])

						lv = len(self.cont_times(xeff, self.cont_cards(xeff, bp), self.cd))
					if "lower" in auto[1] and self.cd[bo].level_t > lv:
						aa = 0
					elif "lower" not in auto[1] and self.cd[bo].level_t < lv:
						aa = 0
			elif "atkpwrdif" in auto[1]:
				aa = 0
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
						aa = 2
			elif "atkpwrchk" in auto[1]:
				aa = 0
				if "self" in auto[1]:
					if auto[1][0] == -2:
						stage1 = [s for s in stage if s != ""]
						if auto[0] in stage1:
							stage1.remove(auto[0])
						if "lower" in auto[1] and all(self.cd[ind].power_t < self.cd[auto[0]].power_t for ind in stage1):
							aa = 2
						elif "lower" not in auto[1] and all(self.cd[ind].power_t > self.cd[auto[0]].power_t for ind in stage1):
							aa = 2
			elif "experience" in auto[1]:
				aa = 0
				if "Name=" in auto[1]:
					if len([nn for nn in self.pd[p]["Level"] if auto[1][auto[1].index("Name=") + 1] in self.cd[nn].name_t]) >= auto[1][auto[1].index("experience") + 1]:
						aa = 2
				elif "Trait" in auto[1]:
					if len([nn for nn in self.pd[p]["Level"] if any(tr in self.cd[nn].trait_t for tr in auto[1][auto[1].index("Trait") + 1].split("_"))]) >= auto[1][auto[1].index("experience") + 1]:
						aa = 2
				elif "Colour" in auto[1]:
					if len([nn for nn in self.pd[p]["Level"] if any(tr.lower() in self.cd[nn].colour for tr in auto[1][auto[1].index("Colour") + 1].split("_"))]) >= auto[1][auto[1].index("experience") + 1]:
						aa = 2
				else:
					if sum([self.cd[lv].level_t for lv in self.pd[p]["Level"] if lv != ""]) >= auto[1][auto[1].index("experience") + 1]:
						aa = 2
			elif "markers" in auto[1] and "numbers" not in auto[1]:
				aa = 2
				markers = 0
				if auto[0] in self.pd[auto[0][-1]]["marker"]:
					markers = len(self.pd[auto[0][-1]]["marker"][auto[0]])

				if "lower" in auto[1] and markers > auto[1][auto[1].index("markers") + 1]:
					aa = 0
				elif "lower" not in auto[1] and markers < auto[1][auto[1].index("markers") + 1]:
					aa = 0
			elif "opposite" in auto[1]:  
				aa = 2
				if "Center" not in self.cd[auto[0]].pos_new:
					aa = 0
				else:
					if auto[0][-1] == "1":
						op = "2"
					elif auto[0][-1] == "2":
						op = "1"
					opp = self.pd[op]["Center"][self.m[int(self.cd[auto[0]].pos_new[-1])]]
					if opp == "":
						aa = 0
					elif "OPlevel" in auto[1]:
						if "OP==" in auto[1] and self.cd[opp].level_t != auto[1][auto[1].index("OPlevel") + 1]:
							aa = 0
						elif "OPlower" in auto[1] and self.cd[opp].level_t > auto[1][auto[1].index("OPlevel") + 1]:
							aa = 0
						elif "OPlower" not in auto[1] and self.cd[opp].level_t < auto[1][auto[1].index("OPlevel") + 1]:
							aa = 0
					elif "OPtraits" in auto[1]:
						if "OPlower" in auto[1] and len([t for t in self.cd[opp].trait_t if t != ""]) > auto[1][auto[1].index("OPtraits") + 1]:
							aa = 0
						elif "OPlower" not in auto[1] and len([t for t in self.cd[opp].trait_t if t != ""]) < auto[1][auto[1].index("OPtraits") + 1]:
							aa = 0
			elif "stage" in auto[1]:
				aa = 2
				if "Center" in auto[1] and "Center" not in self.cd[auto[0]].pos_new:
					aa = 0
				elif "Memory" in auto[1] and "Memory" not in self.cd[auto[0]].pos_new:
					aa = 0
			elif "plevel" in auto[1]:
				aa = 0
				if "antilvl" in auto[1]:
					caa = auto[1][auto[1].index("antilvl") + 1]
					if self.cd[caa].level_t > len(self.pd[caa[-1]]["Level"]):
						aa = 2
				elif "==" in auto[1]:
					if len(self.pd[auto[0][-1]]["Level"]) == auto[1][1]:
						aa = 2
				elif len(self.pd[auto[0][-1]]["Level"]) >= auto[1][1]:
					aa = 2
			elif "souls" in auto[1]:
				aa = 2
				if "lower" in auto[1] and self.cd[auto[0]].soul_t > auto[1][auto[1].index("souls") + 1]:
					aa = 0
				elif "lower" not in auto[1] and self.cd[auto[0]].soul_t < auto[1][auto[1].index("souls") + 1]:
					aa = 0

			if "Stage" in auto[1] and "Open" in auto[1]:
				o = p
				if "Opp" in auto[1]:
					if p == "1":
						o = "2"
					elif p == "2":
						o = "1"
				if "Center" in auto[1]:
					stage1 = [s for s in self.pd[o]["Center"] if s == ""]
				elif "Back" in auto[1]:
					stage1 = [s for s in self.pd[p]["Back"] if s == ""]
				else:
					stage1 = [s for s in self.pd[o]["Center"] + self.pd[p]["Back"] if s == ""]

				if len(stage1) < 1:
					a = 0

			if not aa and "dont" in auto[1]:
				do = auto[1][auto[1].index("dont") + 1]
				aa = 2

			if aa > 1:
				self.gd["stack"][p].remove(auto)
				if aa == 4:
					if "do" in do:
						do.insert(do.index("do"), "alarmed")
					else:
						do.append("alarmed")
				auto[1] = do
				if done:
					auto[1].extend(["done", done])
				self.gd["stack"][p].append(auto)
				self.gd["auto_recheck"] = True
				break
			elif aa < 0:
				self.auto_reserve(p, auto, False)
			elif not aa:
				if multicond:
					self.gd["stack"][p].remove(auto)
					if aa == 4:
						multicond.insert(do.index("do"), "alarmed")
					auto[1] = multicond
					self.gd["stack"][p].append(auto)
					self.gd["auto_recheck"] = True
					break
				else:
					self.auto_reserve(p, auto)
				if done:
					auto[1] = done
					self.gd["stack"][p].append(auto)

			if not self.auto_check_pay(auto, s="auto") and "dont" not in auto[1]:
				self.auto_reserve(p, auto)

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

			if "Flip" in lst[1] or "MFlip" in lst[1]:
				if "Flip" in lst[1]:
					qty = lst[1][lst[1].index("Flip") + 1]
					st = lst[1][lst[1].index("Flip") + 2]
				elif "MFlip" in lst[1]:
					qty = lst[1][lst[1].index("MFlip") + 1]
					st = lst[1][lst[1].index("MFlip") + 2]

				if qty == 0:
					if st == "down" and self.cd[ind].back:
						return False
					elif st == "up" and not self.cd[ind].back:
						return False
					if "MFlip" in lst[1] and ind not in self.pd[p]["Memory"]:
						return False
			if "Swap" in lst[1]:
				if ind not in stage:
					return False
				else:
					stage1 = stage
					if "PCenter" in lst[1]:
						stage1 = list(self.pd[p]["Center"])
					elif "PBack" in lst[1]:
						stage1 = list(self.pd[p]["Back"])
					if "PStand" in lst[1] and len([s for s in stage1 if s != "" and self.cd[s].status == "Stand"]) < lst[1][lst[1].index("Swap") + 1]:
						return False
			if "Discard" in lst[1]:
				qty = lst[1][lst[1].index("Discard") + 1]
				if qty == 0 and ind not in self.pd[p]["Hand"]:
					return False
				elif qty == -10 and len(self.pd[p]["Hand"]) < 1:
					return False
				elif qty > 0:
					leff = []
					if "CName" in lst[1]:
						leff = ["CName", lst[1][lst[1].index("CName") + 1]]
					elif "Name=" in lst[1]:
						leff = ["Name=", lst[1][lst[1].index("Name=") + 1]]
					elif "Trait" in lst[1]:
						leff = ["Trait", lst[1][lst[1].index("Trait") + 1]]
					elif "TriggerCX" in lst[1]:
						leff = ["TriggerCX", lst[1][lst[1].index("TriggerCX") + 1]]
					elif "ColourCx" in lst[1]:
						leff = ["ColourCx", lst[1][lst[1].index("ColourCx") + 1]]
					elif "CColourT" in lst[1]:
						leff = ["CColourT", lst[1][lst[1].index("CColourT") + 1]]
					elif "Character" in lst[1][lst[1].index("Discard") + 2] or "Climax" in lst[1][lst[1].index("Discard") + 2]:
						leff = [lst[1][lst[1].index("Discard") + 2]]
					if len(self.pd[p]["Hand"]) < qty:
						return False
					elif len(self.cont_times(leff, self.pd[p]["Hand"], self.cd)) < qty:
						return False
			if "Salvage" in lst[1]:
				qty = lst[1][lst[1].index("Salvage") + 1]
				if qty > 0:
					leff = []
					if "CName" in lst[1]:
						leff = ["CName", lst[1][lst[1].index("CName") + 1]]
					elif "Name=" in lst[1]:
						leff = ["Name=", lst[1][lst[1].index("Name=") + 1]]
					elif "Trait" in lst[1]:
						leff = ["Trait", lst[1][lst[1].index("Trait") + 1]]
					elif "TriggerCX" in lst[1]:
						leff = ["TriggerCX", lst[1][lst[1].index("TriggerCX") + 1]]
					elif "ColourCx" in lst[1]:
						leff = ["ColourCx", lst[1][lst[1].index("ColourCx") + 1]]
					elif "CColourT" in lst[1]:
						leff = ["CColourT", lst[1][lst[1].index("CColourT") + 1]]
					elif "Character" in lst[1][lst[1].index("Salvage") + 2] or "Climax" in lst[1][lst[1].index("Salvage") + 2]:
						leff = [lst[1][lst[1].index("Salvage") + 2]]
					if len(self.pd[p]["Waiting"]) < qty:
						return False
					elif len(self.cont_times(leff, self.pd[p]["Waiting"], self.cd)) < qty:
						return False
			if "MDiscard" in lst[1]:
				qty = lst[1][lst[1].index("MDiscard") + 1]
				if qty == 0 and ind not in self.pd[p]["Memory"]:
					return False
				elif qty > 0:
					leff = []
					if "MCName" in lst[1]:
						leff = ["CName", lst[1][lst[1].index("MCName") + 1]]
					elif "MName=" in lst[1]:
						leff = ["Name=", lst[1][lst[1].index("MName=") + 1]]
					elif "MTrait" in lst[1]:
						leff = ["Trait", lst[1][lst[1].index("MTrait") + 1]]
					if len(self.pd[p]["Memory"]) < qty:
						return False
					elif len(self.cont_times(leff, self.pd[p]["Memory"], self.cd)) < qty:
						return False
			if "CXDiscard" in lst[1]:
				qty = lst[1][lst[1].index("CXDiscard") + 1]
				if qty == 0 and ind not in self.pd[p]["Climax"]:
					return False
				elif qty > 0:
					leff = []
					if "CXName=" in lst[1]:
						leff = ["Name=", lst[1][lst[1].index("CXName=") + 1]]
					if len(self.pd[p]["Climax"]) < qty:
						return False
					elif len(self.cont_times(leff, self.pd[p]["Climax"], self.cd)) < qty:
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
				if all(name not in self.cd[nn].name_t for nn in self.pd[p]["Hand"]):
					return False
			if "RevealMarker" in lst[1]:
				name = lst[1][lst[1].index("RevealMarker") + 1]
				if all(name not in self.cd[nn].name_t for nn in self.pd[p]["Hand"]):
					return False
			if "Reveal" in lst[1]:
				name = lst[1][lst[1].index("Reveal") + 1]
				if all(name not in self.cd[nn].name_t for nn in self.pd[p]["Hand"]):
					return False
			if "ClockH" in lst[1]:
				if len(self.pd[p]["Hand"]) < lst[1][lst[1].index("ClockH") + 1]:
					return False
				else:
					leff = []
					if "Name=" in lst[1]:
						leff = ["Name=", lst[1][lst[1].index("Name=") + 1]]
					if len(self.cont_times(leff, self.pd[p]["Hand"], self.cd)) < lst[1][lst[1].index("ClockH") + 1]:
						return False
			elif "ClockS" in lst[1]:
				if lst[1][lst[1].index("ClockS") + 1] == 0 and ind not in stage:
					return False
				elif lst[1][lst[1].index("ClockS") + 1] > 0 and len(self.cont_times(lst[1], stage, self.cd)) < lst[1][lst[1].index("ClockS") + 1]:
					return False
			elif "ClockW" in lst[1]:
				if len(self.pd[p]["Waiting"]) < lst[1][lst[1].index("ClockW") + 1]:
					return False
				elif "Trait" in lst[1] and len(self.cont_times(lst[1], stage, self.cd)) < lst[1][lst[1].index("ClockW") + 1]:
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
					if "BTrait" in lst[1]:
						b1 = [s for s in stage1 if s != "" and self.cd[s].status == "Stand" and lst[1][lst[1].index("Trait") + 1].split("_")[0] in self.cd[s].trait_t]
						b2 = [s for s in stage1 if s != "" and self.cd[s].status == "Stand" and lst[1][lst[1].index("Trait") + 1].split("_")[1] in self.cd[s].trait_t]
						if list(set(b1 + b2)) < qty:
							return False
					elif "Trait" in lst[1]:
						if len([s for s in stage1 if s != "" and self.cd[s].status == "Stand" and any(tt in self.cd[s].trait_t for tt in lst[1][lst[1].index("Trait") + 1].split("_"))]) < qty:
							return False
					elif "Name" in lst[1]:
						if len([s for s in stage1 if s != "" and self.cd[s].status == "Stand" and any(tt in self.cd[s].name_t for tt in lst[1][lst[1].index("Name") + 1].split("_"))]) < qty:
							return False
					elif "Text" in lst[1]:
						if len([s for s in stage1 if s != "" and self.cd[s].status == "Stand" and any(any(tt.lower() in text.lower() for text in self.cd[s].text_c) for tt in lst[1][lst[1].index("text") + 1].split("_"))]) < qty:
							return False
			elif "Marker" in lst[1]:
				qty = lst[1][lst[1].index("Marker") + 1]
				if ind in self.pd[ind[-1]]["marker"]:
					if len(self.pd[ind[-1]]["marker"]) < qty:
						return False
				else:
					return False
			if "Waiting" in lst[1]:
				if lst[1][lst[1].index("Waiting") + 1] == 0 and ind not in stage and ind not in self.pd[p]["Memory"]:
					return False
				elif lst[1][lst[1].index("Waiting") + 1] > 0:
					if "WOther" in lst[1] and len([s for s in stage if s != "" and s != ind]) < lst[1][lst[1].index("Waiting") + 1]:
						return False
					elif len([s for s in stage if s != ""]) < lst[1][lst[1].index("Waiting") + 1]:
						return False
					else:
						if "WTrait" in lst[1] and "WOther" in lst[1] and len([s for s in stage if s != "" and s != ind and any(tt in self.cd[s].trait_t for tt in lst[1][lst[1].index("WTrait") + 1].split("_"))]) < lst[1][lst[1].index("Waiting") + 1]:
							return False
						elif "WTrait" in lst[1] and len([s for s in stage if s != "" and any(tt in self.cd[s].trait_t for tt in lst[1][lst[1].index("WTrait") + 1].split("_"))]) < lst[1][lst[1].index("Waiting") + 1]:
							return False
						elif "WCenter" in lst[1] and "WOther" in lst[1] and len([s for s in self.pd[p]["Center"] if s != "" and s != ind]) < lst[1][lst[1].index("Waiting") + 1]:
							return False
						elif "WCenter" in lst[1] and len([s for s in self.pd[p]["Center"] if s != ""]) < lst[1][lst[1].index("Waiting") + 1]:
							return False
			elif "Stocker" in lst[1]:
				if lst[1][lst[1].index("Stocker") + 1] == 0 and ind not in stage:
					return False
				elif lst[1][lst[1].index("Stocker") + 1] > 0:
					if "Name=" in lst[1]:
						if len([s for s in stage if s != "" and lst[1][lst[1].index("Name=") + 1] in self.cd[s].name]) < lst[1][lst[1].index("Stocker") + 1]:
							return False
					elif len([s for s in stage if s != ""]) < lst[1][lst[1].index("Stocker") + 1]:
						return False
			elif "Memory" in lst[1]:
				if lst[1][lst[1].index("Memory") + 1] == 0 and ind not in stage:
					return False
			elif "Hander" in lst[1]:
				if lst[1][lst[1].index("Hander") + 1] == 0 and ind not in stage:
					return False
		return True

	def stack_popup(self, *args):
		self.popup_clr_button()

		self.gd["p_over"] = False
		self.gd["p_c"] = "auto"
		self.gd["stack_pop"] = True
		self.gd["popup_done"] = (True, False)
		self.sd["popup"]["popup"].title = "Triggered AUTO abilities"
		self.shelve_save()
		self.sd["popup"]["p_scv"].do_scroll_y = False
		self.sd["popup"]["stack"].clear_widgets()
		self.gd["sn"] = {}

		height = self.sd["card"][1] + self.sd["padding"] * 0.75
		xscat = (self.sd["padding"] + self.sd["card"][0]) * (starting_hand + 1) + self.sd["padding"] * 2

		self.sd["btn"]["label"].text = "Choose which AUTO ability to activate first."
		self.sd["btn"]["label"].text_size = (xscat * 0.9, None)
		self.sd["btn"]["label"].texture_update()

		r = len(self.gd["stack"]["1"])

		if r > 6:
			self.sd["popup"]["p_scv"].do_scroll_y = True
			yscv = height * (r - 0.5)
		elif r > 0:
			yscv = height * r
		else:
			yscv = height
		yscv += self.sd["padding"]

		yscat = yscv + self.sd["card"][1]
		title = self.sd["popup"]["popup"].title_size + self.sd["popup"]["popup"].separator_height + self.sd["btn"]["label"].texture.size[1] + self.sd["card"][1]
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
			self.cpop[item[0]].selected_c(False)
			self.cpop[item[0]].update_text()
			repl = ""
			if self.cpop[item[0]] in self.sd["popup"]["stack"].children:
				for xx in self.cpop.keys():
					if xx.endswith("0") and self.cpop[xx] not in self.sd["popup"]["stack"].children:
						self.sd["popup"]["stack"].add_widget(self.cpop[xx])
						if self.cd[item[0]].cid == "player":
							self.cpop[xx].import_data("player",self.gd["DLimg"])
						else:
							self.cpop[xx].import_data(sc[self.cd[item[0]].cid],self.gd["DLimg"])
						self.gd["so"].append(xx)
						repl = xx
						break
			else:
				repl = item[0]
				self.sd["popup"]["stack"].add_widget(self.cpop[item[0]])

			if self.cd[item[0]].name_t in self.gd["sn"] and item[2] in self.gd["sn"][self.cd[item[0]].name_t]:
				if item[0] not in self.gd["sn"][self.cd[item[0]].name_t][item[2]]:
					self.gd["sn"][self.cd[item[0]].name_t][item[2]].append((item[0], repl))
			elif self.cd[item[0]].name_t in self.gd["sn"] and item[2] not in self.gd["sn"][self.cd[item[0]].name_t]:
				self.gd["sn"][self.cd[item[0]].name_t][item[2]] = [(item[0], repl)]
			else:
				self.gd["sn"][self.cd[item[0]].name_t] = {}
				self.gd["sn"][self.cd[item[0]].name_t][item[2]] = [(item[0], repl)]

			if ("do" in item[1] and "revive" in item[1][-1]) or "revive" in item[1]:
				if item[3] == item[0]:
					self.sd["sbtn"][f"{inx}"].btn.text = f"Target:\tThis card\n{self.cardinfo.replaceMultiple(item[2], True)}"
				else:
					self.sd["sbtn"][f"{inx}"].btn.text = f"Target:\t\"{self.cd[item[3]].name_t}\"\n{self.cardinfo.replaceMultiple(item[2], True)}"
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
		self.sd["btn"]["field_btn"].center_x = xscat / 2. - self.sd["card"][0] / 4  
		self.sd["btn"]["field_btn"].y = self.sd["padding"] * 1.5

		self.sd["popup"]["p_scv"].y = self.sd["btn"]["field_btn"].y * 2.5 + self.sd["btn"]["field_btn"].size[1]
		self.sd["popup"]["p_scv"].scroll_y = 1

		self.sd["btn"]["label"].pos = (self.sd["padding"] / 2., self.sd["popup"]["p_scv"].y + yscv)  

		if self.gd["stack_return"]:
			self.gd["stack_return"] = False
			Clock.schedule_once(self.popup_delay, popup_dt)
		else:
			self.sd["popup"]["popup"].open()

	def level(self, *args):
		if "power" in self.gd["effect"]:
			inx = self.gd["effect"].index("power") + 1
		else:
			inx = 0
		idm = self.gd["ability_trigger"].split("_")[1]
		if self.gd["effect"][inx] > 0:
			for r in range(len(self.gd["target"])):
				temp = self.gd["target"].pop(0)
				if temp != "":
					self.cd[temp].level_c.append([self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"], self.gd["turn"]])
					self.cd[temp].update_level()
					if "extra" in self.gd["effect"]:
						self.gd["extra"].append(temp)
				if self.net["game"]:  
					self.net["act"][4].append(temp)
				if "power" in self.gd["effect"]:
					self.gd["target"].append(temp)
					if self.net["game"]:  
						self.net["act"][4].remove(temp)
		elif self.gd["effect"][inx] == 0:
			self.cd[idm].level_c.append([self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"], self.gd["turn"]])
			self.cd[idm].update_level()
		elif self.gd["effect"][inx] < 0:
			if self.gd["effect"][inx] == -1:
				for ind in self.pd[idm[-1]]["Center"] + self.pd[idm[-1]]["Back"]:
					if ind != "":
						self.cd[ind].level_c.append([self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"], self.gd["turn"]])
						self.cd[ind].update_level()
			elif self.gd["effect"][inx] == -2:
				for ind in self.pd[idm[-1]]["Center"] + self.pd[idm[-1]]["Back"]:
					if ind != "" and ind != idm:
						self.cd[ind].level_c.append([self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"], self.gd["turn"]])
						self.cd[ind].update_level()

		if "level" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("level")

		self.do_check(True)

	def power(self, dt=0, *args):
		idm = self.gd["ability_trigger"].split("_")[1]
		if self.gd["effect"][0] > 0:
			if self.gd["effect"][0] == 1:
				if "X" in self.gd["effect"]:
					stage = list(self.pd[idm[-1]]["Center"] + self.pd[idm[-1]]["Back"])
					tx = 0
					if "xName" in self.gd["effect"]:
						tx = len(self.cont_times(self.gd["effect"], stage, self.cd))
					elif "xlevel" in self.gd["effect"]:
						tx = self.cd[self.gd["target"][0]].level_t
					elif "xsoul" in self.gd["effect"]:
						tx = self.cd[self.gd["target"][0]].soul_t
					elif "xplevel" in self.gd["effect"]:
						tx = len(self.pd[idm[-1]]["Level"])
					elif "xReverse" in self.gd["effect"]:
						tx = len([s for s in stage if s != "" and self.cd[s].status == "Reverse"])
					self.gd["effect"][1] = tx * self.gd["effect"][1]
				elif "#" in self.gd["effect"]:
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
					if "save_name" in self.gd["effect"]:
						self.gd["save_name"] = [self.cd[temp].name, temp]
					self.cd[temp].power_c.append([self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"], self.gd["turn"]])
					self.cd[temp].update_power()
					if self.cd[temp].power_t <= 0:
						self.power_zero.append(temp)
				if self.net["game"]:  
					self.net["act"][4].append(temp)
			else:
				for r in range(len(self.gd["target"])):
					temp = self.gd["target"].pop(0)
					if "extra" in self.gd["effect"]:
						self.gd["extra"].append(temp)
					if temp != "" and self.gd["effect"][1] != 0:
						self.cd[temp].power_c.append([self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"], self.gd["turn"]])
						self.cd[temp].update_power()
						if self.cd[temp].power_t <= 0:
							self.power_zero.append(temp)
					if self.net["game"]:  
						self.net["act"][4].append(temp)
		elif self.gd["effect"][0] == 0:
			card = self.cd[idm]
			if any(st in card.pos_new for st in self.stage):
				if "random" in self.gd["effect"]:
					self.gd["effect"][1] = choice([s for s in range(self.gd["effect"][1], self.gd["effect"][self.gd["effect"].index("random") + 1] + 500, 500)])

				if "lvl" in self.gd["effect"]:
					if "opp" in self.gd["effect"]:
						if card.ind[-1] == "1":
							op = "2"
						else:
							op = "1"
						m = [2, 1, 0]
						opp = self.pd[op]["Center"][m[int(card.pos_new[-1])]]
						if opp != "" and self.cd[opp].level_t >= self.gd["effect"][self.gd["effect"].index("lvl") + 1]:
							card.power_c.append([self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"], self.gd["turn"]])
				elif "X" in self.gd["effect"]:
					times = 0
					if "xsoul" in self.gd["effect"]:
						times = card.soul_t
					elif "xplevel" in self.gd["effect"]:
						if "xopp" in self.gd["effect"]:
							if card.ind[-1] == "1":
								op = "2"
							elif card.ind[-1] == "2":
								op = "1"
							times = len(self.pd[op]["Level"])
						else:
							times = len(self.pd[card.ind[-1]]["Level"])
					elif "xopposite" in self.gd["effect"]:
						if card.ind[-1] == "1":
							op = "2"
						elif card.ind[-1] == "2":
							op = "1"
						_ = ""
						if "Center" in self.cd[idm].pos_new:
							_ = self.pd[op]["Center"][self.m[int(self.cd[idm].pos_new[-1])]]
						if _ != "":
							if "xlevel" in self.gd["effect"]:
								times = int(self.cd[_].level_t)
					card.power_c.append([self.gd["effect"][1] * times, self.gd["effect"][2], self.gd["ability_trigger"], self.gd["turn"]])
				elif "#" in self.gd["effect"]:
					ind = self.gd["ability_trigger"].split("_")[1]
					times = 0

					stage = self.cont_cards(self.gd["effect"], ind)

					if "Stock" in self.gd["effect"]:
						times = len(self.pd[idm[-1]]["Stock"])
					elif "Marker" in self.gd["effect"]:
						if "under" in self.gd["effect"]:
							if card.ind in self.pd[card.ind[-1]]["marker"]:
								times = len(self.pd[card.ind[-1]]["marker"][card.ind])
					elif "Traits" in self.gd["effect"]:
						times = []
						for t in stage:
							for tr in self.cd[t].trait_t:
								if tr not in times:
									times.append(tr)
						times = len(times)
					elif "Revealed" in self.gd["effect"]:
						times = len(self.gd["resonance"][1])
					else:
						times = len(self.cont_times(self.gd["effect"], stage, self.cd))

					card.power_c.append([self.gd["effect"][1] * times, self.gd["effect"][2], self.gd["ability_trigger"], self.gd["turn"]])
				else:
					card.power_c.append([self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"], self.gd["turn"]])
				card.update_power()
				if "extra" in self.gd["effect"]:
					self.gd["extra"].append(idm)
				if card.power_t <= 0:
					self.power_zero.append(card.ind)
		elif self.gd["effect"][0] < 0:
			if self.gd["effect"][0] == -1:
				if "xmill" in self.gd["effect"]:
					if "xanytrait" in self.gd["effect"]:
						for ind in self.gd["extra"]:
							self.gd["effect"][self.gd["effect"].index("Trait") + 1] = "_".join(list(set(self.cd[ind].trait_t + self.gd["effect"][self.gd["effect"].index("Trait") + 1].split("_"))))
						if self.gd["effect"][self.gd["effect"].index("xanytrait") + 1] == 1:
							pass
						elif self.gd["effect"][self.gd["effect"].index("xanytrait") + 1] == 2 and len(self.gd["effect"][self.gd["effect"].index("Trait") + 1]) == 2:
							self.gd["effect"][self.gd["effect"].index("Trait")] = "ATrait"
						self.gd["effect"].remove("xanytrait")
					elif "xsamelevel" in self.gd["effect"]:
						if len(self.gd["extra"]) == 1:
							if "CLevel" in self.gd["effect"]:
								self.gd["effect"][self.gd["effect"].index("CLevel") + 1] = int(self.cd[self.gd["extra"][0]].level_t)
					if "extra" not in self.gd["effect"]:
						self.gd["extra"] = []
					self.gd["effect"].remove("xmill")
				for ind in self.cont_times(self.gd["effect"], self.cont_cards(self.gd["effect"], idm), self.cd):
					if ind != "":
						self.cd[ind].power_c.append([self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"], self.gd["turn"]])
						self.cd[ind].update_power()
						if self.cd[ind].power_t <= 0:
							self.power_zero.append(ind)
			elif self.gd["effect"][0] == -2:
				for ind in self.pd[idm[-1]]["Center"] + self.pd[idm[-1]]["Back"]:
					if ind != "" and ind != idm:
						self.cd[ind].power_c.append([self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"], self.gd["turn"]])
						self.cd[ind].update_power()
						if self.cd[ind].power_t <= 0:
							self.power_zero.append(ind)
			elif self.gd["effect"][0] == -3:
				ind = self.gd["effect"][self.gd["effect"].index("target") + 1]
				if "extra" in self.gd["effect"]:
					self.gd["extra"].append(ind)
				self.cd[ind].power_c.append([self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"], self.gd["turn"]])
				self.cd[ind].update_power()
				if self.cd[ind].power_t <= 0:
					self.power_zero.append(ind)
			elif self.gd["effect"][0] == -10:
				ind = choice([s for s in self.pd[idm[-1]]["Center"] + self.pd[idm[-1]]["Back"] if s != ""])
				self.cd[ind].power_c.append([self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"], self.gd["turn"]])
				self.cd[ind].update_power()
				if self.cd[ind].power_t <= 0:
					self.power_zero.append(ind)
			elif self.gd["effect"][0] == -11:
				if idm[-1] == "1":
					opp = "2"
				elif idm[-1] == "2":
					opp = "1"
				ind = choice([s for s in self.pd[opp]["Center"] + self.pd[opp]["Back"] if s != ""])
				self.cd[ind].power_c.append([self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"], self.gd["turn"]])
				self.cd[ind].update_power()
				if self.cd[ind].power_t <= 0:
					self.power_zero.append(ind)
			elif self.gd["effect"][0] == -16:
				for ind in list(self.gd["extra"]):
					if "extra" not in self.gd["effect"]:
						self.gd["extra"].remove(ind)
					self.cd[ind].power_c.append([self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"], self.gd["turn"]])
					self.cd[ind].update_power()
					if self.cd[ind].power_t <= 0:
						self.power_zero.append(ind)

		if "power" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("power")

		for pind in reversed(self.power_zero):
			self.gd["no_cont_check"] = True
			self.send_to_waiting(pind)

		if self.gd["btrait"][1]:
			self.gd["btrait"] = ["", [], [], [], [], []]

		self.do_check(True)

	def reverser(self, *args):
		idm = self.gd["ability_trigger"].split("_")[1]
		ss = True
		if self.gd["effect"][0] == -3:
			if idm[-1] == "1" or (idm[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(self.gd["effect"][self.gd["effect"].index("target") + 1])
			self.gd["effect"][0] = 1
			ss = False
		elif self.gd["effect"][0] == 0:
			if idm[-1] == "1" or (idm[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(idm)
			self.gd["effect"][0] = 1
			ss = False

		for r in range(self.gd["effect"][0]):
			ind = self.gd["target"].pop(0)
			if self.net["game"] and idm[-1] == "1" and ss:
				self.net["act"][4].append(ind)
			if ind in self.emptycards:
				continue
			rev = True
			for text in self.cd[ind].text_c:
				if text[0].startswith(cont_ability) and text[1] != 0 and text[1] > -9:
					eff = ab.cont(text[0])
					if "no_reverse_auto_OC" in eff and idm[-1] != ind[-1] and self.cd[idm].card == "Character":
						rev = False
					elif "no_reverse" in eff:
						if "olevel" in eff:
							if ">p" in eff[eff.index("olevel") + 1] and self.cd[idm].level_t > len(self.pd[idm[-1]]["Level"]):
								rev = False
						elif "opcost" in eff or "oplevel" in eff:
							if ind[-1] == "1":
								op = "2"
							elif ind[-1] == "2":
								op = "1"

							opp = ""
							if "Center" in self.cd[ind].pos_new:
								opp = self.pd[op]["Center"][self.m[int(self.cd[ind].pos_new[-1])]]

							if opp:
								if "opcost" in eff:
									if "oplower" in eff and self.cd[opp].cost_t < eff[eff.index("opcost") + 1]:
										rev = False
								elif "oplevel" in eff:
									if ">p" in eff[eff.index("oplevel") + 1] and self.cd[opp].level_t > len(self.pd[opp[-1]]["Level"]):
										rev = False
									if "oplower" in eff and self.cd[opp].level_t < eff[eff.index("oplevel") + 1]:
										rev = False
						else:
							rev = False
			if rev:
				self.cd[ind].reverse()
			self.check_bodyguard()
			self.check_auto_ability(rev=[ind], stacks=False, rst=[ind])

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
		elif self.gd["effect"][inx] == "x":
			self.gd["effect"][inx] = int(self.gd["numbers"])

		if self.gd["effect"][inx] > 0:
			if "X" in self.gd["effect"]:
				if "xmill" in self.gd["effect"]:
					if "xsamelevel" in self.gd["effect"]:
						if len(self.gd["extra"]) == 1:
							self.gd["effect"][inx + 1] = int(self.cd[self.gd["extra"][0]].level_t)
						self.gd["effect"].remove("xsamelevel")
					elif "#soultrigger" in self.gd["effect"]:
						self.gd["effect"][inx + 1] = 0
						for _ in self.gd["extra"]:
							self.gd["effect"][inx + 1] += self.cd[_].trigger.count("soul")
						self.gd["effect"].remove("#soultrigger")
					if "extra" not in self.gd["effect"]:
						self.gd["extra"] = []
					self.gd["effect"].remove("xmill")
				self.gd["effect"].remove("X")
			for r in range(len(self.gd["target"])):
				temp = self.gd["target"].pop(0)
				if temp != "":
					if "extra" in self.gd["effect"]:
						self.gd["extra"].append(temp)

					self.cd[temp].soul_c.append([self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"], self.gd["turn"]])
					self.cd[temp].update_soul()
				if self.net["game"]:  
					self.net["act"][4].append(temp)
				if "power" in self.gd["effect"]:
					self.gd["target"].append(temp)
					if self.net["game"]:  
						self.net["act"][4].remove(temp)
		elif self.gd["effect"][inx] == 0:
			if any(st in self.cd[idm].pos_new for st in self.stage):
				self.cd[idm].soul_c.append([self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"], self.gd["turn"]])
				self.cd[idm].update_soul()
		elif self.gd["effect"][inx] < 0:
			if self.gd["effect"][inx] == -1:
				if "random" in self.gd["effect"]:
					self.gd["effect"][1 + inx] = choice([s for s in range(self.gd["effect"][1 + inx], self.gd["effect"][self.gd["effect"].index("random") + 1 + inx] + 1)])

				for ind in self.cont_times(self.gd["effect"], self.cont_cards(self.gd["effect"], idm), self.cd):
					if ind != "":
						self.cd[ind].soul_c.append([self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"], self.gd["turn"]])
						self.cd[ind].update_soul()
			elif self.gd["effect"][inx] == -19:
				cc = self.gd["effect"][self.gd["effect"].index("player") + 1]
				for ind in self.pd[cc]["Center"] + self.pd[cc]["Back"]:
					if ind != "":
						self.cd[ind].soul_c.append([self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"], self.gd["turn"]])
						self.cd[ind].update_soul()
			elif self.gd["effect"][0] == -16:
				if "xdeclare" in self.gd["effect"]:
					self.gd["effect"][1] = int(self.gd["numbers"])
				for ind in list(self.gd["extra"]):
					if "extra" not in self.gd["effect"]:
						self.gd["extra"].remove(ind)
					if ind != "":
						self.cd[ind].soul_c.append([self.gd["effect"][1], self.gd["effect"][2], self.gd["ability_trigger"], self.gd["turn"]])
						self.cd[ind].update_soul()

		if "soul" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("soul")

		self.do_check(True)


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
			for r in range(len(self.gd["target"])):
				temp = self.gd["target"].pop(0)
				if temp != "":
					if "extra" in self.gd["effect"]:
						self.gd["extra"].append(temp)
					self.cd[temp].trait_c.append([self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"], self.gd["turn"]])
					self.cd[temp].update_trait()
				if self.net["game"]:  
					self.net["act"][4].append(temp)
				if "power" in self.gd["effect"]:
					self.gd["target"].append(temp)
					if self.net["game"]:  
						self.net["act"][4].remove(temp)
		elif self.gd["effect"][inx] == 0:
			if any(st in self.cd[idm].pos_new for st in self.stage):
				self.cd[idm].trait_c.append([self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"], self.gd["turn"]])
				self.cd[idm].update_trait()
				if self.gd["effect"][2 + inx] == -66:
					self.check_cont_ability()
		elif self.gd["effect"][inx] < 0:
			if self.gd["effect"][inx] == -1 or self.gd["effect"][inx] == -2:
				for ind in self.cont_times(self.gd["effect"], self.cont_cards(self.gd["effect"], idm), self.cd):
					if ind != "":
						if self.gd["effect"][inx] == -2 and ind == idm:
							continue
						self.cd[ind].trait_c.append([self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"], self.gd["turn"]])
						self.cd[ind].update_trait()
						if "extra" in self.gd["effect"]:
							self.gd["extra"].append(ind)
			elif self.gd["effect"][0] == -16:
				for ind in list(self.gd["extra"]):
					if "extra" not in self.gd["effect"]:
						self.gd["extra"].remove(ind)
					self.cd[ind].trait_c.append([self.gd["effect"][1 + inx], self.gd["effect"][2 + inx], self.gd["ability_trigger"], self.gd["turn"]])
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
			self.check_auto_ability(rev=[ind], rst=[ind], stacks=False)

	def restart(self):
		self.gd["game_start"] = False
		self.rect.source = f"atlas://{img_in}/other/blank"
		self.rect.pos = (-Window.width * 2, -Window.height * 2)
		self.rect1.source = f"atlas://{img_in}/other/blank"
		self.rect1.pos = (-Window.width * 2, -Window.height * 2)

		for player in self.pd:
			for key in self.pd[player]:
				if key in "deck":
					self.pd[player][key] = {}
				elif key in ("phase", "done"):
					for item in self.pd[player][key]:
						self.pd[player][key][item] = False
				elif key in ("deck_id", "deck_name", "name", "janken"):
					self.pd[player][key] = ""
				elif key in ("Hand", "Res", "Clock", "Level", "Climax", "Stock", "Memory", "Waiting"):
					for inx in range(len(self.pd[player][key])):
						temp = self.pd[player][key].pop()
						if temp not in self.pd[player]["Library"]:
							self.pd[player]["Library"].append(temp)
					self.pd[player][key] = []
				elif key in "colour":
					self.pd[player][key] = []
				elif key in "marker":
					for ind in self.pd[player][key]:
						for item in self.pd[player][key][ind]:
							if item[0] not in self.pd[player]["Library"]:
								self.pd[player]["Library"].append(item[0])
						self.pd[player][key][ind] = []
				elif key in ("Center", "Back"):
					for inx in range(len(self.pd[player][key])):
						if self.pd[player][key][inx] != "":
							if self.pd[player][key][inx] not in self.pd[player]["Library"]:
								self.pd[player]["Library"].append(self.pd[player][key][inx])
							self.pd[player][key][inx] = ""

		try:
			for r in ("starting_player", "second_player", "active", "opp", "phase"):
				self.gd[r] = ""

			for ind in self.cd:
				if ind in self.emptycards or ind == "1" or ind == "2" or ind.endswith("3"):
					continue
				self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Library"], t="Library")
				self.cd[ind].update_text()

			self.clear_ability()

			self.multi_info["popup"].dismiss()
			self.sd["text"]["popup"].dismiss()
			self.sd["popup"]["popup"].dismiss()

			self.cardinfo.dismiss()

			self.sd["menu"]["popup"].size = (self.sd["card"][0] * 4.5, self.sd["card"][1] * 5.5)
			self.sd["menu"]["wl_box"].remove_widget(self.sd["menu"]["wl"])

			for label in phases + steps:
				self.sd["label"][label].center_y = Window.height / 2
				self.sd["label"][label].x = -Window.width * 2
				self.sd["label"][label].color = (.5, .5, .5, 1.)

			for field in self.field_label:
				self.field_label[field].x = -Window.width

			for field in self.field_btn:
				self.field_btn[field].x -= Window.width * 5

			for player in self.pd:
				self.cd[player].text_c = []
				self.update_colour(player)

			for ind in self.cd:
				try:
					self.cd[ind].selectable(False)
				except AttributeError:
					pass

			for r in ("Clock",):
				self.sd["btn"][f"{r}_btn"].text = f"End {r}"

			for fields in self.gd["select_btns"]:
				if "Clock" in fields:
					for ind in self.pd[fields[-1]]["Clock"]:
						self.cd[ind].selectable(False)
				elif ("Stage" in self.gd["status"] or self.gd["move"]) and fields[:-1] in self.gd["stage"]:
					if self.field_btn[field].x > 0:
						self.field_btn[f"{fields}s"].x = -Window.width * 5
				else:
					if "Climax" in fields:
						self.cd[self.pd[fields[-1]][fields[:-1]][0]].selectable(False)
					else:
						if self.pd[fields[-1]][fields[:-2]][int(fields[-2])] != "":
							self.cd[self.pd[fields[-1]][fields[:-2]][int(fields[-2])]].selectable(False)

			self.gd["select_btns"] = []
			for r in ("end", "end_attack", "end_phase", "continue", "draw_upto", "ablt_info"):
				self.sd["btn"][r].y = -Window.height
			self.hide_attack_btn()
			self.act_ability_show(hide=True)
			self.hand_btn_show(False)
			self.popup_clr()
			self.check_cont_ability()
		except KeyError:
			pass

		delete_load_file()

		self.gd["reshuffle"] = False
		self.gd["rev"] = False

	def start_game(self, *args):
		if not self.sd["field_btn_fill"]:
			Clock.schedule_once(self.start_game, move_dt * 2)
		else:
			Clock.schedule_once(self.start_game_1)

	def start_game_1(self, *args):
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

		if self.net["game"]:
			self.sd["text"]["popup"].dismiss()

		if self.gd["load"]:
			for player in list(self.pd.keys()):
				self.import_mat(player, self.decks[player][1])
				self.scale_mat(t=False, player=player)
				self.import_deck(player, self.decks[player][0])
		else:
			self.gd["shuffle_trigger"] = "turn0"
			self.gd["turn"] = 0

			for player in list(self.pd.keys()):
				if self.decks[player][3]:
					mat = choice([s for s in sp.keys() if sp[s]["c"]])
					self.import_mat(player, mat)
				else:
					self.import_mat(player, self.decks[player][1])

				self.scale_mat(t=False, player=player)

				if player == "2" and self.net["game"]:
					self.import_deck(player, self.decks[player][0])
				elif self.decks[player][2]:
					self.import_deck(player, choice([s for s in sd.keys() if sd[s]["c"]]))
				else:
					self.import_deck(player, self.decks[player][0])

		self.sd["b_bar"].x = 0
		self.sd["t_bar"].x = 0
		self.sd["t_bar"].y = Window.height - self.sd["menu"]["btn"].size[1]
		self.sd["b_bar"].y = 0
		self.mat["1"]["mat"].x = (Window.width - self.mat["1"]["mat"].size[0]) / 2
		self.mat["1"]["mat"].y = Window.height / 2 - self.sd["padding"] - self.sd["card"][1] / 6 - self.mat["1"]["mat"].height
		self.mat["2"]["mat"].reverse()

		self.mat["2"]["mat"].x = (Window.width - self.mat["2"]["mat"].size[0]) / 2
		self.mat["2"]["mat"].y = Window.height / 2 + self.sd["padding"] + self.sd["card"][1] / 6
		self.rect.size = (Window.width + self.sd["card"][0], Window.height / 2 - self.sd["padding"] - self.sd["card"][1] / 6)  

		self.sd["btn"]["end"].x = Window.width - self.sd["btn"]["end"].size[0]
		self.sd["btn"]["end"].y = -Window.height
		self.sd["btn"]["end"].disabled = False

		self.sd["btn"]["end_attack"].x = Window.width - self.sd["btn"]["end"].size[0] - self.sd["btn"]["end_attack"].size[0]
		self.sd["btn"]["end_attack"].y = -Window.height
		self.sd["btn"]["end_attack"].disabled = False

		self.sd["btn"]["end_phase"].x = Window.width - self.sd["btn"]["end"].size[0] - self.sd["btn"]["end_attack"].size[0] - self.sd["btn"]["end_phase"].size[0]
		self.sd["btn"]["end_phase"].y = -Window.height
		self.sd["btn"]["end_phase"].disabled = False
		self.sd["btn"]["ablt_info"].y = -Window.height
		self.sd["btn"]["draw_upto"].y = -Window.height

		self.field_btn_pos()
		self.change_label(True)
		for label in phases:
			self.sd["label"][label].center_y = Window.height / 2

		for r in ("end", "end_attack", "end_phase", "ablt_info", "draw_upto", "continue", "end_eff"):
			try:
				self.parent.add_widget(self.sd["btn"][r])
			except WidgetException:
				pass

		self.gd["game_start"] = True  
		self.deck_fill()
		self.add_field_label()
		self.update_field_label()

		self.gd["p_ld"] = []
		if self.gd["load"]:
			self.load_pos()
			self.check_cont_ability()
			self.gd["load"] = False
			self.sd["text"]["popup"].dismiss()
			if self.net["game"] and self.net["failed"] and not self.net["got"]:
				self.mping_data()
			elif (self.gd["popup_done"][0] and not self.gd["popup_done"][1]) or (not self.gd["popup_done"][0] and not self.gd["popup_done"][1]):
				self.sd["menu"]["btn"].disabled = True
				self.sd["btn"]["continue"].y = -Window.height
				self.hand_btn_show(False)

				if self.infot:
					self.infot.cancel()
					self.infot = None

				if self.gd["select_on"]:
					self.select_card()
				elif self.gd["choose_trait"]:
					self.gd["p_c"] = ""
					self.choose_trait()
				elif self.gd["stack_pop"]:
					self.stack_popup()
				elif self.gd["confirm_pop"]:
					self.gd["confirm_var"] = dict(self.gd["confirm_temp"])
					self.confirm_popup()
				elif self.gd["popup_pop"]:
					self.gd["confirm_var"] = dict(self.gd["confirm_temp"])
					if "z" in self.gd["confirm_var"]:
						self.sd["popup"]["popup"].title = self.gd["confirm_var"]["z"]
					self.popup_start()

				elif self.gd["act_poped"]:
					self.act_popup(self.gd["act_poped"])
				elif self.gd["per_poped"][0]:
					self.perform_popup(self.gd["per_poped"])
			else:
				if "Mulligan" in self.gd["phase"]:
					self.mulligan_start()
				else:
					if not self.gd['ability_effect'] and not self.gd['ability_doing']:
						Clock.schedule_once(self.ability_event, move_dt_btw)
					else:
						Clock.schedule_once(self.ability_effect, move_dt_btw)
		else:
			self.sd["text"]["popup"].dismiss()
			self.gd["j_result"] = 0

			if not self.net["game"] and not self.gd["com"]:
				self.gd["com"] = True
			self.gd["stack"] = {"1": [], "2": []}
			Clock.schedule_once(partial(self.shuffle_deck, "0"), phase_dt)

	@staticmethod
	def str_dict(ddeck):
		temp = {}
		for ind in ddeck.split("~")[1].split(","):
			i, j = ind.split(":")
			temp[i] = int(j)
		return temp

	def import_deck(self, owner, ddeck):
		if owner == "2" and ddeck.startswith("CEJ") and self.net["game"]:
			self.pd[owner]["deck"] = self.str_dict(ddeck)
			self.pd[owner]["deck_name"] = "Custom"
			self.pd[owner]["deck_id"] = ddeck.split("!")[0]
		else:
			self.pd[owner]["deck"] = sd[ddeck]["deck"]
			self.pd[owner]["deck_name"] = sd[ddeck]["name"]
			self.pd[owner]["deck_id"] = ddeck

	def import_mat(self, player, mat="mat"):
		self.mat[player]["id"] = mat
		try:
			if self.gd["DLimg"]:
				self.mat[player]["mat"].import_mat(sp[mat], self.mat[player]["per"])
			else:
				self.mat[player]["mat"].import_mat(sp["nodl"], self.mat[player]["per"])
		except KeyError:
			if self.gd["DLimg"]:
				self.mat[player]["id"] = "mat"
			else:
				self.mat[player]["id"] = "nodl"
			self.mat[player]["mat"].import_mat(sp["mat"], self.mat[player]["per"])
		self.sd[f"colour{player}"].x = self.mat[player]["field"]["Level"][0] + self.mat[player]["mat"].x - self.sd["padding"] / 2
		self.sd[f"colour{player}"].y = self.mat[player]["field"]["Level"][1] - self.sd[f"colour{player}"].size[1] / 3

	def clear_deck_pop(self, *args):
		self.decks["stack"].clear_widgets()

	def popup_deck_start(self, *args):
		self.decks["popup"] = Popup(size_hint=(None, None))
		self.decks["popup"].bind(on_dismiss=self.clear_deck_pop)
		self.decks["sctm"] = RelativeLayout(size_hint=(1, 1))
		self.decks["stack"] = StackLayout(orientation="lr-tb", size_hint_y=None, padding=self.sd["padding"] / 2, spacing=self.sd["padding"])
		self.decks["stack"].bind(minimum_height=self.decks["stack"].setter('height'))
		self.decks["sspaced"] = StackSpacer(o=(self.sd["card"][0] * 1.5, self.sd["card"][1] * 1.5))
		self.decks["scv"] = ScrollView(do_scroll_x=False, size_hint=(1, None), effect_cls="ScrollEffect")
		self.decks["p_info"] = None
		self.decks["selected"] = ""
		self.decks["dbuilding"] = ""
		self.decks["build_pop"] = False
		self.decks["dbuild"] = {}
		self.decks["dbtn"] = {}
		self.decks["imgs"] = []
		self.decks["add_chosen"] = []
		self.decks["img_pop"] = False
		self.decks["sets"] = Popup(size_hint=(None, None))
		self.decks["sets"].size = (self.sd["card"][0] * 6, self.sd["card"][1])

		self.decks["rv_rel"] = RelativeLayout(size_hint=(1, None))
		self.decks["rv_all"] = Button(size_hint=(None, None), text="Download All", on_release=self.deck_set_title_btn, size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.), cid="all")
		self.decks["rv_close"] = Button(size_hint=(None, None), text="Close", on_release=self.deck_set_title_btn, size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.), cid="close")
		self.decks["rv"] = RV()
		self.decks["rv"].bind(set_title=self.deck_set_title)
		self.decks["rv"].box.padding = self.sd["padding"]
		self.decks["rv"].box.spacing = self.sd["padding"]

		self.decks["close"] = Button(size_hint=(None, None), text="Close", on_release=self.popup_deck_slc, size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.), cid="")
		self.decks["confirm"] = Button(cid="1", size_hint=(None, None), text="Confirm", on_release=self.popup_deck_slc, size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.))

		self.decks["dismantle"] = Button(size_hint=(None, None), text="Dismantle", on_release=self.popup_deck_slc, size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.), cid="z")
		self.decks["dismantle"].disabled = True
		self.decks["create"] = Button(cid="c", size_hint=(None, None), text="Create new", on_release=self.popup_deck_slc, size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.))
		self.decks["save"] = Button(cid="done", size_hint=(None, None), text="Save & Exit", on_release=self.building_btn, size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.))
		self.decks["import"] = Button(cid="import", size_hint=(None, None), text="Import Deck", on_release=self.building_btn, size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.))

		self.decks["rearrange"] = Button(cid="r", size_hint=(None, None), text="Confirm", on_release=self.popup_deck_slc, size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.))
		self.decks["back"] = Button(cid="b", size_hint=(None, None), text="Back", on_release=self.popup_deck_slc, size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.))

		self.decks["setting_pop"] = False
		self.decks["st"] = {}
		self.decks["st"]["name"] = Label(text="Deck Name", halign='center', valign='middle', outline_width=1.9)
		self.decks["st"]["name_btn"] = TextInput(text="", cid="name")
		self.decks["st"]["name_btn"].bind(text=self.deck_set_slc)
		self.decks["st"]["name_box"] = BoxLayout(orientation="vertical", size_hint=(1, None))
		self.decks["st"]["lang"] = Label(text="Language", halign='center', valign='middle', outline_width=1.9)
		self.decks["st"]["lang_spn"] = Spinner(text="Both", values=("Both", "Jap", "Eng"), cid="lang")
		self.decks["st"]["lang_spn"].bind(text=self.deck_set_slc)
		self.decks["st"]["lang_box"] = BoxLayout(orientation="horizontal", size_hint=(1, None))
		self.decks["st"]["format"] = Label(text="Format", halign='center', valign='middle', outline_width=1.9)
		self.decks["st"]["format_spn"] = Spinner(text="-", values=("Standard", "Side", "Neo-Standard"), cid="format")  
		self.decks["st"]["format_spn"].bind(text=self.deck_set_slc)
		self.decks["st"]["format_btn"] = Button(text="", on_press=self.deck_set_slc, cid="title", disabled=True, halign='center', valign='middle', max_lines=1)
		self.decks["st"]["format_box"] = BoxLayout(orientation="vertical", size_hint=(1, None))
		self.decks["st"]["format_box1"] = BoxLayout(orientation="horizontal", size_hint=(1, 1))
		self.decks["st"]["image"] = Label(text="Default Image", halign='center', valign='middle', outline_width=1.9, max_lines=1)
		self.decks["st"]["image_btn"] = ImgButton(self.sd["card"], self.sd["card"], cid="image", source=f"atlas://{img_in}/other/empty")
		self.decks["st"]["image_btn"].btn.bind(on_press=self.deck_set_slc)
		self.decks["st"]["image_box"] = BoxLayout(orientation="vertical", size_hint=(1, None))
		self.decks["st"]["import"] = Label(text="Website", halign='center', valign='middle', outline_width=1.9)
		self.decks["st"]["import_spn"] = Spinner(text="-", values=("EncoreDecks", "DECK LOG EN", "DECK LOG JP"), cid="import")
		self.decks["st"]["import_spn"].bind(text=self.deck_set_slc)
		self.decks["st"]["import_btn"] = TextInput(text="", cid="website")
		self.decks["st"]["import_btn"].bind(text=self.deck_set_slc)
		self.decks["st"]["import_box"] = BoxLayout(orientation="vertical", size_hint=(1, None))
		self.decks["st"]["import_box1"] = BoxLayout(orientation="horizontal", size_hint=(1, 1))

		self.decks["st"]["name_box"].add_widget(self.decks["st"]["name"])
		self.decks["st"]["name_box"].add_widget(self.decks["st"]["name_btn"])
		self.decks["st"]["format_box1"].add_widget(self.decks["st"]["format"])
		self.decks["st"]["format_box1"].add_widget(self.decks["st"]["format_spn"])
		self.decks["st"]["format_box"].add_widget(self.decks["st"]["format_box1"])
		self.decks["st"]["format_box"].add_widget(self.decks["st"]["format_btn"])
		self.decks["st"]["import_box1"].add_widget(self.decks["st"]["import"])
		self.decks["st"]["import_box1"].add_widget(self.decks["st"]["import_spn"])
		self.decks["st"]["import_box"].add_widget(self.decks["st"]["import_box1"])
		self.decks["st"]["import_box"].add_widget(self.decks["st"]["import_btn"])
		self.decks["st"]["image_box"].add_widget(self.decks["st"]["image"])
		self.decks["st"]["image_box"].add_widget(self.decks["st"]["image_btn"])
		self.decks["st"]["lang_box"].add_widget(self.decks["st"]["lang"])
		self.decks["st"]["lang_box"].add_widget(self.decks["st"]["lang_spn"])

		self.decks["add_btn"] = Button(size_hint=(0.3, 1), text="Add Card", cid="add", on_press=self.building_btn)
		self.decks["name_btn"] = Button(size_hint=(0.2, 1), text="Setting", cid="name", on_press=self.building_btn)
		self.decks["done_btn"] = Button(size_hint=(0.2, 1), text="Done", cid="done", on_press=self.building_btn)

		self.decks["50"] = Label(text="00/50", halign='center', valign='middle', outline_width=1.9, size_hint=(0.15, 1))
		self.decks["8"] = Label(text="0/8", halign='center', valign='middle', outline_width=1.9, size_hint=(0.15, 1))
		self.decks["dbuild_btn"] = BoxLayout(orientation="horizontal", size=(Window.width, self.sd["card"][1] / 2), size_hint=(None, None))

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

		self.sd["dpop_press"] = []
		self.popup_deck(t="start")

	def deck_set_slc(self, inst, value=""):
		if self.decks["setting_pop"]:
			if inst.cid == "image":
				if len(self.decks["dbuild"]["deck"]) > 0:
					self.sd["popup"]["popup"].title = "Choose an Image"
					self.popup_start(c="Image")
			elif inst.cid == "format":
				if value == "Standard":
					self.decks["dbuild"]["n"] = value.split("-")[0]
					self.decks["close"].disabled = False
					self.decks["st"]["format_btn"].disabled = True
					self.decks["st"]["format_btn"].text = ""
					self.decks["dbuild"]["t"] = ""
				else:
					self.decks["set_temp"] = value.split("-")[0]
					self.decks["st"]["format_btn"].disabled = False
					self.decks["st"]["format_btn"].text = ""
					self.decks["close"].disabled = True
					self.deck_title_pop()
			elif inst.cid == "name":
				self.decks["dbuild"]["name"] = value
			elif inst.cid == "lang":
				self.decks["lang"] = value
				if value == "Both":
					self.decks["dbuild"]["l"] = ""
				else:
					self.decks["dbuild"]["l"] = value[0].lower()
			elif inst.cid == "title":
				self.decks["rv"].set_title = ""
				self.deck_title_pop("title")
			elif inst.cid == "import":
				if value != "-":
					self.decks["st"]["import_btn"].disabled = False
					self.decks["st"]["import_btn"].text = ""
				else:
					self.decks["st"]["import_btn"].disabled = True
					self.decks["st"]["import_btn"].text = ""
			elif inst.cid == "website":
				if value != "" and self.net[self.decks["st"]["import_spn"].text] in value:
					self.decks["close"].disabled = False
				else:
					self.decks["close"].disabled = True
			elif inst.cid == "sets":
				pass

	def deck_set_title_btn(self, btn):
		self.deck_set_title(btn, btn.cid)

	def deck_set_title(self, inst, val):
		if val != "":
			if val != "close":
				if val == "all":
					self.net["var"] = [str(val), 0]
					self.temp = []
					for var in se["check"].keys():
						if any(var == self.decks["rv"].data[ids]["id"] for ids in range(len(self.decks["rv"].data))):
							temp = str(var)
							temp1 = [str(var), 0]
							self.net["var"].append(temp)
							self.temp.append(temp1)
					self.net["var1"] = f"down_{val}"
					self.mconnect("down")
				elif val in se["check"]:
					self.net["var"] = [str(val), 0]
					self.net["var1"] = f"down_{val}"
					self.mconnect("down")
				elif val in sn["Title"] and "download" in self.decks["sets"].title:
					self.net["var"] = ["all", 0]
					self.temp = []
					for var in self.title_pack[val][1]:
						temp = str(var)
						temp1 = [str(var), 0]
						self.net["var"].append(temp)
						self.temp.append(temp1)
					self.net["var1"] = f"down_{val}"
					self.mconnect("down")
				else:
					self.decks["dbuild"]["n"] = str(self.decks["set_temp"])
					self.decks["dbuild"]["t"] = val
					self.decks["st"]["format_btn"].text = val
					self.decks["st"]["format_btn"].disabled = False
					self.decks["close"].disabled = False
					self.decks["sets"].dismiss()
			else:
				self.decks["sets"].dismiss()
			self.decks["rv"].set_title = ""

	def deck_title_pop(self, t=""):
		self.decks["rv"].data = []
		data = []
		self.decks["rv"].do_scroll_y = False
		size = (self.sd["card"][0] * 5.6, self.sd['card'][1] / 1.25)
		text = (self.sd["card"][0] * 5.4, self.sd['card'][1] / 1.25)
		if "down" in t:
			self.decks["sets"].title = f"Choose a package to download"
			title = False
			if "Bo" in t[-2:] or "Ex" in t[-2:] or "Tr" in t[-2:]:
				sets = [s for s in se["check"].keys() if s.startswith(t[-2].lower())]
			elif "Ti" in t[-2:]:
				sets = [s for s in sn["Title"]]
				title = True
			else:
				sets = [s for s in se["check"].keys() if all(not s.startswith(ss) for ss in ("b", "e", "t"))]

			for s in sets:
				down = True
				if title:
					if s not in self.title_pack:
						self.title_pack[s] = [[], []]
						self.title_pack[s][0] = list(set([_.split("/")[1].split("-")[0].lower() for _ in sc if any(ns in _ for ns in sn["Title"][s])]))
					dd = [False]
					if s in self.title_pack and self.title_pack[s][1]:
						packs = self.title_pack[s][1]
					else:
						packs = se["check"]

					for pack in packs:
						if any(ts in pack for ts in self.title_pack[s][0]):
							if pack not in self.title_pack[s][1]:
								self.title_pack[s][1].append(pack)
							for item in se["check"][pack]:
								if "-d" in item:
									if self.multi_info["dw"]["2"].state == 'down' and (exists(f"{data_ex}/{item}") or ("tws01-d" in item or "as11e-d" in item)):
										dd.append(False)
									elif self.multi_info["dw"]["3"].state == 'down' and not exists(f"{data_ex}/{item}") and "tws01-d" not in item and "as11e-d" not in item:
										dd.append(False)
									else:
										dd.append(True)
									break
					if all(not d for d in dd):
						down = False
				else:
					for item in se["check"][s]:
						if "-d" in item:
							if self.multi_info["dw"]["2"].state == 'down' and (exists(f"{data_ex}/{item}") or ("tws01-d" in item or "as11e-d" in item)):
								down = False
							elif self.multi_info["dw"]["3"].state == 'down' and not exists(f"{data_ex}/{item}") and "tws01-d" not in item and "as11e-d" not in item:
								down = False
							break

				if down:
					if title:
						data.append({"text": s, "size": size, "size_hint": (1, None), "text_size": text, "id": s, "disabled": False})
					else:
						data.append({"text": se["check"][s]["e"], "size": size, "size_hint": (1, None), "text_size": text, "id": s, "disabled": False})
			for var in sorted(data, key=lambda x: x["text"]):
				self.decks["rv"].data.append(var)
		else:
			if "set_temp" not in self.decks:
				self.decks["set_temp"] = self.decks["dbuild"]["n"]
			if "Neo" in self.decks["set_temp"]:  
				key = "Title"
			else:
				key = self.decks["set_temp"]

			self.decks["sets"].title = f"Choose a {key}"

			for name in sorted(se["main"]["s"][key]):
				self.decks["rv"].data.append({"text": name, "size": size, "size_hint": (1, None), "disabled": False, "text_size": text, "id": name})

		yscv = (self.sd["card"][1] / 1.25 + self.sd["padding"]) * len(self.decks["rv"].data)
		ybtn = self.sd["padding"] * 2.5 + self.sd["card"][1] / 2.
		ypop = yscv + ybtn + self.decks["sets"].title_size + self.decks["sets"].separator_height + self.sd["card"][1] * 0.75

		if ypop > Window.height:
			self.decks["rv"].do_scroll_y = True
			ypop = Window.height * 0.95
			yscv = ypop - self.sd["card"][1] * 0.75 - self.decks["sets"].title_size - self.decks["sets"].separator_height - (self.sd["card"][1] / 1.25 + self.sd["padding"] * 0)

		self.decks["sets"].content = self.decks["rv_rel"]

		self.decks["sets"].size = (self.sd["card"][0] * 6 + self.sd["padding"] * 2, ypop)
		self.decks["rv_close"].y = self.sd["padding"] * 1
		self.decks["rv"].y = ybtn
		self.decks["rv_rel"].size = (self.decks["sets"].size[0], yscv)

		if "down" in t:
			self.decks["rv_all"].center_x = self.decks["sets"].size[0] / 4. - self.sd["padding"] / 2
			self.decks["rv_all"].y = self.sd["padding"] * 1
			self.decks["rv_close"].center_x = self.decks["sets"].size[0] / 4. * 3 - self.sd["card"][0] / 2  
		else:
			self.decks["rv_close"].center_x = self.decks["sets"].size[0] / 2 - self.sd["card"][0] / 4  
			self.decks["rv_all"].y = -Window.height * 2
			self.decks["rv_rel"].size = (self.decks["sets"].size[0], yscv)

		self.decks["rv"].scroll_y = 1
		self.decks["sets"].open()

	def popup_deck(self, t="start", dt=.0, *args):
		self.decks["c"] = t
		self.decks["selected"] = ""
		deck_size = (self.sd["card"][0] * 1.5, self.sd["card"][1] * 1.5)
		mat_size = (self.sd["card"][1] * 1.9, self.sd["card"][0] * 1.9)
		self.decks["close"].text = "Close"
		self.decks["close"].disabled = False
		self.decks["save"].text = "Save & Exit"
		self.decks["import"].y = -Window.height * 2

		if t == "start":
			self.dpop["idadd"] = ImgButton(source=f"atlas://{img_in}/other/add", size=deck_size, cid="a", card=self.sd["card"])
			self.dpop["idadd"].btn.bind(on_press=self.popup_deck_slc)

			self.add_deckpop_btn(start=True)

			for mat in sorted(se["main"]["m"]):
				if not sp[mat]["c"]:
					continue

				source = "main"
				img = sp[mat]["img"]
				if not self.gd["DLimg"] and "mat_mat" in img:
					continue
				if "mat_mat" in img or "mat_nodl" in img:
					source = "other"
					if "." in img:
						img = img[:-4]

				self.decks["sspacem"] = StackSpacer(o=mat_size)

				if "main" in source:
					if exists(f"{cache}/{img}"):
						self.dpop[f"im{mat}"] = ImgButton(source=f"{cache}/{img}", size=mat_size, cid=f"m{mat}", card=self.sd["card"])
					else:
						self.dpop[f"im{mat}"] = ImgButton(source=f"atlas://{img_in}/other/grey", size=mat_size, cid=f"m{mat}", card=self.sd["card"])
				else:
					self.dpop[f"im{mat}"] = ImgButton(source=f"atlas://{img_in}/{source}/{img}", size=mat_size, cid=f"m{mat}", card=self.sd["card"])
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
					self.add_deckpop_btn(start=True)
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
						self.dpop[f"id{ind}"].selected_c(False)
						self.decks["stack"].add_widget(self.dpop[f"id{ind}"])
						self.add_deckpop_btn(start=True)
			elif "m" in t:
				self.decks["popup"].title = "Playmats"
				decks = [s for s in sorted(sp.keys()) if sp[s]["c"]]

				if not self.gd["DLimg"] and "mat" in decks:
					decks.remove("mat")
					temp = decks.pop(decks.index("nodl"))
					decks.insert(0, "nodl")

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
						self.dpop[f"im{ind}"].selected_c(False)
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
				ypop = Window.height * 0.95
				yscatm = ypop - self.decks["popup"].title_size - self.decks["popup"].separator_height
				yscv = yscatm - height * 0.5 - self.decks["close"].size[1] - self.sd["padding"] * 4
				if "dd" in t:
					yscv = yscv - self.decks["close"].size[1] - self.sd["padding"] * 2

			self.decks["scv"].size = (width * self.decks["max_col"] + self.sd["padding"] * 4, yscv)
			self.decks["popup"].size = (width * self.decks["max_col"] + self.sd["padding"] * 4, ypop)

			self.decks["close"].y = self.sd["padding"] * 1.5

			if "dd" in t:
				self.decks["close"].center_x = self.decks["popup"].size[0] / 2 - self.sd["card"][0] / 4
				self.decks["confirm"].y = -Window.height
				self.decks["dismantle"].disabled = True
				self.decks["dismantle"].center_x = self.decks["popup"].size[0] / 4 - self.sd["padding"] / 2
				self.decks["dismantle"].y = self.decks["close"].y * 2.5 + self.decks["close"].size[1]
				self.decks["create"].text = "Create new"
				self.decks["create"].center_x = self.decks["popup"].size[0] / 4 * 3 - self.sd["card"][0] / 2
				self.decks["create"].y = self.decks["close"].y * 2.5 + self.decks["close"].size[1]
				self.decks["scv"].y = (self.decks["close"].y * 2 + self.decks["close"].size[1]) * 2
			else:
				self.decks["create"].y = -Window.height * 2
				self.decks["dismantle"].y = -Window.height * 2
				self.decks["close"].center_x = self.decks["popup"].size[0] / 4 - self.sd["padding"] / 2
				self.decks["confirm"].center_x = self.decks["popup"].size[0] / 4 * 3 - self.sd["card"][0] / 2
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
			self.decks["close"].center_x = xscat / 2 - self.sd["card"][0] / 4  
			self.decks["close"].text = "Confirm"
			ypos = self.sd["padding"] * 4.5 + self.sd["card"][1] / 2

			for item in self.deck_spinner:
				if item == "import":
					self.decks["st"][f"{item}_box"].y = -Window.height * 2
				elif item == "image" and "img" in t:
					self.decks["st"][f"{item}_box"].pos = (0, ypos)
					self.decks["st"][f"{item}_box"].size = (xscat, self.sd["card"][1] * 1.5)
					self.decks["st"][item].size = (xscat, self.sd["card"][1] / 2)
					self.decks["st"][f"{item}_btn"].size = (xscat - self.sd["card"][0] / 2, self.sd["card"][1])
					self.decks["save"].y = self.sd["padding"] * 1.5
					self.decks["save"].center_x = xscat / 4 * 3 - self.sd["card"][0] / 2
					self.decks["close"].center_x = xscat / 4 - self.sd["padding"] / 2
					self.decks["close"].text = "Close"
					ypos += self.sd["card"][1] * 1.5 + self.sd["padding"] * 1
				elif item == "image" and "img" not in t:
					self.decks["st"][f"{item}_box"].y = -Window.height * 2
					self.decks["save"].y = self.sd["padding"] * 1.5
					self.decks["save"].center_x = xscat / 4 - self.sd["padding"] / 2
					self.decks["close"].center_x = xscat / 4 * 3 - self.sd["card"][0] / 2
					self.decks["save"].text = "Discard"
					self.decks["import"].y = self.sd["card"][1] / 2 + self.sd["padding"] * 4
					self.decks["import"].center_x = xscat / 2 - self.sd["card"][0] / 4
					ypos += self.sd["card"][1] / 2 + self.sd["padding"] * 3
				else:
					self.decks["st"][f"{item}_box"].pos = (0, ypos)
					if item == "lang":
						self.decks["st"][f"{item}_box"].size = (xscat, self.sd["card"][1] / 2)
						ypos += self.sd["card"][1] / 2 + self.sd["padding"] * 3
					else:
						self.decks["st"][f"{item}_box"].size = (xscat, self.sd["card"][1])
						ypos += self.sd["card"][1] + self.sd["padding"] * 3
					if item == "format":
						self.decks["st"][f"{item}_btn"].text_size = (xscat * 0.9, self.sd["card"][1] / 2)

			ypop += ypos + self.sd["padding"] * 5
			if self.decks["dbuild"]["n"]:
				self.decks["close"].disabled = False
			else:
				self.decks["close"].disabled = True
			self.decks["st"]["image"].text_size = (xscat / 2, self.sd["card"][1])
			self.decks["popup"].size = (xscat, ypop)
			self.decks["popup"].open()
		elif "download" in t:
			self.decks["popup"].title = "Download"
			self.decks["popup"].open()
		elif "import" in t:
			self.decks["scv"].y = -Window.height * 2
			self.decks["popup"].title = "Import Deck"

			xscat = self.sd["card"][0] * 6
			ypop = self.decks["popup"].title_size + self.decks["popup"].separator_height

			self.decks["close"].y = self.sd["padding"] * 1.5
			self.decks["close"].center_x = xscat / 2 - self.sd["card"][0] / 4  
			self.decks["close"].text = "Import"
			ypos = self.sd["padding"] * 4.5 + self.sd["card"][1] / 2

			for item in self.deck_spinner:
				if "import" in item:
					self.decks["st"][f"{item}_box"].pos = (0, ypos)
					self.decks["st"][f"{item}_box"].size = (xscat, self.sd["card"][1])
					self.decks["st"][item].size = (xscat, self.sd["card"][1] / 2)
					self.decks["st"][f"{item}_btn"].text_size = (xscat * 0.9, self.sd["card"][1] / 2)
					self.decks["st"][f"{item}_btn"].disabled = True
				else:
					self.decks["st"][f"{item}_box"].y = -Window.height * 2
			ypos += self.sd["card"][1] + self.sd["padding"] * 5
			self.decks["save"].y = self.sd["padding"] * 1.5
			self.decks["save"].center_x = xscat / 4 - self.sd["padding"] / 2
			self.decks["close"].center_x = xscat / 4 * 3 - self.sd["card"][0] / 2
			self.decks["save"].text = "Back"
			self.decks["import"].y = -Window.height * 2
			self.decks["import"].center_x = xscat / 2 - self.sd["card"][0] / 4

			ypop += ypos + self.sd["padding"] * 5
			if self.decks["dbuild"]["n"]:
				self.decks["close"].disabled = False
			else:
				self.decks["close"].disabled = True
			self.decks["popup"].size = (xscat, ypop)
			self.decks["popup"].open()

	def popup_deck_slc(self, btn):
		try:
			cid = str(btn.cid)
		except AttributeError:
			cid = str(btn)

		if self.decks["p_info"] is not None:
			self.decks["p_info"].cancel()
			self.decks["p_info"] = None
		if not cid:
			if self.decks["setting_pop"]:
				self.decks["setting_pop"] = False
				if "Import" in btn.text:
					Clock.schedule_once(partial(self.popup_text, "Loading"), ability_dt)
					Clock.schedule_once(self.deck_import, move_dt_btw)
				else:
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
		elif cid == "a":
			self.decks["selected"] = ""
			self.decks["popup"].dismiss()
			Clock.schedule_once(partial(self.popup_text, "Loading"), ability_dt)
			Clock.schedule_once(self.gotodeckedit, move_dt_btw)
		elif cid == "c":
			self.decks["popup"].dismiss()
			Clock.schedule_once(partial(self.popup_text, "Loading"), ability_dt)
			Clock.schedule_once(self.gotodeckedit, move_dt_btw)
		elif cid == "z" and self.decks["selected"]:
			self.gd["confirm_trigger"] = "Dismantle"
			self.gd["confirm_var"] = {"c": "Dismantle"}
			Clock.schedule_once(self.confirm_popup, popup_dt)
		elif cid == "1":
			source = "main"
			if "d" in self.decks["c"]:
				self.decks[self.decks["c"][1]][0] = self.decks["selected"][1:]
				self.decks[self.decks["c"][1]][2] = False
				img = sd[self.decks[self.decks["c"][1]][0]]["img"]
				if img[:-4] in other_img or ("." not in img and img in other_img):
					source = "other"
					if "." in img:
						img = img[:-4]
				elif self.gd["DLimg"] and (img[:-4] in annex_img or (img in annex_img and "." not in img)):
					if not exists(f"{cache}/{img}"):
						source = "annex"
						if "." in img:
							img = img[:-4]

				if source == "main" and self.decks[self.decks["c"][1]][0].startswith("CEJ"):
					if (img in se["main"]["a"][_] for _ in se["main"]["a"]):
						pass
					else:
						source = "other"
						img = "grey"
			elif "m" in self.decks["c"]:
				self.decks[self.decks["c"][1]][1] = self.decks["selected"][1:]
				self.decks[self.decks["c"][1]][3] = False
				img = sp[self.decks[self.decks["c"][1]][1]]["img"]

				if "mat_mat" in img or "mat_nodl" in img:
					source = "other"
					if "." in img:
						img = img[:-4]

			if "main" in source:
				if self.gd["DLimg"] and (exists(f"{cache}/{img}")):
					self.network[f"{self.decks['c'][1]}{self.decks['c'][2]}"].source = f"{cache}/{img}"
				else:
					self.network[f"{self.decks['c'][1]}{self.decks['c'][2]}"].source = f"atlas://{img_in}/other/grey"
			else:
				self.network[f"{self.decks['c'][1]}{self.decks['c'][2]}"].source = f"atlas://{img_in}/{source}/{img}"
			self.network[f"{self.decks['c'][1]}{self.decks['c'][2]}_ran"].state = "normal"
			self.popup_network_slc(self.network[f"{self.decks['c'][1]}{self.decks['c'][2]}_ran"])
			self.decks["popup"].dismiss()
		elif self.decks["selected"] == cid:
			self.dpop[f"i{cid}"].selected_c(False)
			self.decks["selected"] = ""
			self.decks["confirm"].disabled = True
			self.decks["dismantle"].disabled = True
			self.decks["create"].text = "Create new"
		elif self.decks["selected"] != cid:
			if self.decks["selected"] != "":
				self.dpop[f"i{self.decks['selected']}"].selected_c(False)
			self.decks["selected"] = cid
			self.decks["confirm"].disabled = False
			self.dpop[f"i{cid}"].selected_c()
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
		self.multi_info["t"] = False
		self.multi_info["deck"] = AsyncImage(source=f"atlas://{img_in}/other/empty", allow_stretch=True, height=self.sd["card"][1] * 3, size=(self.sd["card"][0] * 3, self.sd["card"][1] * 3), size_hint=(None, None))

		self.multi_info["shuffle"] = ""
		self.multi_info["popup"] = Popup(size_hint=(None, None))  
		self.multi_info["popup"].bind(on_open=self.multi_info_open, on_dismiss=self.multi_info_dismiss)
		self.multi_info["close"] = Button(size_hint=(None, None), text="Close", on_release=self.popup_multi_info_slc, size=(self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.), cid="close")
		self.multi_info["stack"] = StackLayout(orientation="lr-tb", size_hint_y=None, padding=self.sd["padding"] / 2, spacing=self.sd["padding"])
		self.multi_info["stack"].bind(minimum_height=self.multi_info["stack"].setter('height'))
		self.multi_info["sctm"] = RelativeLayout(size_hint=(1, 1))
		self.multi_info["scv"] = ScrollView(do_scroll_x=False, size_hint=(1, None), effect_cls="ScrollEffect")
		self.multi_info["sctm"].add_widget(self.multi_info["scv"])
		self.multi_info["sctm"].add_widget(self.multi_info["close"])
		self.multi_info["scv"].add_widget(self.multi_info["stack"])
		self.multi_info["popup"].content = self.multi_info["sctm"]
		self.multi_info["sspace"] = StackSpacer(o=self.sd["card"])

		self.multi_info["download"] = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=self.sd["padding"])
		self.multi_info["sctm"].add_widget(self.multi_info["download"])
		for ind in ("Booster Pack", "Extra Booster", "Trial Deck", "Other", "Titles"):
			rr = Button(text=ind, on_release=self.down_popup_btn, cid=ind[:2])
			self.multi_info["download"].add_widget(rr)

		self.multi_info["dw"] = {}
		self.multi_info["dw"]["h"] = BoxLayout(orientation='horizontal', size_hint=(None, 1))
		self.multi_info["dw"]["v"] = BoxLayout(orientation='vertical', size_hint=(None, None))
		self.multi_info["dw"]["1"] = ToggleButton(text='All', group='Down', state='down')
		self.multi_info["dw"]["2"] = ToggleButton(text='New', group='Down')
		self.multi_info["dw"]["3"] = ToggleButton(text='Download', group='Down')
		self.multi_info["dw"]["4"] = Label(text="Filter", halign='center', valign='middle', outline_width=1.9)

		self.multi_info["dw"]["v"].add_widget(self.multi_info["dw"]["4"])
		self.multi_info["dw"]["h"].add_widget(self.multi_info["dw"]["1"])
		self.multi_info["dw"]["h"].add_widget(self.multi_info["dw"]["2"])
		self.multi_info["dw"]["h"].add_widget(self.multi_info["dw"]["3"])
		self.multi_info["dw"]["v"].add_widget(self.multi_info["dw"]["h"])
		self.multi_info["sctm"].add_widget(self.multi_info["dw"]["v"])

		for x in range(1, 51):
			self.cpop[f"{x}0"] = CardImg(f"{x}0", self.sd["card"], "1", self.mat["1"]["per"])
			self.cpop[f"{x}0"].btn.bind(on_press=self.card_btn_press, on_release=self.card_btn_release)


	def multi_info_open(self, *args):
		self.multi_info["t"] = True

	def multi_info_dismiss(self, *args):
		self.multi_info["t"] = False
		self.multi_info["stack"].clear_widgets()

	def popup_multi_info_slc(self, btn, *args):
		if btn.cid == "close":
			self.multi_info["popup"].dismiss()
			self.multi_info["t"] = False
			if len(self.gd["show"]) > 0:
				self.gd["show"] = []

			if "marker" in self.gd["ability_doing"]:
				self.marker()
			elif "numbers" in self.gd["ability_doing"]:
				if "nowreveal" in self.gd["effect"]:
					self.ability_effect()
				else:
					self.cardnum()
			elif self.gd["popup_done"][1]:
				if "search" in self.gd["ability_doing"]:  
					if "Reveal" in self.gd["effect"]:
						Clock.schedule_once(self.ability_effect)
					elif "stsearch" in self.gd["effect"]:
						self.gd["shufflest_trigger"] = "ability"
						if self.net["game"]:
							self.gd["shuffle_send"] = True
						self.shuffle_stock(self.multi_info["owner"])
					else:
						self.gd["shuffle_trigger"] = "ability"
						if self.net["game"]:
							self.gd["shuffle_send"] = True
						self.shuffle_deck(self.multi_info["owner"])
				elif "salvage" in self.gd["ability_doing"]:
					if "Library" in self.gd["effect"] and "top" not in self.gd["effect"] and "bottom" not in self.gd["effect"]:
						self.gd["shuffle_trigger"] = "ability"
						if self.net["game"]:
							self.gd["shuffle_send"] = True
						self.shuffle_deck(self.multi_info["shuffle"])
					else:
						Clock.schedule_once(self.ability_effect)
				elif self.gd["random_reveal"]:
					self.gd["random_reveal"] = []
					Clock.schedule_once(self.ability_effect)
				elif self.gd["ability_doing"] in ("looktop", "look"):
					if self.gd["ability_doing"] in self.gd["ability_effect"]:
						if "look" in self.gd["ability_doing"]:
							if "do" in self.gd["ability_effect"]:
								self.gd["ability_effect"].remove("do")
						self.gd["done"] = True
						self.gd["ability_effect"].remove(self.gd["ability_doing"])
					Clock.schedule_once(self.ability_effect)
				elif "waitinger" in self.gd["ability_doing"]:
					Clock.schedule_once(self.ability_effect)
		else:
			if self.gd["turn"] <= 0:
				self.cardinfo.import_data(self.multi_info[f"c_{btn.cid}"], annex_img,self.gd["DLimg"])
			else:
				if self.check_back_hidden(self.multi_info[f"c_{btn.cid}"]):
					self.cardinfo.import_data(self.multi_info[f"c_{btn.cid}"], annex_img,self.gd["DLimg"])

	def popup_multi_info(self, field="", owner="", deck="", cards=[], t="", shuffle="", *args):
		self.multi_info["download"].y = -Window.height * 2
		self.multi_info["dw"]["v"].y = -Window.height * 2
		c = 1
		if deck != "":
			self.multi_info["popup"].title = sd[deck[1:]]["name"]
			self.multi_info["owner"] = "deck"
			self.multi_info["cards"] = []
			self.multi_info["deck_list"] = ["", ]
			for mcards in sorted(sd[deck[1:]]["deck"].keys()):
				for card in range(sd[deck[1:]]["deck"][mcards]):
					if c > 98:
						self.cpop[f"{c - 1}0"].import_data("add",self.gd["DLimg"])
						continue
					self.multi_info["cards"].append(f"{c}0")
					self.cpop[f"{c}0"].import_data(sc[mcards],self.gd["DLimg"])
					self.multi_info["deck_list"].append(mcards)
					c += 1
		else:
			if shuffle != "":
				self.multi_info["shuffle"] = shuffle
			else:
				self.multi_info["shuffle"] = owner

			if owner == "2":
				own = "Opponent"
			elif owner == "1":
				own = "Player"
			if field:
				self.multi_info["cards"] = list(self.pd[owner][field])
				t = field
			elif cards:
				self.multi_info["cards"] = cards
			if t == "OChoose" or t == "Numbers":
				self.multi_info["popup"].title = "Opponent choices"
			elif t == "Random":
				self.multi_info["popup"].title = f"{own} random choices"
			elif t == "Reveal":
				self.multi_info["popup"].title = f"{own} revealed card"
			else:
				if "Waiting" in t:
					t += " room"
				if "Stock" in self.gd["effect"]:
					self.multi_info["popup"].title = f"{own} choices"
				else:
					self.multi_info["popup"].title = f"{own}'s {t.lower()}"
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

			if not deck[1:].startswith("CJ") and not deck[1:].startswith("CE") and sd[deck[1:]]["img"] not in other_img:
				if self.gd["DLimg"] and (img[:-4] in annex_img or (img in annex_img and "." not in img)):
					if "." in img:
						img = img[:-4]
					self.multi_info["deck"].source = f"atlas://{img_in}/annex/{img}"
				elif "ws01v" in img or ("demo" in img and not exists(f"{cache}/{img}")):
					if "." in img:
						img = img[:-4]
					self.multi_info["deck"].source = f"atlas://{img_in}/other/{img}"
				else:
					if self.gd["DLimg"] and (exists(f"{cache}/{img}")):
						self.multi_info["deck"].source = f"{cache}/{img}"
					else:
						self.multi_info["deck"].source = f"atlas://{img_in}/other/grey"
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
				if t != "Numbers":
					self.cpop[ind].selected_c(False)
					self.cpop[ind].update_text()
					if not ind.endswith("0") and self.cd[ind].back:
						if owner == "2" and any(tt in t for tt in ("Search", "Salvage", "Stocker", "Hand")):
							self.cpop[ind].show_front()
						elif "Library" not in self.cd[ind].pos_new:
							self.cpop[ind].show_back()
						else:
							self.cpop[ind].show_front()
					else:
						if c > 98 and ind == "980":
							pass
						else:
							self.cpop[ind].show_front()
				try:
					self.multi_info["stack"].add_widget(self.cpop[ind])
				except WidgetException:
					pass

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
			yscv = yscatm - self.sd["card"][1] * 1.6

		if len(self.multi_info["popup"].title) > 60:
			self.multi_info["scv"].size = (width * ncards + self.sd["padding"] * 4, yscv - self.sd["card"][1] / 3)
		else:
			self.multi_info["scv"].size = (width * ncards + self.sd["padding"] * 4, yscv)
		self.multi_info["popup"].size = (width * ncards + self.sd["padding"] * 4, ypop)

		self.multi_info["close"].center_x = self.multi_info["popup"].size[0] / 2. - self.sd["card"][0] / 4  
		self.multi_info["close"].y = self.sd["padding"] * 1.5
		self.multi_info["scv"].y = self.multi_info["close"].y * 2 + self.multi_info["close"].size[1]
		self.multi_info["scv"].scroll_y = 1
		self.multi_info["t"] = True

		Clock.schedule_once(self.popup_multi_delay, move_dt_btw)

	def popup_network_start(self, *args):
		self.network["m_connect"] = Button(text="Connect", on_release=self.mconnect, cid="connect", size_hint=(None, None), size=(self.sd["card"][0] * 4, self.sd["card"][1] * 2))
		self.network["sctm"] = RelativeLayout(size_hint=(1, 1), pos=(0, 0))

		self.network["m_close"] = Button(size_hint=(None, None), text="Back", on_release=self.popup_network_slc, cid="back", size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.))
		self.network["m_confirm"] = Button(size_hint=(None, None), on_release=self.popup_network_slc, cid="confirm", text="Start", size=(self.sd["card"][0] * 2.25, self.sd["card"][1] / 2.))

		self.network["1d"] = ImgButton(source=f"atlas://{img_in}/other/demo", card=self.sd["card"], cid="x1d", size=(self.sd["card"][1] * 1.5, self.sd["card"][1] * 1.5))
		self.network["2d"] = ImgButton(source=f"atlas://{img_in}/other/demo", card=self.sd["card"], cid="x2d", size=(self.sd["card"][1] * 1.5, self.sd["card"][1] * 1.5))
		if self.gd["DLimg"]:
			self.network["1m"] = ImgButton(source=f"atlas://{img_in}/other/mat_mat", cid="x1m", card=self.sd["card"], size=(self.sd["card"][1] * 1.5, self.sd["card"][1] * 1.5))
			self.network["2m"] = ImgButton(source=f"atlas://{img_in}/other/mat_mat", card=self.sd["card"], cid="x2m", size=(self.sd["card"][1] * 1.5, self.sd["card"][1] * 1.5))
		else:
			self.network["1m"] = ImgButton(source=f"atlas://{img_in}/other/mat_nodl", cid="x1m", card=self.sd["card"], size=(self.sd["card"][1] * 1.5, self.sd["card"][1] * 1.5))
			self.network["2m"] = ImgButton(source=f"atlas://{img_in}/other/mat_nodl", card=self.sd["card"], cid="x2m", size=(self.sd["card"][1] * 1.5, self.sd["card"][1] * 1.5))

		self.network["1d"].btn.bind(on_press=self.popup_network_slc)
		self.network["1m"].btn.bind(on_press=self.popup_network_slc)
		self.network["2d"].btn.bind(on_press=self.popup_network_slc)
		self.network["2m"].btn.bind(on_press=self.popup_network_slc)
		self.network["1d_ran"] = ToggleButton(text="Random", on_release=self.popup_network_slc, size_hint=(None, None), cid="r1d", size=(self.sd["card"][1] * 1.5, self.sd["card"][1] / 3))
		self.network["1m_ran"] = ToggleButton(text="Random", on_release=self.popup_network_slc, size_hint=(None, None), cid="r1m", size=(self.sd["card"][1] * 1.5, self.sd["card"][1] / 3))
		self.network["2d_ran"] = ToggleButton(text="Random", on_release=self.popup_network_slc, size_hint=(None, None), cid="r2d", size=(self.sd["card"][1] * 1.5, self.sd["card"][1] / 3))
		self.network["2m_ran"] = ToggleButton(text="Random", on_release=self.popup_network_slc, size_hint=(None, None), cid="r2m", size=(self.sd["card"][1] * 1.5, self.sd["card"][1] / 3))
		self.network["1text"] = Label(text="P1", size_hint=(None, None))
		self.network["2text"] = Label(text="P2", size_hint=(None, None))
		for x in range(1, 3):
			self.network[f"{x}text"].color = (1, 1, 1, 1)
			self.network[f"{x}text"].outline_width = 2
			self.network[f"{x}text"].halign = "center"
			self.network[f"{x}text"].valing = "middle"
			self.network[f"{x}text"].size = (self.sd["card"][1], self.sd["card"][1] * 2)

		self.network["popup"] = Popup(size=(self.sd["card"][1] * 5, self.sd["card"][1] * 7.25), size_hint=(None, None))

		for item in self.network:
			if item.startswith("1") or item.startswith("2") or item.startswith("m_"):
				self.network["sctm"].add_widget(self.network[item])


		self.network["popup"].content = self.network["sctm"]
		self.multiplay_popup_create()

	def popup_network(self, t="", *args):
		self.network["popup"].open()

	def popup_network_slc(self, btn, *args):
		if btn.cid == "":
			pass
		elif btn.cid.startswith("r"):
			if btn.state == "normal":
				source = "main"
				img = "blank"
				if "d" in btn.cid:
					img = sd[self.decks[btn.cid[1]][0]]["img"]
					if img[:-4] in other_img or ("." not in img and img in other_img):
						source = "other"
						if "." in img:
							img = img[:-4]
					elif self.gd["DLimg"] and (img[:-4] in annex_img or (img in annex_img and "." not in img)):
						if not exists(f"{cache}/{img}"):
							source = "annex"
							if "." in img:
								img = img[:-4]
					self.decks[f"{btn.cid[1]}"][2] = False
				elif "m" in btn.cid:
					img = sp[self.decks[btn.cid[1]][1]]["img"]
					if "mat_mat" in img or "mat_nodl" in img:
						source = "other"
						if "." in img:
							img = img[:-4]
					self.decks[btn.cid[1]][3] = False

				if "main" in source:
					if self.gd["DLimg"] and (exists(f"{cache}/{img}")):
						self.network[f"{btn.cid[1]}{btn.cid[2]}"].source = f"{cache}/{img}"
					else:
						self.network[f"{btn.cid[1]}{btn.cid[2]}"].source = f"atlas://{img_in}/other/grey"
				else:
					self.network[f"{btn.cid[1]}{btn.cid[2]}"].source = f"atlas://{img_in}/{source}/{img}"
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
			Clock.schedule_once(partial(self.popup_text, "Loading"))
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
							self.network[item].center_x = self.network["popup"].size[0] / 2. - self.sd["card"][0] / 4  
						else:
							self.network[item].center_x = self.network["popup"].size[0] / 4. - self.sd["padding"] / 2
					elif "confirm" in item:
						if btn.cid == "multi":
							self.network[item].center_x = -Window.width * 2
						else:
							self.network[item].center_x = self.network["popup"].size[0] / 4. * 3 - self.sd["card"][0] / 2
					elif "connect" in item:
						if btn.cid == "multi":
							self.network[item].center_x = self.network["popup"].size[0] / 2. - self.sd["card"][0] / 4  
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

			try:
				self.sd["menu"]["popup"].dismiss()
			except KeyError:
				pass
			self.network["popup"].open()

	def play(self, lst, cnt=False):
		self.sd["btn"]["end"].y = -Window.height
		self.sd["btn"]["end_attack"].y = -Window.height
		self.sd["btn"]["end_phase"].y = -Window.height
		self.gd["movable"] = []

		self.play_to_stage(lst[0], f"{lst[1]}{lst[2]}")

		if not self.gd["waiting_cost"][1] and not self.gd["estock_pop"]:
			if self.gd["active"] == "1":
				if self.net["game"] and not cnt:
					self.net["send"] = False
			if not self.gd["waiting_cost"][2]:
				self.gd["play"] = []
				self.gd["play_card"] = lst[0]
				self.play_card()
			else:
				self.gd["waiting_cost"][2] = 0


	def multiplay_popup_create(self, *args):
		self.mcreate_popup = Popup(size_hint=(None, None))
		self.mcreate_popup.bind(on_open=self.update_time)

		xscat = self.sd["padding"] * 2 + (self.sd["card"][0] + self.sd["padding"]) * starting_hand
		yscat = (self.sd["card"][1] + self.sd["padding"]) + self.sd["card"][1] + self.sd["padding"] * 5 + self.mcreate_popup.title_size + self.mcreate_popup.separator_height

		self.mcreate_popup.size = (xscat, yscat + self.sd["padding"] * 1)
		self.mcreate_sct = RelativeLayout()
		self.mcreate_popup.content = self.mcreate_sct

		self.mcancel_create_btn = Button(text="Cancel", on_release=self.mcancel_room, size_hint=(None, None))
		self.mcancel_create_time = Label(text="0s", halign="center", text_size=(xscat, None), size_hint=(1, None))
		self.mcancel_create_text = Label(text=".", halign="center", text_size=(xscat, None), size_hint=(1, None))
		self.mcancel_create_bar = ProgressBar(size_hint=(None, None), size=(xscat * 0.8, self.sd["card"][1] / 2.5))

		self.mcancel_create_bar1 = ProgressBar(size_hint=(None, None), size=(xscat * 0.8, self.sd["card"][1] / 2.5))
		self.mcreate_sct.add_widget(self.mcancel_create_btn)
		self.mcreate_sct.add_widget(self.mcancel_create_text)
		self.mcreate_sct.add_widget(self.mcancel_create_time)
		self.mcreate_sct.add_widget(self.mcancel_create_bar)

		self.mcancel_create_bar.y = self.sd["padding"] * 3.5 + self.sd["card"][1] / 2
		self.mcancel_create_bar.center_x = xscat / 2 - self.sd["card"][0] / 4 - Window.width * 2

		self.mcancel_create_btn.size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
		self.mcancel_create_btn.center_x = xscat / 2 - self.sd["card"][0] / 4  
		self.mcancel_create_btn.y = self.sd["padding"] * 1.5

		self.mcancel_create_time.texture_update()
		self.mcancel_create_time.pos = (0, self.sd["padding"] * 3.5 + self.sd["card"][1] / 2.)

		self.mcancel_create_text.texture_update()
		self.mcancel_create_text.pos = (0, self.mcancel_create_time.y + self.sd["padding"] + self.mcancel_create_time.texture.size[1])

	def failure_message(self, request, result):
		self.net["failed"] = True
		if self.net["status"] == "down":
			request.cancel()
			temp = request.url.split("/")[-1]
			if temp not in self.downloads_key:
				self.downloads_key.append(temp)
		else:
			self.cnet.cancel()
			temp = self.net["body"]

		if self.net["status"] != "version":
			logging.exception(f'Got exception on main handler\nFailure\n{temp}\n{[request]}\n{request.url}\n{[result]}')
			Clock.schedule_once(partial(self.popup_text, "no_internet"))

	def error_message(self, request, result):
		self.net["failed"] = True
		if self.net["status"] == "down":
			request.cancel()
			temp = request.url.split("/")[-1]
			if temp not in self.downloads_key:
				self.downloads_key.append(temp)
		else:
			self.cnet.cancel()
			temp = self.net["body"]

		if self.net["status"] != "version":
			logging.exception(f'Got exception on main handler\nError\n{temp}\n{[request]}\n{request.url}\n{[result]}')
			Clock.schedule_once(partial(self.popup_text, "no_error"))

	def progress_message(self, request, current_size, total_size):
		item = request.url.split("/")[-1]
		self.downloads[item][1] = current_size
		current = 0
		for key in self.downloads.keys():
			current += self.downloads[key][1]

		self.mcancel_create_bar.value = current
		self.mcancel_create_text.text = f"{round(self.mcancel_create_bar.value_normalized * 100, 2):.2f}%"


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
			if self.mcancel_create_bar.x > 0:
				self.mcancel_create_bar.x -= Window.width * 2
			self.mcancel_create_btn.cid = self.net["status"]
		elif self.net["status"] == "roomdis":
			self.mcreate_popup.title = "Room Created"
			self.mcancel_create_text.text = "There was an error joining the room.\nPlease try again later."
			self.mcancel_create_btn.text = "Close"
			self.mcancel_create_btn.cid = self.net["status"]
		elif self.net["status"] == "down":
			self.gd["cancel_down"] = False
			self.mcreate_popup.title = "Download progress"
			self.mcancel_create_text.text = "0.00%"
			self.mcancel_create_bar.value = 0

			if self.mcancel_create_bar.x < 0:
				self.mcancel_create_bar.x += Window.width * 2

			self.mcancel_create_time.x = -Window.width * 2
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
			Clock.schedule_once(self.update_time, 1)
		else:
			self.mcancel_create_time.text = " "



	def check_internet(self, url="", timeout=2, ver=False):
		_ = False
		if ver:
			timeout = 1
		try:
			socket.create_connection(("8.8.8.8", 53), timeout=timeout)
			_ = True
		except socket.error:
			pass

		if not ver and not _:
			Clock.schedule_once(partial(self.popup_text, "no_internet"))

		return _

	def mconnect(self, btn, dt=0):
		if isinstance(btn, str):
			var = btn
		else:
			var = btn.cid
		if "version" in var or self.check_internet():  
			self.net["wait"] = True
			self.net["got"] = False
			dat = {}
			headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain', 'User-Agent': 'Mozilla/5.0'}
			if "connect" in var:

				self.network["m_connect"].disabled = True
				Clock.schedule_once(partial(self.popup_text, "making"), popup_dt)
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

				dat = {"0": "c0", "1": deck1, "2": mat, "3": dset, "v": __version__}
			elif "disconn" in var:
				dat = {"0": "dc", "1": self.net["room"]}
			elif "room" in var:
				dat = {"0": f"r{self.net['player']}", "1": self.net["room"], "2": self.net["ready"]}
			elif "winlose" in var:
				self.net["status"] = "winlose"
				dat = {"0": f"w{self.net['player']}", "1": self.net["room"], "2": f"{self.net['var']}"}
			elif "shuffleplr" in var:
				self.net["status"] = "shuffleplr"
				if self.net["var1"] == "shufflest":
					library = list_str(self.pd["1"]["Stock"])
				else:
					library = list_str(self.pd["1"]["Library"])
				dat = {"0": f"s{self.net['player']}", "1": self.net["room"], "2": library, "8": self.net["select"], "9": self.gd["turn"]}
			elif "shuffleopp" in var:
				self.net["status"] = "shuffleopp"
				dat = {"0": f"z{self.net['player']}", "1": self.net["room"], "8": self.net["select"], "9": self.gd["turn"]}
			elif "janken" in var:
				self.net["status"] = "janken"
				dat = {"0": f"j{self.net['player']}", "1": self.net["room"], "2": self.gd["j_hand"], "8": self.net["select"], "9": self.gd["turn"]}
			elif "mulligan" in var:
				self.net["status"] = "mulligan"
				mulligan = list_str(self.gd["mulligan"][0])
				dat = {"0": f"m{self.net['player']}", "1": self.net["room"], "2": mulligan, "8": self.net["select"], "9": self.gd["turn"]}
			elif "act" in var:
				self.net["status"] = "act"
				if len(self.net["var"][3]) >= 0:
					self.net["var"][3] = f"{list_str(self.net['var'][3], '~')}"
				if len(self.net["var"][4]) >= 0:
					self.net["var"][4] = f"{list_str(self.net['var'][4], '~')}"

				temp = f"{self.gd['phase'][:3]}_{list_str(self.net['var'])}"  
				dat = {"0": f"p{self.net['player']}", "1": self.net["room"], "2": temp, "8": self.net["select"], "9": self.gd["turn"]}
			elif "phase" in var:
				self.net["status"] = "phase"
				if (self.gd["active"] == "2" and not self.gd["rev"]) or (self.gd["rev"] and self.gd["active"] == "1"):
					self.gd["popup_on"] = True
					dat = {"0": f"o{self.net['player']}", "1": self.net["room"], "8": self.net["select"], "9": self.gd["turn"]}
				elif (self.gd["active"] == "1" and not self.gd["rev"]) or (self.gd["rev"] and self.gd["active"] == "2"):
					_ = list_str(self.net['var'][:3])
					if len(self.net["var"]) >3:
						_+=f".{list_str(self.net['var'][3],sep='_')}"
					temp = f"{self.gd['phase'][:3]}_{_}"  
					dat = {"0": f"p{self.net['player']}", "1": self.net["room"], "2": temp, "8": self.net["select"], "9": self.gd["turn"]}
			elif "oppchoose" in var:
				self.net["status"] = "oppchoose"
				ind = self.gd["ability_trigger"].split("_")[1]
				if ind[-1] == "1":
					self.gd["popup_on"] = True
					dat = {"0": f"o{self.net['player']}", "1": self.net["room"], "8": self.net["select"], "9": self.gd["turn"]}
				elif ind[-1] == "2":
					temp = f"och_{list_str(self.net['var'])}"  
					dat = {"0": f"p{self.net['player']}", "1": self.net["room"], "2": temp, "8": self.net["select"], "9": self.gd["turn"]}
			elif "oppturn" in var:
				self.net["status"] = "oppturn"
				self.gd["popup_on"] = True
				dat = {"0": f"o{self.net['player']}", "1": self.net["room"], "8": self.net["select"], "9": self.gd["turn"]}
			elif "plturn" in var:
				self.net["status"] = "plturn"
				temp = f"pch_{list_str(self.net['var'])}"  
				dat = {"0": f"p{self.net['player']}", "1": self.net["room"], "2": temp, "8": self.net["select"], "9": self.gd["turn"]}
			elif "plchoose" in var:
				self.net["status"] = "plchoose"
				ind = self.gd["ability_trigger"].split("_")[1]
				if ind[-1] == "1":
					temp = f"pch_{list_str(self.net['var'])}"  
					dat = {"0": f"p{self.net['player']}", "1": self.net["room"], "2": temp, "8": self.net["select"], "9": self.gd["turn"]}
				elif ind[-1] == "2":
					self.gd["popup_on"] = True
					dat = {"0": f"o{self.net['player']}", "1": self.net["room"], "8": self.net["select"], "9": self.gd["turn"]}
			elif "confirm" in var:
				self.net["status"] = "confirm"
				self.gd["popup_on"] = True
				dat = {"0": f"c{self.net['player']}", "1": self.net["room"], "8": self.net["select"], "9": self.gd["turn"]}
			elif "lvl" in var:
				self.net["status"] = "lvl"
				temp = f"lvu_{list_str(self.net['var'])}"
				dat = {"0": f"p{self.net['player']}", "1": self.net["room"], "2": temp, "8": self.net["select"], "9": self.gd["turn"]}
			elif "counter" in var:
				self.net["status"] = "counter"
				if self.gd["active"] == "1":
					dat = {"0": f"o{self.net['player']}", "1": self.net["room"], "8": self.net["select"], "9": self.gd["turn"]}
				else:
					temp = f"{self.gd['phase'][:3]}_{list_str(self.net['var'])}_{self.gd['ability_doing']}"
					dat = {"0": f"p{self.net['player']}", "1": self.net["room"], "2": temp, "8": self.net["select"], "9": self.gd["turn"]}
			elif "version" in var:
				self.net["status"] = "version"
				dat = {"0": "q"}
			elif "down" in var:
				if self.net["var"][1] <= 0:
					Clock.schedule_once(partial(self.popup_text, "Loading"), ability_dt)
				self.net["status"] = "down"
				if self.gd["HDimg"]:
					im = "h"
				else:
					im = "i"

				if "all" in self.net["var"][0]:
					dat = {"0": "w", "1": f"{list_str(self.net['var'])}", "2": im,"3":self.gd["DLimg"]}
				else:
					dat = {"0": "w", "1": f"{list_str(self.net['var'])}", "2": im,"3":self.gd["DLimg"]}

			if "down" in var and self.net["var"][1] > 0:
				self.downloads = {}
				self.downloads_key = []
				self.mcancel_create_bar.value = 0
				self.mcancel_create_bar1.value = 0

				if self.gd["HDimg"]:
					im = "h"
				else:
					im = "i"

				if "all" in self.net["var"][0]:
					for item in self.temp:
						for item1 in se["check"][item[0]]:
							if f"-{im}" not in item1 and "-d" not in item1:  
								continue
							if not self.gd["DLimg"] and  f"-{im}" in item1:
								continue
							self.downloads[item1] = [f"{self.net['data']}", 0, 0]
							self.downloads_key.append(item1)
				else:
					if ".d" in self.net["var"][0]:
						self.downloads[self.net["var"][0]] = [f"{self.net['data']}", 0, 0]
						self.downloads_key.append(self.net["var"][0])
					elif self.net["var"][0] in se["check"]:
						for item3 in se["check"][self.net["var"][0]]:
							if f"-{im}" not in item3 and "-d" not in item3:  
								continue
							if not self.gd["DLimg"] and  f"-{im}" in item3:
								continue
							self.downloads[item3] = [f"{self.net['data']}", 0, 0]
							self.downloads_key.append(item3)

				self.mcancel_create_bar1.max = len(self.downloads) * 11

				down = self.downloads_key.pop()
				self.req[down] = UrlRequest(f"{self.downloads[down][0]}{down}", timeout=10, on_success=self.down_data, on_cancel=self.down_data_cnc, on_failure=self.failure_message, on_error=self.error_message, on_progress=self.progress_message, ca_file=cfi.where(), verify=True)
			else:
				self.net["body"] = urlencode(dat)
				self.cnet = UrlRequest(self.net["url"], req_body=self.net["body"], req_headers=headers, on_success=self.mcheck_data, timeout=10, ca_file=cfi.where(), on_failure=self.failure_message, on_error=self.error_message, verify=True)  
				self.shelve_save()
		else:
			Clock.schedule_once(partial(self.popup_text, "no_internet"))

	def mcancel_room(self, *args):
		self.mcreate_popup.dismiss()
		self.net["time"] = -1
		self.update_time()
		self.cnet.cancel()
		if self.net["status"] == "create":
			self.net["status"] = "disconn"
			self.mconnect("disconn")
		elif self.net["status"] == "down":
			self.gd["cancel_down"] = True
			for item in self.req:
				if not self.req[item].is_finished:
					self.req[item].cancel()


	def mping_data(self, dt=0):
		self.net["got"] = False
		if "create" in self.net["status"] or "join" in self.net["status"]:
			self.room = Clock.schedule_once(partial(self.mconnect, "room"), 1)
		elif any(s in self.net["status"] for s in ("shuffle", "janken", "mulligan", "phase", "counter", "oppchoose", "plchoose", "winlose", "oppturn", "plturn")):
			Clock.schedule_once(partial(self.mconnect, self.net["status"]), 1)

	def mcheck_data(self, request, result):
		self.net["failed"] = False
		self.net["got"] = True
		mail[1] = self.net["room"]
		var = str(result)
		self.net["history"][self.net["select"]] = var
		if var.startswith("w"):
			self.gd["confirm_trigger"] = "Download"
			self.mcancel_create_bar.max = float(var.split("_")[1]) * 1024
			self.gd["confirm_var"] = {"c": "Download", "ind": var.split("_")[1]}
			Clock.schedule_once(self.confirm_popup)
		elif var.startswith("q"):
			if check_version(var.split("_")[1], __version__):  
				self.sd["update"] = var.split("_")[1]
				Clock.schedule_once(partial(self.popup_text, "update"))
			else:
				self.main_scrn.disabled = False
				self.sd["text"]["popup"].dismiss()
		elif var.startswith("1c"):
			self.net["time"] = 0
			self.net["status"] = "create"
			self.multiplay_cjpopup()
			self.mcreate_popup.open()
			self.net["room"] = int(result[2:])
			self.net["player"] = 1
			self.sd["text"]["popup"].dismiss()
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
				self.start_game()
			elif "r1_" in var and self.net["player"] == 1 and self.net["ready"] == 0:
				self.mcreate_popup.dismiss()
				Clock.schedule_once(partial(self.popup_text, "waitingopp"))
				self.net["ready"] = 1
				var = var.split("_")
				self.decks["2"] = [var[2], var[3], False, False]
				self.mping_data()
			else:
				if "making" in self.sd["text"]["c"]:
					self.sd["text"]["popup"].dismiss()
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
				if self.net["var1"] == "shufflest":
					if len(self.gd["shufflest"]) <= 0:
						self.sd["text"]["popup"].dismiss()
						self.net["select"] += 1
					self.shuffle_animation_st()
				else:
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
				elif "shufflest" in self.net["var1"]:
					Clock.schedule_once(self.shuffle_start_st, move_dt_btw)
				elif "shuffle" in self.net["var1"]:
					Clock.schedule_once(self.shuffle_start, move_dt_btw)
				elif "auto" in self.net["var1"] or "event" in self.net["var1"] or "act" in self.net["var1"]:
					Clock.schedule_once(self.stack_ability, ability_dt)
				elif "confirm" in self.net["var1"]:
					Clock.schedule_once(self.ability_effect, ability_dt)
				elif "perform" in self.net["var1"]:
					Clock.schedule_once(self.ability_event, ability_dt)
				elif "stacked" in self.net["var1"]:
					self.look_top("l")
				elif "searchopp" in self.net["var1"] or "looktopopp" in self.net["var1"]:
					Clock.schedule_once(self.ability_effect, ability_dt)
				elif "draw" in self.net["var1"]:
					Clock.schedule_once(self.draw, ability_dt)
				elif "numbers" in self.net["var1"]:
					if "oppturn" in self.gd["effect"]:
						if all(s == "" for s in self.net["act"][4]):
							self.net["act"][4] = []
						self.gd["target"] = []
					Clock.schedule_once(self.cardnum, ability_dt)
				elif "plchoose" in self.net["var1"]:
					if "salvage" in self.net["var1"]:
						self.net["send"] = False
						if self.net["act"][4]:
							self.net["act"][4] = []
						Clock.schedule_once(self.salvage)
					else:
						self.gd["oppchoose"] = True
						Clock.schedule_once(self.ability_effect)
				elif "oppchoose" in self.net["var1"]:
					if "search" in self.gd["ability_doing"]:
						Clock.schedule_once(self.search)
					elif "salvage" in self.gd["ability_doing"]:
						if "play" in self.net["var1"]:
							self.gd["target"].append("")
							st = self.net["var1"].split("_")
							self.play_to_stage(st[2], st[3])
						Clock.schedule_once(self.salvage)
					elif "looktop" in self.gd["ability_doing"]:
						self.look_top("l")
					elif "confirm" in self.gd["ability_doing"]:
						Clock.schedule_once(self.ability_effect)
					elif "hander" in self.gd["ability_doing"]:
						if any(s in self.gd["effect"] for s in ("do", "done")):
							self.gd["oppchoose"] = True
						Clock.schedule_once(self.ability_effect)
				elif "plturn" in self.net["var1"]:
					Clock.schedule_once(self.ability_effect)
				elif "end current" in self.net["var1"]:
					self.pd[self.gd["active"]]["done"][self.gd["phase"]] = True
					self.sd["btn"]["end"].disabled = True
					if "Attack" in self.gd["phase"]:
						self.attack_phase_end()
					elif "Climax" in self.gd["phase"]:
						self.gd["phase"] = "Attack"
						Clock.schedule_once(self.attack_phase_beginning, move_dt_btw)
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
							Clock.schedule_once(self.climax_phase_beginning, ability_dt)
						else:
							self.play_card()
				elif "Climax" in self.gd["phase"]:
					if "skip" in self.net["var1"]:
						self.climax_phase_beginning()
					elif "no climax" in self.net["var1"]:
						self.climax_phase_done()
					else:
						self.climax_phase()
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
					Clock.schedule_once(self.end_phase_beginning)
			else:
				self.mping_data()
		elif any(var.startswith(v) for v in ("z", "j", "m", "o")):
			var = var.split("_")
			if f"z{self.net['player']}" in var[0]:
				opp = var[1].split(".")

				if "shufflest" in self.net["var1"] and len(opp) == len(self.pd["2"]["Stock"]):
					self.pd["2"]["Stock"] = []
					for ind in opp:
						self.pd["2"]["Stock"].append(f"{ind}2")
					if len(self.gd["shufflest"]) <= 0:
						self.sd["text"]["popup"].dismiss()
						self.net["select"] += 1
					self.shuffle_animation_st()
				elif len(opp) == len(self.pd["2"]["Library"]):
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
				self.gd["j_hand_opp"] = var[1]
				self.net["select"] += 1
				self.janken_results()
			elif f"m{self.net['player']}" in var[0]:
				self.sd["text"]["popup"].dismiss()
				self.cardinfo.dismiss()
				self.multi_info["popup"].dismiss()
				self.gd["chosen"] = []
				if "x" not in var[1]:
					for ind in var[1].split("."):
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
				self.sd["btn"]["continue"].y = -Window.height * 2
				self.hand_btn_show(False)
				self.sd["cpop_press"] = []
				self.sd["text"]["popup"].dismiss()

				self.cardinfo.dismiss()
				self.multi_info["popup"].dismiss()
				self.net["select"] += 1
				self.net["wait"] = False
				cont = []
				if len(var) > 2:
					cont = var[2].split(".")
				if "lvu" in var[1]:
					self.gd["chosen"] = [f"{var[2].replace('l', '')}2"]
					self.level_up_done()
				elif any(var[2].startswith(s) for s in ("a", "t", "e", "p")):
					p = []
					c = []
					if "x" not in cont[3]:
						for ind in cont[3].split("~"):
							p.append(f"{ind}2")
					if "x" not in cont[4]:
						if "opc" in cont[4]:
							c = []
						else:
							for ind in cont[4].split("~"):
								try:
									c.append(f"{int(ind)}2")
								except ValueError:
									if "C" in ind:
										c.append(f"{ind.replace('C', 'Center')}")
									elif "B" in ind:
										c.append(f"{ind.replace('B', 'Back')}")
									else:
										c.append(f"{ind}")
							if c[0] == "l" or c[0] == "r":
								c[1] = int(c[1][0])
								c[2] = int(c[2][0])
					else:
						c = [""]
					if cont[6] == "-":
						cont[6] = "-1"
					self.net["act"] = [cont[0], f"{cont[1]}2", int(cont[2]), p, c, int(cont[5]), int(cont[6])]
					self.gd["confirm2"] = [True, int(cont[5])]
					if "t" in self.net["act"][0]:
						self.act_ability_show(player="2")
						self.act_ability(self.net["act"][1], self.net["act"][2])
					elif "a" in self.net["act"][0]:
						self.stack_resolve(self.net["act"][2], "2")
					elif "e" in self.net["act"][0]:
						self.ability_event()
					elif "p" in self.net["act"][0]:
						self.gd["waiting_cost"][2] = int(self.net["act"][5])
						if self.gd["waiting_cost"][2] == 2:
							if not self.gd["waiting_cost"][1]:
								_ = self.net["history"][self.net["select"] - 2].split("_")[-1]
								if self.net["act"][1] == f"{_[0]}2":
									if "C" in _:
										self.gd["waiting_cost"][1] = f"{_[0]}2_Center{_[2]}"
									elif "B" in _:
										self.gd["waiting_cost"][1] = f"{_[0]}2_Back{_[2]}"
							if not self.gd["waiting_cost"][1]:
								if self.gd["show_wait_popup"]:
									Clock.schedule_once(partial(self.popup_text, "waiting"), move_dt_btw)
								self.mconnect("phase")
							else:
								ind, st = self.gd["waiting_cost"][1].split("_")
								self.play([ind, st[:-1], st[-1]])
						else:
							self.stack_resolve(self.net["act"][2], "2")
				elif "och" in var[1]:
					self.net["send"] = True
					self.gd["oppchoose"] = True
					if "confirm" in self.gd["ability_doing"]:
						self.gd["confirm2"] = [True, int(var[2])]
						self.ability_effect()
					else:
						if "x" not in var[2]:
							for ind in cont:
								self.gd["chosen"].append(f"{ind}1")
						if "search" in self.gd["ability_doing"]:
							self.gd["p_c"] = "Search"
							self.search()
						elif "looktop" in self.gd["ability_doing"]:
							if "stack" in self.gd["effect"]:
								self.gd["p_c"] = "Look_stack"
							self.look_top("l")
						elif "hander" in self.gd["ability_doing"]:
							for _ in self.gd["chosen"]:
								self.gd["target"].append(_)
							if not self.gd["target"]:
								self.gd["target"].append("")
							self.gd["choose"] = True
							self.ability_effect()
				elif "pch" in var[1]:
					self.net["send"] = True
					self.gd["oppchoose"] = True
					if "x" not in var[2]:
						self.gd["target"] = var[2].split(".")
						for rr in range(len(self.gd["target"])):
							try:
								if self.gd["effect"] and self.gd["ability_trigger"]:
									ind = self.gd["ability_trigger"].split("_")[1]
									if ("opp" in self.gd["effect"] or "Opp" in self.gd["effect"]) and ind[-1] == "1":
										self.gd["target"][rr] = f"{int(self.gd['target'][rr])}2"
									elif ("opp" in self.gd["effect"] or "Opp" in self.gd["effect"]) and ind[-1] == "2":
										self.gd["target"][rr] = f"{int(self.gd['target'][rr])}1"
									elif "oppturn" in self.gd["effect"]:
										self.gd["target"][rr] = f"{int(self.gd['target'][rr])}2"
									else:
										self.gd["target"][rr] = f"{int(self.gd['target'][rr])}{ind[-1]}"
								else:
									self.gd["target"][rr] = f"{int(self.gd['target'][rr])}2"
							except ValueError:
								if "C" in self.gd["target"][rr] and len(self.gd["target"][rr]) <= 2:
									self.gd["target"][rr] = self.gd["target"][rr].replace("C", "Center")
								elif "B" in self.gd["target"][rr] and len(self.gd["target"][rr]) <= 2:
									self.gd["target"][rr] = self.gd["target"][rr].replace("B", "Back")
					else:
						self.gd["target"] = [""]

					if "looktop" in self.gd["ability_doing"]:
						self.gd["target"][1] = int(self.gd["target"][1][:-1])
						self.gd["target"][2] = int(self.gd["target"][2][:-1])
						self.look_top("l")
					elif "salvage" in self.gd["ability_doing"]:
						self.gd["p_c"] = "Salvage"
						self.salvage()
					elif "discard" in self.gd["ability_doing"]:
						self.gd["p_c"] = "Discard"
						if "invert" in self.gd["effect"]:
							self.gd["discard"] = len(self.gd["target"])
						self.discard()
					elif "give" in self.gd["ability_doing"]:
						self.give()
					elif "rest" in self.gd["ability_doing"]:
						self.gd["choose"] = True
						self.rest()
					elif "drawupto" in self.gd["ability_doing"]:
						if "plchoose" in self.gd["effect"]:
							if not self.net["act"][4]:
								self.net["act"][4] = list(self.gd["target"])
						self.ability_effect()
					elif "numbers" in self.gd["ability_doing"]:
						self.gd["numbers"] = str(self.gd["target"][0][0])
						self.popup_multi_info(cards=[f"n{self.gd['numbers']}"], owner="2", t="Numbers")
				elif var[1] in "Clock":
					self.gd["p_owner"] = "2"
					self.gd["chosen"] = []
					if "x" not in var[2]:
						for ind in cont:
							self.gd["chosen"].append(f"{ind}2")
					self.clock_phase_done()
				elif var[1] in "Main":
					if "x" not in var[2]:
						if "." not in var[2]:
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
								Clock.schedule_once(self.climax_phase_beginning, ability_dt)
						else:
							if "C" in cont[1]:
								opp = [f"{cont[0]}2", "Center", int(cont[2])]
							elif "B" in cont[1]:
								opp = [f"{cont[0]}2", "Back", int(cont[2])]
							else:
								_=[]
								if len(cont)>3:
									_ = cont[3].split("_")
									if _ and _[0]:
										self.gd["estock_pop"] = f"{cont[0]}2_Res_1"
										for r in _:
											self.gd["target"].append("es")
											self.gd["target"].append(f"{r}2")
								opp = [f"{cont[0]}2", "Res", cont[2],_]
							if opp[0] in self.pd["2"]["Hand"]:
								self.gd["opp_play"] = [opp]
								self.opp_play()
							elif opp[0] in self.pd["2"]["Center"] + self.pd["2"]["Back"]:
								self.gd["opp_move"] = [opp]
								self.opp_move()
				elif var[1] in "Climax":
					if "k" in var[2]:
						if "ca" in var[2]:
							self.end_to_end()
						elif "c" in var[2]:
							self.end_to_attack()
					elif "x" not in var[2]:
						self.play_climax(f"{var[2]}2")
						if self.gd["phase"] == "Main":
							self.pd[self.gd["active"]]["done"]["Main"] = True
							self.gd["phase"] = "Climax"
							self.gd["nomay"] = True
							Clock.schedule_once(self.climax_phase_beginning, ability_dt)
						else:
							Clock.schedule_once(self.climax_phase, ability_dt)
					else:
						self.end_to_attack()
				elif var[1] in "Declaration":
					if "x" not in var[2]:
						opp = [f"{cont[0]}2", cont[1], int(cont[2]), int(cont[3]), cont[4]]
						self.gd["opp_attack"].append(opp)
					self.opp_attack()
				elif var[1] in "Attack":
					if "x" in var[2]:
						self.end_current_phase()
				elif var[1] in "Counter":
					if "x" not in var[2]:
						if len(cont) > 3:
							_ = cont[3].split("_")
							if _ and _[0]:
								self.gd["estock_pop"] = f"{cont[0]}2_Res_1"
								for r in _:
									self.gd["target"].append("es")
									self.gd["target"].append(f"{r}2")
						self.gd["counter_id"] = f"{cont[0]}2"
						self.gd["rev_counter"] = True
						self.counter_done()
					else:
						self.counter_step_done()
				elif var[1] in "Encore":
					if "ke" in var[2]:
						self.skip_encore("2")
						self.encore_start()
					else:
						self.gd["encore_ind"] = f"{cont[0]}2"
						self.encore_middle()
				elif var[1] in "End":
					if "kn" in var[2]:
						self.gd["attack"] = 0
						self.attack_phase()
					else:
						if "x" not in var[2]:
							for ind in cont:
								self.gd["chosen"].append(f"{ind}2")
						self.hand_limit_done()
			else:
				self.mping_data()

	def add_deckpop_btn(self, start=False):
		deck_size = (self.sd["card"][0] * 1.5, self.sd["card"][1] * 1.5)
		for deck1 in sd:
			if start:
				if f"id{deck1}" in self.dpop:
					continue
				self.dpop[f"id{deck1}"] = ImgButton(source=f"atlas://{img_in}/other/grey", size=deck_size, cid=f"d{deck1}", card=self.sd["card"])
				self.dpop[f"id{deck1}"].btn.bind(on_release=self.popup_deck_slc, on_press=self.popup_deck_info)

			img = sd[deck1]["img"]
			source = "main"
			if img[:-4] in other_img or ("." not in img and img in other_img):
				source = "other"
				if "." in img:
					img = img[:-4]
			elif self.gd["DLimg"] and (img[:-4] in annex_img or (img in annex_img and "." not in img)):
				if not exists(f"{cache}/{img}"):
					source = "annex"
					if "." in img:
						img = img[:-4]

			if deck1.startswith("CE") or deck1.startswith("CJ"):
				if img[:-4] in annex_img or img[:-4] in other_img or ("." not in img and img in other_img) or (img in annex_img and "." not in img):
					pass
				elif not exists(f"{cache}/{img}"):
					source = "other"
					img = "grey"

			if "main" in source:
				if self.gd["DLimg"] and (exists(f"{cache}/{img}")):
					self.dpop[f"id{deck1}"].source = f"{cache}/{img}"
				else:
					self.dpop[f"id{deck1}"].source = f"atlas://{img_in}/other/grey"
			else:
				self.dpop[f"id{deck1}"].source = f"atlas://{img_in}/{source}/{img}"

	def update_deckpop_btn(self):
		self.decks["stack"].clear_widgets()
		temp = list(self.dpop.keys())
		for deck in temp:
			if "add" in deck:
				continue
			if deck[2:] not in sd:
				del self.dpop[deck]

	def get_index_stack(self, lst, m):
		n = len(lst) % m
		s = (m - n) / 2
		return -n, s

	def clear_loaded_game(self, dt=0):
		delete_load_file()
		self.gd = gdata_init()
		self.update_gdata_config()
		self.gd["load"] = False
		self.gd["gg"] = False
		self.gd["menu"] = False
		self.gd["ability_effect"] = []
		self.gd["p_c"] = ""
		self.gd["confirm_var"] = {}
		self.gd["confirm_temp"] = {}
		self.gd["phase"] = ""
		self.gd["p_ltitle"] = ""
		self.gd["p_t"] = []
		self.gd["target"] = []
		self.restart()
		self.net = network_init()
		self.decks["1"] = ["S11E000", "mat", False, False]
		self.decks["2"] = ["S11E000", "mat", False, False]
		if not self.gd["DLimg"]:
			self.decks["1"][1] = "nodl"
			self.decks["2"][1] = "nodl"

		if self.check_internet(ver=True):
			Clock.schedule_once(partial(self.popup_text, "version"))
			self.main_scrn.disabled = True
			self.mconnect("version")


	def main_menu(self, *args):
		self.sd["single"] = Button(text="Start Game", on_release=self.popup_network_slc, cid="single")
		self.network["multi_btn"] = Button(text="Multiplayer", on_release=self.popup_network_slc, cid="multi")
		self.network["deck_btn"] = Button(text="Deck Building", on_release=self.popup_network_slc, cid="ddd")
		self.network["setting_btn"] = Button(text="Settings", on_release=App.get_running_app().btn_open_settings)
		self.network["other_btn"] = Button(text="About", on_release=self.other_open, cid="other")
		self.sd["other"] = {}
		self.sd["other"]["down"] = Button(size_hint=(1, 1), text="Download", on_release=self.down_open)
		if not self.gd["multiplay_btn"]:
			self.network["multi_btn"].disabled = True
		if not self.gd["download_btn"]:
			self.sd["other"]["down"].disabled = True

		self.main_scrn = BoxLayout(orientation='vertical', size=(Window.width, Window.height))
		self.main_scrn.disabled = True
		boxv2 = BoxLayout(orientation='vertical')
		boxv3 = BoxLayout(orientation='horizontal')

		if self.gd["DLimg"]:
			img = Image(source=f"atlas://{img_in}/other/shiyoko", allow_stretch=True, size_hint=(1, 0.8))
		else:
			img = Image(source=f"atlas://{img_in}/other/icon-512", allow_stretch=True, size_hint=(1, 0.8))

		boxv3.add_widget(self.sd["other"]["down"])
		boxv3.add_widget(self.network["setting_btn"])
		boxv3.add_widget(self.network["other_btn"])

		boxv2.add_widget(self.sd["single"])
		boxv2.add_widget(self.network["multi_btn"])
		boxv2.add_widget(self.network["deck_btn"])
		boxv2.add_widget(boxv3)
		self.sd["main_btn"] = [self.network["multi_btn"], self.network["deck_btn"], self.sd["other"]["down"], self.network["other_btn"], self.sd["single"]]
		self.main_scrn.add_widget(img)
		self.main_scrn.add_widget(boxv2)
		self.parent.add_widget(self.main_scrn)

		self.parent.parent.version = __version__
		mail[0] = __version__
		self.scale_mat()
		Clock.schedule_once(self.start_setting)

	def scale_mat(self, per=1.00, t=True, player=""):
		if t:
			mat = self.mat["1"]["id"]

			total_height = (sp[mat]["card"][1] / 10 * 8 + (sp[mat]["size"][1] + sp[mat]["card"][1] * 1.5) * 2) * per + sp[mat]["card"][1] / 6 * 2
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
			for field in sp[mat].keys():
				if field in ("card", "pos", "size", "actual", "name", "img", "c"):
					continue
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
		self.sd["build_scv"].x = 0
		self.sd["b_bar"].x = 0
		self.sd["menu"]["btn"].x = -Window.width * 2
		self.mat["1"]["mat"].x = 0
		self.mat["1"]["mat"].y = -self.mat["1"]["mat"].size[1]
		self.mat["2"]["mat"].stand()
		self.mat["2"]["mat"].x = 0
		self.mat["2"]["mat"].y = -self.mat["2"]["mat"].size[1]
		self.parent.add_widget(self.decks["dbuild_btn"])
		self.decks["dbuild_btn"].pos = (0, 0)
		self.decks["sctm"].add_widget(self.decks["save"])
		self.decks["sctm"].add_widget(self.decks["import"])

		for item in self.deck_spinner:
			self.decks["sctm"].add_widget(self.decks["st"][f"{item}_box"])

		self.decks["dbuild"] = {"l": "", "qty": {}, "names": {}, "neo": {}, "ns": [], "c": True, "n": "", "t": "", "img": "", "jap": "", "name": "", "date": "", "deck": {}, "pos": {}}
		self.decks["dbuild"]["qty"]["inds"] = [f"{s}2" for s in range(1, 51)]  

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
			elif self.gd["DLimg"] and self.decks['dbuild']['img'] in annex_img:
				self.decks["st"]["image_btn"].source = f"atlas://{img_in}/annex/{self.decks['dbuild']['img']}"
			else:
				if self.gd["DLimg"] and (exists(f"{cache}/{self.decks['dbuild']['img']}")):
					self.decks["st"]["image_btn"].source = f"{cache}/{self.decks['dbuild']['img']}"
				else:
					self.decks["st"]["image_btn"].source = f"atlas://{img_in}/other/grey"
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


		self.decks["name_btn"].disabled = False
		self.decks["done_btn"].disabled = True

		if not self.decks["dbuild"]["n"]:
			self.decks["setting_pop"] = True
			self.popup_deck(t="setting")
		else:
			self.deck_building_cards()

	def check_card_neo(self, ind):
		if self.decks["dbuild"]["n"] and any(dset in ind for dset in self.decks["dbuild"]["ns"]):
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

		if d > 99:
			self.decks["add_btn"].disabled = True
		else:
			self.decks["add_btn"].disabled = False

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
				self.decks["st"]["format_spn"].text = "Neo-Standard"
				self.decks["dbuild"]["n"] = "Neo"
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
			elif "Neo" in self.decks["dbuild"]["n"]:
				self.decks["dbuild"]["ns"] = sn["Title"][self.decks["dbuild"]["t"]]
				self.decks["dbuild"]["ns"].extend(sn["Exception"]["Neo"]["All"])
				try:
					self.decks["dbuild"]["ns"].extend(sn["Exception"]["Neo"][self.decks["dbuild"]["t"]])
				except KeyError:
					pass
			else:
				self.decks["dbuild"]["ns"] = sn["Title"][self.decks["dbuild"]["t"]]
				try:
					self.decks["dbuild"]["ns"].extend(sn["Exception"][self.decks["dbuild"]["n"]][self.decks["dbuild"]["t"]])
				except KeyError:
					pass
		else:
			self.decks["dbuild"]["n"] = "Standard"
			self.decks["dbuild"]["ns"] = ["-"]

		if self.decks["dbuild"]["l"]:
			if not self.gd["filter_card"][0]:
				self.gd["filter_card"][0] = True
				self.gd["filter_card"][1] = [s for s in sorted(se["main"]["c"]) if any(end in s for end in ("EN", "-E", "-TE", "-PE", "/WX", "/SX", "BCS20", "BSF20")) and "DC/W01" not in s and "LB/W02" not in s]
				self.gd["filter_card"][2] = [s for s in sorted(se["main"]["c"]) if s not in self.gd["filter_card"][1]]

			if self.decks["dbuild"]["l"] == "e":
				self.gd["p_cards"] = list(sorted(self.gd["filter_card"][1]))
			elif self.decks["dbuild"]["l"] == "j":
				self.gd["p_cards"] = list(sorted(self.gd["filter_card"][2]))
			else:
				self.gd["p_cards"] = list(sorted(se["main"]["c"]))
		else:
			self.gd["p_cards"] = list(sorted(se["main"]["c"]))

		if self.decks["dbuild"]["n"]:
			self.gd["p_cards"] = [s for s in self.gd["p_cards"] if any(ns in s for ns in self.decks["dbuild"]["ns"])]

		if self.decks["dbuild"]["n"] == "Side" and "Schwarz" in self.decks["dbuild"]["t"]:
			self.gd["p_cards"] = [s for s in self.gd["p_cards"] if "CGS/" in s or sc[s]["side"] == "Schwarz"]
		elif self.decks["dbuild"]["n"] == "Side" and "Weiβ" in self.decks["dbuild"]["t"]:
			self.gd["p_cards"] = [s for s in self.gd["p_cards"] if "CGS/" in s or sc[s]["side"] == "Weiβ" or sc[s]["side"] == "Weiss"]

		trait = ["Trait"]
		for ind in self.gd["p_cards"]:
			for trt in sc[ind]["trait"]:
				if trt and trt not in trait:
					trait.append(trt)
			if len(sc[ind]["trait"]) == 0 and sc[ind]["type"] == "Character":
				if "No Trait" not in trait:
					trait.insert(1, "No Trait")
		self.sd["btn"]["ftrait"].values = trait

		self.gd["p_ld"] = list(sorted(self.cpop.keys()))

		for cc in self.skip_cpop:
			if cc in self.gd["p_ld"]:
				self.gd["p_ld"].remove(cc)

		for rr in range(popup_max_cards):
			if len(self.gd["p_ld"]) % popup_max_cards == 0:
				break
			self.gd["p_ld"].pop()

		Clock.schedule_once(self.deck_building_layout)

	def moving_touch_down(self, *args):
		if not self.hscv[2] and self.gd["p_c"] == "Add" and len(self.gd["p_fcards"]) > len(self.sd["popup"]["stack"].children):
			dc = self.sd["card"][1] + self.sd["padding"]
			dh = 1 / dc

			if self.sd["popup"]["p_scv"].scroll_y < dh * 2:
				if self.sim < len(self.gd["p_fcards"]):
					self.hscv[2] = 2
					for xx in range(popup_max_cards):
						temp = self.gd["p_l"].pop(0)
						self.gd["p_l"].append(temp)
						if temp in self.hscv[0]:
							self.hscv[0].remove(temp)
						if self.cpop[temp].cid not in self.hscv[1]:
							self.hscv[1].append(self.cpop[temp].cid)

						if self.sim == len(self.gd["p_fcards"]):
							if temp not in self.hscv[0]:
								self.hscv[0].append(temp)
							continue

						self.sim += 1

						self.cpop[temp].import_data(sc[self.gd["p_fcards"][self.sim - 1]],self.gd["DLimg"])
						if self.gd["p_fcards"][self.sim - 1] in self.decks["add_chosen"]:
							self.cpop[temp].selected_c()
						else:
							self.cpop[temp].selected_c(False)
						self.sin += 1
			elif self.sd["popup"]["p_scv"].scroll_y > 1 - dh * 2:
				if self.sin > 0:
					self.hscv[2] = 1
					for xx in range(popup_max_cards):
						temp = self.gd["p_l"].pop(-1)
						self.gd["p_l"].insert(0, temp)
						if temp in self.hscv[0]:
							self.hscv[0].remove(temp)

						if len(self.hscv[1]) > 0:
							tempid = self.hscv[1].pop(-1)
							self.cpop[temp].import_data(sc[tempid],self.gd["DLimg"])

							if tempid in self.decks["add_chosen"]:
								self.cpop[temp].selected_c()
							else:
								self.cpop[temp].selected_c(False)

						if self.sin != 0:
							self.sin -= 1
							self.sim -= 1

			if self.hscv[2]:
				for temp in self.gd["p_l"]:
					if self.cpop[temp] in self.sd["popup"]["stack"].children:
						self.sd["popup"]["stack"].remove_widget(self.cpop[temp])
					if temp not in self.hscv[0] and self.cpop[temp] not in self.sd["popup"]["stack"].children:
						self.sd["popup"]["stack"].add_widget(self.cpop[temp])
				if self.hscv[2] == 1:
					self.sd["popup"]["p_scv"].scroll_y += dh
					self.sd["popup"]["p_scv"].effect_y.value += dc
				else:
					self.sd["popup"]["p_scv"].scroll_y -= dh
					self.sd["popup"]["p_scv"].effect_y.value -= dc
				self.hscv[2] = 0

	def deck_building_layout(self, *args):
		self.sd["popup"]["stack"].clear_widgets()
		for ind in reversed(self.cd):
			if ind in self.skip_cpop:
				continue
			try:
				self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
			except (WidgetException, KeyError) as e:
				pass
			try:
				self.sd["build_layout"].add_widget(self.cd[ind])
			except WidgetException:
				pass
			self.cd[ind].stand(a=False)
			self.cd[ind].pos = (-Window.width * 2, 0)
			if ind.endswith("1"):
				self.decks["dbtn"][f"{ind}bb"].pos = (-Window.width * 2, 0)

		self.hand_btn_show(False)
		ypos = self.sd["padding"] * 1.5
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
		self.sd["build_layout"].size = (Window.width, Window.height - self.sd["b_bar"].size[1])

		for it in (d_0, d_1, d_2, d_3, d_cx):
			d_r += int(ceil(len(it) / dbuild_limit))
		self.sd["build_scv"].do_scroll_y = False
		self.sd["build_scv"].do_scroll_y = False
		if d_r > 0:
			self.sd["build_layout"].size = (Window.width, d_height * d_r + ypos * 2)
			if d_r > 7:
				self.sd["build_scv"].do_scroll_y = True
			d_r -= 1

		inx = 1

		for item in (d_0, d_1, d_2, d_3, d_cx):
			xpos = 0
			c = 0

			if len(item) % dbuild_limit == 0:
				d_j = int(dbuild_limit)
			else:
				d_j = len(item) % dbuild_limit

			for ind in sorted(item):
				self.cd[f"{inx}1"].import_data(sc[ind],self.gd["DLimg"])
				self.cd[f"{inx}1"].show_front()

				if len(item) > dbuild_limit and dbuild_limit % 2 == 0 and d_r > 0:
					xpos = Window.width / 2. - self.sd["padding"] / 2 * 0 - dbuild_limit / 2. * d_width + d_width * c
				elif len(item) > dbuild_limit and dbuild_limit % 2 != 0 and d_r > 0:
					xpos = Window.width / 2. - self.sd["padding"] / 2 * 0 - (dbuild_limit - 1) / 2. * d_width - self.sd["card"][1] / 2. + d_width * c
				elif d_j % 2 != 0:
					xpos = Window.width / 2. - self.sd["padding"] / 2 * 0 - (d_j - 1) / 2. * d_width - self.sd["card"][1] / 2. + d_width * c
				elif d_j % 2 == 0:
					xpos = Window.width / 2. - self.sd["padding"] / 2. * 0 - d_j / 2. * d_width + d_width * c

				self.decks["dbtn"][f"{inx}1bb"].x = xpos
				self.decks["dbtn"][f"{inx}1bb"].y = ypos + d_height * d_r + self.sd["padding"] / 3
				ybar = self.decks["dbtn"][f"{inx}1bb"].y + self.decks["dbtn"][f"{inx}1bb"].size[1] + self.sd["padding"] * 0.25


				self.cd[f"{inx}1"].y = ybar
				self.decks["dbuild"]["pos"][f"{inx}1"] = (xpos, ybar, self.mat["1"]["mat"].size[1])

				self.update_qty_card(f"{inx}1")

				self.decks["dbtn"][f"{inx}1t"].text = str(self.decks["dbuild"]["deck"][ind])
				inx += 1
				c += 1
				if c >= dbuild_limit:
					d_r -= 1
					c = 0
			if len(item) > 0 and len(item) % dbuild_limit != 0:
				d_r -= 1

		self.update_deck_label()
		self.update_deck_names()
		self.sd["text"]["popup"].dismiss()


	def deck_import(self, dt=0, *arg):
		_ = self.net[self.decks["st"]["import_spn"].text]
		d = self.decks["st"]["import_btn"].text.split(_)[1]
		url = ""
		if d:
			url = f'https://{_}{d}'
		if platform == "android":
			self.get_html(url)
		else:
			if url:
				session = HTMLSession()
				r = session.get(url)
				r.html.render(sleep=3)
				if "EncoreDecks" in self.decks["st"]["import_spn"].text:
					self.decks["dbuild"]["name"] = str(r.html.find('h2')[0].text)
					self.decks["st"]["name_btn"].text = self.decks["dbuild"]["name"]
					cards = []
					images = []
					l = []
					s = []
					i = []
					_ = r.html.find('sup')
					for c in _:
						cards.append(c.attrs["title"])
					_ = r.html.find('img')

					for c in _:
						if "images/JP" in c.attrs["src"] or "images/EN" in c.attrs["src"]:
							images.append(c.attrs["src"])

					for _ in images:
						t = _.split("/")
						l.append(t[2])
						s.append(t[3])
						i.append(t[4].split(".")[0])

					l = list(set(l))
					ss = list(set(s))

					if len(l) == 1:
						self.decks["dbuild"]["l"] = str(l[0][0].lower())
					else:
						self.decks["dbuild"]["l"] = "b"

					cc = [c for c in sorted(se["main"]["c"]) if any(_ in c for _ in ss)]
					for inx in range(len(i)):
						for _ in cc:
							if s[inx] in _ and i[inx] in _:
								self.decks["dbuild"]["deck"][_] = int(cards[inx])
								break

					s = []
					for _ in self.decks["dbuild"]["deck"]:
						s.append(f"{_.split('/')[0]}/")
					s = list(set(s))

					l = []
					if s:
						for cc in self.decks["dbuild"]["deck"]:
							for _ in se["neo"]["Title"]:
								if any(ss in cc for ss in se["neo"]["Title"][_]):
									l.append(_)
									break

					l = list(set(l))
					if len(l) == 1:
						self.decks["dbuild"]["t"] = str(l[0])
						self.decks["dbuild"]["n"] = "Title"
					else:
						self.decks["dbuild"]["n"] = "Standard"
				elif "DECK LOG" in self.decks["st"]["import_spn"].text:
					if self.decks["st"]["import_spn"].text.endswith("EN"):
						self.decks["dbuild"]["name"] = str(r.html.find('h2')[0].text.split("]")[0].split("[")[-1])
					elif self.decks["st"]["import_spn"].text.endswith("JP"):
						self.decks["dbuild"]["name"] = str(r.html.find('h2')[0].text.split("」")[0].split("「")[-1])
					self.decks["st"]["name_btn"].text = self.decks["dbuild"]["name"]
					cards = []
					images = []
					l = []
					s = []

					_ = r.html.find('.num')
					for c in _:
						cards.append(c.text)

					_ = r.html.find('img')
					for c in _:
						if "title" in c.attrs:
							if " :" in c.attrs["title"]:
								images.append(c.attrs["title"].split(" :")[0])
							else:
								images.append(c.attrs["title"])

					if self.decks["st"]["import_spn"].text.endswith("EN"):
						self.decks["dbuild"]["l"] = "e"
					elif self.decks["st"]["import_spn"].text.endswith("JP"):
						self.decks["dbuild"]["l"] = "j"
					else:
						self.decks["dbuild"]["l"] = "b"

					for _ in range(len(images)):
						self.decks["dbuild"]["deck"][images[_]] = int(cards[_])

					s = []
					for _ in self.decks["dbuild"]["deck"]:
						s.append(f"{_.split('/')[0]}/")
					s = list(set(s))

					l = []
					if s:
						for cc in self.decks["dbuild"]["deck"]:
							for _ in se["neo"]["Title"]:
								if any(ss in cc for ss in se["neo"]["Title"][_]):
									l.append(_)
									break

					l = list(set(l))
					if len(l) == 1:
						self.decks["dbuild"]["t"] = str(l[0])
						self.decks["dbuild"]["n"] = "Title"
					else:
						self.decks["dbuild"]["n"] = "Standard"

				if self.decks["dbuild"]["l"] == "j":
					self.decks["st"]["lang_spn"].text = "Jap"
				elif self.decks["dbuild"]["l"] == "e":
					self.decks["st"]["lang_spn"].text = "Eng"
				else:
					self.decks["st"]["lang_spn"].text = "Both"

				if self.decks["dbuild"]["deck"]:
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

				session.close()
			self.deck_building_cards()

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
		if not self.decks["add_btn"].disabled:
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
			else:
				if self.decks["dbuild"]["deck"][inx] == 2:
					self.cd[ind].y = self.decks["dbuild"]["pos"][ind][1] + sep / 3 * 2
				elif self.decks["dbuild"]["deck"][inx] == 3:
					self.cd[ind].y = self.decks["dbuild"]["pos"][ind][1] + sep / 3
				elif self.decks["dbuild"]["deck"][inx] >= 4:
					self.cd[ind].y = self.decks["dbuild"]["pos"][ind][1]
				for nx in range(len(self.decks["dbuild"]["qty"][inx])):
					inq = self.decks["dbuild"]["qty"][inx][nx]

					self.cd[inq].y = self.cd[ind].y - sep + sep / 3 * 2 * (nx + 1)
					self.cd[inq].x = self.cd[ind].x + sep
					self.cd[inq].climax(a=False)
					self.cd[inq].show_back()
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
					inq = self.decks["dbuild"]["qty"][inx][nx]
					self.cd[inq].x = self.cd[ind].x + sep / 3 * 2 * (nx + 1)
					self.cd[inq].y = self.cd[ind].y
					self.cd[inq].show_back()

		if self.decks["dbuild"]["deck"][inx] > 1:
			for nx in reversed(range(len(self.decks["dbuild"]["qty"][inx]))):
				inq = self.decks["dbuild"]["qty"][inx][nx]
				self.sd["build_layout"].remove_widget(self.cd[inq])
				self.sd["build_layout"].add_widget(self.cd[inq])

		self.sd["build_layout"].remove_widget(self.cd[ind])
		self.sd["build_layout"].add_widget(self.cd[ind])

		for ind in self.decks["dbuild"]["qty"]["inds"]:
			self.cd[ind].stand(a=False)
			self.cd[ind].pos = (-Window.width * 2, 0)

	def clear_building(self, *args):
		self.mat["1"]["mat"].pos = (-Window.width * 2, Window.height / 2 - self.sd["padding"] - self.sd["card"][1] / 6 - self.mat["1"]["mat"].height)
		self.mat["2"]["mat"].pos = (-Window.width * 2, Window.height / 2 + self.sd["padding"] + self.sd["card"][1] / 6)
		self.mat["2"]["mat"].reverse()
		self.sd["b_bar"].x = -Window.width * 2
		self.sd["build_scv"].x = -Window.width * 2

		for ind in self.cd:
			if ind in self.emptycards or ind == "1" or ind == "2":
				continue
			self.cd[ind].stand(a=False)
			self.cd[ind].pos = (0, 0)
			if ind.endswith("3"):
				self.cd[ind].pos = (-Window.width * 2, 0)
			elif not ind.endswith("0"):
				self.sd["build_layout"].remove_widget(self.cd[ind])
				try:
					self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])
				except WidgetException:
					pass

		self.hand_btn_show(False)
		for inx in range(1, 51):
			self.decks["dbtn"][f"{inx}1bb"].x = -Window.width * 2

		for item in self.deck_spinner:
			self.decks["sctm"].remove_widget(self.decks["st"][f"{item}_box"])

		self.decks["sctm"].remove_widget(self.decks["save"])
		self.decks["sctm"].remove_widget(self.decks["import"])
		self.decks["st"]["name_btn"].text = ""
		self.decks["st"]["format_spn"].text = "-"
		self.decks["st"]["format_btn"].text = ""
		self.decks["st"]["import_spn"].text = "-"
		self.decks["st"]["import_btn"].text = ""
		self.decks["st"]["import_btn"].disabled = True
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

			if self.decks["50"].text[:2] == "50":
				self.decks["dbuild"]["c"] = True
				if self.decks["8"].text[0] > "8":
					self.decks["dbuild"]["c"] = False
			else:
				self.decks["dbuild"]["c"] = False

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
			self.add_deckpop_btn(start=True)

		self.gd["update_edata"] = False
		Clock.schedule_once(self.clear_building)
		Clock.schedule_once(self.update_edata)
		Clock.schedule_once(self.wait_update, move_dt_btw)

	def building_btn(self, btn):
		if btn.cid == "done":
			self.decks["popup"].dismiss()
			self.popup_text("Loading")
			if "Import" in self.decks["popup"].title:
				self.decks["st"]["import_spn"].text = "-"
				self.decks["close"].disabled = True
				Clock.schedule_once(partial(self.popup_deck, "setting"), popup_dt)
			else:
				Clock.schedule_once(self.building_btn_done)
		elif btn.cid == "name":
			self.decks["setting_pop"] = True
			self.popup_deck(t="setting_img")
		elif btn.cid == "close":
			self.sd["cpop_press"] = []
			self.decks["add_chosen"] = []
			self.sd["popup"]["popup"].dismiss()
			self.gd["popup_pop"] = False
		elif btn.cid == "add":
			self.popup_text("Loading")
			Clock.schedule_once(self.add_building_popup)
		elif btn.cid == "adding":
			self.gd["popup_pop"] = False
			self.popup_text("Loading")
			self.decks["done_btn"].disabled = True
			self.sd["popup"]["popup"].dismiss()
			self.sd["cpop_press"] = []
			if self.sd["cpop_pressing"] is not None:
				self.sd["cpop_pressing"].cancel()
				self.sd["cpop_pressing"] = None
			if int(self.decks["50"].text.split("/")[0]) < 100 and len(self.decks["dbuild"]["deck"]) < 50:
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
		elif btn.cid == "import":
			self.decks["popup"].dismiss()
			self.popup_text("Loading")
			Clock.schedule_once(partial(self.popup_deck, "import"), popup_dt)


	def add_building_popup(self, *args):
		self.sd["popup"]["popup"].title = "Add cards to deck"
		self.gd["confirm_var"] = {"o": "1", "c": "Add", "m": 1}
		self.hscv = [[], [], 0]
		self.popup_start()

	def popup_filter_add(self, spinner, text):
		if "Lvl" in text:
			self.gd["p_flvl"] = text
		elif any(text == s for s in self.sd["btn"]["fcolour"].values):
			self.gd["p_fcolour"] = text
		elif any(text == s for s in self.sd["btn"]["ftype"].values):
			self.gd["p_ftype"] = text
		elif any(text == s for s in self.sd["btn"]["ftrait"].values):
			self.gd["p_ftrait"] = text
		elif any(text == s for s in self.sd["btn"]["ftextl"].values):
			self.gd["p_ftext"] = self.sd["btn"]["ftext"].text
		elif text != "":
			self.gd["p_ftext"] = text
		else:
			self.gd["p_ftext"] = ""

		if "Add" in self.gd["p_c"]:
			self.hscv = [[], [], 0]
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
				self.gd["p_fcards"] = [s for s in self.gd["p_fcards"] if sc[s]["level"] == int(self.gd["p_flvl"][-1]) and sc[s]["type"] != "Climax"]
			else:
				self.gd["p_fcards"] = [s for s in self.gd["p_fcards"] if sc[s]["level"] == int(self.gd["p_flvl"][-1])]
		if self.gd["p_fcolour"] != "Colour":
			self.gd["p_fcards"] = [s for s in self.gd["p_fcards"] if sc[s]["colour"] == self.gd["p_fcolour"]]
		if self.gd["p_ftype"] != "Type":
			self.gd["p_fcards"] = [s for s in self.gd["p_fcards"] if sc[s]["type"] == self.gd["p_ftype"]]
		if self.gd["p_ftrait"] != "Trait":
			if self.gd["p_ftrait"] == "No Trait":
				self.gd["p_fcards"] = [s for s in self.gd["p_fcards"] if sc[s]["type"] == "Character" and len(sc[s]["trait"]) == 0]
			else:
				self.gd["p_fcards"] = [s for s in self.gd["p_fcards"] if self.gd["p_ftrait"] in sc[s]["trait"]]
		if self.gd["p_ftext"] != "":
			if self.sd["btn"]["ftextl"].text == "Name":
				self.gd["p_fcards"] = [s for s in self.gd["p_fcards"] if self.gd["p_ftext"].lower() in sc[s]["name"].lower()]
			elif self.sd["btn"]["ftextl"].text == "Card No":
				self.gd["p_fcards"] = [s for s in self.gd["p_fcards"] if self.gd["p_ftext"].lower() in sc[s]["id"].lower()]
			elif self.sd["btn"]["ftextl"].text == "Text":
				self.gd["p_fcards"] = [s for s in self.gd["p_fcards"] if any(self.gd["p_ftext"].lower() in tex.lower() for tex in sc[s]["text"])]
		self.gd["p_l"] = self.gd["p_ld"][:len(self.gd["p_fcards"])]

	def deck_create(self, *args):
		self.cd[""] = CardEmpty()
		self.cd["1"] = Card(code="1", card=self.sd["card"], owner="1", per=self.mat["1"]["per"])
		self.cd["2"] = Card(code="2", card=self.sd["card"], owner="2", per=self.mat["2"]["per"])
		self.cd["sspace"] = CardEmpty()
		self.cd["1"].show_front()
		self.cd["2"].show_front()
		for player in list(self.pd.keys()):  
			for inx in range(1, 51):
				ind = f"{inx}{player}"
				if player not in self.pd:
					per = self.mat["1"]["per"]
				else:
					per = self.mat[player]["per"]
				self.cd[ind] = Card(code=ind, card=self.sd["card"], owner=player, per=per)
				self.cd[ind].setPos(xpos=-Window.width, ypos=-Window.height, a=False, t="Library")
				self.cd[ind].btn.bind(on_press=self.card_btn_press, on_release=self.card_btn_release)
				self.cd[ind].show_back()
				if player in self.pd:
					self.mat[player]["mat"].add_widget(self.cd[ind])
					if ind not in self.pd[player]["Library"]:
						self.pd[player]["Library"].append(ind)

				if player in self.pd:
					self.cpop[ind] = CardImg(ind, self.sd["card"], player, self.mat[player]["per"])
					self.cpop[ind].btn.bind(on_press=self.card_btn_press, on_release=self.card_btn_release)

	def deck_fill(self, *args):
		for player in list(self.pd.keys()):
			self.gd["inx"] = 1
			for card in sorted(self.pd[player]["deck"].keys()):
				for nx in range(self.pd[player]["deck"][card]):
					if self.gd["inx"] > 50:
						continue
					ind = f"{self.gd['inx']}{player}"
					if card in cont_waiting:
						self.check_cont_waiting.append(ind)
					if card in cont_waiting_cost:
						self.check_waiting_cost.append(ind)
						if card not in self.gd["waiting_cost"]:
							for text in sc[card]["text"]:
								eff = ab.cont(text)
								if "waiting_cost" in eff:
									self.gd["waiting_cost"][0][card] = [eff[1], eff[eff.index("waiting_cost") + 1], text]
									break
					try:
						self.mat[player]["mat"].add_widget(self.cd[ind])
					except WidgetException:
						pass
					self.cd[ind].import_data(sc[card],self.gd["DLimg"])
					self.cd[ind].setPos(field=self.mat[player]["field"]["Library"], a=False, t="Library")
					self.cd[ind].setPos(field=self.mat[player]["field"]["Library"], a=False, t="Library")
					self.cd[ind].setPos(field=self.mat[player]["field"]["Library"], t="Library")
					self.cpop[ind].import_data(sc[card],self.gd["DLimg"])
					self.gd["inx"] += 1

	def on_touch_down(self, touch):
		self.sd["touch_down"] = touch.pos
		if self.gd["game_start"] and self.gd["active"] != "" and self.gd["active"] is not None:

			if self.gd["phase"] not in ("Draw", "Janken", "Stand Up", "") and self.gd["ability_doing"] != "drawupto":  
				if self.gd["popup_on"] or self.gd["active"] == "1":
					for field in self.gd["fields"]:
						for card in self.pd[self.gd["active"]][field]:
							if card == "":
								continue

							width = (self.mat[self.gd["active"]]["mat"].x + self.cd[card].x, self.mat[self.gd["active"]]["mat"].x + self.cd[card].x + self.sd["card"][0])
							height = (self.mat[self.gd["active"]]["mat"].y + self.cd[card].y, self.mat[self.gd["active"]]["mat"].y + self.cd[card].y + self.sd["card"][1])

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
		if self.gd["game_start"] and (self.gd["phase"] == "Main" or self.gd["phase"] == "Climax") and self.gd["active"] == "1":
			if self.sd["touch_down"] and (touch.pos[0] / self.sd["touch_down"][0] >= 1.33 or touch.pos[0] / self.sd["touch_down"][0] <= 0.67) and (touch.pos[1] / self.sd["touch_down"][1] >= 1.33 or touch.pos[1] / self.sd["touch_down"][1] <= 0.67):
				self.gd["moving"] = True
			if self.infot:
				self.infot.cancel()
				self.infot = None
			if self.infob:
				self.infob.cancel()
				self.infob = None
			if self.gd["selected"] != "" and self.gd["selected"] in self.gd["movable"] and self.sd["touch_down"] is not None:
				self.act_ability_show(hide=True)
				self.gd["touch_move_x"] = touch.pos[0] - self.sd["touch_down"][0]

				card = self.cd[self.gd["selected"]]
				self.mat[self.gd["selected"][-1]]["mat"].remove_widget(card)
				self.mat[self.gd["selected"][-1]]["mat"].add_widget(card)
				width = (self.mat[self.gd["active"]]["field"]["Climax"][0] - self.sd["card"][1] / 2., self.mat[self.gd["active"]]["field"]["Climax"][0] + self.sd["card"][1] + self.sd["card"][1] / 2.)
				height = (self.mat[self.gd["active"]]["field"]["Climax"][1] - self.sd["card"][0] / 2., self.mat[self.gd["active"]]["field"]["Climax"][1] + self.sd["card"][0] + self.sd["card"][0] / 2.)

				if card.card == "Climax" and width[0] < card.center_x < width[1] and height[0] < card.center_y < height[1]:
					card.climax()
				elif card.card == "Climax" and card.status == "":
					card.stand()

				self.gd["touch_move_y"] = touch.pos[1] - self.sd["touch_down"][1]
				if not self.gd["confirm_requirement"] and "Hand" in card.pos_new:
					if card.card == "Climax" and card.mcolour.lower() not in self.pd[self.gd["active"]]["colour"] and touch.pos[1] >= self.mat[self.gd["active"]]["mat"].y:
						self.gd["touch_move_y"] = self.mat[self.gd["active"]]["mat"].y - self.sd["touch_down"][1]
					elif card.card != "Climax" and card.level_t != 0:
						if len(self.pd[self.gd["active"]]["Level"]) < card.level_t and touch.pos[1] >= self.mat[self.gd["active"]]["mat"].y:
							self.gd["touch_move_y"] = self.mat[self.gd["active"]]["mat"].y - self.sd["touch_down"][1]
						elif len(self.pd[self.gd["active"]]["Level"]) >= card.level_t and card.mcolour.lower() not in self.pd[self.gd["active"]]["colour"] and touch.pos[1] >= self.mat[self.gd["active"]]["mat"].y:
							self.gd["touch_move_y"] = self.mat[self.gd["active"]]["mat"].y - self.sd["touch_down"][1]
						elif len(self.pd[self.gd["active"]]["Level"]) >= card.level_t and card.mcolour.lower() in self.pd[self.gd["active"]]["colour"] and len(self.pd[self.gd["active"]]["Stock"]) < card.cost_t and touch.pos[1] >= self.mat[self.gd["active"]]["mat"].y:
							self.gd["touch_move_y"] = self.mat[self.gd["active"]]["mat"].y - self.sd["touch_down"][1]

				card.center_y = self.gd["old_pos"][1] + self.gd["touch_move_y"] + self.sd["card"][1] / 2.
				card.center_x = self.gd["old_pos"][0] + self.gd["touch_move_x"] + self.sd["card"][0] / 2.

		return True

	def on_touch_up(self, touch):
		if self.infot:
			self.infot.cancel()
			self.infot = None
		self.sd["touch_down"] = None
		if self.gd["game_start"] and self.gd["phase"] == "Main":
			if self.gd["selected"] != "":
				card = self.cd[self.gd["selected"]]

				if self.gd["selected"] in self.pd[self.gd["active"]]["Hand"]:
					fields = list(self.gd["stage"]) + ["Climax"]

					if touch.pos[1] <= self.mat[self.gd["active"]]["mat"].y:
						for ncard in self.pd[self.gd["active"]]["Hand"]:
							width = (self.cd[ncard].x, self.cd[ncard].x + self.sd["card"][0])
							height = (self.cd[ncard].y, self.cd[ncard].y + self.sd["card"][1])

							if width[0] < self.cd[self.gd["selected"]].center_x < width[1] and height[0] < self.cd[self.gd["selected"]].center_y < height[1] and ncard != self.gd["selected"]:
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
						self.update_movable(self.gd["active"])
					else:
						if card.card == "Event":
							if touch.pos[1] > self.mat[self.gd["active"]]["mat"].y + self.sd["card"][0]:
								if not self.check_condition(self.gd["selected"]):
									Clock.schedule_once(self.check_cont_ability, ability_dt)
									self.gd["selected"] = ""
									self.hand_size(self.gd["active"])
									return True

								self.play([self.gd["selected"], "Res", ""])
						else:
							for field in fields:
								width = (self.mat[self.gd["active"]]["field"][field][0], self.mat[self.gd["active"]]["field"][field][0] + self.sd["card"][0])
								height = (self.mat[self.gd["active"]]["field"][field][1], self.mat[self.gd["active"]]["field"][field][1] + self.sd["card"][1])

								if width[0] < card.center_x < width[1] and height[0] < card.center_y < height[1]:
									if not self.check_condition(self.gd["selected"]):
										break
									if field == "Climax" and card.card == "Climax":
										self.play_climax(self.gd["selected"])
										self.gd["selected"] = ""
										self.pd[self.gd["active"]]["done"]["Main"] = True
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
											Clock.schedule_once(self.climax_phase_beginning, ability_dt)

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

							if not self.gd["waiting_cost"][1]:
								self.hand_size(self.gd["active"])
								self.update_movable(self.gd["active"])
							self.gd["selected"] = ""
				elif any(self.gd["selected"] in self.pd[self.gd["active"]][field] for field in ("Center", "Back")):
					for field in self.gd["stage"]:
						width = (self.mat[self.gd["active"]]["field"][field][0], self.mat[self.gd["active"]]["field"][field][0] + self.sd["card"][0])
						height = (self.mat[self.gd["active"]]["field"][field][1], self.mat[self.gd["active"]]["field"][field][1] + self.sd["card"][1])

						if width[0] < card.center_x < width[1] and height[0] < card.center_y < height[1]:
							if field != card.pos_new:
								if self.pd[self.gd["active"]][field[:-1]][int(field[-1])] != "":
									if self.pd[self.gd["active"]][field[:-1]][int(field[-1])] in self.gd["movable"]:
										temp = self.pd[self.gd["active"]][field[:-1]][int(field[-1])]
										self.cd[temp].setPos(field=self.mat[temp[-1]]["field"][card.pos_new], t=card.pos_new)
										self.pd[self.gd["active"]][card.pos_new[:-1]][int(card.pos_new[-1])] = temp
									else:
										break
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
								self.shelve_save()
							break

					card.setPos(field=self.mat[card.owner]["field"][card.pos_new], t=card.pos_new)
					self.update_marker()
					self.check_cont_ability()
					self.update_movable(self.gd["active"])

				self.gd["selected"] = ""
				if not self.gd["play"]:
					self.hand_size(self.gd["active"])

		if self.gd["game_start"] and self.gd["phase"] == "Climax":
			if self.gd["selected"] != "":
				card = self.cd[self.gd["selected"]]
				width = (self.mat[self.gd["active"]]["field"]["Climax"][0], self.mat[self.gd["active"]]["field"]["Climax"][0] + self.sd["card"][0])
				height = (self.mat[self.gd["active"]]["field"]["Climax"][1], self.mat[self.gd["active"]]["field"]["Climax"][1] + self.sd["card"][1])

				if width[0] < card.center_x < width[1] and height[0] < card.center_y < height[1]:
					if self.check_condition(self.gd["selected"]):
						self.gd["movable"] = []
						self.gd["playable_climax"] = []
						self.play_climax(self.gd["selected"])
						self.gd["selected"] = ""
						Clock.schedule_once(self.climax_phase, ability_dt)

			self.gd["selected"] = ""
			self.hand_size(self.gd["active"])

		if self.gd["game_start"] and self.gd["phase"] == "End":
			self.hand_size(self.gd["active"])

		return True

	def field_btn_fill(self, dt=0):
		pos = (-Window.width * 2, -Window.height * 2)
		for player in list(self.pd.keys()):
			for field in self.mat[player]["field"]:
				if field == "Level":
					size = (self.sd["card"][1], abs(self.mat[player]["field"][field][3] - self.mat[player]["field"][field][1]) + self.sd["card"][0])
				elif field == "Stock":
					size = (self.sd["card"][1], abs(self.mat[player]["field"][field][3] - self.mat[player]["field"][field][1]) + self.sd["card"][0])
				elif field == "Climax" or field == "Memory":
					size = (self.sd["card"][1], self.sd["card"][0])
				elif field == "Clock":
					size = (abs(self.mat[player]["field"][field][2] - self.mat[player]["field"][field][0]) + self.sd["card"][0], self.sd["card"][1])
				elif field == "Res":
					size = (abs(self.mat[player]["field"][field][2] - self.mat[player]["field"][field][0] + self.sd["card"][0]), abs(self.mat[player]["field"][field][3] - self.mat[player]["field"][field][1] + self.sd["card"][1]))

					size1 = (self.sd["card"][0], abs(self.mat[player]["field"]["Library"][1] + self.sd["card"][1] - self.mat[player]["mat"].pos_mat[1]))

					self.field_btn[f"{field}1{player}"] = Button(text=f"{field}1", cid=field + player, pos=pos, opacity=0, on_press=self.show_info_btn, size=size1, on_release=self.show_info_re)
					self.parent.add_widget(self.field_btn[f"{field}1{player}"])
				else:
					size = self.sd["card"]

				self.field_btn[f"{field}{player}"] = Button(text=field, cid=f"{field}{player}", opacity=0, pos=pos, size=size, on_press=self.show_info_btn, on_release=self.show_info_re)
				self.parent.add_widget(self.field_btn[f"{field}{player}"])

			for r in range(select2cards):
				self.field_btn[f"stage{r}{player}s"] = Image(source=f"atlas://{img_in}/other/select2", size=(self.sd["card"][0] + self.sd["padding"] * 2, self.sd["card"][1] + self.sd["padding"] * 2), pos=pos, size_hint=(None, None), allow_stretch=True, keep_ratio=False)
				self.mat[f"{player}"]["mat"].add_widget(self.field_btn[f"stage{r}{player}s"])

			for field in self.gd["stage"]:
				size = (self.sd["card"][0] + self.sd["padding"] * 2, self.sd["card"][1] + self.sd["padding"] * 2)
				pos = (-Window.width * 5, self.mat[player]["field"][field][1] - self.sd["padding"] + self.mat[player]["mat"].y)
				self.field_btn[f"{field}{player}s"] = Image(source=f"atlas://{img_in}/other/movable", size=size, pos=pos, size_hint=(None, None), allow_stretch=True, keep_ratio=False)
				self.mat[player]["mat"].add_widget(self.field_btn[f"{field}{player}s"])
		self.sd["field_btn_fill"] = True

	def field_btn_pos(self, dt=0):
		sep = (self.sd["card"][1] - self.sd["card"][0]) / 2
		for player in list(self.pd.keys()):
			for field in self.mat[player]["field"]:
				if field == "Res":
					if player == "1":
						pos1 = (self.mat[player]["field"]["Library"][0] - self.sd["padding"] / 4 - self.sd["card"][0] + self.mat[player]["mat"].x, self.mat[player]["mat"].y + self.mat[player]["field"]["Library"][1] + self.sd["card"][1] - self.field_btn[f"{field}1{player}"].size[1])
					elif player == "2":
						pos1 = (self.mat[player]["mat"].x + self.mat[player]["mat"].size[0] + self.sd["card"][0] + self.sd["padding"] / 4 - self.sd["card"][0] - self.mat[player]["field"]["Library"][0], self.mat[player]["mat"].y + self.mat[player]["mat"].size[1] - self.mat[player]["field"]["Library"][1] - self.sd["card"][1])

					self.field_btn[f"{field}1{player}"].x = Window.width * 5
				if player == "1":
					pos = (self.mat[player]["field"][field][0] + self.mat[player]["mat"].x, self.mat[player]["field"][field][1] + self.mat[player]["mat"].y)

					if field == "Climax" or field == "Memory" or field == "Level":
						pos = (pos[0] - sep, pos[1] + sep)

					if field == "Stock":
						pos = (self.mat[player]["field"][field][0] + self.mat[player]["mat"].x - sep, self.mat[player]["field"][field][3] + self.mat[player]["mat"].y + sep)
				elif player == "2":
					pos = (self.mat[player]["mat"].x + self.mat[player]["mat"].size[0] - self.sd["card"][0] - self.mat[player]["field"][field][0], self.mat[player]["mat"].y + self.mat[player]["mat"].size[1] - self.sd["card"][1] - self.mat[player]["field"][field][1])
					if field == "Level":
						pos = (self.mat[player]["mat"].x + self.mat[player]["mat"].size[0] - self.sd["card"][1] - self.mat[player]["field"][field][0] + sep, self.mat[player]["mat"].y + self.mat[player]["mat"].size[1] - self.mat[player]["field"][field][1] - self.field_btn[f"{field}{player}"].size[1] - sep)
					elif field == "Stock":
						pos = (self.mat[player]["mat"].x + self.mat[player]["mat"].size[0] - self.sd["card"][1] - self.mat[player]["field"][field][0] + sep, self.mat[player]["mat"].y + self.mat[player]["mat"].size[1] - self.mat[player]["field"][field][1] - self.sd["card"][0] - sep)

					elif field == "Climax" or field == "Memory":
						pos = (self.mat[player]["mat"].x + self.mat[player]["mat"].size[0] - self.sd["card"][1] - self.mat[player]["field"][field][0] + sep, self.mat[player]["mat"].y + self.mat[player]["mat"].size[1] - self.sd["card"][0] - self.mat[player]["field"][field][1] - sep)
					elif field == "Clock":
						pos = (self.mat[player]["mat"].x + self.mat[player]["mat"].size[0] - self.mat[player]["field"][field][0] - self.field_btn[f"{field}{player}"].size[0], self.mat[player]["mat"].y + self.mat[player]["mat"].size[1] - self.sd["card"][1] - self.mat[player]["field"][field][1])
					elif field == "Res":
						pos = (self.mat[player]["mat"].x + self.mat[player]["mat"].size[0] - self.mat[player]["field"][field][0] - self.field_btn[f"{field}{player}"].size[0], self.mat[player]["mat"].y)

				self.field_btn[f"{field}{player}"].pos = pos


	def move_field_btn(self, p="", y=False):
		for fields in self.gd["select_btns"]:
			if "Clock" in fields:
				for ind in self.pd[fields[-1]]["Clock"]:
					self.cd[ind].selectable(False)
			elif not y and ("Stage" in self.gd["status"] or self.gd["move"]) and fields[:-1] in self.gd["stage"]:
				self.field_btn[f"{fields}s"].x = -Window.width * 5
			elif y and ("Stage" in self.gd["pay_status"] or self.gd["move"]) and fields[:-1] in self.gd["stage"]:
				self.field_btn[f"{fields}s"].x = -Window.width * 5
			else:
				if "Climax" in fields:
					self.cd[self.pd[fields[-1]][fields[:-1]][0]].selectable(False)
				else:
					self.cd[self.pd[fields[-1]][fields[:-2]][int(fields[-2])]].selectable(False)

		self.gd["select_btns"] = []
		self.gd["mstock"][0] = ""

		if (p == "Main" and self.gd["active"] == "1") or p == "restart" or (p == "Main" and self.gd["active"] == "2" and "oppturn" in self.gd["effect"]):
			for field in self.gd["stage"]:
				self.field_btn[f"{field}1"].x = -Window.width * 5
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
		if self.gd["com"] and self.gd["active"] == "2":
			play = self.ai.main_play(self.pd, self.cd, self.gd)
			if play != "pass":
				self.gd["opp_play"] = list(play)

		if len(self.gd["opp_play"]) > 0:
			play = ""
			for x in range(len(self.gd["opp_play"])):
				play = self.gd["opp_play"].pop(0)
				if play[0] in self.pd[self.gd["active"]]["Hand"]:
					break
				else:
					play = ""
			if play:
				if len(play) > 3:
					self.gd["ability_trigger"] = f"Event_{play[0]}"
					self.pay_mstock(s="es")
				else:
					self.play(play)
			else:
				self.opp_play_done()
		else:
			self.opp_play_done()

	def opp_play_done(self):
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

			self.cd[move[0]].setPos(field=self.mat[move[0][-1]]["field"][f"{move[1]}{move[2]}"], t=f"{move[1]}{move[2]}")
			self.pd[move[0][-1]][move[1]][move[2]] = move[0]
			self.check_cont_ability()
			self.update_marker(move[0][-1])
			if self.net["game"] and self.gd["active"] == "2":
				if self.gd["show_wait_popup"]:
					Clock.schedule_once(partial(self.popup_text, "waiting"), move_dt_btw)
				self.mconnect("phase")
			else:
				Clock.schedule_once(self.opp_move, move_dt_btw)
		else:
			self.gd["opp_move"] = []
			Clock.schedule_once(self.end_current_phase)

	def beginning_phase(self, *args):
		self.dismiss_all()
		self.change_label()
		self.clear_ability()
		if self.gd["pp"] < 0:
			Clock.schedule_once(self.check_auto_ability)
			return False
		else:
			if "Stand" in self.gd["phase"]:
				Clock.schedule_once(self.stand_phase)
			elif "Draw" in self.gd["phase"]:
				Clock.schedule_once(self.draw_phase)
			elif "Clock" in self.gd["phase"]:
				Clock.schedule_once(self.clock_phase)
			elif "Main" in self.gd["phase"]:
				Clock.schedule_once(self.main_phase)
			elif "Climax" in self.gd["phase"]:
				if "Climax" in self.gd["skip"]:
					self.climax_phase_done()
				else:
					Clock.schedule_once(self.climax_phase)
			elif "Attack" in self.gd["phase"]:
				Clock.schedule_once(self.attack_phase)
			elif "Declaration" in self.gd["phase"]:
				Clock.schedule_once(self.attack_declaration_done)
			elif "Trigger" in self.gd["phase"]:
				Clock.schedule_once(self.trigger_step)
			elif "Counter" in self.gd["phase"]:
				Clock.schedule_once(self.counter_step)
			elif "Damage" in self.gd["phase"]:
				Clock.schedule_once(self.damage_step)
			elif "Battle" in self.gd["phase"]:
				Clock.schedule_once(self.battle_step)
			elif "Encore" in self.gd["phase"]:
				Clock.schedule_once(self.encore_phase)
			elif "End" in self.gd["phase"]:
				Clock.schedule_once(self.end_phase)

	def main_phase(self, *args):
		self.sd["btn"]["end"].text = "Climax Phase"
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
			Clock.schedule_once(self.opp_play, move_dt_btw)
		else:
			self.sd["btn"]["end"].x = Window.width - self.sd["btn"]["end"].size[0]
			self.sd["btn"]["end"].y = 0
			self.sd["btn"]["end"].disabled = False

			self.sd["btn"]["end_attack"].x = Window.width - self.sd["btn"]["end"].size[0] - self.sd["btn"]["end_attack"].size[0]
			self.sd["btn"]["end_attack"].y = 0 
			self.sd["btn"]["end_attack"].disabled = False

			self.sd["btn"]["end_phase"].x = Window.width - self.sd["btn"]["end"].size[0] - self.sd["btn"]["end_attack"].size[0] - self.sd["btn"]["end_phase"].size[0]
			self.sd["btn"]["end_phase"].y = 0 
			self.sd["btn"]["end_phase"].disabled = False
			self.sd["btn"]["ablt_info"].y = -Window.height
			self.sd["btn"]["draw_upto"].y = -Window.height

			self.update_movable(self.gd["active"])


	def update_movable(self, player):
		if not self.gd["cont_on"]:
			self.sd["menu"]["btn"].disabled = False
			self.gd["movable"] = []
			self.gd["ability_doing"] = []
			for field in self.gd["fields"]:
				for _ in self.pd[player][field]:
					if _ in self.emptycards:
						continue
					aa = True
					for item in self.cd[_].text_c:
						if item[0].startswith(cont_ability) and item[1] != 0 and item[1] > -9:
							eff = ab.cont(item[0])
							if "no_move" in eff and self.cd[_].pos_new != "Hand":
								aa = False
								break
					if aa:
						self.gd["movable"].append(_)
			if not self.gd["play"]:
				self.act_ability_show()

	def update_playable_climax(self, player):
		self.gd["movable"] = []
		self.gd["playable_climax"] = []
		for ind in self.pd[self.gd["active"]]["Hand"]:
			self.gd["movable"].append(ind)
			if self.cd[ind].card == "Climax":
				if self.gd["any_Clrclimax"][self.gd["active"]] or self.cd[ind].mcolour.lower() in self.pd[self.gd["active"]]["colour"]:
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
		elif self.gd["ability_doing"] in ("give", "power", "trait", "soul", "hander", "waitinger", "clocker", "memorier"):
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
		self.sd["btn"]["end"].y = -Window.height
		self.sd["btn"]["end_attack"].y = -Window.height
		self.sd["btn"]["end_phase"].y = -Window.height
		self.act_ability_show(hide=True)
		if self.gd["astock_select"]:
			self.gd["astock_select"] = False
			for ind in self.gd["chosen"]:
				self.gd["target"].append(ind)
			if not self.gd["chosen"]:
				self.gd["target"].append("")
			self.gd["choose"] = True
			for fields in self.gd["select_btns"]:
				self.cd[self.pd[fields[-1]][fields[:-2]][int(fields[-2])]].selectable(False)
				self.cd[self.pd[fields[-1]][fields[:-2]][int(fields[-2])]].update_text()
			self.gd["payed_mstock"] = False
			Clock.schedule_once(self.pay_mstock)
		elif "Effect" in self.sd["btn"]["end"].text:  
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
					self.cd[self.gd["ability_trigger"].split("_")[1]].update_text()
					self.gd["move"] = "none"
				elif "stand" in self.gd["ability_doing"]:
					if "swap" in self.gd["effect"] and self.gd["effect"][0] == 2:
						self.gd["target"] = ["", ""]
				else:
					if self.gd["ability_doing"] in ("give", "power", "level", "trait", "soul") and len(self.gd["chosen"]) > 0:
						for ind in self.gd["chosen"]:
							self.cd[ind].update_text()
						self.gd["chosen"] = []
					self.gd["ability_effect"].remove(self.gd["ability_doing"])
			self.move_field_btn(self.gd["phase"])
			for ind in self.gd["chosen"]:
				if ind != "" and ind in self.cd:
					self.cd[ind].selectable(False)
					self.cd[ind].update_text()
			if "Reveal" in self.gd["effect"] and "if" in self.gd["effect"]:
				if len(self.pd[self.gd["ability_trigger"].split("_")[1][-1]]["Res"]) >= self.gd["effect"][self.gd["effect"].index("if") + 1]:
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
				self.sd["btn"]["end"].text = "Climax Phase"
			else:
				self.sd["btn"]["end"].text = f"End {self.gd['phase']}"
			self.sd["btn"]["end"].x = Window.width - self.sd["btn"]["end"].size[0]
			self.sd["btn"]["end_eff"].y = -Window.height * 2
			if self.net["game"] and not self.net["send"] and "drawupto" in self.gd["ability_doing"] and "plchoose" in self.gd["effect"]:
				self.net["var"] = list(self.net["act"][4])
				self.net["var1"] = "draw"
				if not self.poptext:
					Clock.schedule_once(partial(self.popup_text, "waitingser"))
				self.mconnect("plturn")
				return False
			else:
				self.ability_effect()
		elif self.gd["phase"] == "Clock":
			self.pd[self.gd["active"]]["done"]["Clock"] = True
			self.sd["btn"]["end"].disabled = True
			self.gd["phase"] = "Main"
			Clock.schedule_once(self.beginning_phase)
		elif self.gd["phase"] == "Main":
			self.pd[self.gd["active"]]["done"]["Main"] = True
			self.sd["btn"]["end_attack"].disabled = True
			self.sd["btn"]["end_phase"].disabled = True
			self.sd["btn"]["end"].disabled = True
			self.gd["phase"] = "Climax"
			Clock.schedule_once(self.climax_phase_beginning, move_dt_btw)
		elif self.gd["phase"] == "Climax":
			if self.net["game"] and self.gd["active"] == "1":
				self.net["var"] = ["x"]
				self.net["var1"] = "end current"
				self.mconnect("phase")
			else:
				self.pd[self.gd["active"]]["done"]["Climax"] = True
				self.sd["btn"]["end"].disabled = True
				self.gd["phase"] = "Attack"
				Clock.schedule_once(self.attack_phase_beginning, move_dt_btw)
		elif (self.gd["phase"] == "Attack" or self.gd["phase"] == "Declaration") and "AUTO" in self.gd["ability_trigger"]:
			self.pd[self.gd["active"]]["done"]["Attack"] = True
			self.sd["btn"]["end"].disabled = True
			self.sd["btn"]["end"].y = -Window.height
			Clock.schedule_once(self.beginning_phase, move_dt_btw)
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

	def skip_encore(self, p="1", *args):
		self.gd["nomay"] = True
		self.move_field_btn(self.gd["phase"])
		for cind in list(self.gd["encore"][p]):
			self.gd["no_cont_check"] = True
			self.cd[cind].selected_c(False)
			self.send_to_waiting(cind)
		if self.gd["encore"][p]:
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
			Clock.schedule_once(self.climax_phase_beginning)

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
			Clock.schedule_once(self.climax_phase_beginning)

	def create_field_label(self):
		for player in list(self.pd.keys()):
			for field in self.labelfield:
				self.field_label[f"{field}{player}"] = Label(text="50", halign="center", font_size=self.sd["card"][1] / 4, text_size=self.sd["card"], color=(1, 1, 1, 1), outline_width=2, size_hint=(None, None), pos_hint=(None, None), size=self.sd["card"], pos=(-Window.width * 2, 0))
				self.parent.add_widget(self.field_label[f"{field}{player}"])
				self.field_label[f"{field}{player}"].texture_update()
				self.field_label[f"{field}{player}"].size = self.field_label[f"{field}{player}"].texture.size
				if field == "Stock":
					if player == "1":
						self.field_label[f"{field}{player}"].halign = "right"
					else:
						self.field_label[f"{field}{player}"].halign = "left"

	def add_field_label(self, *args):
		for player in list(self.pd.keys()):
			for field in self.labelfield:
				self.field_label[f"{field}{player}"].center = self.field_btn[f"{field}{player}"].center
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

	def shuffle_stock(self, player, *args):
		if player == "0":
			for player in self.pd:
				self.gd["shufflest"].append(player)
		else:
			self.gd["shufflest"].append(player)

		for player in self.gd["shufflest"]:
			for _ in self.pd[player]["Stock"]:
				pos = self.mat[player]["field"]["Stock"]
				self.cd[_].setPos(pos[0], pos[1], t="Stock")

		_ = self.gd["ability_trigger"].split("_")[1][-1]
		if self.net["game"] and not self.net["send"] and _ == "1":
			self.net["var"] = list(self.net["act"])
			self.net["var1"] = "shufflest"
			if not self.poptext:
				Clock.schedule_once(partial(self.popup_text, "waitingser"))
			self.mconnect("act")
			return False

		Clock.schedule_once(self.shuffle_start_st, move_dt_btw)

	def shuffle_deck(self, player, *args):
		if player == "0":
			for player in list(self.pd.keys()):
				for n in range(shuffle_n * 1):
					shuffle(self.pd[player]["Library"])
				self.gd["shuffle"].append(player)
		else:
			for n in range(shuffle_n * 1):
				shuffle(self.pd[player]["Library"])
			self.gd["shuffle"].append(player)

		if self.net["game"] and self.gd["turn"] != 0:
			player = self.gd["ability_trigger"].split("_")
			if len(player) > 1:
				player = str(player[1][-1])
				if self.gd["auto_effect"] in self.gd["stack"][player]:
					self.gd["stack"][player].remove(self.gd["auto_effect"])
				if self.net["game"] and player == "1" and self.gd["ability_doing"] != "confirm" and not self.gd["oppchoose"]:
					self.net["var"] = list(self.net["act"])
					self.net["var1"] = "shuffle"
					self.gd["oppchoose"] = False
					self.mconnect("act")
					return False

		Clock.schedule_once(self.shuffle_start, move_dt_btw)

	def shuffle_start(self, dt=0):
		Clock.schedule_once(self.shuffle_animation, shuffle_dt * shuffle_n)

	def shuffle_start_st(self, dt=0):
		Clock.schedule_once(self.shuffle_animation_st, shuffle_dt * shuffle_n)


	def shuffle_animation(self, dt=0):
		if self.gd["shuffle_rep"] > 0:
			for player in self.gd["shuffle"]:
				if self.gd["turn"] > 0:
					self.check_auto_ability(refr=player, stacks=False)
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
			Clock.schedule_once(self.shuffle_animation, shuffle_dt * shuffle_n)
		else:

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
					Clock.schedule_once(self.refresh, move_dt_btw)
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

	def shuffle_animation_st(self, dt=0):
		if self.gd["shuffle_rep"] > 0:
			for player in self.gd["shufflest"]:
				library = self.mat[player]["field"]["Stock"][:2]
				card = self.pd[player]["Stock"]

				if len(library) > 0:
					def front(*args):
						f = self.cd[self.pd[player]["Stock"][0]]

						self.mat[player]["mat"].remove_widget(f)
						self.mat[player]["mat"].add_widget(f)

					def top(*args):
						t = self.cd[self.pd[player]["Stock"][-1]]
						self.mat[player]["mat"].remove_widget(t)
						self.mat[player]["mat"].add_widget(t)

					a1 = Animation(x=library[0], y=library[1] - self.sd["card"][1], d=shuffle_dt)
					a2 = Animation(x=library[0], y=library[1], d=shuffle_dt)
					a1.bind(on_complete=front)
					a2.bind(on_complete=top)

					animation = a1 + a2
					animation.start(self.cd[card[0]])

			self.gd["shuffle_rep"] -= 1
			Clock.schedule_once(self.shuffle_animation_st, shuffle_dt * shuffle_n)
		else:
			if len(self.gd["shufflest"]) > 0 and self.net["game"]:
				self.net["var1"] = "shufflest"
				if "1" in self.gd["shufflest"]:
					for n in range(shuffle_n * 1):
						shuffle(self.pd["1"]["Stock"])
					self.gd["shufflest"].remove("1")
					self.stock_size("1")
					self.mconnect("shuffleplr")
				elif "2" in self.gd["shufflest"]:
					self.gd["shufflest"].remove("2")
					if self.gd["show_wait_popup"]:
						Clock.schedule_once(partial(self.popup_text, "waiting"))
					self.stock_size("2")
					self.mconnect("shuffleopp")
			else:
				self.gd["shuffle_rep"] = shuffle_n
				self.net["var1"] = ""
				if not self.net["game"]:
					for player in self.gd["shufflest"]:
						for n in range(shuffle_n * 1):
							shuffle(self.pd[player]["Stock"])
						self.stock_size(player)
					self.gd["shufflest"] = []

				if self.gd["shufflest_trigger"] == "ability":
					self.gd["shufflest_trigger"] = ""
					Clock.schedule_once(self.ability_effect)

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
		else:
			if self.gd["phase"] == "Janken":
				self.gd["draw_both"] = [starting_hand, False, False]
				self.gd["phase"] = "Mulligan"
				Clock.schedule_once(self.mulligan_start)  

	def mulligan_start(self, *args):
		if self.gd["rev"]:
			player = self.gd["opp"]
		else:
			player = self.gd["active"]

		self.pd[player]["phase"]["Mulligan"] = True
		self.hand_btn_show(False)

		if self.net["game"] and player == "2":
			self.gd["rev"] = True
			Clock.schedule_once(self.mulligan_start)
		elif self.gd["com"] and player == "2":
			self.gd["chosen"] = self.ai.mulligan(self.pd, self.cd)
			self.gd["p_owner"] = player
			self.mulligan_done()
		else:
			self.cardinfo.dismiss()
			self.sd["popup"]["popup"].title = self.gd["phase"]
			self.gd["uptomay"] = True
			self.gd["confirm_var"] = {"o": player, "c": "Mulligan", "m": starting_hand}
			self.popup_start()

	def hand_waiting(self, dt=0, chosen=[]):
		for ind in chosen:
			if ind in self.emptycards:
				continue
			if "xdiscard" in self.gd["effect"]:
				self.gd["xdiscard"].append(ind)
			self.check_pos(ind)
			self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Waiting"], t="Waiting")
			self.pd[ind[-1]]["Waiting"].append(ind)
			self.update_field_label()
			if "Hand" in self.cd[ind].pos_new:
				if "Mulligan" not in self.gd["phase"]:
					self.check_auto_ability(dis=ind, stacks=False)

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
		rr = False
		temp = []
		if "rescue" in self.gd["effect"]:
			temp = self.gd["effect"][self.gd["effect"].index("rescue") + 1]
			if "Waiting" in self.cd[temp[0]].pos_new:
				rr = True
		elif "return" in self.gd["effect"]:
			temp = self.gd["effect"][self.gd["effect"].index("return") + 1]
			if any(pos in self.cd[temp[0]].pos_new for pos in ("Center", "Back")):
				rr = True

		if rr and "Hand" in temp:
			self.send_to("Hand", temp[0])

		if "rescue" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("rescue")

		if "do" in self.gd["effect"] and self.gd["do"][0] > 0:
			self.gd["done"] = True

		if "do" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("do")

		self.ability_effect()

	def stocker(self, *args):
		ind = self.gd["ability_trigger"].split("_")[-1]

		if self.gd["effect"][0] == 0:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(ind)
			self.gd["effect"][0] = 1
		elif self.gd["effect"][0] == -1:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				for ta in self.cont_times(self.gd["effect"], self.cont_cards(self.gd["effect"], ind), self.cd):
					self.gd["target"].append(ta)
			self.gd["effect"][0] = len(self.gd["target"])
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
					fop = [o for o in self.pd[op]["Center"] if self.cd[o].level_t <= int(lvl[-1])]
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
			if "bottom" in self.gd["effect"] and "replace" not in self.gd["effect"]:
				self.send_to("Stock", temp, pos=0)
			else:
				self.send_to("Stock", temp)
			if "replace" in self.gd["effect"]:
				if "bottom" in self.gd["effect"]:
					temp1 = self.pd[temp[-1]]["Stock"].pop(0)
					self.mat[temp1[-1]]["mat"].remove_widget(self.cd[temp1])
					self.mat[temp1[-1]]["mat"].add_widget(self.cd[temp1])
					self.pd[temp1[-1]]["Waiting"].append(temp1)
					self.cd[temp1].setPos(field=self.mat[temp1[-1]]["field"]["Waiting"], t="Waiting")
					self.stock_size(temp1[-1])
		if self.gd["notarget"]:
			self.gd["notarget"] = False

		if "choice" in self.gd["effect"] and "salvage" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("salvage")
		elif "stocker" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("stocker")

		if "if" in self.gd["effect"]:
			if len(lif) >= self.gd["effect"][self.gd["effect"].index("if") + 1]:
				self.gd["done"] = True
		elif "do" in self.gd["effect"] and self.gd["do"][0] > 0:
			self.gd["done"] = True

		if "do" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("do")

		if self.gd["pay"] and not self.gd["payed"]:
			self.pay_condition()
		else:
			self.ability_effect()

	def clocker(self, *args):
		ind = self.gd["ability_trigger"].split("_")[1]
		if not self.gd["clocker"]:
			self.gd["clocker"] = True
			if self.gd["effect"][0] == 0:  
				if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
					self.gd["target"].append(ind)
				self.gd["effect"][0] = 1
			elif self.gd["effect"][0] == -3:
				self.gd["effect"][0] = 1
				if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
					self.gd["target"].append(self.gd["effect"][self.gd["effect"].index("target") + 1])
				elif self.net["game"] and ind[-1] == "2":
					self.fix_opp_net(ind, self.gd["effect"][0])

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
					self.send_to("Clock", temp)

				if not self.gd["both"] and self.check_lose():
					return False

				if self.gd["both"]:
					self.gd["both"] = False

				if player and len(self.pd[player]["Clock"]) >= 7:
					self.popup_clr()
					self.gd["level_up_trigger"] = "clocker"
					Clock.schedule_once(partial(self.level_up, player), move_dt_btw)
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
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(ind)
			self.gd["effect"][0] = 1
		elif self.gd["effect"][0] == -1:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				self.gd["target"].append("all")
			self.gd["effect"][0] = 1
		elif self.gd["effect"][0] == -3:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(self.gd["effect"][self.gd["effect"].index("target") + 1])
			self.gd["effect"][0] = 1
			ss = False
		elif self.gd["effect"][0] == -9:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(self.pd[ind[-1]]["Library"][-1])
			self.gd["effect"][0] = 1
		elif self.gd["effect"][0] == -20:
			self.gd["effect"][0] = len(self.gd["extra1"])
			for r in range(len(self.gd["extra1"])):
				ex = self.gd["extra1"].pop(0)
				if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
					self.gd["target"].append(ex)

		deck = ""
		for r in range(self.gd["effect"][0]):
			if "bottom" in self.gd["effect"]:
				temp = self.gd["target"].pop(-1)
			else:
				temp = self.gd["target"].pop(0)
			if self.net["game"] and ind[-1] == "1" and ss:
				self.net["act"][4].append(temp)
			if temp == "":
				self.gd["notarget"] = True
				continue
			if "extra" in self.gd["effect"]:
				self.gd["extra"].append(temp)
			if "save_name" in self.gd["effect"]:
				self.gd["save_name"] = [self.cd[temp].name, temp]
			if temp == "all":
				self.send_to_deck(allc=True)
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
			if self.net["game"]:
				self.gd["shuffle_send"] = True
			self.shuffle_deck(player)
		else:
			self.ability_effect()

	def fix_opp_net(self, ind, r):
		if ("Opp" in self.gd["effect"] or "opp" in self.gd["effect"]) and ind[-1] == "1":
			p = "2"
		elif ("Opp" in self.gd["effect"] or "opp" in self.gd["effect"]) and ind[-1] == "2":
			p = "1"
		else:
			p = ind[-1]

		for rr in range(r):
			try:
				int(self.gd["target"][rr])
				if self.gd["target"][rr][-1] == ind[-1]:
					self.gd["target"][rr] = f"{self.gd['target'][rr][:-1]}{p}"
			except ValueError:
				continue

	def waitinger(self, *args):
		ind = self.gd["ability_trigger"].split("_")[1]

		if self.gd["com"] and (ind[-1] == "2" or "oppturn" in self.gd["effect"]):
			pick = self.ai.ability(self.pd, self.cd, self.gd)
			if "AI_waitinger" in pick:
				inx = pick.index("AI_waitinger")
				self.gd["target"] = list(pick[inx + 1])
			else:
				self.gd["target"] = [""]

		if self.gd["effect"][0] == 0:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(ind)
			self.gd["effect"][0] = 1
		elif self.gd["effect"][0] == -1:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				if "all" in self.gd["effect"] and "both" in self.gd["effect"]:
					stage = self.pd["1"]["Center"] + self.pd["1"]["Back"] + self.pd["2"]["Center"] + self.pd["2"]["Back"]
					if "Other" in self.gd["effect"] and ind in stage:
						stage.remove(ind)
					for rr in stage:
						self.gd["target"].append(rr)
				else:
					self.gd["status"] = self.add_to_status("", self.gd["effect"])
					for rr in self.select_card(card_filter=True):
						self.gd["target"].append(rr)
					self.gd["status"] = ""
			self.gd["effect"][0] = len(self.gd["target"])
		elif self.gd["effect"][0] == -3:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(self.gd["effect"][self.gd["effect"].index("target") + 1])
			self.gd["effect"][0] = 1

		if self.net["game"]:
			self.fix_opp_net(ind, self.gd["effect"][0])

		wait = []
		show = []
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
			if "aselected" in self.gd["effect"]:
				if "xchoose" in self.gd["effect"]:
					self.cd[ind].aselected = str(temp)
					if "show" in self.gd["effect"]:
						show.append(temp)
				else:
					if "atarget" in self.gd["effect"]:
						_ = self.gd["effect"][self.gd["effect"].index("atarget") + 1]
					else:
						_ = self.cd[ind].aselected

					if _ != "" and _ in self.pd[ind[-1]]["Center"] + self.pd[ind[-1]]["Back"]:
						self.send_to_waiting(_)
						self.cd[ind].aselected = ""
			else:
				self.send_to_waiting(temp)

		if self.gd["notarget"]:
			self.gd["notarget"] = False

		if "waitinger" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("waitinger")
			self.gd["choose"] = False

		if "do" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("do")

		if "if" in self.gd["effect"]:
			self.gd["waiting_cost"][2] = 0
			if "iflower" not in self.gd["effect"] and len(wait) >= self.gd["effect"][self.gd["effect"].index("if") + 1]:
				self.gd["done"] = True
				if self.gd["waiting_cost"][1]:
					self.gd["waiting_cost"][2] = 1
			if "iflower" in self.gd["effect"] and len(wait) <= self.gd["effect"][self.gd["effect"].index("if") + 1]:
				self.gd["done"] = True
		elif "do" in self.gd["effect"] and self.gd["do"][0] > 0:
			self.gd["done"] = True

		if self.gd["waiting_cost"][1] and self.gd["waiting_cost"][2]:
			self.gd['ability_effect'] = []
			ind, st = self.gd["waiting_cost"][1].split("_")
			self.play([ind, st[:-1], st[-1]])
		elif self.gd["pay"] and not self.gd["payed"]:
			self.pay_condition()
		elif "show" in self.gd["effect"] and len(show) > 0 and ind[-1] == "2":
			self.popup_multi_info(cards=show, owner=ind[-1], t="OChoose")
		else:
			self.ability_effect()

	def memorier(self, *args):
		ind = self.gd["ability_trigger"].split("_")[1]

		if self.gd["com"] and (ind[-1] == "2" or "oppturn" in self.gd["effect"]):
			pick = self.ai.ability(self.pd, self.cd, self.gd)
			if "AI_memorier" in pick:
				inx = pick.index("AI_memorier")
				self.gd["target"] = list(pick[inx + 1])
			else:
				self.gd["target"] = [""]

		if ("Opp" in self.gd["effect"] or "opp" in self.gd["effect"]) and ind[-1] == "1":
			pl = "2"
		elif ("Opp" in self.gd["effect"] or "opp" in self.gd["effect"]) and ind[-1] == "2":
			pl = "1"
		else:
			pl = ind[-1]

		if self.gd["effect"][0] == 0:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(ind)
			self.gd["effect"][0] = 1
		elif self.gd["effect"][0] == -1:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				for rr in self.cont_cards(self.gd["effect"], ind):
					self.gd["target"].append(rr)
			self.gd["effect"][0] = len(self.gd["target"])
		elif self.gd["effect"][0] == -3:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(self.gd["effect"][self.gd["effect"].index("target") + 1])
			self.gd["effect"][0] = 1

		if "this" in self.gd["effect"] and self.gd["effect"][0] > 0:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(ind)
			self.gd["effect"][0] += 1

		if self.net["game"] and pl != ind[-1]:
			for rr in range(len(self.gd["target"])):
				if self.gd["target"][rr] != "" and self.gd["target"][rr][-1] == ind[-1]:
					self.gd["target"][rr] = f"{self.gd['target'][rr][:-1]}{pl}"
			if not self.gd["target"]:
				self.gd["target"].append("")

		lif = []
		for r in range(self.gd["effect"][0]):
			temp = self.gd["target"].pop(0)
			if self.net["game"] and ind[-1] == "1":
				self.net["act"][4].append(temp)
			if temp != "":
				for item in self.cd[temp].text_c:
					if item[0].startswith(cont_ability) and item[1] != 0 and item[1] > -9:
						eff = ab.cont(item[0])
						if "no_memory" in eff:
							temp = ""
							break
			if temp == "":
				self.gd["notarget"] = True
				continue
			if "if" in self.gd["effect"]:
				lif.append(ind)
			if "extra" in self.gd["effect"]:
				self.gd["extra"].append(temp)
			self.send_to("Memory", temp)

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

		if self.gd["com"] and (ind[-1] == "2" or "oppturn" in self.gd["effect"]):
			pick = self.ai.ability(self.pd, self.cd, self.gd)
			if "AI_hander" in pick:
				inx = pick.index("AI_hander")
				self.gd["target"] = list(pick[inx + 1])
			else:
				self.gd["target"] = [""]

		if self.gd["effect"][0] == 0:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(ind)
			self.gd["effect"][0] = 1
		elif self.gd["effect"][0] == -1:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				self.gd["status"] = self.add_to_status("", self.gd["effect"])
				for rr in self.select_card(card_filter=True):
					self.gd["target"].append(rr)
				self.gd["status"] = ""
			self.gd["effect"][0] = len(self.gd["target"])

		if "this" in self.gd["effect"] and self.gd["effect"][0] > 0 and "thisupto" not in self.gd["effect"]:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(ind)
			self.gd["effect"][0] += 1

		if len(self.gd["target"]) < self.gd["effect"][0]:
			for r in range(self.gd["effect"][0] - len(self.gd["target"])):
				self.gd["target"].append("")

		if self.net["game"] and "Opp" in self.gd["effect"] and "opp" not in self.gd["effect"]:
			for tr in range(len(self.gd["target"])):
				if self.gd["target"][tr] == "":
					continue
				if self.gd["ability_trigger"].split("_")[1][-1] == "1" and self.gd["target"][tr][-1] != "2":
					self.gd["target"][tr] = f"{self.gd['target'][tr][:-1]}2"
				elif self.gd["ability_trigger"].split("_")[1][-1] == "2" and self.gd["target"][tr][-1] != "1":
					self.gd["target"][tr] = f"{self.gd['target'][tr][:-1]}1"

		retr = []
		for r in range(self.gd["effect"][0]):
			temp = self.gd["target"].pop(0)
			if self.net["game"] and (ind[-1] == "1" or (ind[-1] == "2" and "oppturn" in self.gd["effect"])):
				self.net["act"][4].append(temp)
			if temp != "":
				for item in self.cd[temp].text_c:
					if item[0].startswith(cont_ability) and item[1] != 0 and item[1] > -9:
						eff = ab.cont(item[0])
						if "no_hand" in eff:
							temp = ""
							break
			if temp == "":
				self.gd["notarget"] = True
				continue
			self.send_to("Hand", temp)
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

		if self.net["game"] and ("oppturn" in self.gd["effect"] and not self.net["send"]):
			self.net["var"] = list(self.net["act"][4])
			self.net["var1"] = "oppchoose"
			if not self.poptext:
				Clock.schedule_once(partial(self.popup_text, "waitingser"))
			self.mconnect("oppchoose")
		else:
			self.ability_effect()

	def play_to_stage(self, ind, st, *args):
		card = self.cd[ind]
		old = str(self.cd[ind].pos_new)
		if ind not in self.gd["standby"] and card.card != "Climax" and "Hand" in old:
			if ind in self.check_waiting_cost and ("Play" in self.gd["ability_trigger"] or len([s for s in self.pd[ind[-1]]["Center"] + self.pd[ind[-1]]["Back"] if s != "" and self.gd["waiting_cost"][0][card.cid][1] in self.cd[s].name_t]) > 0):
				if not self.gd["waiting_cost"][1]:
					self.gd["waiting_cost"][1] = f"{ind}_{st}"
					self.gd["waiting_cost"][2] = 0
					self.pd[ind[-1]]["Hand"].remove(ind)
					self.pd[ind[-1]]["Res"].append(ind)
					self.gd["selected"] = ""
					self.gd["ability"] = self.gd["waiting_cost"][0][self.cd[ind].cid][2]
					self.gd["stack"][ind[-1]].append([ind, ab.play(a=self.gd["ability"], p=True), self.gd["ability"], "Play", 0, self.gd["phase"], self.gd["pp"]])

					if self.net["game"] and ind[-1] == "1":
						self.net["send"] = True
					self.gd["ability_trigger"] = f"Play_{ind}"

					Clock.schedule_once(self.stack_ability)
					return False
				else:
					if ind in self.pd[ind[-1]]["Res"]:
						self.pd[ind[-1]]["Res"].remove(ind)
						self.pd[ind[-1]]["Hand"].append(ind)
					if "pay" in self.gd["ability_effect"]:
						self.gd["ability_effect"].remove("pay")
					if "do" in self.gd["ability_effect"]:
						self.gd["ability_effect"].remove("do")
					if self.gd["waiting_cost"][2]:
						if self.gd["waiting_cost"][2] > 1:
							if len(self.pd[self.gd["active"]]["Stock"]) >= card.cost_t:
								self.pay_stock(card.cost_t, card.owner)
							else:
								if self.gd["waiting_cost"][1]:
									self.gd["waiting_cost"][1] = ""
								self.hand_size(self.gd["active"])
								return False
						else:
							self.pay_stock(self.gd["waiting_cost"][0][self.cd[ind].cid][0], card.owner)
						self.gd["stock_payed"] = True
					else:
						self.hand_size(self.gd["active"])
						Clock.schedule_once(self.stack_ability)
						return False
			elif card.card == "Event" and "estock" in self.gd["markerstock"] and len(self.gd["estock"][card.ind[-1]]) > 0:
				if not self.gd["estock_pop"]:
					self.gd["estock_payed"] = []
					self.gd["estock_pop"] = f"{ind}_{st}"
					self.pd[ind[-1]]["Hand"].remove(ind)
					self.pd[ind[-1]]["Res"].append(ind)
					self.gd["selected"] = ""
					self.gd["ability_trigger"] = f"Event_{card.ind}"
					self.gd["confirm_trigger"] = f"estock_{card.ind}"
					self.gd["confirm_var"] = {"c": "estock"}
					Clock.schedule_once(self.confirm_popup, popup_dt)
				else:
					if ind in self.pd[ind[-1]]["Res"]:
						self.pd[ind[-1]]["Res"].remove(ind)
						self.pd[ind[-1]]["Hand"].append(ind)
					if len(self.gd["estock_pop"].split("_"))>2:
						if self.gd["estock_pop"][-1]=="2":
							self.gd["estock_payed"] = []
							if len(self.pd[self.gd["active"]]["Stock"]) >= card.cost_t:
								self.pay_stock(card.cost_t, card.owner)
							else:
								if self.gd["estock_pop"]:
									self.gd["estock_pop"] = ""
								self.hand_size(self.gd["active"])
								return False
						else:
							self.pay_stock(card.cost_t-len(self.gd["estock_payed"]), card.owner)
						self.gd["stock_payed"] = True
					else:
						self.hand_size(self.gd["active"])
						return False
			elif len(self.pd[self.gd["active"]]["Stock"]) >= card.cost_t:
				self.pay_stock(card.cost_t, card.owner)
				self.gd["stock_payed"] = True
		self.gd["payed"] = True
		self.check_pos(ind)

		if self.gd["waiting_cost"][1]:
			self.gd["waiting_cost"][1] = ""
		if self.gd["waiting_cost"][2]:
			self.gd["waiting_cost"][2] = 0
		if self.gd["estock_pop"]:
			self.gd["estock_pop"] = ""

		if "Center" in st or "Back" in st:
			if self.pd[ind[-1]][st[:-1]][int(st[-1])] != "":
				temp = self.pd[ind[-1]][st[:-1]][int(st[-1])]
				self.send_to_waiting(temp)

			self.cd[ind].setPos(field=self.mat[ind[-1]]["field"][st], t=st)
			self.pd[ind[-1]][st[:-1]][int(st[-1])] = ind
			self.cd[ind].turn = [int(self.gd["turn"]), self.cd[ind].pos_old, str(self.gd["standby"][1])]
		elif "Res" in st:
			res = self.mat[ind[-1]]["field"][st]
			self.cd[ind].setPos(field=((res[2] - res[0]) / 2 + res[0], (res[3] - res[1]) / 2 + res[1]), t="Res")
			self.pd[ind[-1]]["Res"].append(ind)

		self.update_field_label()
		self.check_cont_ability(act=False)
		if self.gd["pp"] >= 0 or ("Hand" in old or "Memory" in old or "Waiting" in old):
			self.check_auto_ability(play=ind, stacks=False)

	def check_pos(self, ind, wig=True):
		if wig:
			self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
			self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])
		if self.cd[ind].pos_new == "Res":
			if ind in self.pd[ind[-1]]["Res"]:
				self.pd[ind[-1]]["Res"].remove(ind)
		elif ind in self.pd[ind[-1]]["Climax"]:
			self.pd[ind[-1]]["Climax"].remove(ind)
		elif ind in self.pd[ind[-1]]["Memory"]:
			self.pd[ind[-1]]["Memory"].remove(ind)
		elif self.cd[ind].pos_new == "Waiting":
			if ind in self.pd[ind[-1]]["Waiting"]:
				self.pd[ind[-1]]["Waiting"].remove(ind)
		elif ind in self.pd[ind[-1]]["Level"]:
			self.pd[ind[-1]]["Level"].remove(ind)
			self.level_size(ind[-1])
		elif self.cd[ind].pos_new == "Library":
			if ind in self.pd[ind[-1]]["Library"]:
				self.pd[ind[-1]]["Library"].remove(ind)
		elif ind in self.pd[ind[-1]]["Clock"]:
			self.pd[ind[-1]]["Clock"].remove(ind)
			self.clock_size(ind[-1])
		elif ind in self.pd[ind[-1]]["Hand"]:
			self.pd[ind[-1]]["Hand"].remove(ind)
			self.hand_size(ind[-1])
		else:
			if "Marker" in self.cd[ind].pos_new:
				if self.gd["ksalvage"] and "Stage" in self.gd["effect"]:
					self.remove_marker(ind=self.gd["ksalvage"], wif=True,stg=True)
				elif self.gd["ksalvage"]:
					self.remove_marker(ind=self.gd["ksalvage"], m=ind)
			else:
				self.pd[ind[-1]][self.cd[ind].pos_new[:-1]][int(self.cd[ind].pos_new[-1])] = ""
				self.remove_marker(ind)
		self.update_field_label()

	def send_to(self, field, ind, pos=None, wig=True, update_field=True, face_down=False):
		if "Waiting" in field:
			self.send_to_waiting(ind)
		else:
			self.check_pos(ind, wig=wig)
			if "Hand" in field:
				if pos is not None:
					self.pd[ind[-1]]["Hand"].insert(pos, ind)
				else:
					self.pd[ind[-1]]["Hand"].append(ind)
				self.hand_size(ind[-1])
			elif "Library" in field:
				if pos is not None:
					self.pd[ind[-1]]["Library"].insert(pos, ind)
				else:
					self.pd[ind[-1]]["Library"].append(ind)
				self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Library"], t="Library")
				self.stack(ind[-1])
			elif "Stock" in field:
				if pos is not None:
					self.pd[ind[-1]]["Stock"].insert(pos, ind)
				else:
					self.pd[ind[-1]]["Stock"].append(ind)
				self.stock_size(ind[-1])
			elif "Clock" in field:
				if pos is not None:
					self.pd[ind[-1]]["Clock"].insert(pos, ind)
				else:
					self.pd[ind[-1]]["Clock"].append(ind)
				self.clock_size(ind[-1])
			elif "Memory" in field:
				self.pd[ind[-1]]["Memory"].append(ind)
				self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Memory"], t="Memory")
				if face_down:
					idm = self.gd["ability_trigger"].split("_")[1]
					if ind[-1] != idm[-1]:
						self.cd[ind].show_back(False)
					else:
						self.cd[ind].show_back()
			elif "Climax" in field and self.cd[ind].card == "Climax":
				self.pd[ind[-1]]["Climax"].append(ind)
				self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Climax"], t="Climax")
			elif "Level" in field:
				if pos is not None and "up" not in pos:
					self.pd[ind[-1]]["Level"].insert(pos, ind)
				else:
					self.pd[ind[-1]]["Level"].append(ind)
				self.level_size(ind[-1])
				if pos == "lvlup":
					self.check_auto_ability(lvup=ind[-1], stacks=False)
					self.gd["no_cont_check"] = True
				else:
					self.check_auto_ability(lvc=ind, stacks=False)

			if update_field:
				if field in self.labelfield:
					self.update_field_label()

			if self.gd["no_cont_check"]:
				self.gd["no_cont_check"] = False
			else:
				self.check_cont_ability()

			if "Clock" in field:
				if self.check_lose(ind[-1]):
					return False

	def send_to_deck(self, ind="", allc=False, pos="", *args):
		if allc:
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
			self.check_pos(ind)
			if pos == "bottom":
				self.pd[ind[-1]]["Library"].insert(0, ind)
				self.stack(ind[-1])
			else:
				self.pd[ind[-1]]["Library"].append(ind)

			self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Library"], t="Library")

			self.remove_marker(ind)
		self.update_field_label()
		self.check_cont_ability()

	def damage(self, *args):
		if self.gd["drev"]:
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
					self.send_to("Clock", temp)
					self.gd["damage_refresh"] -= 1
				else:
					card.setPos(library[0] - self.sd["padding"] / 4 - self.sd["card"][0], library[1] - self.sd["card"][1] / 3. * len(self.pd[player]["Res"]), t="Res")
					self.pd[player]["Res"].append(temp)

					if not self.gd["Res1_move"]:
						if self.field_btn[f"Res1{player}"].x < 0:
							self.field_btn[f"Res1{player}"].x += Window.width * 2
						self.gd["Res1_move"] = True

				self.update_field_label()

				if card.card == "Climax" and self.gd["damage"] > 0:
					self.gd["cancel_dmg"] = True
					self.gd["damage"] = 0
				else:
					self.gd["damage"] -= 1

			if self.gd["damageref"]:
				if not self.gd["both"] and self.gd["damage_refresh"] >= 0 >= len(self.pd[player]["Library"]) and len(self.pd[player]["Clock"]) >= 7:
					self.gd["reflev"] = ["ref", f"lev{player}"]
					if player == "1":
						self.gd["confirm_var"] = {"c": "reflev"}
						Clock.schedule_once(self.confirm_popup, popup_dt)
					elif self.net["game"] and player == "2":
						rule = self.gd["target"].pop(0)
						Clock.schedule_once(partial(self.reflev, rule))
					elif self.gd["com"] and player == "2":
						Clock.schedule_once(partial(self.reflev, choice(("ref", f"lev{player}"))))
					return False
				elif not self.gd["both"] and len(self.pd[player]["Clock"]) >= 7:
					self.gd["level_up_trigger"] = "damage"
					Clock.schedule_once(partial(self.level_up, player), move_dt_btw)
					return False
			elif not self.gd["both"] and len(self.pd[player]["Library"]) <= 0:
				if self.gd["reshuffle_trigger"]:
					self.gd["reshuffle_trigger_temp"] = str(self.gd["reshuffle_trigger"])
				self.gd["reshuffle_trigger"] = "damage"
				self.gd["rrev"] = player
				Clock.schedule_once(self.refresh, move_dt_btw)
				return False

			Clock.schedule_once(self.damage, move_dt_btw)
		else:
			for inx in range(len(self.pd[player]["Res"])):
				temp = self.pd[player]["Res"].pop(0)
				if "Event" in self.gd["ability_trigger"] and temp in self.gd["ability_trigger"]:
					self.pd[player]["Res"].append(temp)
					continue
				if self.gd["cancel_dmg"]:
					cc = False
					if "oncancelput" in self.gd["effect"]:
						if "ocLevel" in self.gd["effect"]:
							if "oclower" not in self.gd["effect"] and self.cd[temp].level_t >= self.gd["effect"][self.gd["effect"].index("ocLevel") + 1]:
								cc = True
							elif "oclower" in self.gd["effect"] and self.cd[temp].level_t <= self.gd["effect"][self.gd["effect"].index("ocLevel") + 1]:
								cc = True
					if cc:
						self.send_to("Clock", temp)
					else:
						self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Waiting"], t="Waiting")
						self.pd[player]["Waiting"].append(temp)
				else:
					self.send_to("Clock", temp)

			self.update_field_label()

			if self.gd["Res1_move"]:
				if self.field_btn[f"Res1{player}"].x > 0:
					self.field_btn[f"Res1{player}"].x -= Window.width * 2
				self.gd["Res1_move"] = False
			self.gd["level_up_trigger"] = ""

			self.check_cont_ability()

			self.check_auto_ability(atk=self.gd["attacking"][0], cnc=(player, self.gd["cancel_dmg"]), dmg=self.gd["dmg"], stacks=False)
			if self.gd["cancel_dmg"]:
				self.gd["cancel_dmg"] = False
			self.gd["dmg"] = 0

			if len(self.gd["reflev"]) > 0:
				Clock.schedule_once(partial(self.reflev, self.gd["reflev"][0]))
				return False

			if not self.gd["both"] and len(self.pd[player]["Clock"]) >= 7:
				self.gd["level_up_trigger"] = "damage"
				Clock.schedule_once(partial(self.level_up, player), move_dt_btw)
				return False

			self.gd["drev"] = False

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
				Clock.schedule_once(self.pay_condition, move_dt_btw)
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
			elif "reveal" in self.gd["reshuffle_trigger"]:
				self.gd["reshuffle_trigger"] = ""
				Clock.schedule_once(self.reveal_done, move_dt_btw)
			elif "marker" in self.gd["reshuffle_trigger"]:
				self.gd["reshuffle_trigger"] = ""
				Clock.schedule_once(self.marker, move_dt_btw)
			elif "encore" in self.gd["reshuffle_trigger"]:
				self.gd["reshuffle_trigger"] = ""
				Clock.schedule_once(self.encore_done, move_dt_btw)
			elif "damage" in self.gd["ability_effect"]:
				Clock.schedule_once(self.ability_effect, move_dt_btw)
			elif len(self.gd["attacking"]) >= 3:
				if "escanor" in self.gd["attacking"] and "xtimes" in self.gd["attacking"] and self.gd["attacking"][self.gd["attacking"].index("xtimes") + 1] > 0:
					self.gd["damage"] = self.gd["attacking"][self.gd["attacking"].index("escanor") + 1]
					self.gd["dmg"] = int(self.gd["damage"])
					self.gd["drev"] = True
					self.gd["attacking"][self.gd["attacking"].index("xtimes") + 1] -= 1
					Clock.schedule_once(self.damage, move_dt_btw)
				else:
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
			self.rect.pos = (-self.sd["card"][0] / 2, 0)  
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
		for card in self.pd[self.gd["active"]]["Center"] + self.pd[self.gd["active"]]["Back"]:
			if card != "":
				stand = True
				for item in self.cd[card].text_c:
					if item[0].startswith(cont_ability) and item[1] != 0 and item[1] > -9:
						eff = ab.cont(item[0])
						if "no_stand" in eff:
							if "OMore" in eff:
								if self.omore(eff, card):
									stand = False
							elif "Marker#" in eff:
								mm = 0
								if card in self.pd[card[-1]]["marker"]:
									mm = len(self.pd[card[-1]]["marker"][card])
								if "lower" not in eff and mm >= eff[eff.index("Marker#") + 1]:
									stand = False
								elif "lower" in eff and mm <= eff[eff.index("Marker#") + 1]:
									stand = False
							elif "sLevel" in eff:
								if ">p" in eff and self.cd[card].level_t > len(self.pd[card[-1]]["Level"]):
									stand = False
							else:
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
		if self.gd["turn"] == 1:
			Clock.schedule_once(self.beginning_phase)
		else:
			Clock.schedule_once(self.beginning_phase, phase_dt)

	def draw_phase(self, *args):
		self.gd["draw"] = 1
		Clock.schedule_once(self.draw, move_dt_btw)

	def effect_to_stage(self, s="Stage", dt=0):
		ind = self.gd["ability_trigger"].split("_")[1]
		if (ind[-1] == "1" and "oppturn" not in self.gd["effect"]) or (ind[-1] == "2" and "oppturn" in self.gd["effect"]):
			self.gd["move"] = ""
			self.gd["choose"] = True
			self.gd["status"] = self.add_to_status(f"{s}Select1", self.gd["effect"])
			self.select_field()
			Clock.schedule_once(partial(self.popup_text, "Move"))
		elif self.gd["com"] and ((ind[-1] == "2" and "oppturn" not in self.gd["effect"]) or (ind[-1] == "1" and "oppturn" in self.gd["effect"])):
			pick = self.ai.play_stage(self.pd, self.cd, self.gd)

			if "AI_PlayStage" in pick:
				inx = pick.index("AI_PlayStage")
				if len(self.gd["target"])>1:
					temp = []
					for _ in self.gd["target"]:
						temp.append(_)
						temp.append(pick[inx + 1+self.gd["target"].index(_)])
					self.gd["target"] = list(temp)
				else:
					self.gd["target"].append(pick[inx + 1])

			else:
				self.gd["target"].append("")

			if "search" in self.gd["ability_doing"]:
				self.search()
			elif "salvage" in self.gd["ability_doing"]:
				self.salvage()
			elif "discard" in self.gd["ability_doing"]:
				self.discard()
			elif "heal" in self.gd["ability_doing"]:
				self.heal()
			elif "move" in self.gd["ability_doing"]:
				self.move()

	def popup_title_search(self, ind="", uptomay="", word=""):
		if not ind:
			ind = self.gd["ability_trigger"].split("_")[1]
		if not word:
			word = " card"
		search = ""
		if "NameSet" in self.gd["search_type"]:
			n = self.gd["search_type"].split("_")[1:]
			if len(n) / 2 == 1:
				search = f"character with\"{n}\" in its card name"
			else:
				search = f"character with\"{n}\" or \"{n}\" in its card name"
		elif "CLevel" in self.gd["search_type"]:
			c = ""
			l = self.gd["search_type"].split("_")[1]
			if "CLevelC" in self.gd["search_type"]:
				c = self.gd["search_type"].split("_")[-1]

			if "_standby" in l:
				lvl = f"{len(self.pd[ind[-1]]['Level']) + 1} or lower"
			elif "<=p" in l:
				if "<=p+" in l:
					lvl = f"{len(self.pd[ind[-1]]['Level']) + int(l[-1])} or lower"
				else:
					lvl = f"{len(self.pd[ind[-1]]['Level'])} or lower"
			elif "=p" in l:
				lvl = "equal to your level"
			elif "<=" in l:
				lvl = f"{l[-1]} or lower"
			elif ">=" in l:
				lvl = f"{l[-1]} or higher"
			elif "==" in l:
				lvl = f"{l[-1]}"
			if "=p" in l and "<=p" not in l:
				search = f"character with level {lvl}"
			else:
				search = f"level {lvl} "
				if "CLevelC" not in self.gd["search_type"]:
					search += "character"

				if "CLevelN" in self.gd["search_type"]:
					search += f" with \"{self.gd['search_type'].split('_')[-1]}\" in its card name"
				elif "CLevelC" in self.gd["search_type"]:
					search += f"and cost {c[-1]} or "
					if "<=" in c:
						search += "lower"
					elif ">=" in c:
						search += "higher"
					search += " character"
		elif "TraitLC" in self.gd["search_type"]:
			trait = self.gd['search_type'].split('_')[1:-2]
			lc = [self.gd['search_type'].split('_')[-2], self.gd['search_type'].split('_')[-1]]
			search = "level "
			if "<=p" in lc[0]:
				search += f"{len(self.pd[ind[-1]]['Level'])} or lower"
			if "<=" in lc[1]:
				search += f" and cost {lc[1][-1]} or lower"
			for rr in range(len(trait)):
				if rr == 0:
					search += f" with «{trait[rr]}»"
				else:
					search += f" or «{trait[rr]}»"
			search += " character"
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
					search += f"«{trait[rr]}»"
				else:
					search += f" or «{trait[rr]}»"
			search += " character"
		elif "TraitN" in self.gd["search_type"]:
			if "BTraitN" in self.gd["search_type"]:
				search = f"«{self.gd['search_type'].split('_')[1]}» and_\"{self.gd['search_type'].split('_')[-1]}\" in its card name"
			elif "TraitN=" in self.gd["search_type"]:
				search = f"«{self.gd['search_type'].split('_')[1]}» or \"{self.gd['search_type'].split('_')[-1]}\""
			else:
				search = f"«{self.gd['search_type'].split('_')[1]}» or \"{self.gd['search_type'].split('_')[-1]}\" in its card name"
		elif "TraitE" in self.gd["search_type"]:
			for _ in self.gd['search_type'].split('_')[1:]:
				if not search:
					search=f"«{_}»"
				else:
					search += f" or «{_}»"
			search += " character or event card"
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
			if "TextN" in self.gd["search_type"]:
				name = self.gd['search_type'].split('_')[-1]
				search += f" or with \"{name}\" in its card name"
		elif "EachCName" in self.gd["search_type"]:
			name = self.gd['search_type'].split('_')[1:]
			for x in range(len(name)):
				if x == 0:
					search += f"character with \"{name[x]}\" in name"
				else:
					search += f" and {uptomay}character with \"{name[x]}\" in its card name"
		elif "NameO_" in self.gd["search_type"]:
			name = self.gd['search_type'].split('_')
			search = f"\"{name[1]}\" in its card name other than \"{name[2]}\""
		elif "Name" in self.gd["search_type"]:
			if "Name=T" in self.gd["search_type"]:
				n = self.gd['search_type'].split('_')[1:-1]
				t = self.gd['search_type'].split('_')[-1]
			else:
				n = self.gd['search_type'].split('_')[1:]
				t = ""

			for s in range(len(n)):
				if s == 0:
					search += f"\"{n[s]}\""
				else:
					search += f" or \"{n[s]}\""

			if "CName=" in self.gd["search_type"]:
				search += "character"
			elif "Name=T" in self.gd["search_type"]:
				search += f" or «{t}» character"
			elif "Name=" in self.gd["search_type"]:
				pass
			elif "CXName" in self.gd["search_type"]:
				search = f"climax wih {search} in its card name"
			elif "CName" in self.gd["search_type"]:
				search = f"character wih {search} in its card name"
			else:
				search = f"{word} wih {search} in its card name"
		elif "CTrigger" in self.gd["search_type"]:
			search = f"character with {self.gd['search_type'].split('_')[1].upper()} in its trigger icon"
		elif "TriggerCX" in self.gd["search_type"]:
			search = f"climax with a {self.gd['search_type'].split('_')[1]} trigger icon"
		elif "CNCost" in self.gd["search_type"]:
			nc = self.gd['search_type'].split('_')
			if "<=" in nc[2]:
				search += f"cost {nc[2][-1]} or lower"
			search += f" character with \"{nc[1]}\" in name"
		elif "CCost" in self.gd["search_type"]:
			cost = self.gd['search_type'][-1]
			if "CCostT" in self.gd["search_type"]:
				cost = self.gd["search_type"].split("_")[1][-1]
			search = f"cost {cost} "
			if "<=" in self.gd["search_type"]:
				search += "or lower"
			elif ">=" in self.gd["search_type"]:
				search += "or higher"
			if "CCostT" in self.gd["search_type"]:
				search += f' «{self.gd["search_type"].split("_")[2]}»'
			search += " character"
		elif "CColourT" in self.gd["search_type"]:
			search = f"character that is either {self.gd['search_type'].split('_')[1]} or «{self.gd['search_type'].split('_')[2]}»"
		elif "Colour" in self.gd["search_type"]:
			cc = self.gd["search_type"].split("_")[1:]
			for rr in range(len(cc)):
				if rr == 0:
					search += f"{cc[rr].lower()}"
				else:
					search += f" or {cc[rr].lower()}"
			if "ColourCx" in self.gd["search_type"]:
				search = f"{search} climax"
			else:
				search = f"{search} card"
		elif "Face-down" in self.gd["search_type"]:
			search = f"face down card"
		else:
			if "Character" in self.gd["search_type"] or "Event" in self.gd["search_type"] or "Climx" in self.gd["search_type"]:
				word = ""
			if len(self.gd['search_type'].split('_')) > 1:
				ss = self.gd['search_type'].split('_')
				for rr in range(len(ss)):
					if rr == 0:
						search += f"{ss[rr]}"
					else:
						search += f" or {ss[rr]}{word}"
			else:
				search = f'{self.gd["search_type"].lower()}{word}'
				if not search:
					search = word

		return search

	def search(self, dt=0):
		imd = self.gd["ability_trigger"].split("_")[1]
		if self.gd["p_c"] != "" and (not self.gd["target"] or self.gd["p_again"]):
			self.gd["p_again"] = False
			self.sd["popup"]["popup"].dismiss()
			if self.net["game"] and "oppturn" in self.gd["effect"] and not self.net["send"]:
				self.net["var"] = list(self.gd["chosen"])
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
					if "Change" in self.gd["effect"]:
						self.gd["move"] = self.cd[imd].pos_old
						Clock.schedule_once(self.search)
					else:
						if len([c for c in self.gd["chosen"] if c != ""]) > 0:
							self.effect_to_stage()
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

			search = self.popup_title_search(ind, uptomay)

			c = "Search"
			if "Reveal" in self.gd["effect"]:
				c += "_Reveal"
			elif "stsearch" in self.gd["effect"]:
				c += "_Stock"

			if "Reveal" in self.gd["effect"]:
				self.sd["popup"]["popup"].title = f"Choose {uptomay}{self.gd['search']} {search}"
			elif "BTraitN" in self.gd["search_type"]:
				self.sd["popup"]["popup"].title = f"Search {uptomay}{self.gd['search'] - 1} {search.split('_')[0]} {uptomay}{self.gd['search'] - 1} {search.split('_')[1]}"
			else:
				self.sd["popup"]["popup"].title = f"Search {uptomay}{self.gd['search']} {search}"
			self.gd["confirm_var"] = {"o": ind[-1], "c": c, "m": self.gd["search"]}
			self.popup_start()
		else:
			if self.gd["end_stage"]:
				self.gd["end_stage"] = False
				self.gd["target"][-1] = ""
				self.gd["target"].append("")
				self.gd["p_stage"] -= 1
			elif "Stage" in self.gd["effect"] and self.gd["move"] and (imd[-1] == "1" or (imd[-1] == "2" and "oppturn" in self.gd["effect"]) or (imd[-1] == "2" and self.gd["com"] and "oppturn" not in self.gd["effect"])):
				if self.gd["uptomay"] and (not self.gd["move"] or self.gd["move"] == "none"):
					self.gd["target"].append("")
				else:
					self.gd["target"].append(self.gd["move"])
				self.gd["move"] = ""
				self.gd["p_stage"] -= 1

			if "Stage" in self.gd["effect"] and self.gd["p_stage"] > 0 and len([c for c in self.gd["target"] if c == ""]) < 2:
				self.gd["p_again"] = True
				self.gd["confirm_var"] = dict(self.gd["confirm_temp"])
				self.gd["confirm_var"]["m"] = self.gd["p_stage"]
				self.popup_start()
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
				st = ""
				if "Stage" in self.gd["effect"]:
					st = self.gd["target"].pop(0)
				if self.net["game"] and self.gd["p_owner"] == "1" and not self.gd["oppchoose"]:  
					self.net["act"][4].append(ind)
					if "Stage" in self.gd["effect"]:
						self.net["act"][4].append(st)
				if ind in self.emptycards:
					continue
				if "extra" in self.gd["effect"]:
					if ind not in self.gd["extra"]:
						self.gd["extra"].append(ind)
				if "Stage" in self.gd["effect"]:
					if st:
						self.gd["standby"] = [imd, self.cd[imd].name, ind]
						self.cpop[ind].stage_slc(False)
						for _ in range(select2cards):
							self.field_btn[f"stage{_}{ind[-1]}s"].pos = (-Window.width * 2, -Window.height * 2)
						self.play_to_stage(ind, st)
				elif "Waiting" in self.gd["effect"]:
					self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
					self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])
					self.pd[ind[-1]]["Library"].remove(ind)
					self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Waiting"], t="Waiting")
					self.pd[ind[-1]]["Waiting"].append(ind)
					wait.append(ind)
				elif "Stock" in self.gd["effect"]:
					self.send_to("Stock", ind)
				else:
					if "Reveal" in self.gd["effect"]:
						self.pd[ind[-1]]["Res"].remove(ind)
					elif "stsearch" in self.gd["effect"]:
						self.pd[ind[-1]]["Stock"].remove(ind)
					else:
						self.pd[ind[-1]]["Library"].remove(ind)
					self.pd[ind[-1]]["Hand"].append(ind)

				player = ind[-1]
				if player == "2":
					idm.append(ind)

			if self.gd["notarget"]:
				self.gd["notarget"] = False

			self.hand_size(imd[-1])
			self.update_field_label()

			if "Reveal" in self.gd["effect"] and "extrareveal" not in self.gd["effect"]:
				for inx in range(len(self.pd[imd[-1]]["Res"])):
					temp = self.pd[imd[-1]]["Res"].pop(0)
					self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Waiting"], t="Waiting")
					self.pd[temp[-1]]["Waiting"].append(temp)
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
			elif "stsearch" in self.gd["effect"] and "top" in self.gd["effect"]:
				self.ability_effect()
			elif "stsearch" in self.gd["effect"] and "stshuff" in self.gd["effect"]:
				self.gd["shufflest_trigger"] = "ability"
				if self.net["game"]:
					self.gd["shuffle_send"] = True
				self.shuffle_stock(imd[-1])
			else:
				self.gd["shuffle_trigger"] = "ability"
				if self.net["game"]:
					self.gd["shuffle_send"] = True
				if "noshuff" in self.gd["effect"]:
					self.ability_effect()
				else:
					self.shuffle_deck(imd[-1])

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
					if "w/oextra" in self.gd["effect"] and temp in self.gd["extra"]:
						self.pd[player]["Waiting"].insert(0, temp)
					else:
						self.pd[player]["Library"].append(temp)
						self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Library"], t="Library")
				self.update_field_label()

			if "extra" not in self.gd["effect"]:
				self.gd["extra"] = []
			self.gd["shuffle_trigger"] = "ability"
			self.gd["ability_effect"].remove("shuffle")
			self.do_check()
			if self.net["game"]:
				self.gd["shuffle_send"] = True
			if "both" in self.gd["effect"]:
				self.shuffle_deck("0")
			else:
				self.shuffle_deck(player)
		elif self.gd["effect"][0] == 0:
			if "shuffle" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("shuffle")

			self.gd["shuffle_trigger"] = "ability"
			self.do_check()
			if self.net["game"]:
				self.gd["shuffle_send"] = True
			self.shuffle_deck(player)
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
					self.popup_start()
				else:
					self.gd["p_c"] = "Shuffle_"
					self.gd["chosen"] = []
					self.shuffle_ability()
			else:
				if "shuffle" in self.gd["ability_effect"]:
					self.gd["ability_effect"].remove("shuffle")

				for r in range(self.gd["effect"][0]):
					temp = self.gd["target"].pop(0)
					if self.net["game"] and self.gd["p_owner"] == "1":  
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
				if self.net["game"]:
					self.gd["shuffle_send"] = True
				self.shuffle_deck(player)

	def salvage(self, dt=0):
		imd = self.gd["ability_trigger"].split("_")[1]
		if self.gd["p_c"] != "" and (not self.gd["target"] or self.gd["p_again"]):
			self.gd["p_again"] = False
			self.sd["popup"]["popup"].dismiss()

			if self.gd["p_stage"] <= 0:
				if len(self.gd["chosen"]) < self.gd["salvage"]:
					for r in range(self.gd["salvage"] - len(self.gd["chosen"])):
						self.gd["chosen"].append("")
				self.gd["target"] = list(self.gd["chosen"])
			else:
				if len(self.gd["chosen"]) > 0:
					for card in self.gd["chosen"]:
						self.gd["target"].append(card)
				else:
					self.gd["target"].append("")

			if self.gd["notarget"]:
				self.gd["notarget"] = False

			if "Stage" in self.gd["effect"]:
				if "Change" in self.gd["effect"]:
					self.gd["move"] = self.cd[imd].pos_old
					Clock.schedule_once(self.salvage)
				elif "swap" in self.gd["effect"]:
					if self.gd["extra"]:
						self.gd["move"] = self.cd[self.gd["extra"][0]].pos_old
						self.gd["extra"] = []
					Clock.schedule_once(self.salvage)
				elif self.gd["com"] and ((imd[-1] == "2" and "oppturn" not in self.gd["effect"]) or (imd[-1] == "1" and "oppturn" in self.gd["effect"])):
					stage = []
					for s in self.gd["stage"]:
						if self.pd[self.gd["p_owner"]][s[:-1]][int(s[-1])] == "":
							stage.append(s)
					if len(stage) > 0 or "Open" in self.gd["effect"]:
						if self.gd["target"] and self.cd[self.gd["target"][0]].pos_old[:-1] in self.stage and self.pd[self.gd["p_owner"]][self.cd[self.gd["target"][0]].pos_old[:-1]][int(self.cd[self.gd["target"][0]].pos_old[-1])] == "":
							self.gd["target"].append(self.cd[self.gd["target"][0]].pos_old)
						else:
							self.gd["target"].append(stage[0])
					elif "Open" not in self.gd["effect"] and len(stage) <= 0:
						self.gd["target"].append(choice(self.gd["stage"]))
					Clock.schedule_once(self.salvage)
				else:
					if len([c for c in self.gd["chosen"] if c != ""]) > 0:
						self.effect_to_stage()
					else:
						self.gd["move"] = "none"
						Clock.schedule_once(self.salvage)
			elif "choice" in self.gd["effect"]:
				if self.gd["p_owner"] == "1" and len([s for s in self.gd["chosen"] if s != ""]) > 0:
					Clock.schedule_once(partial(self.popup_text, "choice"))
				elif self.gd["p_owner"] == "2" and self.opp_choice == "Stock":
					Clock.schedule_once(self.stocker)
				else:
					Clock.schedule_once(self.salvage)
			elif "swap" in self.gd["effect"]:
				swap = self.gd["effect"][self.gd["effect"].index("swap") + 1]
				if "CX" in swap:
					swap = "Climax"
				if len(self.gd["target_temp"]) > 0:
					for rr in self.gd["target_temp"]:
						self.gd["target"].append(rr)
					self.gd["target_temp"] = []
				elif len([s for s in self.gd["target"] if s != ""]) > 0:
					if "Resonance" in self.gd["effect"]:
						for rr in self.gd["resonance"][1]:
							self.gd["target"].append(rr)
					elif len(self.pd[imd[-1]][swap]) > 0:
						for rr in self.gd["target"]:
							self.gd["target_temp"].append(rr)
						self.gd["target"] = []
						if "salvage" in self.gd["ability_effect"]:
							self.gd["ability_effect"].remove("salvage")
						self.gd["done"] = True
						self.gd["salvage"] = 0
						Clock.schedule_once(self.ability_effect)
						return False
				Clock.schedule_once(self.salvage)
			else:
				Clock.schedule_once(self.salvage)
		elif self.gd["p_c"] == "" and not self.gd["target"]:

			if self.gd["uptomay"]:
				uptomay = "up to "
			else:
				uptomay = ""

			ind = self.gd["ability_trigger"].split("_")[1]
			if ("oppturn" in self.gd["effect"] and "opp" in self.gd["effect"]) and ind[-1] == "1":
				if "Opp" in self.gd["effect"]:
					opp = "2"
				else:
					opp = "1"
			elif ("oppturn" in self.gd["effect"] and "opp" in self.gd["effect"]) and ind[-1] == "2":
				if "Opp" in self.gd["effect"]:
					opp = "1"
				else:
					opp = "2"
			elif ("oppturn" in self.gd["effect"] or "opp" in self.gd["effect"]) and ind[-1] == "1":
				opp = "2"
			elif ("oppturn" in self.gd["effect"] or "opp" in self.gd["effect"]) and ind[-1] == "2":
				opp = "1"
			else:
				opp = ind[-1]

			if "_standby" in self.gd["search_type"]:
				search = f"level {len(self.pd[opp]['Level']) + 1} or lower character"
			elif "BTrait" in self.gd["search_type"]:
				pass
			else:
				search = self.popup_title_search(ind, uptomay)

			c = "Salvage"
			if "revive" in self.gd["effect"]:
				c = f"revive_{c}"
			elif "marker" in self.gd["effect"]:
				c = f"Marker_{c}"
			elif "ksalvage" in self.gd["effect"]:
				c += f"_Markers_{ind}"
				self.gd["ksalvage"] = str(ind)
			elif "csalvage" in self.gd["effect"]:
				c += "_Clock"
			elif "msalvage" in self.gd["effect"]:
				c += "_Memory"
			if "Revealed" in self.gd["effect"]:
				c += "_Reveal"
			if "&Hand" in self.gd["effect"]:
				c += "_&Hand"

			if "ID=" in self.gd["search_type"] and "passed" in self.gd["effect"]:
				self.sd["popup"]["popup"].title = f"Choose cards from previous effect to continue."
			elif "Name=" in self.gd["search_type"] or "NameO_" in self.gd["search_type"]:
				if "passed" in self.gd["effect"]:
					self.sd["popup"]["popup"].title = f"Choose characters from previous effect to continue."
				else:
					self.sd["popup"]["popup"].title = f"Choose {uptomay}{self.gd['salvage']} {search}"
			elif "Name" in self.gd["search_type"]:
				self.sd["popup"]["popup"].title = f"Choose a character with {search} in its card name"
			elif "BTrait" in self.gd["search_type"]:
				self.gd["btrait"][1] = self.gd["search_type"].split("_")[1:]
				self.gd["btrait"][3] = list(self.gd["btrait"][1])
				if self.gd["salvage"] == len(self.gd["btrait"][1]):
					for nx in range(len(self.gd["btrait"][1])):
						if nx == 0:
							self.sd["popup"]["popup"].title = f"Choose {uptomay}1 «{self.gd['btrait'][1][nx]}» character"
						elif nx == len(self.gd["btrait"][1]) - 1:
							self.sd["popup"]["popup"].title += f", and {uptomay}1 «{self.gd['btrait'][1][nx]}» character"
						else:
							self.sd["popup"]["popup"].title += f", {uptomay}1 «{self.gd['btrait'][1][nx]}» character"
			else:
				if "swap" in self.gd["effect"] and "Stage" not in self.gd["effect"]:
					self.sd["popup"]["popup"].title = f"Choose {uptomay}{self.gd['salvage']} {search} in waiting room"
				else:
					self.sd["popup"]["popup"].title = f"Choose {uptomay}{self.gd['salvage']} {search}"

			self.gd["confirm_var"] = {"o": opp, "c": c, "m": self.gd["salvage"]}
			self.popup_start()
		else:
			if self.gd["end_stage"]:
				self.gd["end_stage"] = False
				self.gd["target"][-1] = ""
				self.gd["target"].append("")
				self.gd["p_stage"] -= 1
			elif "Stage" in self.gd["effect"] and self.gd["move"] and (imd[-1] == "1" or (imd[-1] == "2" and "oppturn" in self.gd["effect"]) or (imd[-1] == "2" and self.gd["com"] and "oppturn" not in self.gd["effect"])):
				if not self.gd["move"] or self.gd["move"] == "none":
					self.gd["target"].append("")
				else:
					self.gd["target"].append(self.gd["move"])
				self.gd["move"] = ""
				self.gd["p_stage"] -= 1

			if "Stage" in self.gd["effect"] and self.gd["p_stage"] > 0 and len([c for c in self.gd["target"] if c == ""]) < 2:
				self.gd["p_again"] = True
				self.gd["confirm_var"] = dict(self.gd["confirm_temp"])
				self.gd["confirm_var"]["m"] = self.gd["p_stage"]
				self.popup_start()
				return False
			if "Stage" in self.gd["effect"] and len(self.gd["target"]) < self.gd["effect"][0] * 2:
				for r in range(self.gd["salvage"] * 2 - len(self.gd["target"])):
					self.gd["target"].append("")


			idm = []
			player = ""
			ss = ""
			lif = []
			bb = 0
			for r in range(self.gd["salvage"]):
				ind = self.gd["target"].pop(0)
				st = ""
				if "Stage" in self.gd["effect"]:
					st = self.gd["target"].pop(0)
				if self.net["game"] and imd[-1] == "1" and "oppturn" not in self.gd["effect"]:  
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
				if "nogain" in self.gd["effect"]:
					player = ind[-1]
					if player == "2" or (player == "1" and imd[-1] == "2"):
						idm.append(ind)
					continue
				if "Zwei" in self.gd["effect"]:
					self.gd["target"].append(ind)
					continue
				if "Stage" in self.gd["effect"]:
					if st:
						self.gd["standby"] = [imd, self.cd[imd].name, ind]
						if "change [" in self.gd["ability"].lower():
							self.gd["standby"].append("Change")
						self.cpop[ind].stage_slc(False)
						for _ in range(select2cards):
							self.field_btn[f"stage{_}{ind[-1]}s"].pos = (-Window.width * 2, -Window.height * 2)
						if self.net["game"] and "oppturn" in self.gd["effect"] and imd[-1] == "2":
							self.net["var"] = [ind, st]
							self.net["var1"] = f"oppchoose_play_{ind}_{st}"
							if not self.poptext:
								Clock.schedule_once(partial(self.popup_text, "waitingser"))
							self.mconnect("plturn")
							return False
						else:
							self.play_to_stage(ind, st)
				elif "swap" in self.gd["effect"]:
					if "this" in self.gd["effect"]:
						lv = imd
					else:
						lv = self.gd["target"].pop(0)

					lvpos = self.cd[lv].pos_new
					indpos = self.cd[ind].pos_new
					swap = self.gd["effect"][self.gd["effect"].index("swap") + 1]
					if "CX" in swap:
						swap = "Climax"
					if swap in lvpos or swap in indpos:
						if swap in lvpos:
							lpos = self.pd[lv[-1]][swap].index(lv)
							self.send_to(lvpos, ind, lpos)
							self.send_to(indpos, lv)
						else:
							lpos = self.pd[ind[-1]][swap].index(ind)
							self.send_to(lvpos, ind)
							self.send_to(indpos, lv, lpos)
					else:
						self.send_to(lvpos, ind)
						self.send_to(indpos, lv)
				else:
					if "Library" in self.gd["effect"] or "wdecker" in self.gd["effect"] or "WDecker" in self.gd["effect"]:
						self.check_pos(ind)
						if "top" in self.gd["effect"]:
							self.pd[ind[-1]]["Library"].append(ind)
							ss = ""
						elif "bottom" in self.gd["effect"]:
							self.stack(ind[-1])
							self.pd[ind[-1]]["Library"].insert(0, ind)
							ss = ""
						else:
							self.pd[ind[-1]]["Library"].append(ind)
							ss = ind[-1]
						self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Library"], t="Library")
						self.update_field_label()
						self.check_cont_ability()
					elif "Clock" in self.gd["effect"]:
						if "bottom" in self.gd["effect"]:
							self.send_to("Clock", ind, bb)
							bb += 1
						else:
							self.send_to("Clock", ind)
					elif "Memory" in self.gd["effect"]:
						self.send_to("Memory", ind)
					elif "Stock" in self.gd["effect"]:
						self.send_to("Stock", ind)
					else:
						self.send_to("Hand", ind)
						self.update_field_label()
						if "csalvage" not in self.gd["effect"] and "msalvage" not in self.gd["effect"]:
							self.check_auto_ability(sav=ind, stacks=False)

				player = ind[-1]
				if player == "2" or (player == "1" and imd[-1] == "2"):
					idm.append(ind)

			if "salvage" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("salvage")
				if self.gd["ksalvage"]:
					self.update_marker(self.gd["ksalvage"][-1])
					self.gd["ksalvage"] = ""

				if self.gd["markers"]:
					self.gd["markers"] = []

			if "revive" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("revive")

			if "Revealed" in self.gd["effect"] and "exReveal" not in self.gd["effect"]:
				if len(self.pd[imd[-1]]["Res"]) > 0:
					for inx in range(len(self.pd[imd[-1]]["Res"])):
						temp = self.pd[imd[-1]]["Res"].pop(0)
						self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Waiting"], t="Waiting")
						self.pd[temp[-1]]["Waiting"].append(temp)
						self.update_field_label()

			self.popup_clr()
			if self.gd["notarget"]:
				self.gd["notarget"] = False
			self.gd["search_type"] = ""
			self.gd["salvage"] = 0
			if "BTrait" in self.gd["search_type"]:
				self.gd["btrait"] = ["", [], [], [], [], []]

			if "swap" in self.gd["effect"] and len(self.gd["target_temp"]) > 0:
				self.gd["target_temp"] = []

			if "wdecker" in self.gd["effect"]:
				self.gd["effect"].remove("wdecker")

			if "do" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("do")

			if "if" in self.gd["effect"]:
				if lif or ("swap" in self.gd["effect"] and not lif):
					self.gd["done"] = True
					if isinstance(self.gd["effect"][self.gd["effect"].index("if") + 1], int) and len(lif) < self.gd["effect"][self.gd["effect"].index("if") + 1]:
						self.gd["done"] = False
					if "ifLevel" in self.gd["effect"] and all(self.cd[cc].level_t < self.gd["effect"][self.gd["effect"].index("ifLevel") + 1] for cc in lif):
						self.gd["done"] = False
				if not self.gd["done"] and "ifnot" in self.gd["effect"]:
					self.gd["ability_effect"].append("dont")
			elif "do" in self.gd["effect"] and self.gd["do"][0] > 0:
				self.gd["done"] = True

			if self.gd["pay"] and not self.gd["payed"]:
				if "ClockW" in self.gd["pay"]:
					self.gd["pay"].remove("ClockW")
					self.gd["effect"].remove("Clock")
					if "Cbottom" in self.gd["pay"]:
						self.gd["effect"].remove("bottom")
				Clock.schedule_once(self.pay_condition, move_dt_btw)
			elif player == "1" and imd[-1] == "2" and "show" in self.gd["effect"] and len(idm) > 0:
				self.popup_multi_info(cards=idm, owner=player, t="OChoose", shuffle=ss)
			elif player == "2" and imd[-1] == "2" and "show" in self.gd["effect"] and len(idm) > 0:
				self.popup_multi_info(cards=idm, owner=player, t="Salvage", shuffle=ss)
			else:
				if ss:
					self.gd["shuffle_trigger"] = "ability"
					if self.net["game"]:
						self.gd["shuffle_send"] = True
					self.shuffle_deck(ss)
				else:
					if self.net["game"] and (("plchoose" in self.gd["effect"] and not self.net["send"]) or (self.gd["perform_both"] and "oppturn" not in self.gd["effect"])):
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

		if "Face-down" in self.gd["search_type"]:
			if self.cd[ind].back:
				return True
		elif "Colour" in self.gd["search_type"]:
			if "ColourCx" in self.gd["search_type"]:
				if "Climax" in self.cd[ind].card and self.cd[ind].mcolour.lower() in self.gd["search_type"].lower():
					return True
			elif "CColourT" in self.gd["search_type"]:
				if "Character" in self.cd[ind].card and (self.cd[ind].mcolour.lower() in self.gd["search_type"].split("_")[1].lower() or self.gd["search_type"].split("_")[2] in self.cd[ind].trait_t):
					return True
			elif self.cd[ind].mcolour.lower() in self.gd["search_type"].split("_")[1].lower():
				return True
		elif "ID=" in self.gd["search_type"]:
			if any(name == ind for name in self.gd["search_type"].split("_")[1:]):
				return True
		elif "TraitZ" in self.gd["search_type"]:
			if "Character" in self.cd[ind].card:
				if "_<=" in self.gd["search_type"] and "p" not in self.gd["search_type"][-1] and any(tr in self.cd[ind].trait_t for tr in self.gd["search_type"].split("_")[1:-1]) and self.cd[ind].level_t + self.cd[ind].cost_t <= int(self.gd["search_type"][-1]):
					return True
		elif "TraitLC" in self.gd["search_type"]:
			if "Character" in self.cd[ind].card and "<=p" in self.gd["search_type"] and self.cd[ind].level_t <= len(self.pd[ind[-1]]["Level"]) and self.cd[ind].cost_t <= int(self.gd["search_type"][-1]) and any(tr in self.cd[ind].trait_t for tr in self.gd["search_type"].split("_")[1:-1]):
				return True
		elif "TraitL" in self.gd["search_type"]:
			if "Character" in self.cd[ind].card:
				if "_<=p" in self.gd["search_type"] and any(tr in self.cd[ind].trait_t for tr in self.gd["search_type"].split("_")[1:-1]) and self.cd[ind].level_t <= len(self.pd[ind[-1]]["Level"]):
					return True
				elif "_<=" in self.gd["search_type"] and "p" not in self.gd["search_type"][-1] and any(tr in self.cd[ind].trait_t for tr in self.gd["search_type"].split("_")[1:-1]) and self.cd[ind].level_t <= int(self.gd["search_type"][-1]):
					return True
				elif "_>=" in self.gd["search_type"] and "p" not in self.gd["search_type"][-1] and any(tr in self.cd[ind].trait_t for tr in self.gd["search_type"].split("_")[1:-1]) and self.cd[ind].level_t >= int(self.gd["search_type"][-1]):
					return True
				elif "_=" in self.gd["search_type"] and "p" not in self.gd["search_type"][-1] and any(tr in self.cd[ind].trait_t for tr in self.gd["search_type"].split("_")[1:-1]) and self.cd[ind].level_t == int(self.gd["search_type"][-1]):
					return True
		elif "TTName" in self.gd["search_type"]:
			if "Character" in self.cd[ind].card and (self.gd["search_type"].split("_")[1] in self.cd[ind].trait_t or self.gd["search_type"].split("_")[2] in self.cd[ind].trait_t or self.gd["search_type"].split("_")[-1] in self.cd[ind].name_t):
				return True
		elif "TraitE" in self.gd["search_type"]:
			if "Event" in self.cd[ind].card or any(trait in self.cd[ind].trait_t for trait in self.gd["search_type"].split("_")[1:]):
				return True
		elif "BTrait" in self.gd["search_type"]:
			if "Character" in self.cd[ind].card and self.gd["btrait"][3]:
				b = 0
				t = []


				for tr in self.gd["btrait"][3]:
					if "N/" in tr and tr.split("N/")[1] in self.cd[ind].name_t:
						b += 1
						t.append(tr)
					elif tr in self.cd[ind].trait_t:
						b += 1
						t.append(tr)

				if b == 0:
					return False
				elif not self.gd["btrait"][4]:
					if b == 1:
						self.gd["btrait"][3].remove(t[0])
						self.gd["btrait"][5].append((ind, t[0]))
					elif b > 1:
						self.gd["btrait"][4].append(ind)
					return True
				elif self.gd["btrait"][4]:
					ind1 = self.gd["btrait"][4].pop()
					b1 = 0
					t1 = []

					for tr in self.gd["btrait"][3]:
						if "N/" in tr and tr.split("N/")[1] in self.cd[ind1].name_t:
							b1 += 1
							t1.append(tr)
						elif tr in self.cd[ind1].trait_t:
							b1 += 1
							t1.append(tr)

					if b == 1 and b1 > 1 and t[0] in t1:
						self.gd["btrait"][3].remove(t[0])
						self.gd["btrait"][5].append((ind, t[0]))
						t1.remove(t[0])
						if len(t1) == 1:
							self.gd["btrait"][3].remove(t1[0])
							self.gd["btrait"][5].append((ind1, t1[0]))
						else:
							self.gd["btrait"][4].append(ind1)
						return True
					elif b > 1 and b1 > 1:
						if set(t) == set(t1):
							if b == 2 and b1 == 2:
								self.gd["btrait"][3].remove(t[0])
								self.gd["btrait"][5].append((ind, t[0]))
								t1.remove(t[0])
								self.gd["btrait"][3].remove(t1[0])
								self.gd["btrait"][5].append((ind1, t1[0]))
								return True
		elif "TraitN" in self.gd["search_type"]:
			if any(tr in self.cd[ind].trait_t for tr in self.gd["search_type"].split("_")[1:-1]) or self.gd["search_type"].split("_")[-1] in self.cd[ind].name_t:
				return True
		elif "Trait" in self.gd["search_type"]:
			if "Character" in self.cd[ind].card:
				if self.gd["search_type"].split("_")[1:] == [""] and len(self.cd[ind].trait_t) <= 0:
					return True
				elif self.gd["search_type"].split("_")[1:] != [""] and any(trait in self.cd[ind].trait_t for trait in self.gd["search_type"].split("_")[1:]):
					return True
		elif "EachCName" in self.gd["search_type"]:
			names = [n for n in self.gd["search_type"].split("_")[1:] if all(n not in self.cd[nid].name_t for nid in self.gd["chosen"])]
			if "Character" in self.cd[ind].card and any(name in self.cd[ind].name_t for name in names):
				return True
		elif "Name" in self.gd["search_type"]:
			if "NameO" in self.gd["search_type"]:
				if self.gd["search_type"].split("_")[1] in self.cd[ind].name_t and self.gd["search_type"].split("_")[2] not in self.cd[ind].name_t:
					return True
			elif "CName" in self.gd["search_type"]:
				if "Character" in self.cd[ind].card and any(name in self.cd[ind].name_t for name in self.gd["search_type"].split("_")[1:]):
					return True
			elif "CXName=" in self.gd["search_type"]:
				if "Climax" in self.cd[ind].card and any(name in self.gd["search_type"].split("_")[1:] for name in self.cd[ind].name_t.split("\n")):
					return True
			elif "CXName" in self.gd["search_type"]:
				if "Climax" in self.cd[ind].card and any(name in self.cd[ind].name_t for name in self.gd["search_type"].split("_")[1:]):
					return True
			elif "Name=T" in self.gd["search_type"]:
				if any(name in self.gd["search_type"].split("_")[1:-1] for name in self.cd[ind].name_t.split("\n")) or ("Character" in self.cd[ind].card and self.gd["search_type"].split("_")[-1] in self.cd[ind].trait_t):
					return True
			elif "Name=" in self.gd["search_type"]:
				if any(name in self.gd["search_type"].split("_")[1:] for name in self.cd[ind].name_t.split("\n")):
					return True
			else:
				if any(name in self.cd[ind].name_t for name in self.gd["search_type"].split("_")[1:]):
					return True
		elif "Text" in self.gd["search_type"]:
			if "TextN" in self.gd["search_type"]:
				if any(any(txt.lower() in text.lower() for txt in self.gd["search_type"].split("_")[1:-1]) for text in self.cd[ind].text_o) or self.gd["search_type"].split("_")[-1] in self.cd[ind].name_t:
					return True
			elif "CText" in self.gd["search_type"]:
				if "Character" in self.cd[ind].card and any(any(txt.lower() in text.lower() for txt in self.gd["search_type"].split("_")[1:]) for text in self.cd[ind].text_o):
					return True
			elif any(any(txt.lower() in text.lower() for txt in self.gd["search_type"].split("_")[1:]) for text in self.cd[ind].text_o):
				return True
		elif "CNCost" in self.gd["search_type"]:
			if "Character" in self.cd[ind].card and "<=" in self.gd["search_type"] and self.cd[ind].cost_t <= int(self.gd["search_type"][-1]) and self.gd["search_type"].split("_")[1] in self.cd[ind].name_t:
				return True
		elif "CCost" in self.gd["search_type"]:
			if "_<=" in self.gd["search_type"] and self.cd[ind].cost_t <= int(self.gd["search_type"].split("_")[1][-1]) and "Character" in self.cd[ind].card:
				if "CCostT" in self.gd["search_type"] and any(trait in self.cd[ind].trait_t for trait in self.gd["search_type"].split("_")[2:]):
					return True
				else:
					return True
			elif "_>=" in self.gd["search_type"] and self.cd[ind].cost_t >= int(self.gd["search_type"].split("_")[1][-1]) and "Character" in self.cd[ind].card:
				if "CCostT" in self.gd["search_type"] and any(trait in self.cd[ind].trait_t for trait in self.gd["search_type"].split("_")[2:]):
					return True
				else:
					return True
		elif "CLevelC" in self.gd["search_type"]:
			if self.gd["search_type"].count("<=") == 2 and "Character" in self.cd[ind].card and self.cd[ind].level_t <= int(self.gd["search_type"].split("_")[1][-1]) and self.cd[ind].cost_t <= int(self.gd["search_type"].split("_")[2][-1]):
				return True
		elif "CLevelE" in self.gd["search_type"]:
			if "<=" in self.gd["search_type"] and (("Character" in self.cd[ind].card and self.cd[ind].level_t <= int(self.gd["search_type"].split("_")[1][-1])) or "Event" in self.cd[ind].card):
				return True
		elif "CLevelN" in self.gd["search_type"] and "Character" in self.cd[ind].card:
			if "_standby" in self.gd["search_type"] and "Character" in self.cd[ind].card and self.cd[ind].level_t <= len(self.pd[ind[-1]]["Level"]) + 1 and self.gd["search_type"].split("_")[-1] in self.cd[ind].name_t:
				return True
			elif "<=" in self.gd["search_type"] and "Character" in self.cd[ind].card and self.cd[ind].level_t <= int(self.gd["search_type"].split("_")[1][-1]) and self.gd["search_type"].split("_")[-1] in self.cd[ind].name_t:
				return True
		elif "CLevel" in self.gd["search_type"]:
			if "_standby" in self.gd["search_type"] and self.cd[ind].level_t <= len(self.pd[ind[-1]]["Level"]) + 1 and "Character" in self.cd[ind].card:
				return True
			elif "_==" in self.gd["search_type"] and "Character" in self.cd[ind].card and self.cd[ind].level_t == int(self.gd["search_type"][-1]):
				return True
			elif "_<=p" in self.gd["search_type"] and "Character" in self.cd[ind].card:
				if "_<=p+" in self.gd["search_type"] and self.cd[ind].level_t <= len(self.pd[ind[-1]]["Level"]) + int(self.gd["search_type"][self.gd["search_type"].index("<=p+") + 4]):
					return True
				elif self.cd[ind].level_t <= len(self.pd[ind[-1]]["Level"]):
					return True
			elif "_<=" in self.gd["search_type"] and "p" not in self.gd["search_type"][-1] and "Character" in self.cd[ind].card and self.cd[ind].level_t <= int(self.gd["search_type"][-1]):
				return True
			elif "_>=" in self.gd["search_type"] and "p" not in self.gd["search_type"][-1] and "Character" in self.cd[ind].card and self.cd[ind].level_t >= int(self.gd["search_type"][-1]):
				return True
		elif "CTrigger" in self.gd["search_type"]:
			if "Character" in self.cd[ind].card and any(trigger in self.cd[ind].trigger for trigger in self.gd["search_type"].split("_")[1:]):
				return True
		elif "TriggerCX" in self.gd["search_type"]:
			if "Climax" in self.cd[ind].card and any(trigger in self.cd[ind].trigger for trigger in self.gd["search_type"].split("_")[1:]):
				return True
		elif "Level" in self.gd["search_type"]:
			if "_<=p" in self.gd["search_type"] and self.cd[ind].level_t <= len(self.pd[ind[-1]]["Level"]):
				return True
			elif "_<=" in self.gd["search_type"] and "p" not in self.gd["search_type"][-1] and self.cd[ind].level_t <= int(self.gd["search_type"][-1]):
				return True
			elif "_>=" in self.gd["search_type"] and "p" not in self.gd["search_type"][-1] and self.cd[ind].level_t >= int(self.gd["search_type"][-1]):
				return True
		elif ("Character" in self.gd["search_type"] or "Event" in self.gd["search_type"] or "Climax" in self.gd["search_type"]) and self.cd[ind].card in self.gd["search_type"]:
			return True
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
		self.gd["selected"] = ""
		if self.infot:
			self.infot.cancel()
			self.infot = None
		if self.infob:
			self.infob.cancel()
			self.infob = None
		if self.gd["phase"] in ("", "Janken") and self.gd["popup_done"][1]:  
			pass
		elif self.gd["btn_release"]:
			pass
		elif self.gd["moving"]:
			pass
		else:
			if "Trigger" in self.gd["btn_id"]:
				self.cardinfo.import_data(self.cd[self.pd[self.gd["active"]]["Res"][0]], annex_img,self.gd["DLimg"])
			elif self.gd["btn_id"][:-1] in self.fields:
				if self.gd["btn_id"][:-1] in self.gd["stage"]:
					cc = self.pd[str(self.gd["btn_id"][-1])][self.gd["btn_id"][:-2]][int(self.gd["btn_id"][-2])]
					if cc:
						if self.check_back_hidden(self.cd[cc]):
							self.cardinfo.import_data(self.cd[cc], annex_img,self.gd["DLimg"])
				elif "Climax" in self.gd["btn_id"]:
					try:
						cc = self.pd[str(self.gd["btn_id"][-1])][self.gd["btn_id"][:-1]][0]
						if cc:
							if self.check_back_hidden(self.cd[cc]):
								self.cardinfo.import_data(self.cd[cc], annex_img,self.gd["DLimg"])
					except IndexError:
						pass
				elif self.gd["btn_id"][:-1] in ("Memory", "Clock", "Level", "Waiting", "Res"):
					if self.pd[str(self.gd["btn_id"][-1])][self.gd["btn_id"][:-1]]:
						self.sd["popup"]["stack"].clear_widgets()
						self.popup_multi_info(field=self.gd["btn_id"][:-1], owner=self.gd["btn_id"][-1])
			else:
				if self.gd["btn_id"]:
					self.gd["info_p"] = True
					if self.check_back_hidden(self.cd[self.gd["btn_id"]]):
						self.cardinfo.import_data(self.cd[self.gd["btn_id"]], annex_img,self.gd["DLimg"])
					self.hand_size(self.gd["btn_id"][-1])

	def update_gdata_config(self, dt=0):
		for s in App.get_running_app().default_settings:
			self.gd[s] = bool(int(App.get_running_app().config.get("Settings", s)))

	def popup_text_start(self):
		self.sd["text"] = {}
		self.sd["text"]["popup"] = Popup(title="", separator_height=0, size_hint=(None, None))
		self.sd["text"]["popup"].bind(on_dismiss=self.popup_text_check_open)
		self.sd["text"]["c"] = ""
		self.sd["text"]["close"] = Button(size_hint=(None, None), text="Close", on_release=self.popup_text_close)
		self.sd["text"]["retry"] = Button(size_hint=(None, None), text="Retry", on_release=self.popup_text_retry)
		self.sd["text"]["label"] = Label(text="", text_size=(self.sd["card"][0] * 0.9 * starting_hand, None), halign='center', valign="middle")
		self.sd["text"]["hand"] = Button(size_hint=(None, None), text="Hand", on_release=self.popup_text_close, cid="hand")
		self.sd["text"]["stock"] = Button(size_hint=(None, None), text="Stock", on_release=self.popup_text_close, cid="stock")
		self.sd["text"]["stage"] = Button(size_hint=(None, None), text="Stage", on_release=self.popup_text_close, cid="stage")
		self.sd["text"]["sct"] = RelativeLayout()
		self.sd["text"]["popup"].content = self.sd["text"]["sct"]
		self.sd["text"]["sct"].add_widget(self.sd["text"]["label"])
		self.sd["text"]["sct"].add_widget(self.sd["text"]["close"])
		self.sd["text"]["sct"].add_widget(self.sd["text"]["retry"])
		self.sd["text"]["sct"].add_widget(self.sd["text"]["hand"])
		self.sd["text"]["sct"].add_widget(self.sd["text"]["stock"])
		self.sd["text"]["sct"].add_widget(self.sd["text"]["stage"])
		self.sd["popup_text_retry"] = False

	def popup_text_check_open(self, *args):
		self.poptext = False
		self.gd["text_popup"] = False

	def popup_text_retry(self, btn):
		if not self.sd["popup_text_retry"]:
			self.sd["popup_text_retry"] = True
			self.sd["text"]["popup"].dismiss()
			self.gd["text_popup"] = False
			if "LoadGame" in self.sd["text"]["c"]:
				self.main_scrn.disabled = True
				self.gd["load"] = True
				self.gd["gg"] = False
				self.gd["menu"] = False
				Clock.schedule_once(partial(self.popup_text, "Loading"), popup_dt)
				Clock.schedule_once(self.start_game, move_dt * 2)
			elif "update" in self.sd["text"]["c"]:
				var = self.sd["update"].split(".")
				if len(var) > 3 and "db" in var[3]:
					_ = ".".join(var[:4])
					self.net["var"] = [str(_), 0]
					self.net["var1"] = f"down_{_}"
					self.mconnect("down")
				else:
					if "debug" not in self.gd or ("debug" in self.gd and not self.gd["debug"]):
						if installer_info == "com.android.vending":
							url = 'market://details?id=' + app_package_name
							intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
							PythonActivity.mActivity.startActivity(intent)
						else:
							webbrowser.open('https://github.com/tintedmoth/wss/releases')
				scej["version"] = ".".join(var[:3])
				self.sd["update"] = False
				Clock.schedule_once(self.update_edata)
			elif "no_internet" in self.sd["text"]["c"] or "no_error" in self.sd["text"]["c"]:
				if self.net["status"] == "down":
					if self.downloads_key:
						down = self.downloads_key.pop()
						self.req[down] = UrlRequest(f"{self.downloads[down][0]}{down}", timeout=10, on_success=self.down_data, on_cancel=self.down_data_cnc, on_failure=self.failure_message, on_error=self.error_message, on_progress=self.progress_message, ca_file=cfi.where(), verify=True)
				else:
					Clock.schedule_once(self.mping_data, popup_dt * 3)

	def popup_text_close(self, btn):
		self.sd["text"]["popup"].dismiss()
		self.gd["text_popup"] = False
		if self.decks["dbuilding"]:
			pass
		elif self.gd["ability_doing"] == "look":
			self.gd["ability_doing"].remove("look")
			self.ability_effect()
		elif "Load" in self.sd["text"]["c"]:
			Clock.schedule_once(self.clear_loaded_game)
		elif "choice" in self.sd["text"]["c"]:
			if btn.cid == "hand":
				Clock.schedule_once(self.salvage)
			elif btn.cid == "stock":
				Clock.schedule_once(self.stocker)
			elif btn.cid == "stage":
				self.gd["target"] = []
				if "Stage" not in self.gd["effect"]:
					self.gd["effect"].append("Stage")
					if "StageRest" in self.gd["effect"]:
						self.gd["effect"].extend(["extra", "do", [-16, "rested"]])
					if "do" in self.gd["effect"]:
						self.gd["do"] = [1, list(self.gd["effect"][self.gd["effect"].index("do") + 1])]
				Clock.schedule_once(self.salvage)
			else:
				self.gd["target"] = []
				self.gd["choose"] = False
				self.gd["chosen"] = []
				self.gd["confirm_var"] = dict(self.gd["confirm_temp"])
				Clock.schedule_once(self.popup_start, move_dt_btw)
		elif "Counter" in self.sd["text"]["c"]:
			Clock.schedule_once(self.counter_step_done)
		elif "Climax" in self.sd["text"]["c"]:
			self.gd["phase"] = "Attack"
			Clock.schedule_once(self.attack_phase_beginning, phase_dt)
		elif self.gd["notargetfield"]:
			self.sd["btn"]["end"].disabled = True
			self.gd["move"] = "none"
			self.ability_effect()
		elif self.gd["notarget"]:
			self.sd["btn"]["end"].disabled = True
			self.gd["choose"] = True
			self.gd["chosen"] = []
			if len(self.gd["chosen"]) < self.gd["effect"][0]:
				for r in range(self.gd["effect"][0] - len(self.gd["chosen"])):
					self.gd["chosen"].append("")
			self.gd["target"] = list(self.gd["chosen"])
			self.ability_effect()
		elif "roomdis" in self.sd["text"]["c"] or "no_internet" in self.sd["text"]["c"] or "no_error" in self.sd["text"]["c"]:
			self.net = network_init()
			self.network["m_connect"].disabled = False
		elif self.sd["text"]["c"] == "waitingopp":
			self.mcancel_room()
		elif self.net["game"] and self.sd["text"]["c"] == "waiting":
			self.gd["popup_on"] = True
			self.sd["btn"]["continue"].disabled = False
			self.sd["cpop_press"] = []
			self.hand_btn_show()
			self.sd["btn"]["continue"].size = (Window.width / 5., self.sd["b_bar"].size[1])
			self.sd["btn"]["continue"].x = Window.width - self.sd["btn"]["continue"].size[0]
			self.sd["btn"]["continue"].y = 0
			self.gd["cont_on"] = True

	def popup_text_delay(self, *args):
		self.sd["text"]["popup"].open()

	def popup_text(self, c="", dt=0):
		try:
			self.multi_info["popup"].dismiss()
		except KeyError:
			pass
		self.cardinfo.dismiss()
		self.poptext = True
		self.gd["text_popup"] = True
		self.sd["popup_text_retry"] = False
		self.sd["text"]["c"] = c
		self.sd["cpop_press"] = []
		ptext = "　"

		xscat = self.sd["card"][0] * starting_hand
		yscat = self.sd["padding"] * 1.5 + self.sd["card"][1] / 4. + self.sd["padding"] * 8  

		self.sd["text"]["close"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
		yscat += self.sd["card"][1] / 4. + self.sd["padding"] * 2
		self.sd["text"]["close"].text = "Close"

		self.sd["text"]["retry"].y = -Window.height
		self.sd["text"]["hand"].y = -Window.height
		self.sd["text"]["stock"].y = -Window.height
		self.sd["text"]["stage"].y = -Window.height

		if "Debugtext" in c:
			ptext = c
			if mail[2] != "":
				ptext = mail[2]
		elif c in ("Attack", "Declaration"):
			ptext = "Choose a character and select the attack type"
		elif "Counter" in c:
			ptext = "There are no playable counter cards in your hand."
		elif "Climax" in c:
			ptext = "There are no playable climax cards in your hand."
		elif "Encore" in c:
			ptext = "Choose a reversed character and put it into the waiting room.\n(Repeate this step until there are no reversed character remaining.)"
		elif c == "connect":
			ptext = "Waiting for opponent to join."
			self.sd["text"]["close"].text = "Disconnect"
		elif "down" in c:
			ptext = "Trial version can only download 1 title."
		elif "no_internet" in c:
			self.sd["text"]["retry"].text = "Retry"
			ptext = "Cannot connect to server.\nPlease try again later."
		elif "no_error" in c:
			self.sd["text"]["retry"].text = "Retry"
			ptext = "There was an error while connect to the server.\nPlease try again."
		elif "choice" in c:
			if "StageRest" in self.gd["effect"]:
				ptext = "Return the card to your hand or put the card rested in any position on the stage"
				self.sd["text"]["stage"].y = self.sd["padding"] * 3.5 + self.sd["card"][1] / 2.
				self.sd["text"]["stage"].center_x = xscat / 4 * 3 - self.sd["card"][0] / 2  #
				self.sd["text"]["stage"].size = (self.sd["card"][0] * 2, self.sd["card"][1] / 2.)
			else:
				ptext = "Return the card to your hand or put the card into your stock"
				self.sd["text"]["stock"].y = self.sd["padding"] * 3.5 + self.sd["card"][1] / 2.
				self.sd["text"]["stock"].center_x = xscat / 4 * 3 - self.sd["card"][0] / 2  #
				self.sd["text"]["stock"].size = (self.sd["card"][0] * 2, self.sd["card"][1] / 2.)

			self.sd["text"]["hand"].y = self.sd["padding"] * 3.5 + self.sd["card"][1] / 2.
			self.sd["text"]["hand"].center_x = xscat / 4 - self.sd["padding"] / 2  #
			self.sd["text"]["hand"].size = (self.sd["card"][0] * 2, self.sd["card"][1] / 2.)
			self.sd["text"]["close"].text = "Back"
		elif "roomdis" in c:
			ptext = "There was an error joining the room.\nPlease try again later."
		elif "waiting" in c:
			if "opp" in c:
				ptext = "Found a room.\n Waiting for Opponent..."
			elif "ser" in c:
				ptext = "Connecting to server..."
			else:
				ptext = "Waiting for Opponent..."
				yscat += self.sd["card"][1] / 2
		elif "LookOpp" in c:
			ptext = "Opponent is looking at your hand"
		elif "making" in c:
			ptext = "Waiting to create room..."
		elif "update" in c:
			self.sd["text"]["retry"].text = "Update"
			ptext = f"There is a new version.\nPlease update the application.\nVersion: {self.sd['update']}\n\nUpdating will delete unfinished game."
		elif "Loading" in c:
			ptext = "Loading..."
		elif "version" in c:
			ptext = "Checking for new app version..."
		elif "mstock" in c:
			ptext = "Choose a card with markers to pay the cost."
		elif "LoadGame" in c:
			if "ClearLoadGame" in c:
				ptext = "Checking for new app version..."
			else:
				self.sd["text"]["retry"].text = "Continue"
				ptext = "You are part way through a game?\nDo you want to continue?"
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
					e1 = ""
					n = ""
					o = ""
					if "Opp" in status:
						e += " opponent's"
					if "Other" in status:
						o += " other "

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
						names = status.split("_")[1:-1]
						for rr in names:
							if names.index(rr) == 0:
								e += f" \"{rr}\""
							else:
								e += f" or \"{rr}\""
					elif "NameO" in status:
						names = status.split("_")[1:-1]
						n += f" with \"{names[0]}\" in its card name other than \"{names[1]}\""
					elif "Name" in status:
						n += f" with \"{status.split('_')[-2]}\" in its card name"
					elif "Text" in status:
						names = status.split("_")[1:-1]
						if len(names[0]) < 15:
							n += f" with \"{names[0].replace('] ', '')}\""
						else:
							n += f" with \"{names[0]}\""
					elif "Colour" in status:
						names = status.split("_")[1:-1]
						for rr in names:
							if names.index(rr) == 0:
								if "ColourWo" in status:
									e += f" non-{status.split('_')[-2].lower()}"
								else:
									e += f" {status.split('_')[-2].lower()}"
							else:
								if "ColourWo" in status:
									e += f" or non-{status.split('_')[-2].lower()}"
								else:
									e += f" or {status.split('_')[-2].lower()}"

					if "Stand" in status:
						e += " stand"
					elif "Reverse" in status:
						e += " reverse"
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
						if "Level<=p" in status:
							ind = self.gd["ability_trigger"].split("_")[1]
							e += f" level {len(self.pd[ind[-1]]['Level'])} or lower"
						elif "Level<=" in status:
							e += f" level {status[status.index('Level<=') + 7]} or lower"
						elif "Level>=" in status:
							e += f" level {status[status.index('Level>=') + 7]} or higher"

					if "Cost" in status:
						if "Cost<=" in status:
							e += f" cost {status[status.index('Cost<=') + 6]} or lower"
						elif "Cost>=" in status:
							e += f" cost {status[status.index('Cost>=') + 6]} or higher"
					if "Markers" in status:
						if "Markers<=0" in status:
							n += f" that has no markers"

					if "Middle" in status:
						e += ""
						n += " in the middle position of your center stage"
					elif "Center" in status:
						e += " center stage"
					elif "Back" in status:
						e += " back stage"

					if "BBattle" in status:
						n += " in battle"

					if "Osite" in status:
						ptext = f"Choose the character opposite this cards."
					elif "revive" in self.gd["effect"]:
						ptext = f"Choose {upto}{status[-1]} positions of your stage."
					elif "backatk" in self.gd["effect"]:
						ptext = f"Choose {upto}{status[-1]} of your{o}{e} characters to attack."
					elif "Climax" in status:
						ptext = f"Choose {upto}{status[-1]} climax in your{e} climax area."
					elif self.gd["thisupto"][1]:
						ptext = f"You may choose this and {upto}{int(status[-1]) - 1} of your{o}{e} characters{n}."
					else:
						if self.gd["btrait"][0]:
							ptext = f"Choose 1 of your{e} characters{n} and 1 of your{o}{e1} characters{n}."
						else:
							if "this" in self.gd["effect"] and o:
								ptext = f"Choose {upto}{status[-1]} of your{o}{e} characters{n} and this card."
							else:
								ptext = f"Choose {upto}{status[-1]} of your{o}{e} characters{n}."
				else:
					ptext = "There are no target to choose."
					self.gd["notarget"] = True
		elif "Move" in c:
			if len(self.gd["select_btns"]) > 0:
				d = ""
				e = ""
				s = ""
				oo = ""
				if "separate" in self.gd["effect"]:
					s = "separate "
				if "Opp" in self.gd["status"] and self.gd["rev"]:
					e += ""
				elif "Opp" in self.gd["status"] and "opp" in self.gd["effect"] and "oppturn" in self.gd["effect"]:
					e += ""
				elif "Opp" in self.gd["status"]:
					e += " opponent's"
				if "Center" in self.gd["status"]:
					e += " center"
				elif "Back" in self.gd["status"]:
					e += " back"
				if "Open" in self.gd["status"]:
					d = "n open"
				if "Onentsite" in self.gd["status"]:
					oo = " with a character facing this card"
				if "Clock" in self.gd["status"]:
					ptext = f"Put up to {self.gd['status'][-1]} card from the top of your clock into your waiting room"
				else:
					ptext = f"Choose a{d} {s}position in your{e} stage{oo}."
			else:
				if "Clock" in self.gd["status"]:
					ptext = "There are no cards in your clock."
				else:
					ptext = "There are no position in stage to choose."
				self.gd["notargetfield"] = True


		self.sd["text"]["label"].text = ptext
		self.sd["text"]["label"].texture_update()

		yscat += self.sd["text"]["label"].texture.size[1]
		if "choice" in c:
			yscat += self.sd["padding"] * 1 + self.sd["card"][1] / 3.
		self.sd["text"]["sct"].size = (xscat, yscat)
		self.sd["text"]["popup"].size = (xscat, yscat)


		self.sd["text"]["close"].y = self.sd["padding"] * 1.5
		self.sd["text"]["close"].center_x = xscat / 2. - self.sd["card"][0] / 4
		self.sd["text"]["label"].y = self.sd["padding"] * 3.5 + self.sd["card"][1] / 3.

		if "waiting" not in c and "making" not in c and "Loading" not in c and "version" not in c and "Clear" not in c:
			if "LoadGame" in c or "no_internet" in c or "no_error" in c or "update" in c:
				self.sd["text"]["close"].size = (self.sd["card"][0] * 2, self.sd["card"][1] / 2.)
				self.sd["text"]["retry"].size = (self.sd["card"][0] * 2, self.sd["card"][1] / 2.)
				self.sd["text"]["close"].center_x = xscat / 4 - self.sd["padding"] / 2
				self.sd["text"]["retry"].center_x = xscat / 4 * 3 - self.sd["card"][0] / 2
				self.sd["text"]["retry"].y = self.sd["padding"] * 1.5
			if c == "choice":
				self.sd["text"]["label"].y += self.sd["card"][1] / 3.
		elif "waiting" in c and "ser" not in c and self.net["game"] and all(self.gd["phase"] != phase for phase in ("Janken", "Mulligan", "")):
			self.sd["text"]["label"].y = self.sd["padding"] * 3 + self.sd["card"][1] / 3.
			self.sd["text"]["close"].text = "Show Field"
		else:
			self.sd["text"]["label"].y = self.sd["padding"] * 3
			self.sd["text"]["close"].y = -Window.height

		self.sd["text"]["label"].x = 0  

		if "Debugtext" in c or ("choice" in self.gd["effect"] and c == "Move"):
			Clock.schedule_once(self.popup_text_delay, popup_dt)
		else:
			self.sd["text"]["popup"].open()

	def popup_start(self, dt=0, o="1", c="", m="", l="", t=None):
		self.gd["popup_pop"] = True
		self.multi_info["popup"].dismiss()
		self.sd["text"]["popup"].dismiss()
		self.cardinfo.dismiss()
		self.popup_clr_button()

		if self.gd["confirm_var"]:
			self.gd["confirm_temp"] = dict(self.gd["confirm_var"])
			if "z" not in self.gd["confirm_temp"]:
				self.gd["confirm_temp"]["z"] = str(self.sd["popup"]["popup"].title)
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
				elif "z" in key:
					self.sd["popup"]["popup"].title = str(self.gd["confirm_var"][key])
			self.gd["confirm_var"] = {}

		self.gd["p_c"] = c

		if not self.gd["p_ld"]:
			if t is not None:
				self.gd["p_t"] = t
		self.gd["p_owner"] = o
		if self.gd["p_ltitle"]:
			self.sd["popup"]["popup"].title = str(self.gd["p_ltitle"])
			self.gd["p_ltitle"] = ""
		self.gd["popup_done"] = (True, False)
		self.gd["popup_on"] = True
		self.gd["chosen"] = []
		self.gd["p_select"] = []
		self.gd["p_over"] = False
		self.gd["p_f"] = True
		self.gd["p_min_s"] = -1
		self.sd["popup"]["p_scv"].bar_margin = 0

		if not m:
			if self.gd["p_c"] == "Clock" or self.gd["p_c"] == "Level":
				self.gd["p_max_s"] = 1
			elif self.gd["p_c"] == "Hand":
				self.gd["p_max_s"] = len(self.pd[self.gd["active"]]["Hand"]) - hand_limit
			else:
				self.gd["p_max_s"] = hand_limit
		elif isinstance(m, list):
			if "stack" in self.gd["p_c"] and "stacked" not in self.gd["p_c"]:
				self.gd["p_max_s"] = sorted(m, reverse=True)[0]
				self.gd["p_min_s"] = sorted(m, reverse=False)[0]
		else:
			self.gd["p_max_s"] = m

		if "Stage" in self.gd["effect"] and self.gd["p_max_s"] > 1 and "Change" not in self.gd["effect"]:
			self.gd["p_stage"] = int(self.gd["p_max_s"])
			self.gd["p_max_s"] = 1

		if not l:
			self.gd["p_look"] = 1
		else:
			self.gd["p_look"] = l

		if "Add" in self.gd["p_c"]:
			self.decks["add_chosen"] = []

		if self.gd["p_ld"]:
			self.gd["p_l"] = list(self.gd["p_t"])
			self.gd["p_t"] = []
			if "Add" not in self.gd["p_c"] and "Image" not in self.gd["p_c"]:
				self.gd["p_ld"] = []
		elif "Numbers" in self.gd["p_c"]:
			if "any" in self.gd["effect"]:
				self.gd["p_l"] = ["digit"]
			else:
				self.gd["p_l"] = [f"n{s}" for s in self.gd["effect"][1]]
		elif "Levelup" in self.gd["p_c"]:
			self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Clock"][:7])

		elif "Shuffle" in self.gd["p_c"]:
			self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Waiting"])
		elif "Counter" in self.gd["p_c"]:
			self.gd["p_l"] = list(self.gd["counter"])
		elif "Look" in self.gd["p_c"]:
			tt = False
			if "fix" in self.gd["p_c"]:
				if len(self.gd["p_l"]) > 0:
					pass
				else:
					tt = True
			elif self.gd["uptomay"]:
				if self.gd["p_t"]:
					self.gd["p_l"] = list(self.gd["p_t"])
					self.gd["p_t"] = []
				else:
					self.gd["p_l"] = []
			else:
				tt = True
			if tt:
				if "top" in self.gd["effect"]:
					self.gd["p_l"] = self.pd[self.gd["p_owner"]]["Library"][-self.gd["p_look"]:]
					self.gd["p_l"].reverse()
				elif "bottom" in self.gd["effect"]:
					self.gd["p_l"] = self.pd[self.gd["p_owner"]]["Library"][:self.gd["p_look"]]
		elif "Clock" in self.gd["p_c"] and "Discard" in self.gd["phase"]:
			self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Clock"])
		elif "Level" in self.gd["p_c"]:
			self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Level"])
		elif "Memory" in self.gd["p_c"]:
			self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Memory"])
		elif "Climax" in self.gd["p_c"]:
			self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Climax"])
		else:
			self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Hand"])

		if "Image" in self.gd["p_c"]:
			self.sd["btn"]["Addcls_btn"].y = -Window.height * 2
			self.decks["imgs"] = []
			for cc in self.decks["dbuild"]["deck"].keys():
				self.decks["imgs"].append(cc)
			self.gd["p_l"] = self.gd["p_ld"][:len(self.decks["imgs"])]
			self.decks["img_pop"] = True
			self.gd["p_l"].insert(0, "09")
			self.gd["p_l"].insert(0, "9")

		self.gd["p_width"] = self.sd["card"][0] + self.sd["padding"]  
		self.gd["p_height"] = self.sd["card"][1] + self.sd["padding"]  

		self.popup_filter()
		if self.gd["p_c"] == "Hand" or self.gd["p_c"] == "Levelup":
			self.sd["btn"][f"{self.gd['p_c']}_btn"].disabled = True

		Clock.schedule_once(self.popup_delay, popup_dt)


	def popup_pl(self, phase):
		if self.gd["btrait"][1]:
			self.gd["btrait"][4] = []
			self.gd["btrait"][5] = []
			self.gd["btrait"][3] = list(self.gd["btrait"][1])
		p_l = []
		pl = ("Search", "Salvage", "Encore", "Discard", "Markers")
		if self.gd["p_f"] and any(s in self.gd["p_c"] for s in pl):
			self.gd["p_f"] = False
			if "Markers" in self.gd["p_c"]:
				if self.gd["p_c"].split("_")[-1] in self.pd[self.gd["p_owner"]]["marker"]:
					p_l = [s[0] for s in self.pd[self.gd["p_owner"]]["marker"][self.gd["p_c"].split("_")[-1]]]
				else:
					p_l = []
			elif "Search" in self.gd["p_c"]:
				if "Reveal" in self.gd["p_c"]:
					p_l = list(self.pd[self.gd["p_owner"]]["Res"])
				elif "Stock" in self.gd["p_c"]:
					p_l = list(self.pd[self.gd["p_owner"]]["Stock"])
				else:
					p_l = list(self.pd[self.gd["p_owner"]]["Library"])
			elif "Salvage" in self.gd["p_c"]:
				if "&Hand" in self.gd["p_c"]:
					p_l = list(self.pd[self.gd["p_owner"]]["Hand"] + self.pd[self.gd["p_owner"]]["Waiting"])
				elif "Reveal" in self.gd["p_c"]:
					p_l = list(self.pd[self.gd["p_owner"]]["Res"])
				elif "Memory" in self.gd["p_c"]:
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
				elif "Climax" in self.gd["p_c"]:
					p_l = list(self.pd[self.gd["p_owner"]]["Climax"])
				elif "Level" in self.gd["p_c"]:
					p_l = list(self.pd[self.gd["p_owner"]]["Level"])
				elif "Clock" in self.gd["p_c"]:
					p_l = list(self.pd[self.gd["p_owner"]]["Clock"])
				else:
					p_l = list(self.pd[self.gd["p_owner"]]["Hand"])

			if "Face-down" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if "Climax" in self.cd[s].back]
			elif "ColourCx" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if "Climax" in self.cd[s].card and self.cd[s].mcolour.lower() in self.gd["search_type"].lower()]
			elif "CColourT" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if "Character" in self.cd[s].card and (self.cd[s].mcolour.lower() in self.gd["search_type"].split("_")[1].lower() or self.gd["search_type"].split("_")[2] in self.cd[s].trait_t)]
			elif "Colour" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if self.cd[s].mcolour.lower() in self.gd["search_type"].lower()]
			elif "ID=" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if any(name == s for name in self.gd["search_type"].split("_")[1:])]
			elif "NameO" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if self.cd[s].name_t != self.gd["search_type"].split("_")[2] and self.gd["search_type"].split("_")[1] in self.cd[s].name_t]
			elif "Name=T" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if any(name in self.cd[s].name_t for name in self.gd["search_type"].split("_")[1:-1]) or ("Character" in self.cd[s].card and self.gd["search_type"].split("_")[-1] in self.cd[s].trait_t)]
			elif "Name=" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if any(name in self.gd["search_type"].split("_")[1:] for name in self.cd[s].name_t.split("\n"))]
			elif "Card" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if self.cd[s].mcolour.lower() in self.gd["search_type"].split("_")]
			elif "TraitZ" in self.gd["search_type"]:
				if "<=" in self.gd["search_type"]:
					self.gd["p_l"] = [s for s in p_l if "Character" in self.cd[s].card and self.cd[s].level_t + self.cd[s].cost_t <= int(self.gd["search_type"][-1]) and any(trait in self.cd[s].trait_t for trait in self.gd["search_type"].split("_")[1:])]
			elif "TraitE" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if "Event" in self.cd[s].card or ("Character" in self.cd[s].card and any(trait in self.cd[s].trait_t for trait in self.gd["search_type"].split("_")[1:]))]
			elif "TraitL" in self.gd["search_type"]:
				level = self.gd["search_type"].split("_")[-1]
				if "TraitLC" in self.gd["search_type"]:
					level = self.gd["search_type"].split("_")[-2]
					cost = self.gd["search_type"].split("_")[-1]
				trait = self.gd["search_type"].split("_")[1:-1]
				if "<=p" in level:
					if "TraitLC" in self.gd["search_type"]:
						self.gd["p_l"] = [s for s in p_l if "Character" in self.cd[s].card and self.cd[s].level_t <= len(self.pd[self.gd["p_owner"]]["Level"]) and self.cd[s].cost_t <= int(cost[-1]) and any(tr in self.cd[s].trait_t for tr in trait)]
					else:
						self.gd["p_l"] = [s for s in p_l if "Character" in self.cd[s].card and self.cd[s].level_t <= len(self.pd[self.gd["p_owner"]]["Level"]) and any(tr in self.cd[s].trait_t for tr in trait)]
				elif "<=" in level:
					self.gd["p_l"] = [s for s in p_l if "Character" in self.cd[s].card and self.cd[s].level_t <= int(level[-1]) and any(tr in self.cd[s].trait_t for tr in trait)]
				elif ">=" in level:
					self.gd["p_l"] = [s for s in p_l if "Character" in self.cd[s].card and self.cd[s].level_t >= int(level[-1]) and any(tr in self.cd[s].trait_t for tr in trait)]
				elif "=" in level:
					self.gd["p_l"] = [s for s in p_l if "Character" in self.cd[s].card and self.cd[s].level_t == int(level[-1]) and any(tr in self.cd[s].trait_t for tr in trait)]
			elif "TTName" in self.gd["search_type"] or "TraitN" in self.gd["search_type"]:
				name = self.gd["search_type"].split("_")[-1]
				trait = self.gd["search_type"].split("_")[1:-1]
				self.gd["p_l"] = [s for s in p_l if "Character" in self.cd[s].card and (any(tt in self.cd[s].trait_t for tt in trait) or name in self.cd[s].name_t)]
			elif "Trait" in self.gd["search_type"]:
				if self.gd["search_type"].split("_")[1:] == [""]:
					self.gd["p_l"] = [s for s in p_l if len(self.cd[s].trait_t) <= 0 and "Character" in self.cd[s].card]
				else:
					self.gd["p_l"] = [s for s in p_l if "Character" in self.cd[s].card and any(trait in self.cd[s].trait_t for trait in self.gd["search_type"].split("_")[1:])]
			elif "NameSet" in self.gd["search_type"]:
				names = self.gd["search_type"].split("_")[1:]
				sets = names[int(len(names) / 2):]
				for setn in sets:
					if setn in names:
						names.remove(setn)
				self.gd["p_l"] = [s for s in p_l if any(name in self.cd[s].name_t and any(setid in s for setid in se["neo"]["Title"][sets[names.index(name)]]) for name in names)]
			elif "CXName" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if "Climax" in self.cd[s].card and any(name in self.cd[s].name_t for name in self.gd["search_type"].split("_")[1:])]
			elif "CName" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if "Character" in self.cd[s].card and any(name in self.cd[s].name_t for name in self.gd["search_type"].split("_")[1:])]
			elif "Name" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if any(name in self.cd[s].name_t for name in self.gd["search_type"].split("_")[1:])]
			elif "TextN" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if any(any(txt.lower() in text.lower() for txt in self.gd["search_type"].split("_")[1:-1]) for text in self.cd[s].text_o) or self.gd["search_type"].split("_")[-1] in self.cd[s].name_t]
			elif "CText" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if any(any(txt.lower() in text.lower() for txt in self.gd["search_type"].split("_")[1:]) for text in self.cd[s].text_o) and "Character" in self.cd[s].card]
			elif "Text" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if any(any(txt.lower() in text.lower() for txt in self.gd["search_type"].split("_")[1:]) for text in self.cd[s].text_o)]
			elif "CLevelC" in self.gd["search_type"]:
				cost = self.gd["search_type"].split("_")[-1]
				level = self.gd["search_type"].split("_")[:-1]
				if "<=" in level and "<=" in cost:
					self.gd["p_l"] = [s for s in p_l if "Character" in self.cd[s].card and self.cd[s].level_t <= int(level[-1]) and self.cd[s].cost_t <= int(cost[-1])]
			elif "CLevelE" in self.gd["search_type"]:
				level = self.gd["search_type"].split("_")[-1]
				if "<=" in level:
					self.gd["p_l"] = [s for s in p_l if ("Character" in self.cd[s].card and self.cd[s].level_t <= int(level[-1])) or "Event" in self.cd[s].card]
			elif "CLevelN" in self.gd["search_type"]:
				name = self.gd["search_type"].split("_")[-1]
				level = self.gd["search_type"].split("_")[1]
				if "_standby" in level:
					self.gd["p_l"] = [s for s in p_l if "Character" in self.cd[s].card and name in self.cd[s].name_t and self.cd[s].level_t <= len(self.pd[self.gd["p_owner"]]["Level"]) + 1]
				elif "<=" in level:
					self.gd["p_l"] = [s for s in p_l if "Character" in self.cd[s].card and name in self.cd[s].name_t and self.cd[s].level_t <= int(level[-1])]
			elif "Level" in self.gd["search_type"] or "CLevel" in self.gd["search_type"]:
				if "_standby" in self.gd["search_type"]:
					self.gd["p_l"] = [s for s in p_l if self.cd[s].level_t <= len(self.pd[self.gd["p_owner"]]["Level"]) + 1]
				elif "<=" in self.gd["search_type"]:
					if "<=p+" in self.gd["search_type"]:
						self.gd["p_l"] = [s for s in p_l if self.cd[s].level_t <= len(self.pd[s[-1]]["Level"]) + int(self.gd["search_type"][self.gd["search_type"].index("<=p+") + 4])]
					elif "p" in self.gd["search_type"][-1]:
						self.gd["p_l"] = [s for s in p_l if self.cd[s].level_t <= len(self.pd[s[-1]]["Level"])]
					else:
						self.gd["p_l"] = [s for s in p_l if self.cd[s].level_t <= int(self.gd["search_type"][-1])]
				elif ">=" in self.gd["search_type"]:
					self.gd["p_l"] = [s for s in p_l if self.cd[s].level_t >= int(self.gd["search_type"][-1])]
				elif "==" in self.gd["search_type"]:
					self.gd["p_l"] = [s for s in p_l if self.cd[s].level_t == int(self.gd["search_type"][-1])]

				if "CLevel" in self.gd["search_type"]:
					self.gd["p_l"] = [s for s in self.gd["p_l"] if "Character" in self.cd[s].card]
			elif "CNCost" in self.gd["search_type"]:
				nc = self.gd["search_type"].split("_")
				if "<=" in nc[2]:
					self.gd["p_l"] = [s for s in p_l if "Character" in self.cd[s].card and self.cd[s].cost_t <= int(nc[2][-1]) and nc[1] in self.cd[s].name_t]
			elif "CCost" in self.gd["search_type"]:
				cost = self.gd["search_type"]
				if "CCostT" in self.gd["search_type"]:
					cost = self.gd["search_type"].split("_")[1]

				if "<=" in self.gd["search_type"]:
					self.gd["p_l"] = [s for s in p_l if self.cd[s].cost_t <= int(cost[-1]) and "Character" in self.cd[s].card]
				elif ">=" in self.gd["search_type"]:
					self.gd["p_l"] = [s for s in p_l if self.cd[s].cost_t >= int(cost[-1]) and "Character" in self.cd[s].card]
				if "CCostT" in self.gd["search_type"] and self.gd["p_l"]:
					self.gd["p_l"] = [s for s in self.gd["p_l"] if any(trait in self.cd[s].trait_t for trait in self.gd["search_type"].split("_")[2:])]
			elif "CTrigger" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if "Character" in self.cd[s].card and any(trigger in self.cd[s].trigger for trigger in self.gd["search_type"].split("_")[1:])]
			elif "TriggerCX" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if "Climax" in self.cd[s].card and any(trigger in self.cd[s].trigger for trigger in self.gd["search_type"].split("_")[1:])]
			elif "Character" in self.gd["search_type"] or "Climax" in self.gd["search_type"] or "Event" in self.gd["search_type"]:
				self.gd["p_l"] = [s for s in p_l if self.cd[s].card in self.gd["search_type"]]
			else:
				self.gd["p_l"] = p_l

			for s in list(self.gd["p_l"]):
				if "Memory" in self.cd[s].pos_new and self.cd[s].back:
					self.gd["p_l"].remove(s)

			self.sd["btn"]["show_all_btn"].text = "Show All"

			if len(self.gd["p_l"]) <= 0:
				self.gd["notarget"] = True
				self.sd["btn"][f"{phase}_btn"].disabled = False
			else:
				self.gd["notarget"] = False
				if "Salvage" in self.gd["p_c"] and "&Hand" in self.gd["p_c"]:
					for x in range(len(self.gd["p_l"])):
						if self.cd[self.gd["p_l"][x]].pos_new != "Hand":
							self.gd["p_l"].insert(x, "tW0")
							break
					self.gd["p_l"].insert(0, "tH0")
		elif not self.gd["p_f"] and any(s in self.gd["p_c"] for s in ("Search", "Salvage", "Encore", "Discard", "Markers")):
			self.gd["p_f"] = True
			self.sd["btn"]["show_all_btn"].text = "Filter"  
			if "Markers" in self.gd["p_c"]:
				if self.gd["p_c"].split("_")[-1] in self.pd[self.gd["p_owner"]]["marker"]:
					self.gd["p_l"] = [s[0] for s in self.pd[self.gd["p_owner"]]["marker"][self.gd["p_c"].split("_")[-1]]]
				else:
					self.gd["p_l"] = []
			elif "Search" in self.gd["p_c"]:
				if "Reveal" in self.gd["p_c"]:
					self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Res"])
				elif "Stock" in self.gd["p_c"]:
					self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Stock"])
				else:
					self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Library"])
			elif "Salvage" in self.gd["p_c"]:
				if "&Hand" in self.gd["p_c"]:
					self.gd["p_l"] = ["tH0"] + list(self.pd[self.gd["p_owner"]]["Hand"]) + ["tW0"] + list(self.pd[self.gd["p_owner"]]["Waiting"])
				elif "Reveal" in self.gd["p_c"]:
					self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Res"])
				elif "Memory" in self.gd["p_c"]:
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
				elif "Climax" in self.gd["p_c"]:
					self.gd["p_l"] = list(self.pd[self.gd["p_owner"]]["Climax"])
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
			if "Numbers" not in self.gd["p_c"]:
				self.pop_btn_disable(phase)

				if "Add" in self.gd["p_c"]:
					self.filter_deck_add()
					if len(self.decks["add_chosen"]) > 0:
						self.sd["btn"]["Add_btn"].disabled = False
					else:
						self.sd["btn"]["Add_btn"].disabled = True
					self.sin = 0
					self.sd["popup"]["p_scv"].bar_margin = Window.width * 2
				else:
					self.popup_pl(phase)
		self.gd["p_rows"] = 0
		tt = 1
		tic = 7
		if starting_hand < len(self.gd["p_l"]) <= 7:
			self.gd["p_hand"] = len(self.gd["p_l"])
			if len(self.sd["popup"]["popup"].title) > ceil(tic * starting_hand):
				tt += ceil(len(self.sd["popup"]["popup"].title) / tic / len(self.gd["p_l"]))
		elif len(self.gd["p_l"]) > starting_hand:
			self.gd["p_hand"] = int(popup_max_cards)
			self.gd["p_rows"] = int(ceil(len(self.gd["p_l"]) / float(popup_max_cards)))
			if len(self.sd["popup"]["popup"].title) > ceil(tic * starting_hand):
				tt += ceil(len(self.sd["popup"]["popup"].title) / tic / popup_max_cards)
			if len(self.gd["p_l"]) > 7 and len(self.sd["popup"]["popup"].title) > ceil(tic * starting_hand) and tt > 3:
				tt -= 1
		else:
			self.gd["p_hand"] = int(starting_hand)
			if len(self.sd["popup"]["popup"].title) > ceil(tic * starting_hand):
				tt = ceil(len(self.sd["popup"]["popup"].title) / tic / starting_hand)
				if len(self.sd["popup"]["popup"].title) > ceil(tic + 2 * starting_hand):
					tt += 0.5
				if len(self.sd["popup"]["popup"].title) > ceil(tic + 1 * starting_hand):
					tt += 0.5

		if tt < 2.5:
			tt = 2.5


		if self.gd["p_rows"] > 6:
			if "Add" in self.gd["p_c"]:
				tt = 0.5
			self.sd["popup"]["p_scv"].do_scroll_y = True
			self.gd["p_yscv"] = self.gd["p_height"] * (self.gd["p_rows"] - 0.5)
			self.gd["p_yssct"] = self.gd["p_height"] * (self.gd["p_rows"] + 0)
		elif self.gd["p_rows"] > 0:
			self.gd["p_yscv"] = self.gd["p_height"] * (self.gd["p_rows"] + 0)
			self.gd["p_yssct"] = self.gd["p_height"] * (self.gd["p_rows"] + 0)
		else:
			self.gd["p_yscv"] = self.gd["p_height"] + self.sd["padding"]
			self.gd["p_yssct"] = self.gd["p_height"]

		self.gd["p_title"] = self.sd["popup"]["popup"].title_size + self.sd["popup"]["popup"].separator_height + (self.sd["card"][1] / 3 + self.sd["padding"]) * tt


		if "Add" in self.gd["p_c"]:
			self.gd["p_title"] += self.sd["card"][1] + self.sd["padding"] / 2
		elif any(s in self.gd["p_c"] for s in ("Search", "Salvage", "Encore", "Discard")) and self.gd["search_type"]:  
			self.gd["p_title"] += self.sd["card"][1] / 3 + self.sd["padding"] * 2

		self.gd["p_yscat"] = self.gd["p_yscv"] + self.gd["p_title"] + self.sd["card"][1] / 3 + self.sd["padding"] * 3  

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

			pos = (self.sd["padding"] * 0, self.sd["padding"] * 6.5 + self.sd["card"][1] / 2 + self.sd["padding"] * 1)
		elif "Look" in self.gd["p_c"] and "top" in self.gd["effect"] and ("bottom" in self.gd["effect"] or "waiting" in self.gd["effect"]):
			if "opp" in self.gd["effect"]:
				self.sd["btn"]["label"].text = "Choose where to put the top card of your opponent's deck."
			else:
				self.sd["btn"]["label"].text = "Choose where to put the top card of your deck."
			pos = (self.sd["padding"] * 1.5, self.sd["padding"] * 5.5 + self.sd["card"][1] * 2 + self.sd["padding"] * 1.5)
		elif "Look" in self.gd["p_c"] and self.gd["p_look"] >= 1 and self.gd["p_max_s"] >= 1:
			upto = ""
			if self.gd["uptomay"]:
				upto = "up to "
			fix = "up to "
			if "fix" in self.gd["effect"]:
				fix = ""
			td = "top"
			if "bottom" in self.gd["effect"]:
				td = "bottom"
			opp = ""
			if "opp" in self.gd["effect"]:
				opp = "opponets's "
			if "choosestage" in self.gd["effect"]:
				_ = self.popup_title_search(uptomay=upto)
				ss = ""
				rest = ""
				oppos = "any "
				if "restopen" in self.gd["effect"]:
					rest = " as [REST]"
					oppos = "an open "
				stage = f"put it on {oppos}position of your stage{rest}"
				if self.gd["p_max_s"] > 1:
					ss = "s"
					oppos = "open "
					stage = f"put them on separate {oppos}positions of your stage{rest}"
				self.sd["btn"]["label"].text = f"Look at up to {self.gd['p_look']} cards from {td} of your deck. Choose {upto}{self.gd['p_max_s']} {_}{ss} from among them, {stage}, and put the rest in the waiting room."
			elif "reorder" in self.gd["p_c"] and "fix" in self.gd["p_c"]:
				if "treorder" in self.gd["effect"]:
					self.sd["btn"]["label"].text = f'Put the remaining cards on the top of your {opp}deck in any order.'
				elif "breorder" in self.gd["effect"]:
					self.sd["btn"]["label"].text = f'Put the remaining cards on the bottom of your {opp}deck in any order.'
				else:
					self.sd["btn"]["label"].text = f"Look at the {td} {(self.gd['p_look'])} cards of your deck, and put them on the {td} of your deck in any order."
			elif "hand" in self.gd["effect"] or "clock" in self.gd["effect"]:
				if "show" in self.gd["effect"]:
					if "hand" in self.gd["p_c"]:
						tr = self.gd["effect"][self.gd["effect"].index("hand") + 2].split("_")
					elif "clock" in self.gd["p_c"]:
						tr = self.gd["effect"][self.gd["effect"].index("clock") + 2].split("_")

					if "Climax" in tr or "Character" in tr:
						c = tr[0]
					elif "TTName" in tr:
						c = f"character with «{tr[1]}» or «{tr[2]}» or \"{tr[3]}\""
					elif "TraitE" in tr:
						c = ""
						for _ in tr:
							if not c:
								c =f"«{_}»"
							else:
								c = f" or «{_}»"
						c += f" character or event card"
					elif "TraitN=" in tr:
						c = f"«{tr[1]}» or \"{tr[2]}\""
					elif "TraitN" in tr:
						c = f"«{tr[1]}» or \"{tr[2]}\" in its card name"
					elif "Trait" in tr:
						if len(tr) == 3:
							c = f"«{tr[1]}» or «{tr[2]}» character"
						else:
							c = f"«{tr[1]}» character"
					elif "Level" in tr[0]:
						if "<=" in tr[-1]:
							level = "lower"
						elif ">=" in tr[-1]:
							level = "higher"
						if "CLevelE" in tr:
							c = f"level {tr[-1][-1]} or {level} character or an event card"
						else:
							c = f"level {tr[-1][-1]} or {level} card"
					else:
						c = "card"

					if self.gd['p_max_s'] > 1:
						cc = "them"
						if c.endswith("card") or c.endswith("character"):
							c += "s"
					else:
						cc = "it"

					if "extrareveal" in self.gd["effect"]:
						dd = ""
					else:
						dd = f", and put {cc} in your {opp}"
						if "hand" in self.gd["p_c"]:
							dd += "hand"
						elif "clock" in self.gd["p_c"]:
							dd += "clock"
					self.sd["btn"]["label"].text = f"Look at {fix}{self.gd['p_look']} cards from {td} of your {opp}deck. Choose {upto}{self.gd['p_max_s']} {c}, reveal {cc} to your opponent{dd}, and put the rest in your {opp}waiting room."
				else:
					if "stacked" in self.gd["effect"]:
						self.sd["btn"]["label"].text = f"Choose {upto}{self.gd['p_max_s']} face down stack of cards and put them in your hand. Return the rest into your deck, and shuffle your deck."
					else:
						self.sd["btn"]["label"].text = f"Look at {fix}{self.gd['p_look']} cards from {td} of your deck. Choose {upto}{self.gd['p_max_s']} of them and put it in your hand, and put the rest in the waiting room."
			elif "waiting" in self.gd["effect"] or "bdeck" in self.gd["effect"] or "tdeck" in self.gd["effect"] or "climax" in self.gd["effect"]:
				if "all" in self.gd["effect"]:
					upto = ""
				self.sd["btn"]["label"].text = f"Look at {fix}{self.gd['p_look']} cards from {td} of your {opp}deck. Choose {upto}{self.gd['p_max_s']} of them and "
				if "waiting" in self.gd["effect"]:
					self.sd["btn"]["label"].text += f"put it in your {opp}waiting room."
				elif "tdeck" in self.gd["effect"]:
					self.sd["btn"]["label"].text += f"put it on the top of your {opp}deck."
				elif "bdeck" in self.gd["effect"]:
					self.sd["btn"]["label"].text += f"put it on the bottom your {opp}deck."
				if "treorder" in self.gd["effect"]:
					self.sd["btn"]["label"].text = f'{self.sd["btn"]["label"].text[:-1]} and put the remaining cards on the top of your {opp}deck in any order.'
				elif "breorder" in self.gd["effect"]:
					self.sd["btn"]["label"].text = f'{self.sd["btn"]["label"].text[:-1]} and put the remaining cards on the bottom of your {opp}deck in any order.'
			elif "reorder" in self.gd["p_c"]:
				if "any" in self.gd["effect"]:
					self.sd["btn"]["label"].text = f"Look at up to {self.gd['p_look']} cards from {td} of your deck, and choose {upto}{self.gd['p_max_s']} of those cards and put them on the {tt} of your deck in any order."
				else:
					self.sd["btn"]["label"].text = f"Look at up to {self.gd['p_look']} cards from {td} of your deck, and put them on the {td} of your deck in any order."
				if "waity" in self.gd["effect"]:
					self.sd["btn"]["label"].text = f'{self.sd["btn"]["label"].text[:-1]} and put the remaining cards in the waiting room.'
			elif "stack" in self.gd["p_c"]:
				self.sd["btn"]["label"].text = f"Choose {self.gd['p_min_s']} or {self.gd['p_max_s']} cards to add into the first stacks of cards. The rest will make the other stack of cards."
			elif "look" in self.gd["p_c"]:
				self.sd["btn"]["label"].text = f"Look at up to {self.gd['p_look']} cards from {td} of your deck, and put them back in the same order."
			else:
				self.sd["btn"]["label"].text = f"Look at up to {self.gd['p_look']} cards from {td} of your deck. Choose {upto}{self.gd['p_max_s']} of them and put it on top of the deck, and put the rest in the waiting room."
			if "fix" in self.gd["p_c"] and ("top" in self.gd["effect"] or "stack" in self.gd["effect"] or "stacked" in self.gd["effect"]) and self.gd["p_look"] >= 1 and self.gd["p_max_s"] > 0:
				pos = (self.sd["padding"] * 0.5, self.sd["padding"] * 2 + self.sd["card"][1] * 2)
				self.gd["p_yscat"] -= self.sd["card"][1] / 2.
			else:
				pos = (self.sd["padding"] * 0.5, self.sd["padding"] * 7 + self.sd["card"][1] * 2)

		if self.sd["btn"]["label"].text != "":
			self.sd["btn"]["label"].text_size = (self.gd["p_xscat"] * 0.9, None)
			self.sd["btn"]["label"].texture_update()
			self.sd["btn"]["label"].size = self.sd["btn"]["label"].texture.size
			self.sd["btn"]["label"].pos = pos

			if not self.gd["notarget"]:
				self.gd["p_yscat"] += self.sd["padding"] * 2 + self.sd["card"][1] / 2. + self.sd["btn"]["label"].size[1]
		else:
			self.sd["btn"]["label"].x = -Window.width

		if "Image" in self.gd["p_c"]:
			self.gd["p_ypop"] = self.gd["p_title"] + self.gd["p_yscv"]
		else:
			self.gd["p_ypop"] = self.gd["p_yscat"]

		if self.gd["p_ypop"] > Window.height or ("Add" in self.gd["p_c"] and self.gd["p_rows"] > 6):
			self.gd["p_over"] = True
			self.gd["p_ypop"] = Window.height * 0.9
			self.gd["p_yscat"] = self.gd["p_ypop"] - self.gd["p_title"]
			self.gd["p_yscv"] = self.gd["p_yscat"] - self.sd["card"][1] * 0.75  
			if "Add" in self.gd["p_c"]:
				r = (self.gd["p_yscv"] - self.sd["card"][1]) % self.gd["p_height"] / self.gd["p_height"]
				if r > 0.25:
					r = 0.25
					self.sd["p_over"] = r
				self.gd["p_rows"] = int(self.gd["p_yscv"] / self.gd["p_height"]) + r
				self.gd["p_yscv"] -= self.sd["card"][1] - self.gd["p_height"] * r

		self.sd["popup"]["p_scv"].size = (self.gd["p_xscat"], self.gd["p_yscv"])
		self.sd["popup"]["popup"].size = (self.gd["p_xscat"], self.gd["p_ypop"])

		if "sspace" in self.gd["p_l"]:
			self.gd["p_l"].remove("sspace")

		if "Add" in self.gd["p_c"]:
			nx, ns = (0, 0)
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
		c9 = 0
		self.sim = 0
		for inx in range(len(self.gd["p_l"])):
			ind = self.gd["p_l"][inx]
			if ind.endswith("9"):
				c9 += 1
			if "sspace" in ind:
				try:
					self.sd["popup"]["stack"].add_widget(self.sd["popup"][ind])
				except WidgetException:
					pass
				c += 1
			elif "digit" in ind:
				c += 1
				continue
			else:
				if c:
					inx -= 1
				if c9:
					inx -= c9
				self.sim += 1
				if "Numbers" not in self.gd["p_c"]:
					if "Add" in self.gd["p_c"]:
						self.cpop[ind].import_data(sc[self.gd["p_fcards"][inx]],self.gd["DLimg"])

						if self.gd["p_fcards"][inx] in self.decks["add_chosen"]:
							self.cpop[ind].selected_c()
						else:
							self.cpop[ind].selected_c(False)
					elif "Image" in self.gd["p_c"]:
						if ind.endswith("9"):
							if ind == "09":
								self.cpop[ind].import_data("back",self.gd["DLimg"])
							else:
								self.cpop[ind].import_data("empty",self.gd["DLimg"])
						else:
							self.cpop[ind].import_data(sc[self.decks["imgs"][inx]],self.gd["DLimg"])

						self.cpop[ind].selected_c(False)
					else:
						if "Stage" in self.gd["effect"] and ind in self.gd["target"]:
							self.cpop[ind].stage_slc()
							for r in range(select2cards):
								self.field_btn[f"stage{r}{ind[-1]}s"].pos = (self.mat[ind[-1]]["field"][self.gd["target"][self.gd["target"].index(ind) + 1]][0] - self.sd["padding"], self.mat[ind[-1]]["field"][self.gd["target"][self.gd["target"].index(ind) + 1]][1] - self.sd["padding"])
						else:
							self.cpop[ind].selected_c(False)

					if "_look" in self.gd["p_c"]:
						if inx == 0:
							self.cpop[ind].update_text("Top", .45)
						elif (inx + 1) % 10 == 1:
							self.cpop[ind].update_text(f"{inx + 1}st", .45)
						elif (inx + 1) % 10 == 2:
							self.cpop[ind].update_text(f"{inx + 1}nd", .45)
						elif (inx + 1) % 10 == 3:
							self.cpop[ind].update_text(f"{inx + 1}rd", .45)
						else:
							self.cpop[ind].update_text(f"{inx + 1}th", .45)
					else:
						if "tH" in ind:
							self.cpop[ind].update_text("Hand", .35)
						elif "tW" in ind:
							self.cpop[ind].update_text("Waiting Room", .25)
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
					try:
						self.sd["popup"]["stack"].add_widget(self.cpop[ind])
					except WidgetException:
						pass

				if "Image" not in self.gd["p_c"] and "Add" not in self.gd["p_c"] and not ind.startswith("n") and not ind.startswith("t"):
					if self.cpop[ind].level_t != self.cd[ind].level_t:
						self.cpop[ind].level_c = self.cd[ind].level_c
						self.cpop[ind].update_level()
					if self.cpop[ind].cost_t != self.cd[ind].cost_t:
						self.cpop[ind].cost_c = self.cd[ind].cost_c
						self.cpop[ind].update_cost()

		if "Image" not in self.gd["p_c"]:
			self.sd["popup"]["digit"].y = -Window.height * 2
			self.sd["popup"]["p_scv"].y = self.sd["padding"] * 3 + self.sd["card"][1] / 2
			if "Look" in self.gd["p_c"] and "top" in self.gd["effect"] and "fix" not in self.gd["p_c"]:
				self.sd["popup"]["p_scv"].y += self.sd["padding"] * 1.5 + self.sd["btn"]["top_btn"].size[1]

			if self.gd["ability_trigger"]:
				self.sd["btn"]["show_info_btn"].size = (self.sd["card"][1] / 2, self.sd["card"][1] / 4.5)
				self.sd["btn"]["show_info_btn"].y = self.gd["p_ypop"] - self.sd["btn"]["show_info_btn"].size[1] * 2 - self.sd["padding"]
				self.sd["btn"]["show_info_btn"].x = self.gd["p_xscat"] - self.sd["btn"]["show_info_btn"].size[0] * 2 + self.sd["padding"] * 1.5
				self.sd["btn"]["show_info_btn"].font_size = self.sd["btn"]["show_info_btn"].size[1] * 0.85
			if any(item in self.gd["p_c"] for item in ("Search", "Salvage", "Encore", "Discard")) and self.gd["search_type"]:  
				self.sd["btn"]["show_all_btn"].size = (self.sd["card"][0] * 2, self.sd["card"][1] / 3.)
				self.sd["btn"]["show_all_btn"].y = self.sd["popup"]["p_scv"].y + self.sd["popup"]["p_scv"].size[1] + self.sd["padding"]
				self.sd["btn"]["show_all_btn"].center_x = self.gd["p_xscat"] / 2 - self.sd["card"][0] / 4  
		else:
			self.sd["popup"]["p_scv"].y = self.sd["padding"] * 1.5
			self.sd["btn"]["filter_add"].y = -Window.height * 2
			self.sd["btn"]["Add_btn"].y = -Window.height * 2

		self.sd["popup"]["p_scv"].scroll_y = 1

		if "Image" not in self.gd["p_c"]:
			if "Numbers" not in self.gd["p_c"]:
				self.sd["btn"][f"{phase}_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
				self.sd["btn"][f"{phase}_btn"].y = self.sd["padding"] * 1.5

				if "bdeck" in self.gd["effect"] and any(_ in self.gd["effect"] for _ in ("treorder", "breorder")):
					self.sd["btn"]["Look_btn"].text = "Continue Effect"
				elif phase in phases:
					self.sd["btn"][f"{phase}_btn"].text = f"End {phase}"
				elif phase != "Hand":
					self.sd["btn"][f"{phase}_btn"].text = "End Effect"  

				if self.gd["p_c"] == "Add":
					self.sd["btn"]["filter_add"].y = self.gd["p_yscv"] + self.sd["padding"] * 2 + self.sd["popup"]["p_scv"].y
					if len(self.gd["p_l"]) > 1:
						self.sd["btn"][f"{phase}_btn"].text = f"Add cards"
					else:
						self.sd["btn"][f"{phase}_btn"].text = f"Add card"
					self.sd["btn"][f"{phase}_btn"].center_x = self.gd["p_xscat"] / 4 * 3 - self.sd["card"][0] / 2  
					self.sd["btn"][f"{phase}cls_btn"].center_x = self.gd["p_xscat"] / 4 - self.sd["padding"] / 2  
					self.sd["btn"][f"{phase}cls_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
					self.sd["btn"][f"{phase}cls_btn"].y = self.sd["padding"] * 1.5
				else:
					self.sd["btn"][f"{phase}_btn"].center_x = self.gd["p_xscat"] / 4. * 3 - self.sd["card"][0] / 2

			if any(_ in self.gd["p_c"] for _ in ("Clock", "Level", "Hand", "Search", "Salvage", "Counter", "Encore", "Discard", "Marker")):
				self.sd["btn"]["field_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
				self.sd["btn"]["field_btn"].y = self.sd["padding"] * 1.5
				self.sd["btn"]["field_btn"].center_x = self.gd["p_xscat"] / 4. - self.sd["padding"] / 2  
			elif self.gd["p_c"] == "Mulligan":
				self.sd["btn"][f"{phase}_btn"].text = f"End {phase}"
				self.sd["btn"]["M_all_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
				self.sd["btn"]["M_all_btn"].y = self.sd["padding"] * 1.5
				self.sd["btn"]["M_all_btn"].center_x = self.gd["p_xscat"] / 4. - self.sd["padding"] / 2
			elif "Look" in self.gd["p_c"]:
				self.sd["btn"]["field_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
				self.sd["btn"]["field_btn"].y = self.sd["padding"] * 1.5
				self.sd["btn"]["field_btn"].center_x = self.gd["p_xscat"] / 4. - self.sd["padding"] / 2  
				if "top" in self.gd["effect"] and ("bottom" in self.gd["effect"] or "waiting" in self.gd["effect"]):  
					self.sd["btn"][f"{self.gd['p_c']}_btn"].y = -Window.height
					self.sd["btn"]["field_btn"].center_x = self.gd["p_xscat"] / 2. - self.sd["card"][0] / 4  
					self.sd["btn"]["top_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
					self.sd["btn"]["top_btn"].center_x = self.gd["p_xscat"] / 4. - self.sd["padding"] / 2  
					self.sd["btn"]["top_btn"].y = self.sd["padding"] * 3 + self.sd["card"][1] / 2.
					self.sd["btn"]["top_btn"].text = "Top deck"
					if "bottom" in self.gd["effect"]:
						self.sd["btn"]["bottom_btn"].text = "Bottom deck"
					elif "waiting" in self.gd["effect"]:
						self.sd["btn"]["bottom_btn"].text = "Waiting room"
					self.sd["btn"]["bottom_btn"].size = self.sd["btn"]["top_btn"].size
					self.sd["btn"]["bottom_btn"].center_x = self.gd["p_xscat"] / 4. * 3 - self.sd["card"][0] / 2  
					self.sd["btn"]["bottom_btn"].y = self.sd["btn"]["top_btn"].y
					self.sd["popup"]["p_scv"].y = self.sd["padding"] * 3.5 + self.sd["btn"]["top_btn"].size[1] * 2
					self.gd["p_c"] += "_auto"
				elif ("top" in self.gd["effect"] or "bottom" in self.gd["effect"]) and "look" in self.gd["effect"]:
					self.sd["btn"][f"{phase}_btn"].y = -Window.height
					self.sd["btn"]["top_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
					self.sd["btn"]["top_btn"].center_x = self.gd["p_xscat"] * 3 / 4. - self.sd["card"][0] / 2  
					self.sd["btn"]["top_btn"].y = self.sd["padding"] * 1.5
					self.sd["btn"]["top_btn"].text = "End Effect"
					self.sd["btn"]["draw_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
					self.sd["btn"]["draw_btn"].center_x = self.gd["p_xscat"] / 2. - self.sd["card"][0] / 4  
					self.sd["btn"]["draw_btn"].y = self.sd["padding"] * 3 + self.sd["card"][1] / 2.
					self.sd["popup"]["p_scv"].y = self.sd["padding"] * 3.5 + self.sd["btn"]["top_btn"].size[1] * 2
				elif ("top" in self.gd["effect"] or "bottom" in self.gd["effect"]) and self.gd["p_look"] >= 1 and self.gd["p_max_s"] > 0 and "fix" not in self.gd["p_c"]:
					self.sd["btn"]["draw_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
					self.sd["btn"]["draw_btn"].center_x = self.gd["p_xscat"] / 2. - self.sd["card"][0] / 4  
					self.sd["btn"]["draw_btn"].y = self.sd["padding"] * 3 + self.sd["card"][1] / 2.
					self.sd["popup"]["p_scv"].y = self.sd["padding"] * 3.5 + self.sd["btn"]["draw_btn"].size[1] * 2
				elif "check" in self.gd["effect"]:
					self.sd["btn"]["check_btn"].center_x = self.gd["p_xscat"] / 2. - self.sd["card"][0] / 4  
					self.sd["btn"]["check_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
					self.sd["btn"]["check_btn"].y = self.sd["padding"] * 1.5
					self.sd["btn"][f"{phase}_btn"].y = -Window.height
					self.sd["btn"]["field_btn"].y = -Window.height
			elif "Numbers" in self.gd["p_c"]:
				self.sd["btn"]["field_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
				self.sd["btn"]["field_btn"].y = self.sd["padding"] * 1.5
				self.sd["btn"]["field_btn"].center_x = self.gd["p_xscat"] / 2 - self.sd["card"][0] / 4  
				if "any" in self.gd["effect"]:
					self.sd["popup"]["p_scv"].y = -Window.height * 2
					self.sd["btn"]["declare_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
					self.sd["btn"]["declare_btn"].center_x = self.gd["p_xscat"] / 4 * 3 - self.sd["card"][0] / 2  
					self.sd["btn"]["declare_btn"].y = self.sd["padding"] * 1.5
					self.sd["btn"]["field_btn"].center_x = self.gd["p_xscat"] / 4 - self.sd["card"][0] / 4  
					self.sd["popup"]["digit"].size = (self.sd["card"][0] * starting_hand, self.sd["card"][1])
					self.sd["popup"]["digit"].y = self.sd["padding"] * 4.5 + self.sd["card"][1] / 2.
					self.sd["popup"]["digit"].center_x = self.gd["p_xscat"] / 2 - self.sd["card"][0] / 4  

	def popup_slc_move(self, ind):
		if self.gd["p_max_s"] > 0:
			self.cpop[ind].selected_c()
			self.gd["chosen"].append(ind)

			if len(self.gd["chosen"]) > self.gd["p_max_s"] and ind not in self.gd["p_select"]:
				temp = self.gd["p_select"].pop(0)
				self.gd["chosen"].remove(temp)
				self.cpop[temp].selected_c(False)

			self.gd["p_select"].append(ind)
			if "stacked" not in self.gd["p_c"]:
				self.update_text_selected()

	def update_text_selected(self):
		for i in range(len(self.gd["p_l"])):
			if self.gd["p_l"][i] not in self.skip_cpop:
				self.cpop[self.gd["p_l"][i]].update_text()

		for i in range(len(self.gd["chosen"])):
			if ("Look" in self.gd["p_c"] and "reorder" in self.gd["p_c"]) or ("Discard" in self.gd["p_c"] and "Library" in self.gd["effect"]):
				if i == 0 and "breorder" not in self.gd["effect"]:
					self.cpop[self.gd["chosen"][i]].update_text("Top", .45)
				elif (i + 1) % 10 == 1:
					self.cpop[self.gd["chosen"][i]].update_text(f"{i + 1}st", .45)
				elif (i + 1) % 10 == 2:
					self.cpop[self.gd["chosen"][i]].update_text(f"{i + 1}nd", .45)
				elif (i + 1) % 10 == 3:
					self.cpop[self.gd["chosen"][i]].update_text(f"{i + 1}rd", .45)
				else:
					self.cpop[self.gd["chosen"][i]].update_text(f"{i + 1}th", .45)
				if "breorder" in self.gd["effect"]:
					self.cpop[self.gd["chosen"][-1]].update_text("Bottom", .30)
			else:
				self.cpop[self.gd["chosen"][i]].update_text(i + 1)

	def popup_clr_button(self):
		for btn in self.sd["btn"].keys():
			if btn.startswith("a"):
				continue
			elif "filter_add" in btn:
				continue
			self.sd["btn"][btn].y = -Window.height * 2
		self.sd["popup"]["digit"].y = -Window.height * 2
		for nx in self.iach:
			self.iach[nx].y = -Window.height * 2
		self.sd["btn"]["label"].x = -Window.width * 2
		self.sd["popup"]["sutext"].y = -Window.height * 2
		self.sd["cpop_press"] = []

		if self.infob:
			self.infob.cancel()
			self.infob = None
		if self.infot:
			self.infot.cancel()
			self.infot = None
		self.shelve_save()

	def popup_clr(self, *args):
		self.gd["popup_done"] = (False, True)
		self.gd["popup_pop"] = False
		self.gd["popup_on"] = False
		self.gd["uptomay"] = False
		self.gd["chosen"] = []
		self.gd["p_ltitle"] = ""
		self.gd["p_c"] = ""
		self.gd["p_t"] = []
		self.sd["popup"]["stack"].clear_widgets()
		self.sd["popup"]["p_scv"].x = 0

		if not self.decks["dbuilding"]:
			self.popup_clr_button()

			if self.gd["phase"] == "Main" and self.gd["active"] == "1" and "ACT" in self.gd["ability_trigger"]:
				self.act_ability_show(hide=True)
				self.sd["btn"]["end"].y = -Window.height
				self.sd["btn"]["end_attack"].y = -Window.height
				self.sd["btn"]["end_phase"].y = -Window.height
			elif any(self.gd["phase"] == phase for phase in ("Main", "Attack", "Declaration", "Climax", "Encore")):
				if "Main" in self.gd["phase"]:
					self.sd["btn"]["end"].text = "Climax Phase"  
				else:
					self.sd["btn"]["end"].text = f"End {self.gd['phase']}"
				if self.gd["active"] == "1":
					if len(self.gd["select_btns"]) > 0 or len(self.gd["stack"]["1"]) > 0:
						self.act_ability_show(hide=True)
					else:
						self.act_ability_show()

	def card_btn_release(self, btn):
		self.sd["cpop_slc"] = ""

	def card_btn_press(self, btn):
		if self.multi_info["t"]:
			if self.cpop[btn.cid].img_file != "add":
				self.cardinfo.import_data(self.cpop[btn.cid], annex_img,self.gd["DLimg"])
		elif self.decks["dbuilding"]:
			if self.decks["img_pop"]:
				self.decks["img_pop"] = False
				self.decks["dbuild"]["img"] = str(self.cpop[btn.cid].img_file)
				if self.decks['dbuild']['img'] in other_img:
					self.decks["st"]["image_btn"].source = f"atlas://{img_in}/other/{self.decks['dbuild']['img']}"
				elif self.decks['dbuild']['img'] in annex_img and self.gd["DLimg"]:
					self.decks["st"]["image_btn"].source = f"atlas://{img_in}/annex/{self.decks['dbuild']['img']}"
				else:
					if self.gd["DLimg"] and (exists(f"{cache}/{self.decks['dbuild']['img']}")):
						self.decks["st"]["image_btn"].source = f"{cache}/{self.decks['dbuild']['img']}"
					else:
						self.decks["st"]["image_btn"].source = f"atlas://{img_in}/other/grey"

				if f"id{self.decks['dbuilding']}" in self.dpop:
					self.dpop[f"id{self.decks['dbuilding']}"].source = str(self.decks["st"]["image_btn"].source)

				self.popup_clr()
				self.sd["popup"]["popup"].dismiss()
			elif not self.gd["popup_pop"]:
				if not self.cd[btn.cid].back:
					self.cardinfo.import_data(self.cd[btn.cid], annex_img,self.gd["DLimg"])
			else:
				ind = self.cpop[btn.cid].cid
				self.sd["cpop_slc"] = ind
				self.sd["cpop_press"].append(ind)
				if len(self.sd["cpop_press"]) >= info_popup_press:
					if all(prs == self.sd["cpop_press"][-1] for prs in self.sd["cpop_press"][-info_popup_press:]):
						self.cd["00"].import_data(sc[self.sd["cpop_press"][-1]],self.gd["DLimg"])
						self.sd["cpop_press"] = []
						if self.check_back_hidden(self.cd["00"]):
							self.cardinfo.import_data(self.cd["00"], annex_img,self.gd["DLimg"])
				else:
					self.sd["cpop_pressing"] = Clock.schedule_once(self.card_btn_info, info_popup_dt)
				if ind not in self.decks["add_chosen"]:
					self.decks["add_chosen"].append(ind)
					self.cpop[btn.cid].selected_c()
					self.sd["btn"]["Add_btn"].disabled = False
				elif ind in self.decks["add_chosen"]:
					self.decks["add_chosen"].remove(ind)
					self.cpop[btn.cid].selected_c(False)
					if len(self.decks["add_chosen"]) == 0:
						self.sd["btn"]["Add_btn"].disabled = True
		else:
			if not self.multi_info["t"]:
				if "_" in self.gd["p_c"]:
					phase = self.gd["p_c"].split("_")[0]
				else:
					phase = self.gd["p_c"]

				if "auto" in self.gd["p_c"]:
					if "stock" not in self.gd["p_c"] and not self.cd[btn.cid].back:
						try:
							if btn.cid != "1" or btn.cid != "2":
								if self.check_back_hidden(self.cd[btn.cid]):
									self.cardinfo.import_data(self.cd[btn.cid], annex_img,self.gd["DLimg"])
						except KeyError:
							if self.cpop[btn.cid].cid != "player":
								if self.check_back_hidden(self.cd[btn.cid]):
									self.cardinfo.import_data(self.cpop[btn.cid], annex_img,self.gd["DLimg"])
				else:
					self.sd["cpop_slc"] = btn.cid
					self.sd["cpop_press"].append(btn.cid)
					if len(self.sd["cpop_press"]) >= info_popup_press:
						if all(prs == btn.cid for prs in self.sd["cpop_press"][-info_popup_press:]):
							self.sd["cpop_press"] = []
							self.gd["selected"] = ""
							if self.check_back_hidden(self.cd[btn.cid]):
								self.cardinfo.import_data(self.cpop[btn.cid], annex_img,self.gd["DLimg"])
					else:
						self.sd["cpop_pressing"] = Clock.schedule_once(self.card_btn_info, info_popup_dt)

					if (any(s in self.gd["p_c"] for s in ("Salvage", "Search", "Encore", "Discard")) or ("Look" in self.gd["p_c"] and any(_ in self.gd["effect"] for _ in ("hand", "clock", "choosestage")))) and btn.cid not in self.gd["chosen"]:
						if self.select_filter_check(btn.cid):
							self.popup_slc_move(btn.cid)
					elif btn.cid not in self.gd["chosen"]:
						self.popup_slc_move(btn.cid)
					else:
						self.cpop[btn.cid].selected_c(False)
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
								if len(self.gd["chosen"]) == 0 and self.gd["btrait"][5]:
									self.gd["btrait"][5] = []
									self.gd["btrait"][3] = list(self.gd["btrait"][1])
						if btn.cid in self.gd["p_select"]:
							self.gd["p_select"].remove(btn.cid)

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
						elif "revive" in self.gd["p_c"]:
							self.sd["btn"]["revive_btn"].text = f"Choose selected {word}"
						elif any(s in self.gd["p_c"] for s in ("Clock", "Search", "Salvage", "Discard")):
							if "Stage" in self.gd["effect"] or "Library" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = "Continue Effect"
							elif "Memory" in self.gd["effect"] or "hmemory" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = "Put into Memory"
							elif "Stock" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = "Put into Stock"
							elif "Clock" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = "Put into Clock"
							elif "Reveal" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = f"Select {word}"
							elif "Change" in self.gd["p_c"]:
								self.sd["btn"][f"{phase}_btn"].text = "Continue Effect"
							elif "swap" in self.gd["effect"] or "swap" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = f"Select card"
							elif "flip" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = f"Flip card"
							elif "csalvage" in self.gd["effect"] or "wdecker" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = f"Return {word}"
							elif "cdiscard" in self.gd["effect"]:
								if "Level" in self.gd["effect"]:
									self.sd["btn"][f"{phase}_btn"].text = "Put into Level"
								else:
									self.sd["btn"][f"{phase}_btn"].text = "Put into Waiting"
							elif "cxdiscard" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = f"Select {word}"  
							elif "msalvage" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = f"Confirm {word}"
							elif "invert" in self.gd["effect"] or "Zwei" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = f"Select {word}"
							elif "choice" in self.gd["effect"] and "salvage" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = "Continue"
							elif "Reveal" in self.gd["p_c"]:
								self.sd["btn"][f"{phase}_btn"].text = f"Select {word}"
							elif "Discard" in self.gd["p_c"] and "opp" in self.gd["effect"] and "Climax" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = "Select climax"
							elif "marker" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = f"Select {word}"
							else:
								self.sd["btn"][f"{phase}_btn"].text = f"Select {word}"  
						elif "Counter" in self.gd["p_c"]:
							self.sd["btn"]["Counter_btn"].text = f"Select {word}"  
						elif "Shuffle" in self.gd["p_c"]:
							self.sd["btn"]["Shuffle_btn"].text = f"Shuffle {word}"
						elif "Look" in self.gd["p_c"]:
							if "hand" in self.gd["p_c"]:
								if "stacked" in self.gd["p_c"]:
									self.sd["btn"]["Look_btn"].text = "Choose stack"
								else:
									self.sd["btn"]["Look_btn"].text = f"Choose {word}"
							elif "clock" in self.gd["p_c"]:
								self.sd["btn"]["Look_btn"].text = "Put to Clock"
							elif "stack" in self.gd["p_c"] and "stacked" not in self.gd["p_c"]:
								self.sd["btn"]["Look_btn"].text = "Create Stack"
							elif "waiting" in self.gd["p_c"] and "reorder" in self.gd["effect"]:
								self.sd["btn"]["Look_btn"].text = "Continue Effect"
							else:
								self.sd["btn"]["Look_btn"].text = f"Choose {word}"
						elif "Stage" in self.gd["effect"]:
							self.sd["btn"][f"{phase}_btn"].text = f"Play {word}"  
						elif "encore" not in phase:
							if self.gd["resonance"][0]:
								self.sd["btn"][f"{phase}_btn"].text = "Reveal selected"
							elif "swap" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = f"Select {word}"
							elif "Level" in self.gd["effect"]:
								self.sd["btn"][f"{phase}_btn"].text = "Put to Level"
							else:
								self.sd["btn"][f"{phase}_btn"].text = f"Select {word}"  
					else:
						if "_" in self.gd["p_c"]:
							self.sd["btn"][f"{phase}_btn"].text = "End Effect"
						if "Stage" in self.gd["effect"]:
							self.sd["btn"][f"{phase}_btn"].text = "End Effect"
						elif "Counter" in self.gd["p_c"]:
							self.sd["btn"][f"{phase}_btn"].text = "End Counter"
						elif "Mulligan" in self.gd["p_c"]:
							self.sd["btn"]["Mulligan_btn"].text = "End Mulligan"
						elif phase in phases:
							self.sd["btn"][f"{phase}_btn"].text = f"End {phase}"
						elif "breorder" in self.gd["effect"] or "treorder" in self.gd["effect"]:
							self.sd["btn"]["Look_btn"].text = "Continue Effect"
						else:
							self.sd["btn"][f"{phase}_btn"].text = "End Effect"

					if "encore" not in phase:
						self.pop_btn_disable(phase)

	def check_back_hidden(self, card):
		if card.back and "Add" not in self.gd["p_c"]:
			if card.ind[-1] != "1":
				return False
			elif card.ind[-1] == "1" and not card.back_info:
				return False
		return True

	def card_btn_info(self, *args):
		if self.sd["cpop_slc"] != "":
			self.sd["cpop_press"] = []
			if self.decks["dbuilding"]:
				self.cd["00"].import_data(sc[self.sd["cpop_slc"]],self.gd["DLimg"])
				self.cardinfo.import_data(self.cd["00"], annex_img,self.gd["DLimg"])
			else:
				if self.check_back_hidden(self.cd[self.sd["cpop_slc"]]):
					self.cardinfo.import_data(self.cd[self.sd["cpop_slc"]], annex_img,self.gd["DLimg"])
		else:
			if self.sd["cpop_pressing"] is not None:
				self.sd["cpop_pressing"].cancel()
				self.sd["cpop_pressing"] = None

	def show_info_btn(self, btn):
		self.gd["moving"] = False
		self.gd["btn_release"] = False
		self.gd["selected"] = ""
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
			cmax = list(self.gd["p_l"])
			if "sspace" in cmax:
				cmax.remove("sspace")

			if len(cmax) < self.gd["p_max_s"]:
				if "hand" in self.gd["effect"] and "upto" in self.gd["effect"]:
					self.sd["btn"][f"{phase}_btn"].disabled = False
				elif len(self.gd["chosen"]) < len(cmax):
					self.sd["btn"][f"{phase}_btn"].disabled = True
				else:
					self.sd["btn"][f"{phase}_btn"].disabled = False
			else:
				if "hand" in self.gd["effect"] and "upto" in self.gd["effect"]:
					self.sd["btn"][f"{phase}_btn"].disabled = False
				else:
					self.sd["btn"][f"{phase}_btn"].disabled = True
		elif len(self.gd["chosen"]) < self.gd["p_max_s"] and not self.gd["uptomay"]:
			if self.gd["btrait"][1]:
				cmax = list(self.gd["p_l"])
				if self.gd["btrait"][4]:
					for ind in self.gd["btrait"][4]:
						if ind in cmax:
							cmax.remove(ind)
				if len([s for s in cmax if any("N/" not in tr and tr in self.cd[s].trait_t for tr in self.gd["btrait"][3])]) > 0:
					self.sd["btn"][f"{phase}_btn"].disabled = True
				else:
					self.sd["btn"][f"{phase}_btn"].disabled = False
			else:
				self.sd["btn"][f"{phase}_btn"].disabled = True
		elif len(self.gd["chosen"]) < self.gd["p_max_s"] and self.gd["uptomay"] and "all" in self.gd["effect"]:
			cmax = list(self.gd["p_l"])
			if "sspace" in cmax:
				cmax.remove("sspace")

			if len(cmax) < self.gd["p_max_s"]:
				if len(self.gd["chosen"]) < len(cmax):
					self.sd["btn"][f"{phase}_btn"].disabled = True
				else:
					self.sd["btn"][f"{phase}_btn"].disabled = False
			else:
				self.sd["btn"][f"{phase}_btn"].disabled = True
		elif "reorder" in self.gd["p_c"]:
			cmax = len(self.gd["p_l"])
			if "sspace" in self.gd["p_l"]:
				cmax -= 1
			if "any" in self.gd["effect"]:
				self.sd["btn"][f"{phase}_btn"].disabled = False
			elif len(self.gd["chosen"]) < cmax:
				self.sd["btn"][f"{phase}_btn"].disabled = True
			elif len(self.gd["chosen"]) >= cmax:
				self.sd["btn"][f"{phase}_btn"].disabled = False
		else:
			if phase:
				self.sd["btn"][f"{phase}_btn"].disabled = False
			else:
				self.sd["btn"][f"Mulligan_btn"].disabled = False

	def selected_card(self, *args):
		if "Clock" in self.gd["status"] and "Clock" in self.gd["btn_id"] and self.gd["btn_id"] in self.gd["select_btns"]:
			if not self.gd["move"]:
				self.gd["move"] = "clock"
				self.move_field_btn(self.gd["phase"])
				return True
		elif ("Center" in self.gd["btn_id"] or "Back" in self.gd["btn_id"] or "Climax" in self.gd["btn_id"]) and self.gd["btn_id"] in self.gd["select_btns"]:
			if not self.gd["payed"] and self.gd["pay"]:
				if self.gd["mstock"][0]:
					status = str(self.gd["mstock"][1])
				else:
					status = self.gd["pay_status"]
			else:
				status = self.gd["status"]

			if (self.gd["choose"] or self.gd["revive"]) and not self.gd["move"]:
				self.gd["move"] = self.gd["btn_id"][:-1]
			else:
				if "Climax" in self.gd["btn_id"]:
					ind = self.pd[self.gd["btn_id"][-1]][self.gd["btn_id"][:-1]][0]
				else:
					ind = self.pd[self.gd["btn_id"][-1]][self.gd["btn_id"][:-2]][int(self.gd["btn_id"][-2])]
				if ind not in self.gd["chosen"]:
					self.gd["chosen"].append(ind)
					if len(self.gd["chosen"]) > 1:
						if self.gd["btrait"][0]:
							tr = [[], []]
							for sx in self.gd["chosen"]:
								for inx in range(len(self.gd["btrait"][1])):
									if self.gd["btrait"][1][inx] in self.cd[sx].trait_t:
										tr[inx].append(sx)
							if (len(tr[0]) >= 2 and len(tr[1]) < 1) or (len(tr[0]) < 1 and len(tr[1]) >= 2):
								temp = self.gd["chosen"].pop(0)
								self.cd[temp].update_text()
						elif self.gd["thisupto"][0]:
							idm = self.gd["ability_trigger"].split("_")[1]
							if len(self.gd["chosen"]) == int(status[-1]) - 1 and len([s for s in self.gd["chosen"] if s != idm]) == len(self.gd["chosen"]):
								for _ in self.gd["thisupto"][1]:
									if _ != idm and _ not in self.gd["chosen"]:
										self.cd[_].selectable(False)
										r = self.gd["thisupto"][2][self.gd["thisupto"][1].index(_)]
										self.field_btn[r].x = -Window.width
										if r in self.gd["select_btns"]:
											self.gd["select_btns"].remove(r)
				elif ind in self.gd["chosen"]:
					self.cd[ind].update_text()
					self.gd["chosen"].remove(ind)

					if self.gd["thisupto"][0]:
						for _ in self.gd["thisupto"][2]:
							if _ not in self.gd["select_btns"]:
								self.gd["select_btns"].append(_)
								self.cd[self.gd["thisupto"][1][self.gd["thisupto"][2].index(_)]].selectable()
								self.field_btn[_].x = self.gd["thisupto"][3][self.gd["thisupto"][2].index(_)]


			if "Encore" in self.gd["phase"] and self.gd["pp"] >= 0 and len(self.gd["chosen"]) == 1:
				self.gd["encore_ind"] = str(self.gd["chosen"][0])
				self.move_field_btn(self.gd["phase"])
				return True
			elif len(self.gd["chosen"]) == int(status[-1]) or self.gd["move"] or (len(self.gd["chosen"]) == len(self.gd["select_btns"]) and len(self.gd["select_btns"]) < int(status[-1])):
				if not self.gd["choose"]:
					if len(self.gd["chosen"]) < int(status[-1]):
						for r in range(int(status[-1]) - len(self.gd["chosen"])):
							self.gd["chosen"].append("")
					for inx in self.gd["chosen"]:
						if self.gd["mstock"][0]:
							self.gd["target"].append(self.gd["mstock"][0])
						self.gd["target"].append(inx)
						if inx != "" and inx in self.cd:
							self.cd[inx].selectable(False)
							self.cd[inx].update_text()

				if self.gd["btrait"][1]:
					self.gd["btrait"] = ["", [], [], [], [], []]
				if self.gd["thisupto"][1]:
					self.gd["thisupto"] = ["", [], [], []]
				self.gd["choose"] = True
				if not self.gd["payed"] and self.gd["pay"]:
					self.move_field_btn(self.gd["phase"], y=True)
				else:
					self.move_field_btn(self.gd["phase"])
				self.gd["select_on"] = False
				self.sd["btn"]["ablt_info"].y = -Window.height * 2
				return True
			else:
				if "decker" in self.gd["ability_doing"]:
					for tt in range(len(self.gd["chosen"])):
						if tt == 0:
							if "bottom" in self.gd["effect"]:
								self.cd[self.gd["chosen"][tt]].update_text("Bottom", .30)
							elif "top" in self.gd["effect"]:
								self.cd[self.gd["chosen"][tt]].update_text("Top", .45)
							else:
								self.cd[self.gd["chosen"][tt]].update_text(tt + 1)
						else:
							self.cd[self.gd["chosen"][tt]].update_text(tt + 1)
				elif "move" not in self.gd["ability_doing"]:
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
		if self.infob:
			self.infob.cancel()
			self.infob = None
		if btn.cid[:-1] in self.fields:
			self.show_field_label(btn.cid)

		if not self.gd["info_p"]:
			if not self.gd["payed"] and self.gd["pay"]:
				if self.selected_card():
					if self.gd["mstock"][0]:
						self.pay_mstock(self.gd["mstock"][0])
					else:
						self.pay_condition()
			elif not self.gd["text_popup"]:  
				if self.selected_card():
					if "encore" in self.gd["effect"] and self.gd["pp"] >= 0 and "SWaiting" in self.gd["target"]:
						self.encore_done()
					elif "Encore" in self.gd["phase"] and self.gd["pp"] >= 0 and "AUTO" not in self.gd["ability_trigger"]:
						self.encore_start()
					else:
						self.ability_effect()

	def event_done(self, *args):
		if self.gd["ability_trigger"]:
			if self.gd["estock_payed"]:
				self.gd["estock_payed"] = []
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
		if self.cd[ind].card == "Event":
			ablts = self.cd[ind].text_c
		elif self.cd[ind].card == "Character":
			ablts = [tt for tt in self.cd[ind].text_c if tt[0].startswith(cont_ability)]
		for tt in self.cd["1"].text_c:
			if tt[0].startswith(cont_ability):
				ablts.append(tt)

		for item in ablts:
			play = ab.play(item[0], p=True)
			if "play" in play:
				if play[0] == -1:
					if "Name" in play and play[play.index("Name") + 1] in self.cd[ind].name_t:
						return False
				else:
					if "lower" in play and len(self.cont_times(play, self.cont_cards(play, ind), self.cd)) <= play[0]:
						return False
					elif "lower" not in play and len(self.cont_times(play, self.cont_cards(play, ind), self.cd)) >= play[0]:
						return False
		return True

	def check_condition(self, ind):
		card = self.cd[ind]
		check = False
		effect = True
		if card.card == "Climax":
			text = "Colour"
			if self.gd["any_Clrclimax"][self.gd["active"]] or card.mcolour.lower() in self.pd[ind[-1]]["colour"]:
				check = True
		else:
			text = "Level"
			if card.level_t == 0:
				text = "Cost"
				if len(self.pd[ind[-1]]["Stock"]) >= card.cost_t:
					check = True
			elif len(self.pd[ind[-1]]["Level"]) >= card.level_t:
				text = "Colour"
				if card.mcolour.lower() in self.pd[ind[-1]]["colour"] or (self.gd["any_ClrChname"][self.gd["active"]] and card.card == "Character" and any(nn in card.name for nn in self.gd["any_ClrChname"][self.gd["active"]])):
					text = "Cost"
					if len(self.pd[ind[-1]]["Stock"]) >= card.cost_t:
						check = True
					elif card.card == "Event" and len(self.pd[ind[-1]]["Stock"])+len(self.gd["estock"][card.ind[-1]])  >= card.cost_t:
						check = True
					elif ind in self.check_waiting_cost:
						if len([s for s in self.pd[ind[-1]]["Center"] + self.pd[ind[-1]]["Back"] if s != "" and self.gd["waiting_cost"][0][card.cid][1] in self.cd[s].name_t]) > 0:
							check = True

		if card.card == "Event" and (self.gd["no_event"][ind[-1]] or not self.check_event(ind)):
			effect = False
			text = "Effect"
		elif card.card == "Character" and not self.check_event(ind):
			effect = False
			text = "Effect"
		elif card.card == "Climax" and self.gd["no_climax"][ind[-1]]:
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

				self.sd["btn"]["close_btn"].center_x = self.gd["p_xscat"] / 2. - self.sd["card"][0] / 4
				self.sd["btn"]["close_btn"].y = self.sd["padding"] * 1.5

				if card.card == "Event" and self.gd["no_event"][ind[-1]]:
					self.sd["btn"]["label"].text = f"The card \"{card.name}\" cannot be played because you cannot play event cards from hand this turn."
				elif card.card == "Climax" and self.gd["no_climax"][ind[-1]]:
					self.sd["btn"]["label"].text = f"The card \"{card.name}\" cannot be played because you cannot play climax cards from hand during your climax phase."
				else:
					self.sd["btn"]["label"].text = f"The card \"{card.name}\" cannot be played because it does not meet the required {text} condition."
				self.sd["btn"]["label"].text_size = ((self.gd["p_xscat"] - self.sd["padding"] * 2) * 0.9, None)
				self.sd["btn"]["label"].texture_update()
				self.sd["btn"]["label"].height = self.sd["btn"]["label"].texture.size[1]
				self.sd["btn"]["label"].pos = (self.sd["padding"] / 4, self.sd["card"][1] / 2. + self.sd["padding"] * 3.5)  

				self.sd["popup"]["popup"].size = (self.gd["p_xscat"], self.sd["btn"]["label"].texture.size[1] + self.sd["card"][1] * 2 + self.sd["padding"] * 9.5 + self.sd["popup"]["popup"].title_size + self.sd["popup"]["popup"].separator_height)

				self.sd["popup"]["p_scv"].size = (self.gd["p_xscat"], self.gd["p_height"])
				self.sd["popup"]["p_scv"].y = self.sd["card"][1] / 2. + self.sd["padding"] * 3.5 + self.sd["btn"]["label"].texture.size[1] + self.sd["padding"] * 1.5

				self.sd["popup"]["stack"].size = self.sd["popup"]["p_scv"].size

				self.gd["p_l"] = [ind]
				nx, ns = self.get_index_stack(self.gd["p_l"], self.gd["p_hand"])
				if nx:
					self.gd["p_l"].insert(nx, "sspace")
					self.sd["popup"]["sspace"].size = (self.sd["popup"]["sspace"].size_o[0] * ns, self.sd["popup"]["sspace"].size[1])

				for inx in self.gd["p_l"]:
					if "sspace" in inx:
						try:
							self.sd["popup"]["stack"].add_widget(self.sd["popup"][inx])
						except WidgetException:
							pass
					else:
						self.sd["popup"]["stack"].add_widget(self.cpop[inx])
						self.cpop[inx].selected_c(False)
						self.cpop[inx].update_text()

				self.sd["popup"]["popup"].open()
			return False

	def move(self, *args):
		ind = self.gd["ability_trigger"].split("_")[1]
		if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
			if not self.gd["move"] or self.gd["move"] == "none":
				self.gd["target"].append("")
			else:
				self.gd["target"].append(self.gd["move"])
			self.gd["move"] = ""

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
			card.update_text()
			if "Waiting" in card.pos_new:
				continue
			self.mat[idm[-1]]["mat"].remove_widget(self.cd[idm])
			self.mat[idm[-1]]["mat"].add_widget(self.cd[idm])
			temp = ""
			if self.pd[idm[-1]][move[:-1]][int(move[-1])] != "":
				temp = self.pd[idm[-1]][move[:-1]][int(move[-1])]
				self.cd[temp].setPos(field=self.mat[card.owner]["field"][card.pos_new], t=card.pos_new)
				self.pd[idm[-1]][card.pos_new[:-1]][int(card.pos_new[-1])] = temp
			else:
				self.pd[idm[-1]][card.pos_new[:-1]][int(card.pos_new[-1])] = ""
			card.setPos(field=self.mat[card.owner]["field"][move], t=move)
			self.pd[idm[-1]][move[:-1]][int(move[-1])] = card.ind
			if idm in self.pd[idm[-1]]["marker"] or temp in self.pd[idm[-1]]["marker"]:
				self.update_marker(idm[-1])
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

	def get_fields(self, status=""):
		if not status:
			status = self.gd["status"]

		if "Opp" in status and (self.gd["rev"] or self.gd["rev_counter"]):
			player = self.gd["active"]
		elif "Opp" in status or self.gd["rev"] or self.gd["rev_counter"]:
			player = self.gd["opp"]
		else:
			player = self.gd["active"]

		fields = []
		inm = self.gd["ability_trigger"].split("_")[1]
		if "opp" in self.gd["effect"] and "Opp" in status:
			player = inm[-1]

		if "Osite" in status:
			if "Center" in self.cd[inm].pos_new:
				if inm[-1] == "1":
					op = "2"
				elif inm[-1] == "2":
					op = "1"
				opp = self.pd[op]["Center"][self.m[int(self.cd[inm].pos_new[-1])]]
				if opp != "":
					fields.append(opp)
		elif "BBattle" in status:
			atk = self.gd["attacking"][0]
			deff = "0"
			if atk and self.gd["attacking"][1] == "f":
				if atk[-1] == "1":
					op = "2"
				elif atk[-1] == "2":
					op = "1"
				if "C" in self.gd["attacking"][4]:
					deff = self.pd[op]["Center"][self.gd["attacking"][3]]
				elif "B" in self.gd["attacking"][4]:
					deff = self.pd[op]["Back"][self.gd["attacking"][3]]

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
		elif "Middle" in status:
			fields = [self.pd[player]["Center"][1]]
		elif "Center" in status:
			fields = [s for s in self.pd[player]["Center"] if s != ""]
		elif "Back" in status:
			fields = [s for s in self.pd[player]["Back"] if s != ""]
		elif "Any" in status:
			fields = [s for s in self.pd[self.gd["active"]]["Center"] + self.pd[self.gd["active"]]["Back"] + self.pd[self.gd["opp"]]["Center"] + self.pd[self.gd["opp"]]["Back"] if s != ""]
		elif "Another" in status:
			fields = [s for s in self.pd["1"]["Center"] + self.pd["1"]["Back"] + self.pd["2"]["Center"] + self.pd["2"]["Back"] if s != ""]
		else:
			fields = [s for s in self.pd[player]["Center"] + self.pd[player]["Back"] if s != ""]

		if "Antilvl" in status:
			fields = [s for s in fields if self.cd[s].level_t > len(self.pd[player]["Level"])]

		if "TraitN" in status:
			traits = status.split("_")[1:-2]
			names = status.split("_")[-2]
			status = status.split("_")[-1]
			if traits == [""]:
				fields = [s for s in fields if "Character" in self.cd[s].card and (len(self.cd[s].trait_t) <= 0 or names in self.cd[s].name_t)]
			else:
				fields = [s for s in fields if "Character" in self.cd[s].card and (names in self.cd[s].name_t or any(trait in self.cd[s].trait_t for trait in traits))]
		elif "Trait" in status:
			traits = status.split("_")[1:-1]
			status = status.split("_")[-1]
			if traits == [""]:
				fields = [s for s in fields if len(self.cd[s].trait_t) <= 0 and "Character" in self.cd[s].card]
			else:
				fields = [s for s in fields if "Character" in self.cd[s].card and any(trait in self.cd[s].trait_t for trait in traits)]
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
			fields = [s for s in fields if any(name in names for name in self.cd[s].name_t.split("\n"))]
		elif "NameO" in status:
			names = status.split("_")[1:-1]
			status = status.split("_")[-1]
			fields = [s for s in fields if names[0] in self.cd[s].name_t and names[1] != self.cd[s].name_t]
		elif "Name" in status:
			names = status.split("_")[1:-1]
			status = status.split("_")[-1]
			fields = [s for s in fields if any(name in self.cd[s].name_t for name in names)]
		elif "Text" in status:
			names = status.split("_")[1:-1]
			status = status.split("_")[-1]
			fields = [s for s in fields if any(any(text1.lower() in tx[0].lower() and f"\"{text1.lower()}\"" not in tx[0].lower() for text1 in names) for tx in self.cd[s].text_c)]
		elif "ColourWo" in status:
			names = status.split("_")[1:-1]
			status = status.split("_")[-1]
			fields = [s for s in fields if all(name.lower() not in self.cd[s].colour for name in names)]
		elif "Colour" in status:
			names = status.split("_")[1:-1]
			status = status.split("_")[-1]
			fields = [s for s in fields if any(name.lower() in self.cd[s].colour for name in names)]

		if "Markers<=" in status:
			if int(status[status.index("Markers<=") + 9]) == 0:
				fields = [s for s in fields if s not in self.pd[s[-1]]["marker"] or (s in self.pd[s[-1]]["marker"] and len(self.pd[s[-1]]["marker"][s]) <= 0)]
		if "Cost<=" in status:
			fields = [s for s in fields if self.cd[s].cost_t <= int(status[status.index("Cost<=") + 6])]
		elif "Cost>=" in status:
			fields = [s for s in fields if self.cd[s].cost_t >= int(status[status.index("Cost>=") + 6])]

		if "Level<=p+" in status:
			fields = [s for s in fields if self.cd[s].level_t <= len(self.pd[s[-1]]["Level"]) + int(status[status.index("<=p+") + 4])]
		elif "Level<=p" in status:
			fields = [s for s in fields if self.cd[s].level_t <= len(self.pd[s[-1]]["Level"])]
		elif "Level<=" in status:
			fields = [s for s in fields if self.cd[s].level_t <= int(status[status.index("Level<=") + 7])]
		elif "Level>=" in status:
			fields = [s for s in fields if self.cd[s].level_t >= int(status[status.index("Level>=") + 7])]

		if "Stand" in status:
			fields = [s for s in fields if self.cd[s].status == "Stand"]
		elif "Reverse" in status:
			fields = [s for s in fields if self.cd[s].status == "Reverse"]

		if "Other" in status and "Other_same" in self.gd["effect"]:
			if self.gd["effect"][self.gd["effect"].index("Other_same") + 1] in fields:
				fields.remove(self.gd["effect"][self.gd["effect"].index("Other_same") + 1])
		if "Other" in status and inm in fields:
			fields.remove(inm)
		if "This" in status and inm not in fields:
			fields.append(inm)

		if "Opp" in status:
			for idc in list(fields):
				for text in self.cd[idc].text_c:
					if text[0].startswith(cont_ability) and text[1] != 0 and text[1] > -9:
						eff = ab.cont(text[0])
						if eff and "no_target" in eff:
							fields.remove(idc)
							break

		if any(doi in self.gd["ability_doing"] for doi in ("hander", "wind", "memorier")):
			for idc in list(fields):
				for text in self.cd[idc].text_c:
					if text[0].startswith(cont_ability) and text[1] != 0 and text[1] > -9:
						eff = ab.cont(text[0])
						if eff and "no_hand" in eff:
							if idc in fields:
								fields.remove(idc)
						if eff and "no_memory" in eff:
							if idc in fields:
								fields.remove(idc)

		if "BBattleBatk" in status and "May" in status:
			fields.append(self.pd[self.gd["opp"]]["Center"][self.gd["attacking"][3]])
		if self.gd["btrait"][0] and len(self.gd["chosen"]) >= 1:
			for ii in self.gd["chosen"]:
				fields.append(ii)
		return fields

	def select_card(self, s="", p=False, fd=None, card_filter=False, status=""):
		self.gd["movable"] = []
		self.gd["select_on"] = True
		if not card_filter:
			self.gd["select_btns"] = []
			self.act_ability_show(hide=True)
		if p:
			status = self.gd["pay_status"]
		elif not status:
			status = self.gd["status"]

		if fd is None:
			fields = self.get_fields(status)
		else:
			fields = fd

		if card_filter:
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
			if ind[-1] == "2":
				self.field_btn[f"{field}{ind[-1]}"].x = self.mat[ind[-1]]["mat"].x + self.mat[ind[-1]]["mat"].size[0] - self.sd["card"][0] - self.mat[ind[-1]]["field"][field][0]
			else:
				self.field_btn[f"{field}{ind[-1]}"].x = self.mat[ind[-1]]["mat"].x + self.mat[ind[-1]]["field"][field][0]
			self.gd["select_btns"].append(f"{field}{ind[-1]}")
			if "thisupto" in self.gd["effect"] and "Other" in self.gd["effect"]:
				self.gd["thisupto"][0] = str(status)
				self.gd["thisupto"][1].append(ind)
				self.gd["thisupto"][2].append(f"{field}{ind[-1]}")
				self.gd["thisupto"][3].append(self.field_btn[f"{field}{ind[-1]}"].x)

		self.sd["btn"]["ablt_info"].y = 0
		if self.gd["uptomay"] or self.gd["astock_select"]:
			if "Encore" in self.gd["phase"] and "AUTO" not in self.gd["ability_trigger"]:
				self.sd["btn"]["ablt_info"].y = -Window.height
				self.sd["btn"]["end"].text = "End Encore"
			else:
				if self.gd["astock_select"]:
					self.sd["btn"]["end"].text = "End Choose"
				else:
					if "do" in self.gd["effect"]:
						self.sd["btn"]["end"].text = "Continue Effect"
					else:
						self.sd["btn"]["end"].text = "End Effect"

				if self.gd["effect"] and isinstance(self.gd["effect"][0], int) and self.gd["effect"][0] > 1:
					if "stand" in self.gd["effect"] and "swap" in self.gd["effect"] and self.gd["effect"][0] == 2:
						self.sd["btn"]["end"].x = Window.width - self.sd["btn"]["end"].size[0]
					else:
						self.sd["btn"]["end"].x = Window.width - self.sd["btn"]["end"].size[0] * 2
						self.sd["btn"]["end_eff"].y = 0
			self.sd["btn"]["end"].disabled = False
			self.sd["btn"]["end"].y = 0
			self.sd["btn"]["end_attack"].y = -Window.height
			self.sd["btn"]["end_phase"].y = -Window.height
			if self.gd["payed_mstock"] and len(self.pd["1"]["Stock"]) < self.gd["pay"][self.gd["pay"].index("Stock") + 1]:
				self.sd["btn"]["end"].disabled = True
				self.sd["btn"]["end"].y = -Window.height
		self.hand_btn_show(True)

	def select_field(self, p=False, *args):
		player = self.gd["ability_trigger"].split("_")[1][-1]
		self.gd["movable"] = []
		self.gd["select_btns"] = []
		self.act_ability_show(hide=True)
		if p:
			status = self.gd["pay_status"]
		else:
			status = self.gd["status"]

		if "Opp" in status:
			if player == "1":
				player = "2"
			elif player == "2":
				player = "1"

		if "Clock" in status:
			if len(self.pd[player]["Clock"]) > 0:
				self.gd["select_btns"].append(f"Clock{player}")
				if "Top" in status:
					self.cd[self.pd[player]["Clock"][-1]].selectable()
		else:
			fields = []
			if "Change" in status:
				fields = [self.cd[self.gd["ability_trigger"].split("_")[1]].pos_old]
			elif "Onentsite" in status:
				plr = self.gd["ability_trigger"].split("_")[1][-1]
				if plr == "1":
					opp = "2"
				elif plr == "2":
					opp = "1"
				for rr in range(3):
					if self.pd[opp]["Center"][self.m[rr]] != "":
						fields.append(f"Center{rr}")
			elif "Middle" in status:
				fields = list(self.gd["stage"][1])
			elif "Center" in status:
				fields = list(self.gd["stage"][:3])
			elif "Back" in status:
				fields = list(self.gd["stage"][3:])
			else:
				fields = list(self.gd["stage"])

			if "OpenC" in status:
				fields = [fd for fd in fields if self.pd[player][fd[:-1]][int(fd[-1])] == ""]
			elif "Open" in status:
				fields = [fd for fd in fields if self.pd[player][fd[:-1]][int(fd[-1])] == ""]
			if "separate" in self.gd["effect"]:
				for field in list(fields):
					if any(d for d in self.gd["target"] if field in d):
						fields.remove(field)

			for field in sorted(fields):
				self.field_btn[f"{field}{player}s"].x = self.mat[player]["field"][field][0] - self.sd["padding"]
				self.field_btn[f"{field}{player}s"].y = self.mat[player]["field"][field][1] - self.sd["padding"]

				if "Opp" in status and "oppturn" not in self.gd["effect"]:
					self.field_btn[f"{field}{player}"].x = self.mat[player]["mat"].x + self.mat[player]["mat"].size[0] - self.sd["card"][0] - self.mat[player]["field"][field][0]
				else:
					self.field_btn[f"{field}{player}"].x = self.mat[player]["field"][field][0] + self.mat[player]["mat"].x
				self.gd["select_btns"].append(f"{field}{player}")

		if self.gd["uptomay"]:
			if "do" in self.gd["effect"]:
				self.sd["btn"]["end"].text = "Continue Effect"
			else:
				self.sd["btn"]["end"].text = "End Effect"
			self.sd["btn"]["end"].disabled = False
			self.sd["btn"]["end"].y = 0
			self.sd["btn"]["end_attack"].y = -Window.height
			self.sd["btn"]["end_phase"].y = -Window.height
			if isinstance(self.gd["effect"][0], int) and self.gd["effect"][0] > 1 and len(self.gd["target"]) % self.gd["effect"][0] != 0 and len(self.gd["target"]) > 2:
				self.sd["btn"]["end"].x = Window.width - self.sd["btn"]["end"].size[0] * 2
				self.sd["btn"]["end_eff"].y = 0
		self.hand_btn_show(True)

	def janken(self, *args):
		if self.gd["janken_result"] == 0:
			Clock.schedule_once(self.janken_start, move_dt_btw)
		elif self.gd["janken_result"] != 0:
			if "winner" in self.gd["effect"]:
				if self.gd["janken_result"] < 0 and self.gd["ability_trigger"].split("_")[1][-1] == "1" or self.gd["janken_result"] > 0 and self.gd["ability_trigger"].split("_")[1][-1] == "2":
					self.gd["rev"] = True
					self.gd["do"][1].append("opp")
					self.gd["effect"][self.gd["effect"].index("do") + 1].append("opp")
				self.gd["done"] = True

			self.gd["janken_result"] = 0

			if "janken" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("janken")

			self.ability_effect()

	def replaceImage_test(self):
		for nx in range(1, 5):
			self.test[str(nx)] = Label(text="　" * nx, font_size=self.sd["btn"]["label"].font_size, valign='middle')
			self.test[str(nx)].texture_update()
		for nx in range(5):
			self.iach[str(nx)] = Image(source=f"atlas://{img_in}/other/blank", size=(self.test["1"].texture.size[0] * 1.05, self.test["1"].texture.size[1] * 1.05), allow_stretch=True, size_hint=(None, None))
			self.sd["popup"]["p_sct"].add_widget(self.iach[str(nx)])

	def stack_btn_ability(self, qty):
		for inx in range(len(self.sd["sbtn"]), qty - len(self.sd["sbtn"]) + 1):
			self.sd["sbtn"][f"{inx}"] = Labelbtn(size=(self.sd["card"][0] * 5 + self.sd["padding"], self.sd["card"][1]))
			self.sd["sbtn"][f"{inx}"].btn.bind(on_release=self.stack_resolve)

	def stack_btn_perform(self, qty):
		for inx in range(len(self.sd["sbper"]), qty + 1):
			self.sd["sbper"][f"{inx}"] = Labelbtn(size=(self.sd["card"][0] * (starting_hand + 1) + self.sd["padding"], self.sd["card"][1] * 2.25))
			self.sd["sbper"][f"{inx}"].btn.bind(on_release=self.perform_popup_btn)

	def stack_btn_act(self, qty):
		for inx in range(len(self.sd["sbact"]), qty + 1):
			self.sd["sbact"][f"{inx}"] = Labelbtn(size=(self.sd["card"][0] * 5 + self.sd["padding"], self.sd["card"][1]))
			self.sd["sbact"][f"{inx}"].btn.bind(on_release=self.act_popup_btn)

	def replaceImage(self):
		for nx in range(len(self.iach), len(self.sd["btn"]["label"].anchors)):
			self.iach[str(nx)] = Image(source=f"atlas://{img_in}/other/blank", size=(self.test["1"].texture.size[0] * 1.05, self.test["1"].texture.size[1] * 1.05), allow_stretch=True, size_hint=(None, None))
			self.sd["popup"]["p_sct"].add_widget(self.iach[str(nx)])

		self.gd["inx"] = 0
		for item in self.sd["btn"]["label"].anchors:
			self.iach[str(self.gd["inx"])].size = (self.test[item[-1]].texture.size[0] * 1.05, self.test[item[-1]].texture.size[1] * 1.05)
			self.iach[str(self.gd["inx"])].source = f"atlas://{img_in}/other/{item[:-3]}"
			self.iach[str(self.gd["inx"])].pos = (self.sd["padding"] * 1.5 + self.sd["btn"]["label"].anchors[item][0] + self.sd["btn"]["label"].x, self.sd["btn"]["label"].size[1] - self.sd["padding"] / 4.5 - self.sd["btn"]["label"].anchors[item][1] - self.test[item[-1]].texture.size[1] + self.sd["btn"]["label"].y)
			self.gd["inx"] += 1

	def confirm_popup(self, dt=.0, ind="", c="", icon="", a="", o=""):
		self.gd["confirm_pop"] = True
		self.sd["text"]["popup"].dismiss()
		self.cardinfo.dismiss()
		self.popup_clr_button()
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

		xscat = (self.sd["padding"] + self.sd["card"][0]) * starting_hand + self.sd["padding"] * 2
		self.gd["p_hand"] = starting_hand


		self.gd["p_yscat"] = self.sd["padding"] * 3 + self.sd["card"][1] * 3 + self.sd["padding"] * 4 + self.sd["popup"]["popup"].title_size + self.sd["popup"]["popup"].separator_height

		self.sd["btn"]["down_again"].y = -Window.height * 2
		for btn in ("yes_btn", "no_btn", "field_btn"):
			if btn[0] == "f":
				self.sd["btn"][btn].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
				self.sd["btn"][btn].center_x = xscat / 2. - self.sd["card"][0] / 4
				self.sd["btn"][btn].y = self.sd["padding"] * 3 + self.sd["card"][1] / 2.
			else:
				self.sd["btn"][btn].size = (self.sd["card"][0] * 1.5, self.sd["card"][1] / 2.)
				self.sd["btn"][btn].y = self.sd["padding"] * 1.5
				if btn[0] == "y" and "encore" not in self.gd["p_c"]:
					self.sd["btn"][btn].center_x = xscat / 4. - self.sd["padding"] / 2
				elif btn[0] == "n" and "encore" not in self.gd["p_c"]:
					self.sd["btn"][btn].center_x = xscat / 4. * 3 - self.sd["card"][0] / 2

		if "encore" in self.gd["p_c"]:
			self.sd["btn"]["yes_btn"].x = -Window.width * 2
			self.sd["btn"]["no_btn"].x = -Window.width * 2
			self.sd["btn"]["effect_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
			self.sd["btn"]["effect_btn"].center_x = xscat / 4. * 3 - self.sd["card"][0] / 2  
			self.sd["btn"]["effect_btn"].y = self.sd["padding"] * 1.5

			self.sd["btn"]["field_btn"].center_x = xscat / 4. - self.sd["padding"] / 2
			self.sd["btn"]["field_btn"].y = self.sd["padding"] * 1.5
			self.gd["p_yscat"] = self.sd["padding"] * 3.5 + self.sd["card"][1] * 1.5 + self.sd["padding"] * 4 + self.sd["popup"]["popup"].title_size + self.sd["popup"]["popup"].separator_height
		elif "reflev" in self.gd["p_c"]:
			self.sd["btn"]["yes_btn"].x = -Window.width * 2
			self.sd["btn"]["no_btn"].x = -Window.width * 2
			self.sd["btn"]["effect_btn"].x = -Window.width * 2
			self.sd["btn"]["field_btn"].center_x = xscat / 2. - self.sd["card"][0] / 4
			self.sd["btn"]["field_btn"].y = self.sd["padding"] * 1.5
			self.gd["p_yscat"] = self.sd["padding"] * 3.5 + self.sd["card"][1] * 1 + self.sd["padding"] * 4 + self.sd["popup"]["popup"].title_size + self.sd["popup"]["popup"].separator_height
		pos = (self.sd["padding"] / 4, self.sd["padding"] * 5 + self.sd["card"][1])
		confirm_text = "　"
		self.sd["btn"]["label"].halign = "left"
		if "Overplay" in self.gd["p_c"]:
			idm = self.gd["p_ind"].split("_")
			confirm_text = f"Do you want to play \"{self.cd[idm[0]].name_t}\" over \"{self.cd[idm[1]].name_t}\"?"
			self.gd["p_l"] = [idm[0], "arrow", idm[1]]
		elif "Dismantle" in self.gd["p_c"]:
			self.sd["popup"]["popup"].title = "Confirm deck dismantle"
			confirm_text = f"Do you want to dismantle the selected deck?"
			self.gd["p_yscat"] = self.sd["padding"] * 7.5 + self.sd["card"][1] * 1 + self.sd["popup"]["popup"].title_size + self.sd["popup"]["popup"].separator_height
			self.sd["btn"]["field_btn"].y = -Window.height * 2
			self.sd["btn"]["label"].halign = "center"
			pos = (self.sd["padding"] / 4, self.sd["padding"] * 3.5 + self.sd["card"][1] / 2)
		elif "Restart" in self.gd["p_c"]:
			self.sd["btn"]["down_again"].size = self.sd["btn"]["field_btn"].size
			self.sd["btn"]["down_again"].pos = self.sd["btn"]["field_btn"].pos
			self.sd["btn"]["field_btn"].y = -Window.height * 2
			self.sd["btn"]["label"].halign = "center"
			self.gd["p_yscat"] = self.sd["padding"] * 7.5 + self.sd["card"][1] * 1.5 + self.sd["popup"]["popup"].title_size + self.sd["popup"]["popup"].separator_height
			confirm_text = "Would you like to close the app?\n\n*Downloaded files will only be loaded after a restart."
		elif "Download" in self.gd["p_c"]:
			self.sd["popup"]["popup"].title = "Confirm download"
			self.gd["p_ind"] = float(self.gd["p_ind"])
			if self.gd["p_ind"] < 102:
				mb = f"{round(self.gd['p_ind'], 2)} KB"
			else:
				mb = f"{round(self.gd['p_ind'] / 1024, 2)} MB"
			confirm_text = f"Would you like to download the selected game data?\n\nDownload size:\t{mb}\n\n*It is recommended connecting to WI-FI before downloading."
			self.gd["p_yscat"] = self.sd["padding"] * 7.5 + self.sd["card"][1] * 1 + self.sd["popup"]["popup"].title_size + self.sd["popup"]["popup"].separator_height
			self.sd["btn"]["field_btn"].y = -Window.height * 2
			self.sd["btn"]["label"].halign = "center"
			pos = (self.sd["padding"] / 4, self.sd["padding"] * 3.5 + self.sd["card"][1] / 2)
		elif "astock" in self.gd["p_c"]:
			self.sd["popup"]["popup"].title = f"Confirm cost"
			confirm_text = f"Do you want to pay the [ACT] cost using markers of one of your character on stage?\n \n{self.gd['ability']}"
			self.gd["p_yscat"] -= self.sd["card"][1] * 1.5
		elif "estock" in self.gd["p_c"]:
			self.sd["popup"]["popup"].title = f"Confirm cost"
			confirm_text = f"Do you want to pay the event cost using markers of one of your character on stage?\n \n{self.gd['ability']}"
			self.gd["p_yscat"] -= self.sd["card"][1] * 1.5
		elif "confirm" in self.gd["p_c"] or "ability" in self.gd["p_c"]:
			ability = self.cardinfo.replaceMultiple(self.gd["ability"])
			if "do" in self.gd["effect"] and "upto" in self.gd["effect"][self.gd["effect"].index("do") + 1]:
				confirm_text = f"Do you agree to continue the following ability?\n \n{ability}"
			else:
				confirm_text = f"Do you agree to activate the following ability?\n \n{ability}"
			self.gd["p_l"] = [self.gd["p_ind"]]
			if len(self.gd["stack"]["1"]) > 1:
				self.sd["btn"]["return_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
				self.sd["btn"]["return_btn"].center_x = xscat / 2. - self.sd["card"][0] / 4
				self.sd["btn"]["return_btn"].y = self.sd["padding"] * 5 + self.sd["card"][1]
				self.gd["p_yscat"] += self.sd["padding"] * 3 + self.sd["card"][1] / 2.
				pos = (self.sd["padding"] / 4, self.sd["padding"] * 6.5 + self.sd["card"][1] * 1.5)
		elif "trigger" in self.gd["p_c"]:
			confirm_text = f"Do you want to activate the following trigger?\n \n{self.gd['ability']}"
		elif "counter" in self.gd["p_c"]:
			confirm_text = "Do you want to play a card which has a Counter Icon on it?\n "
		elif "encore" in self.gd["p_c"]:
			self.gd['encore_ind'] = ind
			self.sd["popup"]["popup"].title = "Confirm Encore ability"
			self.gd["inx"] = 0
			for item in ("Stock3", "Stock2", "Stock1", "Character", "TraitN", "Trait", "Clock", "Climax", "SWaiting"):
				if item in self.gd["effect"]:
					self.sd["btn"][f"encore_{item}"].size = (self.sd["card"][0] * starting_hand, self.sd["card"][1] / 1.5)
					self.sd["btn"][f"encore_{item}"].y = self.sd["padding"] * 3 + self.sd["card"][1] / 2 + (self.sd["padding"] * 1.5 + self.sd["card"][1] / 1.5) * self.gd["inx"]
					if len(self.gd["stack"][self.gd["active"]]) > 1:
						self.sd["btn"][f"encore_{item}"].y += self.sd["padding"] * 2 + self.sd["card"][1] / 2
					self.sd["btn"][f"encore_{item}"].center_x = xscat / 2. - self.sd["card"][0] / 4
					if "SWaiting" in item:
						self.sd["btn"][f"encore_{item}"].text = markreplace["markreplace"][f'({self.gd["encore_effect"][0]})'] + " " + self.sd["btn"][f"encore_{item}"].text[self.sd["btn"][f"encore_{item}"].text.index("&"):]
					self.gd["inx"] += 1

			confirm_text = f"Do you want to encore \"{self.cd[self.gd['encore_ind']].name_t}\"?\n \n "

			self.gd["p_yscat"] += (self.sd["card"][1] / 1.5 + self.sd["padding"] * 1.5) * self.gd["inx"]
			pos = (self.sd["padding"] / 4, (self.sd["padding"] * 1.5 + self.sd["card"][1] / 1.5) * (self.gd["inx"]) + self.sd["padding"] * 2)
			self.gd["p_l"] = [self.gd["encore_ind"]]
			if len(self.gd["stack"][self.gd["active"]]) > 1:
				self.sd["btn"]["return_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)
				self.sd["btn"]["return_btn"].center_x = xscat / 2. - self.sd["card"][0] / 4  
				self.sd["btn"]["return_btn"].y = self.sd["padding"] * 3 + self.sd["card"][1] / 2
				self.gd["p_yscat"] += self.sd["padding"] * 3 + self.sd["card"][1] / 2.
				pos = (self.sd["padding"] / 4, (self.sd["padding"] * 1.5 + self.sd["card"][1] / 1.5) * (self.gd["inx"]) + self.sd["padding"] * 2 + (self.sd["padding"] * 1.5 + self.sd["card"][1] * 0.5))
		elif "reflev" in self.gd["p_c"]:
			self.sd["popup"]["popup"].title = "Confirm rule action"
			self.gd["inx"] = 0
			for item in ("reshuffle", "levelup"):
				self.sd["btn"][f"{item}_btn"].size = (self.sd["card"][0] * 5 + self.sd["padding"], self.sd["card"][1] / 1.5)
				self.sd["btn"][f"{item}_btn"].y = self.sd["padding"] * 3 + self.sd["card"][1] / 2. + (self.sd["padding"] * 1.5 + self.sd["card"][1] / 1.5) * self.gd["inx"]
				self.sd["btn"][f"{item}_btn"].center_x = xscat / 2. - self.sd["card"][0] / 4
				self.gd["inx"] += 1
			confirm_text = f"Choose which rule action to perform first."
			self.gd["p_yscat"] += (self.sd["card"][1] / 1.5 + self.sd["padding"] * 1.5) * self.gd["inx"]
			pos = (self.sd["padding"] / 4, self.sd["padding"] * 3.5 + self.sd["card"][1] / 3 + (self.sd["padding"] * 1.5 + self.sd["card"][1] / 1.5) * (self.gd["inx"]) + self.sd["padding"] * 2)

		self.sd["btn"]["label"].text_size = ((xscat - self.sd["padding"] * 2) * 0.9, None)
		self.sd["btn"]["label"].text = confirm_text
		self.sd["btn"]["label"].texture_update()
		self.sd["btn"]["label"].height = self.sd["btn"]["label"].texture.size[1]
		self.sd["btn"]["label"].pos = pos
		self.replaceImage()
		if icon != "":
			self.gd["p_l"] = [icon]

		self.sd["popup"]["popup"].size = (xscat, self.gd["p_yscat"] + self.sd["btn"]["label"].texture.size[1])  

		self.sd["popup"]["p_scv"].y = self.sd["btn"]["label"].y + self.sd["btn"]["label"].texture.size[1] + self.sd["padding"] * 1.5
		self.sd["popup"]["p_scv"].size = (xscat, self.gd["p_height"])
		self.sd["popup"]["p_scv"].x = -self.sd["padding"] * 2
		self.sd["popup"]["stack"].size = self.sd["popup"]["p_scv"].size

		if "Restart" not in self.gd["p_c"] and "Download" not in self.gd["p_c"]:
			if "sspace" in self.gd["p_l"]:
				self.gd["p_l"].remove("sspace")
			nx, ns = self.get_index_stack(self.gd["p_l"], self.gd["p_hand"])
			if nx:
				self.gd["p_l"].insert(nx, "sspace")
				self.sd["popup"]["sspace"].size = (self.sd["popup"]["sspace"].size_o[0] * ns + self.sd["padding"], self.sd["popup"]["sspace"].size[1])
			for inx in self.gd["p_l"]:
				if "sspace" in inx:
					try:
						self.sd["popup"]["stack"].add_widget(self.sd["popup"][inx])
					except WidgetException:
						pass
				elif inx == "arrow":
					self.sd["popup"]["stack"].add_widget(self.sd["popup"]["icon"])
					self.sd["popup"]["icon"].source = f"atlas://{img_in}/other/arrow"
				elif inx in icon:
					self.sd["popup"]["stack"].add_widget(self.sd["popup"]["icon"])
					self.sd["popup"]["icon"].source = f"atlas://{img_in}/other/{inx}"
				else:
					self.cpop[inx].selected_c(False)
					self.cpop[inx].update_text()
					self.sd["popup"]["stack"].add_widget(self.cpop[inx])
			if "arrow" in self.gd["p_l"]:
				self.gd["p_l"].remove("arrow")
		self.sd["popup"]["popup"].open()

	def joke(self, player, a=""):
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
		self.gd["confirm_pop"] = False
		self.popup_clr()

		if self.gd["rev"]:
			player = self.gd["opp"]
		else:
			player = self.gd["active"]

		if "pay" in self.gd["ability_doing"]:
			self.gd["paypop"] = True


		if btn.cid == "" or btn.cid == "0":

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
			elif "estock" in self.gd["confirm_trigger"]:
				self.gd["estock_pop"] += "_2"
				ind, st, _ = self.gd["estock_pop"].split("_")
				self.play([ind, st, ""])
			elif "AUTO" in self.gd["confirm_trigger"] or "Event" in self.gd["confirm_trigger"] or "Play" in self.gd["confirm_trigger"]:
				self.gd["confirm1"] = [True, 0]
				if self.net["game"]:
					self.net["act"][5] = 0
				if "dont" in self.gd["effect"]:
					self.gd["ability_effect"].append("dont")
				if "unli" in self.gd["per_poped"] and self.gd["per_poped"][-1]:
					self.gd["per_poped"][-1] = 0
				if "Play" in self.gd["confirm_trigger"]:
					self.gd["waiting_cost"][2] = 2
					if self.net["game"]:
						self.net["act"][5] = 2
					ind, st = self.gd["waiting_cost"][1].split("_")
					self.play([ind, st[:-1], st[-1]])
				else:
					Clock.schedule_once(self.ability_effect)
			elif "ACT" in self.gd["confirm_trigger"] or "Character" in self.gd["confirm_trigger"]:
				if self.net["game"] and self.gd["active"] == "1":
					self.net["act"][0] = ""
				Clock.schedule_once(self.play_card_done)
			elif "Counter" in self.gd["confirm_trigger"]:
				Clock.schedule_once(self.counter_step_done)
		elif btn.cid == "1":
			if "Overplay" in self.gd["confirm_trigger"]:
				self.play(self.gd["play"])
			elif "Dismantle" in self.gd["confirm_trigger"]:
				self.popup_text("Loading")
				del sd[self.decks["selected"][1:]]
				del scej[self.decks["selected"][1:]]
				self.gd["update_edata"] = False
				Clock.schedule_once(self.update_edata)
				Clock.schedule_once(self.wait_update, move_dt_btw)
			elif "Restart" in self.gd["confirm_trigger"]:
				self.reset()
			elif "Download" in self.gd["confirm_trigger"]:
				self.net["var"][1] = 1
				self.decks["sets"].dismiss()
				self.multiplay_cjpopup()
				self.mcreate_popup.open()
				Clock.schedule_once(partial(self.mconnect, "down"), move_dt_btw)
			elif "astock" in self.gd["confirm_trigger"]:
				self.gd["mstock"][0] = ""
				Clock.schedule_once(partial(self.pay_mstock, "as"))
			elif "estock" in self.gd["confirm_trigger"]:
				self.gd["estock_pop"] += "_1"
				self.gd["mstock"][0] = ""
				Clock.schedule_once(partial(self.pay_mstock, "es"))
			elif "AUTO" in self.gd["confirm_trigger"] or "Event" in self.gd["confirm_trigger"] or "Play" in self.gd["confirm_trigger"]:
				if "Play" in self.gd["confirm_trigger"]:
					self.gd["waiting_cost"][2] = 1
				self.gd["confirm_result"] = btn.cid
				self.gd["confirm1"] = [True, 1]
				if self.net["game"] and "confirmbefore" not in self.gd["effect"]:
					self.net["act"][5] = 1
				Clock.schedule_once(self.pay_condition)
			elif "ACT" in self.gd["confirm_trigger"]:
				if self.net["game"] and self.gd["active"] == "1":
					self.net["act"][5] = 1
					self.net["send"] = False
				self.gd["confirm_trigger"] = ""
				Clock.schedule_once(self.pay_condition)
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

			self.gd["active"] = str(self.gd["starting_player"])
			self.gd["opp"] = str(self.gd["second_player"])

			self.change_active_background()

			for _ in self.pd[self.gd["second_player"]]["done"]:
				self.pd[self.gd["second_player"]]["done"][_] = True
			self.pd[self.gd["second_player"]]["done"]["Mulligan"] = False
			self.pd[self.gd["starting_player"]]["done"]["Janken"] = True
			self.gd["mulligan"] = [[], []]
			Clock.schedule_once(self.draw_both, ability_dt)
			self.sd["janken"]["popup"].dismiss()
		elif self.gd["j_result"] != 0:
			self.gd["janken_result"] = int(self.gd["j_result"])
			self.sd["janken"]["popup"].dismiss()
			Clock.schedule_once(self.janken)
		else:
			self.janken_reset()

	def janken_reset(self, *args):
		for _ in self.gd["janken_choice"][1:]:
			self.sd["janken"][f"j{_}1"].show_back()
			self.sd["janken"][f"j{_}0"].show_front()
			self.sd["janken"][f"j{_}0"].disabled = False

		self.gd["j_hand"] = ""
		self.gd["j_hand_opp"] = ""
		self.sd["janken"]["button"].disabled = True
		self.sd["janken"]["button"].text = "Choose One"

	def janken_pick(self, btn):
		self.gd["j_hand"] = str(btn.cid)

		for _ in self.gd["janken_choice"]:
			self.sd["janken"][f"j{_}0"].disabled = True
			if _ != self.gd["j_hand"]:
				self.sd["janken"][f"j{_}0"].show_back()

		if self.net["game"]:
			Clock.schedule_once(partial(self.popup_text, "waiting"), ability_dt)
			self.mconnect("janken")
		else:
			Clock.schedule_once(self.janken_results)

	def janken_results(self, *args):
		if not self.net["game"]:  
			self.gd["j_hand_opp"] = choice(self.gd["janken_choice"][1:])

		self.sd["janken"][f"j{self.gd['j_hand_opp']}1"].show_front()

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

		self.sd["janken"]["button"].disabled = False

	def cardnum_pick(self, btn):
		self.sd["popup"]["popup"].dismiss()
		self.gd["popup_pop"] = False
		if "Numbers" in self.gd["p_c"] and self.gd["numbers"] == "":
			if "any" in self.gd["effect"]:
				self.gd["numbers"] = self.sd["popup"]["digit"].text
			else:
				self.gd["numbers"] = str(btn.cid)
			ind = self.gd["ability_trigger"].split("_")[1]
			if self.net["game"] and "oppturn" in self.gd["effect"] and ind[-1] == "2":
				self.net["var"] = str(self.gd["numbers"])
				self.net["var1"] = "numbers"
				if not self.poptext:
					Clock.schedule_once(partial(self.popup_text, "waitingser"))
				self.mconnect("plturn")
				return False
			else:
				self.cardnum()

	def cardnum(self, dt=0):
		if self.gd["p_c"] == "" and self.gd["numbers"] == "":
			self.sd["popup"]["popup"].title = "Declare a number"
			ind = self.gd["ability_trigger"].split("_")[1][-1]
			self.gd["confirm_var"] = {"o": ind, "c": "Numbers", "m": 1}
			self.popup_start()
		else:
			self.gd["p_c"] = ""
			if "numbers" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("numbers")

			if "do" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("do")

			if "do" in self.gd["effect"] and self.gd["do"][0] > 0:
				self.gd["done"] = True

			if "if" in self.gd["effect"]:
				self.gd["done"] = False
				if "ifpowerrevealvsdeclare" in self.gd["effect"]:
					if "if=" in self.gd["effect"] and self.cd[self.gd["resonance"][1][0]].power_t == int(self.gd["numbers"]):
						self.gd["done"] = True
			if "nowreveal" in self.gd["effect"] and self.gd["resonance"][0]:
				for _ in self.gd["resonance"][1]:
					if self.cd[_].back:
						self.cd[_].show_front()
				self.popup_multi_info(cards=self.gd["resonance"][1], owner=_[-1], t="Reveal")
			else:
				self.ability_effect()

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
				times = 0
				stage = []
				if "xStage" in self.gd["effect"]:
					stage = [_ for _ in self.pd[opp]["Center"] + self.pd[opp]["Back"] if _ != ""]

				if "xTrait" in self.gd["effect"]:
					traits = self.gd["effect"][self.gd["effect"].index("xTrait") + 1].split("_")
					times = len([_ for _ in stage if any(tr in self.cd[_].trait_t for tr in traits)])
				self.gd["effect"][0] = int(times)
			elif self.gd["effect"][0] == "x":
				if "xopp" in self.gd["effect"]:
					self.gd["effect"][0] = len(self.cont_cards(["opp"], idm))
			c = "Look"
			self.sd["btn"]["draw_btn"].disabled = False
			qty = 0
			if "reorder" in self.gd["effect"] and "waiting" not in self.gd["effect"] and "bdeck" not in self.gd["effect"]:
				qty = self.gd["effect"][0]
				c += "_reorder"
			if "top" in self.gd["effect"] and "waiting" in self.gd["effect"]:
				qty = self.gd["effect"][0]
			elif "top" in self.gd["effect"] and isinstance(self.gd["effect"][self.gd["effect"].index("top") + 1], int):
				qty = self.gd["effect"][self.gd["effect"].index("top") + 1]
				if "choosestage" in self.gd["effect"]:
					self.gd["search_type"] = self.gd["effect"][self.gd["effect"].index("top") + 2]
			elif "bottom" in self.gd["effect"] and "top" not in self.gd["effect"] and isinstance(self.gd["effect"][self.gd["effect"].index("bottom") + 1], int):
				qty = self.gd["effect"][self.gd["effect"].index("bottom") + 1]
			elif "hand" in self.gd["effect"]:
				qty = self.gd["effect"][self.gd["effect"].index("hand") + 1]
				self.gd["search_type"] = self.gd["effect"][self.gd["effect"].index("hand") + 2]
				c += "_hand"
				if "stacked" in self.gd["effect"]:
					c += "_stacked"
			elif "waiting" in self.gd["effect"]:
				qty = self.gd["effect"][self.gd["effect"].index("waiting") + 1]
				c += "_waiting"
			elif "clock" in self.gd["effect"]:
				qty = self.gd["effect"][self.gd["effect"].index("clock") + 1]
				self.gd["search_type"] = self.gd["effect"][self.gd["effect"].index("clock") + 2]
				c += "_clock"
			elif "look" in self.gd["effect"]:
				c += "_look_auto"
			elif "stack" in self.gd["effect"]:
				c += "_stack"
				qty = list(self.gd["effect"][self.gd["effect"].index("stack") + 1])
			elif "treorder" in self.gd["effect"] or "breorder" in self.gd["effect"]:
				qty = self.gd["effect"][0]
				c += "_reorder"

			if "fix" in self.gd["effect"]:
				c += "_fix"
			if self.gd["clear"]:
				self.gd["p_l"] = []
			self.sd["popup"]["popup"].title = f"{self.gd['ability_trigger'].split('_')[0]} Effect"
			self.gd["confirm_var"] = {"o": opp, "c": c, "m": qty, "l": self.gd["effect"][0]}
			Clock.schedule_once(self.popup_start, move_dt_btw)
		elif not self.gd["target"]:  
			if self.net["game"] and "looktopopp" in self.gd["effect"] and not self.net["send"]:
				self.net["var"] = list(self.gd["chosen"])
				self.net["var1"] = "oppchoose"
				if not self.poptext:
					Clock.schedule_once(partial(self.popup_text, "waitingser"))
				self.mconnect("oppchoose")
				return False
			else:
				if "sspace" in self.gd["p_l"]:
					self.gd["p_l"].remove("sspace")
				if "done" not in self.gd["p_c"]:
					if "reorder" in self.gd["p_c"]:
						self.gd["target_temp"].append("r")
					else:
						self.gd["target_temp"].append(btn)
					if btn is not None and btn == "l":
						self.gd["target_temp"].append(len(self.gd["p_l"]))
						self.gd["target_temp"].append(len(self.gd["chosen"]))
						chosen = list(self.gd["chosen"])
						if len(chosen) < len(self.gd["p_l"]):
							for _ in range(len(self.gd["p_l"]) - len(chosen)):
								if "reorder" in self.gd["effect"] and "waiting" in self.gd["effect"] and "waity" not in self.gd["effect"]:
									chosen.append("R")
								elif "treorder" in self.gd["effect"] or "breorder" in self.gd["effect"]:
									chosen.append("R")
								elif "shuff" in self.gd["effect"]:
									chosen.append("D")
								elif "stacked" in self.gd["effect"]:
									chosen.append("D")
								elif "stack" in self.gd["effect"]:
									chosen.append("S")
								else:
									chosen.append("W")
						for _ in chosen:
							self.gd["target_temp"].append(_)
				if ("reorder" in self.gd["effect"] and "waiting" in self.gd["effect"] and "reorder" not in self.gd["p_c"]) or (("treorder" in self.gd["effect"] or "breorder" in self.gd["effect"]) and "reorder" not in self.gd["p_c"]):
					if len(self.gd["p_l"]) > len(self.gd["chosen"]):
						for _ in self.gd["chosen"]:
							if _ in self.gd["p_l"]:
								self.gd["p_l"].remove(_)
						if "opp" in self.gd["effect"] and idm[-1] == "1":
							opp = "2"
						elif "opp" in self.gd["effect"] and idm[-1] == "2":
							opp = "1"
						else:
							opp = idm[-1]
						self.gd["uptomay"] = False
						self.sd["btn"]["draw_btn"].disabled = True
						self.sd["btn"]["Look_btn"].disabled = True
						self.gd["confirm_var"] = {"o": opp, "c": "Look_reorder_fix", "m": len(self.gd["p_l"]), "l": len(self.gd["p_l"])}
						Clock.schedule_once(self.popup_start, move_dt_btw)
						return False
					else:
						self.gd["p_c"] = "Look_reorder_fix_done"
				else:
					self.gd["p_c"] = "Look_"
					for _ in range(len(self.gd["target_temp"])):
						_ = self.gd["target_temp"].pop(0)
						self.gd["target"].append(_)
				if self.net["game"] and self.gd["p_owner"] == "1" and not self.gd["oppchoose"]:
					for _ in self.gd["target"]:
						self.net["act"][4].append(_)
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
				top = self.pd[idm[-1]]["Library"].pop(-1)
				if "opp" in self.gd["effect"]:
					if idm[-1] == "1":
						top = self.pd["2"]["Library"].pop(-1)
					elif idm[-1] == "2":
						top = self.pd["1"]["Library"].pop(-1)

				if "bottom" in self.gd["effect"]:
					self.pd[top[-1]]["Library"].insert(0, top)
					self.stack(top[-1])
				elif "waiting" in self.gd["effect"]:
					self.mat[top[-1]]["mat"].remove_widget(self.cd[top])
					self.mat[top[-1]]["mat"].add_widget(self.cd[top])
					self.cd[top].setPos(field=self.mat[top[-1]]["field"]["Waiting"], t="Waiting")
					self.pd[top[-1]]["Waiting"].append(top)
				self.look_top_done()
			elif "r" in item:
				d = self.gd["target"].pop(0)
				c = self.gd["target"].pop(0)
				for n in reversed(range(int(d))):
					ind = self.gd["target"].pop(n)
					if ind in self.emptycards:
						continue
					if ind == "W":
						if "top" in self.gd["effect"]:
							ind = str(self.pd[self.gd["p_owner"]]["Library"][-(n + 1)])
						elif "bottom" in self.gd["effect"]:
							ind = str(self.pd[self.gd["p_owner"]]["Library"][n])
						self.pd[ind[-1]]["Library"].remove(ind)
						self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Waiting"], t="Waiting")
						self.pd[ind[-1]]["Waiting"].append(ind)
					else:
						if "breorder" in self.gd["effect"]:
							self.gd["target_temp"].append(ind)
						else:
							self.pd[ind[-1]]["Library"].remove(ind)
							self.pd[ind[-1]]["Library"].append(ind)
					if "breorder" not in self.gd["effect"]:
						self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
						self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])
					self.update_field_label()
				if "breorder" in self.gd["effect"]:
					ind = ""
					for _ in range(len(self.gd["target_temp"])):
						ind = self.gd["target_temp"].pop(-1)
						self.pd[ind[-1]]["Library"].remove(ind)
						self.pd[ind[-1]]["Library"].insert(0, ind)
					self.stack(ind[-1])
				self.look_top_done()
			elif "l" in item:
				d = self.gd["target"].pop(0)
				c = self.gd["target"].pop(0)
				s = []
				for n in range(int(d)):
					ind = self.gd["target"].pop(0)
					if ind in self.emptycards:
						continue
					if ind == "W":
						for rr in range(d):
							if "top" in self.gd["effect"]:
								ind = str(self.pd[self.gd["p_owner"]]["Library"][-(rr + 1)])
							elif "bottom" in self.gd["effect"]:
								ind = str(self.pd[self.gd["p_owner"]]["Library"][rr])
							if ind not in self.gd["skip_top"]:
								break
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
						if len(s) > 0:
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
							if "extra" in self.gd["effect"]:
								if ind not in self.gd["extra"]:
									self.gd["extra"].append(ind)
							if "hand" in self.gd["effect"]:
								self.pd[ind[-1]]["Library"].remove(ind)
								if "extrareveal" in self.gd["effect"]:
									library = self.mat[ind[-1]]["field"]["Library"]
									self.cd[ind].show_front()
									self.cd[ind].setPos(library[0] - self.sd["padding"] / 4 - self.sd["card"][0], library[1] - self.sd["card"][1] / 3. * len(self.pd[ind[-1]]["Res"]), t="Res")
									self.pd[ind[-1]]["Res"].append(ind)
								else:
									self.pd[ind[-1]]["Hand"].append(ind)
									self.hand_size(ind[-1])
								self.update_field_label()
								self.gd["search_type"] = ""
								if "show" in self.gd["effect"]:
									self.gd["show"].append(ind)
								self.gd["if"].append(ind)
							elif "clock" in self.gd["effect"]:
								self.pd[ind[-1]]["Library"].remove(ind)
								self.pd[ind[-1]]["Clock"].append(ind)
								self.update_field_label()
								self.clock_size(ind[-1])
								self.gd["search_type"] = ""
								self.gd["if"].append(ind)
							elif "waiting" in self.gd["effect"]:
								self.pd[ind[-1]]["Library"].remove(ind)
								self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Waiting"], t="Waiting")
								self.pd[ind[-1]]["Waiting"].append(ind)
								self.update_field_label()
							elif "tdeck" in self.gd["effect"]:
								self.gd["target_temp"].append(ind)
							elif "bdeck" in self.gd["effect"]:
								self.pd[ind[-1]]["Library"].remove(ind)
								self.pd[ind[-1]]["Library"].insert(0, ind)
								self.stack(ind[-1])
							elif "stack" in self.gd["effect"]:
								if len(self.gd["stacked"]["0"]) <= 0:
									self.gd["stacked"]["0"].append([])
								self.gd["stacked"]["0"][0].append(ind)
								self.gd["stacked"][ind] = 0
							else:
								self.gd["skip_top"].append(ind)

				if "tdeck" in self.gd["effect"] and len(self.gd["target_temp"]) > 0:
					ind = ""
					for n in range(len(self.gd["target_temp"])):
						ind = self.gd["target_temp"].pop(-1)
						self.pd[ind[-1]]["Library"].remove(ind)
						self.pd[ind[-1]]["Library"].append(ind)
					self.stack(ind[-1])

				if len(self.gd["target"]) > 0:
					self.look_top(btn)
				elif "shuff" in self.gd["effect"]:
					self.gd["shuffle_trigger"] = "looktop"
					if self.net["game"]:
						self.gd["shuffle_send"] = True
					if "opp" in self.gd["effect"] and idm[-1] == "1":
						self.shuffle_deck("2")
					elif "opp" in self.gd["effect"] and idm[-1] == "2":
						self.shuffle_deck("1")
					else:
						self.shuffle_deck(idm[-1])
				elif len(self.pd[idm[-1]]["Library"]) <= 0:
					self.gd["reshuffle_trigger"] = "looktop"
					self.gd["rrev"] = idm[-1]
					Clock.schedule_once(self.refresh, move_dt_btw)
					return False
				else:
					self.look_top_done()

	def look_top_done(self, dt=0):
		self.check_cont_ability()
		self.update_field_label()
		if "looktop" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("looktop")

		self.popup_clr()
		player = ""
		if "show" in self.gd["effect"] and len(self.gd["show"]) > 0:
			for _ in self.gd["show"]:
				player = _[-1]

		if "do" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("do")
		ind = self.gd["ability_trigger"].split("_")[1]
		if "if" in self.gd["effect"]:
			self.gd["done"] = True
			if "ifLevel" in self.gd["effect"] and all(self.cd[cc].level_t < self.gd["effect"][self.gd["effect"].index("ifLevel") + 1] for cc in self.gd["if"]):
				self.gd["done"] = False
			if "ifMemory" in self.gd["effect"]:
				if "iflower" in self.gd["effect"] and len(self.cont_cards(["Memory"], ind)) > self.gd["effect"][self.gd["effect"].index("if") + 1]:
					self.gd["done"] = False
				elif "iflower" not in self.gd["effect"] and len(self.cont_cards(["Memory"], ind)) < self.gd["effect"][self.gd["effect"].index("if") + 1]:
					self.gd["done"] = False
			else:
				if "iflower" not in self.gd["effect"] and len(self.gd["if"]) < self.gd["effect"][self.gd["effect"].index("if") + 1]:
					self.gd["done"] = False
			self.gd["if"] = []
		elif "do" in self.gd["effect"] and self.gd["do"][0] > 0:
			self.gd["done"] = True

		self.gd["skip_top"] = []
		ind = self.gd["ability_trigger"].split("_")[1]
		if "check" in self.gd["effect"] and ind[-1] == "1":
			self.popup_multi_info(cards=[self.pd[ind[-1]]["Library"][-1]], owner=ind[-1], t="top card")
		elif player == "2" and "show" in self.gd["effect"] and len(self.gd["show"]) > 0:
			self.popup_multi_info(cards=self.gd["show"], owner=player, t="Search")
		else:
			if "deck" in self.gd["effect"]:
				self.gd["shuffle_trigger"] = "ability"
				if self.net["game"]:
					self.gd["shuffle_send"] = True
				self.shuffle_deck(ind[-1])
			else:
				Clock.schedule_once(self.ability_effect, move_dt_btw)

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
					if "top" in self.gd["effect"]:
						self.gd["p_l"].append(self.pd[self.gd["p_owner"]]["Library"][-(pl + 1)])
					elif "bottom" in self.gd["effect"]:
						self.gd["p_l"].append(self.pd[self.gd["p_owner"]]["Library"][pl])
					self.gd["p_t"] = list(self.gd["p_t"])
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
			self.shelve_save()

	def info_ability_pop(self, btn):
		self.cardinfo.import_data(self.cd[self.gd["ability_trigger"].split("_")[1]], annex_img,self.gd["DLimg"])

	def play_card(self, *args):
		self.sd["btn"]["end"].disabled = True
		self.sd["btn"]["end_attack"].disabled = True
		self.sd["btn"]["end_phase"].disabled = True
		self.act_ability_show(hide=True)
		card = self.cd[self.gd["play_card"]]

		if self.net["game"] and not self.net["send"] and self.gd["active"] == "1":
			if card.card == "Event":
				self.net["var"] = [card.ind, card.pos_new, "",self.gd["estock_payed"]]
			else:
				self.net["var"] = [card.ind, card.pos_new[:-1], card.pos_new[-1]]
			self.net["var1"] = "play_card"
			if not self.poptext:
				Clock.schedule_once(partial(self.popup_text, "waitingser"))
			self.mconnect("phase")
		else:
			if card.card == "Character":
				self.gd["ability_trigger"] = f"Character_{card.ind}"
				Clock.schedule_once(self.stack_ability)
			elif card.card == "Event":
				self.gd["ability_trigger"] = f"Event_{card.ind}"
				if card.text_c[0][0].startswith(cont_ability) and len(card.text_c) > 1:
					self.gd["effect"] = ab.event(card.text_c[1][0])
				else:
					self.gd["effect"] = ab.event(card.text_c[0][0])
				self.gd["ability"] = card.text_c[0][0]
				self.gd["pay"] = ab.pay(a=self.gd["ability"])
				if self.gd["pay"]:
					self.gd["payed"] = False
				else:
					self.gd["payed"] = True
				self.check_auto_ability(play=card.ind, stacks=False)
				if "more" in self.gd["effect"]:
					aa = self.check_more(self.gd["effect"], card.ind)
					done = []
					if "done" in self.gd["effect"]:
						done = self.gd["effect"][self.gd["effect"].index("done") + 1]
					if aa:
						self.gd["effect"] = self.gd["effect"][self.gd["effect"].index("do") + 1]
					else:
						self.gd["effect"] = []
					if done:
						self.gd["effect"].extend(["done", done])

				if self.net["game"]:
					if card.ind[-1] == "1":
						self.net["act"] = ["e", card.ind, 0, [], [], 0, -1]
						self.net["send"] = False
						self.ability_event()
					elif card.ind[-1] == "2" and self.gd["active"] == "1" and self.gd["phase"] == "Counter":
						if self.gd["show_wait_popup"]:
							Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
						self.mconnect("counter")
					elif card.ind[-1] == "2":
						if self.gd["show_wait_popup"]:
							Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
						self.mconnect("phase")
				else:
					self.ability_event()

	@staticmethod
	def add_to_status(stat, eff):
		if "Opp" in eff:
			stat = f"Opp{stat}"
		if "top" in eff and "heal" in eff:
			stat = f"Top{stat}"
		if "OpponentOpposite" in eff:
			stat = f"Onentsite{stat}"
		elif "Opposite" in eff:
			stat = f"Osite{stat}"
		if "Change" in eff:
			stat = f"Change{stat}"
		if "Battle" in eff:
			if "both" in eff:
				stat = f"BBattleBoth{stat}"
			elif "opp" in eff:
				stat = f"BBattleBopp{stat}"
			else:
				stat = f"BBattle{stat}"
		elif "Middle" in eff:
			stat = f"Middle{stat}"
		elif "Center" in eff:
			stat = f"Center{stat}"
		elif "Back" in eff:
			stat = f"Back{stat}"
		elif "Another" in eff:
			stat = f"Another{stat}"
		if "Climax" in eff:
			stat = f"Climax{stat}"
		if "This" in eff:
			stat = f"This{stat}"
		if "Standing" in eff or "Stand" in eff:
			stat = f"Stand{stat}"
		elif "Reverse" in eff:
			stat = f"Reverse{stat}"
		if "Antilvl" in eff:
			stat = f"Antilvl{stat}"
		if "Open" in eff:
			stat = f"Open{stat}"
		if "Other" in eff:
			stat = f"Other{stat}"
		if "Cost" in eff:
			stat = f"Cost{eff[eff.index('Cost') + 1]}{stat}"
		if "Level" in eff:
			stat = f"Level{eff[eff.index('Level') + 1]}{stat}"
		if "ZMarkers" in eff:
			if "ZMlower" in eff:
				stat = f"Markers<={eff[eff.index('ZMarkers') + 1]}{stat}"
		if "BTraitN" in eff:
			stat = f"BTraitN_{eff[eff.index('BTraitN') + 1]}_{stat}"
		elif "BTrait" in eff:
			stat = f"BTrait_{eff[eff.index('BTrait') + 1]}_{stat}"
		elif "TraitN" in eff:
			stat = f"TraitN_{eff[eff.index('TraitN') + 1]}_{stat}"
		elif "Trait" in eff:
			stat = f"Trait_{eff[eff.index('Trait') + 1]}_{stat}"
		elif "NameSet" in eff:
			stat = f"NameSet_{eff[eff.index('NameSet') + 1]}_{stat}"
		elif "ZMName=" in eff:
			stat = f"Name=_{eff[eff.index('ZMName=') + 1]}_{stat}"
		elif "Name=" in eff:
			stat = f"Name=_{eff[eff.index('Name=') + 1]}_{stat}"
		elif "NameO" in eff:
			stat = f"NameO_{eff[eff.index('NameO') + 1]}_{stat}"
		elif "Name" in eff:
			stat = f"Name_{eff[eff.index('Name') + 1]}_{stat}"
		elif "Text" in eff:
			stat = f"Text_{eff[eff.index('Text') + 1]}_{stat}"
		elif "ColourWo" in eff:
			stat = f"ColourWo_{eff[eff.index('ColourWo') + 1]}_{stat}"
		elif "Colour" in eff:
			stat = f"Colour_{eff[eff.index('Colour') + 1]}_{stat}"
		return stat

	def ability_event(self, dt=0, m=""):

		self.gd["chosen"] = []
		self.gd["target"] = []
		self.gd["choose"] = False

		if self.gd["effect"] and isinstance(self.gd["effect"][0], int):
			if self.gd["effect"][0] > 0 and not self.gd["choose"]:
				self.gd["status"] = self.add_to_status(f"Select{self.gd['effect'][0]}", self.gd["effect"])

		self.gd["uptomay"] = False
		if ("may" in self.gd["effect"] and "may not" not in self.gd["effect"]) or "upto" in self.gd["effect"]:
			self.gd["uptomay"] = True
			self.gd["confirm1"] = [False, 0]
			self.gd["confirm_result"] = ""
		if not self.gd["payed"]:
			self.gd["confirm1"] = [False, 0]
			self.gd["confirm_result"] = ""

		if "stock" in self.gd["effect"]:
			self.gd["stock"] = self.gd["effect"][self.gd["effect"].index("stock") + 1]
			self.gd["ability_effect"].append("stock")

		if "draw" in self.gd["effect"] and "Trigger" not in self.gd["effect"]:
			self.gd["ability_effect"].append("draw")
		if "pay" in self.gd["effect"] and not m:
			if "ACT" not in self.gd["ability_trigger"] and self.gd["paypop"]:
				self.gd["paypop"] = False
			if "do" in self.gd["effect"] and "confirmpayafter" in self.gd["effect"][self.gd["effect"].index("do")+1]:
				self.gd["effect"].append("confirmbefore")
			self.gd["ability_effect"].append("pay")
		elif "d_atk" in self.gd["effect"]:
			self.gd["d_atk"][0] = self.gd["effect"][1]
		elif "escanor" in self.gd["effect"]:
			self.gd["attacking"].extend(self.gd["effect"])
			self.gd["effect"] = []
		elif "trigger" in self.gd["effect"]:
			self.gd["trigger"] = self.gd["effect"][1]
		elif "drawupto" in self.gd["effect"]:
			self.gd["draw_upto"] = self.gd["effect"][self.gd["effect"].index("drawupto") + 1]
			if self.gd["draw_upto"] == "x":
				if "xdeclare+" in self.gd["effect"]:
					self.gd["effect"][1] = int(self.gd["numbers"]) + self.gd["effect"][self.gd["effect"].index("xdeclare+") + 1]
				elif "xdeclare*" in self.gd["effect"]:
					self.gd["effect"][1] = int(self.gd["numbers"]) * self.gd["effect"][self.gd["effect"].index("xdeclare*") + 1]
				self.gd["draw_upto"] = self.gd["effect"][1]

			if self.gd["draw_upto"] > 0:
				self.gd["ability_effect"].append("drawupto")
		elif "confirm" in self.gd["effect"]:
			self.gd["confirm1"] = [False, 0]
			if self.net["game"]:
				self.net["send"] = False
			self.gd["ability_effect"].append("confirm")
		elif "perform" in self.gd["effect"]:
			self.gd["ability_effect"].append("perform")
			self.gd["per_poped"] = [0, "", [], 0, -1, 0]
			self.gd["ability"] = str(self.gd["effect"][2])
		elif "numbers" in self.gd["effect"]:
			self.gd["ability_effect"].append("numbers")
			self.gd["numbers"] = ""
			self.sd["popup"]["digit"].text = "0"
		elif "mill" in self.gd["effect"]:
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
			self.gd["show"] = []
			if self.net["game"] and "looktopopp" in self.gd["effect"]:
				self.net["send"] = False
			self.gd["ability_effect"].append("looktop")
		elif "discard" in self.gd["effect"] or "ldiscard" in self.gd["effect"] or "cdiscard" in self.gd["effect"] or "mdiscard" in self.gd["effect"] or "cxdiscard" in self.gd["effect"]:
			self.gd["discard"] = int(self.gd["effect"][1])
			self.gd["search_type"] = self.gd["effect"][2]
			self.gd["ability_effect"].append("discard")
		elif "brainstorm" in self.gd["effect"]:
			self.gd["ability_effect"].append("brainstorm")
		elif "rescue" in self.gd["effect"] or "return" in self.gd["effect"]:
			self.gd["ability_effect"].append("rescue")
		elif "reveal" in self.gd["effect"]:
			self.gd["ability_effect"].append("reveal")
		elif "look" in self.gd["effect"]:
			self.gd["ability_effect"].append("look")
		elif "janken" in self.gd["effect"]:
			self.gd["ability_effect"].append("janken")
			self.gd["janken_result"] = 0
		elif "move" in self.gd["effect"]:  
			self.gd["move"] = ""
			self.gd["ability_effect"].append("move")
		elif "hander" in self.gd["effect"] or "wind" in self.gd["effect"]:
			self.gd["ability_effect"].append("hander")
		elif "stocker" in self.gd["effect"]:
			self.gd["ability_effect"].append("stocker")
		elif "decker" in self.gd["effect"]:
			if "same_name" in self.gd["effect"]:
				self.same_name_check()
			self.gd["ability_effect"].append("decker")
		elif "waitinger" in self.gd["effect"]:
			self.gd["ability_effect"].append("waitinger")
		elif "clocker" in self.gd["effect"]:
			self.gd["ability_effect"].append("clocker")
		elif "memorier" in self.gd["effect"]:
			self.gd["ability_effect"].append("memorier")
		elif "shuffle" in self.gd["effect"]:
			self.gd["ability_effect"].append("shuffle")
		elif "salvage" in self.gd["effect"] or "csalvage" in self.gd["effect"] or "msalvage" in self.gd["effect"] or "ksalvage" in self.gd["effect"]:
			self.gd["search_type"] = self.gd["effect"][2]
			self.gd["salvage"] = self.gd["effect"][0]
			self.gd["ability_effect"].append("salvage")
		elif "search" in self.gd["effect"] or "stsearch" in self.gd["effect"]:
			self.gd["search"] = self.gd["effect"][0]
			if "EName=" in self.gd["effect"][2] and len(self.gd["extra"]) > 0:
				self.gd["search_type"] = f"{self.gd['effect'][2][1:]}"
				for _ in range(self.gd["search"]):
					temp = self.gd["extra"].pop(0)
					self.gd["search_type"] += f"_{self.cd[temp].name}"
			else:
				self.gd["search_type"] = self.gd["effect"][2]
			if self.net["game"] and "oppturn" in self.gd["effect"]:
				self.net["send"] = False
			self.gd["ability_effect"].append("search")
		elif "declare" in self.gd["effect"]:
			self.gd["ability_effect"].append("declare")
		elif "revive" in self.gd["effect"]:
			self.gd["ability_effect"].append("revive")
		elif "give" in self.gd["effect"]:
			self.gd["ability_effect"].append("give")
		elif "reverser" in self.gd["effect"] or "reverse" in self.gd["effect"]:
			self.gd["ability_effect"].append("reverser")
		elif "heal" in self.gd["effect"]:
			self.gd["ability_effect"].append("heal")
		elif "flipper" in self.gd["effect"]:
			self.gd["ability_effect"].append("flipper")
		elif "marker" in self.gd["effect"] or "markers" in self.gd["effect"]:
			self.gd["p_c"] = ""
			self.gd["ability_effect"].append("marker")
		elif "more" in self.gd["effect"]:
			self.gd["ability_effect"].append("more")
		elif "cards" in self.gd["effect"]:
			self.gd["ability_effect"].append("cards")
		if "power" in self.gd["effect"]:
			if "same_name" in self.gd["effect"]:
				self.same_name_check()
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
			if "multiple" in self.gd["effect"]:
				self.gd["do"][0] = len(self.cont_times(self.gd["effect"], self.cont_cards(self.gd["effect"], self.gd["ability_trigger"].split("_")[1]), self.cd))
				self.gd["done"] = True
			elif self.gd["do"][0] < 1:
				self.gd["do"][0] = 1
		elif self.gd["do_both"]:
			if "do" not in self.gd["ability_effect"]:
				self.gd["ability_effect"].append("do")
			self.gd["do"][0] = 1
			self.gd["do"][1] = list(self.gd["do_both"][0])
			del self.gd["do_both"][0]
			self.gd["done"] = False
		else:
			if self.gd["brainstorm_c"][0] and "perform" in self.gd["effect"]:
				pass
			else:
				self.gd["do"][0] = 0
				self.gd["do"][1] = []
			self.gd["done"] = False
		if "done" in self.gd["effect"]:
			self.gd["do"][2] = list(self.gd["effect"][self.gd["effect"].index("done") + 1])
			self.gd["ability_effect"].append("done")
		if "dont" in self.gd["effect"]:
			self.gd["dont"] = list(self.gd["effect"][self.gd["effect"].index("dont") + 1])

		if self.gd["ability_effect"]:
			Clock.schedule_once(self.shelve_save,ability_dt)
		self.ability_effect()

	def same_name_check(self):
		if self.gd["save_name"][0] != "":
			self.gd["effect"][self.gd["effect"].index("Name=") + 1] = str(self.gd["save_name"][0])
			self.gd["effect"].append("saved_name")
			if "Other_same" in self.gd["effect"]:
				self.gd["effect"][self.gd["effect"].index("Other_same") + 1] = str(self.gd["save_name"][1])
			self.gd["status"] = self.add_to_status(f"Select{self.gd['effect'][0]}", self.gd["effect"])
			self.gd["save_name"] = ["", ""]

	def do_check(self, effect=False, r=False):
		if "do" in self.gd["ability_effect"]:
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
		for p in (self.gd["active"], self.gd["opp"]):
			if self.check_lose(p):
				return False
			if len(self.pd[p]["Library"]) <= 0 and len(self.pd[p]["Clock"]) >= 7:
				self.gd["reflev"] = ["ref", f"lev{p}"]
				if p == "1":
					self.gd["confirm_var"] = {"c": "reflev"}
					Clock.schedule_once(self.confirm_popup, popup_dt)
				elif self.net["game"] and p == "2":
					rule = self.gd["target"].pop(0)
					Clock.schedule_once(partial(self.reflev, rule))
				elif self.gd["com"] and p == "2":
					Clock.schedule_once(partial(self.reflev, choice(("ref", f"lev{p}"))))
				return False
			if len(self.pd[p]["Library"]) <= 0:
				self.gd["trev"] = p
				self.gd["reshuffle_trigger"] = "ability"
				self.gd["rrev"] = p
				Clock.schedule_once(self.refresh, move_dt_btw)
				return False
			if len(self.pd[p]["Clock"]) >= 7:
				self.gd["level_up_trigger"] = "ability"
				Clock.schedule_once(partial(self.level_up, p), move_dt_btw)
				return False

		ind = self.gd["ability_trigger"].split("_")[1]

		if self.net["game"] and self.gd["ability_trigger"] and ind[-1] == "2" and "oppturn" not in self.gd["effect"] and "plchoose" not in self.gd["effect"]:
			self.gd["choose"] = True
			self.gd["p_owner"] = "2"
			self.gd["target"] = self.net["act"][4]

		if self.gd["phase"] != "Encore":
			self.gd["confirm_trigger"] = self.gd["ability_trigger"]

		if self.gd["done"] and self.gd["do"][0] > 0:
			if "do" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("do")
			if "brainstorm" in self.gd["effect"]:
				self.gd["do"][0] += 1
			self.gd["effect"] = list(self.gd["do"][1])
			self.gd["done"] = False
			if self.gd["do"][0] > 0:
				self.gd["do"][0] -= 1
				self.gd["ability_effect"].append("do")
				Clock.schedule_once(self.ability_event)
			else:
				self.ability_effect()
		elif "dont" in self.gd["ability_effect"]:
			self.gd["effect"] = list(self.gd["dont"])
			self.gd["done"] = False
			self.gd["payed"] = True
			self.gd["ability_effect"].remove("dont")
			self.ability_event()
		elif "pay" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "pay"
			if not self.gd["pay"] and self.gd["payed"]:
				self.gd["paypop"] = True
			if self.net["game"] and (ind[-1] == "2" or ("opp" in self.gd["effect"] and ind[-1] == "1")):
				self.gd["ability_effect"].remove("pay")
				if not self.net["act"][5]:
					self.gd["ability_effect"].remove("do")
					self.gd["done"] = False
					if "dont" in self.gd["effect"]:
						self.gd["ability_effect"].append("dont")
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
				if "pass" not in pick:
					self.gd["ability_effect"].remove("pay")
					self.gd["done"] = True
					self.gd["p_owner"] = ind[-1]
					self.pay_condition()
				else:
					self.gd["ability_effect"].remove("pay")
					self.gd["ability_effect"].remove("do")
					if "dont" in self.gd["effect"]:
						self.gd["ability_effect"].append("dont")
					self.ability_effect()
			elif ind[-1] == "1" and "opp" not in self.gd["effect"] and not self.gd["payed"] and self.gd["paypop"]:
				self.gd["ability_effect"].remove("pay")
				self.gd["ability_effect"].remove("do")
				self.gd["confirm_result"] = ""
				if "dont" in self.gd["effect"]:
					self.gd["ability_effect"].append("dont")
				self.ability_effect()
			elif ind[-1] == "1" and "opp" not in self.gd["effect"] and self.gd["payed"] and self.gd["paypop"]:
				self.gd["ability_effect"].remove("pay")
				if "do" in self.gd["ability_effect"]:
					self.gd["ability_effect"].remove("do")
				self.gd["done"] = True
				self.gd["confirm_result"] = ""
				self.ability_effect()
			elif ind[-1] == "1" and "opp" not in self.gd["effect"] and (not self.gd["payed"] or self.gd["uptomay"]) and not self.gd["paypop"]:
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
					if "dont" in self.gd["effect"]:
						self.gd["ability_effect"].append("dont")
					self.ability_effect()
		elif "flipper" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "flipper"

			if self.gd["effect"][0] == 0:
				self.gd["target"].append(ind)
				self.gd["effect"][0] = 1
			elif self.gd["effect"][0] > 0:
				if "ID=" in self.gd["effect"][2]:
					temp = self.gd["effect"][2].split("_")[1:]
					for t in temp:
						self.gd["target"].append(t)

			for r in range(self.gd["effect"][0]):
				_ = self.gd["target"].pop(0)
				if self.net["game"] and ind[-1] == "1" and "oppturn" not in self.gd["effect"]:  
					self.net["act"][4].append(_)
				if _ in self.emptycards:
					continue
				if "down" in self.gd["effect"] and not self.cd[_].back:
					if _[-1] != ind[-1]:
						self.cd[_].show_back(False)
					else:
						self.cd[_].show_back()
				elif "up" in self.gd["effect"] and self.cd[_].back:
					self.cd[_].show_front()

			self.gd["ability_effect"].remove("flipper")
			if "do" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("do")

			self.ability_effect()
		elif "stand" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "stand"
			if self.gd["target"]:
				self.stand()
			elif self.gd["effect"][0] > 0 and not self.gd["choose"]:
				if ind[-1] == "1":
					self.select_card()
					Clock.schedule_once(partial(self.popup_text, "Main"))
				elif ind[-1] == "2" and self.gd["com"]:
					self.gd["p_l"] = self.get_fields()
					pick = self.ai.ability(self.pd, self.cd, self.gd)
					self.gd["choose"] = True
					if "AI_target" in pick:
						for pp in pick[pick.index("AI_target") + 1]:
							self.gd["target"].append(pp)
					else:
						self.gd["notarget"] = True
						for pp in range(self.gd["effect"][0]):
							self.gd["target"].append("")
					self.ability_effect()
			else:
				self.gd["confirm_result"] = ""
				self.stand()
		elif "rest" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "rest"
			if self.gd["target"]:
				self.rest()
			elif self.gd["effect"][0] > 0 and not self.gd["choose"]:
				if ind[-1] == "1":
					if self.net["game"]:
						if self.gd["oppchoose"]:
							self.gd["oppchoose"] = False
							if "plchoose" in self.gd["effect"]:
								self.net["act"][4] = []
						self.net["send"] = False
					Clock.schedule_once(partial(self.popup_text, "Main"), move_dt_btw)
					if "Stand" in self.gd["effect"]:
						self.select_card(s="Stand")
					else:
						self.select_card()
				elif ind[-1] == "2":
					if self.net["game"]:
						if not self.net["send"]:
							self.net["act"][5] = 1
							self.net["var"] = list(self.net["act"])
							self.net["var1"] = "oppchoose"
							if not self.poptext:
								Clock.schedule_once(partial(self.popup_text, "waitingser"))
							self.mconnect("act")
						else:
							if self.gd["show_wait_popup"]:
								Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
							if "plchoose" in self.gd["effect"]:
								if self.gd["oppchoose"]:
									self.gd["oppchoose"] = False
								self.mconnect("plchoose")
							else:
								self.mconnect("oppchoose")
					elif self.gd["com"]:
						pick = self.ai.ability(self.pd, self.cd, self.gd)
						self.gd["choose"] = True
						if pick != "pass":
							for pp in pick[pick.index("AI_target") + 1]:
								self.gd["target"].append(pp)
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


			if self.net["game"] and not self.gd["confirm2"][0]:
				if ind[-1] == "1":
					if not self.gd["confirm1"][0]:
						self.net["send"] = False
					elif not self.net["send"]:
						self.net["var"] = list(self.net["act"])
						self.net["var1"] = "confirm"
						if not self.poptext:
							Clock.schedule_once(partial(self.popup_text, "waitingser"))
						self.mconnect("act")
						return
					else:
						if self.gd["show_wait_popup"]:
							Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
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
			elif self.gd["com"] and not self.gd["confirm2"][0] and ("opp" in self.gd["effect"] or "both" in self.gd["effect"]):
				pick = self.ai.ability(self.pd, self.cd, self.gd)
				if pick != "pass" or not pick:
					if "y" in pick:
						self.gd["confirm2"][1] = True
					elif "n" in pick:
						self.gd["confirm2"][1] = False
				else:
					self.gd["confirm2"][1] = False
				self.gd["confirm2"][0] = True


			if not self.gd["confirm1"][0] and "both" in self.gd["effect"]:
				self.gd["confirm_var"] = {"ind": ind, "c": "confirm"}
				Clock.schedule_once(self.confirm_popup, popup_dt)
				return False
			elif not self.gd["confirm1"][0] and self.gd["active"] == "2" and ind[-1] == "2" and "opp" in self.gd["effect"]:
				self.gd["confirm_var"] = {"ind": ind, "c": "confirm"}
				Clock.schedule_once(self.confirm_popup, popup_dt)
				return False
			elif not self.gd["confirm1"][0] and self.gd["active"] == "1" and ind[-1] == "1" and "opp" in self.gd["effect"]:
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
		elif "numbers" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "numbers"
			if "markers" in self.gd["effect"]:
				m = 1
				if ind in self.pd[ind[-1]]["marker"]:
					m = len(self.pd[ind[-1]]["marker"][ind]) + 1
				self.gd["effect"][1] = range(m)
				if m > 4:
					for rr in range(4, m):
						self.cpop[f"n{rr}"] = CardNum(f"{rr}", self.sd["card"])
						self.cpop[f"n{rr}"].bind(on_release=self.cardnum_pick)
						self.skip_cpop.append(f"n{rr}")
			if self.net["game"] and "oppturn" in self.gd["effect"]:
				if ind[-1] == "1":
					if not self.net["send"]:
						self.net["act"][5] = 1
						self.net["var"] = list(self.net["act"])
						self.net["var1"] = "searchopp"
						if not self.poptext:
							Clock.schedule_once(partial(self.popup_text, "waitingser"))
						self.mconnect("act")
					else:
						if self.gd["show_wait_popup"]:
							Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
						self.mconnect("oppchoose")
				elif ind[-1] == "2":
					if not self.gd["target"]:
						self.gd["p_c"] = ""
					self.cardnum()
			elif self.gd["com"] and ((ind[-1] == "1" and "oppturn" in self.gd["effect"]) or (ind[-1] == "2" and "oppturn" not in self.gd["effect"])):
				self.gd["p_c"] = "Numbers"
				pick = self.ai.ability(self.pd, self.cd, self.gd)

				if "AI_number" in pick:
					inx = pick.index("AI_number")
					self.gd["numbers"] = pick[inx + 1]
				else:
					self.gd["numbers"] = choice(self.gd["effect"][1])
				self.popup_multi_info(cards=[f"n{self.gd['numbers']}"], owner="2", t="Numbers")
			else:
				self.gd["p_c"] = ""
				self.cardnum()
		elif "declare" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "declare"
			if "text" in self.gd["effect"]:
				if "all" in self.gd["effect"]:
					player = list(self.pd.keys())
				else:
					player = [ind[-1]]
				for p in player:
					self.sd["joke"][p].change_texture(self.gd["effect"][self.gd["effect"].index("text") + 1])
					self.sd["joke"][p].center_x = self.mat[p]["mat"].size[0] / 2.
					self.sd["joke"][p].x = self.mat[p]["mat"].x
					self.sd["joke"][p].y = -Window.height

					self.joke(p, "d")
			elif "five" in self.gd["effect"]:
				for player in list(self.pd.keys()):
					if player == "1":
						self.sd["joke"][player].img_src = f"atlas://{img_in}/other/random"
						self.sd["joke"][player].rect.source = f"atlas://{img_in}/other/random"
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
		elif "perform" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "perform"
			if any(_ in self.gd["effect"] for _ in ("unli","xclock/","xsoultriggers","x#trait")):
				if "xclock/" in self.gd["effect"]:
					inx = self.gd["effect"].index("xclock/")
					self.gd["effect"][1] = int(len(self.pd[ind[-1]]["Clock"]) / self.gd["effect"][inx + 1])
					del self.gd["effect"][inx:inx + 2]
				elif "x#trait" in self.gd["effect"]:
					inx = self.gd["effect"].index("x#trait")
					if "xCenter" in self.gd["effect"]:
						self.gd["effect"][1] = int(len(self.cont_times(["Trait",self.gd["effect"][inx+1]], self.cont_cards(["Center"],ind), self.cd)))
				elif "xsoultriggers" in self.gd["effect"]:
					trig = []
					for t in self.gd["extra"]:
						for ts in self.cd[t].trigger:
							if "soul" in ts:
								trig.append(ts)
					self.gd["effect"][1] = len(trig)
					self.gd["effect"].remove("xsoultriggers")

				if self.gd["effect"][1] <= 0:
					self.gd["ability_effect"].remove("perform")
					self.gd["effect"] = []
				if self.gd["effect"]:
					if len(self.gd["effect"][2].split("_")) > 1:
						self.gd["per_poped"] = [ind, self.gd["effect"][2].split("_"), self.gd["effect"][2], 0, self.gd["effect"][1]]
					else:
						self.gd["per_poped"] = [ind, [self.gd["effect"][2]] * self.gd["effect"][1], self.gd["effect"][2], 0, self.gd["effect"][1]]
					if "unli" in self.gd["effect"]:
						self.gd["per_poped"].insert(-1, "unli")
						self.gd["per_poped"][-1] = 99
						self.gd["effect"].remove("unli")
						if "xlvlup" in self.gd["effect"]:
							self.gd["effect"].remove("xlvlup")
							self.gd["per_poped"].insert(-1, "xlvlup")
				self.ability_effect()
			elif self.gd["per_poped"][-1]:
				if self.net["game"] and ind[-1] == "2":
					self.gd["per_poped"][3] = int(self.net["act"][6])
					self.perform_popup_btn(None, a=self.gd["per_poped"][1][self.gd["per_poped"][3]], net=True)
				elif ind[-1] == "2" and self.gd["com"]:
					if self.gd["per_poped"][-1] > 0:
						self.gd["per_poped"][3] = self.gd["per_poped"][1].index(choice(self.gd["per_poped"][1]))
						self.perform_popup_btn(None, self.gd["per_poped"][1][self.gd["per_poped"][3]])
					else:
						self.ability_effect()
				else:
					if len(self.gd["per_poped"][2].split("_")) > 1:
						self.perform_popup(self.gd["per_poped"])
					else:
						self.perform_popup_btn(None, a=self.gd["per_poped"][2])
			elif "both" in self.gd["effect"]:
				first = False
				a = ab.event(self.gd["ability"])
				b = ab.event(self.gd["ability"])
				if "do" in b:
					b.insert(b.index("do"), "oppturn")
					if "do" in b[b.index("do") + 1]:
						b[b.index("do") + 1].insert(b[b.index("do") + 1].index("do"), "oppturn")
						b[b.index("do") + 1][b[b.index("do") + 1].index("do") + 1].append("oppturn")
					else:
						b[b.index("do") + 1].append("oppturn")
				else:
					b.append("oppturn")

				if ind[-1] == "1":
					first = True

				self.gd["do_both"] = []

				if first:
					self.gd["do_both"].append(b)
					self.gd["effect"] = list(a)
				else:
					self.gd["do_both"].append(a)
					self.gd["effect"] = list(b)

				self.gd["ability_effect"].remove("perform")
				self.gd["oppchoose"] = True
				self.gd["perform_both"] = True

				if self.net["game"] and ind[-1] == "1":
					if not self.net["send"]:
						self.net["act"][5] = 1
						self.net["var"] = list(self.net["act"])
						self.net["var1"] = "perform"
						if not self.poptext:
							Clock.schedule_once(partial(self.popup_text, "waitingser"))
						self.mconnect("act")
				else:
					self.ability_event()
			elif "choice" in self.gd["effect"]:
				self.gd["per_poped"] = [ind, self.gd["effect"][2].split("_"), self.gd["effect"][2], -1, "choice", self.gd["effect"][1]]
				self.ability_effect()
			elif "twice" in self.gd["effect"]:
				a = ab.event(self.gd["ability"])
				self.gd["do_both"] = []
				self.gd["do_both"].append(a)
				if "do" in self.gd["effect"]:
					self.gd["do_both"].append(self.gd["effect"][self.gd["effect"].index("do") + 1])

				self.gd["effect"] = list(a)

				self.gd["ability_effect"].remove("perform")
				self.gd["perform_both"] = True
				self.ability_event()
			else:
				self.gd["per_poped"] = [ind, self.gd["effect"][2].split("_"), self.gd["effect"][2], 0, 1]
				self.perform_popup_btn(None, a=self.gd["effect"][2])
		elif "more" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "more"
			idm = ind[-1]
			if self.gd["perform_both"]:
				if "oppturn" in self.gd["effect"]:
					if ind[-1] == "1":
						idm = "2"
					elif ind[-1] == "2":
						idm = "2"
				else:
					if ind[-1] == "2":
						idm = "1"
					elif ind[-1] == "1":
						idm = ind[-1]

			mm = self.check_more(self.gd["effect"], ind, idm)

			self.gd["ability_effect"].remove("more")
			if "do" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("do")

			if mm:
				self.gd["done"] = True
				self.ability_effect()
			elif not mm:
				self.gd["done"] = False
				if self.gd["do_both"]:
					self.gd["effect"] = list(self.gd["do_both"][0])
					del self.gd["do_both"][0]
					self.ability_event()
				elif "multicond" in self.gd["effect"]:
					self.gd["effect"] = list(self.gd["effect"][self.gd["effect"].index("multicond") + 1])
					self.ability_event()
				else:
					self.ability_effect()
		elif "cards" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "cards"
			aa = 1
			if "Clock" in self.gd["effect"]:
				if "lower" in self.gd["effect"] and len(self.pd[ind[-1]]["Clock"]) > self.gd["effect"][0]:
					aa = 0
				elif "=" in self.gd["effect"] and len(self.pd[ind[-1]]["Clock"]) != self.gd["effect"][0]:
					aa = 0
				elif "lower" not in self.gd["effect"] and len(self.pd[ind[-1]]["Clock"]) < self.gd["effect"][0]:
					aa = 0
			self.gd["ability_effect"].remove("cards")
			if "do" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("do")
			if aa:
				self.gd["done"] = True
				self.ability_effect()
			else:
				if "multicond" in self.gd["effect"]:
					self.gd["effect"] = list(self.gd["effect"][self.gd["effect"].index("multicond") + 1])
					self.ability_event()
				else:
					self.ability_effect()
		elif "distock" in self.gd["ability_effect"]:
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
					if "ifcount" in self.gd["effect"]:
						self.gd["ifcount"] += 1
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
				if "iftotal" in self.gd["effect"]:
					if self.gd["ifcount"] >= self.gd["effect"][self.gd["effect"].index("if") + 1]:
						self.gd["done"] = True
					self.gd["ifcount"] = 0
				elif wait:
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
			self.gd["brainstorm_c"] = [0, [], []]
			self.gd["brainstorm"] = int(self.gd["effect"][self.gd["effect"].index("brainstorm") + 1])
			self.brainstorm()
		elif "looktop" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "looktop"

			if self.gd["effect"][0] == -16:
				self.gd["effect"][0] = len(self.gd["extra"])
				self.gd["p_l"] = list(self.gd["extra"])
				if "extra" not in self.gd["effect"]:
					self.gd["extra"] = []
				self.gd["clear"] = False

			if self.net["game"] and "looktopopp" in self.gd["effect"]:
				if ind[-1] == "1":
					if self.gd["show_wait_popup"]:
						Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
					self.mconnect("oppchoose")
				elif ind[-1] == "2":
					if not self.net["send"]:
						self.gd["oppchoose"] = True
						self.look_top("s")
					else:
						if self.gd["show_wait_popup"]:
							Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
						self.mconnect("plchoose")
			elif self.gd["com"] and (ind[-1] == "2" or ("looktopopp" in self.gd["effect"] and ind[-1] == "1")):
				if "stack" in self.gd["effect"]:
					self.gd["p_c"] = "Look_stack"
				if self.gd["effect"][0] == -16:
					self.gd["effect"][0] = len(self.gd["extra"])
					self.gd["p_l"] = list(self.gd["extra"])
					if "extra" not in self.gd["effect"]:
						self.gd["extra"] = []
				if "hand" in self.gd["effect"] or "choosestage" in self.gd["effect"]:
					if len(self.pd[ind[-1]]["Library"]) < self.gd["effect"][0]:
						self.gd["effect"][0] = len(self.pd[ind[-1]]["Library"])
					if "top" in self.gd["effect"]:
						self.gd["p_l"] = self.pd[ind[-1]]["Library"][-self.gd["effect"][0]:]
					elif "bottom" in self.gd["effect"]:
						self.gd["p_l"] = self.pd[ind[-1]]["Library"][:self.gd["effect"][0]]
					if "hand" in self.gd["effect"]:
						self.gd["search_type"] = self.gd["effect"][self.gd["effect"].index("hand") + 2]
					elif "choosestage" in self.gd["effect"]:
						self.gd["search_type"] = self.gd["effect"][self.gd["effect"].index("top") + 2]
				pick = self.ai.ability(self.pd, self.cd, self.gd)
				pick1 = ""
				if "AI_looktop" in pick:
					inx = pick.index("AI_looktop")
					self.gd["target"] = list(pick[inx + 1])
					pick1 = pick[inx + 1][0]
				else:
					self.gd["chosen"] = []

				if "stack" in self.gd["effect"]:
					self.look_top("l")
				else:
					self.look_top(pick1)
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
		elif "look" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "look"
			if "opp" in self.gd["effect"] and ind[-1] == "1":
				opp = "2"
			elif "opp" in self.gd["effect"] and ind[-1] == "2":
				opp = "1"
			else:
				opp = ind[-1]
			if ind[-1] == self.gd["active"]:
				self.popup_multi_info(field=self.gd["effect"][0], owner=opp, t="Look")
			elif ind[-1] != self.gd["active"]:
				Clock.schedule_once(partial(self.popup_text, "LookOpp"))
		elif "marker" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "marker"

			if "markers" in self.gd["effect"]:
				mk = True
				markers = 0
				if "under" in self.gd["effect"]:
					if ind in self.pd[ind[-1]]["marker"]:
						markers = len(self.pd[ind[-1]]["marker"][ind])
				else:
					for imd in self.pd[ind[-1]]["marker"]:
						markers += len(self.pd[ind[-1]]["marker"][imd])

				if "lower" in self.gd["effect"] and markers > self.gd["effect"][0]:
					mk = False
				elif "lower" not in self.gd["effect"] and markers < self.gd["effect"][0]:
					mk = False

				if mk:
					self.gd["done"] = True

				if "do" in self.gd["ability_effect"]:
					self.gd["ability_effect"].remove("do")
				self.gd["ability_effect"].remove("marker")
				self.ability_effect()
			else:
				self.marker()
		elif "drawupto" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "drawupto"
			if "if" in self.gd["effect"]:
				self.gd["drawed"] = []

			if ind[-1] == "1":
				if self.net["game"] and "plchoose" in self.gd["effect"]:
					self.net["send"] = False
				if "do" in self.gd["effect"]:
					self.sd["btn"]["end"].text = "Continue Effect"
				else:
					self.sd["btn"]["end"].text = "End Effect"
				if "Reveal" in self.gd["effect"]:
					self.sd["btn"]["draw_upto"].text = "Reveal card"
				elif "Stock" in self.gd["effect"]:
					self.sd["btn"]["draw_upto"].text = "Add Stock"
				elif "heal" in self.gd["effect"]:
					self.sd["btn"]["draw_upto"].text = "Heal Damage"
				elif "Marker" in self.gd["effect"]:
					self.sd["btn"]["draw_upto"].text = "Add Marker"
				else:
					self.sd["btn"]["draw_upto"].text = "Draw card"
				self.sd["btn"]["draw_upto"].disabled = False
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
				if "plchoose" in self.gd["effect"] and not self.gd["target"]:
					if self.gd["show_wait_popup"]:
						Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
					self.mconnect("plchoose")
				else:
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
			if "opp" in self.gd["effect"] and ind[-1] == self.gd["active"]:
				self.gd["rev"] = True
			elif "opp" in self.gd["effect"] and ind[-1] != self.gd["active"]:
				self.gd["rev"] = False
			elif "opp" not in self.gd["effect"] and ind[-1] == self.gd["active"]:
				self.gd["rev"] = False
			elif "opp" not in self.gd["effect"] and ind[-1] != self.gd["active"]:
				self.gd["rev"] = True

			if self.gd["effect"][1] == "x":
				if "xrlevel+1" in self.gd["effect"]:
					self.gd["effect"][1] = self.cd[self.gd["resonance"][1][0]].level_t + 1
				elif "xifcount" in self.gd["effect"]:
					self.gd["effect"][1] = int(self.gd["ifcount"])
					self.gd["ifcount"] = 0

			if "More" in self.gd["effect"]:
				if "lower" in self.gd["effect"] and len(self.cont_times(self.gd["effect"], self.cont_cards(self.gd["effect"], ind), self.cd)) > self.gd["effect"][self.gd["effect"].index("More") + 1]:
					self.gd["effect"][1] = 0
				elif "lower" not in self.gd["effect"] and len(self.cont_times(self.gd["effect"], self.cont_cards(self.gd["effect"], ind), self.cd)) < self.gd["effect"][self.gd["effect"].index("More") + 1]:
					self.gd["effect"][1] = 0
			self.gd["draw"] = self.gd["effect"][1]
			self.draw()
		elif "discard" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "discard"
			if "xshift" in self.gd["effect"]:
				self.gd["target_temp"].append(ind)
				if "Colour_x" in self.gd["effect"][2]:
					self.gd["effect"][2] = f"Colour_{self.cd[ind].mcolour}"
					self.gd["search_type"] = self.gd["effect"][2]
			elif "cdiscard" in self.gd["effect"] and (self.gd["effect"][1] == -17 or self.gd["effect"][1] == -18):
				self.gd["discard"] = 1
				if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
					if "opp" in self.gd["effect"]:
						if ind[-1] == "1":
							p = "2"
						elif ind[-1] == "2":
							p = "1"
					else:
						p = ind[-1]
					self.gd["p_owner"] = ind[-1]
					if len(self.pd[p]["Clock"]) > 0:
						if self.gd["effect"][1] == -17:
							self.gd["chosen"].append(self.pd[p]["Clock"][-1])
						elif self.gd["effect"][1] == -18:
							self.gd["chosen"].append(self.pd[p]["Clock"][0])
					else:
						self.gd["chosen"].append("")
					self.gd["p_c"] == "Discard"
				elif ind[-1] == "2" and self.net["game"]:
					self.fix_opp_net(ind, self.gd["discard"])

			if "random" in self.gd["effect"]:
				op = ind[-1]
				if "opp" in self.gd["effect"]:
					if ind[-1] == "1":
						op = "2"
					elif ind[-1] == "2":
						op = "1"
				dd = sample(self.pd[op]["Hand"], self.gd["discard"])
				for d in dd:
					self.gd["target"].append(d)
					if "Reveal" in self.gd["effect"]:
						self.gd["random_reveal"].append(d)
				self.gd["effect"].remove("random")
			if "Reveal" in self.gd["effect"]:
				self.gd["resonance"][0] = True
				self.gd["resonance"][2] = self.gd["discard"]

			if "swap" in self.gd["effect"] and "Stage" not in self.gd["effect"]:
				swap = self.gd["effect"][self.gd["effect"].index("swap") + 1]
				if "CX" in swap:
					swap = "Climax"
				if "discard" in self.gd["effect"] and (len(self.pd[ind[-1]]["Hand"]) <= 0 or len(self.pd[ind[-1]][swap]) <= 0):
					self.gd["target"] = ["", ""]
				elif "mdiscard" in self.gd["effect"] and (len(self.pd[ind[-1]]["Memory"]) <= 0 or len(self.pd[ind[-1]][swap]) <= 0):
					self.gd["target"] = ["", ""]
				elif "cdiscard" in self.gd["effect"] and (len(self.pd[ind[-1]]["Clock"]) <= 0 or len(self.pd[ind[-1]][swap]) <= 0):
					self.gd["target"] = ["", ""]
				elif "cxdiscard" in self.gd["effect"] and (len(self.pd[ind[-1]]["Climax"]) <= 0 or len(self.pd[ind[-1]][swap]) <= 0):
					self.gd["target"] = ["", ""]
				elif "ldiscard" in self.gd["effect"] and (len(self.pd[ind[-1]]["Level"]) <= 0 or len(self.pd[ind[-1]][swap]) <= 0):
					self.gd["target"] = ["", ""]

			if self.gd["effect"][1] == -1:
				for dd in self.pd[ind[-1]]["Hand"]:
					self.gd["target"].append(dd)
				if not self.gd["target"]:
					self.gd["target"].append("")
				self.gd["effect"][1] = len(self.gd["target"])
				self.gd["discard"] = int(self.gd["effect"][1])

			if self.net["game"] and "oppturn" in self.gd["effect"]:
				if self.gd["show_wait_popup"]:
					Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
				self.mconnect("oppturn")
			elif self.gd["com"] and ((ind[-1] == "2" and "oppturn" not in self.gd["effect"]) or ("oppturn" in self.gd["effect"] and ind[-1] == "1")):
				self.gd["p_c"] = "Discard"
				if "mdiscard" in self.gd["effect"]:
					self.gd["p_c"] += "_Memory"
				elif "ldiscard" in self.gd["effect"]:
					self.gd["p_c"] += "_Level"

				self.gd["p_owner"] = ind[-1]
				if "oppturn" in self.gd["effect"] and "opp" in self.gd["effect"]:
					if ind[-1] == "1":
						self.gd["p_owner"] = "2"
					elif ind[-1] == "2":
						self.gd["p_owner"] = "1"
				elif "opp" in self.gd["effect"]:
					if ind[-1] == "1":
						self.gd["p_owner"] = "2"
					elif ind[-1] == "2":
						self.gd["p_owner"] = "1"
				self.gd["p_f"] = True
				self.popup_pl("Discard")
				for cc in self.skip_cpop:
					if cc in self.gd["p_l"]:
						self.gd["p_l"].remove(cc)
				pick = self.ai.ability(self.pd, self.cd, self.gd)

				if "AI_discard" in pick:
					inx = pick.index("AI_discard")
					self.gd["chosen"] = pick[inx + 1]
				else:
					self.gd["chosen"] = []
				self.discard()
			else:
				if not self.gd["chosen"]:
					self.gd["p_c"] = ""
				self.discard()
		elif "encore" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "encore"
			self.gd["encore_ind"] = str(self.gd["auto_effect"][0])
			if self.gd["target"]:
				self.encore_pay()
			elif self.gd["com"] and self.gd["encore_ind"][-1] == "2":
				if self.pd[self.gd["encore_ind"][-1]][self.cd[self.gd["encore_ind"]].pos_old[:-1]][int(self.cd[self.gd["encore_ind"]].pos_old[-1])] != "":
					self.gd["target"].append("")
				elif "Clock" in self.gd["effect"] and len(self.pd[self.gd["encore_ind"][-1]]["Level"]) <= 2:
					self.gd["target"].append("Clock")
				elif "Stock1" in self.gd["effect"] and len(self.pd[self.gd["encore_ind"][-1]]["Stock"]) >= 1:
					self.gd["target"].append("Stock1")
				elif "Stock2" in self.gd["effect"] and len(self.pd[self.gd["encore_ind"][-1]]["Stock"]) >= 2:
					self.gd["target"].append("Stock2")
				elif "Stock3" in self.gd["effect"] and len(self.pd[self.gd["encore_ind"][-1]]["Stock"]) >= 3:
					self.gd["target"].append("Stock3")
				self.encore_pay()
			else:
				self.gd["confirm_trigger"] = f"Encore_{self.gd['ability_trigger']}"
				self.gd["confirm_var"] = {"ind": self.gd["encore_ind"], "c": "encore"}
				Clock.schedule_once(self.confirm_popup, popup_dt)
				return False
		elif "give" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "give"

			if self.net["game"] and ind[-1] == "2" and not self.gd["target"] and self.gd["effect"][0] > 0:
				if self.gd["show_wait_popup"]:
					Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
				self.mconnect("oppchoose")
			elif ind[-1] == "1" and self.gd["effect"][0] > 0 and not self.gd["target"]:
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"), popup_dt)
			elif self.gd["effect"][0] > 0 and not self.gd["target"] and ind[-1] == "2":
				cards = [s for s in self.pd[ind[-1]]["Center"] + self.pd[ind[-1]]["Back"] if s != ""]
				if "other" in self.gd["effect"] and ind in cards:
					cards.remove(ind)
				for cc in range(len(cards)):
					self.gd["target"].append(cards[cc])
				self.give()
			else:
				self.give()
		elif "rescue" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "rescue"

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
			if (ind[-1] == "1" or ("oppturn" in self.gd["effect"] and ind[-1] == "2")) and self.gd["effect"][0] > 0 and not self.gd["choose"]:
				if "oppturn" in self.gd["effect"] and "Opp" in self.gd["effect"] and "opp" in self.gd["effect"]:
					if ind[-1] == "1":
						if self.net["game"]:
							if not self.net["send"]:
								self.net["act"][5] = 1
								self.net["act"][4].append("opc")
								self.net["var"] = list(self.net["act"])
								self.net["var1"] = "searchopp"
								self.gd["oppchoose"] = True
								if self.gd["do"][1]:
									if "opp" not in self.gd["do"][1] and "oppturn" not in self.gd["do"][1]:
										self.gd["do"][1].append("plchoose")
								if self.gd["do"][2]:
									if "opp" not in self.gd["do"][2] and "oppturn" not in self.gd["do"][2]:
										self.gd["do"][2].append("plchoose")
								if not self.poptext:
									Clock.schedule_once(partial(self.popup_text, "waitingser"))
								self.mconnect("act")
							else:
								if self.gd["show_wait_popup"]:
									Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
								self.mconnect("oppchoose")
						else:
							pick = self.ai.ability(self.pd, self.cd, self.gd)
							if "AI_waitinger" in pick:
								inx = pick.index("AI_waitinger")
								self.gd["target"] = list(pick[inx + 1])
							else:
								self.gd["target"] = [""]
							self.wind()
					elif ind[-1] == "2":
						self.net["send"] = False
						self.gd["oppchoose"] = True
						if self.gd["do"][1]:
							if "opp" not in self.gd["do"][1] and "oppturn" not in self.gd["do"][1]:
								self.gd["do"][1].append("plchoose")
						if self.gd["do"][2]:
							if "opp" not in self.gd["do"][2] and "oppturn" not in self.gd["do"][2]:
								self.gd["do"][2].append("plchoose")
						Clock.schedule_once(partial(self.popup_text, "Main"), move_dt_btw)
						self.select_card()
				else:
					self.select_card()
					Clock.schedule_once(partial(self.popup_text, "Main"))
			else:
				self.gd["confirm_result"] = ""
				self.wind()
		elif "stocker" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "stocker"
			if ind[-1] == "1" and self.gd["effect"][0] > 0 and not self.gd["target"]:
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"))
			else:
				self.stocker()
		elif "clocker" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "clocker"
			if ind[-1] == "1" and self.gd["effect"][0] > 0 and not self.gd["choose"]:
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"))
			else:
				self.clocker()
		elif "decker" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "decker"
			if ind[-1] == "1" and self.gd["effect"][0] > 0 and not self.gd["choose"]:
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"))
			else:
				self.decker()
		elif "waitinger" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "waitinger"
			if ind[-1] == "1" and self.gd["effect"][0] > 0 and not self.gd["choose"]:
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"))
			else:
				self.waitinger()
		elif "memorier" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "memorier"
			if ind[-1] == "1" and self.gd["effect"][0] > 0 and not self.gd["choose"]:  
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"))
			else:
				self.memorier()
		elif "reverser" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "reverser"

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
		elif "revive" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "revive"
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
					elif self.gd["attacking"] and "f" in self.gd["attacking"][1] and self.gd["attacking"][0][-1] != ind[-1] and "Center" in self.cd[self.gd["effect"][2][0]].pos_new:
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
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				if "this" in self.gd["effect"] and ind not in self.gd["target"]:
					self.gd["target"].append(ind)
				elif self.gd["effect"][0] == -16:
					for r in range(len(self.gd["extra"])):
						self.gd["target"].append(self.gd["extra"][r])
				for _ in self.gd["target"]:
					self.cd[_].update_text("Moving", .30)

			if "this" in self.gd["effect"]:
				self.gd["choose"] = True
				self.gd["notarget"] = False
			if self.gd["effect"][0] == -16:
				self.gd["effect"][0] = len(self.gd["extra"])
				if all(e == "" for e in self.gd["extra"]):
					self.gd["move"] = "none"
				if "extra" not in self.gd["effect"]:
					self.gd["extra"] = []
				self.gd["choose"] = True
				self.gd["notarget"] = False
				self.gd["status"] = self.add_to_status("Select1", self.gd["effect"])
			elif self.gd["effect"][0] == 0:
				self.gd["effect"][0] = 1
				self.cd[ind].update_text("Moving", .30)

			if self.gd["target"] and len(self.gd["target"]) % 2 == 0:
				self.move()
			elif self.gd["effect"][0] > 0 and not self.gd["choose"]:
				if self.gd["com"] and ((ind[-1] == "2" and "oppturn" not in self.gd["effect"]) or (ind[-1] == "1" and "oppturn" in self.gd["effect"])):
					self.effect_to_stage()
				else:
					self.select_card()
					Clock.schedule_once(partial(self.popup_text, "Main"))
			elif self.gd["choose"] and not self.gd["notarget"] and not self.gd["move"]:
				if self.gd["com"] and ((ind[-1] == "2" and "oppturn" not in self.gd["effect"]) or (ind[-1] == "1" and "oppturn" in self.gd["effect"])):
					if "this" in self.gd["effect"] and ind not in self.gd["target"]:
						self.gd["target"].append(ind)
					self.effect_to_stage("Field")
				else:
					self.select_field()
					Clock.schedule_once(partial(self.popup_text, "Move"))
			else:
				self.move()
		elif "damage" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "damage"
			if "both" in self.gd["effect"]:
				self.gd["both"] = True
			if self.gd["damage"] == "x":
				tx = 0
				if "Waiting" in self.gd["effect"]:
					tx = len(self.cont_times(self.gd["effect"], self.pd[ind[-1]]["Waiting"], self.cd))
				elif "xlvlhigh" in self.gd["effect"]:
					tx = sorted([self.cd[s].level_t for s in self.pd[ind[-1]]["Center"] + self.pd[ind[-1]]["Back"] if s != ""], reverse=True)[0]
				elif "xmill" in self.gd["effect"]:
					if "xClimax" in self.gd["effect"]:
						tx = len(self.cont_times(["Climax"], self.gd["extra"], self.cd))
					elif "xLevel+x" in self.gd["effect"]:
						if len(self.gd["extra"]) > 0:
							tx = self.cd[self.gd["extra"][0]].level_t + self.gd["effect"][self.gd["effect"].index("xLevel+x") + 1]
					elif "xLevel" in self.gd["effect"]:
						if len(self.gd["extra"]) > 0:
							tx = self.cd[self.gd["extra"][0]].level_t
					self.gd["extra"] = []
				elif "xdeclare" in self.gd["effect"]:
					tx = int(self.gd["numbers"])
				elif "xdiscard" in self.gd["effect"]:
					if "xLevel" in self.gd["effect"]:
						if len(self.gd["xdiscard"]) > 0:
							tx = self.cd[self.gd["xdiscard"][0]].level
					self.gd["xdiscard"] = []
				elif "xreveals" in self.gd["effect"]:
					if "xTrigger" in self.gd["effect"]:
						tx = len([s for s in self.gd["extra"] if self.gd["effect"][self.gd["effect"].index("xTrigger") + 1].lower() in self.cd[s].trigger])
					self.gd["extra"] = []
				elif "xreveal" in self.gd["effect"]:
					if "xTrigger+" in self.gd["effect"]:
						tx = self.cd[self.gd["reveal_ind"]].trigger.count(self.gd["effect"][self.gd["effect"].index("xTrigger+") + 1].lower()) + self.gd["effect"][self.gd["effect"].index("xTrigger+") + 2]
					elif "xSoul" in self.gd["effect"]:
						tx = int(self.cd[self.gd["reveal_ind"]].soul_t)
				elif "xResonance" in self.gd["effect"]:
					if "xSoul" in self.gd["effect"]:
						tx = sum([self.cd[s].soul_t for s in self.gd["resonance"][1] if s != ""])
				elif "xself" in self.gd["effect"]:
					if "xSoul" in self.gd["effect"]:
						tx = int(self.cd[ind].soul_t)
				self.gd["damage"] = tx
			elif self.gd["damage"] == -16:
				if "xSoul" in self.gd["effect"]:
					self.gd["damage"] = int(self.cd[self.gd["extra"][0]].soul_t)
				else:
					self.gd["damage"] = len(self.gd["extra"])
				self.gd["extra"] = []
			elif self.gd["damage"] == -36:
				if len(self.gd["extra"]) > 0:
					self.gd["damage"] = self.cd[self.gd["extra"][0]].level
				else:
					self.gd["damage"] = 0
				self.gd["extra"] = []

			if self.gd["damage"] > 0 or self.gd["damage_refresh"] > 0:
				if "opp" in self.gd["effect"] and ind[-1] == self.gd["active"]:
					self.gd["drev"] = True
				elif "opp" in self.gd["effect"] and ind[-1] != self.gd["active"]:
					self.gd["drev"] = False
				elif "opp" not in self.gd["effect"] and ind[-1] == self.gd["active"]:
					self.gd["drev"] = False
				elif "opp" not in self.gd["effect"] and ind[-1] != self.gd["active"]:
					self.gd["drev"] = True

				if "AUTO" in self.gd["ability_trigger"]:
					if "Climax_auto" not in self.gd["effect"]:
						if self.gd["no_damage_auto_opp"]["1"] and "opp" in self.gd["effect"] and ind[-1] == "2":
							self.gd["damage"] = 0
						elif self.gd["no_damage_auto_opp"]["2"] and "opp" in self.gd["effect"] and ind[-1] == "1":
							self.gd["damage"] = 0

				if ind in self.gd["no_damage"][ind[-1]]:
					self.gd["damage"] = 0

				self.gd["dmg"] = int(self.gd["damage"])
				self.damage()
			else:
				self.gd["dmg"] = 0
				self.gd["ability_effect"].remove("damage")
				self.do_check(True)
		elif "mill" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "mill"
			if self.gd["effect"][1] == "x":
				m = []
				meff = list(self.gd["effect"])
				if "xopp" not in meff and "opp" in meff:
					meff.remove("opp")
				elif "xopp" in meff and "opp" not in meff:
					meff.append("opp")
				if "xTrait" in self.gd["effect"]:
					m = ["Trait", self.gd["effect"][self.gd["effect"].index("xTrait") + 1]]
				self.gd["effect"][1] = len(self.cont_times(m, self.cont_cards(meff, ind), self.cd))

			if self.gd["ability_doing"] in self.gd["contadd"] and ind[-1] in self.gd["contadd"][self.gd["ability_doing"]]:
				if self.cd[ind].name_t in self.gd["contadd"][self.gd["ability_doing"]][ind[-1]]:
					self.gd["effect"][1] += self.gd["contadd"][self.gd["ability_doing"]][ind[-1]][self.cd[ind].name_t]
			self.gd["mill"] = int(self.gd["effect"][1])

			self.mill()
		elif "salvage" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "salvage"
			if self.gd["effect"][0] == "x" or (isinstance(self.gd["effect"][0], int) and self.gd["effect"][0] > 0 and self.gd["effect"][2][-2:] == "=x"):
				if "xrlevel+1" in self.gd["effect"]:
					self.gd["effect"][2] = f"{self.gd['effect'][2][:-1]}{self.cd[self.gd['resonance'][1][0]].level_t + 1}"
				elif "xvlevel" in self.gd["effect"] and self.gd["effect"][2][-1] == "x":
					self.gd["effect"][2] = f"{self.gd['effect'][2][:-1]}{self.cd[self.gd['reveal_ind']].level_t}"
				elif "xsmlevel" in self.gd["effect"] and (self.gd["effect"][2][-1] == "x" or self.gd["effect"][0] == "x"):
					lv = 0
					for rr in self.gd["extra"]:
						lv += self.cd[rr].level
					if self.gd["effect"][0] == "x":
						self.gd["effect"][0] = lv
						self.gd["salvage"] = self.gd["effect"][0]
					elif self.gd["effect"][2][-1] == "x":
						self.gd["effect"][2] = f"{self.gd['effect'][2][:-1]}{lv}"
					self.gd["extra"] = []
				elif "xrqclevel" in self.gd["effect"] and self.gd["effect"][0] == "x":
					lv = 0
					for rr in self.gd["extra"]:
						if "Character" in self.cd[rr].card and self.cd[rr].level_t == self.gd["effect"][self.gd["effect"].index("xrqclevel") + 1]:
							lv += 1
					self.gd["effect"][0] = lv
					self.gd["salvage"] = self.gd["effect"][0]
					self.gd["extra"] = []
					if lv == 0:
						self.gd["target"] = [""]
						self.gd["p_c"] = "Salvage"
						self.gd["salvage"] = 1
						self.gd["effect"][0] = 1
				elif "xslevel-" in self.gd["effect"] and self.gd["effect"][2][-1] == "x":
					if self.gd["extra"] and "swap" in self.gd["effect"]:
						lv = self.cd[self.gd['extra'][0]].level_t - self.gd["effect"][self.gd["effect"].index("xslevel-") + 1]
						if lv < 0:
							lv = 0
						self.gd["effect"][2] = f"{self.gd['effect'][2][:-1]}{lv}"
						self.gd["move"] = self.cd[self.gd["extra"][0]].pos_old
					self.gd["extra"] = []
				elif "xqwrlevel" in self.gd["effect"] and self.gd["effect"][2][-1] == "x":
					xeff = []
					if "xName=" in self.gd["effect"]:
						xeff = ["Name=", self.gd["effect"][self.gd["effect"].index("xName=") + 1]]
					self.gd["effect"][2] = f"{self.gd['effect'][2][:-1]}{len(self.cont_times(xeff, self.cont_cards(['Waiting'], ind), self.cd))}"
				elif "xqmlevel" in self.gd["effect"] and self.gd["effect"][2][-1] == "x":
					self.gd["effect"][2] = f"{self.gd['effect'][2][:-1]}{len(self.cont_cards(['Memory'], ind))}"
				self.gd["search_type"] = self.gd["effect"][2]
			elif "Name=_x" in self.gd["effect"]:
				if "xStage" in self.gd["effect"]:
					self.gd["effect"][2] = "_".join(["Name="] + list(set([self.cd[s].name_t for s in self.pd[ind[-1]]["Center"] + self.pd[ind[-1]]["Back"] if s != ""])))
				self.gd["search_type"] = str(self.gd["effect"][2])
			elif "ColourCx_x" in self.gd["effect"]:
				if "xResonance" in self.gd["effect"]:
					if "xcolourdiff" in self.gd["effect"]:
						self.gd["effect"][2] = "_".join(["ColourCx"] + [cc for cc in self.colour if cc.lower() not in list(set([self.cd[s].mcolour.lower() for s in self.gd["resonance"][1] if s != ""]))])
					else:
						self.gd["effect"][2] = "_".join(["ColourCx"] + list(set([self.cd[s].mcolour.lower() for s in self.gd["resonance"][1] if s != ""])))
				self.gd["search_type"] = str(self.gd["effect"][2])

			if self.gd["effect"][0] == -16:
				self.gd["effect"][0] = len(self.gd["extra"])
				self.gd["salvage"] = int(self.gd["effect"][0])

				if "ID=_x" in self.gd["effect"]:
					self.gd["effect"][2] = "_".join(["ID="] + [n for n in self.gd["extra"] if n != ""])
					self.gd["effect"].append("passed")
					self.gd["search_type"] = str(self.gd["effect"][2])
				for r in range(len(self.gd["extra"])):
					_ = self.gd["extra"].pop(0)
					if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
						if "Markers" in self.gd["effect"] and "Stage" in self.gd["effect"]:
							self.gd["markers"].append(_)
						else:
							self.gd["target"].append(_)
				if self.gd["target"]:
					self.gd["p_c"] = "Salvage"
				if "extra" not in self.gd["effect"]:
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
						if self.gd["effect"][0] > 0:
							if self.gd["show_wait_popup"]:
								Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
							self.mconnect("plchoose")
							return False
				elif "Stage" in self.gd["effect"] and self.gd["effect"][0] >= 1:
					if len([c for c in self.gd["target"] if c != ""]) > 0:
						Clock.schedule_once(partial(self.effect_to_stage, "Stage"), move_dt_btw)
						return False
					else:
						self.gd["move"] = "none"
			if "swap" in self.gd["effect"] and "Stage" not in self.gd["effect"] and "Hand" not in self.gd["effect"]:
				self.gd["chosen"] = []
				swap = self.gd["effect"][self.gd["effect"].index("swap") + 1]
				if "CX" in swap:
					swap = "Climax"
				if "salvage" in self.gd["effect"] and (len(self.pd[ind[-1]]["Waiting"]) <= 0 or len(self.pd[ind[-1]][swap]) <= 0):
					self.gd["target"] = ["", ""]
					self.gd["p_c"] = "Salvage"

			if self.net["game"] and "oppturn" in self.gd["effect"]:
				if ind[-1] == "1":
					if not self.net["send"]:
						self.net["act"][5] = 1
						self.net["var"] = list(self.net["act"])
						self.net["var1"] = "searchopp"
						if not self.poptext:
							Clock.schedule_once(partial(self.popup_text, "waitingser"))
						self.mconnect("act")
					else:
						if self.gd["show_wait_popup"]:
							Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
						self.mconnect("oppchoose")
				elif ind[-1] == "2":
					if not self.gd["target"]:
						self.gd["p_c"] = ""
					self.salvage()
			elif self.gd["com"] and ((ind[-1] == "2" and "oppturn" not in self.gd["effect"]) or (ind[-1] == "1" and "oppturn" in self.gd["effect"])):
				if "ksalvage" in self.gd["effect"] and self.gd["markers"]:
					for _ in self.gd["markers"]:
						self.gd["target"].append(_)
					self.effect_to_stage(ind)
				else:
					self.choose_opp(ind)
					self.salvage()
			else:
				if "passed" in self.gd["effect"] and self.gd["p_c"]:
					pass
				else:
					self.gd["p_c"] = ""
				self.salvage()
		elif "search" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "search"
			if "CLevel_<=x" in self.gd["effect"]:
				if "xlevelextra" in self.gd["effect"] and self.gd["extra"]:
					self.gd["effect"][self.gd["effect"].index("CLevel_<=x")] = f"CLevel_<={self.cd[self.gd['extra'][0]].level}"
			elif "CLevel_==x" in self.gd["effect"] and self.gd["extra"]:
				if "xlevelextra" in self.gd["effect"] and self.gd["extra"]:
					self.gd["effect"][self.gd["effect"].index("CLevel_==x")] = f"CLevel_=={self.cd[self.gd['extra'][0]].level}"
			elif "TraitZ" in self.gd["search_type"] and "<=x" in self.gd["search_type"]:
				if "xextraZ" in self.gd["effect"]:
					_ = 0
					if self.gd["extra"]:
						_ = sum([self.cd[z].level_t + self.cd[z].cost_t for z in self.gd["extra"]])
					self.gd["effect"][2] = self.gd["effect"][2].replace("<=x", f"<={_}")
					if "extra" not in self.gd["effect"]:
						self.gd["extra"] = []
			elif "Trait_x" in self.gd["effect"]:
				if "xany" in self.gd["effect"] and "xextratrait" in self.gd["effect"]:
					self.gd["effect"][self.gd["effect"].index("Trait_x")] = f"Trait_{'_'.join(self.cd[self.gd['extra'][0]].trait_t)}"
			elif "Name=_x" in self.gd["search_type"]:
				if "xcxsamewr" in self.gd["effect"] and "CXName=" in self.gd["search_type"]:
					self.gd["effect"][self.gd["effect"].index("CXName=_x")] = f'CXName=_{"_".join(list(set([self.cd[_].name for _ in self.cont_times(["Climax"], self.cont_cards(["Waiting"], ind), self.cd)])))}'

			self.gd["search_type"] = self.gd["effect"][2]

			if "BTraitN" in self.gd["search_type"]:
				self.gd["btrait"][1] = self.gd["effect"][2].split("_")[1:]
				self.gd["btrait"][1][-1] = f'N/{self.gd["btrait"][1][-1]}'
				self.gd["btrait"][2] = self.cont_times([self.gd["effect"][2].split("_")[0], "_".join(self.gd["btrait"][1])], self.cont_cards(["Library"], ind), self.cd)
				self.gd["btrait"][3] = list(self.gd["btrait"][1])
				self.gd["btrait"][0] = str(self.gd["status"])

			if self.gd["effect"][0] == -9:
				self.gd["effect"][0] = 1
				self.gd["search"] = 1
				self.gd["chosen"].append(self.pd[ind[-1]]["Library"][-1])
				if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
					self.gd["p_c"] = "Search_Stage"
			elif self.gd["effect"][0] == -16:
				if not self.gd["extra"]:
					self.gd["extra"].append("")
				self.gd["effect"][0] = len(self.gd["extra"])
				self.gd["search"] = len(self.gd["extra"])
				if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
					self.gd["p_c"] = "Search_Stage"
					for _ in self.gd["extra"]:
						if _ not in self.gd["chosen"]:
							self.gd["chosen"].append(_)
				if "extra" not in self.gd["effect"]:
					self.gd["extra"] = []
			elif self.gd["effect"][0] == -17 and "stsearch" in self.gd["effect"]:
				self.gd["effect"][0] = 1
				self.gd["search"] = 1
				if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
					if "opp" in self.gd["effect"]:
						if ind[-1] == "1":
							p = "2"
						elif ind[-1] == "2":
							p = "1"
					else:
						p = ind[-1]
					self.gd["p_owner"] = ind[-1]
					if len(self.pd[p]["Stock"]) > 0:
						self.gd["target"].append(self.pd[p]["Stock"][-1])
					else:
						self.gd["target"].append("")
				elif ind[-1] == "2" and self.net["game"]:
					self.fix_opp_net(ind, self.gd["effect"][0])

			if self.net["game"] and "oppturn" in self.gd["effect"]:
				if ind[-1] == "1":
					if not self.net["send"]:
						self.net["act"][5] = 1
						self.net["var"] = list(self.net["act"])
						self.net["var1"] = "searchopp"
						if not self.poptext:
							Clock.schedule_once(partial(self.popup_text, "waitingser"))
						self.mconnect("act")
					else:
						if self.gd["show_wait_popup"]:
							Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
						self.mconnect("oppchoose")
			elif self.gd["com"] and ((ind[-1] == "2" and "oppturn" not in self.gd["effect"]) or (ind[-1] == "1" and "oppturn" in self.gd["effect"])):
				if not self.gd["chosen"]:
					self.gd["p_c"] = "Search"
					if "oppturn" in self.gd["effect"] and ind[-1] == "1":
						self.gd["p_owner"] = "1"
					elif ind[-1] == "2":
						self.gd["p_owner"] = "2"

					if "Reveal" in self.gd["effect"]:
						self.gd["p_c"] += "_Reveal"
					if "stsearch" in self.gd["effect"]:
						self.gd["p_c"] += "_Stock"

					self.gd["p_f"] = True
					self.popup_pl("Search")
					for cc in self.skip_cpop:
						if cc in self.gd["p_l"]:
							self.gd["p_l"].remove(cc)
					pick = self.ai.ability(self.pd, self.cd, self.gd)

					if "AI_search" in pick:
						inx = pick.index("AI_search")
						self.gd["chosen"] = list(pick[inx + 1])
					else:
						self.gd["chosen"] = []
				self.search()
			else:
				if "topdeck" not in self.gd["effect"] and not self.gd["chosen"]:
					self.gd["p_c"] = ""
				self.search()
		elif "level" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "level"

			if self.gd["effect"][0] > 0 and not self.gd["target"] and ind[-1] == "1":
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"))
			elif self.gd["effect"][0] > 0 and not self.gd["target"] and ind[-1] == "2":
				cards = self.get_fields()
				pick = ""
				if "other" in self.gd["effect"] and ind in cards:
					cards.remove(ind)
					pick = self.ai.choose_stage_target("Buff", self.pd, self.cd, self.gd, cards)

				if "AI_Stage" in pick:
					inx = pick.index("AI_Stage")
					self.gd["choose"] = True
					for x in pick[inx + 1]:
						self.gd["target"].append(x)
				else:
					for x in range(self.gd["effect"][0]):
						self.gd["target"].append("")

				self.level()
			else:
				self.level()
		elif "soul" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "soul"
			if self.gd["effect"][0] > 0 and not self.gd["target"] and ind[-1] == "1":
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"))
			elif self.gd["effect"][0] > 0 and not self.gd["target"] and ind[-1] == "2":
				cards = self.get_fields()
				if "other" in self.gd["effect"] and ind in cards:
					cards.remove(ind)
				pick = self.ai.choose_stage_target("Buff", self.pd, self.cd, self.gd, cards)

				if "AI_Stage" in pick:
					inx = pick.index("AI_Stage")
					self.gd["choose"] = True
					for x in pick[inx + 1]:
						self.gd["target"].append(x)
				else:
					for x in range(self.gd["effect"][0]):
						self.gd["target"].append("")

				self.soul()
			else:
				self.soul()
		elif "trait" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "trait"
			if self.gd["effect"][0] > 0 and not self.gd["target"] and ind[-1] == "1":
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"))
			else:
				if "xchoose" in self.gd["effect"] and self.gd["effect"][0] == 0:
					self.choose_trait()
				else:
					self.trait()
		elif "power" in self.gd["ability_effect"]:
			self.gd["ability_doing"] = "power"
			if "xrlevel+1" in self.gd["effect"] and self.gd["effect"][0] == "x":
				self.gd["effect"][0] = self.cd[self.gd["resonance"][1][0]].level_t + 1
				if self.gd["effect"][0] > 0 and not self.gd["choose"]:
					self.gd["status"] = f"Select{self.gd['effect'][0]}"
					self.gd["status"] = self.add_to_status(self.gd["status"], self.gd["effect"])
			elif "xrlevel" in self.gd["effect"] and self.gd["effect"][1] == "x":
				self.gd["effect"][1] = self.gd["effect"][self.gd["effect"].index("xrlevel") + 1] * self.cd[
					self.gd["resonance"][1][0]].level

			if "BTrait" in self.gd["effect"]:
				self.gd["btrait"][1] = self.gd["effect"][self.gd["effect"].index("BTrait") + 1].split("_")
				self.gd["btrait"][2] = self.cont_times(self.gd["effect"], self.cont_cards(self.gd["effect"], ind), self.cd)
				self.gd["btrait"][0] = str(self.gd["status"])

			if self.gd["effect"][0] > 0 and not self.gd["target"] and ind[-1] == "1":
				self.select_card()
				Clock.schedule_once(partial(self.popup_text, "Main"), popup_dt)
			elif self.gd["effect"][0] > 0 and not self.gd["target"] and ind[-1] == "2":
				cards = self.get_fields()
				if "other" in self.gd["effect"] and ind in cards:
					cards.remove(ind)
				pick = self.ai.choose_stage_target("Buff", self.pd, self.cd, self.gd, cards)

				if "AI_Stage" in pick:
					inx = pick.index("AI_Stage")
					self.gd["choose"] = True
					for x in pick[inx + 1]:
						self.gd["target"].append(x)
				else:
					for x in range(self.gd["effect"][0]):
						self.gd["target"].append("")

				self.power()
			else:
				self.power()
		elif "done" in self.gd["ability_effect"] and self.gd["per_poped"][-1] <= 0:
			self.gd["effect"] = list(self.gd["do"][2])
			self.gd["ability_effect"].remove("done")
			self.gd["do"][2] = []
			self.gd["done"] = False
			Clock.schedule_once(self.ability_event)
		else:
			Clock.schedule_once(self.stack_ability)

	def heal(self, dt=0):
		ind = self.gd["ability_trigger"].split("_")[1]
		if ind[-1] == "1" or (self.gd["com"] and ind[-1] == "2"):
			for x in range(self.gd["effect"][1]):
				if len(self.pd[ind[-1]]["Clock"]) > x:
					if "top" in self.gd["effect"]:
						cind = self.pd[ind[-1]]["Clock"][-1 + x]
						if self.gd["uptomay"] and (not self.gd["move"] or self.gd["move"] == "none"):
							self.gd["target"].append("")
						else:
							self.gd["target"].append(cind)
					elif "bottom" in self.gd["effect"]:
						cind = self.pd[ind[-1]]["Clock"][0 + x]
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
			if "Stock" in self.gd["effect"]:
				self.pd[ind[-1]]["Stock"].append(temp)
				self.stock_size(ind[-1])
			elif "Hand" in self.gd["effect"]:
				self.pd[ind[-1]]["Hand"].append(temp)
				self.hand_size(ind[-1])
			else:
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
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(ind)
			self.gd["effect"][0] = 1
		elif self.gd["effect"][0] == -1:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
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
				if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
					if self.cd[ex].status != "Rest" and ("Center" in self.cd[ex].pos_new or "Back" in self.cd[ex].pos_new):
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
			if self.cd[temp].status != "Rest" and ("Center" in self.cd[temp].pos_new or "Back" in self.cd[temp].pos_new):
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
		if self.net["game"] and (("plchoose" in self.gd["effect"] and not self.net["send"]) or (self.gd["perform_both"] and "oppturn" not in self.gd["effect"])):
			self.net["var"] = list(self.net["act"][4])
			self.net["var1"] = "plchoose"
			if not self.poptext:
				Clock.schedule_once(partial(self.popup_text, "waitingser"))
			self.mconnect("plchoose")
		else:
			self.ability_effect()

	def stand(self, *args):
		ind = self.gd["ability_trigger"].split("_")[1]
		if self.gd["effect"][0] == 0:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(ind)
			self.gd["effect"][0] = 1
		elif "this" in self.gd["effect"] and self.gd["effect"][0] > 0:
			if ind[-1] == "1" or (ind[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(ind)
			self.gd["effect"][0] += 1

		s = []
		for r in range(self.gd["effect"][0]):
			temp = self.gd["target"].pop(0)
			if self.net["game"] and ind[-1] == "1":
				self.net["act"][4].append(temp)
			if temp in self.emptycards:
				self.gd["notarget"] = True
				continue
			if "extra" in self.gd["effect"]:
				self.gd["extra"].append(ind)

			if "swap" in self.gd["effect"]:
				s.append(temp)
			if "Center" in self.cd[temp].pos_new or "Back" in self.cd[temp].pos_new:
				if self.cd[temp].status != "Stand" and "nostand" not in self.gd["effect"]:
					self.cd[temp].stand()
					for item in self.cd[temp].text_c:
						if item[0].startswith(auto_ability) and item[1] == -31:
							self.cd[temp].text_c[self.cd[temp].text_c.index(item)][1] = -1
				self.gd["check_atk"] = True

		if len(s) == 2:
			self.gd["movable"] = []
			for sm in self.pd[s[0][-1]]["Center"] + self.pd[s[0][-1]]["Back"]:
				if ind in self.emptycards:
					continue
				aa = True
				for item in self.cd[sm].text_c:
					if item[0].startswith(cont_ability) and item[1] != 0 and item[1] > -9:
						eff = ab.cont(item[0])
						if "no_move" in eff and self.cd[sm].pos_new != "Hand":
							aa = False
							break
				if aa:
					self.gd["movable"].append(sm)
			if all(_ in self.gd["movable"] for _ in s):
				_ = str(self.cd[s[0]].pos_new)
				self.cd[s[0]].setPos(field=self.mat[s[0][-1]]["field"][self.cd[s[1]].pos_new], t=self.cd[s[1]].pos_new)
				self.pd[s[0][-1]][self.cd[s[1]].pos_new[:-1]][int(self.cd[s[1]].pos_new[-1])] = s[0]
				self.cd[s[1]].setPos(field=self.mat[s[1][-1]]["field"][_], t=_)
				self.pd[s[1][-1]][_[:-1]][int(_[-1])] = s[1]
			self.gd["movable"] = []

		if "stand" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("stand")

		if "do" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("do")

		if "do" in self.gd["effect"] and self.gd["do"][0] > 0:
			self.gd["done"] = True

		self.check_cont_ability()

		if self.gd["pay"] and not self.gd["payed"]:
			Clock.schedule_once(self.pay_condition, move_dt_btw)
		else:
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

				card.setPos(library[0] - self.sd["padding"] - self.sd["card"][0], library[1] - self.sd["card"][1] / 3. * len(self.pd[player]["Res"]), t="Res")
				card.show_front()
				if "Climax" in self.gd["effect"] and card.card == "Climax":
					self.gd["brainstorm_c"][0] += 1
				self.gd["brainstorm_c"][2].append(card.card)
				self.pd[player]["Res"].append(temp)

				if not self.gd["Res1_move"]:
					if self.field_btn[f"Res1{player}"].x < 0:
						self.field_btn[f"Res1{player}"].x += Window.width * 2
					self.gd["Res1_move"] = True

				self.update_field_label()
				self.gd["brainstorm"] -= 1

			if len(self.pd[player]["Library"]) <= 0:
				self.gd["reshuffle_trigger"] = "brainstorm"
				self.gd["rrev"] = player
				Clock.schedule_once(self.refresh, move_dt_btw)
				return False
			Clock.schedule_once(self.brainstorm, move_dt_btw)
		else:
			cany = []
			if "any" in self.gd["effect"]:
				cany = self.cont_times(self.gd["effect"], self.pd[player]["Res"], self.cd)
			elif "each" in self.gd["effect"]:
				self.gd["brainstorm_c"][0] = len(self.cont_times(self.gd["effect"], self.pd[player]["Res"], self.cd))

			for r in range(len(self.pd[player]["Res"])):
				temp = self.pd[player]["Res"].pop(0)
				if "Event" in self.gd["ability_trigger"] and temp in self.gd["ability_trigger"]:
					self.pd[player]["Res"].append(temp)
					continue
				self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Waiting"], t="Waiting")
				self.pd[player]["Waiting"].append(temp)
				self.update_field_label()

			if self.gd["Res1_move"]:
				if self.field_btn[f"Res1{player}"].x > 0:
					self.field_btn[f"Res1{player}"].x -= Window.width * 2
				self.gd["Res1_move"] = False

			self.check_cont_ability()
			self.check_auto_ability(brt=(self.gd["ability_trigger"].split("_")[1], self.gd["brainstorm_c"][2]), stacks=False)
			self.gd["rev"] = False

			if "brainstorm" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("brainstorm")

			if "do" in self.gd["ability_effect"] and "any" in self.gd["effect"] and len(cany) >= self.gd["effect"][self.gd["effect"].index("any") + 1]:
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
				if "draw" in self.gd["do"][1] or "drawupto" in self.gd["do"][1]:
					if "xclimax*" in self.gd["do"][1] and self.gd["do"][1][1] == "x":
						self.gd["do"][1][1] = self.gd["brainstorm_c"][0] * self.gd["do"][1][self.gd["do"][1].index("xclimax*") + 1]
						if "do" in self.gd["do"][1] and "xclimax*" in self.gd["do"][1][self.gd["do"][1].index("do") + 1] and self.gd["do"][1][self.gd["do"][1].index("do") + 1][1] == "x":
							self.gd["do"][1][self.gd["do"][1].index("do") + 1][1] = self.gd["brainstorm_c"][0] * self.gd["do"][1][self.gd["do"][1].index("do") + 1][self.gd["do"][1][self.gd["do"][1].index("do") + 1].index("xclimax*") + 1]
					else:
						self.gd["do"][1][1] = self.gd["do"][1][1] * self.gd["brainstorm_c"][0]
				elif "stocker" in self.gd["do"][1]:
					self.gd["do"][0] = 1
				elif "power" in self.gd["do"][1]:
					self.gd["do"][1][1] = self.gd["do"][1][1] * self.gd["brainstorm_c"][0]
				elif "perform" in self.gd["do"][1]:
					self.gd["do"][1][1] = self.gd["do"][1][1] * self.gd["brainstorm_c"][0]
					self.gd["do"][1][2] = "_".join([self.gd["do"][1][2]] * self.gd["do"][1][1])
					self.gd["do"][1].extend(["choice", self.gd["do"][1][1]])
				elif any(eff in self.gd["do"][1] for eff in ("search", "salvage", "waitinger")):
					if isinstance(self.gd["do"][1][0], str) and "x" in self.gd["do"][1][0]:
						if self.gd["brainstorm_c"][0] <= 0:
							self.gd["done"] = False
						else:
							self.gd["do"][1][0] = int(self.gd["brainstorm_c"][0])
							if "do" in self.gd["do"][1] and self.gd["do"][1][self.gd["do"][1].index("do") + 1][1] == "x":
								self.gd["do"][1][self.gd["do"][1].index("do") + 1][1] = int(self.gd["brainstorm_c"][0])
					elif isinstance(self.gd["do"][1][-1], list) and "discard" in self.gd["do"][1][-1]:
						self.gd["brainstorm_c"][1] = list(self.gd["do"][1])
						self.gd["brainstorm_c"][0] -= 1
					else:
						self.gd["do"][1][0] = self.gd["do"][1][0] * self.gd["brainstorm_c"][0]
				else:
					self.gd["do"][0] = int(self.gd["brainstorm_c"][0])
					temp = []
					for rr in range(self.gd["do"][0]):
						if rr == 0:
							temp = list(self.gd["do"][1])
						else:
							temp1 = temp
							temp = list(self.gd["do"][1])
							temp.extend(["do", temp1])
					self.gd["do"][1] = temp
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
		self.gd["extra"] = []
		self.gd["status"] = ""
		self.gd["mstock"] = ["", 0]
		self.gd["show"] = []
		self.gd["do"] = [0, [], []]
		self.gd["done"] = False
		self.gd["dont"] = []
		self.gd["p_c"] = ""
		self.gd["cont_on"] = False

		if self.gd["both"]:
			self.gd["both"] = False

		if self.gd["uptomay"]:
			self.gd["uptomay"] = False
			self.sd["btn"]["end"].y = -Window.height * 2
			self.sd["btn"]["end_eff"].y = -Window.height * 2

		self.gd["pay"] = []
		self.gd["payed"] = False
		self.gd["paypop"] = False
		if self.gd["per_poped"][0]:
			self.gd["per_poped"] = ["", [], 0, -1, 0]
			if not self.gd["popup_done"][1]:
				self.gd["popup_done"] = [False, True]
		self.gd["pay_status"] = ""
		self.gd["brainstorm_c"] = [0, [], []]
		self.gd["notarget"] = False
		self.gd["notargetfield"] = False
		self.gd["select_on"] = False
		self.gd["draw_upto"] = 0
		self.gd["dmg"] = 0
		self.gd["auto_effect"] = ""
		self.gd["ability_doing"] = ""
		self.gd["ability_effect"] = []
		self.gd["confirm_result"] = ""
		self.gd["target_temp"] = []
		self.gd["standby"] = ["", "", ""]


		if self.net["game"]:
			self.net["act"] = ["", "", 0, [], [], 0, -1]

	def play_card_done(self, dt=0):
		if self.net["game"] and self.net["act"][5] and not self.net["send"] and self.gd["active"] == "1":
			if "ACT" in self.gd["ability_trigger"]:
				self.net["var1"] = "act"
			elif "AUTO" in self.gd["ability_trigger"]:
				self.net["var1"] = "auto"
			self.net["var"] = list(self.net["act"])
			self.mconnect("act")
		else:
			if "Event" in self.gd["ability_trigger"]:
				self.event_done()

			self.gd["play_card"] = ""
			self.clear_ability()
			self.check_cont_ability()

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
					self.sd["btn"]["end"].text = "Attack Phase"
					self.sd["btn"]["end_attack"].y = -Window.height
					self.sd["btn"]["end_phase"].y = -Window.height
				else:
					self.sd["btn"]["end"].disabled = False
					self.sd["btn"]["end"].text = "Climax Phase"
					self.sd["btn"]["end_attack"].y = 0
					self.sd["btn"]["end_phase"].y = 0
				self.update_movable(self.gd["active"])

			if self.gd["resonance"][0]:
				for _ in self.gd["resonance"][1]:
					if not self.cd[_].back:
						self.cd[_].show_back()
				self.gd["resonance"] = [False, [], 0]

			if self.net["game"] and self.gd["active"] == "2":
				if self.gd["show_wait_popup"]:
					Clock.schedule_once(partial(self.popup_text, "waiting"), move_dt_btw)
				self.mconnect("phase")
			elif self.gd["com"] and self.gd["active"] == "2":
				Clock.schedule_once(self.opp_play, move_dt_btw)
			elif "Counter" in self.gd["phase"]:
				Clock.schedule_once(self.counter_step_done)
			else:
				if "Climax" in self.gd["phase"]:
					self.update_playable_climax(self.gd["active"])
				else:
					self.update_movable(self.gd["active"])
				self.hand_btn_show(False)

	def omore(self, eff, ind):
		if "Oopp" in eff and ind[-1] == "1":
			p = "2"
		elif "Oopp" in eff and ind[-1] == "2":
			p = "1"
		else:
			p = ind[-1]

		if "OMemory" in eff:
			estage = [s for s in self.pd[p]["Memory"] if s != ""]
		elif "OLVL" in eff:
			estage = [s for s in self.pd[p]["Level"] if s != ""]
		elif "OWaiting" in eff:
			estage = [s for s in self.pd[p]["Waiting"] if s != ""]
		elif "OCX" in eff:
			estage = [s for s in self.pd[p]["Climax"] if s != ""]
		elif "OCenter" in eff:
			estage = [s for s in self.pd[p]["Center"] if s != ""]
		elif "OBack" in eff:
			estage = [s for s in self.pd[p]["Back"] if s != ""]
		else:
			estage = [s for s in self.pd[p]["Center"] + self.pd[p]["Back"] if s != ""]

		if "Oother" in eff and ind in estage:
			estage.remove(ind)

		meff = []
		if "OCharacter" in eff:
			meff = ["Character"]
		elif "OClimax" in eff:
			meff = ["Climax"]
		elif "OCColourT" in eff:
			meff = ["CColourT", eff[eff.index("OCColourT") + 1]]
		elif "OColour" in eff:
			meff = ["Colour", eff[eff.index("OColour") + 1]]
		elif "OCBName=" in eff:
			meff = ["Name=", eff[eff.index("OCBName=") + 1].split("_")[0]]
			meff1 = ["Name=", eff[eff.index("OCBName=") + 1].split("_")[1]]
			estage = [s for s in self.pd[p]["Center"] if s != ""]
		elif "OCLevel" in eff:
			meff = ["Name=", eff[eff.index("OCLevel") + 1]]
		elif "OName=" in eff:
			meff = ["Name=", eff[eff.index("OName=") + 1]]
		elif "OName" in eff:
			meff = ["Name", eff[eff.index("OName") + 1]]
		elif "OTrait" in eff:
			meff = ["Trait", eff[eff.index("OTrait") + 1]]
		elif "OText" in eff:
			meff = ["Text", eff[eff.index("OText") + 1]]
		elif "OStand" in eff:
			meff = ["Stand"]
		elif "ORest" in eff:
			meff = ["Rest"]
		elif "OReverse" in eff:
			meff = ["Reverse"]
		emore = self.cont_times(meff, estage, self.cd)

		if "OCB" in eff:
			estage = [s for s in self.pd[p]["Back"] if s != ""]
			emore1 = self.cont_times(meff1, estage, self.cd)

			if "Olower" not in eff and len(emore) + len(emore1) < eff[eff.index("OMore") + 1]:
				return False
			elif "Olower" in eff and len(emore) + len(emore1) > eff[eff.index("OMore") + 1]:
				return False
		elif "Oall" in eff:
			if "Olower" not in eff and (len(emore) < eff[eff.index("OMore") + 1] or len(emore) != len(estage)):
				return False
			elif "Olower" in eff and (len(emore) > eff[eff.index("OMore") + 1] or len(emore) != len(estage)):
				return False
		elif "O&" in eff:
			if "Olower" not in eff and len(set([self.cd[s].name for s in emore])) < eff[eff.index("OMore") + 1]:
				return False
			elif "Olower" in eff and len(set([self.cd[s].name for s in emore])) > eff[eff.index("OMore") + 1]:
				return False
		elif "Olower" in eff and len(emore) > eff[eff.index("OMore") + 1]:
			return False
		elif "Olower" not in eff and len(emore) < eff[eff.index("OMore") + 1]:
			return False
		return True

	def cont_cards(self, eff, ind):
		p = ind[-1]
		if "opp" in eff:
			if ind[-1] == "1":
				p = "2"
			elif ind[-1] == "2":
				p = "1"
		if "Memory" in eff:
			cards = [s for s in self.pd[p]["Memory"] if s != ""]
		elif "Waiting" in eff:
			cards = [s for s in self.pd[p]["Waiting"] if s != ""]
		elif "LevelZ" in eff:
			cards = [s for s in self.pd[p]["Level"] if s != ""]
		elif "Stock" in eff:
			cards = [s for s in self.pd[p]["Stock"] if s != ""]
		elif "Library" in eff:
			cards = [s for s in self.pd[p]["Library"] if s != ""]
		elif "Hand" in eff:
			cards = [s for s in self.pd[p]["Hand"] if s != ""]
		elif "CX" in eff:
			cards = [s for s in self.pd[p]["Climax"] if s != ""]
		elif "Clock" in eff:
			cards = [s for s in self.pd[p]["Clock"] if s != ""]
		elif "Back" in eff:
			cards = [s for s in self.pd[p]["Back"] if s != ""]
		elif "Middle" in eff:
			cards = [s for s in self.pd[p]["Center"] if s != "" and self.pd[p]["Center"].index(s) == 1]
		elif "Center" in eff:
			cards = [s for s in self.pd[p]["Center"] if s != ""]
		else:
			cards = [s for s in self.pd[p]["Center"] + self.pd[p]["Back"] if s != ""]

		if "other" in eff and ind in cards:
			cards.remove(ind)
		return cards

	def cont_times(self, eff, cs, cd):
		if "Face-down" in eff:
			nc = [n for n in cs if cd[n].back]
		elif "NameSet" in eff:
			names = eff[eff.index("NameSet") + 1].split("_")
			nc = []
			for n in cs:
				if cd[n].back:
					continue
				if n != "":
					for nx in range(int(len(names) / 2)):
						if names[nx] in cd[n].name_t:
							if names[nx + int(len(names) / 2)] != "":
								for ss in sn["Title"][names[nx + int(len(names) / 2)]]:
									if ss in cd[n].cid:
										nc.append(n)
							else:
								nc.append(n)
		elif "CName&Reverse" in eff:
			names = eff[eff.index("CName&Reverse") + 1].split("_")
			nc = [n for n in cs if any(name in cd[n].name_t for name in names[:-1]) and cd[n].card == "Character" and cd[n].status == "Reverse"]
		elif "xName" in eff:
			names = eff[eff.index("xName") + 1].split("_")
			nc = [n for n in cs if any(name in cd[n].name_t for name in names)]
		elif "&Name=" in eff:
			names = eff[eff.index("&Name=") + 1].split("_")
			nn = []
			nc = []
			for n in cs:
				for name in names:
					if name in nn or n in nc:
						continue
					if any(name == ns for ns in self.cd[n].name_t.split("\n")):
						nn.append(name)
						nc.append(n)
		elif "NameWo" in eff:
			names = eff[eff.index("NameWo") + 1].split("_")
			nc = [n for n in cs if all(name not in cd[n].name_t for name in names)]
		elif "eName=" in eff:
			names = eff[eff.index("eName=") + 1].split("_")
			nc = [n for n in cs if any(name in cd[n].name_t for name in names)]
		elif "Name=" in eff or "eName=" in eff:
			names = eff[eff.index("Name=") + 1].split("_")
			nc = [n for n in cs if any(name in cd[n].name_t for name in names)]
		elif "NameA" in eff:
			names = eff[eff.index("NameA") + 1].split("_")
			nc = [n for n in cs if cd[n].name_t in names]
			nm = [cd[n].name_t for n in nc]
			if not all(nn in nm for nn in names):
				nc = []
		elif "CName" in eff:
			names = eff[eff.index("Name") + 1].split("_")
			nc = [n for n in cs if any(name in cd[n].name_t for name in names) and cd[n].card == "Character"]
		elif "NameO" in eff:
			names = eff[eff.index("NameO") + 1].split("_")
			nc = [n for n in cs if names[0] in cd[n].name_t and names[1] != cd[n].name_t]
		elif "Name" in eff:
			names = eff[eff.index("Name") + 1].split("_")
			nc = [n for n in cs if any(name in cd[n].name_t for name in names)]
		elif "Trait&L" in eff:
			traits = eff[eff.index("Trait&L") + 1].split("_")
			if ">=" in traits[-1]:
				nc = [n for n in cs if any(trait in cd[n].trait_t for trait in traits[:-1]) and cd[n].level_t >= int(traits[-1][-1])]
		elif "TraitN" in eff or "BTraitN" in eff:
			if "BTraitN" in eff:
				traits = eff[eff.index("BTraitN") + 1].split("_")
			else:
				traits = eff[eff.index("TraitN") + 1].split("_")
			nc = [n for n in cs if any(trait in cd[n].trait_t for trait in traits[:-1]) or traits[-1] in cd[n].name_t]
		elif "Trait" in eff or "BTrait" in eff:
			if "BTrait" in eff:
				traits = eff[eff.index("BTrait") + 1].split("_")
			elif "ATrait" in eff:
				traits = eff[eff.index("ATrait") + 1].split("_")
			elif "Trait" in eff:
				traits = eff[eff.index("Trait") + 1].split("_")
			if traits == [""]:
				nc = [n for n in cs if len(cd[n].trait_t) <= 0 and "Character" in cd[n].card]
			elif "ATrait" in eff:
				nc = [n for n in cs if all(trait in cd[n].trait_t for trait in traits)]
			else:
				nc = [n for n in cs if any(trait in cd[n].trait_t for trait in traits)]
		elif "ColourCx" in eff:
			colours = eff[eff.index("ColourCx") + 1].split("_")
			nc = [n for n in cs if "Climax" in cd[n].card and (colours[-1] in cd[n].trait_t or any(colour.lower() in cd[n].colour for colour in colours[:-1]))]
		elif "CColourT" in eff:
			colours = eff[eff.index("CColourT") + 1].split("_")
			nc = [n for n in cs if "Character" in cd[n].card and (colours[-1] in cd[n].trait_t or any(colour.lower() in cd[n].colour for colour in colours[:-1]))]
		elif "Colour" in eff:
			colours = eff[eff.index("Colour") + 1].split("_")
			nc = [n for n in cs if any(colour.lower() in cd[n].colour for colour in colours)]
		elif "CLevel" in eff:
			if "<=p+1" in eff:
				nc = [n for n in cs if cd[n].card == "Character" and cd[n].level_t <= len(self.pd[n[-1]]["Level"]) + int(eff[eff.index("CLevel") + 1][-1])]
			elif "==" in eff:
				nc = [n for n in cs if cd[n].card == "Character" and cd[n].level_t == eff[eff.index("CLevel") + 1]]
			elif "Llower" in eff:
				nc = [n for n in cs if cd[n].card == "Character" and cd[n].level_t <= eff[eff.index("CLevel") + 1]]
			elif "Llower" not in eff:
				nc = [n for n in cs if cd[n].card == "Character" and cd[n].level_t >= eff[eff.index("CLevel") + 1]]
		elif "Level" in eff:
			if "Llower" in eff:
				nc = [n for n in cs if cd[n].level_t <= eff[eff.index("Level") + 1]]
			elif "Llower" not in eff:
				nc = [n for n in cs if cd[n].level_t >= eff[eff.index("Level") + 1]]
		elif "CText" in eff:
			text = eff[eff.index("CText") + 1].split("_")
			nc = [n for n in cs if cd[n].card == "Character" and any(any(text1.lower() in tx[0].lower() and f"\"{text1.lower()}\"" not in tx[0].lower() for text1 in text) for tx in cd[n].text_c)]
		elif "Text" in eff:
			text = eff[eff.index("Text") + 1].split("_")
			nc = [n for n in cs if any(any(text1.lower() in tx[0].lower() and f"\"{text1.lower()}\"" not in tx[0].lower() for text1 in text) for tx in cd[n].text_c)]
		elif "Trigger" in eff:
			triggers = eff[eff.index("Trigger") + 1].split("_")
			nc = [n for n in cs if any(trigger in cd[n].trigger for trigger in triggers)]
		elif "Character" in eff:
			nc = [n for n in cs if cd[n].card == "Character"]
		elif "Climax" in eff:
			nc = [n for n in cs if cd[n].card == "Climax"]
		elif "Event" in eff:
			nc = [n for n in cs if cd[n].card == "Event"]
		elif "Rest" in eff:
			nc = [n for n in cs if cd[n].status == "Rest"]
		elif "Stand" in eff:
			nc = [n for n in cs if cd[n].status == "Stand"]
		elif "Reverse" in eff:
			nc = [n for n in cs if cd[n].status == "Reverse"]
		else:
			nc = cs
		for n in list(nc):
			if "Memory" in cd[n].pos_new and cd[n].back and "Face-down" not in eff:
				nc.remove(n)
		return nc

	def cont_remove(self, power, ind, player):
		pp = False
		otd = power[2].split("_")[1]
		card = self.cd[ind]
		stage = list(self.pd[player]["Center"] + self.pd[player]["Back"])

		if "Turn" in power:
			if "Topp" in power and self.gd["active"] == otd[-1]:
				pp = True
			elif "Topp" not in power and self.gd["active"] != otd[-1]:
				pp = True

		if "plevel" in power:
			if "p==" in power and len(self.pd[otd[-1]]["Level"]) != power[power.index("plevel") + 1]:
				pp = True
			elif "plower" in power and len(self.pd[otd[-1]]["Level"]) > power[power.index("plevel") + 1]:
				pp = True
			elif "plower" not in power and len(self.pd[otd[-1]]["Level"]) < power[power.index("plevel") + 1]:
				pp = True

		if "pHand" in power:
			if "Hand" not in self.cd[otd].pos_new:
				pp = True
			else:
				cx = []
				cxi = 0
				if "ClimaxWR" in power:
					cxi = power[power.index("ClimaxWR") + 1]
					cx = [s for s in self.pd[ind[-1]]["Waiting"] if "Climax" in self.cd[s].card]
				elif "NameWR" in power:
					cxi = power[power.index("NameWR") + 1]
					cx = self.cont_times(power, self.pd[ind[-1]]["Waiting"], self.cd)
				elif "NameCL" in power:
					cxi = power[power.index("NameCL") + 1]
					cx = self.cont_times(power, self.pd[ind[-1]]["Clock"], self.cd)
				elif "Deck" in power:
					cxi = power[power.index("Deck") + 1]
					cx = self.pd[player]["Library"]
				elif "OMore" in power:
					cxi = power[power.index("OMore") + 1]
					cx = "O" * cxi
					if not self.omore(power, otd):
						if "pHlower" in power:
							cx = "O" * (cxi + 1)
						else:
							cx = "O" * (cxi - 1)

				if "pHlower" in power and len(cx) > cxi:
					pp = True
				elif "pHlower" not in power and len(cx) < cxi:
					pp = True
		elif "sMemory" in power:
			if otd != ind and "Memory" not in self.cd[otd].pos_new:
				pp = True
			if otd != ind and "Hand" in power and "Hand" not in self.cd[ind].pos_new:
				pp = True
		elif "sWaiting" in power:
			if "Waiting" not in self.cd[otd].pos_new:
				pp = True
		elif "sMiddle" in power:
			if otd not in stage:
				pp = True
			elif card.pos_new != "Center1" and "other" not in power:
				pp = True
			elif "other" in power and card.pos_new == "Center1" and ind in power[2]:
				pp = True
			elif "other" in power and ind not in power[2] and card.pos_new == "Center1":
				if "Level" in power and otd in stage:
					if "lower" in power and card.level_t > power[power.index("Level") + 1]:
						pp = True
					elif "lower" not in power and card.level_t < power[power.index("Level") + 1]:
						pp = True
		elif "sCenter" in power:
			if otd not in stage:
				pp = True
			elif "Center" not in card.pos_new:
				pp = True
		elif "Stage" in power and "Opposite" not in power:
			if self.cd[otd].card == "Climax" and otd not in self.pd[otd[-1]]["Climax"]:
				pp = True
			elif otd not in stage:
				if otd[-1] != player and "opp" in power:
					if otd not in list(self.pd[otd[-1]]["Center"] + self.pd[otd[-1]]["Back"]):
						pp = True
				else:
					pp = True
			elif "Hand" not in power and "Center" not in card.pos_new and "Back" not in card.pos_new:
				pp = True
			elif "Hand" in power and "Hand" not in card.pos_new and "Hand" not in card.pos_old:
				pp = True
			elif "Hand" in power and self.gd["stock_payed"]:
				self.gd["stock_payed"] = False
				pp = True
			if "OCenter" in power and "Center" not in self.cd[otd].pos_new:
				pp = True
			if "ONot_Reverse" in power and self.cd[otd].status == "Reverse":
				pp = True
		elif "StageCX" in power and len(self.pd[ind[-1]]["Climax"]) <= 0:
			pp = True
		elif "StageCX" in power and "cx" in power and power[power.index("cx") + 1] not in self.cd[self.pd[ind[-1]]["Climax"]].name_t:
			pp = True
		elif "Alarm" in power:
			if len(self.pd[ind[-1]]["Clock"]) <= 0:
				pp = True
			elif otd != self.pd[ind[-1]]["Clock"][-1]:
				pp = True
			elif "plevel" in power:
				if len(self.pd[ind[-1]]["Level"]) < power[power.index("plevel") + 1]:
					pp = True
		elif "Climax" in power[2]:
			if len(self.pd[otd[-1]]["Climax"]) < 1 or (len(self.pd[otd[-1]]["Climax"]) > 0 and otd not in self.pd[otd[-1]]["Climax"]):
				pp = True
		if "Not_Reverse" in power and card.status == "Reverse":
			pp = True

		if "no_encore_self" in power:
			pp = True

		if "cx" in power:
			if len(self.pd[otd[-1]]["Climax"]) < 1 or (len(self.pd[otd[-1]]["Climax"]) > 0 and power[power.index("cx") + 1] not in self.cd[self.pd[otd[-1]]["Climax"][0]].name_t):
				pp = True
		if "Experience" in power and "Opposite" not in power:
			if "eName=" in power and len(self.cont_times(power, self.pd[ind[-1]]["Level"], self.cd)) < power[power.index("Experience") + 1]:
				pp = True
			elif sum([self.cd[lv].level_t for lv in self.pd[ind[-1]]["Level"] if lv != ""]) < power[power.index("Experience") + 1]:
				pp = True

		if "OMore" in power:
			if not self.omore(power, otd):
				pp = True

		if not pp:
			if "Battle" in power:
				deff = ""
				pp = True
				if self.gd["attacking"][0] != "" and self.gd["attacking"][0] == "f":
					if self.gd["attacking"][0][-1] == "1":
						op = "2"
					elif self.gd["attacking"][0][-1] == "2":
						op = "1"
					if "C" in self.gd["attacking"][4]:
						deff = self.pd[op]["Center"][self.gd["attacking"][3]]
					elif "B" in self.gd["attacking"][4]:
						deff = self.pd[op]["Back"][self.gd["attacking"][3]]

					if "oplevel" in power:
						opp = ""
						if "Center" in self.cd[ind].pos_new:
							opp = self.pd[op]["Center"][self.m[int(self.cd[ind].pos_new[-1])]]
						if opp:
							pp = False
							if "oplower" in power and self.cd[opp].level_t > power[power.index("oplevel") + 1]:
								pp = True
							elif "oplower" not in power and self.cd[opp].level_t < power[power.index("oplevel") + 1]:
								pp = True
					elif deff != "":
						pp = False
						if ind == self.gd["attacking"][0]:
							if "olevelvsself" in power:
								if "olower" not in power and self.cd[deff].level_t <= card.level_t:
									pp = True
								elif "olower" in power and self.cd[deff].level_t >= card.level_t:
									pp = True
							elif "olevel" in power and self.cd[deff].level_t < power[power.index("olevel") + 1]:
								pp = True
							elif "otrait" in power and all(otr not in self.cd[deff].trait_t for otr in power[power.index("otrait") + 1].split("_")):
								pp = True
						elif deff == ind:
							if "olevelsvself" in power:
								if "olower" not in power and self.cd[self.gd["attacking"][0]].level_t <= card.level_t:
									pp = True
								elif "olower" in power and self.cd[self.gd["attacking"][0]].level_t >= card.level_t:
									pp = True
							elif "olevel" in power and self.cd[self.gd["attacking"][0]].level_t < power[power.index("olevel") + 1]:
								pp = True
							elif "otrait" in power and all(otr not in self.cd[self.gd["attacking"][0]].trait_t for otr in power[power.index("otrait") + 1].split("_")):
								pp = True
			elif "Assist" in power:
				if "Center" in card.pos_new:
					if "1" in card.pos_new:
						if otd not in self.pd[player]["Back"]:
							pp = True
						elif "Text" in power and all(not any(txt.lower() in txtl[0].lower() and f"{txt.lower()}" not in txtl[0].lower() for txt in power[power.index("Text") + 1].split("_")) for txtl in card.text_c):
							pp = True
						elif "Name" in power and all(nn not in card.name_t for nn in power[power.index("Name") + 1].split("_")):
							pp = True
						elif "Trait" in power and all(nn not in card.trait_t for nn in power[power.index("Trait") + 1].split("_")):
							pp = True
					else:
						if otd not in self.pd[player]["Back"][int(int(card.pos_new[-1]) / 2)]:
							pp = True
						elif "Trait" in power and all(nn not in card.trait_t for nn in power[power.index("Trait") + 1].split("_")):
							pp = True
						elif "Name" in power and all(nn not in card.name_t for nn in power[power.index("Name") + 1].split("_")):
							pp = True
						elif "Text" in power and all(not any(txt.lower() in txtl[0].lower() and f"{txt.lower()}" not in txtl[0].lower() for txt in power[power.index("Text") + 1].split("_")) for txtl in card.text_c):
							pp = True
				elif "Back" in card.pos_new:
					pp = True
			elif "Marker#" in power:
				if ind in self.pd[ind[-1]]["marker"] and len(self.pd[ind[-1]]["marker"][ind]) < power[power.index("Marker#") + 1]:
					pp = True
				elif ind not in self.pd[ind[-1]]["marker"]:
					pp = True
			elif "Each" in power:
				if otd == ind:
					pp = True
				elif otd not in stage:
					pp = True
			elif "All" in power:
				cards = [s for s in stage if s != ""]
				if len(self.cont_times(power, cards, self.cd)) != len(cards):
					pp = True
			elif "Hands" in power:
				if "HandvsOpp" in power:
					if ind[-1] == "1":
						op = "2"
					elif ind[-1] == "2":
						op = "1"
					if "Hlower" not in power and len(self.pd[ind[-1]]["Hand"]) <= len(self.pd[op]["Hand"]):
						pp = True
					elif "Hlower" in power and len(self.pd[ind[-1]]["Hand"]) >= len(self.pd[op]["Hand"]):
						pp = True
				elif "lower" in power and len(self.pd[ind[-1]]["Hand"]) > power[power.index("Hands") + 1]:
					pp = True
				elif "lower" not in power and len(self.pd[ind[-1]]["Hand"]) < power[power.index("Hands") + 1]:
					pp = True
			elif "Stocks" in power:
				if "lower" in power and len(self.pd[player]["Stock"]) > power[power.index("Stocks") + 1]:
					pp = True
				elif "lower" not in power and len(self.pd[player]["Stock"]) < power[power.index("Stocks") + 1]:
					pp = True
			elif "Opposite" in power:
				if ind[-1] == "1":
					op = "2"
				else:
					op = "1"

				opp = ""
				if "Center" in self.cd[otd].pos_new:
					opp = self.pd[op]["Center"][self.m[int(self.cd[otd].pos_new[-1])]]

				if opp != "":
					if "Stage" in power and "Center" not in self.cd[otd].pos_new:
						pp = True
					if "OPtraits" in power:
						if "OPlower" not in power and len([t for t in self.cd[opp].trait_t if t != ""]) < power[power.index("OPtraits") + 1]:
							pp = True
						elif "OPlower" in power and len([t for t in self.cd[opp].trait_t if t != ""]) > power[power.index("OPtraits") + 1]:
							pp = True
					elif "OPlevel" in power:
						if "OPlower" not in power and self.cd[opp].level_t < power[power.index("OPlevel") + 1]:
							pp = True
						elif "OPlower" in power and self.cd[opp].level_t > power[power.index("OPlevel") + 1]:
							pp = True
					elif "OPcolour" in power:
						if all(_.lower() not in self.cd[opp].colour for _ in power[power.index("OPcolour") + 1].split("_") ):
							pp = True

					if "Experience" in power:
						if "eName=" in power and len(self.cont_times(power, self.pd[opp[-1]]["Level"], self.cd)) < power[power.index("Experience") + 1]:
							pp = True
						elif sum([self.cd[lv].level_t for lv in self.pd[opp[-1]]["Level"] if lv != ""]) < power[power.index("Experience") + 1]:
							pp = True

				if "Center" not in card.pos_new:
					pp = True
				elif opp == "":  
					pp = True
			elif "Clocks" in power:
				if "opp" in power and ind[-1] == "1":
					op = "2"
				elif "opp" in power and ind[-1] == "2":
					op = "1"
				else:
					op = ind[-1]
				if len(self.pd[op]["Clock"]) < int(power[power.index("Clocks") + 1]):
					pp = True
			elif "LevelP" in power:
				if otd not in stage:
					pp = True
				elif "lower" not in power:
					if self.cd[ind].level_t <= len(self.pd[ind[-1]]["Level"]):
						pp = True
			elif "X" in power:
				if "xoplevel" in power:
					pp = True
				elif "xhighlevel" in power:
					pp = True
			elif "Aselected" in power:
				pp = True
				if self.cd[ind].aselected:
					if self.cd[ind].aselected in self.pd[ind[-1]]["Center"] or self.cd[ind].aselected in self.pd[ind[-1]]["Back"]:
						pp = False
			if not pp:
				if "Trait" in power:
					if all(_ not in self.cd[ind].trait_t for _ in power[power.index("Trait") + 1].split("_")):
						pp = True
		return pp

	def cont_cc(self, ind, peff):
		if "power" in peff:
			self.cd[ind].update_power()
			if self.cd[ind].power_t <= 0:
				self.power_zero.append(ind)
		elif "soul" in peff:
			self.cd[ind].update_soul()
		elif "level" in peff:
			self.cd[ind].update_level()
		elif "ability" in peff:
			self.cd[ind].update_ability()
			if ind not in self.cont_recheck:
				self.cont_recheck[ind] = []
			self.cont_recheck[ind].append(peff[1:])
		elif "trait" in peff:
			self.cd[ind].update_trait()
		elif "name" in peff:
			self.cd[ind].update_name()
		elif "cost" in peff:
			self.cd[ind].update_cost()

	def cont_add(self, peff, ind, player, instage=True):
		card = self.cd[ind]
		if card.card == "Climax" and "Stage" in peff:
			for x in range(peff.count("Stage")):
				peff.remove("Stage")
				peff.append("StageCX")
		if "pHand" in peff and "Hand" not in card.pos_new:
			return
		elif "Stage" in peff and "Center" not in card.pos_new and "Back" not in card.pos_new:
			return
		elif "sMemory" in peff and "Memory" not in card.pos_new:
			return
		elif "sWaiting" in peff and "Waiting" not in card.pos_new:
			return
		elif "sMiddle" in peff and card.pos_new != "Center1":
			return
		elif "sCenter" in peff and "Center" not in card.pos_new:
			return
		elif "Alarm" in peff and (len(self.pd[ind[-1]]["Clock"]) <= 0 or (len(self.pd[ind[-1]]["Clock"]) > 0 and self.pd[ind[-1]]["Clock"][-1] != ind)):
			if "plevel" in peff and len(self.pd[ind[-1]]["Level"]) >= peff[peff.index("plevel") + 1]:
				pass
			else:
				return
		elif "StageCX" in peff and len(self.pd[ind[-1]]["Climax"]) <= 0:
			return
		elif "StageCX" in peff and "cx" in peff and peff[peff.index("cx") + 1] not in self.cd[self.pd[ind[-1]]["Climax"]].name_t:
			return

		if "Not_Reverse" in peff and card.status == "Reverse":
			return

		if "plevel" in peff:
			if "p==" in peff and len(self.pd[ind[-1]]["Level"]) == peff[peff.index("plevel") + 1]:
				return
			elif "plower" in peff and len(self.pd[ind[-1]]["Level"]) > peff[peff.index("plevel") + 1]:
				return
			elif "plower" not in peff and len(self.pd[ind[-1]]["Level"]) < peff[peff.index("plevel") + 1]:
				return

		if "Turn" in peff:
			if "Topp" in peff and self.gd["active"] in ind[-1]:
				return
			elif "Topp" not in peff and self.gd["active"] not in ind[-1]:
				return

		if "astock" in peff:
			if "astock" not in self.gd["markerstock"]:
				self.gd["markerstock"].append("astock")
			return

		if "estock" in peff:
			if "estock" not in self.gd["markerstock"]:
				self.gd["markerstock"].append("estock")
			return

		if "contadd" in peff:
			if "Add" in peff:
				add = peff[peff.index("Add") + 1]
				if add[0] not in self.gd["contadd"]:
					self.gd["contadd"][add[0]] = {}
				if player not in self.gd["contadd"][add[0]]:
					self.gd["contadd"][add[0]][player] = {}
				if peff[1] not in self.gd["contadd"][add[0]][player]:
					self.gd["contadd"][add[0]][player][peff[1]] = add[1]
				else:
					self.gd["contadd"][add[0]][player][peff[1]] += add[1]
			return

		if ind not in peff[3]:
			peff.insert(3, f"O_{ind}")
		if card.card == "Climax":
			peff[3] += f"_Climax"
		if "opp" in peff:
			if player == "1":
				p = "2"
			elif player == "2":
				p = "1"
		else:
			p = player
		pcards = self.cont_cards(peff, ind)
		ptimes = self.cont_times(peff, pcards, self.cd)

		if "Climax" in peff[3]:
			if len(self.pd[player]["Climax"]) < 1 or (len(self.pd[player]["Climax"]) > 0 and ind not in self.pd[player]["Climax"]):
				return
		if "Experience" in peff:
			if "eName=" in peff:
				if len(self.cont_times(peff, self.pd[p]["Level"], self.cd)) < peff[peff.index("Experience") + 1]:
					return
			elif sum([self.cd[lv].level_t for lv in self.pd[p]["Level"] if lv != ""]) < peff[peff.index("Experience") + 1]:
				return

		if "All" in peff:
			if len(ptimes) != len(pcards):
				return
		if "Hands" in peff:
			if "HandvsOpp" in peff:
				if ind[-1] == "1":
					op = "2"
				elif ind[-1] == "2":
					op = "1"
				if "Hlower" not in peff and len(self.pd[ind[-1]]["Hand"]) <= len(self.pd[op]["Hand"]):
					return
				elif "Hlower" in peff and len(self.pd[ind[-1]]["Hand"]) >= len(self.pd[op]["Hand"]):
					return
			elif "lower" not in peff and len(self.pd[p]["Hand"]) < peff[peff.index("Hands") + 1]:
				return
			elif "lower" in peff and len(self.pd[p]["Hand"]) > peff[peff.index("Hands") + 1]:
				return
		if "Stocks" in peff:
			if "lower" in peff and len(self.pd[p]["Stock"]) > peff[peff.index("Stocks") + 1]:
				return
			elif "lower" not in peff and len(self.pd[p]["Stock"]) < peff[peff.index("Stocks") + 1]:
				return
		if "Clocks" in peff:
			if "lower" in peff and len(self.pd[p]["Clock"]) > peff[peff.index("Clocks") + 1]:
				return
			elif "lower" not in peff and len(self.pd[p]["Clock"]) < peff[peff.index("Clocks") + 1]:
				return
		if "OMore" in peff:
			if not self.omore(peff, ind):
				return
		if "cx" in peff:
			if len(self.pd[p]["Climax"]) < 1 or (len(self.pd[p]["Climax"]) > 0 and peff[peff.index("cx") + 1] not in self.cd[self.pd[ind[-1]]["Climax"][0]].name_t):
				return
		if "Marker#" in peff:
			if ind not in self.pd[p]["marker"] or (ind in self.pd[p]["marker"] and len(self.pd[p]["marker"][ind]) < peff[peff.index("Marker#") + 1]):
				return
		if "pHand" in peff:
			cx = []
			if "ClimaxWR" in peff:
				cx = [s for s in self.pd[ind[-1]]["Waiting"] if "Climax" in self.cd[s].card]
				cxi = peff[peff.index("ClimaxWR") + 1]
			elif "NameWR" in peff:
				cx = self.cont_times(peff, self.pd[ind[-1]]["Waiting"], self.cd)
				cxi = peff[peff.index("NameWR") + 1]
			elif "NameCL" in peff:
				cx = self.cont_times(peff, self.pd[ind[-1]]["Clock"], self.cd)
				cxi = peff[peff.index("NameCL") + 1]
			elif "Deck" in peff:
				cx = self.pd[player]["Library"]
				cxi = peff[peff.index("Deck") + 1]
			elif "OMore" in peff:
				cxi = peff[peff.index("OMore") + 1]
				cx = "O" * cxi
				if not self.omore(peff, ind):
					if "pHlower" in peff:
						cx = "O" * (cxi + 1)
					else:
						cx = "O" * (cxi - 1)

			if "pHlower" in peff and len(cx) > cxi:
				return
			elif "pHlower" not in peff and len(cx) < cxi:
				return

		if peff[0] == 0:
			pp = False
			if "power" in peff:
				cc = card.power_c
			elif "soul" in peff:
				cc = card.soul_c
			elif "level" in peff:
				cc = card.level_c
			elif "trait" in peff:
				cc = card.trait_c
			elif "ability" in peff:
				cc = card.text_c
			elif "cost" in peff:
				cc = card.cost_c
			elif "name" in peff:
				cc = card.name_c

			if "Each" in peff:
				if "marker" in peff:
					if ind in self.pd[ind[-1]]["marker"]:
						for mnx in range(len(self.pd[ind[-1]]["marker"][ind])):
							cc.append(peff[1:] + [mnx])
							self.cont_cc(ind, peff)
				else:
					if "marker" in peff and ind not in self.pd[p]["marker"]:
						return
					if "Traits" in peff:
						ptimes = []
						for t in pcards:
							for tr in self.cd[t].trait_t:
								if tr not in ptimes:
									ptimes.append(tr)
					for mnx in range(len(ptimes)):
						cc.append(peff[1:] + [mnx])
						self.cont_cc(ind, peff)
			elif "X" in peff:
				tip = 0
				if "xoplevel" in peff:
					if ind[-1] == "1":
						op = "2"
					else:
						op = "1"
					opp = self.pd[op]["Center"][self.m[int(card.pos_new[-1])]]
					if opp != "":
						tip = self.cd[opp].level
				elif "xhighlevel" in peff:
					if len(ptimes) > 0:
						tip = self.cd[sorted(ptimes, key=lambda z: self.cd[z].level_t)[-1]].level_t
				peff[1] = tip * peff[peff.index("x") + 1]
				if peff[1] != 0 and peff[1:] not in cc:
					cc.append(peff[1:])
					self.cont_cc(ind, peff)
			elif "Battle" in peff:
				deff = ""
				if self.gd["attacking"][0] != "" and self.gd["attacking"][0] == "f":
					if self.gd["attacking"][0][-1] == "1":
						op = "2"
					elif self.gd["attacking"][0][-1] == "2":
						op = "1"
					if "C" in self.gd["attacking"][4]:
						deff = self.pd[op]["Center"][self.gd["attacking"][3]]
					elif "B" in self.gd["attacking"][4]:
						deff = self.pd[op]["Back"][self.gd["attacking"][3]]

					if "xoplevel" in peff:
						opp = self.pd[op]["Center"][self.m[int(self.cd[ind].pos_new[-1])]]
						peff[1] = peff[1] * self.cd[opp].level_t

					if "oplevel" in peff:
						opp = ""
						if "Center" in self.cd[ind].pos_new:
							opp = self.pd[op]["Center"][self.m[int(self.cd[ind].pos_new[-1])]]
						if opp:
							if "oplower" in peff and self.cd[opp].level_t <= peff[peff.index("oplevel") + 1]:
								pp = True
							elif "oplower" not in peff and self.cd[opp].level_t >= peff[peff.index("oplevel") + 1]:
								pp = True
					elif deff != "":
						if ind == self.gd["attacking"][0]:
							if "xolevel" in peff:
								peff[1] = peff[1] * self.cd[deff].level_t
							if "olevelvsself" in peff:
								if "olower" not in peff and self.cd[deff].level_t < card.level_t:
									pp = True
								elif "olower" in peff and self.cd[deff].level_t < card.level_t:
									pp = True
							elif "olevel" in peff and self.cd[deff].level_t >= peff[peff.index("olevel") + 1]:
								pp = True
							elif "otrait" in peff and any(otr in self.cd[deff].trait_t for otr in peff[peff.index("otrait") + 1].split("_")):
								pp = True
							elif "olevel" not in peff and "otrait" not in peff:
								pp = True
						elif deff == ind:
							if "xolevel" in peff:
								peff[1] = peff[1] * self.cd[self.gd["attacking"][0]].level_t
							if "olevelvsself" in peff:
								if "olower" not in peff and self.cd[self.gd["attacking"][0]].level_t < card.level_t:
									pp = True
								elif "olower" in peff and self.cd[self.gd["attacking"][0]].level_t < card.level_t:
									pp = True
							elif "olevel" in peff and self.cd[self.gd["attacking"][0]].level_t >= peff[peff.index("olevel") + 1]:
								pp = True
							elif "otrait" in peff and any(otr in self.cd[self.gd["attacking"][0]].trait_t for otr in peff[peff.index("otrait") + 1].split("_")):
								pp = True
							elif "olevel" not in peff and "otrait" not in peff:
								pp = True
			elif "Opposite" in peff:
				if ind[-1] == "1":
					op = "2"
				else:
					op = "1"

				opp = ""
				if "Center" in card.pos_new:
					opp = self.pd[op]["Center"][self.m[int(card.pos_new[-1])]]

				if opp != "":
					if "OPlevel" in peff:
						if "OPlower" not in peff and self.cd[opp].level_t < peff[peff.index("OPlevel") + 1]:
							return
						elif "OPlower" in peff and self.cd[opp].level_t > peff[peff.index("OPlevel") + 1]:
							return
					elif "OPcolour" in peff:
						if all(_.lower() not in self.cd[opp].colour for _ in peff[peff.index("OPcolour") + 1].split("_")):
							return
				else:
					return
				pp = True
			elif "Aselected" in peff:
				if self.cd[ind].aselected:
					if self.cd[ind].aselected not in self.pd[ind[-1]]["Center"] and self.cd[ind].aselected not in self.pd[ind[-1]]["Back"]:
						self.cd[ind].aselected = ""
					else:
						pp = True
			else:
				pp = True

			if pp and peff[1:] not in cc:
				cc.append(peff[1:])
				self.cont_cc(ind, peff)
		elif peff[0] == -2 or peff[0] == -1 or peff[0] == -32:
			if peff[0] == -2 and ind in ptimes:
				ptimes.remove(ind)
			elif peff[0] == -32 and ind not in ptimes:
				ptimes.append(ind)

			markers = 1
			if "Each" in peff:
				if "marker" in peff and ind not in self.pd[p]["marker"]:
					return
				elif "marker" in peff and ind in self.pd[p]["marker"]:
					markers = len(self.pd[player]["marker"][ind])
			if markers <= 0:
				markers = 1

			if "sCenter" in peff:
				peff[peff.index("sCenter")] = "OCenter"
			if "Not_Reverse" in peff:
				peff[peff.index("Not_Reverse")] = "ONot_Reverse"
			for pnx in ptimes:
				hid =[]
				if not instage:
					hid = list(peff[1:])
					hid[1] = -3

				if "power" in peff:
					cc = self.cd[pnx].power_c
				elif "soul" in peff:
					cc = self.cd[pnx].soul_c
				elif "level" in peff:
					cc = self.cd[pnx].level_c
				elif "ability" in peff:
					cc = self.cd[pnx].text_c
				elif "trait" in peff:
					cc = self.cd[pnx].trait_c
				elif "name" in peff:
					cc = self.cd[pnx].name_c
				elif "cost" in peff:
					cc = self.cd[pnx].cost_c

				if "xlevel" in peff:
					peff[1] = peff[peff.index("x") + 1] * self.cd[pnx].level_t
				for rr in range(markers):
					if peff[1:] + [rr] not in cc:
						if not instage and hid in cc:
							continue
						if "LevelP" in peff:
							if "lower" not in peff:
								if self.cd[pnx].level_t > len(self.pd[pnx[-1]]["Level"]):
									cc.append(peff[1:] + [rr])
						else:
							if "[AUTO] When this card becomes [REVERSE] in battle, put this card at the bottom of your deck." in str(peff[1]):
								tea = False
								for tex in cc:
									if len(tex) > 2 and "[AUTO] When this card becomes [REVERSE] in battle, put this card at the bottom of your deck." in tex[0] and "CONT" in tex[2]:
										tea = True
										break
								if tea:
									continue
							cc.append(peff[1:] + [rr])
				self.cont_cc(pnx, peff)
		elif peff[0] == -5:
			cind = self.pd[p]["Center"][1]
			if "other" in peff and ind == cind:
				cind = ""
			if cind and "Level" in peff:
				if "lower" in peff and self.cd[cind].level_t > peff[peff.index("Level") + 1]:
					cind = ""
				elif "lower" not in peff and self.cd[cind].level_t < peff[peff.index("Level") + 1]:
					cind = ""
			if cind and "Trait" in peff:
				if all(tt not in self.cd[cind].trait_t for tt in peff[peff.index("Trait") + 1].split("_")):
					cind = ""

			if cind != "":
				if "power" in peff:
					cc = self.cd[cind].power_c
				elif "soul" in peff:
					cc = self.cd[cind].soul_c
				elif "cost" in peff:
					cc = self.cd[cind].cost_c
				elif "level" in peff:
					cc = self.cd[cind].level_c
				elif "ability" in peff:
					cc = self.cd[cind].text_c
				elif "trait" in peff:
					cc = self.cd[cind].trait_c
				elif "name" in peff:
					cc = self.cd[cind].name_c

				peff[peff.index("Middle")] = "sMiddle"
				if "other" in peff:
					peff.remove("other")
				if peff[1:] not in cc:
					cc.append(peff[1:])
					self.cont_cc(cind, peff)
		elif peff[0] == -6 and "Center" in card.pos_new:
			if ind[-1] == "1":
				op = "2"
			else:
				op = "1"

			opp = self.pd[op]["Center"][self.m[int(card.pos_new[-1])]]

			if opp != "":
				if "power" in peff:
					cc = self.cd[opp].power_c
				elif "soul" in peff:
					cc = self.cd[opp].soul_c
				elif "level" in peff:
					cc = self.cd[opp].level_c
				elif "cost" in peff:
					cc = self.cd[opp].cost_c
				elif "ability" in peff:
					cc = self.cd[opp].text_c
				elif "trait" in peff:
					cc = self.cd[opp].trait_c
				elif "name" in peff:
					cc = self.cd[opp].name_c

				if "OPtraits" in peff:
					if "OPlower" not in peff and len([t for t in self.cd[opp].trait_t if t != ""]) < peff[peff.index("OPtraits") + 1]:
						return
					elif "OPlower" in peff and len([t for t in self.cd[opp].trait_t if t != ""]) > peff[peff.index("OPtraits") + 1]:
						return

				if peff[1:] not in cc:
					cc.append(peff[1:])
					self.cont_cc(opp, peff)
		elif peff[0] == "front" and "Assist" in peff and "Back" in card.pos_new:
			for finx in range(int(card.pos_new[-1]), int(card.pos_new[-1]) + 2):
				if self.pd[p]["Center"][finx] != "":
					pp = True
					find = self.pd[p]["Center"][finx]
					front = self.cd[find]
					if "x" in peff and "xlevel" in peff:
						peff[1] = front.level_t * peff[peff.index("x") + 1]
					elif "x" in peff and "xlevTrait" in peff:
						trait = peff[peff.index("xlevTrait") + 1].split("_")
						asst = len([lv for lv in self.pd[ind[-1]]["Level"] if any(tr in self.cd[lv].trait_t for tr in trait)])
						peff[1] = asst * peff[peff.index("x") + 1]
					elif "lower" not in peff and "flevel" in peff and front.level_t < peff[peff.index("flevel") + 1]:
						pp = False
					elif "lower" in peff and "flevel" in peff and front.level_t > peff[peff.index("flevel") + 1]:
						pp = False

					if "Trait" in peff and all(tr not in front.trait_t for tr in peff[peff.index("Trait") + 1].split("_")):
						pp = False
					elif "Name" in peff and all(nn not in front.name_t for nn in peff[peff.index("Name") + 1].split("_")):
						pp = False
					elif "Text" in peff:
						if any(any(text.lower() in txt[0].lower() and f"\"{text.lower()}" not in txt[0].lower() for text in peff[peff.index('Text') + 1].split("_")) for txt in front.text_c):
							pass
						else:
							pp = False
					if pp:
						if "power" in peff:
							cc = self.cd[find].power_c
						elif "soul" in peff:
							cc = self.cd[find].soul_c
						elif "level" in peff:
							cc = self.cd[find].level_c
						elif "ability" in peff:
							cc = self.cd[find].text_c
						elif "cost" in peff:
							cc = self.cd[find].cost_c
						elif "trait" in peff:
							cc = self.cd[find].trait_c
						elif "name" in peff:
							cc = self.cd[find].name_c

						if peff[1:] not in cc:
							cc.append(peff[1:])
							self.cont_cc(find, peff)

	def cont_recheck_run(self):
		for ind in self.cont_recheck:
			for item in self.cont_recheck:
				if item[0].startswith(cont_ability) and item[1] > -9 and item[1] != 0:
					effect = ab.cont(a=item[0])
					if len(effect) < 4 and "multicond" not in effect:
						continue
					self.check_no_effect(effect, ind)

					fc = self.effs_sep(effect)
					for ff in fc:
						if fc[ff]:
							if "Experience" in item:
								fc[ff].append("Experience")
								fc[ff].append(item.index("Experience") + 1)
							self.cont_add(fc[ff], ind, ind[-1])
		self.cont_recheck = {}

	def check_no_effect(self, effect, ind):
		player = ind[-1]
		if "no_move" in effect:
			if ind in self.gd["movable"]:
				self.gd["movable"].remove(ind)
			self.update_movable(player)

		if "skip_attack" in effect:
			if "Attack" not in self.gd["skip"]:
				self.gd["skip"].append("Attack")
		if "no_damage" in effect:
			self.gd["no_damage"][ind[-1]].append(ind)
		if "no_damage_auto_opp" in effect:
			self.gd["no_damage_auto_opp"][ind[-1]] = True

		for rr in ("act", "clock", "climax", "Clrclimax", "ClrChname", "encore", "event", "backup"):
			if f"no_{rr}" in effect or ("Clr" in rr and f"any_{rr}" in effect):
				e = player
				if "opp" in effect:
					if player == "1":
						e = "2"
					elif player == "2":
						e = "1"
				if rr in ("backup", "event"):
					if "Battle" in effect and self.gd["phase"] in self.battle and self.gd["attacking"][1] == "f":
						self.gd[f"no_{rr}"][e] = True
					elif "Battle" not in effect:
						self.gd[f"no_{rr}"][e] = True
				elif "Clrclimax" in rr:
					self.gd[f"any_{rr}"][e] = True
				elif "ClrChname" in rr:
					self.gd[f"any_{rr}"][e].append(effect[effect.index("Name") + 1])
				else:
					self.gd[f"no_{rr}"][e] = True

	def effs_sep(self, effs):
		fc = {}
		for ff in [c for c in effs if c in self.cc]:
			fd = f"{ff[0]}"
			if fd in fc:
				fd += str(effs.index(ff))
			if fd not in fc:
				fc[fd] = []
			fc[fd] = effs[:effs.index(ff) + 1]
			effs = effs[effs.index(ff) + 1:]
		return fc

	def check_cont_ability(self, dt=0, act=True, *args):
		for rr in ("act", "clock", "climax", "event", "backup"):
			self.gd[f"no_{rr}"] = {"1": False, "2": False}
		self.gd["no_damage"] = {"1": [], "2": []}
		self.gd["no_damage_auto_opp"] = {"1": False, "2": False}
		self.gd["any_Clrclimax"] = {"1": False, "2": False}
		self.gd["any_ClrChname"] = {"1": [], "2": []}
		self.gd["markerstock"] = []
		self.gd["contadd"] = {}

		for player in list(self.pd.keys()):
			self.check_cont_hand(player)
			stage = list(self.pd[player]["Center"] + self.pd[player]["Back"])

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
				to_remove_c = []

				for power in card.power_c:
					if power[1] < 0:
						if self.cont_remove(power, ind, player) and power not in to_remove_p:
							to_remove_p.append(power)

				for soul in card.soul_c:
					if soul[1] < 0:
						if self.cont_remove(soul, ind, player) and soul not in to_remove_s:
							to_remove_s.append(soul)

				for text in card.text_c:
					if len(text) > 2 and -9 < text[1] < 0:
						if self.cont_remove(text, ind, player) and text not in to_remove_t:
							to_remove_t.append(text)

				for level in card.level_c:
					if level[1] < 0:
						if self.cont_remove(level, ind, player) and level not in to_remove_l:
							to_remove_l.append(level)

				for trait in card.trait_c:
					if trait[1] < 0 and trait[1] != -66:
						if self.cont_remove(trait, ind, player) and trait not in to_remove_tr:
							to_remove_tr.append(trait)

				for name in card.name_c:
					if name[1] < 0:
						if self.cont_remove(name, ind, player) and name not in to_remove_n:
							to_remove_n.append(name)

				for cost in card.cost_c:
					if cost[1] < 0:
						if self.cont_remove(cost, ind, player) and cost not in to_remove_c:
							to_remove_c.append(cost)

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
				for itemc in to_remove_c:
					card.cost_c.remove(itemc)


				for item in card.text_c:
					if item[0].startswith(cont_ability) and item[1] > -9 and item[1] != 0:
						effect = ab.cont(a=item[0])

						if len(effect) < 4 and "multicond" not in effect:
							continue
						if "pHand" in effect:
							continue
						if len(item) >= 4 and "give" in item[2]:
							effect.append(item[3])

						self.check_no_effect(effect, ind)

						if "multicond" in effect:
							effect = effect[1]
						else:
							effect = [effect]

						for effs in effect:
							fc = self.effs_sep(effs)
							for ff in fc:
								if fc[ff]:
									if "Experience" in item:
										fc[ff].append("Experience")
										fc[ff].append(item.index("Experience") + 1)
									self.cont_add(fc[ff], ind, player)

				if ind != "1" and ind != "2":
					card.update_power()
					if card.power_t <= 0:
						self.power_zero.append(ind)
					card.update_soul()
					card.update_ability()
					card.update_level()
					card.update_trait()
					card.update_name()
					card.update_cost()

			for field in ("Clock", "Memory", "Climax"):
				for ind in self.pd[player][field]:
					if ind in self.emptycards:
						continue
					if self.cd[ind].back:
						continue
					card = self.cd[ind]
					if card.card == "Climax" and field != "Climax":
						continue
					for item in card.text_c:
						if item[0].startswith(cont_ability) and item[1] > -9 and item[1] != 0:
							effect = ab.cont(a=item[0])
							if len(effect) < 4:
								continue

							if "multicond" in effect:
								effect = effect[1]
							else:
								effect = [effect]

							for effs in effect:
								fc = self.effs_sep(effs)
								for ff in fc:
									if fc[ff]:
										self.cont_add(fc[ff], ind, player, False)

			if self.check_cont_waiting:
				for ind in self.check_cont_waiting:
					if ind in self.pd[ind[-1]]["Waiting"]:
						to_remove_n = []
						for name in self.cd[ind].name_c:
							if name[1] < 0 and len(name) > 2:
								if self.cont_remove(name, ind, player) and name not in to_remove_n:
									to_remove_n.append(name)
						for itemn in to_remove_n:
							self.cd[ind].name_c.remove(itemn)
						if to_remove_n:
							self.cd[ind].update_name()

						for item in self.cd[ind].text_c:
							if item[0].startswith(cont_ability) and item[1] > -9 and item[1] != 0:
								effect = ab.cont(a=item[0])
								if len(effect) < 4:
									continue
								if "sWaiting" not in effect:
									continue
								if "name" in effect:
									self.cont_add(effect, ind, player, False)

		if self.cont_recheck:
			self.cont_recheck_run()

		for pind in reversed(self.power_zero):
			self.gd["no_cont_check"] = True
			self.send_to_waiting(pind)
		if "1" in self.gd["active"]:
			if not act or len(self.gd["stack"]["1"]) > 0:
				self.act_ability_show(hide=True)
			elif self.gd["popup_done"][1] and act:
				self.act_ability_show()

	def check_cont_hand(self, player):
		for ind in self.pd[player]["Hand"]:
			if ind in self.emptycards:
				continue
			if self.cd[ind].card == "Climax":
				continue
			card = self.cd[ind]

			to_remove_l = []
			to_remove_c = []

			for level in card.level_c:
				if level[1] < 0 and len(level) > 2:
					if self.cont_remove(level, ind, player) and level not in to_remove_l:
						to_remove_l.append(level)
			for cost in card.cost_c:
				if cost[1] < 0:
					if self.cont_remove(cost, ind, player) and cost not in to_remove_c:
						to_remove_c.append(cost)

			for iteml in to_remove_l:
				card.level_c.remove(iteml)
			if to_remove_l:
				card.update_level()
			for itemc in to_remove_c:
				card.cost_c.remove(itemc)
			if to_remove_c:
				card.update_cost()

			for item in card.text_c:
				if item[0].startswith(cont_ability) and item[1] > -9 and item[1] != 0:
					effect = ab.cont(a=item[0])
					if len(effect) < 4:
						continue
					if "pHand" not in effect:
						continue
					if "level" in effect or "cost" in effect:
						self.cont_add(effect, ind, player, False)

	def revealx(self, dt=0):
		ind = self.gd["ability_trigger"].split("_")[1]
		if len(self.pd[ind[-1]]["Res"]) < self.gd["effect"][0]:
			if len(self.pd[ind[-1]]["Library"]) > 0:
				temp = self.pd[ind[-1]]["Library"].pop(-1)
				card = self.cd[temp]
				self.mat[ind[-1]]["mat"].remove_widget(card)
				self.mat[ind[-1]]["mat"].add_widget(card)
				library = self.mat[ind[-1]]["field"]["Library"]
				card.show_front()
				card.setPos(library[0] - self.sd["padding"] / 4 - self.sd["card"][0], library[1] - self.sd["card"][1] / 3. * len(self.pd[ind[-1]]["Res"]), t="Res")
				self.pd[ind[-1]]["Res"].append(temp)
				Clock.schedule_once(self.revealx, move_dt_btw)
			else:
				if self.gd["reshuffle_trigger"]:
					self.gd["reshuffle_trigger_temp"] = str(self.gd["reshuffle_trigger"])
				self.gd["reshuffle_trigger"] = "revealx"
				self.gd["rrev"] = ind[-1]
				Clock.schedule_once(self.refresh, move_dt_btw)
				return False
		elif len(self.pd[ind[-1]]["Res"]) == self.gd["effect"][0]:
			if "do" in self.gd["ability_effect"]:
				self.gd["done"] = True
			if "xreveals" in self.gd["effect"]:
				for inx in self.pd[ind[-1]]["Res"]:
					self.gd["extra"].append(inx)
			if "shuff" in self.gd["effect"]:
				self.gd["no_cont_check"] = True
				for inx in list(self.pd[ind[-1]]["Res"]):
					self.send_to("Library", inx, wig=False, update_field=False)
				self.update_field_label()
				self.check_cont_ability()
			Clock.schedule_once(self.reveal_done, move_dt_btw)

	def reveal(self, dt=0):
		ind = self.gd["ability_trigger"].split("_")[1]
		if self.gd["effect"][0] == -9:
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
								self.gd["rrev"] = self.gd["active"]
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
					if "TTName" in self.gd["effect"]:
						traits = self.gd["effect"][self.gd["effect"].index("TTName") + 1].split("_")
						if any(tr in card.trait_t for tr in traits[:2]) or traits[-1] in card.name_t:
							rr = True
					elif "Name=" in self.gd["effect"]:
						if card.name in self.gd["effect"][self.gd["effect"].index("Name=") + 1]:
							rr = True
					elif "Name" in self.gd["effect"]:
						names = self.gd["effect"][self.gd["effect"].index("Name") + 1].split("_")
						if any(name in card.name for name in names):
							rr = True

					if "TraitE" in self.gd["effect"]:
						traits = self.gd["effect"][self.gd["effect"].index("TraitE") + 1].split("_")
						if any(tr in card.trait_t for tr in traits) or "Event" in card.card:
							rr = True
					elif "TraitL" in self.gd["effect"]:
						traits = self.gd["effect"][self.gd["effect"].index("TraitL") + 1].split("_")
						lvl = traits.pop(-1)
						if "<=p" in lvl:
							if any(tr in card.trait_t for tr in traits) and card.level_t <= len(self.pd[card.ind[-1]]["Level"]):
								rr = True
					elif "Trait" in self.gd["effect"]:
						traits = self.gd["effect"][self.gd["effect"].index("Trait") + 1].split("_")
						if any(tr in card.trait_t for tr in traits):
							rr = True
					if "CLevel" in self.gd["effect"]:
						if card.card == "Character":
							if "==x" in self.gd["effect"]:
								if "xdeclare" in self.gd["effect"]:
									if card.level_t == int(self.gd["numbers"]):
										rr = True
					elif "Level" in self.gd["effect"]:
						if "<=p" in self.gd["effect"]:
							if card.level_t <= len(self.pd[card.ind[-1]]["Level"]):
								rr = True
						elif "lower" in self.gd["effect"]:
							if card.level_t <= self.gd["effect"][self.gd["effect"].index("Level") + 1]:
								rr = True
						elif card.level_t >= self.gd["effect"][self.gd["effect"].index("Level") + 1]:
							rr = True
						if "Character" in self.gd["effect"]:
							if card.card != "Character":
								rr = False
					if "Cost" in self.gd["effect"]:
						if "<=p" in self.gd["effect"]:
							if card.cost_t <= len(self.pd[card.ind[-1]]["Level"]):
								rr = True
						elif "lower" in self.gd["effect"]:
							if card.cost_t <= self.gd["effect"][self.gd["effect"].index("Cost") + 1]:
								rr = True
						elif card.cost_t >= self.gd["effect"][self.gd["effect"].index("Cost") + 1]:
							rr = True
						if "Character" in self.gd["effect"]:
							if card.card != "Character":
								rr = False
					if "Climax" in self.gd["effect"]:
						if card.card == "Climax":
							rr = True
					if "Colour" in self.gd["effect"]:
						if any(ccl.lower() in card.mcolour.lower() for ccl in self.gd["effect"][self.gd["effect"].index("Colour") + 1].split("_")):
							rr = True
					if "continue" in self.gd["effect"]:
						self.gd["reveal_ind"] = str(card.ind)
						if "extra" in self.gd["effect"]:
							self.gd["extra"].append(ind)
						rr = True

					if "do" in self.gd["ability_effect"]:
						if not rr and "isnot" in self.gd["effect"]:
							self.gd["do"][1] = list(self.gd["effect"][self.gd["effect"].index("isnot") + 1])
							self.gd["done"] = True
						elif rr:
							self.gd["done"] = True

					if "continue" not in self.gd["effect"]:
						card.show_back()
						self.gd["reveal_ind"] = ""
					Clock.schedule_once(self.reveal_done, move_dt_btw)
		elif self.gd["effect"][0] > 0:
			Clock.schedule_once(self.revealx, move_dt_btw)
			return False

	def reveal_done(self, dt=0):
		if len(self.pd[self.gd["active"]]["Clock"]) >= 7:
			self.gd["level_up_trigger"] = "reveal"
			Clock.schedule_once(partial(self.level_up, self.gd["active"]), move_dt_btw)
			return False

		if "do" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("do")

		if "reveal" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("reveal")

		if "shuff" in self.gd["effect"]:
			ind = self.gd["ability_trigger"].split("_")[1]
			self.gd["shuffle_trigger"] = "ability"
			if self.net["game"]:
				self.gd["shuffle_send"] = True
			self.shuffle_deck(ind[-1])
		else:
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
					self.stack(player)
					temp = self.pd[player]["Library"].pop(0)
				else:
					temp = self.pd[player]["Library"].pop(-1)
					self.mat[player]["mat"].remove_widget(self.cd[temp])
					self.mat[player]["mat"].add_widget(self.cd[temp])

				if "Memory" in self.gd["effect"]:
					if "top-down" in self.gd["effect"]:
						self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Memory"], t="Memory", d=True)
					else:
						self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Memory"], t="Memory")
					self.pd[player]["Memory"].append(temp)
				elif "Stock" in self.gd["effect"]:
					self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Stock"], t="Stock")
					self.pd[player]["Stock"].append(temp)
				else:
					self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Waiting"], t="Waiting")
					self.pd[player]["Waiting"].append(temp)
				self.gd["mill_check"].append(temp)
				self.update_field_label()
				self.gd["mill"] -= 1

			if self.gd["mill"] > 0 and "upto" in self.gd["effect"] and len(self.pd[player]["Library"]) <= 0 and "fix" not in self.gd["effect"]:
				self.gd["mill"] = 0

			if len(self.pd[player]["Library"]) <= 0:
				self.gd["trev"] = player
				self.gd["reshuffle_trigger"] = "mill"
				self.gd["rrev"] = player
				Clock.schedule_once(self.refresh, move_dt_btw)
				return False
			Clock.schedule_once(self.mill, move_dt_btw)
		else:
			self.check_cont_ability()

			self.gd["trev"] = ""

			if "mill" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("mill")

			if self.gd["effect"][1] == -20:
				self.gd["effect"][1] = len(self.gd["extra1"])
				self.gd["mill_check"] = list(self.gd["extra1"])
				if "extra1" not in self.gd["effect"]:
					self.gd["extra1"] = []

			if self.gd["effect"][1] > 0:
				if "if" in self.gd["effect"]:
					self.gd["done"] = False
					if "x#" in self.gd["effect"]:
						txt = 0
						if "pwr" in self.gd["effect"]:
							if "cCColourT" in self.gd["effect"]:
								trt = self.gd["effect"][self.gd["effect"].index("cCColourT") + 1].split("_")
								txt = len([s for s in self.gd["mill_check"] if trt[-1] in self.cd[s].trait_t or any(cl.lower() in self.cd[s].colour for cl in trt[:-1])])
							if "ctrait" in self.gd["effect"]:
								trt = self.gd["effect"][self.gd["effect"].index("ctrait") + 1].split("_")
								txt = len([s for s in self.gd["mill_check"] if any(tr in self.cd[s].trait_t for tr in trt)])
						elif "Climax" in self.gd["effect"]:
							txt = len([s for s in self.gd["mill_check"] if self.cd[s].card == "Climax"])
						if txt > 0:
							self.gd["done"] = True
						self.gd["effect"][self.gd["effect"].index("do") + 1][1] = self.gd["effect"][self.gd["effect"].index("do") + 1][1] * txt
						self.gd["do"][1] = list(self.gd["effect"][self.gd["effect"].index("do") + 1])
					elif "lvl" in self.gd["effect"]:
						lvl = self.gd["effect"][self.gd["effect"].index("lvl") + 1]
						if "==" in self.gd["effect"]:
							if "Character" in self.gd["effect"]:
								nlv = len([s for s in self.gd["mill_check"] if self.cd[s].level_t == lvl and "Character" in self.cd[s].card])
							else:
								nlv = len([s for s in self.gd["mill_check"] if self.cd[s].level_t == lvl])
						elif "lower" in self.gd["effect"]:
							if "Character" in self.gd["effect"]:
								nlv = len([s for s in self.gd["mill_check"] if self.cd[s].level_t <= lvl and "Character" in self.cd[s].card])
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

						if "anyx" in self.gd["effect"] and ntr >= self.gd["effect"][self.gd["effect"].index("Trait") + 2]:
							self.gd["done"] = True
						elif "any" in self.gd["effect"] and ntr >= 1:
							self.gd["done"] = True
						elif "all" in self.gd["effect"] and ntr == self.gd["effect"][1]:
							self.gd["done"] = True
						if "extra1" in self.gd["effect"]:
							if not self.gd["done"]:
								self.gd["extra1"] = []
							else:
								if not self.gd["extra1"]:
									for _ in self.gd["mill_check"]:
										self.gd["extra1"].append(_)
					elif "Character" in self.gd["effect"]:
						cx = self.gd["effect"][self.gd["effect"].index("Character") + 1]
						ncx = len([s for s in self.gd["mill_check"] if "Character" in self.cd[s].card])
						if self.gd["effect"] and ncx >= cx:
							self.gd["done"] = True
						if "extra" in self.gd["effect"]:
							for temp in self.gd["mill_check"]:
								self.gd["extra"].append(temp)
					elif "Event" in self.gd["effect"]:
						cx = self.gd["effect"][self.gd["effect"].index("Event") + 1]
						ncx = len([s for s in self.gd["mill_check"] if "Event" in self.cd[s].card])
						if self.gd["effect"] and ncx >= cx:
							self.gd["done"] = True
					elif "Climax" in self.gd["effect"]:
						cx = self.gd["effect"][self.gd["effect"].index("Climax") + 1]
						ncx = len([s for s in self.gd["mill_check"] if "Climax" in self.cd[s].card])
						if self.gd["effect"] and ncx >= cx:
							self.gd["done"] = True
						if "extra1" in self.gd["effect"] and not self.gd["extra1"]:
							for _ in self.gd["mill_check"]:
								self.gd["extra1"].append(_)
					elif "xdeclare" in self.gd["effect"]:
						if "Level" in self.gd["effect"]:
							if "==x" in self.gd["effect"]:
								if self.cd[self.gd["mill_check"][0]].level_t == int(self.gd["numbers"]):
									self.gd["done"] = True
					elif "extra" in self.gd["effect"]:
						for temp in self.gd["mill_check"]:
							self.gd["extra"].append(temp)
						self.gd["done"] = True
				else:
					self.gd["done"] = True

			if "do" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("do")
			if "confirmpayafter" in self.gd["effect"]:
				self.gd["do"][1] =["pay","may","do",self.gd["do"][1]]
			self.ability_effect()

	def give(self, dt=0):
		idm = self.gd["ability_trigger"].split("_")[1]
		gt = 10
		if "if" in self.gd["effect"]:
			extra = len(self.gd["extra"])

		if "xreplacetext" in self.gd["effect"]:
			if "xlenextra" in self.gd["effect"]:
				if " X " in self.gd["effect"][1]:
					self.gd["effect"][1] = self.gd["effect"][1].replace(" X ", f" {len(self.gd['extra'])} ")
				elif " x " in self.gd["effect"][1]:
					self.gd["effect"][1] = self.gd["effect"][1].replace(" x ", f" {len(self.gd['extra'])} ")
				if self.gd["effect"] != -16 and "extra" not in self.gd["effect"]:
					self.gd["extra"] = []

		if self.gd["effect"][0] == 0:
			if idm[-1] == "1" or (idm[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(idm)
			self.gd["effect"][0] = 1
		elif self.gd["effect"][0] == -3:
			if idm[-1] == "1" or (idm[-1] == "2" and self.gd["com"]):
				for xx in self.gd["effect"][self.gd["effect"].index("target") + 1].split("_"):
					self.gd["target"].append(xx)
			self.gd["effect"][0] = len(self.gd["target"])
		elif self.gd["effect"][0] == -12:
			if idm[-1] == "1" or (idm[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(self.gd["attacking"][0])
			self.gd["effect"][0] = 1
		elif self.gd["effect"][0] == -25:
			if idm[-1] == "1" or (idm[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(self.gd["attacking"][0])
				if self.gd["attacking"][4] == "C":
					self.gd["target"].append(self.pd[self.gd["opp"]]["Center"][self.gd["attacking"][3]])
				elif self.gd["attacking"][4] == "B":
					self.gd["target"].append(self.pd[self.gd["opp"]]["Back"][self.gd["attacking"][3]])
				else:
					self.gd["target"].append("")
			self.gd["effect"][0] = 2
		elif self.gd["effect"][0] == -16:
			self.gd["effect"][0] = len(self.gd["extra"])
			for r in range(len(self.gd["extra"])):
				ex = self.gd["extra"].pop(0)
				if idm[-1] == "1" or (idm[-1] == "2" and self.gd["com"]):
					self.gd["target"].append(ex)
		elif self.gd["effect"][0] == -21:
			self.gd["effect"][0] = 1
			self.gd["target"].append("P")
		elif self.gd["effect"][0] == -1:
			if idm[-1] == "1" or (idm[-1] == "2" and self.gd["com"]):
				if "Battle" in self.gd["effect"] and self.gd["effect"][0] == -1 and self.gd["attacking"][1] == "f":
					self.gd["target"].append(self.gd["attacking"][0])
					if self.gd["attacking"][0][-1] == "1":
						op = "2"
					elif self.gd["attacking"][0][-1] == "2":
						op = "1"
					if "C" in self.gd["attacking"][4]:
						self.gd["target"].append(self.pd[op]["Center"][self.gd["attacking"][3]])
					elif "B" in self.gd["attacking"][4]:
						self.gd["target"].append(self.pd[op]["Back"][self.gd["attacking"][3]])
				else:
					for ta in self.cont_times(self.gd["effect"], self.cont_cards(self.gd["effect"], idm), self.cd):
						self.gd["target"].append(ta)
			self.gd["effect"][0] = len(self.gd["target"])
		if "this" in self.gd["effect"] and self.gd["effect"][0] > 0:
			if idm[-1] == "1" or (idm[-1] == "2" and self.gd["com"]):
				self.gd["target"].append(idm)
			self.gd["effect"][0] += 1

		if len(self.gd["target"]) < self.gd["effect"][0]:
			for r in range(self.gd["effect"][0] - len(self.gd["target"])):
				self.gd["target"].append("")

		for r in range(self.gd["effect"][0]):
			ind = self.gd["target"].pop(0)
			if self.net["game"] and self.gd["ability_trigger"].split("_")[1][-1] == "1":  
				self.net["act"][4].append(ind)
			if ind in self.emptycards:
				continue
			if ind == "P":
				ind = idm[-1]
			gg = 99
			if "give" in self.gd["effect"]:
				gg = self.gd["effect"].index("give")
				self.gd["effect"][gg] = f"{self.gd['effect'][gg]}_{idm}"
				self.anx += 1
				self.gd["effect"].insert(gg + 1, self.anx)
				if "expass" in self.gd["effect"]:
					if not self.gd["extra"]:
						continue
					self.gd["effect"].insert(gg + 2, "pass")
					if len([n for n in self.gd["extra"] if n != ""]) < self.gd["effect"][self.gd["effect"].index("expass") + 1]:
						self.gd["effect"].insert(gg + 3, len([n for n in self.gd["extra"] if n != ""]))
					else:
						self.gd["effect"].insert(gg + 3, self.gd["effect"][self.gd["effect"].index("expass") + 1])

					if "ex_ID=" in self.gd["effect"]:
						self.gd["effect"].insert(gg + 4, "_".join(["ID="] + [n for n in self.gd["extra"] if n != ""]))
					elif "ex_Name=" in self.gd["effect"]:
						self.gd["effect"].insert(gg + 4, "_".join(["Name="] + [self.cd[n].name for n in self.gd["extra"] if n != ""]))
					if "extra" not in self.gd["effect"]:
						self.gd["extra"] = []
					gg += 5
				else:
					gg += 2

			for a in str(self.gd["effect"][1]).split("_"):
				self.gd["effect"][1] = a
				if self.gd["effect"][1:gg] not in self.cd[ind].text_c:
					self.cd[ind].text_c.append(self.gd["effect"][1:gg] + ["turn", self.gd["turn"]])
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
		Clock.schedule_once(self.ability_effect)

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
		if self.gd["rev"] and self.gd["rev_counter"] and "Counter" not in self.gd["phase"]:
			player = self.gd["active"]
		elif self.gd["rev"] or self.gd["rev_counter"]:
			player = self.gd["opp"]
		else:
			player = self.gd["active"]
		self.sd["menu"]["btn"].disabled = True
		if self.gd["draw"] > 0:
			if "drawupto" in self.gd["effect"] and "heal" in self.gd["effect"]:
				if len(self.pd[player]["Clock"]) > 0:
					if "bottom" in self.gd["effect"]:
						temp = self.pd[player]["Clock"].pop(0)
					else:
						temp = self.pd[player]["Clock"].pop()
					self.gd["drawed"].append(temp)
					self.mat[player]["mat"].remove_widget(self.cd[temp])
					self.mat[player]["mat"].add_widget(self.cd[temp])
					self.cd[temp].setPos(field=self.mat[temp[-1]]["field"]["Waiting"], t="Waiting")
					self.pd[player]["Waiting"].append(temp)
					self.clock_size(temp[-1])
			elif len(self.pd[player]["Library"]) > 0:
				temp = self.pd[player]["Library"].pop()
				self.gd["drawed"].append(temp)

				if "Reveal" in self.gd["effect"]:
					self.mat[player]["mat"].remove_widget(self.cd[temp])
					self.mat[player]["mat"].add_widget(self.cd[temp])
					library = self.mat[player]["field"]["Library"]
					self.cd[temp].setPos(library[0] - self.sd["padding"] / 4 - self.sd["card"][0], library[1] - self.sd["card"][1] / 3. * len(self.pd[player]["Res"]), t="Res")
					self.cd[temp].show_front()
					self.pd[player]["Res"].append(temp)
					if not self.gd["Res1_move"]:
						if self.field_btn[f"Res1{player}"].x < 0:
							self.field_btn[f"Res1{player}"].x += Window.width * 2
						self.gd["Res1_move"] = True
				elif "Stock" in self.gd["effect"]:
					self.pd[player]["Stock"].append(temp)
					self.stock_size(player)
				elif "Marker" in self.gd["effect"]:
					face = False
					if "face-up" in self.gd["effect"]:
						face = True
					card = self.gd["ability_trigger"].split("_")[1]
					self.add_marker(card, temp, face)
					self.update_marker(card[-1])
					self.update_field_label()
					self.check_cont_ability()
				else:
					self.pd[player]["Hand"].append(temp)
					self.hand_size(player)

			self.gd["draw"] -= 1
			self.update_field_label()

			if len(self.pd[player]["Library"]) <= 0:
				if "Reveal" in self.gd["effect"]:
					self.gd["draw"] = 0
					self.gd["draw_upto"] = 0
				self.gd["reshuffle_trigger"] = "draw"
				self.gd["rrev"] = player
				Clock.schedule_once(self.refresh, move_dt_btw)
			else:
				Clock.schedule_once(self.draw, move_dt_btw)
		else:
			self.check_cont_ability()

			if self.gd["active"] == "1" and self.gd["phase"] in ("", "Main", "Climax", "Mulligan", "Janken"):
				self.hand_btn_show(False)

			if self.gd["draw_upto"] <= 0:
				if self.net["game"] and not self.net["send"] and "plchoose" in self.gd["effect"]:
					self.net["var"] = list(self.net["act"][4])
					self.net["var1"] = "draw"
					if not self.poptext:
						Clock.schedule_once(partial(self.popup_text, "waitingser"))
					self.mconnect("plturn")
					return False

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

				self.gd["rev"] = False
				if "AUTO" in self.gd["ability_trigger"] or "ACT" in self.gd["ability_trigger"] or "Event" in self.gd["ability_trigger"]:
					Clock.schedule_once(self.ability_effect)
				elif self.gd["phase"] == "Main":
					Clock.schedule_once(self.ability_effect, move_dt_btw)
				elif self.gd["phase"] == "Draw":
					self.pd[self.gd["active"]]["done"]["Draw"] = True
					self.gd["phase"] = "Clock"
					if self.gd["active"] == "1":
						Clock.schedule_once(self.beginning_phase)
					else:
						Clock.schedule_once(self.beginning_phase, phase_dt)
				elif self.gd["phase"] == "Clock":
					self.pd[self.gd["active"]]["done"]["Clock"] = True
					self.gd["phase"] = "Main"
					Clock.schedule_once(self.beginning_phase)
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
							Clock.schedule_once(self.mulligan_start)  
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
			self.check_pos(var)
			self.pd[ind[-1]]["marker"][ind].append([var, face])
		if self.gd["markerstock"]:
			for text in self.cd[ind].text_c:
				if text[0].startswith(cont_ability) and text[1] != 0 and text[1] > -9:
					ef = ab.cont(text[0])
					if ef:
						if "astock" in ef:
							self.gd["astock"][ind[-1]].append((ind, var))
							if "Name" in ef:
								if ef[ef.index("Name") + 1] not in self.gd["astock"]:
									self.gd["astock"][ef[ef.index("Name") + 1]] = {}
								if ind[-1] not in self.gd["astock"][ef[ef.index("Name") + 1]]:
									self.gd["astock"][ef[ef.index("Name") + 1]][ind[-1]] = []
								self.gd["astock"][ef[ef.index("Name") + 1]][ind[-1]].append((ind, var))
							break
						elif "estock" in ef:
							self.gd["estock"][ind[-1]].append((ind, var))
							break
		for text in self.cd[ind].text_c:
			if text[0].startswith(auto_ability) and text[1] != 0 and text[1] > -9:
				ef = ab.marker(text[0])
				if ef and "markers" in ef:
					stack = [ind, ef, text[0], "", (self.cd[ind].pos_old, self.cd[ind].pos_new, "", ""), self.gd["phase"], self.cd[ind].text_c.index(text), self.gd["pp"]]
					if stack not in self.gd["stack"][ind[-1]]:
						self.gd["stack"][ind[-1]].append(stack)

	def update_marker(self, p=""):
		if p == "":
			p = "12"
		for player in p:
			space = self.sd["card"][0] * 0.1
			for ind in self.pd[player]["marker"]:
				card = self.cd[ind]
				if len(self.pd[player]["marker"][ind]) > 3:
					space = space / (len(self.pd[player]["marker"][ind]) / 3)
				for inx in range(len(self.pd[player]["marker"][ind])):
					inm = self.pd[player]["marker"][ind][inx]
					marker = self.cd[inm[0]]

					self.mat[player]["mat"].remove_widget(marker)
					self.mat[player]["mat"].add_widget(marker)
					xpos = self.mat[player]["field"][card.pos_new][0] + space * (len(self.pd[player]["marker"][ind]) - inx)
					ypos = self.mat[player]["field"][card.pos_new][1] - space * (len(self.pd[player]["marker"][ind]) - inx)
					marker.setPos(xpos, ypos, t="Marker")
					if not inm[1]:
						marker.show_back()
					else:
						marker.show_front()
					if marker.status != "Stand":
						marker.stand()
				self.mat[player]["mat"].remove_widget(card)
				self.mat[player]["mat"].add_widget(card)
				card.update_marker(len(self.pd[player]["marker"][ind]))
			for _ in self.pd[player]["Clock"] + self.pd[player]["Center"] + self.pd[player]["Back"]:
				card1 = self.cd[_]
				if _ == "" or _ in self.pd[player]["marker"]:
					continue
				self.mat[player]["mat"].remove_widget(card1)
				self.mat[player]["mat"].add_widget(card1)

	def remove_marker(self, ind="", q=0, s=None, m="", wif=False, stg=False):
		idm = ""
		if self.gd["ability_trigger"] and "_" in self.gd["ability_trigger"]:
			idm = self.gd["ability_trigger"].split("_")[1]

		if ind in self.pd[ind[-1]]["marker"]:
			rev = []
			if q <= 0:
				q = len(self.pd[ind[-1]]["marker"][ind])

			if m != "":
				for inm in self.pd[ind[-1]]["marker"][ind]:
					if m == inm:
						rev.append(inm)
						self.mat[ind[-1]]["mat"].remove_widget(self.cd[inm[0]])
						self.mat[ind[-1]]["mat"].add_widget(self.cd[inm[0]])
			else:
				if wif:
					self.gd["marker_waiting"] = []
				for inx in range(1, q + 1):
					inm = self.pd[ind[-1]]["marker"][ind][-inx]
					rev.append(inm)
					if not stg:
						self.mat[ind[-1]]["mat"].remove_widget(self.cd[inm[0]])
						self.mat[ind[-1]]["mat"].add_widget(self.cd[inm[0]])
						self.cd[inm[0]].setPos(field=self.mat[ind[-1]]["field"]["Waiting"], t="Waiting")
						self.pd[ind[-1]]["Waiting"].append(inm[0])

					if wif:
						self.gd["marker_waiting"].append(inm[0])

			for item in rev:
				self.pd[ind[-1]]["marker"][ind].remove(item)
				if s is None:
					sx = ["as", "es"]
				else:
					sx = [s]

				for m in sx:
					if (ind, item[0]) in self.gd[f"{m}tock"][ind[-1]]:
						self.gd[f"{m}tock"][ind[-1]].remove((ind, item[0]))
						for nm in self.gd[f"{m}tock"]:
							if nm == "1" or nm == "2" or ind[-1] not in self.gd[f"{m}tock"][nm]:
								continue
							if (ind, item[0]) in self.gd[f"{m}tock"][nm][ind[-1]]:
								self.gd[f"{m}tock"][nm][ind[-1]].remove((ind, item[0]))
			self.cd[ind].update_marker(len(self.pd[ind[-1]]["marker"][ind]))
			if len(self.pd[ind[-1]]["marker"][ind]) <= 0:
				del self.pd[ind[-1]]["marker"][ind]
			self.update_marker(ind[-1])

	def choose_opp(self, ind, target=False):
		if ("oppturn" in self.gd["effect"] and "opp" in self.gd["effect"]) and ind[-1] == "1":
			if "Opp" in self.gd["effect"]:
				self.gd["p_owner"] = "2"
			else:
				self.gd["p_owner"] = "1"
		elif ("oppturn" in self.gd["effect"] and "opp" in self.gd["effect"]) and ind[-1] == "2":
			if "Opp" in self.gd["effect"]:
				self.gd["p_owner"] = "1"
			else:
				self.gd["p_owner"] = "2"
		elif ("oppturn" in self.gd["effect"] or "opp" in self.gd["effect"]) and ind[-1] == "1":
			self.gd["p_owner"] = "2"
		elif ("oppturn" in self.gd["effect"] or "opp" in self.gd["effect"]) and ind[-1] == "2":
			self.gd["p_owner"] = "1"
		else:
			self.gd["p_owner"] = ind[-1]

		self.gd["search_type"] = str(self.gd["effect"][2])

		if "marker" in self.gd["ability_effect"]:
			if "Waiting" in self.gd["effect"]:
				self.gd["salvage"] = int(self.gd["effect"][0])
				self.gd["p_c"] = "Salvage"
			elif "Hand" in self.gd["effect"]:
				self.gd["discard"] = self.gd["effect"][0]
				self.gd["p_c"] = "Discard"
		elif "salvage" in self.gd["ability_effect"]:
			self.gd["p_c"] = "Salvage"


		if "msalvage" in self.gd["effect"]:
			self.gd["p_c"] += "_Memory"
		if "Revealed" in self.gd["effect"]:
			self.gd["p_c"] += "_Reveal"
		if "&Hand" in self.gd["effect"]:
			self.gd["p_c"] += "_&Hand"
		if "Reveal" in self.gd["effect"]:
			self.gd["p_c"] += "_Reveal"
		if "stsearch" in self.gd["effect"]:
			self.gd["p_c"] += "_Stock"

		self.gd["p_f"] = True
		self.popup_pl(self.gd["p_c"])
		for cc in self.skip_cpop:
			if cc in self.gd["p_l"]:
				self.gd["p_l"].remove(cc)
		pick = self.ai.ability(self.pd, self.cd, self.gd)

		if any(_ in pick for _ in ("AI_salvage", "AI_discard","AI_search")):
			if "AI_salvage" in pick:
				inx = pick.index("AI_salvage")
			elif "AI_discard" in pick:
				inx = pick.index("AI_discard")
			elif "AI_search" in pick:
				inx = pick.index("AI_search")
			self.gd["chosen"] = list(pick[inx + 1])
			if "choice" in self.gd["effect"]:
				self.opp_choice = pick[inx + 2]
		else:
			self.gd["chosen"] = []

		if target:
			if self.gd["chosen"]:
				for _ in self.gd["chosen"]:
					self.gd["target"].append(_)
			else:
				self.gd["target"].append("")

	def marker(self, *args):
		face = False
		if "face-up" in self.gd["effect"]:
			face = True

		card = self.gd["ability_trigger"].split("_")[1]
		target = ""
		if "target" in self.gd["effect"] and self.gd["effect"][self.gd["effect"].index("target") + 1] == -16 and self.gd["extra"]:
			target = self.gd["extra"][0]
			if "extra" not in self.gd["effect"]:
				self.gd["extra"] = []

		if "Return" in self.gd["effect"]:
			if card in self.pd[card[-1]]["marker"] and len(self.pd[card[-1]]["marker"][card]) >0:
				if self.gd["effect"][0] == -1:
					if "Waiting" in self.gd["effect"] or "Stage" in self.gd["effect"]:
						if "if" in self.gd["effect"]:
							if "Stage" in self.gd["effect"]:
								for _ in [m[0] for m in self.pd[card[-1]]["marker"][card]]:
									self.gd["marker_waiting"].append(_)
							else:
								self.remove_marker(card, self.gd["effect"][0], wif=True)
						else:
							self.remove_marker(card, self.gd["effect"][0])
						self.gd["effect"][0] = 0
				for rr in range(self.gd["effect"][0]):
					inm = self.pd[card[-1]]["marker"][card].pop()

					if "Hand" in self.gd["effect"]:
						self.pd[card[-1]]["Hand"].append(inm[0])
					elif "Stock" in self.gd["effect"]:
						self.pd[card[-1]]["Stock"].append(inm[0])


				if "Stage" not in self.gd["effect"]:
					self.update_marker(card[-1])
					self.check_cont_ability()
			self.gd["effect"].remove("Return")
			if "Hand" in self.gd["effect"]:
				self.hand_size(card[-1])
				self.gd["effect"].remove("Hand")
			elif "Stock" in self.gd["effect"]:
				self.stock_size(card[-1])
				self.gd["effect"].remove("Stock")
			elif "Waiting" in self.gd["effect"]:
				self.gd["effect"].remove("Waiting")
				self.update_field_label()
			elif "Stage" in self.gd["effect"]:
				self.gd["effect"].append("no_cont_check")
				self.gd["effect"].remove("Stage")
			self.marker()
		elif "top" in self.gd["effect"]:
			if "none" in self.gd["effect"] and (card in self.pd[card[-1]]["marker"] and len(self.pd[card[-1]]["marker"][card]) > 0):
				self.gd["effect"].remove("top")
				Clock.schedule_once(self.marker)
				return False
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
			elif "Clock" in self.gd["effect"]:
				if len(self.pd[card[-1]]["Clock"]) > 0:
					temp = self.pd[card[-1]]["Clock"].pop()
					self.cd[temp].stand()
					self.add_marker(card, temp, face)
					self.update_marker()
					self.clock_size(temp[-1])
					self.check_cont_ability()
				self.gd["effect"].remove("top")
				self.gd["effect"].remove("Clock")
				self.marker()
			else:
				for x in range(int(self.gd["effect"][0])):
					if len(self.pd[card[-1]]["Library"]) > 0:
						temp = self.pd[card[-1]]["Library"].pop()
						if "target" in self.gd["effect"]:
							self.gd["effect"].remove("target")
							self.add_marker(target, temp, face)
						else:
							self.add_marker(card, temp, face)
						self.gd["effect"][0] -= 1
						self.update_marker()
						self.update_field_label()
						self.check_cont_ability()
					else:
						self.gd["reshuffle_trigger"] = "marker"
						self.gd["rrev"] = card[-1]
						Clock.schedule_once(self.refresh, move_dt_btw)
						return False
				self.gd["effect"].remove("top")

				if len(self.pd[card[-1]]["Library"]) <= 0:
					self.gd["reshuffle_trigger"] = "marker"
					self.gd["rrev"] = card[-1]
					Clock.schedule_once(self.refresh, move_dt_btw)
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
					if self.net["game"] and self.gd["p_owner"] == "1":  
						self.net["act"][4].append(ind)
					if ind in self.emptycards:
						continue
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
		elif "Stage" in self.gd["effect"]:
			if "ID=" in self.gd["effect"][2] and not self.gd["target"]:
				imd = self.gd["effect"][2].split("_")[1]
				if "Center" in self.cd[imd].pos_new or "Back" in self.cd[imd].pos_new:
					self.gd["target"].append(imd)
				else:
					self.gd["target"].append("")

			if "targetunderthis" in self.gd["effect"]:
				if card not in self.gd["target"]:
					self.gd["target"].append(card)

			if self.gd["effect"][0] == -1 or self.gd["effect"][0] == -2:
				stage = [_ for _ in self.pd[card[-1]]["Center"] + self.pd[card[-1]]["Back"] if _!=""]
				if self.gd["effect"][0] == -2 and card in stage:
					stage.remove(card)

				self.gd["effect"][0] = len(stage)
				if stage:
					for _ in stage:
						if _ not in self.gd["target"]:
							self.gd["target"].append(_)
				else:
					self.gd["target"].append("")
					self.gd["effect"][0] = 1

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
					if self.net["game"] and self.gd["p_owner"] == "1":  
						self.net["act"][4].append(ind)
					if ind in self.emptycards:
						continue
					if "self" in self.gd["effect"]:
						self.add_marker(ind, card, face)
					elif "thisunder" in self.gd["effect"]:
						self.add_marker(ind, card, face)
					elif "targetunderthis" in self.gd["effect"]:
						if target:
							self.add_marker(target, ind, face)
					else:
						self.add_marker(card, ind, face)
				self.update_marker()
				self.check_cont_ability()
				self.gd["effect"].remove("Stage")
				self.marker()
			else:
				self.gd["choose"] = False
				self.gd["chosen"] = []
				self.gd["search_type"] = self.gd["effect"][2]
				if "self" in self.gd["effect"]:
					self.gd["status"] = self.add_to_status(self.gd["status"], [self.gd["search_type"].split("_")[0], "_".join(self.gd["search_type"].split("_")[1:])])
				self.gd["p_c"] = ""
				if card[-1] == "1" and self.gd["effect"][0] > 0 and not self.gd["choose"]:
					self.select_card()
					Clock.schedule_once(partial(self.popup_text, "Main"))
					return False
		elif "Waiting" in self.gd["effect"]:
			if "none" in self.gd["effect"] and (card in self.pd[card[-1]]["marker"] and len(self.pd[card[-1]]["marker"][card]) > 0):
				self.gd["effect"].remove("Waiting")
				Clock.schedule_once(self.marker)
				return False

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
					if self.net["game"] and self.gd["p_owner"] == "1":  
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
				if self.gd["com"] and ((card[-1] == "2" and "oppturn" not in self.gd["effect"]) or (card[-1] == "1" and "oppturn" in self.gd["effect"])):
					self.choose_opp(card,target=True)
					Clock.schedule_once(self.marker)
					return False
				else:
					self.gd["search_type"] = str(self.gd["effect"][2])
					self.gd["salvage"] = int(self.gd["effect"][0])
					self.gd["p_c"] = ""
				Clock.schedule_once(self.salvage)
				return False
		else:
			self.popup_clr()

			if self.gd["rev"]:
				self.gd["rev"] = False

			if self.gd["notarget"]:
				self.gd["notarget"] = False

			if "marker" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("marker")

			if "do" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("do")

			if "if" in self.gd["effect"]:
				if len(self.gd["marker_waiting"]) >= self.gd["effect"][self.gd["effect"].index("if") + 1]:
					if "ifCLevel<=" in self.gd["effect"]:
						if "ifany" in self.gd["effect"] and any(self.cd[mm].level_t <= self.gd["effect"][self.gd["effect"].index("ifCLevel<=") + 1] and self.cd[mm].card == "Character" for mm in self.gd["marker_waiting"]):
							self.gd["done"] = True
					else:
						self.gd["done"] = True
					if "extra" in self.gd["effect"]:
						for _ in self.gd["marker_waiting"]:
							self.gd["extra"].append(_)
				self.gd["marker_waiting"] = []
			elif "do" in self.gd["effect"] and self.gd["do"][0] > 0:
				self.gd["done"] = True

			if "no_cont_check" not in self.gd["effect"]:
				self.check_cont_ability()
			Clock.schedule_once(self.ability_effect)
			return False

	def stock(self, dt=0):
		if self.gd["rev"]:
			player = self.gd["opp"]
		else:
			player = self.gd["active"]

		if self.gd["stock"] > 0:
			if "Reveal" in self.gd["effect"]:
				if len(self.pd[player]["Res"]) > 0:
					temp = self.pd[player]["Res"].pop()
					self.pd[player]["Stock"].append(temp)
					self.stock_size(player)
					self.update_field_label()
				self.gd["stock"] -= 1
			else:
				if len(self.pd[player]["Library"]) > 0:
					temp = self.pd[player]["Library"].pop()
					self.pd[player]["Stock"].append(temp)
					self.stock_size(player)
					self.update_field_label()
					self.gd["stock"] -= 1

				if len(self.pd[player]["Library"]) <= 0:
					self.gd["reshuffle_trigger"] = "stock"
					self.gd["rrev"] = player
					Clock.schedule_once(self.refresh, move_dt_btw)
					return False
			Clock.schedule_once(self.stock, move_dt_btw)
		else:
			if self.gd["rev"]:
				self.gd["rev"] = False
			self.check_cont_ability()
			if "stock" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("stock")

			self.do_check()
			self.ability_effect()

	def change_label(self,s=False):
		self.gd["inx"] = 0
		if self.sd["alabel"] != self.gd["phase"] or s:
			self.sd["alabel"] = str(self.gd["phase"])
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
						self.rect1.pos = (xpos * self.gd["inx"], Window.height / 2 - self.sd["padding"] - self.sd["card"][1] / 6)
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
						self.rect1.pos = (xpos * self.gd["inx"], Window.height / 2 - self.sd["padding"] - self.sd["card"][1] / 6)
					else:
						self.sd["label"][label].color = (.5, .5, .5, 1.)
					self.gd["inx"] += 1

		if self.gd["phase"] != "":
			if "Stand" in self.gd["phase"]:
				self.change_active_background()
			if not self.pd[self.gd["active"]]["phase"][self.gd["phase"]]:
				self.pd[self.gd["active"]]["phase"][self.gd["phase"]] = True
				self.gd["pp"] = -1
				self.gd["stage-1"] = []
			else:
				if not self.gd["load"]:
					if self.gd["pp"] < 0:
						self.gd["pp"] = 0  
					elif self.gd["pp"] == 0:
						self.gd["pp"] = 1
					elif self.gd["pp"] >= 1:
						self.gd["pp"] += 1

	def battle_step(self, *args):
		if self.gd["attacking"][0] and self.gd["attacking"][1] == "f" and self.gd["attack_t"][self.gd["attacking"][1]][self.gd["attacking"][2]] and self.gd["attacking"][4] != "":
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
						if "event" in effect:
							reverse[0] = False
						elif "olevel" in effect:
							if ">p" in effect[effect.index("olevel") + 1] and card_opp.level_t > len(self.pd[card_opp.owner]["Level"]):
								reverse[0] = False
						elif "oplevel" in effect or "opcost" in effect:
							if self.gd["attacking"][0][-1] == "1":
								op = "2"
							else:
								op = "1"
							opp = ""
							if "Center" in card.pos_new:
								opp = self.pd[op]["Center"][self.m[int(card.pos_new[-1])]]

							if opp:
								if "oplevel" in effect:
									if ">p" in effect[effect.index("oplevel") + 1] and self.cd[opp].level_t > len(self.pd[opp[-1]]["Level"]):
										reverse[0] = False
									elif "oplower" in effect and self.cd[opp].level_t <= effect[effect.index("oplevel") + 1]:
										reverse[0] = False
								elif "opcost" in effect:
									if "oplower" in effect and self.cd[opp].cost_t <= effect[effect.index("opcost") + 1]:
										reverse[0] = False
						else:
							reverse[0] = False

				for text in card_opp.text_c:
					effect = ab.cont(text[0])
					if "no_reverse" in effect:
						if "event" in effect:
							reverse[1] = False
						elif "olevel" in effect:
							if ">p" in effect[effect.index("olevel") + 1] and card.level_t > len(self.pd[card.owner]["Level"]):
								reverse[1] = False
						elif "oplevel" in effect or "opcost" in effect:
							if opp_ind[-1] == "1":
								op = "2"
							else:
								op = "1"
							opp = ""
							if "Center" in card_opp.pos_new:
								opp = self.pd[op]["Center"][self.m[int(card_opp.pos_new[-1])]]

							if opp:
								if "oplevel" in effect:
									if ">p" in effect[effect.index("oplevel") + 1] and self.cd[opp].level_t > len(self.pd[opp[-1]]["Level"]):
										reverse[1] = False
									elif "oplower" in effect and self.cd[opp].level_t <= effect[effect.index("oplevel") + 1]:
										reverse[1] = False
								elif "opcost" in effect:
									if "oplower" in effect and self.cd[opp].cost_t <= effect[effect.index("opcost") + 1]:
										reverse[1] = False
						else:
							reverse[1] = False

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

			self.check_auto_ability(rev=revlist, rst=revlist, stacks=False)
			Clock.schedule_once(self.stack_ability, move_dt_btw)
		else:
			self.pd[self.gd["active"]]["done"]["Battle"] = True
			Clock.schedule_once(self.attack_phase_done)

	def check_atk_type(self, inx=""):
		if inx:
			lst = [inx]
			for t in self.gd["attack_t"]:
				i = self.pd[self.gd["active"]]["Center"].index(inx)
				self.gd["attack_t"][t][i] = True
		else:
			lst = self.pd[self.gd["active"]]["Center"]

			for t in self.gd["attack_t"]:
				for i in self.gd["attack_t"][t]:
					self.gd["attack_t"][t][i] = True

		for ind in lst:
			for text in self.cd[ind].text_c:
				if text[0].startswith(cont_ability) and text[1] > -9 and text[1] != 0:
					effect = ab.cont(text[0])
					aa = True
					if any(at in effect for at in self.no_attack):
						if "no_attack" in effect:
							if "Clocks" in effect:
								if "lower" in effect and len(self.pd[ind[-1]]["Clock"]) > effect[effect.index("Clocks") + 1]:
									aa = False
								elif "lower" not in effect and len(self.pd[ind[-1]]["Clock"]) < effect[effect.index("Clocks") + 1]:
									aa = False
							elif "Stocks" in effect:
								if "lower" in effect and len(self.pd[ind[-1]]["Stock"]) > effect[effect.index("Stocks") + 1]:
									aa = False
								elif "lower" not in effect and len(self.pd[ind[-1]]["Stock"]) < effect[effect.index("Stocks") + 1]:
									aa = False
							elif "OMore" in effect:
								if not self.omore(effect, ind):
									aa = False
							elif "oplevel" in effect:
								op = self.pd[self.gd["opp"]]["Center"][self.m[self.pd[ind[-1]["Center"].index(ind)]]]
								if "oplower" not in effect and self.cd[ind].level_t >= self.cd[op].level_t:
									aa = False
								elif "oplower" in effect and self.cd[ind].level_t <= self.cd[op].level_t:
									aa = False
							elif "plevel" in effect:
								if "p==" in effect and self.cd[ind].level_t != len(self.pd[ind[-1]]["Level"]):
									aa = False
								elif "plower" in effect and self.cd[ind].level_t > len(self.pd[ind[-1]]["Level"]):
									aa = False
								elif "plower" not in effect and self.cd[ind].level_t < len(self.pd[ind[-1]]["Level"]):
									aa = False
							elif "Stage" in effect:
								if "Back" in effect:
									stage = len([s for s in self.pd[ind[-1]]["Back"] if s != ""])
								else:
									stage = len([s for s in self.pd[ind[-1]]["Center"] + self.pd[ind[-1]]["Back"] if s != ""])

								if "lower" in effect and stage > effect[effect.index("Stage") + 1]:
									aa = False
								elif "lower" not in effect and stage < effect[effect.index("Stage") + 1]:
									aa = False
							if aa:
								self.gd["attack_t"]["s"][int(self.cd[ind].pos_new[-1])] = False
								self.gd["attack_t"]["f"][int(self.cd[ind].pos_new[-1])] = False
								self.gd["attack_t"]["d"][int(self.cd[ind].pos_new[-1])] = False
						else:
							if "oplevel" in effect or "opgive" in effect:
								if ind[-1] == "1":
									op = "2"
								else:
									op = "1"
								opp = self.pd[op]["Center"][self.m[int(self.cd[ind].pos_new[-1])]]
								if opp != "":
									if "oplevel" in effect:
										if "oplower" not in effect and self.cd[opp].level_t <= self.cd[ind].level_t:
											aa = False
									elif "opgive" in effect:
										if "no_front" in effect:
											self.gd["attack_t"]["f"][self.m[int(self.cd[ind].pos_new[-1])]] = False
										if "no_side" in effect:
											self.gd["attack_t"]["s"][self.m[int(self.cd[ind].pos_new[-1])]] = False
										if "no_direct" in effect:
											self.gd["attack_t"]["d"][self.m[int(self.cd[ind].pos_new[-1])]] = False
								if "opgive" in effect:
									aa = False
							if aa and "no_side" in effect:
								self.gd["attack_t"]["s"][int(self.cd[ind].pos_new[-1])] = False
							if aa and "no_front" in effect:
								self.gd["attack_t"]["f"][int(self.cd[ind].pos_new[-1])] = False
							if aa and "no_direct" in effect:
								self.gd["attack_t"]["d"][int(self.cd[ind].pos_new[-1])] = False

	def attack_phase_done(self, *args):
		if self.gd["pp"] < 9:
			self.gd["pp"] = 9
			self.gd["popup_attack"] -= 1
			self.clear_ability()
			self.gd["phase"] = "Attack"
			self.check_cont_ability()
			self.check_auto_ability(atk=self.gd["attacking"][0])
		else:
			self.gd["attacking"] = ["", "", 0, 0, ""]
			if self.gd["check_atk"]:
				self.gd["attack"] = len([s for s in self.pd[self.gd["active"]]["Center"] if self.cd[s].status == "Stand"])
			else:
				self.gd["attack"] -= 1
			Clock.schedule_once(self.attack_phase_end)

	def attack_phase_end(self, *args):
		if self.gd["turn"] == 1 and self.gd["d_atk"][0] and len(self.gd["d_atk"][1]) >= self.gd["d_atk"][0]:
			self.gd["attack"] = 0
			self.gd["d_atk"] = [1, []]
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
				if not self.gd["opp_attack"]:
					discard = self.ai.attack(self.pd, self.cd, self.gd)
					self.gd["attack"] = len(discard)
					if discard == "pass":
						self.end_current_phase()
					else:
						self.gd["opp_attack"] = list(discard)
				Clock.schedule_once(self.opp_attack, move_dt_btw)
			else:
				Clock.schedule_once(self.attack_phase)
		else:
			self.hand_btn_show(False)
			self.hide_attack_btn()
			self.gd["attack"] = 0
			self.gd["popup_attack"] = 1
			self.pd[self.gd["active"]]["done"]["Attack"] = True
			self.gd["bodyguard"] = False
			if self.gd["nomay"]:
				self.gd["nomay"] = False
			self.gd["phase"] = "Encore"
			self.gd["check_ctr"] = False
			self.gd["popup_encore"] = True
			if "Attack" in self.gd["skip"]:
				self.gd["skip"].remove("Attack")
				Clock.schedule_once(self.beginning_phase)  
			else:
				Clock.schedule_once(self.beginning_phase, phase_dt)

	def damage_step(self, *args):
		card = self.cd[self.gd["attacking"][0]]
		if self.gd["attack_t"][self.gd["attacking"][1]][self.gd["attacking"][2]] and card.soul_t > 0:
			d = True
			for text in card.text_c:
				if text[0].startswith(cont_ability) and text[1] != 0 and text[1] > -9:
					eff = ab.cont(text[0])
					if "no_damage" in eff:
						d = False
						break
			if d and self.gd["attacking"][0] not in self.gd["no_damage"][self.gd["attacking"][0][-1]]:
				self.gd["damage"] = card.soul_t
				if "escanor" in self.gd["attacking"]:
					self.gd["damage"] = self.gd["attacking"][self.gd["attacking"].index("escanor") + 1]
					if "xtimes" in self.gd["attacking"]:
						dd = 0
						if "xsoul" in self.gd["attacking"]:
							dd = int(self.cd[self.gd["attacking"][0]].soul_t)
						if dd > 0:
							self.gd["attacking"][self.gd["attacking"].index("xtimes") + 1] = dd - 1
						else:
							self.gd["damage"] = 0
				self.gd["dmg"] = int(self.gd["damage"])
				self.gd["drev"] = True

		Clock.schedule_once(self.damage, move_dt_btw)

	def rested_card_update(self):
		if len(self.pd[self.gd["active"]]["Res"]) < 1 and not self.event_move:
			c = (0, 1, 2)
			b = (0, 1)
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
		Clock.schedule_once(self.trigger, move_dt_btw)

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
				self.gd["rrev"] = self.gd["active"]
				Clock.schedule_once(self.refresh, move_dt_btw)
			else:
				Clock.schedule_once(self.trigger_effect, move_dt_btw)
		else:
			Clock.schedule_once(self.trigger_done)

	def trigger_effect(self, *args):
		if len(self.gd["trigger_icon"]) > 0:
			trigger = self.gd["trigger_icon"].pop(0)
			if not trigger:
				self.trigger_effect()
			else:
				self.gd["effect"] = ab.trigger(a=trigger)
				ind = self.pd[self.gd['attacking'][0][-1]]['Res'][0]
				self.gd["ability"] = self.gd["effect"][self.gd["effect"].index("text") + 1]
				if self.gd["effect"][0] != -12:
					self.gd["stack"][ind[-1]].append([ind, self.gd["effect"], self.gd["ability"], "Trigger", 1, self.gd["pp"], "TriggerIcon"])
					if self.net["game"] and self.gd['attacking'][0][-1] == "1":
						self.net["act"] = ["a", ind, 0, [], [], 0, -1]
						self.net["send"] = False
					Clock.schedule_once(self.stack_ability)
				else:
					self.gd["ability_trigger"] = f"AUTO_{ind}_{trigger.lower()}_Trigger"
					self.gd["payed"] = True
					self.ability_event()
		else:
			Clock.schedule_once(self.trigger_done, move_dt_btw)

	def trigger_done(self, dt=0):
		if self.gd["trigger"] >= 0:
			if len(self.pd[self.gd["active"]]["Res"]) > 0:
				temp = self.pd[self.gd["active"]]["Res"].pop(0)
				self.pd[self.gd["active"]]["Stock"].append(temp)
				self.update_field_label()
				self.stock_size(self.gd["active"])
				self.gd["trigger_card"] = ""

			if self.gd["trigger"] == 0:
				self.gd["trigger"] = -1
				Clock.schedule_once(self.trigger_done)
			else:
				Clock.schedule_once(self.trigger, move_dt_btw)
		else:
			self.check_auto_ability(rev=self.gd["triggers"])
			return False

	def trigger_step_done(self, *args):

		if self.gd["attacking"][1] == "f":
			self.pd[self.gd["active"]]["done"]["Trigger"] = True
			self.gd["phase"] = "Counter"
			Clock.schedule_once(self.beginning_phase, phase_dt)
		else:
			self.pd[self.gd["active"]]["done"]["Trigger"] = True
			self.pd[self.gd["active"]]["phase"]["Counter"] = True
			self.pd[self.gd["active"]]["done"]["Counter"] = True
			self.gd["phase"] = "Damage"
			Clock.schedule_once(self.beginning_phase, phase_dt)



	def counter_step(self, *args):
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

		if not self.gd["no_backup"][self.gd["opp"]] or not self.gd["no_event"][self.gd["opp"]]:
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
					if card.card == "Character" and not self.gd["no_backup"][self.gd["opp"]] and self.gd["counter_icon"][self.gd["opp"]][0]:
						for text in card.text_c:
							if text[0].startswith(act_ability) and text[1] != 0 and text[1] > -9:
								act = ab.act(a=text[0])
								if act and ab.req(a=text[0], x=len(self.pd[opp]["Stock"])) and "backup" in act and len(self.pd[opp]["Level"]) >= act[act.index("backup") + 1]:
									if s not in self.gd["counter"]:
										self.gd["counter"].append(s)
					elif card.card == "Event" and ("[counter]" in card.text_c[0][0].lower() or (len(card.text_c) > 1 and "[counter]" in card.text_c[1][0].lower())) and not self.gd["no_event"][self.gd["opp"]] and self.gd["counter_icon"][opp][1] and len(self.pd[opp]["Level"]) >= card.level_t and card.mcolour.lower() in self.pd[opp]["colour"] and len(self.pd[opp]["Stock"])+len(self.gd["estock"][opp]) >= card.cost_t:
						if self.check_event(s) and s not in self.gd["counter"]:
							self.gd["counter"].append(s)

			if self.net["game"]:
				self.net["send"] = False

			if len(self.gd["counter"]) > 0:
				self.gd["confirm_trigger"] = "Counter"
				self.gd["confirm_var"] = {"icon": "counter", "c": "counter", "ind": self.gd["counter"][0]}
				Clock.schedule_once(self.confirm_popup, popup_dt)
			else:
				if self.gd["show_counter_popup"]:
					Clock.schedule_once(partial(self.popup_text, self.gd["phase"]), popup_dt)
				else:
					Clock.schedule_once(self.counter_step_done, move_dt_btw)
			return False
		elif self.net["game"] and self.gd["active"] == "1":
			if self.gd["show_wait_popup"]:
				Clock.schedule_once(partial(self.popup_text, "waiting"), popup_dt)
			self.mconnect("counter")
		elif self.gd["com"] and self.gd["active"] == "1":
			counter = self.ai.counter_step(self.pd, self.cd, self.gd, str(self.gd["attacking"][0]), str(self.pd[self.gd["opp"]]["Center"][self.gd["attacking"][3]]))
			if counter == "pass":
				Clock.schedule_once(self.counter_step_done, ability_dt)
			else:
				self.gd["chosen"].append(counter[0])
				self.gd["p_owner"] = self.gd["opp"]
				self.gd["p_c"] = "Counter"
				Clock.schedule_once(self.counter_step_done)

	def counter(self, *args):
		self.gd["uptomay"] = True
		self.gd["payed"] = False
		self.sd["popup"]["popup"].title = "Choose a card"
		self.gd["confirm_var"] = {"o": self.gd["opp"], "c": "Counter", "m": 1}
		self.popup_start()

	def counter_done(self, dt=0):
		if not self.gd["counter_id"]:
			self.sd["popup"]["popup"].dismiss()
			self.sd["text"]["popup"].dismiss()

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
				if counter.card == "Event" and item[0].lower().startswith("[counter]") and item[1] > -9 and item[1] != 0:
					if self.gd["estock_pop"]:
						self.gd["ability_trigger"] = f'Event_{self.gd["counter_id"]}_Counter'
						self.pay_mstock(s="es")
						return False
					else:
						self.play([self.gd["counter_id"], "Res", ""], cnt=True)
						return False
				elif counter.card == "Character" and item[0].lower().startswith("[act] [counter]") and item[1] != 0 and item[1] > -9:
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
						ability = ab.auto(a=text[0], p=self.gd["phase"], r=(counter.ind, counter.ind, counter.card, counter.colour, counter.aselected), act=counter.ind)
						stack = [self.gd["counter_id"], ability, text[0], self.gd["counter_id"], (counter.pos_old, counter.pos_new, "", ""), self.gd["phase"], 0, self.gd["pp"]]
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
		Clock.schedule_once(self.beginning_phase, phase_dt)

	def show_attack_btn(self, dt=0):
		self.sd["btn"]["end"].disabled = False
		self.sd["btn"]["end"].y = 0
		self.sd["menu"]["btn"].disabled = False
		if self.gd["popup_attack"] > 0:
			Clock.schedule_once(partial(self.popup_text, "Attack"))
		if self.gd["com"] and self.gd["active"] == "2":
			pass
		else:
			for n in range(3):
				if self.pd[self.gd["active"]]["Center"][n] != "" and self.cd[self.pd[self.gd["active"]]["Center"][n]].status == "Stand":
					btns = []
					self.check_atk_type(self.pd[self.gd["active"]]["Center"][n])
					if self.pd[self.gd["opp"]]["Center"][self.m[n]] != "":
						if self.gd["attack_t"]["f"][n]:
							self.sd["btn"][f"af{n}"].y = self.cd[self.pd[self.gd["active"]]["Center"][n]].y + self.sd["card"][1] + self.mat[self.gd["active"]]["mat"].y
							btns.append("f")

						if self.gd["attack_t"]["s"][n]:
							self.sd["btn"][f"as{n}"].y = self.cd[self.pd[self.gd["active"]]["Center"][n]].y - self.sd["btn"][f"as{n}"].size[1] + self.mat[self.gd["active"]]["mat"].y
							btns.append("s")
					else:
						if self.gd["attack_t"]["d"][n]:
							self.sd["btn"][f"ad{n}"].y = self.cd[self.pd[self.gd["active"]]["Center"][n]].y + self.sd["card"][1] + self.mat[self.gd["active"]]["mat"].y
							btns.append("d")
						for text in self.cd[self.pd[self.gd["active"]]["Center"][n]].text_c:
							if text[0].startswith(cont_ability) and text[1] != 0 and text[1] > -9:
								self.gd["effect"] = ab.cont(text[0])
								if "backatk" in self.gd["effect"]:
									self.sd["btn"][f"af{n}"].y = self.cd[self.pd[self.gd["active"]]["Center"][n]].y - self.sd["btn"][f"af{n}"].size[1] + self.mat[self.gd["active"]]["mat"].y
									btns.append("f")
									self.sd["btn"][f"as{n}"].y = self.cd[self.pd[self.gd["active"]]["Center"][n]].y - self.sd["btn"][f"as{n}"].size[1] + self.mat[self.gd["active"]]["mat"].y
									btns.append("s")
									break
					for btn in btns:
						self.sd["btn"][f"a{btn}{n}"].x = self.mat["1"]["mat"].x + self.cd[self.pd[self.gd["active"]]["Center"][n]].x

	def hide_attack_btn(self):
		for item in self.sd["btn"]:
			if item.startswith("a"):
				self.sd["btn"][item].y = -Window.height * 2


	def attack_phase_beginning(self, *args):
		self.sd["btn"]["end"].text = "End Attack"
		self.sd["btn"]["end"].disabled = True
		self.sd["btn"]["end"].y = -Window.height
		self.sd["btn"]["end_attack"].y = -Window.height
		self.sd["btn"]["end_phase"].y = -Window.height
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
				self.gd["d_atk"][0] = 1
			self.gd["attack"] = len([s for s in self.pd[self.gd["active"]]["Center"] if self.cd[s].status == "Stand"])
		Clock.schedule_once(self.beginning_phase)

	def attack_phase(self, dt=0):
		self.sd["btn"]["end"].disabled = True
		self.change_label()
		self.clear_ability()
		if "Attack" not in self.gd["skip"]:
			self.gd["attack"] = len([s for s in self.pd[self.gd["active"]]["Center"] if self.cd[s].status == "Stand"])

		if self.gd["attack"] > 0:
			if self.gd["active"] == "1":
				self.sd["btn"]["end"].text = "End Attack"
				self.sd["btn"]["end"].x = Window.width - self.sd["btn"]["end"].size[0]
				self.sd["btn"]["end"].y = 0
			self.sd["btn"]["end"].disabled = False
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
				Clock.schedule_once(self.show_attack_btn, move_dt_btw)
		else:
			if self.net["game"] and self.gd["active"] == "1":
				self.net["var"] = ["x"]
				self.net["var1"] = "no attack"
				self.mconnect("phase")
			else:
				Clock.schedule_once(self.attack_phase_done)  

	def opp_attack(self, dt=0):
		if len(self.gd["opp_attack"]) > 0:
			self.gd["phase"] = "Declaration"
			self.change_label()
			self.gd["pp"] = 0
			temp = self.gd["opp_attack"].pop(0)
			if temp[0] in self.pd[temp[0][-1]]["Center"] + self.pd[temp[0][-1]]["Back"]:
				self.gd["attacking"] = list(temp)
				self.check_bodyguard(self.gd["phase"])
				self.attack_declaration_middle()
			else:
				self.opp_attack()
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
		if card.status == "Stand":
			self.gd["trigger"] = 1
			self.gd["triggers"] = []
			self.rest_card(self.gd["attacking"][0])
			self.mat[self.gd["active"]]["mat"].remove_widget(card)
			self.mat[self.gd["active"]]["mat"].add_widget(card)
			if self.gd["bodyguard"] and self.gd["attacking"][1] != "f" and self.gd["attacking"][3] != 1:
				self.gd["attacking"][3] = 1
				self.gd["attacking"][1] = "f"
				self.gd["attacking"][4] = "C"
			elif self.gd["attacking"][1] == "d":
				card.soul_c.append([1, 1, "Direct", self.gd["turn"]])
				card.update_soul()
			elif self.gd["attacking"][1] == "s":
				aa = True
				for text in card.text_c:
					if text[0].startswith(cont_ability) and text[1] > -9 and text[1] != 0:
						eff = ab.cont(text[0])
						if "no_decrease" in eff:
							aa = False
							break
				if aa:
					card.soul_c.append([-self.cd[self.pd[self.gd["opp"]]["Center"][self.gd["attacking"][3]]].level_t, 1, "Side", self.gd["turn"]])
					card.update_soul()

			if self.gd["d_atk"][0]:
				self.gd["d_atk"][1].append(self.gd["attacking"][0])
			self.check_cont_ability()
			self.check_auto_ability(atk=self.gd["attacking"][0])
		else:
			self.gd["pp"] = 9
			self.attack_phase_done()

	def attack_declaration(self, btn):
		self.sd["btn"]["end"].disabled = True
		self.sd["btn"]["end"].y = -Window.height
		self.hide_attack_btn()
		self.gd["phase"] = "Declaration"
		self.change_label()
		self.gd["pp"] = 0
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

		if len([b for b in self.pd[self.gd["opp"]]["Back"] if b != ""]) >= 1 and btn.cid[0] == "f":
			for text in self.cd[ind].text_c:
				if text[0].startswith(cont_ability) and text[1] != 0 and text[1] > -9:
					self.gd["effect"] = ab.cont(text[0])
					if "backatk" in self.gd["effect"]:
						self.gd["chosen"] = []
						self.gd["choose"] = False
						self.gd["ability_trigger"] = f"BattleBatk_{ind}"
						self.gd["ability_effect"].append("backatk")
						self.gd["status"] = "BBattleBatkOppSelect1"
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
			Clock.schedule_once(self.beginning_phase, phase_dt)
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
		self.sd["btn"]["end"].disabled = True
		self.act_ability_show(hide=True)
		self.sd["btn"]["end"].y = -Window.height
		self.sd["btn"]["end_attack"].y = -Window.height
		self.sd["btn"]["end_phase"].y = -Window.height
		if self.net["game"] and self.gd["active"] == "1":
			self.net["send"] = False
		self.sd["btn"]["end"].text = f"End {self.gd['phase']}"
		if len(self.pd[self.gd["active"]]["Climax"]) > 0:
			self.check_cont_ability()
		Clock.schedule_once(self.beginning_phase)

	def climax_phase(self, dt=0):
		self.gd["nomay"] = False
		if self.net["game"] and self.gd["active"] == "2" and len(self.pd[self.gd["active"]]["Climax"]) <= 0:
			if self.gd["show_wait_popup"]:
				Clock.schedule_once(partial(self.popup_text, "waiting"))
			self.mconnect("phase")
		elif self.net["game"] and self.gd["active"] == "1" and not self.net["send"] and self.gd["play_card"] and not self.gd["climax_play"]:
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

			if self.gd["ability"].startswith(auto_ability):
				self.gd["stack"][card.ind[-1]].append([card.ind, ab.climax(self.gd["ability"]), str(self.gd["ability"]), card.ind, (card.pos_old, card.pos_new, "", ""), self.gd["phase"], 0, self.gd["pp"]])
			self.check_auto_ability(play=card.ind)
		elif not self.gd["play_card"] and len(self.pd[self.gd["active"]]["Climax"]) > 0:
			self.gd["ability_trigger"] = ""
			self.climax_phase_done()
		elif self.gd["com"] and self.gd["active"] == "2":
			climax = self.ai.climax(self.pd, self.cd)
			if climax == "pass":
				self.end_current_phase()
			else:
				self.play_climax(climax)
				Clock.schedule_once(self.climax_phase)
		else:
			self.sd["btn"]["end"].y = 0
			self.update_playable_climax(self.gd["active"])
			if len(self.gd["playable_climax"]) < 1 or self.gd["no_climax"][self.gd["active"]]:
				self.sd["btn"]["end"].y = -Window.height
				if self.net["game"] and self.gd["active"] == "1":
					self.net["var"] = ["x"]
					self.net["var1"] = "no climax"
					self.mconnect("phase")
				else:
					self.climax_phase_done()
			else:
				self.sd["btn"]["end"].disabled = False

	def play_climax(self, ind):
		self.gd["playable_climax"] = []
		self.pd[ind[-1]]["Hand"].remove(ind)
		self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Climax"], t="Climax")
		self.pd[ind[-1]]["Climax"].append(ind)
		self.hand_size(ind[-1])
		self.hand_size(ind[-1])
		self.update_field_label()
		if self.gd["phase"] != "Main":
			self.check_cont_ability()
		self.gd["play_card"] = str(ind)

	def climax_phase_done(self, dt=0):
		self.sd["btn"]["end"].disabled = True
		self.pd[self.gd["active"]]["done"]["Climax"] = True
		self.gd["phase"] = "Attack"
		if "Climax" in self.gd["skip"]:
			self.gd["nomay"] = True
			self.gd["skip"].remove("Climax")
			Clock.schedule_once(self.attack_phase_beginning)
		else:
			Clock.schedule_once(self.attack_phase_beginning, phase_dt)

	def level_up(self, player, *args):
		if self.gd["gg"]:
			return
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
			self.popup_start()

	def level_up_done(self, *args):
		self.sd["popup"]["popup"].dismiss()
		if self.net["game"] and self.net["lvlsend"] and self.gd["chosen"][0][-1] == "1":  
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
				self.send_to("Level", card, pos="lvlup")

			if len(self.pd[card[-1]]["Clock"]) > 0:
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

			if "unli" in self.gd["per_poped"] and self.gd["per_poped"][-1] and "xlvlup" in self.gd["per_poped"]:
				self.gd["per_poped"][-1] = 0

			if self.gd["level_up_trigger"] == "rule":
				self.gd["level_up_trigger"] = str(self.gd["level_up_trigger_temp"])
				self.gd["level_up_trigger_temp"] = ""

			if self.gd["reflev"]:
				Clock.schedule_once(partial(self.reflev, self.gd["reflev"][0]))
			elif "damage" in self.gd["level_up_trigger"]:
				Clock.schedule_once(self.damage, move_dt_btw)
			elif "draw" in self.gd["level_up_trigger"]:
				Clock.schedule_once(self.draw, move_dt_btw)
			elif "refresh" in self.gd["level_up_trigger"]:
				Clock.schedule_once(self.refresh, move_dt_btw)
			elif "draw" in self.gd["level_up_trigger"]:
				Clock.schedule_once(self.draw, move_dt_btw)
			elif "clocker" in self.gd["level_up_trigger"]:
				Clock.schedule_once(self.clocker, move_dt_btw)
			elif "clock" in self.gd["level_up_trigger"]:
				Clock.schedule_once(self.clock_phase_done, move_dt_btw)
			elif "encore" in self.gd["level_up_trigger"]:
				Clock.schedule_once(self.encore_done, move_dt_btw)
			elif "reveal" in self.gd["level_up_trigger"]:
				Clock.schedule_once(self.reveal_done, move_dt_btw)
			elif "ability" in self.gd["level_up_trigger"]:
				Clock.schedule_once(self.ability_effect, move_dt_btw)
			elif "stack" in self.gd["leve_up_trigger"]:
				Clock.schedule_once(self.stack_ability, move_dt_btw)
			elif "pay_choose" in self.gd["level_up_trigger"]:
				Clock.schedule_once(self.pay_condition_done, move_dt_btw)
			elif "pay" in self.gd["level_up_trigger"]:
				Clock.schedule_once(self.pay_condition_done, move_dt_btw)
			self.gd["level_up_trigger"] = ""

	def clock_phase(self, *args):
		self.gd["level_up_trigger"] = ""
		if self.net["game"]:
			self.net["send"] = False

		if self.net["game"] and self.gd["active"] == "2":
			if self.gd["show_wait_popup"]:
				Clock.schedule_once(partial(self.popup_text, "waiting"))
			self.mconnect("phase")
		elif self.gd["com"] and self.gd["active"] == "2":
			discard = self.ai.clock(self.pd, self.cd, self.gd)
			if discard == "pass" or self.gd["no_clock"][self.gd["active"]]:
				self.end_current_phase()
			else:
				self.gd["p_owner"] = self.gd["active"]
				self.gd["chosen"] = []
				self.gd["chosen"].append(discard)
				self.clock_phase_done()
		else:
			if self.gd["no_clock"][self.gd["active"]]:
				Clock.schedule_once(self.clock_phase_done, phase_dt)
			else:
				self.sd["popup"]["popup"].title = self.gd["phase"]
				self.gd["uptomay"] = True
				self.gd["confirm_var"] = {"o": self.gd["active"], "c": "Clock", "m": 1}
				self.popup_start()

	def clock_phase_done(self, bt=None):
		self.sd["popup"]["popup"].dismiss()
		if self.gd["chosen"] and self.gd["level_up_trigger"] == "":
			self.gd["target"] = list(self.gd["chosen"])
		if self.gd["clock_temp"]:
			self.gd["target"] = self.gd["clock_temp"]
			self.gd["clock_temp"] = None
		if self.net["game"] and not self.net["send"] and self.gd["active"] == "1" and "Clock" in self.gd["phase"]:
			self.net["var"] = list(self.gd["chosen"])
			self.net["var1"] = "Clock"
			if not self.poptext:
				Clock.schedule_once(partial(self.popup_text, "waitingser"))
			self.mconnect("phase")
		elif self.gd["target"] and not self.gd["clock_done"]:
			if self.gd["level_up_trigger"] == "":
				ind = self.gd["target"].pop(0)
				self.send_to("Clock", ind)

				if self.gd["both"]:
					self.gd["both"] = False

				self.gd["clock_done"] = True
				if len(self.pd[self.gd["active"]]["Clock"]) >= 7:
					self.gd["clock_temp"] = self.gd["target"]
					self.popup_clr()
					self.gd["level_up_trigger"] = "clock"
					Clock.schedule_once(partial(self.level_up, self.gd["active"]), move_dt_btw)
				else:
					Clock.schedule_once(self.clock_phase_done)
		elif self.gd["clock_done"] and self.gd["level_up_trigger"] == "" and "Clock" in self.gd["phase"]:
			self.gd["clock_done"] = False
			self.gd["draw"] = 2
			self.popup_clr()
			Clock.schedule_once(self.draw, move_dt_btw)
		else:
			self.popup_clr()

			if not self.gd["payed"] and ("AUTO" in self.gd["ability_trigger"] or "ACT" in self.gd["ability_trigger"]):
				self.pay_condition_done()
			elif "Clock" in self.gd["phase"]:
				self.clock_phase_end()

	def clock_phase_end(self, dt=0):
		self.pd[self.gd["p_owner"]]["done"]["Clock"] = True
		self.gd["phase"] = "Main"
		self.gd["clock_done"] = False
		Clock.schedule_once(self.beginning_phase)

	def check_lose(self, player=""):
		if player == "":
			if self.gd["trev"]:
				player = self.gd["trev"]
			else:
				if self.gd["rrev"]:
					player = self.gd["rrev"]
				elif self.gd["drev"]:
					player = self.gd["opp"]
				elif self.gd["rev"]:
					player = self.gd["opp"]
				else:
					player = self.gd["active"]

		if self.gd["both"]:
			w = {"1": False, "2": False}
			for p in w:
				if len(self.pd[p]["Clock"]) >= 7 and len(self.pd[p]["Level"]) >= 3:
					w[p] = True
				if len(self.pd[p]["Level"]) >= 4:
					w[p] = True
				if len(self.pd[p]["Library"]) <= 0 and len(self.pd[p]["Waiting"]) <= 0 and len(self.pd[p]["Res"]) <= 0:
					w[p] = True
		elif (len(self.pd[player]["Clock"]) >= 7 and len(self.pd[player]["Level"]) >= 3) or len(self.pd[player]["Level"]) >= 4 or (len(self.pd[player]["Library"]) <= 0 and len(self.pd[player]["Waiting"]) <= 0):  
			if player == "1":
				self.gd["wl"] = False
			else:
				self.gd["wl"] = True
			self.gd["gg"] = True
			Clock.schedule_once(self.winlose, move_dt_btw)
			return True

	def show_continue_btn(self, btn=None):
		if self.gd["popup_done"][1]:
			self.gd["popup_pop"] = False
		self.sd["popup"]["stack"].clear_widgets()
		self.sd["btn"]["filter_add"].y = -Window.height * 2

	def show_popup(self, btn):
		if self.infot:
			self.infot.cancel()
			self.infot = None
		self.shelve_save()
		if not self.gd["popup_done"][0] and not self.gd["popup_done"][1]:
			self.sd["menu"]["btn"].disabled = True
			self.gd["popup_done"] = (True, False)
			self.sd["btn"]["continue"].y = -Window.height
			self.hand_btn_show(False)
			self.act_ability_show(hide=True)

			if btn.cid == "cont":
				self.gd["cont_on"] = False
				if self.gd["choose_trait"]:
					self.gd["p_c"] = ""
					self.choose_trait()
				elif self.gd["stack_pop"]:
					self.stack_popup()
				elif self.gd["confirm_pop"]:
					self.gd["confirm_var"] = dict(self.gd["confirm_temp"])
					self.confirm_popup()
				elif self.gd["popup_pop"]:
					self.gd["confirm_var"] = dict(self.gd["confirm_temp"])
					self.popup_start()

				elif self.gd["act_poped"]:
					self.act_popup(self.gd["act_poped"])
				elif self.gd["per_poped"][0]:
					self.perform_popup(self.gd["per_poped"])
		elif self.gd["popup_on"] and self.net["game"] and self.sd["text"]["c"] == "waiting" and self.gd["active"] == "2" and all(self.gd["phase"] != phase for phase in ("Janken", "Mulligan", "")):
			self.sd["btn"]["continue"].y = -Window.height
			self.hand_btn_show(False)
			self.sd["cpop_press"] = []
			if "Counter" not in self.gd["p_c"]:  
				self.sd["text"]["popup"].open()

	def show_menu(self, btn=None):
		self.gd["menu"] = True
		if self.net["game"]:
			self.sd["menu"]["restart"].disabled = True
			self.sd["menu"]["change"].disabled = True
		else:
			self.sd["menu"]["restart"].disabled = False
			self.sd["menu"]["change"].disabled = False
		self.sd["menu"]["main"].disabled = False

		self.shelve_save()
		self.sd["menu"]["popup"].open()

	def menu_dismiss(self, btn=None):
		self.gd["menu"] = False
		self.sd["menu"]["popup"].dismiss()
		if self.gd["gg"]:
			self.move_field_btn(self.gd["phase"])

	def show_field(self, btn=None):
		self.sd["popup"]["popup"].dismiss()
		if self.gd["ability_doing"] == "looktop" and ("hand" in self.gd["p_c"] or "clock" in self.gd["p_c"]):
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
			self.gd["cont_on"] = True
			self.sd["btn"]["continue"].disabled = False
			self.sd["cpop_press"] = []
			self.hand_btn_show()
			self.act_ability_show(hide=True)
		self.sd["menu"]["btn"].disabled = False

	def refresh(self, dt=0):
		player = self.gd["rrev"]

		if not self.gd["reshuffle"]:
			self.check_cont_ability()
			self.gd["reshuffle"] = True
			self.gd["refresh_point"] = True
			if len(self.pd[player]["Waiting"]) <= 0 and ((len(self.pd[player]["Res"]) > 0 and not self.gd["cancel_dmg"]) or len(self.pd[player]["Res"]) <= 0):
				if player == "1":
					self.gd["wl"] = False
				else:
					self.gd["wl"] = True
				self.gd["gg"] = True
				Clock.schedule_once(self.winlose, popup_dt)
				return
			else:

				self.gd["no_cont_check"] = True
				for n in list(self.pd[player]["Waiting"]):
					self.send_to("Library", n, wig=False, update_field=False)

				self.check_cont_ability()
				self.update_field_label()
				self.gd["shuffle_trigger"] = "refresh"
				if self.net["game"]:
					self.gd["shuffle_send"] = True
				self.shuffle_deck(player)
		else:
			if self.gd["refresh_point"]:
				self.gd["refresh_point"] = False
				temp = self.pd[player]["Library"][-1]
				self.send_to("Clock", temp)

			if self.gd["reshuffle_trigger"] == "rule":
				self.gd["reshuffle_trigger"] = str(self.gd["reshuffle_trigger_temp"])
				self.gd["reshuffle_trigger_temp"] = ""

			if self.gd["reflev"]:
				Clock.schedule_once(partial(self.reflev, self.gd["reflev"][0]))

			if len(self.pd[player]["Clock"]) >= 7:
				self.gd["level_up_trigger"] = "refresh"
				Clock.schedule_once(partial(self.level_up, player), move_dt_btw)
				return False

			self.gd["reshuffle"] = False

			if self.gd["reshuffle_trigger"] == "damage":
				Clock.schedule_once(self.damage, move_dt_btw)
			elif self.gd["reshuffle_trigger"] == "draw":
				Clock.schedule_once(self.draw, move_dt_btw)
			elif self.gd["reshuffle_trigger"] == "trigger":
				Clock.schedule_once(self.trigger, move_dt_btw)
			elif self.gd["reshuffle_trigger"] == "looktop":
				Clock.schedule_once(self.look_top_done, move_dt_btw)
			elif self.gd["reshuffle_trigger"] == "stock":
				Clock.schedule_once(self.stock, move_dt_btw)
			elif self.gd["reshuffle_trigger"] == "revealx":
				Clock.schedule_once(self.revealx, move_dt_btw)
			elif self.gd["reshuffle_trigger"] == "reveal":
				Clock.schedule_once(self.reveal, move_dt_btw)
			elif self.gd["reshuffle_trigger"] == "mill":
				Clock.schedule_once(self.mill, move_dt_btw)
			elif self.gd["reshuffle_trigger"] == "marker":
				Clock.schedule_once(self.marker, move_dt_btw)
			elif self.gd["reshuffle_trigger"] == "ability":
				Clock.schedule_once(self.ability_effect, move_dt_btw)
			elif self.gd["reshuffle_trigger"] == "stack":
				Clock.schedule_once(self.stack_ability, move_dt_btw)
			elif self.gd["reshuffle_trigger"] == "brainstorm":
				Clock.schedule_once(self.brainstorm, move_dt_btw)
			self.gd["reshuffle_trigger"] = ""

	def send_to_waiting(self, ind):
		if not self.gd["no_cont_check"]:
			self.check_cont_ability()
		if "Waiting" not in self.cd[ind].pos_new:
			if ind in self.power_zero:
				self.power_zero.remove(ind)
			if ind in self.gd["encore"][ind[-1]]:
				self.gd["encore"][ind[-1]].remove(ind)
			if any(ss in self.cd[ind].pos_new for ss in self.stage):
				self.check_auto_ability(rev=[ind], wait=ind, stacks=False)
			self.check_pos(ind)

			if ind in self.gd["stage-1"]:
				self.gd["stage-1"].remove(ind)

			self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Waiting"], t="Waiting")
			self.pd[ind[-1]]["Waiting"].append(ind)

			self.update_field_label()

			if ind in self.gd["attacking"][0]:  
				self.gd["attacking"][0] = ""

			if self.gd["no_cont_check"]:
				self.gd["no_cont_check"] = False
			else:
				if self.gd["play"]:
					self.check_cont_ability(act=False)
				else:
					self.check_cont_ability()

	def encore_card(self, ind):
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
		self.gd["encore_ind"] = ""
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
				for p in self.gd["encore"]:
					self.skip_encore(p)
				self.pd[self.gd["active"]]["done"]["Encore"] = True
				self.gd["phase"] = "End"
				Clock.schedule_once(self.end_phase_beginning, move_dt_btw)

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

	def reflev(self, btn, dt=0):
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
		elif "lev" in rule:
			self.gd["reflev"].remove(rule)
			if self.gd["level_up_trigger"]:
				self.gd["level_up_trigger_temp"] = str(self.gd["level_up_trigger"])
			self.gd["level_up_trigger"] = "damage"
			self.check_cont_ability()
			Clock.schedule_once(partial(self.level_up, rule[-1]), move_dt_btw)
			return False

	def encore_pay(self):
		if "Character" in self.gd["target"]:
			self.gd["search_type"] = "Character"
			Clock.schedule_once(self.encore_popup)
		elif "TraitN" in self.gd["target"]:
			self.gd["search_type"] = self.gd["effect"][self.gd["effect"].index("TraitN") + 1]
			Clock.schedule_once(self.encore_popup)
		elif "Trait" in self.gd["target"]:
			self.gd["search_type"] = self.gd["effect"][self.gd["effect"].index("Trait") + 1]
			Clock.schedule_once(self.encore_popup)
		elif "Climax" in self.gd["target"]:
			self.gd["search_type"] = "Climax"
			Clock.schedule_once(self.encore_popup)
		elif "Clock" in self.gd["target"]:
			self.gd["reshuffle_trigger"] = "encore"
			self.gd["damage_refresh"] = 1
			self.gd["damageref"] = True
			Clock.schedule_once(self.damage, move_dt_btw)
		elif "SWaiting" in self.gd["target"]:
			wtar = self.gd["encore_effect"][self.gd["encore_effect"].index("StockWaiting") + 1].split("_")
			self.pay_stock(self.gd["encore_effect"][0], self.gd["encore_ind"][-1])
			self.gd["payed"] = True
			self.gd["chosen"] = []
			self.gd["choose"] = False
			self.gd["status"] = self.add_to_status(f'Select{wtar[0]}', wtar[1:])
			self.select_card()
			Clock.schedule_once(partial(self.popup_text, "Main"))
		elif any("Stock" in encore for encore in self.gd["target"]):
			for encore in self.gd["target"]:
				if "Stock" in encore:
					self.pay_stock(int(self.gd["target"][self.gd["target"].index(encore)][-1]), self.gd["encore_ind"][-1])
					self.gd["payed"] = True
					break
			Clock.schedule_once(self.encore_done)
		else:
			self.encore_done()

	def encore_done(self, bt=None):
		self.sd["popup"]["popup"].dismiss()

		if self.gd["chosen"]:
			for ind in self.gd["chosen"]:
				self.gd["target"].append(ind)

		if any("Stock" in trg for trg in self.gd["target"]) or "Clock" in self.gd["target"]:
			if "Waiting" in self.cd[self.gd["encore_ind"]].pos_new:
				self.encore_card(self.gd["encore_ind"])
		elif len(self.gd["target"]) > 1 and any(tr in self.gd["target"] for tr in ("Character", "Trait", "TraitN", "Climax")):
			temp = self.gd["target"].pop(-1)
			self.hand_waiting(chosen=[temp])
			self.encore_card(self.gd["encore_ind"])
			if self.net["game"] and ((self.gd["active"] == "1" and not self.gd["rev"]) or (self.gd["active"] == "2" and self.gd["rev"])):
				self.net["act"][4].append(temp)
		elif len(self.gd["target"]) > 1 and "SWaiting" in self.gd["target"]:
			self.gd["encore_effect"] = []
			temp = self.gd["target"].pop(-1)
			self.gd["no_cont_check"] = True
			self.send_to_waiting(temp)
			self.encore_card(self.gd["encore_ind"])
			if self.net["game"] and ((self.gd["active"] == "1" and not self.gd["rev"]) or (self.gd["active"] == "2" and self.gd["rev"])):
				self.net["act"][4].append(temp)

		self.popup_clr()
		self.check_cont_ability()

		if "encore" in self.gd["ability_effect"]:
			self.gd["ability_effect"].remove("encore")

		self.gd["encore_ind"] = ""
		self.gd["p_c"] = ""
		Clock.schedule_once(self.ability_effect, move_dt_btw)

	def encore_popup(self, dt=0):
		self.popup_clr()
		self.sd["popup"]["popup"].title = f"Encore {self.cd[self.gd['encore_ind']].name_t}"
		self.gd["uptomay"] = True
		self.gd["confirm_var"] = {"o": self.gd["encore_ind"][-1], "c": "Encore", "m": 1}
		self.popup_start()

	def check_reversed(self):
		self.gd["encore"]["1"] = [s for s in self.pd["1"]["Center"] + self.pd["1"]["Back"] if s != "" and self.cd[s].status == "Reverse"]
		self.gd["encore"]["2"] = [s for s in self.pd["2"]["Center"] + self.pd["2"]["Back"] if s != "" and self.cd[s].status == "Reverse"]

	def encore_phase(self, *args):
		self.gd["encore_ind"] = ""
		self.check_reversed()
		if len(self.gd["encore"]["1"]) + len(self.gd["encore"]["2"]) <= 0:
			self.pd[self.gd["active"]]["phase"]["Encore"] = True
			self.pd[self.gd["active"]]["done"]["Encore"] = True
			self.gd["phase"] = "End"

			Clock.schedule_once(self.end_phase_beginning, move_dt_btw)
			return False

		if self.gd["com"] and len(self.gd["encore"]["2"]) > 0:
			encore = self.ai.encore(self.pd, self.cd, self.gd)
			self.gd["opp_encore"] = encore
		self.hand_btn_show()
		Clock.schedule_once(self.encore_start)

	def end_phase_beginning(self, dt=0):
		self.sd["menu"]["btn"].disabled = True
		self.sd["btn"]["end"].y = -Window.height
		self.sd["btn"]["end_attack"].y = -Window.height
		self.sd["btn"]["end_phase"].y = -Window.height
		self.sd["btn"]["ablt_info"].y = -Window.height
		self.sd["btn"]["draw_upto"].y = -Window.height
		self.gd["nomay"] = False
		self.gd["skip"] = []
		self.gd["climax_play"] = False
		Clock.schedule_once(self.beginning_phase)

	def end_phase(self, *args):
		self.hand_btn_show(False)
		if len(self.pd[self.gd["active"]]["Climax"]) > 0:
			ind = self.pd[self.gd["active"]]["Climax"].pop()
			self.mat[ind[-1]]["mat"].remove_widget(self.cd[ind])
			self.mat[ind[-1]]["mat"].add_widget(self.cd[ind])
			self.cd[ind].setPos(field=self.mat[ind[-1]]["field"]["Waiting"], t="Waiting")
			self.pd[ind[-1]]["Waiting"].append(ind)
			self.update_field_label()
		self.check_cont_ability()
		self.hand_limit_start()

	def reset_auto(self):
		for player in list(self.pd.keys()):
			for ind in self.pd[player]["Center"] + self.pd[player]["Back"] + self.pd[player]["Memory"] + self.pd[player]["Clock"]:
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

	def reduce_c_counter(self):
		for player in list(self.pd.keys()):
			for ind in self.pd[player]["Center"] + self.pd[player]["Back"] + [player]:
				if ind != "" and "space" not in ind:
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
				self.net["var"] = str(wl[0])
				self.net["var1"] = "winlose"
				self.mconnect("winlose")

		self.sd["menu"]["popup"].title = "End of Game"
		self.sd["menu"]["popup"].size = (self.sd["card"][0] * 5, self.sd["card"][1] * 6.5)
		self.sd["menu"]["wl_box"].remove_widget(self.sd["menu"]["wl_box1"])
		try:
			self.sd["menu"]["wl_box"].add_widget(self.sd["menu"]["wl"])
		except WidgetException:
			pass
		self.sd["menu"]["wl_box"].add_widget(self.sd["menu"]["wl_box1"])
		self.sd["btn"]["end"].disabled = True
		self.sd["btn"]["end_attack"].disabled = True
		self.sd["btn"]["end_phase"].disabled = True
		self.sd["btn"]["continue"].disabled = True
		self.sd["menu"]["btn"].disabled = False

		self.gd["game_start"] = False


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

			if "Library" in self.gd["effect"] and "top" in self.gd["effect"]:
				self.gd["chosen"].reverse()

			if "invert" in self.gd["effect"]:
				cind = ""
				for card in self.gd["chosen"]:
					if card != "":
						cind = str(card)
						break
				if cind and "mdiscard" in self.gd["effect"]:
					for card in self.pd[cind[-1]]["Memory"]:
						self.gd["target"].append(card)

			for ix in self.gd["chosen"]:
				if "invert" in self.gd["effect"]:
					if ix in self.gd["target"]:
						self.gd["target"].remove(ix)
						self.gd["discard"] = len(self.gd["target"])
				else:
					self.gd["target"].append(ix)

			if "Stage" in self.gd["effect"]:
				if "Change" in self.gd["effect"]:
					self.gd["move"] = self.cd[imd].pos_new
					if self.gd["move"] == "Waiting":
						self.gd["move"] = self.cd[imd].pos_old
					Clock.schedule_once(self.discard)
				elif len([c for c in self.gd["chosen"] if c != ""]) > 0:
					self.effect_to_stage()
				else:
					self.gd["target"].append("")
					Clock.schedule_once(self.discard)
			elif "swap" in self.gd["effect"]:
				swap = self.gd["effect"][self.gd["effect"].index("swap") + 1]
				if "CX" in swap:
					swap = "Climax"
				if len(self.gd["target_temp"]) > 0:
					for rr in self.gd["target_temp"]:
						self.gd["target"].append(rr)
					self.gd["target_temp"] = []
				elif len([s for s in self.gd["target"] if s != ""]) > 0 and len(self.pd[imd[-1]][self.gd["effect"][self.gd["effect"].index(swap)]]) > 0:
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
				elif self.gd["chosen"] == [""]:
					self.gd["done"] = False
					self.gd["target"].append("")
				Clock.schedule_once(self.discard)
			elif "marker" in self.gd["effect"]:
				Clock.schedule_once(self.marker)
			else:
				Clock.schedule_once(self.discard)
		elif self.gd["p_c"] == "" and not self.gd["target"]:
			self.gd["chosen"] = []

			if self.gd["uptomay"]:
				uptomay = "up to "
			else:
				uptomay = ""

			if self.gd["discard"] > 1:
				word = " cards"
			else:
				word = " card"

			if "opp" in self.gd["effect"] and imd[-1] == "1":
				player = "2"
			elif "opp" in self.gd["effect"] and imd[-1] == "2":
				player = "1"
			elif self.gd["perform_both"] and imd[-1] == "2":
				player = "1"
			else:
				player = imd[-1]

			disc = self.popup_title_search(imd, uptomay, word)

			if "marker" in self.gd["effect"] and isinstance(self.gd["effect"][0], str) and "discard" in self.gd["effect"][0]:
				c = "Marker_Discard"
			elif "Stage" in self.gd["effect"] and isinstance(self.gd["effect"][0], str) and "discard" in self.gd["effect"][0]:
				c = "Discard_stage"
			else:
				c = "Discard"

			if "cdiscard" in self.gd["effect"]:
				c += "_Clock"
			elif "ldiscard" in self.gd["effect"]:
				c += "_Level"
			elif "mdiscard" in self.gd["effect"]:
				c += "_Memory"
			elif "cxdiscard" in self.gd["effect"]:
				c += "_Climax"

			if self.gd["resonance"][0] and len(self.gd["resonance"][1]) < self.gd["resonance"][2]:
				c += "_Reveal"
				self.sd["popup"]["popup"].title = f"Reveal {uptomay}{self.gd['discard']} {disc}"
			elif "_" in c or "Clock" in self.gd["effect"]:
				if "swap" in self.gd["effect"] and "Stage" not in self.gd["effect"]:
					if "ldiscard" in self.gd["effect"]:
						self.sd["popup"]["popup"].title = f"Choose {self.gd['discard']} {disc} in your level"
					elif "cdiscard" in self.gd["effect"]:
						self.sd["popup"]["popup"].title = f"Choose {self.gd['discard']} {disc} in your clock"
					elif "mdiscard" in self.gd["effect"]:
						self.sd["popup"]["popup"].title = f"Choose {self.gd['discard']} {disc} in your memory"
					elif "cxdiscard" in self.gd["effect"]:
						self.sd["popup"]["popup"].title = f"Choose {self.gd['discard']} {disc} in your climax"
					else:
						self.sd["popup"]["popup"].title = f"Choose {self.gd['discard']} {disc} in your hand"
				else:
					self.sd["popup"]["popup"].title = f"Choose {uptomay}{self.gd['discard']} {disc}"
			else:
				if "Name=" in self.gd["effect"] or "Name=" in self.gd["pay"]:
					self.sd["popup"]["popup"].title = f"Choose {self.gd['discard']} {disc}"
				elif "hmemory" in self.gd["effect"]:
					self.sd["popup"]["popup"].title = f"Put {self.gd['discard']} {disc} into your memory"
				else:
					self.sd["popup"]["popup"].title = f"Choose {self.gd['discard']} {disc}"
			self.gd["confirm_var"] = {"o": player, "c": c, "m": self.gd["discard"]}
			self.popup_start()
		else:
			if "discard" in self.gd["ability_effect"]:
				self.gd["ability_effect"].remove("discard")

			if "Stage" in self.gd["effect"] and self.gd["move"] and (imd[-1] == "1" or (imd[-1] == "2" and "oppturn" in self.gd["effect"]) or (imd[-1] == "2" and self.gd["com"] and "oppturn" not in self.gd["effect"])):
				if self.gd["uptomay"] and (not self.gd["move"] or self.gd["move"] == "none"):
					self.gd["target"].append("")
				else:
					self.gd["target"].append(self.gd["move"])
				self.gd["move"] = ""

			idm = []
			discard = []
			st = ""
			lif = []
			for r in range(self.gd["discard"]):
				ind = self.gd["target"].pop(0)
				if "Stage" in self.gd["effect"]:
					st = self.gd["target"].pop(0)
				if self.net["game"] and self.gd["p_owner"] == "1":  
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
				if "ifcount" in self.gd["effect"]:
					self.gd["ifcount"] += 1
				if self.gd["resonance"][0] and len(self.gd["resonance"][1]) < self.gd["resonance"][2]:
					self.gd["resonance"][1].append(ind)
				elif "Stage" in self.gd["effect"]:
					if "if" in self.gd["effect"]:
						lif.append(ind)
					if st:
						self.gd["standby"] = [imd, self.cd[imd].name, ind]
						self.play_to_stage(ind, st)
				elif "swap" in self.gd["effect"]:
					if len(self.gd["target"]) > 0:
						lv = self.gd["target"].pop(0)
						lvpos = self.cd[lv].pos_new
						indpos = self.cd[ind].pos_new
						swap = self.gd["effect"][self.gd["effect"].index("swap") + 1]
						if "CX" in swap:
							swap = "Climax"
						if swap in lvpos:
							lpos = self.pd[lv[-1]][swap].index(lv)
							ipos = self.pd[lv[-1]][indpos].index(ind)
							self.send_to(lvpos, ind, lpos)
							self.send_to(indpos, lv, ipos)
						else:
							lpos = self.pd[ind[-1]][swap].index(ind)
							ipos = self.pd[ind[-1]][lvpos].index(lv)
							self.send_to(lvpos, ind, ipos)
							self.send_to(indpos, lv, lpos)
				elif "flip" in self.gd["effect"]:
					if "down" in self.gd["effect"] and not self.cd[ind].back:
						if ind[-1] != imd[-1]:
							self.cd[ind].show_back(False)
						else:
							self.cd[ind].show_back()
					elif "up" in self.gd["effect"] and self.cd[ind].back:
						self.cd[ind].show_front()
				elif "Level" in self.gd["effect"]:
					if "if" in self.gd["effect"]:
						lif.append(ind)
					self.send_to("Level", ind)
				elif "Clock" in self.gd["effect"]:
					self.send_to("Clock", ind)
				elif "Stock" in self.gd["effect"]:
					self.send_to("Stock", ind)
				elif "CX" in self.gd["effect"]:
					self.send_to("Climax", ind)
				elif "Memory" in self.gd["effect"] or "hmemory" in self.gd["effect"]:
					if "face-down" in self.gd["effect"]:
						self.send_to("Memory", ind, face_down=True)
					else:
						self.send_to("Memory", ind)
				elif "Library" in self.gd["effect"]:
					self.send_to("Library", ind)
				else:
					lif.append(ind)
					discard.append(ind)
				if ind[-1] == "2" or (ind[-1] == "1" and imd[-1] == "2"):
					idm.append(ind)

			if discard:
				self.hand_waiting(chosen=discard)

			self.gd["discard"] = 0
			if self.gd["notarget"]:
				self.gd["notarget"] = False
			self.check_cont_ability()
			self.popup_clr()
			if self.gd["dismay"]:
				self.gd["dismay"] = False

			if self.gd["resonance"][0] and "afterreveal" not in self.gd["effect"]:
				for r in self.gd["resonance"][1]:
					if self.cd[r].back:
						self.cd[r].show_front()
					if r not in lif:
						lif.append(r)
			if "mdiscard" in self.gd["effect"]:
				self.gd["effect"].remove("mdiscard")
			elif "cxdiscard" in self.gd["effect"]:
				self.gd["effect"].remove("cxdiscard")
			elif "hmemory" in self.gd["effect"]:
				self.gd["effect"].remove("hmemory")

			if self.gd["pay"] and not self.gd["payed"]:
				Clock.schedule_once(self.pay_condition, move_dt_btw)
			else:
				if "if" in self.gd["effect"]:
					if lif or ("swap" in self.gd["effect"] and not lif):
						self.gd["done"] = True
						if isinstance(self.gd["effect"][self.gd["effect"].index("if") + 1], int) and len(lif) < self.gd["effect"][self.gd["effect"].index("if") + 1]:
							self.gd["done"] = False
					if not self.gd["done"] and "ifnot" in self.gd["effect"]:
						self.gd["ability_effect"].append("dont")
					if not self.gd["done"] and "unli" in self.gd["per_poped"] and self.gd["per_poped"][-1]:
						self.gd["per_poped"][-1] = 0
				elif "do" in self.gd["effect"] and self.gd["do"][0] > 0:
					self.gd["done"] = True
				elif self.gd["brainstorm_c"][1] and self.gd["brainstorm_c"][0] > 0:
					self.gd["brainstorm_c"][0] -= 1
					self.gd["do"][0] = 1
					self.gd["do"][1] = list(self.gd["brainstorm_c"][1])
					self.gd["done"] = True
				elif self.gd["brainstorm_c"][1] and self.gd["brainstorm_c"][0] <= 0:
					self.gd["brainstorm_c"][1] = []
				elif "do" not in self.gd["effect"] and self.gd["do_both"]:
					self.gd["do_both"] = []
					self.gd["done"] = True

				if "do" in self.gd["ability_effect"]:
					self.gd["ability_effect"].remove("do")

				if "discard" in self.gd["ability_effect"]:
					self.gd["ability_effect"].remove("discard")

				if self.gd["random_reveal"]:
					self.popup_multi_info(cards=self.gd["random_reveal"], owner=imd[-1], t="Random")
				else:
					if self.net["game"] and (("plchoose" in self.gd["effect"] and not self.net["send"]) or (self.gd["perform_both"] and "oppturn" not in self.gd["effect"])):
						self.net["var"] = list(self.net["act"][4])
						self.net["var1"] = "plchoose"
						if not self.poptext:
							Clock.schedule_once(partial(self.popup_text, "waitingser"))
						self.mconnect("plturn")
					else:
						self.ability_effect()

	def choose_trait(self, dt=0):
		imd = self.gd["ability_trigger"].split("_")[1]
		if self.gd["com"] and (imd[-1] == "2" or ("oppturn" in self.gd["effect"] and imd[-1] == "1")) and not self.gd["chosen"]:
			self.gd["target"].append(choice(all_traits))

		if self.gd["p_c"] != "" and not self.gd["target"]:
			self.sd["popup"]["popup"].dismiss()
			self.gd["choose_trait"] = False
			self.popup_clr()
			self.gd["target"].append("".join(str(self.sd["popup"]["sutext"].text).strip()))
			Clock.schedule_once(self.choose_trait)
		elif self.gd["p_c"] == "" and not self.gd["target"]:
			self.popup_clr_button()
			self.sd["popup"]["popup"].title = "Choose a trait"
			self.gd["popup_pop"] = True
			self.gd["popup_done"] = (True, False)
			self.gd["popup_on"] = True
			self.gd["choose_trait"] = True
			self.gd["p_c"] = "trait"
			self.gd["p_owner"] = "1"
			self.gd["p_xscat"] = self.sd["padding"] * 2 + self.gd["p_width"] * starting_hand
			self.gd["p_hand"] = starting_hand
			self.sd["popup"]["p_scv"].do_scroll_y = False
			self.sd["popup"]["stack"].clear_widgets()

			self.sd["btn"]["field_btn"].center_x = self.gd["p_xscat"] / 4 - self.sd["padding"] / 2
			self.sd["btn"]["field_btn"].y = self.sd["padding"] * 1.5
			self.sd["btn"]["choose_trait_btn"].center_x = self.gd["p_xscat"] / 4 * 3 - self.sd["card"][0] / 2
			self.sd["btn"]["choose_trait_btn"].y = self.sd["padding"] * 1.5
			self.sd["btn"]["choose_trait_btn"].size = (self.sd["card"][0] * 2.5, self.sd["card"][1] / 2.)

			self.sd["popup"]["sutext"].text = ""
			self.sd["popup"]["sutext"].size = (self.sd["card"][0] * starting_hand, self.sd["card"][1] / 1.5)
			self.sd["popup"]["sutext"].y = self.sd["padding"] * 3 + self.sd["card"][1] / 2.
			self.sd["popup"]["sutext"].center_x = self.gd["p_xscat"] / 2 - self.sd["card"][0] / 4

			self.sd["popup"]["popup"].size = (self.gd["p_xscat"], self.sd["popup"]["sutext"].size[1] + self.sd["card"][1] + self.sd["padding"] * 7 + self.sd["popup"]["popup"].title_size + self.sd["popup"]["popup"].separator_height)

			self.sd["popup"]["p_scv"].size = (self.gd["p_xscat"], self.sd["card"][1] + self.sd["padding"])
			self.sd["popup"]["p_scv"].y = self.sd["popup"]["sutext"].y

			self.sd["popup"]["popup"].open()
		else:
			if "xremovechoose" in self.gd["effect"]:
				if self.gd["effect"][0] == 0:
					trait = ""
					for _ in list(self.cd[imd].trait_c):
						if _[1] == -66:
							trait = _[0]
							self.cd[imd].trait_c.remove(_)
							break

			ind = self.gd["target"].pop(0)
			self.gd["effect"][1] = ind

			if self.net["game"] and self.gd["p_owner"] == "1":  
				self.net["act"][4].append(ind)

			self.trait()

	def hand_limit_start(self):
		self.gd["chosen"] = []
		self.gd["choose"] = False
		self.gd["uptomay"] = False

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

				self.gd["confirm_var"] = {"o": self.gd["active"], "c": "Hand"}
				self.popup_start()
		else:
			self.hand_limit_done()

	def hand_limit_done(self, btn=None):
		self.sd["popup"]["popup"].dismiss()

		if len(self.pd[self.gd["active"]]["Hand"]) > hand_limit and self.net["game"] and self.gd["active"] == "1" and not self.net["send"]:
			self.net["var"] = list(self.gd["chosen"])
			self.net["var1"] = "hand_limit"
			if not self.poptext:
				Clock.schedule_once(partial(self.popup_text, "waitingser"))
			self.mconnect("phase")
		else:
			self.hand_waiting(chosen=self.gd["chosen"])
			self.check_cont_ability()
			self.popup_clr()
			self.end_phase_end()

	def end_phase_end(self, dt=0):
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
			self.gd["no_encore"] = {"1": False, "2": False}
			self.pd[self.gd["active"]]["done"]["End"] = True
			for key in self.pd[self.gd["opp"]]["phase"].keys():
				if any(key != phase for phase in ("Janken", "Mulligan")):
					self.pd[self.gd["opp"]]["phase"][key] = False
					self.pd[self.gd["opp"]]["done"][key] = False
			self.pd[self.gd["active"]]["phase"]["Encore"] = False
			self.pd[self.gd["active"]]["done"]["Encore"] = False
			self.gd["turn"] += 1
			if self.gd["turn"] % 2 == 0 and self.gd["turn"] > 0:
				self.gd["active"] = str(self.gd["second_player"])
				self.gd["opp"] = str(self.gd["starting_player"])
			else:
				self.gd["active"] = str(self.gd["starting_player"])
				self.gd["opp"] = str(self.gd["second_player"])

			self.gd["phase"] = "Stand Up"
			Clock.schedule_once(self.beginning_phase, phase_dt)

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

	def level_size(self, player):
		pos = self.mat[player]["field"]["Level"]

		_ = 0
		for card in self.pd[player]["Level"]:
			self.mat[player]["mat"].remove_widget(self.cd[card])
			self.mat[player]["mat"].add_widget(self.cd[card])

			y = pos[1] + _ * (pos[3] - pos[1]) / 2
			self.cd[card].setPos(pos[0], y, t="Level")

			_ += 1

		self.update_colour(player)

	def update_colour(self, player):
		self.pd[player]["colour"] = []
		for _ in self.pd[player]["Level"] + self.pd[player]["Clock"]:
			if self.cd[_].mcolour.lower() not in self.pd[player]["colour"]:
				self.pd[player]["colour"].append(self.cd[_].mcolour.lower())
		self.sd[f"colour{player}"].update_colour(self.pd[player]["colour"])

	def stack(self, player, field="Library"):
		if len(self.pd[player][field]) > 0:
			for ind in self.pd[player][field]:
				self.mat[player]["mat"].remove_widget(self.cd[ind])
				self.mat[player]["mat"].add_widget(self.cd[ind])

	def hand_size(self, owner, move=True):
		cards = self.pd[owner]["Hand"]
		width = self.sd["card"][0] + self.sd["padding"]
		height = self.sd["card"][1] + self.sd["padding"] * 1.5
		many = False

		if self.mat[owner]["mat"].size[0] - (len(cards) * width + self.sd["padding"]) < 0:
			width = (self.mat[owner]["mat"].size[0] - self.sd["padding"] * 2 - self.sd["card"][0]) / (len(cards) - 1)
			many = True

		_ = 0
		for card in cards:
			if owner == "3":
				self.cd[card].show_back()  
			else:
				self.cd[card].show_front()

			self.mat[owner]["mat"].remove_widget(self.cd[card])
			self.mat[owner]["mat"].add_widget(self.cd[card])

			if self.gd["swap_card"][0] and self.gd["selected"] != "" and _ < self.gd["swap_card"][2]:
				self.mat[owner]["mat"].remove_widget(self.cd[self.gd["swap_card"][1]])
				self.mat[owner]["mat"].add_widget(self.cd[self.gd["swap_card"][1]])
				self.gd["swap_card"][0] = False

			if move:
				if many:
					xpos = self.sd["padding"] + width * _
				elif len(cards) % 2 == 0:
					xpos = self.mat[owner]["mat"].size[0] / 2. - len(cards) / 2. * width + self.sd["padding"] / 2. + width * _
				elif len(cards) % 2 != 0:
					xpos = self.mat[owner]["mat"].size[0] / 2. - (len(cards) - 1) / 2. * width - self.sd["card"][0] / 2. + width * _

				self.cd[card].setPos(xpos, -height, t="Hand")
			_ += 1

		if self.sd["hbtn"]:
			self.hand_btn_show(False)
			self.hand_btn_show()

	def sort_by_level(self, player):
		self.pd[player]["Hand"] = sorted(self.pd[player]["Hand"], key=lambda x: self.cd[x].level)
