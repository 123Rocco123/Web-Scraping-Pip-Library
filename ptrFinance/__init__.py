import requests
import time
import os
import csv
# Used to search using our default webbrowser
import webbrowser

import pandas as pd
import numpy as np

from requests_html import HTMLSession
from bs4 import BeautifulSoup
from datetime import datetime
from csv import writer

# Used for reading websites
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Class Variable
previousVol = 0

# Function used to get the current stock values of the specified stocks
    # stocks parameter is used to contain the array with all the names of the stocks
def getLiveValues(stocks):
    # Return array used to contain the live values for each stock
    liveValues = {}

    # Iterate over the file
    for x in stocks:
        session = HTMLSession()
        stockValues = session.get("https://finance.yahoo.com/quote/{stock}".format(stock = x)).text
        soup = BeautifulSoup(stockValues, "html5lib")

        # Append the stock with the current value
        liveValues[x] = soup.find("fin-streamer", {"class" : "Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text

    return liveValues

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

# Functions used to gather stock information from Yahoo Finance

# Return the closing stock price
def closeValue(stockName):
    # Create the session for webscraping
    session = HTMLSession()
    page = session.get("https://finance.yahoo.com/quote/{stockName}?p={stockName}".format(stockName = stockName)).text

    soup = BeautifulSoup(page, "html5lib")

    return float(soup.find("fin-streamer", {"class" : "Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text)

# Return the previous closing price
def previousClose(stockName):
    # Create the session for webscraping
    session = HTMLSession()
    page = session.get("https://finance.yahoo.com/quote/{stockName}?p={stockName}".format(stockName = stockName)).text

    soup = BeautifulSoup(page, "html5lib")

    # Used to contain the body where the stock info is kept
    stockInfoBody = soup.find("table", {"class" : "W(100%)"}).findAll("tr")
    return float(stockInfoBody[0].findAll("td")[1].text)

# Return the open price
def openValue(stockName):
    # Create the session for webscraping
    session = HTMLSession()
    page = session.get("https://finance.yahoo.com/quote/{stockName}?p={stockName}".format(stockName = stockName)).text

    soup = BeautifulSoup(page, "html5lib")

    # Used to contain the body where the stock info is kept
    stockInfoBody = soup.find("table", {"class" : "W(100%)"}).findAll("tr")
    return float(stockInfoBody[1].findAll("td")[1].text)

# Return the low price for the day
def dayLowValue(stockName):
    # Create the session for webscraping
    session = HTMLSession()
    page = session.get("https://finance.yahoo.com/quote/{stockName}/history?p={stockName}".format(stockName = stockName)).text

    soup = BeautifulSoup(page, "html5lib")

    # Used to contain the body where the info is kept
    stockInfoBody = soup.find("table", {"class" : "W(100%) M(0)"}).findAll("tr")
    return float(stockInfoBody[1].findAll("td")[3].text)

# Return the high price for the day
def dayHighValue(stockName):
    # Create the session for webscraping
    session = HTMLSession()
    page = session.get("https://finance.yahoo.com/quote/{stockName}/history?p={stockName}".format(stockName = stockName)).text

    soup = BeautifulSoup(page, "html5lib")

    # Used to contain the body where the info is kept
    stockInfoBody = soup.find("table", {"class" : "W(100%) M(0)"}).findAll("tr")
    return float(stockInfoBody[1].findAll("td")[2].text)

# Return the volume of trades for the day
def dayVolume(stockName):
    # Create the session for webscraping
    session = HTMLSession()
    page = session.get("https://finance.yahoo.com/quote/{stockName}/history?p={stockName}".format(stockName = stockName)).text

    soup = BeautifulSoup(page, "html5lib")

    # Used to contain the body where the info is kept
    stockInfoBody = soup.find("table", {"class" : "W(100%) M(0)"}).findAll("tr")
    return int(stockInfoBody[1].findAll("td")[6].text.replace(",", ""))

# Return the EPS value for the stock
def stockEPSValue(stockName):
    # Create the session for webscraping
    session = HTMLSession()
    page = session.get("https://finance.yahoo.com/quote/{stockName}?p={stockName}".format(stockName = stockName)).text

    soup = BeautifulSoup(page, "html5lib")

    # Used to contain the body where the info is kept
    stockInfoBody = soup.find("table", {"class" : "W(100%) M(0) Bdcl(c)"}).findAll("tr")
    return float(stockInfoBody[3].findAll("td")[1].text)

# Return the PE Ratio value for the stock
def PERatio(stockName):
    # Create the session for webscraping
    session = HTMLSession()
    page = session.get("https://finance.yahoo.com/quote/{stockName}?p={stockName}".format(stockName = stockName)).text

    soup = BeautifulSoup(page, "html5lib")

    # Used to contain the body where the info is kept
    stockInfoBody = soup.find("table", {"class" : "W(100%) M(0) Bdcl(c)"}).findAll("tr")
    # Try - Except is used in case we have a N/A for the PE Ratio
    try:
        return float(stockInfoBody[2].findAll("td")[1].text)
    except:
        return stockInfoBody[2].findAll("td")[1].text

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

# Functions used to gather stock information from MarketWatch

# Gather Yearly Earnings Estimates - O(n)
    # Returns: High, Low, Average
def stockYearlyNumbers(stockName):
    session = HTMLSession()
    requests = session.get("https://www.marketwatch.com/investing/stock/{stockName}/analystestimates?mod=mw_quote_tab".format(stockName = stockName)).text

    soup = BeautifulSoup(requests, "html5lib")

    returnDictionary = {}

    dataRow = [x.text for x in soup.find("div", {"class", "element element--table yearly"}).find("tbody").findAll("th")]
    for x in [x.text for x in soup.find("div", {"class", "element element--table yearly"}).find("thead").findAll("th") if x.text != ""]:
        index = [x.text for x in soup.find("div", {"class", "element element--table yearly"}).find("thead").findAll("th") if x.text != ""].index(x)
        returnDictionary[x] = [dataRow[index], dataRow[4 + index], dataRow[8 + index]]

    return returnDictionary

# Gather Quarterly Estimates - O(n)
    # Returns: High, Low, Average
def stockQuarterlyEstimates(stockName):
    session = HTMLSession()
    requests = session.get("https://www.marketwatch.com/investing/stock/{stockName}/analystestimates?mod=mw_quote_tab".format(stockName = stockName)).text

    soup = BeautifulSoup(requests, "html5lib")

    returnDictionary = {}

    rows = [x.findAll("th") for x in soup.find("div", {"class", "tab__pane j-tabPane"}).findAll("tr")]

    for x in rows:
        # Try - Except used to change between the float and string values
        try:
            # Append the values for the specific columns
            returnDictionary[toAdd[0]].append([float(y.text) for y in x if y.text != ""][0])
            returnDictionary[toAdd[1]].append([float(y.text) for y in x if y.text != ""][1])
        except:
            toAdd = [y.text for y in x if y.text != ""]
            # Create the dictionary arrays used to contain the two columns
            returnDictionary[toAdd[0]] = []
            returnDictionary[toAdd[1]] = []

    return returnDictionary

# Gather Quarterly Actuals - O(n)
    # Returns: Estimate, Actual, Surprise
def stockQuarterlyActuals(stockName):
    session = HTMLSession()
    requests = session.get("https://www.marketwatch.com/investing/stock/{stockName}/analystestimates?mod=mw_quote_tab".format(stockName = stockName)).text

    soup = BeautifulSoup(requests, "html5lib")

    returnDictionary = {}

    rows = [x.findAll("th") for x in soup.find("div", {"class", "tab__pane j-tabPane is-active"}).findAll("tr")]

    for x in rows:
        # Try - Except used to change between the float and string values
        try:
            # Append the values for the specific columns
            returnDictionary[toAdd[0]].append([float(y.text) for y in x if y.text != ""][0])
            returnDictionary[toAdd[1]].append([float(y.text) for y in x if y.text != ""][1])
            returnDictionary[toAdd[2]].append([float(y.text) for y in x if y.text != ""][2])
            returnDictionary[toAdd[3]].append([float(y.text) for y in x if y.text != ""][3])
        except:
            toAdd = [y.text for y in x if y.text != ""]
            # Create the dictionary arrays used to contain the two columns
            returnDictionary[toAdd[0]] = []
            returnDictionary[toAdd[1]] = []
            returnDictionary[toAdd[2]] = []
            returnDictionary[toAdd[3]] = []

    return returnDictionary

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
    # specificDay parameter is used in case the user wants to find the article of a specific day
        # The month, day, and year parameters are used to specify the date
def returnDailyStockReviewArticle(stockName, openArticle = False, specificDay = False, month = None, day = None, year = None):
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
            # If-Else block is used if the user decides to find the automated article of a specific day or not
            if specificDay == False:
                # If statement used to check for the most recent day's stock summary article
                if "{year}-{month}-{day}".format(year = datetime.now().year, month = datetime.now().strftime("%m"), day = datetime.now().day) in str(newsTable[x].find("span", {"class" : "article__timestamp"})["data-est"]):
                    if newsTable[x].find("span", {"class" : "article__author"}).text == "by MarketWatch Automation":
                        if openArticle == False:
                            return newsTable[x].find("a")["href"]
                        else:
                            webbrowser.open(newsTable[x].find("a")["href"])
                            break
            else:
                # If statement used to check for the most recent day's stock summary article
                if "{year}-{month}-{day}".format(year = year, month = month, day = day) in str(newsTable[x].find("span", {"class" : "article__timestamp"})["data-est"]):
                    if newsTable[x].find("span", {"class" : "article__author"}).text == "by MarketWatch Automation":
                        if openArticle == False:
                            return newsTable[x].find("a")["href"]
                        else:
                            webbrowser.open(newsTable[x].find("a")["href"])
                            break
        except:
            continue

# Function used to return the name, date, and link of the article of the stock that the user specifies - O(n)
def returnDateOfArticle(stockName):
    # Requests is used to get the HTML page that we need to parse over
    session = HTMLSession()
    # Link used to contain the google finance page of the chosen stock
    page = session.get("https://www.marketwatch.com/investing/stock/{stockName}".format(stockName = stockName)).text

    soup = BeautifulSoup(page, "html5lib")
    # The variable below contains the table for the table containing the news
    newsTable = soup.findAll("div", {"class" : "article__content"})

    # Array used to contain the name of the article, its link, and its date
    returnArray = []

    # For loop used to check for the daily updated value
    for x in range(len(newsTable)):
        # Try-Catch used incase of a Nonetype error
        try:
            # Used to gather just the date of the article rather than the time of it as well
            nameOfArticle = newsTable[x].find("a").text.strip()
            dateOfArticle = str(newsTable[x].find("span", {"class" : "article__timestamp"})["data-est"])[:10]
            linkOfArticle = newsTable[x].find("a")["href"]

            # Array contains the information of the article gathered from the website
            returnArray.append([nameOfArticle, dateOfArticle, linkOfArticle])

        except:
            continue

    return returnArray

# Function used to return articles of a specified date
def returnSpecificDateOfArticle(stockName, month = 0, day = 0, year = 0, today = False):
    # Requests is used to get the HTML page that we need to parse over
    session = HTMLSession()
    # Link used to contain the google finance page of the chosen stock
    page = session.get("https://www.marketwatch.com/investing/stock/{stockName}".format(stockName = stockName)).text

    soup = BeautifulSoup(page, "html5lib")
    # The variable below contains the table for the table containing the news
    newsTable = soup.findAll("div", {"class" : "article__content"})

    # Array used to contain the name of the article, its link, and its date
    articleArray = []

    # For loop used to check for the daily updated value
    for x in range(len(newsTable)):
        # Try-Catch used incase of a Nonetype error
        try:
            # Used to gather just the date of the article rather than the time of it as well
            nameOfArticle = newsTable[x].find("a").text.strip()
            dateOfArticle = str(newsTable[x].find("span", {"class" : "article__timestamp"})["data-est"])[:10]
            linkOfArticle = newsTable[x].find("a")["href"]

            # Array contains the information of the article gathered from the website
            articleArray.append([nameOfArticle, dateOfArticle, linkOfArticle])

        except:
            continue

    # Array contains the articles that have the matching date
    returnArray = []

    # If-Else block used to depending on if the use has specified a date or not
    if today == False:
        specifiedDate = "{year}-{month}-{day}".format(year = year, month = month, day = day)

        # For loop used to check for the date inside of the elements
        for x in articleArray:
            # If condition is used to check that if the article is of the specified date
            if x[1] == specifiedDate:
                returnArray.append(x)
    else:
        # Variable is used to contain todays date
        currentDate = str(datetime.now())[:10]

        # For loop used to check for the date inside of the elements
        for x in articleArray:
            # If condition is used to check that if the article is of the specified date
            if x[1] == currentDate:
                returnArray.append(x)

    return returnArray

# Function used to return the most recent analyst ratings for a specified stock - O(n)
    # Return values: Date, Brokerage Name, Action, Rating, Price Target, Upside / Downside on Report Date
def returnAnalystRatings(stockName, marketName):
    # Requests is used to get the HTML page that we need to parse over
    session = HTMLSession()
    # Link used to contain the google finance page of the chosen stock
    page = session.get("https://www.marketbeat.com/stocks/{marketName}/{stockName}/price-target/".format(stockName = stockName, marketName = marketName)).text

    soup = BeautifulSoup(page, "html5lib")

    # Variable used to contain the ratings table for the stock by the different companies
    ratingsTable = soup.find("div", {"id" : "cphPrimaryContent_cphTabContent_pnlPriceUpdate"})

    # Try-Except statement is used to check that the
    try:
        # Variable contains the individual ratings of the brokarage for the stock
        brokerageRatings = ratingsTable.find("tbody").findAll("tr")

        # Return array is used to contain and then eventually return all the analyst ratings
        returnArray = []
        # For loop used to iterate over the table containing the brokerage ratings
        for x in brokerageRatings:
            toAppend = [y.text for y in x.findAll("td")]

            # Remove the subscribe row
            if len(toAppend) != 1:
                # Replace the subscribe text placed into the second index of the toAppend cell
                toAppend[1] = toAppend[1].replace("Subscribe to MarketBeat All Access for the recommendation accuracy rating", "")

                # Remove the indexes that aren't related to the brokarage ratings
                del toAppend[2]
                del toAppend[len(toAppend) - 1]

                if "" in toAppend:
                    del toAppend[toAppend.index("")]

                # Append the row to the returnArray
                returnArray.append(toAppend)

        return returnArray

    except:
        print("Couldn't find the stock, check spelling")
        return -1

# Company Owners Functions

# Auxiliary function for the gatherShareholders function
    # "increaseLoadTimeSeconds" variable is used only if the user thinks that 1 second is too short
def findStocksIndexMarket(stockName, increaseLoadTimeSeconds = 0):
    # Used to run the chrome driver without opening the browser
    options = Options()
    # Used to run the browser without opening it
    options.headless = True
    # Used to contain the web scraping driver
    driver = webdriver.Chrome(options = options)
    # Try-Except used to account for the different formatting by Google
    try:
        # Search the stock on the internet
        driver.get("https://www.google.com/search?q=what+market+does+{stockName}+trade+on+us".format(stockName = stockName))
        # Give the website time to load
        time.sleep(1 + increaseLoadTimeSeconds)
        # Contains the market index for the stock
        marketIndex = driver.find_element(By.CSS_SELECTOR, "[class*='iAIpCb PZPZlf']").text.split(":")[0]
        stock = driver.find_element(By.CSS_SELECTOR, "[class*='iAIpCb PZPZlf']").text.split(":")[1].replace(" ", '')
        # Close the driver
        driver.close()

        return marketIndex, stock
    except:
        # Search the stock on the internet
        driver.get("https://www.google.com/search?q={stockName}+stock".format(stockName = stockName))
        # Give the website time to load
        time.sleep(1 + increaseLoadTimeSeconds)
        # Contains the market index for the stock
        marketIndex = driver.find_element(By.CSS_SELECTOR, "[class*='iAIpCb PZPZlf']").text.split(":")[0]
        stock = driver.find_element(By.CSS_SELECTOR, "[class*='iAIpCb PZPZlf']").text.split(":")[1].replace(" ", '')
        # Close the driver
        driver.close()

        return marketIndex, stock

# Function used to return the percentage chance that a company may be going bankrupt
def bankrupt(stockName):
    # Requests is used to get the HTML page that we need to parse over
    session = HTMLSession()
    # Link used to contain the google finance page of the chosen stock
    page = session.get("https://www.macroaxis.com/invest/ratio/{stockName}/Probability-Of-Bankruptcy".format(stockName = stockName)).text

    soup = BeautifulSoup(page, "html5lib")

    # Returns the percentage chance that a company will go bankrupt
    return soup.find("div", {"class" : "importantValue"}).text.strip()

# Function used to return the volatility of a specified function
    # stockName parameter is used to contain the stock naming format of the user specified company
    # stringOutput is used to specifiy if we need
def impliedVolatilityFunc(stockName, stringOutput = True):
    # Requests is used to get the HTML page that we need to parse over
    session = HTMLSession()
    # Link used to contain the google finance page of the chosen stock
    page = session.get("https://volafy.net/equity/{stockName}".format(stockName = stockName)).text

    soup = BeautifulSoup(page, "html5lib")

    # Returns the percentage chance of a company's current volatility
    volatilityPercent = soup.find("div", {"style" : "max-width:150px;position:relative;text-align:center"}).find("b").text.replace("Implied Volatility:", "")
    #  Returns the percentage chance of a company's last month volatility
    previousVolatilityPercent = soup.find("table", {"class" : "table table-sm table-striped table-hover"}).findAll("tr")[5].find("div", {"style" : "position:relative;width:120px"}).text
    # Percentage Difference
    percentageDifference = str(float(volatilityPercent.replace("%", "")) - float(previousVolatilityPercent.replace("%", "")))[:4]

    # If-Else block used to return either a string or an array output
        # The string output is to format the volatility for the users
        # The array output gives the float values to allow users to add that information to their files or for calculations
    if stringOutput == True:
        return "Current Volatility: {volatilityPercent}\nPrevious Volatility: {previousVolatilityPercent}\nPercentage Difference: {percentageDifference}".format(volatilityPercent = volatilityPercent, previousVolatilityPercent = previousVolatilityPercent, percentageDifference = percentageDifference)
    else:
        return [float(volatilityPercent.replace("%", "")), float(previousVolatilityPercent), float(percentageDifference)]

# Function used to return the volatility of a given time set
def returnVolatilityGivenTime(stockName, numberOfDays):
    # Requests is used to get the HTML page that we need to parse over
    session = HTMLSession()
    # Link used to contain the google finance page of the chosen stock
    page = session.get("https://finance.yahoo.com/quote/{stockName}/history?p={stockName}".format(stockName = stockName)).text

    soup = BeautifulSoup(page, "html5lib")
    # Variable used to contain the table with the historic data
    historicData = soup.find("table", {"class" : "W(100%) M(0)"}).findAll("tr")[1:]
    # Array used to contain the closedValues
    closedValues = []

    currentDays = 1
    for x in historicData:
        for dataPoints in x:
            if (x.index(dataPoints) % 4 == 0 and x.index(dataPoints) != 0) and currentDays <= numberOfDays + 1:
                closedValues.append(float(dataPoints.text))
                currentDays += 1

    # Memory Management
    del session, page, soup, historicData, currentDays

    # Used to calculate the daily returns of the stock over the week
    dailyReturn = [closedValues[x] - closedValues[x - 1] for x in range(1, 8)]
    # Contains the average daily return
    averageReturn = np.average(dailyReturn)
    # Contains the squared differences for each daily return
    dailyReturn = [(x - averageReturn) ** 2 for x in dailyReturn]
    # Save Memory
    del averageReturn
    # Contains the variance
    varianceOfSquaredDiff = sum(dailyReturn) / 7
    del dailyReturn

    # Returns the volatility of the stock
    return np.sqrt(varianceOfSquaredDiff)
