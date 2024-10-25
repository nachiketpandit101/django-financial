from django.urls import path
from . import views
from .views import backtest_view

urlpatterns = [
    path('', views.home_view, name='home'),
    path('stock-data/', views.stock_data_view, name='stock_data'),
    path('backtest/', views.backtest_view, name='backtest'),
    path('backtest/', backtest_view, name='backtest_view'),
    path('results/', views.results_view, name='results'),  # Changed from 'results_view' to 'results'
]