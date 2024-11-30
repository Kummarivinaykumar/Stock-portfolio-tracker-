def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.user = request.user
            symbol = request.POST.get('symbol')
            if symbol:
                stock.symbol = symbol  # Set the symbol field
            else:
                stock.symbol = '' 
            # Fetch the latest stock data using yfinance
            ticker = yf.Ticker(stock.ticker)
            stock_data = ticker.history(period="1d")
            
            if not stock_data.empty:
                stock.price = stock_data['Close'][0]  # Set the stock price
            else:
                # Handle the case where data is unavailable (e.g., set price to None or 0)
                stock.price = 0.0  # Or choose another default value, like None
            
            stock.save()
            return redirect('dashboard')
    else:
        form = StockForm()
    return render(request, 'portfolio/add_stock.html', {'form': form})