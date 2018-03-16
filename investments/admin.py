from django.contrib import admin
from .models import StockInvestment, CryptoInvestment

admin.site.register(StockInvestment)
admin.site.register(CryptoInvestment)
