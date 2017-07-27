from selenium.webdriver import Chrome
import sys, hashlib, os
from selenium.common.exceptions import TimeoutException
from PIL import Image

class Screenshooter():

	def __init__(self):
		self.driver = Chrome()
		self.driver.set_page_load_timeout(45)
		self.driver.set_window_size(1024, 768)

	def screenshot(self, url):
		file_path = 'screenshots/'+hashlib.sha224(url).hexdigest()
		if os.path.isfile(file_path+'.jpg'):
			print 'already have', url
			os.remove(file_path+'.jpg')
		print 'attempting', url
		try:
			self.driver.get(url)
			self.driver.save_screenshot(file_path+'.png') # save a screenshot to disk
			self.convert_to_jpg(file_path)
		except:
			print sys.exc_info()
			self.driver.quit()
			#self.sdriver = Chrome()
			raise Exception()
		print 'screenshot', url
		return file_path+'.jpg'

	def convert_to_jpg(self, path):
		im = Image.open(path + '.png')
		rgb_im = im.convert('RGB')
		rgb_im.save(path+'.jpg')
		os.remove(path+'.png')


	def close(self):
		self.driver.quit()