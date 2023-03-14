import requests
import time
import os
import csv
# Used to search using our default webbrowser
import webbrowser

import pandas as pd

from requests_html import HTMLSession
from bs4 import BeautifulSoup
from datetime import datetime
from csv import writer

# Class Variable
previousVol = 0

# Used for the whileTrueStock
def repetitionsFunc(stockName, interval, repetitions):
    global previousVol

    session = HTMLSession()
    requests = session.get("https://finance.yahoo.com/quote/{stockName}/history?p={stockName}".format(stockName = stockName)).text

    soup = BeautifulSoup(requests, "html5lib")

    newVolume = float((soup.find("tr", {"class" : "BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"})).findAll("td")[6].text.replace(",", ""))

    high = soup.find("tr", {"class" : "BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"}).findAll("td")[2].text
    low = soup.find("tr", {"class" : "BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"}).findAll("td")[3].text

    # Current Stock Price update
    currentPrice = soup.find("tr", {"class" : "BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"}).findAll("td")[4].text

    if previousVol == 0 or previousVol == 0.0:
        # Current Volume
        previousVol = float((soup.find("tr", {"class" : "BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"})).findAll("td")[6].text.replace(",", ""))
    else:
        # Current Volume
        newVolume = float((soup.find("tr", {"class" : "BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"})).findAll("td")[6].text.replace(",", "")) - previousVol

    with open("{workingDirectory}/ptrFinance/repetitionCSV.csv".format(workingDirectory = os.getcwd()).replace("\\", "/"), "a") as f:
        writer = csv.writer(f)

        # Stock Price, Volume Per Min
        writer.writerow([currentPrice, newVolume, high, low])

        previousVol = float((soup.find("tr", {"class" : "BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"})).findAll("td")[6].text.replace(",", ""))

# Function used to gather main information
def stockInformation(url, url1, url2):
    # Requests is used to get the HTML page that we need to parse over
    session = HTMLSession()
    page = session.get(url).text

    soup = BeautifulSoup(page, "html5lib")

    # For EPS
    session1 = HTMLSession()
    page1 = session1.get(url1).text

    soup1 = BeautifulSoup(page1, "html5lib")

    # For High and Low
    session2 = HTMLSession()
    page2 = session2.get(url2).text

    soup2 = BeautifulSoup(page2, "html5lib")

    # Open Price
    openPrice = soup.find("table", class_="W(100%)").findAll("td", {"class" : "Ta(end) Fw(600) Lh(14px)"})[1].text

    # High
    high = soup2.find("table", {"data-test" : "historical-prices"}).find("tbody").find("tr", {"class" : "BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"}).findAll("td", {"class" : "Py(10px) Pstart(10px)"})[1].find("span").text

    # Low
    low = soup2.find("table", {"data-test" : "historical-prices"}).find("tbody").find("tr", {"class" : "BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"}).findAll("td", {"class" : "Py(10px) Pstart(10px)"})[2].find("span").text

    # Stock Price
    stockPrice = soup.find("fin-streamer", class_="Fw(b) Fz(36px) Mb(-4px) D(ib)").text
    #print(stockPrice)

    # Stock Change
    stockChange = soup.find("fin-streamer", class_="Fw(500) Pstart(8px) Fz(24px)").span.text
    #print(stockChange)

    # Stock Percentage Change
    StockPercentageChange = soup.find("fin-streamer", {"class" :"Fw(500) Pstart(8px) Fz(24px)", "data-field" : "regularMarketChangePercent"}).span.text[1:-1]
    floatStockChange = float(StockPercentageChange[:-1])
    #print(floatStockChange)

    # EPS
    eps = soup1.find("div", {"class" : "group group--elements left"}).findAll("ul", {"class" : "list list--kv list--col50"})[0].findAll("li", {"class" : "kv__item"})[9].find("span", {"class" : "primary"}).text[1:]

    if soup.find("td", {"class" : "Ta(end) Fw(600) Lh(14px)", "data-test" : "ONE_YEAR_TARGET_PRICE-value"}) != None:
        # Investor Confidence (Price in One Year)
        investorConfidence = soup.find("td", {"class" : "Ta(end) Fw(600) Lh(14px)", "data-test" : "ONE_YEAR_TARGET_PRICE-value"}).text
        #print(investorConfidence)
    else:
        investorConfidence = None

    volume = float((soup.find("fin-streamer", {"data-field" : "regularMarketVolume"}).text).replace(",", ""))

    # stockPrice,stockChange,floatStockChange,investorConfidence,volume,volumePerMinute,month,day,year
        # It's important to remember that the stockChange and floatStockChange are all based on 1 minute transactions.
        # This is to better predict end of the day stock values
            # So as to make sure that the values aren't locked in on the moment, but rather a general trend over the day
    return {"Open" : openPrice, "High" : high, "Low" : low, "Stock Price (Close)" : stockPrice, "Stock Change" : stockChange, "Float Stock Change" : floatStockChange, "1 Year Val (Expected)" : investorConfidence, "Volume" : volume, "Month" : datetime.now().month, "Day" : datetime.now().day, "Year" : datetime.now().year, "EPS" : eps}

