from base64 import b64decode as bdeco
from base64 import b64encode as benco
from hashlib import md5
from json import dump as jdump
from json import dumps as jdumps
from json import load as jload
from json import loads as jloads
from os import remove
from zlib import compress as zcom
from zlib import decompress as zdecom
from core.ability import Ability as Ab
from core.datapath import *
def json_zip(j):
	j = {ZIP_KEY: benco(zcom(jdumps(j, ensure_ascii=False, separators=(',', ':')).encode('utf-8'))).decode('ascii')}
	return j
def json_unzip(j, insist=True):
	try:
		assert (j[ZIP_KEY])
		assert (set(j.keys()) == {ZIP_KEY})
	except:
		if insist:
			raise RuntimeError("JSON not in the expected format {" + str(ZIP_KEY) + ": zipstring}")
		else:
			return j
	try:
		j = zdecom(bdeco(j[ZIP_KEY]))
	except:
		raise RuntimeError("Could not decode/unzip the contents")
	try:
		j = jloads(j)
	except:
		raise RuntimeError("Could interpret the unzipped contents")
	return j
def pdata_init():
	return {
		"1": {"Hand": [], "Res": [], "Clock": [], "Library": [], "Level": [], "Climax": [], "Stock": [], "Memory": [],
		      "Center": ["", "", ""], "Back": ["", ""], "Waiting": [], "colour": [], "janken": "",
		      "marker": {},
		      "deck": {},
		      "name": "",
		      "deck_name": "",
		      "deck_id": "",
		      "phase": {"Janken": False,
		                "Mulligan": False,
		                "Stand Up": False,
		                "Draw": False,
		                "Clock": False,
		                "Main": False,
		                "Climax": False,
		                "Attack": False,
		                "Declaration": False,
		                "Trigger": False,
		                "Counter": False,
		                "Damage": False,
		                "Battle": False,
		                "Encore": False,
		                "End": False},
		      "done": {"Janken": False,
		               "Mulligan": False,
		               "Stand Up": False,
		               "Draw": False,
		               "Clock": False,
		               "Main": False,
		               "Climax": False,
		               "Attack": False,
		               "Declaration": False,
		               "Trigger": False,
		               "Counter": False,
		               "Damage": False,
		               "Battle": False,
		               "Encore": False,
		               "End": False}},
		"2": {"Hand": [], "Res": [], "Clock": [], "Library": [], "Level": [], "Climax": [], "Stock": [], "Memory": [],
		      "Center": ["", "", ""], "Back": ["", ""], "Waiting": [], "encore": [], "colour": [], "janken": "",
		      "marker": {},
		      "deck": {},
		      "name": "",
		      "deck_name": "",
		      "deck_id": "",
		      "phase": {"Janken": False,
		                "Mulligan": False,
		                "Stand Up": False,
		                "Draw": False,
		                "Clock": False,
		                "Main": False,
		                "Climax": False,
		                "Attack": False,
		                "Declaration": False,
		                "Trigger": False,
		                "Counter": False,
		                "Damage": False,
		                "Battle": False,
		                "Encore": False,
		                "End": False},
		      "done": {"Janken": False,
		               "Mulligan": False,
		               "Stand Up": False,
		               "Draw": False,
		               "Clock": False,
		               "Main": False,
		               "Climax": False,
		               "Attack": False,
		               "Declaration": False,
		               "Trigger": False,
		               "Counter": False,
		               "Damage": False,
		               "Battle": False,
		               "Encore": False,
		               "End": False}}}
