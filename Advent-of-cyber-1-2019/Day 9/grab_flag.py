import requests

flag = ''
host = 'http://10.10.169.100:3000/'
path = ""

while True:
    response = requests.get(host + path)
    response.encoding = "utf-8"

    response = response.json()
    if response["value"] == "end":
        break
    flag += response["value"]
    path = response["next"] + "/"

print(f"Flag is {flag}")


