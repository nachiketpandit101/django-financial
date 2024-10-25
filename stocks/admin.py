from django.contrib import admin
from .models import StockData

@admin.register(StockData)
class StockDataAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'timestamp', 'open_price', 'close_price', 'high_price', 'low_price', 'volume')
    list_filter = ('symbol',)
    search_fields = ('symbol',)
