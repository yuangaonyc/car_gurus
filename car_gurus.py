from bs4 import BeautifulSoup
from selenium import webdriver
import pandas
import os

link = "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePage_false_0&formSourceTag=104&entitySelectingHelper.selectedEntity=&zip=11206"
pages = 10
data = []

chromedriver = "C:\Users\NERO\Downloads/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get(link)
assert "CarGurus" in driver.title

for i in range(pages):

	html = driver.page_source
	soup = BeautifulSoup(html, "html.parser")
	cars = soup.find_all("div", {"class":"ft-car cg-dealFinder-result-wrap clearfix"})

	for car in cars:
		row = {}
		title = car.find_all("h4", {"class":"cg-dealFinder-result-model"})
		info = car.find_all("div", {"class":"cg-dealFinder-result-stats"})
		deal = car.find_all("div", {"class":"cg-dealFinder-result-deal" })

		for item in info:
			pre_price = item.find_all("span", {"class": "cg-dealFinder-priceAndMoPayment"})[0].text
			row["price"] = pre_price[pre_price.index("$"):] 
			row["mileage"] = item.find_all("p")[1].text
			row["address"] = item.find_all("span",{"class":"cg-dealFinder-result-stats-distance"})[0].text
			row["dealer_rating"] = str(item.find_all("span", {"class": "cg-dealFinder-result-sellerRatingValue"})[0])
			
		for item in title:
			row["year"] = title[0].text
			row["make"] = title[0].text
		
		for item in deal:
			row["market_price"] = item.find_all("p",{"class": "cg-dealfinder-result-deal-imv"})[0].text
			row["days_listed"] = item.find_all("p", {"class": "cg-dealfinder-result-deal-imv"})[1].text
		
		data.append(row)

	print("page {} scraping finished!".format(i+1))
	next_page = driver.find_element_by_class_name("nextPageElement")
	next_page.click()
	assert "CarGurus" in driver.title

driver.close()
df = pandas.DataFrame(data)
df.to_csv("output.csv", encoding="ascii")
print("data extraction success!")