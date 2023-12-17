# cstnetdown/crawl.py

import glob
import os
import time
import zmail
from selenium import webdriver
from chromedriver_py import binary_path
from cstnetdown.bypop import save_mail

def prepare(directory):
	options = webdriver.ChromeOptions()
	prefs = {"profile.default_content_settings.popups": 0, 
			"download.default_directory": directory, 
			"profile.default_content_setting_values.automatic_downloads": 1}
	options.add_experimental_option("prefs", prefs)
	driver = webdriver.Chrome(options=options, executable_path=binary_path)
	driver.get("https://mail.cstnet.cn/")
	return driver

def download(driver, sleep=2):
	read_more_xpath = "//div[@class='toolbar f-cf j-toolbar']//span[@data-dropdown='read-more']"
	read_more_button = driver.find_element_by_xpath(read_more_xpath)
	read_more_button.click()
	time.sleep(sleep)
	download_xpath = "//li[@value='more:mailDownload']"
	download_button = read_more_button.find_element_by_xpath(download_xpath)
	download_button.click()
	time.sleep(sleep)

def next(driver, sleep=2):
	try:
		next_xpath = "//div[@class='toolbar f-cf j-toolbar']//div[@id='pagination']//a[@class='u-page-next']"
		next_button = driver.find_element_by_xpath(next_xpath)
		next_button.click()
		time.sleep(sleep)
		return True
	except Exception as e:
		print(e)
		return False

def start(driver, sleep=2, long_sleep=10):
	ended = False
	i = 0
	while True:
		try:
			while True:
				download(driver, sleep=sleep)
				i += 1
				print(i)
				if not next(driver, sleep=sleep):
					ended = True
					break
		except Exception as e:
			print(e)
			time.sleep(long_sleep)
		if ended:
			break

def convert(source_directory, target_directory, remove=True):
	files = glob.glob(os.path.join(source_directory, "*.eml"))
	files.sort(key = lambda file: os.path.getctime(file), reverse=True)
	for (i, file) in enumerate(files):
		mail = zmail.read(file)
		path = save_mail(mail, target_directory)
		print(i+1, path)
		if remove:
			os.remove(file)
