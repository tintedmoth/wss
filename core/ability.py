from unicodedata import numeric
from re import finditer

from core.markreplace import markreplace
from copy import deepcopy


def transform_list(lst, key=""):
	result = lst[-1]
	for i in range(len(lst) - 2, -1, -1):
		item = lst[i]
		if key:
			result = item + [key, result]
		else:
			result = item + [result]
	return result


class Ability:
	ablt = 0
	opnextturn = False
	target = ""
	aselected = ""
	cx = False
	center = False
	cond = [0, 0, 0, 0, 0, 0]  
	ee = False
	start = False
	cond_later = False
	no_pay = False
	cond_rep = [False, []]
	isnot = ""
	donot = ""
	multicond = ["", 0]
	tt = ""
	dmg = 0
	dd = ""
	temp = [0, ""]
	xx = None
	resource = {
		"Library": "Deck", "library": "deck", "gain": "get", "a Character": "1 Character", "a character": "1 character", "hoose either an ": "hooses 1 ", "hoose either a ": "hooses 1 ", "hooses a ": "hooses 1 ", "hoose a ": "hoose 1 ", "hoose an ": "hoose 1 ", " a card": " 1 card", "is equal to": "=",
		"all of your": "all your", "discard an ": "put 1 ", "discard a ": "put 1 ", "put a ": "put 1 ", "put an ": "put 1 ",
		"or a ": "or 1 ", "or an ": "or 1 ", "this card": "this", "three cards": "3 cards", "two cards": "2 cards",
		" four ": " 4 ", " five ": " 5 ", " six ": " 6 ", " seven ": " 7 ", "into your": "in your", "into his": "in his",
		" one ": " 1 ", " two ": " 2 ", "reversed": "reverse", "climax zone": "climax area", "underneath": "under",
		"three": "3", "facing": "opposite", " 2 soul": " soulsoul", " 2 Soul": " soulsoul",
		"foe or 1 new": "foe or a new", "the 2 of us": "the two of us", "libraries": "decks",
		"times per turn": "time per turn", "when 1 card named": "when a card named", "frontal": "front",
		"When 1 card named": "When a card named", "not an ": "not a ", "for an ": "for 1 ", "if a climax is put": "if 1 climax is put",
		"if 1 card": "if a card", "If 1 card": "If a card", "back row": "back stage", "level-up": "level up",
		"front row slots on stage": "position on your center stage", "front row": "center stage", "twice": "2 times"
	}
	text_change = {"enemy? ally? or 1 new character?": "enemy? ally? or a new character?", "new route of 2 nights and 3 days": "new route of two nights and three days", "fight agetst the strong": "fight against the strong", "unit 1 of the public safety bureau's criminal investigation division": "unit one of the public safety bureau's criminal investigation division"}
	icon = {"[SHOT]": "SHOT", "[BOUNCE]": "BOUNCE", "[POOL]": "POOL", "[SOUL]": "SOUL", "[TREASURE]": "TREASURE", "[DOOR]": "DOOR", "[STANDBY]": "STANDBY", "[DRAW]": "DRAW", "[GATE]": "GATE", "[STOCK]": "STOCK"}
	colour = ("red", "blue", "yellow", "green")
	ability = ("[CONT]", "[AUTO]", "[ACT]", "[CLOCK]", "[COUNTER]", "[Counter]", "[CXCOMBO]", "[ALARM]")
	status = {"[REST]": "REST", "[STAND]": "STAND", "[REVERSE]": "REVERSE"}
	skip_text = {"[Deploy]": "Deploy"}
	stage = ("Center", "Back")
	abstart = ("change [", "accelerate [", "resonate [", "resonance [", "cx combo [", "memory [", "recollection [", "brainstorm [", "experience [")
	attack = ("Attack", "Declaration", "Trigger", "Counter", "Damage", "Battle")
	alpha = "qwertyuiopasdfghjklzxcvbnm"
	digits = "0123456789"
	text_name = {
		"Assist": "] Assist", "Memory": "] Memory_] Recollection", "Experience": "] Experience",
		"Accelerate": "] Accelerate", "Change": "] Change", "Resonance": "] Resonance", "Resonate": "] Resonate",
		"[AUTO] Encore [Put the top card of your deck into your clock]": "[AUTO] Encore [Put the top card of your deck into your clock]",
		"[AUTO] Encore [Put 1 character from your hand into your waiting room]": "[AUTO] Encore [Put 1 character from your hand into your waiting room]_[AUTO] Encore [Put a character from your hand into your waiting room]",
		"[AUTO] Encore [Put a character from your hand into your waiting room]": "[AUTO] Encore [Put 1 character from your hand into your waiting room]_[AUTO] Encore [Put a character from your hand into your waiting room]"
	}
	remove_text = ["Encore [Put 1 character from your hand in your waiting room]", "Encore [Put a character from your hand into your waiting room]", "Encore [Put the top card of your deck into your clock]"]
	set_only = markreplace["set_only"]
	skill_name = ("[Deploy]", "[Cascade]")
	donot_text = ["if not", "if you do not"]
	isnot_text = ["if it is not", "if it's not", " otherwise"]
	cont_key = ("ability", "ability0", "ability1", "power", "soul", "level", "trait", "name", "cost", "contadd", "astock", "estock")
	pay_stock = [("[(7)", 7), ("[(6)", 6), ("[(5)", 5), ("[(4)", 4), ("[(3)", 3), ("[(2)", 2), ("[(1)", 1)]

	def pay(self, a=""):
		self.cond = [0, 0, 0, 0, 0, 0]
		t = str(a)
		for _, value in self.set_only.items():
			t = t.replace(f"{_}", f"{value}")

		for item, value in self.status.items():
			t = t.replace(item, value)

		for item1 in self.remove_text:
			t = t.replace(item1, "")

		for item1 in self.ability:
			t = t.replace(item1, "")

		t = t.lower()

		for rep, value in self.resource.items():
			t = t.replace(rep, value)

		if " (" in t:
			t = t.split(" (")[0]

		if "{" in t or "}" in t:
			t = t.replace("{", "(").replace("}", ")")

		if "\"[" in t or "\" [" in t:
			if "\"[" in t:
				t = t.split("\"[")[0]
			elif "\" [" in t and "bond" not in t:
				t = t.split("\" [")[0]
		s = []
		o = []
		r = []
		e = []

		for substring, value in self.pay_stock:
			if substring in t:
				s = ["Stock", value]
				break

		if "exchange a stand character in your center stage and this]" in t:
			o = ["Swap", 1, "PStand", "PCenter"]
		elif "choose 1 \"" in t and "\" in your waiting room and put it face-down as marker under a \"" in t and "\" that had no markers]" in t:
			o = ["Zwei", 1, "ZName=", self.name(a, s='n', p=True), "ZM", 1, "ZMName=", self.name(a, 2, s='n', p=True), "ZMarkers", 0, "ZMlower"]
		elif "put this face-down under an \"" in t and "\" with no markers]" in t:
			o = ["Zwei", 1, "Zthis", "ZM", 1, "ZMName=", self.name(a, s='n', p=True), "ZMarkers", 0, "ZMlower"]
		elif "turn this face-up card face-down]" in t:
			if "if this is in memory" in a.lower():
				o = ["MFlip", 0, "down"]
			else:
				o = ["Flip", 0, "down"]
		elif ("reveal a \"" in t or "reveal 1 \"" in t or "reveal 1 character with \"" in t) and ("\" in your hand and put it in your stock]" in t or "\" from your hand and put it face-down under this as marker]" in t or "\" from your hand]" in t or "\" in your hand]" in t or "\" from your hand to your opponent]" in t or "\" from hand]" in t or "\" in name in your hand]" in t):
			if "\" in your hand and put it in your stock]" in t:
				o = ["RevealStock", self.name(a, s='n', p=True)]
			elif "\" from your hand and put it face-down under this as marker]" in t:
				o = ["RevealMarker", self.name(a, s='n', p=True)]
			elif "\" from your hand]" in t or "\" in your hand]" in t or "\" from your hand to your opponent]" in t or "\" from hand]" in t or "\" in name in your hand]" in t:
				if self.play(t) and "Name" in self.play(t):
					o = ["Reveal", self.name(a, 2, s='n', p=True)]
				else:
					o = ["Reveal", self.name(a, s='n', p=True)]
		elif "reveal any number of \"" in t and ("\" from your hand]" in t or "\" in your hand]" in t):
			o = ["Reveal", self.name(a, s='n', p=True), "any"]
		elif "put this stand card in your memory]" in t or "send this standing card to memory]" in t:
			o = ["Memory", 0]
		elif "put this in your memory]" in t or "send this to memory]" in t:
			o = ["Memory", 0]
		elif "put 1 \"" in t and ("\" from your hand to the waiting room]" in t or "\" from your hand in your waiting room]" in t or "\" from hand to the waiting room]" in t or "\" from your hand in your waiting room]" in t):
			if "\" or \"" in t.split("waiting room]")[0]:
				o = ["Discard", 1, "Name=", f"{self.name(a, s='n', p=True)}_{self.name(a, 2, s='n', p=True)}"]
			else:
				o = ["Discard", 1, "Name=", self.name(a, s='n', p=True)]
		elif "put 1 \"" in t and "\" from hand in clock]" in t:
			o = ["ClockH", 1, "Name=", self.name(a, s='n', p=True)]
		elif "put 1 character card with \"" in t and "\" in name from your hand to the waiting room]" in t:
			o = ["Discard", 1, "CName", self.name(a, s='n', p=True)]
		elif "put 1 \"" in t and ("from your memory to your waiting room]" in t or "from your memory to the waiting room]" in t or "from your memory in the waiting room]" in t):
			o = ["MDiscard", 1, "MName=", self.name(a, s='n', p=True)]
		elif "put 1 character with \"" in t and "in name from your memory in the waiting room]" in t:
			o = ["MDiscard", 1, "MCName", self.name(a, s='n', p=True)]
		elif "put 1 \"" in t and ("from your climax area in your waiting room]" in t or "from your climax area to the waiting room]" in t or "from your climax area in the waiting room]" in t):
			if "\" from your hand in your waiting room &" in t:
				o = ["CXDiscard", 1, "CXName=", self.name(a, 2, s='n', p=True)]
			else:
				o = ["CXDiscard", 1, "CXName=", self.name(a, s='n', p=True)]
		elif "put 1 climax card with a gate trigger icon from hand to the waiting room]" in t:
			o = ["Discard", 1, "TriggerCX", "gate"]
		elif "put 1 climax with [treasure] in its trigger icon from your hand in your waiting room]" in t:
			o = ["Discard", 1, "TriggerCX", "treasure"]
		elif "put 1 climax from your hand in your waiting room]" in t or "put 1 climax card from hand to the waiting room]" in t or "put 1 climax card from your hand to the waiting room]" in t:
			o = ["Discard", 1, "Climax"]
		elif "put 1 climax from your waiting room in your memory]" in t:
			o = ["Salvage", 1, "Climax", "SMemory"]
		elif "put 1 blue climax from your hand in your waiting room]" in t:
			o = ["Discard", 1, "ColourCx", "Blue"]
		elif "put 1 character from your hand in your waiting room]" in t or "put 1 character card from your hand to the waiting room]" in t or "discard 1 character card from hand to the waiting room]" in t:
			o = ["Discard", 1, "Character"]
		elif "put this from your hand in your waiting room]" in t or "discard this from your hand to the waiting room]" in t or "discard this from hand to the waiting room]" in t:
			o = ["Discard", 0, ""]
		elif "put 1 random card from your hand in your waiting room]" in t:
			o = ["Discard", -10, ""]
		elif "put 1 character card from hand in memory]" in t:
			o = ["HMemory", 1, "Character"]
		elif "put 1 card from your hand in clock]" in t or "put 1 card from your hand in your clock]" in t or "put 1 card from hand in clock]" in t or "put 1 card from hand in your clock]" in t:
			o = ["ClockH", 1]
		elif "choose 1 \"" in t and "\" on your stage and put it in stock]" in t:
			o = ["Stocker", 1, "Name=", self.name(a, self.cond[1], s='n', p=True)]
			self.cond[1] += 2
		elif "put 1 of your characters in the waiting room]" in t or "put 1 character from the stage to the waiting room]" in t or "put 1 character from your stage in the waiting room]" in t or "put 1 character from your stage in your waiting room]" in t:
			o = ["Waiting", 1]
		elif "put 1 of your other characters from the stage in the waiting room]" in t or "choose 1 of your other characters on the stage and put it in the waiting room]" in t or "put 1 other character from your stage in your waiting room]" in t:
			o = ["Waiting", 1, "WOther"]
		elif "choose 1 of your other center stage characters and put it in the waiting room]" in t:
			o = ["Waiting", 1, "WOther", "WCenter"]
		elif "put the top card of your deck in your clock]" in t or "put 1 card from the top of your deck in your clock]" in t or "put the top card of your deck to clock]" in t:
			o = ["ClockL", 1]
		elif "put this in the waiting room]" in t or "put this in your waiting room]" in t or "put this in waiting room]" in t:
			o = ["Waiting", 0]
		elif "put 3 cards from your hand in your waiting room]" in t:
			o = ["Discard", 3, ""]
		elif "put 2 cards from your hand in your waiting room]" in t or "discard 2 cards from hand to the waiting room]" in t or "discard 2 cards from your hand to the waiting room]" in t:
			o = ["Discard", 2, ""]
		elif "discard 1 card from your hand to the waiting room]" in t or "put 1 card from your hand in your waiting room]" in t or "discard 1 card from hand to the waiting room]" in t:
			o = ["Discard", 1, ""]
		elif "return this to your hand]" in t:
			o = ["Hander", 0, ""]
		elif any(_ in t for _ in ("return 2 characters from your waiting room to your deck. shuffle your deck afterwards]", "return 2 characters in your waiting room to your deck. shuffle your deck afterwards]", "return 2 characters from your waiting room in your deck & shuffle your deck]", "return 2 character cards from your waiting room to your deck, shuffle your deck]", "return 2 characters from your waiting room to your deck & shuffle your deck]", "return 2 characters in your waiting room to your deck, and shuffle your deck]")):
			o = ["WDecker", 2, "Character"]
		elif "put this in your clock]" in t:
			o = ["ClockS", 0]
		elif "put 2 markers from under this in your waiting room]" in t:
			o = ["Marker", 2]
		elif "put 1 marker from under this in the waiting room]" in t:
			o = ["Marker", 1]
		elif "put 1 character with \"" in t and "\" in its card name from your stage in your clock]" in t:
			o = ["ClockS", 1, "Name", self.name(a, s="n", p=True)]
		elif "put 1 card named \"" in t and "\" from your hand in your waiting room]" in t:
			o = ["Discard", 1, "Name=", self.name(a, s="n", p=True)]
		elif "of your standing characters]" in t or "of your stand characters]" in t:
			if "[rest 1" in t or "[rest one" in t or "& rest 1" in t:
				o = ["Rest", 1, ""]
			elif "[rest 2" in t:
				o = ["Rest", 2, ""]
		elif "rest 1 of your characters with assist]" in t:
			o = ["Rest", 1, "Text", "] Assist"]
		elif "rest 1 of your characters]" in t:
			o = ["Rest", 1, ""]
		elif "rest this]" in t:
			o = ["Rest", 0, ""]
		elif "rest 2 of your other characters]" in t:
			o = ["Rest", 2, "Other"]
		elif "rest 2 of your characters]" in t or "rest 2 characters]" in t:
			o = ["Rest", 2, ""]
		elif "rest 3 of your characters]" in t:
			o = ["Rest", 3, ""]
		elif "rest 1 of your characters with \"" in t and ("\" in name]" in t or "\" in the name]" in t):
			o = ["Rest", 1, "Name", self.name(a, s="n", p=True)]
		elif "«" in t:
			t1 = str(a)
			for item in self.status:
				t1 = t1.replace(item, self.status[item])
			for item in self.ability:
				t1 = t1.replace(item, "")
			t1 = f'{t1.split("]")[0]}]'
			if "\"[" in t1:
				t1 = t1.split("\"[")[0]
			trait = []
			for nx in range(t1.count("«")):
				trait.append(t1.split("«")[nx + 1].split("»")[0])
			for tra in trait:
				t1 = t1.replace(tra, "").replace("«", "").replace("»", "")

			for rep in self.resource:
				if rep in t1:
					t1 = t1.replace(rep, self.resource[rep])

			if "rest 1 of your  characters and 1 of your  characters]" in t1.lower():
				o = ["Rest", 2, "BTrait", f"{trait[0]}_{trait[1]}"]
			elif "rest 1 of your  characters]" in t1.lower() or "rest 1 of your stand  characters]" in t1.lower():
				o = ["Rest", 1, "Trait", trait[0]]
			elif "rest 2 of your characters with  or ]" in t1.lower():
				o = ["Rest", 2, "Trait", f"{trait[0]}_{trait[1]}"]
			elif "rest 2 of your  characters]" in t1.lower():
				o = ["Rest", 2, "Trait", trait[0]]
			elif "rest another of your stand characters with  or ]" in t1.lower() or "rest 1 of your other stand  or  characters]" in t1.lower():
				o = ["Rest", 1, "Trait", f"{trait[0]}_{trait[1]}", "Other"]
			elif "rest 1 of your characters with  or ]" in t1.lower():
				o = ["Rest", 1, "Trait", f"{trait[0]}_{trait[1]}"]
			elif "rest 1 of your other  characters]" in t1.lower() or "rest 1 of your other stand  characters]" in t1.lower() or "rest another of your standing  characters]" in t1.lower():
				o = ["Rest", 1, "Trait", trait[0], "Other"]
			elif "choose 2  characters in the waiting room and return them to the deck]" in t1.lower():
				o = ["WDecker", 2, "Trait", trait[0]]
			elif "return 2 characters with  and/or  from your waiting room to your deck]" in t1.lower() or "return 2  or  characters from your waiting room to your deck & shuffle your deck]" in t1.lower():
				o = ["WDecker", 2, "Trait", f"{trait[0]}_{trait[1]}"]
			elif "put a  or  or  character from your hand in your waiting room]" in t1.lower():
				o = ["Discard", 1, "Trait", f"{trait[0]}_{trait[1]}_{trait[2]}"]
			elif "discard a  or  character from hand to the waiting room]" in t1.lower() or "discard a character card with either  or  from your hand to the waiting room]" in t1.lower() or "put 1  or  character from your hand in your waiting room]" in t1.lower():
				o = ["Discard", 1, "Trait", f"{trait[0]}_{trait[1]}"]
			elif "put a  character from your hand in your waiting room]" in t1.lower() or "discard a  character card from your hand to the waiting room]" in t1.lower() or "discard a  character from hand to the waiting room]" in t1.lower() or "put 1  character from your hand in your waiting room]" in t1.lower():
				o = ["Discard", 1, "Trait", trait[0]]
			elif "put 2  characters from your hand in your waiting room]" in t1.lower():
				o = ["Discard", 2, "Trait", trait[0]]
			elif "put 3  characters from your hand in your waiting room]" in t1.lower():
				o = ["Discard", 3, "Trait", trait[0]]
			elif any(f"discard a {cl} or  character card from your hand to the waiting room]" in t1.lower() for cl in self.colour):
				o = ["Discard", 1, "CColourT", f"{self.colour_t(t1, p=True)}_{trait[0]}"]
			elif "put a  character card from your hand in clock]" in t1.lower() or "put 1  character from your hand in your clock]" in t1.lower():
				o = ["ClockH", 1, "Trait", trait[0]]
			elif "put 1  or  character on your stage in your clock]" in t1.lower():
				o = ["ClockS", 1, "Trait", f"{trait[0]}_{trait[1]}"]
			elif "put a  character from your stage in your clock]" in t1.lower():
				o = ["ClockS", 1, "Trait", trait[0]]
			elif "put a  character from your waiting room on the bottom of the clock]" in t1.lower() or "put 1  character from your waiting room at the bottom of your clock]" in t1.lower():
				o = ["ClockW", 1, "Trait", trait[0], "Cbottom"]
			elif "put 1 of your other  characters from stage in the waiting room]" in t1.lower():
				o = ["Waiting", 1, "WTrait", trait[0], "WOther"]
			elif "put 1  character from your stage in your waiting room]" in t1.lower() or "put a  character from your stage in your waiting room]" in t1.lower():
				o = ["Waiting", 1, "WTrait", trait[0]]
			elif "put a  character from your memory in your waiting room]" in t1.lower():
				o = ["MDiscard", 1, "MTrait", trait[0]]

		if ("reveal a \"" in t or "reveal 1 \"" in t) and ("\" from your hand &" in t or "\" in your hand &" in t):
			e = ["Reveal", self.name(a, s='n', p=True)]

		if "put all your stock in the waiting room &" in t:
			r = ["Stock", -1]
		elif "put the top card of your deck in your clock &" in t or "put the top card of your deck in your clock," in t:
			r = ["ClockL", 1]
		elif "put 1 marker from under this in the waiting room &" in t:
			r = ["Marker", 1]
		elif "put 2 cards from your hand in your waiting room &" in t or "discard 2 cards from hand to the waiting room &" in t:
			r = ["Discard", 2, ""]
		elif "put 1 card from your hand in your waiting room &" in t or "discard 1 card from your hand to the waiting room &" in t or "discard 1 card from your hand to waiting room &" in t or "discard 1 card from hand to the waiting room &" in t or "put 1 card from your hand to your waiting room &" in t:
			r = ["Discard", 1, ""]
		elif "put 1 climax from your hand in your waiting room &" in t or "put 1 climax card from hand to the waiting room &" in t:
			r = ["Discard", 1, "Climax"]
		elif "put 1 card from your hand in your clock &" in t:
			r = ["ClockH", 1, ""]
		elif "put 1 character with \"" in t and "\" in its card name from your stage in your clock &" in t:
			r = ["ClockS", 1, "Name", self.name(a, s="n", p=True)]
		elif ("put 1 \"" in t or "put 1 character with \"" in t) and ("\" from your hand in your waiting room &" in t or "\" in its card name from your hand in your waiting room &" in t):
			r = ["Discard", 1, "Name", self.name(a, s="n", p=True)]
		elif "choose 1 \"" in t and "\" in hand and put it in memory &" in t:
			r = ["HMemory", 1, "Name=", self.name(a, s="n", p=True)]
		elif ("discard 2 characters with «" in t or "put 2 «" in t) and ("» and/or «" in t or "» or «" in t) and ("from your hand to the waiting room &" in t or "characters from your hand in your waiting room &" in t):
			r = ["Discard", 2, "Trait", f"{self.trait(a)}_{self.trait(a, 1)}"]
		elif ("discard 2 characters with «" in t or "put 2 «" in t) and ("from your hand to the waiting room &" in t or "characters from your hand in your waiting room &" in t):
			r = ["Discard", 2, "Trait", self.trait(a)]
		elif "put 1 «" in t and ("» character from your hand in your waiting room &" in t or "» character card from your hand to the waiting room &" in t):
			r = ["Discard", 1, "Trait", self.trait(a)]
		elif "put 1 of your other characters on the stage in the waiting room &" in t or "put 1 other character from your stage in your waiting room &" in t:
			r = ["Waiting", 1, "WOther"]
		elif "rest 2 of your characters &" in t:
			r = ["Rest", 2, ""]
		elif "rest 1 of your characters &" in t:
			r = ["Rest", 1, ""]
		elif "rest 2 of your other characters with «" in t and "» or «" in t and "» &" in t:
			r = ["Rest", 2, "Trait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}", "Other"]

		if "] accelerate [" in a.lower():
			s.insert(0, "Accelerate")
		return s + e + r + o

	def req(self, a="", x=0, m=0, ss=(), nn=0, h=(), my=(), wr=(), cx=()):
		"""
		:param wr:
		:param cx:
		:param a: ability (string)
		:param x: stock qty (int)
		:param ss: stand character owned (list)
		:param h: cards in hand (list)
		:param nn: cards indices on stage (int)
		:param m: marker under card
		:param my: cards in memory (list)
		:return:
		"""
		self.cond = [0, 0, 0, 0, 0, 0]
		if ss is None:
			ss = []
		t = str(a)
		for _, value in self.set_only.items():
			t = t.replace(f"{_}", f"{value}")

		for item, value in self.status.items():
			t = t.replace(item, value)

		for item1 in self.remove_text:
			t = t.replace(item1, "")

		for item1 in self.ability:
			t = t.replace(item1, "")

		t = t.lower()
		for rep, value in self.resource.items():
			t = t.replace(rep, value)

		if "[auto] encore [(3)]" in t or "[auto] encore" in t:
			t = t.replace("[auto] encore [(3)]", "").replace("[auto] encore", "")

		if "{" in t or "}" in t:
			t = t.replace("{", "(").replace("}", ")")

		if "\"[" in t or "\" [" in t:
			if "\"[" in t:
				t = t.split("\"[")[0]
			elif "\" [" in t and "bond" not in t:
				t = t.split("\" [")[0]
		rs = True
		re = False
		rr = False
		ro = False

		for condition, value in self.pay_stock:
			if condition in t and x < value:
				rs = False
				break

		if "exchange a stand character in your center stage and this]" in t:
			if len([sx for sx in ss[:3] if sx[0] == "Stand" and sx[4] != "" and sx != ss[nn]]) >= 1:
				ro = True
		elif "choose 1 \"" in t and "\" in your waiting room and put it face-down as marker under a \"" in t and "\" that had no markers]" in t:
			if len([sx for sx in wr if self.name(a, s='n', p=True) in sx[1]]) >= 1 and len([sx for sx in ss if self.name(a, 2, s='n', p=True) in sx[1] and sx[4] <= 0]) >= 1:
				ro = True
		elif "put this face-down under an \"" in t and "\" with no markers]" in t:
			if len([sx for sx in ss if self.name(a, s='n', p=True) in sx[1] and sx[4] <= 0]) >= 1:
				ro = True
		elif "turn this face-up card face-down]" in t:
			if len(my) > 1 and any(h[3] and h[4] for hn in my):
				ro = True
		elif ("reveal a \"" in t or "reveal 1 \"" in t or "reveal 1 character with \"" in t) and ("\" from your hand]" in t or "\" in your hand]" in t or "\" in your hand and put it in your stock]" in t or "\" from your hand to your opponent]" in t or "\" from hand]" in t or "\" from your hand and put it face-down under this as marker]" in t or "\" in name in your hand]" in t):
			if len(h) >= 1:
				if self.play(t) and "Name" in self.play(t) and any(self.name(a, 2, s='n', p=True) in hn[1] for hn in h):
					ro = True
				elif any(self.name(a, s='n', p=True) in hn[1] for hn in h):
					ro = True
		elif "reveal any number of \"" in t and ("\" from your hand]" in t or "\" in your hand]" in t):
			if len(h) >= 0:
				ro = True
		elif "put this stand card in your memory]" in t or "send this standing card to memory]" in t:
			if nn > -1 and ss[nn][0] == "Stand":
				ro = True
		elif "put this in your memory]" in t or "send this to memory]" in t:
			ro = True
		elif "put this from your hand in your waiting room]" in t or "discard this from your hand to the waiting room]" in t or "discard this from hand to the waiting room]" in t:
			ro = True
		elif "put 1 card from your hand in clock]" in t or "put 1 card from your hand in your clock" in t or "put 1 card from hand in clock]" in t or "put 1 card from hand in your clock]" in t:
			if len(h) >= 1:
				ro = True
		elif "put 1 \"" in t and "\" from hand in clock]" in t:
			if len(h) >= 1 and any(self.name(a, s='n', p=True) in hn[1] for hn in h):
				ro = True
		elif "put 1 \"" in t and ("\" from your hand to the waiting room]" in t or "\" from your hand in your waiting room]" in t or "\" from hand to the waiting room]" in t or "\" from your hand in your waiting room]" in t):
			if "\" or \"" in t.split("waiting room]")[0]:
				if len(h) >= 1 and any(self.name(a, s='n', p=True) in hn[1] or self.name(a, 2, s='n', p=True) in hn[1] for hn in h):
					ro = True
			else:
				if len(h) >= 1 and any(self.name(a, s='n', p=True) in hn[1] for hn in h):
					ro = True
		elif "put 1 character card with \"" in t and "\" in name from your hand to the waiting room]" in t:
			if len(h) >= 1 and any(self.name(a, s='n', p=True) in hn[1] and "Character" in hn[0] for hn in h):
				ro = True
		elif "put 1 \"" in t and ("\" from your memory to your waiting room]" in t or "\" from your memory to the waiting room]" in t or "from your memory in the waiting room]" in t):
			if len(my) >= 1 and any(self.name(a, s='n', p=True) in hn[1] for hn in my):
				ro = True
		elif "put 1 character with \"" in t and "in name from your memory in the waiting room]" in t:
			if len(my) >= 1 and any(self.name(a, s='n', p=True) in hn[1] and "Character" in hn[0] for hn in my):
				ro = True
		elif "put 1 \"" in t and ("from your climax area in your waiting room]" in t or "from your climax area to the waiting room]" in t or "from your climax area in the waiting room]" in t):
			if "\" from your hand in your waiting room &" in t:
				if len(cx) >= 1 and any(self.name(a, 2, s='n', p=True) in hn[0] for hn in cx):
					ro = True
			else:
				if len(cx) >= 1 and self.name(a, s='n', p=True) in cx[0]:
					ro = True
		elif "put 3 cards from your hand in your waiting room]" in t:
			if len(h) >= 3:
				ro = True
		elif "discard 2 cards from your hand to the waiting room]" in t or "put 2 cards from your hand in your waiting room]" in t or "discard 2 cards from hand to the waiting room]" in t:
			if len(h) >= 2:
				ro = True
		elif "discard 1 card from your hand to the waiting room]" in t or "put 1 card from your hand in your waiting room]" in t or "discard 1 card from hand to the waiting room]" in t:
			if len(h) >= 1:
				ro = True
		elif "discard a character card from your hand to the waiting room]" in t or "put 1 character from your hand in your waiting room]" in t or "discard 1 character card from hand to the waiting room]" in t:
			if len([p for p in h if p[0] == "Character"]) >= 1:
				ro = True
		elif "put 1 character card from hand in memory]" in t:
			if len([p for p in h if p[0] == "Character"]) >= 1:
				ro = True
		elif "put this in your memory]" in t:
			ro = True
		elif "choose 1 \"" in t and "\" on your stage and put it in stock]" in t:
			if len([sx for sx in ss if self.name(a, self.cond[1], s='n', p=True) in sx[1]]) > 0:
				ro = True
		elif "put 1 of your characters in the waiting room]" in t or "put 1 character from the stage to the waiting room]" in t or "put 1 character from your stage in the waiting room]" in t or "put 1 character from your stage in your waiting room]" in t:
			if len([sx for sx in ss if sx[0] != ""]) > 0:
				ro = True
		elif "put 1 of your other characters from the stage in the waiting room]" in t or "choose 1 of your other characters on the stage and put it in the waiting room]" in t or "put 1 other character from your stage in your waiting room]" in t:
			if len([sx for sx in ss if sx[0] != "" and sx != ss[nn]]) > 1:
				ro = True
		elif "choose 1 of your other center stage characters and put it in the waiting room]" in t:
			if len([sx for sx in ss if sx[0] != "" and sx != ss[nn] and ss.index(sx) < 3]) > 1:
				ro = True
		elif "put this in your waiting room]" in t or "put this in waiting room]" in t or "put this in the waiting room]" in t:
			ro = True
		elif "return this to your hand]" in t:
			ro = True
		elif "put this in your clock]" in t:
			ro = True
		elif "put this in your waiting room]" in t or "put this in the waiting room]" in t:
			ro = True
		elif "put 1 random card from your hand in your waiting room]" in t:
			if len(h) >= 1:
				ro = True
		elif "put 1 climax card with a gate trigger icon from hand to the waiting room]" in t:
			if len([p for p in h if p[0] == "Climax" and "gate" in p[4]]) >= 1:
				ro = True
		elif "put 1 climax with [treasure] in its trigger icon from your hand in your waiting room]" in t:
			if len([p for p in h if p[0] == "Climax" and "treasure" in p[4]]) >= 1:
				ro = True
		elif "put 1 climax from your hand in your waiting room]" in t or "put 1 climax card from hand to the waiting room]" in t or "put 1 climax card from your hand to the waiting room]" in t:
			if len([p for p in h if p[0] == "Climax"]) >= 1:
				ro = True
		elif "put 1 climax from your waiting room in your memory]" in t:
			if len([p for p in wr if p[0] == "Climax"]) >= 1:
				ro = True
		elif "put 1 blue climax from your hand in your waiting room]" in t:
			if len([p for p in h if p[0] == "Climax" and "blue" in p[3]]) >= 1:
				ro = True
		elif "rest 1 of your characters with assist]" in t:
			if len([sx for sx in ss if sx[0] == "Stand" and sx[3]]) >= 1:
				ro = True
		elif "rest 1 of your standing characters]" in t or "rest 1 of your stand characters]" in t or "rest 1 of your characters]" in t:
			if len([sx for sx in ss if sx[0] == "Stand"]) >= 1:
				ro = True
		elif "rest 2 of your standing characters]" in t or "rest 2 of your stand characters]" in t or "rest 2 of your characters]" in t or "rest 2 characters]" in t:
			if len([sx for sx in ss if sx[0] == "Stand"]) >= 2:
				ro = True
		elif "rest 3 of your characters]" in t:
			if len([sx for sx in ss if sx[0] == "Stand"]) >= 3:
				ro = True
		elif "rest 2 of your other characters]" in t:
			if len([sx for sx in ss if sx[0] == "Stand" and sx != ss[nn]]) >= 2:
				ro = True
		elif "rest this]" in t:
			if nn > -1 and ss[nn][0] == "Stand":
				ro = True
		elif "put the top card of your deck in your clock]" in t or "put 1 card from the top of your deck in your clock]" in t or "put the top card of your deck to clock]" in t:
			ro = True
		elif "put 1 character with \"" in t and "\" in its card name from your stage in your clock]" in t:
			if len([sx for sx in ss if sx[0] != "" and self.name(a, s='n', p=True) in sx[1]]) >= 1:
				ro = True
		elif "put 1 card named \"" in t and "\" from your hand in your waiting room]" in t:
			if len(h) >= 1 and any(self.name(a, s='n', p=True) in hn[1] for hn in h):
				ro = True
		elif "rest 1 of your characters with \"" in t and ("\" in name]" in t or "\" in the name]" in t):
			if len([sx for sx in ss if sx[0] == "Stand" and self.name(a, s="n") in sx[1]]) >= 1:
				ro = True
		elif "put 2 markers from under this in your waiting room]" in t:
			if m >= 2:
				ro = True
		elif "put 1 marker from under this in the waiting room]" in t:
			if m >= 1:
				ro = True
		elif any(_ in t for _ in ("return 2 characters from your waiting room to your deck. shuffle your deck afterwards]", "return 2 characters in your waiting room to your deck. shuffle your deck afterwards]", "return 2 characters from your waiting room in your deck & shuffle your deck]", "return 2 character cards from your waiting room to your deck, shuffle your deck]", "return 2 characters from your waiting room to your deck & shuffle your deck]", "return 2 characters in your waiting room to your deck, and shuffle your deck]")):
			if len([sx for sx in wr if sx[0] == "Character"]) >= 2:
				ro = True
		elif "«" in t:
			t1 = str(a)
			for item in self.status:
				t1 = t1.replace(item, self.status[item])
			for item in self.ability:
				t1 = t1.replace(item, "")
			t1 = t1.split("]")[0]

			trait = []
			for nx in range(t1.count("«")):
				trait.append(t1.split("«")[nx + 1].split("»")[0])
			for tra in trait:
				t1 = t1.replace(tra, "").replace("«", "").replace("»", "")

			for rep in self.resource:
				t1 = t1.replace(rep, self.resource[rep])
			if "rest 1 of your  characters and 1 of your  characters]" in t1.lower():
				sn = {"0": [sx for sx in ss if sx[0] == "Stand" and any(tx in sx[2] for tx in trait)], "1": [], "2": []}
				for sx in sn["0"]:
					if trait[0] in sx[2]:
						sn["1"].append(sx)
					if trait[1] in sx[2]:
						sn["2"].append(sx)
				if len(sn["1"]) >= 1 and len(sn["2"]) >= 1 and len(sn["0"]) >= 2:
					ro = True
			elif "rest 1 of your  characters]" in t1.lower() or "rest 1 of your stand  characters]" in t1.lower():
				if len([sx for sx in ss if sx[0] == "Stand" and any(tx in sx[2] for tx in trait)]) >= 1:
					ro = True
			elif "rest 2 of your  characters]" in t1.lower() or "rest 2 of your characters with  or ]" in t1.lower():
				if len([sx for sx in ss if sx[0] == "Stand" and any(tx in sx[2] for tx in trait)]) >= 2:
					ro = True
			elif "rest another of your stand characters with  or ]" in t1.lower() or "rest 1 of your other stand  or  characters]" in t1.lower():
				if nn > -1 and len([sx for sx in ss if sx != ss[nn] and sx[0] == "Stand" and any(tx in sx[2] for tx in trait)]) >= 1:
					ro = True
			elif "rest 1 of your characters with  or ]" in t1.lower():
				if len([sx for sx in ss if sx[0] == "Stand" and any(tx in sx[2] for tx in trait)]) >= 1:
					ro = True
			elif "rest 1 of your other  characters]" in t1.lower() or "rest 1 of your other stand  characters]" in t1.lower() or "rest another of your standing  character]" in t1.lower():
				if nn > -1 and len([sx for sx in ss if sx != ss[nn] and sx[0] == "Stand" and any(tx in sx[2] for tx in trait)]) >= 1:
					ro = True
			elif "return 2 characters with  and/or  from your waiting room to your deck]" in t1.lower() or "choose 2  characters in the waiting room and return them to the deck]" in t1.lower() or "return 2  or  characters from your waiting room to your deck & shuffle your deck]" in t1.lower():
				if len([sx for sx in wr if sx[0] == "Character" and any(tx in sx[2] for tx in trait)]) >= 2:
					ro = True
			elif "put a  or  or  character from your hand in your waiting room]" in t1.lower():
				if len(h) >= 1 and len([p for p in h if any(tx in p[2] for tx in trait)]) >= 1:
					ro = True
			elif "discard a  or  character from hand to the waiting room]" in t1.lower() or "discard a character card with either  or  from your hand to the waiting room]" in t1.lower() or "put 1  or  character from your hand in your waiting room]" in t1.lower():
				if len(h) >= 1 and len([p for p in h if any(tx in p[2] for tx in trait)]) >= 1:
					ro = True
			elif "put a  character from your hand in your waiting room]" in t1.lower() or "discard a  character card from your hand to the waiting room]" in t1.lower() or "discard a  character from hand to the waiting room]" in t1.lower() or "put 1  character from your hand in your waiting room]" in t1.lower():
				if len(h) >= 1 and len([p for p in h if any(tx in p[2] for tx in trait)]) >= 1:
					ro = True
			elif "put 2  characters from your hand in your waiting room]" in t1.lower():
				if len(h) >= 2 and len([p for p in h if any(tx in p[2] for tx in trait)]) >= 2:
					ro = True
			elif "put 3  characters from your hand in your waiting room]" in t1.lower():
				if len(h) >= 3 and len([p for p in h if any(tx in p[2] for tx in trait)]) >= 3:
					ro = True
			elif any(f"discard a {cl} or  character card from your hand to the waiting room]" in t1.lower() for cl in self.colour):
				if len(h) >= 1 and len([p for p in h if any(tx in p[2] for tx in trait) or self.colour_t(t1, p=True) in p[3]]) >= 1:
					ro = True
			elif "put a  character card from your hand in clock]" in t1.lower() or "put 1  character from your hand in your clock]" in t1.lower():
				if len(h) >= 1 and len([p for p in h if any(tx in p[2] for tx in trait)]) >= 1:
					ro = True
			elif "put 1  or  character on your stage in your clock]" in t1.lower():
				if len([sx for sx in ss if any(tx in sx[2] for tx in trait)]) >= 1:
					ro = True
			elif "put a  character from your stage in your clock]" in t1.lower():
				if len([sx for sx in ss if any(tx in sx[2] for tx in trait)]) >= 1:
					ro = True
			elif "put a  character from your waiting room on the bottom of the clock]" in t1.lower() or "put 1  character from your waiting room at the bottom of your clock]" in t1.lower():
				if len([sx for sx in wr if any(tx in sx[2] for tx in trait)]) >= 1:
					ro = True
			elif "put 1 of your other  characters from stage in the waiting room" in t1.lower():
				if nn > -1 and len([sx for sx in ss if any(tx in sx[2] for tx in trait) and sx != ss[nn]]) >= 1:
					ro = True
			elif "put 1  character from your stage in your waiting room]" in t1.lower() or "put a  character from your stage in your waiting room]" in t1.lower():
				if len([sx for sx in ss if any(tx in sx[2] for tx in trait)]) >= 1:
					ro = True
			elif "put a  character from your memory in your waiting room]" in t1.lower():
				if len([sx for sx in my if any(tx in sx[2] for tx in trait)]) >= 1:
					ro = True
			elif "[(" in t:
				ro = True
			elif t1.count("[") == 0:
				ro = True
		elif t.count("[") >= 2 and ")]" in t:
			ro = True
		elif t.count("[") == 2:
			for item in self.ability:
				t = t.replace(item.lower(), "")
			if t.count("[") == 0:
				ro = True
		elif t.count("[") == 1:
			ro = True
		elif t.count("[") == 0:
			ro = True

		if ("reveal a \"" in t or "reveal 1 \"" in t) and ("\" from your hand &" in t or "\" in your hand &" in t):
			if len(h) >= 1 and any(self.name(a, s='n', p=True) in hn[1] for hn in h):
				re = True
		else:
			re = True

		if "put all your stock in the waiting room &" in t:
			rr = True
		elif "put 2 cards from your hand in your waiting room &" in t or "discard 2 cards from hand to the waiting room &" in t:
			if len(h) >= 2:
				rr = True
		elif "put 1 card from your hand in your waiting room &" in t or "discard 1 card from your hand to waiting room &" in t or "put 1 card from your hand to your waiting room &" in t or "discard 1 card from your hand to the waiting room &" in t:
			if len(h) >= 1:
				rr = True
		elif "put 1 climax from your hand in your waiting room &" in t or "put 1 climax card from hand to the waiting room &" in t:
			if len([p for p in h if p[0] == "Climax"]) >= 1:
				rr = True
		elif "put 1 marker from under this in the waiting room &" in t:
			if m >= 1:
				rr = True
		elif "put the top card of your deck in your clock &" in t:
			rr = True
		elif "put 1 card from your hand in your clock &" in t:
			if len(h) >= 1:
				rr = True
		elif "put 1 character with \"" in t and "\" in its card name from your stage in your clock &" in t:
			if len([sx for sx in ss if sx[0] != "" and self.name(a, s='n', p=True) in sx[1]]) >= 1:
				rr = True
		elif ("put 1 \"" in t or "put 1 character with \"" in t) and ("\" from your hand in your waiting room &" in t or "\" in its card name from your hand in your waiting room &" in t):
			if len([sx for sx in h if sx[0] != "" and self.name(a, s='n', p=True) in sx[1]]) >= 1:
				rr = True
		elif "choose 1 \"" in t and "\" in hand and put it in memory &" in t:
			if len([sx for sx in h if sx[0] != "" and self.name(a, s='n', p=True) in sx[1]]) >= 1:
				rr = True
		elif ("discard 2 characters with «" in t or "put 2 «" in t) and ("» and/or «" in t or "» or «" in t) and ("from your hand to the waiting room &" in t or "characters from your hand in your waiting room &" in t):
			if len(h) >= 2 and len([p for p in h if any(tx in p[2] for tx in (self.trait(a), self.trait(a, 1)))]) >= 1:
				rr = True
		elif ("discard 2 characters with «" in t or "put 2 «" in t) and ("from your hand to the waiting room &" in t or "characters from your hand in your waiting room &" in t):
			if len(h) >= 2 and len([p for p in h if self.trait(a) in p[2]]) >= 2:
				rr = True
		elif "put 1 «" in t and ("» character from your hand in your waiting room &" in t or "» character card from your hand to the waiting room &" in t):
			if len(h) >= 1 and len([p for p in h if self.trait(a) in p[2]]) >= 1:
				rr = True
		elif "put 1 of your other characters on the stage in the waiting room &" in t or "put 1 other character from your stage in your waiting room &" in t:
			if len([sx for sx in ss if sx[0] != "" and sx != ss[nn]]) > 0:
				rr = True
		elif "rest 2 of your characters &" in t:
			if len([sx for sx in ss if sx[0] == "Stand"]) >= 2:
				rr = True
		elif "rest 1 of your characters &" in t:
			if len([sx for sx in ss if sx[0] == "Stand"]) >= 1:
				rr = True
		elif "rest 2 of your other characters with «" in t and "» or «" in t and "» &" in t:
			if len([sx for sx in ss if sx[0] == "Stand" and sx != ss[nn] and (self.trait(a, self.cond[2]) in sx[2] or self.trait(a, self.cond[2] + 1) in sx[2])]) >= 2:
				rr = True
		elif "&" not in t.replace("[act]", "").replace("[auto]", "").split("]")[0]:
			rr = True

		if rs and ro and rr and re:
			return True
		else:
			return False

	def act(self, a=""):
		t = self.text(a)
		aa = self.a_replace(a)

		self.opnextturn = False
		self.ablt = 0
		self.target = ""
		self.cx = False
		self.center = False
		pay = self.pay(a)
		if pay:
			if "Trait" in pay:
				self.cond[2] += len(pay[pay.index("Trait") + 1].split("_"))
			elif "BTrait" in pay:
				self.cond[2] += len(pay[pay.index("BTrait") + 1].split("_"))
			elif "CColourT" in pay:
				self.cond[2] += len(pay[pay.index("CColourT") + 1].split("_"))

		if t.startswith("backup"):
			return [1, self.digit(a, self.cond[0]), 1, "backup", self.digit(a, self.cond[0] + 1)]
		elif "return a marker from under this to your hand" in t:
			return [1, "marker", "Return", "Hand"]
		else:
			self.ablt = 8

		if self.ablt:
			return self.effect(a, t, aa, self.ablt)
		else:
			return []

	def event(self, a=""):
		t = self.text(a)
		self.opnextturn = False
		if "next end of your opponent's turn" in t:
			x = 2
		elif "for the turn" in t or "until end of turn" in t:
			x = 1
		else:
			x = 1

		self.ablt = 0
		self.target = ""
		self.cx = False
		self.center = False
		self.cond = [0, 0, 0, 0, 0, 0]
		_, t = self.limit(t, a)
		self.play(a, t)

		self.ablt = 7
		e = []
		d = []
		ee = ""

		if "if there are no face down cards in your opponent's memory" in t:
			if "your opponent chooses  card from your opponent's hand" in t and "puts it face down in his or her memory" in t:
				tt = "puts it face down in his or her memory, and draws up to  card.\n"
				t1 = f"{t.split(tt)[0]}{tt}"
				t = t.split(tt)[1]
				d = self.effect(a, t1, "", self.ablt)
		elif t.count("if the number of cards named  in your memory is  or more") > 1:
			tt = "if the number of cards named  in your memory is  or more"
			if not t.startswith(tt):
				d = self.effect(a, t.split(tt)[0], "", self.ablt)
				t = f"{tt}{tt.join(t.split(tt)[1:])}"
				for _ in range(t.count(tt)):
					e.append(self.effect(a, f"{tt}{t.split(tt)[_ + 1]}", "", self.ablt))
				return d + ["done", transform_list(e, "done")]
		elif a.lower().startswith("[counter]"):
			self.ablt = 4
			if t.count("choose  of your characters with  in the name") == 2 and t.count("that character gets + power") == 2:
				return [self.digit(a), self.digit(a, 1), x, "power", "Name", self.name(a, s='n'), "do", [self.digit(a, 2), self.digit(a, 3), x, "power", "Name", self.name(a, 2, s='n')]]
			elif t.count("choose  of your character") == 2:
				if "if you have  or more climax" in t:
					tt = "if you have  or more climax"
					t1 = t.split(tt)[0]
					t2 = f"{tt}{t.split(tt)[1]}"
				else:
					t2 = f'choose  of your character{t.replace("choose  of your character", "", 1).split("choose  of your character")[1]}'
					t1 = t.replace(t2, "")
				ab = self.effect(a, t1, "", self.ablt)
				ab.extend(["do", self.effect(a, t2, "", self.ablt)])
				return ab
			elif "your opponent may choose  of your character" in t and "choose  of your opponent's character" in t:
				tt = "your opponent may choose  of your character"
				ts = "choose  of your opponent's character"
				if t.index(tt) < t.index(ts):
					t1 = t.split(ts)[0]
					t = f"{ts}{t.split(ts)[1]}"
					d = self.effect(a, t1, "", self.ablt)
			elif "choose  of your opponent's climax in your opponent's climax area" in t or "choose  of your opponent's climax in the climax area" in t:
				if "put it in his or her waiting room" in t:
					return [self.digit(a), "waitinger", "Climax", "Opp"]
		elif "repeat the following action until you level up" in t:
			d = ["perform", 1, self.name(a, self.cond[1], s='p'), "unli", "xlvlup"]
			self.cond[1] += 2
			t = t.split("repeat the following action until you level up")[1]
		elif "if there are cards in your hand" in t:
			if "randomly reveal  card from your hand" in t:
				if "choose up to x of your characters" in t:
					if "those characters get + power and + soul" in t:
						if "x =  + level of the card revealed this way" in t:
							return [1, "more", "Hand", "do", ["discard", self.digit(a), "", "random", "Reveal", "do", ["x", self.digit(a, 1), x, f"xrlevel+{self.digit(a, 3)}", "power", "extra", "upto", "do", [-16, self.digit(a, 2), x, "soul"]]]]
				elif "choose  level x or lower character in your waiting room" in t:
					if "return it to your hand" in t:
						if "x =  + level of revealed card" in t:
							return [1, "more", "Hand", "do", ["discard", self.digit(a), "", "random", "Reveal", "do", [self.digit(a, 1), "salvage", f"CLevel_<=x", f"xrlevel+{self.digit(a, 1)}", "show"]]]
				elif "all your characters get +x power" in t:
					if "x = level times  of the revealed card" in t:
						return [1, "more", "Hand", "do", ["discard", self.digit(a), "", "random", "Reveal", "do", [-1, "x", x, "power", "xrlevel", self.digit(a, 1)]]]
				elif "draw x card" in t:
					if "x =  + level of revealed card" in t:
						return [1, "more", "Hand", "do", ["discard", self.digit(a), "", "random", "Reveal", "do", ["draw", "x", f"xrlevel+{self.digit(a, 1)}"]]]
		elif "you may choose  card in your clock, and put it in your level" in t:
			tt = "you may choose  card in your clock, and put it in your level"
			ts = "choose up to  character"
			if t.index(tt) < t.index(ts):
				e = ["cdiscard", self.digit(a, self.cond[0]), "", "Level", "upto", "if", self.digit(a, self.cond[0])]
				self.cond[0] += 1
				t = f"{ts}{t.split(ts)[1]}"
		elif "choose  of your stand  character" in t or "choose  of your standing  character" in t:
			if "rest it" in t or "rest them" in t:
				if "choose  of your opponent's level  or lower characters on the center stage" in t or "choose  level  or lower character in your opponent's center stage" in t:
					if "put it on the bottom of your opponent's deck" in t or "put it on the bottom of the deck" in t:
						return [self.digit(a), "rest", "Stand", "Trait", self.trait(a), "if", self.digit(a), "do", [self.digit(a, 1), "decker", "bottom", "Level", f"<={self.digit(a, 2)}", "Opp", "Center"]]
				elif "deal x damage to your opponent" in t:
					if "x = level of your highest level character" in t:
						return [self.digit(a), "rest", "Stand", "Trait", self.trait(a), "if", self.digit(a), "do", ["damage", "x", "opp", "xlvlhigh"]]
				elif "draw up to  card" in t:
					if "discard  card from your hand to the waiting room" in t or "discard  card from your hand to your waiting room" in t:
						return [self.digit(a), "rest", "Stand", "Trait", self.trait(a), "if", self.digit(a), "do", ["drawupto", self.digit(a, 1), "do", ["discard", self.digit(a, 2), ""]]]
		elif "choose  of your level  or higher characters and put it in the waiting room" in t:
			if "choose  level  or lower  character in your waiting room" in t:
				if "put it in any slot on the stage" in t:
					if "choose up to  character in your waiting room" in t:
						if "return them to your hand" in t:
							return [self.digit(a), "waitinger", "Level", f">={self.digit(a, 1)}", "if", self.digit(a), "do", [self.digit(a, 2), "salvage", f"TraitL_{self.trait(a)}_<={self.digit(a, 3)}", "Stage", "do", [self.digit(a, 4), "salvage", "Character", "upto", "show"]]]
		elif "put the top  cards of your deck face down in your memory" in t:
			if "your opponent looks at those cards and separates them into stacks of  cards and  cards" in t:
				if "choose  face down stack from among them" in t:
					if "put them in your hand" in t:
						if "return the rest in your deck" in t:
							return ["mill", self.digit(a), "top-down", "Memory", "extra", "if", self.digit(a), "do", [-16, "looktopopp", "stack", (self.digit(a, 1), self.digit(a, 2)), "fix", "extra", "do", [-16, "looktop", "hand", self.digit(a, 3), "stacked", "fix", "deck"]]]
		elif "choose  character in your clock whose level = or lower than your level" in t:
			if "put it in any slot on the stage" in t:
				if "you cannot play this from your hand" in t:
					return ["cdiscard", self.digit(a, 1), "CLevel_<=p", "Stage"]
		elif "choose   character in your hand" in t:
			if "put them in your waiting room" in t or "from your hand to the waiting room" in t or "put it in the waiting room" in t:
				if "draw up to  cards" in t:
					if "send this to memory" in t:
						return ["discard", self.digit(a), f"Trait_{self.trait(a)}", "if", self.digit(a), "do", ["drawupto", self.digit(a, 1), "do", [0, "memorier"]]]
		elif "return all your opponent's level  or lower characters to the deck, and your opponent shuffles that deck" in t:
			if "put this in your clock" in t:
				return [-1, "decker", "Level", f"<={self.digit(a)}", "Opp", "do", [0, "clocker"]]
		elif "choose  of your character" in t:
			tt = "choose  of your character"
			ts = "return it to your hand"
			if ts in t and t.index(tt) < 10 and t.index(ts) < len(tt) + 10:
				e = [self.digit(a, self.cond[0]), "hander"]
				self.cond[0] += 1
				if "if so" in t:
					e.extend(["if", e[0]])
					t = t.split("if so")[1]
		elif "declare any number" in t and "\nsearch your deck for up to" in t:
			tt = "declare any number"
			ts = "\nsearch your deck for up to"
			if t.index(tt) < t.index(ts):
				d = self.effect(a, t.split(ts)[0], "", self.ablt)
				t = f"{ts}{t.split(ts)[1]}"

		if "you may discard  cards from your hand to the waiting room" in t or "you may discard  card from hand to the waiting room" in t:
			if "you may discard  cards from your hand to the waiting room" in t:
				t = t.split("you may discard  cards from your hand to the waiting room")[1]
			elif "you may discard  card from hand to the waiting room" in t:
				t = t.split("you may discard  card from hand to the waiting room")[1]
			e = ["discard", self.digit(a, self.cond[0]), "", "upto"]
			e.extend(["if", e[1]])
			self.cond[0] += 1
		elif "\nif your opponent does not have any stand character" in t or "\nif your opponent has no stand character" in t:
			if "\nif your opponent has no stand character" in t:
				ts = "\nif your opponent has no stand character"
			elif "\nif your opponent does not have any stand character" in t:
				ts = "\nif your opponent does not have any stand character"
			d = self.effect(a, t.split(ts)[0], "", self.ablt)
			t = f"{ts}{t.split(ts)[1]}"

		if self.ablt:
			ab = self.effect(a, t, "", self.ablt)
			if "perform" in ab and "do" in ab:
				ab[ab.index("do")] = "done"
			if e:
				e.extend(["do", ab])
				return e
			elif d:
				d.extend(["done", ab])
				return d
			else:
				return ab
		else:
			return []

	def auto(self, a="", p="", r=("0", "0", "", ""), v=("", ""), passed=False, lvop=(0, 0), cx=("", "0", ""), text=([], []), pos=("", "", "", ""), n="", begin=(), tr=([], []), z=(0, 0, ""), act="", cnc=("0", False), pp=0, dis=("", ""), nr=("", ""), atk="", dmg=0, nmop=("", ""), rst=None, lvc=("", ""), refr="", sav=("", ""), brt=("", []), lr=(0, 0), lvup="", baind=("0", "0"), csop=(0, 0), suop=("", ""), trop=([], []), ty=("", [], "", ""), std=("", "", ""), opp="", chg="", accel=""):
		"""
		:param opp:
		:param lvup:
		:param lr:
		:param brt:
		:param sav:
		:param refr:
		:param lvc:
		:param rst:
		:param text:
		:param dmg: damage received/dealt
		:param a: ability (string)
		:param p: phase (string)
		:param r: active card  _ triggering effect card _ triggering effect card type(list)
		:param v: status of both cards (list)
		:param ty: triggering effect card type,trigger (list)
		:param lvop: level of both cards (list)
		:param trop: trait of both cards (list)
		:param cx: climax name _ climax id (list)
		:param pos: position of both cards (list)
		:param n: turn player (int)
		:param begin: list of card at the beginning of turn on stage (list)
		:param tr: trait active card  _ triggering effect card (list)
		:param nr: name active card  _ triggering effect card (list)
		:param z: active card turn played _ actual turn _ played from _ ability turn (list)
		:param act: card who used act (str)
		:param chg: card who used change (str)
		:param atk: atk type (str)
		:param cnc: Damage dealt by attacking character is cancelled (boolean)
		:param pp: Beginning, Actual, End of the phase (-1,0,1) (int)
		:param dis:
		:param std: standby or played card form another ability (card that trigger the ability, name of card that triggered the ability,card played by ability)
		:param baind: attacking_batteling opp (list)
		:param lvop: card and batteling opp level(list)
		:param csop: card and batteling opp cost(list)
		:param suop: card and batteling opp status(list)
		:param nmop: card and batteling opp name(list)
		:param passed: check if ability is not finished and come form passed ability
		:return:
		"""
		if rst is None:
			rst = []
		t = self.text(a)
		aa = self.a_replace(a)
		self.opnextturn = False
		if "until the next end of your opponent's turn" in t or "until the end of your opponent's next turn" in t or "until end of your opponent's next turn" in t or "until end of your opponent's next turn" in t or "until the end of the next turn" in t:
			x = 2
			if r[0][-1] != n:
				self.opnextturn = True
				x += 1
		elif "for the turn" in t or " until end of turn" in t:
			x = 1
		else:
			x = 1

		self.xx = None
		self.ablt = 0
		self.target = ""
		self.aselected = ""
		self.cx = False
		self.center = False
		self.cond_rep = [False, []]
		pay = self.pay(a)
		if pay:
			if "Trait" in pay:
				self.cond[2] += len(pay[pay.index("Trait") + 1].split("_"))
			elif "BTrait" in pay:
				self.cond[2] += len(pay[pay.index("BTrait") + 1].split("_"))
			elif "CColourT" in pay:
				self.cond[2] += len(pay[pay.index("CColourT") + 1].split("_"))
			if "Reveal" in pay:
				self.cond[1] += 2

		if r[1] == "":
			r = (r[0], "0")
		if dis[0]:
			if "when  of your characters is put in your waiting room from your hand" in t:
				if r[0] != dis[0] and r[0][-1] == dis[0][-1] and "Hand" in pos[2] and "Waiting" in pos[3] and "Character" in dis[1]:
					self.ablt = 9
					self.cond[0] += 1
		elif lvup:
			if "when your opponent levels up" in t or "when your opponent levels-up" in t:
				if lvup not in r[0][-1]:
					self.ablt = 9

					if "\" is in your climax area" in aa:
						self.ablt = 0
						if (f"\"{cx[0].lower()}\" is in your climax area" in aa and r[0][-1] == cx[1][-1] and n in cx[1][-1]) or (f"\"{cx[3].lower()}\" is in your climax area" in aa and r[0][-1] == cx[4][-1] and n not in cx[1][-1]):
							self.ablt = 9
			elif "when you level up" in t or "when you level-up" in t:
				if lvup in r[0][-1]:
					self.ablt = 9
		elif refr:
			if "when you refresh your deck" in t:
				if refr in r[0][-1]:
					self.ablt = 9
		elif sav[0]:
			if "when your character or your opponent's character is returned to hand from the waiting room" in t:
				if "Character" in sav[1]:
					if "during the attack phase" in t and p in self.attack:
						if "all of that player's characters get - soul" in t:
							return [-19, self.digit(a, self.cond[0]), x, "soul", "player", sav[0][-1]]
			elif "when an opponent's character is returned to hand from the waiting room" in t:
				if "Character" in sav[1] and sav[0][-1] != r[0][-1] and sav[0] != r[0]:
					self.ablt = 9
		elif brt[0]:
			if ("when your opponent uses " in t and "when your opponent uses \"brainstorm\"" in aa) or "when your opponent uses brainstorm" in t:
				if brt[0][-1] != r[0][-1] and brt[0] != r[0]:
					if "puts at least  climax card in the waiting room" in t or "if  climax is put into the waiting room by that effect" in t:
						if len([_ for _ in brt[1] if _ == "Climax"]) >= self.digit(a, self.cond[0]):
							self.ablt = 9
						self.cond[0] += 1
		elif accel:
			if "when you use " in t and "when you use \"accelerate\"" in aa:
				if r[0][-1] == r[1][-1] and accel == r[1]:
					self.ablt = 9
		elif "encore [" in t and ("cannot use \"[auto] encore\"" not in aa and "may not use \"[auto] encore\"" not in aa):
			if r[0] == r[1] and any(field in pos[0] for field in self.stage) and "Waiting" in pos[1] and "Waiting" in pos[3]:
				if "[put  character card from your hand to the waiting room]" in t or "[put  character from your hand in your waiting room]" in t:
					return [1, "Character", "may", "encore"]
				elif "[put   character card from your hand to the waiting room]" in t or "[put   character from your hand in your waiting room]" in t:
					return [1, "Trait", self.trait(a, self.cond[2]), "may", "encore"]
				elif "» or «" in aa and ("[put   or   character card from your hand to the waiting room" in t or "[put  character card with  or  from your hand to the waiting room" in t or "[put  character card with either  or  from your hand to the waiting room" in t or "[discard  character card with  or  from your hand to the waiting room" in t or "[put   or  character from your hand to the waiting room" in t or "[put   or  character from your hand in your waiting room" in t):
					return [1, "Trait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}", "may", "encore"]
				elif "[discard  character card with  or  in name from your hand to the waiting room]" in t:
					return [1, "TraitN", f"{self.trait(a)}_{self.name(a, self.cond[1], s='n')}", "may", "encore"]
				elif "[put the top card of your deck in your clock]" in t:
					return [1, "Clock", "may", "encore"]
				elif "[put  climax from your hand in your waiting room]" in t:
					return [1, "Climax", "may", "encore"]
				elif "[() put  character from your stage in your waiting room]" in t:
					if "[(1) put" in aa:
						return [1, "StockWaiting", f"{self.digit(a, self.cond[0])}_Character", "may", "encore"]
				elif "[()]" in t:
					if "[(2)]" in a:
						return [2, "Stock", "may", "encore"]
					elif "[(1)]" in a:
						return [1, "Stock", "may", "encore"]
		elif "bond/" in t:
			if r[0] == r[1] and "Hand" in pos[0]:
				if a.count('"') / 2 == 4:
					_ = [1, "salvage", f"Name=_{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}", "show"]
				else:
					_ = [1, "salvage", f"Name=_{self.name(a, self.cond[1], s='n')}", "show"]
				return ["pay", "may", "played", "do", _]
		elif "when you play an event" in t:
			if r[0][-1] == r[1][-1] and r[0] != r[1] and r[2] == "Event" and "Hand" in pos[2] and v[1] == "Stand":
				self.ablt = 9
		elif "when your opponent plays an event" in t:
			if r[0][-1] != r[1][-1] and r[0] != r[1] and r[2] == "Event" and "Hand" in pos[2] and v[1] == "Stand":
				self.ablt = 9
		elif "when you use an act" in t:
			if act and r[0][-1] == act[-1]:
				self.ablt = 9
		elif "when you use " in t and "when you use \"change\"" in aa:
			if chg and r[0][-1] == chg[-1]:
				self.ablt = 9
		elif ("when this is placed on the stage from your hand or by a  effect" in t or "when this is placed on stage from your hand or by a  effect" in t or "when this is placed from hand to the stage or via " in t) and ("by a \"change\" effect" in aa or "via change to the stage" in t):
			if ("Hand" in pos[0] and r[0] == r[1] and v[0] == "Stand" and any(field in pos[1] for field in self.stage)) or (std[0] and std[2] == r[0] and std[0][-1] == r[1][-1] and std[0] != r[1] and r[0] == r[1] and any(field in pos[1] for field in ("Center", "Back")) and "Waiting" in pos[0] and "Change" in std):
				if "\"change\"" in aa:
					self.cond[1] += 2
				self.ablt = 1
		elif "when this is placed from hand to the stage or via the  effect of" in t or "when this is placed from hand to the stage or via the effect of" in t or "when this is placed on the stage from your hand or by the  effect of" in t:
			if ("Hand" in pos[0] and r[0] == r[1] and v[0] == "Stand" and any(field in pos[1] for field in self.stage)) or (std[0] and std[2] == r[0] and std[0][-1] == r[1][-1] and std[0] != r[1] and r[0] == r[1] and (f"\"{std[1].lower()}\" to the stage" in aa or f"effect of \"{std[1].lower()}\"" in aa) and any(field in pos[1] for field in ("Center", "Back")) and all(field not in pos[0] for field in ("Center", "Back"))):
				self.cond[1] += 2
				self.ablt = 1
		elif "when your other  is placed to the stage via change" in t:
			if r[0] != r[1] and r[0][-1] == r[1][-1] and any(field in pos[3] for field in ("Center", "Back")) and "Waiting" in pos[2] and self.name(a, self.cond[1], s='n') in nr[1] and "Change" in std:
				self.ablt = 1
		elif "when this is placed on the stage by the effect of \"" in aa or "when this is placed on the stage by the standby effect of \"" in aa or "when this is placed from hand to the stage or by the [auto] effect of \"" in aa or "when this is placed from hand to the stage or via effect of [auto] ability of your \"" in aa:
			if ("Hand" in pos[0] and r[0] == r[1] and v[0] == "Stand" and any(field in pos[1] for field in self.stage)) or (std[0] and std[2] == r[0] and std[0][-1] == r[1][-1] and std[0] != r[1] and r[0] == r[1] and (f"\"{std[1].lower()}\" to the stage" in aa or f"effect of \"{std[1].lower()}\"" in aa) and any(field in pos[1] for field in ("Center", "Back")) and ("Waiting" in pos[0] or "Library" in pos[0])):
				self.ablt = 1
			self.cond[1] += 2
		elif "when this is placed from hand to the stage or at the beginning of your main phase" in t:
			if ("Hand" in pos[0] and r[0] == r[1] and v[0] == "Stand" and any(field in pos[1] for field in self.stage)) or (pp < 0 and "Main" in p and n in r[0][-1]):
				self.ablt = 3
		elif "when this is placed to the stage via the  effect of " in t and "[auto] effect of \"" in aa:
			if std[0] and std[2] == r[0] and std[0][-1] == r[1][-1] and std[0] != r[1] and r[0] == r[1] and (f"\"{std[1].lower()}\" to the stage" in aa or f"effect of \"{std[1].lower()}\"" in aa) and any(field in pos[1] for field in ("Center", "Back")) and all(field not in pos[0] for field in ("Center", "Back")):
				self.ablt = 1
		elif "when your other character with assist is placed from hand to the stage" in t:
			if r[0] != r[1] and r[0][-1] == r[1][-1] and any(self.text_name["Assist"].lower() in tx[0].lower() for tx in text[1]) and "Hand" in pos[2] and any(field in pos[3] for field in self.stage) and "Stand" in v[1]:
				self.ablt = 9
		elif "when this or your other  character is placed on the stage from your hand" in t or "when your other  character or this is placed from hand to stage" in t:
			if (r[0] != r[1] and r[0][-1] == r[1][-1] and self.trait(a) in tr[1] and "Hand" in pos[2] and any(field in pos[3] for field in self.stage) and "Stand" in v[1]) or ("Hand" in pos[0] and r[0] == r[1] and v[0] == "Stand" and any(field in pos[1] for field in self.stage)):
				self.ablt = 9
		elif "when your other  is placed on the stage from your hand" in t and "\" is placed on" in aa:
			if r[0] != r[1] and r[0][-1] == r[1][-1] and self.name(a, self.cond[1], s='n') in nr[1] and "Hand" in pos[2] and any(field in pos[3] for field in self.stage) and "Stand" in v[1]:
				self.ablt = 9
				self.cond[1] += 2
				self.target = r[1]
		elif "» or «" in aa and ("when your other character with  or  is placed from hand to the stage" in t or "when your other  or  character is placed on stage from hand" in t):
			if r[0] != r[1] and r[0][-1] == r[1][-1] and (self.trait(a, self.cond[2]) in tr[1] or self.trait(a, self.cond[2] + 1) in tr[1]) and "Hand" in pos[2] and any(field in pos[3] for field in self.stage) and "Stand" in v[1]:
				self.ablt = 9
				self.target = r[1]
			self.cond[2] += 2
		elif "» or \"" in aa and "when another of your characters with  or  in its card name is placed on stage from your hand" in t:
			if r[0] != r[1] and r[0][-1] == r[1][-1] and (self.trait(a, self.cond[2]) in tr[1] or self.name(a, self.cond[1], s='n') in nr[1]) and "Hand" in pos[2] and any(field in pos[3] for field in self.stage) and "Stand" in v[1]:
				self.ablt = 9
				self.target = r[1]
			self.cond[2] += 1
			self.cond[1] += 2
		elif "when your other  character is played and placed to the stage" in t or "when another of your  characters is placed on the stage from your hand" in t or "when another of your  characters is placed from hand to the stage" in t or "when another  character of yours is placed from hand to the stage" in t or "when another  character is placed on the stage from your hand" in t or "when your other  character is placed on the stage from your hand" in t or "when your other  character is placed from hand to the stage" in t:
			if r[0] != r[1] and r[0][-1] == r[1][-1] and self.trait(a, self.cond[2]) in tr[1] and ("Hand" in pos[2] or ("on the stage from your hand or memory" in t and "Memory" in pos[2])) and any(field in pos[3] for field in self.stage) and "Stand" in v[1]:
				self.ablt = 9
				self.target = r[1]
		elif "when your other  character is placed from the stage to the waiting room" in t and "when your other «" in aa:
			if r[0] != r[1] and r[0][-1] == r[1][-1] and any(field in pos[2] for field in ("Center", "Back")) and "Waiting" in pos[3] and self.trait(a, self.cond[2]) in tr[1]:
				self.ablt = 9
				self.cond[2] += 1
				self.target = r[1]
		elif ("when your other  is placed from the stage to the waiting room" in t and "when your other \"" in aa) or "when your other character with  in its card name is put in your waiting room from the stage" in t or "when another of your characters with  in its card name is put in your waiting room from the stage" in t:
			if r[0] != r[1] and r[0][-1] == r[1][-1] and any(field in pos[2] for field in ("Center", "Back")) and "Waiting" in pos[3] and self.name(a, self.cond[1], s='n') in nr[1]:
				self.ablt = 9
				self.cond[1] += 2
				self.target = r[1]
		elif "when your other level  or lower character is placed from the stage to the waiting room" in t:
			if r[0] != r[1] and r[0][-1] == r[1][-1] and any(field in pos[2] for field in ("Center", "Back")) and "Waiting" in pos[3] and lr[1] <= self.digit(a, self.cond[0]):
				self.ablt = 9
				self.cond[0] += 1
				self.target = r[1]
		elif "when your other character is put in your waiting room from the stage" in t or "when your other character is put in the waiting room" in t or "when another character of yours is placed from the stage to the waiting room" in t or "when your other character is placed from the stage to the waiting room" in t or "when another of your characters is put in your waiting room from the stage" in t:
			if r[0] != r[1] and r[0][-1] == r[1][-1] and any(field in pos[2] for field in ("Center", "Back")) and "Waiting" in pos[3]:
				self.ablt = 9
				self.target = r[1]
		elif "when this is placed to the stage via change" in t:
			if std[0] and std[2] == r[0] and std[0][-1] == r[1][-1] and std[0] != r[1] and r[0] == r[1] and any(field in pos[1] for field in ("Center", "Back")) and "Waiting" in pos[0] and "Change" in std:
				self.ablt = 1
		elif "when this is placed from hand or waiting room to the stage" in t or "when this is placed from either hand or the waiting room to the stage" in t or "when this is placed on the stage from your hand or waiting room" in t:
			if r[0] == r[1] and ((any(field in pos[1] for field in self.stage) and "Waiting" in pos[0]) or ("Hand" in pos[0] and v[0] == "Stand" and any(field in pos[1] for field in self.stage))):
				self.ablt = 1
		elif "when this is placed from hand or the deck to the stage" in t:
			if r[0] == r[1] and ((any(field in pos[1] for field in self.stage) and "Library" in pos[0]) or ("Hand" in pos[0] and v[0] == "Stand" and any(field in pos[1] for field in self.stage))):
				self.ablt = 1
		elif "when this is placed on the stage from your hand or put in your waiting room from the stage" in t:
			if r[0] == r[1] and ((any(field in pos[0] for field in self.stage) and "Waiting" in pos[1]) or ("Hand" in pos[0] and v[0] == "Stand" and any(field in pos[1] for field in self.stage))):
				self.ablt = 9
		elif "when this is put in your waiting room from the stage" in t or "when this is placed from the stage to the waiting room" in t or "when this goes from stage to the waiting room" in t or "when this is put in the waiting room from the stage" in t or "when this is placed from stage to the waiting room" in t:
			if r[0] == r[1] and any(field in pos[0] for field in ("Center", "Back")) and "Waiting" in pos[1]:
				self.ablt = 1
				if r[4] != "":
					self.aselected = r[4]
				if "\" is in your climax area" in aa:
					self.ablt = 0
					if (f'\"{cx[0].lower()}\" is in your climax area' in aa and r[0][-1] == cx[1][-1]) or (f'\"{cx[3].lower()}\" is in your climax area' in aa and r[0][-1] == cx[4][-1]):
						self.ablt = 1
				if "you may put this rested in the slot this was in" in t or "you may return this to its previous stage position as rest" in t or "you may put it rested in the slot this was in" in t:
					return ["pay", "may", "played", "do", [0, "revive", "Stage", "do", [0, "rested"]]]
		elif "when another of your character whose level is  or lower is placed from the stage to the waiting room" in t:
			if r[0][-1] == r[1][-1] and r[0] != r[1] and any(field in pos[2] for field in ("Center", "Back")) and "Waiting" in pos[3] and lr[1] <= self.digit(a):
				self.ablt = 9
				self.target = r[1]
				if "if this is in the back stage" in t:
					if "Back" in pos[1]:
						self.ablt = 0
		elif "when an opponent's character is placed from hand to the stage" in t:
			if "Hand" in pos[2] and r[0] != r[1] and r[0][-1] != r[1][-1] and v[1] == "Stand" and any(field in pos[3] for field in self.stage):
				self.ablt = 9
		elif "when this is placed on the stage from your hand" in t or "when this is placed from your hand to the stage" in t or "when this is placed on stage from your hand" in t or "when this is placed from hand to the stage" in t or "when this is played and placed to the stage" in t:
			if "Hand" in pos[0] and r[0] == r[1] and v[0] == "Stand" and any(field in pos[1] for field in self.stage):
				self.ablt = 1
		elif "when this is placed from the waiting room to the stage" in t or "when this is placed from waiting room to the stage" in t:
			if r[0] == r[1] and any(field in pos[1] for field in self.stage) and "Waiting" in pos[0]:
				self.ablt = 1
		elif "when another of your characters is placed from the waiting room to the stage" in t:
			if r[0][-1] == r[1][-1] and r[0] != r[1] and any(field in pos[3] for field in self.stage) and "Waiting" in pos[2] and v[1] != "Reverse":
				self.ablt = 1
		elif "when this is placed on stage" in t or "when this is placed to the stage" in t:
			if pos[0] and r[0] == r[1] and v[0] == "Stand" and any(field in pos[1] for field in self.stage):
				self.ablt = 1
		elif "when this becomes rested from standing" in t:
			if r[0] == r[1] and r[0] in rst and v[0] == "Rest":
				self.ablt = 9
		elif "when your opponent's stand character becomes rest" in t:
			if r[0] != r[1] and r[0][-1] != r[1][-1] and r[1] in rst and v[1] == "Rest":
				self.ablt = 9
		elif "Battle" in p and (("when this's battle opponent becomes reverse" in t and "\"[auto] when this's battle" not in aa) or ("when the battle opponent of this becomes reverse" in t and "\"[auto] when the battle opponent" not in aa) or ("when this character's battle opponent becomes reverse" in t and "\"[auto] when this character's battle opponent" not in aa)):
			if r[0] != r[1] and r[1] in rst and r[0][-1] != r[1][-1] and r[0] in baind and r[1] in baind and ((r[0] == baind[0] and suop[1] == "Reverse") or (r[0] == baind[1] and suop[0] == "Reverse")):  
				if r[0] == baind[0]:
					self.target = baind[1]
				elif r[0] == baind[1]:
					self.target = baind[0]
				self.ablt = 2

				if "x = " in t:
					if "x = level of that character" in t:
						self.xx = lvop[1]
					elif "x = the cost of that character" in t or "x = cost of that character" in t:
						self.xx = csop[1]

				if ("\" is in the climax area" in aa or '\" is in your climax area' in aa) and (("\" is in the climax area" in aa and f"\"{cx[0].lower()}\" is in the climax area" not in aa) or ('\" is in your climax area' in aa and f'\"{cx[0].lower()}\" is in your climax area' not in aa) or r[0][-1] != cx[1][-1]):
					self.ablt = 0
				elif (f"\"{cx[0].lower()}\" is in the climax area" in aa or f'\"{cx[0].lower()}\" is in your climax area' in aa) and r[0][-1] == cx[1][-1]:
					self.ablt = 2
					self.cond[1] += 2
				elif "if there is a climax in your climax area" in t or "if there is a climax card in your climax area" in t:
					self.ablt = 0
					if (n == "1" and cx[1] != "" and cx[1][-1] == r[0][-1]) or (n == "2" and cx[4] != "" and cx[4][-1] == r[0][-1]):
						self.ablt = 2
		elif "Battle" in p and ("when the battle opponent of your other" in t or "when your other character's battle opponent" in t or "when the battle opponent of your other character" in t) and "becomes reverse" in t:
			if "other character becomes reverse" in t or "other character's battle opponent becomes reverse" in t or "when the battle opponent of your other character" in t:
				if r[0] != r[1] and r[1] in rst and r[0][-1] != r[1][-1] and v[1] == "Reverse" and r[0] not in baind and r[1] in baind:
					self.ablt = 2
			elif ("other  becomes reverse" in t or "other character with  in name becomes reverse" in t or "whose name includes  becomes reverse" in t) and ("\" becomes reverse" in aa or "\" in name becomes reverse" in aa):
				if r[0] != r[1] and r[1] in rst and r[0][-1] != r[1][-1] and v[1] == "Reverse" and r[0] not in baind and ((r[1] in baind[1] and self.name(a, s='n') in nmop[0]) or (r[1] in baind[0] and self.name(a, s='n') in nmop[1])):
					self.ablt = 9
					self.cond[1] += 2
		elif "Battle" in p and ("when this's level  or higher battle opponent becomes reverse" in t or "when a level  or higher battle opponent of this becomes reverse" in t or "when a level  or higher battle opponent of this becomes reverse" in t):
			if r[0] != r[1] and r[1] in rst and r[0][-1] != r[1][-1] and v[1] == "Reverse" and r[0] in baind and r[1] in baind and ((r[0] == baind[0] and lvop[1] >= self.digit(a)) or (r[0] == baind[1] and lvop[0] >= self.digit(a))):
				self.ablt = 2
				self.cond[0] += 1
				if "\" is in your climax area" in aa:
					self.ablt = 0
					if (f"\"{cx[0].lower()}\" is in your climax area" in aa and r[0][-1] == cx[1][-1] and n in cx[1][-1]) or (f"\"{cx[3].lower()}\" is in your climax area" in aa and r[0][-1] == cx[4][-1] and n not in cx[1][-1]):
						self.ablt = 9
					self.cond[1] += 2
		elif "Battle" in p and "when a level  or higher battle opponent of another character of yours becomes reverse" in t:
			if r[0] != r[1] and r[1] in rst and r[0][-1] != r[1][-1] and v[1] == "Reverse" and r[1] in baind and r[0] not in baind and ((r[1] == baind[1] and lvop[1] >= self.digit(a)) or (r[1] == baind[0] and lvop[0] >= self.digit(a))):
				if r[0] == baind[0]:
					self.target = baind[1]
				elif r[0] == baind[1]:
					self.target = baind[0]
				self.ablt = 9
		elif "Battle" in p and ("when another of your  characters becomes reverse in battle" in t or "when another of your  character becomes reverse in battle" in t):
			if r[0] != r[1] and r[1] in rst and r[0][-1] == r[1][-1] and v[1] == "Reverse" and r[1] in baind and r[0] not in baind and self.trait(a) in tr[1]:
				self.ablt = 9
		elif "Battle" in p and ("when this becomes reverse in battle" in t or "when this becomes reverse while battling" in t):
			if r[0] == r[1] and r[0] in rst and v[0] == "Reverse" and ((suop[0] == "Reverse" and r[0] in baind[0]) or (suop[1] == "Reverse" and r[0] in baind[1])):  
				if r[0] == baind[0]:
					self.target = baind[1]
				elif r[0] == baind[1]:
					self.target = baind[0]
				self.ablt = 2

				if "you may pay the cost" in t:
					if "rest this" in t and "reverse the battle opponent of this" in t:
						if r[0] == baind[0]:
							bopp = baind[1]
						elif r[0] == baind[1]:
							bopp = baind[0]
						return ["pay", "may", "at", "do", [0, "rest", "do", [-3, "reverser", "target", bopp, "Opp"]]]
				elif "level of its battle opponent is  or lower" in t or "this's battle opponent is level  or lower" in t or "level of the battle opponent of this is  or lower" in t or "level of this's battle opponent is  or lower" in t:
					self.ablt = 0
					if (r[0] == baind[0] and lvop[1] <= self.digit(a)) or (r[0] == baind[1] and lvop[0] <= self.digit(a)):
						self.ablt = 2
		elif "when this or the battle opponent of this becomes reverse" in t:
			if (r[0] == r[1] and r[0] in rst and v[0] == "Reverse") or (r[0] != r[1] and r[0][-1] != r[1][-1] and r[1] in rst and v[1] == "Reverse" and r[1] in baind and r[0] in baind and ((r[0] == baind[0] and suop[1] == "Reverse") or (r[0] == baind[1] and suop[0] == "Reverse")) and "Battle" in p):
				if v[0] == "Reverse" and v[1] == "Reverse" and r[0] != r[1] and r[0] in rst and r[1] in rst:
					self.target = f"{r[0]}_{r[1]}"
				else:
					self.target = r[1]
				self.ablt = 2
				if "Encore" in p:
					self.ablt = 0
		elif "when another  character of yours becomes reverse" in t:
			if r[0] != r[1] and r[1] in rst and r[0][-1] == r[1][-1] and v[1] == "Reverse" and self.trait(a) in tr[1]:
				self.ablt = 9
			if ("becomes reverse in battle" in t or " while battling" in t) and "Battle" not in p:
				self.ablt = 0
			if "Encore" in p:
				self.ablt = 0
		elif "when your other character with  or  in name" in t and " becomes reverse" in t and "\" or \"" in aa:
			if r[0] != r[1] and r[1] in rst and r[0][-1] == r[1][-1] and v[1] == "Reverse" and (self.name(a, self.cond[1], s='n') in nr[1] or self.name(a, self.cond[1] + 2, s='n') in nr[1]):  
				self.cond[1] += 4
				self.ablt = 9
				self.target = r[1]
				if "in the center stage center slot becomes reverse" in t:
					if "Center" not in pos[3]:
						self.ablt = 0
				if ("in battle" in t or " while battling" in t) and r[1] not in baind and "Battle" not in p:
					self.ablt = 0
		elif "when your other character becomes reverse" in t or "when another of your characters becomes reverse" in t:
			if r[0] != r[1] and r[1] in rst and r[0][-1] == r[1][-1] and r[1] in baind and v[1] == "Reverse":  
				self.ablt = 9
				self.target = r[1]

				if ("in battle" in t or "while battling" in t) and r[1] not in baind and "Battle" not in p:
					self.ablt = 0
		elif "when this becomes reversed" in t or "when this becomes reverse" in t:
			if r[0] == r[1] and r[0] in rst and v[0] == "Reverse":  
				if r[0] == baind[0]:
					self.target = baind[1]
				elif r[0] == baind[1]:
					self.target = baind[0]
				self.ablt = 0
				if "level of its battle opponent is  or lower" in t or "this's battle opponent is level  or lower" in t or "level of the battle opponent of this is  or lower" in t or "level of the battle opponent is  or lower" in t or "level of this's battle opponent is  or lower" in t:
					if (r[0] == baind[0] and lvop[1] <= self.digit(a, self.cond[0])) or (r[0] == baind[1] and lvop[0] <= self.digit(a, self.cond[0])):
						self.ablt = 2
						self.cond[0] += 1
				elif "level of its battle opponent is same or lower than this" in t or "level of this's battle opponent is lower than or equal to the level of this" in t or "level of its battle opponent = or lower than the level of this" in t or "level of its battle opponent is lower than or equal to the level of this" in t:
					if (r[0] == baind[0] and lvop[1] <= lvop[0]) or (r[0] == baind[1] and lvop[0] <= lvop[1]):
						self.ablt = 2
				elif "level of the battle opponent of this is higher than the level of your opponent" in t or "level of this's battle opponent is higher than your opponent's level" in t or "level of the battle opponent of this is higher than the level of the opponent" in t:
					self.ablt = 2
				elif "cost of the battle opponent of this is  or lower" in t or "this's battle opponent is cost  or lower" in t or "cost of the battle opponent of this is  or lower" in t:
					if (r[0] == baind[0] and csop[1] <= self.digit(a, self.cond[0])) or (r[0] == baind[1] and csop[0] <= self.digit(a, self.cond[0])):
						self.ablt = 2
						self.cond[0] += 1
				else:
					self.ablt = 9

				if ("in battle" in t or " while battling" in t) and "Battle" not in p:
					self.ablt = 0
				if "battle opponent" in t and all(phase not in p for phase in self.attack):
					self.ablt = 0
				if "Encore" in p:
					self.ablt = 0
		elif "when the damage dealt by this is cancelled" in t or "when the damage dealt by this becomes canceled" in t or "when damage dealt by this is canceled" in t or "when damage dealt by this is cancelled" in t or "when this's damage is cancelled" in t or "when the next damage dealt by this is canceled" in t:
			if dmg > 0 and r[0] == r[1] and cnc[0] not in r[0][-1] and cnc[1]:
				self.dmg = dmg
				if "\" is in your climax area" in aa:
					if f"\"{cx[0].lower()}\" is in your climax area" in aa and r[0][-1] == cx[1][-1] and n in cx[1][-1]:
						self.cx = True
						self.ablt = 9
				else:
					self.ablt = 9
				if "next damage dealt by this" in t and self.ablt:
					self.ablt = 1
		elif "when damage dealt by your level  or higher characters is canceled" in t:
			if dmg > 0 and r[0] != r[1] and r[0][-1] == r[1][-1] and cnc[0] not in r[0][-1] and cnc[1] and lr[1] >= self.digit(a, self.cond[0]):
				self.ablt = 9
				self.cond[0] += 1
		elif "when damage dealt by your direct attacking character is not cancel" in t or "when the damage dealt by your direct attacking character is not cancel" in t:
			if dmg > 0 and r[0] != r[1] and r[0][-1] == r[1][-1] and cnc[0] not in r[0][-1] and not cnc[1] and atk == "d":
				self.ablt = 9
		elif "when damage dealt by this is not cancel" in t:
			if dmg > 0 and r[0] == r[1] and cnc[0] not in r[0][-1] and not cnc[1]:
				self.ablt = 9
				if " is in your climax area" in t:
					self.ablt = 0
					if (f"\"{cx[0].lower()}\" is in your climax area" in aa and r[0][-1] == cx[1][-1] and n in cx[1][-1]) or (f"\"{cx[3].lower()}\" is in your climax area" in aa and r[0][-1] == cx[4][-1] and n not in cx[1][-1]):
						self.ablt = 9
		elif "when the damage dealt by your character is cancelled" in t:
			if dmg > 0 and r[0] != r[1] and r[0][-1] == r[1][-1] and cnc[0] not in r[0][-1] and cnc[1]:
				self.ablt = 9
		elif "if damage taken by you is not canceled" in t or "when the damage you received is not canceled" in t or "when the damage taken by you is not cancelled" in t:
			if dmg > 0 and not cnc[1] and cnc[0] in r[0][-1]:
				self.dmg = dmg
				self.ablt = 9
		elif "when the damage you received is canceled" in t or "when damage taken by you is cancelled" in t:
			if dmg > 0 and r[0] != r[1] and r[0][-1] != r[1][-1] and cnc[1] and cnc[0] in r[0][-1]:
				self.ablt = 9
		elif pp == 9 and atk and p in self.attack:
			if "at the end of this's attack" in t:
				if n in r[0][-1] and r[0] == r[1] and atk != "" and r[0] == baind[0]:
					if "\" is in your climax area" in aa:
						if f"\"{cx[0].lower()}\" is in your climax area" in aa and r[0][-1] == cx[1][-1] and n in cx[1][-1]:
							self.ablt = 2
					else:
						self.ablt = 2
		elif "Draw" in p and pp < 0:
			if "at the beginning of your draw phase" in t or "at the start of your draw phase" in t:
				if n in r[0][-1] and r[0] in begin:
					self.ablt = 3
					if "put those characters from your memory on to separate positions of your stage" in t:
						if "those characters get + power" in t:
							return [-38, "msalvage", "", "Stage", "a1", "separate", "extra", "do", [-16, self.digit(a), x, "power"]]
			elif "at the beginning of your opponent's draw phase" in t or "at the start of your opponent's draw phase" in t:
				if n not in r[0][-1] and r[0] in begin:
					self.ablt = 3
		elif "Main" in p and pp < 0:
			if "shift, level " in t:
				if n in r[0][-1] and "Clock" in pos[1] and r[0] in begin:
					self.ablt = 3
			elif "at the start of your main phase" in t or "at the beginning of your main phase" in t:
				if n in r[0][-1] and r[0] in begin:
					self.ablt = 3
			elif "at the beginning of your opponent's main phase" in t:
				if n not in r[0][-1] and r[0] in begin:
					self.ablt = 3
		elif "Climax" in p and pp < 0:
			if "at the start of your climax phase" in t or "at the beginning of your climax phase" in t:
				if n in r[0][-1] and r[0] in begin:  
					self.ablt = 3
		elif "Climax" in p and pp >= 0:
			if f" \"{cx[0].lower()}\" is placed to your or your opponent's climax area" in aa or f" \"{cx[3].lower()}\" is placed to your or your opponent's climax area" in aa:
				if (cx[0] != "" and r[0][-1] == cx[1][-1] and cx[1] == r[1] and n in cx[1][-1] and n in r[0][-1]) or (cx[3] != "" and r[0][-1] == cx[4][-1] and cx[4] == r[1] and n not in cx[4][-1] and n not in r[0][-1]) or (cx[0] != "" and r[0][-1] != cx[1][-1] and cx[1] == r[1] and n not in r[0][-1] and n in cx[1][-1]) or (cx[3] != "" and r[0][-1] != cx[4][-1] and cx[4] == r[1] and n in r[0][-1] and n not in cx[4][-1]):  
					self.ablt = 9
					self.cond[1] += 2
			elif f" \"{cx[0].lower()}\" is put on your climax area" in aa or f" \"{cx[0].lower()}\" is placed on your climax area" in aa or f" \"{cx[0].lower()}\" is placed in your climax area" in aa or f" \"{cx[0].lower()}\" is placed to your climax area" in aa or f" \"{cx[0].lower()}\" is placed in the climax area" in aa:
				if r[0][-1] == cx[1][-1] and cx[1] == r[1]:  
					self.ablt = 9
					self.cond[1] += 2
			elif "when a climax is placed on your opponent's climax area" in t or "when your opponent's climax card is placed in the climax area" in t or "when your opponent's climax is placed on their climax area" in t:
				if (cx[0] != "" and r[0][-1] != cx[1][-1] and cx[1] == r[1] and n not in r[0][-1] and n in cx[1][-1]) or (cx[3] != "" and r[0][-1] != cx[4][-1] and cx[4] == r[1] and n in r[0][-1] and n not in cx[4][-1]):
					self.ablt = 9
					if "character opposite this" in t:
						if "Center" not in pos[1]:
							self.ablt = 0
			elif "when your climax with treasure in its trigger icon is placed on your climax area" in t:
				if (cx[0] != "" and r[0][-1] == cx[1][-1] and cx[1] == r[1] and n in cx[1][-1] and n in r[0][-1] and "treasure" in ty[1]) or (cx[3] != "" and r[0][-1] == cx[4][-1] and cx[4] == r[1] and n not in cx[4][-1] and n not in r[0][-1] and "treasure" in ty[1]):
					self.ablt = 9
			elif "when your climax with door in its trigger icon is placed on your climax area" in t:
				if (cx[0] != "" and r[0][-1] == cx[1][-1] and cx[1] == r[1] and n in cx[1][-1] and n in r[0][-1] and "door" in ty[1]) or (cx[3] != "" and r[0][-1] == cx[4][-1] and cx[4] == r[1] and n not in cx[4][-1] and n not in r[0][-1] and "door" in ty[1]):
					self.ablt = 9
			elif "when a climax is placed on your climax area" in t or "when your climax is placed in the climax area" in t or "when your climax is placed on your climax area" in t or "when your climax card is placed in the climax area" in t or "when a climax is put on your climax area" in t:
				if (cx[0] != "" and r[0][-1] == cx[1][-1] and cx[1] == r[1] and n in cx[1][-1] and n in r[0][-1]) or (cx[3] != "" and r[0][-1] == cx[4][-1] and cx[4] == r[1] and n not in cx[4][-1] and n not in r[0][-1]):
					self.ablt = 9
			elif "when your  climax is placed in the climax area" in t and any(f"when your {cc} climax is placed" in aa for cc in self.colour):
				if (cx[0] != "" and r[0][-1] == cx[1][-1] and cx[1] == r[1] and n in cx[1][-1] and n in r[0][-1] and self.colour_t(a).lower() in cx[2].lower()) or (cx[3] != "" and r[0][-1] == cx[4][-1] and cx[4] == r[1] and n not in cx[4][-1] and n not in r[0][-1] and self.colour_t(a).lower() in cx[5].lower()):
					self.ablt = 9
		elif "Attack" in p and pp < 0:
			if "at the start of your opponent's attack phase" in t or "at the beginning of your opponent's attack phase" in t:
				if n not in r[0][-1] and r[0] in begin:
					self.ablt = 3
					if "if your opponent doesn't have a climax card in his or her climax area" in t:
						if cx[4] != "":
							self.ablt = 0
			elif "at the beginning of your attack phase" in t or "at the start of your attack phase" in t:
				if n in r[0][-1] and r[0] in begin:
					if "\" is in your climax area" in aa:
						if f"\"{cx[0].lower()}\" is in your climax area" in aa and r[0][-1] == cx[1][-1] and n in cx[1][-1]:
							self.ablt = 3
					else:
						self.ablt = 3
		elif "Declaration" in p:
			if "when this attacks or is attacked" in t or "when this attacks or is front attacked" in t:
				if atk != "" and r[0] in baind and n in r[1][-1] and (r[0] == r[1] or (r[0] != r[1] and r[0][-1] != r[1][-1] and atk == "f")):
					self.ablt = 9
			elif "when this attack" in t:
				if r[0] == r[1] and n in r[1][-1] and atk != "" and r[0] == baind[0]:
					if "\" is in the climax area" in aa or "\" is in your climax area" in aa or "\" on your climax area" in aa:
						if (f"\"{cx[0].lower()}\" is in the climax area" in aa or f"\"{cx[0].lower()}\" is in your climax area" in aa or f"\"{cx[0].lower()}\" on your climax area" in aa) and r[0][-1] == cx[1][-1] and n in cx[1][-1]:
							self.cx = True
							self.ablt = 2
							self.cond[1] += 2
							if "you have  card named  on your climax area" in t:
								self.cond[0] += 1
					elif "if a  climax is in your climax area" in t or "if there's a  climax card in the climax area" in t:
						if (f"if a {cx[2].lower()} climax is in your climax area" in aa or f"if there's a {cx[2].lower()} climax card in the climax area" in aa) and r[0][-1] == cx[1][-1] and n in cx[1][-1]:
							self.ablt = 2
					else:
						self.ablt = 2
			elif "when this is front attacked" in t and "\"[auto] when this is front attacked" not in aa:
				if r[0] != r[1] and n in r[1][-1] and r[0][-1] != r[1][-1] and r[0] in baind[1] and r[1] in baind[0] and "f" in atk:
					self.ablt = 2
					if "if the level of the battle opponent of this is higher or equal to the level of this" in t:
						if lvop[0] < lvop[1]:
							self.ablt = 0
			elif "when this direct attack" in t:
				if r[0] == r[1] and n in r[1][-1] and r[0] in baind[0] and "d" in atk:
					if "if  is in the climax area" in t:
						if f"if \"{cx[0].lower()}\" is in the climax area" in aa and r[0][-1] == cx[1][-1] and n in cx[1][-1]:
							self.ablt = 2
					else:
						self.ablt = 2
			elif "when this front attack" in t:
				if r[0] == r[1] and n in r[1][-1] and r[0] in baind[0] and "f" in atk:
					self.ablt = 2
					if "the level of the battle opponent of this is lower than the level of this" in t:
						if lvop[1] >= lvop[0]:
							self.ablt = 0
			elif "when this side attack" in t:
				if r[0] == r[1] and n in r[1][-1] and r[0] in baind[0] and "s" in atk:
					if "\" is in the climax area" in aa or "\" is in your climax area" in aa:
						if (f"\"{cx[0].lower()}\" is in the climax area" in aa or f'\"{cx[0].lower()}\" is in your climax area' in aa) and r[0][-1] == cx[1][-1] and n in cx[1][-1]:
							self.ablt = 2
					else:
						self.ablt = 2
			elif "when your other character in the middle position of the center stage attacks" in t:
				if r[0] != r[1] and r[0][-1] == r[1][-1] and n in r[1][-1] and r[1] in baind[0] and r[0] not in baind and atk != "" and pos[3] == "Center1":
					self.ablt = 2
			elif "when another of your characters is being attacked" in t:
				if r[0] != r[1] and n in r[1][-1] and r[0][-1] != r[1][-1] and r[0] not in baind and r[1] in baind[0] and atk != "d":
					self.target = baind[1]
					self.ablt = 2
			elif "when your other  character is front attacked" in t or "when your other  characters is front attacked" in t:
				if r[0] != r[1] and n in r[1][-1] and r[0][-1] != r[1][-1] and r[0] not in baind and r[1] in baind[0] and self.trait(a, self.cond[2]) in trop[1] and "f" in atk:
					self.target = baind[1]
					self.ablt = 2
				self.cond[2] += 1
			elif "when your other character is front attacked" in t or "when another of your characters is being front attacked" in t:
				if r[0] != r[1] and n in r[1][-1] and r[0][-1] != r[1][-1] and r[0] not in baind and r[1] in baind[0] and "f" in atk:
					self.target = baind[1]
					self.ablt = 2
			elif "when your other  character or character with  in its card name attacks" in t:
				if r[0] != r[1] and r[0][-1] == r[1][-1] and n in r[0][-1] and (self.trait(a) in tr[1] or self.name(a, s="a") in nr[1]) and r[1] in baind[0] and r[0] not in baind and atk != "":
					if "this gets + power" in t:
						return [0, self.digit(a), x, "power", "at"]
			elif "when another of your characters whose name includes  attacks" in t:
				if r[0] != r[1] and r[0][-1] == r[1][-1] and n in r[0][-1] and self.name(a, s="a") in nr[1] and r[1] in baind[0] and r[0] not in baind and atk != "":
					if "if that character's power is at least  higher than its battle opponent" in t:
						if "your opponent may not play backup from hand during that character's battle" in t:
							return [self.digit(a), "atkpwrdif", r[1], "do", [-12, "[CONT] During this card's battle, your opponent cannot play \"Backup\" from hand.", -2, "give"]]
			elif ("when  of your other  or  characters attack" in t or "when your other character with either  or  attack" in t or "when your other character with  or  attack" in t or "when your other  or  character attack" in t) and "» or «" in aa:
				if r[0] != r[1] and r[0][-1] == r[1][-1] and n in r[1][-1] and (self.trait(a, self.cond[2]) in tr[1] or self.trait(a, self.cond[2] + 1) in tr[1]) and r[1] in baind[0] and r[0] not in baind and atk != "":
					self.ablt = 2
					if "when  of your other" in t:
						self.cond[0] += 1
					self.cond[2] += 2
					self.target = r[1]
			elif "when your other character that is either  or  attack" in t and " or «" in aa and any(f"when your other character that is either {cl} or «" in aa for cl in self.colour):
				if r[0] != r[1] and r[0][-1] == r[1][-1] and n in r[1][-1] and (self.trait(a, self.cond[2]) in tr[1] or self.colour_t(a, self.cond[4]).lower() in r[3]) and r[1] in baind[0] and r[0] not in baind and atk != "":
					self.ablt = 2
					self.cond[2] += 1
					self.cond[4] += 1
					self.target = r[1]
			elif "when your other  character attacks" in t or "when another of your  character attacks" in t:
				if r[0] != r[1] and r[0][-1] == r[1][-1] and n in r[1][-1] and self.trait(a, self.cond[2]) in tr[1] and r[1] in baind[0] and r[0] not in baind and atk != "":
					self.cond[2] += 1
					self.ablt = 2
			elif "» or «" in aa and "when your other  or  character is front attacked" in t:
				if r[0] != r[1] and r[0][-1] != r[1][-1] and r[0] not in baind and r[1] in baind[0] and "f" in atk and n in r[1][-1] and (self.trait(a, self.cond[1]) in trop[1] or self.trait(a, self.cond[1] + 1) in trop[1]) and r[0][-1] == baind[1][-1]:
					self.ablt = 9
					self.cond[2] += 2
					self.target = baind[1]
				self.cond[2] += 2
			elif "» or \"" in aa and "when your other character with  or " in t and "\" in name is front attacked" in aa:
				if r[0] != r[1] and r[0][-1] != r[1][-1] and r[0] not in baind and r[1] in baind[0] and "f" in atk and n in r[1][-1] and (self.name(a, self.cond[1], s="n") in nmop[1] or self.trait(a, self.cond[2]) in trop[1]) and r[0][-1] == baind[1][-1]:
					self.ablt = 9
					self.cond[1] += 4
					self.target = baind[1]
				self.cond[1] += 2
				self.cond[2] += 1
			elif ("when your other character with  or " in t or "when another of your characters with  or  " in t) and ("in name is front attacked" in t or "in its card name is front attacked" in t):
				if r[0] != r[1] and r[0][-1] != r[1][-1] and r[0] not in baind and r[1] in baind[0] and "f" in atk and n in r[1][-1] and (self.name(a, self.cond[1], s="n") in nmop[1] or self.name(a, self.cond[1] + 2, s='n') in nmop[1]) and r[0][-1] == baind[1][-1]:
					self.ablt = 9
					self.cond[1] += 4
					self.target = baind[1]
				self.cond[1] += 4
			elif "when another of your characters with  in its card name is front attacked" in t:
				if r[0] != r[1] and r[0][-1] != r[1][-1] and r[0] not in baind and r[1] in baind[1] and "f" in atk and n in r[1][-1] and self.name(a, s="a") in nmop[1]:
					self.ablt = 9
			elif "when your character direct attacks" in t:
				if r[0][-1] == r[1][-1] and n in r[1][-1] and r[1] in baind[0] and "d" in atk:
					self.ablt = 9
			elif "when your other  direct attack" in t and "\" direct attack" in aa:
				if "there isn't another \"" in aa and aa.index("there isn't another \"") < aa.index("when your other \""):
					self.cond[1] += 2
					self.cond_rep[0] = True
				if r[0] != r[1] and r[0][-1] == r[1][-1] and n in r[1][-1] and self.name(a, self.cond[1], s='n') in nmop[0] and r[1] in baind[0] and r[0] not in baind and atk == "d":
					self.cond[1] += 2
					if "\" is in the climax area" in aa:
						if f"\"{cx[0].lower()}\" is in the climax area" in aa and r[0][-1] == cx[1][-1] and n in cx[1][-1]:
							self.cond[1] += 2
							self.ablt = 2
					else:
						self.ablt = 2
					if self.cond_rep[0]:
						self.cond_rep[1] = [1, self.cond[1]]
			elif "when your other  attack" in t and "\" attack" in aa:
				if r[0] != r[1] and r[0][-1] == r[1][-1] and n in r[1][-1] and self.name(a, self.cond[1], s='n') in nmop[0] and r[1] in baind[0] and r[0] not in baind and atk != "":
					self.cond[1] += 2
					self.ablt = 2
			elif "when the character opposite this attack" in t:
				if r[0] != r[1] and r[0][-1] != r[1][-1] and n in r[1][-1] and r[1] in baind[0] and opp == r[1]:
					self.ablt = 9
			elif "when your character is attacked" in t:
				if r[0] != r[1] and r[0][-1] != r[1][-1] and n in r[1][-1] and r[1] in baind[0]:
					self.ablt = 9
		elif "Trigger" in p:
			if ("when your character reveals  or  during their trigger check" in t or "when your character's trigger check reveals  or " in t) and "\" or \"" in aa:
				if n in r[0][-1] and r[0][-1] == r[1][-1] and r[0] != r[1] and (self.name(a, self.cond[1], s='n') in ty[3] or self.name(a, self.cond[1] + 2, s='n') in ty[3]) and ty[0] == r[2]:
					self.ablt = 9
				self.cond[1] += 4
			elif "when your character's trigger check reveals a climax" in t or "when the trigger check of this reveals a climax" in t or "when your trigger check reveals a climax" in t or "when your character's trigger check reveals  card with" in t or ("when your character reveals a " in t and " trigger icon on a climax" in t) or ("when this's trigger check reveals a climax with" in t and " in its trigger icon" in t):
				if "when your character's trigger check reveals  card " in t:
					self.cond[0] += 1
				if n in r[0][-1] and r[0][-1] == r[1][-1] and r[0] != r[1] and "Climax" in ty[0] and ty[0] == r[2]:
					if "if the trigger icons of that card are" in t or "if that card's trigger icon is" in t or "in its trigger icon" in t or "if that card has" in t or "climax card with a " in t or "reveals a climax with a " in t:
						if (("soulsoul trigger icons" in t or "icon is soulsoul" in t or "soulsoul in its trigger icon" in t) and len([s for s in ty[1] if s == "soul"]) == 2) or (("trigger icon is door" in t or "climax with a door trigger" in t) and "door" in ty[1]) or ("trigger icon is bounce" in t and "bounce" in ty[1]) or ("trigger icon is stock" in t and "stock" in ty[1]) or ("trigger icon is draw" in t and "draw" in ty[1]) or (("trigger icon is gate" in t or "with gate in its trigger icon" in t) and "gate" in ty[1]) or (("card has a treasure icon" in t or "with a treasure trigger" in t or "treasure in its trigger icon" in t or "with treasure in its trigger icon" in t) and "treasure" in ty[1]):
							self.ablt = 9
					else:
						self.ablt = 9
					if "when the trigger check of this reveals a climax" in t and r[0] not in baind[0] and r[0] != ty[2]:
						self.ablt = 0
				if self.ablt and "if there is a climax in your climax area" in t or "if there is a climax card in your climax area" in t:
					self.ablt = 0
					if (n == "1" and cx[1] != "" and cx[1][-1] == r[0][-1]) or (n == "2" and cx[4] != "" and cx[4][-1] == r[0][-1]):
						self.ablt = 9
			elif "when your character's trigger check reveals a  climax card" in t:
				if n in r[0][-1] and r[0][-1] == r[1][-1] and r[0] != r[1] and "Climax" in ty[0] and ty[0] == r[2] and self.colour_t(a, self.cond[4]).lower() in ty[4].lower():
					self.ablt = 9
				self.cond[4] += 1
			elif "when this's trigger check reveals a level  or lower card" in t:
				if n in r[0][-1] and r[0] == ty[2] and r[0][-1] == r[1][-1] and r[0] != r[1] and r[0] in baind[0] and ty[5] <= self.digit(a, self.cond[0]):
					self.ablt = 9
				self.cond[0] += 1
		elif "Counter" in p:
			if pp < 0:
				if "at the beginning of counter step during your opponent's turn" in t:
					if n not in r[0][-1]:
						self.ablt = 3
			elif pp == 0:
				if "when you use this's " in t or "when you use the backup of this" in t:
					if r[0] == r[1] and r[0] == act:
						if "\"backup\"" in aa:
							self.cond[1] += 2
						self.ablt = 2
				elif "when you use a backup" in t or ("when you use " in t and "when you use \"backup\"" in aa):
					if r[0] != r[1] and r[0][-1] == r[1][-1] and r[1] == act:
						self.ablt = 9
		elif "Encore" in p and pp < 0:
			if "at the beginning of the encore step" in t or "at the start of encore step" in t:
				if r[0] in begin:
					self.ablt = 3
					if "if those characters are on stage" in t:
						if "return them to your deck" in t:
							return [-20, "decker", "a1"]
			elif "at the start of your encore step" in t or "at the beginning of your encore step" in t:
				if n in r[0][-1] and r[0] in begin:
					if "\" is in the climax area" in aa or "\" is in your climax area" in aa or "\" on your climax area" in aa:
						if (f"\"{cx[0].lower()}\" is in the climax area" in aa or f'\"{cx[0].lower()}\" is in your climax area' in aa or f'\"{cx[0].lower()}\" on your climax area' in aa) and r[0][-1] == cx[1][-1] and n in cx[1][-1]:
							self.ablt = 3
					else:
						self.ablt = 3
			elif "at the beginning of your opponent's encore step" in t:
				if n not in r[0][-1] and r[0] in begin:
					self.ablt = 3
		elif "End" in p and pp > 0:
			if "at the end of of your opponent's next turn" in t or "at the end of your opponent's turn" in t:
				if n != r[0][-1] and z[0] != z[1]:
					self.ablt = 3
			elif "at the end of your turn" in t:
				if n == r[0][-1]:
					self.ablt = 3
			elif "at the end of the turn" in t and "at the start of your climax phase" not in t:
				self.ablt = 3
				if "you may place the previously chosen character face up under this as a marker" in t:
					return ["pay", "may", "a1", "do", [-38, "marker", "", "Stage", "face-up"]]

		if "during the turn this is placed via the effect of  ability of" in t:
			if z[0] != z[1] or z[3] != self.name(a, self.cond[1], s='n'):
				self.ablt = 0
			self.cond[1] += 2
		elif ("during the turn that this is placed" in t or "during the turn this is placed" in t or "during the turn this was placed" in t) and ("placed on the stage from your hand" in t or "placed on stage from your hand" in t or "placed from hand to the stage" in t):
			if "from your hand or by the  effect of " in t:
				if z[0] != z[1] or (z[3] != self.name(a, self.cond[1], s='n') and "Hand" not in z[2] and all(field not in pos[1] for field in self.stage)):
					self.ablt = 0
				self.cond[1] += 2
			else:
				if z[0] != z[1] or "Hand" not in z[2] or all(field not in pos[1] for field in self.stage):
					self.ablt = 0
		elif "it is the first turn of the player who went first" in t:
			if z[1] != 1:
				self.ablt = 0
		elif "after the current turn" in t and "until the end of the turn" not in t:
			if z[0] == z[1]:
				self.ablt = 0

		if "during your turn" in t:
			if n not in r[0][-1]:
				self.ablt = 0
		elif "during this's battle" in t or "during battles involving this" in t:
			if r[0] not in baind or atk != "f":
				self.ablt = 0
		elif "during your opponent's turn" in t:
			if n in r[0][-1]:
				self.ablt = 0
		elif "during your climax phase" in t:
			if n not in r[0][-1] or "Climax" not in p:
				self.ablt = 0

		if "if this is in your memory" in t or "if this is in memory" in t:
			if "Memory" not in pos[1]:
				self.ablt = 0
		elif "if this is in the waiting room" in t:
			if "Waiting" not in pos[1]:
				self.ablt = 0
		elif "if this is in your back stage" in t or "if this is in the back stage" in t or "if this is on the back stage" in t:
			if "Back" not in pos[1]:
				self.ablt = 0
		elif "if this is in the center stage center slot" in t:
			if "Center1" not in pos[1]:
				self.ablt = 0
		elif "if this is in your center stage" in t or "if this is in the center stage" in t or "if this is on your center stage" in t or "if this in on your center stage" in t or "and this is in your center stage" in t or "if this is on the center stage" in t:
			if "Center" not in pos[1]:
				self.ablt = 0

		if "if this is rest" in t:
			if v[0] != "Rest":
				self.ablt = 0
		elif "if this is standing in the center stage" in t:
			if v[0] != "Stand" or "Center" not in pos[1]:
				self.ablt = 0
		if "if this is stand" in t or "and this is stand" in t:
			if v[0] != "Stand":
				self.ablt = 0

		if "and that damage is  or more" in t:
			if self.dmg < self.digit(a, self.cond[0]):
				self.ablt = 0
			self.cond[0] += 1

		if self.ablt:
			if passed:
				self.ablt = self.ablt * -1
			return self.effect(a, t, aa, self.ablt)
		else:
			return []

	def effect(self, a, t="", aa="", pl=0):
		if aa == "":
			aa = self.a_replace(a)
		if t == "":
			t = self.text(a)
		self.start = False
		e = []
		self.ee = False
		self.isnot = ""
		self.donot = ""
		if "you may pay the cost" in t or ("you may " in t and "you may not " not in t and "you may perform that action as many times as you like" not in t) or ("your opponent may pay" in t and "your opponent may not" not in t):
			e = ["pay", "may"]
			if "may pay the cost" not in t and "may pay cost" not in t:
				self.ee = True
			if "your opponent may pay" in t:
				e.append("opp")

		m = []
		multi = False
		if "for each  you have" in t and "perform the following action" in t and "for each \"" in aa:
			mn = self.name(a, self.cond[1], s='n')
			m = ["multiple", "Name", mn]
			multi = True

		p = []
		if abs(pl) == 1:
			p = ["played"]
		elif abs(pl) == 2:
			p = ["at"]
		elif abs(pl) == 3:
			p = ["a1"]
		elif abs(pl) == 6:
			p = ["as"]

		if "this ability activates up to once per turn" in t or "this ability may be activated up to once per turn" in t:
			if "a1" not in p:
				p.append("a1")
			if "played" in p:
				p.remove("played")
			if "at" in p:
				p.remove("at")
		elif "this ability activates up to  time per turn" in t:
			self.cond[0] += 1
			if f"a{self.digit(a)}" not in p:
				p.append(f"a{self.digit(a)}")
			if "played" in p:
				p.remove("played")
			if "at" in p:
				p.remove("at")

		ef = self.condition(a, t, aa)
		tempcond = list(self.cond)
		if multi:
			n = self.name(a, -1, s="n")
			cv = self.convert(n, self.text(n), self.a_replace(n))
		else:
			cv = self.convert(a, t, aa)

		cm = []
		if self.isnot:
			cm = self.add_notisdo(cm, "isnot", a, t, aa)
		elif self.multicond[0]:
			cm = self.add_notisdo(cm, self.multicond[0], a, t, aa)

		if "d_atk" in cv:
			e = []

		if self.no_pay:
			e = []
			self.no_pay = False
		if e:
			if self.ee and "upto" not in cv and all(ss not in cv for ss in ["draw", "heal", "trigger", "shuffle", "hander", "salvage", "drawupto", "damage"]):
				if "reveal" in cv:
					if "do" in cv and "drawupto" in cv[cv.index("do") + 1] and "upto" in cv[cv.index("do") + 1]:
						pass
					else:
						if "do" in cv and "done" in cv:
							if "upto" not in cv[cv.index("do") + 1]:
								cv[cv.index("do") + 1].append("upto")
							temp = cv[cv.index("done") + 1]
							cv.remove(temp)
							cv.remove("done")
							temp1 = cv[cv.index("do") + 1]
							cv.remove(temp1)
							cv.extend([e + ["do", temp1]])
							cv.extend(["done", temp])
						elif "do" in cv:
							if "upto" not in cv[cv.index("do") + 1]:
								cv[cv.index("do") + 1].append("upto")
							temp = cv[cv.index("do") + 1]
							cv.remove(temp)
							cv = cv + [e + ["do", temp]]
						elif "done" in cv:
							if "upto" not in cv[cv.index("done") + 1]:
								cv[cv.index("done") + 1].append("upto")
							temp = cv[cv.index("done") + 1]
							cv.remove(temp)
							cv = cv + [e + ["do", temp]]
				elif "mill" in cv and "do" in cv and any(abi in cv[cv.index("do") + 1] for abi in ("stocker", "salvage")):
					temp = cv[cv.index("do") + 1]
					cv.remove(temp)
					cv = cv + [e + ["do", temp]]
				elif "if" in cv:
					if "discard" in cv and "upto" not in cv:
						pass
					else:
						cv.insert(cv.index("if"), "upto")
					if "waitinger" in cv:
						pass
					else:
						cv = e + ["do", cv]
				elif "give" in cv and "you may" in cv[1]:
					pass
				else:
					cv = e + ["do", cv + ["upto"]]
			else:
				if ("reveal" in cv or "mill" in cv) and "payafter" in cv:
					temp = cv[cv.index("do") + 1]
					cv.remove(temp)
					cv = cv + [e + ["do", temp]]
				elif ("reveal" in cv or "mill" in cv) and "paybefore" in cv:
					temp = cv[cv.index("do") + 1]
					cv.remove(temp)
					cv = cv + [e + ["do", temp]]
				else:
					cv = e + ["do", cv]
			e = []

		if self.donot:
			cv = self.add_notisdo(cv, "dont", a, t, aa, 1)

		if not self.cond_later and ef and cv:
			try:
				ef[ef.index("do") + 1].append(cv)
			except IndexError:
				ef.append(cv)
		else:
			ef = cv

		if "instead of" in t and "more" in ef and self.temp[0]:
			ef[ef.index("more") - 1] = self.temp[0]
			ef.extend(["dont", deepcopy(ef[ef.index("do") + 1])])
			if "pay" in ef[ef.index("do") + 1] and "do" in ef[ef.index("do") + 1]:
				ef[ef.index("do") + 1][ef[ef.index("do") + 1].index("do") + 1].append(self.temp[1])
			else:
				ef[ef.index("do") + 1].append(self.temp[1])

		if e and m:
			d = e + ["do", m + ["do", ef]]
		elif e:
			if self.ee and all(eb in ef for eb in ("upto", "stock", "draw", "heal")):
				d = e + ["do", ef + ["upto"]]
			else:
				d = e + ["do", ef]
		else:
			d = e + ef

		if t.startswith("alarm"):
			d = ["alarm", "do", d]

		if p:
			if "give" in d:
				d.insert(d.index("give"), p[0])
				if len(p) == 2:
					d.insert(d.index(p[0]), p[1])
			elif "do" in d:
				if "if" in d:
					d.insert(d.index("if"), p[0])
				else:
					d.insert(d.index("do"), p[0])
				if len(p) == 2:
					d.insert(d.index(p[0]), p[1])
			elif "done" in d:
				if "if" in d:
					d.insert(d.index("if"), p[0])
				else:
					d.insert(d.index("done"), p[0])
				if len(p) == 2:
					d.insert(d.index(p[0]), p[1])
			else:
				d.append(p[0])
				if len(p) == 2:
					d.append(p[1])

		if cm:
			if "pay" in d and "do" in d:
				d[d.index("do") + 1].extend(cm)
			else:
				d.extend(cm)
		return d

	def condition(self, a, t, aa):
		b = []
		c = []
		if self.cond_rep[0]:
			self.cond[self.cond_rep[1][0]] = 0

		if "if there are no markers under this" in t or "if this does not have a marker under it" in t:
			b = ["markers", 0, "lower", "under"]
		elif "if there are  or more markers under this" in t or "and there are  or more markers under this" in t:
			b = ["markers", self.digit(a, self.cond[0]), "under"]
			self.cond[0] += 1
		elif "if there are  or fewer markers under this" in t:
			b = ["markers", self.digit(a, self.cond[0]), "lower", "under"]
			self.cond[0] += 1
		elif "if there is a marker under this" in t or "and there is a marker under this" in t:
			b = ["markers", 1, "under"]
		elif "if your level has a  card" in t and any(f"level has a {cc.lower()} card" in aa for cc in self.colour):
			b = ["experience", 1, "Colour", self.colour_t(a)]
			self.cond[1] += 2
		elif "this's soul is  or lower" in t:
			b = ["souls", self.digit(a, self.cond[0]), "lower"]
			self.cond[0] += 1
		elif "if this's battle opponent is level x or lower" in t:
			b = ["battleopp", "Level", "x", "lower"]
			if "x = the number of  in your waiting room" in t:
				b.extend(["xName=", self.name(a, self.cond[1], s='n'), "xWaiting"])

		if "if all your other characters have lower power than this" in t:
			c = [-2, "atkpwrchk", "lower", "self"]
		elif "if it is the first turn of the player who went first" in t:
			c = ["turn", 1]
		elif "if there are  or more climax cards in your opponent's waiting room" in t or "if your opponent's waiting room has  or more climax" in t:
			c = [self.digit(a, self.cond[0]), "more", "Climax", "Waiting", "opp"]
			self.cond[0] += 1
		elif "if your opponent's hand has  or more card" in t:
			c = [self.digit(a, self.cond[0]), "more", "Hand", "opp"]
			self.cond[0] += 1
		elif "if there is a climax in your opponent's climax area" in t:
			c = [1, "more", "Climax", "CX", "opp"]
		elif "if all your opponent's characters are rest" in t:
			c = [-1, "more", "Rest", "opp"]
		elif ("if there are no other rested character" in t or "if you have no other rested character" in t or "if you do not have another rest character" in t) and ("rested characters in your center stage" in t or "rested characters in the center stage" in t or "rest character in your center stage" in t):
			c = [0, "Rest", "Center", "other"]
		elif "if your opponent does not have any characters in his or her center stage" in t and "or if all characters in your opponent's center stage are reverse" in t:
			c = [-1, "more", "Reverse", "Center", "opp"]
		elif "if your opponent does not have any stand character" in t:
			c = [0, "more", "Stand", "opp", "lower"]
		elif "if there's  character opposite this" in t:
			c = ["opposite"]
		elif "if the number of cards in your deck is  or less" in t or " if there are  or fewer cards in your deck" in t:
			c = [self.digit(a), "more", "Library", "lower"]
			self.cond[0] += 1
		elif "if there are no cards in your stock" in t:
			c = [0, "more", "Stock", "lower"]
		elif "if the number of cards in your stock is  or less" in t or "if your stock has  or less cards" in t or "if there are  or fewer cards in your stock" in t:
			c = [self.digit(a, self.cond[0]), "more", "Stock", "lower"]
			self.cond[0] += 1
		elif "if there are  or more cards in your stock" in t:
			c = [self.digit(a, self.cond[0]), "more", "Stock"]
			self.cond[0] += 1
		elif "if there are  or fewer cards in your clock" in t:
			c = [self.digit(a, self.cond[0]), "more", "Clock", "lower"]
			self.cond[0] += 1
		elif "if there are exactly  cards in your clock" in t:
			c = [self.digit(a, self.cond[0]), "more", "Clock", "="]
			self.cond[0] += 1
		elif "if you have  or more climax cards in your waiting room" in t:
			c = [self.digit(a, self.cond[0]), "more", "Climax", "Waiting"]
			self.cond[0] += 1
		elif "if there are  or more  in your waiting room" in t:
			c = [self.digit(a, self.cond[0]), "more", "Name", self.name(a, self.cond[1], s='n'), "Waiting"]
			self.cond[0] += 1
			self.cond[1] += 2
		elif "if the character opposite this has no traits" in t:
			c = ["opposite", "OPtraits", 0, "OPlower"]
		elif "if the character opposite this is level  or higher" in t or "if the level of the character opposite this is  or higher" in t:
			self.cond[0] += 1
			c = ["opposite", "OPlevel", self.digit(a)]
		elif "if the character opposite this is level " in t or "if the card opposite this is level " in t or "and the character opposite this is level" in t or "if the level of the character opposite this is " in t:
			self.cond[0] += 1
			c = ["opposite", "OPlevel", self.digit(a), "OP=="]
		elif "if the level of the battle opponent of this is higher than the level of your opponent" in t or "if the level of this's battle opponent is higher than your opponent's level" in t:
			c = ["plevel", "antilvl", self.target, "opp"]
		elif "if your level is  or higher" in t or "if you are level  or higher" in t:
			c = ["plevel", self.digit(a, self.cond[0])]
			self.cond[0] += 1
		elif "if your level is " in t:
			c = ["plevel", self.digit(a, self.cond[0]), "=="]
			self.cond[0] += 1
		elif "if the total level of the cards in your level is  or higher" in t or "if the sum of levels of cards in your level zone is  or higher" in t or "if the sum of the levels of the cards in your level zone is  or more" in t or "and the sum of the levels of the cards in your level zone is  or more" in t:
			self.cond[0] += 1
			c = ["experience", self.digit(a)]
		elif "if  is in your level" in t or "and  is in your level" in t:
			c = ["experience", 1, "Name=", self.name(a, self.cond[1], s='n')]
			self.cond[1] += 2
		elif "if there are  or more  characters in your level zone" in t and "or more «" in aa:
			c = ["experience", self.digit(a, self.cond[0]), "Trait", self.trait(a, self.cond[2])]
			self.cond[2] += 1
			self.cond[0] += 1
		elif "if there are no face down cards in your opponent's memory" in t:
			c = [0, "more", "lower", "Memory", "Face-down", "opp"]
		elif " there isn't another  in your memory" in t:
			c = [0, "more", "lower", "other", "Name", self.name(a, self.cond[1], s='n'), "Memory"]
			self.cond[1] += 2
		elif "if there are no  cards in your memory" in t and any(f"no {cc.lower()} cards" in aa for cc in self.colour):
			c = [0, "more", "Colour", self.colour_t(a), "Memory", "lower"]
		elif "if your memory has  or more card" in t or "if there are  or more cards in your memory" in t or "if you have  or more cards in your memory" in t or "if you have  or more cards in memory" in t:
			c = [self.digit(a, self.cond[0]), "more", "Memory"]
			self.cond[0] += 1
		elif "if your memory has  or less card" in t or "if there are  or fewer cards in your memory" in t:
			if "\nif your memory has  or less card" in t and t.endswith("put this in your memory.") and not self.cond_later:
				self.cond_later = True
			else:
				c = [self.digit(a, self.cond[0]), "more", "Memory", "lower"]
				self.cond[0] += 1
		elif "if you have  character in your memory" in t:
			c = [self.digit(a, self.cond[0]), "more", "Memory", "Character"]
			self.cond[0] += 1
		elif "if there's a climax card in your opponent's memory" in t:
			c = [1, "more", "Memory", "Climax", "opp"]
		elif "if there is at least  card in your opponent's memory" in t:
			c = [self.digit(a, self.cond[0]), "more", "Memory", "opp"]
			self.cond[0] += 1
		elif "if the number of cards in your hand = or lower than the number of cards in your opponent's hand" in t:
			c = [self.digit(a), "more", "Hand", "HandvsOpp", "lower"]
			self.cond[0] += 1
		elif "if the number of cards in your hand is  or more" in t or "if your hand has  or more cards" in t or "if you have  or more cards in your hand" in t:
			c = [self.digit(a), "more", "Hand"]
			self.cond[0] += 1
		elif "and your hand has  or less cards" in t or "and you have less than  cards in your hand" in t:
			self.cond[0] += 1
			c = [self.digit(a), "more", "Hand", "lower"]
		elif "if there are fewer cards in your hand than your opponent's hand" in t:
			c = [0, "more", "Hand", "HandvsOpp", "fewer"]
		elif "if there are cards in your memory" in t:
			c = [1, "more", "Memory"]
		elif "if you have  card in memory" in t or "if you have  card in your memory" in t or "if there is  card in your memory" in t:
			c = [self.digit(a, self.cond[0]), "more", "Memory"]
			self.cond[0] += 1
		elif "you have a reverse character whose name includes either  or " in t:
			c = [1, "more", "CName&Reverse", f"{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}_Reverse"]
			self.cond[1] += 4
		elif "if you have a character with  in name" in t or "if you have  character with  in name" in t:
			c = [1, "more", "Name", self.name(a, self.cond[1], s='n')]
			self.cond[1] += 2
			if "if you have  character with  in name":
				self.cond[0] += 1
		elif "if you have another character with  in the name" in t or "if you have another card named  " in t or "if you have other characters named" in t:
			if "\"backup\"" in aa:
				c = [1, "more", "Name", self.name(a, self.cond[1] + 2, s='n'), "other"]
			else:
				c = [1, "more", "Name", self.name(a, self.cond[1], s='n'), "other"]
			self.cond[1] += 2
			if "\" and \"" in aa and "other characters named" in t:
				c[0] = 2
				c[c.index("Name") + 1] = f"{c[c.index('Name') + 1]}_{self.name(a, self.cond[1], s='n')}"
				c[c.index("Name")] = "&Name="
				self.cond[1] += 2

			if "named  in your center stage" in t:
				c.append("Center")
		elif ("if you have another character with  or " in t or "if you have another  or  character" in t or "if you have another character with either  or " in t or "and you have another  or  character" in t) and "» or «" in aa:
			c = [1, "more", "Trait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}", "other"]
			self.cond[2] += 2
		elif ("if you have  or more characters with  or " in t or "if you have  or more characters with  and/or " in t or "and you have  or more characters with  and/or " in t or "if you have  or more  or  character" in t) and ("» or «" in aa or "» and/or «" in aa):
			c = [self.digit(a, self.cond[0]), "more", "Trait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"]
			self.cond[0] += 1
			self.cond[2] += 2
		elif any(_ in t for _ in ("if you have  or more other characters with  or ", "if you have  or more other characters with  and/or ", "if you have  or more other characters with either  or ", "if you have  or more other  and/or  character", "and you have  or more other characters with  and/or ", "if you have  or more other  or  character", "and you have  or more other  or  character", "if the number of other  or  characters you have is  or more", "if the number of other  or  or  characters you have is  or more")):
			if "» or «" in aa or "» and/or «" in aa:
				c = [self.digit(a, self.cond[0]), "more", "Trait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}", "other"]
				if aa.count("» or «") >= 2:
					c[c.index("Trait") + 1] += f"_{self.trait(a, self.cond[2] + 2)}"
					self.cond[2] += 1
				self.cond[2] += 2
			elif "\" and/or \"" in aa or "\" or \"" in aa:
				c = [self.digit(a, self.cond[0]), "more", "Name", f"{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}", "other"]
				self.cond[1] += 4
			self.cond[0] += 1
		elif "if the number of cards named  in your memory is  or more" in t:
			c = [self.digit(a, self.cond[0]), "more", "Name=", self.name(a, self.cond[1], s='n'), "Memory"]
			self.cond[0] += 1
			self.cond[1] += 2
		elif "if there are  or more  characters in your memory" in t:
			c = [self.digit(a, self.cond[0]), "more", "Trait", self.trait(a, self.cond[2]), "Memory"]
			self.cond[0] += 1
			self.cond[2] += 1
		elif "if you have  or more other  characters" in t or "and you have  or more other  character" in t or "if the number of your other  characters is  or more" in t or "and the number of other  characters you have is  or more" in t or "if the number of other  characters you have is  or more" in t:
			c = [self.digit(a, self.cond[0]), "more", "Trait", self.trait(a, self.cond[2]), "other"]
			self.cond[0] += 1
			self.cond[2] += 1
			if "and the character opposite this is level" in t:
				c.extend(["do", ["opposite", "OPlevel", self.digit(a, self.cond[0]), "OP=="]])
				self.cond[0] += 1
		elif "if you have  or fewer other  characters" in t:
			self.cond[0] += 1
			self.cond[2] += 1
			c = [self.digit(a), "more", "Trait", self.trait(a), "other", "lower"]
		elif "if you have  or less other character" in t or "if the number of other characters you have is  or less" in t or "if you have  or fewer other character" in t:
			self.cond[0] += 1
			c = [self.digit(a), "more", "other", "lower"]
		elif "if the number of  characters you have is  or more" in t or "if you have  or more  character" in t or "and you have  or more  characters" in t:
			c = [self.digit(a, self.cond[0]), "more", "Trait", self.trait(a, self.cond[2])]
			self.cond[0] += 1
			self.cond[2] += 1
		elif "if the number of your other  characters you have is  or more" in t:
			c = [self.digit(a, self.cond[0]), "more", "Trait", self.trait(a, self.cond[2]), "other"]
			self.cond[0] += 1
			self.cond[2] += 1
		elif "if  is in your waiting room" in t:
			c = [1, "more", "Name", self.name(a, self.cond[1], s='n'), "Waiting"]
			self.cond[1] += 2
		elif "if  is in your memory" in t or "and  is in your memory" in t:
			if "\"backup\"" in aa:
				c = [1, "more", "Name=", self.name(a, self.cond[1] + 2, s='n'), "Memory"]
			else:
				c = [1, "more", "Name=", self.name(a, self.cond[1], s='n'), "Memory"]
			self.cond[1] += 2
		elif "if you have another  character" in t or "and you have another  character" in t:
			c = [1, "more", "Trait", self.trait(a, self.cond[2]), "other"]
			self.cond[2] += 1
		elif "if your opponent has a \"" in aa or "if your opponent has a character named \"" in aa:
			c = [1, "more", "Name=", self.name(a, self.cond[1], s='n'), "opp"]
			self.cond[1] += 2
		elif "if your opponent has  character named" in t:
			c = [self.digit(a, self.cond[0]), "more", "Name=", self.name(a, self.cond[1], s='n'), "opp"]
			self.cond[1] += 2
			self.cond[0] += 1
		elif "if there is  or fewer characters in your opponent" in t:
			c = [self.digit(a, self.cond[0]), "more", "opp", "lower"]
			self.cond[1] += 2
			self.cond[0] += 1
			if "fewer characters in your opponent's center stage" in t:
				c.append("Center")
		elif "if you have a  character" in t:
			c = [1, "more", "Trait", self.trait(a, self.cond[2])]
			self.cond[2] += 1
		elif "if you have another ," in t or "and you have another ," in t or "if have another ," in t:
			c = [1, "more", "Name", self.name(a, self.cond[1], s='n'), "other"]
			self.cond[1] += 2
		elif "if you do not have \"" in aa:
			c = [0, "more", "Name", self.name(a, self.cond[1], s='n'), "other", "lower"]
			self.cond[1] += 2
			if "this cannot be played from your hand" in t and t.index("if you do not have ") < t.index("this cannot be played from your hand"):
				c = []
		elif "if you have no other character" in t:
			c = [0, "more", "Character", "other", "lower"]
		elif "you have a level  or higher  character" in t:
			c = [1, "more", "Trait&L", f"{self.trait(a, self.cond[2])}_>={self.digit(a, self.cond[0])}"]
			self.cond[2] += 1
			self.cond[0] += 1
		elif ("if all your characters are  and/or " in t or "if all your characters are either  or " in t or "and all your characters have  and/or " in t or "if all your characters are  or " in t) and ("» or «" in aa or "» and/or «" in aa):
			c = [-1, "more", "Trait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"]
			self.cond[2] += 2
		elif any(f"if all your characters are either {cl} or «" in aa for cl in self.colour):
			c = [-1, "more", "CColourT", f"{self.colour_t(a)}_{self.trait(a, self.cond[2])}"]
			self.cond[2] += 1
		elif "if all your characters are «" in aa or "and all your characters are «" in aa:
			c = [-1, "more", "Trait", self.trait(a, self.cond[2])]
			self.cond[2] += 2
		elif "if your opponent's center stage has  or less characters" in t or "if the number of characters in your opponent's center stage is  or less" in t:
			c = [self.digit(a, self.cond[0]), "more", "opp", "Center", "lower"]
			self.cond[0] += 1

		if self.cond_rep[0]:
			self.cond[self.cond_rep[1][0]] = self.cond_rep[1][1]
			self.cond_rep = [False, []]

		if b and c:
			b.extend(["do", c])
			c = b
		elif b and not c:
			c = b

		if c:
			if not self.cond_later:
				if "do" in c:
					c[c.index("do") + 1].append("do")
				else:
					c.append("do")
			return c
		else:
			return []

	def convert(self, a, t, aa=""):
		if aa == "":
			aa = self.a_replace(a)
		if "until the next end of your opponent's turn" in t or "until the end of your opponent's next turn" in t or "until end of your opponent's next turn" in t or "until the end of the turn after the current turn" in t or "until the end of the next turn" in t:
			x = 2
			if self.opnextturn:
				x += 1
		elif "until the end of your next stand phase" in t:
			x = 3
		elif "for the turn" in t or "until end of turn" in t or "\" for the turn." in aa:
			x = 1
		else:
			x = 1
		t1 = ""
		b = []
		c = []
		cc = False
		cd = []
		gg = []
		d = []
		e = []
		f = []
		g = []
		h = []
		i = []

		if "rest  of your standing character" in t or "rest  of your  character" in t or "choose  of your characters and rest them" in t:
			f = [self.digit(a, self.cond[0]), "rest", "Stand"]
			self.cond[0] += 1

			if "standing characters with  in name" in t:
				f.extend(["Name", self.name(a, self.cond[1], s='n')])
				self.cond[1] += 2
			elif "standing characters with  or " in t and "» or «" in aa:
				f.extend(["Trait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"])
				self.cond[2] += 2
			elif "rest  of your  character" in t and (" of your «" in aa and "» character" in aa):
				f.extend(["Trait", self.trait(a, self.cond[2])])
				self.cond[2] += 1

			if "if you rest " in t:
				f.extend(["if", self.digit(a, self.cond[0])])
				self.cond[0] += 1

				if "those characters do not stand during your next stand phase" in t.split("if you rest")[0] or "those characters cannot stand during your next stand phase" in t.split("if you rest")[0]:
					f.extend(["extra", "do", [-16, "[CONT] This cannot [STAND] during your stand phase", 3, "give"]])

				t = t.split("if you rest")[1]
			elif "if you do" in t or "if so" in t:
				f.extend(["if", f[0]])
				if "if you do" in t:
					t = t.split("if you do")[1]
				elif "if so" in t:
					t = t.split("if so")[1]
		elif ("put the top card of your deck" in t and ("deck in your stock" in t or "deck into stock" in t or "deck to your stock" in t or "deck in stock" in t)) or "choose the top card of your deck and put it in your stock" in t:  
			f = ["stock", 1]
			if "put this in your stock" in t:
				ts = "put this in your stock"
				if "put the top card of your deck in your stock" in t:
					tt = "put the top card of your deck in your stock"
				if t.index(ts) < t.index(tt):
					h = list(f)
					f = []
		elif ("put up to  cards from the top of your deck" in t or "put up to  card from the top of your deck" in t or "put up to  cards from top of your deck" in t or "put up to  card from top of your deck" in t) and ("top of your deck to your stock" in t or "top of your deck in your stock" in t or "top of your deck in stock" in t):
			if "draw up to  card" in t:
				tt = "draw up to  card"
				ts = "put up to  card"
				if t.index(tt) < t.index(ts):
					gg, t = self.seperate(ts, a, t, aa, True)
					g = gg
			f = ["drawupto", self.digit(a, self.cond[0]), "Stock"]
			self.cond[0] += 1
		elif "put up to x cards from top of your deck in your stock" in t:
			f = ["drawupto", "x", "Stock"]
			if "x = level of that character" in t:
				if self.xx is not None:
					f[1] = self.xx
		elif "declare any number equal to or less than the number of markers underneath this" in t:
			f = ["numbers", "markers"]
			if "that character gets + power and +x soul" in t:
				if "x = the number you declared" in t:
					f.extend(["do", [-3, self.digit(a, self.cond[0]), x, "power", "target", self.target, "extra", "do", [-16, "x", x, "soul", "xdeclare"]]])
				t = t.split("that character gets + power and +x soul")[1]
		elif "declare a number of your choice" in t or "declare any number" in t:
			f = ["numbers", "any"]
			if "your opponent chooses  card in their hand" in t:
				g = ["discard", self.digit(a, self.cond[0]), "", "Reveal", "oppturn"]
				self.cond[0] += 1
				if t.index("your opponent chooses  card in their hand") < t.index("declare any number"):
					g.extend(["afterreveal"])
					f.append("nowreveal")
				if "if that card's power is the same as the number you declared" in t:
					f.extend(["if", "ifpowerrevealvsdeclare", "if="])
		elif "your opponent declares  or  or " in t:
			f = ["numbers", [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), self.digit(a, self.cond[0] + 2)], "oppturn"]
			self.cond[0] += 3
			if " or  or  or " in t:
				f[1].append(self.digit(a, self.cond[0]))
				self.cond[0] += 1
		elif self.ablt < 0 and "your opponent puts that character from their memory in any position of their stage" in t:
			f = [-38, "msalvage", "", "Stage", "Opp", "oppturn", "opp"]
		elif self.ablt < 0 and "your opponent returns that card to their hand" in t:
			f = [-38, "msalvage", "", "Opp", "oppturn", "opp"]
		elif self.ablt < 1 and "put that card face up" in t:
			f = [-38, "flipper", "", "up"]

		if "you may return this to your hand" in t and "if you do" in t and t.index("you may return this to your hand") < t.index("if you do"):
			d = [0, "hander", "upto"]
			t = t.replace("you may return this to your hand", "")
		elif "put the top  cards of your deck in your waiting room" in t or "put the top  cards of your deck in the waiting room" in t or "put  cards from the top of your deck in your waiting room" in t:
			d = ["mill", self.digit(a, self.cond[0]), "top", "fix"]
			self.cond[0] += 1
			if "if there is a climax among those card" in t and "if there is an event among those card" in t:
				d.extend(["if", "Climax", 1, "extra1"])
				tt = "if there is a climax among those card"
				ts = "if there is an event among those card"
				if t.index(tt) < t.index(ts):
					t1 = f"{ts}{t.split(ts)[1]}"
					t = t.split(ts)[0]
					d.extend(["done", ["mill", -20, "if", "Event", 1, "do", self.convert(a, t1, aa)]])
			elif "if all cards put in the waiting room this way are  characters" in t or "if all those cards are  characters" in t:
				d.extend(["Trait", self.trait(a, self.cond[2]), "if", "all"])
				self.cond[2] += 1
			elif "if there is a climax among those cards" in t or "if there's a climax card among them" in t or "if there is a climax revealed among those card" in t:
				d.extend(["payafter", "if", "Climax", 1])
				if "a climax among those card" in t:
					t = t.split("a climax among those card")[1]
				elif "a climax card among them" in t:
					t = t.split("a climax card among them")[1]
			elif "if there were at least  climax card among them" in t or "if there is at least  climax card among them" in t:
				d += ["if", "Climax", self.digit(a, self.cond[0])]
				self.cond[0] += 1
				t = t.split("at least  climax card among them")[1]
			elif "if there is a level  or lower character among those cards" in t or "if there is a level  or lower character revealed among" in t:
				d.extend(["if", "lvl", self.digit(a, self.cond[0]), "lower", "Character", "any"])
				self.cond[0] += 1
			elif "if there is a level  or higher card among those card" in t:
				d.extend(["if", "lvl", self.digit(a, self.cond[0]), "any"])
				self.cond[0] += 1
			elif "if there is  or more  characters among those card" in t or "if there are  or more  characters among those card" in t:
				d.extend(["if", "Trait", self.trait(a, self.cond[2]), self.digit(a, self.cond[0]), "anyx"])
				ts = "if there is  or more  characters among those card"
				tt = "if there are  or more  characters among those card"
				if t.count(ts) == 1 and t.count(tt) == 2:
					d.append("extra1")
				self.cond[0] += 1
				self.cond[2] += 1

				if t.count(ts) == 1 and t.count(tt) == 2:
					t2 = f"{tt}{t.split(tt)[2]}"
					t1 = f"{tt}{t.split(tt)[1]}"
					t = t.split(tt)[0].split(ts)[1]
					k = ["do", self.convert(a, t, aa)]
					if "you may" not in t:
						self.no_pay = True
					t = ""
					_ = ["if", "Trait", self.trait(a, self.cond[2]), self.digit(a, self.cond[0]), "anyx", "extra1"]
					self.cond[0] += 1
					self.cond[2] += 1
					h = ["mill", -20] + _ + ["do", self.convert(a, t1, aa)]
					_ = ["if", "Trait", self.trait(a, self.cond[2]), self.digit(a, self.cond[0]), "anyx"]
					self.cond[0] += 1
					self.cond[2] += 1
					j = ["do", ["mill", -20] + _ + ["do", self.convert(a, t2, aa)]]
					h[h.index("do") + 1].extend(j)
					d.extend(k)

			if "x = the total level of the cards put in your waiting room" in t or "x equals the number of level  or lower characters moved to the waiting room" in t or "x = sum of levels of cards put in the waiting room" in t or "x = the total level of those card" in t:
				d.extend(["if", "extra"])
			elif "» or «" in aa and ("x =  times # of characters with either  or  among those cards" in t or "x = the number of  or  characters among those card" in t):
				d += ["pwr", "x#", "ctrait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}", "if"]
				self.cond[2] += 2
			elif "x = the number of  characters among those card" in t or "x =  times # of  characters among those card" in t or "x =  multiplied by the number of  characters revealed among those card" in t:
				d += ["pwr", "x#", "ctrait", self.trait(a, self.cond[2]), "if"]
				self.cond[2] += 1
			elif "x =  times # of characters that are either  or  among those card" in t:
				d += ["pwr", "x#", "cCColourT", f"{self.colour_t(a)}_{self.trait(a, self.cond[2])}", "if"]
				self.cond[2] += 1
			elif "for each soul trigger icon those cards have" in t:
				d.extend(["if", "extra"])

			if "reveal the top  cards of your deck" in t:
				gg, t = self.seperate("reveal the top  cards of your deck", a, t, aa)
				c.extend(gg)
		elif "put the top card of your deck in your waiting room" in t or "put the top card of your deck in the waiting room" in t or "put  card from the top of your deck in your waiting room" in t:
			d = ["mill", 1, "top"]
			if "put  card from the top of your deck" in t:
				self.cond[0] += 1
			if "if that card's level is the number your opponent declared" in t:
				d.extend(["xdeclare", "Level", "==x", "if", 1])
			elif "for each soul trigger icon on the card put in your waiting room" in t:
				d.extend(["if", "extra"])
			elif "» or «" in aa and ("if it's  character with  or " in t or "if that card is a  or  character" in t):
				d.extend(["Trait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}", "any", "if"])
				self.cond[2] += 2
			elif "that card is a  character" in t or "if it's a  character" in t or "if it is a  character" in t:
				if "if" in d:
					d.remove("if")
				d.extend(["Trait", self.trait(a, self.cond[2]), "any", "if"])
			elif "that card is a level  or lower" in t or "if it's a level  or lower" in t or "if that card is level  or lower" in t:
				d.extend(["lvl", self.digit(a, self.cond[0]), "lower", "any", "if"])
				self.cond[0] += 1
				if "or lower character" in t:
					d.insert(d.index("lower"), "Character")
				if "put that character on any position of your back stage" in t or "put that character in any slot in the back stage" in t or "put it on any position of your back stage" in t or "put that character in any position of your back stage" in t:
					d.extend(["extra", "do", [-16, "salvage", "ID=_x", "Stage", "Back"]])
					if "that character gets «" in aa:
						d[d.index("do") + 1].extend(["extra", "do", [-16, self.trait(a, self.cond[2]), x, "trait"]])
						self.cond[2] += 1
			elif "that card is level  or higher" in t or "if it's level  or higher" in t or "if that card is a level  or higher" in t:
				d.extend(["lvl", self.digit(a, self.cond[0]), "any", "if"])
				self.cond[0] += 1
				if "or higher character" in t:
					d.insert(d.index("any"), "Character")
			elif "if it's a level  character" in t:
				d.extend(["lvl", self.digit(a, self.cond[0]), "Character", "==", "any", "if"])
				self.cond[0] += 1
			elif "if it's a climax card" in t or "if that card is a climax" in t:
				d.extend(["if", "Climax", 1])
			elif "if that card is  character" in t:
				d.extend(["if", "Character", self.digit(a, self.cond[0])])
				self.cond[0] += 1
				if "with the same level as that" in t:
					d.append("extra")
			if "x = the level of that card" in t or "x = level of the card" in t:
				d.extend(["if", "extra"])
			if "you may pay the cost" in t:
				tt = "put the top card of your deck"
				ts = "you may pay the cost"
				if t.index(tt) < t.index(ts):
					d.append("payafter")
			if "you may put the top card of your deck in your waiting room" in t:
				if "if" in d:
					d.insert(d.index("if"), "upto")
				elif "do" in d:
					d.insert(d.index("do"), "upto")
				else:
					d.append("upto")
				if "payafter" in d:
					d[d.index("payafter")] = "confirmpayafter"
		elif "put the top card of your opponent's deck in your opponent's waiting room" in t:
			d = ["mill", 1, "top", "opp"]
			if "if that card is  character" in t:
				d.extend(["if", "Character", self.digit(a, self.cond[0])])
				self.cond[0] += 1
				if "with  or more of the same trait as that character" in t:
					d.extend(["extra"])
		elif "put the bottom  cards of your opponent's deck into their waiting room" in t or "put the bottom  cards of your opponent's deck in their waiting room" in t or "put the bottom  cards of your opponent's deck in the waiting room" in t:
			d = ["mill", self.digit(a, self.cond[0]), "bottom", "opp", "fix"]
			self.cond[0] += 1
			if "x = the number of climax among those card" in t or "x is the number of climax cards among those card" in t or "x = # of climax cards among those card" in t or "x = # of climax cards among them" in t or "x = the number of climax among those card" in t:
				d.extend(["if", "extra"])
		elif "put the top card of your opponent's deck in his or her stock" in t:
			d = ["mill", 1, "top", "opp", "Stock"]
		elif "put the top card of your stock in the waiting room" in t:
			d = ["distock", 1, "top"]
			if "if so" in t:
				d.extend(["if", 1])
		elif "put the top card of your opponent's stock in the waiting room" in t:
			d = ["distock", 1, "top", "opp", "if", 1]
		elif "flip over the top  cards of your deck" in t or "flip over  cards from the top of your deck" in t or ("reveal  cards from the top of your deck" in t and "put them in your waiting room" in t):  
			d = ["brainstorm", self.digit(a, self.cond[0])]
			self.cond[0] += 1
			if "if there is a climax with" in t and ("trigger icon among them" in t or "in its trigger icon among those cards" in t):
				d.extend(["Trigger", "", "any", 1])
				if "with draw in its trigger" in t or "with draw trigger" in t:
					d[3] = "draw"
			elif "if there is at least  climax card among them" in t:
				d.extend(["Climax", "any", 1])
			elif "if there is at least   among them" in t:
				d.extend(["Name=", self.name(a, self.cond[1], s='n'), "any", self.digit(a, self.cond[0] + 1)])
				self.cond[0] += 1
				self.cond[1] += 2
			elif "x = the number of  characters revealed among those cards" in t or "x = the number of  characters revealed" in t:
				d.extend(["Trait", self.trait(a, self.cond[2]), "any", 0])
				self.cond[2] += 1
			elif "for each climax card revealed this way" in t or "for each climax revealed" in t or "x = number of climax cards revealed this way" in t or "x =  times the number of climax cards revealed this way" in t:
				d.extend(["Climax"])
			elif "for each  character revealed among those cards" in t:
				d.extend(["Trait", self.trait(a, self.cond[2]), "each"])
				self.cond[2] += 1
			elif "for each  or  revealed among those card" in t and "\" or \"" in aa:
				d.extend(["Name=", f"{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}", "each"])
				self.cond[1] += 4
		elif "reveal up to  cards from the top of your deck" in t or "reveal up to  cards from top of your deck" in t:
			d = ["drawupto", self.digit(a, self.cond[0]), "Reveal"]
			self.cond[0] += 1
			if "if you reveal  or more card" in t or "if you revealed  or more card" in t or "if you reveal at least  card this way" in t:
				d.extend(["if", self.digit(a, self.cond[0])])
				self.cond[0] += 1
			if "put it in your hand" in t:
				d.extend(["do", []])
				if "» or «" in aa and "choose up to  character with  or  from among them" in t or "choose up to   or  character from among them" in t:
					d[d.index("do") + 1].extend([self.digit(a, self.cond[0]), "search", f"Trait_{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}", "Reveal", "upto", "show"])
					self.cond[0] += 1
					self.cond[2] += 2
				elif "choose up to   character from among them" in t or "choose up to   character among them" in t:
					d[d.index("do") + 1].extend([self.digit(a, self.cond[0]), "search", f"Trait_{self.trait(a, self.cond[2])}", "Reveal", "upto", "show"])
					self.cond[0] += 1
					self.cond[2] += 1
				d = self.discard_card(d, a, t)
		elif "reveal the top  cards of your deck" in t:
			d = [self.digit(a, self.cond[0]), "reveal", "top"]
			self.cond[0] += 1
			if ("put it in your hand" in t or "put it in your hand" in t) and ("put the rest in the waiting room" in t or "put the rest in your waiting room" in t):
				if "your opponent chooses  character or  event among those card" in t or "your opponent chooses  character or  event from them" in t:
					d.extend(["do", [self.digit(a, self.cond[0]), "salvage", "Character_Event", "oppturn", "opp", "Revealed"]])
					self.cond[0] += 2
					if "you choose up to  card from the other cards revealed this way" in t and "put it on top of the deck" in t:
						d[d.index("do") + 1].extend(["exReveal", "do", [self.digit(a, self.cond[0]), "salvage", "", "Library", "top", "upto", "Revealed"]])
						self.cond[0] += 1
				elif "your opponent chooses  character or event from among them" in t or "your opponent chooses  event or character from among them" in t:
					d.extend(["do", [self.digit(a, self.cond[0]), "salvage", "Character_Event", "oppturn", "opp", "Revealed"]])
					self.cond[0] += 1
			if "x = the number of standby trigger icons among those card" in t:
				d.append("xreveals")
			if "shuffle your deck" in t and "put the revealed cards back" in t:
				d.append("shuff")
		elif "reveal the top card of your deck" in t:
			tc = "reveal the top card of your deck"
			tt = ""
			if "rest this" in t:
				tt = "rest this"
			elif "choose  level  or lower character" in t:
				tt = "choose  level  or lower character"
			elif "choose up to   in your waiting room" in t:
				tt = "choose up to   in your waiting room"
			if tt:
				if t.index(tt) < t.index(tc):
					gg, t = self.seperate(tc, a, t, aa, True)
					g = gg
				tt = ""
			d = [-9, "reveal"]
			if "if that card is  character of the level that your opponent declared" in t:
				d.extend(["CLevel", "==x", "xdeclare"])
				self.cond[0] += 1
			elif "if that card is a  or  character, or " in t or "if that card is a character with  or , or " in t or "if that card is  character with  or , or " in t or ("reveal the top card of your deck" in t and "» or «" in aa and "\" or " in aa):
				d.extend(["TTName", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}_{self.name(a, self.cond[1], s='n')}"])
				self.cond[2] += 2
				self.cond[1] += 2
				if "card is  character with" in t:
					self.cond[0] += 1
			elif "if that card is an event or   or  character" in t and "» or «" in aa and "\" or " not in aa:
				d.extend(["TraitE", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"])
				self.cond[2] += 2
				self.cond[0] += 1
			elif ("if the revealed card is a  or  character" in t or "if it's  character with  or " in t or "if that card is a  or  character" in t or "if that card is a  or  or  character" in t) and "» or «" in aa:
				d.extend(["Trait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"])
				if aa.count("» or «") == 2:
					d[d.index("Trait") + 1] += f"_{self.trait(a, self.cond[2] + 2)}"
					self.cond[2] += 1
				self.cond[2] += 2
			elif ("if it's either a  character or  event" in t or "if that card is an event or   character" in t) and "» character" in aa:
				d.extend(["TraitE", self.trait(a, self.cond[2])])
				self.cond[2] += 1
				self.cond[0] += 1
			elif "if it's a climax" in t or "if the revealed card is a climax" in t:
				d.extend(["Climax"])
			elif "if that card is not a  character" in t or "if it's not a  character" in t or "revealed card is not a  character" in t:
				d.extend(["Trait", self.trait(a, self.cond[2]), "not", "if"])
				self.cond[2] += 1
				if "put that card in your hand" in t and "if that card is not a  character" in t and "choose  card in your hand" in t and "put it in your waiting room" in t:
					ts = "put that card in your hand"
					tt = "if that card is not a  character"
					t1 = "choose  card in your hand"
					if t.index(ts) < t.index(tt) < t.index(t1):
						d.remove("not")
						d.remove("if")
						d.extend(["do", ["draw", 1], "isnot", ["draw", 1, "do", ["discard", self.digit(a, self.cond[0]), ""]]])
						self.cond[0] += 1
			elif "if that card is a  character" in t or "if it is a  character" in t or "if the revealed card is a  character" in t or "if that's a  character" in t or "if it's a  character" in t:
				d.extend(["Trait", self.trait(a, self.cond[2])])
				self.cond[2] += 1
				if "if it's a  character or " in t and "or \"" in aa:
					d.extend(["Name", self.name(a, self.cond[1], s='n')])
					self.cond[1] += 2
				if "character whose level is lower than or equal to your level" in t:
					d.extend(["Level", "<=p"])
			elif "if it's a character with  in name" in t or "if it's  character with  in name" in t:
				d.extend(["Name", self.name(a, self.cond[1], s='n')])
				self.cond[1] += 2
			elif "if it's level  or lower" in t or "if that card is level  or lower" in t or "if it's a level  or lower" in t or "if that card is a level  or lower" in t:
				if "if it is not" in t:
					t = self.isnot_filter(t)
				d.extend(["Level", self.digit(a, self.cond[0]), "lower"])
				if "or lower character" in t:
					d.insert(d.index("lower"), "Character")
				self.cond[0] += 1
			elif "if it's level  or higher" in t or "if that card is level  or higher" in t:
				d.extend(["Level", self.digit(a, self.cond[0])])
				self.cond[0] += 1
			elif "if it's a cost  or lower" in t:
				d.extend(["Cost", self.digit(a, self.cond[0]), "lower"])
				if "or lower character" in t:
					d.insert(d.index("lower"), "Character")
				self.cond[0] += 1
			elif "if it's a  card" in t and any(f"if it's a {cc} card" in aa for cc in self.colour):
				d.extend(["Colour", self.colour_t(a)])
			elif "x = the level of the revealed card" in t or "x is the number of soul trigger icons on that card" in t or "x = that card's level" in t:
				d.append("continue")

			if "if it's  character" in t:
				self.cond[0] += 1

			if "may pay the cost" in t and t.index(tc) < t.index("may pay the cost"):
				d.append("payafter")

			if "if it's not" in t and "(if it is not" not in t and "not" not in d:
				t = self.isnot_filter(t)
			elif " otherwise" in t and t.count("deal  damage to your opponent") > 1:
				t = self.isnot_filter(t, otherwise=True)

			if "put it in your hand" in t:
				d.extend(["do", ["draw", 1]])
				d = self.discard_card(d, a, t)
			elif "put it in your clock" in t or "put it in clock" in t:
				d.append("clock")
				if "if" in d:
					d.remove("if")
			elif "put it on the bottom of your deck" in t:
				if "x = that card's level" in t:
					d.append("extra")
				d.extend(["do", [-9, "decker", "bottom"]])
			elif "put it in stock" in t or "put it in your stock" in t or "put that card to your stock" in t:
				d.extend(["do", ["stock", 1]])
			elif "put it face down under this as a marker" in t or "put it face-down under this as marker" in t:
				d.extend(["do", [1, "marker", "top"]])
			elif "put that character in any slot on your stage" in t or "put it on any position of your stage" in t or "put that character in any slot on the stage" in t:
				d.extend(["payafter", "do", [-9, "search", "", "Stage", "topdeck"]])
			elif "put up to x cards from the top of your deck in your stock" in t:
				if "x =  times the number that your opponent declared" in t:
					d.extend(["do", ["drawupto", "x", "Stock", "xdeclare*", self.digit(a, self.cond[0])]])
					self.cond[0] += 1
			elif "discard  card at random from your hand to the waiting room" in t:
				d.extend(["do", ["discard", self.digit(a, self.cond[0]), "", "random"]])
				self.cond[0] += 1
			elif "at the beginning of your encore step" in t:
				d.extend(["do", [0, self.name(a, s='ay'), 1, "give"]])
				t = t.split("at the beginning of your encore step")[0]
		elif "reveal up to  climax card in your hand" in t:
			d = ["discard", self.digit(a, self.cond[0]), "Climax", "Reveal", "upto"]
			self.cond[0] += 1
			if "swap them" in t and "choose  climax card in your waiting room" in t and 'with a different color than the card revealed' in t:
				d.extend(["extra", "if", d[1], "do", [self.digit(a, self.cond[0]), "salvage", "ColourCx_x", "xcolourdiff", "xResonance", "swap", "Hand", "Resonance", "show"]])
				t = t[t.index("swap them") + len("swap them"):]
		elif "all players return cards in their waiting room to their decks" in t or "all players return cards in their waiting rooms to their respective decks" in t or "each player returns all cards in the waiting room to his or her deck" in t:
			if "shuffle their respective decks" in t or "shuffle them" in t or "shuffles his or her deck" in t:
				d = [-1, "shuffle", "both"]
		elif "return all cards except that card in your waiting room to your deck" in t:
			if "shuffle your deck" in t:
				if "choose  card in your waiting room" in t:
					d = [self.digit(a, self.cond[0]), "salvage", "", "nogain", "extra", "do", [-1, "shuffle", "w/oextra"]]
					self.cond[0] += 1
					t = t.replace("choose  card in your waiting room", "")
		elif "return all cards from your waiting room to your deck" in t or "return all cards in your waiting room to your deck" in t or "return all cards in your waiting room to the deck" in t or "return all cards from your waiting room to the deck" in t:
			if "shuffle your deck" in t:
				d = [-1, "shuffle"]
		elif "your opponent returns all cards in their waiting room to the deck" in t or "return all cards in your opponent's waiting room in your opponent's deck" in t:
			if "shuffle that deck" in t or "shuffles his or her deck" in t:
				d = [-1, "shuffle", "opp"]
		elif "returns all other cards in their waiting room to their deck" in t or "returns all cards from their waiting room except that card to their deck" in t or "returns all cards in their waiting room except that card to their deck" in t:
			if "shuffles their deck" in t:
				if "your opponent chooses  climaxes in their waiting room" in t or "your opponent chooses  climax in their waiting room" in t:
					d = [self.digit(a, self.cond[0]), "salvage", "Climax", "oppturn", "opp", "Opp", "nogain", "extra", "do", [-1, "shuffle", "opp", "w/oextra"]]
					self.cond[0] += 1
		elif "return all your standing characters in your center stage to your hand" in t:
			d = [-1, "hander", "Standing", "Center"]
			if "if at least  character was returned this way" in t:
				d.extend(["if", self.digit(a, self.cond[0])])
				self.cond[0] += 1
		elif "discard your hand and put all your stock in the waiting room" in t:
			d = ["discard", -1, "", "ifcount", "do", ["distock", -1, "top", "ifcount", "if", self.digit(a, self.cond[0]), "iftotal"]]
			self.cond[0] += 1
		elif "put all cards in your stock in your waiting room" in t:
			d = ["distock", -1, "top"]
		elif "choose up to  of your other  character" in t:
			if "stand it" in t:
				d = [self.digit(a, self.cond[0]), "stand", "Trait", self.trait(a, self.cond[2]), "Other", "upto"]
				self.cond[0] += 1
				self.cond[2] += 1

		if "all cards in your hand to the deck" in t:
			c = ["discard", -1, "", "Library"]
			if "draw the same number of cards" in t:
				c.extend(["ifcount", "do", [0, "shuffle", "do", ["draw", "x", "xifcount"]]])
		elif "play rock-paper-scissors with your opponent until someone wins" in t or ("play  with your opponent until someone wins" in t and "play \"rock-paper-scissors\" with your opponent" in aa):
			c = ["janken", "winner"]
			if "the winner draws  card" in t or "winner draws  card" in t:
				c.extend(["do", ["draw", self.digit(a, self.cond[0])]])
		elif "all players declare \"" in aa:
			if not g and ("and all players agree" in t or "and everyone agrees" in t):
				g = ["confirm", "both"]
			c = ["declare", "text", self.name(a, self.cond[1], s='n'), "all"]
			self.cond[1] += 2
		elif "you may declare \"" in aa:
			c = ["declare", "text", self.name(a, self.cond[1], s='n')]
			self.cond[1] += 2
		elif "high-five" in t and "everyone draws  card" in t:
			if not g and ("and all players agree" in t or "and everyone agrees" in t):
				g = ["confirm", "both"]
			c = ["declare", "five", "do", ["draw", self.digit(a, self.cond[0]), "do", ["draw", self.digit(a, self.cond[0]), "opp"]]]
			self.cond[0] += 1
		elif "shift, level" in t:
			c = ["shift", self.digit(a, self.cond[0]), "do", ["discard", 1, "Colour_x", "swap", "Clock", "xshift", "upto"]]
		elif "you may attack with up to  characters during this turn" in t:
			c = ["d_atk", self.digit(a, self.cond[0])]
			self.cond[0] += 1
		elif "choose this and  character in your waiting room" in t and "and exchange them" in t:
			c = [self.digit(a, self.cond[0]), "salvage", "Character", "swap", "Clock", "upto", "this"]
			self.cond[0] += 1
		elif "all players perform the following action" in t:
			c = ["perform", 1, self.name(a, s='p'), "both"]
		elif "perform a trigger check  times on the trigger step" in t or "trigger check  times during this attack's trigger step" in t or "trigger check  times during the trigger step" in t:
			c = ["trigger", self.digit(a, self.cond[0])]
		elif "perform  of the following  effects" in t or (("choose  of the following effect" in t or "choose  of the following  effect" in t or "choose  of the  following effect" in t or "choose  of the following abilit" in t) and "perform it" in t) or "perform the following  effects" in t or "perform each of the following  effects once in any order of your choice" in t or "do the following  actions once each in any order" in t or "perform each of the following abilities  time in any order" in t:
			if "stand this" in t:
				tt = "stand this"
				ts = "perform the following  effect"
				if t.index(tt) < t.index(ts):
					gg, t = self.seperate(ts, a, t, aa, True)
					g = gg
			if "this cannot be played from your hand" in t:
				t = t.split("this cannot be played from your hand")[1]
			if "if not" in t or "if you do not" in t:
				t = self.donot_filter(t)

			if "perform the following effects in any order" in t or "perform each of the following abilities  time in any order" in t:
				c = ["perform", 0, "", "choice", 0]
			elif "perform each of the following  effects once" in t:
				c = ["perform", self.digit(a, self.cond[0]), "", "choice", self.digit(a, self.cond[0])]
			elif "perform the following  effects" in t:
				c = ["perform", self.digit(a, self.cond[0]), "", "choice", self.digit(a, self.cond[0])]
			elif "choose  of the following abiliti" in t or "choose  of the following effect" in t:
				c = ["perform", self.digit(a, self.cond[0]), "", "choice", 0]
			else:
				c = ["perform", self.digit(a, self.cond[0]), "", "choice", self.digit(a, self.cond[0] + 1)]
				self.cond[0] += 1

			if "following  effect" in t or "  following effects" in t:
				rr = self.digit(a, self.cond[0])
			else:
				rr = int(a.count("\"") / 2)
				if "[CXCOMBO]" in a:
					rr -= 1
				if "  is in your level" in t and "\" is in your level" in aa:
					rr -= 1
				if "resonate [reveal 1 \"" in aa:
					rr -= 1
				if "choose  of the following abiliti" in t or "choose  of the following effect" in t:
					c[c.index("choice") + 1] = rr
				elif "perform the following effects in any order" in t or "perform each of the following abilities  time in any order" in t:
					c[c.index("choice") + 1] = rr
					c[c.index("perform") + 1] = rr

			for r in range(rr):
				if r == 0:
					c[2] += f"{self.name(a, self.cond[1], s='p')}"
					self.cond[1] += 2
				else:
					c[2] += f"_{self.name(a, self.cond[1], s='p')}"
					self.cond[1] += 2
		elif "perform the following action" in t or "perform the following" in t:
			if "choose  of your  character" in t:
				tt = "choose  of your  character"
				ts = "perform the following action"
				if t.index(tt) < t.index(ts):
					gg, t = self.seperate(ts, a, t, aa, True)
					g = gg
			c = ["perform", 1, self.name(a, self.cond[1], s='p')]
			if "following action twice" in t or "following action 2 times" in aa:
				c.append("twice")
				self.cond[0] += 1
			elif "for every  cards in your clock" in t:
				c.extend(["xclock/", self.digit(a, self.cond[0])])
				self.cond[0] += 1
			elif "for each  character in your center stage" in t:
				c.extend(["x#trait", self.trait(a, self.cond[2]), "xCenter"])
				self.cond[2] += 1
			elif "for each soul trigger icon those cards have" in t:
				c.append("xsoultriggers")
			elif "perform that action as many times as you like" in t:
				c.append("unli")
			self.cond[0] += self.digit(self.name(a, self.cond[1], s='p'), num=True)
			if "shuffle your deck afterward" in t:
				c.extend(["done", [0, "shuffle"]])
		elif "your opponent cannot use any act of characters on his or her stage" in t:
			c = [-21, "[CONT] Your opponent cannot use any [ACT] of characters on his or her stage.", x, "give"]
		elif "your opponent may not play events from hand" in t or "your opponent cannot play event cards from hand" in t:
			c = [-21, "[CONT] Your opponent cannot play events from hand", x, "give"]
		elif "your opponent may draw  card" in t:
			c = ["draw", self.digit(a, self.cond[0]), "opp"]
			self.cond[0] += 1
			if "if so," in t:
				c.extend(["if", 1])
			if "your opponent discards  card from hand to the waiting room" in t:
				c.extend(["do", ["discard", self.digit(a, self.cond[0]), "", "opp", "oppturn"]])
				self.cond[0] += 1
		elif "draw up to x card" in t:
			if "x = the number your opponent declared +" in t:
				c = ["drawupto", "x", "xdeclare+", self.digit(a, self.cond[0])]
				self.cond[0] += 1
			elif "x =  times the number of climax cards revealed this way":
				c = ["drawupto", "x", "xclimax*", self.digit(a, self.cond[0])]
				self.cond[0] += 1
				c = self.discard_card(c, a, t)
				if "do" in c and "discard" in c[c.index("do") + 1] and "x" in c[c.index("do") + 1]:
					c[c.index("do") + 1].extend(["xclimax*", c[c.index("xclimax*") + 1]])
		elif "draw up to  card" in t or "draws up to  card" in t:
			if "your opponent choose" in t:
				tt = "your opponent choose"
				if "draws up to" in t:
					t = t.replace("draws up", "draw up")
				ts = "draw up to  card"
				if t.index(tt) < t.index(ts):
					gg, t = self.seperate(ts, a, t, aa, True)
					g = list(gg)
					gg = ""
			c = ["drawupto", self.digit(a, self.cond[0])]
			self.cond[0] += 1
			if g and "discard" in g and "opp" in g and "oppturn" in g:
				c.extend(["oppturn", "opp"])
			c = self.discard_card(c, a, t, True)
			if "your opponent draws  card" in t:
				c.extend(["do", ["draw", self.digit(a, self.cond[0]), "opp"]])
			if "choose up to  cost  or" in t:
				gg, t = self.seperate("choose up to  cost  or", a, t, aa)
			elif "choose  card in your hand" in t:
				gg, t = self.seperate("choose  card in your hand", a, t, aa)
				if gg == ["do", []]:
					gg = []
			elif "choose  of your opponent" in t:
				gg, t = self.seperate("choose  of your opponent", a, t, aa)
			if gg:
				c.extend(gg)
		elif "draw  card" in t:
			tt = ""
			if "choose   in your hand" in t:
				tt = "choose   in your hand"
			elif "look at up to  cards from the top of your deck" in t:
				tt = "look at up to  cards from"

			if tt and t.index(tt) < t.index("draw  card"):
				gg, t = self.seperate("draw  card", a, t, aa, True)
				g = gg
				gg = []

				if "if not" in t:
					t = self.donot_filter(t)

			c = ["draw", self.digit(a, self.cond[0])]
			self.cond[0] += 1
			if "may draw  card" in t:
				c[0] = "drawupto"
				c.append("upto")
			if "if you do," in t or "if so," in t:
				c.extend(["if", 1])
			c = self.discard_card(c, a, t)
			if "put this in your memory" in t:
				if t.index("put this in your memory") < t.index("draw  card"):
					h = list(c)
					c = []
			if "choose  card in your clock" in t:
				gg, t = self.seperate("choose  card in your clock", a, t, aa)
			elif "choose  of your character" in t:
				gg, t = self.seperate("choose  of your character", a, t, aa)
			elif "choose  of your other" in t:
				gg, t = self.seperate("choose  of your other", a, t, aa)
			elif "you may put the top card of your clock" in t:
				gg, t = self.seperate("you may put the top card of your clock", a, t, aa)
			elif "choose up to  of your opponent" in t:
				gg, t = self.seperate("choose up to  of your opponent", a, t, aa)
			elif "look at the top of your deck" in t:
				gg, t = self.seperate("look at the top of your deck", a, t, aa)
			elif "search your deck" in t:
				gg, t = self.seperate("search your deck", a, t, aa)
			if gg:
				if "do" in c:
					c[c.index("do") + 1].extend(gg)
				else:
					c.extend(gg)
		elif "return the top card of your stock to your hand" in t:
			c = [-17, "stsearch", "", "top"]
		elif "put x cards from the bottom of your opponent's deck into their waiting room" in t or "put the bottom x cards of your opponent's deck into their waiting room" in t:
			if "x = the number of  characters you have" in t:
				c = ["mill", "x", "bottom", "opp", "xTrait", self.trait(a)]
		elif "put the top  cards of every player's deck in the waiting room" in t:
			c = ["mill", self.digit(a), "top", "do", ["mill", self.digit(a), "top", "opp"]]
		elif "put the top  cards of your opponent's deck in the waiting room" in t or "your opponent puts the top  cards of their deck in the waiting room" in t or "put the top  cards of your opponent's deck into their waiting room" in t:
			c = ["mill", self.digit(a), "top", "opp"]
		elif "put up to  card from the top of your deck face up underneath this" in t:
			if "look at up to  cards from the top of your deck" in t:
				tt = "look at up to  cards from the top of your deck"
				tc = "put up to  card from the top of your deck face up underneath this"
				if t.index(tt) < t.index(tc):
					gg, t = self.seperate(tc, a, t, aa, True)
					g = gg
			c = ["drawupto", self.digit(a, self.cond[0]), "Marker", "top"]
			if "faceup as marker" in t:
				c.append("face-up")
		elif "put the top  cards of your deck under this as marker" in t:
			c = [self.digit(a, self.cond[0]), "marker", "top"]
			if "face-up" in t:
				c.append("face-up")
		elif "put the top card of your deck" in t and ("under this as marker" in t or "under this as a marker" in t):
			if "put this rested in the slot this was in" in t:
				tt = "put this rested in the slot this was in"
				ts = "put the top card of your deck"
				if t.index(tt) < t.index(ts):
					gg, t = self.seperate(ts, a, t, aa, True)
					g = [0, "revive", "Stage", "do", [0, "rested"]]
			c = [1, "marker", "top"]
			if "face-up" in t:
				c.append("face-up")
		elif "put this face up underneath your  or  as a marker" in t:
			c = [1, "marker", f"Name=_{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}", "face-up", "Stage", "self"]
			if "you may put this face up underneath":
				c.append("upto")
		elif ("put up to  card from the top of your clock" in t or "put up to  cards from top of your clock" in t or "put up to  card from top of your clock" in t) and ("clock in your waiting room" in t or "clock into the waiting room" in t or "clock in the waiting room" in t):
			if "deal  damage to your opponent" in t:
				tt = "deal  damage to your opponent"
				if t.index(tt) < t.index("put up to  card"):
					if "put up to  card from the top of your clock into the waiting room" in t:
						ts = "put up to  card from the top of your clock into the waiting room"
					elif "put up to  card from the top of your clock in your waiting room" in t:
						ts = "put up to  card from the top of your clock in your waiting room"
					gg, t = self.seperate(ts, a, t, aa, True)
					g = list(gg)
			if "instead of" in t:
				if "if you have  or more other  character" in t:
					self.temp[0] = self.digit(a, self.cond[0])
					self.cond[0] -= 1
					if "put it in stock instead of waiting room" in t:
						self.temp[1] = "Stock"

			if self.digit(a, self.cond[0]) > 1:
				c = ["drawupto", self.digit(a, self.cond[0]), "heal"]
			else:
				c = ["heal", self.digit(a, self.cond[0]), "top", "upto"]
			self.cond[0] += 1

			gg = []
			if "choose  of your character" in t:
				gg, t = self.seperate("choose  of your character", a, t, aa)
			elif "choose  of your other character" in t:
				gg, t = self.seperate("choose  of your other character", a, t, aa)
			elif "search your deck for up to   character" in t:
				gg, t = self.seperate("search your deck for up to   character", a, t, aa)
			elif "at the end of the turn" in t:
				c.extend(["do", [-21, f"[AUTO] {a[a.lower().index('at the end of the turn'):]}", 2, "give"]])
				t = t[:t.index("at the end of the turn")]

			if gg:
				c.extend(gg)
		elif "put the top card of your clock to your stock" in t or "put the top card of your clock in your stock" in t:
			c = ["heal", 1, "top", "Stock"]
			if "choose  card in your hand" in t:
				cc = self.discard_card([], a, t)
				if cc:
					tt = "choose  card in your hand"
					ts = "put the top card of your clock"
					if tt and t.index(tt) < t.index(ts):
						if "do" in cc and len(cc) == 2:
							cc.remove("do")
							cc = cc[0]
						if "if you do" in t:
							cc.extend(["if", cc[1]])
						c = cc + ["do", c]
					else:
						c.extend(cc)
		elif "return the top card of your clock to your hand" in t:
			c = ["heal", 1, "top", "Hand"]
		elif "put the top card of your clock in your waiting room" in t or "put the top card of your clock in the waiting room" in t or "put the top card in your clock in your waiting room" in t or "put the top card of your clock to your waiting room" in t:
			if "choose  face down card in your opponent's memory" in t:
				tt = "choose  face down card"
				ts = "put the top card of your clock"
				if t.index(tt) < t.index(ts):
					gg, t = self.seperate(ts, a, t, aa, True)
					g = gg
			c = ["heal", 1, "top"]
			if "you may put the top card of your clock" in t:
				c = ["drawupto", 1, "heal"]
				if t.count("you may") <= 1:
					self.no_pay = True
			if "search your deck for up" in t:
				gg, t = self.seperate("search your deck for up", a, t, aa)
				c.extend(gg)
		elif "put the bottom  cards of your clock in the waiting room" in t:
			c = ["heal", self.digit(a, self.cond[0]), "bottom"]
		elif "put up to  cards from the bottom of your clock in the waiting room" in t:
			if self.digit(a, self.cond[0]) > 1:
				c = ["drawupto", self.digit(a, self.cond[0]), "heal", "bottom"]
			else:
				c = ["heal", self.digit(a, self.cond[0]), "bottom", "upto"]
		elif "put the top card of your opponent's clock into their waiting room" in t or "put the top card of your opponent's clock in the waiting room" in t or "put the top card of your opponent's clock in his or her waiting room" in t:
			c = ["cdiscard", -17, "", "opp"]
			if self.target and "put that character in your opponent's clock" in t or "put that character in clock" in t or "put that battle opponent in clock" in t:
				c += ["if", 1, "do", [-3, "clocker", "target", self.target, "Opp"]]
		elif "your opponent puts all of their stock into their waiting room" in t or "put all cards in your opponent's stock in your opponent's waiting room" in t or "put all cards in your opponent's stock in the waiting room" in t or "put all your opponent's stock in the waiting room" in t or "your opponent puts all of their stock to the waiting room" in t or "your opponent puts all cards from their stock into their waiting room" in t:
			if "puts the same number of cards from the top of their deck into their stock" in t or "your opponent puts the same number of cards from the top of your opponent's deck in his or her stock" in t or "your opponent puts the same number of cards from top of the deck in the stock" in t or "your opponent put the same number of cards from the top of their deck in the stock" in t or "puts the same number of cards from the top of their deck to their stock" in t:
				c = ["distock", -1, "top", "opp", "count", "do", ["stock", "count", "opp"]]
				if "choose up to  character" in t:
					gg, t = self.seperate("choose up to  character", a, t, aa)
					c[c.index("do") + 1].extend(gg)
		elif "your opponent may put the top  cards of their stock in the waiting room" in t:
			c = ["distock", self.digit(a, self.cond[0]), "top", "opp", "oppturn", "if", self.digit(a, self.cond[0])]
			if "this cannot front attack" in t:
				c.extend(["do", [0, "[CONT] This cannot front attack", x, "give"]])
		elif "your opponent searches your deck for  level  or higher character" in t:
			c = [self.digit(a, self.cond[0]), "search", f"CLevel_>={self.digit(a, self.cond[0] + 1)}", "oppturn", "opp"]
			self.cond[0] += 2
		elif "your opponent chooses  card from your opponent's hand" in t:
			c = ["discard", self.digit(a, self.cond[0]), "", "oppturn", "opp"]
			self.cond[0] += 1
			if "puts it face down in his or her memory" in t:
				c.extend(["Memory", "face-down"])
		elif "your opponent may choose  of your character" in t:
			if "return that character to your hand" in t:
				c = [self.digit(a, self.cond[0]), "hander", "Opp", "oppturn", "opp", "upto"]
				self.cond[0] += 1
		elif "return all your opponent's center stage characters whose level is  or lower to the hand" in t:
			c = [-1, "hander", "Opp", "Center", "Level", f"<={self.digit(a, self.cond[0])}"]
			self.cond[0] += 1
		elif self.target and ("put that character on the stage position it was on as rest" in t or "put that character rest in the slot it was in" in t or "put that character rested in the slot it was in" in t or "return that character to its previous stage position as rest" in t):
			c = [-7, "revive", [self.target, "Stage"], "extra", "do", [-16, "rested"]]
			if "that character gets + power" in t:
				c[c.index("do") + 1].extend(["extra", "do", [-16, self.digit(a, self.cond[0]), x, "power"]])
		elif self.target and "return that character to your hand" in t:
			c = [-7, "return", [self.target, "Hand"]]
		elif self.target and "return your opponent's battle character in your opponent's hand" in t:
			c = [-3, "return", [self.target, "Hand"]]
			if "your opponent chooses  card in his or her hand and puts it in your opponent's waiting room" in t:
				c.extend(["do", ["discard", self.digit(a, self.cond[0]), "", "opp", "oppturn"]])
		elif self.target and ("put that character on top of the deck" in t or "put it on top of the deck" in t or "put that character on the top of your opponent's deck" in t):
			c = [-3, "decker", "top", "target", self.target, "Opp"]
		elif self.target and ("put that character on the bottom of your opponent's deck" in t or "put that character on the bottom of the deck" in t or "put that character at the bottom of your opponent's deck" in t or "put it on the bottom of the deck" in t or "put that card at the bottom of your opponent's deck" in t):
			c = [-3, "decker", "bottom", "target", self.target, "Opp"]
			if "if you do" in t:
				c.extend(["if", 1])
				if "search your deck for up to  character whose level = or lower than that character" in t:
					c.extend(["extra", "do", [self.digit(a, self.cond[0]), "search", "CLevel_<=x", "upto", "show", "xlevelextra"]])
		elif self.target and ("put that character in stock" in t or "put that character in your opponent's stock" in t):
			c = [-3, "stocker", "target", self.target, "Opp"]
			if "put the bottom card of your opponent's stock in the waiting room" in t or "put the bottom card of your opponent's stock into their waiting room" in t:
				c.extend(["replace", "bottom"])
		elif self.target and ("put that character in your opponent's memory" in t or "send that card to your opponent's memory" in t or "send that character to memory" in t or "send that battle opponent to memory" in t):
			c = [-3, "memorier", "target", self.target, "Opp"]
			if "swap this with  of your back stage character" in t:
				c.extend(["do", [self.digit(a, self.cond[0]), "stand", "swap", "nostand", "Back", "this"]])
		elif self.target and ("put that character in your opponent's clock" in t or "put that character in clock" in t):
			c = [-3, "clocker", "target", self.target, "Opp"]
		elif self.target and ("reverse that character" in t or "reverse that battle opponent" in t):
			c = [-3, "reverser", "target", self.target, "Opp"]
		elif self.target and "that character cannot use \"[auto] encore\"" in aa:  
			c = [-3, "[CONT] This card cannot use \"[AUTO] Encore\".", 1, "target", self.target, "give"]
		elif self.target and "that character gets + power" in t and "choose  of your character" not in t:
			c = [-3, self.digit(a, self.cond[0]), x, "power", "target", self.target]
			self.cond[0] += 1
			if "power and «" in aa:
				c.extend(["extra", "do", [-16, self.trait(a, self.cond[2]), x, "trait"]])
				self.cond[2] += 1
		elif "put the top card of your clock face-down under this as marker" in t:
			c = [1, "marker", "top", "Clock"]
		elif "put the top card of your stock under this as marker" in t:
			c = [1, "marker", "top", "Stock"]
		elif "put all markers from under this" in t or "put all markers under this" in t:
			c = [-1, "marker", "Return"]
			if "under this in the waiting room" in t or "under this in your waiting room" in t:
				c.append("Waiting")
				if "if at least  level  or lower character card is placed in the waiting room this way" in t:
					c.extend(["if", self.digit(a, self.cond[0]), "ifCLevel<=", self.digit(a, self.cond[0] + 1), "ifany"])
					self.cond[0] += 2
				if "choose   either in your" in t:
					gg, t = self.seperate("choose   either in your", a, t, aa)
					c.extend(gg)
			elif "under this in your stock" in t:
				c.append("Stock")
			elif "under this on to separate positions of your stage" in t:
				c.extend(["Stage", "extra", "if", 1, "do", [-16, "ksalvage", "ID=_x", "Markers", "Stage", "separate"]])
		elif "put the character chosen by this's effect in your waiting room" in t:
			c = [0, "waitinger", "aselected", "atarget", self.aselected]
		elif "put all players' characters except this into their waiting rooms" in t:
			c = [-1, "waitinger", "both", "all", "Other"]
		elif " put all your opponent's level  or lower characters into their waiting room" in t:
			c = [-1, "waitinger", "Level", f"<={self.digit(a, self.cond[0])}", "Opp"]
		elif "put all level  or lower characters in your opponent's center stage" in t:
			c = [-1, "", "Level", f"<={self.digit(a, self.cond[0])}", "Opp", "Center"]
			if "opponent's center stage to the waiting room" in t or "opponent's center stage in the waiting room" in t:
				c[1] = "waitinger"
			elif "opponent's center stage in stock" in t:
				c[1] = "stocker"
		elif "put all your opponent's characters in stock" in t:
			c = [-1, 'stocker', 'opp']
		elif "you may put all your opponent's characters in your opponent's memory" in t:
			c = [-1, "memorier", "opp"]
			if "put those characters on to separate positions of his or her stage" in t:
				c.extend(["extra", "if", 1, "do", [-16, "msalvage", "ID=_x", "Stage", "Opp", "plchoose", "separate", "opp"]])
		elif "put all your other characters" in t:
			c = [-2]
			if "characters face down in any order under this as marker" in t:
				c.extend(["marker", "Stage"])
		elif "look at your opponent's hand" in t:
			c = ["Hand", "look"]
			if "choose up to  climax card" in t:
				c = ["discard", self.digit(a, self.cond[0]), "Climax", "upto"]
				if "put it in opponent's climax area" in t:
					c.append("CX")
			c.append("opp")
			if "choose up to " in t:
				ts = ""
				if "choose up to  of your opponent" in t:
					ts = "choose up to  of your opponent"
				elif "choose up to   in your" in t:
					ts = "choose up to   in your"
				if ts:
					c.extend(["do", self.convert(a, ts + t.split(ts)[1], aa)])
					t = t.split(ts)[0]
		elif "look at up to x cards from the top of your deck" in t or "look at up to x cards from top of your deck" in t:
			c = ["x", "looktop", "top"]
			if "put it in your hand" in t or "put them in your hand" in t:
				c.extend(["hand"])
				if "choose up to   character from among them" in t:
					c.extend([self.digit(a, self.cond[0]), f"Trait_{self.trait(a, self.cond[2])}"])
					self.cond[2] += 1
				elif "choose up to  card from among them" in t or "choose up to  of them" in t:
					c.extend([self.digit(a, self.cond[0]), ""])
				self.cond[0] += 1

			c.append("upto")

			if "x = the number of characters your opponent has" in t:
				c.append("xopp")
			elif "x = # of your characters with either  or " in t or "x = the number of  or  characters you have" in t:
				c[0] = -14
				c.extend(["xTrait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}", "xStage"])
			elif "x = the number of  characters you have" in t or "x = the number of your  characters" in t or "x = # of your  character" in t or "x = the number of other  characters you have" in t:
				c[0] = -14
				c.extend(["xTrait", self.trait(a, self.cond[2]), "xStage"])

			if "reveal it" in t and "show" not in c:
				if "if" in c:
					c.insert(c.index("if"), "show")
				elif "do" in c:
					c.insert(c.index("do"), "show")
				else:
					c.append("show")
		elif "look at up to  cards from top of your deck" in t or "look at up to  cards from the top of your deck" in t:
			if "if there are no  cards in your memory" in t and "send this to memory" in t:
				self.cond_later = True
				self.cond = [0, 0, 0, 0, 0, 0]

			c = [self.digit(a, self.cond[0]), "looktop", "top"]
			self.cond[0] += 1
			if "put it in your hand" in t and "put it in your stock" in t and t.count("choose  card from the revealed card") == 2:
				c.extend(["hand", self.digit(a, self.cond[0])])
				self.cond[0] += 1
				if "choose up to  level  or higher cards from among them" in t:
					c.extend([f"Level_>={self.digit(a, self.cond[0])}", "any"])
					self.cond[0] += 1
				c.append("show")
				if t.index("put it in your hand") < t.index("put it in your stock"):
					c.extend(["extrareveal", "do", [self.digit(a, self.cond[0]), "search", "", "Reveal", "extrareveal", "show", "do", ["stock", self.digit(a, self.cond[0] + 1), "Reveal"]]])
					self.cond[0] += 2
			elif "put them on the top of your deck in any order" in t or "put them on top of your deck in any order" in t or "put them on top of the deck in any order" in t:
				if "choose up to  of those card" in t or "choose up to  cards from among them" in t:
					c.extend([self.digit(a, self.cond[0]), "any"])
				c.append("treorder")
				if "put the remaining cards in the waiting room" in t or "put the rest in your waiting room" in t:
					c.append("waity")
			elif "put them back in the same order" in t or "put them on the top of your deck in the original order" in t:
				pass
			elif "put them in your hand" in t or "put it in your hand" in t:
				c.extend(["hand", self.digit(a, self.cond[0])])
				if "» or «" in aa and ("choose up to   or  or  character" in t and "\" or «" in aa) or ("choose up to   or  character or character with  in its card name" in t):
					c.extend([f"TTName_{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}_{self.name(a, self.cond[1], s='n')}", "any"])
					self.cond[2] += 2
					self.cond[1] += 2
				elif "choose up to  level  or lower character, or  event" in t or "choose up to  event or level  or lower character from among them" in t:
					c.extend([f"CLevelE_<={self.digit(a, self.cond[0] + 1)}", "any"])
					self.cond[0] += 2
				elif "choose up to  event or  character from among them" in t:
					c.extend([f"TraitE_{self.trait(a, self.cond[2])}", "any"])
					self.cond[2] += 1
				elif "search for up to   character or  " in t and "» character or 1 \"" in aa:
					c.extend([f"TraitN=_{self.trait(a, self.cond[2])}_{self.name(a, self.cond[1], s='n')}", "any"])
					self.cond[2] += 1
					self.cond[1] += 2
				elif "reveal up to  character with  or  in name" in t and "» or \"" in aa:
					c.extend([f"TraitN_{self.trait(a, self.cond[2])}_{self.name(a, self.cond[1], s='n')}"])
					self.cond[2] += 1
					self.cond[1] += 2
				elif ("» or «" in aa or "» and/or «" in aa) and ("choose up to   or  character from among them" in t or "search for up to  character with  or " in t or "choose up to  characters with  and/or  from among them" in t or "choose up to   or  character" in t):
					c.extend([f"Trait_{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}", "any"])
					self.cond[2] += 2
				elif "choose up to  level  or higher card from among them" in t or "search for up to  level  or higher card" in t:
					c.extend([f"Level_>={self.digit(a, self.cond[0] + 1)}", "any"])
					self.cond[0] += 1
				elif "search for up to   character" in t or "search them for up to  character" in t:
					if "up to  character with  and/or " in t and "» and/or «" in aa:
						c.extend([f"Trait_{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}", "any"])
						self.cond[2] += 2
					else:
						c.extend([f"Trait_{self.trait(a, self.cond[2])}", "any"])
						self.cond[2] += 1
				elif ("choose up to   characters from among them" in t or "choose up to   character from among them" in t) and "» character" in aa:
					c.extend([f"Trait_{self.trait(a, self.cond[2])}", "any"])
					self.cond[2] += 1
				elif "search for up to  character with  in name" in t or "choose up to  character with  in its card name" in t:
					c.extend([f"Name_{self.name(a, self.cond[1], s='n')}", "any"])
					self.cond[1] += 2
				elif "choose up to  of them" in t or "choose up to  card from among them" in t or "choose up to  of those card" in t:
					c.extend(["", "any"])
				elif "choose up to  climax from among them" in t or "search for up to  climax card" in t:
					c.extend(["Climax", "any"])
				elif "choose up to  character from among them" in t or "choose up to  character" in t:
					c.extend(["Character", "any"])
				self.cond[0] += 1
				if "if you searched for  level  or higher character this way" in t:
					c.extend(["if", self.digit(a, self.cond[0]), "ifLevel", self.digit(a, self.cond[0] + 2)])
					self.cond[0] += 3
				elif "if you put  card in your hand" in t:
					c.extend(["if", self.digit(a, self.cond[0])])
					self.cond[0] += 1
					c = self.discard_card(c, a, t)
			elif "put them in your waiting room" in t:
				if "choose  cards from among them" in t or "choose  card from among them" in t or "choose  of them" in t:
					if "put the rest on the top of your deck in any order" in t:
						c = ["waiting", self.digit(a, self.cond[0]), "all", "reorder"]
			elif "put it on the top of your deck" in t or "put it on top of the deck" in t or "put it on top of your deck" in t:
				if "choose  cards from among them" in t or "choose  card from among them" in t or "choose  of them" in t:
					c.extend([self.digit(a, self.cond[0])])
			elif "put it rested in an empty slot on the stage" in t:
				if "search for up to  character" in t:
					c.extend([self.digit(a, self.cond[0]), "Character", "any", "choosestage", "restopen"])
					self.cond[0] += 1
				c.extend(["extra", "do", [-16, "search", "", "Stage", "Open", "noshuff", "extra", "do", [-16, "rested"]]])
			if "place them back on top of your deck in any order" in t:
				c.append("treorder")

			if "if" in c:
				c.insert(c.index("if"), "upto")
			elif "do" in c:
				c.insert(c.index("do"), "upto")
			else:
				c.append("upto")

			if ("reveal it" in t or "reveal them" in t or "show it" in t or "show them" in t or "show your opponent" in t) and "show" not in c:
				if "if" in c:
					c.insert(c.index("if"), "show")
				elif "do" in c:
					c.insert(c.index("do"), "show")
				else:
					c.append("show")

			if self.cond_later:
				c.extend(["do", self.condition(a, t, aa)])
			if "choose up to  of your opponent's character" in t:
				c.extend(["do", self.convert(a, "choose up to  of your opponent's character" + t.split("choose up to  of your opponent's character")[1], aa)])
			elif "choose  of your character" in t:
				gg, t = self.seperate("choose  of your character", a, t, aa)
			elif "choose  of your opponent" in t:
				gg, t = self.seperate("choose  of your opponent", a, t, aa)

			if gg:
				if "do" in c:
					c[c.index("do") + 1].extend(gg)
				else:
					c.extend(gg)
		elif "look at up to  cards of the top of your opponent's deck" in t or "look at up to  cards from top of your opponent's deck" in t or "look at up to  cards from the top of your opponent's deck" in t:
			c = [self.digit(a, self.cond[0]), "looktop", "top"]
			self.cond[0] += 1

			if "put them in the waiting room" in t:
				c.append("waiting")
				if "choose up to  of them" in t:
					c.extend([self.digit(a, self.cond[0]), "", "any"])
					self.cond[0] += 1
			elif "place as many cards from among them in the waiting room" in t:
				c.append("waiting")
				c.extend([c[0], "", "any"])
			elif "put them on top of the deck in any order" in t or "put them back in any order" in t:
				if "choose up to  of them" in t:
					c.extend([self.digit(a, self.cond[0]), "", "any"])
					self.cond[0] += 1
				c.append("tdeck")
			elif "put it on the bottom of the deck" in t:
				if "choose up to  of them" in t:
					c.extend([self.digit(a, self.cond[0]), "", "any"])
					self.cond[0] += 1
				c.append("bdeck")
			c.extend(["opp", "upto"])
			if "return the rest to the deck" in t:
				c.append("shuff")
			elif "put the rest on the bottom of the deck in any order" in t:
				c.append("breorder")
			elif "put the remaining cards back on top of their deck in any order" in t or "put the rest back on top of the deck in any order" in t:
				c.append("treorder")
			if "choose  of your character" in t:
				gg, t = self.seperate("choose  of your character", a, t, aa)
				c.extend(gg)
		elif "look at up to  cards from the bottom of your opponent's deck" in t:
			c = [self.digit(a, self.cond[0]), "looktop", "bottom", "upto", "opp"]
			self.cond[0] += 1
			if "put them in clock" in t or "put them in your opponent's clock" in t:
				c.append("clock")
				if "choose up to  climax card" in t or "choose up to  climax from among them" in t:
					c.extend([self.digit(a, self.cond[0]), "Climax", "any"])
		elif "look at the top  cards of your opponent's deck" in t:
			c = [self.digit(a, self.cond[0]), "looktop", "top"]
			self.cond[0] += 1
			if "choose up to  of them" in t:
				c.extend([self.digit(a, self.cond[0]), "upto", "opp"])
				self.cond[0] += 1
				if "put it on the bottom of the deck" in t:
					c.append("bdeck")
				elif "put them in the waiting room" in t:
					c.insert(c.index("top") + 1, "waiting")
			c.append("fix")
			if "return the rest to the deck" in t and ("shuffle that deck" in t or "your opponent shuffles that deck" in t):
				c.append("shuff")
			elif "put the rest on top of the deck in any order" in t:
				c.append("treorder")
		elif "look at the top card of your opponent's deck" in t:
			ts = "look at the top card of your opponent's deck"
			if "choose  of your stand character" in t or "choose  of your standing character" in t:
				if "choose  of your stand character" in t:
					tt = "choose  of your stand character"
				elif "choose  of your standing character" in t:
					tt = "choose  of your standing character"
			elif "deal  damage to your opponent" in t:
				tt = "deal  damage to your opponent"
			if tt and t.index(tt) < t.index(ts):
				gg, t = self.seperate(ts, a, t, aa, True)
				g = gg
			tt = ""
			ts = ""

			if any(_ in t for _ in ("put it on the top or the bottom of your opponent's deck", "put it either on top or bottom of the deck", "put it on the top or the bottom of his or her deck", "put it on the top or at the bottom of their deck")):
				c = [1, "looktop", "top", "bottom", "opp"]
			elif "put it on the top of their deck or into their waiting room" in t:
				c = [1, "looktop", "top", "waiting", "opp"]
			if "deal  damage to" in t:
				gg, t = self.seperate("deal  damage to", a, t, aa)
				c.extend(gg)
		elif "look at the top  cards of your deck" in t or "look at top  cards of your deck" in t:
			if "put them back in any order" in t:
				c = [self.digit(a, self.cond[0]), "looktop", "top", "tdeck"]
			elif "choose up to  character with  or  in name" in t or "reveal up to  character with  or  in name" in t:
				if "put it in your hand" in t:
					c = [self.digit(a, self.cond[0]), "looktop", "top", "hand", self.digit(a, self.cond[0] + 1), f"Name_{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}", "fix", "upto"]
					if "» or \"" in aa:
						c[5] = f"TraitN_{self.trait(a, self.cond[2])}_{self.name(a, self.cond[1], s='n')}"
				if "reveal it" in t:
					c.append("show")
		elif "look at the top card of your deck" in t or "look at the top of your deck" in t:
			if "choose  card in your hand" in t and "put it in your waiting room" in t:
				tt = "choose  card in your hand"
				gg = "put it in your waiting room"
				ts = "look at the top"
				if t.index(tt) < t.index(ts) and t.index(tt) < t.index(gg) < t.index(ts):
					_ = t
					gg, t = self.seperate(ts, a, t, aa, True)
					if not gg:
						gg = ["discard", self.digit(a, self.cond[0]), ""]
						if "if you do" in _ and _.index("if you do") < _.index(ts):
							gg.extend(["if", gg[1]])
						self.cond[0] += 1
					g = gg
				gg = ""
			if "put it on the top or bottom of your deck" in t or "put it on the top or at the bottom of your deck" in t or "put it on top or bottom of your deck" in t or "put it either on top or bottom of your deck" in t or "put it on the top or the bottom of your deck" in t or "put it back either on top or bottom of the deck" in t or "put it either on top or bottom of the deck" in t or "put it either on top of bottom of the deck" in t or "put it back on top or bottom of deck" in t:
				c = [1, "looktop", "top", "bottom"]
			elif "put it either on top of the deck or in the waiting room" in t or "put it on top of your deck or in your waiting room" in t or "put it on the top of your deck or in your waiting room" in t or "place it back on top of your deck or in your waiting room" in t or "put it either on top of your deck or in your waiting room" in t:
				c = [1, "looktop", "top", "waiting"]
			elif "put that card face-down under this as marker" in t or "put it face-down under this as marker" in t or "put that card face down under this as a marker" in t:
				c = [1, "looktop", "check", "do", [1, "marker", "top"]]
			else:
				c = [1, "looktop", "check"]
			if "choose  of your character" in t:
				gg, t = self.seperate("choose  of your character", a, t, aa)
				c.extend(gg)
			elif "choose  of your  character" in t:
				gg, t = self.seperate("choose  of your  character", a, t, aa)
				c.extend(gg)
		elif (("choose  of the following  abilit" in t or "choose  of the following abilit" in t) and "this gets that ability" in t) or "this gets  of the following abilities of your choice" in t:
			c = ["perform", self.digit(a, self.cond[0]), "", "choice", 0, "giver", 0, x]
			self.cond[0] += 1
			if "following  abilitie" in t:
				rr = self.digit(a, self.cond[0])
				self.cond[0] += 1
			else:
				rr = int(a.count("\"") / 2)
				if "[CXCOMBO]" in a or "\" is in the climax area" in aa:
					rr -= 1
			c[4] = rr
			for r in range(rr):
				if r == 0:
					c[2] += f"{self.name(a, self.cond[1], s='p')}"
					self.cond[1] += 2
				else:
					c[2] += f"_{self.name(a, self.cond[1], s='p')}"
					self.cond[1] += 2
		elif "choose  climax in your climax area" in t:
			if "put it in the stock" in t:
				c = [self.digit(a, self.cond[0]), "stocker", "Climax"]
				self.cond[0] += 1
			if "you may choose  climax" in t:
				c.append("upto")
		elif "choose  character opposite this" in t:
			if "put it in your opponent's waiting room" in t or "put it in the waiting room" in t:
				c = [self.digit(a, self.cond[0]), "waitinger", "Opposite"]
			elif "that character gets - power" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power", "Opposite"]
				self.cond[0] += 1
			self.cond[0] += 1
		elif "choose the character opposite this" in t:
			if "this gets + power" in t:
				tt = "this gets + power"
				ts = "choose the character opposite this"
				if t.index(tt) < t.index(ts):
					gg, t = self.seperate(ts, a, t, aa, True)
					g = gg
			if "that character gets + soul" in t:
				c = [1, self.digit(a, self.cond[0]), x, "soul", "Opposite", "Opp"]
			elif "that character gets " in t and "character gets \"[" in aa or "gets the following ability" in t:
				c = [1, self.name(a, s='a'), x, "Opposite", "give"]
		elif "chooses   or   in your waiting room" in t:
			c = [1, "salvage", f"Name=_{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}"]
			if "put it in any slot on the stage" in t:
				c.append("Stage")
			elif "put it in the slot this was in" in t:
				c.extend(["Stage", "Change"])
		elif "choose  of either  or  or  or  in your clock" in t:
			c = [self.digit(a, self.cond[0]), "csalvage", f"Name=_{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}_{self.name(a, self.cond[1] + 4, s='n')}_{self.name(a, self.cond[1] + 6, s='n')}"]
			if "you may choose  of " in t:
				c.append("upto")
			self.cond[0] += 1
			self.cond[1] += 8
			if "if so," in t:
				c.extend(["if", c[0]])
			c = self.discard_card(c, a, t)
		elif "choose either this or  of your  " in t:
			if "put it in your waiting room" in t:
				c = [self.digit(a), "waitinger", "Name=", self.name(a, s="n"), "This"]
		elif "choose   either in your hand or in your waiting room" in t and "\" either in your" in aa:
			c = [self.digit(a, self.cond[0]), "salvage", f"Name=_{self.name(a, self.cond[1], s='n')}", "&Hand"]
			if "put it rested in any slot on the stage" in t:
				c.extend(["Stage", "extra", "do", [-16, "rested"]])
		elif "choose another of your  characters" in t:
			if "that character gets + power" in t:
				c = [1, self.digit(a, self.cond[0]), x, "power", "Trait", self.trait(a, self.cond[2]), "Other"]
		elif "choose another character" in t or "choose another of your character" in t:
			if "choose  of your  character" in t:
				tt = "choose  of your  character"
				if "choose another character" in t:
					ts = "choose another character"
				elif "choose another of your character" in t:
					ts = "choose another of your character"
				if t.index(tt) < t.index(ts):
					gg, t = self.seperate(ts, a, t, aa, True)
					g = gg

			c = [1, self.digit(a, self.cond[0]), x]
			if "return it to your hand" in t:
				c = [1, "hander"]
			elif "that character gets + level" in t:
				c.append("level")
			elif "that character gets + power" in t:
				c.append("power")
			elif "that character gets + soul" in t:
				c.append("soul")
				if "for each soul trigger icon on the card put in your waiting room" in t:
					c.extend(["X", "xmill", "#soultrigger"])

			self.cond[0] += 1

			c.append("Other")
			if "your" not in t:
				c.append("Another")
			if "character of yours with  in the name" in t:
				c.extend(["Name", self.name(a, self.cond[1], s='n')])
				self.cond[1] += 2
			elif "with the same card name as the character chosen" in t:
				c.extend(["Name=", "same_name"])
				c.extend(["Other_same", ""])
				if "choose another of your character" in t and gg:
					gg.append("save_name")
			elif "your characters with «" in aa:
				c.extend(["Trait", self.trait(a, self.cond[2])])
				self.cond[2] += 1
		elif "choose  card in your hand" in t and ("put it in your stock" in t or "put it in stock" in t):
			if "choose up to  character" in t:
				tt = "choose up to  character"
				ts = "choose  card in your hand"
				if t.index(tt) < t.index(ts):
					gg, t = self.seperate(ts, a, t, aa, True)
					g = gg
			c = ["discard", self.digit(a, self.cond[0]), "", "Stock"]
			self.cond[0] += 1
			if "you may choose  card" in t:
				c.append("upto")
		elif ("choose  card in your level and" in t or "choose  card on your level area and" in t or "choose  card in your level zone and" in t) and ("and  card in your waiting room" in t or "and  character in your waiting room" in t or "and   or  character in your waiting room" in t):
			if "exchange them" in t or "swap them" in t:
				c = ["ldiscard", self.digit(a, self.cond[0]), "", "swap", "Waiting", "if", "do", [self.digit(a, self.cond[0] + 1), "salvage", "", "swap", "Level"]]
				self.cond[0] += 2
			if "and   or  character in your waiting room" in t and "» or «" in aa:
				c[c.index("do") + 1][2] = f"Trait_{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"
			if "choose up to  of your" in t:
				gg, t = self.seperate("choose up to  of your", a, t, aa)
				c[c.index("do") + 1].extend(gg)
		elif "choose  card in your hand and  card in your level" in t:
			if "exchange them" in t:
				c = ["discard", self.digit(a), "", "swap", "Level", "if", "do", ["ldiscard", self.digit(a), "", "swap", "Hand"]]
		elif "choose   in your climax area and a climax card in your waiting room" in t:
			if "swap them" in t:
				c = ["cxdiscard", self.digit(a, self.cond[0]), f"Name=_{self.name(a, self.cond[1], s='n')}", "swap", "Waiting", "if", "do", [self.digit(a, self.cond[0]), "salvage", "Climax", "swap", "CX"]]
		elif "choose   character, a  character, and a  character in your waiting room" in t:
			c = [self.digit(a, self.cond[0]) + 2, "salvage", f"BTrait_{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}_{self.trait(a, self.cond[2] + 2)}", "show"]
			self.cond[2] += 3
			self.cond[0] += 1
		elif "choose  character in your waiting room" in t and "and  card in your memory" in t:
			if "swap them" in t or "exchange them" in t:
				c = [self.digit(a, self.cond[0]), "salvage", "", "swap", "Memory", "if", 1, "do", ["mdiscard", self.digit(a, self.cond[0] + 1), "", "swap", "Waiting"]]
				if "waiting room with  in name" in t:
					c[2] = f"Name_{self.name(a, self.cond[1], s='n')}"
		elif "choose   character in your waiting room and the bottom card of your clock" in t:
			if "exchange them" in t:
				c = [self.digit(a, self.cond[0]), "salvage", "", "swap", "Clock", "if", 1, "do", ["cdiscard", -18, "", "swap", "Waiting"]]
				if "» character in your waiting room" in aa:
					c[2] = f"Trait_{self.trait(a, self.cond[2])}"
		elif "choose  face up card in your opponent's memory" in t:
			if "put it face down" in t:
				c = ["mdiscard", self.digit(a, self.cond[0]), "", "opp", "flip", "down"]
				self.cond[0] += 1
				if "at the end of your turn" in t:
					t1 = t.split("at the end of your turn")[1]
					if "put that card face up" in t1:
						c.extend(["extra", "do", [-21, self.name(a, s='ae'), 1, "give", "expass", c[1], "ex_ID="]])
		elif "choose  face down card in your opponent's memory" in t:
			c = ["mdiscard", self.digit(a, self.cond[0]), "Face-down", "opp"]
			self.cond[0] += 1
			if "put it in his or her waiting room" in t:
				pass
			elif "put it in his or her clock" in t:
				c.append("Clock")

			if "if you do" in t:
				c.extend(["if", 1])
			if "search your deck for" in t:
				gg, t = self.seperate("search your deck for", a, t, aa)
				c.extend(gg)
			elif "choose   character" in t:
				gg, t = self.seperate("choose   character", a, t, aa)
				c.extend(gg)
		elif "choose up to x  characters from your waiting room" in t or "choose up to x  characters in your waiting room" in t:
			if "return them to hand" in t or "return them to your hand" in t:
				c = ["x", "salvage", f"Trait_{self.trait(a, self.cond[2])}", "show", "upto"]
			if "x = the total level of the cards put in your waiting room" in t:
				c += ["xsmlevel"]
			elif "x = the number of level  or lower characters put in your waiting room" in t:
				c.extend(["xrqclevel", self.digit(a, self.cond[0])])
		elif "choose up to  cards in your clock" in t:
			if "put them in the waiting room" in t:
				c = ["cdiscard", self.digit(a, self.cond[0]), "", "upto"]
		elif "choose up to   characters in your clock" in t:
			if "return it to your hand" in t:
				c = [self.digit(a, self.cond[0]), "csalvage", f"Trait_{self.trait(a, self.cond[2])}", "upto"]
				self.cond[0] += 1
		elif "choose up to  character in your clock" in t:
			if "choose up to  of your opponent" in t:
				tt = "choose up to  of your opponent"
				ts = "choose up to  character in your clock"
				if t.index(tt) < t.index(ts):
					gg, t = self.seperate(ts, a, t, aa, True)
					g = gg

			if "return it to your hand" in t:
				c = [self.digit(a, self.cond[0]), "csalvage", "Character", "upto"]
				self.cond[0] += 1
		elif "choose up to  climax in your hand" in t:
			if "put it face down under this as a marker" in t and "reveal it" in t:
				c = [self.digit(a, self.cond[0]), "marker", "Climax", "Hand", "at", "show", "upto"]
		elif "choose up to  climax in your waiting room" in t or "choose up to  climax card in your waiting room" in t:
			if "choose up to  character" in t:
				tt = "choose up to  character"
				ts = "choose up to  climax"
				if t.index(tt) < t.index(ts):
					gg, t = self.seperate(ts, a, t, aa, True)
					g = gg
			if "return it to your hand" in t:
				c = [self.digit(a, self.cond[0]), "salvage", "Climax", "upto", "show"]
				self.cond[0] += 1
			if "choose up to   characters in your waiting room" in t:
				gg, t = self.seperate("choose up to   characters in your waiting room", a, t, aa)
				c.extend(gg)
		elif "choose up to   and up to   and up to   in your waiting room" in t and aa.count("\" and") == 2:
			c = [self.digit(a, self.cond[0]), "salvage", f"Name=_{self.name(a, self.cond[1], s='n')}", "upto", "do", [self.digit(a, self.cond[0] + 1), "salvage", f"Name=_{self.name(a, self.cond[1] + 2, s='n')}", "upto", "do", [self.digit(a, self.cond[0] + 1), "salvage", f"Name=_{self.name(a, self.cond[1] + 4, s='n')}", "upto"]]]
			self.cond[0] += 3
			self.cond[1] += 6
			if "put them in separate slots on the stage" in t:
				c.insert(c.index("do"), "Stage")
				c[c.index("do") + 1].insert(c[c.index("do") + 1].index("do"), "Stage")
				c[c.index("do") + 1][c[c.index("do") + 1].index("do") + 1].append("Stage")
		elif "choose up to   and   from your waiting room" in t and "\" and" in aa:
			c = [self.digit(a, self.cond[0]), "salvage", f"Name=_{self.name(a, self.cond[1], s='n')}", "upto", "do", [self.digit(a, self.cond[0] + 1), "salvage", f"Name=_{self.name(a, self.cond[1] + 2, s='n')}", "upto"]]
			self.cond[0] += 2
			self.cond[1] += 4
			if "put them in separate slots on the stage" in t:
				c.insert(c.index("do"), "Stage")
				c[c.index("do") + 1].append("Stage")
			if "those characters get + power and + soul" in t:
				c[c.index("do") + 1].extend(["extra", "do", [-16, self.digit(a, self.cond[0]), x, "power", "extra", "do", [-16, self.digit(a, self.cond[0] + 1), x, "soul"]]])
				c.insert(c.index("do"), "extra")
		elif "choose up to  character with level equal to or lower than your level in your hand" in t:
			c = ["discard", self.digit(a, self.cond[0]), "CLevel_<=p", "upto"]
			self.cond[0] += 1
			if "put it on any position of your stage" in t:
				c.append("Stage")
				if "that character gets + soul" in t:
					c.extend(["extra", "do", [-16, self.digit(a, self.cond[0]), x, "soul"]])
		elif "choose up to   character with level equal to or lower than your level in your hand" in t:
			c = ["discard", self.digit(a, self.cond[0]), f"TraitL_{self.trait(a, self.cond[2])}_<=p", "upto"]
			self.cond[0] += 1
			self.cond[2] += 1
			if "put it on the stage position that this was on" in t:
				c.extend(["Stage", "Change"])
		elif ("choose up to   in your hand" in t or "choose up to  card named " in t) and "\" in your hand" in aa:
			if "search your deck for up to   character" in t:
				tt = "search your deck for up to   character"
				if "choose up to   in your hand" in t:
					ts = "choose up to   in your hand"
				elif "choose up to  card named " in t:
					ts = "choose up to  card named "
				if t.index(tt) < t.index(ts) or t.index(tt) < t.index(ts):
					g, t = self.seperate(ts, a, t, aa, True)
			c = ["discard", self.digit(a, self.cond[0]), f"Name=_{self.name(a, self.cond[1], s='n')}", "upto"]
			self.cond[0] += 1
			self.cond[1] += 2
			if "put it in any slot on the stage" in t or "put it on any position of your stage" in t:
				c.append("Stage")
			elif "put it in a back stage slot" in t:
				c.extend(["Stage", "Back"])
			elif "put it on the stage position that this was on" in t or "put it in the slot this was in" in t or "put it on this's stage position as the defending character" in t:
				c.extend(["Stage", "Change"])
			elif "put it in an empty slot on the stage" in t:
				c.extend(["Stage", "Open"])
			elif "put it face-down under this as marker" in t:
				c.insert(0, c[1])
				c[1] = "marker"
				del c[2]
				c.extend(["Hand", "show"])

			if "at the beginning of your next" in t:
				c.extend(["extra", "do", [-21, self.name(a, s='at'), 3, "give"]])
		elif "choose up to   in your waiting room" in t or "choose up to   from your waiting room" in t:
			if "put them face-down under this as markers" in t:
				c = [self.digit(a, self.cond[0]), "marker", f"Name=_{self.name(a, self.cond[1], s='n')}", "Waiting", "upto", "show"]
			elif "return them to your hand" in t or "return it to your hand" in t:
				c = [self.digit(a, self.cond[0]), "salvage", f"Name=_{self.name(a, self.cond[1], s='n')}", "upto", "show"]
		elif "choose up to   characters in your waiting room" in t or "choose up to   character in your waiting room" in t:
			tt = ""
			if "search your deck for up to" in t:
				tt = "search your deck for up to"
			elif "choose up to  character in your waiting room" in t:
				tt = "choose up to  character in your waiting room"
			if tt and t.index(tt) < t.index("choose up to   character"):
				gg, t = self.seperate("choose up to   character", a, t, aa, True)
				if f and "rest" in f and not d:
					d = gg
				else:
					g = gg

			c = [self.digit(a, self.cond[0]), "salvage", f"Trait_{self.trait(a, self.cond[2])}", "upto", "show"]
			self.cond[0] += 1
			if "return it to your hand" in t:
				if "choose  cards from your hand" in t:
					c.extend(["if", c[0]])
					c = self.discard_card(c, a, t)
			elif "put them in your stock" in t or "put it in your stock" in t:
				c.extend(["Stock"])
				if "(climax and events are regarded as  power)" in t:
					self.cond[0] += 1
			elif "put them on the bottom of the clock in any order" in t:
				c.extend(["Clock", "bottom"])
				if "at the end of the turn" in t and "put the bottom x cards of your clock in the waiting room" in t:
					if "x = # of cards put in clock via this effect" in t:
						c.extend(["extra", "if", 1, "do", [-21, f"[AUTO] {a[a.lower().index('at the end of the turn'):a.lower().index('. x') + 1]}", 1, "give", "xreplacetext", "xlenextra"]])

			if "and reveal the top card of your deck" in t:
				_ = d
				d = c
				c = _
			if "deal  damage to" in t:
				gg, t = self.seperate("deal  damage to", a, t, aa)
				c.extend(gg)
		elif "choose up to  characters in your waiting room" in t or "choose up to  character in your waiting room" in t:
			c = [self.digit(a, self.cond[0]), "salvage", "Character", "upto", "show"]
			self.cond[0] += 1
			if "put it in stock" in t:
				c.append("Stock")
			if " with  in the name" in t:
				c[2] = f"CName_{self.name(a, self.cond[1], s='n')}"
				self.cond[1] += 2
			elif "with  or " in t and "» or «" in aa:
				c[2] = f"Trait_{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"
				self.cond[2] += 2
			c = self.discard_card(c, a, t)
		elif ("choose up to  character in your hand" in t or ("choose up to  character" in t and "in your hand" in t)) and ("put it on any position of your stage" in t or "put it in any slot on the stage" in t or "put it in any position of your stage" in t):
			c = ["discard", self.digit(a, self.cond[0]), f"Character", "upto", "Stage"]
			self.cond[0] += 1
			if "with  in name whose level is less than or equal to your level plus  " in t:
				c[2] = f"CLevelN_standby_{self.name(a, s='n')}"
				self.cond[0] += 1
			elif "whose level = or lower than your level" in t or "with level equal to or lower than your level" in t:
				c[2] = f"CLevel_<=p"
				if "that character gets + power" in t:
					c += ["extra", "do", [-16, self.digit(a, self.cond[0]), x, "power"]]
					self.cond[0] += 1
		elif "choose up to  character with  in its card name in your hand" in t:
			if "put it on the stage position that this was on" in t:
				c = ["discard", self.digit(a, self.cond[0]), f"Name_{self.name(a, s='n')}", "Stage", "Change", "upto"]
		elif "choose up to  characters with  in name in your waiting room" in t:
			if "return them to your hand" in t:
				c = [self.digit(a), "salvage", f"Name_{self.name(a, s='n')}", "show", "upto"]
		elif "choose up to  of your  character" in t:
			c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "", "Trait", self.trait(a, self.cond[2]), "upto"]
			if "characters get + power" in t:
				c[3] = "power"
			elif "characters get + soul" in t:
				c[3] = "soul"
			self.cond[0] += 2
			self.cond[2] += 1
		elif "choose up to  of your other character" in t or "choose up to  other of your character" in t:
			if "put them in your waiting room" in t or "put them in the waiting room" in t:
				c = [self.digit(a, self.cond[0]), "waitinger"]
			elif "put them in your memory" in t or "put it in your memory" in t:
				c = [self.digit(a, self.cond[0]), "memorier"]
				if "at the beginning of your next draw phase" in t:
					c.extend(["do", [-21, self.name(a, s='at'), 3, "give", "expass", self.digit(a, self.cond[0]), "ex_ID="]])
			elif "put it in stock" in t:
				c = [self.digit(a, self.cond[0]), "stocker"]
			elif "return them to your hand" in t or "return them to hand" in t:
				c = [self.digit(a, self.cond[0]), "hander"]
				if "your other characters and up to  of your opponent's character" in t:
					t = f"choose up{t.split('your other characters and up')[1]}"
			elif "those characters get + power and + soul" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power", "extra", "do", [-16, self.digit(a, self.cond[0] + 2), x, "soul"]]
				self.cond[0] += 2
			elif "those characters get" in t and "get \"[" in aa:
				c = [self.digit(a, self.cond[0]), self.name(a, s='a'), x, "give"]
			elif "that character gets +x power" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power"]
				if "x =  times level of that character" in t:
					c.extend(["X", "xlevel", "x", self.digit(a, self.cond[0] + 1)])
				self.cond[0] += 2

			if "do" in c:
				c.insert(c.index("do"), "Other")
				c.insert(c.index("do"), "upto")
			else:
				c.extend(["Other", "upto"])

			self.cond[0] += 1
			if "deal x damage to" in t:
				if "x = the number of characters put in your waiting room" in t or "x = # of characters put in the waiting room" in t:
					c.append("extra")
				gg, t = self.seperate("deal x damage to", a, t, aa)
				c.extend(gg)
			elif "choose up to  of your opponent" in t:
				gg, t = self.seperate("choose up to  of your opponent", a, t, aa)
				c.extend(gg)
		elif "choose up to  of your character" in t:
			if "those characters gets + power" in t or "those characters get + power" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "upto", "power"]
				self.cond[0] += 1
				if "power and «" in aa:
					c.extend(["extra", "do", [-16, self.trait(a, self.cond[2]), x, "trait"]])
					self.cond[2] += 1
			elif "they get the following ability" in t:
				c = [self.digit(a, self.cond[0]), self.name(a, s='a'), x, "give"]
			elif "that character gets + power" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power", "upto"]
				self.cond[0] += 1
			elif "that character gets + level" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "level", "upto"]
				self.cond[0] += 1
			elif "put them in your waiting room" in t:
				c = [self.digit(a, self.cond[0]), "waitinger", "upto"]
				if "x = the total level and cost of the characters put in your waiting room" in t:
					c.extend(["if", 0, "extra"])
			self.cond[0] += 1
			if "search your deck for up to" in t:
				gg, t = self.seperate("search your deck for up to", a, t, aa)
			if gg:
				if "do" in c:
					c[c.index("do") + 1].extend(gg)
				else:
					c.extend(gg)
		elif "choose up to  cards in your opponent's waiting room" in t or "choose up to  card in your opponent's waiting room" in t:
			if "deal  damage to your opponent" in t:
				tt = "deal  damage to your opponent"
				if "choose up to  cards in your opponent" in t:
					ts = "choose up to  cards in your opponent"
				elif "choose up to  card in your opponent" in t:
					ts = "choose up to  card in your opponent"
				if t.index(tt) < t.index(ts):
					gg, t = self.seperate(ts, a, t, aa, True)
					g = gg
			c = [self.digit(a, self.cond[0]), "salvage", ""]
			self.cond[0] += 1
			if "put it on top of the deck" in t:
				c.extend(["Library", "upto", "opp", "top", "show"])
			elif "return them to your opponent's deck" in t or "return it to the deck" in t or "return them to their deck" in t or "return them to the deck" in t:
				c.extend(["Library", "upto", "opp", "show"])
		elif "choose up to  cost  or lower character in your hand" in t:
			if "put it on any position of your stage" in t:
				c = ["discard", self.digit(a, self.cond[0]), f"CCost_<={self.digit(a, self.cond[0] + 1)}", "Stage", "upto"]
		elif "choose up to  cost  or lower  character in your waiting room" in t and "» character" in aa:
			c = [self.digit(a, self.cond[0]), "salvage", f"CCost_<={self.digit(a, self.cond[0] + 1)}", "upto", "show"]
			self.cond[0] += 1
			if "either return it to your hand" in t and "or put it rested in any slot on the stage" in t:
				c.extend(["choice", "StageRest"])
		elif "choose up to  cost  or lower character in your waiting room" in t:
			c = [self.digit(a, self.cond[0]), "salvage", f"CCost_<={self.digit(a, self.cond[0] + 1)}", "show", "upto"]
			self.cond[0] += 1
			if "put them in separate slots on the stage" in t:
				c.append("Stage")
		elif "choose up to  level  or lower character in your hand" in t:
			c = ["discard", self.digit(a, self.cond[0]), f"CLevel_<={self.digit(a, self.cond[0] + 1)}", "upto"]
			self.cond[0] += 2
			if "whose cost is  or lower" in t:
				c[2] = f'{c[2].split("_")[0]}C_{c[2].split("_")[1]}_<={self.digit(a, self.cond[0])}'
			if "put it in any slot on the stage" in t:
				c.extend(["Stage"])
		elif "choose up to  level x or lower  character in your waiting room" in t:
			c = [self.digit(a, self.cond[0]), "salvage", f"TraitL_{self.trait(a, self.cond[2])}_<=x", "show", "upto"]
			self.cond[0] += 1
			self.cond[2] += 1
			if "x = the total level of the cards put in your waiting room" in t or "x = sum of levels of cards put in the waiting room" in t:
				c.append("xsmlevel")
			elif "x = the level of that card" in t:
				c.append("xsmlevel")

			if "if you choose  level  or higher character card this way" in t:
				c.extend(["if", self.digit(a, self.cond[0]), "ifLevel", self.digit(a, self.cond[0] + 1)])
				self.cond[0] += 2

				gg, t = self.seperate("if you choose  level  or higher character card this way", a, t, aa)
				c.extend(gg)
		elif "choose up to  level  or lower character in your waiting room" in t:
			if "put them on separate positions of your stage" in t:
				c = [self.digit(a, self.cond[0]), "salvage", f"CLevel_<={self.digit(a, self.cond[0] + 1)}", "Stage", "separate", "upto"]
		elif "choose up to  level  or lower  characters in your waiting room" in t:
			if "put them in separate position on your center stage" in t:
				c = [self.digit(a, self.cond[0]), "salvage", f"TraitL_{self.trait(a, self.cond[2])}_<={self.digit(a, self.cond[0] + 1)}", "Stage", "Center", "separate", "upto"]
				if "at the start of the encore step, if those characters are on stage, return them to the deck" in t:
					c.extend(["extra1", "do", [-21, "[AUTO] At the beginning of the encore step, if those characters are on stage, return them to your deck", 1, "give"]])
		elif "choose up to  level  or lower  character in your hand" in t:
			if "put it in any slot on the stage" in t:
				c = ["discard", self.digit(a, self.cond[0]), f"TraitL_{self.trait(a, self.cond[2])}_<={self.digit(a, self.cond[0] + 1)}", "Stage", "upto"]
				self.cond[0] += 2
		elif "choose up to  cost  or lower character in your opponent's" in t:
			if "put it in the waiting room" in t:
				c = [self.digit(a, self.cond[0]), "waitinger", "Opp", "Center", "Cost", f"<={self.digit(a, self.cond[0] + 1)}", "upto"]
		elif "choose up to  of your opponent's level  or lower character" in t or "choose up to  level  or lower character in your opponent" in t or "choose up to  level  or lower characters in opponent" in t or "choose up to  level  or lower characters in your opponent" in t:
			c = [self.digit(a, self.cond[0])]
			self.cond[0] += 1
			if "put that character into the stock" in t:
				c.append("stocker")
			elif "put it in clock" in t or "put them in clock" in t:
				c.append("clocker")
			elif "put them on the bottom of your opponent's deck" in t:
				c.extend(["decker", "bottom"])
			elif "return it to your opponent's deck" in t or "return it to their deck" in t:
				c.append("decker")
			elif "return it to hand" in t:
				c.append("hander")
			elif "put it in his or her waiting room" in t:
				c.append("waitinger")
			elif "that character does not stand during your opponent's next stand phase" in t or "those characters do not stand during your opponent's next stand phase" in t:
				c.extend(["[CONT] This cannot [STAND] during your stand phase", 2, "give"])
			c.extend(["Level", f"<={self.digit(a, self.cond[0])}", "Opp", "upto"])
			self.cond[0] += 1
			if "opponent's center stage" in t or "opponent's level  or lower characters in the center stage" in t:
				c.append("Center")

			if "and at the end of the turn, put this in the waiting room" in t:
				c.extend(["do", [0, "[AUTO] At the end of the turn, put this in the waiting room.", -3, "give"]])
				t = t[:t.index("and at the end of the turn")]
			if "choose  of your character" in t:
				gg, t = self.seperate("choose  of your character", a, t, aa)
			if gg:
				if "do" in c:
					c[c.index("do") + 1].extend(gg)
				else:
					c.extend(gg)
		elif "choose up to  of your opponent's character" in t:
			if "return that character to their hand" in t or "return it to the hand" in t or "return it to hand" in t or "return it to your opponent's hand" in t or "return it to their hand" in t or "return them to hand" in t or "return it to his or her hand" in t:
				c = [self.digit(a, self.cond[0]), "hander", "Opp", "upto"]
				self.cond[0] += 1
			elif "that character gets + soul and the following ability" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "soul", "Opp", "upto", "extra", "do", [-16, self.name(a, s='a'), x, "give"]]
				self.cond[0] += 2
			elif "that character gets - power" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power", "Opp", "upto"]
				self.cond[0] += 2
			elif "send it to memory" in t or "put it into their memory" in t:
				c = [self.digit(a, self.cond[0]), "memorier", "Opp", "upto"]
				self.cond[0] += 1
				if "your opponent puts that character from memory to any slot on their stage" in t or "your opponent puts that character from their memory on any position of their stage" in t:
					c.extend(["extra", "if", c[0], "do", [-16, "msalvage", "ID=_x", "Stage", "Opp", "oppturn", "opp"]])
					self.cond[0] += 1

			if "choose  of your  or" in t:
				gg, t = self.seperate("choose  of your  or", a, t, aa)
				c.extend(gg)
		elif "choose up to  other character in your opponent" in t:
			if "choose  cost  or lower" in t:
				tt = "choose  cost  or lower"
				if t.index(tt) < t.index("choose up to  other") or t.index(tt) < t.index("choose   or  in your waiting"):
					gg, t = self.seperate("choose up to  other", a, t, aa, True)
					g = gg
			if "put it on bottom of the deck" in t:
				c = [self.digit(a, self.cond[0]), "decker", "bottom", "Opp"]
				self.cond[0] += 1

			if "opponent's center stage" in t:
				c.append("Center")
			if "with the same name as that character" in t:
				c.extend(["Name=", "same_name"])
				if g:
					g.append("save_name")
		elif "choose   marker under this" in t or "choose   from under this as marker" in t:
			if "put it on any position of your stage" in t:
				c = [self.digit(a), "ksalvage", f"Name=_{self.name(a, s='n')}", "Stage"]
				if "at the end of the turn" in t and ("you may place that character face-up" in t or "you may put that character face up" in t) and ("under this as marker" in t or "under this as a marker" in t):
					c += ["extra", "do", [0, "[AUTO] At the end of the turn, you may put the previously chosen character face up underneath this as a marker.", 1, "give", "expass", self.digit(a), "ex_ID="]]
					self.ee = False
		elif "choose  cost  or lower  character in your waiting room" in t:
			c = [self.digit(a, self.cond[0]), "salvage", f"CCostT_<={self.digit(a, self.cond[0] + 1)}_{self.trait(a, self.cond[2])}"]
			self.cond[0] += 2
			self.cond[2] += 1
			if "put it on any position of your stage" in t:
				c.append("Stage")
		elif "choose  cost  or less character with  in name in your waiting room" in t:
			c = [self.digit(a, self.cond[0]), "salvage", f"CNCost_{self.name(a, self.cond[1], s='n')}_<={self.digit(a, self.cond[0] + 1)}"]
			self.cond[0] += 2
			self.cond[1] += 2
			if "put it in the slot this was in" in t:
				c.extend(["Stage", "Change"])
		elif "choose  cost  or lower character in your clock" in t:
			c = ["cdiscard", self.digit(a, self.cond[0]), f"CCost_<={self.digit(a, self.cond[0] + 1)}"]
			self.cond[0] += 2
			if "put it in the slot this was in" in t:
				c.extend(["Stage", "Change"])
		elif "choose  level  or higher character battling this" in t:
			if "put it on bottom of the deck" in t:
				c = [self.digit(a, self.cond[0]), "decker", "bottom", "Battle", "Opp", "Level", f">={self.digit(a, self.cond[0] + 1)}"]
		elif "choose  level x or lower  character in your waiting room" in t:
			c = [self.digit(a, self.cond[0]), "salvage", f"TraitL_{self.trait(a, self.cond[2])}_<=x"]
			if "put it on any position of your stage" in t:
				c.append("Stage")
			elif "return it to your hand" in t:
				c.append("show")
			if "x = # of cards in your memory" in t or "x = the number of cards in your memory" in t:
				c.append("xqmlevel")
			elif "brainstorm" in aa and ("x = the number of  characters revealed among those cards" in t or "x = the number of  characters revealed" in t):
				c[2] = f"{c[2][:-1]}#"
				c.extend(["#trait", "#"])
			elif "x = the number of  in your waiting room" in t:
				c.extend(["xqwrlevel", "xName=", self.name(a, self.cond[1], s='n')])
			elif "x = the total level of those card" in t:
				c.append("xsmlevel")
		elif "choose  character of level x or lower in waiting room" in t or "choose  level x or lower character in your waiting room" in t:
			c = [self.digit(a, self.cond[0]), "salvage", "CLevel_<=x"]
			if "return it to hand" in t or "return it to your hand" in t:
				c.append("show")
			if "x = the level of the revealed card" in t:
				c.append("xvlevel")
			elif "x = the number of  in your waiting room" in t:
				c.extend(["xqwrlevel", "xName=", self.name(a, self.cond[1], s='n')])
		elif "choose  level  or lower  character in your waiting room" in t:
			c = [self.digit(a, self.cond[0]), "salvage", f"TraitL_{self.trait(a)}_<={self.digit(a, self.cond[0] + 1)}"]
			if "put it in any slot on the stage" in t:
				c.append("Stage")
			elif "put it rested in the slot this was in" in t:
				c.extend(["Stage", "Change", "extra", "do", [-16, "rested"]])
		elif "choose  level  or lower character in your clock" in t or "choose  level  or lower character from your clock" in t:
			c = ["cdiscard", self.digit(a, self.cond[0]), f"CLevel_<={self.digit(a, self.cond[0] + 1)}"]
			self.cond[0] += 2
			if "put it in any slot on stage" in t or "put it in any slot on the stage" in t or "put it on any position of your stage" in t:
				c.extend(["Stage"])
				if "that character gets «" in aa:
					c.extend(["extra", "do", [-16, self.trait(a, self.cond[2]), x, "trait"]])
					self.cond[2] += 1
			if "character in your clock with  in name" in t:
				c[2] = f"{c[2].replace('CLevel', 'CLevelN')}_{self.name(a, self.cond[1], s='n')}"
			if "if you do," in t or "if so," in t:
				c.extend(["if", c[1]])
			if "at the next end of your opponent's turn" in t and "put that character in clock" in t:
				c.extend(["extra", "do", [-16, "[AUTO] At the end of of your opponent's next turn, put this card into your clock.", -3, "give"]])
		elif "choose  level  or lower character in your waiting room" in t:
			c = [self.digit(a, self.cond[0]), "salvage", f"CLevel_<={self.digit(a, self.cond[0] + 1)}"]
			self.cond[0] += 1
			if "put it in any slot in the back stage" in t:
				c.extend(["Stage", "Back"])
			elif "put it in an empty slot in the back stage" in t:
				c.extend(["Stage", "Back", "Open"])
			elif "put it on any position of your stage" in t or "put it in any slot on the stage" in t:
				c.append("Stage")
			elif "put it in the slot this was in" in t:
				c.extend(["Stage", "Change"])
			if "in your waiting room with  in name" in t:
				c[2] = f"CLevelN_<={self.digit(a, self.cond[0])}_{self.name(a, self.cond[1], s='n')}"
				self.cond[1] += 2
			self.cond[0] += 1
		elif "choose  level  or lower character opposite this" in t:
			if "put it on top of the deck" in t:
				c = [self.digit(a, self.cond[0]), "decker", "top", "Opp", "Level", f"<={self.digit(a, self.cond[0] + 1)}", "Opposite"]
				self.cond[0] += 2
		elif "choose  level  or higher character in your waiting room" in t:
			if "return it to your hand" in t:
				c = [self.digit(a), "salvage", f"CLevel_>={self.digit(a, 1)}", "show"]
		elif "choose  level  or lower  character in your clock" in t:
			if "put it on any position of your stage" in t:
				c = [self.digit(a, self.cond[0]), "csalvage", f"TraitL_{self.trait(a, self.cond[2])}_<={self.digit(a, self.cond[0] + 1)}", "Stage"]
		elif "choose  of your level  or higher character" in t:
			if "that character gets + level" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 2), x, "level", "Level", f">={self.digit(a, self.cond[0] + 1)}"]
				self.cond[0] += 3
				if "level and + power" in t:
					c.extend(["extra", "do", [-16, self.digit(a, self.cond[0]), x, "power"]])
					self.cond[0] += 1
			elif "that character gets + power" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 2), x, "power", "Level", f">={self.digit(a, self.cond[0] + 1)}"]
				self.cond[0] += 3
		elif "choose  of your other level  or lower character" in t:
			if "that character gets + power" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 2), x, "power", "Other", "Level", f"<={self.digit(a, self.cond[0] + 1)}"]
		elif "choose  of your other characters with  in name" in t or "choose  of your other characters with  in its card name" in t:
			if "put it in your stock" in t:
				c = [self.digit(a, self.cond[0]), "stocker"]
			elif "that character gets the following ability" in t:
				c = [self.digit(a, self.cond[0]), self.name(a, self.cond[1], s='a'), x, "give"]
			elif "that character gets + level" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "level"]
				self.cond[0] += 2
				if "level and + power" in t:
					c.extend(["extra", "do", [-16, self.digit(a, self.cond[0]), x, "power"]])
					self.cond[0] += 1
			elif "that character gets + power" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power"]
			c.extend(["Name", self.name(a, self.cond[1], s='n'), "Other"])
		elif "choose  climax in your waiting room" in t or "choose  climax card in your waiting room" in t:
			if "return it to your hand" in t:
				c = [self.digit(a), "salvage", "Climax", "show"]
		elif "choose   character in your waiting room" in t or "choose   character from your waiting room" in t or "choose   or  in your waiting room" in t or ("choose   character or " in t and "from your waiting room" in t) or ("choose  character with  or " in t and " in your waiting room" in t):
			if "choose  of your stand character" in t or "choose  of your standing character" in t:
				if "choose  of your stand character" in t:
					tt = "choose  of your stand character"
				elif "choose  of your standing character" in t:
					tt = "choose  of your standing character"
				if t.index(tt) < t.index("choose   character ") or t.index(tt) < t.index("choose   or  in your waiting"):
					gg, t = self.seperate("choose   character in your waiting room", a, t, aa, True)
					g = gg
					gg = ""
			c = [self.digit(a, self.cond[0]), "salvage", f"Trait_{self.trait(a, self.cond[2])}"]
			if ("choose   or  " in t or "choose  character with" in t) and "» or «" in aa:
				c[2] = f"Trait_{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"
				self.cond[2] += 1
			elif ("choose   or  " in t or "choose  character with  or  in its card name") and "\" or \"" in aa:
				c[2] = f"Name_{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}"
				self.cond[1] += 4
			elif "character or character with  in its card name" in t:
				c[2] = f"TraitN_{self.trait(a, self.cond[2])}_{self.name(a, self.cond[1], s='n')}"
				self.cond[1] += 2
				self.cond[2] += 1
			elif "whose level = or lower than your level" in t:
				c[2] = f"TraitL_{self.trait(a, self.cond[2])}_<=p"
			self.cond[0] += 1
			self.cond[2] += 1

			if "you may choose   character in your waiting room" in t:
				c.append("upto")

			if "return it to your hand" in t or "return it to hand" in t or "put it in your hand" in t:
				c.append("show")
				c = self.discard_card(c, a, t)
			elif "put it in your stock" in t or "put it in stock" in t:
				c.extend(["Stock", "show"])
			elif "put it face-up under this as marker" in t:
				c[1] = "marker"
				c.extend(["Waiting", "show", "face-up"])
			elif "put it face-down under this as marker" in t:
				c[1] = "marker"
				c.extend(["Waiting", "show"])
			elif "put it rested in any slot on the stage" in t:
				c.extend(["Stage", "extra", "do", [-16, "rested"]])

			if "choose  of your other" in t:
				gg, t = self.seperate("choose  of your other", a, t, aa)
			elif "choose  of your  character" in t:
				gg, t = self.seperate("choose  of your  character", a, t, aa)
			if gg:
				if "do" in c:
					c[c.index("do") + 1].extend(gg)
				else:
					c.extend(gg)
		elif "choose  character in your waiting room" in t or "choose  of your character in your waiting room" in t or "choose  character from your waiting room" in t or "choose  of your characters in your waiting room" in t or "choose  characters in your waiting room" in t:
			c = [self.digit(a, self.cond[0]), "salvage", "Character"]
			self.cond[0] += 1

			if "you may choose  character" in t:
				c.append("upto")

			if "return it to your hand" in t or "return them to your hand" in t:
				c.append("show")
				c = self.discard_card(c, a, t)
				if "choose  of your character" in t:
					gg, t = self.seperate("choose  of your character", a, t, aa)
				elif "choose  of your  character" in t:
					gg, t = self.seperate("choose  of your  character", a, t, aa)
				if gg:
					if "do" in c:
						c[c.index("do") + 1].extend(gg)
					else:
						c.extend(gg)
			elif "place it to any slot on your stage" in t or "put it on any position of your stage" in t:
				c.append("Stage")
			elif "put it on the stage position that this was on" in t:
				c.extend(["Stage", "Change"])
			elif "put it in your stock" in t:
				c.extend(["Stock", "show"])

			if "if you do not" in t:
				t = self.donot_filter(t)
				if "upto" in c:
					c.extend(["if", c[0], "ifnot"])

			if ("with  or " in t or "with either  or  " in t) and "» or «" in aa:
				c[2] = f"Trait_{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"
			elif "with  or  in name" in t and "\" or \"" in aa:
				c[2] = f"Name_{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}"
			elif "that either is  or has  in name" in t and "» or has \"" in aa:
				c[2] = f"TraitN_{self.trait(a, self.cond[2])}_{self.name(a, self.cond[1], s='n')}"
			elif "with  in name" in t or "whose name includes " in t:
				c[2] = f"Name_{self.name(a, self.cond[1], s='n')}"
		elif "choose  character in your clock" in t:
			c = [self.digit(a, self.cond[0]), "csalvage", "Character", "show"]
			self.cond[0] += 1
			if "clock with  in name" in t:
				c[2] = f"Name_{self.name(a, self.cond[1], s='n')}"
				self.cond[1] += 2
			if "you may choose  character" in t:
				c.append("upto")
			if "send it to memory" in t or "put it in your memory" in t:
				c.append("Memory")
			elif "return it to your hand" in t:
				if "choose  card in your hand" in t:
					if "put it in your clock" in t:
						c.extend(["if", c[0], "do", ["discard", self.digit(a, self.cond[0]), "", "Clock"]])
				if "choose  of your opponent's character" in t:
					gg, t = self.seperate("choose  of your opponent's character", a, t, aa)
					c.extend(gg)
		elif "choose  character with a level equal to or lower than your level + in your hand" in t or "choose  character with a level equal to or less than your level + in your hand" in t:
			c = ["discard", self.digit(a, self.cond[0]), f"CLevel_<=p+{self.digit(a, self.cond[0] + 1)}"]
			if "put it on the stage position this was on" in t:
				c.extend(["Stage", "Change"])
			elif "put it on any position of your stage as rest" in t:
				c.extend(["Stage", "extra", "do", [-16, "rested"]])
		elif "choose   character with level equal to or lower than your level in your waiting room" in t:
			c = [self.digit(a, self.cond[0]), "salvage", f"TraitL_{self.trait(a, self.cond[2])}_<=p"]
			self.cond[0] += 1
			self.cond[2] += 1
			if "put it on the stage position that this was on" in t:
				c.extend(["Stage", "Change"])
		elif "choose  character in your hand" in t and ("place it to any slot on your stage" in t):
			c = ["discard", self.digit(a, self.cond[0]), "Character", "Stage"]
			if "any slot on your stage rested" in t:
				c.extend(["extra", "do", [-16, "rested"]])
			if "hand that = or lower in level than  + your level" in t:
				c[2] = "CLevel_standby"
		elif "choose  card in your clock" in t or "choose  character card in your clock" in t:
			if "return it to your hand" in t:
				c = [self.digit(a, self.cond[0]), "csalvage", ""]
				if "you may choose  character" in t:
					c.append("upto")
				self.cond[0] += 1
				if "choose  card in your hand" in t:
					if "put it in your clock" in t or "put it in clock" in t:
						c.extend(["if", c[0], "do", ["discard", c[0], "", "Clock"]])
			elif "put it in the waiting room" in t:
				c = ["cdiscard", self.digit(a, self.cond[0]), ""]
		elif "choose  card in your waiting room" in t:
			c = [self.digit(a, self.cond[0]), "salvage", ""]
			self.cond[0] += 1
			if "put it on any position of your stage" in t:
				c.append("Stage")
			elif "return it to your deck" in t:
				c.append("Library")
			elif "put it in your stock" in t:
				c.append("Stock")
			if "with the same card name as a character on your stage" in t or "with the same card name as  character on your stage" in t:
				c[2] = f"Name=_x"
				c.insert(3, "xStage")
				if "as  character" in t:
					self.cond[0] += 1
		elif ("choose  character with either  or  in your waiting room" in t or "choose   or  character in your waiting room" in t) and "» or «" in aa:
			c = [self.digit(a, self.cond[0]), "salvage", f"Trait_{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}", "show"]
			self.cond[0] += 1
			self.cond[2] += 2
			if "return it to your hand" in t or "return it to hand" in t:
				c = self.discard_card(c, a, t)
			elif "put it in your stock" in t:
				c.append("Stock")
			if "choose  of your other  or  character" in t:
				gg, t = self.seperate("choose  of your other  or  character", a, t, aa)
				c.extend(gg)
		elif "choose   or  from your waiting room" in t and "\" or \"" in aa:
			if "return it to hand" in t:
				c = [self.digit(a, self.cond[0]), "salvage", f"Name=_{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}", "show"]
		elif ("choose   in your waiting room" in t and "\" in your waiting room" in aa) or "choose  card named  in your waiting room" in t:
			if "choose   in your waiting room" in t:
				ts = "choose   in your waiting room"
			elif "choose  card named  in your waiting room" in t:
				ts = "choose  card named  in your waiting room"
			if "put this in the waiting room" in t:
				tt = "put this in the waiting room"
				if t.index(tt) < t.index(ts):
					gg, t = self.seperate(ts, a, t, aa, True)
					g = gg
			elif "at the start of your next" in t:
				tt = "at the start of your next"
				if t.index(tt) < t.index(ts):
					t = t.split(ts)[0]
			if "choose   in your memory" in t:
				tt = "choose   in your memory"
				if t.index(ts) < t.index(tt) and "return it to your hand" in t and "put it in any slot on the stage" in t:
					t1 = f'choose   in your memory{t.split("choose   in your memory")[1]}'
					t = t.split("choose   in your memory")[0]
			if "put it on the stage position that this was on as rest" in t or "put it on the stage position this was on as rest" in t or "put it rested in the slot this was in" in t or "put it on any position of your stage as rest" in t:
				c = [self.digit(a), "salvage", f"Name=_{self.name(a, s='n')}", "Stage", "Change", "extra", "do", [-16, "rested"]]
			elif "put it on any position of your stage" in t or "put it in any slot on the stage" in t or "put it in any slot on stage" in t or "put it on any slot on your stage" in t or "put it in any position of your stage" in t:
				c = [self.digit(a, self.cond[0]), "salvage", f"Name=_{self.name(a, self.cond[1], s='n')}", "Stage"]
				if "discard  card from your hand to the waiting room" in t:
					c += ["do", ["discard", self.digit(a, self.cond[0] + 1), ""]]
			elif "put it rested in any slot on the stage" in t:
				c = [self.digit(a, self.cond[0]), "salvage", f"Name=_{self.name(a, self.cond[1], s='n')}", "Stage", "extra", "do", [-16, "rested"]]
			elif "put it rested in a vacant slot on the stage" in t:
				c = [self.digit(a, self.cond[0]), "salvage", f"Name=_{self.name(a, self.cond[1], s='n')}", "Stage", "Open", "extra", "do", [-16, "rested"]]
				if "put this face-down under it as marker" in t:
					c[c.index("do") + 1].extend(["extra", "do", [1, "marker", "", "Stage", "targetunderthis", "target", -16]])
			elif "put it in the slot this was in" in t or "put it on the stage position that this was on" in t or "put it on the stage position this was on" in t or "place it to the slot this was in" in t or "put it in the stage position that this was in" in t:
				c = [self.digit(a, self.cond[0]), "salvage", f"Name=_{self.name(a, self.cond[1], s='n')}", "Stage", "Change"]
				if "that character gets the following ability" in t:
					c.extend(["extra", "do", [-16, self.name(a, s='a'), x, "give"]])
			elif "put it in any slot in the back stage" in t:
				c = [self.digit(a, self.cond[0]), "salvage", f"Name=_{self.name(a, self.cond[1], s='n')}", "Stage", "Back"]
			elif "put it face up under this as a marker" in t or "put it face-up under this as marker" in t or "place it face up under this as marker" in t:
				c = [self.digit(a, self.cond[0]), "marker", f"Name=_{self.name(a, self.cond[1], s='n')}", "Waiting", "show", "face-up"]
			elif "put it face-down under this as marker" in t or "put it face down under this as a marker" in t:
				c = [self.digit(a, self.cond[0]), "marker", f"Name=_{self.name(a, self.cond[1], s='n')}", "Waiting", "show"]
			elif "put it on the bottom of your deck" in t:
				c = [self.digit(a, self.cond[0]), "salvage", f"Name=_{self.name(a, self.cond[1], s='n')}", "Library", "bottom", "show"]
			elif "return it to your hand" in t or "return it to hand" in t:
				c = [self.digit(a, self.cond[0]), "salvage", f"Name=_{self.name(a, self.cond[1], s='n')}", "show"]
				self.cond[0] += 1
				self.cond[1] += 2
			elif "send it to memory" in t or "put it in your memory" in t:
				c = [self.digit(a, self.cond[0]), "salvage", f"Name=_{self.name(a, self.cond[1], s='n')}", "Memory"]
			if t1:
				t += t1
			if "choose   in your memory" in t:
				gg, t = self.seperate("choose   in your memory", a, t, aa)
				c.extend(gg)
		elif "choose  of your characters with assist in your waiting room" in t:
			c = [self.digit(a), "salvage", f"CText_{self.text_name['Assist']}"]
			if "return it to your hand" in t:
				c += ["show"]
		elif "choose  character with  in its card name except  in your waiting room" in t:
			c = [self.digit(a), "salvage", f"NameO_{self.name(a, s='n')}_{self.name(self.name(a, 2, s='n'))}"]
			if "return it to your hand" in t:
				c += ["show"]
		elif "choose  character with  in name in your waiting room" in t or "choose  character with  in its card name in your waiting room" in t:
			c = [self.digit(a, self.cond[0]), "salvage", f"Name_{self.name(a, self.cond[1], s='n')}", "show"]
			self.cond[0] += 1
			self.cond[1] += 2
		elif "choose   in your clock" in t and "\" in your clock" in aa:
			if "put it in any slot on stage" in t:
				c = ["cdiscard", self.digit(a, self.cond[0]), f"Name=_{self.name(a, self.cond[1], s='n')}", "Stage"]
				self.cond[0] += 1
			if "choose  card in your hand" in t:
				if "put it in your clock" in t:
					c.extend(["do", ["discard", self.digit(a, self.cond[0]), "", "Clock"]])
		elif "choose   character in your clock" in t:
			c = [self.digit(a), "csalvage", f"Trait_{self.trait(a)}"]
			if "put it at the bottom of your deck" in t or "put it on the bottom of your deck" in t:
				c += ["Library", "bottom", "show"]
			elif "return it to your hand" in t:
				c += ["show"]
				if "put  card from your hand to the clock" in t:
					c += ["do", ["discard", self.digit(a, 1), "", "Clock"]]
		elif "choose  of your characters in battle" in t or "choose  of your battling characters" in t or "choose  character in battle" in t:
			if "that character gets +x power" in t:
				if "x =  multiplied by the number of characters you have with  or " in t and "\" or \"" in aa:
					c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "X", "xName", f"{self.name(a, self.cond[1])}_{self.name(a, self.cond[1] + 2)}", "Battle", "x", self.digit(a, self.cond[0] + 1), "at", "power"]
					self.cond[1] += 4
				elif "x =  multiplied by your level" in t or "x =  times your level" in t:
					c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "X", "xplevel", "Battle", "x", self.digit(a, self.cond[0] + 1), "power"]
				elif "x =  times # of your reverse character" in t:
					c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "X", "xReverse", "Battle", "x", self.digit(a, self.cond[0] + 1), "power"]
				self.cond[0] += 2
			elif "that character gets the following ability" in t or ("that character gets " in t and "gets \"[" in aa):
				c = [self.digit(a, self.cond[0]), self.name(a, s='a'), x, "give", "Battle"]
				self.cond[0] += 1
				t1 = ""
				if "choose  of your characters in battle" in t:
					t1 = t.split("choose  of your characters in battle")[1]
				elif "choose  of your battling characters" in t:
					t1 = t.split("choose  of your battling characters")[1]
				elif "choose  character in battle" in t:
					t1 = t.split("choose  character in battle")[1]
				if "choose  of your character" in t1:
					gg, t = self.seperate("choose  of your character", a, t, aa)
					c.extend(gg)
			elif "that character gets + power" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power", "Battle"]
				self.cond[0] += 2
				if "gets + power and  " and "and «" in aa:
					c.extend(["extra", "do", [-16, self.trait(a, self.cond[2]), x, "trait"]])
					self.cond[2] += 1
		elif "choose   in your hand" in t or "choose  card named  in your hand" in t or "choose   character in your hand" in t:
			if "put it in the slot this was in" in t or "put it on the stage position that this was on" in t:
				c = ["discard", self.digit(a, self.cond[0]), "", "Stage", "Change"]
			elif "put them in the waiting room" in t or "put it in the waiting room" in t:
				c = ["discard", self.digit(a, self.cond[0]), ""]
				if "if so" in t:
					c.extend(["if", c[1]])

			if "card named \"" in aa:
				c[2] = f"Name_{self.name(a, self.cond[1], s='n')}"
			elif "\" in your hand" in aa:
				c[2] = f"Name=_{self.name(a, self.cond[1], s='n')}"
			elif "» character" in aa or "» in your hand" in aa:
				if "whose level = or lower than your level" in t:
					c[2] = f"TraitL_{self.trait(a, self.cond[2])}_<=p"
				else:
					c[2] = f"Trait_{self.trait(a, self.cond[2])}"
		elif "choose   in your climax area" in t:
			if "return it to your hand" in t:
				c = [1, "hander", "Climax"]
		elif "choose  card named  in your memory" in t and "\" in your memory" in aa:
			c = [self.digit(a, self.cond[0]), "msalvage", f"Name=_{self.name(a, self.cond[1], s='n')}"]
			self.cond[0] += 1
			self.cond[2] += 2
			if "put it on any position of your stage" in t:
				c.append("Stage")
		elif "choose   in your memory" in t and "\" in your memory" in aa:
			if "send this to memory" in t:
				tt = "send this to memory"
				ts = "choose   in your memory"
				if t.index(tt) < t.index(ts):
					gg, t = self.seperate(ts, a, t, aa, True)
					g = gg
			if "put it in the stock" in t:
				c = ["mdiscard", self.digit(a, self.cond[0]), f"Name=_{self.name(a, self.cond[1], s='n')}", "Stock", "show"]
				self.cond[0] += 1
				self.cond[1] += 2
			else:
				c = [self.digit(a, self.cond[0]), "msalvage", f"Name=_{self.name(a, self.cond[1], s='n')}"]
				self.cond[0] += 1
				self.cond[1] += 2
				if "put it on any position on your stage" in t or "put it on any position of your stage" in t or "put it in any slot on the stage" in t:
					c.append("Stage")
					if "that character gets + power" in t:
						c.extend(["extra", "do", [-16, self.digit(a, self.cond[0]), x, "power"]])
						self.cond[0] += 1
					elif "put the top card of your deck under that character as marker" in t:
						c.extend(["extra", "do", [1, "marker", "top", "target", -16]])
				elif "put it in the slot this was in" in t or "put it on the stage position that this was on" in t:
					c.extend(["Stage", "Change"])
		elif "choose   on your stage" in t and "\" on your stage" in aa:
			if "put it in the waiting room" in t:
				c = [self.digit(a, self.cond[0]), "waitinger"]
			elif "return it to your hand" in t:
				c = [self.digit(a, self.cond[0]), "hander"]
			c.extend(["Name=", self.name(a, self.cond[1], s='n')])
		elif "choose  cards in your memory" in t:
			if "put all cards except those cards in your waiting room" in t or "put all cards in your memory except those cards in your waiting room" in t:
				c = ["mdiscard", self.digit(a, self.cond[0]), "", "invert"]
		elif "choose  of your stand  character" in t or "choose  of your standing  character" in t:
			if "rest it" in t or "rest them" in t:
				c = [self.digit(a, self.cond[0]), "rest", "Stand", "Trait", self.trait(a, self.cond[2])]
				self.cond[0] += 1
				self.cond[2] += 1
		elif "choose  of your stand character" in t or "choose  of your standing character" in t:
			if "rest it" in t or "rest them" in t:
				c = [self.digit(a, self.cond[0]), "rest", "Stand"]
				self.cond[0] += 1
				if "characters with no traits" in t:
					c.extend(["Trait", ""])
				elif "standing characters with  in name" in t:
					c.extend(["Name", self.name(a, self.cond[1], s='n')])

				if "if you rest " in t:
					c.extend(["if", self.digit(a, self.cond[0])])
					self.cond[0] += 1
				elif "if you do," in t or "if so," in t:
					c.extend(["if", c[0]])

				if "search your deck for up to" in t:
					gg, t = self.seperate("search your deck for up to", a, t, aa)
					c.extend(gg)
				elif "choose  card in your opponent" in t:
					gg, t = self.seperate("choose  card in your opponent", a, t, aa)
					c.extend(gg)
				elif "choose  opponent's character" in t:
					gg, t = self.seperate("choose  opponent's character", a, t, aa)
					c.extend(gg)
				elif "choose  of your opponent's" in t:
					if t.count("choose  of your opponent") == 2:
						tt = "choose  of your opponent"
						t1 = tt + t.split(tt)[2]
					gg, t = self.seperate("choose  of your opponent's", a, t, aa)
					c.extend(gg)

					if t1:
						h = self.convert(a, t1, aa)
						tt = ""
		elif ("choose  of your " in t and "of your \"" in aa) or "choose  of your cards named " in t:
			if "put this face-down under that character as marker" in t:
				c = [self.digit(a, self.cond[0]), "marker", "Name=", self.name(a, self.cond[1], s='n'), "Stage", "thisunder", "show"]
			elif "put it in your waiting room" in t:
				c = [self.digit(a, self.cond[0]), "waitinger", "Name=", self.name(a, self.cond[1], s='n')]
				if "if you do" in t:
					c.extend(["if", c[0]])
			elif "that character gets + power" in t or "that card gets + power" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power", "Name=", self.name(a, self.cond[1], s='n')]
				self.cond[0] += 1
				if "power and + soul" in t:
					self.cond[0] += 1
					c.extend(["extra", "do", [-16, self.digit(a, self.cond[0]), x, "soul"]])
			elif "that card gets the following ability" in t:
				c = [self.digit(a, self.cond[0]), self.name(a, s='a'), x, "give", "Name=", self.name(a, self.cond[1], s='n')]
			self.cond[0] += 1
			self.cond[1] += 2

			if "you may choose  of your" in t:
				if "do" in c:
					c.insert(c.index("do"), "upto")
				else:
					c.append("upto")

			if "\" in battle" in aa:
				c.append("Battle")
			elif "choose  of your  or  or " in t and aa.count("\" or \"") == 2:
				c[c.index("Name=") + 1] += f"_{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}"
				self.cond[1] += 4
		elif "choose  of your  characters and another  of your  character" in t:
			if "they get + power" in t:
				c = [self.digit(a, self.cond[0]) + self.digit(a, self.cond[0] + 1), self.digit(a, self.cond[0] + 2), x, "power", "BTrait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"]
				self.cond[0] += 3
				self.cond[2] += 2
		elif "choose this and up to  of your other character" in t:
			if "return them to your hand" in t:
				c = [self.digit(a, self.cond[0]), "hander", "this", "upto", "Other"]
				self.cond[0] += 1
			if "you may choose this" in t:
				c.extend(["thisupto", "This"])
				c[0] += 1
		elif "choose this and  of your  character" in t or "choose  of your  characters and this" in t or "choose this and  of your other  character" in t:
			if "exchange them as stand" in t or "stand and swap them" in t:
				c = [self.digit(a, self.cond[0]), "stand", "Trait", self.trait(a, self.cond[2]), "swap", "this", "Other"]
				self.cond[0] += 1
				self.cond[2] += 1
				if "in the middle position of your center stage" in t:
					c.extend(["Middle"])
		elif ("choose  of your  or  character" in t or "choose  of your  or  or  character" in t) and "» or «" in aa:
			c = [self.digit(a, self.cond[0]), "", x, ""]
			self.cond[0] += 1
			if "that character gets + power" in t:
				c[1] = self.digit(a, self.cond[0])
				c[3] = "power"
				self.cond[0] += 1
				if "power and the following ability" in t:
					c.extend(["extra", "do", [-16, self.name(a, s='a'), x, "give"]])
			elif "that character gets + level" in t:
				c[1] = self.digit(a, self.cond[0])
				c[3] = "level"
				self.cond[0] += 1
				if "level and + power" in t:
					c.extend(["extra", "do", [-16, self.digit(a, self.cond[0]), x, "power"]])
					self.cond[0] += 1
			elif "that character gets the following ability" in t or "it gets the following ability" in t:
				c[1] = self.name(a, s='a')
				c[3] = "give"

			if aa.count("» or «") == 2:
				c.extend(["Trait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}_{self.trait(a, self.cond[2] + 2)}"])
				self.cond[2] += 1
			else:
				c.extend(["Trait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"])
			self.cond[2] += 2
			if "do" in c:
				cd = c[c.index("do") + 1]
				c.remove("do")
				c.remove(cd)
				c.extend(["do", cd])
		elif "choose  of your  character" in t:
			tt = ""
			if "choose  of your opponent's character" in t:
				tt = "choose  of your opponent's character"
			if tt:
				ts = "choose  of your  character"
				if t.index(tt) < t.index(ts):
					gg, t = self.seperate(ts, a, t, aa, True)
					g = gg

			c = [self.digit(a, self.cond[0])]
			self.cond[0] += 1
			if "that character gets + power and + soul" in t:
				if t.count("choose  of your  character") == 2:
					if t.count("that character gets + power and + soul") == 2:
						if t.count("for the turn") == 2:
							c.extend([self.digit(a, self.cond[0]), x, "power", "Trait", self.trait(a, self.cond[2]), "extra", "do", [-16, self.digit(a, self.cond[0] + 1), x, "soul", "do", [self.digit(a, self.cond[0] + 2), self.digit(a, self.cond[0] + 3), x, "power", "Trait", self.trait(a, self.cond[2] + 1), "extra", "do", [-16, self.digit(a, self.cond[0] + 4), x, "soul"]]]])
							self.cond[0] += 4
							self.cond[2] += 1
				else:
					c.extend([self.digit(a, self.cond[0]), x, "power", "Trait", self.trait(a, self.cond[2]), "extra", "do", [-16, self.digit(a, self.cond[0] + 1), x, "soul"]])
					self.cond[0] += 1
			elif "that character gets +x power" in t:
				c.extend([self.digit(a, self.cond[0]), x, "power", "#", "Trait", self.trait(a, self.cond[2]), '#trait', self.trait(a, self.cond[2] + 1)])
				self.cond[2] += 1
			elif "that character gets + power" in t:
				c.extend([self.digit(a, self.cond[0]), x, "power", "Trait", self.trait(a, self.cond[2])])

				if "power, + soul, and the following ability" in t:
					c.extend(["extra", "do", [-16, self.digit(a, self.cond[0] + 1), x, "soul", "extra", "do", [-16, self.name(a, s='a'), x, "give"]]])
					self.cond[0] += 1
				elif "gets + power and the following ability" in t:
					c.extend(["extra", "do", [-16, self.name(a, s='a'), x, "give"]])
				elif "gets + power and  " in t and "power and «" in aa:
					c.extend(["extra", "do", [-16, self.trait(a, self.cond[2] + 1), x, "trait"]])
					self.cond[2] += 1
				if "choose  of your opponent's character" in t:
					c.extend(["do", self.convert(a, "choose  of your opponent's character" + t.split("choose  of your opponent's character")[1], aa)])
				else:
					if "at the end of the turn" in t and "put that character in the waiting room" in t:
						c.extend(["extra", "do", [-16, "[AUTO] At the end of the turn, put this card into your waiting room.", -3, "give"]])
						t = t[:t.index("at the end of the turn")]
			elif "that character gets + level" in t:
				c.extend([self.digit(a, self.cond[0]), x, "Trait", self.trait(a, self.cond[2]), "level"])

				if "that character gets + level and + power" in t:
					c.extend(["extra", "do", [-16, self.digit(a, self.cond[0] + 1), x, "power"]])
					self.cond[0] += 1
			elif "that character gets + soul" in t:
				c.extend([self.digit(a, self.cond[0]), x, "Trait", self.trait(a, self.cond[2]), "soul"])
			elif "that character gets the following ability" in t:
				c.extend([self.name(a, s='a'), x, "Trait", self.trait(a, self.cond[2]), "give"])
				self.cond[0] -= 1
			elif "put it in your waiting room" in t:
				c.extend(["waitinger", "Trait", self.trait(a, self.cond[2])])

			self.cond[0] += 1
			self.cond[2] += 1
			if "\nchoose  of your  character" in t:
				c.append("dn")

			if any(f"of your {cl} character" in aa for cl in self.colour):
				c[c.index("Trait") + 1] = self.colour_t(a, self.cond[4])
				c[c.index("Trait")] = "Colour"
			elif any(f"of your non-{cl} character" in aa for cl in self.colour):
				c[c.index("Trait") + 1] = self.colour_t(a, self.cond[4])
				c[c.index("Trait")] = "ColourWo"
			if "with the same card name as the character chosen" in t:
				c.append("save_name")
			if "characters in battle" in t:
				c.append("Battle")
		elif "choose  of your other  or  character" in t or "chosose  of your other characters with  or " in t:
			if "that character gets + power" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power", "Other"]
				self.cond[0] += 2
				if "power and the following ability" in t:
					c.extend(["extra", "do", [-16, self.name(a, s='a'), x, "give"]])
			elif "that character gets + soul" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "soul", "Other"]
				self.cond[0] += 2
			if "» or «" in aa:
				if "power" in c:
					c.insert(c.index("power") + 1, f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}")
					c.insert(c.index("power") + 1, "Trait")
				elif "soul" in c:
					c.insert(c.index("soul") + 1, f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}")
					c.insert(c.index("soul") + 1, "Trait")
				self.cond[2] += 2
		elif "choose  of your other  character" in t or "choose  other  character" in t:
			if "stand it" in t or "stand and swap them" in t:
				c = [self.digit(a, self.cond[0]), "stand", "Trait", self.trait(a, self.cond[2]), "Other"]
				self.cond[0] += 1
				self.cond[2] += 1
				if "stand and swap them" in t:
					c.append("swap")
			elif ("rest them" in t or "rest it" in t) and ("move them to an open slot in the back stage" in t or "move it to an open position of your back stage" in t):
				c = [self.digit(a), "rest", "Other", "Trait", self.trait(a, self.cond[2]), "extra", "do", [-16, "move", "Open", "Back"]]
			elif "return it to your hand" in t:
				c = [self.digit(a), "hander", "Other"]
				if "» character" in aa:
					c += ["Trait", self.trait(a)]
				elif "\" character" in aa:
					c += ["Name", self.name(a, s='n')]
			elif "that character gets +x power" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power", "Trait", self.trait(a, self.cond[2]), "Other"]
				self.cond[2] += 1
				self.cond[0] += 2
				if "x = the number of other  characters you have" in t or "x =  times # of your other  characters" in t or "x = the number of your other  characters" in t or "x =  multiplied by the number of other  character" in t:
					c.extend(["#", "#trait", self.trait(a, self.cond[2]), "#other"])
			elif "that character gets + power" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power", "Trait", self.trait(a, self.cond[2]), "Other"]
				if "power and the following ability" in t:
					c.extend(["extra", "do", [-16, self.name(a, s='a'), x, "give"]])
			elif "that character gets + soul" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "soul", "Trait", self.trait(a, self.cond[2]), "Other"]
		elif "choose  of your other characters and this" in t or "choose  of your characters and this" in t or "choose this and  of your other character" in t:
			if "return them to your hand" in t:
				c = [self.digit(a, self.cond[0]), "hander"]
			elif "put them in your memory" in t:
				c = [self.digit(a, self.cond[0]), "memorier"]
			elif "they get the following ability" in t or "those cards get the following ability" in t:
				c = [self.digit(a, self.cond[0]), self.name(a, s='a'), x, "give"]
			c.extend(["Other", "this"])
			if "at the beginning of your next" in t:
				c.extend(["extra", "do", [-21, self.name(a, s='at'), 3, "give", "expass", self.digit(a, self.cond[0]) + 1, "ex_ID="]])
		elif "choose  of your other character" in t:
			c = [self.digit(a, self.cond[0])]
			if "put it in the waiting room" in t:
				c.extend(["waitinger", "Other"])
				if "that shares at least  trait as the character put in the waiting room this way" in t:
					c.extend(["if", 1, "extra"])
			elif "put it in your stock" in t:
				c.extend(["stocker", "Other"])
			elif "return it to your hand" in t:
				c.extend(["hander", "Other"])
			elif "that character gets the following ability" in t:
				c.extend([self.name(a, s='a'), x, "give", "Other"])
			elif "that character gets + level" in t:
				c.extend([self.digit(a, self.cond[0] + 1), x, "level", "Other"])
				self.cond[0] += 1
				if "level and + power" in t:
					c.extend(["extra", "do", [-16, self.digit(a, self.cond[0] + 1), x, "power"]])
					self.cond[0] += 1
			elif "that character gets + power" in t and "this gets + power" in t:
				c.extend([self.digit(a, self.cond[0] + 1), x, "power", "Other", "do", [0, self.digit(a, self.cond[0] + 2), x, "power"]])
				self.cond[0] += 2
			elif "that character gets + power" in t:
				c.extend([self.digit(a, self.cond[0] + 1), x, "power"])
				self.cond[0] += 1
				if "power and the following ability" in t:
					c.extend(["Other", "extra", "do", [-16, self.name(a, s='a'), x, "give"]])
			elif "that character gets + soul" in t:
				c.extend([self.digit(a, self.cond[0] + 1), x, "soul"])
				self.cond[0] += 1
			elif "that character gets +x power" in t:
				c.extend([self.digit(a, self.cond[0] + 1), x, "X", "power", "x", self.digit(a, self.cond[0] + 1)])
				self.cond[0] += 1
				if "x =  times level of that character" in t or "x = that character's level" in t:
					c.append("xlevel")
				elif "x = that character's soul" in t or "x =  times soul of that character" in t:
					c.append("xsoul")
			elif "that character gets «" in aa:
				c.extend([self.trait(a, self.cond[2]), x, "trait", "Other"])
				self.cond[2] += 1
			elif "rest it" in t and ("move it to an empty slot in the back stage" in t or "move it to an open position of your back stage" in t):
				c.extend(["rest", "Other", "extra", "do", [-16, "move", "Open", "Back"]])
			elif "choose  of your other characters." in t:
				c.extend(["waitinger", "aselected", "xchoose", "show"])

			self.cond[0] += 1

			if "Other" not in c:
				c.append("Other")

			if ("characters with either  or " in t or "characters with either  and/or " in t or "characters with  or " in t) and ("» or «" in aa or "» and/or «" in aa):
				c.insert(c.index("Other"), "Trait")
				c.insert(c.index("Other"), f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}")
			if "search your deck for up to" in t and "that shares at least  trait" in t:
				gg, t = self.seperate("search your deck for up to", a, t, aa)
				if gg:
					if "do" in c:
						c[c.index("do") + 1].extend(gg)
					else:
						c.extend(gg)
		elif "choose  of your other reverse " in t and "your other [reverse] \"" in aa:
			if "stand it" in t:
				c = [self.digit(a, self.cond[0]), "stand", "Name=", self.name(a, self.cond[1], s='n'), "Reversed", "Other"]
		elif "choose  of your character" in t:
			tt = ""
			if "deal  damage to your opponent" in t:
				tt = "deal  damage to your opponent"
			elif "choose  of your opponent's character" in t:
				tt = "choose  of your opponent's character"
				if d:
					d = []
			elif "search your deck for up to" in t:
				tt = "search your deck for up to"
				if d:
					d = []
			if tt:
				ts = "choose  of your character"
				if t.index(tt) < t.index(ts):
					g, t = self.seperate(ts, a, t, aa, True)

			c = [self.digit(a, self.cond[0])]
			self.cond[0] += 1
			if "put it in your clock" in t:
				c.append("clocker")
			elif "put it on top of the deck" in t:
				c.extend(["decker", "top"])
			elif "put it in the waiting room" in t or "put it in your waiting room" in t:
				c.append("waitinger")
			elif "put them in your memory" in t:
				c.append("memorier")
			elif "put it in stock" in t:
				c.append("stocker")
			elif "return it to your hand" in t:
				c.append("hander")
			elif "stand them and swap them" in t:
				c.extend(["stand", "swap"])
			elif "that character gets +x power" in t:
				c.extend([self.digit(a, self.cond[0]), x, "power"])
				self.cond[0] += 1
				if "x =  times level of that character" in t or "x =  times the level of that character" in t:
					c.extend(["X", "xlevel", "x", self.digit(a, self.cond[0])])
					self.cond[0] += 1
				elif "x =  times # of your  characters" in t:
					c.extend(["#", "#trait", self.trait(a, self.cond[2])])
					self.cond[2] += 1
				elif "x =  multiplied by the number of cards in your stock" in t:
					c.extend(["#", "#stock"])
			elif "that character gets +x soul" in t:
				c.extend(["x", x, "soul"])
				if "x = level of the card put in the waiting room by this effect" in t:
					c.extend(["X", "xsamelevel", "xmill"])
			elif "that character gets + power" in t:
				c.extend([self.digit(a, self.cond[0]), x, "power"])
				self.cond[0] += 1
				if "that character gets + power and + soul" in t:
					c.extend(["extra", "do", [-16, self.digit(a, self.cond[0]), x, "soul"]])
					self.cond[0] += 1
				elif "that character gets + power and " in t and "power and «" in aa:
					c.extend(["extra", "do", [-16, self.trait(a, self.cond[2]), x, "trait"]])
					self.cond[2] += 1
				elif "that character gets + power and the following ability" in t:
					c.extend(["extra", "do", [-16, self.name(a, s='a'), x, "give"]])
				elif "at the end of the turn, put that card in your stock" in t:
					c.extend(["extra", "do", [-16, "[AUTO] At the end of the turn, put this card into your stock.", -3, "give"]])
					t = t[:t.index("at the end of the turn")]
			elif "that character gets + level" in t:
				c.extend([self.digit(a, self.cond[0]), x, "level"])
				self.cond[0] += 1
				if "level and + power" in t:
					c.extend(["extra", "do", [-16, self.digit(a, self.cond[0]), x, "power"]])
					self.cond[0] += 1
			elif "that character gets + soul" in t:
				c.extend([self.digit(a, self.cond[0]), x, "soul"])
				self.cond[0] += 1
				if "that character gets + soul and this gets + power" in t:
					c += ["do", [0, self.digit(a, self.cond[0]), x, "power"]]
					self.cond[0] += 1
			elif "that character gets «" in aa:
				c.extend([self.trait(a, self.cond[2]), x, "trait"])
				self.cond[2] += 1
				if "» and \"[" in aa:
					c.extend(["extra", "do", [-16, self.name(a, s='a'), x, "give"]])
			elif "that character gets the following  abilities" in t:
				c.extend([f"{self.name(a, s='a')}_{self.name(a, 1, s='a')}", x, "give"])
			elif "that character gets the following ability" in t or ("that character gets " in t and "that character gets \"[" in aa):
				c.extend([self.name(a, s='a'), x, "give"])

			if "characters being front attacked" in t:
				cd = ["Battle"]
			elif "characters with assist" in t:
				cd = ["Text", f"{self.text_name['Assist']}"]
			elif "characters with  or  in its card name" in t and "» or \"" in aa:
				cd = ["TraitN", f"{self.trait(a, self.cond[2])}_{self.name(a, self.cond[1], s='n')}"]
			elif ("characters with either  or " in t or "characters with  or " in t) and "» or «" in aa:
				cd = ["Trait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"]
			elif "with  in name and this" in t:
				cd = ["Name", self.name(a, self.cond[1], s='n'), "this", "Other"]
			elif "characters with  in name" in t or "characters with  in its card name" in t or "characters with  in the name" in t:
				cd = ["Name", self.name(a, self.cond[1], s="n")]
				self.cond[1] += 2
			elif "characters with \"" in a.lower():
				if "with  or  in the name" in t and "\" or \"" in a.lower():
					cd = ["Name", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}"]
				elif self.name(a, s='n') in self.text_name:
					cd = ["Text", f"{self.text_name[self.name(a, s='n')]}"]
			elif "characters named \"" in aa:
				cd = ["Name=", self.name(a, self.cond[1], s="n")]
				self.cond[1] += 2
			elif "characters and this" in t:
				cd = ["Other", "this"]
			elif "whose level = or lower than your level" in t:
				cd = ["Level", "<=p"]

			if cd:
				if "do" in c:
					c.insert(c.index("do"), cd[0])
					c.insert(c.index("do"), cd[1])
				else:
					c.extend(cd)

			if "if you do," in t or "if so," in t:
				c.extend(["if", c[0]])
			elif "if you can't" in t:
				c.extend(["if", 0, "iflower"])

			if "search your deck for up to" in t:
				if "level is the same as the character send to waiting room this way" in t:
					if "do" in c:
						c.insert(c.index("do"), "extra")
					elif "if" in c:
						c.insert(c.index("if"), "extra")
					else:
						c.append("extra")
				gg, t = self.seperate("search your deck for up to", a, t, aa)
			elif "choose  of your opponent's level  or lower character" in t:
				gg, t = self.seperate("choose  of your opponent's level  or lower character", a, t, aa)
			elif "choose  level  or lower character in your opponent" in t:
				gg, t = self.seperate("choose  level  or lower character in your opponent", a, t, aa)
			if gg:
				if "do" in c:
					c[c.index("do") + 1].extend(gg)
				else:
					c.extend(gg)
		elif "choose  cost  or higher character in your opponent's waiting room" in t:
			if "put it on an open position of your opponent's back stage" in t or "put it in an empty slot in your opponent's back stage" in t or "put it on an open position of their back stage" in t:
				c = [self.digit(a, self.cond[0]), "salvage", f"CCost_>={self.digit(a, self.cond[0] + 1)}", "Stage", "opp", "Back", "Open", "Opp"]
				self.cond[0] += 2
		elif "choose  of your opponent's cards in in the waiting room" in t:
			if "return them in your opponent's deck" in t:
				c = [self.digit(a), "shuffle", "opp"]
				self.cond[0] += 1
		elif "choose  of your opponent's characters with level higher than your opponent's level" in t or "choose  of your opponent's characters whose level is higher than the level of your opponent" in t or "choose  of your opponent's characters that is higher level than your opponent" in t or "choose  of your opponent's characters whose level is higher than the level of the opponent" in t:
			c = [self.digit(a, self.cond[0]), "", "Opp", "Antilvl"]
			if "put it in the waiting room" in t or "put it into their waiting room" in t or "put it in your opponent's waiting room" in t:
				c[1] = "waitinger"
			elif "put it into their memory" in t or "put it in your opponent's memory" in t or "send it to their memory" in t:
				c[1] = "memorier"
			elif "put it on the bottom of the deck" in t or "put it at the bottom of their deck" in t:
				c[1] = "decker"
				c.insert(2, "bottom")
		elif "choose  cost  or lower character in your opponent" in t or "choose  of your opponent's cost  or lower character" in t or "choose  opponent's character whose cost is  or lower" in t or "choose  of your opponent's cost  or less character" in t:
			c = [self.digit(a, self.cond[0]), "", "Opp", "Cost", f"<={self.digit(a, self.cond[0] + 1)}"]
			if "put it in the waiting room" in t or "put it into their waiting room" in t or "put it in your opponent's waiting room" in t:
				c[1] = "waitinger"
			elif "put it on the top of his or her deck" in t or "put it on top of the deck" in t:
				c[1] = "decker"
				c.insert(2, "top")
			elif "put it on the bottom of the deck" in t or "put it on bottom of the deck" in t:
				c[1] = "decker"
				c.insert(2, "bottom")
			elif "put it in stock" in t or "put it in the stock" in t:
				c[1] = "stocker"
			elif "return it to hand" in t or "return it to his or her hand" in t:
				c[1] = "hander"
			self.cond[0] += 2
			if "opponent's center stage" in t or "opponent's cost  or less characters in the center stage" in t:
				c.append("Center")
		elif "choose  of your opponent's level  or higher character" in t:
			if "your opponent chooses  level x or lower character in their waiting room" in t and ("exchanges them" in t or "swap the chosen character" in t):
				if "x = the level of the character you chose -" in t or "x = the level of your chosen character minus" in t or "x = level of the character you chose this way -" in t:
					c = [self.digit(a, self.cond[0]), "waitinger", "Level", f">={self.digit(a, self.cond[0] + 1)}", "Opp", "swap", "extra", "if", "do", [self.digit(a, self.cond[0] + 2), "salvage", f"CLevel_<=x", "xslevel-", abs(self.digit(a, self.cond[0] + 3)), "opp", "oppturn", "Opp", "swap", "Stage"]]
			elif "that character gets \"" in aa:
				c = [self.digit(a, self.cond[0]), self.name(a, s='a'), x, "Level", f">={self.digit(a, self.cond[0] + 1)}", "Opp", "give"]
				self.cond[0] += 2
		elif "choose  of your opponent's level  or lower character" in t or "choose  level  or lower character on your opponent's" in t or ("choose  of your opponent's" in t and ("character whose level is  or lower" in t or "characters whose level is  or lower" in t)) or "choose  level  or lower character in your opponent" in t or "choose  opponent's level  or lower character" in t:
			if "search your deck for" in t:
				tt = "search your deck for"
				if "choose  of your opponent's level" in t:
					tc = "choose  of your opponent's level"
				elif "choose  level  or lower " in t:
					tc = "choose  level  or lower "
				elif "choose  opponent's level" in t:
					tc = "choose  opponent's level"
				if t.index(tt) < t.index(tc):
					gg, t = self.seperate("choose  level  or lower character in your opponent", a, t, aa, True)
					g = gg
			c = [self.digit(a, self.cond[0])]
			_ = ["Opp", "Level", f"<={self.digit(a, self.cond[0] + 1)}"]
			self.cond[0] += 2

			if "opponent's center stage" in t or "in the center stage" in t or "on the center stage" in t:
				_.append("Center")
			elif "in the back stage" in t or "opponent's back stage" in t:
				_.append("Back")
			if "you may choose  level" in t or "you may choose  of your opponent's level" in t:
				_.append("upto")

			if "that character doesn't stand" in t or "that character cannot stand" in t:
				if "during your opponent's next stand phase" in t:
					x = 3
				c.extend(["[CONT] This cannot [STAND] during your stand phase", x, "give"])
			elif "return it to hand" in t or "return it to your opponent's hand" in t or "return it to the hand" in t:
				c.append("hander")
				if "at the end of turn" in t and "put this in your memory" in t:
					c.extend(_)
					_ = []
					c.extend(["do", [0, "[AUTO] At the end of the turn, put this card into your memory.", -3, "AUTO", "give"]])
					t = t[:t.index("at the end of turn")]
			elif "put it in stock" in t or "put it in your opponent's stock" in t:
				c.append("stocker")
			elif "put it in his or her waiting room" in t or "put it in the waiting room" in t or "put it into their waiting room" in t or "put it in your opponent's waiting room" in t:
				c.append("waitinger")
				if "your opponent chooses up to  cost  or lower character in their waiting room" in t:
					if "puts it on the stage position that their character was on" in t:
						c.extend(_)
						_ = []
						c.extend(["swap", "extra", "if", "do", [self.digit(a, self.cond[0]), "salvage", f"CCost_<={self.digit(a, self.cond[0] + 1)}", "opp", "oppturn", "swap", "Stage"]])
						self.cond[0] += 2
			elif "put it on the bottom of his or her deck" in t or "put it on the bottom of the deck" in t:
				c.extend(["decker", "bottom"])
			elif "put it on the top of your opponent's deck" in t or "put it on top of the deck" in t:
				c.extend(["decker", "top"])
			elif "put it in your opponent's memory" in t or "put it into their memory" in t or "send it to memory" in t:
				c.append("memorier")
			elif "put it in your opponent's clock" in t:
				c.append("clocker")
			c.extend(_)

			if "search your deck for" in t:
				if "character with the same name as" in t:
					c.extend(["extra"])
				gg, t = self.seperate("search your deck for", a, t, aa)

			if gg:
				if "do" in c:
					c[c.index("do") + 1].extend(gg)
				else:
					c.extend(gg)
		elif "choose  card in your opponent's waiting room" in t or "choose  card from your opponent's waiting room" in t:
			c = [self.digit(a, self.cond[0]), "salvage", "", "opp", "show"]
			if "put it in stock" in t:
				c.append("Stock")
			elif any(_ in t for _ in ("put it on top of the deck", "put that character on top of your opponent's deck", "put it on top of your opponent's deck", "put it on the top of your opponent's deck", "put it on the top of his or her deck")):
				c.extend(["Library", "top"])
			elif "return it to your opponent's deck" in t:
				c.append("Library")
			elif "send it to memory" in t or "put it in your opponent's memory" in t or "put it into their memory" in t:
				c.append("Memory")
			self.cond[0] += 1
			if "you may choose  card in your opponent's waiting room" in t:
				c.append("upto")
		elif "choose  card in your opponent's clock" in t:
			c = [self.digit(a, self.cond[0]), "csalvage", "", "opp", "show"]
			if "put it in his or her waiting room" in t:
				c.append("Waiting")
			self.cond[0] += 1
			if "you may choose  card in your opponent's clock" in t:
				c.append("upto")
				if "if you do," in t:
					c.extend(["if", 1])
			if "your opponent puts the top card of your opponent's deck in his or her clock" in t:
				c.extend(["do", ["damageref", 1, "opp"]])
		elif "choose  opponent's character" in t or "choose  of your opponent's character" in t or "choose  of your opponent" in t or "choose  character in your opponent" in t or "choose  of opponent" in t or "choose  character on your opponent" in t or "choose up to  of opponent" in t:
			if t.count("choose  of your opponent's character") == 2:
				tt = "choose  of your opponent's character"
				ts = "if your opponent does not have any stand character"
				if ts in t and t.count(ts) == 1:
					t1 = f"{ts}{t.split(ts)[1]}"
					t = t.split(ts)[0]
				else:
					t1 = f"{tt}{t.split(tt)[2]}"
					t = f"{t.split(tt)[0]}{tt}{t.split(tt)[1]}"

				h = self.convert(a, t1, aa)
				if ts in t1 and ts not in t:
					self.cond_later = True
					_ = self.condition(a, t1, aa)
					_.extend(["do", h])
					h = _

				tt = ""

			if "move it to another vacant slot" in t or "move it to another empty slot" in t or "move it to another open position of their stage" in t or "move it to another open position of your opponent's stage" in t or "move it to another open position of their" in t:
				c = [self.digit(a, self.cond[0]), "move", "Character", "Opp", "Open", "may"]
				if "slot in the center stage" in t or "open position of their center stage" in t:
					c.append("Center")
			elif "return it to the hand" in t or "return it to your opponent's hand" in t or "return it to their hand" in t or "return it to hand" in t or "return it to your opponent's hand" in t or "return it to his or her hand" in t:
				c = [self.digit(a, self.cond[0]), "hander", "Opp"]
			elif "put it in the waiting room" in t:
				c = [self.digit(a, self.cond[0]), "waitinger", "Opp"]
			elif "put it into their memory" in t or "send it to memory" in t or "put that character in your opponent's memory" in t:
				c = [self.digit(a, self.cond[0]), "memorier", "Opp"]
				if "your opponent puts that character from their memory on any position of their stage" in t or "your opponent puts that character from their memory in any position of their stage" in t:
					if "at the beginning of the encore step" in t:
						c.extend(["extra", "if", self.digit(a, self.cond[0]), "do", [-21, self.name(a, s='ac'), 2, "give", "expass", self.digit(a, self.cond[0]), "ex_ID="]])
						t = t.split("at the start of encore step")[0]
					else:
						c.extend(["extra", "if", c[0], "do", [-16, "msalvage", "ID=_x", "Stage", "Opp", "oppturn", "opp"]])
			elif "that character cannot stand during your opponent's next stand phase" in t or "that character doesn't stand during your opponent's next stand phase" in t:
				c = [self.digit(a, self.cond[0]), "[CONT] This cannot [STAND] during your stand phase", 2, "give", "Opp"]
			elif "that character gets the following ability" in t:
				c = [self.digit(a, self.cond[0]), self.name(a, s='a'), x, "give", "Opp"]
			elif "then stand and swap them" in t:
				c = [self.digit(a, self.cond[0]), "stand", "Opp", "swap"]
			elif "that character gets - power" in t or "that character gets + power" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power", "Opp"]
				self.cond[0] += 1
				if "power and gets " in t and "gets «" in aa:
					c.extend(["extra", "do", [-16, self.trait(a, self.cond[2]), x, "trait"]])
					self.cond[2] += 1
			elif "that character gets -x power" in t:
				if "x =  times # of your  characters" in t or "x =  multiplied by the number of  characters you have" in t:
					c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "#", "power", "Opp", "#trait", self.trait(a), "x", self.digit(a, self.cond[0] + 1), "negative"]
					self.cond[0] += 1
			elif "that character gets - level" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "level", "Opp"]
				self.cond[0] += 1
			elif "that character gets - soul" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "soul", "Opp"]
				self.cond[0] += 1
			elif "rest it" in t:
				c = [self.digit(a, self.cond[0]), "rest", "Opp"]
				if "standing character" in t:
					c.append("Stand")
			self.cond[0] += 1

			if "characters in battle" in t:
				c.insert(c.index("Opp"), "Battle")
			elif "character in center stage" in t or "opponent's center stage characters" in t or "opponent's center stage" in t or "on the center stage" in t:
				c.insert(c.index("Opp"), "Center")
			elif "character in your opponent's back stage" in t:
				c.insert(c.index("Opp"), "Back")
			elif "opponent's stand character" in t or "opponent's stand card" in t:
				c.insert(c.index("Opp"), "Stand")
			if "with level higher than your opponent's level" in t or "whose level is higher than your opponent" in t:
				c.insert(c.index("Opp"), "Antilvl")
			if "choose up to  of opponent" in t or "you may choose  of your opponent" in t:
				c.insert(c.index("Opp"), "upto")
			if "at the end of turn" in t and ("put this in your memory" in t or "send this to memory" in t):
				gg = ["do", [0, "[AUTO] At the end of the turn, put this card into your memory.", -3, "give"]]
				if "do" in c:
					c[c.index("do") + 1].extend(gg)
				else:
					c.extend(gg)
				t = t[:t.index("at the end of turn")]
			elif "deal x damage" in t:
				if "x = the soul of that character" in t:
					c.append("extra")
				gg, t = self.seperate("deal x damage", a, t, aa)
			elif "deal  damage to" in t:
				gg, t = self.seperate("deal  damage to", a, t, aa)

			if gg:
				if "do" in c:
					c[c.index("do") + 1].extend(gg)
				else:
					c.extend(gg)
		elif "choose  random opponent" in t:
			if "that character gets - power" in t:
				c = [-11, self.digit(a, self.cond[0]), x, "power", "opp", "random"]
		elif "choose  random card in your opponent's hand" in t:
			if "put it into their memory" in t:
				c = ["discard", self.digit(a, self.cond[0]), "", "random", "opp", "Memory"]
			if "reveal it" in t:
				c.append("show")
			if "at the end of your opponent's next turn" in t:
				c.extend(["extra", "do", [-21, self.name(a, s='an'), 3, "give", "expass", self.digit(a, self.cond[0]), "ex_ID="]])
		elif "choose  character" in t:
			if "that character gets + power" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power"]
		elif "choose  trait" in t:
			if "this gets the chosen trait" in t:
				if "until the next time you choose  trait with this ability" in t:
					x = -66
				c = [0, "x", x, "trait", "xchoose", "xremovechoose"]

			if "you may choose  trait" in t:
				c.append("upto")
		elif "search deck for up to x characters" in t:
			if "reveal them" in t and "put them in your hand" in t:
				c = ["x", "search", "Character", "upto", "show"]
			if "characters with  in name" in t:
				c[2] = f"Name_{self.name(a, self.cond[1], s='n')}"
			if "discard x cards from your hand to the waiting room" in t:
				c += ["do", ["discard", "x", ""]]
		elif "search your deck for up to  level  or higher character with  or " in t:
			c = [self.digit(a, self.cond[0]), "search", f"TraitL_{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}_>={self.digit(a, self.cond[0] + 1)}", "upto"]
			self.cond[0] += 2
			self.cond[2] += 2
			if "reveal it" in t:
				c.append("show")
		elif "search your deck for up to  climax" in t:
			c = [self.digit(a, self.cond[0]), "search", "Climax", "upto"]
			self.cond[0] += 1
			if "put it in the waiting room" in t:
				c.append("Waiting")
			if "reveal it" in t:
				c.append("show")
			if "climax with the same card name as a climax in your waiting room" in t:
				c[2] = "CXName=_x"
				c.append("xcxsamewr")
			if "you put  card in the waiting room this way" in t:
				c.extend(["if", self.digit(a, self.cond[0])])
				self.cond[0] += 1
		elif "search your deck for up to  event" in t:
			c = [self.digit(a, self.cond[0]), "search", "Event", "upto"]
			self.cond[0] += 1
			if "reveal it" in t:
				c.append("show")
		elif "search your deck for up to  level  or lower  character" in t:
			c = [self.digit(a), "search", f"TraitL_{self.trait(a)}_<={self.digit(a, 1)}", "upto"]
			if "put it on any position of your stage" in t:
				c.append("Stage")
			elif "put that card on an open position of your stage" in t:
				c.extend(["Stage", "Open"])
			elif "put it on any position of your back stage" in t:
				c.extend(["Stage", "Back"])

			if "reveal it" in t:
				c.append("show")

			if "position of your stage as rest" in t:
				c.extend(["extra", "do", [-16, "rested"]])
		elif "search your deck for up to  level  or lower character" in t:
			if "put it in your hand" in t:
				c = [self.digit(a, self.cond[0]), "search", f"CLevel_<={self.digit(a, self.cond[0] + 1)}", "upto"]
				self.cond[0] += 2
				if "reveal it" in t:
					c.append("show")
				c = self.discard_card(c, a, t)
		elif "search your deck for up to  cost  or lower  character" in t:
			c = [self.digit(a, self.cond[0]), "search", f"TraitC_{self.trait(a, self.cond[2])}_<={self.digit(a, self.cond[0] + 1)}", "upto"]
			self.cond[0] += 2
			self.cond[2] += 1
			if "put it on any position of your stage" in t:
				c.append("Stage")

			if "with level equal to or lower than your level" in t or "with level equal or lower than your level" in t:
				c[2] = f'TraitLC_{c[2].split("_")[1]}_<=p_{c[2].split("_")[2]}'
		elif "search your deck for up to   or " in t or "search your deck for  character with  or " in t:
			c = [self.digit(a, self.cond[0]), "search", "", "upto"]
			if "reveal it" in t or "show it" in t:
				c.append("show")
			c = self.discard_card(c, a, t)
			if "\" or \"" in aa and "\" in the name" in aa:
				c[2] = f"Name_{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}"
				self.cond[1] += 4
			elif "\" or character with \"resonate\"" in aa:
				c[2] = f"TextN_{self.text_name['Resonate']}_{self.name(a, self.cond[1], s='n')}"
				self.cond[1] += 2
			elif "\" or «" in aa:
				self.cond[2] -= 2
				c[2] = f"Name=T_{self.name(a, self.cond[1], s='n')}_{self.trait(a, self.cond[2])}"
				self.cond[1] += 2
				self.cond[2] += 1
			elif "» or «" in aa:
				c[2] = f"Trait_{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"
				self.cond[2] += 2
			self.cond[0] += 1
		elif "search your deck for up to   character" in t and "» character" in aa:
			c = [self.digit(a, self.cond[0]), "search", f"Trait_{self.trait(a, self.cond[2])}", "upto"]
			self.cond[0] += 1

			if "put it in your hand" in t or "put them in your hand" in t:
				c = self.discard_card(c, a, t)
			elif "put it in the waiting room" in t or "put it in your waiting room" in t:
				c.extend(["Waiting"])
			elif "put it in your stock" in t:
				c.extend(["Stock"])
			elif "put it in any slot on the stage" in t or "put it on any position of your stage" in t:
				c.extend(["Stage"])
			elif "put it in the slot this was in" in t:
				c.extend(["Stage", "Change"])

			if "reveal it" in t or "reveal them" in t or "show it" in t or "show them" in t:
				c.append("show")

			if "character with a total level and cost of x or lower" in t:
				if "x = the total level and cost of the characters put in your waiting room" in t:
					c[2] = f"TraitZ_{self.trait(a, self.cond[2])}_<=x"
					c.append("xextraZ")
			elif "character and up to  character with  in its card name" in t:
				c[0] += self.digit(a, self.cond[0])
				self.cond[0] += 1
				_ = c[2].split("_")
				c[2] = f"B{_[0]}N_{_[1]}_{self.name(a, self.cond[1], s='n')}"
				self.cond[1] += 2
			elif "whose level = or lower than your level and whose cost is  or lower" in t:
				c[2] = f"TraitLC_{self.trait(a, self.cond[2])}_<=p_<={self.digit(a, self.cond[0])}"
				self.cond[0] += 1
			elif "whose level is lower than or equal to your level" in t:
				c[2] = f"TraitL_{self.trait(a, self.cond[2])}_<=p"
			elif "  character or character with  in its card name" in t and "» character or character with \"" in aa:
				_ = c[2].split("_")
				c[2] = f"{_[0]}N_{_[1]}_{self.name(a, self.cond[1], s='n')}"
				self.cond[1] += 2
			self.cond[2] += 1
			if "that character gets + power" in t:
				c.extend(["extra", "do", [-16, self.digit(a, self.cond[0]), x, "power"]])
				self.cond[0] += 1
		elif "search your deck for up to  character with " in t or "search your deck for  character with " in t or "search your deck for up to  characters with" in t:
			c = [self.digit(a, self.cond[0]), "search", ""]
			self.cond[0] += 1
			if "search your deck for up to" in t:
				c.append("upto")

			if "put it in any slot on the stage" in t:
				c.append("Stage")
			if "reveal it" in t or "reveal them" in t or "show it" in t:
				c.append("show")

			if "character with  in name and up to  character with  in name" in t:
				c[2] = f"EachCName_{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}"
				c[0] += self.digit(a, self.cond[0])
				self.cond[0] += 1
				self.cond[1] += 4
			elif "character with the same name as that character" in t:
				c[2] = "EName="
			elif "character with no traits" in t:
				c[2] = "Trait_"
			elif "with resonance or " in t and "with resonance or \"" in aa:
				c[2] = f"TextN_{self.text_name['Resonance']}_{self.name(a, self.cond[1], s='n')}"
			elif "with resonance" in t:
				c[2] = f"Text_{self.text_name['Resonance']}"
			elif "with assist" in t:
				c[2] = f"Text_{self.text_name['Assist']}"
			elif "character with  in the name" in t or "character with  in name" in t or "character with  in its card name" in t:
				c[2] = f"CName_{self.name(a, self.cond[1], s='n')}"
				if any(setonly in a for setonly in self.set_only):
					for sto in self.set_only:
						if sto in a:
							c[2] = f"NameSet_{self.name(a, s='n')}_{self.set_only[sto]}"
			elif "character with  or  or " in t and aa.count("\" or \"") == 2:
				c[2] = f"CName_{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}_{self.name(a, self.cond[1] + 4, s='n')}"
			elif "character with  or  in its card name" in t and "» or \"" in aa:
				c[2] = f"TraitN=_{self.trait(a, self.cond[2])}_{self.name(a, self.cond[1], s='n')}"
				self.cond[1] += 2
				self.cond[2] += 1
			elif "character with  or " in t and "\" or \"" in aa:
				c[2] = f"CName_{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}"
			elif ("character with either  or " in t or "character with either  and/or" in t or "character with  or " in t or "characters with  or" in t) and ("» and/or «" in aa or "» or «" in aa):
				c[2] = f"Trait_{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"
			elif self.name(a, s='n') in self.text_name:
				c[2] = f"Text_{self.text_name[self.name(a, s='n')]}"
			c = self.discard_card(c, a, t)
		elif "search your deck for up to  " in t or "search your deck for up to  card named " in t:
			c = [self.digit(a, self.cond[0]), "search", f"Name=_{self.name(a, self.cond[1], s='n')}", "upto"]
			self.cond[0] += 1
			if ("reveal it" in t or "show it to your opponent" in t) and "put it in your hand" in t:
				c.append("show")
				if self.name(a, self.cond[1], s='n') in self.text_name:
					c[2] = f"Text_{self.name(a, self.cond[1], s='n')}"
			if "put it in any slot in the back stage" in t:
				c.extend(["Stage", "Back"])
			elif "put them on separate positions of your center stage" in t:
				c.extend(["Stage", "Center", "separate"])
			elif "put them in separate slots" in t:
				c.extend(["Stage", "separate"])
			elif "place it to any slot on the stage" in t or "put it on any position of your stage" in t or "place it to any slot on your stage" in t or "put it in any slot on the stage" in t or "put it in any position of your stage" in t:
				c.append("Stage")
			elif "put it in the slot this was in" in t:
				c.extend(["Stage", "Change"])
			if "that card gets + power and the following ability" in t or "that character gets + power and the following ability" in t:
				c.extend(["extra", "do", [-16, self.digit(a, self.cond[0]), x, "power", "extra", "do", [-16, self.name(a, s='a'), x, "give"]]])
			if "search your deck for up to  card" in t and "search your deck for up to  card named" not in t:
				c[2] = ""
			elif "character whose level is the same as the character send to waiting room this way" in t:
				c[2] = "CLevel_==x"
				if "CLevel_==x" in c:
					c.insert(c.index("CLevel_==x") + 1, "xlevelextra")
			elif "character that shares at least  trait as the character put in the waiting room this way" in t:
				c[2] = "Trait_x"
				c.extend(["xany", "xextratrait"])
			elif "deck for up to  level  or higher character" in t:
				c[2] = f"CLevel_>={self.digit(a, self.cond[0])}"
			elif "character that is either  or " in t and any(f"{cl} or «" in aa for cl in self.colour):
				c[2] = f"CColourT_{self.colour_t(a)}_{self.trait(a, self.cond[2])}"
		elif "search your deck for up to x  character" in t and "» character" in aa:
			c = ["x", "search", "Character", "upto"]
			if "for up to x «" in aa:
				c[2] = f"Trait_{self.trait(a, self.cond[2])}"
				self.cond[2] += 1
			if "x = number of climax cards revealed this way" in t:
				if "brainstorm" in aa:
					pass
			c = self.discard_card(c, a, t)
		elif "search your deck for   character" in t and "» character" in aa:
			c = [self.digit(a, self.cond[0]), "search", f"Trait_{self.trait(a, self.cond[2])}"]
			if "put it in any slot on stage" in t:
				c.append("Stage")
			if "character whose level is  or lower" in t:
				c[2] = f"{c[2].split('_')[0]}L_{c[2].split('_')[1:]}_<={self.digit(a, self.cond[0])}"
				self.cond[0] += 1
		elif "search your stock for up to  " in t:
			c = [self.digit(a, self.cond[0]), "stsearch", "", "upto"]
			self.cond[0] += 1
			if " reveal it" in t:
				c.append("show")
			if "shuffle your stock" in t:
				c.append("stshuff")
			if "stock for up to   or  character or event" in t and "» or «" in aa:
				c[2] = f"TraitE_{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"
				self.cond[2] += 2
			elif "stock for up to  character" in t:
				c[2] = "Character"
		elif "move this to the open left" in t:
			c = [1, "move", "Open", "Left", "this"]
			if "open left position of your center stage" in t:
				c.append("Center")
			if "you may move this" in t:
				c.append("may")
		elif "move this to an empty" in t or "move this to an open position" in t or "put this to an empty slot" in t or "move this to a vacant slot" in t or "move this to the open middle position" in t:
			c = [1, "move", "Open", "this"]
			if "with a character opposite this" in t or "that has an opponent's character opposite that slot" in t or "opposite an opponent's character" in t or "with  character opposite this" in t:
				c.append("OpponentOpposite")
				if "with  character opposite" in t:
					self.cond[0] += 1
			elif "empty center stage center slot" in t or "open middle position of your center stage" in t:
				c.append("Middle")
			elif "in your center stage" in t or "of your center stage" in t or "in the center stage" in t:
				c.append("Center")
			elif "in the back stage" in t or "of your back stage" in t:
				c.append("Back")
			if "you may move this" in t:
				c.append("may")
		elif "deal  damage x times to your opponent instead" in t:
			if "during that attack" in t and "when this deals attack damage to your opponent" in t:
				c = ["escanor", self.digit(a, self.cond[0]), "xtimes", 0]
				self.cond[0] += 1
				if "x = this's soul" in t:
					c.append("xsoul")
		elif "deal x damage to your opponent" in t:
			c = ["damage", "x", "opp"]
			if "x = the declared number" in t or "x = the number you declared" in t:
				c.extend(["xdeclare"])
			elif "x is the number of soul trigger icons on that card + " in t or "x = the total number of soul in the trigger icon of that card +" in t:
				c.extend(["xreveal", "xTrigger+", "Soul", self.digit(a, self.cond[0])])
			elif "x = soul of the character revealed via the cost of this ability" in t:
				if "resonate [" in aa or "resonance [" in aa:
					c.extend(["xResonance", "xSoul"])
				else:
					c.extend(["xreveal", "xSoul"])
			elif "x = the number of standby trigger icons among those card" in t:
				c.extend(["xreveals", "xTrigger", "Standby"])
			elif "x = the number of climax among those cards" in t or "x is the number of climax cards among those cards" in t or "x = # of climax cards among those cards" in t or "x = # of climax cards among them" in t:
				c.extend(["xmill", "xClimax"])
			elif "x = the level of that card +" in t or "x =  + level of that card" in t or "x equals the level of that card + " in t:
				c.extend(["xmill", "xLevel+x", self.digit(a, self.cond[0])])
			elif "x = that card's level" in t:
				c.extend(["xmill", "xLevel"])
			elif "x = the level of the card put in your waiting room by this ability's cost" in t or "x = the level of the card discarded by the cost of this ability" in t or "x = level of that card" in t:
				c.extend(["xdiscard", "xLevel"])
			elif "x = # of  in your waiting room" in t or "x = the number of  in your waiting room" in t:
				c.extend(["Name=", self.name(a, -1, s='n'), "Waiting"])
			elif "x = # of climax cards in your waiting room" in t:
				c.extend(["Climax", "Waiting"])
			elif "x equals the soul of this" in t or "x = this's soul" in t:
				c.extend(["xself", "xSoul"])
			elif "x = the soul of that character" in t:
				c[1] = -16
				c.append("xSoul")
			elif "x = the number of characters put in your waiting room" in t or "x = # of characters put in the waiting room" in t:
				c[1] = -16
			elif "x = the cost of that character" in t or "x = cost of that character" in t:
				if self.xx is not None:
					c[1] = self.xx
		elif "deal  damage to all players" in t:
			c = ["damage", self.digit(a), "both", "do", ["damage", self.digit(a), "opp"]]
		elif "deal  damage to your opponent" in t:
			if t.count("deal  damage to your opponent") >= 2:
				if t.count("deal  damage to your opponent") == 3:
					c = ['damage', self.digit(a, self.cond[0]), 'opp', "do", ['damage', self.digit(a, self.cond[0] + 1), 'opp', "do", ['damage', self.digit(a, self.cond[0] + 2), 'opp']]]
				else:
					if t.count("if th") >= 2:
						self.multicond = ["if th", 1, 2]
						c = ['damage', self.digit(a, self.cond[0]), 'opp']
					else:
						c = ['damage', self.digit(a, self.cond[0]), 'opp', "do", ['damage', self.digit(a, self.cond[0] + 1), 'opp']]
				if "you may deal  damage" in t:
					c.append("upto")
			else:
				c = ['damage', self.digit(a, self.cond[0]), 'opp']
				self.cond[0] += 1
				if "you may deal  damage" in t:
					c.append("upto")
				if "even if the damage is cancelled" in t:
					if "put all level  or higher cards revealed due to this damage in clock" in t:
						c.extend(["oncancelput", "ocLevel", self.digit(a, self.cond[0])])
						self.cond[0] += 1
				if "choose randomly  of your character" in t:
					if "that card gets + power" in t:
						c.extend(["do", [-8, self.digit(a, self.cond[0] + 1), x, "power"]])
		elif "deals  damage to you" in t:
			c = ["damage", self.digit(a, self.cond[0])]
		elif "deal the same amount of damage to your opponent" in t or "deal the same damage to your opponent" in t:
			c = ["damage", self.dmg, "opp"]

		if "all characters in your opponent's center stage get" in t or "all your opponent's center stage characters get" in t:
			if "get - power" in t:
				b = [-1, self.digit(a), x, "power", "Center", "opp"]
		elif "all your opponent's characters with  or more of the same trait as that character" in t:
			_ = ["opp", "Trait", "", "xanytrait", self.digit(a, self.cond[0]), "xmill"]
			self.cond[0] += 1
			if "get - power" in t:
				b = [-1, self.digit(a, self.cond[0]), x, "power"]
				self.cond[0] += 1
			b.extend(_)
		elif "all your opponent's characters get" in t:
			if "get - power" in t:
				b = [-1, self.digit(a, self.cond[0]), x, "power", "opp"]
			self.cond[0] += 1
		elif "all the battling characters get" in t or "all characters in battle" in t:
			if "get the following ability" in t:
				b = [-1, self.name(a, s='a'), x, "give", "Battle"]
		elif "all your other level  or lower character" in t:
			if "get  and the following ability" in t and "get «" in aa:
				b = [-2, self.trait(a, self.cond[2]), x, "trait", "extra", "do", [-16, self.name(a, s='a'), x, "give"]]
			elif "get the following ability" in t:
				b = [-2, self.name(a, s='a'), x, "give"]
			b.extend(["CLevel", self.digit(a, self.cond[0]), "Llower"])
			self.cond[0] += 1

			if "do" in b:
				cd = b[b.index("do") + 1]
				b.remove("do")
				b.remove(cd)
				b.extend(["do", cd])
		elif "all your characters with  or " in t and "» or «" in aa:
			if "get + soul" in t:
				b = [-1, self.digit(a, self.cond[0]), x, "soul", "Trait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"]
			elif "get + power" in t:
				b = [-1, self.digit(a, self.cond[0]), x, "power", "Trait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"]
			self.cond[0] += 1
			self.cond[2] += 2
		elif "all your characters with the same" in t:
			b = [-1, self.digit(a, self.cond[0]), x]
			if "get + power" in t:
				b.append("power")
			if "with the same level as that card" in t:
				b.extend(["xsamelevel", "xmill", "CLevel", 0, "=="])
		elif "all your characters with \"" in aa:
			if "get + power" in t:
				b = [-1, self.digit(a, self.cond[0]), x, "power"]
			if " or  or " in t and aa.count("\" or \"") == 2:
				b.extend(["Name", f"{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}_{self.name(a, self.cond[1] + 4, s='n')}"])
				self.cond[1] += 4
			else:
				b.extend(["Name", self.name(a, self.cond[1], s='n')])
			self.cond[1] += 2
		elif "all your  characters get" in t:
			if "get + power" in t:
				b = [-1, self.digit(a, self.cond[0]), x, "power", "Trait", self.trait(a, self.cond[2])]
				if " + power and + soul" in t:
					b.extend(["extra", "do", [-16, self.digit(a, self.cond[0] + 1), x, "soul"]])
			elif "get + soul" in t:
				b = [-1, self.digit(a, self.cond[0]), x, "soul", "Trait", self.trait(a, self.cond[2])]
			elif "get the following ability" in t or "get \"[" in aa:
				b = [-1, self.name(a, s='a'), x, "give", "Trait", self.trait(a, self.cond[2])]
			elif "characters gets " in t and "characters gets «" in aa:
				b = [-1, self.trait(a, self.cond[2] + 1), x, "Trait", self.trait(a, self.cond[2]), "trait"]
		elif "all your characters get" in t or "all your character get" in t:
			if "get + soul" in t or "gets + soul" in t:
				b = [-1, self.digit(a, self.cond[0]), x, "soul"]
			elif "get + power" in t:
				b = [-1, self.digit(a, self.cond[0]), x, "power"]
				if "+ power and + soul" in t:
					b.extend(["extra", "do", [-16, self.digit(a, self.cond[0] + 1), x, "soul"]])
			elif "get + level" in t:
				b = [-1, self.digit(a, self.cond[0]), x, "level"]
			elif ("get " in t and "characters get \"[" in self.a_replace(a)) or "get the following ability" in t:
				b = [-1, self.name(a, s='a'), x, "give"]
			if "your opponent may not use \"[auto] encore\"" in aa:
				b.extend(["do", [-21, "[CONT] Your opponent cannot use \"[AUTO] Encore\" until end of turn.", x, "give"]])
		elif "all your other characters get" in t:
			if "get + power" in t:
				b = [-2, self.digit(a, self.cond[0]), x, "power"]
				self.cond[0] += 1
			elif "get + level" in t:
				b = [-2, self.digit(a, self.cond[0]), x, "level"]
				self.cond[0] += 1
			elif "get the following ability" in t:
				b = [-2, self.name(a, s='a'), x, "ability"]
		elif "this randomly gets between +~+ power" in t:
			b = [0, self.digit(a, self.cond[0]), x, "random", self.digit(a, self.cond[0] + 1), "power"]
			self.cond[0] += 2
		elif "this gets + level" in t:
			b = [0, self.digit(a, self.cond[0]), x, "level"]
			self.cond[0] += 1
			if "level and + power" in t:
				b.extend(["extra", "do", [-16, self.digit(a, self.cond[0]), x, "power"]])
		elif "this gets the following  abilities" in t:
			b = [0, "", x, "give"]
			if "following 2 abilities" in aa:
				b[1] = f"{self.name(a, s='a')}_{self.name(a, 1, s='a')}"
		elif "this gets the following abilities" in t:
			b = [0, "", x, "give"]
			if a.lower().split("gets the following abilities")[1].count("\"") / 2 == 2:
				b[1] = f"{self.name(a, s='a')}_{self.name(a, 1, s='a')}"
		elif "this gets the following ability" in t or ("this gets " in t and "this gets \"[" in aa):
			b = [0, self.name(a, s='a'), x, "give"]
		elif "this gets + power" in t or "this get + power" in t or "this gets - power" in t:
			b = [0, self.digit(a, self.cond[0]), x, "power"]
			self.cond[0] += 1
			if "for each different trait on your characters" in t:
				b += ["#", "Traits"]

			if "power, + soul, and the following ability" in t:
				b.extend(["extra", "do", [-16, self.digit(a, self.cond[0]), x, "soul", "extra", "do", [-16, self.name(a, s='a'), x, "give"]]])
				self.cond[0] += 1
			elif "power and + soul" in t:
				b.extend(["extra", "do", [-16, self.digit(a, self.cond[0]), x, "soul"]])
				self.cond[0] += 1
			elif "power and the following ability" in t or "power and \"[" in aa:
				b.extend(["extra", "do", [-16, self.name(a, s='a'), x, "give"]])
			elif "power and your opponent cannot use" in t and "cannot use \"[auto] encore\"" in aa:
				b.extend(["do", [-21, "[CONT] Your opponent cannot use \"[AUTO] Encore\" until end of turn.", x, "give"]])
			elif "your opponent cannot play event cards and \"backup\" from his or her hand" in t:
				b.extend(["do", [-21, "[CONT] Your opponent cannot play event cards and \"Backup\" from his or her hand.", x, "give"]])
			elif "your opponent may not play backup from hand" in t:
				b.extend(["do", [-21, "[CONT] Your opponent cannot play \"Backup\" from his or her hand.", x, "give"]])
			elif ("at the end of turn" in t or "at the end of the turn" in t) and ("put this in your memory" in t or "send this to memory" in t):
				b.extend(["do", [0, "[AUTO] At the end of the turn, put this card into your memory.", -3, "give"]])
				if "at the end of the turn" in t:
					tt = "at the end of the turn"
				elif "at the end of turn" in t:
					tt = "at the end of turn"
				t = t[:t.index(tt)]
		elif "this gets + soul" in t:
			b = [0, self.digit(a, self.cond[0]), x, "soul"]
		elif "this gets +x power" in t:
			b = [0, self.digit(a, self.cond[0]), x, "power"]
			if "x = the number of  characters among those cards " in t or "x =  times # of  characters among those cards" in t or "x =  times # of characters with either  or  among those cards" in t or "x =  multiplied by the number of  characters revealed among those card" in t:
				pass
			elif "x = the number of cards you revealed" in t or "x = the number of cards revealed" in t:
				b.extend(["#", "Revealed"])
			elif "» or «" in aa and ("x =  times # of characters that are either  or  among those cards" in t or "x = the number of  or  characters among those card" in t):
				pass
			elif "x =  times # of climax cards in your waiting room" in t:
				b.extend(["#", "Climax", "Waiting"])
				if "all battling characters get the following ability" in t:
					b.extend(["do", [-25, self.name(a, s='a'), x, "give"]])
			elif "» or «" in aa and any(_ in t for _ in ("x =  multiplied by the number of  or  characters you have", "x =  times # of your characters with  or ", "x =  times # of your characters with either  or ", "x =  times number of your characters with  or ", "x = the number of  or  characters you have", "x =  multiplied by the number of  or  or  characters you have")):
				b.extend(["#", "Trait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"])
				if aa.count("» or «") == 2:
					b[b.index("Trait") + 1] += f"_{self.trait(a, self.cond[2] + 2)}"
					self.cond[2] += 1
				self.cond[2] += 2
			elif ("x =  times # of your other characters with  or " in t or "x =  times # of your other characters with either  and/or " in t or "x = the number of other  or  characters you have" in t) and ("» or «" in aa or "» and/or «" in aa):
				b.extend(["#", "Trait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}", "other"])
				self.cond[2] += 1
			elif any(f"times # of your characters that are either {cl} or " in aa for cl in self.colour):
				b.extend(["#", "CColourT", f"{self.colour_t(a)}_{self.trait(a, self.cond[2])}"])
				self.cond[2] += 1
			elif "x = the number of characters your opponent has" in t or "x =  times # of your opponent's characters" in t:
				b.extend(["#", "opp"])
			elif "x =  times # of cards in your stock" in t:
				b.extend(["#", "Stock"])
			elif "x =  times # of markers under this" in t:
				b.extend(["#", "Marker", "under"])
			elif "x =  multiplied by the soul of this" in t:
				b.extend(["X", "xsoul", "x", self.digit(a, self.cond[0])])
			elif "x = the number of other  characters you have" in t or "x =  times # of your other  characters" in t or "x = the number of your other  character" in t or "x = number of your other  character" in t:
				b.extend(["#", "Trait", self.trait(a, self.cond[2]), "other"])
				self.cond[2] += 1
			elif "x = the number of  characters you have" in t or "x =  times # of your  characters" in t or "x =  multiplied by the number of  characters you have" in t or "x =  multiplied by the number of your  characters" in t or "x equals the number of your  characters" in t:
				b.extend(["#", "Trait", self.trait(a, self.cond[2])])
				self.cond[2] += 1
			elif "x =  times level of your opponent" in t:
				b.extend(["X", "xplevel", "xopp", "x", self.digit(a, self.cond[0])])
			elif "x =  multiplied by the level of the character opposite this" in t:
				b.extend(["X", "xlevel", "xopposite"])
			self.cond[0] += 1
		elif "you cannot use " in t and "\"[auto] encore\"" in aa:
			b = [-21, "[CONT] You cannot use \"[AUTO] Encore\".", x, "give"]
		elif "your opponent may not use \"[auto] encore\"" in aa or "your opponent cannot use \"[auto] encore\"" in aa:
			b = [-21, "[CONT] Your opponent cannot use \"[AUTO] Encore\" until end of turn.", x, "give"]
		elif "your opponent cannot play events from hand" in t or "your opponent cannot play event cards from their hand" in t:
			b = [-21, "[CONT] Your opponent cannot play events from hand", x, "give"]
		elif "your opponent cannot play climax cards from hand" in t:
			b = [-21, "[CONT] Your opponent cannot play climax cards from hand", x, "give"]

		if "put the top card of your deck in your clock" in t:
			e = ["damageref", 1]
			if "if not" in t:
				t = self.donot_filter(t)
			if "this gets + power" in t and t.index("put the top card of your deck in your clock") < t.index("this gets + power"):
				_ = e
				e = b
				b = _
		elif "put the top  cards of your deck in your clock" in t or "put  cards from top of your deck in your clock" in t or "put the top  cards of your deck in clock" in t:
			e = ["damageref", self.digit(a, self.cond[0])]
		elif "put this in clock" in t or "put this in your clock" in t:
			e = [0, "clocker"]
		elif "put this in the waiting room" in t or "put this in your waiting room" in t:
			e = [0, "waitinger"]
			if "at the start of your next" in t and "] at the start of your next" not in aa and "\"at the start of your next" not in aa:
				e.extend(["do", [0, self.name(a, s='at'), 3, "give"]])
			if "at the beginning of your next" in t and "] at the beginning of your next" not in aa and "\"at the beginning of your next" not in aa:
				ts = "at the beginning of your next"
				if "put this in the waiting room" in t:
					tt = "put this in the waiting room"
				elif "put this in your waiting room" in t:
					tt = "put this in your waiting room"
				if t.index(ts) < t.index(tt):
					e = []
				else:
					e.extend(["do", [0, self.name(a, s='at'), 3, "give"]])
		elif "put this at the bottom of your deck" in t or "put this on the bottom of your deck" in t or "put this on the bottom of the deck" in t:
			e = [0, "decker", "bottom"]
		elif "put this on the bottom of the stock" in t:
			if t.index("put this on the bottom of the stock") < 20:
				g = [0, "stoker", "bottom"]
			else:
				e = [0, "stoker", "bottom"]
		elif "put this in your stock" in t or "put this in stock" in t:
			e = [0, "stocker"]
		elif "put this in your memory" in t or "send this to memory" in t:
			if "rest this" in t and "at the beginning of your next" in t and t.index("rest this") < t.index("memory"):
				pass
			elif ("\nput this in your memory" in aa and aa.index("\nput this in your memory") >= len(aa) - 2 - len("\nput this in your memory")) or ("\nsend this to memory" in aa and aa.index("\nsend this to memory") >= len(aa) - 2 - len("\nsend this to memory")):
				e = [0, "memorier"]
			elif t.endswith("put this in your memory."):
				e = [0, "memorier"]
				if "\nif your memory has  or less card" in t:
					self.cond_later = True
					self.cond = [0, 0, 0, 0, 0, 0]
					ts = "\nif your memory has"
					_ = a[[_.start() for _ in finditer(ts, a.lower())][0]:]
					_ = self.condition(_, f"{ts}{t.split(ts)[1]}", self.a_replace(_))
					_.extend(["do", e])
					e = _
			elif ("send this to memory" in t and t.index("send this to memory") < 20) or ("put this in your memory" in t and t.index("put this in your memory") < 20) or "send this to memory. if so," in t:
				g = [0, "memorier"]
				if "at the start of your next" in t:
					g.extend(["if", 1, "do", [-21, self.name(a, s='at'), 3, "give"]])
					t = t.split("at the start of your next")[0]
			elif ("at the start of your next" in t and ("] at the start of your next" not in t or "\"at the start of your next" not in aa)) or ("at the beginning of your next" in t and ("] at the beginning of your next" not in t or "\"at the beginning of your next" not in aa)):
				e = [0, "memorier"]
				e.extend(["if", 1, "do", [-21, self.name(a, s='at'), 3, "give"]])
			else:
				e = [0, "memorier"]
				if "choose   in your memory" in t:
					gg, t = self.seperate("choose   in your memory", a, t, aa)
					e.extend(gg)
		elif "return this to your hand" in t or "return this to hand" in t or "return this in your hand" in t:
			e = [0, "hander"]
		elif "return this to your deck" in t:
			e = [0, "decker"]
		elif "this cannot become reverse" in t and "\"[CONT]" not in a:
			e = [0, "[CONT] This card cannot become [REVERSE].", x, "give"]
		elif "this's soul does not decrease by side attacking" in t or "this may side attack without soul penalty" in t or "this may side attack this turn without soul penalty" in t:
			e = [0, "[CONT] This card's soul does not decrease by side attacking.", x, "give"]
		elif "you cannot play  from your hand" in t and "you cannot play \"" in aa:
			e = [-21, f"[CONT] You cannot play \"{self.name(a, self.cond[1], s='n')}\" from your hand.", x, "give"]
		elif "you cannot attack this turn" in t:
			e = [-21, "[CONT] You cannot attack until end of turn.", 1, "give"]
		elif "you cannot receive damage by the  effect of your opponent's character" in t and "damage by the [auto] effect" in aa:
			e = [-21, "[CONT] You cannot receive damage by the [AUTO] effect of your opponent's characters", x, "give"]
			if "during this's battle" in t:
				e[0] = 0
				e[1] = e[1].replace("] You", "] During this card's battle, you")

		if "rest all your other standing character" in t or "rest all your other stand character" in t:
			i = [-1, "rest", "Stand", "Other"]
		elif "rest all your opponent's standing character" in t or "rest all your opponent's stand character" in t:
			i = [-1, "rest", "Stand", "Opp"]
		elif "rest this" in t:
			i = [0, "rest"]
			if "at the beginning of your next" in t or "at the start of your next" in t:
				i.extend(["do", [-21, self.name(a, s='at'), 3, "give"]])
				if "at the beginning of your next" in t:
					t = t.split("at the beginning of your next")[0]
				elif "at the start of your next" in t:
					t = t.split("at the start of your next")[0]
			elif "move it to any slot on the stage" in t:
				i.extend(["extra", "do", [-16, "move", "this"]])
		elif "reverse this" in t:
			i = [0, "reverse"]
		elif "stand this" in t:
			i = [0, "stand"]
			if "move this to another empty slot on the stage" in t:
				i.extend(["extra", "do", [-16, "move", "this", "Open"]])

		if c and "do" in c:
			cc = True

		if i and h:
			i.extend(["do", h])
		elif not i and h:
			i = h

		if e and i:
			e.extend(["do", i])
		elif not e and i:
			e = i

		if b and e:
			b.extend(["do", e])
		elif not b and e:
			b = e

		if c and b:
			if cc:
				c[c.index("do") + 1].extend(["do", b])
			else:
				c.extend(["do", b])
		elif not c and b:
			c = b

		if d and c:
			if "do" and "reveal" in d and ("marker" in c or "dn" in c):
				if "dn" in c:
					c.remove("dn")
				d.extend(["done", c])
			elif "do" in d:
				d[d.index("do") + 1].extend(["do", c])
			else:
				d.extend(["do", c])
		elif not d and c:
			d = c

		if f and d:
			if "do" in f:
				f[f.index("do") + 1].extend(["do", d])
			else:
				f.extend(["do", d])
		elif not f and d:
			f = d
		if g and f:
			if "do" in g:
				g[g.index("do") + 1].extend(["do", f])
				return g
			else:
				g.extend(["do", f])
				return g
		elif not g and f:
			return f
		elif g and not f:
			return g
		else:
			return []

	def cont(self, a="", x=-1):
		self.cond = [0, 0, 0, 0, 0, 0]
		t = self.text(a)
		aa = self.a_replace(a)
		c = []
		de = ["Stage"]
		e = []

		d, t = self.limit(t, a)

		if "this gets - level while in your hand" in t or "this gets - level in your hand" in t:
			if "if your waiting room has  or less climax" in t or "if there are  or fewer climax cards in your waiting room" in t or "if the number of climax in your waiting room is  or less" in t:
				d.extend(["ClimaxWR", self.digit(a, self.cond[0]), "pHlower"])
			elif "if there are  or more climax cards in your waiting room" in t or "f the number of climax cards in your waiting room is  or more" in t:
				d.extend(["ClimaxWR", self.digit(a, self.cond[0])])
			elif "if the number of cards named  in your waiting room is  or more" in t or "if you have  or more  in your waiting room" in t:
				d.extend(["NameWR", self.digit(a, self.cond[0]), "Name=", self.name(a, s="a")])
				self.cond[1] += 2
			elif "if a card named  is in your clock" in t or ("if  is in your clock" in t and "if \"" in aa):
				d.extend(["NameCL", 1, "Name=", self.name(a, self.cond[1], s="a")])
				self.cond[0] -= 1
				self.cond[1] += 2
			elif "if your memory has  or more  card" in t and any(f" or more {cl} card" in aa for cl in self.colour):
				d.extend(["OMore", self.digit(a, self.cond[0]), "OColour", self.colour_t(a), "OMemory"])
				self.cond[1] += 2
			elif ("if there are  or more  in your memory" in t or "if your memory has  or more " in t) and "or more \"" in aa:
				d.extend(["OMore", self.digit(a, self.cond[0]), "OName=", self.name(a, self.cond[1], s='n'), "OMemory"])
				self.cond[1] += 2
			elif "if there are  or more cards in your memory" in t:
				d.extend(["OMore", self.digit(a, self.cond[0]), "OMemory"])
				if "if all the cards in your memory have  in name" in t:
					d.extend(["OName", self.name(a, self.cond[1], s='n'), "Oall"])
					self.cond[1] += 2
			elif "if  and  are in your level" in t:
				d.extend(["OMore", 2, "O&", "OName=", f"{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}", "OLVL"])
				self.cond[1] += 4
				self.cond[0] -= 1
			elif "if there are  or fewer cards in your deck" in t:
				d.extend(["Deck", self.digit(a, self.cond[0]), "pHlower"])
			elif ("if you have  or more characters with either  or " in t or "if you have  or more characters with  or " in t or "if you have  or more  or  character" in t) and "» or «" in aa:
				d.extend(["OMore", self.digit(a, self.cond[0]), "OTrait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"])
				self.cond[2] += 2
			elif "if you have  or more characters that are either  or " in t and any(f"{cl} or «" in aa for cl in self.colour):
				d.extend(["OMore", self.digit(a, self.cond[0]), "OCColourT", f"{self.colour_t(a)}_{self.trait(a, self.cond[2])}"])
				self.cond[1] += 1
			elif "if you have  or more " in t and " or more \"" in aa:
				d.extend(["OMore", self.digit(a, self.cond[0]), "OName", self.name(a, self.cond[1], s='n')])
				self.cond[1] += 2
			elif ("if you have  or more  character" in t and "or more «" in aa) or ("if the number of  characters you have is  or more" in t and "if the number of «" in aa):
				d.extend(["OMore", self.digit(a, self.cond[0]), "OTrait", self.trait(a, self.cond[2])])
				self.cond[2] += 1

			self.cond[0] += 1
			de = ["pHand"]
		elif "this gets - cost while in your hand" in t:
			if "if you have  or more  character" in t and "or more «" in aa:
				d.extend(["OMore", self.digit(a, self.cond[0]), "OTrait", self.trait(a, self.cond[2])])
				self.cond[2] += 1
			self.cond[0] += 1
			de = ["pHand"]
		elif "if you have  character chosen by this's effect" in t:
			self.cond[0] += 1
			d.append("Aselected")
		elif "if your opponent does not have any stand character" in t or "if your opponent has no standing character" in t:
			d.extend(["OMore", 0, "OStand", "Olower", "Oopp"])
		elif "if the total level of the cards in your level is  or higher" in t or "if the sum of levels of cards in your level zone is  or higher" in t or "if the total level of cards in your level zone is  or higher" in t or "if this sum of the levels of the cards in your level zone is  or more" in t or "if the sum of the levels of the cards in your level zone is  or higher" in t:
			d.extend(["Experience", self.digit(a, self.cond[0])])
			self.cond[0] += 1
		elif "if a card named  is in your level" in t or "if  is in your level" in t or "if you have  in your level" in t or "if  is in your level" in t:
			d.extend(["Experience", 1, "eName=", self.name(a, self.cond[1], s="n")])
			self.cond[1] += 2
		elif "if the character opposite this is higher level than this" in t or "if the level of the character opposite this is higher than the level of this" in t or "if the character opposite this is a higher level than this" in t:
			t = "".join(t.split("character opposite this is")[1:])
			d.extend(["oplevel"])
		elif "if the level of the character opposite this is higher than your opponent's level" in t:
			d.extend(["oplevel", ">p"])
			t = t.replace("if the level of the character opposite this is higher than your opponent's level", "")
		elif "if you have  or more other character" in t:
			d.extend(['OMore', self.digit(a, self.cond[0]), 'Oother'])
			self.cond[0] += 1
			if "characters with assist" in t:
				d.extend(["OText", f"{self.text_name['Assist']}"])
			elif ("characters with  and/or" in t or "with either  or " in t or "characters with  or " in t) and ("» and/or «" in aa or "» or «" in aa):
				d.extend(["OTriait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"])
				self.cond[2] += 1
			elif "with  and/or  in name" in t or "with  or  in their card name" in t:
				d.extend(["OName", f"{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}"])
				self.cond[1] += 4
			elif "characters with  in name" in t:
				d.extend(["OName", self.name(a, self.cond[1], s='n')])
				self.cond[1] += 2
		elif "if there is a marker under this" in t or "if there are markers under this" in t or "if there's a marker under this" in t or "if there are any markers under this" in t:
			d.extend(["Marker#", 1])
		elif "if there is at least  marker under this" in t:
			d.extend(["Marker#", self.digit(a, self.cond[0])])
			self.cond[0] += 1
		elif "if there are  or more markers under this" in t:
			d.extend(["Marker#", self.digit(a, self.cond[0])])
			self.cond[0] += 1
		elif "if there are  or fewer cards" in t or "if there is  or fewer card in your" in t or "if your stock has  or less card" in t:
			if "in your stock" in t or "if your stock has  or less card" in t:
				d.extend(["Stocks", self.digit(a, self.cond[0]), "lower"])
			elif "in your waiting room" in t:
				d.extend(["OMore", self.digit(a, self.cond[0]), "OWaiting", "Olower"])
			elif "in your hand" in t:
				d.extend(["Hands", self.digit(a, self.cond[0]), "lower"])
			elif "in your clock" in t:
				d.extend(["Clocks", self.digit(a, self.cond[0]), "lower"])
			self.cond[0] += 1
		elif "if the number of cards in your stock is  or more" in t:
			d.extend(["Stocks", self.digit(a, self.cond[0])])
			self.cond[0] += 1
		elif "if there are more cards in your hand than your opponent's hand" in t:
			d.extend(["Hands", "HandvsOpp"])
		elif "you have fewer cards in your hand than your opponent" in t:
			d.extend(["Hands", "HandvsOpp", "Hlower"])
		elif "if the number of cards in your hand is  or more" in t or "if you have  or more cards in your hand" in t or "if your hand has  or more card" in t:
			d.extend(["Hands", self.digit(a, self.cond[0])])
			self.cond[0] += 1
		elif "there's a climax in your climax area" in t:
			d.extend(["OMore", 1, "OClimax", "OCX"])
		elif "if there's a climax card in your opponent's climax area" in t:
			d.extend(["OMore", 1, "OClimax", "OCX", "Oopp"])
		elif "if the number of characters your opponent has is  or more" in t:
			d.extend(["OMore", self.digit(a), "OCharacter", "Oopp"])
			self.cond[0] += 1
		elif "if there are  or more  in your waiting room" in t:
			d.extend(["OMore", self.digit(a), "OName=", self.name(a, self.cond[1], s='n'), "OWaiting"])
			self.cond[0] += 1
			self.cond[1] += 2
		elif ("if there are  or more characters in your memory with  or " in t or "if your memory has  or more  or  character" in t) and "» or «" in aa:
			d.extend(["OMore", self.digit(a, self.cond[0]), "OTrait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}", "OMemory"])
			self.cond[0] += 1
			self.cond[2] += 1
		elif "if there are  or more  in your memory" in t:
			d.extend(["OMore", self.digit(a, self.cond[0]), f"OName=_{self.name(a, self.cond[1], s='n')}", "OMemory"])
			self.cond[0] += 1
			self.cond[1] += 1
		elif "if there are  or more cards in your memory" in t or "if you have  card in your memory" in t or "if you have  or more cards in memory" in t or "number of cards in your memory is  or more" in t or "if your memory has  or more card" in t:
			d.extend(["OMore", self.digit(a, self.cond[0]), "OMemory"])
			self.cond[0] += 1
			if "for each other rested characters you have" in t:
				d.extend(["Each", "Rest", "other"])
		elif ("number of  characters in your memory is  or more" in t or "if there are  or more  characters in your memory" in t) and "» characters in your memory" in aa:
			d.extend(["OMore", self.digit(a, self.cond[0]), "OTrait", self.trait(a, self.cond[2]), "OMemory"])
			self.cond[0] += 1
			self.cond[2] += 1
		elif "if  is in your memory" in t or "if there is a  in your memory" in t:
			d.extend(["OMore", 1, "OName=", self.name(a, self.cond[1], s='n'), "OMemory"])
			self.cond[1] += 2
		elif "there is no  in your memory" in t:
			d.extend(["OMore", 0, "OName=", self.name(a, self.cond[1], s='n'), "Olower", "OMemory"])
			self.cond[1] += 2
		elif "if there are cards in your memory" in t:
			d.extend(["OMore", 1, "OMemory"])
		elif "if there is a  card in your memory" in t and any(f"if there is a {cl} card in your memory" in aa for cl in self.colour):
			d.extend(["OMore", 1, "OMemory", "OColour", self.colour_t(a)])
		elif "if there's  card in your memory" in t or "if there is at least  card in your memory" in t or "if there is  card in your memory" in t:
			d.extend(["OMore", self.digit(a, self.cond[0]), "OMemory"])
			self.cond[0] += 1
		elif "if there is at least  card in your opponent's memory" in t:
			d.extend(["OMore", self.digit(a, self.cond[0]), "OMemory", "Oopp"])
			self.cond[0] += 1
		elif "if there is  or fewer character in your" in t or "if there is  or fewer other characters in your" in t:
			d.extend(["OMore", self.digit(a, self.cond[0]), "Olower"])
			self.cond[0] += 1
			if "in your back stage" in t:
				d.append("OBack")
			if "in your center stage" in t:
				d.append("OCenter")
		elif "if you have another level  or higher character" in t or "if you have another character whose level is  or higher" in t:
			d.extend(["OMore", 1, "OCLevel", self.digit(a, self.cond[0]), "Oother"])
			self.cond[0] += 1
		elif "if you have  or more climax cards in your waiting room" in t:
			d.extend(["OMore", self.digit(a, self.cond[0]), "OClimax", "OWaiting"])
			self.cond[0] += 1
		elif "if there are  or fewer climax cards in your waiting room" in t:
			d.extend(["OMore", self.digit(a, self.cond[0]), "OClimax", "OWaiting", "Olower"])
			self.cond[0] += 1
		elif "if you have  or more other  or  character" in t or "if the number of other  or  characters you have is  or more" in t:
			d.extend(["OMore", self.digit(a, self.cond[0]), "OTrait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}", "Oother"])
			self.cond[0] += 1
			self.cond[2] += 2
		elif "if you have  or more other  character" in t or "and you have  or more other  character" in t:
			d.extend(["OMore", self.digit(a, self.cond[0]), "OTrait", self.trait(a, self.cond[2]), "Oother"])
			self.cond[0] += 1
			self.cond[2] += 1
		elif "if you have  or more  character" in t:
			d.extend(["OMore", self.digit(a, self.cond[0]), "OTrait", self.trait(a, self.cond[2])])
			self.cond[0] += 1
			self.cond[2] += 1
		elif "if you have another character with" in t:
			d.extend(["OMore", 1])
			if "character with  in name" in t or "character with  in the name" in t or "character with  in its card name" in t:
				d.extend(["OName", self.name(a, self.cond[1], s="n")])
				self.cond[1] += 1
			elif "character with assist" in t:
				d.extend(["OText", self.text_name["Assist"]])
			d.append("Oother")
		elif "if you have another «" in aa:
			d.extend(["OMore", 1, "OTrait", self.trait(a, self.cond[2]), "Oother"])
			if "» or «" in aa:
				d[3] = f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"
				self.cond[2] += 1
			self.cond[2] += 1
		elif "if you have another \"" in aa or ("if you have " in t and "if you have \"" in aa) or "if you have another card named \"" in aa:
			d.extend(["OMore", 1, "Oother", "OName=", self.name(a, self.cond[1], s='n')])
			if aa.count("\" and \"") == 3:
				d = ["OMore", 4, "Oother", "O&", "OName", f"{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}_{self.name(a, self.cond[1] + 4, s='n')}_{self.name(a, self.cond[1] + 6, s='n')}"]
				self.cond[1] += 6
			elif ("and \"" in aa or "and another \"" in aa) and "in your center stage" in t and "in your back stage" in t:
				d = ["OMore", 2, "Oother", "OCBName=", f"{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}", "OCB"]
				self.cond[1] += 2
			elif "\" and \"" in aa:
				d = ["OMore", 2, "Oother", "O&", "OName=", f"{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}"]
				self.cond[1] += 2
			elif "another  and  character with " in t and "\" and " in aa:
				d = ["OMore", 2, "Oother", "O&", "OName=", f"{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}"]
				self.cond[1] += 2
				self.cond[0] += 1

			if "in your center stage" in t:
				d.append("OCenter")
			elif "in your back stage" in t:
				d.append("OBack")

			self.cond[1] += 2
		elif "if all your characters either are  or have  in name" in t and "» or have \"" in aa:
			d.extend(["All", "TraitN", f"{self.trait(a, self.cond[2])}_{self.name(a, self.cond[1], s='n')}"])
			self.cond[1] += 2
			self.cond[2] += 1
		elif "if all your characters have either  or" in t and "in name" in t and aa.count("\" or \"") == 2:
			d.extend(["All", "Name", f"{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}_{self.name(a, self.cond[1] + 4, s='n')}"])
			self.cond[1] += 6
		elif "if all your characters have  or " in t and ("in its card name" in t or "in their card name" in t) and "\" or \"" in aa:
			d.extend(["All", "Name", f"{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}"])
			self.cond[1] += 4
		elif ("if all your characters are either  or " in t or "all your characters have  and/or " in t or "if all your characters are  or " in t) and ("» or «" in aa or "» and/or «" in aa):
			d.extend(["All", "Trait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"])
			self.cond[2] += 2
		elif "if all your characters are either  or " in t and any(f"{cl} or «" in aa for cl in self.colour):
			d.extend(["All", "CColourT", f"{self.colour_t(a)}_{self.trait(a, self.cond[2])}"])
			self.cond[2] += 1
		elif "if all your characters are «" in aa or "if all of your characters are «" in aa or "if all your characters have «" in aa:
			d.extend(["All", "Trait", self.trait(a, self.cond[2])])
			self.cond[2] += 1
		elif "if there are  or fewer character" in t or "if you have  or less character" in t:
			d.extend(["OMore", self.digit(a, self.cond[0]), "Olower"])
			if "in your opponent's center stage" in t:
				d.extend(["OCenter", "Oopp"])
			elif "in your back stage" in t:
				d.extend(["OBack"])
			self.cond[0] += 1
		elif "if your opponent has  or fewer character" in t or "if your opponent has  or less character" in t:
			d.extend(["OMore", self.digit(a, self.cond[0]), "Olower", "Oopp"])
			self.cond[0] += 1
			if "characters in center stage" in t or "characters in their center stage" in t:
				d.append("OCenter")
		elif "if the number of your other  or  characters is  or more" in t:
			d.extend(["OMore", self.digit(a, self.cond[0]), "Oother", "OTrait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"])
			self.cond[0] += 1
			self.cond[2] += 2
		elif "you have  or more other" in t or "if the number of other  characters you have is  or more" in t or "if the number of your other  characters is  or more" in t:
			d.extend(["OMore", self.digit(a, self.cond[0]), "Oother"])
			self.cond[0] += 1
			if " with  or " in t and " or «" in aa:
				d.extend(["OTrait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"])
				self.cond[2] += 2
			elif " other \"" in aa:
				d.extend(["OName=", self.name(a, self.cond[1], s='n')])
				self.cond[1] += 2
			elif " other «" in aa:
				d.extend(["OTrait", self.trait(a, self.cond[2])])
				self.cond[2] += 1
		elif "if you have  or fewer other  character" in t:
			d.extend(["OMore", self.digit(a, self.cond[0]), "Oother", "Olower"])
			self.cond[0] += 1
			if "other «" in aa:
				d.extend(["OTrait", self.trait(a, self.cond[2])])
				self.cond[2] += 1
		elif "if the character opposite this has no traits" in t:
			d.extend(["Opposite", "OPtraits", 0, "OPlower"])
			t = t.split("has no traits")[1]
		elif "if the character opposite this is  or " in t and any(f"is {cl} or " in aa for cl in self.colour) and any(f" or {cl}" in aa for cl in self.colour):
			d.extend(["Opposite", "OPcolour", f"{self.colour_t(a, self.cond[4])}_{self.colour_t(a, self.cond[4] + 1)}"])
			self.cond[4] += 2
			t = t.split("this is  or ")[1]
		elif "if the level of the character opposite this is  or higher" in t or "if the character opposite this is level  or higher" in t:
			d.extend(["Opposite", "OPlevel", self.digit(a, self.cond[0])])
			self.cond[0] += 1
		elif "during battles involving this" in t or "during this's battle" in t or "in battles involving this" in t:
			d.extend(["Battle"])
			if "if the battle opponent of this is level  or higher" in t:
				d.extend(["olevel", self.digit(a, self.cond[0])])
				self.cond[0] += 1
			elif "if the level of the battle opponent of this is lower than the level of this" in t:
				d.extend(["olevelvsself", "olower"])
			elif "if the battle opponent of this has  or " in t and "» or «" in aa:
				d.extend(["otrait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"])
				self.cond[2] += 2
			elif "if the battle opponent of this has " in t and "has «" in aa:
				d.extend(["otrait", self.trait(a, self.cond[2])])
				self.cond[2] += 1
				if "x =  times level of that character" in t:
					d.extend(["xolevel", "x", self.digit(a, self.cond[0])])
		elif "if the number of cards in your opponent's clock is  or more" in t:
			d.extend(["Clocks", self.digit(a, self.cond[0]), "opp"])
			self.cond[0] += 1
		elif "if you do not have another character" in t or "if you have no other character" in t or "if you do not have any other characters" in t or "if you have no other  character" in t:
			d.extend(["OMore", 0, "Olower", "Oother"])
			if "in the center stage" in t:
				d.append("OCenter")
			if "no other character with  or " in t and "» or «" in aa:
				d.extend(["OTrait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"])
				self.cond[2] += 2
			elif "no other characters with  in the name" in t or "no other characters with  in name" in t:
				d.extend(["OName", self.name(a, self.cond[1], s='n')])
				self.cond[1] += 2
			elif "no other  character" in t and "no other «" in aa:
				d.extend(["OTrait", self.trait(a, self.cond[2])])
				self.cond[2] += 1
		elif "if the number of other characters in your center stage is  or less" in t:
			d.extend(["OMore", self.digit(a, self.cond[0]), "Olower", "Oother", "Center"])
			self.cond[0] += 1
		elif "if you have  or fewer other characters" in t or "if the number of other characters you have is  or less" in t or "if the number of your other characters is  or less" in t or "if you have  of fewer other character" in t or "if you have  or less other character" in t:
			d.extend(["OMore", self.digit(a, self.cond[0]), "Olower", "Oother"])
			self.cond[0] += 1
			if "other characters in your center stage" in t:
				d.append("OCenter")
		elif "if you do not have another " in t or "if you don't have another " in t:
			d.extend(["OMore", self.digit(a, self.cond[0]), "Olower", "Oother"])
			if "have another «" in aa:
				d.extend(["OTrait", self.trait(a, self.cond[2])])
				self.cond[2] += 1
			elif "have another \"" in aa:
				d.extend(["OName=", self.name(a, self.cond[1], s='n')])
				self.cond[1] += 2
			self.cond[0] += 1
		elif "if there are  or more cards" in t or "if you have  or more cards" in t:
			if " in your stock" in t:
				d.extend(["Stocks", self.digit(a, self.cond[0])])
			elif " in your hand" in t:
				d.extend(["Hands", self.digit(a, self.cond[0])])
			self.cond[0] += 1
		elif "if this's level is higher than your level" in t:
			d.extend(["sLevel", ">p"])

		if "pHand" not in de:
			if "for each card in your clock" in t:
				d.extend(["Each", "Clock"])
			elif "for each card in your hand" in t:
				d.extend(["Each", "Hand"])
			elif "for each climax card in your waiting room" in t:
				d.extend(["Each", "Climax", "Waiting"])
			elif "for each marker under this" in t:
				d.extend(["Each", "marker"])
			elif "for each  in your waiting room" in t:
				d.extend(["Each", "Name=", self.name(a, self.cond[1], s='n'), "Waiting"])
				self.cond[1] += 2
			elif "for each of your other cards named " in t or "for each other \"" in aa or "for each of your other character with \"" in aa:
				d.extend(["Each", "Name=", self.name(a, self.cond[1], s="n"), "other"])

				if "\" in the center stage" in aa or "\" in your center stage" in aa:
					d.append("Center")
				if "\" in your back stage" in aa:
					d.append("Back")
				self.cond[1] += 2
			elif "for each of your other  characters" in t or (("for each other  you have" in t or "for each other  character you have" in t or "for each other  character in" in t) and "for each other «" in aa):
				d.extend(["Each", "Trait", self.trait(a, self.cond[2]), "other"])
				self.cond[2] += 1
				if "in your back stage" in t or "in the back stage" in t:
					d.append("Back")
				elif "in your center stage" in t or "in the center stage" in t:
					d.append("Center")
					if "if there's a marker under this" in t:
						d.append("markers")
			elif "for each of your other" in t:
				d.extend(["Each", "other"])
				if "\" in the center stage" in aa:
					d.extend(["Name=", self.name(a, self.cond[1], s='n'), "Center"])
					self.cond[1] += 2
				elif "in your center stage that is either  or " in t and any(f"{cl} or «" in aa for cl in self.colour):
					d.extend(["CColourT", f"{self.colour_t(a)}_{self.trait(a, self.cond[2])}", "Center"])
					self.cond[2] += 1
				elif "other back stage «" in aa:
					d.extend(["Trait", self.trait(a, self.cond[2]), "Back"])
					self.cond[2] += 1
				elif "other rested characters" in t or "other rest characters" in t:
					d.append("Rest")
				elif "other characters with assist" in t:
					d.extend(["Text", f"{self.text_name['Assist']}"])
				elif "your other  or  character" in t and any(f"{cl} or «" in aa for cl in self.colour):
					d.extend(["CColourT", f"{self.colour_t(a)}_{self.trait(a, self.cond[2])}"])
					self.cond[2] += 1
				elif ("other  or  character" in t or "characters with  or " in t or "characters with either  or " in t) and "or «" in aa:
					d.extend(["Trait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"])
					self.cond[2] += 2
				elif "characters with " in t and self.name(a, self.cond[1], s='n') in self.text_name:
					d.extend(["Text", self.text_name[self.name(a, self.cond[1], s='n')]])
					self.cond[1] += 2
				elif "level  or lower characters" in t:
					d.extend(["CLevel", self.digit(a, self.cond[0]), "Llower"])
					self.cond[0] += 1
				elif " or  or " in t and "\" or \"" in aa:
					d.extend(["Name=", f"{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}_{self.name(a, self.cond[1] + 4, s='n')}"])
					self.cond[1] += 6
				elif "your other \"" in aa:
					d.extend(["Name=", self.name(a, self.cond[1], s='n')])
					self.cond[1] += 2
			elif ("for each of your  character" in t or "for each  character" in t) and ("each of your «" in aa or "for each «" in aa):
				d.extend(["Each", "Trait", self.trait(a, self.cond[2])])
				self.cond[2] += 1
				if "characters in the back stage" in t:
					d.append("Back")
				elif "character in your level zone" in t:
					d.append("LevelZ")
			elif "for each card in your opponent's memory" in t:
				d.extend(["Each", "opp", "Memory"])
			elif "for each character in your opponent's back stage" in t or "for each of your opponent's back stage character" in t:
				d.extend(["Each", "opp", "Back"])
			elif "for each other rested character you have" in t:
				d.extend(["Each", "Rest", "other"])
			elif "for each of your opponent's rested character" in t or "for each of your opponent's rest character" in t:
				d.extend(["Each", "Rest", "opp"])
			elif "for each standing character your opponent has" in t:
				d.extend(["Each", "Stand", "opp"])
			elif "for each different trait on your characters" in t:
				d.extend(["Each", "Traits"])
			elif "for each your other level  or lower character" in t:
				d.extend(["Each", "CLevel", self.digit(a, self.cond[0]), "Llower"])
				self.cond[0] += 1

			if t.startswith("alarm"):
				de = ["Alarm"]
			elif "if this is in memory" in t or "if this is in your memory" in t:
				de = ["sMemory"]
			elif "if this is in the waiting room" in t:
				de = ["sWaiting"]
			elif "if this is in the middle position of the center stage" in t or "if this is in the middle position of your center stage" in t or "if this is in the center stage center slot" in t or "and this is in the center stage center slot" in t:
				de = ["sMiddle"]
			elif "if this is in the center stage" in t:
				de = ["sCenter", "Stage"]
				if "center stage and not reverse" in t:
					de.append("Not_Reverse")

		if "you're level  or higher" in t or ("your level is  or higher" in t and "if the total level of the cards" not in t) or "if you are level  or higher" in t:
			d.extend(["plevel", self.digit(a, self.cond[0])])
			self.cond[0] += 1
		elif "if you are level " in t:
			d.extend(["plevel", self.digit(a, self.cond[0]), "p=="])
			self.cond[0] += 1

		if t.startswith("assist"):
			d.append("Assist")
			if self.name(a, self.cond[1], s='n') in self.text_name:
				d.extend(["Text", self.text_name[self.name(a, self.cond[1], s='n')]])
				self.cond[1] += 2
			elif "all your level  or higher characters in front" in t:
				d.extend(["flevel", self.digit(a, self.cond[0])])
				self.cond[0] += 1
			elif "all your level  or lower characters in front" in t:
				d.extend(["flevel", self.digit(a, self.cond[0]), "lower"])
				self.cond[0] += 1
			elif "all your  or  characters in front" in t or "all your characters with  or  in front" in t:
				d.extend(["Trait", f"{self.trait(a)}_{self.trait(a, 1)}"])
				self.cond[2] += 2
			elif "all your  characters in front" in t:
				d.extend(["Trait", self.trait(a, self.cond[2])])
				self.cond[2] += 1
			elif "all your characters with  or  in name" in t:
				d.extend(["Name", f"{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}"])
				self.cond[1] += 4
			elif "all your characters in front of this with  in name" in t:
				d.extend(["Name", self.name(a, self.cond[1], s='n')])
				self.cond[1] += 2

			if "get + level" in t:
				c = ["front", self.digit(a, self.cond[0]), x, "level"]
				if "level and + power" in t:
					c.extend(["front", self.digit(a, self.cond[0] + 1), x, "power"])
			elif "get + power" in t:
				c = ["front", self.digit(a, self.cond[0]), x, "power"]
				if "power and + soul" in t:
					c.extend(["front", self.digit(a, self.cond[0] + 1), x, "soul"])
				elif "power and \"[" in aa:
					c.extend(["front", self.name(a, s="a"), x, "ability"])
			elif "get + soul" in t:
				c = ["front", self.digit(a, self.cond[0]), x, "soul"]
			elif "get +x power" in t:
				c = ["front", self.digit(a, self.cond[0]), x, "power"]
			elif "get \"" in t or "get the following ability" in t:
				c = ["front", self.name(a, s="a"), x, "ability"]
		elif t.startswith("bodyguard") or t.startswith("great performance"):
			c = [0, "", -1, "bodyguard"]
		elif t.count("if your memory has  or more card") == 1 and t.count("if there are  or more card") > 0:
			c = ["multicond", []]
			a1 = []
			a3 = []
			a1.append(a.lower().split("if your memory has ")[1].split("if there are ")[0])
			a1.extend(a.lower().split("if there are ")[1:])

			for at in a1:
				_ = at.split('or more cards, ')[1].replace('"', "'").capitalize()
				if _[-1] == " ":
					_ = _[:-1]
				a3.append(f"[CONT] if your memory has {self.digit(at)} or more cards, this gets the following ability. \"[CONT] {_}\"")

			for a2 in a3:
				d = self.cont(a=a2, x=-3)
				if d:
					c[1].append(d)
			de = []
			d = []
			e = []
			t = ""
		elif "this's card name will also be regarded as" in t or "this is also considered to have  as the name" in t:
			c = [0, self.name(a, self.cond[1], s='n'), x, "name"]
		elif "effect of [cxcombo] of your other " in t:
			c = [0, self.name(a, self.cond[1], s='n'), x, ]
			if "puts  additional card from the bottom of your opponent's deck in the waiting room" in t:
				c.extend(["Add", ["mill", self.digit(a, self.cond[0])]])
			c.append("contadd")
		elif t.count("if there are  or more markers under this") > 1 or t.count("if there are  or more markers") > 1:
			c = ["multicond", []]
			a1 = a.lower().split("if there are")[1:]
			a3 = []
			for at in a1:
				if "or more markers under this," in at:
					a4 = at.lower().split('or more markers under this,')[1]
				elif "or more markers," in at:
					a4 = at.lower().split('or more markers,')[1]
				a3.append(f"[CONT] if there are {self.digit(at)} or more markers under this, this gets the following ability. \"[CONT] {a4[1].upper()}{a4[2:]}\"")
			for a2 in a3:
				d = self.cont(a=a2, x=-3)
				if d:
					c[1].append(d)
			de = []
			d = []
			e = []
			t = ""
		elif "when this attacks, you may instead choose  character on your opponent's back stage, and have this front attack with the chosen character as the defending character" in t or "when this attacks, you may instead choose  character in opponent's back stage and have this front attack that character as the defending character" in t:
			c = [1, "", -1, "backatk", "may"]
		elif "you may play this with  cost" in t:
			if "choose  of your cards named " in t:
				self.cond[0] += 1
			c = [0, self.digit(a, self.cond[0]), -1, "waiting_cost", self.name(a, self.cond[1], s='n')]
		elif "cost of the character opposite this is  or lower" in t or "if the character opposite this is cost  or lower" in t:
			if "this does not reverse" in t or "this cannot become reverse" in t:
				c = [0, "", -1, "no_reverse", "opcost", self.digit(a, self.cond[0]), "oplower"]
		elif "if you would pay the cost for  event in your hand" in t:
			if "you may put  marker from under this in your waiting room instead of  card from your stock" in t:
				c = [0, self.digit(a, self.cond[0]), x, "estock"]
		elif "if you would pay the act cost for  of your characters in your hand or stage" in t:
			if "you may put  marker from under this in your waiting room instead of  card from your stock" in t:
				c = [0, self.digit(a, self.cond[0]), x, "astock"]
		elif "when you pay for the cost of act of your " in t and "[act] of your \"" in aa:
			if "you may put  marker from under this in the waiting room in place of a stock" in t:
				c = [0, self.digit(a, self.cond[0]), x, "astock", "Name", self.name(a, self.cond[1], s='n')]

		elif "all your other character" in t or "all of your other" in t or "all your other" in t or "all your other cards" in t:
			dd = []
			if self.name(a, self.cond[1], s='n') in self.text_name and "the following ability" not in t and "get \"[" not in a:
				dd = ["Text", self.text_name[self.name(a, self.cond[1], s='n')]]
				self.cond[1] += 2
			elif "characters that are either  or " in t and any(f"{cl} or «" in aa for cl in self.colour):
				dd = ["CColourT", f"{self.colour_t(a)}_{self.trait(a, self.cond[2])}"]
				self.cond[2] += 1
			elif "other characters without \"" in aa:
				dd = ["NameWo", self.name(a, self.cond[1], s='n')]
			elif " your other characters with \"" in aa or "all your other \"" in aa or "all of your other \"" in aa or "all your other cards named" in t:
				dd = ["Name", self.name(a, self.cond[1], s='n')]
				if "  or  or " in t and "\" or \"" in aa:
					if "\" is in your climax area" in aa:
						dd[1] = f"{self.name(a, self.cond[1] + 2, s='n')}_{self.name(a, self.cond[1] + 4, s='n')}_{self.name(a, self.cond[1] + 6, s='n')}"
						dd.extend(["cx", self.name(a, self.cond[1], s='n')])
					else:
						dd[1] = f"{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}_{self.name(a, self.cond[1] + 4, s='n')}"
				elif "\" or \"" in aa or "\" and \"" in aa:
					dd[1] = f"{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}"
			elif "all your other «" in aa or "all of your other «" in aa or "all your other characters with either «" in aa or "all your other characters with «" in aa:
				dd = ["Trait", ""]
				if "» or «" in aa or "» and «" in aa or "» and/or «" in aa:
					dd[1] = f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}"
					self.cond[2] += 1
				elif "» or \"" in aa and "characters with  or  in its card name" in t:
					dd = "TraitN", f"{self.trait(a, self.cond[2])}_{self.name(a, self.cond[1], s='n')}"
					self.cond[1] += 2
				elif "» character" in aa:
					dd[1] = self.trait(a, self.cond[2])
				self.cond[2] += 1

			if dd:
				d.extend(dd)

			if (("gets + power and " in t or "get + power and" in t) and "power and \"[" in aa) or "power and the following ability" in t or "power and the following  abilities" in t:
				c = [-2, self.digit(a, self.cond[0]), x, "power"]
				self.cond[0] += 1
				if "power and the following  abilities" in t:
					for _ in range(self.digit(a, self.cond[0])):
						c.extend([-2, self.name(a, self.cond[5], s='a'), x, f"ability"])
						self.cond[5] += 1
				else:
					c.extend([-2, self.name(a, s="a"), x, "ability"])
			elif "get the following ability" in t or " get \"[" in aa:
				c = [-2, self.name(a, s='a'), x, "ability"]
				if "and this gets \"" in aa:
					c[0] = -32
			elif "get + power" in t or "gets + power" in t:
				if "whose level is  or lower" in t:
					c = [-2, self.digit(a, self.cond[0] + 1), x, "CLevel", self.digit(a, self.cond[0]), "Llower", "power"]
				else:
					c = [-2, self.digit(a, self.cond[0]), x, "power"]
			elif "get + level" in t or "gets + level" in t:
				c = [-2, self.digit(a, self.cond[0]), x, "level"]
				if "level and + power" in t:
					c.extend([-2, self.digit(a, self.cond[0] + 1), x, "power"])
			elif "get + soul" in t or "gets + soul" in t:
				c = [-2, self.digit(a, self.cond[0]), x, "soul"]
			elif "get +x power" in t:
				if "x =  multiplied by that character's level" in t or "x =  times level of that character" in t or "x = that character's level ×" in t:
					c = [-2, self.digit(a, self.cond[0]), x, "xlevel", "x", self.digit(a, self.cond[0]), "power"]
		elif "all your characters whose level is higher than your level" in t:
			if "gets + power" in t:
				c = [-1, self.digit(a, self.cond[0]), x, "LevelP", "power"]
		elif "all your characters get" in t or "all of your characters get" in t:
			if "get + power and + soul" in t:
				c = [-1, self.digit(a, self.cond[0]), x, "power", -1, self.digit(a, self.cond[0] + 1), x, "soul"]
			elif "get + soul" in t:
				c = [-1, self.digit(a, self.cond[0]), x, "soul"]
			elif "get + power" in t:
				c = [-1, self.digit(a, self.cond[0]), x, "power"]
			elif "get the following ability" in t or ("get " in t and "get \"" in aa):
				c = [-1, self.name(a, s='a'), x, "ability"]
				if "character opposite this gets - soul" in t:
					c.extend([-6, self.digit(a, self.cond[0]), x, "Opposite", "soul"])
		elif "all your opponent's characters get" in t and "get \"[" in aa:
			c = [-1, self.name(a, s='a'), x, "opp", "ability"]
		elif ("if all your " not in t or ("if all your " in t and t.count("all your ") > 1)) and ("all your " in t or "all your characters with " in t):
			dd = []
			if "all your characters with no traits" in t:
				dd = ["Trait", ""]
			elif any(f"all your {cl} characters" in aa for cl in self.colour):
				dd = ["Colour", self.colour_t(a)]
			elif "all your characters with " in t and self.name(a, self.cond[1], s='n') in self.text_name:
				dd = ["Text", self.text_name[self.name(a, self.cond[1], s='n')]]
				self.cond[3] += 1
				self.cond[1] += 2
			elif "all your \"" in aa or "all your characters with  in the name" in t or "all your characters with  in its card name" in t:
				dd = ["Name", self.name(a, self.cond[1], s='n')]
				if "\" and \"" in aa:
					dd[1] = f"{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}"
			elif "all your «" in aa:
				dd = ["Trait", self.trait(a, self.cond[2])]
				if "» or «" in aa:
					dd[1] = f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 2)}"
			elif "all your level  or higher characters" in t:
				dd = ["CLevel", self.digit(a, self.cond[0])]
				self.cond[0] += 1
			if dd:
				d.extend(dd)

			if "get + power" in t:
				c = [-1, self.digit(a, self.cond[0]), x, "power"]
			elif "get the following ability" in t or ("get " in t and "get \"" in aa):
				c = [-1, self.name(a, self.cond[3], s='a'), x, "ability"]
			elif "get + soul" in t:
				c = [-1, self.digit(a, self.cond[0]), x, "soul"]
		elif "your other level  or lower character in the middle position of your center stage" in t or "your other level  or lower center stage middle character" in t:
			if "gets + power" in t:
				c = [-5, self.digit(a, self.cond[0] + 1), x, "Middle", "Level", self.digit(a, self.cond[0]), "lower", "other", "power"]
		elif "your other character in" in t or "your other  character in" in t:
			if "center stage center slot" in t or "middle position of your center stage" in t or "middle position of the center stage" in t:
				if "gets + power and " in t and "power and \"[" in aa:
					c = [-5, self.digit(a, self.cond[0]), x, "Middle", "other", "power", -5, self.name(a, s="a"), x, "Middle", "other", "ability"]
				elif 'gains "[' in aa or 'gets "[' in aa:
					c = [-5, self.name(a, s='a'), x, "Middle", "ability", "other"]
				elif "gets + power" in t:
					c = [-5, self.digit(a, self.cond[0]), x, "Middle", "other", "power"]
				elif "gets + soul" in t:
					c = [-5, self.digit(a, self.cond[0]), x, "Middle", "other", "soul"]
				if "your other  character in" in t and "your other «" in aa:
					c.insert(c.index("Middle") + 1, self.trait(a, self.cond[2]))
					c.insert(c.index("Middle") + 1, "Trait")
		elif ("in your hand gets - cost" in t and "\" in your hand gets -" in aa) or ("gets - cost while in your hand" in t and "this gets -" not in t):
			c = [-1, self.digit(a, self.cond[0]), x, "Name=", self.name(a, self.cond[1], s='n'), "Hand", "cost"]
		elif "events get + cost while in your opponent's hand" in t:
			c = [-1, self.digit(a, self.cond[0]), x, "Event", "Hand", "opp", "cost"]
		elif "character opposite this" in t or "card opposite this" in t:
			if "this gets + power, , and the character opposite this gets - soul" in t:
				c = [0, self.digit(a, self.cond[0]), x, "power", 0, self.name(a, s='a'), x, "ability", -6, self.digit(a, self.cond[0] + 1), x, "Opposite", "soul"]
			elif "this gets + power" in t and "this gets the following ability" in t:
				c = [0, self.digit(a, self.cond[0]), x, "power", -6, self.name(a, s='a'), x, "Opposite", "ability"]
			elif "this gets +x power" in t and "x =  multiplied by the level of the character opposite this" in t:
				c = [0, self.digit(a, self.cond[0]), x, "power"]
			elif "gets + soul and cannot side attack" in t:
				c = [-6, "[CONT] This cannot side attack.", x, "Opposite", "ability", -6, self.digit(a, self.cond[0]), -1, "Opposite", "soul"]
			elif "gets + soul" in t or "gets - soul" in t:
				c = [-6, self.digit(a, self.cond[0]), x, "Opposite", "soul"]
			elif ("gets " in t and "gets \"[" in aa) or "this gets the following ability" in t:
				c = [-6, self.name(a, s='a'), x, "Opposite", "ability"]
			elif ("gets " in t or "get " in t) and ("get «" in aa or "gets «" in aa):
				c = [-6, self.trait(a, self.cond[2]), x, "Opposite", "trait"]
			elif "cannot be returned to hand, move to another stage position, or be put into memory" in t:
				c = [-6, "[CONT] This card cannot be returned to hand, move to another stage position, or be put into memory.", -3, "Opposite", "ability"]
			elif "cannot move to another position on the stage" in t or "cannot move to another slot" in t or "cannot move to another position of the stage" in t:
				c = [-6, "[CONT] This card cannot move to another position on the stage.", -3, "Opposite", "ability"]
			elif "cannot front attack" in t:
				c = [-6, "", x, "no_front", "opgive"]
			elif "cannot side attack" in t:
				c = [-6, "", x, "no_side", "opgive"]
		elif "this gets  and is also considered to have  as the name" in t:
			c = [0, self.trait(a, self.cond[2]), x, "trait", 0, self.name(a, self.cond[1], s='n'), x, "name"]
		elif "this gets + power and the following ability" in t or ("this gets + power and " in t and "and \"[" in aa):
			c = [0, self.digit(a, self.cond[0]), x, "power", 0, self.name(a, s='a'), x, "ability"]
			if "the card opposite this" in t:
				c.extend(self.cont(a=a[a.lower().index("the card opposite this"):]))
		elif "this gets +x power" in t:
			c = [0, self.digit(a, self.cond[0]), x, "power"]
		elif "this gets - level" in t or "this gets + level" in t:
			c = [0, self.digit(a, self.cond[0]), x, "level"]
			if "level, + power, and the following ability" in t:
				c.extend([0, self.digit(a, self.cond[0] + 1), x, "power"])
				c.extend([0, self.name(a, s='a'), x, "ability"])
			elif "level and + power" in t or "and gets + power" in t:
				c.extend([0, self.digit(a, self.cond[0] + 1), x, "power"])
			if "and cannot be chosen by your opponent's effects" in t:
				c.extend([0, "[CONT] This card cannot be chosen by your opponent's effects.", x, "ability"])
		elif "this gets - cost" in t or "this gets + cost" in t:
			c = [0, self.digit(a, self.cond[0]), x, "cost"]
		elif "this gets + power" in t or "this gets - power" in t:
			c = [0, self.digit(a, self.cond[0]), x, "power"]
			if "power, " in t and "power, \"[" in aa:
				c.extend([0, self.name(a, s='a'), x, "ability"])
			elif "power and + soul" in t:
				c.extend([0, self.digit(a, self.cond[0] + 1), x, "soul"])
			if "and the character opposite this gets + soul" in t or "and the card opposite this gets - soul" in t:
				c.extend([-6, self.digit(a, self.cond[0] + 1), x, "Opposite", "soul"])
			elif "and cannot be reverse by effects of [auto] abilities of your opponent's characters" in t:
				c.extend([0, "[CONT] This cannot be [REVERSE] by effects of [AUTO] abilities of your Opponent's Characters.", x, "ability"])
			elif "and this cannot be chosen by your opponent's effects" in t:
				c.extend([0, "[CONT] This card cannot be chosen by your opponent's effects.", x, "ability"])
		elif "this gets + soul" in t:
			c = [0, self.digit(a, self.cond[0]), x, "soul"]
		elif "this gets «" in aa:
			c = [0, self.trait(a, self.cond[2]), x, "trait"]
		elif "this gets the following  abilities" in t:
			for _ in range(self.digit(a, self.cond[0])):
				c.extend([0, self.name(a, self.cond[5], s='a'), x, f"ability{_}"])
				self.cond[5] += 1
			self.cond[0] += 1
		elif ("this gets " in t and "this gets \"[" in aa) or "this gets the following ability" in t:
			c = [0, self.name(a, s='a'), x, "ability"]
		elif "this cannot be returned to hand, move to another stage position, or be put into memory" in t:
			c = [0, "", x, "no_move", "no_hand", "no_memory"]
		elif "this cannot move to another position" in t:
			c = [0, "", x, "no_move"]
			if "this cannot side attack" in t in t:
				c.append("no_side")
		elif "no player may play backup from hand" in t or "no player may use backup from hand" in t or ("all players cannot play  from their hand" in t and "\"backup\"" in aa):
			c = [0, "", x, "no_backup", "both"]
		elif (("your opponent cannot play  from hand" in t or "your opponent cannot play  from his or her hand" in t or "your opponent cannot play  from their hand" in t) and "\"backup\"" in aa) or "your opponent may not play backup from hand" in t or "your opponent cannot play backup from hand" in t:
			c = [0, "", x, "no_backup", "opp"]
		elif "your opponent cannot play event cards and  from his or her hand" in t or "your opponent can't play events or backup from hand" in t or "your opponent cannot play event cards or  from their hands" in t:
			c = [0, "", x, "no_backup", "no_event", "opp"]
		elif "your opponent cannot play events from hand" in t or "your opponent cannot play event cards from their hand" in t:
			c = [0, "", x, "no_event", "opp"]
		elif ("you cannot play event cards or  from your hand" in t and "event cards or \"backup\"" in aa) or "you cannot play events or backup from hand" in t or "you cannot play event cards and  from your hand" in t or "you cannot play event cards and  from hand" in t:
			c = [0, "", x, "no_backup", "no_event"]
		elif "you cannot play events from hand" in t:
			c = [0, "", x, "no_event"]
		elif "you cannot play a climax card from your hand" in t:
			c = [0, "", x, "no_climax"]
		elif "you cannot put  card from your hand in your clock and draw cards during your clock phase" in t or "you cannot put a card from your hand in your clock and draw cards during your clock phase" in t:
			c = [0, "", x, "no_clock"]
		elif "your opponent cannot play climax cards from hand" in t:
			c = [0, "", x, "no_climax", "opp"]
		elif "your opponent cannot use any act of characters on his or her stage" in t:
			c = [0, "", x, "no_act", "opp"]
		elif "your opponent cannot use " in t and "\"[auto] encore\"" in aa:
			c = [0, "", x, "no_encore", "opp"]
		elif "you cannot use " in t and "\"[auto] encore\"" in aa:
			c = [0, "", x, "no_encore"]
		elif "you cannot attack until end of turn" in t:
			c = [0, "", x, "skip_attack"]
		elif "you may play characters with  in name as well as climax cards from your hand without meeting the color requirement" in t:
			c = [0, "", x, "any_Clrclimax", "any_ClrChname", "Name", self.name(a, self.cond[1], s='n')]
		elif "your climax can be played from your hand without fulfilling color requirements" in t:
			c = [0, "", x, "any_Clrclimax"]
		elif "this cannot be returned to hand or put into memory" in t:
			c = [0, "", x, "no_hand", "no_memory"]
		elif "this cannot be reverse by effects of [auto] abilities of your opponent's characters" in t or "this character cannot be reverse by your opponent's character's [auto] effects" in t or "this cannot become reverse by the [auto] effects of your opponent's character" in t or "this cannot become reverse by [auto] effects of your opponent's character" in t:
			c = [0, "", x, "no_reverse_auto_OC"]
			if "this cannot side attack" in t:
				c.append("no_side")
		elif "this cannot become reverse" in t or "this does not reverse" in t or "this cannot be reverse" in t:
			c = [0, "", x, "no_reverse"]
		elif "this cannot side attack" in t:
			c = [0, "", x, "no_side"]
		elif "this cannot front attack" in t:
			c = [0, "", x, "no_front"]
		elif "this cannot direct attack" in t:
			c = [0, "", x, "no_direct"]
		elif "this cannot attack" in t:
			c = [0, "", x, "no_attack"]
		elif "this cannot be chosen by your opponent's effects" in t or "this cannot be chosen as the target of your opponent's effects" in t or "this may not be chosen by your opponent's effects" in t:
			c = [0, "", x, "no_target"]
		elif "this cannot stand during your stand phase" in t or "this does not stand during your stand phase" in t:
			c = [0, "", x, "no_stand"]
		elif "this's soul does not decrease by side attacking" in t or "this character's soul does not decrease by side attacking" in t:
			c = [0, "", x, "no_decrease"]
		elif "this cannot deal damage to players" in t or "this cannot deal damage to a player" in t:
			c = [0, "", x, "no_damage"]
		elif "you cannot take damage from your opponent character's [auto] effects" in t or "you cannot receive damage by the [auto] effect of your opponent's character" in t:
			c = [0, "", x, "no_damage_auto_opp"]
		elif "this cannot use " in t and "\"[auto] encore\"" in aa:
			c = [0, "", x, "no_encore_self"]

		if "x =  multiplied by the level of the character opposite this" in t or "x =  times level of the character opposite this" in t:
			e = ["X", "xoplevel", "x", self.digit(a, self.cond[0])]
		elif "x =  times the highest level amongst your characters with  in the name" in t:
			e = ["X", "xhighlevel", "xName", self.name(a, self.cond[1], s='n'), "x", self.digit(a, self.cond[0])]
		elif "x =  times level of that character" in t or "x = that character's level" in t or "x =  times level" in t or "x =  multiplied by that character's level" in t or "x = the level of that character" in t or "x =  times the level of that character" in t:
			e = ["X", "xlevel", "x", self.digit(a, self.cond[0])]
			if "during battles involving this" in t:
				e = []
		elif "x =  multiplied by the number of  characters in your level" in t:
			e = ["X", "xlevTrait", self.trait(a, self.cond[2]), "x", self.digit(a, self.cond[0])]

		if "x" in c:
			e = []

		if "Assist" in d and "X" in e:
			e.remove("X")

		if "during your turn" in t or "during your opponent's turn" in t or "on your turn" in t:
			d.append("Turn")
			if "during your opponent's turn" in t:
				d.append("Topp")

		d.extend(de)
		for y in (d, e):
			if y:
				if any(cont in c for cont in self.cont_key):
					for cc in self.cont_key:
						if cc in c:
							for yy in range(len(y)):
								c.insert(c.index(cc), y[yy])
				else:
					for yy in y:
						c.append(yy)
		if "ability0" in c:
			c.insert(c.index("ability0"), "ability")
			c.remove("ability0")
		if "ability1" in c:
			c.insert(c.index("ability1"), "ability")
			c.remove("ability1")
		return c

	def limit(self, t, a):
		d = []
		if "you may have up to  cards with the same name as this in your deck" in t or "you can put up to  cards with the same card name as this in your deck" in t or "you may put up to  cards with the same card name as this in your deck" in t:
			d.extend([self.digit(a, self.cond[0]), "limit"])
			self.cond[0] += 1
		elif "you can put any number of cards with the same card name as this in your deck" in t or "you may have as many copies of cards with the same name as this in your deck" in t or "you may put any number of cards with the same card name as this in your deck" in t:
			d.extend([50, "limit"])
		if d:
			t = t.split("name as this in your deck")[1]
		return d, t

	def play(self, a="", t="", p=False):
		if p:
			self.cond = [0, 0, 0, 0, 0, 0]
		if not t:
			t = self.text(a)
		c = []
		if "if there are no characters in your back stage, you cannot play this from hand" in t:
			c = [0, "Character", "Back", "lower", "play"]
		elif ("if you don't have  character with either  and/or  in name" in t or "if you don't have  character with  or  or  in name" in t) and "you cannot play this from your hand" in t:
			c = [0, "Name", f"{self.name(a, self.cond[1], s='n')}_{self.name(a, self.cond[1] + 2, s='n')}", "lower", "play"]
			self.cond[1] += 4
			if "with  or  or  in name in your center stage center slot" in t:
				c[2] = f"{c[2]}_{self.name(a, self.cond[1], s='n')}"
				self.cond[1] += 2
				c.append("Middle")
			if "[counter]" not in t:
				self.cond[0] += 1
		elif ((("if you don't have  character with  in name" in t or "if you do not have  character with  in name" in t or "if you have no characters with  in name" in t) and "\" in name" in a.lower()) or ("if you don't have a " in t and "if you don't have a \"" in a.lower())) and ("you may not play this from hand" in t or "you cannot play this from your hand" in t or "you may not play this" in t) or ("\" in its card name" in a.lower() and "if you do not have  character with  in its card name" in t):
			c = [0, "Name", self.name(a, self.cond[1], s='n'), "lower", "play"]
			self.cond[1] += 2
			if "have  character" in t:
				self.cond[0] += 1
		elif "if you do not have \"" in a.lower() and "this cannot be played from your hand" in t:
			c = [0, "Name", self.name(a, self.cond[1], s='n'), "lower", "play"]
			self.cond[1] += 2
		elif ("you do not have an  character" in t or "you do not have a  character" in t or "if you do not have any  characters" in t or "if you have no  characters" in t or "if you don't have a  character" in t) and ("this cannot be played from hand" in t or " this cannot be played from your hand" in t or "you cannot play this from your hand" in t or "you cannot play this from hand" in t):
			c = [0, "Trait", self.trait(a, self.cond[2]), "lower", "play"]
			self.cond[2] += 1
		elif "if the number of  or  characters you have is  or less" in t and "» or «" in a.lower() and "this cannot be played from your hand" in t:
			c = [self.digit(a, self.cond[0]), "Trait", f"{self.trait(a, self.cond[2])}_{self.trait(a, self.cond[2] + 1)}", "lower", "play"]
			self.cond[0] += 1
			self.cond[2] += 2
		elif "if you have  or fewer  characters, you cannot play this from hand" in t or "if the number of  characters on your stage is  or less, this cannot be played from your hand" in t or "if you have  or less  characters, this cannot be played from your hand" in t or "if you have  or fewer  characters, you may not play this from hand" in t or "if you have  or fewer  characters, you cannot play this from your hand" in t:
			c = [self.digit(a, self.cond[0]), "Trait", self.trait(a, self.cond[2]), "lower", "play"]
			self.cond[0] += 1
			self.cond[2] += 1
		elif "if you have  or fewer characters, you cannot play this from your hand" in t:
			c = [self.digit(a, self.cond[0]), "Character", "lower", "play"]
			self.cond[0] += 1
			self.cond[2] += 1
		elif "if the number of characters in your center stage is  or more, this cannot be played from your hand" in t:
			c = [self.digit(a, self.cond[0]), "Character", "Center", "play"]
			self.cond[0] += 1
		elif "if you have  or more characters, you cannot play this from your hand" in t:
			c = [self.digit(a, self.cond[0]), "Character", "play"]
			self.cond[0] += 1
		elif "if you have  or fewer climax cards in your waiting room" in t and "you cannot play this from your hand" in t:
			c = [self.digit(a, self.cond[0]), "Climax", "Waiting", "lower", "play"]
			self.cond[0] += 1
		elif "you cannot play  from your hand" in t:
			c = [-1, "Name", self.name(a, self.cond[1], s='n'), "play"]
		elif "you may play this with  cost" in t:
			if "when this is played from your hand" in t:
				c = ["pay", "may", "do", self.convert(a, t)]
		return c

	def climax(self, a=""):
		e = []
		b = []
		t = self.text(a)

		self.cond = [0, 0, 0, 0, 0, 0]
		if "for the turn" in t or " until end of turn" in t:
			x = 1
		else:
			x = -1

		if "when this is placed on your climax area from your hand" in t or 'when this is placed from hand to the climax area' in t or "when this is placed on your climax area from hand" in t or "when this is placed from hand to the climax stage" in t:
			if "perform the standby effect" in t or "perform the [standy] effect" in t:
				return self.trigger("standby")
			elif "choose up to  level  or lower character in your waiting room" in t:
				if "put it in your stock" in t or "put it to stock" in t:
					e = [self.digit(a), "salvage", f"CLevel_<={self.digit(a, 1)}", "Stock", "show", "upto"]
					self.cond[0] += 2
			elif "choose up to  character with soul in its trigger icon in your waiting room" in t or "choose up to  character with soul trigger icon in your waiting room" in t:
				if "return it to your hand" in t:
					e = [self.digit(a), "salvage", "CTrigger_soul", "upto", "show"]
					self.cond[0] += 1
			elif "choose up to   card in your waiting room" in t and self.colour_t(a).lower() in a.lower():
				if "put it in your stock" in t or "put it in stock" in t:
					e = [self.digit(a), "salvage", f"Colour_{self.colour_t(a)}", "Stock", "upto", "show"]
					self.cond[0] += 1
			elif "choose up to  character in your waiting room" in t:
				if "return it to your hand" in t:
					if "with level equal to or lower than your level" in t:
						e = [self.digit(a), "salvage", "CLevel_<=p", "show", "upto"]
						self.cond[0] += 1
			elif "put the top card of your deck in your stock" in t:
				e = ["stock", 1]
			elif "draw  card" in t:
				e = ["draw", self.digit(a, self.cond[0])]
				self.cond[0] += 1

		if "all your characters get" in t or "all of your characters get" in t:
			if "+ power and + soul" in t:
				b = [-1, self.digit(a, self.cond[0]), x, "power", "do", [-1, self.digit(a, self.cond[0] + 1), x, "soul"]]
			elif "+ soul" in t:
				b = [-1, self.digit(a, self.cond[0]), x, "soul"]
			elif "+ power" in t:
				b = [-1, self.digit(a, self.cond[0]), x, "power"]
		elif "choose up to  of your character" in t:
			if "those characters get + soul" in t:
				b = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "soul", "upto"]
			elif "those characters get + power" in t:
				b = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power", "upto"]
				if "power and + soul" in t:
					b.extend(["extra", "do", [-16, self.digit(a, self.cond[0] + 2), x, "soul"]])
		elif "choose  of your character" in t:
			if "that character gets + power and + soul" in t:
				b = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power", "extra", "do", [-16, self.digit(a, self.cond[0] + 2), x, "soul"]]
			elif "that character gets + soul" in t:
				b = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "soul"]
		elif "all your characters randomly get between +~+ soul" in t:
			b = [-1, self.digit(a, self.cond[0]), x, "random", self.digit(a, self.cond[0] + 1), "soul"]

		if e and b:
			return e + ["do", b]
		elif b:
			return b
		else:
			return []

	def marker(self, a=""):
		self.cond = [0, 0, 0, 0, 0, 0]
		t = self.text(a)
		c = []
		if "when a marker is placed under this" in t:
			if "if there are  or more markers under this" in t:
				c = ["markers", self.digit(a, self.cond[0])]
				self.cond[0] += 1
				c.extend(["do", self.convert(a, t.split("if there are  or more markers under this")[1])])
		return c

	@staticmethod
	def trigger(a=""):
		_ = {
			"door": ["pay", "may", "do", [1, "salvage", "Character", "upto", "show"], "text", "When this card triggers, you may choose a character in your waiting room, and return it to your hand."],
			"gate": ["pay", "may", "do", [1, "salvage", "Climax", "upto", "show"], "text", "When this card triggers, you may choose a climax card in your waiting room, and return it to your hand."],
			"bounce": ["pay", "may", "do", [1, "Character", "wind", "Opp", "may"], "text", "When this card triggers, you may choose an opponent's character on stage, and return it to his or her hand."],
			"standby": ["pay", "may", "do", [1, "salvage", f"CLevel_standby", "Stage", "extra", "upto", "do", [-16, "rested"]], "text", "When this card triggers, you may choose 1 character with a level equal to or less than your level +1 in your waiting room, and put it on any position of your stage as [REST]"],
			"draw": ["pay", "may", "do", ["draw", 1], "text", "When this card triggers, you may draw a card."],
			"soul": [-12, 1, 1, "soul", "text", "Give +1 soul to the attacking character until the end of the turn."],
			"shot": [-12, "[AUTO] When the next damage dealt by this card is canceled, deal one damage to your opponent", -2, "give", "Climax_auto", "text", "During this turn, when the next damage dealt by the attacking character that triggered this card is canceled, deal 1 damage to your opponent."],
			"stock": ["pay", "may", "do", ["stock", 1], "text", "When this card triggers, you may put the top card of your deck into your stock"],
			"treasure": [0, "hander", "do", ["pay", "may", "do", ["stock", 1]], "text", "When this card triggers, return this card to your hand. You may put the top card of your deck into your stock"],
			"choice": ["pay", "may", "do", [1, "salvage", "CTrigger_soul", "upto", "show", "choice"], "text", "When this card triggers, you may choose a character with [SOUL] in its trigger icon in your waiting room, and return it to your hand or put it into your stock."]
		}
		return _.get(a, [])

	def digit(self, a="", i=0, p=False, num=False):
		n = []
		t = str(a)

		for ss in self.text_name:
			if f"\"{ss}\"" in t:
				t = t.replace(f"\"{ss}\"", "")
		if t.count("[") >= 2:
			for item in self.status:
				t = t.replace(item, self.status[item])
		for ablt in self.ability:
			t = t.replace(ablt, "")
		for ss in self.set_only:
			t = t.replace(ss, "")

		if t.count("\n") == 1 and "you cannot play this from your hand.\n" in t:
			t = t.split("\n")[1]

		if t.startswith(" "):
			t = t.strip()

		if " (" in t:
			if "(If it is not, the revealed card is returned to its original place" in t:
				t = t.replace("(If it is not, the revealed card is returned to its original place", "")
			elif ")»" in t or ")\"":
				pass
			else:
				t = t.split(" (")[0]

		for s in range(7):
			if f"({s})" in t:
				t = t.replace(f"({s})", "()")

		if "[()" in t and ")]" not in t:
			t = t.replace("]", "]").replace("[()", "[")
		elif "[(" in t and ")]" in t:
			t = t.replace(")]", "]").replace("[(", "")

		for rep in self.resource:
			t = t.replace(rep, self.resource[rep])
		for rep in self.icon:
			t = t.replace(rep, self.icon[rep])

		if "~" in t:
			t = t.replace("~", " ")
		if "+" in t:
			t = t.replace("+", "")
		if "×" in t:
			t = t.replace("×", "")
		if "," in t:
			t = t.replace(",", "")

		if "ALARM" in t:
			t = t.replace("ALARM", "")
		elif "Alarm" in t:
			t = t.replace("Alarm", "")

		if p:
			t = t.split()
		elif "[counter] backup" in a.lower():
			t = t.split("[")[0].split()
		elif ("get \"" in t or "gets \"" in t) and t.count("[") == 1:
			if "get \" ENCORE [" in t or "gets \" ENCORE [" in t:
				t = t.split("[")[0].split()
			elif self.pay(a):
				t = t.split("]")[1].split()
			else:
				t = t.split("[")[0].split()
		elif t.count("]") == 1:
			if t.startswith(" "):
				t = t[1:]
			if t.startswith("[") or t.startswith(" ["):
				t = t.split("]")[1].split()
			elif t.startswith("\" ENCORE ["):
				t = t.split("]")[1].split()
			elif any(t.lower().startswith(rr) for rr in self.abstart):
				t = t.split("]")[1].split()
			elif t.count("[") == 0:
				if "the following ability for the turn. \"" in t or "the following ability. \"" in t or "get \"" in t or "gets \"" in t or "the following ability until end of turn. \"" in t or "and the following ability. \"" in t or "effects. \"" in t or "perform it. \"" in t or "power and \"" in t or "the following ability until the end of your opponent's next turn. \"" in t:
					if t.count("]") == 1 and t.index("]") < 10:
						t = t.split("]")[1].split()
					else:
						t = t.split("]")[0].split()
				elif "gets the following 2 abilities" in t or "the following 3 abilities" in t:
					t = t.split("gets the following")[0].split()
				else:
					t = t.split("]")[1].split()
			else:
				if any(sk.lower() in t.lower() for sk in self.skill_name):
					for sk in self.skill_name:
						if sk.lower() in t.lower():
							t = t.replace(sk, sk.replace("]", "")).split("]")[0].split()
							break
				elif "this cannot be played" in t.lower() and "resonate [" in t.lower():
					t = t.split("]")[1].split()
				else:
					t = t.split("]")[0].split()
		elif t.count("]") < 1:
			t = t.split("]")[0].split()
		else:
			t = t.split()

		for s in t:
			if self.is_number(s):
				if "." in s:
					s = s[:-1]
				n.append(int(s))

		if num:
			return len(n)

		if len(n) < 1:
			n = [0]
			i = 0

		if num:
			return len(n)
		return n[i]

	def trait(self, a="", i=0):
		if a.count("«") >= 1:
			t = []
			for nx in range(a.count("«")):
				t.append(a.split("«")[nx + 1].split("»")[0])

			if len(t) < 1:
				t = ""
			else:
				try:
					t = t[i]
				except IndexError:
					if i > 1:
						t = t[i - 1]
					else:
						t = t[0]

		else:
			t = self.text(a=a, c=False)
			if any(f"{colour} characters" in t for colour in self.colour):
				for colour in self.colour:
					if f"{colour} characters" in t:
						t = f"{colour}_colour"
		return t

	def colour_t(self, a="", i=0, p=False):
		if not p:
			t = self.text(a=a, c=False)
		else:
			t = a.lower()

		t = [_ for _ in self.colour if f" {_} " in t or f"non-{_}" in t or f" or {_}" in t]
		if len(t) < 1:
			t = ""
		else:
			t = f"{t[i][0].upper()}{t[i][1:]}"
		return t

	def name(self, a="", i=0, s="", n="", p=False):
		if n:
			n = "'"
		else:
			n = "\""
		t = a
		if len(s) == 2:
			t = self.text(a)
		if "b" in s:
			t = a.split("]")[1].split("[")[0]
			if t.endswith(" "):
				t = t[:-1]
			if len(t.split(n)) == 5:
				t = t[t.index(n) + 1:-1]
			else:
				try:
					t = t.split(n)[1]
				except IndexError:
					t = t.split(n)[0]
		elif "s" in s:
			t = []
			for se in self.set_only:
				if se in a:
					t.append(self.set_only[se])
			if len(t) <= 0:
				i = 0
				t = [""]
			elif len(t) < 1:
				i = 0
			return t[i]
		elif "ay" in s:
			ba = "at the beginning of your encore step"
			bc = ""
			if ba in a.lower():
				if ". (" in a.lower():
					bc = a[a.lower().index(ba) + len(ba):a.lower().index('. (') + 1]
				else:
					bc = a[a.lower().index(ba) + len(ba):]
			t = f"[AUTO] At the beginning of your encore step{bc}"
		elif "ac" in s:
			ba = "at the start of encore step"
			bb = "at the beginning of the encore step"
			bc = ""
			if ba in a.lower():
				if ". (" in a.lower():
					bc = a[a.lower().index(ba) + len(ba):a.lower().index('. (') + 1]
				else:
					bc = a[a.lower().index(ba) + len(ba):]
			elif bb in a.lower():
				if ". (" in a.lower():
					bc = a[a.lower().index(bb) + len(bb):a.lower().index('. (') + 1]
				else:
					bc = a[a.lower().index(bb) + len(bb):]
			t = f"[AUTO] At the beginning of the encore step{bc}"
		elif "at" in s:
			ba = "at the beginning of your next"
			bb = "at the start of your next"
			bc = ""
			if ba in a.lower():
				if ". (" in a.lower():
					bc = a[a.lower().index(ba) + len(ba):a.lower().index('. (') + 1]
				else:
					bc = a[a.lower().index(ba) + len(ba):]
			elif bb in a.lower():
				if ". (" in a.lower():
					bc = a[a.lower().index(bb) + len(bb):a.lower().index('. (') + 1]
				else:
					bc = a[a.lower().index(bb) + len(bb):]

			t = f"[AUTO] At the beginning of your{bc}"
		elif "ae" in s:
			ba = "at the end of your"
			bc = ""
			if ba in a.lower():
				if ". (" in a.lower():
					bc = a[a.lower().index(ba) + len(ba):a.lower().index('. (') + 1]
				else:
					bc = a[a.lower().index(ba) + len(ba):]

			t = f"[AUTO] At the end of your{bc}"
		elif "an" in s:
			ba = "at the next end of your opponent's"
			bb = "at the end of your opponent's next turn"
			bc = ""
			opp = False
			if ba in a.lower():
				if "opponent" in ba:
					opp = True
				if ". (" in a.lower():
					bc = a[a.lower().index(ba) + len(ba):a.lower().index('. (') + 1]
				else:
					bc = a[a.lower().index(ba) + len(ba):]
			elif bb in a.lower():
				if "opponent" in bb:
					opp = True
				if ". (" in a.lower():
					bc = a[a.lower().index(bb) + len(bb):a.lower().index('. (') + 1]
				else:
					bc = a[a.lower().index(bb) + len(bb):]

			if opp:
				t = f"[AUTO] At the end of your opponent's{bc}"
			else:
				t = f"[AUTO] At the end of your{bc}"
		elif "a" in s:
			c = a.count(n)
			if c == 2:
				t = a.split(n)[1]
			elif c > 2:
				t1 = a.split(n)
				t = [p for p in t1 if any(p.startswith(abl) for abl in self.ability[:3]) and f"\"{p}\"" in a]
				if len(t) < 1:
					t = ""
				else:
					if t[i].endswith("hoose a "):
						t2 = t1.index(t[i])
						t = f"{t1[t2]}\"{t1[t2 + 1]}\"{t1[t2 + 2]}"
					else:
						t = t[i]

			if t.count("'") >= 2:
				t = t.replace(" '", " \"").replace("' ", "\" ")

			if "(" in t and ")" in a and "encore" not in t.lower():
				if "[(" in t and (")]" in t or (")" in t and "]" in t) and ")]" not in t) and t.count("(") == 1:
					pass
				else:
					t = t.split("(")[0]
		elif "p" in s:
			k = False
			c = a.count(n)

			if c >= 2:

				t = a.split(n)
				t = [p for p in t if f"\"{p}\"" in a]
				if "resonance [" in a.lower():
					t = t[2:]
				for p in range(len(t)):
					if "'s " in t[p] or "'ll " in t[p]:
						k = True
						t[p] = t[p].replace("'s ", "?s ").replace("'ll ", "?ll ")
					t[p] = t[p].replace("'", "\"")
					if k:
						k = False
						t[p] = t[p].replace("?s ", "'s ").replace("?ll ", "'ll ")

				if len(t) < 1:
					t = ""
				else:
					t = t[i]
			elif c == 2:
				t = a.split(n)[1]
		elif "n" in s:
			if not p and (a.startswith("[ACT] [") or a.startswith("[AUTO] [")):
				a = "]".join(a.split("]")[2:])
			elif not p and a.startswith("[CONT]"):
				a = "]".join(a.split("]")[1:])
			c = a.count(n)
			if c == 2:
				t = a.split(n)[1]
			elif c > 2:
				t = a.split(n)
				t = [s for s in t if f"\"{s}\"" in a]

				if len(t) < 1:
					t = ""
				else:
					t = t[i]

			if "(" in t and ")" in a:
				t = t.split("(")
				if t[1][-1] == ")":
					t[1] = t[1][:-1]
				if t[0][-1] == " ":
					t[0] = t[0][:-1]
				if all(al.lower() in self.alpha + self.digits for al in t[1]):
					t = f"{t[0]} ({t[1]})"
				else:
					t = t[0]

		else:
			t = a.split(n)[i]
			if "(" in t and ")" in a:
				t = t.split("(")[0]

		return t

	def a_replace(self, a=""):
		if ")»" in a:
			for ss in self.set_only:
				a = a.replace(f"{ss}", f"{self.set_only[ss]}")

		a = a.lower()

		if " (" in a:
			if ")»" in a or ")\"":
				pass
			else:
				a = a.split(" (")[0]

		for rep in self.resource:
			if rep in a:
				a = a.replace(rep, self.resource[rep])
		for rep in self.text_change:
			if rep in a:
				a = a.replace(rep, self.text_change[rep])
		if "{" in a or "}" in a:
			a = a.replace("{", "(").replace("}", ")")

		return a

	def text(self, a="", i=1, lower=True, c=True):
		t = a
		if t.count("[") >= 2:
			for item in self.status:
				t = t.replace(item, self.status[item])
			for item in self.skip_text:
				t = t.replace(item, self.skip_text[item])
			for icn in self.icon:
				if icn in t:
					t = t.replace(icn, self.icon[icn])
		for item in self.status:
			t = t.replace(item, self.status[item])
		for ablt in self.ability:
			if t.startswith(ablt) or t.startswith(ablt.lower()):
				t = t.replace(ablt, "")
			if t.startswith(" "):
				t = t[1:]
		for ss in self.set_only:
			if f"{ss} " in t:
				t = t.replace(f"{ss} ", "")
			else:
				t = t.replace(ss, self.set_only[ss])

		if "[ACT]" in t:
			t = t.replace("[ACT]", "ACT")

		if t.startswith(" "):
			t = t[1:]

		if " (" in t and ")\"" not in t and t.count(" (") >= 2:
			t = t.split(" (")[0]
		elif " (" in t and ")\"" in t and t.count(" (") == 1:
			pass

		if lower:
			t = t.lower()
		else:
			t = t

		if " (you may " in t:
			t = t.split(" (you may ")[0]

		for rep in self.resource:
			t = t.replace(rep, self.resource[rep])

		if "{" in t or "}" in t:
			t = t.replace("{", "(").replace("}", ")")

		if 'get "[' in t:
			t = t[:t.index('get "[') + 6]

		if "bond/" in a.lower():
			t = t.split("[")[0].split("]")[0]
		elif any(t.startswith(rr) for rr in self.abstart):
			t = t.split("]")[i]
		elif t.startswith("["):
			t = t.split("]")[i]
		else:
			t = t

		if t.endswith("\"[cont"):
			t = t[:-len("\"[cont")]
		if t.count("«") >= 1:
			trait = []
			for nx in range(t.count("«")):
				trait.append(t.split("«")[nx + 1].split("»")[0])
			for tr in trait:
				t = t.replace(tr, "")
			if "«fe»" in t and all(any(_ in tr for tr in trait) for _ in ("female", "male")):
				t = t.replace("«fe»", "«»")
			t = t.replace("«", "").replace("»", "")

		if t.count('"') > 0 and t.count('"') % 2 == 0:
			if not t.startswith("brainstorm"):
				name = []
				for nx in range(t.count('"') // 2):
					name.append(t.split('"')[nx + 1 + nx])
				for nm in name:
					t = t.replace(f"\"{nm}\"", "")

		elif t.count('"') == 3:
			name = a.split('"')[1]  
			t = t.replace(f"\"{name.lower()}\"", "")

		t = t.translate(str.maketrans('', '', self.digits))

		if c:
			for colour in self.colour:
				if f" {colour} " in t:
					t = t.replace(f" {colour} ", "  ")
				elif f" non-{colour} " in t:
					t = t.replace(f" non-{colour} ", "  ")
				elif f" or {colour}" in t:
					t = t.replace(f" or {colour}", " or ")
		if t.startswith(" "):
			t = t[1:]

		return t

	def seperate(self, tt, a, t, aa, rev=False, d=False):
		if rev:
			c = self.convert(a, t.split(tt)[0], aa)
			tc = "at the start of your next"
			if tc in t and t.index(tc) < t.index(tt):
				t = ""
			else:
				t = tt + t.split(tt)[1]
		else:
			if d:
				c = ["done", self.convert(a, tt + t.split(tt)[1], aa)]
			else:
				c = ["do", self.convert(a, tt + t.split(tt)[1], aa)]
			t = t.split(tt)[0]
		return c, t

	@staticmethod
	def is_number(s):
		try:
			float(s)
			return True
		except ValueError:
			pass
		try:
			numeric(s)
			return True
		except (TypeError, ValueError):
			pass
		return False

	def discard_card(self, c, a, t, force=False):
		d = []
		if any(_ in t for _ in ("choose  cards from your hand", "choose  cards in your hand", "choose  card in your hand", "discard  card from your hand", "discard  card from hand", "discard  cards from your hand", "choose  cards in your hand", "choose  card from your hand", "discard x cards from your hand", "put  card from your hand")) and any(_ in t for _ in ("hand to the waiting room", "put it in your waiting room", "discard it to the waiting room", "put them in your waiting room", "from your hand to the waiting room", "from your hand in your waiting room")):
			if "discard x cards from your hand" in t:
				d = ["do", ["discard", "x", ""]]
			else:
				if "if" not in c and not force:
					if "upto" in c:
						d.extend(["if", 1])
					else:
						if "drawupto" in c:
							d.extend(["if", c[1]])
						else:
							d.extend(["if", c[0]])
				d.extend(["do", ["discard", self.digit(a, self.cond[0]), ""]])
				self.cond[0] += 1
		elif "put  cards from your hand on top of your deck" in t or ("choose  card from your hand" in t and "put that card on top of your deck" in t):
			d = ["do", ["discard", self.digit(a, self.cond[0]), "", "Library", "top"]]
			self.cond[0] += 1
		elif "choose  card in your hand" in t and "put it in clock" in t:
			d = ["do", ["discard", self.digit(a, self.cond[0]), "", "Clock"]]
			self.cond[0] += 1
		if "do" in c:
			c[c.index("do") + 1].extend(d)
		else:
			c.extend(d)
		return c

	def isnot_filter(self, t, otherwise=False):
		for tt in self.isnot_text:
			if not otherwise and "otherwise" in tt:
				continue
			if tt in t:
				self.tt = tt
				self.isnot = t.split(tt)[1]
				t = t.split(tt)[0]
				break
		return t

	def donot_filter(self, t):
		for tt in self.donot_text:
			if tt in t:
				self.dd = tt
				self.donot = t.split(tt)[1]
				t = t.split(tt)[0]
				break
		return t

	def add_notisdo(self, cv, isdo, a, t, aa, index=None):
		nn = ""
		inx = 0
		if self.tt:
			nn = self.tt
		elif self.dd:
			nn = self.dd
		elif self.multicond:
			nn = self.multicond[0]
			inx = self.multicond[1]
			if len(self.multicond) > 2:
				index = self.multicond[2]
		self.cond = [0, 0, 0, 0, 0, 0]

		a = a[[i.start() for i in finditer(nn, a.lower())][inx]:]
		aa = aa.split(nn)[inx]
		if index is not None:
			inx = index
		t = t.split(nn)[inx]
		if "dont" in isdo:
			cv.extend(["dont", self.convert(a, t, aa)])
			self.dd = ""
		elif "isnot" in isdo:
			cv.extend(["isnot", self.convert(a, self.isnot, aa)])
			self.tt = ""
		elif "if th" in isdo:
			self.multicond = ["", 0]
			cv.extend(["multicond", self.effect(a, f"if th{t}", aa)])
		return cv
