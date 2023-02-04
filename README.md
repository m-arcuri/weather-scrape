# weather-scrape
A short python script to obtain weather information from weather.com and output the forecast for the next 15 days as a text file.

This started as an academic project to serve as an introduction to web scraping, but it only scraped data from a specific weather.com link.
I expanded it to allow the user to obtain information for any location using command line arguments.

Weather.com uses location id's in their links instead of the location name, posing an issue for user input locations. To get around this issue, I used google to search for the location in weather.com, then obtain the link to the weather.com page from there.

# Dependencies
This script uses BeautifulSoup4, requests, and lxml libraries. Check requirements.txt for the full list of dependencies.
To install these libraries, run:
```bash
pip install -r requirements.txt
```

# Usage
To use this script, run the following:
```bash
python weatherscrape.py <City/Region> <Province/State>
```
Example:
```bash
python weatherscrape.py Toronto Ontario
```

Alternatively,
```bash
python weatherscrape.py -h
```
will output some help text and explain the use of this script.
