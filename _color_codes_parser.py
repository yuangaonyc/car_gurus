import requests
from bs4 import BeautifulSoup

r = requests.get("https://css-tricks.com/snippets/css/named-colors-and-hex-equivalents/")
c = r.content
soup = BeautifulSoup(c, "html.parser")

all = soup.find_all("tr")

colors=[]
for tr in all:
    try:
        color = tr.find_all("td")[1].text
        colors.append(color)
    except:
        pass