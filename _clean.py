
# coding: utf-8

# In[1]:

import pandas as pd
 
data = pd.read_csv("output.csv")

def remove_dollar_and_comma(string):
    string = string.replace("$","")
    string = string.replace(",","")
    return string

def star_counter(string):
    num = 5 - string.count("star_disabled") - 0.5 * string.count("star_half")
    return num

# extract year from title
data["year"] = data["year"].str[:4]
data["year"] = data["year"].astype("int")

# extract price
price = data["price"]
for i in range(len(price)):
    price[i] = price[i].split()[0]
    price[i] = remove_dollar_and_comma(price[i])
price = price.astype("int")
    
# extract mileage
mileage = data["mileage"]
for i in range(len(mileage)):
    mileage[i] = mileage[i][mileage[i].index(" ")+1:]
    mileage[i] = mileage[i][:mileage[i].index(" ")]
    mileage[i] = mileage[i].replace(",","")
mileage = mileage.astype("int")

# extract market_price
market_price = data["market_price"]
for i in range(len(market_price)):
    market_price[i]= market_price[i][market_price[i].index("$"):] 
    market_price[i] = remove_dollar_and_comma(market_price[i])
market_price = market_price.astype("int")

# extract make
make = data["make"]
for i in range(len(make)):
    make[i] = make[i].split()[1]
    if make[i] == "Land":
        make[i] = "land Rover"
make = make.astype("str")

# calculate rating
dealer_rating = data["dealer_rating"]
for i in range(len(dealer_rating)):
    dealer_rating[i] = star_counter(dealer_rating[i])
dealer_rating = dealer_rating.astype("float")
    
# extract days_listed
days_listed = data["days_listed"]
for i in range(len(days_listed)):
    days_listed[i] = days_listed[i].split()[0]
    if days_listed[i] == "<":
        days_listed[i] = 1
days_listed = days_listed.astype("int")

# create column state
data["state"] = data["address"][:]
data["city"] = data["address"][:]

address = data["address"]
state = data["state"]
city = data["city"]

for i in range(len(state)):
    city[i] = address[i][:address[i].index(",")]
    state[i] = address[i][address[i].index(","):]
    state[i] = state[i].replace(",","")
    
# remove address column
data = data.drop("address", 1)

# rearrange columns
cols = ["year", "make", "mileage", "dealer_rating", "days_listed", "price", "market_price", "city", "state"]
data = data[cols]

data.to_csv("clean.csv")

