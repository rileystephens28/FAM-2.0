from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from cryptocurrencies.models import Cryptocurrency
from stocks.models import Stock
from .models import StockInvestment, CryptoInvestment

def search_view(request):
    if request.method == 'POST':
        query = request.POST.get('q')
        try:
            query = str(query)
        except ValueError:
            query = None
            asset = None
        if query:
            if Stock.objects.filter(symbol = query.upper()):
                if Stock.objects.filter(symbol = query.lower()):
                    asset = Stock.objects.get(symbol = query.lower())
                else:
                    asset = Stock.objects.get(symbol = query.upper())
                asset.update_data()
                asset_type = "stock"
                return render(request, 'investments/search.html', {"asset": asset, "type": asset_type})

            elif Cryptocurrency.objects.filter(symbol = query.upper()):
                if Cryptocurrency.objects.filter(symbol = query.lower()):
                    asset = Cryptocurrency.objects.get(symbol = query.lower())
                else:
                    asset = Cryptocurrency.objects.get(symbol = query.upper())
                asset.update_data()
                asset_type = "crypto"
                return render(request, 'investments/search.html', {"asset": asset, "type": asset_type})

            else:
                return render(request, 'investments/search.html')

    return render(request, 'investments/search.html')

def add_asset(request):
    if request.method == 'POST':
        asset = request.POST.get("q")
        user = request.user
        if Cryptocurrency.objects.filter(symbol = asset.upper()):
            if not CryptoInvestment.objects.filter(asset=Cryptocurrency.objects.get(symbol=asset.upper()),investor=User.objects.get(username=user.get_username())):
                investment = CryptoInvestment()
                investment.investor = User.objects.get(username = user.get_username())
                investment.asset = Cryptocurrency.objects.get(symbol = request.POST.get("q"))
                investment.save()
        elif Stock.objects.filter(symbol = asset.upper()):
            if not StockInvestment.objects.filter(asset=Stock.objects.get(symbol=asset.upper()),investor=User.objects.get(username=user.get_username())):
                investment = StockInvestment()
                investment.investor = User.objects.get(username = user.get_username())
                investment.asset = Stock.objects.get(symbol = request.POST.get("q"))
                investment.save()
        return redirect('investments')
        
@login_required(login_url="login/")
def delete_asset(request):
    if request.method == 'POST':
        asset = request.POST.get("q")
        user = request.user
        if Cryptocurrency.objects.filter(symbol = asset.upper()):
            if CryptoInvestment.objects.filter(asset=Cryptocurrency.objects.get(symbol=asset.upper()),investor=User.objects.get(username=user.get_username())):
                investment = CryptoInvestment.objects.get(asset=Cryptocurrency.objects.get(symbol=asset.upper()),investor=User.objects.get(username=user.get_username()))
                investment.delete()
        elif Stock.objects.filter(symbol = asset.upper()):
            if StockInvestment.objects.filter(asset=Stock.objects.get(symbol=asset.upper()),investor=User.objects.get(username=user.get_username())):
                investment = StockInvestment.objects.get(asset=Stock.objects.get(symbol=asset.upper()),investor=User.objects.get(username=user.get_username()))
                investment.delete()
        return redirect('investments')

@login_required(login_url="login/")
def investment_view(request):
    assets = []
    user_obj = request.user
    user = User.objects.get(username = user_obj.get_username())
    if StockInvestment.objects.filter(investor = user):
        for stock in StockInvestment.objects.filter(investor = user):
            assets.append(stock.asset)

    if CryptoInvestment.objects.filter(investor = user):
        for crypto in CryptoInvestment.objects.filter(investor = user):
            assets.append(crypto.asset)
    print(assets)
    return render(request, 'investments/investments.html', {"assets":assets})
