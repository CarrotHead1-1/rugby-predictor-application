#libaries
from typing import List, Any

from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
import requests as r

#from datasetManager import createDf


#BrightData setup 

#brd-customer-hl_5939d09e-zone-dissertation_webscrapper:8m4ixpt9p4yk@brd.superproxy.io:9515
AUTH = 'brd-customer-hl_353b4db0-zone-dissertation_webscrapper:y1xz8r818u2d'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'


#gets webpage from the given url
def getWebpage(webpage):

   # if r.get(webpage).status_code == 404:
   #    return
    
   sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
   with Remote(sbr_connection, options=ChromeOptions()) as driver:
      driver.get(webpage)

      ##check if page exsits - some games have not been played yet, should continue with the loop. 
      #check for page error 
      #if error --> return nothing otherwise return html.
      html = driver.page_source
      return html

#extracts webpage html
def extractHtml(html):
   #create parse tree 
   soup = BeautifulSoup(html, 'html.parser')
   htmlBody = soup.body
   #check htmlBody exsits
   if htmlBody:
      return str(htmlBody)
   return ""

def cleanHtml(content):
    #creates new parse tree on body content
    soup = BeautifulSoup(content, 'html.parser')
    #loops through the html to remove all script and style tags
    for tags in soup(['script', 'style']):
       tags.extract()
    #gets the cleaned html
    cleanedHtml = soup.get_text(separator='\n')
    cleanedHtml = '\n'.join(
       line.strip() for line in cleanedHtml.splitlines() if line.strip()
    )
    #returns the cleaned html content
    return cleanedHtml

#returns the url split up into different sections by each /
def stripRugbyPassURL(url):
   split = url.split('/')

   return split

#gets delimeters for the lastest page on rugbypass
def getLatestPageDelimeters(content):
   while True:
      try:
         startPnt = content.find("Attack Profile")
         endPnt = content.find("Other Fixtures")
      
         if startPnt != -1 and endPnt != -1:
            return startPnt, endPnt
      
      except:
         continue


#gets delimeters for the stats page on rubgypass
def getStatsPageDelimeters(content):
   while True:
      try:
         startPnt = content.find("Match Summary")
         endPnt = content.find("Other Fixtures")

         return startPnt, endPnt
      except:
         continue

def statsPageURL(split):
   return f'{split[0]}//{split[2]}/{split[3]}/{split[4]}/stats/{split[5]}'

def extractData(matchData: List[str]):

   #stores the match data from the webpage
   matchDataArr = []
   
   for data in matchData:
      #checks for % -> changes them to floats
      if "%" in data:
         #removes the %
         value = data.split('%')
         #checks the value is numerical      
         if value[0].isdigit():
            #adds data to the array, converts value to a float
            matchDataArr.append(float(int(value[0]) / 100))
         
      try:
         #tries to convert data to a float
         float(data)
         #checks if the data is an interger
         if data.isdigit():
            #adds interger data
            matchDataArr.append(int(data))
         else:
            #adds the data if a decimal / float
            matchDataArr.append(float(data))
      except ValueError:
         continue

   return matchDataArr

#checks for 404 errors
def checkPage(webpage):
   #checks for a 404 error
   if r.get(webpage).status_code == 404:
      #returns 1 for an error
      return 1
   return 0

def scrapeData(url):

   # #latest page url from rubgy pass
   latest = url 
   stats = stripRugbyPassURL(url)
   stats = statsPageURL(stats)
   if checkPage(latest) == 0:
      html = getWebpage(latest)
      body = extractHtml(html)
      content = cleanHtml(body)
      
      startPnt, endPnt = getLatestPageDelimeters(content)
      
      pageData = content[startPnt : endPnt]
      dataSplit = pageData.splitlines()
      latestData = extractData(dataSplit)
      #print(latestData)
   if checkPage(stats) == 0:
      html = getWebpage(stats)
      body = extractHtml(html)
      content = cleanHtml(body)
      
      startPnt, endPnt = getStatsPageDelimeters(content)
      
      pageData = content[startPnt : endPnt]
      dataSplit = pageData.splitlines()
      
      statsData = extractData(dataSplit)
      #print(statsData)
   return latestData, statsData
   # if checkPage(url) == 0:
   #    html = getWebpage(url)
   #    content = extractHtml(html)
   #    content = cleanHtml(html)

   #    startPnt, endPnt = getLatestPageDelimeters(content)

   #    matchData = content[startPnt : endPnt]
   #    matchData = matchData.splitlines()

   #    matchData = extractData(matchData)

   #    strip = stripRugbyPassURL(url)
   #    url = statsPageURL(strip)

   #    if checkPage(url) == 0:


   #stats page url from rugby pass
   
      #content = extractHtml(html)
      #content = cleanHtml(content)
      #print('success')
      #print(content)

   #split = stripRugbyPassURL('https://www.rugbypass.com/live/exeter-chiefs-vs-gloucester/?g=943614')
   #statsURL = statsPageURL(split)
   #print(checkPage(statsURL))
