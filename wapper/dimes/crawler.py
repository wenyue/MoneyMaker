# -*- coding: utf-8 -*-

import os
from selenium import webdriver
from wapper.common.crawler_base import CrawlerBase


class Crawler(CrawlerBase):
	def init(self):
		chromeOptions = webdriver.ChromeOptions()
		path = os.path.join(os.path.dirname(__file__), os.pardir)
		self.driver = webdriver.Chrome('%s/common/chromedriver.exe' % path, chrome_options=chromeOptions)

	def update(self):
		self.driver.get('https://www.5dimes.eu/livelines/livelines.aspx')
		sportsList = self.driver.find_element_by_class_name('SportsList')
		sports = sportsList.find_elements_by_class_name('Sport')
		soccerIndex = [sport.text for sport in sports].index('Soccer')
		sportSubTypes = sportsList.find_elements_by_class_name('SportSubTypes')
		soccersList = sportSubTypes[soccerIndex].find_elements_by_tag_name('input')
		for soccer in soccersList:
			self.driver.execute_script("arguments[0].click();", soccer)
		lineFormat = self.driver.find_element_by_id('lnkEU')
		lineFormat.click()
