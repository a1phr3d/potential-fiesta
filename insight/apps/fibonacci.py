import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from app import app

import plotly.graph_objects as go
from plotly.subplots import make_subplots

def loadJSON(some_json):
    import json
    with open(some_json, 'r') as content:
        data = json.load(content)
        return (data)
def jsonTOdict(some_list):
    import datetime
    mainrow = []
    for i in range(len(some_list)):
        for j in some_list[i]['candles']:
            row = []
            row.extend((some_list[i]['symbol'], 
                       j['open'], j['high'], j['low'], 
                       j['close'], j['volume'],
                       datetime.date.fromtimestamp(j['datetime']/1000)))
            mainrow.append(row)
    return(mainrow)
   
dat = loadJSON('C:\\Users\\alfre\\Desktop\\dash-apps\\update\\Stocks\\stockScreen.json')
data = jsonTOdict(dat)
stock = pd.DataFrame(data, columns=['Stock', 'Open', 'High','Low', 'Close', 'Volume', 'Date'])
symbols = sorted(pd.unique(stock['Stock']))

periodDict = {'2 Months': 30, '3 Months': 90,'6 Months': 180,
              '1 Year': 365, '2 Years':730, '3 Years': 1095,}


headerLayout = html.Div(children=[
    html.H1(children="Fibonacci", className= 'header-content'),],className='header')
stockFilterLayout = html.Div(children=[
    html.Div(children='Stock', className='menu-title'),
    dcc.Dropdown(id= 'stock-filter',
                options=[{"label": symbol, "value": symbol} for symbol in symbols],
                value=symbols[0], clearable=False, className='filter-menus')], className='filter-menu2')
periodFilterLayout = html.Div(children=[
    html.Div(children="Period", className= 'menu-title'),
    dcc.Dropdown(id = "period",
                options=[{'label':period, 'value':period} for period in ('2 Months', '3 Months', '6 Months', '1 Year', '2 Years', '3 Years')],
                value='2 Months', className = 'filter-menus')], className='filter-menu2')

def makeLayouts(num_of_charts, some_name):
    outList = [html.Div(children=dcc.Graph(id=(some_name + str(i)), config={"displayModeBar": False}), className='card') for i in range(num_of_charts)]
    return outList
 
menuLayout  = html.Div(children=[stockFilterLayout, periodFilterLayout], className='menu')
graphLayout = html.Div(children=makeLayouts(1, 'fibonacci'), className = 'wrapper')

layout = html.Div(children=[headerLayout, menuLayout, graphLayout])

@app.callback(
    #[
        Output("fibonacci0", "figure"),
        #Output("fibonacci1", "figure"),
        #],
    [
        Input("stock-filter", "value"),
        Input("period", "value"),],)
 
def update_charts(symbol, per):
    period          = periodDict[per]
    filtered_data   = stock[stock['Stock'] == symbol]
    filtered_data   = filtered_data.iloc[-period:]
    Highs           = list(filtered_data['High'])
    Lows_           = list(filtered_data['Low'])
    highest_swing   = lowest_swing = -1
    
    for i in range(1,filtered_data.shape[0]-1):
        if Highs[i] > Highs[i-1] and Highs[i] > Highs[i+1] and (highest_swing == -1 or Highs[i] > Highs[highest_swing]):
            highest_swing = i
        if Lows_[i] < Lows_[i-1] and Lows_[i] < Lows_[i+1] and (lowest_swing  == -1 or Lows_[i] < Lows_[lowest_swing]):
                lowest_swing = i
                 
    ratios = [0,0.236, 0.382, 0.5 , 0.618, 0.786,1]
    #colors = ["black","red","lightseagreen","navy","cyan","magenta","goldenrod"]
    colors = ['rgb(0,0,0, 0.1)', 'rgb(255,0,0,0.1)', 'rgb(32, 178, 170, 0.1)', 'rgb(0, 0, 128,0.1)', 'rgb(0, 255, 255,0.1)', 'rgb(255, 0, 255,0.1)', 'rgb(218, 165, 32,0.1)']
    levels = []
    max_level = Highs[highest_swing]
    min_level = Lows_[lowest_swing]
    for ratio in ratios:
        if highest_swing > lowest_swing: # Uptrend
            levels.append(max_level - (max_level-min_level)*ratio)
        else: # Downtrend
            levels.append(min_level + (max_level-min_level)*ratio)
    
    leName = ""
    if levels[0] > levels[-1]:
        leName = 'Bullish'
    elif levels[0] < levels[-1]:
        leName = 'Bearish'
    else:
        leName= Neutral

    
    fibonacci_chart_figure = make_subplots(specs=[[{"secondary_y": True}]])
    fibonacci_chart_figure.add_trace(go.Scatter
                                     (x=filtered_data["Date"], y=filtered_data["Close"],fill=None, name= leName), secondary_y=False,)
    for k in range(len(levels)):
        fibonacci_chart_figure.add_trace(go.Scatter
                                         (x=filtered_data["Date"], y=[levels[k]]*len(filtered_data['Date']), fill='tonexty',
                                          #fillcolor=colors[k-1],
                                          name = str(round(ratios[k]*100, 2)) + '%', line=dict(color=colors[k], width=1.5,dash='dash')), 
                                         secondary_y=False,)
    fibonacci_chart_figure.update_layout(autosize=False,
                                         #width=500,
                                         height=500,
                                         #title_text=symbol + " -- Fibonacci", 
                                         title_text=symbol,template="plotly_white",
                                         # showlegend=False,
        )
   
    return fibonacci_chart_figure

