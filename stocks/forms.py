# stocks/forms.py
from django import forms

class BacktestForm(forms.Form):
    initial_investment = forms.DecimalField(label='Initial Investment', max_digits=10, decimal_places=2)
    short_window = forms.IntegerField(label='Short Moving Average Window', min_value=1, initial=50)
    long_window = forms.IntegerField(label='Long Moving Average Window', min_value=1, initial=200)
