#!/usr/bin/env python

# import.io seems to be able to scrape Javascript sites like  http://www.yvr.ca/en/flight-information/arriving.aspx
# can then create a "query" for Excel that creates a simple table; that seems to update at least once a day, maybe live
# could then pull in that table using the query from scraperwiki on a regular basis (as import.io doesn't have scheduling yet)

import scraperwiki
import tweepy
import time
from datetime import datetime
import smtplib
import requests
from BeautifulSoup import BeautifulSoup
import random
import datetime


url = "https://query.import.io/store/connector/cd943034-faa6-452c-8ddb-94e7bd5113c1/_query?_user=3a3ba656-b1c2-4dc0-9c56-7f0cf7df1f24&_apikey=fOsF7Ia6VLppr77z883Bgfufu8Qks%2B7CE50fxMXHJD%2BFM91XMsXjU3%2BjDoOd0b2hTIHBv8U3KMNsssTqLE0cWw%3D%3D&format=HTML&input/webpage/url=http%3A%2F%2Fwww.yvr.ca%2Fen%2Fflight-information%2Farriving.aspx"

html = requests.get(url)
htmlpage = html.content

soup = BeautifulSoup(htmlpage)

rows = soup.findAll("tr")

for row in rows:
    print row
    cells = row.findAll("td")
    for cell in cells:
        print cell
        

