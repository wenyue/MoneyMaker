# -*- coding: utf-8 -*-
import config
import data
from pinnacle.apiclient import APIClient
from pinnacle.enums import BetType, Boolean, TeamType


class BetManager(object):

	def __init__(self):
		self.apis = [
			APIClient(account['username'], account['password'])
			for account in config.B_ACCOUNTS
		]
		self.api_index = 0

	def log(self, *args):
		output = '\n'.join(args)
		with open('log.txt', 'a') as f:
			print >> f, output.encode('utf-8')

	def _placeBet(self, format_str, **kwargs):
		api = self.apis[self.api_index]
		account_str = u'下单账号:%s' % api.username
		self.api_index = (self.api_index + 1) % len(self.apis)
		try:
			# result = api.betting.place_bet(**kwargs)
			# result = result['status'] == 'ACCEPTED'
			result = True
		except Exception:
			result = False
		result_str = u'成功' if result else u'失败'
		self.log(format_str, account_str, result_str, '=' * 50)
		print u'下单' + result_str

	def placeBet(self, expection):
		line_id = expection.line_id
		league = data.getLeague(line_id)
		event = data.getEvent(line_id)
		line = data.getLine(line_id)
		sport_id = data.getSoccerId()
		event_id = event['id']
		period_number = line['number']
		accept_better_line = Boolean.FALSE.name

		home_str = league['homeTeamType']
		away_str = TeamType.Team2.value if home_str == TeamType.Team1.value else TeamType.Team1.value
		# home
		team = home_str
		home_hdp = expection.home_hdp
		if home_hdp is None:
			bet_type = BetType.MoneyLine.value
			spread = None
			stake = config.STACK_FACTOR / line['moneyline']['home']
			alt_line_id = None
		else:
			bet_type = BetType.Spread.value
			spread = filter(lambda spread: spread['hdp'] == home_hdp, line['spreads'])[0]
			stake = config.STACK_FACTOR / spread['home']
			alt_line_id = spread.get('altLineId', None)
		self._placeBet(
			self.format(event, line, spread, expection, 'home', stake),
			sport_id=sport_id,
			event_id=event_id,
			line_id=line_id,
			period_number=period_number,
			bet_type=bet_type,
			stake=stake,
			team=team,
			alt_line_id=alt_line_id,
			accept_better_line=accept_better_line)
		# away
		team = away_str
		away_hdp = expection.away_hdp
		if away_hdp is None:
			bet_type = BetType.MoneyLine.value
			spread = None
			stake = config.STACK_FACTOR / line['moneyline']['away']
			alt_line_id = None
		else:
			bet_type = BetType.Spread.value
			spread = filter(lambda spread: spread['hdp'] == away_hdp, line['spreads'])[0]
			stake = config.STACK_FACTOR / spread['away']
			alt_line_id = spread.get('altLineId', None)
		self._placeBet(
			self.format(event, line, spread, expection, 'away', stake),
			sport_id=sport_id,
			event_id=event_id,
			line_id=line_id,
			period_number=period_number,
			bet_type=bet_type,
			stake=stake,
			team=team,
			alt_line_id=alt_line_id,
			accept_better_line=accept_better_line)
		# draw
		stake = config.STACK_FACTOR * expection.draw_exp / line['moneyline']['draw']
		if stake < 1:
			return
		team = TeamType.Draw.value
		bet_type = BetType.MoneyLine.value
		alt_line_id = None
		self._placeBet(
			self.format(event, line, None, expection, 'draw', stake),
			sport_id=sport_id,
			event_id=event_id,
			line_id=line_id,
			period_number=period_number,
			bet_type=bet_type,
			stake=stake,
			team=team,
			alt_line_id=alt_line_id,
			accept_better_line=accept_better_line)

	def format(self, event, line, spread, expection, team, stake):
		formats = []
		odd = spread[team] if spread else line['moneyline'][team]
		bet_type = u'让球盘(%.2f)' % spread['hdp'] if spread else u'输赢盘'
		formats.append(u'比赛: "%s" VS "%s"' % (event['home'], event['away']))
		formats.append(u'方案: %s 下 %s' % (bet_type, team))
		formats.append(u'赔率: %.3f' % odd)
		formats.append(u'下注金: %.2f' % stake)
		formats.append(u'距离比赛: %d天' % expection.day_delta)
		formats.append(u'年化利率: %.2f%%' % (expection.annualized_returns * 100))
		return '\n'.join(formats)


_instance = BetManager()

_EXPORT_FUNC = [
	'placeBet',
]

for func in _EXPORT_FUNC:
	globals()[func] = getattr(_instance, func)
