from django.http import JsonResponse
import pandas as pd
import yfinance as yf
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from .models import Stock
from .forms import StockForm
from .utils import fetch_real_time_data, fetch_historical_data
from django.utils import timezone

# Custom login view
def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')  # Redirect to home/dashboard
        else:
            return render(request, 'portfolio/login.html', {'error': 'Invalid credentials'})
    return render(request, 'portfolio/login.html')

# Dashboard view
# def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('custom-login')  # Adjust 'custom-login' to match your login view name
    
    stocks = Stock.objects.filter(user=request.user)  # Get stocks for the logged-in user
    stock_data = []

    for stock in stocks:
        ticker = stock.ticker
        data = fetch_real_time_data(ticker)

        if data is not None:
            current_price = data['current_price']
            profit_loss = (current_price - stock.purchase_price) * stock.quantity if current_price is not None else None
            
            stock_data.append({
                'id': stock.id,
                'ticker': ticker,
                'current_price': round(current_price, 2) if current_price is not None else None,
                'profit_loss': round(profit_loss, 2) if profit_loss is not None else None
            })
        else:
            stock_data.append({
                'id': stock.id,
                'ticker': ticker,
                'current_price': None,
                'profit_loss': None
            })

    return render(request, 'portfolio/dashboard.html', {'stocks': stock_data})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('custom-login')  # Adjust 'custom-login' to match your login view name
    
    stocks = Stock.objects.filter(user=request.user)  # Get stocks for the logged-in user
    stock_data = []

    for stock in stocks:
        ticker = stock.ticker
        data = fetch_real_time_data(ticker)

        if data is not None:
            current_price = data['current_price']
            profit_loss = (current_price - stock.purchase_price) * stock.quantity if current_price is not None else None
            
            stock_data.append({
                'id': stock.id,
                'ticker': ticker,
                'name': stock.name,  # Include the name
                'purchase_price': stock.purchase_price,  # Include the purchase price
                'quantity': stock.quantity,  # Include the quantity
                'current_price': round(current_price, 2) if current_price is not None else None,
                'profit_loss': round(profit_loss, 2) if profit_loss is not None else None
            })
        else:
            stock_data.append({
                'id': stock.id,
                'ticker': ticker,
                'name': stock.name,  # Include the name
                'purchase_price': stock.purchase_price,  # Include the purchase price
                'quantity': stock.quantity,  # Include the quantity
                'current_price': None,
                'profit_loss': None
            })

    return render(request, 'portfolio/dashboard.html', {'stocks': stock_data})

def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.user = request.user
            
            # Fetch the latest stock data using yfinance
            ticker = yf.Ticker(stock.ticker)
            stock_data = ticker.history(period="1d")
            
            if not stock_data.empty:
                stock.price = stock_data['Close'][0]  # Set the stock price
            else:
                stock.price = 0.0  # Or choose another default value, like None
            
            stock.added_on = timezone.now()  # Set the added_on field
            stock.save()
            return redirect('dashboard')
    else:
        form = StockForm()
    return render(request, 'portfolio/add_stock.html', {'form': form})

def remove_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    stock.delete()  # Remove the stock from the database
    return redirect('dashboard')  # Redirect back to the dashboard

def get_real_time_stock_data(request, ticker):
    """View to get real-time stock data."""
    # Ensure ticker is provided
    ticker = request.GET.get('ticker')  # Get ticker from query parameters
    if not ticker:
        return JsonResponse({'error': 'Ticker symbol is required'}, status=400)

    # Fetch real-time data using the utility function
    data = fetch_real_time_data(ticker)
    
    if data is not None:
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Failed to fetch real-time data'}, status=500)
    

 

def get_stock_history(request, ticker):
    """Django view to get stock history."""
    # Ensure ticker is provided
    if not ticker:
        return JsonResponse({'error': 'Ticker symbol is required'}, status=400)

    # Get the period from query parameters, default to '1mo'
    period = request.GET.get('period', '1d') 
    data = fetch_historical_data(ticker, period)  # Pass the period to the fetch function

    if data is not None:
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Failed to fetch stock history'}, status=500)