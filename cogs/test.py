import requests
from bs4 import BeautifulSoup

r = requests.get("https://steamcrackedgames.com/games/hogwarts-legacy").text
soup = BeautifulSoup(r, "html.parser")
status = soup.find_all("dd", class_="col-sm-7")

# print(status)
for x in status:
    if x.a != None:
        print(x.a.text)