# Function used to gather historic details of a company
def stockInformationHistoric(url):
    session = HTMLSession()
    requests = session.get(url).text

    soup = BeautifulSoup(requests, "html5lib")

    date = [x.span.text for x in soup.findAll("td", class_="Py(10px) Ta(start) Pend(10px)")][::-1]

    if soup.findAll("td", class_="Py(10px) Pstart(10px)") != []:
        volume = [x.span.text for x in soup.findAll("td", class_="Py(10px) Pstart(10px)")][::-1]

    stockPrice = []
    newVolume = []

    for x in range(0, len(volume), 6):
        stockPrice.append(float(volume[x+2]))
        newVolume.append(int(volume[x].replace(",", "")))

    returnArray = []

    # stockPrice,stockChange,floatStockChange,investorConfidence,volume,volumePerMinute,month,day,year
        # It's important to remember that the stockChange and floatStockChange are all based on 1 minute transactions.
        # This is to better predict end of the day stock values
            # So as to make sure that the values aren't locked in on the moment, but rather a general trend over the day
    for x in range(len(date)):
        if x - 1 >= 0:
            returnArray.append([stockPrice[x], (float(stockPrice[x]) - float(stockPrice[x-1])), (100*(float(stockPrice[x]) - float(stockPrice[x-1])) / float(stockPrice[x-1])), None, newVolume[x], datetime.month, datetime.day, datetime.year])
        else:
            returnArray.append([stockPrice[x], None, None, None, newVolume[x], datetime.month, datetime.day, datetime.year])

    return returnArray

# Function used to return up to minute stock update
def whileTrueStock(stockName, interval = 1, repetitions = -1):
    # Infinite Repetitions
    if repetitions == -1:
        while datetime.now().hour != "21":
            repetitionsFunc(stockName, interval, repetitions)

            # The time sleep function below is used to allow enough time to pass to for the update to be useful
            time.sleep(interval * 1)
    else:
        for x in range(repetitions):
            repetitionsFunc(stockName, interval, repetitions)

            # The time sleep function below is used to allow enough time to pass to for the update to be useful
            time.sleep(interval * 1)

    returnPD = pd.read_csv("{workingDirectory}/ptrFinance/repetitionCSV.csv".format(workingDirectory = os.getcwd()).replace("\\", "/"))

    # Used to clear the repetitionCSV
    with open("{workingDirectory}/ptrFinance/repetitionCSV.csv".format(workingDirectory = os.getcwd()).replace("\\", "/"), "w") as f:
        writer = csv.writer(f)

        # Feature Names
        writer.writerow(["stockPrice","volumePerMinute","high","low"])

    return returnPD

# Function used to get the most recent news articles - O(1)
def returnMostRecentArticles(stockName):
    # Requests is used to get the HTML page that we need to parse over
    session = HTMLSession()
    # Link used to contain the google finance page of the chosen stock
    page = session.get("https://www.marketwatch.com/investing/stock/{stockName}".format(stockName = stockName)).text

    soup = BeautifulSoup(page, "html5lib")
    # The variable below contains the table for the table containing the news
    newsTable = soup.findAll("div", {"class" : "article__content"})
    # Return used to contain the artile headlines of the markets
    return [x.find("a", {"class" : "link"}).text.replace("\n", "").strip() for x in newsTable]

# Function used to gather the links of the news articles - O(1)
    # It's important to note that the links returned from this function are differ somewhat from the returnArticleAndLink, even though they are the same
def returnWebArticles(stockName, mostRecent = False, numberOfArticles = 0):
    # Requests is used to get the HTML page that we need to parse over
    session = HTMLSession()
    # Link used to contain the google finance page of the chosen stock
    page = session.get("https://www.marketwatch.com/investing/stock/{stockName}".format(stockName = stockName)).text

    soup = BeautifulSoup(page, "html5lib")
    # The variable below contains the table for the table containing the news
    newsTable = soup.findAll("div", {"class" : "article__content"})
    # Array used to contain the artile headlines of the markets
    links = [x.find("a", {"class" : "link"}) for x in newsTable]

    # If-Else block used to allow user to select most recent articles, specific articles, or all articles
    if mostRecent == True:
        # If the user selects that they want the most recent article, then an array with the name of the article, and the article's link is returned
        return [links[0].text.replace("\n", "").strip(), links[0]["href"]]
    elif numberOfArticles != 0 and numberOfArticles > 0:
        return links[:numberOfArticles]
    else:
        # The return statement returns the links for the news articles
        return [x["href"] for x in links if x["href"] != "#"]

# Function used to return the name of the article with its respecitve link - O(n)
def returnArticleAndLink(stockName):
    # Array contains the titles of the stock that the user has selected
    articleTitles = [x for x in returnMostRecentArticles(stockName) if x != ""]

    # Contains the links to all of the articles for the specified stock
    links = returnWebArticles(stockName)

    # Dictionary used to contain the articles and their links that meet the requirements
    returnArticles = {}

    # First for loop used to iterate over the article title array
    for x in articleTitles:
        returnArticles[x] = links[articleTitles.index(x)]

    # The return statement will return the dictionary containig the titles of the website and their links
    return returnArticles

# Function used to return the daily automated stock review article - O(1)
    # openArticle parameter is used in case the user wants the function to automatically open the article in their browser
def returnDailyStockReviewArticle(stockName, openArticle = False):
    # Requests is used to get the HTML page that we need to parse over
    session = HTMLSession()
    # Link used to contain the google finance page of the chosen stock
    page = session.get("https://www.marketwatch.com/investing/stock/{stockName}".format(stockName = stockName)).text

    soup = BeautifulSoup(page, "html5lib")
    # The variable below contains the table for the table containing the news
    newsTable = soup.findAll("div", {"class" : "article__content"})

    # For loop used to check for the daily updated value
    for x in range(len(newsTable)):
        # Try-Catch used incase of a Nonetype error
        try:
            # If statement used to check for the most recent day's stock summary article
            if str(newsTable[x].find("span", {"class" : "article__timestamp"})["data-est"]) == "{year}-{month}-{day}T16:36:00".format(year = datetime.now().year, month = datetime.now().strftime("%m"), day = datetime.now().day):
                if openArticle == False:
                    return newsTable[x].find("a")["href"]
                else:
                    webbrowser.open(newsTable[x].find("a")["href"])
                    break
        except:
            continue

