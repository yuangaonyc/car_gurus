
# coding: utf-8

# In[3]:

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
def price_clean(price):
    price = price.split()[0]
    price = remove_dollar_and_comma(price)
    return price
data["price"] = data["price"].apply(price_clean).astype("int")

# extract market_price
def market_price_clean(market_price):
    market_price = market_price[market_price.index("$"):] 
    market_price = remove_dollar_and_comma(market_price)
    return market_price
data["market_price"] = data["market_price"].apply(market_price_clean).astype("int")

# extract mileage
def mileage_clean(mileage):
    mileage = mileage[mileage.index(" ")+1:]
    mileage = mileage[:mileage.index(" ")]
    mileage = mileage.replace(",","")
    return(mileage)
data["mileage"] = data["mileage"].apply(mileage_clean).astype("int")

# extract make
def make_clean(make):
    make = make.split()[1]
    if make == "Land":
        make = "Land Rover"
    return make
data["make"] = data["make"].apply(make_clean).astype("str")

# calculate rating
def dealer_rating_clean(dealer_rating):
    return star_counter(dealer_rating)
data["dealer_rating"] = data["dealer_rating"].apply(dealer_rating_clean).astype("float")
    
# extract days_listed
def days_listed_clean(days_listed):
    days_listed = days_listed.split()[0]
    if days_listed == "<":
        days_listed = 1
    return days_listed
data["days_listed"] = data["days_listed"].apply(days_listed_clean).astype("int")

# create column state
data["state"] = data["address"][:]
data["city"] = data["address"][:]

address = data["address"]
state = data["state"]
city = data["city"]

for i in range(len(state)):
    city[i] = address[i][:address[i].index(",")]
    state[i] = address[i][address[i].index(","):]
    state[i] = state[i].replace(", ","")
    
# remove address column
data = data.drop("address", 1)

# rearrange columns
cols = ["year", "make", "mileage", "dealer_rating", "days_listed", "price", "market_price", "city", "state"]
data = data[cols]

data.to_csv("clean.csv")
data

