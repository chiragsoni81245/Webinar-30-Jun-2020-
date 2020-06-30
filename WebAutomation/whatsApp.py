from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import sys

name = sys.argv[1]
file_path = sys.argv[2]


browser = webdriver.Chrome(executable_path="/home/chirag/Webinar( 30 Jun 2020 )/WebAutomation/chromedriver")

browser.maximize_window()

browser.get("https://web.whatsapp.com/")

def wait( css_selector ):
	try:
		WebDriverWait( browser, 20 ).until( EC.visibility_of_element_located( (By.CSS_SELECTOR, css_selector) ) )
	except  TimeoutException:
		print("time out in wait of {}, Please Connect to a Fast internet".format(css_selector))
		exit()


wait("div._3FRCZ")		
# Type Name in Search
browser.find_element_by_css_selector("div._3FRCZ").send_keys( name )

search_result_list = browser.find_elements_by_css_selector("div.-GlrD > div._210SC")

for person in search_result_list:
	try:
		person_name = person.find_element_by_css_selector("span.matched-text")
		# print( person, person_name)
		if person_name.text==name:
			print( person_name.text )
			person.click()
			break
	except: 
		pass

message_box = browser.find_elements_by_css_selector("div._3FRCZ")[1]

with open(file_path, "r") as file:
	line = file.readline()
	while line!="":
		abv,meaning = line.split("|")
		message_box.send_keys( "{} = {}".format(abv,meaning) )
		message_box.send_keys( Keys.ENTER )
		line = file.readline()

# browser.quit()


