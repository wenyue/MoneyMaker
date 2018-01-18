# -*- coding: utf-8 -*-
import time
import datetime
import config
from exception import NetworkException
import data
import betting
from expection import Expection


class MoneyMaker(object):
	def __init__(self):
		pass

	def run(self):
		while True:
			# main loop
			try:
				lines = data.getAvalableLines()
			except NetworkException:
				time.sleep(3.0)
				continue

			# print a message
			timestamp = datetime.datetime.now().strftime('%H:%M:%S')
			print '(%s) process: %d' % (timestamp, len(lines))

			# find make money chances
			expections = [Expection(line) for line in lines]
			[betting.placeBet(exp) for exp in expections if exp.is_valid]

			# sleep
			time.sleep(8.0)


if __name__ == '__main__':
	mm = MoneyMaker()
	mm.run()
