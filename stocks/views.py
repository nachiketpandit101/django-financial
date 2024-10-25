from django.shortcuts import render
from .models import StockData

def stock_data_view(request):
    stock_data = StockData.objects.filter(symbol='AAPL').order_by('-timestamp')  # Order by date descending
    return render(request, 'stocks/stock_data.html', {'stock_data': stock_data})
