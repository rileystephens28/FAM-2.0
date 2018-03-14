from django.contrib import admin
from .models import StockExchange, CryptoExchange

admin.site.register(StockExchange)
admin.site.register(CryptoExchange)