def gdata_init():
	return {"debug": True,
	        "d_rotation": False,
	        "d_opp_first": False,
	        "d_pl_first": False,
	        "d_3atk_1turn": False,
	        "d_btn_list": [],
	        "multiplay_btn": True,
	        "download_btn": True,
	        "show_opp_hand": False,
	        "show_wait_popup": True,  
	        "com": True,
	        "confirm_requirement": True,
	        "overlap_confirm": True,  
	        "remove_cards_in_deck": False,
				"HDimg":False,
	        "load": False,
	        "check_atk": True,
	        "check_ctr": False,
	        "status": "",
	        "req": False,
	        "cancel_down": False,
	        "pay": [],
	        "payed": False,
	        "paypop": False,
	        "pay_status": "",
	        "do_status": "",
	        "done": "",
	        "do": [0, [],[]],
	        "do_both": [],
	        "decker": False,
	        "selected": "",
	        "selected_o": "",
	        "stage": ["Center0", "Center1", "Center2", "Back0", "Back1"],
	        "fields": ["Hand", "Center", "Back"],
	        "janken_choice": ("l", "k", "p", "s"),
	        "moveable": [], "playable_climax": [],
				"cont_on":False,
	        "stack": {"1": [], "2": []},
	        "stacked": {"0": []},
	        "save_name": "",
			  "filter_card": [False,[],[]],
	        "update_edata": False,
	        "swap_card": [False, "", 0, 0],
	        "select_btns": [],
	        "chosen": [],
	        "text": "",
	        "text_popup": False,
	        "popup_on": False,
	        "active_card": None,
	        "results": 0,
	        "drawed": [],
	        "per_poped": ["",[],0,-1,0],
	        "act_pop": {},
	        "act_poped": "",
	        "reshuffle_trigger_temp": "",
	        "mill_check": [],
	        "cancel_dmg": False,
	        "trigger_icon": [],
	        "stage-1": [],
	        "p_owner": "",
	        "p_ind": "",
	        "menu": False,
	        "p_select": [],
	        "p_c": "",
	        "p_f": True,
	        "p_max_s": 0,
	        "p_min_s": -1,
	        "popup_done": (False, False),  
	        "p_rows": 1,
	        "p_l": [],
	        "p_ld": [],
	        "p_t": [],
	        "p_ltitle": "",
	        "p_j": 0,
	        "p_width": 0,
	        "p_height": 0,
	        "p_pad": 0,
	        "p_hand": 0,
	        "p_xscat": 0,
	        "p_yscat": 0,
	        "p_title": 0,
	        "p_yscv": 0,
	        "p_yssct": 0,
	        "p_ypop": 0,
	        "p_look": 0,
	        "p_cards": [],
	        "p_fcards": [],
	        "p_stage": 0,
	        "p_again": False,
	        "p_flvl": "Lvl -",
	        "p_fcolour": "Colour",
	        "p_ftype": "Type",
	        "p_ftrait": "Trait",
	        "p_over": False,
	        "p_ftext": "",
	        "j_hand": "",
	        "j_hand_opp": "",
	        "j_result": 0,
	        "end_stage": False,
	        "touch_down": (0., 0.),
	        "touch_move_x": tuple(),
	        "touch_move_y": tuple(),
	        "old_pos": tuple(),
	        "popup_encore": True,
	        "auto_recheck": False,
	        "counter_icon": {"1": [True, True], "2": [True, True]},
	        "triggers": [],
	        "game_start": False,
	        "gg": False,
	        "no_backup": {"1": False, "2": False},
	        "no_event": {"1": False, "2": False},
	        "no_cont_check": False,
	        "reserve": {"1": [], "2": []},
	        "check_reserve": False,
	        "confirm_pop": False,
	        "popup_pop":False,
	        "phase": "", "pp": -1,
	        "starting_player": "", "second_player": "", "active": "", "opp": "", "rev": False, "turn": 0, "inx": 0,
	        "rev_counter": False,
	        "mulligan": [[], []],
	        "encore_type": "",
	        "attack_start": True,
	        "contadd":{},
	        "dmg": 0,
	        "attack": 0,
	        "clear": True,
	        "oppchoose": False,
	        "trigger_card": "",
	        "d_atk": [1, []],
	        "attacking": ["", "", 0, 0, ""],
	        "draw_both": [int(starting_hand), False, False],
	        "draw_upto": 0,
	        "shuffle": [],
	        "levelup": {"1": False, "2": False},
	        "shuffle_trigger": "",
	        "shuffle_rep": int(shuffle_n),
	        "shuffle_send": False,
	        "draw": 0,
	        "play": [],
	        "xdiscard": [],
	        "discard": 0,
	        "btrait": ["", [], [], [], [], []],
	        "dismay": False,
	        "extra": [],
	        "extra1": [],
	        "mill": 0,
	        "reveal": 0,
	        "reveal_ind": "",
	        "trigger": 1,
	        "mtrigger": 0,
	        "standby": ["", "", ""],
	        "clocker": False,
	        "clocker_rev": False,
	        "no_act": {"1": False, "2": False},
	        "no_climax": {"1": False, "2": False},
	        "any_Clrclimax": {"1": False, "2": False},
	        "any_ClrChname": {"1": [], "2": []},
	        "no_clock": {"1": False, "2": False},
	        "no_damage":{"1": [], "2": []},
	        "no_damage_auto_opp":{"1": False, "2": False},
	        "climax_play": False,
	        "reshuffle": False,
	        "reshuffle_trigger": "",
	        "level_up_trigger": "",
	        "level_up": False,
	        "rrev":False,
	        "drev":False,
	        "damage": 0,
	        "damage_trigger":"",
	        "damage_refresh": 0,
	        "ability_trigger": "",
	        "power": (),
	        "marker_waiting":[],
	        "soul": (),
	        "stock": 0,
	        "numbers": "",
	        "play_card": "",
	        "check_clock":False,
	        "payed_mstock":False,
	        "ability_effect": [],
	        "ability": "",
	        "ability_doing": "",
	        "targetpay": [],
	        "moving": False,
	        "uptomay": False,
	        "nomay": False,
	        "notarget": False,
	        "target": [],
	        "target_temp": [],
	        "salvage_cost": [],
	        "salvage": 0,
	        "ksalvage": "",
	        "reveal_top": [],
	        "skip_top": [],
	        "clock_done": "",
	        "both": False,
	        "confirm_trigger": "",
	        "confirm_var": {},
	        "janken_result": 0,
	        "confirm_result": "",
	        "stack_pop": False,
	        "confirm_temp": {},
	        "btn_id": "",
	        "ifcount":0,
	        "refresh_point":False,
	        "trev": "",
	        "search": "",
	        "damageref": False,
	        "show": [],
	        "reflev": [],
	        "choose": False,
	        "encore": {"1": [], "2": []},
	        "stock_payed":False,
	        "no_encore": {"1": False, "2": False},
	        "search_type": "",
	        "counter": [],
	        "counter_id": "",
	        "opp_play": [],
	        "opp_move": [],
	        "opp_attack": [],
	        "clock_temp": None,
	        "perform": 0,
	        "perform_both": False,
	        "perform_a": [],
	        "opp_encore": [],
	        "opp_ability": [],
	        "effect": [],
	        "btn_release": True,
	        "skip": [],
	        "encore_ind": "",
	        "Res1_move": False,
	        "auto_effect": [],
	        "bodyguard": False,
	        "move": "",
	        "markerstock":[],
	        "astock": {"1": [], "2": []},
	        "astock_select":False,
	        "estock": {"1": [], "2": []},
	        "mstock": ["",0],
	        "if": [],
	        "ld": False,
	        "astock_pop": False,
	        "estock_pop": False,
	        "notargetfield": False,
	        "brainstorm": 0,
	        "stack_return":False,
	        "brainstorm_c": [0, []],
	        "resonance": [False, [],0],
	        "random_reveal": [],
	        "confirm": False,
	        "confirm1": [False, 0],
	        "confirm2": [False, 0],
	        "popup_attack": 1,
	        "btn_pressed": [0, None],
	        "revive": [],
	        "info_p": False,
	        "last": "",
	        "so": [],
	        "sn": {},
	        "battle": [],
	        "attack_t": {"d": [True, True, True], "s": [True, True, True], "f": [True, True, True]}
	        }
