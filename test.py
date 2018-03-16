import json
import requests

TRADIER_API_KEY = 'XCp8C02gIfnzIW99aTTU4jnPQGVJ'
s = requests.Session()
s.headers.update({'Authorization':'Bearer ' + TRADIER_API_KEY, 'Accept':'application/json'})
url = 'https://api.tradier.com/v1/markets/quotes'
params = {"symbols":'AAPL'}
r = s.get(url, params=params)
content = json.loads(r.text)
print(content)
