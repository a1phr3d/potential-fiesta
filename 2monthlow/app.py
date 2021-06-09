import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

def stockList(some_txt):
    my_file = open(some_txt, "r")
    symbols = my_file.read().split('\n')[:-1]
    my_file.close()
    return (symbols)


def rank_2ml(data):
    mainrow = []
    symbols = pd.unique(data['stock'])
    for symbol in symbols[:10]:
        row=[]
        filtered_data = data[data['stock'] == symbol]
        filtered_data = filtered_data.iloc[-60:]
        price_indicator = 'Low'
        
        min_price = round(min(filtered_data[price_indicator]), 2)        
        max_price = round(max(filtered_data[price_indicator]), 2)        
        latest_price = round(filtered_data.iloc[[-1]][price_indicator], 2)

        
        #if(float(latest_price) < float(min_price)):
        if(float(latest_price) < float(min_price)):
            row.append(symbol)
            row.append(float(latest_price))
            row.append(float(min_price))
            row.append(float(max_price))
            mainrow.append(row)
    return mainrow


data = pd.read_csv("stockScreen.csv")
temp = rank_2ml(data)
print(temp)

        
#     filtered_data   = filtered_data.iloc[-period:]
#     
#             c=[]
#         decayVal = []
#         close = list(filtered_data['Close'])
#         open = list(filtered_data['Open'])
#         for i in range(len(filtered_data)):
#             c.append(i+1)    
#         