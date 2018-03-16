import requests
import json
from django.db import models
from sources.models import StockExchange

class Stock(models.Model):
    company = models.CharField(max_length=500, null = True)
    symbol = models.CharField(max_length=50)
    exchange = models.ForeignKey(StockExchange, on_delete=models.CASCADE,unique=False)
    bid = models.FloatField(default = None, null = True)
    ask = models.FloatField(default = None, null = True)
    last = models.FloatField(default = None, null = True)
    volume = models.FloatField(default = None, null = True)
    high =  models.FloatField(default = None, null = True)
    low =  models.FloatField(default = None, null = True)
    open_price =  models.FloatField(default = None, null = True)
    close_price =  models.FloatField(default = None, null = True)

    def __str__(self):
        return self.symbol

    def update_data(self):
        TRADIER_API_KEY = 'XCp8C02gIfnzIW99aTTU4jnPQGVJ'
        s = requests.Session()
        s.headers.update({'Authorization':'Bearer ' + TRADIER_API_KEY, 'Accept':'application/json'})
        url = 'https://api.tradier.com/v1/markets/quotes'
        params = {"symbols":self.symbol}
        r = s.get(url, params=params)
        content = json.loads(r.text)
        quote = content["quotes"]["quote"]
        self.bid = quote["bid"]
        self.ask = quote["ask"]
        self.last = quote["last"]
        self.volume = quote["volume"]
        self.high = quote["high"]
        self.low = quote["low"]
        self.open_price = quote["open"]
        self.close_price =  quote["close"]
        self.save()
