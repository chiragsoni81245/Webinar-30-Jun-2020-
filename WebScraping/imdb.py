import requests
from bs4 import BeautifulSoup as bs
import re
import csv

movies = [] # [ [], [], [], [] ] 

for page in range(5):
	
	response = requests.get("https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start={}&ref_=adv_nxt".format( page*50+1 ))

	soup = bs( response.text, "html.parser" )

	list_movies = soup.find("div", {"class":"lister-list"})

	content_elements = list_movies.find_all("div", {"class":"lister-item-content"})


	for element in content_elements:

		title = element.find("h3", {"class": "lister-item-header"}).a.text.strip()
		year = element.find("span", {"class":"lister-item-year"}).text.strip()
		year = re.search("([0-9]{4})", year).groups()[0]
		genre = element.find("span", {"class":"genre"}).text.strip()
		runtime = element.find("span", {"class":"runtime"}).text.strip()
		rating = element.find("div", {"class":"ratings-imdb-rating"})["data-value"].strip()

		movies.append( [ title, year, genre, runtime, rating ] )

filtered_movies =[]

for movie in movies:

	if "Horror" in movie[2]:
		filtered_movies.append(movie)


with open("imdb_data.csv","w") as file:

	writer = csv.writer( file )

	writer.writerow( ["Title","Year","Genre","Runtime", "Rating"] )

	writer.writerows( filtered_movies )
