import requests
import time
import os
import csv

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
