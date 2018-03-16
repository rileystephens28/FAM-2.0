import requests
from django.db import models
from sources.models import CryptoExchange

class Cryptocurrency(models.Model):
    base = models.CharField(max_length=10)
    quote = models.CharField(max_length=10)
    symbol = models.CharField(max_length=20)
    exchange = models.ForeignKey(CryptoExchange, on_delete=models.CASCADE,)
    bid = models.FloatField(default = None, null = True)
    ask = models.FloatField(default = None, null = True)
    last = models.FloatField(default = None, null = True)
    base_volume = models.FloatField(default = None, null = True)
    quote_volume = models.FloatField(default = None, null = True)
    last_updated = models.DateTimeField(default = None, null = True)

    def __str__(self):
        return self.base + self.quote

    def update_data(self):
        ticker_data = requests.get('https://api.hitbtc.com/api/2/public/ticker/' + self.symbol.upper()).json()
        self.bid = float(ticker_data["bid"])
        self.ask = float(ticker_data["ask"])
        self.last = float(ticker_data["last"])
        self.base_volume = float(ticker_data["volume"])
        self.quote_volume = float(ticker_data["volumeQuote"])
        self.save()
