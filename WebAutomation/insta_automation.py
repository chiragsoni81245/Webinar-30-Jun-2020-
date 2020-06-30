from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import csv

browser = webdriver.Chrome(executable_path="/home/chirag/Webinar( 30 Jun 2020 )/WebAutomation/chromedriver")

browser.maximize_window()  

browser.get("https://www.instagram.com/")


def wait( css_selector ):
	try:
		WebDriverWait( browser, 20 ).until( EC.visibility_of_element_located( (By.CSS_SELECTOR, css_selector) ) )
	except  TimeoutException:
		print("time out in wait of {}, Please Connect to a Fast internet".format(css_selector))
		exit()


def login( username, password ):
	wait( "input[name='username']" )
	browser.find_element_by_name("username").send_keys(username)
	browser.find_element_by_name("password").send_keys(password)
	browser.find_element_by_css_selector("button.L3NKy[type='submit']").click()

#------------------------------------------------------ 
with open("/home/chirag/credentials/insta.txt","r") as credential_file:
	username = credential_file.readline().strip("\n")
	password = credential_file.readline().strip("\n")

login( username, password )
# -----------------------------------------------------

wait("div.cmbtv")
browser.find_element_by_class_name("cmbtv").click()


browser.get("https://www.instagram.com/{}/".format(username))

def find_all_follow( what ):
	wait( "span.g47SY" )
	no_follow = int( browser.find_element_by_css_selector("a[href='/{}/{}/'] span".format(username,what)).text )
	browser.find_element_by_css_selector("a[href='/{}/{}/']".format(username,what)).click()
	wait( "div.PZuss" )
	list_len = len( browser.find_elements_by_css_selector("li.wo9IH") )
	while list_len!=no_follow:
		browser.execute_script('document.getElementsByClassName("isgrP")[0].scrollTop = document.getElementsByClassName("isgrP")[0].scrollHeight;')
		list_len = len( browser.find_elements_by_css_selector("li.wo9IH") )

	follow_handle_html = browser.find_elements_by_css_selector("div.d7ByH > a")
	follow = set( [ i.text.strip() for i in follow_handle_html ] )

	browser.find_element_by_css_selector("div.WaOAr > button.wpO6b").click()

	return follow


def follow():
	wait( "span.g47SY" )
	browser.find_element_by_css_selector("a[href='/{}/followers/']".format(username)).click()
	no_followers = int( browser.find_element_by_css_selector("a[href='/{}/followers/'] span".format(username)).text )
	wait( "div.PZuss" )
	list_len = len( browser.find_elements_by_css_selector("li.wo9IH") )
	while list_len!=no_followers:
		browser.execute_script('document.getElementsByClassName("isgrP")[0].scrollTop = document.getElementsByClassName("isgrP")[0].scrollHeight;')
		list_len = len( browser.find_elements_by_css_selector("li.wo9IH") )

	follow_buttons = browser.find_elements_by_css_selector("button.y3zKF")

	for button in follow_buttons:
		button.click()

	browser.find_element_by_css_selector("div.WaOAr > button.wpO6b").click()


def unfollow():
	followers = find_all_follow("followers")

	wait( "span.g47SY" )
	browser.find_element_by_css_selector("a[href='/{}/following/']".format(username)).click()
	no_following = int( browser.find_element_by_css_selector("a[href='/{}/following/'] span".format(username)).text )

	wait( "div.PZuss" )
	list_len = len( browser.find_elements_by_css_selector("li.wo9IH") )
	while list_len!=no_following:
		browser.execute_script('document.getElementsByClassName("isgrP")[0].scrollTop = document.getElementsByClassName("isgrP")[0].scrollHeight;')
		list_len = len( browser.find_elements_by_css_selector("li.wo9IH") )


	persons = browser.find_elements_by_css_selector("div.PZuss > li.wo9IH") #_8A5w5


	for person in persons:
		handle = person.find_element_by_css_selector("a.FPmhX").text.strip()
		print( handle, followers )
		if handle not in followers:
			unfollow_button = person.find_element_by_css_selector("button._8A5w5")
			unfollow_button.click()
			wait("button.-Cab_")
			confirm_btn = browser.find_element_by_css_selector("button.-Cab_")
			confirm_btn.click()

	browser.find_element_by_css_selector("div.WaOAr > button.wpO6b").click()

	following = find_all_follow("following")


def followers_vs_following():
	followers = find_all_follow("followers")
	following = find_all_follow("following")

	with open("Insta_data.csv","w") as file:
		writer = csv.writer( file )
		writer.writerow( ["handle","follower","following"] )
		for person in followers | following:
			writer.writerow( [ person, [u'\u2713', u"\u2718"][ person not in followers ], [u'\u2713', u"\u2718"][ person not in following ] ] )



# followers_vs_following()
follow()
unfollow()

# browser.quit()