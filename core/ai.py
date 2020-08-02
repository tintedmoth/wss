from random import sample, choice


class AI:
	def __init__(self, player):
		self.player = player
		# if self.player == "1":
		# 	gdata["opp"] = "2"
		# elif self.player == "2":
		# 	gdata["opp"] = "1"
		# self.colour = {"yellow": 0, "green": 0, "red": 0, "blue": 0, "0": [], "1": [], "2": [], "3": [], "CX": []}
		# self.level = {"0": 0, "1": 0, "2": 0, "3": 0, "CX": 0}
		# self.hand = {"0": 0, "1": 0, "2": 0, "3": 0, "CX": 0}
		# self.open_front = 0
		# self.open_back = 0
		# self.fill_data()
		self.counter = [1500]

	def ability(self, pdata, cdata,gdata):
		pay = (gdata["pay"], gdata["payed"])
		effect = gdata["effect"]
		hand = pdata[self.player]["Hand"]
		stage = pdata[self.player]["Center"] + pdata[self.player]["Back"]
		stand = len([s for s in stage if cdata[s].status == "Stand"])
		stock = len(pdata[self.player]["Stock"])
		card = cdata[gdata["ability_trigger"].split("_")[1]]
		back = [s for s in pdata[self.player]["Back"] if s != ""]
		center = [s for s in pdata[self.player]["Center"] if s != ""]
		stand_back = [s for s in back if cdata[s].status == "Stand"]
		waiting = pdata[self.player]["Waiting"]
		confirm = "pass"

		if not pay[0]:
			payable = ["np"]
		else:
			payable = [""]

		if "Stock" in pay[0] and not stock >= pay[0][pay[0].index("Stock") + 1]:
			payable = pay[0]
		if "Rest" in pay[0]:
			ind = pay[0].index("Rest")
			if pay[0][ind + 1] == 0 and card.status != "Rest":
				payable = pay[0]
			elif pay[0][ind + 1] >= 1 and stand >= 1:
				if len(back) > 0 and len(stand_back) > 0:
					payable = pay[0]
					payable.append("AI_pay")
					payable.append(back[0])
		if "Clock" in pay[0]:
			ind = pay[0].index("Clock")
			if pay[0][ind + 1] >= 1 and len(hand) >= 1:
				payable = pay[0]
				payable.append("AI_pay")
				payable.append(choice(hand))  # @ Random

		if "janken" in effect and payable:
			pass
		elif "confirm" in effect and payable:
			y = ["y", ] * 9
			y = y + ["n"]
			payable.append(choice(y))
		elif "salvage" in effect and pay[1]:
			# if "Character" in effect[2] or "Climax" in effect[2]:
			# 	salvage = [s for s in waiting if cdata[s].card in effect[2]]
			# elif "Trait" in effect[2]:
			# 	salvage = [s for s in waiting if any(trait in cdata[s].trait_t for trait in effect[2].split("_")[1:])]

			# hand = pdata[self.player]["Hand"]
			# salvage(self, trigger, ctype, n, cost)
			salvage = list(gdata["p_l"])

			if pay[1] and len(salvage) >= 1:
				salvage = sorted(salvage, key=lambda e: cdata[e].level, reverse=True)
				# elif "Climax" in effect[2]:
				# 	pass
				# elif "bond" in effect:
				# 	pass

				payable.append("AI_salvage")
				if pay[1] and len(salvage) >= 1:
					payable.append(salvage[:effect[0]])
				else:
					payable.append([""])



			#
			# 	if "Character" in effect[2]:
			# 		# if any("counter" in cdata[self.player][ind].icon.lower() for ind in discard):
			# 		salvage = sorted(salvage, key=lambda e: cdata[e].level, reverse=True)
			# 	elif "Climax" in effect[2]:
			# 		pass
			# 	elif "bond" in effect:
			# 		pass
			# 	payable.append(salvage[:effect[0]])
			# else:
			# 	payable.append([""])
		elif ("search" in effect or "searchopp" in effect) and pay[1]:
			# if "Character" in effect[2] or "Climax" in effect[2]:
			# 	search = [s for s in pdata[self.player]["Library"] if effect[2].split("_")[0] in cdata[s].card]
			# elif "Trait" in effect[2]:
			# 	search = [s for s in pdata[self.player]["Library"] if
			# 	          any(trait in cdata[s].trait_t for trait in effect[2].split("_")[1:])]

			# hand = pdata[self.player]["Hand"]
			# salvage(self, trigger, ctype, n, cost)
			search = list(gdata["p_l"])
			if pay[1] and len(search) >=1:
				# if "Character" in effect[2]:
					# if any("counter" in cdata[self.player][ind].icon.lower() for ind in discard):
				if "searchopp" in effect:
					search = sorted(search, key=lambda e: cdata[e].level)
				else:
					search = sorted(search, key=lambda e: cdata[e].level, reverse=True)
				# elif "Climax" in effect[2]:
				# 	pass
				# elif "bond" in effect:
				# 	pass

				payable.append("AI_search")
				if pay[1] and len(search) >= 1:
					payable.append(search[:effect[0]])
				else:
					payable.append([""])
		elif "discard" in effect and pay[1]:
			payable.append("AI_discard")
			temp=[]
			for r in range(effect[1]):
				if len(pdata[self.player]["Hand"])-len(temp)>0:
					temp.append(choice(pdata[self.player]["Hand"]))
				else:
					temp.append("")
			payable.append(temp)
		elif "survive" in effect and pay[1]:
			play = 0
			attacker = 0
			for ind in hand:
				if self.playable(pdata, cdata, ind):
					if "Character" in cdata[ind].card:
						attacker += 1

			for indd in stage:
				if cdata[indd].status != "Reverse":
					attacker += 1
			if attacker <= 1:
				payable.append("AI_survive")
		elif "rest" in effect and pay[1]:
			pick = []
			var = []
			if effect[0] > 1:
				for ind in back:
					if cdata[ind].status != "Rest":
						pick.append(ind)
				if effect[0] > len(pick):
					for ind in pick:
						var.append(ind)
					pick = []
					for ind in center:
						if cdata[ind].status != "Rest":
							pick.append(ind)
					temp = sample(pick, effect[0] - len(var))
					for ind in temp:
						var.append(ind)
				else:
					var.append(choice(pick))
					if len(var) < effect[0]:
						for ind in pick:
							if ind not in var:
								var.append(ind)

			payable.append("AI_target")
			for ind in var:
				payable.append(ind)

		if payable:
			confirm = payable
		return confirm

	def playable(self, pdata, cdata, ind):
		level = len(pdata[self.player]["Level"])
		card = cdata[ind]
		if card.card == "Climax":
			if card.mcolour in pdata[self.player]["colour"]:
				return True
		else:
			if card.level == 0:
				return True

			elif card.level <= level:
				if card.mcolour in pdata[self.player]["colour"]:
					if card.cost <= len(pdata[self.player]["Stock"]):
						return True
		return False

	# def fill_data(self):
	# 	for inx in range(50):
	# 		card = cdata[str(inx + 1)]
	#
	# 		if card.card == "Climax":
	# 			self.level["CX"] += 1
	# 			if card.mcolour not in self.colour["CX"]:
	# 				self.colour["CX"].append(card.mcolour)
	# 		else:
	# 			self.level[str(card.level)] += 1
	# 			if card.mcolour not in self.colour[str(card.level)]:
	# 				self.colour[str(card.level)].append(card.mcolour)
	#
	# 		self.colour[card.mcolour.lower()] += 1

	# def update_hand(self):
	# 	for ind in pdata[self.player]["Hand"]:
	# 		card = cdata[ind]
	# 		if card.card == "Climax":
	# 			self.hand["CX"] += 1
	# 		else:
	# 			self.hand[str(card.level)] += 1

	def mulligan(self, pdata, cdata):
		# self.update_hand()
		discard = []
		for ind in pdata[self.player]["Hand"]:
			if cdata[ind].level >= 1 or cdata[ind].card == "Climax":
				discard.append(ind)
		return discard

	def clock(self, pdata, cdata):
		# self.update_hand()
		hand = pdata[self.player]["Hand"]
		level = len(pdata[self.player]["Level"])
		clock = len(pdata[self.player]["Clock"])
		center = len([s for s in pdata[self.player]["Center"] if s != ""])
		back = len([s for s in pdata[self.player]["Back"] if s != ""])
		stock = len(pdata[self.player]["Stock"])
		deck = len(pdata[self.player]["Library"])
		climax = [s for s in hand if cdata[s].card == "Climax"]

		clist = []

		if level == 3 and (clock >= 6 or (clock >= 5 and deck < 6)):
			discard = "pass"
		elif center == 3 and back == 2 and len(hand) >= 7:
			discard = "pass"
		elif center == 3 and len(hand) >= 7 and not any(
				len(cdata[ind].text_o) >= 1 and "assist" in cdata[ind].text_o[0].lower() for ind in hand):
			discard = "pass"
		else:
			for ind in hand:
				card = cdata[ind]
				if level <= 1:
					if (clock >= 6 or (clock >= 5 and deck <= 2)) and card.level > level + 1:
						clist.append(ind)
					elif card.level > level:
						clist.append(ind)
				elif level > 1:
					clist.append(ind)

			if len(clist) < 1:
				if level > 1 and "Blue" not in pdata[self.player]["colour"]:
					clist = [s for s in hand if cdata[s].mcolour == "Blue"]
					if len(clist) == 1:
						if cdata[clist[0]].icon == "Counter":
							clist = []
				elif len(climax) > 1:
					clist = [choice(climax)]
				else:
					for ind in hand:
						if not self.playable(pdata, cdata, ind):
							clist.append(ind)

			if len(clist) > 0:
				discard = choice(clist)
			else:
				discard = "pass"

		return discard

	def level_up(self, pdata, cdata):
		# self.update_hand()
		level = [s for s in pdata[self.player]["Clock"] if cdata[s].card != "Climax"]
		discard = choice(level)
		return discard

	def hand_limit(self, pdata, cdata):
		# self.update_hand()
		discard = []
		hand = list(pdata[self.player]["Hand"])

		for inx in range(len(pdata[self.player]["Hand"][7:])):
			r = choice(hand)
			discard.append(r)
			hand.remove(r)

		return discard

	def main_play(self, pdata, cdata, gdata):
		# self.update_hand()
		hand = pdata[self.player]["Hand"]
		center = len([s for s in pdata[self.player]["Center"] if s != ""])
		back = len([s for s in pdata[self.player]["Back"] if s != ""])
		stock = len(pdata[self.player]["Stock"])

		stock_req = 0
		playable = []
		play = []
		assist = []
		for ind in hand:
			card = cdata[ind]
			if card.card == "Climax":
				continue
			elif self.playable(pdata, cdata, ind):
				stock_req += card.cost
				playable.append(ind)
				if any("assist" in nx.lower() for nx in cdata[ind].text_o):
					assist.append(ind)

		playable = sorted(playable, key=lambda x: cdata[x].level, reverse=True)

		if len(assist) > 0 and back < 2:
			occ = []
			for ind in assist:
				for inx in range(2):
					if pdata[self.player]["Back"][inx] == "" and all(item not in occ for item in (ind, inx)):
						if ind in playable:
							playable.remove(ind)
						play.append((ind, "Back", inx))
						occ.append(ind)
						occ.append(inx)
						back += 1
						break
				if back >= 2:
					break

		if len(playable) > 0 and center < 3:
			occ = []
			for ind in playable:
				card = cdata[ind]
				if card.icon == "Counter":
					continue
				elif card.card == "Event":
					continue
				# event = self.event(ind,playable)
				# play.append(event)
				elif card.cost > stock:
					continue
				else:
					for inx in range(3):
						if pdata[self.player]["Center"][inx] == "" and all(item not in occ for item in (ind, inx)):
							play.append((ind, "Center", inx))
							stock -= card.cost
							occ.append(ind)
							occ.append(inx)
							center += 1

						if center >= 1 and gdata["turn"] == 1:
							break
						elif center >= 3:
							break

		if len(play) < 1:
			play = "pass"

		return play

	def encore(self, pdata, cdata, gdata):
		encore = [s for s in pdata[self.player]["Center"] + pdata[self.player]["Back"] if
		          s != "" and cdata[s].status == "Reverse"]
		stock = len(pdata[self.player]["Stock"])
		center = len([s for s in pdata[self.player]["Center"] if s != "" and cdata[s].status != "Reverse"])
		back = len([s for s in pdata[self.player]["Back"] if s != "" and cdata[s].status != "Reverse"])
		hand = pdata[self.player]["Hand"]
		level = len(pdata[self.player]["Level"])

		playable = []

		if len(encore) > 0 and stock >= 3 + level:
			for ind in hand:
				if self.playable(pdata, cdata, ind):
					playable.append(ind)

			playable = [s for s in playable if cdata[s].card == "Character"]

			if center <= 0 and len(playable) <= 1 and self.player not in gdata["active"]:
				encore.sort(key=lambda x: x.power, reverse=True)
		else:
			encore = []

		return encore

	def main_move(self, pdata, cdata):
		hand = pdata[self.player]["Hand"]
		back = [s for s in pdata[self.player]["Back"] if s != ""]

		opp_card = []
		pl_card = []
		place = [0, 1, 2]
		move = []
		assist_move = False

		if self.player == "1":
			opp = "2"
		elif self.player == "2":
			opp = "1"

		c = 0
		m = (2, 1, 0)
		for ind in range(3):
			if pdata[opp]["Center"][ind] == "":
				opp_card.append((0, m[ind]))
			else:
				card = cdata[pdata[opp]["Center"][ind]]
				opp_card.append((card.power_t, m[int(card.pos_new[-1])]))
			c += 1

		opp_card = sorted(opp_card, key=lambda e: e[0], reverse=True)

		for ind in pdata[self.player]["Center"]:
			if ind == "":
				continue
			else:
				aa = True
				for item in cdata[ind].text_c:
					if item[0].startswith("[CONT]") and item[1] != 0 and item[1] > -9:
						if "this cannot move to another position" in item[0].lower():
							aa = False
							break

				if aa:
					pl_card.append((cdata[ind].power_t, int(cdata[ind].pos_new[-1]), ind))
				else:
					for r in range(len(opp_card)):
						if opp_card[r][1] == m[int(cdata[ind].pos_new[-1])]:
							opp_card.remove(opp_card[r])
							break

		pl_card = sorted(pl_card, key=lambda e: e[0], reverse=True)

		for item in pl_card:
			for enemy in opp_card:
				if not assist_move and item[0] > enemy[0] and enemy[1] in place:
					if len(back) > 0:
						if enemy[1] == 0:
							inx = 0
						else:
							inx = enemy[1] - 1
						move.append((back[0], "Back", inx))
						assist_move = True
					move.append((item[2], "Center", enemy[1]))
					place.remove(enemy[1])
				elif item[0] > enemy[0] and enemy[1] in place:
					move.append((item[2], "Center", enemy[1]))
					place.remove(enemy[1])

		if len(move) < 1:
			move = "pass"

		return move

	def event(self, pdata, cdata, ind, playble):
		hand = pdata[self.player]["Hand"]
		level = len(pdata[self.player]["Level"])
		clock = len(pdata[self.player]["Clock"])
		center = len([s for s in pdata[self.player]["Center"] if s != ""])
		back = len([s for s in pdata[self.player]["Back"] if s != ""])
		stock = len(pdata[self.player]["Stock"])
		deck = len(pdata[self.player]["Library"])
		climax = [s for s in hand if cdata[s].card == "Climax"]

		card = cdata[ind]

		if card.name == "Car Ears Magnifying Glass":
			if len(playble.remove(ind)) >= center:
				pass

	def climax(self, pdata, cdata):
		hand = pdata[self.player]["Hand"]
		center = len([s for s in pdata[self.player]["Center"] if s != ""])
		climax = [s for s in hand if cdata[s].card == "Climax" and cdata[s].mcolour in pdata[self.player]["colour"]]

		if len(climax) > 1 and center > 1:
			climax = choice(climax)
		elif len(climax) > 0 and center >= 2:
			climax = choice(climax)
		else:
			climax = "pass"
		return climax

	def confirm_popup(self, effect, req):
		if req and "salvage" in effect:
			ans = "1"
		else:
			ans = ""

		return ans

	def attack(self, pdata, cdata, b=False):
		attack = []
		if self.player == "2":
			popp = "1"
		else:
			popp = self.player

		for inx in range(3):
			if b:
				opp = 1
			else:
				opp = (2, 1, 0)[inx]
			att = ["a","f","d","s"]
			t =""

			if pdata[self.player]["Center"][inx] != "":
				card = cdata[pdata[self.player]["Center"][inx]]
				for item in card.text_c:
					if item[0].startswith("[CONT]") and item[1] != 0 and item[1] > -9:
						if "this cannot side attack" in item[0].lower():
							if "s" in att:
								att.remove("s")
						if "this cannot front attack" in item[0].lower():
							if "f" in att:
								att.remove("f")
						if "this cannot direct attack" in item[0].lower():
							if "d" in att:
								att.remove("d")
						if "this cannot attack" in item[0].lower():
							if "a" in att:
								att.remove("a")
				if card.status == "Stand" and "a" in att:
					if pdata[popp]["Center"][opp] != "":
						copp = cdata[pdata[popp]["Center"][opp]]
						p = copp.pos_new[0]
						if card.power_t > copp.power_t:
							if "f" in att:
								t = "f"
							elif "s" in att:
								t = "s"
						elif card.power_t == copp.power_t:
							if "f" in att and "s" in att:
								t = choice(("f", "s"))
							elif "s" in att:
								t = "s"
							elif "f" in att:
								t = "f"
						elif card.power_t < copp.power_t:
							if card.soul_t - copp.level > 0:
								if "s" in att:
									t = "s"
								elif "f" in att:
									t = "f"
							elif card.soul_t - copp.level == 0:
								if "f" in att and "s" in att:
									t = choice(("f", "s"))
								elif "s" in att:
									t = "s"
								elif "f" in att:
									t = "f"
							else:
								if "f" in att:
									t = "f"
								elif "s" in att:
									t = "s"
						else:
							if "f" in att and "s" in att:
								t = choice(("f", "s"))
							elif "f" in att:
								t = "f"
							elif "s" in att:
								t = "s"
					else:
						if "d" in att:
							t = "d"
						p = ""

					if t != "":
						attack.append([pdata[self.player]["Center"][inx], t, inx, opp, p])

		if len(attack) < 1:
			attack = "pass"
		else:
			attack = sorted(attack, key=lambda e: cdata[e[0]].power_t, reverse=True)

		return attack

	def counter_step(self, pdata, cdata, gdata, opp, pl):
		hand = pdata[self.player]["Hand"]
		level = len(pdata[self.player]["Level"])
		card = cdata[pl]
		copp = cdata[opp]

		counter = []

		if card.power_t < copp.power_t:
			if card.level >= level - 1 and card.power_t + self.counter[0] > copp.power_t:
				counter = [s for s in hand if
				           cdata[s].icon == "Counter" and gdata["backup"][pl[-1]] and gdata["counter_icon"][pl[-1]][0]]

		if len(counter) < 1:
			counter = "pass"

		return counter