def network_init():
	return {
		"url": "https://www.totuccio.com/ws/ws.php",
		"data": "https://www.totuccio.com/ws/data/",
		"var": "",
		"var1": "",
		"room": 0,
		"select": 0,
		"player": 0,
		"actual": "",
		"private": False,
		"status": "",
		"body": "",
		"failed": False,
		"got": False,
		"time": -1,
		"ready": 0,
		"game": "",
		"wait": False,
		"send": False,
		"lvlsend": True,
		"varlvl": [],
		"act": ["", "", 0, [], [], 0, -1]
	}
def add_db(item):
	with open(f"{data_ex}/{item}-d", "r", encoding="utf-8") as rjson:
		temp = json_unzip(jload(rjson))
		for key in list(temp.keys()):
			for item2 in temp[key]:
				if key == "c":
					if item2 not in se["main"][key]:
						se["main"][key].append(item2)
				elif key == "t":
					if item2 not in sd:
						sd[item2] = dict(temp[key][item2])
				elif key == "s":
					if item2 not in se["main"][key]["Title"]:
						se["main"][key]["Title"].append(item2)
					if "w" not in se["main"]:
						se["main"]["w"] = []
					if item2 != "":
						se["main"]["w"].append(item2)
				elif key == "p":
					if item2 not in sp:
						sp[item2] = dict(temp[key][item2])
				elif key == "m":
					if item2 not in se["main"][key]:
						se["main"][key].append(item2)
