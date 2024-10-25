import pandas as pd
from django.test import TestCase
from .backtesting import run_backtest

class BacktestTests(TestCase):
    
    def test_backtest_simple_strategy(self):
        # Sample historical data for testing
        historical_data = {
            'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='D'),
            'close_price': [150] * 25 + [145] * 25 + [155] * 25 + [160] * 25
        }
        data = pd.DataFrame(historical_data)
        data.set_index('timestamp', inplace=True)
        
        # Parameters for the backtest
        params = {
            'data': data,  # Pass the DataFrame here
            'initial_investment': 10000,
            'short_window': 10,
            'long_window': 30
        }

        # Run the backtest
        result = run_backtest(**params)

        # Assertions to validate results
        self.assertIsInstance(result, dict)
        self.assertIn('total_return', result)
        self.assertIn('final_portfolio_value', result)
        self.assertIn('trade_count', result)
