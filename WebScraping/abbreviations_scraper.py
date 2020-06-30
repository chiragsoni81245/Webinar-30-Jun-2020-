import requests
from bs4 import BeautifulSoup as bs 

response = requests.get("https://www.webopedia.com/quick_ref/textmessageabbreviations.asp")

soup = bs( response.text, "html.parser" )

tbody = soup.find("table",{"class":"style5"}).tbody

with open("msg.txt","w") as file:
	for tr in tbody.find_all("tr"):
		tds = tr.find_all("td")
		if len(tds)==2:
			try:
				abv = tds[0].p.text.strip()
			except :
				abv = tds[0].text.strip()

			meaning = tds[1].p.text.strip()
			
			file.write( "{}|{}\n".format( abv, meaning  ) )


