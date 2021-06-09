#import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
from builtins import round


data = pd.read_csv("stockScreen.csv")
symbols = pd.unique(data['stock'])[:5]
price_indicator = 'Close'
period = 90

       
for symbol in symbols:
    filtered_data = data[data['stock'] == symbol]
    filtered_data = filtered_data.iloc[-period:]
    
    earliest_price  = float(filtered_data.iloc[[0]][price_indicator])
    min_price       = float(min(filtered_data[price_indicator]))
    max_price       = float(max(filtered_data[price_indicator]))
    latest_price    = float(filtered_data.iloc[[-1]][price_indicator])
    
    percent_change   = round(((latest_price - earliest_price)/earliest_price) * 100, 2)
    percent_rel_max  = round(((latest_price - max_price)/max_price) * 100, 2)
    percent_rel_min  = round(((latest_price - min_price)/min_price) * 100, 2)
    
    tupOut = (symbol, percent_change, percent_rel_max, percent_rel_min)
    print(tupOut)