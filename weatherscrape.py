#weatherscrape.py
import requests
from bs4 import BeautifulSoup
import re
import argparse

# Setup and parse command line arguments
parser = argparse.ArgumentParser(description= "A python script to scrape weather data from weather.com.",
epilog= "Usage: python weatherscrape.py <City/Region> <Province/State>")

parser.add_argument("City", help="City or region to search. Example: Toronto")
parser.add_argument("Province_State", help="Province or state to search. Example: Ontario")
args = parser.parse_args()

# Obtain command line arguments
input_province = args.Province_State
input_city = args.City

# Search google to obtain a weather.com link for the specified location ------------------------------------------------

search_page = requests.get("https://www.google.com/search?q=site%3Aweather.com+" + input_city + "+" + input_province + "+10-day").text
pre_soup = BeautifulSoup(search_page, 'lxml') #Invoke lxml library to process html

first_result = pre_soup.find("a", href=re.compile("https://weather.com/weather/tenday/l/"))

# Do not continue if no acceptable result is found
if first_result == None:
    print("No results found.")
    exit(1)

#Process the obtained <a> html tag to extract the hyperlink, then clean the hyperlink of escape chatacters
weather_page = (str(first_result).split("q=", 1)[1]).split("&", 1)
weather_page_fixed = weather_page[0].replace("%2B","+").replace("%3F","?").replace("%3D", "=")

#To force metric units (celcius) add an extension to the hyperlink depending on type of hyperlink
# weather.com uses 2 different extensions depending on the format
if weather_page_fixed.find("canonicalCityId") != -1:
    weather_page_fixed += "&unit=m"
else:
    weather_page_fixed += "?unit=m" 

#Scrape data from the obtained weather.com page ---------------------------------------------------------------

http_text = requests.get(weather_page_fixed).text

# All data of interest is nested within <div>
# Find all <div> tags
soup = BeautifulSoup(http_text, 'lxml') #Invoke lxml library to process html

weather_data = soup.find_all('div', class_="DetailsSummary--DetailsSummary--1DqhO DetailsSummary--fadeOnOpen--KnNyF")

#scrape data for each day
compiled_data = []

for day in weather_data:
    date = day.find("h3", class_="DetailsSummary--daypartName--kbngc").text

    temp_section = day.find("div", class_="DetailsSummary--temperature--1kVVp")
    temp_span_tags = temp_section.find_all("span")
    temp_max = temp_span_tags[0].text       #unnested with respect to the span tags
    temp_min = temp_span_tags[1].span.text  #nested within another span

    condition_div = day.find("div", class_="DetailsSummary--condition--2JmHb")
    condition_text = condition_div.span.text
    precip_div = day.find("div", class_="DetailsSummary--precip--1a98O")
    precip_text = precip_div.span.text

    wind_div = day.find("div", class_="DetailsSummary--wind--1tv7t DetailsSummary--extendedData--307Ax")
    wind_text_list = wind_div.span.text.split()
    wind_direction = wind_text_list[0]
    wind_speed = wind_text_list[1] + " " + wind_text_list[2] #Wind and units

    compiled_data.append((date, temp_max, temp_min, condition_text, precip_text, wind_direction, wind_speed))

# Write to file (but only if there is data)
print("\nAttempting to fetch data from: \n" + weather_page_fixed + "\n")

if len(compiled_data) > 0:
    with open('WeatherScrape.txt', 'w') as f:
        print("(Date, Low, High, Conditions, Precipitation, Wind direction, Wind speed)", file=f)
        for entry in compiled_data:
            print(entry, file=f)

    print("Weather data file WeatherScrape.txt successfully created.")
else:
    print("Error fetching data.")