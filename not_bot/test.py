import requests

url = "https://yfapi.net/v6/finance/quote"

querystring = {"symbols": "FB"}

headers = {"x-api-key": "Nnabxc8ja99sUulupqgqE9mEdLbEu28v2jrP0Zbz"}

response = requests.request("GET", url, headers=headers, params=querystring)
json = response.json()
print(json["quoteResponse"]["result"])
print(json["quoteResponse"]["result"][0]["preMarketPrice"])
