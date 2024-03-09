#!/usr/bin/env python3

import requests

for api_key in range(1,100,2):
    html = requests.get(f"http://10.10.42.145:80/api/{api_key}").json()
    
    if html["q"] != "Error. Key not valid!":
        print(f"api key {api_key}")
        print(html)
        break

