"""
Script that scrapes charts and stores the data.
"""

from helpers import store_data
from bs4 import BeautifulSoup
import requests
import os


BASE_URL = "https://www.worldometers.info/coronavirus/"
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

DAILY_CASES_PATH = BASE_PATH + "/../data/daily_cases/"
DAILY_DEATHS_PATH = BASE_PATH + "/../data/daily_deaths/"


# scrapes world graphs

print("Scraping world graphs...")

soup = BeautifulSoup(requests.get(BASE_URL + "worldwide-graphs/").content, 
  "html.parser")

# daily cases
store_data(soup, "coronavirus_cases_daily", 
  DAILY_CASES_PATH + "World.csv", ["date", "daily_cases"])


# daily deaths
store_data(soup, "coronavirus-deaths-daily", 
  DAILY_DEATHS_PATH + "World.csv", ["date", "daily_deaths"])

print("Done.\n")


# scrapes individual country graphs

soup = BeautifulSoup(requests.get(BASE_URL).content, "html.parser")
countries = soup.select_one("table#main_table_countries_today").select("a.mt_a")

for country in countries:
  print("Scraping " + country.text + "...")

  bs = BeautifulSoup(requests.get(BASE_URL + country["href"]).content, 
    "html.parser")

  # daily cases
  store_data(bs, "graph-cases-daily", 
    DAILY_CASES_PATH + country.text + ".csv", ["date", "daily_cases"])


  # daily deaths
  store_data(bs, "graph-deaths-daily", 
    DAILY_DEATHS_PATH + country.text + ".csv", ["date", "daily_deaths"])

  print("Done.\n")

  
