from django.urls import path
from .views import stock_data_view  # Import your view

urlpatterns = [
    path('stock-data/', stock_data_view, name='stock_data'),  # Add this line
]
