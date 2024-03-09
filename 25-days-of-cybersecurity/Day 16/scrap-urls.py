#!/usr/bin/env python3

# Importing libraries
from bs4 import BeautifulSoup
import requests

# Using requests to download the webpage
html = requests.get('http://10.10.42.145:80/')

# Parsing the webpage for beautifulsoup, lxml is the parser
soup = BeautifulSoup(html.text, "lxml")

#print(soup)

# Grab all the links on the parsed webpage
links = soup.find_all('a')

# Showing the links found
count = 1

for link in links:
    if "href" in link.attrs and len(link["href"]) > 1:
        print(f"{'#'*20} Link #{count} {'#'*20}")
        print(link["href"])
        count += 1

