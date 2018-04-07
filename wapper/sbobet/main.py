# -*- coding: utf-8 -*-

if __name__ == '__main__':
	import sys
	sys.path.append('../../')

from selenium import webdriver
from items import Match
from crawlers.crawler_base import CrawlerBase


class Crawler(CrawlerBase):
	def init(self):
		self.driver = webdriver.Chrome('../driver/chromedriver.exe')
		self.driver.get('https://www.sbobet.com/euro/football')

	def update(self):
		print 'wenyue'


if __name__ == '__main__':
	crawler = Crawler()
	crawler.start()
