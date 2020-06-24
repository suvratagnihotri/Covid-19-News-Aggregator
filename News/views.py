from django.shortcuts import render
from django.http import HttpResponse

import requests,json
from bs4 import BeautifulSoup

# news from Times of India
toi = requests.get("https://timesofindia.indiatimes.com/coronavirus").text
soup = BeautifulSoup(toi, 'html.parser')

toi_news = []
for para in soup.find_all('div', {'class' :"_3PMC3"}):
  toi_news.append(para.text)

# news from HdustanTimes
ht = requests.get("https://www.hindustantimes.com/topic/coronavirus").text
soup = BeautifulSoup(ht, 'html.parser')

ht_news = []
for para in soup.find_all('div', {'class' :"para-txt"}):
  ht_news.append(para.text)

# Worldwide covid case
url = 'https://www.worldometers.info/coronavirus/'
world_response = requests.get(url)
html_soup = BeautifulSoup(world_response.text, 'html.parser')

type_of_numbers = html_soup.find_all("div",id = "maincounter-wrap")
world_cases = html_soup.find_all("div",class_= "maincounter-number")

w_case = []
for i in range(len(world_cases)):
    w_case.append(type_of_numbers[i].h1.text +" " + world_cases[i].span.text)


# covid cases in India
url = 'https://api.covid19india.org/data.json'
response = requests.get(url)
data = json.loads(response.text)

totalConfirmedCases = data["cases_time_series"][-1]["totalconfirmed"]
totalRecoveredCases = data["cases_time_series"][-1]["totalrecovered"]
totalDeceasedCases = data["cases_time_series"][-1]["totaldeceased"]

# statewise covid cases
statewise = data["statewise"][1:38]
stateCases = []

for i in statewise:
    stateCases.append(i['state'] + ": " + i['confirmed'])

  

def index(req):
    return render(req, 'index.html', {'toi_news':toi_news, 'ht_news':ht_news,
    'w_case':w_case, 'totalConfirmedCases':totalConfirmedCases, 
    'totalRecoveredCases':totalRecoveredCases, 'totalDeceasedCases':totalDeceasedCases,
    'stateCases':stateCases})



