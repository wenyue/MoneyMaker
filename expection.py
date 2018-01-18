# -*- coding: utf-8 -*-
import math
import data
import config
from datetime import datetime


class ExpToken(object):
	def __init__(self, exp, hdp, draw_factor):
		self.exp = exp
		self.hdp = hdp
		self.ddraw = exp * draw_factor


class Expection(object):

	def __init__(self, line_id):
		self.line_id = line_id
		self.is_valid = False
		self.annual_returns = 0
		self.home_hdp = None
		self.away_hdp = None
		self.draw_exp = 0
		self.day_delta = self._getDayDelta()
		self._initWithLine()

	def _getDayDelta(self):
		event = data.getEvent(self.line_id)
		start = datetime.strptime(event['starts'], "%Y-%m-%dT%H:%M:%SZ")
		now = datetime.utcnow()
		return (start - now).days

# yapf: disable
	def _initWithLine(self): # noqa
		line = data.getLine(self.line_id)
		moneyline = line['moneyline']
		spreads = line['spreads']
		homes = []
		aways = []
		# moneyline
		homes.append(ExpToken(1.0 / moneyline['home'], None, 0.0))
		aways.append(ExpToken(1.0 / moneyline['away'], None, 0.0))
		# spread
		for spread in spreads:
			hdp = spread['hdp']
			home = spread['home']
			away = spread['away']
			if hdp == 0:
				homes.append(ExpToken(1.0 / home, hdp, 1.0))
				aways.append(ExpToken(1.0 / away, hdp, 1.0))
			elif hdp == 0.25:
				homes.append(ExpToken(1.0 / home, hdp, 1.0 + (home - 1.0) / 2))
				aways.append(ExpToken(1.0 / away, hdp, 0.5))
			elif hdp == -0.25:
				homes.append(ExpToken(1.0 / home, hdp, 0.5))
				aways.append(ExpToken(1.0 / away, hdp, 1.0 + (away - 1.0) / 2))
			elif hdp == 0.5:
				homes.append(ExpToken(1.0 / home, hdp, home))
				aways.append(ExpToken(1.0 / away, hdp, 0.0))
			elif hdp == -0.5:
				homes.append(ExpToken(1.0 / home, hdp, 0.0))
				aways.append(ExpToken(1.0 / away, hdp, away))
			elif hdp == 0.75:
				homes.append(ExpToken(1.0 / home, hdp, home))
				away = 1.0 + (away - 1.0) / 2
				aways.append(ExpToken(1.0 / away, hdp, 0.0))
			elif hdp == -0.75:
				home = 1.0 + (home - 1.0) / 2
				homes.append(ExpToken(1.0 / home, hdp, 0.0))
				aways.append(ExpToken(1.0 / away, hdp, away))
			elif hdp >= 1:
				homes.append(ExpToken(1.0 / home, hdp, home))
			elif hdp <= -1:
				aways.append(ExpToken(1.0 / away, hdp, away))
			else:
				raise KeyError()

		draw = moneyline['draw']
		min_exp = float('inf')
		for hToken in homes:
			for aToken in aways:
				draw_exp = max(0, 1.0 - hToken.ddraw - aToken.ddraw) / draw
				exp = hToken.exp + aToken.exp + draw_exp
				if exp < min_exp:
					min_exp = exp
					self.home_hdp = hToken.hdp
					self.away_hdp = aToken.hdp
					self.draw_exp = 1.0 - hToken.ddraw - aToken.ddraw
		win_rate = (1.0 + min_exp * config.RAKEBACK_RATE) / min_exp
		self.annual_returns = math.pow(win_rate, 365.0 / (self.day_delta + 1)) - 1.0
		if self.annual_returns > config.ANNUAL_RETURNS and win_rate > 1.0 + config.MIN_PROFIT_RATE:
			self.is_valid = True

# yapf: enable
