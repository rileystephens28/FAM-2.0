from django.db import models
from django.contrib.auth.models import User
from stocks.models import Stock
from cryptocurrencies.models import Cryptocurrency

class StockInvestment(models.Model):
    investor = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey(Stock, on_delete=models.CASCADE)

class CryptoInvestment(models.Model):
    investor = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
