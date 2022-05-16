from unicodedata import numeric

from core.markreplace import markreplace


# noinspection SpellCheckingInspection
class Ability:
	ablt = 0
	target = ""
	cx = False
	center = False
	cond = [0, 0, 0]
	ee = False
	start = False
	resource = {"library": "deck", "gain": "get", "hoose a ": "hoose 1 ", "a card": "1 card", "is equal to": "=",
	            "all of your": "all your", "discard an": "put 1", "discard a ": "put 1 ", "put a ": "put 1 ", "put an ": "put 1 ",
	            "or a ": "or 1 ", "this card": "this", "three cards": "3 cards", "two cards": "2 cards",
	            " four ": " 4 ", " five ": " 5 ", " six ": " 6 ", " seven ": " 7 ", "into your": "in your",
	            " one ": " 1 ", " two ": " 2 ", "reversed": "reverse", "climax zone": "climax area",
	            "three": "3", "facing": "opposite", " 2 soul": " soulsoul", " 2 Soul": " soulsoul",
	            "foe or 1 new": "foe or a new", "the 2 of us": "the two of us", "libraries": "decks",
	            "times per turn": "time per turn", "when 1 card named": "when a card named", "frontal": "front",
	            "When 1 card named": "When a card named", "not an": "not a", "for an": "for 1", "if a climax is put": "if 1 climax is put",
	            "if 1 card": "if a card", "If 1 card": "If a card", "back row": "back stage", "level-up": "level up",
	            "front row slots on stage": "position on your center stage", "front row": "center stage","twice":"2 times"}
	text_change = {"new route of 2 days and 3 nights":"new route of two days and three nights"}
	icon = {"[SHOT]": "SHOT", "[BOUNCE]": "BOUNCE", "[POOL]": "POOL", "[SOUL]": "SOUL", "[TREASURE]": "TREASURE", "[DOOR]": "DOOR", "[STANDBY]": "STANDBY", "[DRAW]": "DRAW", "[GATE]": "GATE", "[STOCK]": "STOCK"}
	colour = ("red", "blue", "yellow", "green")
	ability = ("[CONT]", "[AUTO]", "[ACT]", "[CLOCK]", "[COUNTER]", "[CXCOMBO]")
	status = {"[REST]": "REST", "[STAND]": "STAND", "[REVERSE]": "REVERSE"}
	skip_text = {"[Deploy]": "Deploy"}
	stage = ("Center", "Back")
	abstart = ("change [", "accelerate [", "resonate [", "resonance [", "cx combo [", "memory [", "recollection [", "brainstorm [", "experience [")
	attack = ("Attack", "Declaration", "Trigger", "Counter", "Damage", "Battle")
	alpha = "qwertyuiopasdfghjklzxcvbnm"
	digits = "0123456789"
	text_name = {"Assist": "] Assist", "Memory": "] Memory_] Recollection", "Experience": "] Experience",
	             "Accelerator": "] Accelerator", "Change": "] Change",
	             "[AUTO] Encore [Put the top card of your deck into your clock]": "[AUTO] Encore [Put the top card of your deck into your clock]",
	             "[AUTO] Encore [Put 1 character from your hand into your waiting room]": "[AUTO] Encore [Put 1 character from your hand into your waiting room]_[AUTO] Encore [Put a character from your hand into your waiting room]",
	             "[AUTO] Encore [Put a character from your hand into your waiting room]": "[AUTO] Encore [Put 1 character from your hand into your waiting room]_[AUTO] Encore [Put a character from your hand into your waiting room]"}
	remove_text = ["Encore [Put 1 character from your hand in your waiting room]", "Encore [Put a character from your hand into your waiting room]", "Encore [Put the top card of your deck into your clock]"]
	set_only = markreplace["set_only"]
	skill_name = ("[Deploy]","[Cascade]")
	dont_text = ["if not","if you do not"]

	def pay(self, a=""):
		t = str(a)

		for item in self.status:
			t = t.replace(item, self.status[item])
		for item1 in self.remove_text:
			t = t.replace(item1, "")
		t = t.lower()
		for rep in self.resource:
			t = t.replace(rep, self.resource[rep])

		# print("pay text\t", t)
		if " (" in t:
			t = t.split(" (")[0]

		s = []
		o = []
		r = []
		if "[(6)" in t:
			s = ["Stock", 6]
		elif "[(5)" in t:
			s = ["Stock", 5]
		elif "[(4)" in t:
			s = ["Stock", 4]
		elif "[(3)" in t:
			s = ["Stock", 3]
		elif "[(2)" in t:
			s = ["Stock", 2]
		elif "[(1)" in t:
			s = ["Stock", 1]

		if "[reveal a \"" in t:
			if "\" in your hand and put it in your stock]" in t:
				o = ["RevealStock", self.name(a, s='n',p=True)]
			elif "\" from your hand]" in t or "\" in your hand]" in t:
				o = ["Reveal", self.name(a, s='n',p=True)]
		elif "[reveal any number of \"" in t and ("\" from your hand]" in t or "\" in your hand]" in t):
			o = ["Reveal", self.name(a, s='n',p=True), "any"]
		elif "put this stand card in your memory]" in t:
			o = ["Memory", 0]
		elif "put this in your memory]" in t or "send this to memory]" in t:
			o = ["Memory", 0]
		elif "put 1 \"" in t and ("\" from your hand to the waiting room]" in t or "\" from your hand in your waiting room]" in t or "\" from hand to the waiting room]"):
			if "\" or \"" in t.split("waiting room]")[0]:
				o = ["Discard", 1, "Name=", f"{self.name(a, s='n', p=True)}_{self.name(a,2, s='n', p=True)}"]
			else:
				o = ["Discard", 1, "Name=", self.name(a, s='n',p=True)]
		elif "put 1 \"" in t and ("from your memory to your waiting room]" in t or "from your memory to the waiting room]" in t):
			o = ["MDiscard", 1, "MName=", self.name(a, s='n',p=True)]
		elif "put 1 \"" in t and ("from your climax area in your waiting room]" in t or "from your climax area to the waiting room]" in t):
			if "\" from your hand in your waiting room &" in t:
				o = ["CXDiscard", 1, "CXName=", self.name(a, 2, s='n',p=True)]
			else:
				o = ["CXDiscard", 1, "CXName=", self.name(a, s='n',p=True)]
		elif "put 1 climax from your hand in your waiting room]" in t or "put 1 climax card from hand to the waiting room]" in t or "put 1 climax card from your hand to the waiting room]" in t:
			o = ["Discard", 1, "Climax"]
		elif "put 1 character from your hand in your waiting room]" in t or "put 1 character card from your hand to the waiting room]" in t:
			o = ["Discard", 1, "Character"]
		elif "put this from your hand in your waiting room]" in t or "discard this from your hand to the waiting room]" in t or "discard this from hand to the waiting room]" in t:
			o = ["Discard", 0, ""]
		elif "put 1 random card from your hand in your waiting room]" in t:
			o = ["Discard", -10, ""]
		elif "put 1 character card from hand in memory]" in t:
			o = ["HMemory", 1, "Character"]
		elif "put 1 card from your hand in clock]" in t or "put 1 card from your hand in your clock]" in t:
			o = ["ClockH", 1]
		elif "put 1 of your characters in the waiting room]" in t:
			o = ["Waiting", 1]
		elif "put 1 of your other characters from the stage in the waiting room]" in t:
			o = ["Waiting", 1, "WOther"]
		elif "put the top card of your deck in your clock]" in t or "put 1 card from the top of your deck in your clock]" in t:
			o = ["ClockL", 1]
		elif "put this in the waiting room]" in t or "put this in your waiting room]" in t or "put this in waiting room]" in t:
			o = ["Waiting", 0]
		elif "discard 3 cards from your hand to the waiting room]" in t:
			o = ["Discard", 3, ""]
		elif "put 2 cards from your hand in your waiting room]" in t or "discard 2 cards from hand to the waiting room]" in t:
			o = ["Discard", 2, ""]
		elif "discard 1 card from your hand to the waiting room]" in t or "put 1 card from your hand in your waiting room]" in t or "discard 1 card from hand to the waiting room]" in t:
			o = ["Discard", 1, ""]
		elif "return this to your hand]" in t:
			o = ["Hander", 0, ""]
		elif "return 2 characters from your waiting room to your deck. shuffle your deck afterwards]" in t or "return 2 characters in your waiting room to your deck. shuffle your deck afterwards]" in t or "return 2 characters from your waiting room in your deck & shuffle your deck]" in t:
			o = ["WDecker", 2, "Character"]
		elif "put this in your clock]" in t:
			o = ["ClockS", 0]
		elif "put 2 markers from under this in your waiting room]" in t:
			o = ["Marker", 2]
		elif "put 1 marker from under this in the waiting room]" in t:
			o = ["Marker", 1]
		elif "put 1 character with \"" in t and "\" in its card name from your stage in your clock]" in t:
			o = ["ClockS", 1, "Name", self.name(a, s="n",p=True)]
		elif "put 1 card named \"" in t and "\" from your hand in your waiting room]" in t:
			o = ["Discard", 1, "Name=", self.name(a, s="n",p=True)]
		elif "of your standing characters]" in t or "of your stand characters]" in t:
			if "[rest 1" in t or "[rest one" in t or "& rest 1" in t:
				o = ["Rest", 1, ""]
			elif "[rest 2" in t:
				o = ["Rest", 2, ""]
		elif "rest 1 of your characters with assist]" in t:
			o = ["Rest", 1, "Text", "Assist"]
		elif "rest 1 of your characters]" in t:
			o = ["Rest", 1, ""]
		elif "rest this]" in t:
			o = ["Rest", 0, ""]
		elif "rest 2 of your other characters]" in t:
			o = ["Rest", 2, "Other"]
		elif "rest 2 of your characters]" in t:
			o = ["Rest", 2, ""]
		elif "rest 1 of your characters with \"" in t and "\" in name]" in t:
			o = ["Rest", 1, "Name", self.name(a, s="n",p=True)]
		elif "«" in t:
			t1 = str(a)
			for item in self.status:
				t1 = t1.replace(item, self.status[item])
			t1 = t1.replace("[ACT] ", "").replace("[AUTO]", "").replace("[CXCOMBO]", "").split("]")[0]

			trait = []
			for nx in range(t1.count("«")):
				trait.append(t1.split("«")[nx + 1].split("»")[0])
			for tra in trait:
				t1 = t1.replace(tra, "").replace("«", "").replace("»", "")

			for rep in self.resource:
				if rep in t1:
					t1 = t1.replace(rep, self.resource[rep])
			# print("pay text1\t", t1.lower())

			if "rest 1 of your  characters and 1 of your  characters" in t1.lower():
				o = ["Rest", 2, "BTrait", f"{trait[0]}_{trait[1]}"]
			elif "rest 1 of your  characters" in t1.lower():
				o = ["Rest", 1, "Trait", trait[0]]
			elif "rest 2 of your  characters" in t1.lower():
				o = ["Rest", 2, "Trait", trait[0]]
			elif "rest 1 of your other  characters" in t1.lower() or "rest 1 of your other stand  characters" in t1.lower():
				o = ["Rest", 1, "Trait", trait[0], "Other"]
			elif "put a  character from your hand in your waiting room" in t1.lower() or "discard a  character card from your hand to the waiting room" in t1.lower() or "discard a  character from hand to the waiting room" in t1.lower() or "put 1  character from your hand in your waiting room" in t1.lower():
				o = ["Discard", 1, "Trait", trait[0]]
			elif "put 2  characters from your hand in your waiting room" in t1.lower():
				o = ["Discard", 2, "Trait", trait[0]]
			elif "put 3  characters from your hand in your waiting room" in t1.lower():
				o = ["Discard", 3, "Trait", trait[0]]
			elif "put a  character card from your hand in clock" in t1.lower() in t1.lower():
				o = ["ClockH", 1, "Trait", trait[0]]
			elif "put 1  or  character on your stage in your clock" in t1.lower():
				o = ["ClockS", 1, "Trait", f"{trait[0]}_{trait[1]}"]
			elif "put a  character from your stage in your clock" in t1.lower():
				o = ["ClockS", 1, "Trait", trait[0]]
			elif "put a  character from your stage in your waiting room" in t1.lower():
				o = ["Waiting", 1, "Trait", trait[0]]
			elif "put a  character from your memory in your waiting room" in t1.lower():
				o = ["MDiscard", 1, "MTrait", trait[0]]

		if "reveal a \"" in t and "from your hand &" in t:
			r = ["Reveal", self.name(a, s='n',p=True)]
		elif "put the top card of your deck in your clock &" in t or "put the top card of your deck in your clock," in t:
			r = ["ClockL", 1]
		elif "put 2 cards from your hand in your waiting room &" in t or "discard 2 cards from hand to the waiting room &" in t:
			r = ["Discard", 2, ""]
		elif "put 1 card from your hand in your waiting room &" in t or "discard 1 card from your hand to the waiting room &" in t or "discard 1 card from your hand to waiting room &" in t or "discard 1 card from hand to the waiting room &" in t or "put 1 card from your hand to your waiting room &" in t:
			r = ["Discard", 1, ""]
		elif "put 1 climax from your hand in your waiting room &" in t:
			r = ["Discard", 1, "Climax"]
		elif "put 1 card from your hand in your clock &" in t:
			r = ["ClockH", 1, ""]
		elif "put 1 character with \"" in t and "\" in its card name from your stage in your clock &" in t:
			r = ["ClockS", 1, "Name", self.name(a, s="n",p=True)]
		elif "put 1 \"" in t and "\" from your hand in your waiting room &" in t:
			r = ["Discard", 1, "Name=", self.name(a, s="n",p=True)]
		elif "put 1 «" in t and "» character from your hand in your waiting room &" in t:
			r = ["Discard", 1, "Trait", self.trait(a)]
		elif "rest 2 of your characters &" in t:
			r = ["Rest", 2, ""]
		elif "rest 1 of your characters &" in t:
			r = ["Rest", 1, ""]

		return s + r + o

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
		if ss is None:
			ss = []
		t = str(a)
		for item in self.status:
			t = t.replace(item, self.status[item])
		for item1 in self.remove_text:
			t = t.replace(item1, "")
		t = t.lower()
		for rep in self.resource:
			t = t.replace(rep, self.resource[rep])

		if "[auto] encore [(3)]" in t or "[auto] encore" in t:
			t = t.replace("[auto] encore [(3)]", "").replace("[auto] encore", "")

		# print("req text\t", t)
		rs = True
		rr = False
		ro = False

		if "[(6)" in t and x < 6:
			rs = False
		elif "[(5)" in t and x < 5:
			rs = False
		elif "[(4)" in t and x < 4:
			rs = False
		elif "[(3)" in t and x < 3:
			rs = False
		elif "[(2)" in t and x < 2:
			rs = False
		elif "[(1)" in t and x < 1:
			rs = False

		if "[reveal a \"" in t:
			if "\" from your hand]" in t or "\" in your hand]" in t or "\" in your hand and put it in your stock]" in t:
				if len(h) >= 1 and any(self.name(a, s='n',p=True) in hn[1] for hn in h):
					ro = True
		elif "[reveal any number of \"" in t and ("\" from your hand]" in t or "\" in your hand]" in t):
			if len(h) >= 0:
				ro = True
		elif "put this stand card in your memory]" in t:
			if ss[nn][0] == "Stand":
				ro = True
		elif "put this in your memory]" in t or "send this to memory]" in t:
			ro = True
		elif "put this from your hand in your waiting room]" in t or "discard this from your hand to the waiting room]" in t or "discard this from hand to the waiting room]" in t:
			ro = True
		elif "put 1 card from your hand in clock]" in t or "put 1 card from your hand in your clock" in t:
			if len(h) >= 1:
				ro = True
		elif "put 1 \"" in t and ("\" from your hand to the waiting room]" in t or "\" from your hand in your waiting room]" in t or "\" from hand to the waiting room]"):
			if "\" or \"" in t.split("waiting room]")[0]:
				if len(h) >= 1 and any(self.name(a, s='n', p=True) in hn[1] or self.name(a,2, s='n', p=True) in hn[1] for hn in h):
					ro = True
			else:
				if len(h) >= 1 and any(self.name(a, s='n',p=True) in hn[1] for hn in h):
					ro = True
		elif "put 1 \"" in t and ("\" from your memory to your waiting room]" in t or "\" from your memory to the waiting room]" in t):
			if len(my) >= 1 and any(self.name(a, s='n',p=True) in hn[1] for hn in my):
				ro = True
		elif "put 1 \"" in t and ("from your climax area in your waiting room]" in t or "from your climax area to the waiting room]" in t):
			if "\" from your hand in your waiting room &" in t:
				if len(cx) >= 1 and any(self.name(a, 2, s='n',p=True) in hn[1] for hn in cx):
					ro = True
			else:
				if len(cx) >= 1 and any(self.name(a, s='n',p=True) in hn[1] for hn in cx):
					ro = True
		elif "discard 3 cards from your hand to the waiting room]" in t:
			if len(h) >= 3:
				ro = True
		elif "discard 2 cards from your hand to the waiting room]" in t or "put 2 cards from your hand in your waiting room]" in t or "discard 2 cards from hand to the waiting room]" in t:
			if len(h) >= 2:
				ro = True
		elif "discard 1 card from your hand to the waiting room]" in t or "put 1 card from your hand in your waiting room]" in t or "discard 1 card from hand to the waiting room]" in t:
			if len(h) >= 1:
				ro = True
		elif "discard a character card from your hand to the waiting room]" in t or "put 1 character from your hand in your waiting room]" in t:
			if len([p for p in h if p[0] == "Character"]) >= 1:
				ro = True
		elif "put 1 character card from hand in memory]" in t:
			if len([p for p in h if p[0] == "Character"]) >= 1:
				ro = True
		elif "put this in your memory]" in t:
			ro = True
		elif "put 1 of your characters in the waiting room]" in t:
			if len([sx for sx in ss if sx[0] != ""]) > 0:
				ro = True
		elif "put 1 of your other characters from the stage in the waiting room]" in t:
			if len([sx for sx in ss if sx[0] != ""]) > 1:
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
		elif "put 1 climax from your hand in your waiting room]" in t or "put 1 climax card from hand to the waiting room]" in t or "put 1 climax card from your hand to the waiting room]" in t:
			if len([p for p in h if p[0] == "Climax"]) >= 1:
				ro = True
		elif "rest 1 of your characters with assist]" in t:
			if len([sx for sx in ss if sx[0] == "Stand" and sx[3]]) >= 1:
				ro = True
		elif "rest 1 of your standing characters]" in t or "rest 1 of your stand characters]" in t or "rest 1 of your characters]" in t:
			if len([sx for sx in ss if sx[0] == "Stand"]) >= 1:
				ro = True
		elif "rest 2 of your standing characters]" in t or "rest 2 of your stand characters]" in t or "rest 2 of your characters]" in t:
			if len([sx for sx in ss if sx[0] == "Stand"]) >= 2:
				ro = True
		elif "rest 2 of your other characters]" in t:
			if len([sx for sx in ss if sx[0] == "Stand"]) >= 3:
				ro = True
		elif "rest this]" in t:
			if ss[nn][0] == "Stand":
				ro = True
		elif "put the top card of your deck in your clock]" in t or "put 1 card from the top of your deck in your clock]" in t:
			ro = True
		elif "put 1 character with \"" in t and "\" in its card name from your stage in your clock]" in t:
			if len([sx for sx in ss if sx[0] != "" and self.name(a, s='n',p=True) in sx[1]]) >= 1:
				ro = True
		elif "put 1 card named \"" in t and "\" from your hand in your waiting room]" in t:
			if len(h) >= 1 and any(self.name(a, s='n',p=True) in hn[1] for hn in h):
				ro = True
		elif "rest 1 of your characters with \"" in t and "\" in name]" in t:
			if any(self.name(a, s="n") in sx[1] for sx in ss) and len([sx for sx in ss if sx[0] == "Stand"]) >= 1:
				ro = True
		elif "put 2 markers from under this in your waiting room]" in t:
			if m >= 2:
				ro = True
		elif "put 1 marker from under this in the waiting room]" in t:
			if m >= 1:
				ro = True
		elif "return 2 characters from your waiting room to your deck. shuffle your deck afterwards]" in t or "return 2 characters in your waiting room to your deck. shuffle your deck afterwards]" in t or "return 2 characters from your waiting room in your deck & shuffle your deck]" in t:
			if len([sx for sx in wr if sx[0] == "Character"]) >= 2:
				ro = True
		elif "«" in t and t.count("[") >= 2:
			t1 = str(a)
			for item in self.status:
				t1 = t1.replace(item, self.status[item])
			t1 = t1.replace("[ACT] ", "").replace("[AUTO]", "").replace("[CXCOMBO]", "").split("]")[0]

			trait = []
			for nx in range(t1.count("«")):
				trait.append(t1.split("«")[nx + 1].split("»")[0])
			for tra in trait:
				t1 = t1.replace(tra, "").replace("«", "").replace("»", "")

			for rep in self.resource:
				t1 = t1.replace(rep, self.resource[rep])
			# print(t1)
			if "rest 1 of your  characters and 1 of your  characters" in t1.lower():
				sn = {"0": [sx for sx in ss if sx[0] == "Stand" and any(tx in sx[2] for tx in trait)], "1": [], "2": []}
				for sx in sn["0"]:
					if trait[0] in sx[2]:
						sn["1"].append(sx)
					if trait[1] in sx[2]:
						sn["2"].append(sx)
				if len(sn["1"]) >= 1 and len(sn["2"]) >= 1 and len(sn["0"]) >= 2:
					ro = True
			elif "rest 1 of your  characters" in t1.lower():
				if len([sx for sx in ss if sx[0] == "Stand" and any(tx in sx[2] for tx in trait)]) >= 1:
					ro = True
			elif "rest 2 of your  characters" in t1.lower():
				if len([sx for sx in ss if sx[0] == "Stand" and any(tx in sx[2] for tx in trait)]) >= 2:
					ro = True
			elif "rest 1 of your other  characters" in t1.lower() or "[rest 1 of your other stand  characters" in t1.lower():
				if len([sx for sx in ss if sx != ss[nn] and sx[0] == "Stand" and any(tx in sx[2] for tx in trait)]) >= 1:
					ro = True
			elif "put a  character from your hand in your waiting room" in t1.lower() or "discard a  character card from your hand to the waiting room" in t1.lower() or "discard a  character from hand to the waiting room" in t1.lower() or "put 1  character from your hand in your waiting room" in t1.lower():
				if len(h) >= 1 and len([p for p in h if any(tx in p[2] for tx in trait)]) >= 1:
					ro = True
			elif "put 2  characters from your hand in your waiting room" in t1.lower():
				if len(h) >= 2 and len([p for p in h if any(tx in p[2] for tx in trait)]) >= 2:
					ro = True
			elif "put 3  characters from your hand in your waiting room" in t1.lower():
				if len(h) >= 3 and len([p for p in h if any(tx in p[2] for tx in trait)]) >= 3:
					ro = True
			elif "put a  character card from your hand in clock" in t1.lower():
				if len(h) >= 1 and len([p for p in h if any(tx in p[2] for tx in trait)]) >= 1:
					ro = True
			elif "put 1  or  character on your stage in your clock" in t1.lower():
				if len([sx for sx in ss if any(tx in sx[2] for tx in trait)]) >= 1:
					ro = True
			elif "put a  character from your stage in your clock" in t1.lower():
				if len([sx for sx in ss if any(tx in sx[2] for tx in trait)]) >= 1:
					ro = True
			elif "put a  character from your stage in your waiting room" in t1.lower():
				if len([sx for sx in ss if any(tx in sx[2] for tx in trait)]) >= 1:
					ro = True
			elif "put a  character from your memory in your waiting room" in t1.lower():
				if len([sx for sx in my if any(tx in sx[2] for tx in trait)]) >= 1:
					ro = True
			elif "[(" in t:
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

		if "reveal a \"" in t and "from your hand &" in t:
			if len(h) >= 1 and any(self.name(a, s='n', p=True) in hn[1] for hn in h):
				rr = True
		elif "put 2 cards from your hand in your waiting room &" in t or "discard 2 cards from hand to the waiting room &" in t:
			if len(h) >= 2:
				rr = True
		elif "put 1 card from your hand in your waiting room &" in t or "discard 1 card from your hand to waiting room &" in t or "put 1 card from your hand to your waiting room &" in t:
			if len(h) >= 1:
				rr = True
		elif "put 1 climax from your hand in your waiting room &" in t:
			if len([p for p in h if p[0] == "Climax"]) >= 1:
				rr = True
		elif "put the top card of your deck in your clock &" in t:
			rr = True
		elif "put 1 card from your hand in your clock &" in t:
			if len(h) >= 1:
				rr = True
		elif "put 1 character with \"" in t and "\" in its card name from your stage in your clock &" in t:
			if len([sx for sx in ss if sx[0] != "" and self.name(a, s='n',p=True) in sx[1]]) >= 1:
				rr = True
		elif "put 1 \"" in t and "\" from your hand in your waiting room &" in t:
			if len([sx for sx in h if sx[0] != "" and self.name(a, s='n',p=True) in sx[1]]) >= 1:
				rr = True
		elif "rest 2 of your characters &" in t:
			if len([sx for sx in ss if sx[0] == "Stand"]) >= 2:
				rr = True
		elif "rest 1 of your characters &" in t:
			if len([sx for sx in ss if sx[0] == "Stand"]) >= 1:
				rr = True
		elif "&" not in t.replace("[act]", "").replace("[auto]", "").split("]")[0]:
			rr = True

		# print(rs, ro, rr)
		if rs and ro and rr:
			return True
		else:
			return False

	def act(self, a=""):
		t = self.text(a)
		aa = self.a_replace(a)

		self.ablt = 0
		self.target = ""
		self.cx = False
		self.center = False
		self.cond = [0, 0, 0]

		if "until the end of your opponent's next turn" in t or "until the next end of your opponent's turn" in t:
			x = 2
		elif "for the turn" in t or "until end of turn" in t:
			x = 1
		else:
			x = 1

		if t.startswith("backup"):
			return [1, self.digit(a), 1, "backup", self.digit(a, 1)]
		elif "choose up to   and  " in t:
			if "from your waiting room" in t:
				if "put them in separate slots on the stage" in t:
					if "those characters get + power and + soul" in t:
						return [self.digit(a), "salvage", f"Name=_{self.name(a, s='n')}", "Stage", "upto", "extra", "do", [self.digit(a, 1), "salvage", f"Name=_{self.name(a, 2, s='n')}", "Stage", "separate", "upto", "extra", "do", [-16, self.digit(a, 2), x, "power", "extra", "do", [-16, self.digit(a, 3), x, "soul"]]]]
		elif "choose   in your clock and put it in any slot on stage" in t:
			if "choose  card in your hand and put it in your clock" in t:
				return ["cdiscard", self.digit(a), f"Name=_{self.name(a, s='n')}", "Stage", "do", ["discard", self.digit(a), "", "Clock"]]
		elif "choose  random opponent's characters" in t:
			if "that character gets - power" in t:
				return [-11, self.digit(a), x, "power", "opp", "random"]
		elif "choose   in your memory" in t:
			if "\" in your memory" in aa:
				if "put it in the stock" in t:
					return ["mdiscard", self.digit(a), f"Name=_{self.name(a, s='n')}", "Stock", "show"]
		elif "choose  level  or lower character in your opponent's center stage" in t or "choose  level  or lower character on your opponent's center stage" in t:
			if "put it on the bottom of the deck" in t:
				if "search your deck for up to  character with the same name as that character and put it in any slot on the stage" in t:
					return [self.digit(a), "decker", "bottom", "Level", f"<={self.digit(a, 1)}", "Opp", "Center", "extra", "do", [self.digit(a, 2), "search", f"EName=", "Stage", "upto"]]
			elif "put it in stock" in t or "put it in your opponent's stock" in t:
				if "search your deck for up to  climax card" in t:
					if "and put it in the waiting room" in t:
						if "if you put  card in the waiting room this way" in t:
							return [self.digit(a), "search", "Climax", "Waiting", "if", "do", [self.digit(a, 2), "stocker", "Level", f"<={self.digit(a, 3)}", "Opp", "Center"]]
				else:
					return [self.digit(a), "stocker", "Level", f"<={self.digit(a, 1)}", "Opp", "Center"]
		elif "choose  of opponent's center stage characters" in t:
			if "choose  of opponent's center stage characters" in t:
				return [self.digit(a), self.digit(a, 1), x, "power", "Opp", "Center"]
		elif "choose  card in your clock" in t:
			if "return it to your hand" in t:
				if "choose  card in your hand" in t:
					if "put it in your clock" in t:
						return [self.digit(a), "csalvage", "", "do", ["discard", self.digit(a), "", "Clock"]]
		elif "return a marker from under this to your hand" in t:
			return [1, "marker", "Return", "Hand"]
		elif "choose  of your other characters" in t:
			if "that character gets + level and + power" in t:
				return [self.digit(a), self.digit(a, 1), x, "level", "Other", "extra", "do", [-16, self.digit(a, 2), x, "power", "extra", "do", [-16, "[AUTO] At the end of the turn, put this card into your memory.", -3, "give"]]]
			elif "that character gets + power" in t:
				return [self.digit(a), self.digit(a, 1), x, "power", "Other"]
		elif "choose  of your " in t and "of your \"" in aa:
			if "that character gets + power" in t:
				return [self.digit(a), self.digit(a, 1), x, "Name=", self.name(a, s='n'), "power"]
		elif "this gets + power" in t:
			if "at the end of the turn" in t and "put this in your memory" in t:
				return [0, self.digit(a), x, "power", "do", [0, "[AUTO] At the end of the turn, put this card into your memory.", -3, "ACT", "give"]]
			elif "and the following ability" in t:
				return [0, self.digit(a), x, "power", "do", [0, self.name(a, s="a"), x, "give"]]
			else:
				try:
					return [0, self.digit(a, 1), x, "power"]
				except IndexError:
					return [0, self.digit(a), x, "power"]
		elif "send this to memory" in t:
			if "choose   character in your hand whose level = or lower than your level" in t:
				if "put it in the slot this was in" in t:
					return [0, "memorier", "do", ["discard", self.digit(a), f"TraitL_{self.trait(a)}_<=p", "Stage", "Change"]]
			else:
				return [0, "memorier"]
		else:
			self.ablt = 8

		if self.ablt:
			return self.effect(a, t, aa, self.ablt)
		else:
			return []

	def event(self, a=""):
		t = self.text(a)
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
		self.cond = [0, 0, 0]

		if a.lower().startswith("[counter]"):
			self.ablt = 4
			if "you may choose  of your characters" in t:
				if "put it in your waiting room" in t:
					if "choose  of your character" in t:
						if "that character gets + level and + power" in t:
							return [self.digit(a), "waitinger", "upto", "if", self.digit(a), "do", [self.digit(a, 1), self.digit(a, 2), x, "level", "extra", "do", [-16, self.digit(a, 3), x, "power"]]]
			elif "put up to  cards from top of your clock" in t:
				if "in your waiting room" in t:
					if "put this in your memory" in t:
						if "if you have  or less  characters, this cannot be played from your hand" in t:
							return ["cdiscard", self.digit(a, 1), "", "upto", "do", [0, "memorier"]]
			elif "choose  of your opponent's climax in your opponent's climax area" in t or "choose  of your opponent's climax in the climax area" in t:
				if "put it into his or her waiting room" in t:
					return [self.digit(a), "waitinger", "Climax", "Opp"]
			elif "choose  level  or lower character in your opponent's back stage" in t:
				if "return it to hand" in t:
					return [self.digit(a), "hander", "Opp", "Back", "Level", f"<={self.digit(a, 1)}"]
			elif "choose  of your characters with  in the name" in t:
				if "that character gets + power" in t:
					if t.count("choose  of your characters with  in the name") == 2:
						if t.count("that character gets + power") == 2:
							return [self.digit(a), self.digit(a, 1), x, "power", "Name", self.name(a, s='n'), "do", [self.digit(a, 2), self.digit(a, 3), x, "power", "Name", self.name(a, 2, s='n')]]
			elif "choose  of your character" in t:
				if "that character gets + power" in t:
					if "put this in your memory" in t or "send this to memory" in t:
						return [self.digit(a), self.digit(a, 1), x, "power", "do", [0, "memorier"]]
				elif "that character gets the following ability" in t:
					if "draw  card" in t:
						if "discard  card from your hand to the waiting room" in t:
							return ["draw", self.digit(a), "do", ["discard", self.digit(a), "", "do", [self.digit(a), self.name(a, s='n'), x, "Event", "give"]]]
				elif "that character gets +x power" in t:
					if "x =  times # of your  characters" in t:
						return [self.digit(a), self.digit(a, 1), x, "#", "power", "#trait", self.trait(a)]
					elif "x =  multiplied by the number of cards in your stock" in t:
						return [self.digit(a), self.digit(a, 1), x, "#", "power", "#stock"]
			elif "choose  of your level  or higher characters" in t:
				if "that character gets + level and + power" in t:
					return [self.digit(a), self.digit(a, 3), x, "Level", f">={self.digit(a, 1)}", "power", self.digit(a), self.digit(a, 2), x, "level"]
			elif "draw  card" in t:
				if "discard  card from your hand to the waiting room" in t:
					if "choose  of your characters" in t:
						if "that character gets the following ability" in t:
							return ["draw", self.digit(a), "do", ["discard", self.digit(a), "", "do", [self.digit(a), self.name(a, s='n'), x, "Event", "give"]]]
			elif "all your  characters get" in t and "get \"[" in self.a_replace(a):
				return [-1, self.name(a, s='a'), x, "give"]
			elif "all your characters get" in t:
				if "get + power" in t:
					if "if the number of characters in your center stage is  or more, this cannot be played from your hand." in t:
						return [-1, self.digit(a, 1), x, "power"]
					else:
						return [-1, self.digit(a), x, "power"]
				elif "get the following ability" in t:
					return [-1, self.name(a, s='a'), x, "give"]
		elif t.startswith("draw  card"):
			if "choose  card in your clock" in t:
				if "put it in the waiting room" in t:
					if "send this to memory" in t:
						return ["draw", self.digit(a), "do", ["cdiscard", self.digit(a, 1), "", "do", [0, "memorier"]]]
		elif "all players return cards in their waiting room to their decks" in t:
			if "shuffle their respective decks" in t:
				return [-1, "shuffle", "both"]
		elif "if there are cards in your hand" in t:
			if "randomly reveal  card from your hand" in t:
				if "choose up to x of your characters" in t:
					if "those characters get + power and + soul" in t:
						if "x =  + level of the card revealed this way" in t:
							return [1, "cards", "Hand", "do", ["discard", self.digit(a), "", "random", "Reveal", "do", ["x", self.digit(a, 1), x, f"xrlevel+{self.digit(a, 3)}", "power", "extra", "upto", "do", [-16, self.digit(a, 2), x, "soul"]]]]
				elif "choose  level x or lower character in your waiting room" in t:
					if "return it to your hand" in t:
						if "x =  + level of revealed card" in t:
							return [1, "cards", "Hand", "do", ["discard", self.digit(a), "", "random", "Reveal", "do", [self.digit(a, 1), "salvage", f"CLevel_<=x", f"xrlevel+{self.digit(a, 1)}", "show"]]]
				elif "all your characters get +x power" in t:
					if "x = level times  of the revealed card" in t:
						return [1, "cards", "Hand", "do", ["discard", self.digit(a), "", "random", "Reveal", "do", [-1, "x", x, "power", "xrlevel", self.digit(a, 1)]]]
				elif "draw x card" in t:
					if "x =  + level of revealed card" in t:
						return [1, "cards", "Hand", "do", ["discard", self.digit(a), "", "random", "Reveal", "do", ["draw", "x", f"xrlevel+{self.digit(a, 1)}"]]]
		elif "you may choose  card in your clock and put it in your level zone" in t:
			if "choose up to  character cards in your waiting room and return them to your hand" in t:
				if "choose up to  climax in your waiting room and return it to your hand" in t:
					if "choose up to   characters in your waiting room and put them in your stock in any order" in t:
						return ["cdiscard", self.digit(a), "", "Level", "upto", "if", self.digit(a), "do", [self.digit(a, 1), "salvage", "Character", "upto", "show", "do", [self.digit(a, 2), "salvage", "Climax", "show", "upto", "do", [self.digit(a, 3), "salvage", f"Trait_{self.trait(a)}", "Stock", "upto", "show"]]]]
		elif "\nyou may draw  card" in t:
			if "choose  card in your hand" in t:
				if "put it in your waiting room" in t:
					if "you may put the top card of your clock in your waiting room" in t:
						if "put this in your memory" in t:
							return ["drawupto", self.digit(a), "if", self.digit(a), "do", ["discard", self.digit(a, 1), "", "do", ["drawupto", 1, "heal", "do", [0, "memorier"]]]]
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
		elif "choose  of your standing characters with  in name" in t:
			if "rest them" in t or "rest it" in t:
				if "choose  card in your opponent's waiting room" in t:
					if "send it to memory" in t:
						if "send this to memory" in t:
							return [self.digit(a), "rest", "Stand", "Name", self.name(a, s='n'), "if", self.digit(a), "do", [self.digit(a, 1), "salvage", "", "Memory", "opp", "show", "do", [0, "memorier"]]]
		elif "choose  of your level  or higher characters and put it in the waiting room" in t:
			if "choose  level  or lower  character in your waiting room" in t:
				if "put it in any slot on the stage" in t:
					if "choose up to  character in your waiting room" in t:
						if "return them to your hand" in t:
							return [self.digit(a), "waitinger", "Level", f">={self.digit(a, 1)}", "if", self.digit(a), "do", [self.digit(a, 2), "salvage", f"TraitL_{self.trait(a)}_<={self.digit(a, 3)}", "Stage", "do", [self.digit(a, 4), "salvage", "Character", "upto", "show"]]]
		elif "put all your opponent's stock in the waiting room" in t:
			if "your opponent put the same number of cards from the top of their deck in the stock" in t:
				return ["distock", -1, "top", "opp", "count", "do", ["stock", "count", "opp"]]
		elif "put up to  cards from top of your clock" in t:
			if "in your waiting room" in t:
				if "choose  of your characters" in t:
					if "that character gets + power" in t:
						if "put this in your memory" in t or "send this to memory" in t:
							return ["cdiscard", self.digit(a), "", "upto", "do", [self.digit(a, 1), self.digit(a, 2), x, "power", "do", [0, "memorier"]]]
		elif "put the top  cards of your deck face down in your memory" in t:
			if "your opponent looks at those cards and separates them into stacks of  cards and  cards" in t:
				if "choose  face down stack from among them" in t:
					if "put them in your hand" in t:
						if "return the rest in your deck" in t:
							return ["mill", self.digit(a), "top-down", "Memory", "extra", "if", self.digit(a), "do", [-16, "looktopopp", "stack", (self.digit(a, 1), self.digit(a, 2)), "fix", "extra", "do", [-16, "looktop", "hand", self.digit(a, 3), "stacked", "fix", "deck"]]]
		elif "search your deck for up to   character" in t:
			if ("put them in your hand" in t or "put it in your hand" in t) and ("reveal it" in t or "reveal them" in t):
				if "rest  of your  characters" in t:
					if "those characters do not stand during your next stand phase" in t:
						if "if you rest  characters this way" in t:
							if "choose up to   character in your waiting room and put it in your stock" in t:
								if "and put this on the bottom of the deck" in t:
									return [self.digit(a), "rest", "Trait", self.trait(a), "Stand", "extra", "do", [-16, "[CONT] This cannot [STAND] during your stand phase", 3, "give", "if", self.digit(a, 1), "do", [self.digit(a, 2), "search", f"Trait_{self.trait(a)}", "upto", "show", "do", [self.digit(a, 3), "salvage", f"Trait_{self.trait(a)}", "Stock", "upto", "show", "do", [0, "decker", "bottom"]]]]]
				elif "choose  of your standing characters" in t:
					if "rest them" in t:
						return [self.digit(a), "rest", "Stand", "if", self.digit(a), "do", [self.digit(a, 1), "search", f"Trait_{self.trait(a)}", "upto", "show"]]
				elif "choose  of your characters" in t:
					if "that character gets + power" in t:
						if "put this in your clock" in t:
							return [self.digit(a), "search", f"Trait_{self.trait(a)}", "upto", "show", "do", [self.digit(a, 1), self.digit(a, 2), x, "power", "do", [0, "clocker"]]]
				elif "send this to memory" in t:
					if "discard  card from hand to the waiting room" in t:
						return [self.digit(a), "search", f"Trait_{self.trait(a)}", "upto", "show", "do", ["discard", self.digit(a, 1), "", "do", [0, "memorier"]]]
					else:
						return [self.digit(a), "search", f"Trait_{self.trait(a)}", "upto", "show", "do", [0, "memorier"]]
				else:
					if "choose  cards from your hand" in t or "choose  card in your hand" in t:
						if "put them in your waiting room" in t or "put it in your waiting room" in t:
							if "you do not have a  character, this cannot be played from your hand" in t:
								return [self.digit(a), "search", f"Trait_{self.trait(a, 1)}", "upto", "show", "do", ["discard", self.digit(a, 1), ""]]
							else:
								return [self.digit(a), "search", f"Trait_{self.trait(a)}", "upto", "show", "do", ["discard", self.digit(a, 1), ""]]
		elif "choose the top card of your deck and put it in your stock" in t:
			if "choose  of your characters, and that character gets + power for the turn" in t:
				return ["stock", 1, "do", [self.digit(a, 0), self.digit(a, 1), x, "power"]]
		elif "choose  character in your clock whose level = or lower than your level" in t:
			if "put it in any slot on the stage" in t:
				if "you cannot play this from your hand" in t:
					return ["cdiscard", self.digit(a, 1), "CLevel_<=p", "Stage"]
		elif "choose up to   characters in your clock" in t:
			if "return it to your hand" in t:
				if "put  cards from top of your deck in your clock" in t:
					return [self.digit(a), "csalvage", f"Trait_{self.trait(a)}", "upto", "do", ["damageref", self.digit(a)]]
		elif "choose up to  characters in your waiting room with  in the name" in t:
			if "return them to your hand" in t or "return it to your hand" in t:
				if "discard  card from your hand to the waiting room" in t or "discard  cards from your hand to the waiting room" in t:
					return [self.digit(a), "salvage", f"Name_{self.name(a, s='n')}", "upto", "show", "do", ["discard", self.digit(a, 1), ""]]
				else:
					return [self.digit(a), "salvage", f"Name_{self.name(a, s='n')}", "show", "upto"]
		elif "choose up to  characters in your waiting room" in t or "choose up to  character in your waiting room" in t:
			if "return them to your hand" in t or "return it to your hand" in t:
				if "discard  card from your hand to the waiting room" in t or "discard  cards from your hand to the waiting room" in t:
					return [self.digit(a), "salvage", "Character", "upto", "show", "do", ["discard", self.digit(a, 1), ""]]
				else:
					return [self.digit(a), "salvage", "Character", "show", "upto"]
		elif "choose up to  character in your hand" in t:
			if "with  in name whose level is less than or equal to your level plus  " in t:
				if "put it in any slot on the stage" in t:
					return ["discard", self.digit(a), f"CLevelN_standby_{self.name(a, s='n')}", "Stage", "upto"]
		elif "choose  of your character" in t:
			self.ablt = 7
			if "put it in your waiting room" in t:
				if "choose  level  or lower character in your opponent's center stage and put it in the waiting room" in t:
					return [self.digit(a), "waitinger", "if", self.digit(a), "do", [self.digit(a, 1), "waitinger", "Level", f"<={self.digit(a, 2)}", "Opp", "Center"]]
			elif "put it on top of the deck" in t:
				if "choose  level  or lower character in your opponent's center stage and return it to the hand" in t:
					return [self.digit(a), "decker", "top", "if", "do", [self.digit(a, 1), "hander", "Level", f"<={self.digit(a, 2)}", "Opp", "Center"]]
			elif "return it to your hand" in t:
				if "choose  opponent's level  or lower character" in t and "put it in stock" in t:
					return [self.digit(a), "hander", "Character", "do", [self.digit(a, 1), "stocker", "Level", f"<={self.digit(a, 2)}", "Opp"]]
			elif "that character gets " in t and "that character gets \"[" in self.a_replace(a):
				if "all players return cards in their waiting rooms to their respective decks, and shuffle them" in t:
					return [-1, "shuffle", "both", "do", [self.digit(a), self.name(a, s='a'), x, "give"]]
		elif "choose  of your opponent's cost  or lower character" in t:
			if "put it on the bottom of the deck" in t:
				if "send this to memory" in t:
					if "if you have  or fewer  characters, you cannot play this from hand" in t:
						return [self.digit(a, 1), "decker", "bottom", "Opp", "Cost", f"<={self.digit(a, 2)}", "do", [0, "memorier"]]
			elif "put it on top of the deck" in t:
				if "put this in your memory" in t:
					return [self.digit(a), "decker", "top", "Opp", "Cost", f"<={self.digit(a, 1)}", "do", [0, "memorier"]]
		elif "choose up to  level  or lower characters in opponent's center stage" in t:
			if "put them in clock" in t:
				return [self.digit(a), "clocker", "Level", f"<={self.digit(a, 1)}", "Opp", "Center", "upto"]
		elif "choose  level  or lower character in your opponent's center stage" in t:
			if "put it in your opponent's memory" in t:
				return [self.digit(a), "memorier", "Level", f"<={self.digit(a, 1)}", "Opp", "Center"]
		elif "choose  level  or lower character in your opponent's back stage" in t:
			if "put it in the waiting room" in t:
				return [self.digit(a), "waitinger", "Level", f"<={self.digit(a, 1)}", "Opp", "Back"]
		elif "choose  card from your opponent's waiting room" in t:
			if "put it in your opponent's memory" in t:
				if "put this in your memory" in t:
					if "if the number of  characters on your stage is  or less, this cannot be played from your hand" in t:
						return [self.digit(a, 1), "salvage", "", "Memory", "opp", "show", "do", [0, "memorier"]]
		elif "choose  character on your opponent's stage" in t:
			if "that character gets - power" in t:
				if "put this in your memory" in t:
					return [self.digit(a), self.digit(a, 1), x, "power", "Opp", "do", [0, "memorier"]]
				else:
					return [self.digit(a), self.digit(a, 1), x, "power", "Opp"]
		elif "choose   character in your hand" in t:
			if "put them in your waiting room" in t or "from your hand to the waiting room" in t or "put it in the waiting room" in t:
				if "draw up to  cards" in t:
					if "send this to memory" in t:
						return ["discard", self.digit(a), f"Trait_{self.trait(a)}", "if", self.digit(a), "do", ["drawupto", self.digit(a, 1), "do", [0, "memorier"]]]
		elif "choose  level  or lower  character in your clock" in t:
			if "put it on any position of your stage" in t:
				if "put this in your clock" in t:
					return [self.digit(a), "csalvage", f"TraitL_{self.trait(a)}_<={self.digit(a, 1)}", "Stage", "do", [0, "clocker"]]
		elif "look at the top  cards of your deck" in t:
			if "choose up to  character with  or  in name" in t:
				if "put it in your hand" in t:
					if "reveal it" in t:
						return [self.digit(a), "looktop", "top", "hand", self.digit(a, 1), f"Name_{self.name(a, s='n')}_{self.name(a, 2, s='n')}", "fix", "upto", "show"]
		elif "look at up to  cards of the top of your opponent's deck" in t:
			if "choose up to  of them" in t:
				if "put them in the waiting room" in t:
					if "return the rest to the deck" in t:
						return [self.digit(a), "looktop", "top", "waiting", self.digit(a, 1), "upto", "any", "opp", "shuff"]
		elif "draw up to  cards" in t:
			if "choose  cards in your hand" in t or "discard  cards from your hand" in t:
				if "put them in your waiting room" in t or "from your hand to the waiting room" in t:
					return ["drawupto", self.digit(a), "do", ["discard", self.digit(a, 1), ""]]
		elif "return all your opponent's level  or lower characters to the deck, and your opponent shuffles that deck" in t:
			if "put this in your clock" in t:
				return [-1, "decker", "Level", f"<={self.digit(a)}", "Opp", "do", [0, "clocker"]]
		else:
			self.ablt = 7

		if self.ablt:
			return self.effect(a, t, "", self.ablt)
		else:
			return []

	def auto(self, a="", p="", r=("0", "0", ""), v=("", ""),passed=False ,lvop=(0, 0), cx=("", "0", ""), pos=("", "", "", ""), n="", sx=[], tr=([], []), z=(0, 0), act="", cnc=("0", False), pp=0, dis=("", ""), nr=("", ""), atk="", dmg=0, nmop=("", ""), rst="", lvc=("", ""), batt=False, refr="", sav=("", ""), brt=("", 0), lr=(0, 0), lvup="", inds=[], baind=("0", "0"), csop=(0, 0), suop=("", ""),trop=([],[]), ty=("", [], ""), ch=False, std=("", "")):
		""":param a: ability (string)
		:param p: phase (string)
		:param r: active card  _ triggering effect card _ triggering effect card type(list)
		:param v: status of both cards (list)
		:param ty: triggering effect card type,trigger (list)
		:param lvop: level of both cards (list)
		:param trop: trait of both cards (list)
		:param cx: climax name _ climax id (list)
		:param pos: position of both cards (list)
		:param n: turn player (int)
		:param tr: trait active card  _ triggering effect card (list)
		:param nr: name active card  _ triggering effect card (list)
		:param z: active card turn played _ actual turn (list)
		:param act: used act (bool)
		:param atk: atk type (str)
		:param sx: Status on stage (list)
		:param inds: Cards on stage (list)
		:param cnc: Damage dealt by attacking character is cancelled (boolean)
		:param pp: Beginning, Actual, End of the phase (-1,0,1) (int)
		:param dis:
		:param baind: attacking_batteling opp (list)
		:param lvop: card and batteling opp level(list)
		:param csop: card and batteling opp cost(list)
		:param suop: card and batteling opp status(list)
		:param nmop: card and batteling opp name(list)
		:param passed: check if ability is not finished and come form passed ability
		:return:
		"""
		t = self.text(a)
		aa = self.a_replace(a)
		if "until the next end of your opponent's turn" in t or "until the end of your opponent's next turn" in t or "until end of your opponent's next turn" in t:
			x = 2
		elif "for the turn" in t or " until end of turn" in t:
			x = 1
		else:
			x = 1

		self.ablt = 0
		self.target = ""
		self.cx = False
		self.center = False
		self.cond = [0, 0, 0]

		if r[1] == "":
			r = (r[0], "0")
		if ch:
			if "when this is placed on the stage from your hand or by a  effect" in t or "when this is placed on stage from your hand or by a  effect" in t:
				if r[0] == r[1] and any(field in pos[1] for field in ("Center", "Back")) and "Waiting" in pos[0]:
					if "you may put the top card of your clock in your waiting room" in t:
						return ["pay", "may", "played", "do", ["heal", 1, "top"]]
					elif "you may draw  card" in t:
						return ["pay", "may", "played", "do", ["draw", self.digit(a)]]
					elif "look at up to x cards from the top of your deck" in t:
						if "x = the number of your  characters" in t:
							if "choose up to  card from among them, and put it in your hand" in t:
								return [-14, "looktop", "Trait", self.trait(a), "Stage", "top", "hand", self.digit(a), "", "upto", "played"]
					elif "choose  of your other characters" in t:
						if "that character gets the following ability" in t:
							return [self.digit(a), self.name(a, s='a'), x, "give", "Other", "played"]
					elif "draw up to  card" in t:
						if "choose  card in your hand, and put it in your waiting room" in t or "discard  card from your hand to the waiting room" in t:
							return ["drawupto", self.digit(a), "played", "do", ["discard", self.digit(a, 1), ""]]
			elif "when your other  is placed to the stage via change" in t:
				if r[0] != r[1] and r[0][-1] == r[1][-1] and any(field in pos[3] for field in ("Center", "Back")) and "Waiting" in pos[2] and self.name(a, s='n') in nr[1]:
					if "you may put the top card of your deck in your stock" in t:
						return ["pay", "may", "played", "do", ["stock", 1]]
			elif "when this is placed from hand or waiting room to the stage" in t:
				if r[0] == r[1] and ((any(field in pos[1] for field in ("Center", "Back")) and "Waiting" in pos[0]) or ("Hand" in pos[0] and v[0] == "Stand" and any(field in pos[1] for field in self.stage))):
					if "this gets the following ability" in t:
						return [0, self.name(a, s='a'), x, "give", "played"]
			elif "when this is placed from the waiting room to the stage" in t or "when this is placed from waiting room to the stage" in t:
				if r[0] == r[1] and any(field in pos[1] for field in self.stage) and "Waiting" in pos[0]:
					self.ablt = 1
			elif "when another of your characters is placed from the waiting room to the stage" in t:
				if r[0][-1] == r[1][-1] and r[0] != r[1] and any(field in pos[3] for field in self.stage) and "Waiting" in pos[2] and v[1] != "Reverse":
					if "this gets + power" in t:
						if "this ability activates up to  time per turn" in t:
							return [0, self.digit(a, 1), x, "power", f"a{self.digit(a)}"]
						else:
							return [0, self.digit(a, 1), x, "power", "played"]
		elif dis[0]:
			if "when  of your characters is put in your waiting room from your hand" in t:
				if r[0] != dis[0] and r[0][-1] == dis[0][-1] and "Hand" in pos[2] and "Waiting" in pos[3] and "Character" in dis[1]:
					self.ablt = 9
					self.cond[0] += 1
		elif lvup:
			if "when your opponent levels up" in t or "when your opponent levels-up" in t:
				if lvup not in r[0][-1]:
					self.ablt = 9

					if "\" is in your climax area" in aa:
						if f"\"{cx[0].lower()}\" is in your climax area" not in aa:
							self.ablt = 0
					if "this is in your center stage" in t:
						if "Center" not in pos[1]:
							self.ablt = 0
			elif "when you level up" in t or "when you level-up" in t:
				if lvup in r[0][-1]:
					self.ablt = 9
		elif refr:
			if "when you refresh your deck" in t:
				if refr in r[0][-1]:
					if "you may pay the cost" in t:
						if "choose up to   in your hand and put it in a back stage slot" in t:
							return ["pay", "may", "do", ["discard", self.digit(a), f"Name=_{self.name(a, s='n')}", "Stage", "Back", "upto"]]
		elif sav[0]:
			if "during attack phase" in t and p in self.attack:
				if "when your or your opponent's character is returned from the waiting room to hand" in t:
					if "all of that player's characters get - soul" in t:
						return [-18, self.digit(a), x, "soul", "player", sav[0][-1]]
		elif brt[0]:
			if "when your opponent uses " in t and "when your opponent uses \"brainstorm\"" in aa:
				if brt[0][-1] != r[0][-1] and brt[0] != r[0]:
					if "puts at least  climax card in the waiting room" in t or "if  climax is put into the waiting room by that effect" in t:
						if brt[1] >= self.digit(a):
							self.cond[0] += 1
							self.ablt = 9
		elif "encore [" in t and "cannot use \"[auto] encore\"" not in aa:
			if r[0] == r[1] and any(field in pos[0] for field in self.stage) and "Waiting" in pos[1] and "Waiting" in pos[3]:
				if "[put  character card from your hand to the waiting room]" in t or "[put  character from your hand in your waiting room]" in t:
					return [1, "Character", "may", "encore"]
				elif "[put   character card from your hand to the waiting room]" in t:
					return [1, "Trait", self.trait(a), "may", "encore"]
				elif "[put   or   character card from your hand to the waiting room]" in t or "[put  character card with  or  from your hand to the waiting room]" in t:
					return [1, "Trait", f"{self.trait(a)}_{self.trait(a, 1)}", "may", "encore"]
				elif "[put the top card of your deck in your clock]" in t:
					return [1, "Clock", "may", "encore"]
				elif "[()]" in t:
					if "[(2)]" in a:
						return [2, "Stock", "may", "encore"]
					elif "[(1)]" in a:
						return [1, "Stock", "may", "encore"]
		elif "bond/" in t:
			if r[0] == r[1] and "Hand" in pos[0]:
				return ["pay", "may", "played", "do", [1, "salvage", f"Bond_{self.name(a, s='n')}", "show"]]
		elif "when you play an event" in t:
			if r[0][-1] == r[1][-1] and r[0] != r[1] and r[2] == "Event" and "Hand" in pos[2] and v[1] == "Stand":
				self.ablt = 9
		elif "when your opponent plays an event" in t:
			if r[0][-1] != r[1][-1] and r[0] != r[1] and r[2] == "Event" and "Hand" in pos[2] and v[1] == "Stand":
				self.ablt = 9
		elif "when you use an act" in t:
			if act and r[0][-1] == act[-1] and r[0][-1] == r[1][-1]:
				self.ablt = 9
		elif "when this is placed on the stage by the effect of \"" in aa or "when this is placed on the stage by the standby effect of \"" in aa or "when this is placed from hand to the stage or by the [auto] effect of \"" in aa:
			if ("Hand" in pos[0] and r[0] == r[1] and v[0] == "Stand" and any(field in pos[1] for field in self.stage)) or (std[0] and std[2] == r[0] and std[0][-1] == r[1][-1] and std[0]!=r[1] and f"effect of \"{std[1].lower()}\"" in aa and any(field in pos[1] for field in ("Center", "Back")) and "Waiting" in pos[0]):
				self.ablt = 1
		elif "when your other  character or this is placed from hand to stage" in t:
			if (r[0] != r[1] and r[0][-1] == r[1][-1] and self.trait(a) in tr[1] and "Hand" in pos[2] and any(field in pos[3] for field in self.stage) and "Stand" in v[1]) or (
				"Hand" in pos[0] and r[0] == r[1] and v[0] == "Stand" and any(field in pos[1] for field in self.stage)):
				self.ablt = 9
		elif "when your other  character is played and placed to the stage" in t or "when another of your  characters is placed on the stage from your hand" in t or "when another of your  characters is placed from hand to the stage" in t or "when another  character of yours is placed from hand to the stage" in t or "when another  character is placed on the stage from your hand" in t or "when your other  character is placed on the stage from your hand" in t:
			if r[0] != r[1] and r[0][-1] == r[1][-1] and self.trait(a) in tr[1] and ("Hand" in pos[2] or ("on the stage from your hand or memory" in t and "Memory" in pos[2])) and any(field in pos[3] for field in self.stage) and "Stand" in v[1]:
				self.ablt = 9
				if "that character gets + power and " in t:
					if "power and «" in aa:
						return [-3, self.digit(a), x, "power", "target", r[1], "extra", "do", [-16, self.trait(a, -1), x, "trait"]]
				if "if this is stand" in t:
					if v[0] != "Stand":
						self.ablt = 0
		elif "when your other  character is placed from the stage to the waiting room" in t:
			if r[0] != r[1] and r[0][-1] == r[1][-1] and any(field in pos[2] for field in ("Center", "Back")) and "Waiting" in pos[3] and self.trait(a) in tr[1]:
				self.ablt = 9
		elif "when your other character is put in your waiting room from the stage" in t or "when your other character is put in the waiting room" in t or "when another character of yours is placed from the stage to the waiting room" in t:
			if r[0] != r[1] and r[0][-1] == r[1][-1] and any(field in pos[2] for field in ("Center", "Back")) and "Waiting" in pos[3]:
				self.ablt = 9
				self.target = r[1]
				if "if this is in your back stage" in t or "if this is in the back stage" in t:
					if "Back" not in pos[1]:
						self.ablt = 0
		elif "when this is placed from hand or waiting room to the stage" in t:
			if r[0] == r[1] and ((any(field in pos[1] for field in self.stage) and "Waiting" in pos[0]) or ("Hand" in pos[0] and v[0] == "Stand" and any(field in pos[1] for field in self.stage))):
				self.ablt = 1
		elif "when this is put in your waiting room from the stage" in t or "when this is placed from the stage to the waiting room" in t or "when this goes from stage to the waiting room" in t or "when this is put in the waiting room from the stage" in t:
			if r[0] == r[1] and any(field in pos[0] for field in ("Center", "Back")) and "Waiting" in pos[1]:
				self.ablt = 1
				if "you may pay the cost" in t:
					if "send this to memory" in t:
						return ["pay", "may", "played", "do", [0, "memorier"]]
				elif "you may put this rested in the slot this was in" in t or "you may return this to its previous stage position as rest" in t:
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
				if "you may pay the cost" in t:
					if "reveal the top card of your deck" in t:
						if "if that card is a  character whose level is lower than or equal to your level" in t:
							if "put that character in any slot on your stage" in t:
								return [-9, "reveal", "TraitL", f"{self.trait(a)}_<=p", "played", "do", ["pay", "may", "do", [-9, "search", "", "Stage", "topdeck"]]]
					elif "search your deck for up to  character with  in its card name" in t or "search your deck for up to  character with  in name" in t:
						if "reveal it" in t and "put it in your hand" in t:
							if any(setonly in a for setonly in self.set_only):
								for sto in self.set_only:
									if sto in a:
										return ["pay", "may", "played", "do", [self.digit(a), "search", f"NameSet_{self.name(a, s='n')}_{self.set_only[set]}", "show", "upto"]]
					elif "search your deck for  character with " in t:
						if "reveal it" in t and "put it in your hand" in t:
							if self.name(a, s='n') in self.text_name:
								return ["pay", "may", "played", "do", [self.digit(a), "search", f"Text_{self.text_name[self.name(a, s='n')]}", "show"]]
					elif "choose   character, a  character, and a  character in your waiting room" in t:
						if "return them to your hand" in t:
							return ["pay", "may", "played", "do", [self.digit(a) + 2, "salvage", f"BTrait_{self.trait(a)}_{self.trait(a, 1)}_{self.trait(a, 2)}", "show"]]
					elif "your opponent cannot play climax cards from hand" in t:
						return ["pay", "may", "played", "do", [-21, "[CONT] Your opponent cannot play climax cards from hand", x, "give"]]
				elif "you may choose  card in your hand" in t:
					if "put it in your stock" in t:
						return ["pay", "may", "played", "do", [self.digit(a), "discard", "", "Stock", "upto"]]
				elif "you may choose  of either  or  or  or  in your clock" in t:
					if "return it to your hand" in t:
						if "choose  card in your hand" in t:
							if "put it in clock" in t:
								return ["pay", "may", "played", "do", [self.digit(a), "csalvage", f"Name_{self.name(a, s='n')}_{self.name(a, 2, s='n')}_{self.name(a, 4, s='n')}_{self.name(a, 6, s='n')}", "upto", "if", self.digit(a), "do", ["discard", self.digit(a, 1), "", "Clock"]]]
				elif "you may choose  character in your clock with  in name" in t:
					if "return it to your hand" in t:
						if "choose  card in your hand" in t:
							if "put it in your clock" in t:
								return ["pay", "may", "played", "do", ["csalvage", self.digit(a), f"Name_{self.name(a, s='n')}", "if", self.digit(a), "do", ["discard", self.digit(a, 1), "", "Clock"]]]
				elif "you may put all your opponent's characters in your opponent's memory" in t:
					if "put those characters on to separate positions of his or her stage" in t:
						return ["pay", "may", "played", "do", [-1, "memorier", "opp", "extra", "if", 1, "do", [-16, "msalvage", "ID=_x", "Stage", "Opp", "plchoose", "separate", "opp"]]]
				elif "you may choose   character in your waiting room" in t:
					if "return it to your hand" in t:
						return ["pay", "may", "played", "do", [self.digit(a), "salvage", f"Trait_{self.trait(a)}", "show"]]
				elif "if there are  or more climax cards in your opponent's waiting room" in t:
					if "rest this" in t:
						return [self.digit(a), "cards", "Waiting", "Climax", "opp", "played", "do", [0, "rest"]]
				elif "look at up to x cards from the top of your deck" in t or "look at up to x cards from top of your deck" in t:
					if "x = the number of  characters you have" in t or "x = the number of your  characters" in t or "x = # of your  characters" in t:
						if "choose up to  card from among them" in t or "choose up to  of them" in t:
							if "put it in your hand" in t:
								return [-14, "looktop", "Trait", self.trait(a), "Stage", "top", "hand", self.digit(a), "", "upto", "played"]
				elif "draw up to  card" in t:
					if "choose  card in your hand, and put it in your waiting room" in t or "discard  card from your hand to the waiting room" in t:
						return ["drawupto", self.digit(a), "played", "do", ["discard", self.digit(a, 1), ""]]
					elif "choose up to  cost  or lower character in your hand" in t:
						if "put it on any position of your stage" in t:
							return ["drawupto", self.digit(a), "played", "do", ["discard", self.digit(a, 1), f"Cost_<={self.digit(a, 2)}", "Stage", "upto"]]
				elif "reveal the top card of your deck" in t:
					if "draw  card" in t or "put it in your hand" in t:
						if "discard  card from your hand to the waiting room" in t or "discard  card from your hand" in t:
							if "if it's a character with  in name" in t:
								return [-9, "reveal", "Name", self.name(a, s='n'), "played", "do", ["draw", 1, "do", ["discard", self.digit(a), ""]]]
							elif "if it's a  character" in t:
								return [-9, "reveal", "Trait", self.trait(a), "played", "do", ["draw", 1, "do", ["discard", self.digit(a), ""]]]
							elif "if it's a  character or " in t and "or \"" in aa:
								return [-9, "reveal", "Trait", self.trait(a), "Name", self.name(a, 1), "played", "do", ["draw", 1, "do", ["discard", self.digit(a), ""]]]
				elif "choose  cost  or higher character in your opponent's waiting room" in t:
					if "put it in an empty slot in your opponent's back stage" in t:
						return [self.digit(a), "salvage", f"Cost_>={self.digit(a)}", "Stage", "opp", "Back", "Open", "Opp"]
				elif "choose  of your standing characters" in t:
					if len([xs for xs in sx if xs == "Stand"]) >= self.digit(a):
						if "rest it" in t:
							return [self.digit(a), "rest", "Stand", "played"]
				elif "choose up to  of your other characters" in t:
					if "those characters get + power and + soul" in t:
						return [self.digit(a), self.digit(a, 1), x, "Other", "played", "upto", "power", self.digit(a), self.digit(a, 2), x, "Other", "upto", "soul"]
				elif "choose  character in your opponent's center stage" in t:
					if "that character gets - power" in t:
						return [self.digit(a), self.digit(a, 1), x, "power", "Opp", "Center", "played"]
				elif "choose   on your stage" in t and "\" on your stage" in aa:
					if "put it in the waiting room" in t:
						return [self.digit(a), "waitinger", "Name", self.name(a, s='n'), "played"]
				elif "if your opponent has a" in t or "if your opponent has a character named " in t:
					if "play rock-paper-scissors with your opponent until someone wins" in t:
						if "the winner draws  card" in t:
							return ["name", self.name(a, 1), "opp", "played", "do", ["pay", "may", "do", ["janken", "winner", "do", ["draw", self.digit(a)]]]]
					elif "and all players agree" in t or "and everyone agrees" in t:
						if "all players declare \"" in aa or "all players declare" in t:
							return ["name", self.name(a, s='n'), "opp", "played", "do", ["confirm", "both", "do", ["declare", "text", self.name(a, -1, s='n'), "all"]]]
						elif "high-five" in t:
							if "everyone draws  card" in t:
								return ["name", self.name(a, 1), "opp", "played", "do", ["confirm", "both", "do", ["declare", "five", "do", ["draw", self.digit(a), "do", ["draw", self.digit(a), "opp"]]]]]
		elif "when this is placed from the waiting room to the stage" in t or "when this is placed from waiting room to the stage" in t:
			if r[0] == r[1] and any(field in pos[1] for field in self.stage) and "Waiting" in pos[0]:
				self.ablt = 1
		elif "when another of your characters is placed from the waiting room to the stage" in t:
			if r[0][-1] == r[1][-1] and r[0] != r[1] and any(field in pos[3] for field in self.stage) and "Waiting" in pos[2] and v[1] != "Reverse":
				self.ablt = 1
		elif "when this is placed on stage" in t:
			if pos[0] and r[0] == r[1] and v[0] == "Stand" and any(field in pos[1] for field in self.stage):
				self.ablt = 1
		elif "when this becomes rested from standing" in t:
			if r[0] == r[1] and r[0] == rst and v[0] == "Rest":
				self.ablt = 9
		elif "when your opponent's stand character becomes rest" in t:
			if r[0] != r[1] and r[0][-1] != r[1][-1] and r[1] == rst and v[1] == "Rest":
				self.ablt = 9
		elif "during this's battle" in t or "during battles involving this" in t:
			if r[0] in baind:
				if "if damage taken by you is not canceled" in t and not cnc[1] and cnc[0] in r[0][-1]:
					if "you may pay the cost" in t:
						if "deal the same amount of damage to your opponent" in t and dmg > 0:
							return ["pay", "may", "do", ["damage", dmg, "opp"]]
				elif "when the damage you received is canceled" in t and cnc[1] and cnc[0] in r[0][-1]:
					self.ablt = 2
		elif pp == 9 and ("Battle" in p or "Damage" in p):
			if "at the end of this's attack" in t:
				if n in r[0][-1] and r[0] == r[1] and atk != "" and r[0] == baind[0]:
					if "\" is in your climax area" in aa:
						if f"\"{cx[0].lower()}\" is in your climax area" in aa and r[0][-1] == cx[1][-1] and n in cx[1][-1]:
							self.ablt = 2
		elif "Draw" in p:
			if pp < 0:
				if "at the beginning of your draw phase" in t:
					if n in r[0][-1]:
						if "you may put the top card of your deck in your clock" in t:
							if "send this to memory" in t:
								if "if not" in t or "if you do not" in t:
									return ["pay", "may", "a1", "dont", [0, "memorier"], "do", ["damageref", 1]]
						elif "you may pay the cost" in t:
							if t.startswith("change"):
								return ["pay", "may", "a1", "do", ["change", self.digit(a), f"Name_{self.name(a, s='n')}"]]
						elif "choose   in your memory" in t or "choose  card named  in your memory" in t:
							if "put it on any position on your stage" in t or "put it on any position of your stage" in t or "put it in any slot on the stage" in t:
								if "that character gets + power" in t:
									return [self.digit(a), "msalvage", f"Name=_{self.name(a, s='n')}", "Stage", "extra", "a1", "do", [-16, self.digit(a, 1), x, "power"]]
								else:
									return [self.digit(a), "msalvage", f"Name=_{self.name(a, s='n')}", "Stage", "a1"]
						elif "put those characters from your memory on to separate positions of your stage" in t:
							if "those characters get + power" in t:
								return [-38, "msalvage", "", "Stage", "a1", "separate", "extra", "do", [-16, self.digit(a), x, "power"]]
				elif "at the beginning of your opponent's draw phase" in t or "at the start of your opponent's draw phase" in t:
					if n not in r[0][-1]:
						self.ablt = 3
						if "if this is in your center stage" in t or "if this is in the center stage" in t:
							if "Center" not in pos[1]:
								self.ablt = 0
		elif "Main" in p:
			if pp < 0:
				if "at the start of your main phase" in t or "at the beginning of your main phase" in t:
					if n in r[0][-1]:
						self.ablt = 3
						if "if this is in your memory" in t or "if this is in memory" in t:
							if "Memory" not in pos[1]:
								self.ablt = 0
		elif "Climax" in p:
			if pp < 0:
				if "at the start of your climax phase" in t or "at the beginning of your climax phase" in t:
					if n in r[0][-1] and any(field in pos[1] for field in self.stage):
						self.ablt = 3
						if "you may pay the cost" in t:
							if aa.startswith("[auto] change"):
								if "choose   or  in your waiting room" in t:
									return ["pay", "may", "a1", "do", ["change", self.digit(a), f"Name_{self.name(a, s='n')}_{self.name(a, 2, s='n')}"]]
								else:
									return ["pay", "may", "a1", "do", ["change", self.digit(a), f"Name_{self.name(a, -1, s='n')}"]]
							elif aa.startswith("[auto] resonance"):
								if "choose  \"" in t and "\" in your waiting room and put it in any slot on the stage" in t:
									return ["pay", "may", "a1", "do", [self.digit(a), "salvage", f"Name=_{self.name(a, -1, s='n')}", "Stage"]]
								elif "this gets + power and + soul" in t:
									return ["pay", "may", "a1", "do", [0, self.digit(a), x, "power", 0, self.digit(a, 1), x, "soul"]]
								elif "this gets + power" in t:
									return ["pay", "may", "a1", "do", [0, self.digit(a), x, "power"]]
			elif pp == 0:
				if f"when \"{cx[0].lower()}\" is put on your climax area" in aa or f"when a card named \"{cx[0].lower()}\" is placed on your climax area" in aa or f"when \"{cx[0].lower()}\" is placed on your climax area" in aa or f"when \"{cx[0].lower()}\" is placed in your climax area" in aa or f"when \"{cx[0].lower()}\" is placed to your climax area" in aa:
					if r[0][-1] == cx[1][-1] and cx[1] == r[1]: #and n in cx[1][-1]
						self.ablt = 1
						self.cond[1] += 2
						if "if this is in your center stage" in t or "if this is in the center stage" in t or "if this is on your center stage" in t or "if this in on your center stage" in t:
							if "Center" not in pos[1]:
								self.ablt = 0

							if "you may pay the cost" in t:
								if "choose  level  or lower character opposite this" in t:
									if "put it on top of the deck" in t:
										return [self.digit(a), "decker", "top", "Opp", "Level", f"<={self.digit(a, 1)}", "Opposite"]
								elif "choose up to  level  or lower  character" in t:
									if "in your waiting room" in t:
										if "put them in separate position on your center stage" in t:
											if "at the start of the encore step, if those characters are on stage, return them to the deck" in t:
												return [0, "stage", "Center", "do", ["pay", "may", "do", [self.digit(a), "salvage", f"TraitL_{self.trait(a)}_<={self.digit(a, 1)}", "Stage", "Center", "extra1", "separate", "upto", "do", [-21, "[AUTO] At the beginning of the encore step, if those characters are on stage, return them to your deck", 1, "give"]]]]
									elif " in your hand" in t:
										if "put it in any slot on the stage" in t:
											return [0, "stage", "Center", "do", ["pay", "may", "do", ["discard", self.digit(a), f"TraitL_{self.trait(a)}_<={self.digit(a, 1)}", "Stage", "upto"]]]
								elif "search your deck for   character whose level is  or lower" in t:
									if "put it in any slot on stage" in t:
										return [0, "stage", "Center", "at", "cxcombo", "do", ["pay", "may", "do", [self.digit(a), "search", f"TraitL_{self.trait(a)}_<={self.digit(a, 1)}", "Stage"]]]
								elif "search your deck for up to  cards named " in t:
									if "put them on separate positions of your center stage" in t:
										return [0, "stage", "Center", "do", ["pay", "may", "do", [self.digit(a), "search", f"Name=_{self.name(a, -1, s='n')}", "Stage", "Center", "separate", "upto"]]]
							# elif "you may choose " in t and "\" in your waiting room" in aa:
							# 	if "put it in any slot on the stage" in t:
							# 		return [0, "stage", "Center", "do", ["pay", "may", "do", [self.digit(a), "salvage", f"Name=_{self.name(a, -1, s='n')}", "Stage", "upto"]]]
							elif "you may choose  level  or lower character from your clock" in t:
								if "put it in any slot on the stage" in t:
									if "put the top  cards of your deck in your clock" in t:
										return [0, "stage", "Center", "do", ["pay", "may", "do", ["cdiscard", self.digit(a), f"CLevel_<={self.digit(a, 1)}", "Stage", "upto", "if", self.digit(a), "do", ["damageref", self.digit(a, 2)]]]]
							# elif "choose up to  cards in your opponent's waiting room" in t:
							# 	if "return it to the deck" in t:
							# 		if "this gets + power" in t:
							# 			return [self.digit(a), "salvage", "", "Library", "upto", "opp", "show", "do", [0, self.digit(a, 1), x, "power"]]
						elif "if you have another card named " in t:
							if "put the top card of your deck in your waiting room" in t:
								if "if that card is level  or lower, you may pay the cost" in t:
									if "all your characters get the following ability" in t:
										return [1, "name", self.name(a, 5), "other", "do", ["mill", 1, "lvl", self.digit(a, 1), "lower", "any", "if", "do", ["pay", "may", "do", [-1, self.name(a, s="a"), x, "give"]]]]
						elif "you may pay the cost" in t:
							if "choose  \"" in t and "put it in the slot this was in" in t:
								if "\" in your memory" in aa:
									return ["pay", "may", "cxcombo", "do", ["mchange", self.digit(a), f"Name=_{self.name(a, -1, s='n')}"]]
								elif "\" in your waiting room" in aa:
									if "put this in the waiting room" in t:
										return ["pay", "may", "cxcombo", "do", [0, "waitinger", "do", ["change", self.digit(a), f"Name=_{self.name(a, -1, s='n')}"]]]
							elif "choose  cost  or less character with \"" in t and "\" in name in your waiting room" in t:
								if "put it in the slot this was in" in t:
									return ["pay", "may", "cxcombo", "do", ["change", self.digit(a), f"NCost_{self.name(a, -1, s='n')}_<={self.digit(a, 1)}"]]
							elif "search your deck for up to   character whose level is lower than or equal to your level" in t:
								if "put it in the slot this was in" in t:
									return ["pay", "may", "cxcombo", "do", ["lchange", self.digit(a), f"TraitL_{self.trait(a)}_<=p", "upto"]]
							# elif "search your deck for up to   and put it in the slot this was in" in t and "\" and put it in" in aa:
							# 	return ["pay", "may", "cxcombo", "do", ["lchange", self.digit(a), f"Name=_{self.name(a, -1, s='n')}", "upto"]]

						if "if this is in your center stage" in t or "if this is in the center stage" in t or "if this is on your center stage" in t or "if this in on your center stage" in t:
							if "Center" not in pos[1]:
								self.ablt = 0
				elif "when a climax is placed on your opponent's climax area" in t or "when your opponent's climax card is placed in the climax area" in t:
					if (cx[0] != "" and r[0][-1] != cx[1][-1] and cx[1] == r[1] and n not in r[0][-1] and n in cx[1][-1]) or (cx[3] != "" and r[0][-1] != cx[4][-1] and cx[4] == r[1] and n in r[0][-1] and n  not in cx[4][-1]):
						self.ablt = 9
						if "character opposite this" in t:
							if "Center" not in pos[1]:
								self.ablt = 0
						# if "you may pay the cost" in t:
						# 	if "choose  character opposite this" in t:
						# 		if "put it in your opponent's waiting room" in t or "put it in the waiting room" in t:
						# 			return ["stage", "Center", "do", ["pay", "may", "do", [1, "waitinger", "Opposite"]]]
				elif "when a climax is placed on your climax area" in t or "when your climax is placed in the climax area" in t or "when your climax is placed on your climax area" in t:
					if (cx[0] != "" and r[0][-1] == cx[1][-1] and cx[1] == r[1] and n in cx[1][-1] and n in r[0][-1]) or (cx[3] != "" and r[0][-1] == cx[4][-1] and  cx[4] == r[1] and n not in cx[4][-1] and n not in r[0][-1]):
						self.ablt = 9
		elif "Attack" in p:
			if pp < 0:
				if "at the start of your opponent's attack phase" in t or "at the beginning of your opponent's attack phase" in t:
					if n not in r[0][-1]:
						self.ablt = 3
				elif "at the beginning of your attack phase" in t:
					if n in r[0][-1]:
						self.ablt = 3
				if "if this is in your center stage" in t:
					if "Center" not in pos[1]:
						self.ablt = 0
		elif "Declaration" in p:
			if "when this attacks or is attacked" in t:
				if atk != "" and r[0] in baind and n in r[1][-1] and (r[0] == r[1] or (r[0] != r[1] and r[0][-1] != r[1][-1])):
					if "put the top card of your stock under this as marker" in t:
						return [1, "marker", "top", "Stock"]
			elif "when this attacks" in t:
				if r[0] == r[1] and n in r[1][-1] and atk != "" and r[0] == baind[0]:
					if "\" is in the climax area" in aa or "\" is in your climax area" in aa or "\" on your climax area" in aa:
						if (f"\"{cx[0].lower()}\" is in the climax area" in aa or f'\"{cx[0].lower()}\" is in your climax area' in aa or f'\"{cx[0].lower()}\" on your climax area' in aa) and r[0][-1] == cx[1][-1] and n in cx[1][-1]:
							self.cx = True
							self.ablt = 2
							self.cond[1]+=2

							if "your opponent searches your deck for  level  or higher character" in t:
								if "put it in your hand" in t:
									return [self.digit(a), "searchopp", f"CLevel_>={self.digit(a, 1)}"]
							elif "your opponent may not play events from hand" in t or "your opponent cannot play event cards from hand" in t:
								return [-21, "[CONT] Your opponent cannot play events from hand", x, "give"]
							elif "you may pay the cost" in t:
								if "your opponent cannot use any act of characters on his or her stage" in t:
									return ["pay", "may", "at", "cxcombo", "do", [-21, "[CONT] Your opponent cannot use any [ACT] of characters on his or her stage.", x, "give"]]
								elif "put all level  or lower characters in your opponent's center stage in stock" in t:
									return ["pay", "may", "cxbombo", "at", "do", [-15, "stocker", "Opp", "Center", "Level", f"<={self.digit(a)}"]]
								elif "put up to  card from top of your clock in your waiting room" in t:
									if "choose  of your other characters" in t:
										if "that character gets the following ability" in t:
											return ["pay", "may", "cxcombo", "at", "do", ["drawupto", self.digit(a), "heal", "do", [self.digit(a), self.name(a, s='a'), x, "give"]]]
								elif "put the top card of your clock in the waiting room" in t:
									return ["pay", "may", "cxcombo", "at", "do", ["heal", 1, "top"]]
								elif "look at top  cards of your deck" in t:
									if "reveal up to  character with  or  in name" in t:
										if "put it in your hand" in t:
											return ["pay", "may", "at", "cxcombo", "do", [self.digit(a), "looktop", "top", "hand", self.digit(a, 1), f"TraitN_{self.trait(a)}_{self.name(a, -1, s='n')}", "fix", "upto", "show"]]
								elif "look at up to  cards from top of your deck" in t:
									if "reveal up to  character with  or  in name" in t:
										if "put it in your hand" in t:
											return ["pay", "may", "at", "cxcombo", "do", [self.digit(a), "looktop", "top", "hand", self.digit(a, 1), f"TraitN_{self.trait(a)}_{self.name(a, -1, s='n')}", "upto", "show"]]
								elif "choose   character in your waiting room" in t or "choose  character from your waiting room" in t:
									if "put it in your stock" in t:
										if "this gets + power" in t:
											return ["pay", "may", "cxbombo", "at", "do", [self.digit(a), "salvage", f"Trait_{self.trait(a)}", "Stock", "show", "do", [0, self.digit(a, 1), x, "power"]]]
									elif "return it to your hand" in t:
										if "rest all your opponent's standing characters" in t or "rest all your opponent's stand characters" in t:
											return ["pay", "may", "cxbombo", "at", "do", [self.digit(a), "salvage", "Character", "show", "do", [-1, "rest", "Stand", "Opp"]]]
										else:
											return ["pay", "may", "cxbombo", "at", "do", [self.digit(a), "salvage", "Character", "show"]]
								elif "choose  character in your waiting room" in t:
									if "return it to your hand" in t:
										if "choose  of your  characters" in t:
											if "that character gets + power" in t:
												return ["pay", "may", "cxbombo", "at", "do", [self.digit(a), "salvage", "Character", "show", "do", [self.digit(a, 1), self.digit(a, 2), x, "power", "Trait", self.trait(a)]]]
								elif "choose  cost  or lower character in your opponent's" in t:
									if "opponent's center stage" in t:
										if "put it on the bottom of the deck" in t:
											if "then choose up to  other character in your opponent's center stage with the same name as that character" in t:
												if "put it on bottom of the deck" in t:
													return ["pay", "may", "cxcombo", "at", "do", [self.digit(a), "decker", "bottom", "Cost", f"<={self.digit(a, 1)}", "Opp", "Center", "save_name", "do", [self.digit(a), "decker", "bottom", "Name=", "same_name", "Center", "Opp"]]]
								elif "choose up to  character in your waiting room" in t:
									if "return it to your hand" in t:
										if "all your  characters get + power" in t:
											return ["pay", "may", "cxcombo", "at", "do", [self.digit(a), "salvage", "Character", "upto", "show", "do", [-1, self.digit(a, 1), x, "power", "Trait", self.trait(a)]]]
								elif "choose up to  other of your character" in t or "choose up to  of your other character" in t:
									if "those characters get" in t:
										return ["pay", "may", "cxbombo", "at", "do", [self.digit(a), self.name(a, s='a'), x, "give", "Other", "upto"]]
									elif "return them to your hand" in t:
										return ["pay", "may", "cxcombo", "at", "do", [self.digit(a), "hander", "at", "Other", "upto"]]
								elif "choose  of your other characters and this" in t:
									if "they get the following ability" in t:
										return ["pay", "may", "at", "cxcombo", "do", [self.digit(a), self.name(a, s='a'), x, "give", "Other", "this"]]
								elif "search your deck for up to  level  or higher character with  or " in t:
									if "reveal it" in t and "put it in your hand" in t:
										return ["pay", "may", "cxcombo", "at", "do", [self.digit(a), "search", f"TraitL_{self.trait(a)}_{self.trait(a, 1)}_>={self.digit(a)}"], "upto", "show"]
								elif "draw up to  cards" in t:
									if "your opponent draws  card" in t:
										return ["pay", "may", "cxcombo", "at", "do", ["drawupto", self.digit(a), "do", ["draw", self.digit(a, 1), "opp"]]]
									else:
										return ["pay", "may", "cxcombo", "at", "do", ["drawupto", self.digit(a)]]
								elif "draw  card" in t:
									if "this gets + power" in t:
										return ["pay", "may", "cxcombo", "at", "do", ["draw", self.digit(a), "do", [0, self.digit(a, 1), x, "power"]]]
									else:
										return ["pay", "may", "cxcombo", "at", "do", ["draw", self.digit(a)]]
								elif "all your characters get" in t:
									if "get + power and + soul" in t:
										return ["pay", "may", "cxcombo", "at", "do", [-1, self.digit(a), x, "power", -1, self.digit(a, 1), x, "soul"]]
									elif "get + power" in t:
										return ["pay", "may", "cxcombo", "at", "do", [-1, self.digit(a), x, "power"]]
								elif "all your  characters get" in t:
									if "get + power" in t:
										return ["pay", "may", "cxcombo", "at", "do", [-1, self.digit(a), x, "power", "Trait", self.trait(a)]]
								elif "this gets + power and your opponent cannot use" in t:
									return ["pay", "may", "cxcombo", "at", "do", [0, self.digit(a), x, "power", "do", [-21, "[CONT] Your opponent cannot use \"[AUTO] Encore\" until end of turn.", x, "give"]]]
							elif "you may choose  cost  or lower character" in t:
								if "return it to hand" in t:
									if "in your opponent's center stage" in t:
										return ["pay", "may", "at", "do", [self.digit(a), "hander", "Opp", "Cost", f"<={self.digit(a, 1)}", "Center"]]
							elif "choose up to  other of your characters" in t:
								if "put it in stock" in t:
									if "choose  of your characters" in t:
										if "that character gets + power" in t:
											return [self.digit(a), "stocker", "Other", "upto", "at", "cxcombo", "do", [self.digit(a, 1), self.digit(a, 2), x, "power"]]
							elif "choose up to  of your other character" in t:
								if "put them in your memory" in t or "put it in your memory" in t:
									return [self.digit(a), "memorier", "Other", "upto", "extra", "at", "cxcombo", "do", [-21, self.name(a, s='at'), 3, "give", "expass", self.digit(a), "ex_ID="]]
							elif "choose up to  card in your opponent's waiting room" in t:
								if "put it on top of the deck" in t:
									if "this gets + power" in t:
										return [self.digit(a), "salvage", "", "opp", "Library", "top", "at", "show", "upto", "do", [0, self.digit(a, 1), x, "power"]]
									else:
										return [self.digit(a), "salvage", "", "opp", "Library", "top", "at", "show", "upto"]
							elif "look at the top card of your opponent's deck" in t:
								if "put it on the top or the bottom of your opponent's deck" in t:
									return [1, "looktop", "top", "bottom", "opp", "cxcombo", "at"]
							elif "you may deal  damage to your opponent" in t:
								return ["pay", "may", "cxbombo", "at", "cxcombo", "do", ["damage", self.digit(a), "opp"]]
							elif "choose  of your other characters" in t:
								if "that character gets + power" in t and "this gets + power" in t:
									return [self.digit(a), self.digit(a, 1), x, "power", "at", "Other", "do", [0, self.digit(a, 2), x, "power"]]
								elif "that character gets + power and the following ability" in t:
									return [self.digit(a), self.digit(a, 1), x, "power", "Other", "extra", "at", "do", [-16, self.name(a, s='a'), x, "give"]]
								elif "that character gets the following ability" in t:
									return [self.digit(a), self.name(a, s='a'), x, "give", "Other", "at"]
							elif "choose up to   in your waiting room" in t:
								if "return it to your hand" in t:
									if "this gets + power" in t:
										if "\" in your waiting room" in aa:
											return [self.digit(a), "salvage", f"Name=_{self.name(a, -1, s='n')}", "show", "at", "upto", "do", [0, self.digit(a, 1), x, "power"]]
							elif "deal  damage to your opponent" in t:
								if "this gets + power" in t:
									if "if you have  card named" in t:
										return ["damage", self.digit(a, 1), "opp", "cxcombo", "at", "do", [0, self.digit(a, 2), x, "power"]]
									else:
										return ["damage", self.digit(a), "opp", "cxcombo", "at", "do", [0, self.digit(a, 1), x, "power"]]
							elif "draw up to  cards" in t:
								if "and discard  card from your hand to the waiting room" in t:
									return ["drawupto", self.digit(a), "do", ["discard", self.digit(a, 1), ""]]
					elif "if a  climax is in your climax area" in t:
						if f"if a {cx[2].lower()} climax is in your climax area" in aa and r[0][-1] == cx[1][-1] and n in cx[1][-1]:
							self.ablt = 2
					elif "if it is the first turn of the player who went first" in t:
						if "you may attack with up to  characters during this turn" in t:
							return ["turn", 1, "at", "do", ["d_atk", self.digit(a)]]
					elif "if all your other characters have lower power than this" in t:
						if "this gets + power" in t:
							return [-2, "atkpwrchk", "lower", "self", "at", "do", [0, self.digit(a), x, "power"]]
					else:
						self.ablt = 2
						if "you may pay the cost" in t:
							if "if you have another card named  in your center stage" in t:
								if "deal  damage to your opponent" in t:
									return [1, "name", self.name(a, s="n"), "other", "Center", "at", "do", ["pay", "may", "do", ["damage", self.digit(a), "opp"]]]
							elif "choose up to  of your other characters" in t:
								if "put them in your waiting room" in t:
									if "deal x damage to your opponent" in t:
										if "x = the number of characters put in your waiting room" in t:
											return ["pay", "may", "at", "do", [self.digit(a), "waitinger", "Other", "upto", "extra", "do", ["damage", -16, "opp"]]]
						elif "you may choose  climax in your climax area" in t:
							if "put it in the stock" in t:
								return ["pay", "may", "at", "do", [self.digit(a), "stocker", "Climax", "upto"]]
						# elif "if you have  or fewer other character" in t:
						# 	if "you may put the top card of your deck in the waiting room" in t:
						# 		if "if it's a level  or lower character" in t:
						# 			if "put that character in any slot in the back stage" in t:
						# 				return [self.digit(a), "more", "", "other", "lower", "do", ["pay", "may", "do", ["mill", 1, "lvl", self.digit(a, 1), "any", "extra", "if", "do", [-16, "salvage", "", "Stage", "Back"]]]]
						elif "choose   on your stage" in t:
							if "return it to your hand" in t:
								if "\" on your stage" in self.a_replace(a):
									return [self.digit(a), "hander", "Name=", self.name(a, s='n')]
						elif "rest all your other standing characters" in t or "rest all your other stand characters" in t:
							return [-1, "rest", "Stand", "Other", "at"]
			elif "when this is front attacked" in t and "\"[auto] when this is front attacked" not in aa:
				if r[0] != r[1] and n in r[1][-1] and r[0][-1] != r[1][-1] and r[0] in baind[1] and r[1] in baind[0] and "f" in atk:
					self.ablt = 2
			elif "when this direct attacks" in t:
				if r[0] == r[1] and n in r[1][-1] and r[0] in baind[0] and "d" in atk:
					if "if  is in the climax area" in t:
						if f"if \"{cx[0].lower()}\" is in the climax area" in aa and r[0][-1] == cx[1][-1] and n in cx[1][-1]:
							self.ablt = 2
					else:
						self.ablt = 2
			elif "when this front attack" in t:
				if r[0] == r[1] and n in r[1][-1] and r[0] in baind[0] and "f" in atk:
					self.ablt = 2
			elif "when this side attacks" in t:
				if r[0] == r[1] and n in r[1][-1] and r[0] in baind[0] and "s" in atk:
					if "\" is in the climax area" in aa or "\" is in your climax area" in aa:
						if (f"\"{cx[0].lower()}\" is in the climax area" in aa or f'\"{cx[0].lower()}\" is in your climax area' in aa) and r[0][-1] == cx[1][-1] and n in cx[1][-1]:
							if "you may pay the cost" in t:
								if "deal  damage to your opponent" in t:
									return ["pay", "may", "at", "do", ["damage", self.digit(a), "opp"]]
							elif "this gets + power" in t:
								if "choose the character opposite this" in t:
									if "that character gets " in t and "character gets \"[" in aa:
										return [0, self.digit(a), x, "power", "at", "do", [1, self.name(a, s='a'), x, "give", "Opposite"]]
			elif "when your other  character is front attacked" in t or"when your other  characters is front attacked" in t:
				if r[0] != r[1] and n in r[1][-1] and r[0][-1] != r[1][-1] and r[0] not in baind and r[1] in baind[0] and self.trait(a) in trop[1] and "f" in atk:
					self.target = baind[1]
					self.ablt = 2
			elif "when your other character is front attacked" in t:
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
			elif "when your other  character attacks" in t or "when another of your  character attacks" in t:
				if r[0] != r[1] and r[0][-1] == r[1][-1] and n in r[1][-1] and self.trait(a) in tr[1] and r[1] in baind[0] and r[0] not in baind and atk != "":
					self.ablt = 2
			elif "when your other character with  or " in t and "in name is front attacked" in t:
				if r[0] != r[1] and r[0][-1] != r[1][-1] and r[0] not in baind and r[1] in baind[0] and "f" in atk and n in r[1][-1] and (self.name(a, s="n") in nmop[1] or self.name(a, 2, s='n') in nmop[1]) and r[0][-1] == baind[1][-1]:
					self.ablt = 9
			elif "when another of your characters with  in its card name is frontal attacked" in t:
				if r[0] != r[1] and r[0][-1] != r[1][-1] and r[0] not in baind and r[1] in baind[1] and "f" in atk and n in r[1][-1] and self.name(a, s="a") in nmop[1]:
					self.ablt = 9
			elif "when your character direct attacks" in t:
				if r[0][-1] == r[1][-1] and n in r[1][-1] and r[1] in baind[0] and "d" in atk:
					self.ablt = 9
		elif "Trigger" in p:
			if "when your character's trigger check reveals a climax" in t or "when the trigger check of this reveals a climax" in t:
				if n in r[0][-1] and r[0][-1] == r[1][-1] and r[0] != r[1] and "Climax" in ty[0] and ty[0] == r[2]:
					if "if the trigger icons of that card are" in t or "if that card's trigger icon is" in t or "in its trigger icon" in t or "if that card has a " in t:
						if (("soulsoul trigger icons" in t or "icon is soulsoul" in t) and len([s for s in ty[1] if s == "soul"]) == 2) or ("trigger icon is door" in t and "door" in ty[1]) or ("trigger icon is bounce" in t and "bounce" in ty[1]) or ("trigger icon is stock" in t and "stock" in ty[1]) or ("trigger icon is draw" in t and "draw" in ty[1]) or (("trigger icon is gate" in t or "with gate in its trigger icon" in t) and "gate" in ty[1]) or ("card has a treasure icon" in t and "treasure" in ty[1]):
							self.ablt = 9
					else:
						self.ablt = 9
					if "when the trigger check of this reveals a climax" in t and r[0] not in baind[0]:
						self.ablt = 0
		elif "Counter" in p:
			if pp < 0:
				if "at the beginning of counter step during your opponent's turn" in t:
					if n not in r[0][-1]:
						self.ablt = 3
						# if "you may pay the cost" in t:
						# 	if "choose  level  or higher character battling this" in t:
						# 		if "put it on bottom of the deck" in t:
						# 			return ["pay", "may", "a1", "do", [self.digit(a), "decker", "bottom", "Battle", "Opp", "Level", f">={self.digit(a, 1)}"]]
			elif pp == 0:
				if "when you use this's " in t or "when you use the backup of this" in t:
					if r[0] == r[1] and r[0] == act:
						self.ablt = 2
				elif "when you use a backup" in t:
					if r[0] != r[1] and r[0][-1] == r[1][-1] and r[1] == act:
						self.ablt = 9
		elif "Damage" in p:
			if "when the damage dealt by this is cancelled" in t or "when the damage dealt by this becomes canceled" in t or "when damage dealt by this is canceled" in t or "when damage dealt by this is cancelled" in t or "when this's damage is cancelled" in t:
				if r[0] == r[1] and n in r[1][-1] and cnc[0] not in r[0][-1] and cnc[1]:
					if "during the turn that this is placed on the stage from your hand" in t or "during the turn that this is placed on stage from your hand" in t or "during the turn this is placed from hand to the stage" in t:
						if z[0] == z[1] and "Hand" in pos[0] and any(field in pos[1] for field in self.stage):
							self.ablt = 2
					else:
						self.ablt = 2

					if "\" is in your climax area" in aa:
						self.ablt = 0
						if f"\"{cx[0].lower()}\" is in your climax area" in aa and r[0][-1] == cx[1][-1] and n in cx[1][-1]:
							self.cx = True
							self.ablt = 2
			elif "when your level  or higher character's damage is cancelled" in t:
				if r[0][-1] == r[1][-1] and n in r[0][-1] and cnc[0] not in r[0][-1] and cnc[1] and lvop[0]>=self.digit(a):
					self.cond[0]+=1
					self.ablt = 9
		elif "Battle" in p:
			if ("when this's battle opponent becomes reverse" in t and "\"[auto] when this's battle" not in aa) or ("when the battle opponent of this becomes reverse" in t and "\"[auto] when the battle opponent" not in aa) or ("when this character's battle opponent becomes reverse" in t and "\"[auto] when this character's battle opponent" not in aa):
				if r[0] != r[1] and r[0][-1] != r[1][-1] and r[0] in baind and r[1] in baind and suop[1] == "Reverse": #(n == "1" and v[1] == "Reverse") or (n == "2" and v[0] == "Reverse")
					if r[0] == baind[0]:
						self.target = baind[1]
					elif r[0] == baind[1]:
						self.target = baind[0]
					self.ablt = 2

					if ("\" is in the climax area" in aa or '\" is in your climax area' in aa) and (("\" is in the climax area" in aa and f"\"{cx[0].lower()}\" is in the climax area" not in aa) or ('\" is in your climax area' in aa and f'\"{cx[0].lower()}\" is in your climax area' not in aa) or r[0][-1] != cx[1][-1]):
						self.ablt = 0
					elif (f"\"{cx[0].lower()}\" is in the climax area" in aa or f'\"{cx[0].lower()}\" is in your climax area' in aa) and r[0][-1] == cx[1][-1]:
						if "you have  or more other  characters" in t:
							if "draw up to  cards" in t:
								if "discard  card from your hand to the waiting room" in t:
									return [self.digit(a), "more", f"Trait", self.trait(a), "other", "at", "cxcombo", "do", ["drawupto", self.digit(a, 1), "do", ["discard", self.digit(a, 2), ""]]]
						elif "you may pay the cost" in t:
							if "return all your standing characters in your center stage to your hand" in t:
								if "if at least  character was returned this way" in t:
									if "choose up to  " in t and "in your hand and put it in an empty slot on the stage" in t:
										return ["pay", "may", "at", "cxcombo", "do", [-1, "hander", "Standing", "Center", "if", self.digit(a), "do", ["discard", self.digit(a), f"Name=_{self.name(a, -1, s='n')}", "Stage", "Open", "upto"]]]
							if "choose up to  card named " in t and "in your hand" in t:
								if "put it on the stage position that this was on" in t:
									return ["pay", "may", "at", "cxcombo", "do", ["discard", self.digit(a), f"Name=_{self.name(a, -1, s='n')}", "Stage", "upto", "Change"]]
							elif "deal x damage to your opponent" in t:
								if "where x = the cost of that character" in t:
									return ["pay", "may", "at", "cxcombo", "do", ["damage", csop[1], "opp"]]
						elif "you may put that character in clock" in t:
							return ["pay", "may", "at", "do", [-3, "clocker", "target", r[1], "Opp"]]
						elif "choose up to  " in t and "in your waiting room" in t:
							if "return it to your hand" in t:
								if "reveal the top card of your deck" in t:
									if "if it's a  character, put it in your hand" in t:
										return [self.digit(a), "salvage", f"Name=_{self.name(a, -1, s='n')}", "upto", "at", "cxcombo", "do", [-9, "reveal", "Trait", self.trait(a), "do", ["draw", 1]]]
						elif "put up to  cards from top of your deck in your stock" in t:
							return ["drawupto", self.digit(a), "Stock"]
						elif "this gets the following ability" in t:
							return [0, self.name(a, s='a'), x, "give"]
					elif "if there is a climax in your climax area" in t:
						self.ablt = 0
						if (n == "1" and cx[1] != "" and cx[1][-1] == r[0][-1]) or (n == "2" and cx[4] != "" and cx[4][-1] == r[0][-1]):
							self.ablt = 2
					elif "you may pay the cost" in t:
						if "return all cards in your opponent's waiting room in your opponent's deck, and your opponent shuffles his or her deck" in t:
							return ["pay", "may", "at", "do", [-1, "shuffle", "opp"]]
						elif "choose   character or character with  in its card name from your waiting room" in t:
							if "return it to your hand" in t:
								return ["pay", "may", "at", "do", [self.digit(a), "salvage", f"TraitN_{self.trait(a)}_{self.name(a, s='ability')}", "or", "show"]]
						elif "search your deck for up to  character with no traits" in t:
							if "reveal it" in t and "put it in your hand" in t:
								return ["pay", "may", "at", "do", [self.digit(a), "search", f"Trait_", "upto", "show"]]
						elif "stand this" in t:
							if "during the turn this is placed from hand to the stage" in t and z[0] == z[1]:
								return ["pay", "may", "at", "do", [0, "stand"]]
							elif "if the number of your other  characters is  or more" in t:
								if "this ability activates up to  time per turn" in t:
									return [self.digit(a, 1), "more", "Trait", self.trait(a), "other", f"a{self.digit(a)}", "do", ["pay", "may", "do", [0, "stand"]]]
								else:
									return [self.digit(a), "more", "Trait", self.trait(a), "other", "at", "do", ["pay", "may", "do", [0, "stand"]]]
						elif "your opponent returns all cards in their waiting room to the deck" in t:
							return ["pay", "may", "at", "do", [-1, "shuffle", "opp"]]
					elif "you may put it on top of the deck" in t or "you may put that character on the top of your opponent's deck" in t:
						return ["pay", "may", "at", "do", [-3, "decker", "top", "target", r[1], "Opp"]]
					elif "you may send this to memory" in t or "you may put this in your memory" in t:
						if "at the start of your next" in t or "at the beginning of your next" in t:
							return ["pay", "may", "at", "do", [0, "memorier", "if", 1, "do", [-21, self.name(a, s='at'), 3, "give"]]]
					elif "during the turn this is placed from hand to the stage" in t and z[0] == z[1]:
						if "if so, stand this" in t:
							return [0, "stand", "may", "played"]
					elif "put up to x cards from top of your deck in your stock" in t:
						if "x = level of that character" in t:
							return ["drawupto", lvop[1], "Stock"]
					elif "choose up to  of opponent's characters" in t:
						if "that character gets - power" in t:
							if "send this to memory" in t:
								return [self.digit(a), self.digit(a, 1), x, "power", "Opp", "upto", "at", "do", [0, "[AUTO] At the end of the turn, put this card into your memory.", -3, "AUTO", "give"]]

					if "during your turn" in t:
						if n not in r[0][-1]:
							self.ablt = 0
			elif ("when the battle opponent of your other" in t or "when your other character's battle opponent" in t) and "becomes reverse" in t:
				if "other character becomes reverse" in t or "other character's battle opponent becomes reverse" in t:
					if r[0] != r[1] and r[0][-1] != r[1][-1] and v[1] == "Reverse" and r[0] not in baind and r[1] in baind:
						self.ablt = 2
				elif ("other  becomes reverse" in t or "other character with  in name becomes reverse" in t) and ("\" becomes reverse" in aa or "\" in name becomes reverse" in aa):
					if r[0] != r[1] and r[0][-1] != r[1][-1] and v[1] == "Reverse" and r[0] not in baind and ((r[1] in baind[1] and self.name(a, s='n') in nmop[0]) or (r[1] in baind[0] and self.name(a, s='n') in nmop[1])):
						self.ablt = 9
						if "you may draw  card" in t:
							if "discard  card from hand to the waiting room" in t:
								return ["drawupto", self.digit(a), "if", self.digit(a), "do", ["discard", self.digit(a, 1), ""]]
			elif "when this's level  or higher battle opponent becomes reverse" in t or "when a level  or higher battle opponent of this becomes reverse" in t or "when a level  or higher battle opponent of this becomes reverse" in t:
				if r[0] != r[1] and r[0][-1] != r[1][-1] and v[1] == "Reverse" and r[0] in baind and r[1] in baind and ((r[0] == baind[0] and lvop[1] >= self.digit(a)) or (r[0] == baind[1] and lvop[0] >= self.digit(a))):
					self.ablt = 2
					self.cond[0] += 1
					if "you may put the top card of your deck in your stock" in t:
						return ["pay", "may", "at", "do", ["stock", 1]]
					elif "you may draw  card" in t:
						return ["pay", "may", "at", "do", ["draw", self.digit(a, 1)]]
					elif "you may pay cost" in t or "you may pay the cost" in t:
						if "choose   character in your waiting room" in t:
							if "return it to your hand" in t:
								return ["pay", "may", "at", "do", [self.digit(a), "salvage", f"Trait_{self.trait(a)}", "show"]]
						elif "put the top card of your clock in the waiting room" in t:
							return ["pay", "may", "at", "do", ["heal", 1, "top"]]
			elif "when a level  or higher battle opponent of another character of yours becomes reverse" in t:
				if r[0] != r[1] and r[0][-1] != r[1][-1] and v[1] == "Reverse" and r[1] in baind and r[0] in baind and ((r[1] == baind[1] and lvop[1] >= self.digit(a)) or (r[1] == baind[0] and lvop[0] >= self.digit(a))):
					if "you may pay the cost" in t:
						if "put that character in your clock" in t:
							return ["pay", "may", "at", "do", [-3, "clocker", "target", r[1], "Opp"]]
			elif "when your other character becomes reverse" in t or "when another of your characters becomes reverse" in t:
				if "in battle" in t:
					if r[0] != r[1] and r[0][-1] == r[1][-1] and r[0] not in baind and r[1] in baind and ((n == "1" and v[0] == "Reverse") or (n == "2" and v[1] == "Reverse")):  # and batt:
						self.ablt = 9
						self.target = r[1]
						if "if this is in the back stage" in t:
							if "Back" not in pos[1]:
								self.ablt = 0
			elif "when another of your  characters becomes reverse in battle" in t or "when another of your  character becomes reverse in battle" in t:
				if r[0] != r[1] and r[0][-1] == r[1][-1] and v[1] == "Reverse" and r[1] in baind and r[0] not in baind and self.trait(a) in tr[1]:
					self.ablt = 9
			elif "when this becomes reverse in battle" in t or "when this becomes reverse while battling" in t:
				if r[0] == r[1] and v[0] == "Reverse" and ((suop[0] == "Reverse" and r[0] in baind[0]) or (suop[1] == "Reverse" and r[0] in baind[1])):  # and batt:
					if r[0] == baind[0]:
						self.target = baind[1]
					elif r[0] == baind[1]:
						self.target = baind[0]
					self.ablt = 2
					if "your opponent may " in t:
						if "put the top card of your opponent's deck into his or her stock" in t:
							return ["pay", "may", "opp", "oppmay", "at", "do", ["stock", 1]]
						elif "draw  card" in t:
							return ["pay", "may", "opp", "oppmay", "at", "do", ["draw", 1]]
					elif "you may return this to hand" in t:
						if "if the number of cards in your hand = or lower than the number of cards in your opponent's hand" in t:
							return [0, "cards", "HandvsOpp", "=lower", "at", "do", ["pay", "may", "do", [0, "hander"]]]
						else:
							return ["pay", "may", "do", [0, "hander"]]
					elif "you may reveal up to  cards from top of your deck" in t:
						if "if you reveal at least  card this way" in t:
							if "choose up to   character among them" in t:
								if "put it in your hand" in t:
									if "discard  card from your hand to the waiting room" in t:
										return ["pay", "may", "at", "do", ["drawupto", self.digit(a), "Reveal", "if", self.digit(a, 1), "do", [self.digit(a, 2), "search", f"Trait_{self.trait(a)}", "Reveal", "show", "upto", "do", ["discard", self.digit(a, 3), ""]]]]
					elif "you may pay the cost" in t:
						if "put this in your memory" in t or "send this to memory" in t:
							return ["pay", "may", "at", "do", [0, "memorier"]]
						elif "rest this" in t:
							if "reverse the battle opponent of this" in t:
								if r[0] == baind[0]:
									bopp = baind[1]
								elif r[0] == baind[1]:
									bopp = baind[0]
								return ["pay", "may", "at", "do", [0, "rest", "do", [-3, "reverser", "target", bopp, "Opp"]]]
					elif "level of its battle opponent is  or lower" in t or "this's battle opponent is level  or lower" in t or "level of the battle opponent of this is  or lower" in t:
						if (r[0] == baind[0] and lvop[1] <= self.digit(a)) or (r[0] == baind[1] and lvop[0] <= self.digit(a)):
							self.ablt = 2

					if "during your opponent's turn" in t:
						if n in r[0][-1]:
							self.ablt = 0
			elif "when this becomes reversed" in t or "when this becomes reverse" in t:
				if r[0] == r[1] and ((n == "1" and v[0] == "Reverse") or (n == "2" and v[1] == "Reverse")):  # and r[0] in baind:
					if r[0] == baind[0]:
						self.target = baind[1]
					elif r[0] == baind[1]:
						self.target = baind[0]
					if "level of its battle opponent is  or lower" in t or "this's battle opponent is level  or lower" in t or "level of the battle opponent of this is  or lower" in t:
						if (r[0] == baind[0] and lvop[1] <= self.digit(a)) or (r[0] == baind[1] and lvop[0] <= self.digit(a)):
							self.ablt = 2
					elif "level of its battle opponent is same or lower than this" in t or "level of this's battle opponent is lower than or equal to the level of this" in t or "level of its battle opponent = or lower than the level of this" in t or "level of its battle opponent is lower than or equal to the level of this" in t:
						if (r[0] == baind[0] and lvop[1] <= lvop[0]) or (r[0] == baind[1] and lvop[0] <= lvop[1]):
							self.ablt = 2
					elif "level of the battle opponent of this is higher than the level of your opponent" in t or "level of this's battle opponent is higher than your opponent's level" in t:
						self.ablt = 2
		elif "Encore" in p:
			if pp < 0:
				if "at the beginning of the encore step" in t or "at the start of encore step" in t:
					self.ablt = 3

					if "if those characters are on stage" in t:
						if "return them to your deck" in t:
							return [-20, "decker", "a1"]
					# elif "return this to your deck" in t:
					# 	return [0, "decker", "a1"]
					# elif "you may return this in your hand" in t:
					# 	return ["pay", "may", "a1", "do", [0, "hander"]]
				elif "at the start of your encore step" in t or "at the beginning of your encore step" in t:
					if n in r[0][-1]:
						if "\" is in the climax area" in aa or "\" is in your climax area" in aa or "\" on your climax area" in aa:
							if (f"\"{cx[0].lower()}\" is in the climax area" in aa or f'\"{cx[0].lower()}\" is in your climax area' in aa or f'\"{cx[0].lower()}\" on your climax area' in aa) and r[0][-1] == cx[1][-1] and n in cx[1][-1]:
								if "you may put this in your memory" in t:
									if "at the beginning of your next" in t:
										return ["pay", "may", "a1", "do", [0, "memorier", "if", 1, "do", [-21, self.name(a, s='at'), 3, "give"]]]
						else:
							self.ablt = 3
							if "if this is rest" in t:
								if v[0] != "Rest":
									self.ablt = 0
							if "you may pay the cost" in t:
								# if "you have no other rested characters in your center stage" in t:
								# 	if "rest this" in t:
								# 		return [0, "Rest", "Center", "other", "a1", "do", ["pay", "may", "do", [0, "rest"]]]
								if "choose  of your characters and this" in t:
									if "put them in your memory" in t:
										if "at the beginning of your next" in t:
											return ["pay", "may", "a1", "do", [self.digit(a), "memorier", "Other", "this", "extra", "do", [-21, self.name(a, s='at'), 3, "give", "expass", self.digit(a) + 1, "ex_ID="]]]
		elif "End" in p:
			if pp > 0:
				if "at the end of of your opponent's next turn" in t:
					if n!=r[0][-1] and z[0]!=z[1]:
						self.ablt = 3
				elif "at the end of the turn" in t:
					self.ablt = 3
					if "you may place the previously chosen character face up underneath this as a marker" in t:
						return ["pay", "may", "a1", "do", [-38, "marker", "", "Stage", "face-up"]]
					elif "put this in your memory" in t:
						return [0, "memorier"]
					elif "put this in your waiting room" in t:
						return [0, "waitinger"]
					elif "put this in your clock" in t:
						return [0, "clocker"]
					elif "put this in your stock" in t:
						return [0, "stocker"]

		if self.ablt:
			if passed:
				self.ablt = self.ablt*-1
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

		if "you may pay the cost" in t or ("you may " in t and "you may not " not in t):
			e = ["pay", "may"]
			if "may pay the cost" not in t and "may pay cost" not in t:
				self.ee = True

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

		if "this ability activates up to once per turn" in t:
			if "a1" not in p:
				p.append("a1")
			if "played" in p:
				p.remove("played")
		elif "this ability activates up to  time per turn" in t:
			self.cond[0] += 1
			if f"a{self.digit(a)}" not in p:
				p.append(f"a{self.digit(a)}")
			if "played" in p:
				p.remove("played")

		ef = self.condition(a, t, aa)
		tempcond = list(self.cond)

		if multi:
			n = self.name(a, -1, s="n")
			cv = self.convert(n, self.text(n), self.a_replace(n))
		else:
			cv = self.convert(a, t, aa)

		if e:
			if self.ee and "upto" not in cv and all(ss not in cv for ss in ["draw","heal","trigger","shuffle","hander","salvage"]):
				if "reveal" in cv:
					if "drawupto" in cv[cv.index("do")+1] and "upto" in cv[cv.index("do")+1]:
						pass
					else:
						if "upto" not in cv[cv.index("do")+1]:
							cv[cv.index("do")+1].append("upto")
						temp = cv[cv.index("do")+1]
						cv.remove(temp)
						cv = cv + [e + ["do", temp]]
				elif "mill" in cv and "stocker" in cv[cv.index("do")+1]:
					temp = cv[cv.index("do")+1]
					cv.remove(temp)
					cv = cv + [e + ["do", temp]]
				elif "if" in cv:
					cv.insert(cv.index("if"), "upto")
					if "waitinger" in cv:
						pass
					else:
						cv = e + ["do", cv]
				else:
					cv = e + ["do", cv + ["upto"]]
			else:
				cv = e + ["do", cv]
			e = []

		if any(nn in t for nn in self.dont_text) and not self.play(a):
			for nn in self.dont_text:
				if nn in t:
					self.cond = [0, 0, 0]
					a = a[a.lower().index(nn):]
					aa = aa.split(nn)[1]
					t = t.split(nn)[1]
					cv.extend(["dont", self.convert(a, t, aa)])
					break

		if ef and cv:
			ef.append(cv)
		else:
			ef = cv

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
			if "do" in d:
				if "if" in d:
					d.insert(d.index("if"), p[0])
				else:
					d.insert(d.index("do"), p[0])
				if len(p) == 2:
					d.insert(d.index(p[0]), p[1])
			else:
				d.append(p[0])
				if len(p) == 2:
					d.append(p[1])

		return d

	def condition(self, a, t, aa):
		c = []
		if "if there are no other rested characters in your center stage" in t or "if you have no other rested characters in your center stage" in t or "if you have no other rested characters in the center stage" in t:
			c = [0,"Rest","Center","other"]
		elif "if the number of cards in your deck is  or less" in t:
			c = [self.digit(a), "more", "Library", "lower"]
			self.cond[0] += 1
		elif "if the number of cards in your stock is  or less" in t or "if your stock has  or less cards" in t:
			self.cond[0] += 1
			c = [self.digit(a), "cards", "Stock", "lower"]
		elif "if the character opposite this has no traits" in t:
			c = ["opposite", "#traits", 0, "#lower"]
		elif "if the character opposite this is level  or higher" in t or "if the level of the character opposite this is  or higher" in t:
			self.cond[0] += 1
			c = ["opposite", "olevel", self.digit(a)]
		elif "if the character opposite this is level " in t:
			self.cond[0] += 1
			c = ["opposite", "olevel", self.digit(a),"=="]
		elif "if there are no markers underneath this" in t or "if there are no markers under this" in t:
			c = [0, "markers", "lower", "under"]
		elif "if the level of the battle opponent of this is higher than the level of your opponent" in t or "if the level of this's battle opponent is higher than your opponent's level" in t:
			c = ["plevel", "antilvl", self.target, "opp"]
		elif "if your level is  or higher" in t or "if you are level  or higher" in t:
			self.cond[0] += 1
			c = ["plevel", self.digit(a)]
		elif "if the total level of the cards in your level is  or higher" in t:
			self.cond[0] += 1
			c = ["experience", self.digit(a)]
		elif "if  is in your level zone" in t or "and  is in your level zone" in t:
			c = ["experience",1,"Name=",self.name(a,self.cond[1],s='n')]
			self.cond[1] += 2
		elif "if your memory has  or more cards" in t or "if there are  or more cards in your memory" in t or "if you have  or more cards in your memory" in t or "if you have  or more cards in memory" in t:
			self.cond[0] += 1
			c = [self.digit(a), "more", "Memory"]
		elif "if the number of cards in your hand is  or more" in t or "if your hand has  or more cards" in t or "if you have  or more cards in your hand" in t:
			self.cond[0] += 1
			c = [self.digit(a), "more", "Hand"]
		elif "and your hand has  or less cards" in t:
			self.cond[0] += 1
			c = [self.digit(a), "more", "Hand", "lower"]
		elif "if there are fewer cards in your hand than your opponent's hand" in t:
			c = [0, "cards", "HandvsOpp", "lower"]
		elif "if there are cards in your memory" in t:
			c = [1, "more", "Memory"]
		elif "if you have  card in memory" in t:
			c = [self.digit(a),"more","Memory"]
			self.cond[0] += 1
		elif "if you have a character with  in name" in t:
			self.cond[1] += 2
			c = [1, "more", "Name", self.name(a, s='n')]
		elif "if you have another character with  in the name" in t:
			self.cond[1] += 2
			if "\"backup\"" in aa:
				c = [1, "more", "Name", self.name(a, 2, s='n'), "other"]
			else:
				c = [1, "more", "Name", self.name(a, s='n'), "other"]
		elif "if you have another character with  or " in t and "» or «" in aa:
			self.cond[2] += 2
			c = [1, "more", "Trait", f"{self.trait(a)}_{self.trait(a, 1)}", "other"]
		elif "if you have  or more characters with  or " in t and "» or «" in aa:
			self.cond[0] += 1
			self.cond[2] += 2
			c = [self.digit(a), "more", "Trait", f"{self.trait(a)}_{self.trait(a, 1)}"]
		elif "if you have  or more other characters with  or " in t and  "» or «" in aa:
			self.cond[0] += 1
			self.cond[2] += 2
			c = [self.digit(a), "more", "Trait", f"{self.trait(a)}_{self.trait(a, 1)}","other"]
		elif "if there are  or more  characters in your memory" in t:
			self.cond[0] += 1
			self.cond[2] += 1
			c = [self.digit(a), "more", "Trait", self.trait(a), "Memory"]
		elif "if you have  or more other  characters" in t or "and you have  or more other  character" in t or "if the number of your other  characters is  or more" in t:
			self.cond[0] += 1
			self.cond[2] += 1
			c = [self.digit(a), "more", "Trait", self.trait(a), "other"]
		elif "if you have  or fewer other  characters" in t:
			self.cond[0] += 1
			self.cond[2] += 1
			c = [self.digit(a), "more", "Trait", self.trait(a), "other", "lower"]
		elif "if you have  or less other character" in t or "if the number of other characters you have is  or less" in t or "if you have  or fewer other character" in t:
			self.cond[0] += 1
			c = [self.digit(a), "more", "other", "lower"]
		elif "if the number of  characters you have is  or more" in t or "if you have  or more  character" in t or "if the number of your other  characters is  or more" in t or "and you have  or more  characters" in t:
			self.cond[0] += 1
			self.cond[2] += 1
			c = [self.digit(a), "more", "Trait", self.trait(a)]
		elif "if the number of your other  characters you have is  or more" in t:
			self.cond[0] += 1
			self.cond[2] += 1
			c = [self.digit(a), "more", "Trait", self.trait(a),"other"]
		elif "if  is in your memory" in t:
			self.cond[1] += 2
			if "\"backup\"" in aa:
				c = [1, "more", "Name", self.name(a, 2, s='n'), "Memory"]
			else:
				c = [1, "more", "Name", self.name(a, s='n'), "Memory"]
		elif "if you have another  character" in t or "and you have another  character" in t:
			self.cond[2] += 1
			c = [1, "more", "Trait", self.trait(a), "other"]
		elif "if your opponent has a \"" in aa or "if your opponent has a character named \"" in aa:
			c = [1, "more", "Name=", self.name(a,s='n'),"opp"]
			self.cond[1]+=1
		elif "if you have a  character" in t:
			self.cond[2] += 1
			c = [1, "more", "Trait", self.trait(a)]
		elif "if you have another ," in t or "and you have another ," in t:
			self.cond[1] += 2
			c = [1, "more", "Name", self.name(a, 2, s='n'), "other"]
		elif "if you have no other character" in t:
			c = [0, "more", "Character", "other", "lower"]

		if c:
			c.append("do")
			return c
		else:
			return []

	def convert(self, a, t, aa):
		if "until the next end of your opponent's turn" in t or "until the end of your opponent's next turn" in t or "until end of your opponent's next turn" in t:
			x = 2
		elif "for the turn" in t or "until end of turn" in t:
			x = 1
		else:
			x = -1


		b = []
		c = []
		cc = False
		cd = []
		d = []
		e = []
		f = []
		g = []
		h = []

		if ("put the top card of your deck" in t and ( "deck in your stock" in t or "deck into stock" in t or "deck to your stock" in t)) or "choose the top card of your deck and put it in your stock" in t:# or "put up to  card from the top of your deck to your stock" in t:
			f = ["stock", 1]
		elif "put up to  card from the top of your deck to your stock" in t:
			f = ["stock",1,"upto"]
		elif "your opponent declares  or  or  or " in t:
			f = ["numbers", (self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), self.digit(a, self.cond[0] + 2), self.digit(a, self.cond[0] + 3)), "oppturn"]
			self.cond[0] += 4
		elif self.ablt < 0 and "your opponent puts that character from his or her memory in any slot on the stage" in t:
			f = [-38, "msalvage", "", "Stage","Opp", "oppturn", "opp"]

		if "put the top  cards of your deck in your waiting room" in t or "put the top  cards of your deck in the waiting room" in t:
			d = ["mill", self.digit(a, self.cond[0]),"top"]
			self.cond[0] += 1
			if "if all cards put in the waiting room this way are  characters" in t or "if all those cards are  characters" in t:
				d += ["Trait", self.trait(a), "if", "all"]
				self.cond[2] += 1
			elif "if there were at least  climax card among them" in t or "if there is at least  climax card among them" in t:
				d += ["if", "Climax", self.digit(a, self.cond[0])]
				self.cond[0] += 1
				t = t.split("if there were at least  climax card among them")[1]
			elif "if there is a level  or lower character among those cards" in t:
				d.extend(["if", "lvl", self.digit(a,self.cond[0]),"lower","Character","any"])
				self.cond[0] += 1
			elif "if there were at least  level  or higher card among them" in t:
				if self.cond[0] == 1:
					d.extend(["if", "lvl", self.digit(a,self.cond[0]+1),"any"])
				self.cond[0] += 1

			if "x = the total level of the cards put in your waiting room" in t or "x equals the number of level  or lower characters moved to the waiting room" in t:
				d += ["if", "extra"]
			elif "x = the number of  characters among those cards " in t or "x =  times # of  characters among those cards" in t:
				d += ["pwr", "x#", "ctrait", self.trait(a,self.cond[2]), "if", "do"]
				self.cond[2]+=1
		elif "put the top card of your deck in your waiting room" in t or "put the top card of your deck in the waiting room" in t:
			d = ["mill", 1, "top", "extra", "if"]
			if "if that card's level is the number your opponent declared" in t:
				d.remove("if")
				d += ["sameoppnum", "if"]
				if "draw up to x cards" in t:
					d += ["do", ["drawupto", "x"]]
					if "x = the number your opponent declared +" in t:
						if "do" in d:
							d[d.index("do") + 1] += ["xsodlevel+", self.digit(a, self.cond[0]), "plchoose"]
			elif "that card is a  character" in t or "if it's a  character" in t:
				d.remove("if")
				d += ["Trait", self.trait(a, self.cond[2]), "any", "if"]
			elif "that card is a level  or lower character" in t or "if it's a level  or lower character" in t:
				d += ["lvl", self.digit(a, self.cond[0]), "Character", "lower", "any", "if"]
				if "put that character on any position of your back stage" in t or "put that character in any slot in the back stage" in t:
					d += ["extra", "do", [-16, "salvage", "ID=_x", "Stage", "Back"]]
			elif "if it's level  or higher" in t:
				d += ["lvl", self.digit(a, self.cond[0]), "Character", "any", "if"]
				self.cond[0]+=1
		elif "put the bottom  cards of your opponent's deck into their waiting room" in t or "put the bottom  cards of your opponent's deck in their waiting room" in t or "put the bottom  cards of your opponent's deck in the waiting room" in t:
			d = ["mill", self.digit(a,self.cond[0]), "bottom", "opp"]
			self.cond[0] += 1
			if "x = the number of climax among those cards" in t or "x is the number of climax cards among those cards" in t or "x = # of climax cards among those cards" in t:
				d += ["if", "extra"]
		elif "put the top card of your opponent's stock in the waiting room" in t:
			d = ["distock", 1, "top", "opp", "if", 1]
		elif "flip over the top  cards of your deck" in t or "flip over  cards from the top of your deck" in t or ("reveal  cards from the top of your deck" in t and "put them in your waiting room" in t):  # and "put them in the waiting room" in t:
			if "if there is a climax with" in t and ("trigger icon among them" in t or "in its trigger icon among those cards" in t):
				d = ["brainstorm", self.digit(a), "Trigger", "", "any", 1]
				if "with draw in its trigger" in t or "with draw trigger" in t:
					d[3] = "draw"
			elif "if there is at least  climax card among them" in t:
				d = ["brainstorm", self.digit(a), "Climax", "any", 1]
			elif "if there is at least   among them" in t:
				d = ["brainstorm", self.digit(a), "Name=", self.name(a, s='n'), "any", self.digit(a, 1)]
				self.cond[0] += 1
				self.cond[1] += 2
			elif "x = the number of  characters revealed among those cards" in t or "x = the number of  characters revealed" in t:
				d = ["brainstorm", self.digit(a), "Trait", self.trait(a), "any", 0]
				self.cond[2] += 1
			elif "for each climax card revealed this way" in t or "for each climax revealed" in t or "x = number of climax cards revealed this way":
				d = ["brainstorm", self.digit(a), "Climax"]
			elif "for each  character revealed among those cards" in t:
				d = ["brainstorm", self.digit(a), "Trait", self.trait(a), "each"]
				self.cond[2] += 1
			self.cond[0] += 1
		elif "reveal the top card of your deck" in t:
			if "if it's either a  character or an event" in t:
				d = [-9, "reveal", "TraitEv", self.trait(a,self.cond[2])]
				self.cond[2]+=1
				if "put it in your hand" in t:
					d.extend(["do", ["draw", 1]])
			elif "if it's a climax card" in t or "if the revealed card is a climax" in t:
				d = [-9, "reveal", "Climax"]
				if "put it in your hand and discard  card from your hand to the waiting room" in t:
					d += ["do", ["draw", 1, "do", ["discard", self.digit(a), ""]]]
					self.cond[0] += 1
			elif "if that card is not a  character" in t or "if it's not a  character" in t or "revealed card is not a  character" in t:
				d = [-9, "reveal", "Trait", self.trait(a,self.cond[2]), "not", "if"]
				self.cond[2] += 1
				if "put it in your clock" in t:
					d.append("clock")
					d.remove("if")
				elif "at the beginning of your encore step" in t:
					d+= ["do", [0, self.name(a, s='ay'), 1, "give"]]
					t = t.split("at the beginning of your encore step")[0]
			elif "if that card is a  character" in t or "if it is a  character" in t or "if the revealed card is a  character" in t or "if that's a  character" in t or "if it's a  character" in t:
				d = [-9, "reveal", "Trait", self.trait(a, self.cond[2])]
				self.cond[2] += 1
				if "put it in your hand" in t:
					if "discard  card from your hand" in t or ("choose  card in your hand" in t and "put it in your waiting room" in t):
						d += ["do", ["draw", 1, "do", ["discard", self.digit(a), ""]]]
					else:
						d += ["do", ["draw", 1]]
				elif "put this in your memory" in t:
					d += ["do", [0, "memorier"]]
			elif "if it's a character with  in name" in t:
				d = [-9, "reveal", "Name", self.name(a,self.cond[1], s='n')]
				self.cond[1] += 1
				if "put it in your hand" in t:
					if "discard  card from your hand" in t or ("choose  card in your hand" in t and "put it in your waiting room" in t):
						d += ["do", ["draw", 1, "do", ["discard", self.digit(a), ""]]]
					else:
						d += ["do", ["draw", 1]]
			elif "if it's level  or lower" in t or "if that card is level  or lower" in t or "if it's a level  or lower character" in t:
				d = [-9, "reveal", "Level", self.digit(a), "lower"]
				self.cond[0] += 1
				if "put it in stock" in t or "put it in your stock" in t:
					d.extend(["do", ["stock", 1]])
				elif "put it in your hand" in t:
					d.extend(["do", ["draw", 1]])
			elif "if it's level  or higher" in t or "if that card is level  or higher" in t:
				d = [-9, "reveal", "Level", self.digit(a, self.cond[0])]
				self.cond[0] += 1
				if "put it in your hand" in t:
					if "discard  card from your hand" in t or ("choose  card in your hand" in t and "put it in your waiting room" in t):
						d.extend(["do", ["draw", 1, "do", ["discard", self.digit(a), ""]]])
					else:
						d.extend(["do", ["draw", 1]])
				elif "put it in stock" in t or "put it in your stock" in t:
					d.extend(["do", ["stock", 1]])
				elif "put it face down underneath this as a marker" in t or "put it face-down underneath this as marker" in t:
					d.extend(["do", [1, "marker", "top"]])
			else:
				if "x = the level of the revealed card" in t:
					d = [-9, "reveal", "continue"]
		elif "return all cards from your waiting room to your deck" in t or "return all cards in your waiting room to your deck" in t or "return all cards in your waiting room to the deck" in t:
			if "shuffle your deck" in t:
				d = [-1, "shuffle"]
		elif "choose up to  of your other  character" in t:
			if "stand it" in t:
				d = [self.digit(a, self.cond[0]), "stand", "Trait", self.trait(a, self.cond[2]), "Other", "upto"]
				self.cond[0] += 1
				self.cond[2] += 1

		if "you may declare \"" in aa:
			c = ["declare", "text", self.name(a, -1, s='n')]
		elif "you may swap a character in your waiting room with this" in t:
			c = [1,"salvage","Character","swap","Clock","upto","this"]
		elif "all players perform the following action" in t:
			c = ["perform", 1, self.name(a, s='p'), "both"]
		elif "perform a trigger check  times on the trigger step" in t or "perform trigger check  times during this attack's trigger step" in t:
			c = ["trigger", self.digit(a)]
		elif "perform  of the following  effects" in t or (("choose  of the following effects" in t or "choose  of the following  effects" in t) and "perform it" in t) or "perform the following  effects" in t:
			if "perform the following  effects" in t:
				c = ["perform", self.digit(a, self.cond[0]), "", "choice", self.digit(a, self.cond[0])]
			else:
				c = ["perform", self.digit(a, self.cond[0]), "", "choice", self.digit(a, self.cond[0] + 1)]
				self.cond[0]+=1
			if "following  effect" in t:
				rr = self.digit(a, self.cond[0])
			else:
				rr = int(a.count("\"") / 2)
				if "[CXCOMBO]" in a:
					rr -= 1
			for r in range(rr):
				if r == 0:
					c[2] += f"{self.name(a, self.cond[1], s='p')}"
					self.cond[1] += 2
				else:
					c[2] += f"_{self.name(a, self.cond[1], s='p')}"
					self.cond[1] += 2
		elif "perform the following action" in t:
			c = ["perform", 1, self.name(a, self.cond[1],s='p')]
			if "following action twice" in t or "following action 2 times" in aa:
				c.append("twice")
		elif "play  with your opponent until someone wins" in t and "play \"rock-paper-scissors\" with your opponent" in aa:
			c = ["janken"]
			if "winner draws  card" in t:
				c.extend(["winner", "do", ["draw", self.digit(a,self.cond[0])]])
		elif "your opponent cannot use any act of characters on his or her stage" in t:
			c = [-21, "[CONT] Your opponent cannot use any [ACT] of characters on his or her stage.", x, "give"]
		elif "draw up to  card" in t:
			c = ["drawupto", self.digit(a, self.cond[0])]
		elif "draw  card" in t:
			c = ["draw", self.digit(a, self.cond[0])]
			self.cond[0] += 1
			if "may draw  card" in t:
				c[0] = ("drawupto")
				c.append("upto")
			if "choose  card in your hand" in t or "discard  card from your hand" in t or "discard  card from hand" in t:
				if "put it in your waiting room" in t or "hand to the waiting room" in t or "discard it to the waiting room" in t:
					c += ["if", 1, "do", ["discard", self.digit(a, self.cond[0]), ""]]
			elif "choose  of your characters" in t:
				if "that character gets + power" in t:
					c += ["do", [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power"]]
		elif "return the top card of your stock to your hand" in t:
			c = [-17, "stsearch", "", "top"]
		elif "put x cards from the bottom of your opponent's deck into their waiting room" in t:
			if "x = the number of  characters you have" in t:
				c = ["mill", "x", "bottom", "opp", "xTrait", self.trait(a)]
		elif "put the top  cards of every player's deck in the waiting room" in t:
			c = ["mill", self.digit(a), "top", "do", ["mill", self.digit(a), "top", "opp"]]
		elif "put the top  cards of your opponent's deck in the waiting room" in t:
			c = ["mill", self.digit(a), "top", "opp"]
		elif "put the top card of your deck" in t and ("under this as marker" in t or "underneath this as a marker" in t):
			d = [1, "marker", "top"]
		elif "put up to  card from the top of your clock in your waiting room" in t:
			c = ["heal", self.digit(a,self.cond[0]),"top","upto"]
			self.cond[0]+=1
		elif "put the top card of your clock in your waiting room" in t or "put the top card of your clock in the waiting room" in t or "put the top card in your clock in your waiting room" in t or "put the top card of your clock to your waiting room" in t:
			c = ["heal", 1, "top"]
		elif "your opponent puts all of their stock into their waiting room" in t or "put all cards in your opponent's stock in your opponent's waiting room" in t or "put all cards in your opponent's stock in the waiting room" in t:
			if "puts the same number of cards from the top of their deck into their stock" in t or "your opponent puts the same number of cards from the top of your opponent's deck into his or her stock" in t or "your opponent puts the same number of cards from top of the deck in the stock" in t:
				c = ["distock", -1, "top", "opp", "count", "do", ["stock", "count", "opp"]]
		elif "put the top card of your opponent's clock into their waiting room" in t or "put the top card of your opponent's clock in the waiting room" in t:
			c = ["cdiscard", -17, "", "opp"]
			if "put that character in your opponent's clock" in t or "put that character in clock" in t:
				c += ["if", 1, "do", [-3, "clocker", "target", self.target, "Opp"]]
		elif "put that character on the stage position it was on as rest" in t or "put that character rest in the slot it was in" in t or "put that character rested in the slot it was in" in t:
			c = [-7, "revive", [self.target, "Stage"], "extra", "do", [-16, "rested"]]
		elif "put that character on the bottom of your opponent's deck" in t or "put that character on the bottom of the deck" in t or "put that character at the bottom of your opponent's deck" in t:
			c = [-3, "decker", "bottom", "target", self.target, "Opp"]
		elif "put that character in stock" in t:
			c = [-3, "stocker", "target", self.target, "Opp"]
			if "put the bottom card of your opponent's stock in the waiting room" in t:
				c.extend(["replace","bottom"])
		elif "put that character in your opponent's memory" in t:
			c = [-3, "memorier", "target", self.target, "Opp"]
		elif "put that character in your opponent's clock" in t:
			c = [-3, "clocker", "target", self.target, "Opp"]
		elif "reverse that character" in t:
			c = [-3, "reverser", "target", self.target, "Opp"]
		elif "put  marker underneath this in your stock" in t:
			c = [self.digit(a), "marker", "Return", "Stock"]
		elif "put all your opponent's level  or lower characters in their waiting room" in t:
			c = [-1, "waitinger", "Level", f"<={self.digit(a,self.cond[0])}", "Opp"]
		elif "put all level  or lower characters in your opponent's center stage to the waiting room" in t:
			c = [-1, "waitinger", "Level", f"<={self.digit(a,self.cond[0])}", "Opp", "Center"]
		elif "put all your opponent's characters in stock" in t:
			c = [-1, 'stocker', 'opp']
		elif "look at your opponent's hand" in t:
			c = ["Hand", "opp", "look"]
		elif "look at up to x cards from the top of your deck" in t:
			if "choose up to   character from among them" in t:
				if "put it in your hand" in t:
					c = ["x", "looktop", "top", "hand", self.digit(a, self.cond[0]), f"Trait_{self.trait(a, self.cond[2])}", "upto"]
			if "x = the number of characters your opponent has" in t:
				c += ["xopp"]
			if "reveal it" in t and "show" not in c:
				if "if" in c:
					c.insert(c.index("if"), "show")
				elif "do" in c:
					c.insert(c.index("do"), "show")
				else:
					c.append("show")
		elif "look at up to  cards from top of your deck" in t or "look at up to  cards from the top of your deck" in t:
			if "put them on the top of your deck in any order" in t or "put them on top of your deck in any order" in t:
				c = [self.digit(a,self.cond[0]), "looktop", "top", "reorder", "upto"]
				self.cond[0] += 1
			elif "put them back in the same order" in t:
				c = [self.digit(a), "looktop", "top", "look", "upto"]
			elif "search for up to  character with  or " in t:
				if "put it in your hand" in t:
					c = [self.digit(a), "looktop", "top", "hand", self.digit(a, 1), f"Trait_{self.trait(a)}_{self.trait(a, 1)}", "upto"]
			elif "search for up to  level  or higher card" in t:
				if "put it in your hand" in t:
					c = [self.digit(a), "looktop", "top", "hand", self.digit(a, 1), f"Level_>={self.digit(a, 2)}", "upto"]
			elif "search for up to   character" in t:
				if "put it in your hand" in t:
					c = [self.digit(a), "looktop", "top", "hand", self.digit(a, 1), f"Trait_{self.trait(a)}", "upto"]
			elif "choose up to  level  or higher card from among them" in t:
				if "put it in your hand" in t:
					c = [self.digit(a), "looktop", "top", "hand", self.digit(a, 1), f"Level_>={self.digit(a, 1)}", "upto"]
			elif ("choose up to   characters from among them" in t or "choose up to   character from among them" in t) and "» character" in aa:
				if "put them in your hand" in t or "put it in your hand" in t:
					c = [self.digit(a,self.cond[0]), "looktop", "top", "hand", self.digit(a, self.cond[0]+1), f"Trait_{self.trait(a,self.cond[2])}", "upto"]
					self.cond[0]+=2
					self.cond[2]+=1
			elif "choose up to  of them" in t or "choose up to  card from among them" in t:
				if "put it in your hand" in t:
					c = [self.digit(a), "looktop", "top", "hand", self.digit(a, 1), "", "upto"]
			elif "choose  cards from among them" in t or "choose  card from among them" in t or "choose  of them" in t:
				if "put them in your waiting room" in t:
					if "put the rest on the top of your deck in any order" in t:
						c = [self.digit(a), "looktop", "top", "waiting", self.digit(a, 1), "upto", "all", "reorder"]
				elif "put it on the top of your deck" in t or "put it on top of the deck" in t:
					c = [self.digit(a, self.cond[0]), "looktop", "top", self.digit(a, self.cond[0] + 1), "upto"]
			elif "choose up to  climax from among them" in t:
				if "put it in your hand" in t:
					c = [self.digit(a), "looktop", "top", "hand", self.digit(a, 1), "Climax", "upto"]
					if "if you put  card in your hand" in t:
						if "choose  card in your hand" in t:
							if "put it in your waiting room" in t:
								c += ["if", self.digit(a, 2), "do", ["discard", self.digit(a, 3), ""]]
			if ("reveal it" in t or "reveal them" in t or "show it" in t) and "show" not in c:
				if "if" in c:
					c.insert(c.index("if"), "show")
				elif "do" in c:
					c.insert(c.index("do"), "show")
				else:
					c.append("show")
			if "choose up to  of your opponent's character" in t:
				c += ["do",self.convert(a,"choose up to  of your opponent's character"+t.split("choose up to  of your opponent's character")[1],aa)]
		elif "look at the top  cards of your opponent's deck" in t:
			if "choose up to  of them" in t:
				if "put it on the bottom of the deck" in t:
					if "put the rest on top of the deck in any order" in t:
						c = [self.digit(a), "looktop", "bdeck", self.digit(a, 1), "upto", "opp", "fix", "reorder"]
				elif "put them in the waiting room" in t:
					if "return the rest to the deck" in t and ("shuffle that deck" in t or "your opponent shuffles that deck" in t):
						c = [self.digit(a), "looktop", "top", "waiting", self.digit(a, 1), "upto", "any", "opp", "shuff"]
		elif "look at the top card of your opponent's deck" in t:
			if "choose  of your stand character" in t or "choose  of your standing character" in t:
				if "choose  of your stand character" in t:
					tt = "choose  of your stand character"
				elif "choose  of your standing character" in t:
					tt = "choose  of your standing character"
				if t.index(tt)<len(tt):
					gg,t = self.seperate("look at the top card of your opponent's deck",a,t,aa,True)
					g = gg
			if "put it on the top or the bottom of your opponent's deck" in t or "put it either on top or bottom of the deck" in t:
				c = [1, "looktop", "top", "bottom", "opp"]
		elif "look at the top  cards of your deck" in t:
			if "put them back in any order" in t:
				c = [self.digit(a), "looktop", "top", "reorder"]
		elif "look at the top card of your deck" in t:
			if "put it on the top or bottom of your deck" in t or "put it on the top or at the bottom of your deck" in t or "put it on top or bottom of your deck" in t or "put it either on top or bottom of your deck" in t or "put it on the top or the bottom of your deck" in t or "put it back either on top or bottom of the deck" in t or "put it either on top or bottom of the deck" in t:
				c = [1, "looktop", "top", "bottom"]
			elif "put it either on top of the deck or in the waiting room" in t or "put it on top of your deck or in your waiting room" in t or "put it on the top of your deck or in your waiting room" in t:
				c = [1, "looktop", "top", "waiting"]
			elif "put that card face-down under this as marker" in t or "put it face-down under this as marker" in t:
				c = [1, "looktop", "check", "do", [1, "marker", "top"]]
			else:
				return [1, "looktop", "check"]
		elif "choose  character opposite this" in t:
			if "put it in your opponent's waiting room" in t or "put it in the waiting room" in t:
				c = [1, "waitinger", "Opposite"]
		elif "choose either this or  of your  " in t:
			if "put it in your waiting room" in t:
				c = [self.digit(a), "waitinger", "Name=", self.name(a, s="n"), "This"]
		elif "choose another of your  characters" in t:
			if "that character gets + power" in t:
				c = [1, self.digit(a,self.cond[0]), x, "power", "Trait", self.trait(a,self.cond[2]), "Other"]
		elif "choose another character" in t:
			if "that character gets + level" in t:
				c = [1, self.digit(a,self.cond[0]), x, "level", "Other"]
		elif "choose  card in your level and  card in your waiting room" in t or "choose  card on your level area and  card in your waiting room" in t:
			if "exchange them" in t:
				c = ["ldiscard", self.digit(a), "", "levswap","Waiting", "if", "do", [self.digit(a), "salvage", "", "levswap","Waiting"]]
		elif "choose  card in your hand and  card in your level" in t:
			if "exchange them" in t:
				c = ["discard", self.digit(a), "", "levswap", "Hand", "if", "do", ["ldiscard", self.digit(a), "", "levswap","Hand"]]
		elif "choose up to x  characters from your waiting room" in t:
			if "return them to hand" in t:
				c = ["x","salvage",f"Trait_{self.trait(a,self.cond[2])}","show","upto"]
			if "x = the total level of the cards put in your waiting room" in t:
				c += ["xsmlevel"]
			elif "x equals the number of level  or lower characters moved to the waiting room" in t:
				c.extend(["xrqlevelc",self.digit(a,self.cond[0])])
		elif "choose up to  cards in your clock" in t:
			if "put them in the waiting room" in t:
				c = ["cdiscard", self.digit(a), "", "upto"]
		elif "choose up to  climax in your hand" in t:
			if "put it face down underneath this as a marker" in t and "reveal it" in t:
				c = [self.digit(a, self.cond[0]), "marker", "Climax", "Hand", "at", "show", "upto"]
		elif "choose up to  climax in your waiting room" in t or "choose up to  climax card in your waiting room" in t:
			if "return it to your hand" in t:
				c = [self.digit(a, self.cond[0]), "salvage", "Climax", "upto", "show"]
		elif "choose up to   in your waiting room" in t:
			if "put them face-down under this as markers" in t:
				c = [self.digit(a), "marker", f"Name=_{self.name(a, -1, s='n')}", "Waiting", "upto"]
		elif "choose up to   characters in your waiting room" in t or "choose up to   character in your waiting room" in t:
			c = [self.digit(a, self.cond[0]), "salvage", f"Trait_{self.trait(a, self.cond[2])}", "upto"]
			if "return it to your hand" in t:
				c += ["show"]
				if "choose  cards from your hand" in t:
					if "put them in your waiting room" in t or "put it in your waiting room" in t:
						c += ["if", 1, ["discard", self.digit(a, self.cond[0] + 1), ""]]
			elif "put them in your stock" in t or "put it in your stock" in t:
				c += ["Stock", "show"]
			self.cond[0] += 1
			if "and reveal the top card of your deck" in t:
				temp = d
				d = c
				c = temp
		elif "choose up to  character in your waiting room" in t:
			if "return it to your hand" in t:
				c = [self.digit(a, self.cond[0]), "salvage", "Character", "upto", "show"]
		elif "choose up to  character with level equal to or lower than your level in your hand" in t or "choose up to  character in your hand whose level = or lower than your level" in t:
			c = ["discard", self.digit(a, self.cond[0]), f"CLevel_<=p", "upto"]
			self.cond[0] += 1
			if "put it on any position of your stage" in t or "put it in any slot on the stage" in t:
				c+= ["Stage"]
				if "that character gets + power" in t:
					c += ["extra", "do", [-16, self.digit(a, self.cond[0] + 1), x, "power"]]
					self.cond[0] += 1
		elif "choose up to  character with  in its card name in your hand" in t:
			if "put it on the stage position that this was on" in t:
				c = ["discard", self.digit(a, self.cond[0]), f"Name_{self.name(a, s='n')}","Stage","Change", "upto"]
		elif "choose up to  characters with  in name in your waiting room" in t:
			if "return them to your hand" in t:
				c = [self.digit(a), "salvage", f"Name_{self.name(a, s='n')}", "show", "upto"]
		elif "choose up to  of your  characters" in t:
			if "characters get + power" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power", "Trait", self.trait(a, self.cond[2]), "upto"]
			elif "characters get + soul" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "soul", "Trait", self.trait(a, self.cond[2]), "upto"]
		elif "choose up to  of your character" in t:
			if "those characters gets + power" in t or "those characters get + power" in t:
				c = [self.digit(a,self.cond[0]), self.digit(a,self.cond[0]+1), x, "upto", "power"]
				if "power and «" in aa:
					c.extend(["extra", "do",[-16, self.trait(a,self.cond[2]), x, "trait"]])
			elif "they get the following ability" in t:
				c = [self.digit(a, self.cond[0]), self.name(a, s='a'), x, "give"]
		elif "choose up to  cards in your opponent's waiting room" in t:
			if "return them to your opponent's deck" in t or "return it to the deck" in t or "return them to their deck" in t or "return them to the deck" in t:
				c = [self.digit(a, self.cond[0]), "salvage", "", "Library", "upto", "opp", "show"]
				self.cond[0] += 1
		elif "choose up to  cost  or lower character in your waiting room" in t:
			if "put them in separate slots on the stage" in t:
				c = [self.digit(a, self.cond[0]), "salvage", f"Cost_<={self.digit(a, self.cond[0] + 1)}", "Stage", "upto"]
		elif "choose up to  level  or lower character in your hand" in t:
			c = ["discard", self.digit(a,self.cond[0]), f"CLevel_<={self.digit(a, self.cond[0]+1)}", "upto"]
			self.cond[0] += 2
			if "put it in any slot on the stage" in t:
				c.extend(["Stage"])
		elif "choose up to  level x or lower  character in your waiting room" in t:
			if "return it to your hand" in t:
				c = [self.digit(a, self.cond[0]), "salvage", f"TraitL_{self.trait(a, self.cond[2])}_<=x", "show", "upto"]
			if "x = the total level of the cards put in your waiting room" in t:
				c += ["xsmlevel"]
		elif "choose up to  level  or lower character in your waiting room" in t:
			if "put them on separate positions of your stage" in t:
				c = [self.digit(a, self.cond[0]), "salvage", f"CLevel_<={self.digit(a, self.cond[0] + 1)}", "Stage", "separate", "upto"]
		elif "choose up to  cost  or lower character in your opponent's" in t:
			if "put it in the waiting room" in t:
				c = [self.digit(a, self.cond[0]), "waitinger", "Opp", "Center", "Cost", f"<={self.digit(a, self.cond[0] + 1)}", "upto"]
		elif "choose up to  of your opponent's level  or lower character" in t:
			if "put that character into the stock" in t:
				c = [self.digit(a), "stocker"]
			elif "return it to your opponent's deck" in t or "return it to their deck" in t:
				c = [self.digit(a), "decker"]
			c += ["Level", f"<={self.digit(a, 1)}", "Opp", "upto"]
		elif "choose up to  of your opponent's character" in t:
			if "return that character to their hand" in t:
				c = [self.digit(a, self.cond[0]), "hander", "Opp",]
			elif "that character gets + soul and the following ability" in t:
				c = [self.digit(a), self.digit(a, 1), x, "soul", "Opp", "upto", "extra", "do", [-16, self.name(a, s='a'), x, "give"]]
		elif "choose   marker underneath this" in t or "choose   from underneath this as marker" in t:
			if "put it on any position of your stage" in t:
				c = [self.digit(a), "ksalvage", f"Name=_{self.name(a, s='n')}", "Stage"]
				if "at the end of the turn" in t and ("you may place that character face-up" in t or "you may put that character face up" in t) and ("underneath this as marker" in t or "underneath this as a marker" in t):
					c += ["extra", "do", [0, "[AUTO] At the end of the turn, you may put the previously chosen character face up underneath this as a marker.", 1, "give", "expass", self.digit(a), "ex_ID="]]
					self.ee = False
		elif "choose  level  or higher character battling this" in t:
			if "put it on bottom of the deck" in t:
				c = [self.digit(a,self.cond[0]), "decker", "bottom", "Battle", "Opp", "Level", f">={self.digit(a, self.cond[0]+1)}"]
		elif "choose  level x or lower  character in your waiting room" in t:
			c = [self.digit(a, self.cond[0]), "salvage", f"TraitL_{self.trait(a, self.cond[2])}_<=x"]
			if "put it on any position of your stage" in t:
				c += ["Stage"]
			elif "return it to your hand" in t:
				c += ["show"]
			if "x = # of cards in your memory" in t:
				c += ["xqmlevel"]
			elif "brainstorm" in aa and ("x = the number of  characters revealed among those cards" in t or "x = the number of  characters revealed" in t):
				c[2] = f"{c[2][:-1]}#"
				c += ["#trait", "#"]
			elif "x = the number of  in your waiting room" in t:
				c += ["xqwrlevel", "xName=", self.name(a, self.cond[1], s='n')]
		elif "choose  character of level x or lower in waiting room" in t or "choose  level x or lower character in your waiting room" in t:
			c = [self.digit(a, self.cond[0]), "salvage", "CLevel_<=x"]
			if "return it to hand" in t or "return it to your hand" in t:
				c += ["show"]
			if "x = the level of the revealed card" in t:
				c += ["xvlevel"]
			elif "x = the number of  in your waiting room" in t:
				c += ["xqwrlevel", "xName=", self.name(a, self.cond[1], s='n')]
		elif "choose  level  or lower  character in your waiting room" in t:
			c = [self.digit(a, self.cond[0]), "salvage", f"TraitL_{self.trait(a)}_<={self.digit(a, self.cond[0]+1)}"]
			if "put it in any slot on the stage" in t:
				c += ["Stage"]
		elif "choose  level  or lower character in your clock" in t:
			c = ["cdiscard", self.digit(a, self.cond[0]), f"CLevel_<={self.digit(a, self.cond[0] + 1)}"]
			if "put it in any slot on stage" in t or "put it in any slot on the stage" in t:
				c.extend(["Stage"])
			if "character in your clock with  in name" in t :
				c[2] = f"CLevelN_<={self.digit(a, self.cond[0]+1)}_{self.name(a, self.cond[1], s='n')}"
			if "at the next end of your opponent's turn" in t and "put that character in clock" in t:
				c.extend(["extra", "do", [-16, "[AUTO] At the end of of your opponent's next turn, put this card into your clock.", -3, "give"]])
		elif "choose  level  or lower character in your waiting room" in t:
			if "put it in any slot in the back stage" in t:
				c = [self.digit(a), "salvage", f"CLevel_<={self.digit(a, 1)}", "Stage", "Back"]
			elif "put it on any position of your stage" in t:
				c = [self.digit(a), "salvage", f"CLevel_<={self.digit(a, 1)}", "Stage"]
		elif "choose  level  or higher character in your waiting room" in t:
			if "return it to your hand" in t:
				c = [self.digit(a), "salvage", f"CLevel_>={self.digit(a, 1)}", "show"]
		elif "choose  of your other level  or lower character" in t:
			if "that character gets + power" in t:
				c = [self.digit(a,self.cond[0]), self.digit(a,self.cond[0]+2), x, "power", "Other", "Level", f"<={self.digit(a, self.cond[0]+1)}"]
		elif "choose  of your other characters with  in name" in t:
			if "put it in your stock" in t:
				c = [self.digit(a,self.cond[0]), "stocker", "Name", self.name(a, s='n'), "Other"]
			elif "that character gets + power" in t:
				c = [self.digit(a,self.cond[0]), self.digit(a,self.cond[0]+ 1), x, "power", "Name", self.name(a, s='n'), "Other"]
		elif "choose  climax in your waiting room" in t or "choose  climax card in your waiting room" in t:
			if "return it to your hand" in t:
				c = [self.digit(a), "salvage", "Climax", "show"]
		elif "choose   character in your waiting room" in t or "choose   character from your waiting room" in t:
			if "choose  of your stand character" in t or "choose  of your standing character" in t:
				if "choose  of your stand character" in t:
					tt = "choose  of your stand character"
				elif "choose  of your standing character" in t:
					tt = "choose  of your standing character"
				if t.index(tt)<len(tt):
					gg,t = self.seperate("choose   character in your waiting room",a,t,aa,True)
					g = gg
			c = [self.digit(a, self.cond[0]), "salvage", f"Trait_{self.trait(a, self.cond[2])}"]
			self.cond[0]+=1
			self.cond[2]+=1
			if "return it to your hand" in t or "return it to hand" in t:
				c += ["show"]
				if "choose  card from your hand" in t or "choose  card in your hand" in t:
					if "put it in your waiting room" in t or "discard it to the waiting room" in t:
						c += ["do", ["discard", self.digit(a, self.cond[0]), ""]]
			elif "put it in your stock" in t or "put it in stock" in t:
				c += ["Stock", "show"]
		elif "choose  character in your waiting room" in t or "choose  of your character in your waiting room" in t or "choose  character from your waiting room" in t:
			if "return it to your hand" in t:
				c = [self.digit(a, self.cond[0]), "salvage", "Character", "show"]
				if "discard  card from your hand" in t or "choose  card in your hand" in t:
					if "hand to the waiting room" in t or "put it in your waiting room" in t:
						c += ["if", self.digit(a, self.cond[0]), "do", ["discard", self.digit(a, self.cond[0] + 1), ""]]
				self.cond[0]+=1
				if "choose  of your characters" in t:
					gg, t = self.seperate("choose  of your characters",a,t,aa)
					if "do" in c:
						c[c.index("do")+1].extend(gg)
					else:
						c.extend(gg)
			elif "place it to any slot on your stage" in t:
				c = [self.digit(a), "salvage", "Character", "Stage"]
			if "with  or " in t and "» or «" in aa:
				c[2] = f"Trait_{self.trait(a)}_{self.trait(a, 1)}"
		elif "choose  character in your clock" in t:
			c = [self.digit(a,self.cond[0]), "csalvage", "Character", "show"]
			self.cond[0] += 1
			if "send it to memory" in t:
				c += ["Memory"]
			elif "return it to your hand" in t:
				if "choose  of your opponent's character" in t:
					gg, t = self.seperate("choose  of your opponent's character",a,t,aa)
					c.extend(gg)
		elif "choose  card in your waiting room" in t:
			if "put it on any position of your stage" in t:
				c = [self.digit(a), "salvage", "Character", "Stage"]
			if "with the same card name as a character on your stage" in t:
				c[2] = f"Name=_x"
				c.insert(3, "xStage")
		elif "choose   or  from your waiting room" in t and "\" or \"" in aa:
			if "return it to hand" in t:
				c = [self.digit(a,self.cond[0]), "salvage", f"Name=_{self.name(a, self.cond[1],s='n')}_{self.name(a, self.cond[1]+2,s='n')}", "show"]
		elif ("choose   in your waiting room" in t and "\" in your waiting room" in aa) or "choose  card named  in your waiting room" in t:
			if "put it on any position of your stage" in t or "put it in any slot on the stage" in t or "put it in any slot on stage" in t or "put it on any slot on your stage" in t:
				c = [self.digit(a, self.cond[0]), "salvage", f"Name=_{self.name(a, self.cond[1], s='n')}", "Stage"]
				if "discard  card from your hand to the waiting room" in t:
					c += ["do", ["discard", self.digit(a, self.cond[0] + 1), ""]]
			elif "put it on the stage position that this was on as rest" in t or "put it on the stage position this was on as rest" in t or "put it rested in the slot this was in" in t:
				c = [self.digit(a), "salvage", f"Name=_{self.name(a, s='n')}","Stage","Change", "extra", "do", [-16, "rested"]]
			elif "put it in the slot this was in" in t or "put it on the stage position that this was on" in t or "put it on the stage position this was on" in t or "place it to the slot this was in" in t:
				c = [self.digit(a,self.cond[0]),"salvage", f"Name=_{self.name(a, self.cond[1],s='n')}","Stage","Change"]
			elif "put it face up underneath this as a marker" in t or "put it face-up under this as marker" in t or "place it face up under this as marker" in t:
				c = [self.digit(a), "marker", f"Name=_{self.name(a, s='n')}", "Waiting", "show", "face-up"]
			elif "put it face-down under this as marker" in t:
				c = [self.digit(a), "marker", f"Name=_{self.name(a, s='n')}", "Waiting", "show"]
			elif "return it to your hand" in t:
				c = [self.digit(a), "salvage", f"Name=_{self.name(a, s='n')}", "show"]
			elif "send it to memory" in t:
				c = [self.digit(a), "salvage", f"Name=_{self.name(a, s='n')}", "Memory"]
		elif "choose  of your character with  in name other than  in your waiting room" in t or "choose  character with  in name other than  in your waiting room" in t:
			c = [self.digit(a), "salvage", f"NameO_{self.name(a, s='n')}_{self.name(self.name(a,2,s='n'))}"]
			if "return it to your hand" in t:
				c += ["show"]
		elif "choose  character with  in name in your waiting room" in t:
			if "return it to your hand" in t:
				c = [self.digit(a), "salvage", f"Name_{self.name(a, s='n')}", "show"]
		elif "choose   character in your clock" in t:
			c = [self.digit(a), "csalvage", f"Trait_{self.trait(a)}"]
			if "put it at the bottom of your deck" in t or "put it on the bottom of your deck" in t:
				c += ["Library", "bottom", "show"]
			elif "return it to your hand" in t:
				c += ["show"]
				if "put  card from your hand to the clock" in t:
					c += ["do", ["discard", self.digit(a, 1), "", "Clock"]]
		elif "choose  of your characters in battle" in t or "choose  of your battling characters" in t:
			if "that character gets +x power" in t:
				if "x =  multiplied by the number of characters you have with  or " in t and "\" or \"" in aa:
					if "\"backup\"" in aa:
						c = [self.digit(a), self.digit(a, 1), x, "X", "xName", f"{self.name(a, 3)}_{self.name(a, 5)}", "Battle", "x", self.digit(a, 1), "at", "power"]
				elif "x =  multiplied by your level" in t:
					if "characters you have is" in t:
						c = [self.digit(a, 1), self.digit(a, 2), x, "X", "xplevel", "Battle", "x", self.digit(a, 2), "power"]
					else:
						c = [self.digit(a), self.digit(a, 1), x, "X", "xplevel", "Battle", "x", self.digit(a, 1), "power"]
			elif "that character gets + power" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power", "Battle"]
		elif ("choose   in your hand" in t or "choose  card named  in your hand" in t) and "\" in your hand" in aa:
			if "put it in the slot this was in" in t or "put it on the stage position that this was on" in t:
				c = ["discard", self.digit(a), f"Name=_{self.name(a, s='n')}", "Stage", "Change"]
		elif "choose   in your climax area" in t:
			if "return it to your hand" in t:
				c = [1, "hander", "Climax"]
		elif "choose  cards in your memory" in t:
			if "put all cards except those cards in your waiting room" in t:
				c = ["mdiscard", self.digit(a, self.cond[0]), "", "invert"]
		elif "choose  of your stand character" in t or "choose  of your standing character" in t:
			if "rest it" in t or "rest them" in t:
				c = [self.digit(a,self.cond[0]), "rest", "Stand"]
				self.cond[0]+=1
				if "characters with no traits" in t:
					c.extend(["Trait", ""])

				if "if you rest  character" in t:
					c.extend(["if",self.digit(a,self.cond[0])])
					self.cond[0]+=1
				elif "if you do" in t or "if so" in t:
					c.extend(["if", c[0]])

				if "search your deck for up to   character" in t:
					gg,t = self.seperate("search your deck for up to   character",a,t,aa)
					c.extend(gg)
		elif "choose  of your " in t and "of your \"" in aa:
			if "that character gets + power" in t:
				c = [self.digit(a), self.digit(a, 1), x, "power", "Name=", self.name(a, s='n')]
		elif "choose this and  of your  character" in t or "choose  of your  characters and this" in t:
			if "exchange them as stand" in t or "stand and swap them" in t:
				c = [self.digit(a), "stand", "Trait", self.trait(a), "this", "swap", "Other"]
		elif "choose  of your  character" in t:
			if "that character gets + power and + soul" in t:
				if t.count("choose  of your  character") == 2:
					if t.count("that character gets + power and + soul") == 2:
						if t.count("for the turn") == 2:
							c = [self.digit(a), self.digit(a, 1), x, "power", "Trait", self.trait(a), "extra", "do", [-16, self.digit(a, 2), x, "soul", "do", [self.digit(a, 3), self.digit(a, 4), x, "power", "Trait", self.trait(a, 1), "extra", "do", [-16, self.digit(a, 5), x, "soul"]]]]
				else:
					c = [self.digit(a), self.digit(a, 1), x, "power", "Trait", self.trait(a), "extra", "do", [-16, self.digit(a, 2), x, "soul"]]
			elif "that character gets + power" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power","Trait", self.trait(a, self.cond[2])]
				self.cond[0]+=2
				self.cond[2]+=1
				if "gets + power and the following ability" in t:
					c.extend(["extra", "do", [-16, self.name(a, s='a'), x, "give"]])
				elif "gets + power and  " in t and "power and «" in aa:
					c.extend(["extra", "do", [-16, self.trait(a,self.cond[2]), x, "trait"]])
					self.cond[2]+=1
				if "choose  of your opponent's character" in t:
					c += ["do", self.convert(a, "choose  of your opponent's character" + t.split("choose  of your opponent's character")[1], aa)]
				else:
					if "at the end of the turn" in t and "put that character in the waiting room" in t:
						c += ["extra", "do", [-16, "[AUTO] At the end of the turn, put this card into your waiting room.", -3, "ACT", "give"]]
					if t.endswith("send this to memory.") or t.endswith("put this in your memory."):
						c += ["do", [0, "memorier"]]
			elif "that character gets + level" in t:
				c = [self.digit(a), self.digit(a, 1), x, "Trait", self.trait(a), "level"]
				if "that character gets + level and + power" in t:
					c += ["extra", "do", [-16, self.digit(a, 2), x, "power"]]
			elif "that character gets + soul" in t:
				c = [self.digit(a), self.digit(a, 1), x, "Trait", self.trait(a), "soul"]
		elif "choose  of your other  character" in t or "choose  other  character" in t:
			if "stand and swap them" in t:
				c = [self.digit(a,self.cond[0]), "stand", "Trait", self.trait(a,self.cond[2]),"swap","Other"]
				self.cond[0]+=1
				self.cond[2]+=1
				if "in your center stage center slot and this" in t:
					c += ["CenterM", "this"]
			elif "rest them" in t and "move them to an open slot in the back stage" in t:
				c = [self.digit(a), "rest", "Other", "extra", "do", [-16, "move", "Open", "Back"]]
			elif "return it to your hand" in t:
				c = [self.digit(a), "hander", "Other"]
				if "» character" in aa:
					c += ["Trait", self.trait(a)]
				elif "\" character" in aa:
					c += ["Name", self.name(a, s='n')]
			elif "that character gets +x power" in t:
				if "x = the number of other  characters you have" in t or "x =  times # of your other  characters" in t or "x = the number of your other  characters" in t:
					c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "#", "power", "Trait", self.trait(a, self.cond[2]), "#trait", self.trait(a, self.cond[2]), "Other", "#other"]
			elif "that character gets + power" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power", "Trait", self.trait(a, self.cond[2]), "Other"]
			elif "that character gets + soul" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "soul", "Trait", self.trait(a, self.cond[2]), "Other"]
		elif "choose  of your other characters and this" in t:
			if "return them to your hand" in t:
				c = [self.digit(a), "hander", "Other", "this"]
		elif "choose  of your other character" in t:
			if "put it in the waiting room" in t:
				c = [self.digit(a), "waitinger", "Other"]
			elif "that character gets the following ability" in t:
				c = [self.digit(a), self.name(a, s='a'), x, "give", "Other"]
			elif "that character gets + level and + power" in t:
				c = [self.digit(a), self.digit(a, 1), x, "level", "Other", "extra", "do", [-16, self.digit(a, 2), x, "power"]]
			elif "that character gets + power" in t:
				c = [self.digit(a), self.digit(a, 1), x, "power", "Other"]
			elif "that character gets +x power" in t:
				c = [self.digit(a), self.digit(a, 1), x, "X", "power", "Other", "x", self.digit(a, 1)]
				if "x =  times level of that character" in t:
					c.append("xlevel")
				elif "x = that character's soul" in t:
					c.append("xsoul")
			elif "rest it" in t and ("move it to an empty slot in the back stage" in t or "move it to an open position of your back stage" in t):
				c = [self.digit(a), "rest", "Other", "extra", "do", [-16, "move", "Open", "Back"]]
		elif "choose  of your character" in t:
			if "deal  damage to your opponent" in t:
				tt = "deal  damage to your opponent"
				if t.index(tt)<len(tt):
					gg,t = self.seperate("choose  of your character",a,t,aa,True)
					g = gg
			if "put it in your clock" in t:
				c = [self.digit(a,self.cond[0]), "clocker"]
			elif "put it in the waiting room" in t or "put it in your waiting room" in t:
				c = [self.digit(a,self.cond[0]), "waitinger"]
				self.cond[0]+=1
				if "if you do" in t or "if so" in t:
					c.extend(["if",c[0]])
				if "search your deck for up to  climax card" in t:
					gg, t = self.seperate("search your deck for up to  climax card", a, t, aa)
					c.extend(gg)
				elif "choose  of your opponent's level  or lower character" in t:
					gg, t = self.seperate("choose  of your opponent's level  or lower character", a, t, aa)
					c.extend(gg)
			elif "that character gets +x power" in t:
				if "x =  times level of that character" in t or "x =  times the level of that character" in t:
					c = [self.digit(a), self.digit(a, 1), x, "X", "power", "xlevel", "x", self.digit(a, 1)]
			elif "that character gets + power" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power"]
				if "that character gets + power and + soul" in t:
					c.extend(["extra", "do", [-16, self.digit(a, self.cond[0] + 2), x, "soul"]])
				elif "that character gets + power and " in t and "power and «" in aa:
					c.extend(["extra", "do", [-16, self.trait(a, self.cond[2]), x, "trait"]])
				elif "that character gets + power and the following ability" in t:
					c.extend(["extra", "do", [-16, self.name(a, self.cond[1], s='a'), x, "give"]])
				elif "this gets + power" in t in t:
					c.extend(["do", [0, self.digit(a, self.cond[0] + 2), x, "power"]])
				elif "at the end of the turn, put that card in your stock" in t:
					c.extend(["extra", "do", [-16, "[AUTO] At the end of the turn, put this card into your stock.", -3, "give"]])
			elif "that character gets + level" in t:
				c = [self.digit(a), self.digit(a, 1), x, "level"]
			elif "that character gets + soul" in t:
				c = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "soul"]
				if "that character gets + soul and this gets + power" in t:
					c += ["do", [0, self.digit(a, self.cond[0] + 2), x, "power"]]
			elif "that character gets «" in aa:
				c = [self.digit(a), self.trait(a), x, "trait"]
			elif "that character gets the following ability" in t:
				c = [self.digit(a), self.name(a, s='a'), x, "give"]

			if "characters with  in name" in t or "characters with  in its card name" in t:
				cd = ["Name", self.name(a, s="n")]
			elif "characters with \"" in a.lower():
				if "with  or  in the name" in t and "\" or \"" in a.lower():
					cd = ["Name", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}"]
				elif self.name(a, s='n') in self.text_name:
					cd = ["Text", f"{self.text_name[self.name(a, s='n')]}"]

			if cd:
				if "do" in c:
					c.insert(c.index("do"), cd[0])
					c.insert(c.index(cd[0]), cd[1])
				else:
					c += cd
		elif "choose  of your opponent's cards in in the waiting room" in t:
			if "return them in your opponent's deck" in t:
				c = [self.digit(a), "shuffle", "opp"]
				self.cond[0] += 1
		elif "choose  of your opponent's characters with level higher than your opponent's level" in t or "choose  of your opponent's characters whose level is higher than the level of your opponent" in t or "choose  of your opponent's characters that is higher level than your opponent" in t:
			if "put it in the waiting room" in t:
				c = [self.digit(a, self.cond[0]), "waitinger", "Opp", "Antilvl"]
			elif "put it into their memory" in t or "put it in your opponent's memory" in t or "send it to their memory" in t:
				c = [self.digit(a), "memorier", "Opp", "Antilvl"]
		elif "choose  cost  or lower character in your opponent's center stage" in t:
			if "put it in the waiting room" in t:
				c = [self.digit(a, self.cond[0]), "waitinger", "Opp", "Cost", f"<={self.digit(a, self.cond[0] + 1)}", "Center"]
			elif "put it on the top of his or her deck" in t:
				c = [self.digit(a, self.cond[0]), "decker", "top", "Cost", f"<={self.digit(a, self.cond[0] + 1)}", "Opp", "Center"]
		elif "choose  of your opponent's level  or higher character" in t:
			if "your opponent chooses  level x or lower character in their waiting room" in t and "exchanges them" in t:
				if "x = the level of the character you chose -" in t:
					c = [self.digit(a, self.cond[0]), "waitinger", "Level", f">={self.digit(a, self.cond[0] + 1)}", "Opp", "swap", "extra", "if", "do", [self.digit(a, self.cond[0] + 2), "salvage", f"CLevel_<=x", "xslevel-", abs(self.digit(a, self.cond[0] + 3)), "opp", "oppturn", "swap", "Stage"]]
		elif "choose  of your opponent's level  or lower characters" in t or "choose  level  or lower character on your opponent's center stage" in t or "choose  of your opponent's character whose level is  or lower" in t:
			if "that character doesn't stand" in t or "that character cannot stand" in t:
				if "during your opponent's next stand phase" in t:
					x = 3
				c = [self.digit(a, self.cond[0]), "[CONT] This cannot [STAND] during your stand phase", x, "give", "Level", f"<={self.digit(a, self.cond[0] + 1)}", "Opp"]
			elif "return it to hand" in t or "return it to your opponent's hand" in t:
				c = [self.digit(a, self.cond[0]), "hander", "Opp", "Level", f"<={self.digit(a, self.cond[0] + 1)}"]
				if "at the end of turn" in t and "put this in your memory" in t:
					c += ["do", [0, "[AUTO] At the end of the turn, put this card into your memory.", -3, "AUTO", "give"]]
			elif "put it in stock" in t or "put it in your opponent's stock" in t:
				c = [self.digit(a, self.cond[0]), "stocker", "Level", f"<={self.digit(a, self.cond[0] + 1)}", "Opp"]
			elif "put it into his or her waiting room" in t or "put it in the waiting room" in t or "put it into their waiting room" in t or "put it in your opponent's waiting room" in t:
				c = [self.digit(a, self.cond[0]), "waitinger", "Level", f"<={self.digit(a, self.cond[0] + 1)}", "Opp"]
				if "your opponent chooses up to  cost  or lower character in their waiting room" in t:
					if "puts it on the stage position that their character was on" in t:
						c += ["swap", "extra", "if", "do", [self.digit(a, self.cond[0] + 2), "salvage", f"Cost_<={self.digit(a, self.cond[0] + 3)}", "opp", "oppturn", "swap", "Stage"]]
			elif "put it on the bottom of his or her deck" in t:
				c = [self.digit(a), "decker", "Level", f"<={self.digit(a, 1)}", "Opp", "bottom"]
			elif "put it on the top of your opponent's deck" in t:
				c = [self.digit(a), "decker", "Level", f"<={self.digit(a, 1)}","top", "Opp"]

			if "opponent's center stage" in t or "in the center stage" in t:
				c.append("Center")
			elif "in the back stage" in t or "opponent's back stage" in t:
				c.append("Back")
		elif "choose  opponent's character" in t or "choose  of your opponent's character" in t or "choose  of your opponent's center stage characters" in t or "choose  character in your opponent's center stage" in t:
			if "move it to another vacant slot" in t:
				c = [self.digit(a,self.cond[0]), "move", "Character", "Opp", "Open", "may"]
			elif "return it to the hand" in t or "return it to your opponent's hand" in t or "return it to their hand" in t or "return it to hand" in t or "return it to your opponent's hand" in t or "return it to his or her hand" in t:
				c = [self.digit(a,self.cond[0]), "hander", "Opp"]
			elif "put it into their memory" in t or "send it to memory" in t:
				c = [self.digit(a, self.cond[0]), "memorier", "Opp"]
				if "your opponent puts that character from their memory on any position of their stage" in t or "your opponent puts that character from his or her memory in any slot on the stage" in t:
					if "at the start of encore step" in t:
						c += ["extra", "if", self.digit(a, self.cond[0]), "do", [-21, self.name(a, s='ac'), 2, "give", "expass", self.digit(a, self.cond[0]), "ex_ID="]]
						t = t.split("at the start of encore step")[0]
					else:
						c += ["extra", "if", self.digit(a, self.cond[0]), "do", [-16, "msalvage", "ID=_x", "Stage", "Opp", "oppturn", "opp"]]
			elif "that character cannot stand during your opponent's next stand phase" in t or "that character doesn't stand during your opponent's next stand phase" in t:
				return [self.digit(a,self.cond[0]), "[CONT] This cannot [STAND] during your stand phase", 2, "give", "Opp"]
			elif "that character gets - power and gets " in t and "gets «" in aa:
				c = [self.digit(a,self.cond[0]), self.digit(a, self.cond[0]+1), x, "power", "Opp", "extra", "do", [-16, self.trait(a), x, "trait"]]
			elif "that character gets the following ability" in t:
				c = [self.digit(a,self.cond[0]), self.name(a, s='a'), x, "give", "Opp"]
			elif "that character gets - power" in t:
				c = [self.digit(a,self.cond[0]), self.digit(a, self.cond[0]+1), x, "power", "Opp"]
			elif "that character gets -x power" in t:
				if "x =  times # of your  characters" in t or "x =  multiplied by the number of  characters you have" in t:
					c = [self.digit(a,self.cond[0]), self.digit(a, self.cond[0]+1), x, "#", "power", "Opp", "#trait", self.trait(a), "x", self.digit(a, self.cond[0]+1), "negative"]
			elif "that character gets - level" in t:
				c = [self.digit(a,self.cond[0]), self.digit(a, self.cond[0]+1), x, "level", "Opp"]
			elif "that character gets - soul" in t:
				c = [self.digit(a,self.cond[0]), self.digit(a, self.cond[0]+1), x, "soul", "Opp"]
			if "character in center stage" in t or "opponent's center stage characters" in t or "opponent's center stage" in t or "on the center stage" in t:
				if "do" in c:
					c.insert(c.index("do"), "Center")
				else:
					c.append("Center")
		elif "choose  card in your opponent's waiting room" in t:
			c = [self.digit(a, self.cond[0]), "salvage", "", "opp", "show"]
			if "put it in stock" in t:
				c += ["Stock"]
			elif "put it on top of the deck" in t or "put that character on top of your opponent's deck" in t or "put it on top of your opponent's deck" in t:
				c += ["Library", "top"]
			elif "return it to your opponent's deck" in t:
				c += ["Library"]
			elif "send it to memory" in t:
				c += ["Memory"]
		elif "search deck for up to x characters" in t:
			if "reveal them" in t and "put them in your hand" in t:
				c = ["x", "search", "Character", "upto", "show"]
			if "characters with  in name" in t:
				c[2] = f"Name_{self.name(a, self.cond[1], s='n')}"
			if "discard x cards from your hand to the waiting room" in t:
				c += ["do", ["discard", "x", ""]]
		elif "search your deck for up to  climax card" in t:
			if "put it in your hand" in t:
				c = [self.digit(a, self.cond[0]), "search", "Climax", "upto"]

			if "reveal it" in t:
				c+= ["show"]
		elif "search your deck for up to  level  or lower  character" in t:
			if "put it on any position of your stage" in t:
				c = [self.digit(a), "search", f"TraitL_{self.trait(a)}_<={self.digit(a, 1)}", "Stage", "upto"]
			elif "put that card on an open position of your stage" in t:
				c = [self.digit(a), "search", f"TraitL_{self.trait(a)}_<={self.digit(a, 1)}", "Stage", "Open", "upto"]
			elif "put it on any position of your back stage" in t:
				c = [self.digit(a), "search", f"TraitL_{self.trait(a)}_<={self.digit(a, 1)}", "Stage", "Back", "upto"]
		elif "search your deck for up to  level  or lower character" in t:
			if "put it in your hand" in t:
				c = [self.digit(a), "search", f"CLevel_<={self.digit(a, 1)}", "upto"]
				if "reveal it" in t:
					c.append("show")
		elif "search your deck for up to   or " in t or "search your deck for  character with  or " in t:
			if "reveal it" in t and "put it in your hand" in t:
				c = [self.digit(a), "search", f"Trait_{self.trait(a)}_{self.trait(a, 1)}", "show", "upto"]
		elif "search your deck for up to   character" in t and "» character" in aa:
			if ("reveal it" in t or "reveal them" in t or "show it to your opponent" in t or "show them to your opponent" in t) and ("put it in your hand" in t or "put them in your hand" in t):
				c = [self.digit(a, self.cond[0]), "search", f"Trait_{self.trait(a, self.cond[2])}", "upto", "show"]
				if "choose  card in your hand" in t:
					if "put it in your waiting room" in t:
						c += ["do", ["discard", self.digit(a, self.cond[0] + 1), ""]]
			elif "put it in the waiting room" in t or "put it in your waiting room" in t:
				c = [self.digit(a, self.cond[0]), "search", f"Trait_{self.trait(a, self.cond[2])}", "Waiting", "upto", "show"]
			elif "put it in any slot on the stage" in t or "put it on any position of your stage" in t:
				c = [self.digit(a, self.cond[0]), "search", f"Trait_{self.trait(a, self.cond[2])}", "Stage", "upto"]
				if "whose level = or lower than your level and whose cost is  or lower" in t:
					c[2] = f"TraitLCost_{self.trait(a, self.cond[2])}_<=p_<={self.digit(a, self.cond[0] + 1)}"
		elif "search your deck for up to  character with  in the name" in t or "search your deck for up to  character with  in name" in t or "search your deck for up to  character with  in its card name" in t:
			if "put them in your hand" in t or "put it in your hand" in t:
				c = [self.digit(a,self.cond[0]), "search", f"Name_{self.name(a, s='n')}", "upto"]
			if "reveal it" in t or "reveal them" in t:
				c.append("show")
		elif "search your deck for up to  character with " in t and self.name(a, s='n') in self.text_name:
			if "reveal it" in t and "put it in your hand" in t:
				c = [self.digit(a), "search", f"Text_{self.text_name[self.name(a, s='n')]}", "show", "upto"]
		elif "search your deck for up to  " in t or "search your deck for up to  card named " in t:
			c = [self.digit(a, self.cond[0]), "search", f"Name=_{self.name(a, self.cond[1], s='n')}", "upto"]

			if ("reveal it" in t or "show it to your opponent" in t) and "put it in your hand" in t:
				c.append("show")
				if self.name(a,self.cond[1], s='n') in self.text_name:
					c[2] = f"Text_{self.name(a, self.cond[1],s='n')}"
			elif "place it to any slot on the stage" in t or "put it on any position of your stage" in t:
				c.append("Stage")
			elif "put it in any slot in the back stage" in t:
				c += ["Stage", "Back"]
			elif "put it in the slot this was in" in t:
				c.extend(["Stage", "Change"])
		elif "move this to an empty slot" in t or "move this to an open position" in t:
			c = [1, "move", "Open", "this"]
			if "with a character opposite this" in t or "that has an opponent's character opposite that slot" in t or "opposite an opponent's character" in t:
				c.append("OpponentOpposite")
			elif "in your center stage" in t or "of your center stage" in t or "in the center stage" in t:
				c.append("Center")
			elif "in the back stage" in t or "of your back stage" in t:
				c.append("Back")
			if "you may move this" in t:
				c.append("may")
		elif "return that character to your hand" in t:
			c = [-7, "return", [self.target, "Hand"]]
		elif "return that character to its previous stage position as rest" in t or "put that character rest in the slot it was in" in t or "put that character rested in the slot it was in" in t:
			c = [-7, "revive", [self.target, "Stage"], "extra", "do", [-16, "rested"]]
		elif "deal x damage to your opponent" in t:
			c = ["damage", "x", "opp"]
			if "x = the number of climax among those cards" in t or "x is the number of climax cards among those cards" in t or "x = # of climax cards among those cards" in t:
				c += ["xmill", "xClimax"]
			elif "x = the level of the card put in your waiting room by this ability's cost" in t or "x = the level of the card discarded by the cost of this ability" in t:
				c += ["xdiscard", "xLevel"]
			elif "x = the level of that card +" in t or "x =  + level of that card" in t or "x equals the level of that card + " in t:
				c += ["xmill", "xLevel+x", self.digit(a, self.cond[0])]
			elif "x = # of  in your waiting room" in t:
				c += ["Name=", self.name(a, -1, s='n'), "Waiting"]
			elif "x = # of climax cards in your waiting room" in t:
				c += ["Climax", "Waiting"]
		elif "deal  damage to all players" in t:
			c = ["damage", self.digit(a), "both", "do", ["damage", self.digit(a), "opp"]]
		elif "deal  damage to your opponent" in t:
			if t.count("deal  damage to your opponent") >= 2:
				if t.count("deal  damage to your opponent") == 3:
					c = ['damage', self.digit(a,self.cond[0]), 'opp', "do", ['damage', self.digit(a, self.cond[0]+1), 'opp', "do", ['damage', self.digit(a, self.cond[0]+2), 'opp']]]
				else:
					c = ['damage', self.digit(a,self.cond[0]), 'opp', "do", ['damage', self.digit(a, self.cond[0]+1), 'opp']]
			else:
				c = ['damage', self.digit(a,self.cond[0]), 'opp']
				self.cond[0]+=1
				if "choose randomly  of your character" in t:
					if "that card gets + power" in t:
						c.extend(["do",[-8, self.digit(a, self.cond[0]+1), x, "power"]])
		elif "deals  damage to you" in t:
			c = ["damage", self.digit(a,self.cond[0])]

		if "all characters in your opponent's center stage get" in t or "all your opponent's center stage characters get" in t:
			if "get - power" in t:
				b = [-1, self.digit(a), x, "power", "Center", "opp"]
		elif "all your opponent's characters get" in t:
			if "get - power" in t:
				b = [-1, self.digit(a), x, "power", "opp"]
		elif "all your characters with  or " in t and "» or «" in aa:
			if "get + soul" in t:
				b = [-1, self.digit(a), x, "soul", "Trait", f"{self.trait(a)}_{self.trait(a, 1)}"]
		elif "all your characters with  in the name get" in t:
			if "get + power" in t:
				b = [-1, self.digit(a), x, "power", "Name", self.name(a, s='n')]
		elif "all your  characters get" in t:
			if "get + power and + soul" in t:
				b = [-1, self.digit(a,self.cond[0]), x, "Trait", self.trait(a,self.cond[2]), "power", "extra", "do", [-16, self.digit(a,self.cond[0]+1), x, "soul"]]
			elif "get + power" in t:
				b = [-1, self.digit(a,self.cond[0]), x, "power", "Trait", self.trait(a,self.cond[2])]
			elif "get + soul" in t:
				b = [-1, self.digit(a,self.cond[0]), x, "soul", "Trait", self.trait(a,self.cond[2])]
			elif "get the following ability" in t:
				b = [-1, self.name(a,self.cond[1] ,s='a'), x, "give", "Trait", self.trait(a,self.cond[2])]
			elif "characters gets " in t and "characters gets «" in aa:
				b = [-1, self.trait(a,self.cond[2]+1), x, "Trait", self.trait(a,self.cond[2]), "trait"]
		elif "all your characters get" in t:
			if "get + soul" in t:
				b = [-1, self.digit(a, self.cond[0]), x, "soul"]
			elif "get + power" in t:
				b = [-1, self.digit(a, self.cond[0]), x, "power"]
			elif "get + level" in t:
				b = [-1, self.digit(a, self.cond[0]), x, "level"]
			elif ("get " in t and "characters get \"[" in self.a_replace(a)) or "get the following ability" in t:
				b = [-1, self.name(a, s='a'), x, "give"]
		elif "all your other characters get" in t:
			if "get + power" in t:
				b = [-2, self.digit(a), x, "power"]
			elif "get + level" in t:
				b = [-2, self.digit(a), x, "level"]
		elif "this randomly gets between +~+ power" in t:
			b = [0, self.digit(a), x, "random", self.digit(a, 1), "power"]
		elif "this gets + level and + power" in t:
			b = [0, self.digit(a, 1), x, "power", "do", [0, self.digit(a), x, "level"]]
		elif "this gets + power and" in t:
			if "and + soul" in t:
				b = [0, self.digit(a, self.cond[0]), x, "power", "do", [0, self.digit(a, self.cond[0] + 1), x, "soul"]]
			elif "and the following ability" in t or "power and \"[" in aa:
				b = [0, self.digit(a, self.cond[0]), x, "power", "do", [0, self.name(a, s='a'), x, "give"]]
			elif "and your opponent cannot use" in t and "cannot use \"[auto] encore\"" in aa:
				b = [0, self.digit(a, self.cond[0]), x, "power", "do", [-21, "[CONT] Your opponent cannot use \"[AUTO] Encore\" until end of turn.", x, "give"]]
			elif "your opponent cannot play event cards and \"backup\" from his or her hand" in t:
				b = [0, self.digit(a, self.cond[0]), x, "power", "do", [-21, "[CONT] Your opponent cannot play event cards and \"Backup\" from his or her hand.", x, "give"]]
		elif "this gets the following  abilities" in t:
			b = [0, f"{self.name(a, s='a')}_{self.name(a, 1, s='a')}", x, "give"]
		elif "this gets the following ability" in t or ("this gets " in t and "this gets \"[" in aa):
			b = [0, self.name(a, s='a'), x, "give"]
		elif "this gets + power" in t:
			b = [0, self.digit(a, self.cond[0]), x, "power"]
			if "for each different trait on your characters" in t:
				b += ["#", "Traits"]
		elif "this gets - power" in t:
			b = [0, self.digit(a), x, "power"]
		elif "this gets + soul" in t:
			b = [0, self.digit(a), x, "soul"]
		elif "this gets +x power" in t:
			if "x =  times # of climax cards in your waiting room" in t:
				if "all battling characters get the following ability" in t:
					b = [0, self.digit(a, -1), x, "power", "#", "Climax", "Waiting", "do", [-25, self.name(a, s='a'), x, "give"]]
				else:
					b = [0, self.digit(a, -1), x, "power", "#", "Climax", "Waiting"]
			elif "x =  times # of your characters with  or " in t:
				b = [0, self.digit(a), x, "power", "#", "Trait", f"{self.trait(a)}_{self.trait(a, 1)}"]
			elif "x =  times # of other  in your center stage" in t:
				b = [0, self.digit(a), x, "Name", self.name(a, 1), "#", self.digit(a), "Center", "other", "power"]
			elif "x = the number of characters your opponent has" in t or "x =  times # of your opponent's characters" in t:
				b = [0, self.digit(a), x, "power", "#", "opp"]
			elif "x = the number of  characters among those cards " in t or "x =  times # of  characters among those cards" in t:
				b = [0, self.digit(a, self.cond[0]), x, "power"]
			elif "x = the number of cards you revealed" in t or "x = the number of cards revealed" in t:
				b = [0, self.digit(a), x, "power", "#", "Revealed"]
			elif "x =  times # of cards in your stock" in t:
				b = [0, self.digit(a), x, "#", "power", "Stock"]
			elif "x =  multiplied by the soul of this" in t:
				b = [0, self.digit(a), x, "X", "xsoul", "x", self.digit(a), "power"]
			elif "x = the number of other  characters you have" in t or "x =  times # of your other  characters" in t or "x = the number of your other  character" in t or "x = number of your other  character" in t:
				b = [0, self.digit(a,self.cond[0]), x, "power", "#", "Trait", self.trait(a), "other"]
			elif "x = the number of  characters you have" in t or "x =  times # of your  characters" in t or "x =  multiplied by the number of  characters you have" in t or "x =  multiplied by the number of your  characters" in t or "x equals the number of your  characters" in t:
				b = [0, self.digit(a), x, "power", "#", "Trait", self.trait(a)]
			elif "x = the number of  characters among those cards " in t or "x =  times # of  characters among those cards" in t:
				b = [0, self.digit(a, self.cond[0]), x, "power"]
		elif "you cannot use  " in t and "\"[auto] encore\"" in aa:
			b = [-21, "[CONT] You cannot use \"[AUTO] Encore\".", x, "give"]
		elif "your opponent cannot play events from hand" in t:
			b = [-21, "[CONT] Your opponent cannot play events from hand", x, "give"]

		if "rest this" in t:
			e = [0, "rest"]
			if "at the beginning of your next" in t or "at the start of your next" in t:
				e += ["do", [0, self.name(a, s='at'), 3, "give"]]
				if "at the beginning of your next" in t:
					t = t.split("at the beginning of your next")[0]
				elif "at the start of your next" in t:
					t = t.split("at the start of your next")[0]

		elif "stand this" in t:
			e = [0, "stand"]
		elif "put the top card of your deck in your clock" in t:
			e = ["damageref", 1]
		elif "put this in clock" in t or "put this in your clock" in t:
			e = [0, "clocker"]
		elif "put this in the waiting room" in t or "put this in your waiting room" in t:
			e = [0, "waitinger"]
			if "at the start of your next" in t and ("] at the start of your next" not in t or "\"at the start of your next" not in aa):
				e += ["do", [0, self.name(a, s='at'), 3, "give"]]
		elif "put this at the bottom of your deck" in t or "put this on the bottom of your deck" in t or "put this on the bottom of the deck" in t:
			e = [0, "decker", "bottom"]
		elif "put this in your stock" in t or "put this in stock" in t:
			e = [0, "stocker"]
		elif "put this in your memory" in t or "send this to memory" in t:
			if "\nput this in your memory" in aa or "\nsend this to memory" in aa or t.endswith("send this to memory.") or t.endswith("put this in your memory."):
				e = [0, "memorier"]
			elif ("send this to memory" in t and t.index("send this to memory")<20)or ("put this in your memory" in t and t.index("put this in your memory")<20):
				g = [0,"memorier"]
		elif "return this to your hand" in t or "return this to hand" in t or "return this in your hand" in t:
			e = [0, "hander"]
		elif "return this to your deck" in t:
			e = [0, "decker"]
		elif "this cannot become reverse" in t and "\"[CONT]" not in a:
			e = [0, "[CONT] This card cannot become [REVERSE].", x, "give"]
		elif "this's soul does not decrease by side attacking" in t or "this may side attack without soul penalty" in t:
			e = [0, "[CONT] This card's soul does not decrease by side attacking.", x, "give"]


		if c and "do" in c:
			cc = True

		# print("b",b)
		# print("c",c)
		# print("d",d)
		# print("e",e)
		# print("f",f)
		if e and h:
			e += ["do", h]
		elif not e and h:
			e = h

		if b and e:
			b += ["do", e]
		elif not b and e:
			b = e

		if c and b:
			if cc:
				c[-1] += ["do", b]
			else:
				c += ["do", b]
		elif not c and b:
			c = b

		if d and c:
			d += ["do", c]
		elif not d and c:
			d = c

		if f and d:
			f += ["do", d]
		elif not f and d:
			f = d

		if g and f:
			return g + ["do", f]
		elif not g and f:
			return f
		elif g and not f:
			return g
		else:
			return []

	def cont(self, a=""):
		t = self.text(a)
		aa = self.a_replace(a)
		c = []
		#
		# if "for the turn" in t or " until end of turn" in t:
		# 	x = 1
		# else:
		x = -1

		if t.startswith("assist"):
			if "all your level  or higher characters in front" in t:
				if "get + soul" in t:
					c = ["front", self.digit(a, 1), -1, "Assist", "soul", "flevel", self.digit(a)]
				elif "get + power" in t:
					c = ["front", self.digit(a, 1), -1, "Assist", "power", "flevel", self.digit(a)]
			elif "all your level  or lower characters in front" in t:
				if "get + power" in t:
					c = ["front", self.digit(a, 1), -1, "Assist", "power", "flevel", self.digit(a), "lower"]
			elif "x = that character's level" in t or "x =  times level" in t or "x =  multiplied by that character's level" in t or "x = the level of that character" in t or "x =  times the level of that character" in t:
				if "all your  or  characters in front" in t:
					c = ["front", self.digit(a), -1, "Assist", "Trait", f"{self.trait(a)}_{self.trait(a, 1)}", "flevel", "x", self.digit(a), "power"]
				elif "all your  characters in front" in t:
					c = ["front", self.digit(a), -1, "Assist", "Trait", self.trait(a), "flevel", "x", self.digit(a), "power"]
				else:
					c = ["front", self.digit(a), -1, "Assist", "flevel", "x", self.digit(a), "power"]
			elif "x =  multiplied by the number of  characters in your level" in t:
				c = ["front", self.digit(a), -1, "Assist", "LevTrait", self.trait(a), "Level", "x", self.digit(a), "power"]
			elif "get + power and + soul" in t:
				if "all your  characters in front" in t:
					c = ["front", self.digit(a), -1, "Assist", "Trait", self.trait(a), "power", "front", self.digit(a, 1), -1, "Assist", "Trait", self.trait(a), "soul"]
				else:
					c = ["front", self.digit(a), -1, "Assist", "power", "front", self.digit(a, 1), -1, "Assist", "soul"]
			elif "get + level and + power" in t:
				if "all your  characters in front" in t:
					c = ["front", self.digit(a, 1), -1, "Assist", "Trait", self.trait(a), "power", "front", self.digit(a), -1, "Assist", "Trait", self.trait(a), "level"]
			elif "get + level" in t:
				c = ["front", self.digit(a), -1, "Assist", "level"]
			elif "get + power" in t:
				if self.name(a, s='n') in self.text_name:
					c = ["front", self.digit(a), -1, "Assist", "Text", self.text_name[self.name(a, s='n')], "power"]
				else:
					c = ["front", self.digit(a), -1, "Assist", "power"]
			elif "get + soul" in t:
				c = ["front", self.digit(a), -1, "Assist", "soul"]
			elif "get \"" in t:
				c = ["front", self.name(a, s="a"), -1, "Assist", "ability"]
		elif t.startswith("alarm"):
			if "you're level  or higher" in t or "your level is  or higher" in t:
				if 'all your  characters' in t:
					if "characters get " in t and "get \"[" in aa:
						c = [-1, self.name(a, s='a'), -1, "Alarm", "plevel", self.digit(a), "Colour", self.trait(a), "ability"]
				elif "all your characters with  " in t:
					if "get the following ability" in t:
						if self.name(a, s='n') in self.text_name:
							c = [-1, self.name(a, -1, s='a'), -1, "Alarm", "plevel", self.digit(a), "Text", self.text_name[self.name(a, s='n')], "ability"]
			elif "all your characters with no traits" in t:
				if "get the following ability" in t:
					c = [-1, self.name(a, s='a'), -1, "Alarm", "Trait", "", "ability"]
			elif "all your level  or higher characters" in t:
				if "get + soul" in t:
					c = [-1, self.digit(a, 1), -1, "Alarm", "LevelC", self.digit(a), "soul"]
				elif "get + power" in t:
					c = [-1, self.digit(a, 1), -1, "Alarm", "LevelC", self.digit(a), "power"]
				elif "get " in t and "get \"" in aa:
					c = [-1, self.name(a, s='n'), -1, "Alarm", "LevelC", self.digit(a), "ability"]
			elif "all your  or  characters" in t:
				if "characters get + power" in t:
					c = [-1, self.digit(a), -1, "Alarm", "Trait", f"{self.trait(a)}_{self.trait(a, 1)}", "power"]
			elif "all your  characters" in t:
				if "characters get the following ability" in t or ("characters get " in t and "get \"[" in aa):
					c = [-1, self.name(a, s='a'), -1, "Alarm", "Trait", self.trait(a), "ability"]
			elif "all your characters" in t:
				if ("characters get " in t and "get \"[" in aa) or "get the following ability" in t:
					c = [-1, self.name(a, s='a'), -1, "Alarm", "ability"]
				elif "characters get + power" in t:
					c = [-1, self.digit(a), -1, "Alarm", "power"]
		elif t.startswith("bodyguard") or t.startswith("great performance"):
			c = [0, "", -1, "bodyguard"]
		elif t.startswith("experience"):
			if "if the total level of the cards in your level is  or higher" in t or "if the sum of levels of cards in your level zone is  or higher" in t:
				if "your other character in the middle position of the center stage gets + power" in t:
					c = [-5, self.digit(a, 1), -1, "Experience", self.digit(a), "power", "other", "fm"]
				elif "all your other characters get + power" in t:
					c = [-2, self.digit(a, 1), -1, "Other", "Experience", self.digit(a), "power"]
				elif "all your other  characters get + power" in t:
					c = [-2, self.digit(a, 1), -1, "Other", "Experience", self.digit(a), "Trait", self.trait(a), "power"]
				elif "all your other  characters get " in t and " get \"[" in aa:
					c = [-2, self.name(a, s='a'), -1, "Other", "Experience", self.digit(a), "Trait", self.trait(a), "ability"]
				elif "this gets + power and the following ability" in t:
					c = [0, self.digit(a, 1), -1, "Experience", self.digit(a), "power", 0, self.name(a, s='a'), -1, "Experience", self.digit(a), "ability"]
				elif "this gets the following ability" in t:
					c = [0, self.name(a, s='a'), -1, "Experience", self.digit(a), "ability"]
				elif "this gets + power" in t:
					c = [0, self.digit(a, 1), -1, "Experience", self.digit(a), "power"]
				elif "this gets +x power" in t:
					if "x =  multiplied by the level of the character opposite this" in t:
						c = [0, self.digit(a, 1), -1, "X", "Experience", self.digit(a), "x", self.digit(a, 1), "xlevel", "opposite", "power"]
				elif "this gets + soul" in t:
					c = [0, self.digit(a, 1), -1, "Experience", self.digit(a), "soul"]
				elif "this gets " in t and "this gets \"[" in aa:
					c = [0, self.name(a, s='a'), -1, "Experience", self.digit(a), "ability"]
			elif "if a card named  is in your level" in t or "if  is in your level zone" in t or "if you have  in your level zone" in t:
				if "this gets + power and the following ability" in t:
					c = [0, self.digit(a), -1, "Experience", 1, "Name=", self.name(a, s="n"), "power", 0, self.name(a, s='a'), -1, "Experience", 1, "Name=", self.name(a, s="n"), "ability"]
				elif "this gets + power" in t:
					c = [0, self.digit(a), -1, "Experience", 1, "Name=", self.name(a, s="n"), "power"]
				elif "this gets + soul" in t:
					c = [0, self.digit(a), -1, "Experience",1, "Name=", self.name(a, s="n"), "soul"]
		elif t.startswith("recollection") or t.startswith("memory"):
			if "if this is in memory" in t or "if this is in your memory" in t:
				if "all your  and  get + power" in t and "\" and \"" in aa:
					c = [-1, self.digit(a), -1, "sMemory", "Name", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}", "power"]
				elif "all your  characters get + power" in t:
					c = [-1, self.digit(a), -1, "sMemory", "Trait", self.trait(a), "power"]
				elif "all your characters with  in the name" in t:
					if "gets + power" in t or "get + power" in t:
						c = [-1, self.digit(a), -1, "sMemory", "Name", self.name(a, s='n'), "power"]
			elif "if there are  or more characters in your memory with  or " in t:
				if "this gets + power" in t:
					c = [0, self.digit(a, 1), -1, "More", self.digit(a), "Trait", f"{self.trait(a)}_{self.trait(a, 1)}", "Memory", "power"]
			elif "if there are  or more  in your memory" in t:
				if "this gets - level while in your hand" in t:
					c = [0, self.digit(a, 1), -1, "More", self.digit(a), f"Name=_{self.name(a, s='n')}", "Memory", "pHand", "level"]
				elif "this gets + power and + soul" in t:
					c = [0, self.digit(a, 1), -1, "More", self.digit(a), f"Name=_{self.name(a, s='n')}", "Memory", "power", 0, self.digit(a, 2), -1, "More", self.digit(a), f"Name=_{self.name(a, s='n')}", "Memory", "soul"]
			elif "if  is in your memory" in t or "if there is a  in your memory" in t:
				if "this gets + power and the following ability" in t:
					c = [0, self.digit(a), x, "More", 1, "Name=", self.name(a, s='n'), "Memory", "power", 0, self.name(a, s='a'), -1, "More", 1, "Name=", self.name(a, s='n'), "Memory", "ability"]
				elif "this gets + power" in t:
					c = [0, self.digit(a), x, "More", 1, "Name=", self.name(a, s='n'), "Memory", "power"]
				elif "this gets the following ability" in t:
					c = [0, self.name(a, s='a'), x, "More", 1, "Name=", self.name(a, s='n'), "Memory", "ability"]
			elif "if there are cards in your memory" in t:
				if "all your other characters get + power" in t:
					c = [-2, self.digit(a), -1, "Other", "OMore", 1, "OMemory", "power"]
				elif "this gets " in t and "gets \"[" in aa:
					c = [0, self.name(a, s='a'), -1, "More", 1, "Memory", "ability"]
			elif "if you have  card in your memory" in t or "if you have  or more cards in memory" in t:
				if t.count("if you have  or more cards in memory")>1:
					c = ["multicond",[]]
					a1 = a.split(" If you have ")
					for a2 in a1:
						d = self.cont(a=f"RECOLLECTION If you have {a2}")
						if d:
							c[1].append(d)
				elif "this gets + power" in t:
					c = [0, self.digit(a, 1), -1, "More", self.digit(a), "Memory", "power"]
				elif "in battles involving this your opponent may not play backup from hand" in t:
					c = [0, "[CONT] During this card's battle, your opponent cannot play \"Backup\" from hand.", x,"More", self.digit(a), "Memory","ability"]
				elif "this cannot be chosen by your opponent's effects." in t:
					c = [0, "[CONT] This card cannot be chosen by your opponent's effects.", x, "More", self.digit(a), "Memory", "ability"]
			elif "number of cards in your memory is  or more" in t or "if there are  or more cards in your memory" in t or "if you have  card in memory" in t:
				if "all your other characters get + power" in t:
					c = [-2, self.digit(a, 1), -1, "Other", "OMore", self.digit(a), "OMemory", "power"]
				elif "this gets + power and the following ability" in t:
					c = [0, self.digit(a, 1), -1, "More", self.digit(a), "Memory", "power", 0, self.name(a, s='a'), -1, "More", self.digit(a), "Memory", "ability"]
				elif "this gets + power and + soul" in t:
					c = [0, self.digit(a, 1), -1, "More", self.digit(a), "Memory", "power", 0, self.digit(a, 2), -1, "More", self.digit(a), "Memory", "soul"]
				elif "this gets - level and gets + power" in t:
					c = [0, self.digit(a, 2), -1, "More", self.digit(a), "Memory", "power", 0, self.digit(a, 1), -1, "More", self.digit(a), "Memory", "level"]
				elif "this gets the following ability" in t or ("this gets " in t and "gets \"[" in aa):
					c = [0, self.name(a, s='a'), -1, "More", self.digit(a), "Memory", "ability"]
				elif "this gets + power" in t:
					if "for each other rested characters you have" in t:
						c = [0, self.digit(a, 1), -1, "Each", "Rest", "OMore", self.digit(a), "OMemory", "power", "other"]
					else:
						c = [0, self.digit(a, 1), -1, "More", self.digit(a), "Memory", "power"]
			elif "number of  characters in your memory is  or more" in t:
				if "this gets + power and the following ability" in t:
					c = [0, self.digit(a, 1), -1, "More", self.digit(a), "Trait", self.trait(a), "Memory", "power", 0, self.name(a, s='a'), -1, "More", self.digit(a), "Trait", self.trait(a), "Memory", "ability"]
				elif "this gets + power" in t:
					c = [0, self.digit(a, 1), -1, "More", self.digit(a), "Trait", self.trait(a), "Memory", "power"]
		elif "if this is on the stage" in t:
			if "this's card name will also be regarded as" in t:
				c = [0, self.name(a, s='n'), -1, "Stage", "name"]
		elif "if this is in the middle position of the center stage" in t or "if this is in the middle position of your center stage" in t or "if this is in the center stage center slot" in t:
			if "this gets + power and the following ability" in t:
				c = [0, self.digit(a), -1, "Middle", "power", 0, self.name(a, s='a'), -1, "Middle", "ability"]
			elif "this gets + level and + power" in t:
				c = [0, self.digit(a,1), -1, "Middle", "power",0, self.digit(a), -1, "Middle", "level"]
			elif "this gets + power" in t:
				c = [0, self.digit(a), -1, "Middle", "power"]
		elif "this gets - level while in your hand" in t or "this gets - level in your hand" in t:
			if "if your waiting room has  or less climax" in t or "if there are  or fewer climax cards in your waiting room" in t:
				c = [0, self.digit(a, 1), -1, "ClimaxWR", self.digit(a), "level", "pHand", "lower"]
			elif "f the number of climax cards in your waiting room is  or more" in t:
				c = [0, self.digit(a, 1), -1, "ClimaxWR", self.digit(a), "level", "pHand"]
			elif "if the number of cards named  in your waiting room is  or more" in t or "if you have  or more  in your waiting room" in t:
				c = [0, self.digit(a, 1), -1, "NameWR", self.digit(a), "Name=", self.name(a, s="a"), "level", "pHand"]
			elif "if a card named  is in your clock" in t or ("if  is in your clock" in t and "if \"" in aa):
				c = [0, self.digit(a), -1, "NameCL", 1, "Name=", self.name(a, s="a"), "pHand", "level"]
			elif "if there are  or more  in your memory" in t:
				c = [0, self.digit(a, 1), -1, "More", self.digit(a), f"Name=_{self.name(a, s='n')}", "Memory", "pHand", "level"]
			elif "if  and  are in your level zone" in t:
				c = [0, self.digit(a), -1, "More", 2, "NameA", f"{self.name(a, s='n')}_{self.name(a,2 ,s='n')}", "LevelZ", "pHand", "level"]
			elif "if there are  or fewer cards in your deck" in t:
				c = [0, self.digit(a, 1), -1, "Deck", self.digit(a), "lower", "pHand", "level"]
			elif "if you have  or more  characters" in t:
				c = [0, self.digit(a, 1), -1, "More", self.digit(a), "Trait", self.trait(a), "pHand", "level"]
		elif "if there are  or more markers under this" in t:
			if "this card cannot be chosen by your opponent's effects" in t:
				if "if there are  or more markers under this" in t:
					if "this gets + power" in t:
						if "if there are  or more markers under this" in t:
							if "all your other characters get + power" in t:
								c = ["marker#", [[0, "[CONT] This card cannot be chosen by your opponent's effects.", -3, "Marker#", self.digit(a), "ability"], [0, self.digit(a, 2), -1, "Marker#", self.digit(a, 1), "power"], [-2, self.digit(a, 4), -1, "Other", "Marker#", self.digit(a, 3), "power"]]]
		elif "if there is a marker underneath this" in t or "if there are markers under this" in t or "if there is a marker under this" in t:
			if "this gets + power and + soul" in t:
				c = [0, self.digit(a), -1, "Marker#", 1, "power", 0, self.digit(a, 1), -1, "Marker#", 1, "soul"]
			elif "this gets + power" in t:
				c = [0, self.digit(a), -1, "Marker#", 1, "power"]
		elif "if there are  or fewer cards" in t:
			if "this gets + level and + power" in t:
				if "in your stock" in t:
					c = [0, self.digit(a, 2), -1, "Stock", self.digit(a), "lower", "power", 0, self.digit(a, 1), -1, "Stock", self.digit(a), "lower", "level"]
			elif "this gets + power" in t:
				if "in your waiting room" in t:
					c = [0, self.digit(a, 1), -1, "More", self.digit(a), "Waiting", "lower", "power"]
				elif "in your hand" in t:
					c = [0, self.digit(a, 1), -1, "Hand", self.digit(a), "lower", "power"]
				elif "in your stock" in t:
					c = [0, self.digit(a, 1), -1, "Stock", self.digit(a), "lower", "power"]
		elif "if there are more cards in your hand than your opponent's hand" in t:
			if "this gets + power" in t:
				c = [0, self.digit(a), -1, "Hand", "HandvsOpp", "power"]
		elif "if there's a climax card in your opponent's climax area" in t:
			if "this gets " in t and "gets \"[" in aa:
				c = [0, self.name(a, s='a'), -1, "More", 1, "Climax", "CX", "opp", "ability"]
		elif "you can put any number of cards with the same card name as this in your deck" in t:
			c = [50, "limit"]
		elif "when this attacks, you may instead choose  character on your opponent's back stage, and have this frontal attack with the chosen character as the defending character" in t or "when this attacks, you may instead choose  character in opponent's back stage and have this front attack that character as the defending character" in t:
			c = [1, "", -1, "backatk", "may"]
		elif "if the number of characters your opponent has is  or more" in t:
			if "this gets + power" in t:
				c = [0, self.digit(a, 1), -1, "More", self.digit(a), "Character", "opp", "power"]
		elif "if there are  or more  in your waiting room" in t:
			if "this gets + power" in t:
				c = [0, self.digit(a, 1), -1, "More", self.digit(a), "Name=", self.name(a, s='n'), "Waiting", "power"]
		elif "if there are  or more cards" in t or "if you have  or more cards" in t:
			if "all your other  characters get + power" in t:
				if " in your stock" in t:
					c = [-2, self.digit(a, 1), -1, "Other", "Stock", self.digit(a), "Trait", self.trait(a), "power"]
			elif "this gets + power and " in t and "and \"[" in aa:
				if " in your stock" in t:
					c = [0, self.digit(a, 1), -1, "Stock", self.digit(a), "power", 0, self.name(a, s='a'), -1, "Stock", self.digit(a), "ability"]
			elif "get the following ability" in t or ("gets \"[" in aa or "get \"[" in aa):
				if "\" in name" in aa or "\" in the name" in aa:
					if "if there are  or more cards in your memory" in t:
						if "and this gets \"" in aa:
							c = [-32, self.name(a, s='a'), -1, "Other", "OMore", self.digit(a), "OMemory", f"Name", f"{self.name(a, s='n')}", "ability"]
			elif "this gets + power" in t:
				if " in your hand" in t:
					c = [0, self.digit(a, 1), -1, "Hand", self.digit(a), "power"]
				elif " in your stock" in t:
					c = [0, self.digit(a, 1), -1, "Stock", self.digit(a), "power"]
		elif "for each card in your clock" in t:
			if "this gets + power" in t:
				c = [0, self.digit(a), -1, "Each", "Clock", "power"]
		elif "for each climax card in your waiting room" in t:
			if "this gets + power" in t:
				c = [0, self.digit(a), -1, "Each", "Climax", "Waiting", "power"]
		elif "for each  in your waiting room" in t:
			if "this gets + power" in t:
				c = [0, self.digit(a), -1, "Each", "Name=", self.name(a, s='n'), "Waiting", "power"]
		elif "for each of your other cards named " in t or "for each other \"" in aa:
			if "this gets + level and + power" in t:
				c = [0, self.digit(a, 1), -1, "Each", "Name=", self.name(a, s="n"), "other", "power", 0, self.digit(a), -1, "Each", "Name=", self.name(a, s="n"), "other", "level"]
			elif "this gets + power" in t:
				if "and the character opposite this gets + soul" in t:
					c = [0, self.digit(a), -1, "Each", "Name=", self.name(a, s='n'), "other", "power", -6, self.digit(a, 1), -1, "Opposite", "soul"]
				elif "\" in the center stage" in aa or "\" in your center stage" in aa:
					c = [0, self.digit(a), -1, "Each", "Name=", self.name(a, s='n'), "other", "Center", "power"]
				else:
					c = [0, self.digit(a), -1, "Each", "Name=", self.name(a, s='n'), "other", "power"]
		elif "for each of your other  characters" in t or (("for each other  you have" in t or "for each other  character you have" in t or "for each other  character in" in t) and "for each other «" in aa):
			if "this gets + power" in t:
				if "in your back stage" in t or "in the back stage" in t:
					c = [0, self.digit(a), -1, "Each", "Trait", self.trait(a), "power", "other", "Back"]
				elif "in the center stage" in t:
					if "if there's a marker under this" in t:
						c = [0, self.digit(a), -1, "Each", "Trait", self.trait(a), "power", "other", "Center", "markers"]
					else:
						c = [0, self.digit(a), -1, "Each", "Trait", self.trait(a), "power", "other", "Center"]
				else:
					c = [0, self.digit(a), -1, "Each", "Trait", self.trait(a), "power", "other"]
		elif "for each of your other" in t:
			if "this gets + power" in t:
				if "\" in the center stage" in aa:
					c = [0, self.digit(a), -1, "Each", "Name=", self.name(a, s='n'), "other", "Center", "power"]
				elif "other back stage «" in aa:
					c = [0, self.digit(a), -1, "Each", "Trait", self.trait(a), "other", "Back", "power"]
				elif "other rested characters" in t or "other rest characters" in t:
					c = [0, self.digit(a), -1, "Each", "Rest", "power", "other"]
				elif "characters with  or " in t:
					c = [0, self.digit(a), -1, "Each", "Trait", f"{self.trait(a)}_{self.trait(a, 1)}", "power", "other"]
				elif "characters with " in t and self.name(a, s='n') in self.text_name:
					c = [0, self.digit(a), -1, "Each", "Text", self.text_name[self.name(a, s='n')], "power", "other"]
				elif "level  or lower characters" in t:
					c = [0, self.digit(a, 1), -1, "Each", "LevelC", self.digit(a), "lower", "power", "other"]
		elif "for each character in your opponent's back stage" in t or "for each of your opponent's back stage character" in t:
			if "this gets + power" in t:
				c = [0, self.digit(a), -1, "Each", "opp", "Back", "power"]
		elif "for each other rested character you have" in t:
			if "this gets + power" in t:
				c = [0, self.digit(a), -1, "Each", "Rest", "other", "power"]
		elif "for each standing character your opponent has" in t:
			if "this gets + power" in t:
				c = [0, self.digit(a), -1, "Each", "Stand", "opp", "power"]
		elif "for each different trait on your characters" in t:
			if "this gets + power" in t:
				c = [0, self.digit(a), -1, "Each", "Traits", "power"]
		elif "your other level  or lower character in the middle position of your center stage" in t or "your other level  or lower center stage middle character" in t:
			if "gets + power" in t:
				c = [-5, self.digit(a, 1), -1, "Middle", "Level", self.digit(a), "lower", "other", "power"]
		elif "your other character in" in t:
			if "center stage center slot" in t or "middle position of your center stage" in t:
				if "gets + power and " in t and "power and \"[" in aa:
					c = [-5, self.digit(a), -1, "Middle", "other", "power", -5, self.name(a, s="a"), -1, "Middle", "other", "ability"]
				elif 'gains "[' in aa or 'gets "[' in aa:
					c = [-5, self.name(a, 1), -1, "Middle", "ability", "other"]
				elif "gets + power" in t:
					c = [-5, self.digit(a), -1, "Middle", "other", "power"]
		elif "if the number of cards in your hand is  or more" in t or "if you have  or more cards in your hand" in t:
			if "this gets + power" in t:
				c = [0, self.digit(a, 1), -1, "Hand", self.digit(a), "power"]
			elif "this gets " in t and "gets \"[" in aa:
				c = [0, self.name(a, s='a'), -1, "Hand", self.digit(a), "ability"]
			elif "all your other characters get + power" in t:
				c = [-2, self.digit(a, 1), -1, "Other", "Hand", self.digit(a), "power"]
		elif "if the number of cards in your stock is  or more" in t:
			if "this gets + power" in t:
				c = [0, self.digit(a, 1), -1, "Stock", self.digit(a), "power"]
		elif "if you have  or more climax cards in your waiting room" in t:
			if "this gets + level and + power" in t:
				c = [0, self.digit(a, 2), -1, "More", self.digit(a), "Climax", "Waiting", "power", 0, self.digit(a, 1), -1, "More", self.digit(a), "Climax", "Waiting", "level"]
		elif "if you have  or more other  character" in t:
			if "this gets + level and cannot be chosen by your opponent's effects" in t:
				c = [0, self.digit(a, 1), -1, "More", self.digit(a), "Trait", self.trait(a), "other", "level", 0, "[CONT] This card cannot be chosen by your opponent's effects.", -1, "More", self.digit(a), "Trait", self.trait(a), "other", "ability"]
			elif "this gets + level and + power" in t:
				c = [0, self.digit(a, 2), -1, "More", self.digit(a), "Trait", self.trait(a), "other", "power", 0, self.digit(a, 1), -1, "More", self.digit(a), "Trait", self.trait(a), "other", "level"]
			elif "this gets the following ability" in t:
				c = [0, self.name(a, s='a'), -1, "More", self.digit(a), "Trait", self.trait(a), "other", "ability"]
			elif "this gets + power" in t:
				c = [0, self.digit(a, 1), -1, "More", self.digit(a), "Trait", self.trait(a), "other", "power"]
		elif "if you have  or more  character" in t:
			if "this gets + level and cannot be chosen by your opponent's effects" in t:
				c = [0, self.digit(a, 1), -1, "More", self.digit(a), "Trait", self.trait(a), "level", 0, "[CONT] This card cannot be chosen by your opponent's effects.", -1, "More", self.digit(a), "Trait", self.trait(a), "ability"]
		elif "if you have another character with  in name" in t or "if you have another character with  in the name" in t:
			if "this gets + power" in t:
				c = [0, self.digit(a), -1, "More", 1, "Name", self.name(a, s="n"), "other", "power"]
			elif "this gets the following ability" in t:
				c = [0, self.name(a, s='a'), -1, "More", 1, "Name", self.name(a, s="n"), "other", "ability"]
		elif "if you have another «" in aa:
			if "this gets +" in t:
				c = [0, self.digit(a), -1, "More", 1, "Trait", self.trait(a), "other", "power"]
		elif "if you have another \"" in aa or ("if you have " in t and "if you have \"" in aa):
			if "character opposite this" in t:
				if "gets - soul" in t:
					if "get " in t and "get \"" in aa:
						if aa.count("\" and \"") == 3:
							c = [-2, self.name(a, s='a'), -1, "Other", "OMore", 4, "Oother", "O&", "OName", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}_{self.name(a, 4, s='n')}_{self.name(a, 6, s='n')}", "ability", -6, self.digit(a), -1, "Opposite", "OMore", 4, "Oother", "O&", "OName", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}_{self.name(a, 4, s='n')}_{self.name(a, 6, s='n')}", "soul"]
			elif "this gets + power" in t:
				if "if you have another  and " in t and "\" and \"" in aa:
					c = [0, self.digit(a), -1, "Another&", "Name", f"{self.name(a, s='n')}_{self.name(a, -1, s='n')}", "power"]
				else:
					c = [0, self.digit(a), -1, "Another", "Name=", self.name(a, s="n"), "power"]
			elif "this gets " in t and "this gets \"" in aa:
				c = [0, self.name(a, s="a"), -1, "Another", "Name=", self.name(a, s="n"), "ability"]
			elif "get + power" in t:
				if "all your other characters with  or " in t:
					c = [-2, self.digit(a), -1, "Other", "OMore", 1, "Oother", "OName=", self.name(a, s='n'), "Trait", f"{self.trait(a)}_{self.trait(a, 1)}", "power"]
				elif "all your other characters with \"" in aa:
					c = [-2, self.digit(a), -1, "Other", "OMore", 1, "Oother", "OName=", self.name(a, s='n'), "Name", self.name(a, -1, s='n'), "power"]
				elif "all your other  characters" in t:
					c = [-2, self.digit(a), -1, "Other", "OMore", 1, "Oother", "OName=", self.name(a, s='n'), "Trait", self.trait(a), "power"]
			elif ("get " in t and "get \"" in aa) or "get following ability" in t:
				if "all your other  characters" in t:
					if "\" and \"" in aa:
						c = [-2, self.name(a, s='a'), -1, "Other", "OMore", 2, "Oother", "O&", "OName", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}", "Trait", self.trait(a), "ability"]
					else:
						c = [-2, self.name(a, s='a'), -1, "Other", "OMore", 1, "Oother", "OName=", self.name(a, s='n'), "Trait", self.trait(a), "ability"]
				elif "all your characters" in t:
					if "\" and \"" in aa:
						c = [-1, self.name(a, s='a'), -1, "Other", "OMore", 2, "Oother", "O&", "OName", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}", "ability"]
					else:
						c = [-1, self.name(a, s='a'), -1, "Other", "OMore", 1, "Oother", "OName=", self.name(a, s='n'), "ability"]
		elif "if you have another level  or higher character" in t or "if you have another character whose level is  or higher" in t:
			if "this gets + level and + power" in t:
				c = [0, self.digit(a, 2), -1, "More", 1, "LevelC", self.digit(a), "power", 0, self.digit(a, 1), -1, "More", 1, "LevelC", self.digit(a), "level"]
			elif "gets + power" in t:
				c = [0, self.digit(a, 1), -1, "More", 1, "LevelC", self.digit(a), "power"]
			elif "this gets + soul" in t:
				c = [0, self.digit(a, 1), -1, "More", 1, "LevelC", self.digit(a), "soul"]
		elif "if  is in your memory" in t:
			if "all your other  characters" in t:
				if "gets + power" in t:
					c = [-2, self.digit(a), -1, "Other", "OMore", 1, "OName=", self.name(a, s='n'), "OMemory", "Trait", self.trait(a), "power"]
			elif "this gets + power and the following ability" in t:
				c = [0, self.digit(a), -1, "More", 1, "Name=", self.name(a, s='n'), "Memory", "power", 0, self.name(a, s='a'), -1, "More", 1, "Name=", self.name(a, s='n'), "Memory", "ability"]
			elif "this gets + power" in t:
				c = [0, self.digit(a), -1, "More", 1, "Name=", self.name(a, s='n'), "Memory", "power"]
		elif "all your opponent's characters get" in t:
			if "get \"[" in aa:
				c = [-1, self.name(a, s='a'), -1, "Other", "opp", "ability"]
		elif ("all your other  and " in t and "\" and \"" in aa) or ("all your other  or " in t and "\" or \"" in aa):
			if "get the following ability" in t:
				c = [-2, self.name(a, s='a'), -1, "Other", f"Name", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}", "ability"]
		elif ("all your other  or  characters" in t or "all your other characters with" in t) and "» or «" in aa:
			if "get + power" in t:
				c = [-2, self.digit(a), -1, "Other", "Trait", f"{self.trait(a)}_{self.trait(a, 1)}", "power"]
		elif "all your other  characters" in t or "all of your other " in t or "all your other " in t:
			if "gets + power and " in t and "power and \"[" in aa:
				c = [-2, self.digit(a), -1, "Other", "Trait", self.trait(a), "power", -2, self.name(a, s="a"), -1, "Other", "Trait", self.trait(a), "ability"]
			elif "get + level and + power" in t:
				c = [-2, self.digit(a, 1), -1, "Other", "Trait", self.trait(a), "power", -2, self.digit(a), -1, "Other", "Trait", self.trait(a), "level"]
			elif "get + power" in t:
				if "all your other \"" in aa or "all of your other \"" in aa:
					c = [-2, self.digit(a), -1, "Other", "Name", self.name(a, s='n'), "power"]
				else:
					c = [-2, self.digit(a), -1, "Other", "Trait", self.trait(a), "power"]
			elif "get + soul" in t:
				if "all your other \"" in aa or "all of your other \"" in aa:
					c = [-2, self.digit(a), -1, "Other", "Name=", self.name(a, s='n'), "soul"]
				else:
					c = [-2, self.digit(a), -1, "Other", "Trait", self.trait(a), "soul"]
			elif "get +x power" in t:
				if "x =  times the level of that character" in t:
					c = [-2, self.digit(a), -1, "Other", "Trait", self.trait(a), "xlevel", "x", self.digit(a), "power"]
			elif "get \"[" in aa:
				c = [-2, self.name(a, s='a'), -1, "Other", "Trait", self.trait(a), "ability"]
		elif ("all your other characters with" in t and "characters with \"" in aa) or ("all your other" in t and "all your other \"" in aa):
			if "gets + power and " in t and "power and \"[" in aa:
				if ("all your other \"" in aa and "\" and \"" in aa) or ("all your other characters with \"" in aa and "\" or \"" in aa):
					c = [-2, self.digit(a), -1, "Other", "Name", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}", "power", -2, self.name(a, -1, s="a"), -1, "Other", "Name", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}", "ability"]
			elif "get the following ability" in t or ("gets \"[" in aa or "get \"[" in aa):
				if "if there are  or more cards in your memory" in t:
					if "and this gets \"" in aa:
						c = [-32, self.name(a, s='a'), -1, "Other", "OMore", self.digit(a), "OMemory", f"Name", f"{self.name(a, s='n')}", "ability"]
				else:
					c = [-2, self.name(a, s='a'), -1, "Other", f"Name", f"{self.name(a, s='n')}", "ability"]
			elif "get + power" in t or "gets + power" in t:
				if self.name(a, s='a') in self.text_name:
					c = [-2, self.digit(a), -1, "Other", "Text", self.text_name[self.name(a, s='a')], "power"]
				elif "all your other cards named  and " in t or "all your other  and " in t:
					c = [-2, self.digit(a), -1, "Other", "Name", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}", "power"]
				elif "all your other characters with  or  or  in name" in t:
					if "\" is in your climax area" in aa:
						c = [-2, self.digit(a), -1, "Other", "Name", f"{self.name(a, 2, s='n')}_{self.name(a, 4, s='n')}_{self.name(a, 6, s='n')}", "cx", self.name(a, s='n'), "power"]
					else:
						c = [-2, self.digit(a), -1, "Other", "Name", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}_{self.name(a, 4, s='n')}", "power"]
				elif "all your other characters with  or " in t:
					c = [-2, self.digit(a), -1, "Other", "Name", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}", "power"]
				elif "all your other  or  or " in t:
					c = [-2, self.digit(a), -1, "Other", f"Name", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}_{self.name(a, 4, s='n')}", "power"]
				else:
					c = [-2, self.digit(a), -1, "Other", f"Name", f"{self.name(a, s='n')}", "power"]
			elif "gets + level" in t or "get + level" in t:
				c = [-2, self.digit(a), -1, "Other", f"Name", f"{self.name(a, s='n')}", "level"]
		elif "all your other characters" in t:
			if "get the following ability" in t:
				c = [-2, self.name(a, 1), -1, "Other", "ability"]
			elif "get + power" in t:
				if "whose level is  or lower" in t:
					c = [-2, self.digit(a, 1), -1, "Other", "LevelC", self.digit(a), "lower","power"]
				else:
					c = [-2, self.digit(a), -1, "Other", "power"]
			elif "get + level" in t:
				c = [-2, self.digit(a), -1, "Other", "level"]
			elif "get +x power" in t:
				if "x =  multiplied by that character's level" in t or "x =  times level of that character" in t:
					c = [-2, self.digit(a), -1, "Other", "xlevel", "x", self.digit(a), "power"]
		elif "if all your characters have  or \"" in aa and "in its card name" in t:
			if "this gets + power" in t:
				c = [0, self.digit(a), -1, "All", "Name", f"{self.name(a, 1)}_{self.name(a, 3)}", "power"]
		elif "if all your characters are «" in aa or "if all of your characters are «" in aa or "if all your characters have «" in aa:
			if "this gets + power" in t:
				c = [0, self.digit(a), -1, "All", "Trait", f"{self.trait(a)}", "power"]
		elif "if there are  or fewer characters" in t:
			if "in your opponent's center stage" in t:
				if "this gets + power" in t:
					c = [0, self.digit(a, 1), -1, "More", self.digit(a), "Center", "opp", "lower", "power"]
		elif "if there are  or fewer climax cards in your waiting room" in t:
			if "this gets + power" in t:
				c = [0, self.digit(a, 1), -1, "More", self.digit(a), "Climax", "Waiting", "lower", "power"]
		elif "if the number of your other  or  characters is  or more" in t:
			if "this gets + power" in t:
				c = [0, self.digit(a, 1), -1, "More", self.digit(a), "other", "Trait", f"{self.trait(a)}_{self.trait(a, 1)}", "power"]
		elif "you have  or more other" in t or "if the number of other  characters you have is  or more" in t or "if the number of your other  characters is  or more" in t:
			if "this gets  and is also considered to have  as the name" in t:
				c = [0, self.trait(a), -1, "More", self.digit(a), "other", "Trait", self.trait(a), "trait", 0, self.name(a, s='n'), -1, "More", self.digit(a), "other", "Trait", self.trait(a), "name"]
			elif "this gets + power" in t and "and \"[" in a:
				c = [0, self.digit(a, 1), -1, "More", self.digit(a), "other", "Trait", self.trait(a), "power", 0, self.name(a, 1), -1, "More", self.digit(a), "Trait", self.trait(a), "ability"]
			elif "this gets + power" in t:
				if "or more other \"" in aa:
					c = [0, self.digit(a, 1), -1, "More", self.digit(a), "other", "Name=", self.name(a, s='n'), "power"]
				elif "characters with  or " in t:
					c = [0, self.digit(a, 1), -1, "More", self.digit(a), "other", "Trait", f"{self.trait(a)}_{self.trait(a, 1)}", "power"]
				else:
					c = [0, self.digit(a, 1), -1, "More", self.digit(a), "other", "Trait", self.trait(a), "power"]
			elif "this gets \"[" in aa or "this gets the following ability" in t:
				c = [0, self.name(a, 1), -1, "More", self.digit(a), "Trait", self.trait(a), "other", "ability"]
		elif "if you have  or fewer other characters" in t or "if the number of other characters you have is  or less" in t or "if the number of your other characters is  or less" in t:
			if "this gets + power and the following ability" in t:
				c = [0, self.digit(a, 1), -1, "More", self.digit(a), "lower", "other", "power", 0, self.name(a, s='a'), -1, "More", self.digit(a), "lower", "other", "ability" ]
			elif "this gets + power" in t:
				c = [0, self.digit(a, 1), -1, "More", self.digit(a), "lower", "other", "power"]
		elif "if you do not have another character" in t or "if you have no other character" in t or "if you do not have any other characters" in t:
			if "this gets + level and + power" in t:
				c = [0, self.digit(a, 1), -1, "More", 0, "lower", "other", "power", 0, self.digit(a), -1, "More", 0, "lower", "other", "level"]
			elif "this gets + power and " in t:
				if "in your center stage" in t:
					c = [0, self.digit(a), -1, "NoCH", "Center", "other", "power", 0, self.name(a, s="a"), -1, "CONT", "ability"]
			elif "this gets + power" in t:
				if "in the center stage" in t:
					c = [0, self.digit(a), -1, "More", 0, "lower", "Center", "other", "power"]
				else:
					c = [0, self.digit(a), -1, "More", 0, "lower", "other", "power"]
		elif "cost of the character opposite this is  or lower" in t:
			if "this does not reverse" in t:
				c = [0, "", -1, "no_reverse", "cost", self.digit(a), "lower"]
		elif "for each marker under this" in t or "for each marker underneath this" in t:
			if "this gets + level and + power" in t:
				c = [0, self.digit(a, 1), -1, "Each", "marker", "power", 0, self.digit(a), -1, "Each", "marker", "level"]
			elif "this gets + power" in t or "this gets - power" in t:
				c = [0, self.digit(a), -1, "Each", "marker", "power"]
		elif "during this's battle, you cannot play event cards and  from your hand" in t or "during this's battle, you cannot play event cards and  from hand" in t:
			c = [0, "", -1, "no_backup", "no_event", "battle"]
		elif "during this's battle, your opponent cannot play  from hand" in t and "\"Backup\"" in a:
			c = [0, "", -1, "no_backup", "opp", "battle"]
		elif "your opponent cannot play event cards and  from his or her hand" in t:
			c = [0, "", -1, "no_backup", "no_event", "opp"]
		elif "your opponent cannot play events from hand" in t:
			c = [0, "", -1, "no_event", "opp"]
		elif ("you cannot play event cards or  from your hand" in t and "event cards or \"backup\"" in aa) or "you cannot play events or backup from hand" in t:
			c = [0, "", -1, "no_backup", "no_event"]
		elif "you cannot play events from hand" in t:
			c = [0, "", -1, "no_event"]
		elif "you cannot play a climax card from your hand" in t:
			# during your climax phase
			c = [0, "", -1, "no_climax"]
		elif "you cannot put  card from your hand in your clock and draw cards during your clock phase" in t or "you cannot put a card from your hand in your clock and draw cards during your clock phase" in t:
			c = [0, "", -1, "no_clock"]
		elif "your opponent cannot play climax cards from hand" in t:
			c = [0, "", x, "no_climax", "opp"]
		elif "your opponent cannot use any act of characters on his or her stage" in t:
			c = [0, "", x, "no_act", "opp"]
		elif "your opponent cannot use " in t and "\"[auto] encore\"" in aa:
			c = [0, "", x, "no_encore", "opp"]
		elif "you cannot use " in t and "\"[auto] encore\"" in aa:
			c = [0, "", x, "no_encore"]
		elif "your climax can be played from your hand without fulfilling color requirements" in t:
			c = [0, "", x, "any_climax"]
		elif "this cannot be returned to hand or put into memory" in t:
			c = [0, "", -1, "no_hand", "no_memory"]
		elif "this cannot be reverse by effects of [auto] abilities of your opponent's characters" in t:
			if "this cannot side attack" in t:
				c = [0, "", -1, "no_reverse_auto", "no_side"]
			else:
				c = [0, "", -1, "no_reverse_auto"]
		elif "this cannot become reverse" in t or "this does not reverse" in t or "this cannot be reverse" in t:
			c = [0, "", -1, "no_reverse"]
			if "if the level of the character opposite this is higher than the level of your opponent" in t:
				c += ["level",">p","Opposite"]
		elif "this cannot side attack" in t:
			if "this cannot move to another position" in t:
				c = [0, "", -1, "no_side", "no_move"]
			else:
				c = [0, "", -1, "no_side"]
		elif "this cannot front attack" in t:
			if "if the level of the character opposite this is higher than the level of this" in t:
				c = [0, "", -1, "no_front", "olevel", "higher"]
			else:
				c = [0, "", -1, "no_front"]
		elif "this cannot attack" in t:
			if "if there is  or fewer card in your clock" in t:
				c = [0, "", -1, "no_attack", "Clock", self.digit(a), "lower"]
			elif "if there is  or fewer character in your back stage" in t:
				c = [0, "", -1, "no_attack", "Stage", self.digit(a), "Back", "lower"]
			elif "if the character opposite this is higher level than this" in t:
				c = [0, "", -1, "no_attack", "OLevel"]
			else:
				c = [0, "", -1, "no_attack"]
		elif "this cannot be chosen by your opponent's effects" in t or "this cannot be chosen as the target of your opponent's effects" in t:
			c = [0, "", -1, "no_target"]
		elif "this cannot stand during your stand phase" in t:
			c = [0, "", -1, "no_stand"]
		elif "this's soul does not decrease by side attacking" in t:
			c = [0, "", -1, "no_decrease"]
		elif "during battles involving this" in t:
			if "this gets +x power" in t:
				if "x =  times level of that character" in t:
					if "if the battle opponent of this has " in t:
						c = [0, self.digit(a), -1, "Battle", "otrait", self.trait(a), "xolevel", "x", self.digit(a), "power"]
			elif "gets + power" in t:
				if "if the battle opponent of this is level  or higher" in t:
					c = [0, self.digit(a, 1), -1, "Battle", "olevel", self.digit(a), "power"]
				elif "if the battle opponent of this has  or " in t and "» or «" in aa:
					c = [0, self.digit(a), -1, "Battle", "otrait", f"{self.trait(a)}_{self.trait(a, 1)}", "power"]
				elif "if the battle opponent of this has " in t and "has «" in aa:
					c = [0, self.digit(a), -1, "Battle", "otrait", self.trait(a), "power"]
			elif "this gets " in t:
				c = [0, self.trait(a), -1, "Battle", "trait"]
		elif "if the character opposite this has no traits" in t:
			if "this gets the following ability" in t:
				c = [0, self.name(a, s='a'), -1, "Opposite", "#traits", 0, "#lower", "ability"]
		elif "if the number of cards in your opponent's clock is  or more" in t:
			if "this gets + power" in t:
				c = [0, self.digit(a, 1), -1, "Clock", self.digit(a), "opp", "power"]
		elif "all your characters whose level is higher than your level" in t:
			if "gets + power" in t:
				c = [-1, self.digit(a), -1, "LevelP", "power"]
		elif "all your characters get" in t or "all of your characters get" in t:
			if "get + power and + soul" in t:
				c = [-1, self.digit(a), x, "CONT", "power", -1, self.digit(a, 1), -1, "CONT", "soul"]
			elif "get + soul" in t:
				c = [-1, self.digit(a), x, "CONT", "soul"]
			elif "get + power" in t:
				c = [-1, self.digit(a), x, "CONT", "power"]
			elif "get the following ability" in t:
				c = [-1, self.name(a, s='a'), x, "CONT", "ability"]
		elif "character opposite this" in t:
			if "gets + soul and cannot side attack" in t:
				c = [-6, "[CONT] This cannot side attack.", x, "Opposite", "ability", -6, self.digit(a), -1, "Opposite", "soul"]
			elif "gets + soul" in t:
				c = [-6, self.digit(a), x, "Opposite", "soul"]
			elif "gets - soul" in t:
				c = [-6, self.digit(a), x, "Opposite", "soul"]
			elif ("gets " in t and "gets \"[" in aa) or "this gets the following ability" in t:
				c = [-6, self.name(a, s='a'), x, "Opposite", "ability"]
			elif "gets " in t:
				c = [-6, self.trait(a), x, "Opposite", "trait"]
			elif "cannot move to another position on the stage" in t:
				c = [-6, "[CONT] This card cannot move to another position on the stage.", x,"Opposite","ability"]
		elif "if you would pay the act cost for  of your characters in your hand or stage" in t:
			if "you may put  marker from underneath this in your waiting room instead of  card from your stock" in t:
				c = [0, self.digit(a), x, "astock"]
		elif "this gets + level and + power" in t:
			c = [0, self.digit(a, 2), x,"Stage", "power", 0, self.digit(a, 1), x, "Stage", "level"]
		elif "this gets +x power" in t:
			if "x =  multiplied by the level of the character opposite this" in t:
				c = [0, self.digit(a), x, "X", "xlevel", "opposite", "power", "x", self.digit(a)]
			elif "x =  times the highest level amongst your characters with  in the name" in t:
				c = [0, self.digit(a), x, "X", "xhighlevel", "xName", self.name(a, s='n'), "power", "x", self.digit(a)]
		elif "this gets - level" in t:
			c = [0, self.digit(a), x, "Stage", "level"]
		elif "this gets + power" in t:
			c = [0, self.digit(a), x, "Stage", "power"]
		elif "this cannot move to another position" in t:
			c = [0, "", x, "no_move"]

		if "during your turn" in t or "during your opponent's turn" in t or "on your turn" in t:
			for cc in ("ability","power","soul","level","name","trait"):
				if cc in c:
					c.insert(c.index(cc),"Turn")
					if "during your opponent's turn" in t:
						c.insert(c.index(cc),"Topp")

		return c

	def play(self, a=""):
		t = self.text(a)

		if "if there are no characters in your back stage, you cannot play this from hand" in t:
			return [0, "Character", "Back", "lower", "play"]
		elif "if you don't have a character with  in name, you may not play this from hand" in t:
			return [0,"Name",self.name(a,s='n'),"lower","play"]
		elif ("you do not have an  character" in t or "you do not have a  character" in t or "if you do not have any  characters" in t or "if you have no  characters" in t or "if you don't have a  character" in t) and ("this cannot be played from hand" in t or " this cannot be played from your hand" in t or "you cannot play this from your hand" in t or "you cannot play this from hand" in t):
			return [0, "Trait", self.trait(a), "lower", "play"]
		elif "if you have  or fewer  characters, you cannot play this from hand" in t or "if the number of  characters on your stage is  or less, this cannot be played from your hand" in t or "if you have  or less  characters, this cannot be played from your hand" in t or "if you have  or fewer  characters, you may not play this from hand" in t:
			return [self.digit(a), "Trait", self.trait(a), "lower", "play"]
		elif "if the number of characters in your center stage is  or more, this cannot be played from your hand" in t:
			return [self.digit(a), "Character", "Center", "play"]
		elif "if you have  or more characters, you cannot play this from your hand" in t:
			return [self.digit(a), "Character", "play"]
		return []

	def climax(self, a=""):
		e = []
		b = []
		text = self.text(a)

		self.cond = [0, 0, 0]
		if "for the turn" in text or " until end of turn" in text:
			x = 1
		else:
			x = -1

		if "when this is placed on your climax area from your hand" in text or 'when this is placed from hand to the climax area' in text or "when this is placed on your climax area from hand" in text:
			if "perform the standby effect" in text or "perform the [standy] effect" in text:
				return self.trigger("standby")
			elif "choose up to  level  or lower character in your waiting room" in text:
				if "put it in your stock" in text:
					e = [self.digit(a), "salvage", f"CLevel_<={self.digit(a, 1)}", "Stock", "show", "upto"]
					self.cond[0] += 2
			elif "choose up to  character with soul in its trigger icon in your waiting room" in text:
				if "return it to your hand" in text:
					e = [self.digit(a), "salvage", "CTrigger_soul", "upto", "show"]
					self.cond[0] += 1
			elif "choose up to   card in your waiting room" in text and self.colour_t(a).lower() in a.lower():
				if "put it in your stock" in text:
					e = [self.digit(a), "salvage", f"Colour_{self.colour_t(a)}", "Stock", "upto", "show"]
					self.cond[0] += 1
			elif "choose up to  character in your waiting room" in text:
				if "return it to your hand" in text:
					if "with level equal to or lower than your level" in text:
						e = [self.digit(a), "salvage", "CLevel_<=p", "show", "upto"]
						self.cond[0] += 1
			elif "put the top card of your deck in your stock" in text:
				e = ["stock", 1]
			elif "draw  card" in text:
				e = ["draw", self.digit(a)]
				self.cond[0] += 1

		if "all your characters get" in text or "all of your characters get" in text:
			if "+ power and + soul" in text:
				b = [-1, self.digit(a, self.cond[0]), x, "power", "do", [-1, self.digit(a, self.cond[0] + 1), x, "soul"]]
			elif "+ soul" in text:
				b = [-1, self.digit(a, self.cond[0]), x, "soul"]
			elif "+ power" in text:
				b = [-1, self.digit(a, self.cond[0]), x, "power"]
		elif "choose up to  of your characters" in text:
			if "those characters get + soul" in text:
				b = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "soul", "upto"]
		elif "choose  of your character" in text:
			if "that character gets + power and + soul" in text:
				b = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "power", "extra", "do", [-16, self.digit(a, self.cond[0] + 2), x, "soul"]]
			elif "that character gets + soul" in text:
				b = [self.digit(a, self.cond[0]), self.digit(a, self.cond[0] + 1), x, "soul"]
		elif "all your characters randomly get between +~+ soul" in text:
			b = [-1, self.digit(a, self.cond[0]), x, "random", self.digit(a, self.cond[0] + 1), "soul"]

		if e and b:
			return e + ["do", b]
		elif b:
			return b
		else:
			return []

	def trigger(self, a=""):
		c = []
		if "door" in a:
			c = ["pay", "may", "do", [1, "salvage", "Character", "upto", "show"], "text", "When this card triggers, you may choose a character in your waiting room, and return it to your hand."]
		elif "gate" in a:
			c = ["pay", "may", "do", [1, "salvage", "Climax", "upto", "show"], "text", "When this card triggers, you may choose a climax card in your waiting room, and return it to your hand."]
		elif "bounce" in a:
			c = ["pay", "may", "do", [1, "Character", "wind", "Opp", "may"], "text", "When this card triggers, you may choose an opponent's character on stage, and return it to his or her hand."]
		elif "standby" in a:
			c = ["pay", "may", "do", [1, "salvage", f"CLevel_standby", "Stage", "extra", "upto", "Standby", "do", [-16, "rested"]], "text", "When this card triggers, you may choose 1 character with a level equal to or less than your level +1 in your waiting room, and put it on any position of your stage as [REST]"]
		elif "draw" in a:
			c = ["pay", "may", "do", ["draw", 1], "text", "When this card triggers, you may draw a card."]
		elif "soul" in a:
			c = [-12, 1, 1, "soul", "text", "Give +1 soul to the attacking character until the end of the turn."]
		elif "shot" in a:
			c = [-12, "[AUTO] When the damage dealt by this card is cancelled, deal one damage to your opponent", -2, "give", "text", "During this turn, when the next damage dealt by the attacking character that triggered this card is canceled, deal 1 damage to your opponent."]
		elif "stock" in a:
			c = ["pay", "may", "do", ["stock", 1], "text", "When this card triggers, you may put the top card of your deck into your stock"]
		elif "treasure" in a:
			c = [0, "hander", "do", ["pay", "may", "do", ["stock", 1]], "text", "When this card triggers, return this card to your hand. You may put the top card of your deck into your stock"]
		elif "choice" in a:
			c = ["pay", "may", "do", [1, "salvage", "CTrigger_soul", "upto", "show", "choice"], "text", "When this card triggers, you may choose a character with [SOUL] in its trigger icon in your waiting room, and return it to your hand or put it into your stock."]
		return c

	def digit(self, a="", i=0, p=False):
		n = []
		t = str(a)

		for ss in self.text_name:
			if f"\"{ss}\"" in t:
				t = t.replace(f"\"{ss}\"", "")
		if t.count("[") >= 2:
			for item in self.status:
				t = t.replace(item, self.status[item])
		for ablt in self.ability:
			# if t.startswith(ablt):
			t = t.replace(ablt, "")
		for ss in self.set_only:
			t = t.replace(ss, "")

		if t.startswith(" "):
			t = t[1:]
		if " (" in t:
			if "(If it is not, the revealed card is returned to its original place)\n" in t:
				t = t.replace("(If it is not, the revealed card is returned to its original place)\n", "")
			else:
				t = t.split(" (")[0]

		for s in range(7):
			if f"({s})" in t:
				t = t.replace(f"({s})", "()")

		if "[()" in t and ")]" not in t:
			t = t.replace("]", "]").replace("[()", "")
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

		if p:
			t = t.split()
		elif "[counter] backup" in a.lower():
			t = t.split("[")[0].split()
		elif ("get \"" in t or "gets \"" in t) and t.count("[") == 1:
			t = t.split("[")[0].split()
		elif t.count("]") == 1:
			if t.startswith("[") or t.startswith(" ["):
				t = t.split("]")[1].split()
			elif t.startswith("\" ENCORE ["):
				t = t.split("]")[1].split()
			elif any(t.lower().startswith(rr) for rr in self.abstart):
				t = t.split("]")[1].split()
			elif t.count("[") == 0:
				if "gets the following ability. \"" in t or "get \"" in t or "gets \"" in t or "get the following ability until end of turn. \"" in t or "and the following ability. \"" in t:
					if t.count("]") == 1 and t.index("]")<10:
						t = t.split("]")[1].split()
					else:
						t = t.split("]")[0].split()
				else:
					t = t.split("]")[1].split()
			else:
				if any(sk.lower() in t.lower() for sk in self.skill_name):
					for sk in self.skill_name:
						if sk.lower() in t.lower():
							t = t.replace(sk,sk.replace("]","")).split("]")[0].split()
							break
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
		# n = [int(unicodedata.numeric(s)) for s in a.replace("+", "").split("]")[-1].split() if self.is_number(s)]
		if len(n) < 1:
			n = [0]
			i = 0
		return n[i]

	def trait(self, a="", i=0):
		if a.count("«") >= 1:
			t = []
			for nx in range(a.count("«")):
				t.append(a.split("«")[nx + 1].split("»")[0])

			if len(t) < 1:
				t = 0
				i = 0
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

	def colour_t(self, a="", i=0):
		t = self.text(a=a, c=False)
		if any(f" {colour} " in t for colour in self.colour):
			for colour in self.colour:
				if f" {colour} " in t:
					t = f"{colour[0].upper()}{colour[1:]}"
		return t

	def name(self, a="", i=0, s="", n="",p=False):
		if n:
			n = "'"
		else:
			n = "\""
		# elif a.count("\"") == 2:
		t = a
		if len(s)==2:
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
					bc = a[a.lower().index(ba)+len(ba):a.lower().index('. (')+1]
				else:
					bc = a[a.lower().index(ba)+len(ba):]
			t = f"[AUTO] At the beginning of your encore step{bc}"
		elif "ac" in s:
			ba = "at the start of encore step"
			bc = ""
			if ba in a.lower():
				if ". (" in a.lower():
					bc = a[a.lower().index(ba)+len(ba):a.lower().index('. (')+1]
				else:
					bc = a[a.lower().index(ba)+len(ba):]
			t = f"[AUTO] At the beginning of the encore step{bc}"
		elif "at" in s:
			ba ="at the beginning of your next"
			bb = "at the start of your next"
			bc = ""
			if ba in a.lower():
				if ". (" in a.lower():
					bc = a[a.lower().index(ba)+len(ba):a.lower().index('. (')+1]
				else:
					bc = a[a.lower().index(ba)+len(ba):]
			elif bb in a.lower():
				if ". (" in a.lower():
					bc = a[a.lower().index(bb)+len(bb):a.lower().index('. (')+1]
				else:
					bc = a[a.lower().index(bb)+len(bb):]
			t = f"[AUTO] At the beginning of your{bc}"
		elif "a" in s:
			c = a.count(n)
			if c == 2:
				t = a.split(n)[1]
			elif c > 2:
				t = a.split(n)
				t = [p for p in t if any(p.startswith(abl) for abl in self.ability[:3]) and f"\"{p}\"" in a]

				if len(t) < 1:
					t = ""
					i = 0
				else:
					t = t[i]

			if "(" in t and ")" in a and "encore" not in t.lower():
				if "[(" in t and (")]" in t or (")" in t and "]" in t) and not ")]" in t)and t.count("(") == 1:
					pass

				else:
					t = t.split("(")[0]
		elif "p" in s:
			k = False
			c = a.count(n)

			if c >= 2:
				t = a.split(n)
				t = [p for p in t if f"\"{p}\"" in a]
				for p in range(len(t)):
					if "'s " in t[p]:
						k = True
						t[p] = t[p].replace("'s ", "?s ")
					t[p] = t[p].replace("'", "\"")
					if k:
						k = False
						t[p] = t[p].replace("?s ", "'s ")
				if len(t) < 1:
					t = ""
					i = 0
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
					i = 0
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
		a = a.lower()
		if " (" in a:
			a = a.split(" (")[0]
		for rep in self.resource:
			if rep in a:
				a = a.replace(rep, self.resource[rep])
		for rep in self.text_change:
			if rep in a:
				a = a.replace(rep, self.text_change[rep])

		return a

	def text(self, a="", i=1, l=True, c=True):
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
			t = t.replace(f"{ss} ", "")

		if "[ACT]" in t:
			t = t.replace("[ACT]", "ACT")

		if t.startswith(" "):
			t = t[1:]

		if " (" in t and ")\"" not in t and t.count(" (") >= 2:
			t = t.split(" (")[0]
		elif " (" in t and ")\"" in t and t.count(" (") == 1:
			pass

		if l:
			t = t.lower()
		else:
			t = t

		for rep in self.resource:
			t = t.replace(rep, self.resource[rep])

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

		# remove trait
		if t.count("«") >= 1:
			trait = []
			for nx in range(t.count("«")):
				trait.append(t.split("«")[nx + 1].split("»")[0])
			for tr in trait:
				t = t.replace(tr, "").replace("«", "").replace("»", "")

		# remove name
		if t.count('"') > 0 and t.count('"') % 2 == 0:
			if not t.startswith("brainstorm"):
				name = []
				for nx in range(t.count('"') // 2):
					name.append(t.split('"')[nx + 1 + nx])
				for nm in name:
					t = t.replace(f"\"{nm}\"", "")
		elif t.count('"') == 3:
			name = a.split('"')[1]  # .split('"')[0]
			t = t.replace(f"\"{name.lower()}\"", "")

		# t = "".join(s for s in t if not s.isdigit())
		t = t.translate(str.maketrans('', '', self.digits))

		if c:
			for colour in self.colour:
				if f" {colour} " in t:
					t = t.replace(f" {colour} ", "  ")

		if t.startswith(" "):
			t = t[1:]

		return t

	def seperate(self,tt,a,t,aa,rev=False):
		if rev:
			c = self.convert(a,t.split(tt)[0], aa)
			t = tt + t.split(tt)[1]
		else:
			c = ["do", self.convert(a, tt + t.split(tt)[1], aa)]
			t = t.split(tt)[0]
		return c,t

	def is_number(self, s):
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
