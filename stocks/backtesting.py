import pandas as pd
from decimal import Decimal
from typing import Dict, Any, Tuple
from .models import BacktestResult

class BacktestStrategy:
    def __init__(self, data: pd.DataFrame, initial_investment: float, short_window: int, long_window: int):
        self.data = data
        self.initial_investment = Decimal(str(initial_investment))
        self.short_window = short_window
        self.long_window = long_window
        self.cash = self.initial_investment
        self.holdings = Decimal('0')
        self.trade_count = 0
        self.trades = []
        
    def calculate_signals(self) -> pd.DataFrame:
        """Calculate trading signals based on moving averages."""
        self.data['short_mavg'] = self.data['close_price'].rolling(window=self.short_window, min_periods=1).mean()
        self.data['long_mavg'] = self.data['close_price'].rolling(window=self.long_window, min_periods=1).mean()
        return self.data
    
    def run(self) -> Dict[str, Any]:
        """Execute the backtest strategy."""
        self.calculate_signals()
        peak = Decimal('-Infinity')
        max_drawdown = Decimal('0')
        
        for index, row in self.data.iterrows():
            close_price = Decimal(str(row['close_price']))
            
            # Buy signal
            if close_price < Decimal(str(row['short_mavg'])) and self.holdings == 0:
                self.holdings = self.cash / close_price
                self.trades.append({
                    'date': index,
                    'type': 'BUY',
                    'price': close_price,
                    'amount': self.holdings
                })
                self.cash = Decimal('0')
                self.trade_count += 1
            
            # Sell signal
            elif close_price > Decimal(str(row['long_mavg'])) and self.holdings > 0:
                self.cash = self.holdings * close_price
                self.trades.append({
                    'date': index,
                    'type': 'SELL',
                    'price': close_price,
                    'amount': self.holdings
                })
                self.holdings = Decimal('0')
                self.trade_count += 1
            
            # Calculate drawdown
            portfolio_value = self.cash + (self.holdings * close_price)
            peak = max(peak, portfolio_value)
            drawdown = (peak - portfolio_value) / peak if peak > 0 else Decimal('0')
            max_drawdown = max(max_drawdown, drawdown)
        
        final_portfolio_value = self.cash + (self.holdings * Decimal(str(self.data.iloc[-1]['close_price'])))
        total_return = (final_portfolio_value - self.initial_investment) / self.initial_investment * 100
        
        result = {
            "initial_investment": float(self.initial_investment),
            "final_portfolio_value": float(final_portfolio_value),
            "total_return": float(total_return),
            "max_drawdown": float(max_drawdown * 100),
            "trade_count": self.trade_count,
            "trades": self.trades
        }
        
        # Save results to database
        BacktestResult.objects.create(
            initial_investment=self.initial_investment,
            final_portfolio_value=final_portfolio_value,
            total_return=total_return,
            max_drawdown=max_drawdown * 100,
            trade_count=self.trade_count
        )
        
        return result