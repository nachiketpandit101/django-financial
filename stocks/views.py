from django.shortcuts import render
from django.http import JsonResponse
from .models import StockData, BacktestResult
import pandas as pd
from stocks.backtesting import BacktestStrategy
from .forms import BacktestForm


def home_view(request):
    return render(request, 'home.html')

def stock_data_view(request):
    stock_data = StockData.objects.filter(symbol='AAPL').order_by('-timestamp')
    return render(request, 'stocks/stock_data.html', {'stock_data': stock_data})

def backtest_view(request):
    result = None  # To hold backtest results
    if request.method == 'POST':
        form = BacktestForm(request.POST)
        if form.is_valid():
            initial_investment = form.cleaned_data['initial_investment']
            short_window = form.cleaned_data['short_window']
            long_window = form.cleaned_data['long_window']

            # Fetch data from the database
            stock_data = StockData.objects.filter(symbol='AAPL').order_by('timestamp')
            data = pd.DataFrame(list(stock_data.values('timestamp', 'close_price')))
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            data.set_index('timestamp', inplace=True)

            # Run backtest
            strategy = BacktestStrategy(data, initial_investment, short_window, long_window)
            result = strategy.run()  # Execute backtest

            return render(request, 'stocks/backtest.html', {'result': result, 'form': form})
    else:
        form = BacktestForm()

    return render(request, 'stocks/backtest.html', {'form': form, 'result': result})

def results_view(request):
    results = BacktestResult.objects.all().order_by('-timestamp')
    return render(request, 'backtest_results.html', {'results': results})