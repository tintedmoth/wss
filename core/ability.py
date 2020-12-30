from unicodedata import numeric

from core.markreplace import markreplace


class Ability:
	ablt = 0
	cx = False
	center = False
	resource = {"library": "deck", "gain": "get", "hoose a ": "hoose 1 ", "a card": "1 card", "is equal to": "=",
	            "all of your": "all your", "discard an": "put 1", "discard a ": "put 1 ", "put a ": "put 1 ", "put an ": "put 1 ",
	            "or a ": "or 1 ", "this card": "this", "three cards": "3 cards", "two cards": "2 cards",
	            " four ": " 4 ", " five ": " 5 ", " six ": " 6 ", " seven ": " 7 ", "into your": "in your",
	            " one ": " 1 ", " two ": " 2 ", "reversed": "reverse", "climax zone": "climax area",
	            "three": "3", "facing": "opposite", " 2 soul": " soulsoul", " 2 Soul": " soulsoul",
	            "foe or 1 new": "foe or a new", "the 2 of us": "the two of us", "libraries": "decks",
	            "times per turn": "time per turn", "when 1 card named": "when a card named", "frontal": "front",
	            "When 1 card named": "When a card named", "not an": "not a", "for an": "for 1",
	            "if a climax is put": "if 1 climax is put",
	            "if 1 card": "if a card", "If 1 card": "If a card", "back row": "back stage", "level-up": "level up",
	            "front row slots on stage": "position on your center stage", "front row": "center stage"}
	icon = {"[SHOT]": "SHOT", "[BOUNCE]": "BOUNCE", "[POOL]": "POOL", "[SOUL]": "SOUL", "[TREASURE]": "TREASURE", "[DOOR]": "DOOR", "[STANDBY]": "STANDBY", "[DRAW]": "DRAW", "[GATE]": "GATE", "[STOCK]": "STOCK"}
	colour = ("red", "blue", "yellow", "green")
	ability = ("[CONT]", "[AUTO]", "[ACT]", "[CLOCK]", "[COUNTER]")
	status = {"[REST]": "REST", "[STAND]": "STAND", "[REVERSE]": "REVERSE", }
	stage = ("Center", "Back")
	attack = ("Attack", "Declaration", "Trigger", "Counter", "Damage", "Battle")
	alpha = "qwertyuiopasdfghjklzxcvbnm0123456789"
	text_name = {"Assist": "] Assist", "Memory": "] Memory_] Recollection", "Experience": "] Experience",
	             "Accelerator": "] Accelerator", "Change": "] Change",
	             "[AUTO] Encore [Put the top card of your deck into your clock]": "[AUTO] Encore [Put the top card of your deck into your clock]",
	             "[AUTO] Encore [Put 1 character from your hand into your waiting room]": "[AUTO] Encore [Put 1 character from your hand into your waiting room]_[AUTO] Encore [Put a character from your hand into your waiting room]",
	             "[AUTO] Encore [Put a character from your hand into your waiting room]": "[AUTO] Encore [Put 1 character from your hand into your waiting room]_[AUTO] Encore [Put a character from your hand into your waiting room]"}
	remove_text = ["Encore [Put 1 character from your hand in your waiting room]", "Encore [Put a character from your hand into your waiting room]", "Encore [Put the top card of your deck into your clock]"]
	set_only = markreplace["set_only"]

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
				o = ["RevealStock", self.name(a, s='n')]
			elif "\" from your hand]" in t:
				o = ["Reveal", self.name(a, s='n')]
		elif "put this in your memory]" in t or "send this to memory]" in t:
			o = ["Memory", 0]
		elif "put 1 \"" in t and "\" from your hand to the waiting room]" in t:
			o = ["Discard", 1, "Name=", self.name(a, s='n')]
		elif "put 1 \"" in t and ("from your memory to your waiting room]" in t or "from your memory to the waiting room]" in t):
			o = ["MDiscard", 1, "Name=", self.name(a, s='n')]
		elif "put 1 climax from your hand in your waiting room]" in t or "put 1 climax card from hand to the waiting room]" in t or "put 1 climax card from your hand to the waiting room]" in t:
			o = ["Discard", 1, "Climax"]
		elif "put 1 character from your hand in your waiting room]" in t:
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
		elif "discard 1 card from your hand to the waiting room]" in t or "put 1 card from your hand in your waiting room]" in t or "discard 1 card from hand to the waiting room]" in t:
			o = ["Discard", 1, ""]
		elif "return this to your hand]" in t:
			o = ["Hander", 0, ""]
		elif "return 2 characters from your waiting room to your deck. shuffle your deck afterwards]" in t or "return 2 characters in your waiting room to your deck. shuffle your deck afterwards]" in t:
			o = ["WDecker", 2, "Character"]
		elif "put this in your clock]" in t:
			o = ["ClockS", 0]
		elif "put 2 markers from under this in your waiting room]" in t:
			o = ["Marker", 2]
		elif "put 1 marker from under this in the waiting room]" in t:
			o = ["Marker", 1]
		elif "put 1 character with \"" in t and "\" in its card name from your stage in your clock]" in t:
			o = ["ClockS", 1, "Name", self.name(a, s="n")]
		elif "put 1 card named \"" in t and "\" from your hand in your waiting room]" in t:
			o = ["Discard", 1, "Name=", self.name(a, s="n")]
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
			o = ["Rest", 1, "Name", self.name(a, s="n")]
		elif "«" in t:
			t1 = str(a)
			for item in self.status:
				t1 = t1.replace(item, self.status[item])
			t1 = t1.replace("[ACT] ", "").replace("[AUTO]", "").split("]")[0]

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
			elif "put a  character from your hand in your waiting room" in t1.lower() or "discard a  character card from your hand to the waiting room" in t1.lower() or "discard a  character from hand to the waiting room" in t1.lower():
				o = ["Discard", 1, "Trait", trait[0]]
			elif "put a  character card from your hand in clock" in t1.lower() in t1.lower():
				o = ["ClockH", 1, "Trait", trait[0]]
			elif "put 1  or  character on your stage in your clock" in t1.lower():
				o = ["ClockS", 1, "Trait", f"{trait[0]}_{trait[1]}"]
			elif "put a  character from your stage in your clock" in t1.lower():
				o = ["ClockS", 1, "Trait", trait[0]]
			elif "put a  character from your stage in your waiting room" in t1.lower():
				o = ["Waiting", 1, "Trait", trait[0]]
			elif "put a  character from your memory in your waiting room" in t1.lower():
				o = ["MDiscard", 1, "Trait", trait[0]]

		if "put the top card of your deck in your clock &" in t or "put the top card of your deck in your clock," in t:
			r = ["ClockL", 1]
		elif "put 1 card from your hand in your waiting room &" in t or "discard 1 card from your hand to the waiting room &" in t or "discard 1 card from your hand to waiting room &" in t or "discard 1 card from hand to the waiting room &" in t or "put 1 card from your hand to your waiting room &" in t:
			r = ["Discard", 1, ""]
		elif "put 1 climax from your hand in your waiting room &" in t:
			r = ["Discard", 1, "Climax"]
		elif "put 1 card from your hand in your clock &" in t:
			r = ["ClockH", 1, ""]
		elif "put 1 character with \"" in t and "\" in its card name from your stage in your clock &" in t:
			r = ["ClockS", 1, "Name", self.name(a, s="n")]
		elif "rest 2 of your characters &" in t:
			r = ["Rest", 2, ""]
		elif "rest 1 of your characters &" in t:
			r = ["Rest", 1, ""]

		return s + r + o

	def req(self, a="", x=0, m=0, ss=(), nn=0, h=(), my=(), wr=()):
		""":param a: ability (string)
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
			if "\" from your hand]" in t or "\" in your hand and put it in your stock]" in t:
				if len(h) >= 1 and any(self.name(a, s='n') in hn[1] for hn in h):
					ro = True
		elif "put this in your memory]" in t or "send this to memory]" in t:
			ro = True
		elif "put this from your hand in your waiting room]" in t or "discard this from your hand to the waiting room]" in t or "discard this from hand to the waiting room]" in t:
			ro = True
		elif "put 1 card from your hand in clock]" in t or "put 1 card from your hand in your clock" in t:
			if len(h) >= 1:
				ro = True
		elif "put 1 \"" in t and "\" from your hand to the waiting room]" in t:
			if len(h) >= 1 and any(self.name(a, s='n') in hn[1] for hn in h):
				ro = True
		elif "put 1 \"" in t and ("\" from your memory to your waiting room]" in t or "\" from your memory to the waiting room]" in t):
			if len(my) >= 1 and any(self.name(a, s='n') in hn[1] for hn in my):
				ro = True
		elif "discard 2 cards from your hand to the waiting room]" in t:
			if len(h) >= 2:
				ro = True
		elif "discard 1 card from your hand to the waiting room]" in t or "put 1 card from your hand in your waiting room]" in t or "discard 1 card from hand to the waiting room]" in t:
			if len(h) >= 1:
				ro = True
		elif "discard a character card from your hand to the waiting room]" in t:
			if len([p for p in h if p[0] == "Character"]) >= 1:
				ro = True
		elif "put 1 character card from hand in memory]" in t:
			if len(h) >= 1:
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
			if len([sx for sx in ss if sx[0] != "" and self.name(a, s='n') in sx[1]]) >= 1:
				ro = True
		elif "put 1 card named \"" in t and "\" from your hand in your waiting room]" in t:
			if len(h) >= 1 and any(self.name(a, s='n') in hn[1] for hn in h):
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
		elif "return 2 characters from your waiting room to your deck. shuffle your deck afterwards]" in t or "return 2 characters in your waiting room to your deck. shuffle your deck afterwards]" in t:
			if len([sx for sx in wr if sx[0] == "Character"]) >= 2:
				ro = True
		elif "«" in t and t.count("[") >= 2:
			t1 = str(a)
			for item in self.status:
				t1 = t1.replace(item, self.status[item])
			t1 = t1.replace("[ACT] ", "").replace("[AUTO]", "").split("]")[0]

			trait = []
			for nx in range(t1.count("«")):
				trait.append(t1.split("«")[nx + 1].split("»")[0])
			for tra in trait:
				t1 = t1.replace(tra, "").replace("«", "").replace("»", "")

			for rep in self.resource:
				t1 = t1.replace(rep, self.resource[rep])
			# print(t1)
			if "rest 1 of your  characters and 1 of your  characters" in t1.lower():
				sn = {"0": [], "1": [], "2": []}
				sn["0"] = [sx for sx in ss if sx[0] == "Stand" and any(tx in sx[2] for tx in trait)]
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
			elif "put a  character from your hand in your waiting room" in t1.lower() or "[discard a  character card from your hand to the waiting room" in t1.lower() or "discard a  character from hand to the waiting room" in t1.lower():
				if len(h) >= 1 and len([p for p in h if any(tx in p[2] for tx in trait)]) >= 1:
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

		if "put 1 card from your hand in your waiting room &" in t or "discard 1 card from your hand to waiting room &" in t or "put 1 card from your hand to your waiting room &" in t:
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
			if len([sx for sx in ss if sx[0] != "" and self.name(a, s='n') in sx[1]]) >= 1:
				rr = True
		elif "rest 2 of your characters &" in t:
			if len([sx for sx in ss if sx[0] == "Stand"]) >= 2:
				rr = True
		elif "rest 1 of your characters &" in t:
			if len([sx for sx in ss if sx[0] == "Stand"]) >= 1:
				rr = True
		elif "&" not in t.replace("[act]", "").replace("[auto]", "").split("]")[0]:
			rr = True

		# print(rs,ro,rr)
		if rs and ro and rr:
			return True
		else:
			return False

	def act(self, a=""):
		t = self.text(a)
		aa = self.a_replace(a)
		if "until the end of your opponent's next turn" in t or "until the next end of your opponent's turn" in t:
			x = 2
		elif "for the turn" in t or " until end of turn" in t:
			x = 1
		else:
			x = 1
		if t.startswith("brainstorm"):
			if "for each climax card revealed this way," in t or "for each climax revealed" in t:
				if "draw up to  card" in t:
					return ["brainstorm", self.digit(a), "Climax", "do", ["drawupto", self.digit(a, 1)]]
				elif "choose  of your opponent's character" in t:
					if "that character gets - power" in t:
						if "in center stage" in t:
							return ["brainstorm", self.digit(a), "Climax", "do", [self.digit(a, 1), self.digit(a, 2), x, "power", "Opp", "Center"]]
						else:
							return ["brainstorm", self.digit(a), "Climax", "do", [self.digit(a, 1), self.digit(a, 2), x, "power", "Opp"]]
				elif "choose up to  cost  or lower character in your waiting room" in t:
					if "put them in separate slots on the stage" in t:
						return ["brainstorm", self.digit(a), "Climax", "do", [self.digit(a, 1), "salvage", f"Cost_<={self.digit(a, 2)}", "Stage", "upto"]]
				elif "choose up to   character in your waiting room" in t:
					if "return it to your hand" in t:
						return ["brainstorm", self.digit(a), "Climax", "do", [self.digit(a, 1), "salvage", f"Trait_{self.trait(a)}", "upto", "show"]]
				elif "choose up to  character in your waiting room" in t:
					if "return it to your hand" in t:
						return ["brainstorm", self.digit(a), "Climax", "do", [self.digit(a, 1), "salvage", "Character", "upto", "show"]]
				elif "choose   character from your waiting room" in t:
					if "return it to your hand" in t:
						if "choose  card from your hand" in t:
							if "put it in your waiting room" in t:
								return ["brainstorm", self.digit(a), "Climax", "do", [self.digit(a, 1), "salvage", f"Trait_{self.trait(a)}", "show", "do", ["discard", self.digit(a, 2), ""]]]
				elif "choose  of your characters with " in t and "\" in its card name" in aa:
					if "that character gets + soul" in t:
						return ["brainstorm", self.digit(a), "Climax", "do", [self.digit(a, 1), self.digit(a, 2), x, "soul", "Name", self.name(a, s='n')]]
				elif "choose  of your  characters" in t:
					if "that character gets + power" in t:
						return ["brainstorm", self.digit(a), "Climax", "do", [self.digit(a, 1), self.digit(a, 2), x, "power", "Trait", self.trait(a)]]
				elif "choose  level  or lower character in opponent's center stage" in t:
					if "return it to hand" in t:
						return ["brainstorm", self.digit(a), "Climax", "do", [self.digit(a, 1), "hander", "Opp", "Center", "Level", f"<={self.digit(a, 2)}"]]
				elif "choose up to  cost  or lower character in your opponent's center stage" in t:
					if "put it in the waiting room" in t:
						return ["brainstorm", self.digit(a), "Climax", "do", [self.digit(a, 1), "waitinger", "Opp", "Center", "Cost", f"<={self.digit(a, 2)}", "upto"]]
				elif "search your deck for up to   character" in t:
					if "reveal it" in t and "put it in your hand" in t:
						if "choose  card in your hand" in t:
							if "put it in your waiting room" in t:
								return ["brainstorm", self.digit(a), "Climax", "do", [self.digit(a, 1), "search", f"Trait_{self.trait(a)}", "show", "upto", "do", ["discard", self.digit(a, 2), ""]]]
						else:
							return ["brainstorm", self.digit(a), "Climax", "do", [self.digit(a, 1), "search", f"Trait_{self.trait(a)}", "show", "upto"]]
				elif "draw  card" in t:
					return ["brainstorm", self.digit(a), "Climax", "do", ["draw", self.digit(a, 1)]]
				elif "this gets + power and + soul" in t:
					return ["brainstorm", self.digit(a), "Climax", "do", [0, self.digit(a, 1), x, "power", 0, self.digit(a, 2), x, "soul"]]
			elif "for each  character revealed among those cards" in t:
				if "choose up to  level  or lower character in your waiting room" in t:
					if "put them on separate positions of your stage" in t:
						return ["brainstorm", self.digit(a), "Trait", self.trait(a), "each", "do", [self.digit(a, 1), "salvage", f"CLevel_<={self.digit(a, 2)}", "Stage", "seperate", "upto"]]
			elif "x = number of climax cards revealed this way" in t:
				if "search deck for up to x characters with  in name" in t:
					if "reveal them" in t and "put them in your hand" in t:
						if "discard x cards from your hand to the waiting room" in t:
							return ["brainstorm", self.digit(a), "Climax", "do", ["x", "search", f"Name_{self.name(a, s='n')}", "upto", "show", "do", ["discard", "x", ""]]]
			elif "if there is at least   among them" in t:
				return ["brainstorm", self.digit(a), "Name=", self.name(a, s='n'), "any", self.digit(a, 1), "do", [self.digit(a, 2), "salvage", f"Name=_{self.name(a, s='n')}", "Stage"]]
			elif "choose  level x or lower  character in your waiting room" in t:
				if "put it on any position of your stage" in t:
					if "x = the number of  characters revealed among those cards" in t:
						return ["brainstorm", self.digit(a), "Trait", self.trait(a), "any", 0, "do", [self.digit(a, 1), "salvage", f"TraitL_{self.trait(a)}_<=#", "Stage", "#", "#trait"]]
		elif t.startswith("backup"):
			return [1, self.digit(a), 1, "backup", self.digit(a, 1)]
		elif "draw  card" in t:
			if "if the number of your other  characters is  or more" in t:
				return ["draw", self.digit(a, 1), "More", self.digit(a), "other", "Trait", self.trait(a)]
			elif "choose  of your characters" in t:
				if "that character gets + power" in t:
					return ["draw", self.digit(a), "do", [self.digit(a, 1), self.digit(a, 2), x, "power"]]
			elif "discard  card from hand to the waiting room" in t or "discard  card from your hand to the waiting room" in t:
				return ["draw", self.digit(a), "do", ["discard", self.digit(a, 1), ""]]
			else:
				return ["draw", self.digit(a)]
		elif "reveal the top card of your deck" in t:
			if "if that card is level  or lower" in t:
				if "this gets the following ability" in t:
					return [-9, "reveal", "Level", self.digit(a), "lower", "do", [0, self.name(a, s="a"), x, "give"]]
			elif "if it's a climax card" in t:
				if "put it in your hand and discard  card from your hand to the waiting room" in t:
					return [-9, "reveal", "Climax", "do", ["draw", 1, "do", ["discard", self.digit(a), ""]]]
		elif "choose up to   and  " in t:
			if "from your waiting room" in t:
				if "put them in separate slots on the stage" in t:
					if "those characters get + power and + soul" in t:
						return [self.digit(a), "salvage", f"Name=_{self.name(a, s='n')}", "Stage", "upto", "extra", "do", [self.digit(a, 1), "salvage", f"Name=_{self.name(a, 2, s='n')}", "Stage", "seperate", "upto", "extra", "do", [-16, self.digit(a, 2), x, "power", "extra", "do", [-16, self.digit(a, 3), x, "soul"]]]]
		elif "choose up to  of your characters" in t:
			if "those characters gets + power and " in t and "power and «" in aa:
				return [self.digit(a), self.digit(a, 1), x, "upto", "power", self.digit(a), self.trait(a), x, "upto", "trait"]
		elif "choose   in your clock and put it in any slot on stage" in t:
			if "choose  card in your hand and put it in your clock" in t:
				return ["cdiscard", self.digit(a), f"Name=_{self.name(a, s='n')}", "Stage", "do", ["discard", self.digit(a), "", "Clock"]]
		elif "choose  of your characters with  in name" in t or "choose  of your characters with  in its card name" in t:
			if "that character gets + soul and this gets + power" in t:
				return [self.digit(a), self.digit(a, 1), x, "soul", "Name", self.name(a, s="n"), "do", [0, self.digit(a, 2), x, "power"]]
			elif "that character gets + power" in t:
				return [self.digit(a), self.digit(a, 1), x, "power", "Name", self.name(a, s="n")]
			elif "that character gets + level" in t:
				return [self.digit(a), self.digit(a, 1), x, "level", "Name", self.name(a, s="n")]
			elif "that character gets + soul" in t:
				return [self.digit(a), self.digit(a, 1), x, "soul", "Name", self.name(a, s="n")]
			elif "that character gets the following ability" in t:
				return [self.digit(a), self.name(a, s='a'), x, "give", "Name", self.name(a, s='n')]
		elif "choose  of your characters with" in t and "characters with \"" in a.lower():
			if "that character gets + power" in t:
				if "\" or \"" in a.lower():
					return [self.digit(a), self.digit(a, 1), x, "power", "Name", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}"]
				elif self.name(a, s='n') in self.text_name:
					return [self.digit(a), self.digit(a, 1), x, "power", "Text", f"{self.text_name[self.name(a, s='n')]}"]
		elif "return this to your hand" in t:
			return [0, "hander"]
		elif "look at the top card of your deck" in t:
			if "put it back either on top or bottom of the deck" in t:
				return [1, "looktop", "top", "bottom"]
			else:
				return [1, "looktop", "check"]
		elif "choose  character in your waiting room with  or " in t:
			if "return it to your hand" in t:
				return [self.digit(a), "salvage", f"Trait_{self.trait(a)}_{self.trait(a, 1)}", "show"]
		elif "choose  level  or lower  character in your waiting room" in t:
			if "put it in any slot on the stage" in t:
				return [self.digit(a), "salvage", f"TraitL_{self.trait(a)}_<={self.digit(a, 1)}", "Stage"]
		elif "choose  character in your waiting room" in t or "choose  character from your waiting room" in t:
			if "return it to your hand" in t:
				return [self.digit(a), "salvage", "Character", "show"]
		elif "choose up to  level  or lower character in your hand" in t:
			if "and put it in any slot on the stage" in t:
				return ["discard", self.digit(a), f"CLevel_<={self.digit(a, 1)}", "upto", "Stage"]
		elif "choose  of your  characters" in t:
			if "that character gets + level and + power" in t:
				return [self.digit(a), self.digit(a, 1), x, "Trait", self.trait(a), "level", "extra", "do", [-16, self.digit(a, 2), x, "power"]]
			elif "that character gets + power" in t:
				if "that character gets + power and  " in t:
					return [self.digit(a), self.digit(a, 1), x, "Trait", self.trait(a), "power", "extra", "do", [-16, self.trait(a, 1), x, "trait"]]
				else:
					if "at the end of the turn" in t and "put that character in the waiting room" in t:
						return [self.digit(a), self.digit(a, 1), x, "Trait", self.trait(a), "power", "extra", "do", [-16, "[AUTO] At the end of the turn, put this card into your waiting room.", -3, "ACT", "give"]]
					else:
						return [self.digit(a), self.digit(a, 1), x, "Trait", self.trait(a), "power"]
			elif "that character gets + level" in t:
				return [self.digit(a), self.digit(a, 1), x, "Trait", self.trait(a), "level"]
			elif "that character gets + soul" in t:
				return [self.digit(a), self.digit(a, 1), x, "Trait", self.trait(a), "soul"]
		elif "choose up to  of your  characters" in t:
			if "characters get + soul" in t:
				return [self.digit(a), self.digit(a, 1), x, "Trait", self.trait(a), "soul", "upto"]
		elif "choose  of your characters" in t:
			if "in your waiting room" in t:
				if "return it to the hand" in t:
					return [self.digit(a), "salvage", "Character", "show"]
			elif "that character gets + power and + soul" in t:
				return [self.digit(a), self.digit(a, 1), x, "power", self.digit(a), self.digit(a, 2), x, "soul"]
			elif "that character gets +x power" in t:
				if "x =  times level of that character" in t or "x =  times the level of that character" in t:
					return [self.digit(a), self.digit(a, 1), x, "X", "power", "xlevel", "x", self.digit(a, 1)]
			elif "that character gets + power" in t:
				return [self.digit(a), self.digit(a, 1), x, "power"]
			elif "that character gets + level" in t:
				return [self.digit(a), self.digit(a, 1), x, "level"]
			elif "that character gets + soul" in t:
				return [self.digit(a), self.digit(a, 1), x, "soul"]
			elif "that character gets  " in t:
				return [self.digit(a), self.trait(a), x, "trait"]
		elif "choose  random opponent's characters" in t:
			if "that character gets - power" in t:
				return [-11, self.digit(a), x, "power", "opp", "random"]
		elif "choose  of your opponent's center stage characters" in t or "choose  character in your opponent's center stage" in t:
			if "that character gets - power and gets " in t and "gets «" in aa:
				return [self.digit(a), self.digit(a, 1), x, "power", "Opp", "Center", "extra", "do", [-16, self.trait(a), x, "trait"]]
			elif "that character gets - power" in t:
				return [self.digit(a), self.digit(a, 1), x, "power", "Opp", "Center"]
		elif "choose   in your memory" in t:
			if "\" in your memory" in aa:
				if "put it in the stock" in t:
					return ["mdiscard", self.digit(a), f"Name=_{self.name(a, s='n')}", "Stock", "show"]
		elif "choose   character in your waiting room" in t:
			if "return it to your hand" in t:
				return [self.digit(a), "salvage", f"Trait_{self.trait(a)}", "show"]
		elif "choose  card in your opponent's waiting room" in t:
			if "put it on top of the deck" in t:
				return [self.digit(a), "salvage", "", "opp", "Library", "top", "show"]
		elif "choose  of your opponent's characters" in t:
			if "that character cannot stand during your opponent's next stand phase" in t or "that character doesn't stand during your opponent's next stand phase" in t:
				return [self.digit(a), "[CONT] This cannot [STAND] during your stand phase", 2, "give", "Opp"]
			elif "that character gets - power" in t:
				return [self.digit(a), self.digit(a, 1), x, "power", "Opp"]
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
			elif "put it in the waiting room" in t or "put it in your opponent's waiting room" in t:
				return [self.digit(a), "waitinger", "Opp", "Level", f"<={self.digit(a, 1)}", "Center"]
			elif "return it to hand" in t:
				return [self.digit(a), "hander", "Opp", "Level", f"<={self.digit(a, 1)}", "Center"]
		elif "choose  cost  or lower character in your opponent's center stage" in t:
			if "put it in the waiting room" in t:
				return [self.digit(a), "waitinger", "Opp", "Cost", f"<={self.digit(a, 1)}", "Center"]
		elif "choose  of your opponent's level  or lower character" in t:
			if "in the center stage" in t and "put it in the waiting room" in t:
				return [self.digit(a), "waitinger", "Level", f"<={self.digit(a, 1)}", "Center", "Opp"]
		elif "search your deck for up to  character with  in the name" in t:
			if "put it in your hand" in t or "put them in your hand" in t:
				if "reveal it" in t or "reveal them" in t:
					return [self.digit(a), "search", f"Name_{self.name(a,s='n')}", "upto", "show"]
		elif "search your deck for up to   character" in t:
			if "put it in your hand" in t or "put them in your hand" in t:
				if "reveal it" in t or "reveal them" in t:
					return [self.digit(a), "search", f"Trait_{self.trait(a)}", "upto", "show"]
		elif "choose   in your waiting room" in t and "\" in your" in aa:
			if " send it to memory" in t:
				return [self.digit(a), "salvage", f"Name=_{self.name(a, s='n')}", "Memory"]
			elif " return it to your hand" in t:
				return [self.digit(a), "salvage", f"Name=_{self.name(a, s='n')}"]
		elif "choose  of opponent's center stage characters" in t:
			if "choose  of opponent's center stage characters" in t:
				return [self.digit(a), self.digit(a, 1), x, "power", "Opp", "Center"]
		elif "choose  card in your clock" in t:
			if "return it to your hand" in t:
				if "choose  card in your hand" in t:
					if "put it in your clock" in t:
						return [self.digit(a), "csalvage", "", "do", ["discard", self.digit(a), "", "Clock"]]
		elif "choose   in your hand" in t and "\" in your hand" in aa:
			if "put it in the slot this was in" in t:
				return ["discard",self.digit(a),f"Name=_{self.name(a,s='n')}","Stage","Change"]
		elif "look at up to  cards from top of your deck" in t or "look at up to  cards from the top of your deck" in t:
			if "search for up to   character" in t and "reveal it" in t and "put it in your hand" in t:
				return [self.digit(a), "looktop", "top", "hand", self.digit(a, 1), f"Trait_{self.trait(a)}", "show", "upto"]
			elif "choose up to  of them and put it in your hand" in t:
				return [self.digit(a), "looktop", "top", "hand", self.digit(a, 1), "", "upto"]
		elif "look at the top  cards of your opponent's deck" in t:
			if "choose up to  of them" in t and "put them in the waiting room" in t:
				if "return the rest to the deck" in t and "shuffle that deck" in t:
					return [self.digit(a), "looktop", "top", "waiting", self.digit(a, 1), "upto", "any", "opp", "shuff"]
		elif "if there's no marker under this" in t:
			if "put the top card of your deck under this as marker" in t:
				return [1, "marker", "top","none"]
			elif "choose  in your waiting room and put it face-down under this as marker" in t:
				return [1, "marker", f"Name=_{self.name(a, -1, s='n')}", "Waiting", "none"]
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
		elif "put the top card of your clock in your waiting room" in t:
			return ["heal", 1, "top"]
		elif "put the top card of your deck in your stock" in t:
			return ["stock", 1]
		elif "deal  damage to your opponent" in t:
			return ["damage", self.digit(a), "opp"]
		elif "all your characters get" in t:
			if "get + soul" in t:
				return [-1, self.digit(a), x, "soul"]
			elif "get + level" in t:
				return [-1, self.digit(a), x, "level"]
		elif "this gets + level and + power" in t:
			return [0, self.digit(a, 1), x, "power", 0, self.digit(a), x, "level"]
		elif "this gets + power and + soul" in t:
			return [0, self.digit(a), x, "power", 0, self.digit(a, 1), x, "soul"]
		elif "this gets + power and " in t and "power and \"[" in aa:
			return [0, self.digit(a), x, "power", "do", [0, self.name(a, s='a'), x, "give"]]
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
		elif "this gets +x power" in t:
			if "x =  multiplied by the number of your  characters" in t:
				return [0, self.digit(a), x, "power", "#", "Trait", self.trait(a)]
		elif "this gets + soul" in t:
			return [0, self.digit(a), x, "soul"]
		elif "this gets the following ability" in t:
			return [0, self.name(a, s='a'), x, "give"]
		elif "this gets " in t and "this gets \"[" in aa:
			return [0, self.name(a, s='a'), x, "give"]
		elif "return this to hand" in t:
			return [0, "hander"]
		elif "send this to memory" in t:
			if "choose   character in your hand whose level = or lower than your level" in t:
				if "put it in the slot this was in" in t:
					return [0, "memorier", "do", ["discard", self.digit(a), f"TraitL_{self.trait(a)}_<=p", "Stage", "Change"]]
			else:
				return [0, "memorier"]
		elif "this's soul does not decrease by side attacking" in t:
			return [0, "[CONT] This card's soul does not decrease by side attacking.", x, "give"]

		return []

	def event(self, a=""):
		t = self.text(a)
		if "next end of your opponent's turn" in t:
			x = 2
		elif "for the turn" in t or "until end of turn" in t:
			x = 1
		else:
			x = 1

		if a.lower().startswith("[counter]"):
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
			elif "put the top card of your deck in the waiting room" in t:
				if "if it's level  or higher, choose up to  of your characters, and they get the following ability for the turn" in t:
					return ["mill", 1, "lvl", self.digit(a), "any", "do", [self.digit(a, 1), self.name(a, 1), x, "Event", "give"]]
			elif "look at up to  cards from top of your deck" in t:
				if "search for up to   character" in t and "reveal it" in t:
					return [self.digit(a), "looktop", "top", "hand", self.digit(a, 1), f"Trait_{self.trait(a)}", "upto", "show"]
			elif "choose  character in your waiting room" in t:
				if "return it to your hand" in t:
					if "choose  of your character" in t:
						if "that character gets + power" in t:
							return [self.digit(a), "salvage", "Character", "show", "do", [self.digit(a, 1), self.digit(a, 2), x, "power"]]
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
							return [self.digit(a),self.digit(a,1),x,"power","Name",self.name(a,s='n'),"do",[self.digit(a,2),self.digit(a,3),x,"power","Name",self.name(a,2,s='n')]]
			elif "choose  of your  character" in t:
				if "that character gets + power and + soul" in t:
					return [self.digit(a), self.digit(a, 1), x, "power", self.digit(a), self.digit(a, 2), x, "soul"]
				elif "that character gets + power" in t:
					return [self.digit(a), self.digit(a, 1), x, "power", "Trait", self.trait(a)]
			elif "choose  of your character" in t:
				if "that character gets + power and + soul" in t:
					return [self.digit(a), self.digit(a, 1), x, "power", self.digit(a), self.digit(a, 2), x, "soul"]
				elif "that character gets + power and the following ability" in t:
					return [self.digit(a), self.digit(a, 1), x, "power", "extra", "do", [-16, self.name(a, s='a'), x, "give"]]
				elif "that character gets + power" in t:
					if "put this in your memory" in t or "send this to memory" in t:
						return [self.digit(a), self.digit(a, 1), x, "power", "do", [0, "memorier"]]
					else:
						return [self.digit(a), self.digit(a, 1), x, "power"]
				elif "that character gets the following ability" in t:
					if "draw  card" in t:
						if "discard  card from your hand to the waiting room" in t:
							return ["draw", self.digit(a), "do", ["discard", self.digit(a), "", "do", [self.digit(a), self.name(a, s='n'), x, "Event", "give"]]]
					else:
						return [self.digit(a), self.name(a, s='a'), x, "Event", "give"]
				elif "that character gets +x power" in t:
					if "x =  times # of your  characters" in t:
						return [self.digit(a), self.digit(a, 1), x, "#", "power", "#trait", self.trait(a)]
					elif "x =  multiplied by the number of cards in your stock" in t:
						return [self.digit(a), self.digit(a, 1), x, "#", "power", "#stock"]
			elif "choose  of your level  or higher characters" in t:
				if "that character gets + level and + power" in t:
					return [self.digit(a), self.digit(a, 3), x, "Level", f">={self.digit(a, 1)}", "power", self.digit(a), self.digit(a, 2), x, "level"]
			elif "choose up to  of your character" in t:
				if "those characters get + power" in t:
					if "put this in your memory" in t:
						return [self.digit(a),self.digit(a,1),x,"upto","power","do",[0,"memorier"]]
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
		elif a.lower().startswith("brainstorm"):
			if "put the top card of your deck in your stock" in t:
				if "climax card among them" in t or " climax revealed among those cards" in t:
					if "put this in your stock" in t:
						return ["stock", 1, "do", ["brainstorm", self.digit(a), "Climax", "any", 1, "do", [0, "stocker"]]]
			elif "choose  level x or lower  character in your waiting room" in t:
				if "return it to your hand" in t:
					if "x = the number of  characters revealed among those cards" in t:
						return ["brainstorm", self.digit(a), "Trait", self.trait(a), "any", 0, "do", [self.digit(a, 1), "salvage", "CLevel_<=#", "show", "#", "#trait"]]
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
						return ["cdiscard", self.digit(a), "", "Level", "upto", "if", self.digit(a), "do", [self.digit(a, 1), "salvage", "Character", "upto", "show", "do", [self.digit(a, 2), "salvage", "Climax", "show", "upto", "do", [self.digit(a, 3), "cstock", f"Trait_{self.trait(a)}", "Waiting", "upto"]]]]
		elif "you may choose  of your characters" in t:
			if "put it in your waiting room" in t:
				if "choose  of your opponent's level  or lower characters" in t:
					if "put it in your opponent's waiting room" in t:
						return [self.digit(a), "waitinger", "upto", "if", self.digit(a), "do", [self.digit(a, 1), "waitinger", "Opp", "Level", f"<={self.digit(a, 2)}"]]
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
		elif "choose  of your stand characters with no traits" in t:
			if "rest it" in t or "rest them" in t:
				if "look at the top card of your opponent's deck" in t:
					if "put it on the top or the bottom of your opponent's deck" in t:
						if "put this in your stock" in t:
							return [self.digit(a), "rest", "Stand", "Trait", "", "if", self.digit(a), "do", [1, "looktop", "top", "bottom", "opp", "do", [0, "stocker"]]]
		elif "choose  of your stand character" in t or "choose  of your standing character" in t:
			if "rest them" in t or "rest it" in t:
				if "choose   character in your waiting room" in t and "» character" in self.a_replace(a):
					if "return it to your hand" in t:
						if "if you rest  character" in t:
							return [self.digit(a), "rest", "Stand", "if", self.digit(a, 1), "do", [self.digit(a, 2), "salvage", f"Trait_{self.trait(a)}", "show"]]
						else:
							return [self.digit(a), "rest", "Stand", "if", self.digit(a), "do", [self.digit(a, 1), "salvage", f"Trait_{self.trait(a)}", "show"]]
				elif "choose  character in your waiting room" in t:
					if "return it to your hand" in t:
						if "if you rest  character" in t:
							return [self.digit(a), "rest", "Stand", "if", self.digit(a, 1), "do", [self.digit(a, 2), "salvage", "Character", "show"]]
						else:
							return [self.digit(a), "rest", "Stand", "if", self.digit(a), "do", [self.digit(a, 1), "salvage", "Character", "show"]]
		elif "deal  damage to your opponent" in t:
			if "choose randomly  of your character" in t:
				if "that card gets + power" in t:
					return ["damage", self.digit(a), "opp", "do", [-8, self.digit(a, 2), x, "power"]]
			elif "choose  of your character" in t:
				if "that character gets + power" in t:
					return ["damage", self.digit(a), "opp","do",[self.digit(a,1),self.digit(a,2),x,"power"]]
			else:
				return ["damage", self.digit(a), "opp"]
		elif "choose  of your level  or higher characters and put it in the waiting room" in t:
			if "choose  level  or lower  character in your waiting room" in t:
				if "put it in any slot on the stage" in t:
					if "choose up to  character in your waiting room" in t:
						if "return them to your hand" in t:
							return [self.digit(a), "waitinger", "Level", f">={self.digit(a, 1)}", "if", self.digit(a), "do", [self.digit(a, 2), "salvage", f"TraitL_{self.trait(a)}_<={self.digit(a, 3)}", "Stage", "do", [self.digit(a, 4), "salvage", "Character", "upto", "show"]]]
		elif "reveal the top card of your deck" in t:
			if "if that card is a  character" in t:
				if "you may draw  card" in t:
					if "all your  characters get + soul" in t:
						return [-1, self.digit(a, 1), x, "soul", "Trait", self.trait(a), "do", [-9, "reveal", "Trait", self.trait(a), "do", ["drawupto", self.digit(a)]]]
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
		elif "search your deck for up to  character with  in the name" in t:
			if "reveal it" in t or "reveal them" in t:
				if "put it in your hand" in t:
					return [self.digit(a), "search", f"Name_{self.name(a, s='n')}", "upto", "show"]
		elif "search your deck for up to   character" in t:
			if "put them in your hand" in t or "put it in your hand" in t:
				if "reveal it" in t or "reveal them" in t:
					if "rest  of your  characters" in t:
						if "those characters do not stand during your next stand phase" in t:
							if "if you rest  characters this way" in t:
								if "choose up to   character in your waiting room and put it in your stock" in t:
									if "and put this on the bottom of the deck" in t:
										return [self.digit(a), "rest", "Trait", self.trait(a), "Stand", "extra", "do", [-16, "[CONT] This cannot [STAND] during your stand phase", 3, "give", "if", self.digit(a, 1), "do", [self.digit(a, 2), "search", f"Trait_{self.trait(a)}", "upto", "show", "do", [self.digit(a, 3), "cstock", f"Trait_{self.trait(a)}", "Waiting", "do", [0, "decker", "bottom"]]]]]
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
						else:
							return [self.digit(a), "search", f"Trait_{self.trait(a)}", "upto", "show"]
				else:
					return [self.digit(a), "search", f"Trait_{self.trait(a)}", "upto"]
		elif "choose up to  cards" in t:
			if "in your clock" in t:
				if "put them in the waiting room" in t:
					if "send this to memory" in t:
						return ["cdiscard", self.digit(a), "", "upto", "do", [0, "memorier"]]
			elif "in your opponent's waiting room" in t:
				if "return them to the deck" in t:
					return [self.digit(a), "salvage", "", "opp", "Library", "upto", "show"]
		elif "choose the top card of your deck and put it in your stock" in t:
			if "choose  of your characters, and that character gets + power for the turn" in t:
				return ["stock", 1, "do", [self.digit(a, 0), self.digit(a, 1), x, "power"]]
		elif "choose  of your opponent's level  or lower characters" in t:
			if "that character cannot stand during your opponent's next stand phase" in t or "that character doesn't stand during your opponent's next stand phase" in t:
				return [self.digit(a), "[CONT] This cannot [STAND] during your stand phase", 2, "give", "Opp", "Level", f"<={self.digit(a, 1)}"]
			elif "return it to hand" in t:
				return [self.digit(a), "hander", "Opp", "Level", f"<={self.digit(a, 1)}"]
			elif "put it into his or her stock" in t:
				return [self.digit(a), "stocker", "Opp", "Level", f"<={self.digit(a, 1)}"]
		elif "choose  character in your waiting room" in t:
			if "return it to your hand" in t:
				if "choose  of your characters" in t:
					if "that character gets + power" in t:
						return [self.digit(a), "salvage", "Character", "show", "do", [self.digit(a, 1), self.digit(a, 2), x, "power"]]
		elif "choose  character in your clock whose level = or lower than your level" in t:
			if "put it in any slot on the stage" in t:
				if "you cannot play this from your hand" in t:
					return ["cdiscard", self.digit(a, 1), "CLevel_<=p", "Stage"]
		elif "choose  character in your clock" in t:
			if "return it to your hand" in t:
				if "choose  of your opponent's characters" in t:
					if "that character gets - power" in t:
						if "put this in your clock" in t:
							return [self.digit(a), "csalvage", "Character", "do", [self.digit(a, 1), self.digit(a, 2), x, "power", "Opp", "do", [0, "clocker"]]]
		elif "choose up to   characters in your clock" in t:
			if "return it to your hand" in t:
				if "put  cards from top of your deck in your clock" in t:
					return [self.digit(a), "csalvage", f"Trait_{self.trait(a)}", "upto", "do", ["damageref", self.digit(a)]]
		elif "choose up to  characters in your waiting room with  in the name" in t:
			if "return them to your hand" in t or "return it to your hand" in t:
				if "discard  card from your hand to the waiting room" in t or "discard  cards from your hand to the waiting room" in t:
					return [self.digit(a), "salvage", f"Name_{self.name(a,s='n')}", "upto", "show", "do", ["discard", self.digit(a, 1), ""]]
				else:
					return [self.digit(a), "salvage", f"Name_{self.name(a,s='n')}", "show", "upto"]
		elif "choose up to  characters in your waiting room" in t or "choose up to  character in your waiting room" in t:
			if "return them to your hand" in t or "return it to your hand" in t:
				if "discard  card from your hand to the waiting room" in t or "discard  cards from your hand to the waiting room" in t:
					return [self.digit(a), "salvage", "Character", "upto", "show", "do", ["discard", self.digit(a, 1), ""]]
				else:
					return [self.digit(a), "salvage", "Character", "show", "upto"]
		elif "choose up to  level  or lower character in your hand" in t:
			if "put it in any slot on the stage" in t:
				return ["discard", self.digit(a), f"CLevel_<={self.digit(a, 1)}", "upto", "Stage"]
		elif "choose up to  character in your hand" in t:
			if "with  in name whose level is less than or equal to your level plus  " in t:
				if "put it in any slot on the stage" in t:
					return ["discard", self.digit(a), f"CLevelN_standby_{self.name(a, s='n')}", "Stage", "upto"]
		elif "choose up to  of your character" in t:
			if "those characters get + power" in t:
				return [self.digit(a), self.digit(a, 1), x, "upto", "power"]
		elif "choose  of your character" in t:
			if "put it in your waiting room" in t:
				if "choose  level  or lower character in your opponent's center stage and put it in the waiting room" in t:
					return [self.digit(a), "waitinger", "if", self.digit(a), "do", [self.digit(a, 1), "waitinger", "Level", f"<={self.digit(a, 2)}", "Opp", "Center"]]
			elif "put it on top of the deck" in t:
				if "choose  level  or lower character in your opponent's center stage and return it to the hand" in t:
					return [self.digit(a), "decker", "top", "if", "do", [self.digit(a, 1), "hander", "Level", f"<={self.digit(a, 2)}", "Opp", "Center"]]
			elif "return it to your hand. if so, choose  opponent's level  or lower character and put it in stock" in t:
				return [self.digit(a), "hander", "Character", "do", [self.digit(a, 1), "stocker", "Level", f"<={self.digit(a, 2)}", "Opp"]]
			elif "that character gets + power" in t:
				if "at the end of the turn, put that card in your stock" in t:
					return [self.digit(a), self.digit(a, 1), x, "power", "extra", "do", [-16, "[AUTO] At the end of the turn, put this card into your stock.", -3, "give"]]
				else:
					return [self.digit(a, 0), self.digit(a, 1), x, "power"]
			elif "that character gets " in t and "that character gets \"[" in self.a_replace(a):
				if "all players return cards in their waiting rooms to their respective decks, and shuffle them" in t:
					return [-1, "shuffle", "both", "do", [self.digit(a), self.name(a, s='a'), x, "give"]]
		elif "choose  of your opponent's character" in t:
			if "whose level is  or lower" in t:
				return [self.digit(a), "waiting", "Opp", "Level", "<=%s" % self.digit(a, 1)]
		elif "choose  of your opponent's cost  or lower character" in t:
			if "put it on the bottom of the deck" in t:
				if "send this to memory" in t:
					if "if you have  or fewer  characters, you cannot play this from hand" in t:
						return [self.digit(a, 1), "decker", "bottom", "Opp", "Cost", f"<={self.digit(a, 2)}", "do", [0, "memorier"]]
			elif "put it on top of the deck" in t:
				if "put this in your memory" in t:
					return [self.digit(a), "decker", "top", "Opp", "Cost", f"<={self.digit(a,1)}", "do", [0, "memorier"]]
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
					return [self.digit(a), self.digit(a, 1), x, "power", "Opp","do",[0, "memorier"]]
				else:
					return [self.digit(a), self.digit(a, 1), x, "power", "Opp"]
		elif "choose   character in your hand" in t:
			if "put them in your waiting room" in t or "from your hand to the waiting room" in t or "put it in the waiting room" in t:
				if "draw up to  cards" in t:
					if "send this to memory" in t:
						return ["discard", self.digit(a), f"Trait_{self.trait(a)}", "if", self.digit(a), "do", ["drawupto", self.digit(a, 1), "do", [0, "memorier"]]]
		elif "choose   character in your clock" in t:
			if "return it to your hand" in t:
				if "put this in your clock" in t:
					if "» character in your clock" in self.a_replace(a):
						return [self.digit(a), "csalvage", f"Trait_{self.trait(a)}", "show", "do", [0, "clocker"]]
		elif "choose   character in your waiting room" in t:
			if "return it to your hand" in t:
				if "» character in your waiting" in self.a_replace(a):
					if "send this to memory" in t:
						return [self.digit(a), "salvage", f"Trait_{self.trait(a)}", "show", "do", [0, "memorier"]]
		elif "choose   in your waiting room and put it in any slot on the stage" in t:
			if "discard  card from your hand to the waiting room" in t:
				return [self.digit(a), "salvage", f"Name=_{self.name(a, s='n')}", "Stage", "do", ["discard", self.digit(a, 1), ""]]
		elif "choose  level  or lower character in your clock" in t:
			if "put it in any slot on stage" in t:
				if "at the next end of your opponent's turn" in t:
					if " put that character in clock" in t:
						return ["cdiscard", self.digit(a), f"CLevel_<={self.digit(a, 1)}", "Stage", "extra", "do", [-16, "[AUTO] At the end of the turn, put this card into your clock.", -30, "Event", "give"]]
		elif "choose  level  or lower  character in your clock" in t:
			if "put it on any position of your stage" in t:
				if "put this in your clock" in t:
					return [self.digit(a), "csalvage", f"TraitL_{self.trait(a)}_<={self.digit(a, 1)}", "Stage", "do", [0, "clocker"]]
		elif "choose  of your  character" in t:
			if "that character gets + power and + soul" in t:
				if t.count("choose  of your  character") == 2:
					if t.count("that character gets + power and + soul") == 2:
						if t.count("for the turn") == 2:
							return [self.digit(a), self.digit(a, 1), x, "power", "Trait", self.trait(a), "extra", "do", [-16, self.digit(a, 2), x, "soul", "do", [self.digit(a, 3), self.digit(a, 4), x, "power", "Trait", self.trait(a, 1), "extra", "do", [-16, self.digit(a, 5), x, "soul"]]]]
		elif "look at the top  cards of your opponent's deck" in t:
			if "choose up to  of them and put it on the bottom of the deck" in t:
				if "put the rest on top of the deck in any order" in t:
					return [self.digit(a), "looktop", "bdeck", self.digit(a, 1), "upto", "opp", "fix", "reorder"]
			elif "choose up to  of them and put them in the waiting room" in t:
				if "return the rest to the deck" in t and "your opponent shuffles that deck" in t:
					return [self.digit(a), "looktop", "top", "waiting", self.digit(a, 1), "upto", "any", "opp", "shuff"]
		elif "look at the top card of your opponent's deck" in t:
			if "put it on the top or the bottom of your opponent's deck" in t:
				if "put this in your stock" in t:
					return [1, "looktop", "top", "bottom", "opp", "do", [0, "stocker"]]
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
		elif "send this to memory" in t or "put this in your memory" in t:
			if "reveal the top card of your deck" in t:
				if "if it's either a  character or an event" in t:
					if "put it in your hand" in t:
						return [0, "memorier", "do", [-9, "reveal", "TraitEv", self.trait(a), "do", ["draw", 1]]]
			else:
				return [0, "memorier"]
		elif "draw up to  cards" in t:
			if "choose  cards in your hand" in t or "discard  cards from your hand" in t:
				if "put them in your waiting room" in t or "from your hand to the waiting room" in t:
					return ["drawupto", self.digit(a), "do", ["discard", self.digit(a, 1), ""]]
		elif "return all your opponent's level  or lower characters to the deck, and your opponent shuffles that deck" in t:
			if "put this in your clock" in t:
				return [-1, "decker", "Level", f"<={self.digit(a)}", "Opp", "do", [0, "clocker"]]
		elif "all your characters get " in t:
			if "get + soul" in t:
				return [-1, self.digit(a), x, "soul"]
			elif "get " in t and "characters get \"[" in self.a_replace(a):
				return [-1, self.name(a, s='a'), x, "give"]

		return []

	def auto(self, a="", p="", r=("0", "0", ""), v=("", ""), lvop=(0, 0), cx=("", "0", ""), pos=("", "", "", ""), n="", sx=[], tr=([], []), z=(0, 0), act="", cnc=("0", False), pp=0, dis=("", ""), nr=("", ""), atk="", dmg=0, nmop=("", ""), rst="", lvc=("", ""), batt=False, refr="", sav=("", ""), brt=("", 0), lr=(0, 0), lvup="", inds=[], baind=("0", "0"), csop=(0, 0), suop=("", ""), ty=("", [], ""), ch=False):
		""":param a: ability (string)
		:param p: phase (string)
		:param r: active card  _ triggering effect card _ riggering effect card type(list)
		:param v: status of both cards (list)
		:param ty: triggering effect card type,trigger (list)
		:param lvop: level of both cards (list)
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
		:param cnc: Damage delt by attacking character is cancelled (boolean)
		:param pp: Beginning, Actual, End of the phase (-1,0,1) (int)
		:param dis:
		:param baind: attacking_batteling opp (list)
		:param lvop: card and batteling opp level(list)
		:param csop: card and batteling opp cost(list)
		:param suop: card and batteling opp status(list)
		:param nmop: card and batteling opp name(list)
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
		self.cx = False
		self.center = False

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
				# if "you may pay the cost" in t:
				# 	if "choose  character in your waiting room" in t:
				# 		if "return it to your hand" in t:
				# 			return ["pay", "may", "played", "do", [self.digit(a), "salvage", "Character", "show"]]
				# elif "this gets the following ability" in t:
				# 	return [0, self.name(a, s='a'), x, "give", "played"]
				# elif "this gets + power" in t:
				# 	return [0, self.digit(a), x, "power", "played"]
				# elif "this gets + soul" in t:
				# 	return [0, self.digit(a), x, "soul", "played"]
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
					if "this ability activates up to  time per turn" in t:
						if "this gets + power" in t:
							return [0, self.digit(a, 2), x, "power", f"a{self.digit(a)}"]
		elif lvup:
			if "when your opponent levels up" in t or "when your opponent levels-up" in t:
				if lvup not in r[0][-1]:
					if "put this in your waiting room" in t:
						return [0, "waitinger"]
					elif "you may choose   in your climax area" in t:
						if "return it to your hand" in t:
							return ["pay", "may", "do", [1, "hander", "Climax"]]
			elif "when you level up" in t or "when you level-up" in t:
				if lvup in r[0][-1]:
					if "you may pay the cost" in t:
						if "search your deck for up to   character" in t:
							if "reveal it" in t and "put it in your hand" in t:
								return ["pay", "may", "do", [self.digit(a), "search", f"Trait_{self.trait(a)}", "upto", "show"]]
						elif "choose   character in your waiting room" in t:
							if "return it to your hand" in t:
								return ["pay", "may", "do", [self.digit(a), "salvage", f"Trait_{self.trait(a)}", "show"]]
						elif "draw  card" in t:
							return ["pay", "may", "do", ["draw", self.digit(a)]]
					elif "you may draw  card" in t:
						if " discard  card from your hand to the waiting room" in t:
							return ["pay", "may", "do", ["draw", self.digit(a), "do", ["discard", self.digit(a, 1), ""]]]
					elif "choose  of your characters" in t:
						if "that character gets + power" in t:
							return [self.digit(a), self.digit(a, 1), x, "power"]
					elif "put this in the waiting room" in t or "put this in your waiting room" in t:
						return [0, "waitinger"]
					elif "all your characters get + level" in t:
						return [-1, self.digit(a), x, "level"]
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
							if "you may draw  card" in t:
								if "discard  card from your hand to the waiting room" in t:
									return ["pay", "may", "do", ["draw", self.digit(a, 1), "do", ["discard", self.digit(a, 2), ""]]]
							elif "you may pay the cost" in t:
								if "choose  of your opponent's character" in t:
									if "that character gets - power" in t:
										return ["pay", "may", "do", [self.digit(a, 1), self.digit(a, 2), x, "power", "Opp"]]
								elif "deal  damage to your opponent" in t:
									return ["pay", "may", "do", ["damage", self.digit(a, 1), "opp"]]
							elif "choose  of your character" in t:
								if "that character gets + power" in t:
									return [self.digit(a, 1), self.digit(a, 2), x, "power"]
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
				if "this ability activates up to once per turn" in t and "battle" not in t:
					if "choose  of your characters" in t:
						if "that character gets + power" in t:
							return [self.digit(a), self.digit(a, 1), x, "power", "a1"]
					elif "choose  of your  characters" in t:
						if "that character gets + power" in t:
							return [self.digit(a), self.digit(a, 1), x, "power", "Trait", self.trait(a), "a1"]
					elif "you may put the top card of your opponent's stock in the waiting room" in t:
						if "choose  card in your opponent's waiting room" in t:
							if "put it in stock" in t:
								return ["pay", "may", "a1", "do", ["distock", 1, "top", "opp", "if", 1, "do", [self.digit(a), "salvage", "", "Stock", "opp", "show"]]]
					elif "this gets + power" in t:
						return [0, self.digit(a), x, "power", "a1"]
				elif "this ability activates up to  time per turn" in t and "battle" not in t:
					if "choose  of your character" in t:
						if "that character gets + power" in t:
							return [self.digit(a, 1), self.digit(a, 2), x, "power", f"a{self.digit(a)}"]
					elif "this gets + power" in t:
						return [0, self.digit(a, 1), x, "power", f"a{self.digit(a)}"]
		elif "when your other  character is played and placed to the stage" in t or "when another of your  characters is placed on the stage from your hand" in t or "when another of your  characters is placed from hand to the stage" in t or "when another  character of yours is placed from hand to the stage" in t or "when another  character is placed on the stage from your hand" in t:
			if n in r[0][-1] and r[0] != r[1] and r[0][-1] == r[1][-1] and self.trait(a) in tr[1] and ("Hand" in pos[2] or ("on the stage from your hand or memory" in t and "Memory" in pos[2])) and any(field in pos[3] for field in self.stage) and "Stand" in v[1]:
				if "if this is stand" in t:
					if v[0] == "Stand":
						if "you may pay the cost" in t:
							if "put the top card of your deck in your stock" in t:
								return ["pay", "may", "do", ["stock", 1]]
				elif "look at the top card of your deck" in t:
					if "put it on top or bottom of your deck" in t or "put it either on top or bottom of your deck" in t:
						return [1, "looktop", "top", "bottom"]
				elif "that character gets + power and " in t:
					if "power and «" in aa:
						return [-3, self.digit(a), x, "power", "target", r[1], "extra", "do", [-16, self.trait(a, -1), x, "trait"]]
				elif "this gets + power" in t:
					if "this ability activates up to  time per turn" in t:
						return [0, self.digit(a, 1), x, f"a{self.digit(a)}", "power"]
					else:
						return [0, self.digit(a), x, "power"]
		elif "when your other  character is placed from the stage to the waiting room" in t:
			if r[0] != r[1] and r[0][-1] == r[1][-1] and any(field in pos[2] for field in ("Center", "Back")) and "Waiting" in pos[3] and self.trait(a) in tr[1]:
				if "you may draw  card" in t:
					if "discard  card from your hand to the waiting room" in t:
						return ["pay", "may", "do", ["draw", self.digit(a), "do", ["discard", self.digit(a), ""]]]
		elif "when your other character is put in the waiting room" in t or "when another character of yours is placed from the stage to the waiting room" in t:
			if r[0] != r[1] and r[0][-1] == r[1][-1] and any(field in pos[2] for field in ("Center", "Back")) and "Waiting" in pos[3]:
				if "if this is in the back stage" in t:
					if "Back" in pos[1]:
						if "you may pay the cost" in t:
							if "put that character rest in the slot it was in" in t or "put that character rested in the slot it was in" in t:
								return ["pay", "may", "do", [-7, "revive", [r[1], "Stage"], "extra", "do", [-16, "rested"]]]
				elif "you may pay the cost" in t:
					if "return that character to your hand" in t:
						return ["pay", "may", "do", [-7, "rescue", [r[1], "Hand"]]]
		elif "when this is placed from hand or waiting room to the stage" in t:
			if r[0] == r[1] and ((any(field in pos[1] for field in self.stage) and "Waiting" in pos[0]) or ("Hand" in pos[0] and v[0] == "Stand" and any(field in pos[1] for field in self.stage))):
				if "this gets the following ability" in t:
					return [0, self.name(a, s='a'), x, "give", "played"]
				else:
					return ["played"]
		elif "when this is put in your waiting room from the stage" in t or "when this is placed from the stage to the waiting room" in t:
			if r[0] == r[1] and any(field in pos[0] for field in ("Center", "Back")) and "Waiting" in pos[1]:
				self.ablt = 1
				if "you may pay the cost" in t:
					if "search your deck for up to  character with  in name" in t or "search your deck for up to  character with  in the name" in t:
						if "reveal it" in t and "put it in your hand" in t:
							return ["pay", "may", "played", "do", [self.digit(a), "search", f"Name_{self.name(a, s='n')}", "show", "upto"]]
					elif "search your deck for up to   character" in t:
						if "reveal it" in t and "put it in your hand" in t:
							return ["pay", "may", "played", "do", [self.digit(a), "search", f"Trait_{self.trait(a)}", "show", "upto"]]
					elif "choose  level  or lower character in your waiting room" in t:
						if "put it in any slot in the back stage" in t:
							return ["pay", "may", "played", "do", [self.digit(a), "salvage", f"CLevel_<={self.digit(a, 1)}", "Stage", "Back"]]
					elif ("choose   in your waiting room" in t and "\" in your waiting room" in aa) or "choose  card named  in your waiting room" in t:
						if "put it on the stage position this was on as rest" in t:
							return ["pay", "may", "played", "do", ["changew", self.digit(a), f"Name=_{self.name(a, s='n')}", "extra", "do", [-16, "rest"]]]
						elif "return it to your hand" in t:
							return ["pay", "may", "played", "do", [self.digit(a), "salvage", f"Name=_{self.name(a, s='n')}"]]
					elif "choose   character in your waiting room" in t:
						if "return it to your hand" in t:
							return ["pay", "may", "played", "do", [self.digit(a), "salvage", f"Trait_{self.trait(a)}", "show"]]
					elif "choose  card in your level and  card in your waiting room" in t:
						if "exchange them" in t:
							return ["pay", "may", "played", "do", ["ldiscard", self.digit(a), "", "levswap", "if", "do", [self.digit(a), "salvage", "", "levswap"]]]
					elif "search your deck for up to  level  or lower character, reveal it, put it in your hand" in t:
						return ["pay", "may", "played", "do", [self.digit(a), "search", f"CLevel_<={self.digit(a, 1)}", "show", "upto"]]
					elif "send this to memory" in t:
						return ["pay", "may", "played", "do", [0, "memorier"]]
				elif "you may put this rested in the slot this was in" in t or "you may return this to its previous stage position as rest" in t:
					return ["pay", "may", "played", "do", [0, "revive", "Stage", "do", [0, "rested"]]]
				elif "you may choose   in your waiting room" in t:
					if "and send it to memory" in t:
						return ["pay", "may", "played", "do", [self.digit(a), "salvage", f"Name=_{self.name(a, s='n')}", "Memory"]]
				elif "you may draw  cards" in t:
					return ["pay", "may", "played", "do", ["draw", self.digit(a)]]
		elif "when another of your character whose level is  or lower is placed from the stage to the waiting room" in t:
			if r[0][-1] == r[1][-1] and r[0] != r[1] and any(field in pos[2] for field in ("Center", "Back")) and "Waiting" in pos[3] and lr[1] <= self.digit(a):
				if "if this is in the back stage" in t:
					if "Back" in pos[1]:
						if "you may pay the cost" in t:
							if "put that character rest in the slot it was in" in t or "put that character rested in the slot it was in" in t:
								return ["pay", "may", "do", [-7, "revive", [r[1], "Stage"], "extra", "do", [-16, "rested"]]]
		elif "when an opponent's character is placed from hand to the stage" in t:
			if "Hand" in pos[2] and r[0] != r[1] and r[0][-1] != r[1][-1] and v[1] == "Stand" and any(field in pos[3] for field in self.stage):
				if "this gets + power" in t:
					return [0, self.digit(a), x, "power"]
		elif "when this is placed from your hand to the stage" in t or "when this is placed on stage from your hand" in t or "when this is placed from hand to the stage" in t or "when this is played and placed to the stage" in t or "when this is placed on the stage from your hand" in t:
			if "Hand" in pos[0] and r[0] == r[1] and v[0] == "Stand" and any(field in pos[1] for field in self.stage):
				self.ablt = 1
				if "you may pay the cost" in t:
					if "if your opponent has a" in t or "if your opponent has a character named " in t:
						if "play  with your opponent until someone wins" in t and "play \"rock-paper-scissors\" with your opponent until someone wins" in aa:
							if "winner draws  card" in t:
								return ["name", self.name(a, 1), "opp", "played", "do", ["pay", "may", "do", ["janken", "winner", "do", ["draw", self.digit(a)]]]]
					elif "reveal the top card of your deck" in t:
						if "if that card is a  character whose level is lower than or equal to your level" in t:
							if "put that character in any slot on your stage" in t:
								return [-9, "reveal", "TraitL", f"{self.trait(a)}_<=p", "played", "do", ["pay", "may", "do", [-9, "search", "", "Stage", "topdeck"]]]
					elif "search your deck for up to  level  or lower  character" in t:
						if "put it on any position of your back stage" in t:
							return ["pay", "may", "do", [self.digit(a), "search", f"TraitL_{self.trait(a)}_<={self.digit(a, 1)}", "Stage", "Back", "upto"]]
					elif "search your deck for up to   character" in t:
						if "put it in your hand" in t and "reveal it" in t:
							return ["pay", "may", "played", "do", [self.digit(a), "search", f"Trait_{self.trait(a, 1)}", "upto", "show"]]
						elif "put it in the waiting room" in t:
							return ["pay", "may", "played", "do", [self.digit(a), "search", f"Trait_{self.trait(a, 1)}", "Waiting", "upto", "show"]]
						elif "put it in any slot on the stage" in t:
							if "whose level = or lower than your level and whose cost is  or lower" in t:
								return ["pay", "may", "played", "do", [self.digit(a), "search", f"LevCost_<=p_<={self.digit(a, 1)}", "upto", "Stage"]]
					elif "search your deck for up to  character with  in its card name" in t or "search your deck for up to  character with  in name" in t:
						if "reveal it" in t and "put it in your hand" in t:
							if any(setonly in a for setonly in self.set_only):
								for sto in self.set_only:
									if sto in a:
										return ["pay", "may", "played", "do", [self.digit(a), "search", f"NameSet_{self.name(a, s='n')}_{self.set_only[set]}", "show", "upto"]]
							else:
								return ["pay", "may", "played", "do", [self.digit(a), "search", f"Name_{self.name(a, -1, s='n')}", "show", "upto"]]
					elif "search your deck for up to  character with " in t:
						if "reveal it" in t and "put it in your hand" in t:
							if self.name(a, -1, s='n') in self.text_name:
								return ["pay", "may", "played", "do", [self.digit(a), "search", f"Text_ {self.text_name[self.name(a, -1, s='n')]} ", "show", "upto"]]
					elif "search your deck for  character with " in t:
						if "reveal it" in t and "put it in your hand" in t:
							if self.name(a, s='n') in self.text_name:
								return ["pay", "may", "played", "do", [self.digit(a), "search", f"Text_{self.text_name[self.name(a, s='n')]}", "show"]]
					elif ("search your deck for up to  " in t or "search your deck for up to  card named " in t) and "for up to \"" in aa:
						if "reveal it" in t and "put it in your hand" in t:
							return ["pay", "may", "played", "do", [self.digit(a), "search", f"Name=_{self.name(a, -1, s='n')}", "show", "upto"]]
						elif "put it on any position of your stage" in t:
							return ["pay", "may", "played", "do", [self.digit(a), "search", f"Name=_{self.name(a, -1, s='n')}", "upto", "Stage"]]
						elif "put it in any slot in the back stage" in t:
							return ["pay", "may", "played", "do", [self.digit(a), "search", f"Name=_{self.name(a, -1, s='n')}", "upto", "Stage", "Back"]]
					elif "choose  cost  or lower character in your opponent's center stage" in t:
						if "put it on the top of his or her deck" in t:
							return ["pay", "may", "played", "do", [self.digit(a), "decker", "top", "Cost", f"<={self.digit(a, 1)}", "Opp", "Center"]]
					elif "choose  of your opponent's level  or lower characters" in t:
						if "put it on the bottom of his or her deck" in t:
							if "characters in the back stage" in t:
								return ["pay", "may", "played", "do", [self.digit(a), "decker", "Level", f"<={self.digit(a, 1)}", "Back", "Opp", "bottom"]]
						elif "that character doesn't stand" in t:
							return ["pay", "may", "played", "do", [self.digit(a), "[CONT] This cannot [STAND] during your stand phase", 2, "give", "Level", f"<={self.digit(a, 1)}", "Opp"]]
						elif "put it in your opponent's stock" in t:
							if "if you have another  character" in t:
								return [1, "more", "Trait", self.trait(a), "other", "played", "do", ["pay", "may", "do", [self.digit(a), "stocker", "Opp", "Level", f"<={self.digit(a, 1)}"]]]
						elif "return it to your opponent's hand" in t:
							if "at the end of turn" in t and "put this in your memory" in t:
								return ["pay", "may", "played", "do", [self.digit(a), "hander", "Level", f"<={self.digit(a, 1)}", "Opp", "do", [0, "[AUTO] At the end of the turn, put this card into your memory.", -3, "AUTO", "give"]]]

					elif "choose   character, a  character, and a  character in your waiting room" in t:
						if "return them to your hand" in t:
							return ["pay", "may", "played", "do", [self.digit(a) + 2, "salvage", f"BTrait_{self.trait(a)}_{self.trait(a, 1)}_{self.trait(a, 2)}", "show"]]
					elif "choose  card in your opponent's waiting room" in t:
						if "return it to your opponent's deck" in t:
							return ["pay", "may", "played", "do", [self.digit(a), "shuffle", "opp"]]
					elif "choose  card in your level and  card in your waiting room" in t or "choose  card on your level area and  card in your waiting room" in t:
						if "exchange them" in t:
							return ["pay", "may", "played", "do", ["ldiscard", self.digit(a), "", "levswap", "if", "do", [self.digit(a), "salvage", "", "levswap"]]]
					elif "choose   character in your clock" in t:
						if "return it to your hand" in t:
							if "put the top card of your deck in your clock" in t:
								return ["pay", "may", "played", "do", [self.digit(a), "csalvage", "", "show","do", ["damageref", 1]]]
					elif "choose  character in your clock" in t:
						if "return it to your hand" in t:
							if "put the top card of your deck in your clock" in t:
								return ["pay", "may", "played", "do", [self.digit(a), "csalvage", "Character", "do", ["damageref", 1]]]
					elif "choose   character in your waiting room" in t or "choose   character from your waiting room" in t:
						if "return it to your hand" in t and "this gets + power" in t:
							return ["pay", "may", "played", "do", [self.digit(a), "salvage", f"Trait_{self.trait(a)}", "show", "do", [0, self.digit(a, 1), x, "power"]]]
						elif "return it to your hand" in t or "return it to hand" in t:
							return ["pay", "may", "played", "do", [self.digit(a), "salvage", f"Trait_{self.trait(a)}", "show"]]
					elif "choose up to  characters with  in name in your waiting room" in t:
						if "return them to your hand" in t:
							return ["pay", "may", "played", "do", [self.digit(a), "salvage", f"Name_{self.name(a, s='n')}", "show", "upto"]]
					elif "choose  character with  in name" in t:
						if "in your waiting room" in t:
							if "return it to your hand" in t:
								return ["pay", "may", "played", "do", [self.digit(a), "salvage", f"Name_{self.name(a, s='n')}", "show"]]
					elif "choose   in your waiting room" in t:
						if "return it to your hand" in t:
							return ["pay", "may", "played", "do", [self.digit(a), "salvage", f"Name=_{self.name(a, s='n')}", "show"]]
					elif "choose  character in your waiting room" in t:
						if "return it to your hand" in t:
							if "with  or  " in t:
								return ["pay", "may", "do", [self.digit(a), "salvage", f"Trait_{self.trait(a)}_{self.trait(a, 1)}"]]
							else:
								return ["pay", "may", "played", "do", [self.digit(a), "salvage", "Character", "show"]]
					elif "choose  card named  in your waiting room" in t:
						if "return it to your hand" in t:
							return ["pay", "may", "played", "do", [self.digit(a), "salvage", f"Name=_{self.name(a, s='n')}", "show"]]
					elif "choose  of your characters" in t:
						if "that character gets the following ability" in t:
							return ["pay", "may", "played", "do", [self.digit(a), self.name(a, s='a'), x, "give"]]
						elif "that character gets + soul" in t:
							return ["pay", "may", "played", "do", [self.digit(a), self.digit(a, 1), x, "soul"]]
					elif "choose  of your other  characters" in t:
						if "that character gets + power" in t:
							return ["pay", "may", "played", "do", [self.digit(a), self.digit(a, 1), x, "power", "Other", "Trait", self.trait(a)]]
					elif "look at up to  cards from top of your deck" in t:
						if "search for up to  characters with  or " in t and "reveal them" in t:
							return ["pay", "may", "played", "do", [self.digit(a), "looktop", "top", "hand", self.digit(a, 1), f"Trait_{self.trait(a)}_{self.trait(a, 1)}", "upto", "show"]]
						elif "choose up to  of them and put it in your hand" in t:
							return ["pay", "may", "played", "do", [self.digit(a), "looktop", "top", "hand", self.digit(a, 1), "", "upto"]]
					elif "look at the top card of your opponent's deck" in t:
						if "put it on the top or the bottom of your opponent's deck" in t:
							return ["pay", "may", "played", "do", [1, "looktop", "top", "bottom", "opp"]]
					elif "put up to  card from the top of your clock in your waiting room" in t:
						if "this gets + power" in t:
							return ["pay", "may", "played", "do", ["heal", self.digit(a), "top", "may", "do", [0, self.digit(a, 1), x, "power"]]]
					elif "put the top card in your clock in your waiting room" in t or "put the top card of your clock in your waiting room" in t:
						return ["pay", "may", "played", "do", ["heal", 1, "top"]]
					elif "put the top card of your deck underneath this as a marker" in t:
						return ["pay", "may", "played", "do", [1, "marker", "top"]]
					elif "deal  damage to your opponent" in t:
						return ["pay", "may", "played", "do", ["damage", self.digit(a), "opp"]]
					elif "draw  card" in t:
						return ["pay", "may", "played", "do", ["draw", self.digit(a)]]
					elif "all your characters get + power" in t:
						return ["pay", "may", "played", "do", [-1, self.digit(a), x, "power"]]
					elif "this gets the following ability" in t:
						return ["pay", "may", "played", "do", [0, self.name(a, s='a'), x, "give"]]
					elif "this gets + power" in t:
						return ["pay", "may", "played", "do", [0, self.digit(a), x, "power"]]
					elif "your opponent cannot play climax cards from hand" in t:
						return ["pay", "may", "played", "do", [-21, "[CONT] Your opponent cannot play climax cards from hand", x, "give"]]
				elif "you may draw  card" in t:
					if "if there are  or more  characters in your memory" in t:
						return [self.digit(a), "more", "Trait", self.trait(a), "Memory", "played", "do", ["pay", "may", "do", ["draw", self.digit(a, 1)]]]
					else:
						return ["pay", "may", "played", "do", ["draw", self.digit(a)]]
				elif "you may choose  card in your hand" in t:
					if "put it in your stock" in t:
						return ["pay", "may", "played", "do", [self.digit(a), "cstock", "", "Hand", "upto"]]
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
						return ["pay", "may", "played", "do", [-1, "memorier", "opp", "extra", "if", 1, "do", [-16, "msalvage", "ID_x", "Stage", "Opp", "plchoose", "seperate", "opp"]]]
				elif "you may put the top card of your opponent's stock in the waiting room" in t:
					if "choose  card in your opponent's waiting room and put it in stock" in t:
						return ["pay", "may", "played", "do", ["distock", 1, "top", "opp", "if", 1, "do", [self.digit(a), "salvage", "", "Stock", "opp", "show"]]]
				elif "you may put the top  cards of your deck in the waiting room" in t:
					return ["pay", "may", "played", "do", ["mill", self.digit(a), "top", "any"]]
				elif "you may choose   character in your waiting room" in t:
					if "return it to your hand" in t:
						return ["pay", "may", "played", "do", [self.digit(a), "salvage", f"Trait_{self.trait(a)}", "show"]]
				elif "you may choose   in your waiting room" in t:
					if "put it face-up under this as marker" in t:
						return ["pay", "may", "played", "do", [1, "marker", f"Name=_{self.name(a, s='n')}", "Waiting", "show", "face-up"]]
				elif "you may put the top card of your clock in the waiting room" in t or "you may put the top card of your clock in your waiting room" in t:
					return ["pay", "may", "played", "do", ["heal", 1, "top"]]
				elif "you may put the top card of your deck in your clock" in t:
					return ["pay", "may", "played", "do", ["damageref", 1]]
				elif "if there are  or more climax cards in your opponent's waiting room" in t:
					if "rest this" in t:
						return [self.digit(a), "cards", "Waiting", "Climax", "opp", "played", "do", [0, "rest"]]
				elif "if there are fewer cards in your hand than your opponent's hand" in t:
					if "you may put the top card of your deck in your stock" in t:
						return [0, "cards", "HandvsOpp", "lower", "played", "do", ["pay", "may", "do", ["stock", 1]]]
				elif "if the number of cards in your deck is  or less" in t:
					if "return all cards in your waiting room to your deck" in t:
						if "choose  of your characters" in t:
							if "that character gets + power" in t:
								return [self.digit(a), "cards", "Library", "lower", "played", "do", [-1, "shuffle", "do", [self.digit(a, 1), self.digit(a, 2), x, "power"]]]
				elif "if you have  or more other characters with  or " in t:
					if "this gets + soul" in t:
						if "» or «" in aa:
							return [self.digit(a), "more", "Trait", f"{self.trait(a)}_{self.trait(a, 1)}", "other", "played", "do", [0, self.digit(a, 1), x, "soul"]]
				elif "if you have  or more other  characters" in t or "if the number of your other  characters is  or more" in t:
					if "you may put the top card of your deck in your stock" in t:
						return [self.digit(a), "more", "Trait", self.trait(a), "other", "played", "do", ["pay", "may", "do", ["stock", 1]]]
					elif "all your characters get + power" in t:
						return [self.digit(a), "more", "Trait", self.trait(a), "other", "played", "do", [-1, self.digit(a, 1), x, "power"]]
				elif "look at the top card of your deck" in t:
					if "put it on top or bottom of your deck" in t or "put it either on top or bottom of your deck" in t or "put it on the top or the bottom of your deck" in t or "put it back either on top or bottom of the deck" in t:
						return [1, "looktop", "top", "bottom", "played"]
					elif "put it either on top of the deck or in the waiting room" in t or "put it on top of your deck or in your waiting room" in t:
						return [1, "looktop", "top", "Waiting", "played"]
				elif "look at up to  cards from top of your deck" in t or "look at up to  cards from the top of your deck" in t:
					if "choose up to  of them" in t:
						if "put it in your hand" in t:
							return [self.digit(a), "looktop", "top", "hand", self.digit(a, 1), "", "upto", "played"]
					elif "choose  cards from among them" in t:
						if "put them in your waiting room" in t:
							if "put the rest on the top of your deck in any order" in t:
								return [self.digit(a), "looktop", "top", "waiting", self.digit(a, 1), "upto", "all", "played", "reorder"]
					elif "put them on the top of your deck in any order" in t:
						return [self.digit(a), "looktop", "top", "reorder", "upto", "played"]
					elif "put them back in the same order" in t:
						return [self.digit(a), "looktop", "top", "look", "upto", "played"]
				elif "look at up to x cards from the top of your deck" in t or "look at up to x cards from top of your deck" in t:
					if "x = the number of your  characters" in t or "x = # of your  characters" in t:
						if "choose up to  card from among them" in t or "choose up to  of them" in t:
							if "put it in your hand" in t:
								return [-14, "looktop", "Trait", self.trait(a), "Stage", "top", "hand", self.digit(a), "", "upto", "played"]
				elif "draw up to  card" in t:
					if "choose  card in your hand, and put it in your waiting room" in t or "discard  card from your hand to the waiting room" in t:
						return ["drawupto", self.digit(a), "played", "do", ["discard", self.digit(a, 1), ""]]
					elif "choose up to  cost  or lower character in your hand" in t:
						if "put it on any position of your stage" in t:
							return ["drawupto", self.digit(a), "played", "do", ["discard", self.digit(a, 1), f"Cost_<={self.digit(a, 2)}", "Stage", "upto"]]
				elif "search your deck for up to   character" in t:
					if "put it in your hand" in t:
						if "reveal it" in t:
							return [self.digit(a), "search", f"Trait_{self.trait(a)}", "upto", "played", "show"]
				elif "put the top  cards of your deck in the waiting room" in t:
					if "this gets +x power" in t:
						if "x =  times # of  characters among those cards" in t:
							return ["mill", self.digit(a), "top", "pwr", "x#", "ctrait", self.trait(a), "if", "do", [0, self.digit(a, 1), x, "power"]]
					elif "this gets + power" in t:
						if "if there is at least  climax card among them" in t:
							return ["mill", self.digit(a), "top", "Climax", self.digit(a, 1), "if", "do", [0, self.digit(a, 2), x, "power"]]
				elif "reveal the top card of your deck" in t:
					if "draw  card" in t or "put it in your hand" in t:
						if "discard  card from your hand to the waiting room" in t or "discard  card from your hand" in t:
							if "if it's a character with  in name" in t:
								return [-9, "reveal", "Name", self.name(a, s='n'), "played", "do", ["draw", 1, "do", ["discard", self.digit(a), ""]]]
							elif "if it's a  character" in t:
								return [-9, "reveal", "Trait", self.trait(a), "played", "do", ["draw", 1, "do", ["discard", self.digit(a), ""]]]
							elif "if it's a  character or " in t and "or \"" in aa:
								return [-9, "reveal", "Trait", self.trait(a), "Name", self.name(a, 1), "played", "do", ["draw", 1, "do", ["discard", self.digit(a), ""]]]
					elif "if it's a climax card" in t:
						if "put this in the waiting room" in t:
							return [-9, "reveal", "Climax", "played", "do", [0, "waitinger"]]
						elif "this gets" in t and "this gets \"" in aa:
							return [-9, "reveal", "Climax", "played", "do", [0, self.name(a, s='a'), x, "give"]]
						elif "rest this" in t:
							return [-9, "reveal", "Climax", "played", "do", [0, "rest"]]
					elif "if it's a  character" in t:
						if "this gets + power" in t:
							return [-9, "reveal", "Trait", self.trait(a), "played", "do", [0, self.digit(a), x, "power"]]
					elif "if it's level  or higher" in t:
						if "put it in stock" in t:
							return [-9, "reveal", "Level", self.digit(a), "played", "do", ["stock", 1]]
					elif "if it's not a  character" in t or "revealed card is not a  character" in t:
						if "this gets " in t and "this gets \"" in aa:
							return [-9, "reveal", "Trait", self.trait(a), "not", "played", "if", "do", [0, self.name(a, s='a'), x, "give"]]
						elif "put it in your clock" in t:
							return [-9, "reveal", "Trait", self.trait(a), "clock", "not", "played"]
						elif "put this in your waiting room" in t:
							if "at the beginning of your encore step" in t:
								return [-9, "reveal", "Trait", self.trait(a), "not", "played", "if", "do", [0, "[AUTO] At the beginning of your encore step, put this card into your waiting room.", 1, "give"]]
						elif "rest this" in t:
							return [-9, "reveal", "Trait", self.trait(a), "not", "played", "if", "do", [0, "rest"]]
				elif "look at your opponent's hand" in t:
					return ["Hand", "opp", "look", "played"]
				elif "choose  cost  or higher character in your opponent's waiting room" in t:
					if "put it in an empty slot in your opponent's back stage" in t:
						return [self.digit(a), "salvage", f"Cost_>={self.digit(a)}", "Stage", "opp", "Back", "Open", "Opp"]
				elif "choose  of your opponent's characters" in t:
					if "move it to another vacant slot" in t:
						return [self.digit(a), "move", "Character", "Opp", "Open", "played", "may"]
				elif "choose  of your other level  or lower character" in t:
					if "that character gets + power" in t:
						return [self.digit(a), self.digit(a, 2), x, "power", "Other", "Level", f"<={self.digit(a, 1)}", "played"]
				elif "choose  of your standing characters" in t:
					if len([xs for xs in sx if xs == "Stand"]) >= self.digit(a):
						if "rest it" in t:
							return [self.digit(a), "rest", "Stand", "played"]
				elif "choose  of your characters with  in name" in t:
					if "put it in your clock" in t:
						return [self.digit(a), "clocker", "Name", self.name(a, s='n')]
					elif "put it in the waiting room" in t:
						return [self.digit(a), "waitinger", "Name", self.name(a, s='n')]
				elif "choose  of your  characters" in t:
					if "that character gets + power" in t:
						return [self.digit(a), self.digit(a, 1), x, "power", "Trait", self.trait(a), "played"]
				elif "choose  of your characters" in t:
					if "that character gets + power and + soul" in t:
						return [self.digit(a), self.digit(a, 1), x, "power", self.digit(a), self.digit(a, 2), x, "soul", "played"]
					elif "that character gets + power" in t:
						return [self.digit(a), self.digit(a, 1), x, "power", "played"]
				elif "choose  of your other  characters" in t:
					if "that character gets + power" in t:
						return [self.digit(a), self.digit(a, 1), x, "power", "Trait", self.trait(a), "Other", "played"]
					elif "that character gets +x power" in t:
						if "x =  times # of your other  characters" in t:
							return [self.digit(a), self.digit(a, 1), x, "#", "power", "Trait", self.trait(a), "Other", "#other", "#trait", self.trait(a), "played"]
					elif "that character gets + soul" in t:
						return [self.digit(a), self.digit(a, 1), x, "soul", "Trait", self.trait(a), "Other", "played"]
				elif "choose  of your other characters" in t:
					if "that character gets the following ability" in t:
						return [self.digit(a), self.name(a, s='a'), x, "give", "Other", "played"]
					elif "that character gets +x power" in t:
						if "x =  times level of that character" in t:
							return [self.digit(a), self.digit(a, 1), x, "X", "power", "Other", "xlevel", "x", self.digit(a, 1)]
				elif "choose another of your  characters" in t:
					if "that character gets + power" in t:
						return [1, self.digit(a), x, "power", "Trait", self.trait(a), "Other", "played"]
				elif "choose another character" in t:
					if "that character gets + level" in t:
						return [1, self.digit(a), x, "level", "Other", "played"]
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
				elif "if the number of your other  characters you have is  or more" in t:
					if "you may put the top card of your deck in your stock" in t:
						return [self.digit(a), "more", "Trait", self.trait(a), "other", "played", "do", ["pay", "may", "do", ["stock", 1]]]
				elif "draw  card" in t:
					if "choose  card in your hand" in t:
						if "put it in your waiting room" in t:
							return ["draw", self.digit(a), "played", "do", ["discard", self.digit(a, 1), ""]]
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
		elif "when this is placed on stage" in t:
			if pos[0] and r[0] == r[1] and v[0] == "Stand" and any(field in pos[1] for field in self.stage):
				if "you may pay the cost" in t:
					if "search your deck for up to  " in t:
						if "reveal it" in t and "put it in your hand" in t:
							return ["pay", "may", "played", "do", [self.digit(a), "search", f"Name=_{self.name(a, -1, s='n')}", "show", "upto"]]
				if "choose either this or  of your  " in t:
					if "put it in your waiting room" in t:
						return [self.digit(a), "waitinger", "Name=", self.name(a, s="n"), "This", "played"]
				else:
					return ["played"]
		elif "when this becomes rested from standing" in t:
			if r[0] == r[1] and r[0] == rst and v[0] == "Rest":
				if "deal  damage to all players" in t:
					return ["damage", self.digit(a), "both", "do", ["damage", self.digit(a), "opp"]]
		elif "when your opponent's stand character becomes rest" in t:
			if r[0] != r[1] and r[0][-1] != r[1][-1] and r[1] == rst and v[1] == "Rest":
				if "this gets + power" in t:
					if "if the total level of the cards in your level is  or higher" in t:
						return ["experience", self.digit(a), "do", [0, self.digit(a, 1), x, "power"]]
					else:
						return [0, self.digit(a), x, "power"]
		elif "during battles involving this" in t:
			if r[0] in baind:
				if "if damage taken by you is not canceled" in t and not cnc[1] and cnc[0] in r[0][-1]:
					if "you may pay the cost" in t:
						if "deal the same amount of damage to your opponent" in t and dmg > 0:
							return ["pay", "may", "do", ["damage", dmg, "opp"]]
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
								return [-38, "msalvage", "", "Stage", "a1", "seperate", "extra", "do", [-16, self.digit(a), x, "power"]]
				elif "at the beginning of your opponent's draw phase" in t or "at the start of your opponent's draw phase" in t:
					if n not in r[0][-1]:
						if "if this is in your center stage" in t or "if this is in the center stage" in t:
							if "Center" in pos[1]:
								if "choose  of your characters" in t:
									if "that character gets + power" in t:
										return [0, "stage", "Center", "a1", "do", [self.digit(a), self.digit(a, 1), x, "power"]]
						elif "reveal the top card of your deck" in t:
							if "if it's level  or higher" in t:
								if "you may return this to your hand" in t:
									return [-9, "reveal", "Level", self.digit(a), "a1", "do", ["pay", "may", "do", [0, "hander"]]]
		elif "Main" in p:
			if pp < 0:
				if "at the start of your main phase" in t:
					if n in r[0][-1]:
						if "if this is in memory" in t:
							if "Memory" in pos[1]:
								if "return this to your hand" in t:
									return [0, "stage", "Memory", "a1", "do", ["pay", "may", "do", [0, "hander", "Memory"]]]
		elif "Climax" in p:
			if pp < 0:
				if "at the start of your climax phase" in t or "at the beginning of your climax phase" in t:
					if n in r[0][-1]:
						if t.startswith("alarm"):
							if "you have  or more characters with  or " in t:
								if "you may put the top card of your deck in your stock" in t:
									if "» or «" in aa:
										return ["alarm","a1","do",[self.digit(a),"more","Trait",f"{self.trait(a)}_{self.trait(a,1)}","a1","do",["pay", "may", "do", ["stock", 1]]]]
						if "this gets +x power for the turn" in t:
							if "x =  times # of other  in your center stage" in t:
								return [0, self.digit(a), x, "Name", self.name(a, 1), "#", self.digit(a), "Center", "other", "a1", "power"]
						elif "you may pay the cost" in t:
							if aa.startswith("[auto] change"):
								if "choose   or  in your waiting room" in t:
									return ["pay", "may", "a1", "do", ["change", self.digit(a), f"Name_{self.name(a, s='n')}_{self.name(a, 2,s='n')}"]]
								else:
									return ["pay", "may", "a1", "do", ["change", self.digit(a), f"Name_{self.name(a, -1, s='n')}"]]
							elif aa.startswith("[auto] resonance"):
								if "choose  \"" in t and "\" in your waiting room and put it in any slot on the stage" in t:
									return ["pay", "may", "a1", "do", [self.digit(a), "salvage", f"Name=_{self.name(a, -1, s='n')}", "Stage"]]
								elif "this gets + power and + soul" in t:
									return ["pay", "may", "a1", "do", [0, self.digit(a), x, "power", 0, self.digit(a, 1), x, "soul"]]
								elif "this gets + power" in t:
									return ["pay", "may", "a1", "do", [0, self.digit(a), x, "power"]]
						elif "reveal the top card of your deck" in t:
							if "if it's a climax card" in t:
								if "choose  of your other characters" in t:
									if "put it in the waiting room" in t:
										return [-9, "reveal", "Climax", "a1", "do", [self.digit(a), "waitinger", "Other"]]
			elif pp == 0:
				if f"when \"{cx[0].lower()}\" is put on your climax area" in aa or f"when a card named \"{cx[0].lower()}\" is placed on your climax area" in aa or f"when \"{cx[0].lower()}\" is placed in your climax area" in aa:
					if r[0][-1] == cx[1][-1] and n in cx[1][-1] and cx[1] == r[1]:
						self.ablt=9
						if "if there are no markers under this" in t:
							if "choose up to   in your waiting room" in t:
								if "put them face-down under this as markers" in t:
									return [0, "markers", "cxcombo", "lower", "do", [self.digit(a), "marker", f"Name=_{self.name(a, -1, s='n')}", "Waiting", "upto", "none"]]
						elif "if this is in your center stage" in t or "if this is in the center stage" in t or "if this is on your center stage" in t or "if this in on your center stage" in t:
							if "Center" not in pos[1]:
								return []
							else:
								if "you may pay the cost" in t:
									if "choose  of your opponent's level  or lower characters" in t:
										if "put it in your opponent's stock" in t:
											return [0, "stage", "Center", "do", ["pay", "may", "do", [self.digit(a), "stocker", "Opp", "Level", f"<={self.digit(a, 1)}"]]]
									elif "choose  level  or lower character opposite this" in t:
										if "put it on top of the deck" in t:
											return [self.digit(a),"decker","top","Opp","Level",f"<={self.digit(a,1)}","Opposite"]
									elif "choose up to  level  or lower  character" in t:
										if "in your waiting room" in t:
											if "put them in separate position on your center stage" in t:
												if "at the start of the encore step, if those characters are on stage, return them to the deck" in t:
													return [0, "stage", "Center", "do", ["pay", "may", "do", [self.digit(a), "salvage", f"TraitL_{self.trait(a)}_<={self.digit(a, 1)}", "Stage", "Center", "extra1", "seperate", "upto", "do", [-21, "[AUTO] At the beginning of the encore step, if those characters are on stage, return them to your deck", 1, "give"]]]]
										elif " in your hand" in t:
											if "put it in any slot on the stage" in t:
												return [0, "stage", "Center", "do", ["pay", "may", "do", ["discard", self.digit(a), f"TraitL_{self.trait(a)}_<={self.digit(a, 1)}", "Stage", "upto"]]]
									elif "search your deck for up to  level  or lower  character" in t:
										if "put it on any position of your stage" in t:
											return [0, "stage", "Center", "at", "cxcombo", "do", ["pay", "may", "do", [self.digit(a), "search", f"TraitL_{self.trait(a)}_<={self.digit(a, 1)}", "Stage", "upto"]]]
									elif "search your deck for   character whose level is  or lower" in t:
										if "put it in any slot on stage" in t:
											return [0, "stage", "Center", "at", "cxcombo", "do", ["pay", "may", "do", [self.digit(a), "search", f"TraitL_{self.trait(a)}_<={self.digit(a, 1)}", "Stage"]]]
									elif "search your deck for up to  cards named " in t:
										if "put them on separate positions of your center stage" in t:
											return [0, "stage", "Center", "do", ["pay", "may", "do", [self.digit(a), "search", f"Name=_{self.name(a, -1, s='n')}", "Stage", "Center", "seperate", "upto"]]]
									elif "search your deck for up to   character" in t:
										if "put it in any slot on the stage" in t or "put it on any position of your stage" in t:
											return [0, "stage", "Center", "do", ["pay", "may", "do", [self.digit(a), "search", f"Trait_{self.trait(a)}", "Stage", "upto"]]]
									elif "search your deck for up to  level  or lower  character" in t:
										if "put that card on an open position of your stage" in t:
											return [0, "stage", "Center", "at", "cxcombo", "do", ["pay", "may", "do", [self.digit(a), "search", f"TraitL_{self.trait(a)}_<={self.digit(a, 1)}", "Stage", "Open", "upto"]]]
								elif "you may choose " in t and "\" in your waiting room" in aa:
									if "put it in any slot on the stage" in t:
										return [0, "stage", "Center", "do", ["pay", "may", "do", [self.digit(a), "salvage", f"Name=_{self.name(a, -1, s='n')}", "Stage", "upto"]]]
								elif "you may choose  level  or lower character from your clock" in t:
									if "put it in any slot on the stage" in t:
										if "put the top  cards of your deck in your clock" in t:
											return [0, "stage", "Center", "do", ["pay", "may", "do", ["cdiscard", self.digit(a), f"CLevel_<={self.digit(a, 1)}", "Stage", "upto", "if", self.digit(a), "do", ["damageref", self.digit(a, 2)]]]]
								elif "choose up to  cards in your opponent's waiting room" in t:
									if "return it to the deck" in t:
										if "this gets + power" in t:
											return [self.digit(a), "salvage", "", "Library", "upto", "opp", "show","do",[0,self.digit(a,1),x,"power"]]
								elif "search your deck for up to  card named " in t:
									if "put it on any position of your stage" in t:
										return [0, "stage", "Center", "do", [self.digit(a), "search", f"Name=_{self.name(a, -1, s='n')}", "upto", "Stage"]]
								elif "draw  card" in t:
									if "this gets + power and the following ability" in t:
										return [0, "stage", "Center", "do", ["draw", self.digit(a, 1), "do", [0, self.name(a, s="a"), x, "give", "do", [0, self.digit(a, 2), x, "power"]]]]
						elif "if you have another card named " in t:
							if "put the top card of your deck in your waiting room" in t:
								if "if that card is level  or lower, you may pay the cost" in t:
									if "all your characters get the following ability" in t:
										return [1, "name", self.name(a, 5), "other", "do", ["mill", 1, "lvl", self.digit(a, 1), "lower", "any", "if", "do", ["pay", "may", "do", [-1, self.name(a, s="a"), x, "give"]]]]
						elif "if you have no other character" in t:
							if "you may pay the cost" in t:
								if "put all your opponent's characters in stock" in t:
									return [0, "more", "Character", "other", "lower", "played", "do", ["pay", "may", "cxcombo", "do", [-1, "stocker", "opp"]]]
						elif "you may pay the cost" in t:
							if "this gets the following ability" in t:
								return ["pay", "may", "cxcombo", "do", [0, self.name(a, s="a"), x, "cxcombo", "give"]]
							elif "choose  level  or lower character in your clock" in t:
								if "put it in any slot on stage" in t:
									return ["pay", "may", "cxcombo", "do", ["cdiscard", self.digit(a), f"CLevel_<={self.digit(a, 1)}", "Stage"]]
							elif "choose  character in your waiting room with  or " in t:
								if "return it to your hand" in t:
									return ["pay", "may", "cxcombo", "do", [self.digit(a), "salvage", f"Trait_{self.trait(a)}_{self.trait(a, 1)}"]]
							elif "choose  card named  in your hand" in t:
								if "put it on the stage position that this was on" in t:
									return ["pay", "may", "cxcombo", "do", ["discard", self.digit(a), f"Name=_{self.name(a, -1, s='n')}", "Stage", "upto", "Change"]]
							elif "choose   character in your clock" in t:
								if "return it to your hand" in t:
									return ["pay","may","cxcombo","do",[self.digit(a),"csalvage",f"Trait_{self.trait(a)}","show"]]
							elif "choose  \"" in t and "put it in the slot this was in" in t:
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
							elif "search your deck for up to   and put it in the slot this was in" in t and "\" and put it in" in aa:
								return ["pay", "may", "cxcombo", "do", ["lchange", self.digit(a), f"Name=_{self.name(a, -1, s='n')}", "upto"]]
							elif "search your deck for up to   character" in t and "» character" in aa:
								if "reveal it" in t and "put it in your hand" in t:
									return ["pay", "may", "cxcombo", "do", [self.digit(a), "search", f"Trait_{self.trait(a)}", "show", "upto"]]
							elif "all your characters get + power" in t:
								return ["pay", "may", "cxcombo", "do", [-1, self.digit(a), x, "power"]]
							elif "this gets + power" in t:
								return ["pay", "may", "cxcombo", "do", [0, self.digit(a), x, "power"]]
						elif "you may put the top card of your deck in your stock" in t:
							return ["pay","may","cxcombo","do",["stock",1]]
						elif "you may put the top card of your deck under this as marker" in t:
							return ["pay", "may", "cxcombo", "do", [1, "marker", "top"]]
						elif "you may choose   character in your waiting room" in t:
							if "put it in stock" in t:
								return ["pay", "may", "cxcombo", "do", [1, "salvage", f"Trait_{self.trait(a)}", "Stock", "upto"]]
						elif "choose  level  or lower character in your clock with  in name" in t:
							if "put it in any slot on the stage" in t:
								return ["cdiscard", self.digit(a), f"CLevelN_<={self.digit(a, 1)}_{self.name(a, -1, s='n')}", "Stage"]
						elif "choose  of your opponent's cards in in the waiting room" in t:
							if "return them in your opponent's deck" in t:
								if "this gets + power" in t:
									return [self.digit(a, 1), "shuffle", "opp", "cxbombo", "do", [0, self.digit(a, 2), x, "power"]]
						elif "choose  of your  characters" in t:
							if "that character gets + power" in t:
								return [self.digit(a), self.digit(a, 1), x, "power", "Trait", self.trait(a)]
						elif "choose  of your other characters" in t:
							if "that character gets the following ability" in t:
								return [self.digit(a), self.name(a, s='a'), x, "give", "Other"]
						elif "choose  of your characters" in t:
							if "gets + power" in t:
								return [self.digit(a), self.digit(a, 1), x, "power"]
						elif "this gets + power" in t:
							return [0, self.digit(a), x, "power"]
				elif "when a climax is placed on your opponent's climax area" in t or "when your opponent's climax card is placed in the climax area" in t:
					if n not in r[0][-1] and n in cx[1][-1] and r[0][-1] != cx[1][-1] and cx[0] != "" and cx[1] == r[1]:
						if "you may pay the cost" in t:
							if "choose  character opposite this" in t:
								if "put it in your opponent's waiting room" in t or "put it in the waiting room" in t:
									return ["stage", "Center", "do", ["pay", "may", "do", [1, "waitinger", "Opposite"]]]
				elif "when your climax is placed in the climax area" in t:
					if r[0][-1] == cx[1][-1] and n in cx[1][-1] and n in r[0][-1] and cx[0] != "" and cx[1] == r[1]:
						self.ablt = 9
						if "you may pay the cost" in t:
							if "look at up to  cards from top of your deck" in t:
								if "search for up to  character with  or " in t:
									if "reveal it" in t and "put it in your hand" in t:
										return ["pay", "may", "do", [self.digit(a), "looktop", "top", "hand", self.digit(a, 1), f"Trait_{self.trait(a)}_{self.trait(a, 1)}", "show", "upto"]]
							elif "choose  of your characters" in t:
								if "that character gets + power" in t:
									return ["pay", "may", "do", [self.digit(a), self.digit(a, 1), x, "power"]]
						elif "choose  of your characters" in t:
							if "that character gets + power" in t:
								return [self.digit(a), self.digit(a, 1), x, "power"]
						elif "this gets + power" in t:
							return [0, self.digit(a), x, "power"]
		elif "Attack" in p:
			if pp < 0:
				if "at the start of your opponent's attack phase" in t or "at the beginning of your opponent's attack phase" in t:
					if n not in r[0][-1]:
						if "you may pay the cost" in t:
							if "move this to an empty slot in your center stage" in t:
								return ["pay", "may", "a1", "do", [1, "move", "Center", "Open", "this"]]
						elif "you may put the top card of your deck in your waiting room" in t or "you may put the top card of your deck in the waiting room" in t:
							if "that card is a  character" in t or "if it's a  character" in t:
								if "you may move this to an open position of your center stage" in t or "you may move this to an empty slot in the center stage" in t:
									return ["pay", "may", "a1", "do", ["mill", 1, "Trait", self.trait(a), "any", "if", "do", [1, "move", "Center", "may", "Open", "this"]]]
						elif "you may move this to an empty slot in the center stage" in t or "you may move this to an open position of your center stage" in t or "you may move this to an empty slot in your center stage" in t:
							return ["pay", "may", "a1", "do", [1, "move", "Center", "Open", "may", "this"]]  # "runner",
						elif "you may move this to an empty slot opposite an opponent's character" in t:
							return ["pay", "may", "a1", "do", [1, "move", "OpponentOpposite", "Open", "may", "this"]]  # "runner",
						elif "this randomly gets between +~+ power" in t:
							return [0, self.digit(a), x, "random", self.digit(a, 1), "a1", "power"]
		elif "Declaration" in p:
			if "when this attacks or is attacked" in t:
				if atk != "" and r[0] in baind and n in r[1][-1] and (r[0] == r[1] or (r[0] != r[1] and r[0][-1] != r[1][-1])):
					if "put the top card of your stock under this as marker" in t:
						return [1, "marker", "top", "Stock"]
			elif "when this attacks" in t:
				if r[0] == r[1] and n in r[1][-1] and atk != "" and r[0] in baind[0] and r[0] not in baind[1]:
					if "\" is in the climax area" in aa or "\" is in your climax area" in aa or "\" on your climax area" in aa:
						if (f"\"{cx[0].lower()}\" is in the climax area" in aa or f'\"{cx[0].lower()}\" is in your climax area' in aa or f'\"{cx[0].lower()}\" on your climax area' in aa) and r[0][-1] == cx[1][-1] and n in cx[1][-1]:
							self.cx = True
							self.ablt = 2
							if "your opponent searches your deck for  level  or higher character" in t:
								if "put it in your hand" in t:
									return [self.digit(a), "searchopp", f"CLevel_>={self.digit(a, 1)}"]
							elif "your opponent may not play events from hand" in t or "your opponent cannot play event cards from hand" in t:
								return [-21, "[CONT] Your opponent cannot play events from hand", x, "give"]
							elif "you may choose  of your opponent's characters" in t:
								if "return it to their hand" in t or "return it to hand" in t or "return it to your opponent's hand" in t or "return it to his or her hand" in t:
									return ["pay", "may", "cxbombo", "at", "do", [self.digit(a), "hander", "Opp", "upto"]]
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
											return ["pay", "may", "cxbombo", "at", "do", [self.digit(a), "cstock", f"Trait_{self.trait(a)}", "Waiting", "do", [0, self.digit(a, 1), x, "power"]]]
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
								elif "choose  card in your opponent's waiting room" in t:
									if "send it to memory" in t:
										return ["pay", "may", "at", "do", [self.digit(a), "salvage", "", "opp", "Memory"]]
								elif "choose  cost  or lower character in your opponent's" in t:
									if "opponent's center stage" in t:
										if "put it on the bottom of the deck" in t:
											if "then choose up to  other character in your opponent's center stage with the same name as that character" in t:
												if "put it on bottom of the deck" in t:
													return ["pay", "may", "cxcombo", "at", "do", [self.digit(a), "decker", "bottom", "Cost", f"<={self.digit(a, 1)}", "Opp", "Center", "save_name", "do", [self.digit(a), "decker", "bottom", "Name=", "same_name", "Center", "Opp"]]]
								elif "choose up to  of your opponent's level  or lower characters" in t:
									if "and put that character into the stock" in t:
										return ["pay", "may", "cxbombo", "at", "do", [self.digit(a), "stocker", "Level", f"<={self.digit(a, 1)}", "Opp", "upto"]]
								elif "choose up to  character in your waiting room" in t:
									if "return it to your hand" in t:
										if "all your  characters get + power" in t:
											return ["pay", "may", "cxcombo", "at", "do", [self.digit(a), "salvage", "Character", "upto", "show", "do", [-1, self.digit(a, 1), x, "power", "Trait", self.trait(a)]]]
								elif "choose up to  other of your character" in t or "choose up to  of your other character" in t:
									if "those characters get" in t:
										return ["pay", "may", "cxbombo", "at", "do", [self.digit(a), self.name(a, s='a'), x, "give", "Other", "upto"]]
									elif "return them to your hand" in t:
										return ["pay", "may", "cxcombo", "at", "do", [self.digit(a), "hander", "at", "Other", "upto"]]
								# elif "choose  of your opponent's level  or lower characters" in t or "choose  level  or lower character in your opponent's" in t or "choose  of your opponent's characters whose level is  or lower" in t:
								# 	if "put it in stock" in t:
								# 		return ["pay", "may", "cxbombo", "at", "do", [self.digit(a), "stocker", "Level", f"<={self.digit(a, 1)}", "Opp"]]
								# 	elif "put it on the bottom of the deck" in t:
								# 		if "opponent's center stage" in t:
								# 			return ["pay", "may", "cxcombo", "at", "do", [self.digit(a), "decker", "bottom", "Level", f"<={self.digit(a, 1)}", "Center", "Opp"]]
								# 	elif "put that character on top of the deck" in t:
								# 		return ["pay", "may", "cxcombo", "at", "do", [self.digit(a), "decker", "top", "Level", f"<={self.digit(a, 1)}", "Opp"]]
								elif "choose  of your other characters and this" in t:
									if "they get the following ability" in t:
										return ["pay", "may", "at", "cxcombo", "do", [self.digit(a), self.name(a, s='a'), x, "give", "Other", "this"]]
								elif "search your deck for up to  level  or higher character with  or " in t:
									if "reveal it" in t and "put it in your hand" in t:
										return ["pay", "may", "cxcombo", "at", "do", [self.digit(a), "search", f"TraitL_{self.trait(a)}_{self.trait(a, 1)}_>={self.digit(a)}"], "upto", "show"]
								elif "search your deck for up to   character" in t:
									if "put it in your hand" in t and "reveal it" in t:
										return ["pay", "may", "cxcombo", "at", "do", [self.digit(a), "search", f"Trait_{self.trait(a)}", "upto", "show"]]
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
								elif "deal x damage to your opponent" in t:
									if "x = # of  in your waiting room" in t:
										return ["pay", "may", "at", "do", ["damage", "x", "Name=", self.name(a, -1, s='n'), "Waiting", "opp"]]
									elif "x = # of climax cards in your waiting room" in t:
										return ["pay", "may", "at", "do", ["damage", "x", "Climax", "Waiting", "opp"]]
								elif "deal  damage to your opponent" in t:
									return ["pay", "may", "cxcombo", "at", "do", ["damage", self.digit(a), "opp"]]
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
							elif "you may choose  level x or lower  character in your waiting room" in t:
								if "x = # of cards in your memory" in t:
									if "return it to your hand" in t:
										return ["pay", "may", "at", "do", [self.digit(a), "salvage", f"CLevel_<=0", "xmemory", "x#"]]
							elif "you may choose  cost  or lower character" in t:
								if "return it to hand" in t:
									if "in your opponent's center stage" in t:
										return ["pay", "may", "at", "do", [self.digit(a), "hander", "Opp", "Cost", f"<={self.digit(a, 1)}", "Center"]]
							elif "you may choose  card in your opponent's waiting room" in t:
								if "put it on top of the deck" in t:
									return ["pay", "may", "at", "cxcombo", "do", [self.digit(a), "salvage", "", "Library", "top", "upto", "opp", "show"]]
							elif "you may choose  character in your waiting room" in t:
								if "return it to your hand" in t:
									return ["pay", "may", "at", "cxcombo", "do", [self.digit(a), "salvage", "Character", "upto", "show"]]
							elif "you may choose up to   characters in your waiting room" in t:
								if "return them to your hand" or "return it to your hand" in t:
									if "choose  cards from your hand" in t:
										if "put them in your waiting room" in t or "put it in your waiting room" in t:
											return ["pay", "may", "at", "cxcombo", "do", [self.digit(a), "salvage", f"Trait_{self.trait(a)}", "upto", "show", "do", ["discard", self.digit(a, 1), ""]]]
							elif "you may put the top card of your clock in the waiting room" in t:
								return ["pay", "may", "cxcombo", "at", "do", ["heal", 1, "top"]]
							elif "put the top card of your deck in your stock" in t or "choose the top card of your deck and put it in your stock" in t:
								if "all your characters get + power" in t:
									return ["stock", 1, "cxcombo", "at", "do", [-1, self.digit(a), x, "power"]]
								elif "this gets +x power" in t:
									if "x =  times # of cards in your stock" in t:
										return ["stock", 1, "cxcombo", "at", "do", [0, self.digit(a), x, "#", "power", "Stock"]]
								elif "this gets + power" in t:
									return ["stock", 1, "cxcombo", "at", "do", [0, self.digit(a), x, "power"]]
							elif "put the top  cards of your deck in your waiting room" in t:
								if "if all those cards are  characters" in t:
									if "draw  card" in t:
										return ["mill", self.digit(a), "Trait", self.trait(a), "if", "at", "cxcombo", "all", "do", ["draw", self.digit(a, 1)]]
							elif "put the bottom  cards of your opponent's deck in the waiting room" in t:
								if "deal x damage to your opponent" in t:
									if "x = # of climax cards among those cards" in t:
										return ["mill", self.digit(a), "bottom", "x#", "Climax", "if", "at", "cxcombo", "do", ["damage", 1, "opp"]]
							elif "search your deck for up to   or  character" in t:
								if "reveal it" in t and "put it in your hand" in t:
									return [self.digit(a), "search", f"Trait_{self.trait(a)}_{self.trait(a, 1)}", "upto", "show", "cxcombo", "at"]
							elif "search your deck for up to   character" in t:
								if "put it in your hand" in t and "reveal it" in t:
									return [self.digit(a), "search", f"Trait_{self.trait(a)}", "upto", "show", "cxcombo", "at"]
							elif "choose  character in your opponent's center stage" in t:
								if "that character gets - power" in t:
									return [self.digit(a), self.digit(a, 1), x, "power", "Opp", "Center"]
							elif "choose  character in your waiting room" in t or "choose  character from your waiting room" in t:
								if "return it to your hand" in t:
									return [self.digit(a), "salvage", "Character", "cxbombo", "at", "show"]
							elif "choose up to  other of your characters" in t:
								if "put it in stock" in t:
									if "choose  of your characters" in t:
										if "that character gets + power" in t:
											return [self.digit(a), "stocker", "Other", "upto", "at", "cxcombo", "do", [self.digit(a, 1), self.digit(a, 2), x, "power"]]
							elif "choose up to  of your other character" in t:
								if "put them in your memory" in t or "put it in your memory" in t:
									return [self.digit(a), "memorier", "Other", "upto", "extra", "at", "cxcombo", "do", [-21, self.name(a, s='at'), 3, "give", "expass", self.digit(a), "ex_ID="]]
							elif "choose up to   character in your waiting room" in t:
								if "put it in your stock" in t:
									if "this gets + power" in t:
										return [self.digit(a), "cstock", f"Trait_{self.trait(a)}", "Waiting", "upto", "do", [0, self.digit(a, 1), x, "power"]]
							elif "choose up to  card in your opponent's waiting room" in t:
								if "put it on top of the deck" in t:
									if "this gets + power" in t:
										return [self.digit(a), "salvage", "", "opp", "Library", "top", "at", "show", "upto", "do", [0, self.digit(a, 1), x, "power"]]
									else:
										return [self.digit(a), "salvage", "", "opp", "Library", "top", "at", "show", "upto"]
							elif "look at up to  cards from top of your deck" in t:
								if "search for up to   character" in t:
									if ("reveal it" in t or "reveal them" in t) and ("put it in your hand" in t or "put them in your hand" in t):
										if "your opponent cannot play events from hand until the next end of your opponent's turn" in t:
											return [self.digit(a), "looktop", "top", "hand", self.digit(a, 1), f"Trait_{self.trait(a)}", "upto", "show", "at", "do", [-21, "[CONT] Your opponent cannot play events from hand", 2, "give"]]
										else:
											return [self.digit(a), "looktop", "top", "hand", self.digit(a, 1), f"Trait_{self.trait(a)}", "upto", "show", "at"]
							elif "look at the top  cards of your deck" in t:
								if "put them back in any order" in t:
									return [self.digit(a), "looktop", "top", "reorder", "cxcombo", "at"]
							elif "look at the top card of your opponent's deck" in t:
								if "put it on the top or the bottom of your opponent's deck" in t:
									return [1, "looktop", "top", "bottom", "opp", "cxcombo", "at"]
							elif "you may deal  damage to your opponent" in t:
								return ["pay", "may", "cxbombo", "at", "cxcombo", "do", ["damage", self.digit(a), "opp"]]
							elif "choose  of your characters with  in name" in t:
								if "that character gets + power" in t and "this gets + power" in t:
									return [self.digit(a), self.digit(a, 1), x, "power", "at", "Name", self.name(a, -1, s='n'), "do", [0, self.digit(a, 2), x, "power"]]
							elif "choose  of your other characters" in t:
								if "that character gets + power" in t and "this gets + power" in t:
									return [self.digit(a), self.digit(a, 1), x, "power", "at", "Other", "do", [0, self.digit(a, 2), x, "power"]]
								elif "that character gets + power and the following ability" in t:
									return [self.digit(a), self.digit(a, 1), x, "power", "Other", "extra", "at", "do", [-16, self.name(a, s='a'), x, "give"]]
								elif "that character gets the following ability" in t:
									return [self.digit(a), self.name(a, s='a'), x, "give", "Other", "at"]
							elif "choose  of your opponent's character" in t:
								if "that character gets -x power" in t:
									if "x =  times # of your  characters" in t or "x =  multiplied by the number of  characters you have" in t:
										return [self.digit(a), self.digit(a, 1), x, "#", "power", "Opp", "#trait", self.trait(a), "at", "cxcombo", "x", self.digit(a, 1), "negative"]
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
							elif "draw  card" in t:
								if "this gets + power" in t:
									if "discard  card from your hand to the waiting room" in t:
										return ["draw", self.digit(a), "at", "cxcombo", "do", ["discard", self.digit(a), "", "do", [0, self.digit(a, 2), x, "power"]]]
									else:
										return ["draw", self.digit(a), "at", "cxcombo", "do", [0, self.digit(a, 1), x, "power"]]
								else:
									return ["draw", self.digit(a), "at", "cxcombo"]
							elif "draw up to  cards" in t:
								if "and discard  card from your hand to the waiting room" in t:
									return ["drawupto", self.digit(a), "do", ["discard", self.digit(a, 1), ""]]
							elif "all your  characters get" in t:
								if "get + power and + soul" in t:
									return [-1, self.digit(a), x, "Trait", self.trait(a), "power", -1, self.digit(a, 1), x, "Trait", self.trait(a), "soul"]
								elif "get the following ability" in t:
									return [-1, self.name(a, s='a'), x, "give", "at", "Trait", self.trait(a)]
								elif "get + power" in t:
									return [-1, self.digit(a), x, "power", "Trait", self.trait(a), "at"]
							elif "all your other characters get + power" in t:
								return [-2, self.digit(a), x, "power", "at"]
							elif "all your characters get + power" in t:
								return [-1, self.digit(a), x, "power", "at"]
					elif "if a  climax is in your climax area" in t:
						if f"if a {cx[2].lower()} climax is in your climax area" in aa and r[0][-1] == cx[1][-1] and n in cx[1][-1]:
							if "draw  card, choose  card in your hand, and put it in your waiting room" in t:
								return ["draw", self.digit(a), "cxcombo", "at", "do", ["discard", self.digit(a, 1), ""]]
					elif "if it is the first turn of the player who went first" in t:
						if "you may attack with up to  characters during this turn" in t:
							return ["turn", 1, "at", "do", ["d_atk", self.digit(a)]]
					elif "if all your other characters have lower power than this" in t:
						if "this gets + power" in t:
							return [-2, "atkpwrchk", "lower", "self", "at", "do", [0, self.digit(a), x, "power"]]
					else:
						self.ablt = 2
						if "you may pay the cost" in t:
							if "put all level  or lower characters in your opponent's center stage to the waiting room" in t:
								return ["pay", "may", "at", "do", [-1, "waitinger", "Level", f"<={self.digit(a)}", "Opp", "Center"]]
							elif "if you have another card named  in your center stage" in t:
								if "deal  damage to your opponent" in t:
									return [1, "name", self.name(a, s="n"), "other", "Center", "at", "do", ["pay", "may", "do", ["damage", self.digit(a), "opp"]]]
							elif "choose   character in your waiting room" in t:
								if "return it to your hand" in t:
									return ["pay", "may", "at", "do", [self.digit(a), "salvage", f"Trait_{self.trait(a)}", "show"]]
							elif "choose  of your other  characters" in t:
								if "return it to your hand" in t:
									if "» characters" in self.a_replace(a):
										return ["pay", "may", "at", "do", [self.digit(a), "hander", "Other", "Trait", self.trait(a)]]
									elif "\" characters" in self.a_replace(a):
										return ["pay", "may", "at", "do", [self.digit(a), "hander", "Other", "Trait", self.trait(a)]]
							elif "choose  of your  character" in t:
								if "that character gets + soul" in t:
									return ["pay", "may", "at", "do", [self.digit(a), self.digit(a, 1), x, "soul", "Trait", self.trait(a)]]
							elif "choose  of your character" in t:
								if "that character gets + power" in t:
									return ["pay", "may", "at", "do", [self.digit(a), self.digit(a, 1), x, "power", "at"]]
							elif "choose up to  of your other characters" in t:
								if "put them in your waiting room" in t:
									if "deal x damage to your opponent" in t:
										if "x = the number of characters put in your waiting room" in t:
											return ["pay", "may", "at", "do", [self.digit(a), "waitinger", "Other", "upto", "extra", "do", ["damage", -16, "opp"]]]
							elif "all your characters with  or " in t:
								if "get + soul" in t:
									return ["pay", "may", "at", "do", [-1, self.digit(a), x, "soul", "Trait", f"{self.trait(a)}_{self.trait(a, 1)}"]]
						elif "you may look at the top card of your deck" in t:
							if "put that card face-down under this as marker" in t:
								return ["pay", "may", "at", "do", [1, "looktop", "check", "do", [1, "marker", "top"]]]
						elif "you may choose  of your other characters with  in name" in t:
							if "put it in your stock" in t:
								return ["pay", "may", "at", "do", [self.digit(a), "stocker", "Name", self.name(a, s='n'), "Other", "upto"]]
						elif "you may choose  climax in your climax area" in t:
							if "put it in the stock" in t:
								return ["pay", "may", "at", "do", [self.digit(a), "stocker", "Climax", "upto"]]
						elif "if the level of the character opposite this is  or higher" in t:
							if "this gets + power and + soul" in t:
								return ["opposite", "olevel", self.digit(a), "at", "do", [0, self.digit(a, 1), x, "power", 0, self.digit(a, 2), x, "soul"]]
							elif "this gets + power" in t:
								return ["opposite", "olevel", self.digit(a), "at", "do", [0, self.digit(a, 1), x, "power"]]
						elif "if you have  or more other  characters" in t:
							if "look at up to  cards from top of your deck, choose  of them and put it on top of the deck, and put the rest in the waiting room" in t:
								return [self.digit(a), "more", "Trait", self.trait(a), "other", "at", "do", [self.digit(a, 1), "looktop", "top", self.digit(a, 2), "upto", "all", "Library"]]
							elif "choose  of your characters" in t:
								if "and that character gets + power and + soul for the turn" in t:
									return [self.digit(a), "more", "Trait", self.trait(a), "other", "at", "do", [self.digit(a, 1), self.digit(a, 2), x, "power", self.digit(a, 1), self.digit(a, 3), x, "soul"]]
						elif "if the number of cards in your hand is  or more" in t:
							if "choose  of your  characters" in t:
								if "that character gets + power" in t:
									return [self.digit(a), "cards", "Hand", "at", "do", [self.digit(a, 1), self.digit(a, 2), x, "Trait", self.trait(a), "power"]]
						elif "if the number of cards in your stock is  or less" in t:
							return [self.digit(a), "cards", "Stock", "lower", "at", "do", [0, "waitinger"]]
						elif "if you have another character with  or " in t:
							if "this gets + power" in t:
								return [1, "more", "Trait", f"{self.trait(a)}_{self.trait(a, 1)}", "other", "at", "do", [0, self.digit(a), x, "power"]]
						elif "if you have  or fewer other character" in t:
							if "you may put the top card of your deck in the waiting room" in t:
								if "if it's a level  or lower character" in t:
									if "put that character in any slot in the back stage" in t:
										return [self.digit(a), "more", "", "other", "lower", "do", ["pay", "may", "do", ["mill", 1, "lvl", self.digit(a, 1), "any", "extra", "if", "do", [-16, "salvage", "", "Stage", "Back"]]]]
						elif "choose  of your other  characters" in t:
							if "that character gets +x power" in t:
								if "x =  times # of your other  characters" in t:
									return [self.digit(a), self.digit(a, 1), x, "#", "power", "#trait", self.trait(a), "Other", "#other"]
							elif "that character gets + power" in t:
								return [self.digit(a), self.digit(a, 1), x, "power", "Trait", self.trait(a), "Other"]
						elif "choose  of your other characters" in t:
							if "that character gets + level and + power" in t:
								return [self.digit(a), self.digit(a, 1), x, "level", "Other", "extra", "do", [-16, self.digit(a, 2), x, "power"]]
							elif "that character gets +x power" in t:
								if "x =  times level of that character" in t:
									return [self.digit(a), self.digit(a, 1), x, "X", "power", "Other", "at", "xlevel", "x", self.digit(a, 1)]
						elif "choose  of your characters with " in t:
							if "that character gets + soul" in t:
								if self.name(a, s='n') in self.text_name:
									return [self.digit(a), self.digit(a, 1), x, "soul", "Text", self.text_name[self.name(a, s='n')]]
						elif "choose  of your  characters" in t:
							if "that character gets + power" in t:
								return [self.digit(a), self.digit(a, 1), x, "power", "at", "Trait", self.trait(a)]
						elif "choose  of your characters" in t:
							if "that character gets + power" in t:
								return [self.digit(a), self.digit(a, 1), x, "power", "at"]
						elif "choose up to  climax in your hand" in t:
							if "put it face down underneath this as a marker" in t and "reveal it" in t:
								return [self.digit(a), "marker", "Climax", "Hand", "at", "show", "upto"]
						elif "choose up to  of your  characters" in t:
							if "those characters get + power" in t or "that character gets + power" in t:
								return [self.digit(a), self.digit(a, 1), x, "power", "at", "Trait", self.trait(a), "upto"]
						elif "choose   on your stage" in t:
							if "return it to your hand" in t:
								if "\" on your stage" in self.a_replace(a):
									return [self.digit(a), "hander", "Name=", self.name(a, s='n')]
						elif "reveal the top card of your deck" in t:
							if "if it's a climax card" in t or "if the revealed card is a climax" in t:
								if "this gets + power" in t:
									return [-9, "reveal", "Climax", "at", "do", [0, self.digit(a), x, "power"]]
								elif "this gets - power" in t:
									return [-9, "reveal", "Climax", "at", "do", [0, self.digit(a), x, "power"]]
						elif "rest all your other standing characters" in t or "rest all your other stand characters" in t:
							return [-1, "rest", "Stand", "Other", "at"]
						elif " all your characters with  in the name get + power" in t:
							return [-1, self.digit(a), x, "power","Name",self.name(a,s='n'), "at"]
						elif "this gets +x power" in t:
							if "x =  times # of your  characters" in t:
								if "if there are  or more cards in your memory" in t:
									return [self.digit(a), "cards", "Memory", "do", [0, self.digit(a, 1), x, "#", "Trait", self.trait(a), "power"]]
								elif "if there are cards in your memory" in t:
									return [1, "cards", "Memory", "do", [0, self.digit(a), x, "#", "Trait", self.trait(a), "power"]]
			elif "when this is front attacked" in t and "\"[auto] when this is front attacked" not in aa:
				if r[0] != r[1] and n in r[1][-1] and r[0][-1] != r[1][-1] and r[0] in baind[1] and r[1] in baind[0] and "f" in atk:
					if "you may choose  of your other characters and this" in t:
						if "return them to your hand" in t:
							return ["pay", "may", "at", "do", [self.digit(a), "hander", "Other", "this"]]
					elif "you may return this to your hand" in t:
						if "if the character opposite this has no traits" in t:
							return ["opposite", "#traits", 0, "#lower", "at", "do", ["pay", "may", "do", [0, "hander"]]]
					elif "you may pay the cost" in t:
						if "choose   in your hand" in t:
							if "put it in the slot this was" in t:
								return ["pay","may","at","do",["discard", self.digit(a), f"Name=_{self.name(a, s='n')}", "Stage", "Change"]]
					elif "look at the top card of your deck" in t:
						if "put it on the top of your deck or in your waiting room" in t:
							return [1, "looktop", "top", "Waiting"]
			elif "when this direct attacks" in t:
				if r[0] == r[1] and n in r[1][-1] and r[0] in baind[0] and "d" in atk:
					if "if  is in the climax area" in t:
						if f"if \"{cx[0].lower()}\" is in the climax area" in aa and r[0][-1] == cx[1][-1] and n in cx[1][-1]:
							if "this gets + power and the following ability" in t:
								return [0, self.digit(a), x, "power", "at", "do", [0, self.name(a, -1, s='a'), x, "give"]]
			elif "when this front attack" in t:
				if r[0] == r[1] and n in r[1][-1] and r[0] in baind[0] and "f" in atk:
					if "you may pay the cost" in t:
						if "choose  of your opponent's character" in t:
							if "that character gets - level" in t:
								return ["pay","may","at","do",[self.digit(a),self.digit(a,1),x,"level","Opp"]]
					elif "if you have another  character" in t:
						if "this gets +x power" in t and "x =  multiplied by the soul of this" in t:
							return [1, "more", "Trait", self.trait(a), "other", "at", "do", [0, self.digit(a), x, "X", "xsoul", "x", self.digit(a), "power"]]
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
					if "this gets + power" in t:
						return [0, self.digit(a), x, "power", "at"]
			elif "when your other character with  or " in t and "in name is front attacked" in t:
				if r[0] != r[1] and r[0][-1] != r[1][-1] and r[0] not in baind and r[1] in baind[0] and "f" in atk and n in r[1][-1] and (self.name(a, s="n") in nmop[1] or self.name(a, 2, s='n') in nmop[1]) and r[0][-1] == baind[1][-1]:
					if "you may pay the cost" in t:
						if "choose  of your characters in battle" in t:
							if "that character gets + power" in t:
								return ["pay", "may", "do", [self.digit(a), self.digit(a, 1), x, "power", "Battle"]]
			elif "when another of your characters with  in its card name is frontal attacked" in t:
				if r[0] != r[1] and r[0][-1] != r[1][-1] and r[0] not in baind and r[1] in baind[1] and "f" in atk and n in r[1][-1] and self.name(a, s="a") in nmop[1]:
					if "you may pay the cost" in t:
						if "choose  of your characters in battle" in t:
							if "that character gets + power" in t:
								return ["pay", "may", "at", "do", [self.digit(a), self.digit(a, 1), x, "Battle", "power"]]
			elif "when your character direct attacks" in t:
				if r[0][-1] == r[1][-1] and n in r[1][-1] and r[1] in baind[0] and "d" in atk:
					if "choose  of your characters" in t:
						if "that character gets + power" in t:
							return [self.digit(a), self.digit(a, 1), x, "power"]
		elif "Trigger" in p:
			if "when your character's trigger check reveals a climax" in t:
				if n in r[0][-1] and r[0][-1] == r[1][-1] and r[0] != r[1] and "Climax" in ty[0]:
					if "if the trigger icons of that card are" in t or "if that card's trigger icon is" in t:
						if (("soulsoul trigger icons" in t or "icon is soulsoul" in t) and len([s for s in ty[1] if s == "soul"]) == 2) or ("trigger icon is door" in t and "door" in ty[1]) or ("trigger icon is bounce" in t and "bounce" in ty[1]) or ("trigger icon is stock" in t and "stock" in ty[1]) or ("trigger icon is draw" in t and "draw" in ty[1]):
							if "you may pay the cost" in t:
								if "choose  character in your waiting room" in t:
									if "return it to your hand" in t:
										return ["pay", "may", "do", [self.digit(a), "salvage", "Character", "show"]]
								elif "choose  of your opponent's level  or lower characters" in t or "choose  level  or lower character in your opponent" in t:
									if "put it into his or her waiting room" in t:
										if "in the center stage" in t or "opponent's center stage" in t:
											return ["pay", "may", "do", [self.digit(a), "waitinger", "Level", f"<={self.digit(a, 1)}", "Opp", "Center"]]
								elif "choose  of your opponent's character" in t:
									if "that character gets - power" in t:
										return ["pay", "may", "do", [self.digit(a), self.digit(a, 1), x, "power", "Opp"]]
								elif "search your deck for up to   character" in t:
									if "reveal it" in t and "put it in your hand" in t:
										return ["pay", "may", "do", [self.digit(a), "search", f"Trait_{self.trait(a)}", "upto", "show"]]
							elif "you may draw  card" in t:
								if "choose  card in your hand" in t:
									if "put it in your waiting room" in t:
										return ["pay", "may", "do", ["draw", self.digit(a), "if", self.digit(a), "do", ["discard", self.digit(a, 1), ""]]]
					elif "choose  of your characters" in t:
						if "that character gets + power" in t:
							return [self.digit(a), self.digit(a, 1), x, "power"]
			elif "when the trigger check of this reveals a climax card" in t:
				if n in r[0][-1] and r[0][-1] == r[1][-1] and r[0] != r[1] and "Climax" in ty[0] and r[0] == ty[2]:
					if "you may put the top card of your clock in your waiting room" in t:
						return ["pay", "may", "do", ["heal", 1, "top"]]
		elif "Counter" in p:
			if pp < 0:
				if "at the beginning of counter step during your opponent's turn" in t:
					if n not in r[0][-1]:
						if "you may pay the cost" in t:
							if "choose  level  or higher character battling this" in t:
								if "put it on bottom of the deck" in t:
									return ["pay", "may", "a1", "do", [self.digit(a), "decker", "bottom", "Battle", "Opp", "Level", f">={self.digit(a, 1)}"]]
			elif pp == 0:
				if "when you use the backup of this" in t or "when you use this's " in t:
					if r[0] == r[1] and r[0] == act:
						if t.startswith("experience"):
							if "if the total level of the cards in your level is  or higher" in t or "if the sum of levels of cards in your level zone is  or higher" in t:
								if "choose  of your characters in battle" in t or "choose  of your battling characters" in t:
									if "that character gets + power" in t:
										return ["experience", self.digit(a), "at", "do", [self.digit(a, 1), self.digit(a, 2), x, "Battle", "power"]]
						elif "you may pay the cost" in t:
							if "return all cards in your waiting room to the deck" in t or "return all cards in your waiting room to your deck" in t:
								if "shuffle your deck" in t:
									return ["pay", "may", "at", "do", [-1, "shuffle"]]
							elif "choose  of your opponent's characters whose level is higher than the level of your opponent" in t:
								if "put it in the waiting room" in t:
									if "if you have  or more characters with  or " in t:
										return [self.digit(a), "more", "Trait", f"{self.trait(a)}_{self.trait(a, 1)}", "at", "do", ["pay", "may", "do", [self.digit(a, 1), "waitinger", "Opp", "Antilvl"]]]
							elif "choose   character in your waiting room" in t:
								if "return it to your hand" in t:
									return ["pay", "may", "at", "do", [self.digit(a), "salvage", f"Trait_{self.trait(a)}"]]
							elif "choose   in your waiting room" in t and "\" in your waiting" in aa:
								if "send it to memory" in t:
									return ["pay", "may", "at", "do", [self.digit(a), "salvage", f"Name=_{self.name(a, s='n')}", "Memory"]]
							elif "choose up to  cards in your opponent's waiting room" in t:
								if "return them to your opponent's deck" in t:
									return ["pay", "may", "at", "do", [self.digit(a), "salvage", "", "Library", "upto", "opp", "show"]]
							elif "draw  card" in t:
								if "if you have a  character" in t:
									return [1, "more", "Trait", self.trait(a), "at", "do", ["pay", "may", "do", ["draw", self.digit(a)]]]
						elif "choose  of your characters in battle" in t or "choose  of your battling characters" in t:
							if "that character gets +x power" in t:
								if "x =  multiplied by the number of characters you have with  or " in t and " in its card name" in t:
									return [self.digit(a), self.digit(a, 1), x, "X", "xName", f"{self.name(a, 3)}_{self.name(a, 5)}", "Battle", "x", self.digit(a, 1), "at", "power"]
								elif "x =  multiplied by your level" in t:
									if "if the number of  characters you have is  or more" in t:
										return [self.digit(a), "more", "Trait", self.trait(a), "at", "do", [self.digit(a, 1), self.digit(a, 2), x, "X", "xplevel", "Battle", "x", self.digit(a, 2), "power"]]
							elif "that character gets + power" in t:
								if "if  is in your memory" in t:
									return ["name", self.name(a, s='n'), "Memory", "at", "do", [self.digit(a), self.digit(a, 1), x, "Battle", "power"]]
								elif "if there are  or more cards in your memory" in t:
									return [self.digit(a), "more", "Memory", "at", "do", [self.digit(a, 1), self.digit(a, 2), x, "Battle", "power"]]
								elif "if you have  or more  character" in t:
									return [self.digit(a), "more", "Trait", self.trait(a), "at", "do", [self.digit(a, 1), self.digit(a, 2), x, "Battle", "power"]]
								elif "if you have a character with  in name" in t:
									return ["name", self.name(a, s='n'), "at", "do", [self.digit(a), self.digit(a, 1), x, "Battle", "power"]]
						elif "choose  of your characters with  or  in the name" in t:
							if "that character gets + power" in t:
								return [self.digit(a),self.digit(a,1),x,"power","Name",f"{self.name(a,s='n')}_{self.name(a,2,s='n')}"]
						elif "choose  of your  characters" in t:
							if "that character gets + power" in t:
								return [self.digit(a), self.digit(a, 1), x, "power", "Trait", self.trait(a)]
						elif "put the top  cards of every player's deck in the waiting room" in t:
							if "if you have another character with  in the name" in t:
								return [1,"more","Name",self.name(a,s='n'),"other","do",["mill", self.digit(a), "top","do",["mill", self.digit(a), "top", "opp"]]]
						elif "put the top  cards of your opponent's deck in the waiting room" in t:
							return ["mill", self.digit(a), "top", "opp"]
						elif "put the top  cards of your deck in the waiting room" in t:
							return ["mill", self.digit(a), "top"]
						elif "reveal the top card of your deck" in t:
							if "if it is a  character" in t:
								if "put it in your hand" in t:
									if "discard  card from your hand" in t:
										return [-9, "reveal", "Trait", self.trait(a), "played", "do", ["draw", 1, "do", ["discard", self.digit(a), ""]]]
						elif "all your  characters" in t:
							if "characters gets " in t and "characters gets «" in aa:
								return [-1, self.trait(a, 1), x, "Trait", self.trait(a), "trait"]
				elif "when you use a backup" in t:
					if r[0] != r[1] and r[0][-1] == r[1][-1] and r[1] == act:
						if "choose  of your battling characters" in t:
							if "that character gets + power" in t:
								if "this ability activates up to once per turn" in t:
									return [self.digit(a), self.digit(a, 1), x, "power", "a1", "Battle"]
		elif "Damage" in p:
			if "when the damage dealt by this is cancelled" in t or "when the damage dealt by this becomes canceled" in t or "when damage dealt by this is canceled" in t:
				if r[0] == r[1] and n in r[1][-1] and cnc[0] not in r[0][-1] and cnc[1]:
					if "during the turn that this is placed on stage from your hand" in t or "during the turn this is placed from hand to the stage" in t:
						if z[0] == z[1] and "Hand" in pos[0] and any(field in pos[1] for field in self.stage):
							if "you may deal  damage to your opponent" in t:
								if "this ability activates up to  time per turn" in t:
									return ["pay", "may", f"a{self.digit(a)}", "do", ["damage", self.digit(a, 1), "at", "opp"]]
							elif "put the top card of your deck in the waiting room" in t:
								if "deal x damage to your opponent" in t:
									if "x =  + level of that card" in t:
										if "this ability activates up to once per turn" in t:
											return ["mill", self.digit(a), "top", "extra", "if", "a1", "do", ["damage", -(36 + self.digit(a)), "opp"]]
					elif "you may put this in your stock" in t:
						return [0, "stocker", "may", "at"]
					elif "you may pay the cost" in t:
						if "choose  character in your waiting room" in t:
							if "return it to your hand" in t:
								if "discard  card from your hand to the waiting room" in t:
									return ["pay", "may", "at", "do", [self.digit(a), "salvage", "Character", "show", "do", ["discard", self.digit(a), ""]]]
					elif "deal  damage to your opponent" in t:
						return ["damage", self.digit(a), "at", "opp"]
		elif "Battle" in p:
			if ("when this's battle opponent becomes reverse" in t and "\"[auto] when this's battle" not in aa) or ("when the battle opponent of this becomes reverse" in t and "\"[auto] when the battle opponent" not in aa) or ("when this character's battle opponent becomes reverse" in t and "\"[auto] when this character's battle opponent" not in aa):
				if r[0] != r[1] and r[0][-1] != r[1][-1] and v[1] == "Reverse" and r[0] in baind and r[1] in baind:
					if f"\"{cx[0].lower()}\" is in the climax area" in aa or f'card named \"{cx[0].lower()}\" is in your climax area' in aa or f' if \"{cx[0].lower()}\" is in your climax area' in aa:
						if n in cx[1][-1] and r[0][-1] == cx[1][-1]:
							if "you have  or more other  characters" in t:
								if "draw up to  cards" in t:
									if "discard  card from your hand to the waiting room" in t:
										return [self.digit(a), "more", f"Trait", self.trait(a), "other", "at", "cxcombo", "do", ["drawupto", self.digit(a, 1), "do", ["discard", self.digit(a, 2), ""]]]
							elif "search your deck for up to   character, reveal it, put it in your hand, and shuffle your deck" in t:
								return [self.digit(a), "search", f"Trait_{self.trait(a)}", "at", "upto", "cxcombo", "show"]
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
								return ["pay", "may", "at", "do", [-3, "clocker", "target", r[1]]]
							elif "choose up to  " in t and "in your waiting room" in t:
								if "return it to your hand" in t:
									if "reveal the top card of your deck" in t:
										if "if it's a  character, put it in your hand" in t:
											return [self.digit(a), "salvage", f"Name=_{self.name(a, -1, s='n')}", "upto", "at", "cxcombo", "do", [-9, "reveal", "Trait", self.trait(a), "do", ["draw", 1]]]
							elif "put up to  cards from top of your deck in your stock" in t:
								return ["drawupto", self.digit(a), "Stock"]
							elif "this gets the following ability" in t:
								return [0, self.name(a, s='a'), x, "give"]
					elif "you may pay the cost" in t:
						if "draw  card" in t:
							return ["pay", "may", "at", "do", ["draw", self.digit(a)]]
						elif "return all cards in your opponent's waiting room in your opponent's deck, and your opponent shuffles his or her deck" in t:
							return ["pay", "may", "at", "do", [-1, "shuffle", "opp"]]
						elif "choose   character or character with  in its card name from your waiting room" in t:
							if "return it to your hand" in t:
								return ["pay", "may", "at", "do", [self.digit(a), "salvage", f"TraitN_{self.trait(a)}_{self.name(a, s='ability')}", "or", "show"]]
						elif "choose   character in your waiting room" in t:
							if "return it to your hand" in t:
								return ["pay", "may", "at", "do", [self.digit(a), "salvage", f"Trait_{self.trait(a)}", "show"]]
						elif "choose  card in your opponent's waiting room" in t:
							if "put it on top of the deck" in t:
								return ["pay", "may", "at", "do", [self.digit(a), "salvage", "", "Library", "top", "opp", "show"]]
						elif "choose  level  or lower character in your opponent's center stage" in t:
							if "put it on the top of your opponent's deck" in t:
								if "during your turn" in t:
									if n in r[0][-1]:
										return ["pay", "may", "at", "do", [self.digit(a), "decker", "top", "Opp", "Level", f"<={self.digit(a, 1)}", "Center"]]
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
					elif "you may draw  card" in t:
						return ["pay", "may", "at", "do", ["draw", self.digit(a)]]
					elif "you may put it on top of the deck" in t or "you may put that character on the top of your opponent's deck" in t:
						return ["pay", "may", "at", "do", [-3, "decker", "top", "target", r[1]]]
					elif "you may put that character" in t:
						if "on the bottom of your opponent's deck" in t:
							if "if  is in your memory" in t:
								return [1, "more", "Name=", self.name(a, s='n'), "Memory", "do", ["pay", "may", "at", "do", [-3, "decker", "bottom", "target", r[1]]]]
							else:
								return ["pay", "may", "at", "do", [-3, "decker", "bottom", "target", r[1]]]
						elif "character in stock" in t:
							if r[0] == baind[0]:
								return ["pay", "may", "at", "do", [-3, "stocker", "target", baind[1]]]
							elif r[0] == baind[1]:
								return ["pay", "may", "at", "do", [-3, "stocker", "target", baind[0]]]
						elif " in your opponent's memory" in t:
							if r[0] == baind[0]:
								return ["pay", "may", "at", "do", [-3, "memorier", "target", baind[1]]]
							elif r[0] == baind[1]:
								return ["pay", "may", "at", "do", [-3, "memorier", "target", baind[0]]]
					elif "you may choose  character in your waiting room" in t:
						if "return it to your hand" in t:
							if "if the number of other characters you have is  or less" in t:
								if "choose  card in your hand" in t:
									if "put it in your waiting room" in t:
										return [self.digit(a), "more", "other", "lower", "at", "do", ["pay", "may", "do", [self.digit(a, 1), "salvage", "Character", "upto", "show", "if", self.digit(a, 1), "do", ["discard", self.digit(a, 2), ""]]]]
							elif "choose  card in your hand" in t:
								if "put it in your waiting room" in t:
									return ["pay", "may", "at", "do", [self.digit(a), "salvage", "Character", "upto", "show", "if", self.digit(a), "do", ["discard", self.digit(a, 1), ""]]]
							else:
								return ["pay", "may", "at", "do", [self.digit(a), "salvage", "Character", "upto", "show"]]
					elif "you may look at the top card of your deck" in t:
						if "put that card face-down under this as marker" in t:
							return ["pay", "may", "at", "do", [1, "looktop", "check", "do", [1, "marker", "top"]]]
					elif "you may put the top card of your deck" in t:
						if "in your stock" in t:
							return ["pay", "may", "at", "do", ["stock", 1]]
						elif "under this as marker" in t:
							return ["pay", "may", "at", "do", [1, "marker", "top"]]
					elif "you may put that character on the bottom of your opponent's deck" in t:
						return ["pay", "may", "at", "do", [-3, "decker", "bottom", "target", r[1]]]
					elif "you may send this to memory" in t or "you may put this in your memory" in t:
						if "at the start of your next" in t or "at the beginning of your next" in t:
							return ["pay", "may", "at", "do", [0, "memorier", "if", 1, "do", [-21, self.name(a, s='at'), 3, "give"]]]
					elif "you may put the top card of your clock in your waiting room" in t:
						return ["pay", "may", "at", "do", ["heal", 1, "top"]]
					elif "during the turn this is placed from hand to the stage" in t and z[0] == z[1]:
						if "if so, stand this" in t:
							return [0, "stand", "may", "played"]
					elif "look at the top card of your deck" in t:
						if "put it face-down under this as marker" in t:
							return [1, "looktop", "check", "at", "do", [0, "marker", "top"]]
					elif "look at the top card of your opponent's deck" in t:
						if "put it either on top or bottom of the deck" in t:
							return [1, "looktop", "top", "bottom", "at", "opp"]
					elif "look at up to  cards from top of your deck" in t:
						if "search for up to   character" in t and "reveal it, put it in your hand" in t:
							return [self.digit(a), "looktop", "top", "hand", self.digit(a, 1), f"Trait_{self.trait(a)}", "show", "upto"]
					elif "put up to x cards from top of your deck in your stock" in t:
						if "x = level of that character" in t:
							return ["drawupto", lvop[1], "Stock"]
					elif "put that character in stock" in t:
						if r[0] == baind[0]:
							return [-3, "stocker", "target", baind[1]]
						elif r[0] == baind[1]:
							return [-3, "stocker", "target", baind[0]]
					elif "choose up to  of opponent's characters" in t:
						if "that character gets - power" in t:
							if "send this to memory" in t:
								return [self.digit(a), self.digit(a, 1), x, "power", "Opp", "upto", "at", "do", [0, "[AUTO] At the end of the turn, put this card into your memory.", -3, "AUTO", "give"]]
					elif "choose  of your other characters" in t:
						if "rest it" in t:
							if "move it to an open position of your back stage" in t:
								return [self.digit(a), "rest", "Other", "at", "extra", "do", [-16, "move", "Open", "Back"]]
					elif "draw  card" in t:
						if "discard  card from your hand to the waiting room" in t:
							return ["draw", self.digit(a), "do", ["discard", self.digit(a), ""]]
						else:
							return ["draw", self.digit(a)]
			elif "when the battle opponent of your other" in t and "becomes reverse" in t:
				if "other character becomes reverse" in t:
					if r[0] != r[1] and r[0][-1] != r[1][-1] and v[1] == "Reverse" and r[0] not in baind and r[1] in baind:
						if "choose  of your characters" in t:
							if "gets + power" in t:
								return [self.digit(a), self.digit(a, 1), x, "power"]
						elif "this gets + power" in t:
							return [0, self.digit(a), x, "power"]
				elif ("other  becomes reverse" in t or "other character with  in name becomes reverse" in t) and ("\" becomes reverse" in aa or "\" in name becomes reverse" in aa):
					if r[0] != r[1] and r[0][-1] != r[1][-1] and v[1] == "Reverse" and r[0] not in baind and ((r[1] in baind[1] and self.name(a, s='n') in nmop[0]) or (r[1] in baind[0] and self.name(a, s='n') in nmop[1])):
						if "you may put the top card of your deck under this as marker" in t:
							return ["pay", "may", "do", [1, "marker", "top"]]
						elif "you may draw  card" in t:
							if "discard  card from hand to the waiting room" in t:
								return ["drawupto", self.digit(a), "if", self.digit(a), "do", ["discard", self.digit(a, 1), ""]]
			elif "when this's level  or higher battle opponent becomes reverse" in t or "when a level  or higher battle opponent of this becomes reverse" in t or "when a level  or higher battle opponent of this becomes reverse" in t:
				if r[0] != r[1] and r[0][-1] != r[1][-1] and v[1] == "Reverse" and r[0] in baind and r[1] in baind and ((r[0] == baind[0] and lvop[1] >= self.digit(a)) or (r[0] == baind[1] and lvop[0] >= self.digit(a))):
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
					elif "choose  of your opponent's characters" in t:
						if "that character gets - power" in t:
							return [self.digit(a, 1), self.digit(a, 2), x, "power", "at", "Opp"]
			elif "when a level  or higher battle opponent of another character of yours becomes reverse" in t:
				if r[0] != r[1] and r[0][-1] != r[1][-1] and v[1] == "Reverse" and r[1] in baind and r[0] in baind and ((r[1] == baind[1] and lvop[1] >= self.digit(a)) or (r[1] == baind[0] and lvop[0] >= self.digit(a))):
					if "you may pay the cost" in t:
						if "put that character in your clock" in t:
							return ["pay","may","at","do",[-3, "clocker","target",r[1]]]
			elif "when another of your characters becomes reverse" in t or "when your other character becomes reverse" in t:
				if "in battle" in t:
					if r[0] != r[1] and r[0][-1] == r[1][-1] and v[1] == "Reverse" and r[1] in baind and r[0] not in baind:  # and batt:
						if "you may pay the cost" in t:
							if "if this is in the back stage" in t:
								if "Back" in pos[1]:
									if "return that character to your hand" in t:
										return ["pay", "may", "do", [-7, "return", [r[1], "Hand"]]]
							if "choose  of your characters" in t:
								if "that character gets + power" in t:
									return ["pay", "may", "do", [self.digit(a), self.digit(a, 1), x, "power"]]
						elif "choose  of your " in t and "of your \"" in aa:
							if "that character gets + power" in t:
								return [self.digit(a), self.digit(a, 1), x, "power", "Name=", self.name(a, s='n')]
						elif "choose  of your character" in t:
							if "that character gets + power" in t:
								return [self.digit(a), self.digit(a, 1), x, "power"]
						elif "this gets + power" in t:
							if "if the sum of levels of cards in your level zone is  or higher" in t:
								return ["experience", self.digit(a), "do", [0, self.digit(a, 1), x, "power"]]
							else:
								return [0, self.digit(a), x, "power"]
			elif "when another of your  characters becomes reverse in battle" in t or "when another of your  character becomes reverse in battle" in t:
				if r[0] != r[1] and r[0][-1] == r[1][-1] and v[1] == "Reverse" and r[1] in baind and r[0] not in baind and self.trait(a) in tr[1]:
					if "choose  of your characters" in t:
						if "that character gets + power" in t:
							return [self.digit(a), self.digit(a, 1), x, "power"]
			elif "when this becomes reverse in battle" in t or "when this becomes reverse while battling" in t:
				if r[0] == r[1] and v[1] == "Reverse" and r[0] in baind:  # and batt:
					if "your opponent may " in t:
						if "put the top card of your opponent's deck into his or her stock" in t:
							return ["pay", "may", "opp", "oppmay", "at", "do", ["stock", 1]]
						elif "draw  card" in t:
							return ["pay", "may", "opp", "oppmay", "at", "do", ["draw", 1]]
					elif "you may choose  of your  characters" in t:
						return ["pay", "may", "at", "do", [self.digit(a), self.digit(a, 1), x, "power", "Trait", self.trait(a), "may"]]
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
						if "choose  character in your waiting room with  or " in t:
							if "return it to your hand" in t:
								return ["pay", "may", "at", "do", [self.digit(a), "salvage", f"Trait_{self.trait(a)}_{self.trait(a, 1)}"]]
						elif "choose  card in your opponent's waiting room" in t:
							if "put that character on top of your opponent's deck" in t or "put it on top of the deck" in t or "put it on top of your opponent's deck" in t:
								return ["pay", "may", "at", "do", [self.digit(a), "salvage", "", "Library", "top", "opp"]]
							elif "return it to your opponent's deck" in t:
								return ["pay","may","at","do",[self.digit(a),"salvage","","Library","opp"]]
						elif "choose   character in your waiting room" in t:
							if "return it to your hand" in t:
								return ["pay", "may", "at", "do", [self.digit(a), "salvage", f"Trait_{self.trait(a)}", "show"]]
						elif "choose   character in your clock" in t:
							if "return it to your hand" in t:
								if "put  card from your hand to the clock" in t:
									return ["pay", "may", "at", "do", [self.digit(a), "csalvage", f"Trait_{self.trait(a)}","show" ,"do", ["discard", self.digit(a, 1), "", "Clock"]]]
						elif "search your deck for  character with  or " in t:
							if "reveal it" in t and "put it in your hand" in t:
								if "rest this" in t:
									return ["pay", "may", "at", "do", [self.digit(a), "search", f"Trait_{self.trait(a)}_{self.trait(a, 1)}", "show", "do", [0, "rest"]]]
						elif "search your deck for up to   character" in t:
							if "reveal it" in t and "put it in your hand" in t:
								return ["pay", "may", "at", "do", [self.digit(a), "search", f"Trait_{self.trait(a)}", "show", "upto"]]
						elif "put this in your memory" in t or "send this to memory" in t:
							return ["pay", "may", "at", "do", [0, "memorier"]]
						elif "rest this" in t:
							if "reverse the battle opponent of this" in t:
								if r[0] == baind[0]:
									bopp = baind[1]
								elif r[0] == baind[1]:
									bopp = baind[0]
								return ["pay", "may", "at", "do", [0, "rest", "do", [-3, "reverser", "target", bopp]]]
							else:
								return ["pay", "may", "at", "do", [0, "rest"]]
					elif "put this on the bottom of your deck" in t:
						return [0, "decker", "bottom", "at"]
					elif "put this in clock" in t:
						if "if you have  or fewer other  characters" in t:
							return [self.digit(a), "more", "Trait", self.trait(a), "other", "lower", "at", "do", [0, "clocker"]]
						else:
							return [0, "clocker", "at"]
					elif "reveal the top card of your deck" in t:
						if "if it's level  or higher" in t or "if that card is level  or higher" in t:
							if "you may return this to your hand" in t:
								return [-9, "reveal", "Level", self.digit(a), "at", "do", ["pay", "may", "do", [0, "hander"]]]
							elif "you may rest this" in t:
								if "this ability activates up to once per turn" in t:
									return [-9, "reveal", "Level", self.digit(a), "a1", "do", ["pay", "may", "do", [0, "rest"]]]
								else:
									return [-9, "reveal", "Level", self.digit(a), "at", "do", ["pay", "may", "do", [0, "rest"]]]
							elif "you may put this in your stock" in t:
								return [-9, "reveal", "Level", self.digit(a), "at", "do", ["pay", "may", "do", [0, "stocker"]]]
						elif "if the revealed card is a  character" in t or "if that's a  character" in t:
							if "you may put this in your memory" in t:
								return [-9, "reveal", "Trait", self.trait(a), "at", "do", ["pay", "may", "do", [0, "memorier"]]]
					elif "choose  of your  character" in t:
						if "that character gets + power" in t:
							if "» character" in aa:
								return [self.digit(a), self.digit(a, 1), x, "power", "Trait", self.trait(a), "at"]
					elif "choose  of your character" in t:
						if "that character gets + power and " in t and "power and «" in aa:
							return [self.digit(a), self.digit(a, 1), x, "power", "at","extra","do",[-16,self.trait(a),x,"trait"]]
						elif "that character gets + power" in t:
							return [self.digit(a), self.digit(a, 1), x, "power", "at"]
					elif "level of its battle opponent is  or lower" in t or "this's battle opponent is level  or lower" in t or "level of the battle opponent of this is  or lower" in t:
						if (r[0] == baind[0] and lvop[1] <= self.digit(a)) or (r[0] == baind[1] and lvop[0] <= self.digit(a)):
							if r[0] == baind[0]:
								bopp = baind[1]
							elif r[0] == baind[1]:
								bopp = baind[0]
							if "you may reverse that character" in t:
								return ["pay", "may", "at", "do", [-3, "reverser", "target", bopp]]
							elif "you may put that character on the bottom of the deck" in t:
								return ["pay", "may", "at", "do", [-3, "decker", "bottom", "target", bopp]]
					elif "you cannot use  for the turn" in t and "\"[auto] encore\"" in aa:
						return [-21, "[CONT] You cannot use \"[AUTO] Encore\" until end of turn.", x, "give"]
					elif "put the top card of your deck in your clock" in t:
						return ["damageref", 1]
					elif "deals  damage to you" in t:
						return ["damage", self.digit(a), "at"]
			elif "when this becomes reversed" in t or "when this becomes reverse" in t:
				if r[0] == r[1] and v[1] == "Reverse":  # and r[0] in baind:
					if "you may reverse that character" in t or ("you may pay the cost" in t and "reverse that character" in t):
						if r[0] == baind[0]:
							bopp = baind[1]
						elif r[0] == baind[1]:
							bopp = baind[0]
						if "level of its battle opponent is  or lower" in t or "this's battle opponent is level  or lower" in t or "level of the battle opponent of this is  or lower" in t:
							if (r[0] == baind[0] and lvop[1] <= self.digit(a)) or (r[0] == baind[1] and lvop[0] <= self.digit(a)):
								return ["pay", "may", "at", "do", [-3, "reverser", "target", bopp]]
						elif "level of its battle opponent is same or lower than this" in t or "level of this's battle opponent is lower than or equal to the level of this" in t or "level of its battle opponent = or lower than the level of this" in t or "level of its battle opponent is lower than or equal to the level of this" in t:
							if (r[0] == baind[0] and lvop[1] <= lvop[0]) or (r[0] == baind[1] and lvop[0] <= lvop[1]):
								return ["pay", "may", "at", "do", [-3, "reverser", "target", bopp]]
						elif "if the level of the battle opponent of this is higher than the level of your opponent" in t:
							return ["plevel", "antilvl", bopp, "opp", "do", ["pay", "may", "at", "do", [-3, "reverser", "target", bopp]]]
					elif "if the level of the battle opponent of this is higher than the level of your opponent" in t:
						if r[0] == baind[0]:
							bopp = baind[1]
						elif r[0] == baind[1]:
							bopp = baind[0]
						if "you may put that character on the bottom of the deck" in t:
							return ["plevel", "antilvl", bopp, "opp", "do", ["pay", "may", "at", "do", [-3, "decker", "bottom", "target", bopp]]]
						elif "you may put the top card of your opponent's clock in the waiting room" in t:
							if "put that character in clock" in t:
								return ["plevel", "antilvl", bopp, "opp", "do", ["pay", "may", "at", "do", ["cdiscard", -17, "opp", "if", 1, "do", [-3, "clocker", "target", bopp]]]]
					elif "you may choose  of your  characters" in t:
						if "that card gets + power" in t:
							return [self.digit(a), self.digit(a, 1), x, "Trait", self.trait(a), "power", "at"]
		elif "Encore" in p:
			if pp < 0:
				if "at the beginning of the encore step" in t or "at the start of encore step" in t:
					if "if there are no other rested characters in your center stage" in t or "if you have no other rested characters in your center stage" in t:
						if "you may pay the cost" in t:
							if "rest this" in t:
								return [0, "Rest", "Center", "other", "a1", "do", ["pay", "may", "do", [0, "rest"]]]
					elif "if those characters are on stage" in t:
						if "return them to your deck" in t:
							return [-20, "decker", "a1"]
					elif "return this to your deck" in t:
						return [0, "decker", "a1"]
					elif "you may return this in your hand" in t:
						return ["pay", "may", "a1", "do", [0, "hander"]]
				elif "at the start of your encore step" in t or "at the beginning of your encore step" in t:
					if n in r[0][-1]:
						if "\" is in the climax area" in aa or "\" is in your climax area" in aa or "\" on your climax area" in aa:
							if (f"\"{cx[0].lower()}\" is in the climax area" in aa or f'\"{cx[0].lower()}\" is in your climax area' in aa or f'\"{cx[0].lower()}\" on your climax area' in aa) and r[0][-1] == cx[1][-1] and n in cx[1][-1]:
								if "you may put this in your memory" in t:
									if "at the beginning of your next" in t:
										return ["pay", "may", "a1", "do", [0, "memorier", "if", 1, "do", [-21, self.name(a, s='at'), 3, "give"]]]
						elif "you may pay the cost" in t:
							if "you have no other rested characters in your center stage" in t:
								if "rest this" in t:
									return [0, "Rest", "Center", "other", "a1", "do", ["pay", "may", "do", [0, "rest"]]]
							elif "choose  of your characters and this" in t:
								if "put them in your memory" in t:
									if "at the beginning of your next" in t:
										return ["pay", "may", "a1", "do", [self.digit(a), "memorier", "Other", "this", "extra", "do", [-21, self.name(a, s='at'), 3, "give", "expass", self.digit(a) + 1, "ex_ID="]]]
							elif "choose   in your waiting room" in t or "choose  card named  in your waiting room" in t:
								if "put it in the slot this was in" in t or "put it on the stage position that this was on" in t or "put it on the stage position this was on" in t:
									if "if this is rest" in t:
										if v[0] == "Rest":
											return ["pay", "may", "a1", "do", ["change", self.digit(a), f"Name=_{self.name(a, s='n')}"]]
									else:
										return ["pay", "may", "a1", "do", ["change", self.digit(a), f"Name=_{self.name(a, s='n')}"]]
						elif "put this in your waiting room" in t:
							return [0, "waitinger", "a1"]
		elif "End" in p:
			if pp > 0:
				if "at the end of the turn," in t:
					if "put this in your memory" in t:
						return [0, "memorier"]
					elif "put this in your waiting room" in t:
						return [0, "waitinger"]
					elif "put this in your clock" in t:
						return [0, "clocker"]
					elif "put this in your stock" in t:
						return [0, "stocker"]

		if self.ablt:
			return self.effect(a, t, aa, self.ablt)
		else:
			return []

	def effect(self, a, t="", aa="", pl=0):
		if aa == "":
			aa = self.a_replace(a)
		if t == "":
			t = self.text(a)

		e = []
		if "you may pay the cost" in t or "you may " in t:
			e = ["pay", "may"]

		m = []
		multi = False
		if "for each  you have" in t and "perform the following action" in t and "for each \"" in aa:
			if self.cx:
				mn = self.name(a,2, s='n')
			else:
				mn = self.name(a, s='n')
			m = ["multiple", "Name", mn]
			multi = True

		p = []
		if pl == 1:
			p = ["played"]
		elif pl == 2:
			p = ["at"]

		if "this ability activates up to once per turn" in t:
			p.append("a1")

		if multi:
			n = self.name(a,-1,s="n")
			ef = self.convert(n,self.text(n),self.a_replace(n))
		else:
			ef = self.convert(a,t,aa)

		if e and m:
			return e + p + ["do", m + ["do", ef]]
		elif e:
			return e + p + ["do", ef]
		else:
			if "do" in ef:
				if p:
					ef.insert(ef.index("do"), p[0])
				return e + ef
			else:
				return e + ef + p

	# 		return ["pay", "may", "cxbombo", "at", "do", [self.digit(a), "stocker", "Level", f"<={self.digit(a, 1)}", "Opp"]]

	def convert(self,a,t,aa):
		if "until the next end of your opponent's turn" in t or "until the end of your opponent's next turn" in t or "until end of your opponent's next turn" in t:
			x = 2
		elif "for the turn" in t or " until end of turn" in t:
			x = 1
		else:
			x = -1

		if "your opponent cannot use any act of characters on his or her stage" in t:
			return [-21,"[CONT] Your opponent cannot use any act of characters on his or her stage.",x,"give"]
		elif "put the top card of your deck under this as marker" in t:
			return [1, "marker", "top"]
		elif "put the top card of your deck in your clock" in t:
			return ["damageref",1]
		elif "put the top  cards of your deck in your waiting room" in t:
			if "if all cards put in the waiting room this way are  characters" in t or "if all those cards are  characters" in t:
				if "put the top card of your clock in your waiting room" in t:
					return ["mill", self.digit(a), "Trait", self.trait(a), "if", "all", "do", ["heal", 1, "top"]]
		elif "put all cards in your opponent's stock in the waiting room" in t:
			if "your opponent puts the same number of cards from top of the deck in the stock" in t:
				return ["distock", -1, "top", "opp", "count", "do", ["stock", "count", "opp"]]
		elif "choose  of your opponent's level  or lower characters" in t or "choose  level  or lower character in your opponent's" in t or "choose  of your opponent's characters whose level is  or lower" in t:
			if "put it in stock" in t:
				return [self.digit(a), "stocker", "Level", f"<={self.digit(a, 1)}", "Opp"]
			elif "put it in the waiting room" in t:
				return [self.digit(a),"waitinger","Level", f"<={self.digit(a, 1)}", "Opp"]
		elif "choose  opponent's character" in t or "choose  of your opponent's character" in t:
			if "return it to the hand" in t or "return it to your opponent's hand" in t:
				if "on the center stage" in t:
					if "this gets + power" in t:
						return [self.digit(a), "hander", "Opp", "Center", "do", [0, self.digit(a, 1), x, "power"]]
				else:
					return [self.digit(a),"hander","Opp"]
			elif "that character gets - power" in t:
				return [self.digit(a),self.digit(a,1),x,"power","Opp"]
		elif "choose  of your other characters with  in name" in t:
			if "that character gets + power" in t:
				return [self.digit(a),self.digit(a,1),x,"power","Name",self.name(a,s='n'),"Other"]
		elif "choose  character in your waiting room" in t:
			if "return it to your hand" in t:
				return [self.digit(a), "salvage", "Character", "show"]
		elif "search your deck for up to   or " in t:
			if "reveal it" in t and "put it in your hand" in t:
				return [self.digit(a),"search",f"Trait_{self.trait(a)}_{self.trait(a,1)}","show","upto"]
		elif "search your deck for up to  " in t:
			if "reveal it" in t and "put it in your hand" in t:
				return [self.digit(a), "search", f"Name=_{self.name(a, s='n')}", "upto", "show"]
		elif "search your deck for up to  character with  in the name" in t:
			if "put them in your hand" in t or "put it in your hand" in t:
				if "reveal it" in t or "reveal them" in t:
					return [self.digit(a), "search", f"Name_{self.name(a, s='n')}", "upto", "show"]
				else:
					return [self.digit(a), "search", f"Name_{self.name(a, s='n')}", "upto"]
		elif "all your characters get" in t:
			if "get + soul" in t:
				return [-1, self.digit(a), x, "soul"]
			elif "get + power" in t:
				return [-1, self.digit(a), x, "power"]
		elif "all your other characters get" in t:
			if "get + level" in t:
				return [-2, self.digit(a), x, "level"]
		elif "this gets + level and + power" in t:
			return [0, self.digit(a, 1), x, "power","do",[0, self.digit(a), x, "level"]]
		elif "this gets + power and" in t:
			if "and + soul" in t:
				return [0, self.digit(a), x, "power", "do", [0, self.digit(a, 1), x, "soul"]]
			elif "and the following ability" in t:
				return [0, self.digit(a), x, "power", "do", [0, self.name(a, s='a'), x, "give"]]
			elif "and your opponent cannot use" in t and "cannot use \"[auto] encore\"" in aa:
				return [0, self.digit(a), x, "power", "do", [-21, "[CONT] Your opponent cannot use \"[AUTO] Encore\" until end of turn.", x, "give"]]
			elif "your opponent cannot play event cards and \"backup\" from his or her hand" in t:
				return [0, self.digit(a), x, "power", "do", [-21, "[CONT] Your opponent cannot play event cards and \"Backup\" from his or her hand.", x, "give"]]
		elif "this gets the following ability" in t or ("this gets " in t and "this gets \"[" in aa):
			return [0, self.name(a, s='a'), x, "give"]
		elif "this gets + power" in t:
			if "for each different trait on your characters" in t:
				return [0, self.digit(a), x, "#", "power", "Traits"]
			else:
				return [0, self.digit(a), x, "power"]
		elif "this gets - power" in t:
			return [0, self.digit(a), x, "power"]
		elif "this gets + soul" in t:
			return [0, self.digit(a), x, "soul"]
		elif "this gets +x power" in t:
			if "x =  times # of climax cards in your waiting room" in t:
				if "all battling characters get the following ability" in t:
					return [0,self.digit(a,-1),x,"power","#","Climax","Waiting","do",[-25,self.name(a,s='a'),x,"give"]]
				else:
					return [0, self.digit(a, -1), x, "power", "#", "Climax", "Waiting"]
			elif "x =  times # of your characters with  or " in t:
				return [0, self.digit(a), x, "power", "#", "Trait", f"{self.trait(a)}_{self.trait(a, 1)}"]
			elif "x =  times # of your  characters" in t or "x =  multiplied by the number of  characters you have" in t:
				return [0, self.digit(a), x, "power", "#", "Trait", self.trait(a)]
			elif "x =  times # of your other  characters" in t:
				return [0, self.digit(a), x, "power", "#", "Trait", self.trait(a), "other"]
		elif "deal  damage to your opponent" in t:
			return ['damage', self.digit(a), 'opp']

		return []

	def cont(self, a=""):
		t = self.text(a)
		aa = self.a_replace(a)
		#
		# if "for the turn" in t or " until end of turn" in t:
		# 	x = 1
		# else:
		# 	x = -1

		if t.startswith("assist"):
			if "all your level  or higher characters in front" in t:
				if "get + soul" in t:
					return ["front", self.digit(a, 1), -1, "Assist", "soul", "flevel", self.digit(a)]
				elif "get + power" in t:
					return ["front", self.digit(a, 1), -1, "Assist", "power", "flevel", self.digit(a)]
			elif "all your level  or lower characters in front" in t:
				if "get + power" in t:
					return ["front", self.digit(a, 1), -1, "Assist", "power", "flevel", self.digit(a), "lower"]
			elif "x =  times level" in t or "x =  multiplied by that character's level" in t or "x = the level of that character" in t or "x =  times the level of that character" in t:
				if "all your  or  characters in front" in t:
					return ["front", self.digit(a), -1, "Assist", "Trait", f"{self.trait(a)}_{self.trait(a,1)}", "flevel", "x", self.digit(a), "power"]
				elif "all your  characters in front" in t:
					return ["front", self.digit(a), -1, "Assist", "Trait", self.trait(a), "flevel", "x", self.digit(a), "power"]
				else:
					return ["front", self.digit(a), -1, "Assist", "flevel", "x", self.digit(a), "power"]
			elif "x =  multiplied by the number of  characters in your level" in t:
				return ["front", self.digit(a), -1, "Assist", "LevTrait", self.trait(a), "Level", "x", self.digit(a), "power"]
			elif "get + power and + soul" in t:
				if "all your  characters in front" in t:
					return ["front", self.digit(a), -1, "Assist", "Trait", self.trait(a), "power", "front", self.digit(a, 1), -1, "Assist", "Trait", self.trait(a), "soul"]
				else:
					return ["front", self.digit(a), -1, "Assist", "power", "front", self.digit(a, 1), -1, "Assist", "soul"]
			elif "get + level and + power" in t:
				if "all your  characters in front" in t:
					return ["front", self.digit(a, 1), -1, "Assist", "Trait", self.trait(a), "power", "front", self.digit(a), -1, "Assist", "Trait", self.trait(a), "level"]
			elif "get + level" in t:
				return ["front", self.digit(a), -1, "Assist", "level"]
			elif "get + power" in t:
				if self.name(a, s='n') in self.text_name:
					return ["front", self.digit(a), -1, "Assist", "Text", self.text_name[self.name(a, s='n')], "power"]
				elif "during your turn" in t:
					return ["front", self.digit(a), -1, "Assist", "power", "Turn"]
				else:
					return ["front", self.digit(a), -1, "Assist", "power"]
			elif "get + soul" in t:
				return ["front", self.digit(a), -1, "Assist", "soul"]
			elif "get \"" in t:
				return ["front", self.name(a, s="a"), -1, "Assist", "ability"]
		elif t.startswith("alarm"):
			if "you're level  or higher" in t or "your level is  or higher" in t:
				if 'all your  characters' in t:
					if "characters get " in t and "get \"[" in aa:
						return [-1, self.name(a, s='a'), -1, "Alarm", "plevel", self.digit(a), "Colour", self.trait(a), "ability"]
				elif "all your characters with  " in t:
					if "get the following ability" in t:
						if self.name(a, s='n') in self.text_name:
							return [-1, self.name(a, -1, s='a'), -1, "Alarm", "plevel", self.digit(a), "Text", self.text_name[self.name(a, s='n')], "ability"]
			elif "all your characters with no traits" in t:
				if "get the following ability" in t:
					return [-1, self.name(a, s='a'), -1, "Alarm", "Trait", "", "ability"]
			elif "all your level  or higher characters" in t:
				if "get + soul" in t:
					return [-1, self.digit(a, 1), -1, "Alarm", "LevelC", self.digit(a), "soul"]
				elif "get + power" in t:
					return [-1, self.digit(a, 1), -1, "Alarm", "LevelC", self.digit(a), "power"]
				elif "get " in t and "get \"" in aa:
					return [-1, self.name(a, s='n'), -1, "Alarm", "LevelC", self.digit(a), "ability"]
			elif "all your  or  characters" in t:
				if "characters get + power" in t:
					return [-1, self.digit(a), -1, "Alarm", "Trait", f"{self.trait(a)}_{self.trait(a, 1)}", "power"]
			elif "all your  characters" in t:
				if "characters get the following ability" in t or ("characters get " in t and "get \"[" in aa):
					return [-1, self.name(a, s='a'), -1, "Alarm", "Trait", self.trait(a), "ability"]
			elif "all your characters" in t:
				if ("characters get " in t and "get \"[" in aa) or "get the following ability" in t:
					return [-1, self.name(a, s='a'), -1, "Alarm", "ability"]
				elif "characters get + power" in t:
					return [-1, self.digit(a), -1, "Alarm", "power"]
		elif t.startswith("bodyguard") or t.startswith("great performance"):
			return [0, "", -1, "bodyguard"]
		elif t.startswith("experience"):
			if "if the total level of the cards in your level is  or higher" in t:
				if "your other character in the middle position of the center stage gets + power" in t:
					return [-5, self.digit(a, 1), -1, "Experience", self.digit(a), "power", "other", "fm"]
				elif "all your other characters get + power" in t:
					if "during your opponent's turn" in t:
						return [-2, self.digit(a, 1), -1, "Turn", "Topp", "Experience", self.digit(a), "power"]
					else:
						return [-2, self.digit(a, 1), -1, "Other", "Experience", self.digit(a), "power"]
				elif "all your other  characters get + power" in t:
					return [-2, self.digit(a, 1), -1, "Other", "Experience", self.digit(a), "Trait", self.trait(a), "power"]
				elif "all your other  characters get " in t and " get \"[" in aa:
					return [-2, self.name(a, s='a'), -1, "Other", "Experience", self.digit(a), "Trait", self.trait(a), "ability"]
				elif "this gets + power and the following ability" in t:
					return [0, self.digit(a, 1), -1, "Experience", self.digit(a), "power", 0, self.name(a, s='a'), -1, "Experience", self.digit(a), "ability"]
				elif "this gets the following ability" in t:
					return [0, self.name(a, s='a'), -1, "Experience", self.digit(a), "ability"]
				elif "this gets + power" in t:
					return [0, self.digit(a, 1), -1, "Experience", self.digit(a), "power"]
				elif "this gets +x power" in t:
					if "x =  multiplied by the level of the character opposite this" in t:
						return [0, self.digit(a, 1), -1, "X", "Experience", self.digit(a), "x", self.digit(a, 1), "xlevel", "opposite", "power"]
				elif "this gets + soul" in t:
					return [0, self.digit(a, 1), -1, "Experience", self.digit(a), "soul"]
				elif "this gets " in t and "this gets \"[" in aa:
					return [0, self.name(a, s='a'), -1, "Experience", self.digit(a), "ability"]
			elif "if a card named  is in your level" in t:
				if "this gets + power" in t:
					return [0, self.digit(a), -1, "Experience", self.digit(a), "Name=", self.name(a, s="a"), "power"]
				elif "this gets + soul" in t:
					return [0, self.digit(a), -1, "Experience", self.digit(a), "Name=", self.name(a, s="a"), "soul"]
		elif t.startswith("recollection") or t.startswith("memory"):
			if "if this is in memory" in t or "if this is in your memory" in t:
				if "all your  and  get + power" in t and "\" and \"" in aa:
					return [-1, self.digit(a), -1, "sMemory", "Name", f"{self.name(a, s='n')}_{self.name(a,2,s='n')}", "power"]
				elif "all your  characters get + power" in t:
					if "during your turn" in t:
						return [-1, self.digit(a), -1, "Turn", "sMemory", "Trait", self.trait(a), "power"]
					elif "during your opponent's turn" in t:
						return [-1, self.digit(a), -1, "Turn", "sMemory", "Topp", "Trait", self.trait(a), "power"]
				elif "all your characters with  in the name" in t:
					if "gets + power" in t or "get + power" in t:
						return [-1, self.digit(a), -1, "sMemory", "Name", self.name(a, s='n'), "power"]
			elif "if there are  or more characters in your memory with  or " in t:
				if "this gets + power" in t:
					return [0, self.digit(a, 1), -1, "More", self.digit(a), "Trait", f"{self.trait(a)}_{self.trait(a, 1)}", "Memory", "power"]
			elif "if there are  or more  in your memory" in t:
				if "this gets - level while in your hand" in t:
					return [0, self.digit(a, 1), -1, "More", self.digit(a), f"Name=_{self.name(a, s='n')}", "Memory", "pHand", "level"]
				elif "this gets + power and + soul" in t:
					return [0, self.digit(a, 1), -1, "More", self.digit(a), f"Name=_{self.name(a, s='n')}", "Memory", "power", 0, self.digit(a, 2), -1, "More", self.digit(a), f"Name=_{self.name(a, s='n')}", "Memory", "soul"]
			elif "if  is in your memory" in t or "if there is a  in your memory" in t:
				if "this gets + power and the following ability" in t:
					return [0, self.digit(a), -1, "More", 1, "Name=", self.name(a, s='n'), "Memory", "power", 0, self.name(a, s='a'), -1, "More", 1, "Name=", self.name(a, s='n'), "Memory", "ability"]
				elif "this gets + power" in t:
					return [0, self.digit(a), -1, "More", 1, "Name=", self.name(a, s='n'), "Memory", "power"]
			elif "if there are cards in your memory" in t:
				if "all your other characters get + power" in t:
					return [-2, self.digit(a), -1,"Other", "OMore", 1, "OMemory", "power"]
				elif "this gets " in t and "gets \"[" in aa:
					return [0,self.name(a,s='a'),-1,"More",1,"Memory","ability"]
			elif "if you have  card in your memory" in t:
				if "this gets + power" in t:
					if "during your turn" in t:
						return [0, self.digit(a, 1), -1, "More", self.digit(a), "Memory", "Turn", "power"]
					else:
						return [0, self.digit(a, 1), -1, "More", self.digit(a), "Memory", "power"]
			elif "number of cards in your memory is  or more" in t or "if there are  or more cards in your memory" in t:
				if "all your other characters get + power" in t:
					return [-2, self.digit(a, 1), -1,"Other", "OMore", self.digit(a), "OMemory", "power"]
				elif "this gets + power and the following ability" in t:
					return [0, self.digit(a, 1), -1, "More", self.digit(a), "Memory", "power", 0, self.name(a, s='a'), -1, "More", self.digit(a), "Memory", "ability"]
				elif "this gets + power and + soul" in t:
					return [0, self.digit(a, 1), -1, "More", self.digit(a), "Memory", "power", 0, self.digit(a,2), -1, "More", self.digit(a), "Memory", "soul"]
				elif "this gets - level and gets + power" in t:
					return [0, self.digit(a, 2), -1, "More", self.digit(a), "Memory", "power", 0, self.digit(a, 1), -1, "More", self.digit(a), "Memory", "level"]
				elif "this gets the following ability" in t or ("this gets " in t and "gets \"[" in aa):
					return [0, self.name(a, s='a'), -1, "More", self.digit(a), "Memory", "ability"]
				elif "this gets + power" in t:
					if "during your turn" in t:
						return [0, self.digit(a, 1), -1, "More", self.digit(a), "Memory", "Turn", "power"]
					elif "during your opponent's turn" in t:
						return [0, self.digit(a, 1), -1, "More", self.digit(a), "Memory", "Turn", "Topp", "power"]
					elif "for each other rested characters you have" in t:
						return [0, self.digit(a, 1), -1, "Each", "Rest", "OMore", self.digit(a), "OMemory", "power", "other"]
					else:
						return [0, self.digit(a, 1), -1, "More", self.digit(a), "Memory", "power"]
			elif "number of  characters in your memory is  or more" in t:
				if "this gets + power and the following ability" in t:
					return [0, self.digit(a, 1), -1, "More", self.digit(a), "Trait", self.trait(a), "Memory", "power", 0, self.name(a, s='a'), -1, "More", self.digit(a), "Trait", self.trait(a), "Memory", "ability"]
				elif "this gets + power" in t:
					return [0, self.digit(a, 1), -1, "More", self.digit(a), "Trait", self.trait(a), "Memory", "power"]
		elif "if this is on the stage" in t:
			if "this's card name will also be regarded as" in t:
				return [0, self.name(a, s='n'), -1, "Stage", "name"]
		elif "if this is in the middle position of the center stage" in t or "if this is in the middle position of your center stage" in t:
			if "this gets + power and the following ability" in t:
				return [0, self.digit(a), -1, "Middle", "power", 0, self.name(a, s='a'), -1, "Middle", "ability"]
			elif "this gets + power" in t:
				return [0, self.digit(a), -1, "Middle", "power"]
		elif "this gets - level while in your hand" in t or "this gets - level in your hand" in t:
			if "if you have  or more  characters" in t:
				return [0, self.digit(a, 1), -1, "More", self.digit(a), "Trait", self.trait(a), "pHand", "level"]
			elif "if there are  or fewer climax cards in your waiting room" in t:
				return [0, self.digit(a, 1), -1, "ClimaxWR", self.digit(a), "level", "pHand", "lower"]
			elif "f the number of climax cards in your waiting room is  or more" in t:
				return [0, self.digit(a, 1), -1, "ClimaxWR", self.digit(a), "level", "pHand"]
			elif "if the number of cards named  in your waiting room is  or more" in t:
				return [0, self.digit(a, 1), -1, "NameWR", self.digit(a), "Name=", self.name(a, s="a"), "level", "pHand"]
			elif "if a card named  is in your clock" in t:
				return [0, self.digit(a, 1), -1, "NameCL", self.digit(a), "Name=", self.name(a, s="a"), "pHand", "level"]
			elif "if there are  or more  in your memory" in t:
				return [0, self.digit(a, 1), -1, "More", self.digit(a), f"Name=_{self.name(a, s='n')}", "Memory", "pHand", "level"]
			elif "if there are  or fewer cards in your deck" in t:
				return [0, self.digit(a, 1), -1, "Deck", self.digit(a), "lower", "pHand", "level"]
		elif "if there are  or more markers under this" in t:
			if "this card cannot be chosen by your opponent's effects" in t:
				if "if there are  or more markers under this" in t:
					if "this gets + power" in t:
						if "if there are  or more markers under this" in t:
							if "all your other characters get + power" in t:
								return ["marker#", [[0, "[CONT] This card cannot be chosen by your opponent's effects.", -3, "Marker#", self.digit(a), "ability"], [0, self.digit(a, 2), -1, "Marker#", self.digit(a, 1), "power"], [-2, self.digit(a, 4), -1, "Other", "Marker#", self.digit(a, 3), "power"]]]
		elif "if there are markers under this" in t or "if there is a marker under this" in t:
			if "this gets + power" in t:
				return [0, self.digit(a), -1, "Marker#", 1, "power"]
		elif "if there are  or fewer cards" in t:
			if "this gets + level and + power" in t:
				if "in your stock" in t:
					return [0, self.digit(a, 2), -1, "Stock", self.digit(a), "lower", "power", 0, self.digit(a, 1), -1, "Stock", self.digit(a), "lower", "level"]
			elif "this gets + power" in t:
				if "in your waiting room" in t:
					return [0, self.digit(a, 1), -1, "More", self.digit(a), "Waiting", "lower", "power"]
				elif "in your hand" in t:
					return [0, self.digit(a, 1), -1, "Hand", self.digit(a), "lower", "power"]
				elif "in your stock" in t:
					return [0, self.digit(a, 1), -1, "Stock", self.digit(a), "lower", "power"]
		elif "if there are more cards in your hand than your opponent's hand" in t:
			if "this gets + power" in t:
				return [0, self.digit(a), -1, "Hand", "HandvsOpp", "power"]
		elif "if there's a climax card in your opponent's climax area" in t:
			if "this gets " in t and "gets \"[" in aa:
				return [0,self.name(a,s='a'),-1,"More",1,"Climax","CX","opp","ability"]
		elif "you can put any number of cards with the same card name as this in your deck" in t:
			return [50, "limit"]
		elif "during your turn" in t:
			if "all your other characters" in t:
				if "get + power" in t:
					if "whose level is  or lower" in t:
						return [-2, self.digit(a, 1), -1, "Turn", "power", "LevelC", self.digit(a), "lower"]
					else:
						return [-2, self.digit(a), -1, "Turn", "power"]
				elif "get +x power" in t:
					if "x =  times level of that character" in t:
						return [-2, self.digit(a), -1, "Turn", "xlevel", "x", self.digit(a), "power"]
				elif "get + level" in t:
					return [-2, self.digit(a), -1, "Turn", "level"]
			elif "all your other  characters" in t:
				if "get + power" in t:
					return [-2, self.digit(a), -1, "Turn", "Trait", self.trait(a), "power"]
			elif "this gets + level and + power" in t:
				if "this gets + level and + power" in t:
					return [0, self.digit(a, 2), -1, "More", self.digit(a), "Trait", self.trait(a), "Turn", "power", 0, self.digit(a, 1), -1, "More", self.digit(a), "Trait", self.trait(a), "Turn", "level"]
			elif "this gets + power" in t:
				if "for each of your other characters with " in t:
					if self.name(a, s='n') in self.text_name:
						return [0, self.digit(a), -1, "Each", "Text", self.text_name[self.name(a, s='n')], "power", "other", "Turn"]
				elif "for each of your other  characters" in t:
					return [0, self.digit(a), -1, "Each", "Trait", self.trait(a), "power", "other", "Turn"]
				elif "if  is in your memory" in t:
					return [0, self.digit(a), -1, "More", 1, "Name=", self.name(a, s='n'), "Memory", "Turn", "power"]
				else:
					return [0, self.digit(a), -1, "Turn", "power"]
		elif "during your opponent's turn" in t:
			if "this gets + power" in t:
				if "for each of your other  character" in t:
					return [0, self.digit(a), -1, "Each", "Trait", self.trait(a), "power", "other", "Turn", "Topp"]
				elif "if  is in your memory" in t:
					return [0, self.digit(a), -1, "More", 1, "Name=", self.name(a, s='n'), "Memory", "Turn", "Topp", "power"]
				else:
					return [0, self.digit(a), -1, "Turn", "Topp", "power"]
			elif "all your other  characters" in t:
				if "get + power" in t:
					return [-2, self.digit(a), -1, "Turn", "Topp", "Trait", self.trait(a), "power"]
			elif "all your other characters" in t:
				if "get + power" in t:
					return [-2, self.digit(a), -1, "Turn", "Topp", "power"]
				elif "get +x power" in t:
					if "x =  multiplied by that character's level" in t:
						return [-2, self.digit(a), -1, "Turn", "Topp", "xlevel", "x", self.digit(a), "power"]
				elif "get + level" in t:
					return [-2, self.digit(a), -1, "Turn", "Topp", "level"]
		elif "when this attacks, you may instead choose  character on your opponent's back stage, and have this frontal attack with the chosen character as the defending character" in t or "when this attacks, you may instead choose  character in opponent's back stage and have this front attack that character as the defending character" in t:
			return [1, "", -1, "backatk", "may"]
		elif "if the number of characters your opponent has is  or more" in t:
			if "this gets + power" in t:
				return [0, self.digit(a, 1), -1, "More", self.digit(a), "Character", "opp", "power"]
		elif "if there are  or more  in your waiting room" in t:
			if "this gets + power" in t:
				return [0, self.digit(a, 1), -1, "More", self.digit(a), "Name=", self.name(a, s='n'), "Waiting", "power"]
		elif "if there are  or more cards" in t or "if you have  or more cards" in t:
			if "all your other  characters get + power" in t:
				if " in your stock" in t:
					return [-2, self.digit(a, 1), -1, "Other", "Stock", self.digit(a), "Trait", self.trait(a), "power"]
			elif "this gets + power and " in t and "and \"[" in aa:
				if " in your stock" in t:
					return [0, self.digit(a, 1), -1, "Stock", self.digit(a), "power", 0, self.name(a, s='a'), -1, "Stock", self.digit(a), "ability"]
			elif "get the following ability" in t or ("gets \"[" in aa or "get \"[" in aa):
				if "\" in name" in aa or "\" in the name" in aa:
					if "if there are  or more cards in your memory" in t:
						if "and this gets \"" in aa:
							return [-32, self.name(a, s='a'), -1, "Other", "OMore", self.digit(a), "OMemory", f"Name", f"{self.name(a, s='n')}", "ability"]
			elif "this gets + power" in t:
				if " in your hand" in t:
					return [0, self.digit(a, 1), -1, "Hand", self.digit(a), "power"]
				elif " in your stock" in t:
					return [0, self.digit(a, 1), -1, "Stock", self.digit(a), "power"]
		elif "for each card in your clock" in t:
			if "this gets + power" in t:
				return [0, self.digit(a), -1, "Each", "Clock", "power"]
		elif "for each climax card in your waiting room" in t:
			if "this gets + power" in t:
				return [0, self.digit(a), -1, "Each", "Climax", "Waiting", "power"]
		elif "for each  in your waiting room" in t:
			if "this gets + power" in t:
				return [0, self.digit(a), -1, "Each", "Name=", self.name(a, s='n'), "Waiting", "power"]
		elif "for each of your other cards named " in t or ("for each other  you have" in t and "for each other \"" in aa):
			if "this gets + level and + power" in t:
				return [0, self.digit(a, 1), -1, "Each", "Name=", self.name(a, s="n"), "other", "power", 0, self.digit(a), -1, "Each", "Name=", self.name(a, s="n"), "other", "level"]
			elif "this gets + power" in t:
				if "and the character opposite this gets + soul" in t:
					return [0, self.digit(a), -1, "Each", "Name=", self.name(a, s='n'), "other", "power", -6, self.digit(a, 1), -1, "Opposite", "soul"]
				else:
					return [0, self.digit(a), -1, "Each", "Name=", self.name(a, s='n'), "other", "power"]
		elif "for each of your other  characters" in t or (("for each other  you have" in t or "for each other  character you have" in t) and "for each other «" in aa):
			if "this gets + power" in t:
				if "in the back stage" in t:
					return [0, self.digit(a), -1, "Each", "Trait", self.trait(a), "power", "other", "Back"]
				elif "in the center stage" in t:
					if "if there's a marker under this" in t:
						return [0, self.digit(a), -1, "Each", "Trait", self.trait(a), "power", "other", "Center", "markers"]
					else:
						return [0, self.digit(a), -1, "Each", "Trait", self.trait(a), "power", "other", "Center"]
				else:
					return [0, self.digit(a), -1, "Each", "Trait", self.trait(a), "power", "other"]
		elif "for each of your other" in t:
			if "this gets + power" in t:
				if "\" in the center stage" in aa:
					return [0, self.digit(a), -1, "Each", "Name=", self.name(a, s='n'), "other", "Center", "power"]
				elif "other rested characters" in t or "other rest characters" in t:
					return [0, self.digit(a), -1, "Each", "Rest", "power", "other"]
				elif "characters with  or " in t:
					return [0, self.digit(a), -1, "Each", "Trait", f"{self.trait(a)}_{self.trait(a, 1)}", "power", "other"]
				elif "level  or lower characters" in t:
					return [0, self.digit(a, 1), -1, "Each", "LevelC", self.digit(a), "lower", "power", "other"]
		elif "for each other rested character you have" in t:
			if "this gets + power" in t:
				return [0, self.digit(a), -1, "Each", "Rest", "other", "power"]
		elif "for each standing character your opponent has" in t:
			if "this gets + power" in t:
				return [0, self.digit(a), -1, "Each", "Stand", "opp","power"]
		elif "for each different trait on your characters" in t:
			if "this gets + power" in t:
				return [0, self.digit(a), -1, "Each", "Traits", "power"]
		elif "your other character in" in t:
			if "center stage center slot" in t or "middle position of your center stage" in t:
				if "gets + power and " in t and "power and \"[" in aa:
					return [-5, self.digit(a), -1, "Middle", "other", "power", -5, self.name(a, s="a"), -1, "Middle", "other", "ability"]
				elif 'gains "[' in aa or 'gets "[' in aa:
					return [-5, self.name(a, 1), -1, "Middle", "ability", "other"]
				elif "gets + power" in t:
					return [-5, self.digit(a), -1, "Middle", "other", "power"]
		elif "if the number of cards in your hand is  or more" in t or "if you have  or more cards in your hand" in t:
			if "this gets + power" in t:
				return [0, self.digit(a, 1), -1, "Hand", self.digit(a), "power"]
			elif "this gets " in t and "gets \"[" in aa:
				return [0, self.name(a, s='a'), -1, "Hand", self.digit(a), "ability"]
			elif "all your other characters get + power" in t:
				return [-2, self.digit(a, 1), -1, "Other", "Hand", self.digit(a), "power"]
		elif "if the number of cards in your stock is  or more" in t:
			if "this gets + power" in t:
				return [0, self.digit(a, 1), -1, "Stock", self.digit(a), "power"]
		elif "if you have  or more climax cards in your waiting room" in t:
			if "this gets + level and + power" in t:
				return [0, self.digit(a, 2), -1, "More", self.digit(a), "Climax", "Waiting", "power", 0, self.digit(a, 1), -1, "More", self.digit(a), "Climax", "Waiting", "level"]
		elif "if you have  or more other  character" in t:
			if "this gets + level and + power" in t:
				return [0, self.digit(a, 2), -1, "More", self.digit(a), "Trait", self.trait(a), "other", "power", 0, self.digit(a, 1), -1, "More", self.digit(a), "Trait", self.trait(a), "other", "level"]
			elif "this gets the following ability" in t:
				return [0, self.name(a, s='a'), -1, "More", self.digit(a), "Trait", self.trait(a), "other", "ability"]
			elif "this gets + power" in t:
				return [0, self.digit(a, 1), -1, "More", self.digit(a), "Trait", self.trait(a), "other", "power"]
		elif "if you have another character with  in name" in t or "if you have another character with  in the name" in t:
			if "this gets + power" in t:
				return [0, self.digit(a), -1, "More", 1, "Name", self.name(a, s="n"), "other", "power"]
			elif "this gets the following ability" in t:
				return [0, self.name(a, s='a'), -1, "More", 1, "Name", self.name(a, s="n"), "other", "ability"]
		elif "if you have another «" in aa:
			if "this gets +" in t:
				return [0, self.digit(a), -1, "More", 1, "Trait", self.trait(a), "other", "power"]
		elif "if you have another \"" in aa or ("if you have " in t and "if you have \"" in aa):
			if "character opposite this" in t:
				if "gets - soul" in t:
					if "get " in t and "get \"" in aa:
						if aa.count("\" and \"") == 3:
							return [-2, self.name(a, s='a'), -1, "Other", "OMore", 4, "Oother", "O&", "OName", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}_{self.name(a, 4, s='n')}_{self.name(a, 6, s='n')}", "ability", -6, self.digit(a), -1, "Opposite", "OMore", 4, "Oother", "O&", "OName", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}_{self.name(a, 4, s='n')}_{self.name(a, 6, s='n')}", "soul"]
			elif "this gets + power" in t:
				if "if you have another  and " in t and "\" and \"" in aa:
					return [0, self.digit(a), -1, "Another&", "Name", f"{self.name(a, s='n')}_{self.name(a, -1, s='n')}", "power"]
				else:
					return [0, self.digit(a), -1, "Another", "Name=", self.name(a, s="n"), "power"]
			elif "this gets " in t and "this gets \"" in aa:
				return [0, self.name(a, s="a"), -1, "Another", "Name=", self.name(a, s="n"), "ability"]
			elif "get + power" in t:
				if "all your other characters with  or " in t:
					return [-2, self.digit(a), -1, "Other", "OMore", 1, "Oother", "OName=", self.name(a, s='n'), "Trait", f"{self.trait(a)}_{self.trait(a, 1)}", "power"]
				elif "all your other characters with \"" in aa:
					return [-2, self.digit(a), -1, "Other", "OMore", 1, "Oother", "OName=", self.name(a, s='n'), "Name", self.name(a, -1, s='n'), "power"]
				elif "all your other  characters" in t:
					return [-2, self.digit(a), -1, "Other", "OMore", 1, "Oother", "OName=", self.name(a, s='n'), "Trait", self.trait(a), "power"]
			elif ("get " in t and "get \"" in aa) or "get following ability" in t:
				if "all your other  characters" in t:
					if "\" and \"" in aa:
						return [-2, self.name(a, s='a'), -1, "Other", "OMore", 2, "Oother", "O&", "OName", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}", "Trait", self.trait(a), "ability"]
					else:
						return [-2, self.name(a, s='a'), -1, "Other", "OMore", 1, "Oother", "OName=", self.name(a, s='n'), "Trait", self.trait(a), "ability"]
				elif "all your characters" in t:
					if "\" and \"" in aa:
						return [-1, self.name(a, s='a'), -1, "Other", "OMore", 2, "Oother", "O&", "OName", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}", "ability"]
					else:
						return [-1, self.name(a, s='a'), -1, "Other", "OMore", 1, "Oother", "OName=", self.name(a, s='n'), "ability"]
		elif "if you have another level  or higher character" in t or "if you have another character whose level is  or higher" in t:
			if "this gets + level and + power" in t:
				return [0, self.digit(a, 2), -1, "More", 1, "LevelC", self.digit(a), "power", 0, self.digit(a, 1), -1, "More", 1, "LevelC", self.digit(a), "level"]
			elif "gets + power" in t:
				return [0, self.digit(a, 1), -1, "More", 1, "LevelC", self.digit(a), "power"]
			elif "this gets + soul" in t:
				return [0, self.digit(a, 1), -1, "More", 1, "LevelC", self.digit(a), "soul"]
		elif "if  is in your memory" in t:
			if "all your other  characters" in t:
				if "gets + power" in t:
					return [-2, self.digit(a), -1, "Other", "OMore", 1, "OName=", self.name(a, s='n'), "OMemory", "Trait", self.trait(a), "power"]
			elif "this gets + power and the following ability" in t:
				return [0, self.digit(a), -1, "More", 1, "Name=", self.name(a, s='n'), "Memory", "power", 0, self.name(a, s='a'), -1, "More", 1, "Name=", self.name(a, s='n'), "Memory", "ability"]
			elif "this gets + power" in t:
				return [0, self.digit(a), -1, "More", 1, "Name=", self.name(a, s='n'), "Memory", "power"]
		elif ("all your other  or  characters" in t or "all your other characters with" in t) and "» or «" in aa:
			if "get + power" in t:
				return [-2, self.digit(a), -1, "Other", "Trait", f"{self.trait(a)}_{self.trait(a, 1)}", "power"]
		elif "all your other  characters" in t:
			if "gets + power and " in t and "power and \"[" in aa:
				return [-2, self.digit(a), -1, "Other", "Trait", self.trait(a), "power", -2, self.name(a, s="a"), -1, "Other", "Trait", self.trait(a), "ability"]
			elif "get + level and + power" in t:
				return [-2, self.digit(a, 1), -1, "Other", "Trait", self.trait(a), "power", -2, self.digit(a), -1, "Other", "Trait", self.trait(a), "level"]
			elif "get + power" in t:
				if "all your other \"" in aa:
					return [-2, self.digit(a), -1, "Other", "Name=", self.name(a, s='n'), "power"]
				else:
					return [-2, self.digit(a), -1, "Other", "Trait", self.trait(a), "power"]
			elif "get +x power" in t:
				if "x =  times the level of that character" in t:
					return [-2, self.digit(a), -1, "Other", "Trait", self.trait(a), "xlevel", "x", self.digit(a), "power"]
			elif "get [" in t:
				return [-2, self.name(a, 1), -1, "Other", "Trait", self.trait(a), "ability"]
		elif ("all your other characters with" in t and "characters with \"" in aa) or ("all your other" in t and "all your other \"" in aa):
			if "gets + power and " in t and "power and \"[" in aa:
				if ("all your other \"" in aa and "\" and \"" in aa) or ("all your other characters with \"" in aa and "\" or \"" in aa):
					return [-2, self.digit(a), -1, "Other", "Name", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}", "power", -2, self.name(a, -1, s="a"), -1, "Other", "Name", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}", "ability"]
			elif "get the following ability" in t or ("gets \"[" in aa or "get \"[" in aa):
				if "if there are  or more cards in your memory" in t:
					if "and this gets \"" in aa:
						return [-32, self.name(a, s='a'), -1, "Other", "OMore", self.digit(a), "OMemory", f"Name", f"{self.name(a, s='n')}", "ability"]
				else:
					return [-2, self.name(a, s='a'), -1, "Other", f"Name", f"{self.name(a, s='n')}", "ability"]
			elif "get + power" in t or "gets + power" in t:
				if self.name(a, s='a') in self.text_name:
					return [-2, self.digit(a), -1, "Other", "Text", self.text_name[self.name(a, s='a')], "power"]
				elif "all your other cards named  and " in t or "all your other  and " in t:
					return [-2, self.digit(a), -1, "Other", "Name", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}", "power"]
				elif "all your other characters with  or  or  in name" in t:
					if "\" is in your climax area" in aa:
						return [-2, self.digit(a), -1, "Other", "Name", f"{self.name(a, 2, s='n')}_{self.name(a, 4, s='n')}_{self.name(a, 6, s='n')}", "cx", self.name(a, s='n'), "power"]
					else:
						return [-2, self.digit(a), -1, "Other", "Name", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}_{self.name(a, 4, s='n')}", "power"]
				elif "all your other characters with  or " in t:
					return [-2, self.digit(a), -1, "Other", "Name", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}", "power"]
				elif "all your other  or  or " in t:
					return [-2, self.digit(a), -1, "Other", f"Name", f"{self.name(a, s='n')}_{self.name(a, 2, s='n')}_{self.name(a, 4, s='n')}", "power"]
				else:
					return [-2, self.digit(a), -1, "Other", f"Name", f"{self.name(a, s='n')}", "power"]
			elif "gets + level" in t or "get + level" in t:
				return [-2, self.digit(a), -1, "Other", f"Name", f"{self.name(a, s='n')}", "level"]
		elif "all your other characters" in t:
			if "get the following ability" in t:
				return [-2, self.name(a, 1), -1, "Other", "ability"]
			elif "get + power" in t:
				return [-2, self.digit(a), -1, "Other", "power"]
		elif "if all your characters have  or" in t and "in its card name" in t:
			if "this gets + power" in t:
				return [0, self.digit(a), -1, "All", "Name", f"{self.name(a, 1)}_{self.name(a, 3)}", "power"]
		elif "if all your characters are " in t or "if all of your characters are " in t:
			if "this gets + power" in t:
				return [0, self.digit(a), -1, "All", "Trait", f"{self.trait(a)}", "power"]
		elif "if there are  or fewer characters" in t:
			if "in your opponent's center stage" in t:
				if "this gets + power" in t:
					return [0, self.digit(a, 1), -1, "More", self.digit(a), "Center", "opp", "lower", "power"]
		elif "if there are  or fewer climax cards in your waiting room" in t:
			if "this gets + power" in t:
				return [0, self.digit(a, 1), -1, "More", self.digit(a), "Climax", "Waiting", "lower", "power"]
		elif "if you do not have any other characters" in t:
			if "in your center stage" in t:
				if "this gets + power and " in t:
					return [0, self.digit(a), -1, "NoCH", "Center", "other", "power", 0, self.name(a, s="a"), -1, "CONT", "ability"]
		elif "if the number of your other  or  characters is  or more" in t:
			if "this gets + power" in t:
				return [0, self.digit(a, 1), -1, "More", self.digit(a), "other", "Trait", f"{self.trait(a)}_{self.trait(a, 1)}", "power"]
		elif "you have  or more other" in t or "if the number of other  characters you have is  or more" in t or "if the number of your other  characters is  or more" in t:
			if "this gets  and is also considered to have  as the name" in t:
				return [0, self.trait(a), -1, "More", self.digit(a), "other", "Trait", self.trait(a), "trait", 0, self.name(a, s='n'), -1, "More", self.digit(a), "other", "Trait", self.trait(a), "name"]
			elif "this gets + power" in t and "and \"[" in a:
				return [0, self.digit(a, 1), -1, "More", self.digit(a), "other", "Trait", self.trait(a), "power", 0, self.name(a, 1), -1, "More", self.digit(a), "Trait", self.trait(a), "ability"]
			elif "this gets + power" in t:
				if "or more other \"" in aa:
					return [0, self.digit(a, 1), -1, "More", self.digit(a), "other", "Name=", self.name(a, s='n'), "power"]
				elif "characters with  or " in t:
					return [0, self.digit(a, 1), -1, "More", self.digit(a), "other", "Trait", f"{self.trait(a)}_{self.trait(a, 1)}", "power"]
				else:
					return [0, self.digit(a, 1), -1, "More", self.digit(a), "other", "Trait", self.trait(a), "power"]
			elif "this gets \"[" in aa or "this gets the following ability" in t:
				return [0, self.name(a, 1), -1, "More", self.digit(a), "Trait", self.trait(a), "other", "ability"]
		elif "if you have  or fewer other characters" in t or "if the number of other characters you have is  or less" in t or "if the number of your other characters is  or less" in t:
			if "this gets + power and the following ability" in t:
				return [0, self.digit(a, 1), -1, "More", self.digit(a), "lower", "other", "power", 0, self.name(a, s='a'), -1, "More", self.digit(a), "lower", "other", "ability", ]
			elif "this gets + power" in t:
				return [0, self.digit(a, 1), -1, "More", self.digit(a), "lower", "other", "power"]
		elif "if you have no other character" in t:
			if "this gets + level and + power" in t:
				return [0, self.digit(a, 1), -1, "More", 0, "lower", "other", "power", 0, self.digit(a), -1, "More", 0, "lower", "other", "level"]
			elif "this gets + power" in t:
				if "in the center stage" in t:
					return [0, self.digit(a), -1, "More", 0, "lower", "Center", "other", "power"]
				else:
					return [0, self.digit(a), -1, "More", 0, "lower", "other", "power"]
		elif "cost of the character opposite this is  or lower" in t:
			if "this does not reverse" in t:
				return [0, "", -1, "no_reverse", "cost", self.digit(a), "lower"]
		elif "for each marker under this" in t or "for each marker underneath this" in t:
			if "this gets + level and + power" in t:
				return [0, self.digit(a, 1), -1, "Each", "marker", "power", 0, self.digit(a), -1, "Each", "marker", "level"]
			elif "this gets + power" in t or "this gets - power" in t:
				return [0, self.digit(a), -1, "Each", "marker", "power"]
		elif "during this's battle, you cannot play event cards and  from your hand" in t or "during this's battle, you cannot play event cards and  from hand" in t:
			return [0, "", -1, "no_backup", "no_event", "battle"]
		elif "during this's battle, your opponent cannot play  from hand" in t and "\"Backup\"" in a:
			return [0, "", -1, "no_backup", "opp", "battle"]
		elif "your opponent cannot play event cards and  from his or her hand" in t:
			return [0, "", -1, "no_backup", "no_event", "opp"]
		elif "your opponent cannot play events from hand" in t:
			return [0, "", -1, "no_event", "opp"]
		elif "you cannot play events or backup from hand" in t:
			return [0, "", -1, "no_backup", "no_event"]
		elif "you cannot play events from hand" in t:
			return [0, "", -1, "no_event"]
		elif "you cannot play a climax card from your hand" in t:
			# during your climax phase
			return [0, "", -1, "no_climax"]
		elif "you cannot put  card from your hand in your clock and draw cards during your clock phase" in t or "you cannot put a card from your hand in your clock and draw cards during your clock phase" in t:
			return [0, "", -1, "no_clock"]
		elif "your opponent cannot play climax cards from hand" in t:
			return [0, "", -1, "no_climax", "opp"]
		elif "your opponent cannot use any act of characters on his or her stage" in t:
			return [0, "", -1, "no_act", "opp"]
		elif "your opponent cannot use  until end of turn" in t and "\"[auto] encore\"" in aa:
			return [0, "", -1, "no_encore", "opp"]
		elif "you cannot use  until end of turn" in t and "\"[auto] encore\"" in aa:
			return [0, "", -1, "no_encore"]
		elif "this does not reverse" in t:
			return [0, "", -1, "no_reverse"]
		elif "this cannot be reverse by effects of [auto] abilities of your opponent's characters" in t:
			if "this cannot side attack" in t:
				return [0, "", -1, "no_reverse_auto", "no_side"]
			else:
				return [0, "", -1, "no_reverse_auto"]
		elif "this cannot side attack" in t:
			if "this cannot move to another position" in t:
				return [0, "", -1, "no_side", "no_move"]
			else:
				return [0, "", -1, "no_side"]
		elif "this cannot front attack" in t:
			if "if the level of the character opposite this is higher than the level of this" in t:
				return [0, "", -1, "no_front", "olevel", "higher"]
			else:
				return [0, "", -1, "no_front"]
		elif "this cannot attack" in t:
			if "if there is  or fewer card in your clock" in t:
				return [0, "", -1, "no_attack", "Clock", self.digit(a), "lower"]
			elif "if there is  or fewer character in your back stage" in t:
				return [0, "", -1, "no_attack", "Stage", self.digit(a), "Back", "lower"]
			elif "if the character opposite this is higher level than this" in t:
				return [0, "", -1, "no_attack", "OLevel"]
			else:
				return [0, "", -1, "no_attack"]
		elif "this cannot be chosen by your opponent's effects" in t or "this cannot be chosen as the target of your opponent's effects" in t:
			return [0, "", -1, "no_target"]
		elif "this cannot stand during your stand phase" in t:
			return [0, "", -1, "no_stand"]
		elif "this's soul does not decrease by side attacking" in t:
			return [0, "", -1, "no_decrease"]
		elif "this cannot move to another position" in t:
			return [0, "", -1, "no_move"]
		elif "during battles involving this" in t:
			if "this gets +x power" in t:
				if "x =  times level of that character" in t:
					if "if the battle opponent of this has " in t:
						return [0, self.digit(a), -1, "Battle", "otrait", self.trait(a), "xolevel", "x", self.digit(a), "power"]
			elif "gets + power" in t:
				if "if the battle opponent of this is level  or higher" in t:
					return [0, self.digit(a, 1), -1, "Battle", "olevel", self.digit(a), "power"]
				elif "if the battle opponent of this has  or " in t and "» or «" in aa:
					return [0, self.digit(a), -1, "Battle", "otrait", f"{self.trait(a)}_{self.trait(a, 1)}", "power"]
				elif "if the battle opponent of this has " in t and "has «" in aa:
					return [0, self.digit(a), -1, "Battle", "otrait", self.trait(a), "power"]
			elif "this gets " in t:
				return [0, self.trait(a), -1, "Battle", "trait"]
		elif "if the character opposite this has no traits" in t:
			if "this gets the following ability" in t:
				return [0, self.name(a, s='a'), -1, "Opposite", "#traits", 0, "#lower", "ability"]
		elif "if the number of cards in your opponent's clock is  or more" in t:
			if "this gets + power" in t:
				return [0, self.digit(a, 1), -1, "Clock", self.digit(a), "opp", "power"]
		elif "all your characters whose level is higher than your level" in t:
			if "gets + power" in t:
				return [-1, self.digit(a), -1, "LevelP", "power"]
		elif "all your characters get" in t or "all of your characters get" in t:
			if "+ power and + soul" in t:
				return [-1, self.digit(a), -1, "CONT", "power", -1, self.digit(a, 1), -1, "CONT", "soul"]
			elif "+ soul" in t:
				return [-1, self.digit(a), -1, "CONT", "soul"]
			elif "+ power" in t:
				return [-1, self.digit(a), -1, "CONT", "power"]
		elif "character opposite this" in t:
			if "gets + soul and cannot side attack" in t:
				return [-6, "[CONT] This cannot side attack.", -1, "Opposite", "ability", -6, self.digit(a), -1, "Opposite", "soul"]
			elif "gets + soul" in t:
				return [-6, self.digit(a), -1, "Opposite", "soul"]
			elif "gets - soul" in t:
				return [-6, self.digit(a), -1, "Opposite", "soul"]
			elif ("gets " in t and "gets \"[" in aa) or "this gets the following ability" in t:
				return [-6, self.name(a, s='a'), -1, "Opposite", "ability"]
			elif "gets " in t:
				return [-6, self.trait(a), -1, "Opposite", "trait"]
		elif "if you would pay the act cost for  of your characters in your hand or stage" in t:
			if "you may put  marker from underneath this in your waiting room instead of  card from your stock" in t:
				return [0, self.digit(a), -1, "astock"]
		elif "this gets +x power" in t:
			if "x =  multiplied by the level of the character opposite this" in t:
				return [0, self.digit(a), -1, "X", "xlevel", "opposite", "power", "x", self.digit(a)]
			elif "x =  times the highest level amongst your characters with  in the name" in t:
				return [0, self.digit(a), -1, "X", "xhighlevel", "xName", self.name(a, s='n'), "power", "x", self.digit(a)]
		elif "this gets - level" in t:
			return [0, self.digit(a), -1, "Stage", "level"]
		return []

	def play(self, a=""):
		t = self.text(a)

		if "if there are no characters in your back stage, you cannot play this from hand" in t:
			return [0, "Character", "Back", "lower", "play"]
		elif "if you have no  characters, you cannot play this from your hand" in t or (("you do not have an  character," in t or "you do not have a  character," in t or "if you do not have any  characters" in t) and ("this cannot be played from hand" in t or " this cannot be played from your hand" in t)) or "you cannot play this from hand if you don't have a  character" in t:
			return [0, "Trait", self.trait(a), "lower", "play"]
		elif "if you have  or fewer  characters, you cannot play this from hand" in t or "if the number of  characters on your stage is  or less, this cannot be played from your hand" in t or "if you have  or less  characters, this cannot be played from your hand" in t:
			return [self.digit(a), "Trait", self.trait(a), "lower", "play"]
		elif "if the number of characters in your center stage is  or more, this cannot be played from your hand" in t:
			return [self.digit(a), "Character", "Center", "play"]
		elif "if you have  or more characters, you cannot play this from your hand" in t:
			return [self.digit(a), "Character", "play"]
		return []

	def climax(self, a=""):
		effect = []
		text = self.text(a)
		if "for the turn" in text or " until end of turn" in text:
			x = 1
		else:
			x = -1

		if 'when this is placed from hand to the climax area' in text or "when this is placed on your climax area from hand" in text or "when this is placed on your climax area from your hand" in text:
			if "perform the [standby] effect" in text:
				return self.trigger("standby")
			elif "choose up to   card in your waiting room" in text:
				if "put it in your stock" in text:
					effect = [self.digit(a), "cstock", self.colour_t(a), "Waiting", "upto"]
			elif "put the top card of your deck in your stock" in text:
				effect = ["stock", 1]
			elif "draw  card" in text:
				effect = ["draw", self.digit(a)]

		if "all your characters get" in text or "all of your characters get" in text:
			if "+ power and + soul" in text:
				return [-1, self.digit(a), x, "power", -1, self.digit(a, 1), x, "soul"]
			elif "+ soul" in text:
				if effect and "stock" in effect:
					return effect + ["do", [-1, self.digit(a), x, "soul"]]
				elif effect:
					return effect + ["do", [-1, self.digit(a, 1), x, "soul"]]
				else:
					return [-1, self.digit(a), x, "soul"]
			elif "+ power" in text:
				if effect and "stock" in effect:
					return effect + ["do", [-1, self.digit(a), x, "soul"]]
				elif effect:
					return effect + ["do", [-1, self.digit(a, 1), x, "power"]]
				else:
					return [-1, self.digit(a), x, "power"]
		elif "choose  of your characters" in text:
			if "that character gets + power and + soul" in text:
				if effect:
					return effect + ["do", [self.digit(a, 1), self.digit(a, 2), x, "power", self.digit(a, 1), self.digit(a, 3), x, "soul"]]
				else:
					return [self.digit(a, 1), self.digit(a, 2), x, "power", self.digit(a, 1), self.digit(a, 3), x, "soul"]
			elif "that character gets + soul" in text:
				if effect:
					return effect + ["do", [self.digit(a, 1), self.digit(a, 2), x, "soul"]]
				else:
					return [self.digit(a, 1), self.digit(a, 2), x, "soul"]
		elif "all your characters randomly get between +~+ soul" in text:
			return [-1, self.digit(a), x, "random", self.digit(a, 1), "soul"]
		return []

	def trigger(self, a=""):
		if "door" in a:
			return ["pay", "may", "do", [1, "salvage", "Character", "upto", "show"], "text", "When this card triggers, you may choose a character in your waiting room, and return it to your hand."]
		elif "gate" in a:
			return ["pay", "may", "do", [1, "salvage", "Climax", "upto", "show"], "text", "When this card triggers, you may choose a climax card in your waiting room, and return it to your hand."]
		elif "bounce" in a:
			return ["pay", "may", "do", [1, "Character", "wind", "Opp", "may"], "text", "When this card triggers, you may choose an opponent's character on stage, and return it to his or her hand."]
		elif "standby" in a:
			return ["pay", "may", "do", [1, "salvage", f"CLevel_standby", "Stage", "extra", "upto", "do", [-16, "rest"]], "text", "When this card triggers, you may choose 1 character with a level equal to or less than your level +1 in your waiting room, and put it on any position of your stage as [REST]"]
		elif "draw" in a:
			return ["pay", "may", "do", ["draw", 1], "text", "When this card triggers, you may draw a card."]
		elif "soul" in a:
			return [-12, 1, 1, "soul", "text", "Give +1 soul to the attacking character until the end of the turn."]
		elif "shot" in a:
			return [-12, "[AUTO] When the damage dealt by this card is cancelled, deal one damage to your opponent", -2, "give", "text", "During this turn, when the next damage dealt by the attacking character that triggered this card is canceled, deal 1 damage to your opponent."]
		elif "stock" in a:
			return ["pay", "may", "do", ["stock", 1], "text", "When this card triggers, you may put the top card of your deck into your stock"]
		elif "treasure" in a:
			return [0, "hander", "do", ["pay", "may", "do", ["stock", 1]], "text", "When this card triggers, return this card to your hand. You may put the top card of your deck into your stock"]
		return []

	def digit(self, a="", i=0):
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

		if "(1)" in t:
			t = t.replace("(1)", "()")
		if "(2)" in t:
			t = t.replace("(2)", "()")
		if "(3)" in t:
			t = t.replace("(3)", "()")
		if "(4)" in t:
			t = t.replace("(4)", "()")
		if "(5)" in t:
			t = t.replace("(5)", "()")

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
		if "[counter] backup" in a.lower():
			t = t.replace(",", "").split("[")[0].split()
		elif ("get \"" in t or "gets \"" in t) and t.count("[") == 1:
			t = t.split("[")[0].split()
		elif t.count("]") == 1:
			if t.startswith("[") or t.startswith(" ["):
				t = t.split("]")[1].split()
			elif t.startswith("\" ENCORE ["):
				t = t.split("]")[1].split()
			elif t.lower().startswith("change ["):
				t = t.split("]")[1].split()
			elif t.count("[") == 0:
				if "gets the following ability. \"" in t or "get \"" in t or "gets \"" in t:
					t = t.split("]")[0].split()
				else:
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
		if any(f"{colour} card" in t for colour in self.colour):
			for colour in self.colour:
				if f"{colour} card" in t:
					t = f"{colour}_Card"
		return t

	def name(self, a="", i=0, s=""):
		n = "\""
		# elif a.count("\"") == 2:
		t = a
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
		elif "at" in s:
			if "at the beginning of your next" in a.lower():
				t = f"[AUTO] At the beginning of your{a.split('the beginning of your next')[1]}"
			elif "at the start of your next" in a.lower():
				t = f"[AUTO] At the beginning of your{a.split('the start of your next')[1]}"
		elif "a" in s:
			c = a.count(n)
			if c == 2:
				t = a.split(n)[1]
			elif c > 2:
				t = a.split(n)
				t = [s for s in t if any(s.startswith(abl) for abl in self.ability[:3]) and f"\"{s}\"" in a]
				if len(t) < 1:
					t = ""
					i = 0
				else:
					t = t[i]

			if "(" in t and ")" in a and "encore" not in t.lower():
				if "[(" in t and ")]" in t and t.count("(") == 1:
					pass
				else:
					t = t.split("(")[0]
		elif "n" in s:
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
				if all(al.lower() in self.alpha for al in t[1]):
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
			a = a.replace(rep, self.resource[rep])

		return a

	def text(self, a="", i=1, l=True, c=True):
		t = a
		if t.count("[") >= 2:
			for item in self.status:
				t = t.replace(item, self.status[item])
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
		elif t.startswith("change ["):
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

		t = "".join(s for s in t if not s.isdigit())

		if c:
			for colour in self.colour:
				if f" {colour} " in t:
					t = t.replace(f" {colour} ", "  ")

		if t.startswith(" "):
			t = t[1:]

		return t

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
