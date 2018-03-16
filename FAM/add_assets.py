import json
import ujson
import requests
import sys
sys.path.insert(0, "/Users/rileystephens/Documents/Projects/FAM/")
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'FAM.settings'
from django.conf import settings
import django
django.setup()
from sources.models import CryptoExchange, StockExchange
from stocks.models import Stock
from cryptocurrencies.models import Cryptocurrency

data = requests.get('https://api.hitbtc.com/api/2/public/symbol').json()
currency_pairs = []
exchange = CryptoExchange.objects.get(name="HitBTC")
for pairs in data:
    if not Cryptocurrency.objects.filter(symbol=pairs['baseCurrency']+pairs['quoteCurrency'],exchange=exchange):
        pair = Cryptocurrency()
        pair.base = pairs["baseCurrency"]
        pair.quote = pairs["quoteCurrency"]
        pair.symbol = pair.base + pair.quote
        pair.exchange = exchange
        pair.save()

s = requests.Session()
s.headers.update({'Authorization':'Bearer ' + 'XCp8C02gIfnzIW99aTTU4jnPQGVJ', 'Accept':'application/json'})
url = 'https://api.tradier.com/v1/markets/lookup'
params = {'types':'stock,etf,index','linebreak':'true'}
r = s.get(url, params=params)
content = json.loads(r.text)
stocks = Stock.objects.all()
stocks = [item.symbol for item in stocks]
for stock in content["securities"]["security"]:
    if stock["symbol"] not in stocks:
        new_stock = Stock()
        new_stock.symbol = stock["symbol"]
        new_stock.company = stock["description"]
        if StockExchange.objects.filter(code=stock["exchange"]):
            new_stock.exchange = StockExchange.objects.get(code=stock["exchange"])
            new_stock.bid = 0
            new_stock.ask = 0
            new_stock.last = 0
            new_stock.price = 0
            new_stock.save()
