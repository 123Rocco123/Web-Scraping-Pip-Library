import requests

from requests_html import HTMLSession
from bs4 import BeautifulSoup
from datetime import datetime

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
    return [openPrice, high, low, stockPrice, float(stockChange) / 390, float(floatStockChange) / 390, investorConfidence, volume, int(volume / 390), datetime.datetime.now().month, datetime.datetime.now().day, datetime.datetime.now().year, "{month}/{day}/{year}".format(day = datetime.datetime.now().day, month = datetime.datetime.now().month, year = datetime.datetime.now().year), 0, eps, float(stockPrice) / float(eps)]
