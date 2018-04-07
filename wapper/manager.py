# -*- coding: utf-8 -*-


class Manager(object):
	def __init__(self):
		self.crawlers = {}

	def addCrawler(self, name, crawler):
		self.crawlers[name] = crawler

	def start(self):
		for crawler in self.crawlers.values():
			crawler.start()
