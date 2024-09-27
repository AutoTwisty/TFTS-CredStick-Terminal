import requests
from requests.auth import HTTPBasicAuth
import json

username = "tales"
password = "IP*OHtkgR5CTi7Gcr6Bao#v0!AGrDKDj"
authentication = HTTPBasicAuth(username, password)

response = requests.get(
    "https://talesbot.codegrotto.com/api/balance/bard",
    auth=HTTPBasicAuth("tales", "IP*OHtkgR5CTi7Gcr6Bao#v0!AGrDKDj") )

print(response.status_code)

content = json.loads(response.content)

print(content["amount"])

transferData = {"receiver": "bard", "amount": 100, "allow_partial":False}
response = requests.post(url = "https://talesbot.codegrotto.com/api/transfer",auth=authentication, json = transferData)

print(response.status_code)
print(response.json)
print(response.text)