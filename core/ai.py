from random import sample, choice
from core.ability import Ability as Ab
class AI:
	def __init__(self, player):
		self.player = player
		self.counter = [1500]
		self.ab = Ab()
	def filter_cards(self,lst,ind,pdata,cdata,gdata):
		lst1 = []
		if "CLevelE" in gdata["search_type"]:
			level = gdata["search_type"].split("_")[-1]
			if "<=" in level:
				lst1 = [s for s in lst if ("Character" in cdata[s].card and cdata[s].level <= int(level[-1])) or "Event" in cdata[s].card]
		elif "CLevel" in gdata["search_type"]:
			if "_standby" in gdata["search_type"]:
				lst1 = [s for s in lst if "Character" in cdata[s].card and cdata[s].level_t <= len(pdata[gdata["p_owner"]]["Level"]) + 1]
			elif "<=" in gdata["search_type"]:
				if "p" in gdata["search_type"][-1]:
					lst1 = [s for s in lst if cdata[s].level_t <= len(pdata[s[-1]]["Level"]) and "Character" in cdata[s].card]
				else:
					lst1 = [s for s in lst if cdata[s].level_t <= int(gdata["search_type"][-1]) and "Character" in cdata[s].card]
			elif ">=" in gdata["search_type"]:
				lst1 = [s for s in lst if cdata[s].level_t >= int(gdata["search_type"][-1]) and "Character" in cdata[s].card]
		elif "Trait" in gdata["search_type"]:
			if gdata["search_type"].split("_")[1:] == [""]:
				lst1 = [s for s in lst if len(cdata[s].trait_t) <= 0 and "Character" in cdata[s].card]
			else:
				lst1 = [s for s in lst if any(trait in cdata[s].trait_t for trait in gdata["search_type"].split("_")[1:])]
		elif "" in gdata["search_type"]:
			lst1 = lst
		return lst1
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
		confirm = "pass"
		if not pay[1]:
			payable = ["np"]
		else:
			payable = [""]
		if "sspace" in gdata["p_l"]:
			gdata["p_l"].remove("sspace")
		if "pay" in effect and "do" in effect:
			effect = effect[effect.index("do")+1]
		if "Stock" in pay[0] and not stock >= pay[0][pay[0].index("Stock") + 1]:
			payable.append("pass")
		if "Rest" in pay[0]:
			ind = pay[0].index("Rest")
			if pay[0][ind + 1] == 0 and card.status != "Rest":
				payable = pay[0]
			elif pay[0][ind + 1] >= 1 and stand >= 1:
				if len(back) > 0 and len(stand_back) > 0:
					payable.append("AI_pay")
					payable.append(back[0])
		if "Clock" in pay[0]:
			ind = pay[0].index("Clock")
			if pay[0][ind + 1] >= 1 and len(hand) >= 1:
				payable.append("AI_pay")
				payable.append(choice(hand))  
		if any("Discard" in str(pp) for pp in pay[0]):
			dis = [pp for pp in pay[0] if "Discard" in str(pp)]
			for dd in dis:
				if "MDiscard" in dd:
					loc = pdata[self.player]["Memory"]
					ind = pay[0].index("MDiscard")
				elif "CXDiscard" in dd:
					loc = pdata[self.player]["Climax"]
					ind = pay[0].index("CXDiscard")
				else:
					loc = pdata[self.player]["Hand"]
					ind = pay[0].index("Discard")
				if pay[0][ind + 1] >= 1 and len(loc) >= 1:
					if pay[0][ind + 2] == "Climax" or pay[0][ind + 2] == "Character" or pay[0][ind + 2] == "Event":
						hand1 = [h for h in loc if cdata[h].card == pay[0][ind + 2]]
					elif "Name" in pay[0][ind + 2]:
						hand1 = [h for h in loc if any(name in cdata[h].name for name in pay[0][ind + 3].split("_"))]
					elif "Trait" in pay[0][ind + 2]:
						hand1 = [h for h in loc if any(name in cdata[h].trait for name in pay[0][ind + 3].split("_"))]
					else:
						hand1 = loc
					hand1 = sorted(hand1, key=lambda e: (cdata[e].level, cdata[e].power), reverse=True)
					if "AI_pay" in payable:
						for hh in hand1[:pay[0][ind + 1]]:
							payable[payable.index("AI_pay")+1].append(hh)
					else:
						payable.append("Discard")
						payable.append("AI_pay")
						payable.append(hand1[:pay[0][ind + 1]])
		if "WDecker" in pay[0] or "Zwei" in pay[0]:
			loc = pdata[self.player]["Waiting"]
			if "WDecker" in pay[0]:
				ind = pay[0].index("WDecker")
			elif "Zwei" in pay[0]:
				ind = pay[0].index("WDecker")
			if len(loc)>=pay[0][ind + 1]:
				if pay[0][ind + 2] == "Climax" or pay[0][ind + 2] == "Character" or pay[0][ind + 2] == "Event":
					hand1 = [h for h in loc if cdata[h].card == pay[0][ind + 2]]
				elif "Name" in pay[0][ind + 2] or "ZName" in pay[0][ind + 2]:
					hand1 = [h for h in loc if any(name in cdata[h].name for name in pay[0][ind + 3].split("_"))]
				elif "Trait" in pay[0][ind + 2]:
					hand1 = [h for h in loc if any(name in cdata[h].trait for name in pay[0][ind + 3].split("_"))]
				else:
					hand1 = loc
				hand1 = sorted(hand1, key=lambda e: (cdata[e].level, cdata[e].power), reverse=True)
				if "AI_pay" not in payable:
					payable.append("AI_pay")
				if "WDecker" in pay[0]:
					payable.append("WDecker")
				elif "Zwei" in pay[0]:
					payable.append("WDecker")
				payable.append(hand1[:pay[0][ind + 1]])
		if "janken" in effect and payable:
			pass
		elif "confirm" in effect and payable:
			y = ["y", ] * 9
			y = y + ["n"]
			payable.append(choice(y))
		elif any("salvage" in str(eff) for eff in effect if not isinstance(eff,list)) and pay[1]: #((any("salvage" in str(eff) for eff in effect) and "oppturn" in effect) or
			salvage = list(gdata["p_l"])
			if pay[1] and len(salvage) >= 1:
				salvage = sorted(salvage, key=lambda e: (cdata[e].level,cdata[e].power), reverse=True)
				payable.append("AI_salvage")
				if pay[1] and len(salvage) >= 1:
					payable.append(salvage[:effect[0]])
					if "choice" in effect:
						payable.append(choice(["Hand","Stock"]))
			else:
				payable.append([""])
		elif any("change" in str(eff) for eff in effect) and pay[1]: #((any("salvage" in str(eff) for eff in effect) and "oppturn" in effect) or
			salvage = list(gdata["p_l"])
			if pay[1] and len(salvage) >= 1:
				salvage = sorted(salvage, key=lambda e: (cdata[e].level,cdata[e].power), reverse=True)
				payable.append("AI_schange")
				if pay[1] and len(salvage) >= 1:
					payable.append(salvage[:effect[0]])
			else:
				payable.append([""])
		elif ("search" in effect or "searchopp" in effect) and pay[1]:
			search = list(gdata["p_l"])
			if pay[1] and len(search) >=1:
				if "searchopp" in effect:
					search = sorted(search, key=lambda e: cdata[e].level)
				else:
					search = sorted(search, key=lambda e: (cdata[e].power, cdata[e].level), reverse=True)
				payable.append("AI_search")
				chosen = []
				if pay[1] and len(search) >= 1:
					if "EachNameC" in effect[2]:
						name = effect[2].split("_")[1:]
						for xin in search:
							if any(nn in cdata[xin].name for nn in name):
								for nn in list(name):
									if nn in cdata[xin].name:
										chosen.append(xin)
										name.remove(nn)
										break
							if len(name)==0:
								break
					else:
						chosen.extend(search[:effect[0]])
				else:
					chosen.append("")
				payable.append(chosen)
		elif ("discard" in effect or "mdiscard" in effect) and pay[1]:
			discard = list(gdata["p_l"])
			if pay[1] and len(discard) >= 1:
				discard = sorted(discard, key=lambda e: (cdata[e].power, cdata[e].level), reverse=True)
				if "invert" in gdata["effect"]:
					for cc in list(discard):
						if cdata[cc].level > 2 or cdata[cc].level <= 0:
							discard.remove(cc)
							discard.append(cc)
				payable.append("AI_discard")
				if pay[1] and len(discard) >= 1:
					payable.append(discard[:effect[1]])
				else:
					payable.append([""])
		elif pay[1] and "memorier" in effect:
			memo = self.get_stage_target(pdata, cdata, gdata)
			payable.append("AI_memorier")
			if pay[1] and len(memo) >= 1:
				memo = sorted(memo, key=lambda e: (cdata[e].power, cdata[e].level), reverse=True)
				payable.append(memo[:effect[0]])
			else:
				payable.append([""])
		elif "numbers" in effect and pay[1]:
			payable.append("AI_numbers")
			if "any" in effect:
				payable.append(choice(range(8)))
			elif "markers" in effect:
				m = 1
				if card.id in pdata[card.owner]["marker"][card.id]:
					m = len(pdata[card.owner]["marker"][card.id])+1
				payable.append(choice(range(m)))
			else:
				payable.append(choice(effect[1]))
		elif ("looktop" in effect or "looktopopp" in effect) and pay[1]:
			payable.append("AI_looktop")
			temp = []
			temppl = list(gdata["p_l"])
			if "stack" in effect:
				sst = effect[effect.index("stack")+1][0]
				for rr in range(sst):
					tt = choice(temppl)
					temppl.remove(tt)
					temp.append(tt)
			elif "waiting" in effect or "bottom" in effect:
				temp.append("b")
			elif "top" in effect or "check" in effect:
				if "hand" in effect:
					temp.append("l")
				else:
					temp.append("t")
			if "hand" in gdata["effect"]:
				temp.append(effect[0])
				temp.append(effect[effect.index("hand")+1])
				discard = self.filter_cards(temppl,card.ind,pdata,cdata,gdata)
				pick = []
				if len(discard)>0:
					pick = sample(temppl,effect[effect.index("hand")+1])
					for rx in pick:
						temp.append(rx)
				for rr in range(effect[0]-len(pick)):
					temp.append("W")
			payable.append(temp)
		elif "survive" in effect and pay[1]:
			attacker = 0
			for ind in hand:
				if self.playable(pdata, cdata,gdata, ind):
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
			print("ai",effect)
			if effect[0] > 0:
				for ind in back:
					if "Stand" in effect and cdata[ind].status != "Stand":
						continue
					if "Other" in effect and ind == card.ind:
						continue
					if "Trait" in effect and all(tt not in cdata[ind].trait_t for tt in effect[effect.index("Trait")+1].split("_")):
						continue
					pick.append(ind)
				if effect[0] > len(pick):
					for ind in pick:
						var.append(ind)
					pick = []
					for ind in center:
						if "Stand" in effect and cdata[ind].status != "Stand":
							continue
						if "Other" in effect and ind == card.ind:
							continue
						if "Trait" in effect and all(tt not in cdata[ind].trait_t for tt in effect[effect.index("Trait") + 1].split("_")):
							continue
						pick.append(ind)
					print(pick,var)
					if pick:
						if effect[0] - len(var)>=len(pick):
							temp = sample(pick, effect[0] - len(var))
							for ind in temp:
								var.append(ind)
						else:
							var.append(choice(pick))
				else:
					var.append(choice(pick))
				if len(var) < effect[0]:
					for ind in pick:
						if ind not in var:
							var.append(ind)
			if len(var)<effect[0]:
				for x in range(len(var)-effect[0]):
					var.append("")
			payable.append("AI_target")
			payable.append(var)
		elif "stand" in effect and pay[1]:
			if "swap" in effect and "this" in effect:
				payable.append("AI_target")
				if effect[0] > 0 and len(gdata["p_l"])>0:
					var = list(gdata["p_l"])
					if card in var:
						var.remove(card)
					temp = sample(var, effect[0])
					payable.append(temp)
				else:
					payable.append([""])
			elif effect[0]>0:
				memo = self.get_stage_target(pdata, cdata, gdata)
				memo = self.get_filtered_cards(memo,pdata,cdata,gdata)
				payable.append("AI_target")
				if pay[1] and len(memo) >= 1:
					memo = sorted(memo, key=lambda e: (cdata[e].power, cdata[e].level), reverse=True)
					payable.append(memo[:effect[0]])
				else:
					payable.append([""]*effect[0])
		if payable:
			confirm = payable
		return confirm
	def get_stage_target(self,pdata, cdata, gdata):
		ind = gdata["ability_trigger"].split("_")[1]
		p = ind[-1]
		if "Opp" in gdata["effect"]:
			if ind[-1] == "1" and self.player == "1":
				p = "2"
			elif ind[-1] == "2" and self.player == "2":
				p = "1"
		if "Back" in gdata["effect"]:
			cards = [s for s in pdata[p]["Back"] if s != ""]
		elif "CenterM" in gdata["effect"]:
			cards = [s for s in pdata[p]["Center"] if s != "" and pdata[p]["Center"].index(s) == 1]
		elif "Center" in gdata["effect"]:
			cards = [s for s in pdata[p]["Center"] if s != ""]
		else:
			cards = [s for s in pdata[p]["Center"] + pdata[p]["Back"] if s != ""]
		if "other" in gdata["effect"] and ind in cards:
			cards.remove(ind)
		for card in list(cards):
			for text in cdata[card].text_c:
				if text[0].startswith("[CONT]") and text[1] != 0 and text[1] > -9:
					eff = self.ab.cont(text[0])
					if eff and "no_target" in eff:
						cards.remove(card)
						break
		return cards
	def get_filtered_cards(self,cards,pdata, cdata, gdata):
		if "Name=" in gdata["effect"]:
			cards = [s for s in cards if gdata["effect"][gdata["effect"].index("Name=")+1] in cdata[s].name]
		elif "Name" in gdata["effect"]:
			cards = [s for s in cards if any(name in cdata[s].name for name in gdata["effect"][gdata["effect"].index("Name") + 1])]
		return cards
	def choose_stage_target(self,des,pdata,cdata,gdata,cards=[]):
		if not cards:
			cards = self.get_stage_target(pdata, cdata, gdata)
		choose = []
		if des:
			choose.append("AI_Stage")
		if "Waiting" in des:
			cards = [s for s in pdata[self.player]["Center"] + pdata[self.player]["Back"] if s != ""]
			if "WOther" in gdata["pay"]:
				ind = gdata["ability_trigger"].split("_")[1]
				if ind in cards:
					cards.remove(ind)
			if "WTrait" in gdata["pay"]:
				cards = [s for s in cards if any(tr in cdata[s].trait_t for tr in gdata["pay"][gdata["pay"].index("WTrait")+1].split("_"))]
			choose.append(sample(cards,gdata["pay"][gdata["pay"].index("Waiting")+1]))
		elif "Marker" in des:
			if "Zwei" in gdata["pay"]:
				if "ZMarkers" in gdata["pay"]:
					if gdata["pay"][gdata["pay"].index("ZMarkers")+1] == 0 and "ZMlower" in gdata["pay"]:
						cards = [s for s in cards if s not in pdata[s[-1]["marker"]] or (s in pdata[s[-1]["marker"]] and len(pdata[s[-1]["marker"]][s])<=0)]
				if "ZMName=" in gdata["pay"]:
					cards = [s for s in cards if gdata["pay"][gdata["pay"].index("ZMName=") + 1] in cdata[s].name_t]
				if len(cards) > 0:
					choose.append(sample(cards, gdata["pay"][gdata["pay"].index("ZMarkers")+1]))
				else:
					for x in range(gdata["pay"][gdata["pay"].index("ZMarkers")+1]):
						choose.append("")
		elif "Buff" in des:
			if len(cards)>0:
				choose.append(sample(cards,gdata["effect"][0]))
			else:
				for x in range(gdata["effect"][0]):
					choose.append("")
		return choose
	def playable(self, pdata, cdata,gdata, ind):
		level = len(pdata[self.player]["Level"])
		card = cdata[ind]
		if card.card == "Climax":
			if gdata["any_Clrclimax"][ind[-1]] or card.mcolour in pdata[ind[-1]]["colour"]:
				return True
		else:
			if card.level == 0:
				if len(pdata[ind[-1]]["Stock"]) >= card.cost_t:
					return True
			elif card.level <= level:
				if card.mcolour in pdata[ind[-1]]["colour"] or (gdata["any_ClrChname"][ind[-1]] and card.card == "Character" and any(nn in card.name for nn in gdata["any_ClrChname"][ind[-1]])):
					if card.cost <= len(pdata[ind[-1]]["Stock"]):
						return True
		return False
	def play_stage(self, pdata, cdata, gdata):
		move = []
		print(gdata["effect"])
		if "Stage" in gdata["effect"]:
			center = [s for s in pdata[self.player]["Center"] if s != ""]
			back = [s for s in pdata[self.player]["Back"] if s != ""]
			level = len([s for s in pdata[self.player]["Level"] if s != ""])
			if len(gdata["target"]) % 2 != 0:
				cid = gdata["target"][-1]
				card = cdata[cid]
				center = sorted(center, key=lambda x: cdata[x].level)
				back = sorted(back, key=lambda x: cdata[x].level)
				if card.level > level:
					if len(back) < 2:
						move.append(f'Back{pdata[self.player]["Back"].index("")}')
					else:
						move.append(f'Back{pdata[self.player]["Back"].index(back[0])}')
				elif card.level <= level:
					if len(center) < 3:
						move.append(f'Center{pdata[self.player]["Center"].index("")}')
					else:
						move.append(f'Center{pdata[self.player]["Center"].index(center[0])}')
				if not move:
					st = choice(["Center", "Back"])
					if st == "Center":
						ps = choice(range(3))
					else:
						ps = choice(range(2))
					move.append(f'{st}{ps}')
				if move:
					move.insert(0, "AI_PlayStage")
		elif "move" in gdata["effect"] and "move" in gdata["ability_doing"]:
			print(gdata["target"])
			if len(gdata["target"]) % 2 != 0:
				field = gdata["stage"]
				if "Back" in gdata["status"]:
					field = [n for n in field if "Back" in n]
				elif "Center" in gdata["status"]:
					field = [n for n in field if "Center" in n]
				if "Open" in gdata["status"]:
					field = [n for n in field if pdata[self.player][n[:-1]][int(n[-1])]==""]
				print(field)
				if field:
					move.append(choice(field))
				if move:
					move.insert(0, "AI_PlayStage")
		return move
	def mulligan(self, pdata, cdata):
		discard = []
		level = len([s for s in pdata[self.player]["Level"] if s != ""])
		for ind in pdata[self.player]["Hand"]:
			if level == 0 and (cdata[ind].level >= 1 or cdata[ind].card == "Climax"):
				discard.append(ind)
			elif cdata[ind].level>=level:
				discard.append(ind)
		return discard
	def clock(self, pdata, cdata,gdata):
		hand = pdata[self.player]["Hand"]
		level = len(pdata[self.player]["Level"])
		clock = len(pdata[self.player]["Clock"])
		center = len([s for s in pdata[self.player]["Center"] if s != ""])
		back = len([s for s in pdata[self.player]["Back"] if s != ""])
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
						if not self.playable(pdata, cdata,gdata, ind):
							clist.append(ind)
			if len(clist) > 0:
				discard = choice(clist)
			else:
				discard = "pass"
		return discard
	def level_up(self, pdata, cdata):
		level = [s for s in pdata[self.player]["Clock"] if cdata[s].card != "Climax"]
		discard = choice(level)
		return discard
	def hand_limit(self, pdata, cdata):
		discard = []
		hand = list(pdata[self.player]["Hand"])
		for inx in range(len(pdata[self.player]["Hand"][7:])):
			r = choice(hand)
			discard.append(r)
			hand.remove(r)
		return discard
	def main_play(self, pdata, cdata, gdata):
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
			elif self.playable(pdata, cdata,gdata, ind):
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
		enc = True
		encore = [s for s in pdata[self.player]["Center"] + pdata[self.player]["Back"] if s != "" and cdata[s].status == "Reverse"]
		stock = len(pdata[self.player]["Stock"])
		center = len([s for s in pdata[self.player]["Center"] if s != "" and cdata[s].status != "Reverse"])
		hand = pdata[self.player]["Hand"]
		level = len(pdata[self.player]["Level"])
		playable = []
		if gdata["no_encore"][self.player]:
			enc = False
		if enc:
			for card in list(encore):
				for text in cdata[card].text_c:
					if text[0].startswith("[CONT]") and text[1] != 0 and text[1] > -9:
						eff = self.ab.cont(text[0])
						if eff and "no_target_self" in eff:
							encore.remove(card)
							break
			if len(encore) > 0 and stock >= 3 + level:
				for ind in hand:
					if self.playable(pdata, cdata,gdata, ind):
						playable.append(ind)
				playable = [s for s in playable if cdata[s].card == "Character"]
				if center <= 0 and len(playable) <= 1 and self.player not in gdata["active"]:
					encore.sort(key=lambda x: cdata[x].power, reverse=True)
			else:
				encore = []
		else:
			encore = []
		return encore
	def main_move(self, pdata, cdata):
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
						if "cannot move to another" in item[0].lower():
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
		center = len([s for s in pdata[self.player]["Center"] if s != ""])
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
		ans = ""
		if req:#and "salvage" in effect:
			ans = "1"
		return ans
	def attack(self, pdata, cdata, gdata):
		attack = []
		if self.player == "2":
			popp = "1"
		else:
			popp = self.player
		for inx in range(3):
			if gdata["bodyguard"]:
				opp = 1
				att = ["a", "f"]
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
				counter = [s for s in hand if cdata[s].icon == "Counter" and gdata["nobackup"][pl[-1]] and gdata["counter_icon"][pl[-1]][0]]
		if len(counter) < 1:
			counter = "pass"
		return counter