def atlas_make():
	files = {}
	to_remove = []
	for item in se["check"]:
		files[item] = {}
		for item1 in se["check"][item]:
			if "-d" in item1 and exists(f"{data_ex}/{item1}"):
				with open(f"{data_ex}/{item1}", "rb") as ft:
					hash_md5 = md5()
					for chunk in iter(lambda: ft.read(4096 * 10), b""):
						hash_md5.update(chunk)
					if hash_md5.hexdigest() == se["check"][item][item1]:
						if "w" in se["main"] and se["check"][item]["s"] in se["main"]["w"]:
							se["main"]["w"].remove(se["check"][item]["s"])
						add_db(item)
					else:
						to_remove.append(f"{data_ex}/{item1}")
			else:
				continue
	for item in to_remove:
		remove(item)
ZIP_KEY = 'I2UHBG58pJ'
ab = Ab()
with open(f"{data_in}/edata.db", "r", encoding="utf-8") as rp:
	se = json_unzip(jload(rp))
with open(f"{data_in}/cdata.db", "r", encoding="utf-8") as rc:
	sc = json_unzip(jload(rc))
sp = se["playmat"]
sd = se["main"]["t"]
sn = se["neo"]
annex_img = []
with open(f"{img_in}/annex.atlas", "r", encoding="utf-8") as ax:
	ann = jload(ax)
	for f in ann:
		for an in ann[f].keys():
			annex_img.append(an)
other_img = []
with open(f"{img_in}/other.atlas", "r", encoding="utf-8") as ox:
	ann = jload(ox)
	for f in ann:
		for an in ann[f].keys():
			other_img.append(an)
if exists(f"{data_ex}/cej.db"):
	with open(f"{data_ex}/cej.db", "r", encoding="utf-8") as rd:
		scej = json_unzip(jload(rd))
		for deck in scej:
			sd[deck] = dict(scej[deck])
else:
	scej = {}
	with open(f"{data_ex}/cej.db", "w") as w_d:
		jdump(json_zip(scej), w_d, separators=(',', ':'))
atlas_make()
phases = ["Stand Up", "Draw", "Clock", "Main", "Climax", "Attack", "End"]  
steps = ["Declaration", "Trigger", "Counter", "Damage", "Battle", "Encore"]  
icon_lst = ("door", "soul", "gate", "bar", "bag", "book", "shot", "bounce", "counter", "clock", "arrow")
info_popup_dt = 1.10  
info_popup_press = 3  
phase_dt = 1.15 * 0.75  
joke_dt = 0.3  
ability_dt = 0.001  
move_dt = 0.35  
move_dt_btw = move_dt * 1.25  
popup_dt = 0.2  
reveal_dt = 1.15
server_dt = 1
match_dt = 2  
shuffle_dt = 0.02  
shuffle_n = 7  
starting_hand = 5  
hand_limit = 7  
dbuild_limit = 5  
popup_max_cards = 7  
select2cards = 5
COMPUTER = True
cont_ability = "[CONT]"
auto_ability = "[AUTO]"
act_ability = "[ACT]"
cont_waiting = ["SHS/W98-040"]
