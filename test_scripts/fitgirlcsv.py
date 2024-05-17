import sys
import time
from bs4 import BeautifulSoup
import csv
import requests
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter("ignore", InsecureRequestWarning)

fitgirlSiteUrl = "fitgirl-repacks.site"


def getPageNumbers():
    url = "https://" + fitgirlSiteUrl + "/all-my-repacks-a-z/"
    payload = {}
    headers = {}
    html_doc = requests.request("GET", url, json=payload, headers=headers, verify=False)
    # print(response.text)
    soup = BeautifulSoup(html_doc.text, "html.parser")
    footerFind = soup.find("ul", class_="lcp_paginator")
    totalPages = int(footerFind.find_all("li")[-2].getText())
    return totalPages


# Actually scrape the page for links/text
def getPageGameList(pageNumber):
    url = (
        "https://"
        + fitgirlSiteUrl
        + "/all-my-repacks-a-z/?lcp_page0="
        + str(pageNumber)
        + "#lcp_instance_0"
    )
    payload = {}
    headers = {}
    html_doc = requests.request("GET", url, json=payload, headers=headers, verify=False)
    # print(response.text)
    soup = BeautifulSoup(html_doc.text, "html.parser")
    listFindUL = soup.find("ul", class_="lcp_catlist")
    # listContents = footerFind.find_all('li')
    listOfGames = []
    for a in listFindUL.find_all("a", href=True):
        # print("URL:", a['href'], 'Text: ', a.getText())
        text = a.getText()

        # Strip Unicode text out by encoding bytes with ascii and "ignore" errors, then re-encode it back to text
        textEnc = text.encode("ascii", "ignore")
        textCleaned = textEnc.decode()
        listOfGames.append(
            {"URL": a["href"], "Name": textCleaned, "Page": str(pageNumber)}
        )

    # for element in listContents:
    # 	href = element.find('ul', class_='lcp_catlist')
    return listOfGames


# print(soup.prettify())
def run():
    # Try to open CSV for writing, error if fails
    try:
        myFile = open("fitgirl.csv", "w", newline="")
    except PermissionError:
        print("Could not open FitgirlToCSV_Output.csv for writing, exiting...")
        sys.exit(1)

    if myFile.writable():
        print("Confirmed FitgirlToCSV_Output.csv is writable, continuing...")
    else:
        print("Could not open FitgirlToCSV_Output.csv for writing, exiting...")
        sys.exit(1)

    # get total page numbers
    totalPages = getPageNumbers()

    # Make actual list of games, put into a list of dicts
    gameList = []
    for i in range(1, totalPages):
        gameList.extend(getPageGameList(i))
        # Sleep at least *some* time between requesting pages...
        time.sleep(0.25)
    # for i in range(1,totalPages)
    # print(gameList)

    # write list of dicts to CSV
    writer = csv.DictWriter(myFile, fieldnames=["Name", "URL", "Page"])
    writer.writeheader()
    writer.writerows(gameList)
    myFile.close()


run()
