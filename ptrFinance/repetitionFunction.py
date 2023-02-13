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

