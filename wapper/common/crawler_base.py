# -*- coding: utf-8 -*-

from abc import abstractmethod
from threading import Thread
import time


class CrawlerBase(object):
	UPDATE_INTERVAL = 500

	def __init__(self):
		self.thread = None

	def start(self):
		if self.thread is None:
			self.thread = Thread(target=self.__run)
			self.thread.start()

	def __run(self):
		self.init()
		while True:
			self.update()
			time.sleep(self.UPDATE_INTERVAL)

	@abstractmethod
	def init(self):
		pass

	@abstractmethod
	def update(self):
		pass
