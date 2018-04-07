# -*- coding: utf-8 -*-

from manager import Manager
m = Manager()


def addCrawler(name, modelName):
	model = __import__('%s.crawler' % modelName, globals())
	m.addCrawler(name, model.crawler.Crawler())


addCrawler('5dimes', 'dimes')

start = m.start
