# -*- coding: utf-8 -*-


class Match(object):
	def __init__(self):
		self.id = 0
		# 主队名字
		self.home = ''
		# 客队名字
		self.away = ''
		# 输赢盘对象
		self.moneyLine = None
		# 让分盘对象容器
		self.spreads = []
