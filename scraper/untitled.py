from selenium.webdriver import Chrome
import sys, hashlib, os.path, glob
from selenium.common.exceptions import TimeoutException

path = "/Users/Sophie/Documents/bachelors-project/scraping/tutorial/files/"

files = glob.glob(path+"*.html")

driver = Chrome()
driver.set_page_load_timeout(30)
driver.set_window_size(1024, 768) # optional

for file_path in files:
	url = 'file:///' + file_path
	file_name = 'alexa_files/'+hashlib.sha224(url).hexdigest()
	if os.path.isfile(file_name):
		print 'already have', url
		continue
	print 'attempting', url
	try:
		driver.get(url)
		driver.save_screenshot(file_name) # save a screenshot to disk
	except KeyboardInterrupt:
		raise
	except:
		print sys.exc_info()[0]
		driver.quit()
		driver = Chrome()
		continue
	print 'screenshot', url