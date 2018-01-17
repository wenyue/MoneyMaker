# -*- coding: utf-8 -*-
import config
from exception import NetworkException
from pinnacle.apiclient import APIClient


class DataManager(object):

	def __init__(self):
		account = config.L_ACCOUNTS[0]
		self.api = APIClient(account['username'], account['password'])
		self.soccer_id = self._getSoccerId()
		self.line2league = {}
		self.line2event = {}
		self.odds_last = None
		self.fixtures_last = None
		self.leagues = {}
		self.events = {}
		self.lines = {}
		self.updateLeagues()

	def _getSoccerId(self):
		sport_ids = self.api.reference_data.get_sports()
		for sport in sport_ids:
			if sport['name'] == 'Soccer':
				return sport['id']

	def getSoccerId(self):
		return self.soccer_id

	def updateLeagues(self):
		try:
			leagues = self.api.reference_data.get_leagues(self.soccer_id)
		except Exception:
			raise NetworkException()

		for league in leagues:
			league_id = league['id']
			self.leagues[league_id] = league

	def getLeague(self, line_id):
		league_id = self.line2league[line_id]
		return self.leagues[league_id]

	def updateEvents(self):
		try:
			fixtures = self.api.market_data.get_fixtures(
				self.soccer_id, since=self.fixtures_last)
		except Exception:
			raise NetworkException()
		self.fixtures_last = fixtures['last'] - 1
		return self._mergeEvents(fixtures)

	def _mergeEvents(self, data):
		events = []
		leagues = data['league']
		for league in leagues:
			events = league['events']
			for event in events:
				if type(event) is int:
					continue
				event_id = event['id']
				self.events[event_id] = event
				events.append(event_id)
		return events

	def isRunningEvent(self, event_id):
		return self.events.get(event_id, {'liveStatus': 1}).get('liveStatus', 0) == 1

	def getEvent(self, line_id):
		event_id = self.line2event[line_id]
		return self.events[event_id]

	def updateLines(self):
		try:
			odds = self.api.market_data.get_odds(self.soccer_id, since=self.odds_last)
		except Exception:
			raise NetworkException()
		self.odds_last = odds['last'] - 1
		return self._mergeLines(odds)

	def _mergeLines(self, data):
		lines = []
		leagues = data['leagues']
		for league in leagues:
			league_id = league['id']
			events = league['events']
			for event in events:
				event_id = event['id']
				periods = event['periods']
				for line in periods:
					line_id = line['lineId']
					self.line2league[line_id] = league_id
					self.line2event[line_id] = event_id
					self.lines[line_id] = line
					lines.append(line_id)
		return lines

	def getLine(self, line_id):
		return self.lines[line_id]

	def isAvalableLine(self, line_id):
		event_id = self.line2event[line_id]
		if self.isRunningEvent(event_id):
			return False
		line = self.lines[line_id]
		if 'moneyline' not in line or 'spreads' not in line:
			return False
		return True

	def getAvalableLines(self):
		self.updateEvents()
		lines = self.updateLines()
		return filter(self.isAvalableLine, lines)


_instance = DataManager()


_EXPORT_FUNC = [
	'getAvalableLines',
	'getSoccerId',
	'getLeague',
	'getEvent',
	'getLine',
]

for func in _EXPORT_FUNC:
	globals()[func] = getattr(_instance, func)
