import time
import os
import csv

from requests_html import HTMLSession
from bs4 import BeautifulSoup
from csv import writer

previousVol = 0

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

