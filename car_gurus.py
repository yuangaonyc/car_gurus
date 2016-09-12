import requests 
import pandas
from bs4 import BeautifulSoup

base_link = "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=&formSourceTag=108&newSearchFromOverviewPage=true&inventorySearchWidgetType=ADVANCED&zip=11206&distance=100&advancedSearchAutoEntities%5B0%5D.selectedEntity=&advancedSearchAutoEntities%5B1%5D.selectedEntity=&advancedSearchAutoEntities%5B2%5D.selectedEntity=&advancedSearchAutoEntities%5B3%5D.selectedEntity=&advancedSearchAutoEntities%5B4%5D.selectedEntity=&advancedSearchAutoEntities%5B5%5D.selectedEntity=&advancedSearchAutoEntities%5B6%5D.selectedEntity=&advancedSearchAutoEntities%5B7%5D.selectedEntity=&advancedSearchAutoEntities%5B8%5D.selectedEntity=&advancedSearchAutoEntities%5B9%5D.selectedEntity=&startYear=&endYear=&__multiselect_bodyTypeGroupIds=&__multiselect_fuelTypes=&minPrice=&maxPrice=&minMileage=&maxMileage=&transmission=ANY&__multiselect_installedOptionIds=&modelChanged=false&filtersModified=true&sortType=undefined&sortDirection=undefined#resultsPage={}"

price = []
mileage = []
state = []
year = []
make = []
market_price = []
rating = []
data = []

for page in range(2, 5):
	link = base_link.format(page)


	r = requests.get(link)
	c = r.content
	soup = BeautifulSoup(c, 'html.parser')

	#print(soup.prettify())

	cars = soup.find_all("div", {"class":"cg-dealFinder-result-wrap clearfix"})
	print(cars[1])

	for car in cars:
		row = {}
		title = car.find_all("span", {"itemprop":"name"})
		info = car.find_all("div", {"class":"cg-dealFinder-result-stats"})
		deal = car.find_all("div", {"class":"cg-dealFinder-result-deal" })
		review = car.find("i", {"class":"cg-icon"})

		for item in info:
			row["price"] = item.find_all("span", {"itemprop": "price"})[0].text
			row["mileage"] = item.find_all("span", {"itemprop": ""})[0].text
			address = item.find_all("p")[2].text.replace("Location: ", "")
			no_borough = address[address.index(",")+2:]
			row["state"] = no_borough[:no_borough.index(" ")]

		for item in title:
			row["year"] = item.text[0:4]
			no_year = item.text[item.text.index(" ")+1:]
			row["make"] = no_year[:no_year.index(" ")]
			if row["make"] == "Land":
				row["make"] = "Land Rover"

		for item in deal:
			nationalAvg = item.find_all("span",{"class": "nationalAvg"})[0].text
			row["market_price"] = nationalAvg[nationalAvg.index("of")+3:]
		
		short_review = str(review)[48:]
		try:
			star = short_review[:short_review.index(" ")]
		except ValueError:
			star = ""
		row["dealer_rating"] = star

		data.append(row)

	print("{} scrape success!".format(link))
	#print(data)
	# print(price)
	# print(mileage)
	# print(state)
	# print(year)
	# print(make)
	# print(market_price)
	# print(rating)

df = pandas.DataFrame(data)
print(df)
df.to_csv("output.csv")
print("output success!")