#! python3

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Output, Input
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
def makeLayouts(num_of_charts, some_name):
    outList = [html.Div(children=dcc.Graph(id=(some_name + str(i)), config={"displayModeBar": False}), className='card') for i in range(num_of_charts)]
    return outList


   
dat = loadJSON('C:\\Users\\alfre\\Desktop\\dash-apps\\update\\Stocks\\stockScreen.json')
data = jsonTOdict(dat)
stock = pd.DataFrame(data, columns=['Stock', 'Open', 'High','Low', 'Close', 'Volume', 'Date'])
symbols = sorted(pd.unique(stock['Stock']))

periodDict = {'2 Months': 30, '3 Months': 90,'6 Months': 180,
              '1 Year': 365, '2 Years':730, '3 Years': 1095,}


headerLayout = html.Div(children=[
    html.H1(children="MACD", className= 'header-content'),],className='header')
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


 
menuLayout  = html.Div(children=[stockFilterLayout, periodFilterLayout], className='menu')

graphLayout = html.Div(children=makeLayouts(1, 'macd'), className = 'wrapper')

layout = html.Div(children=[headerLayout, menuLayout, graphLayout])



@app.callback(
#     [
        Output("macd0", "figure"),
#         Output("stockchart1", "figure"),
#         Output("stockchart2", "figure"),
#         Output("stockchart3", "figure"),
#         ],
    [
        Input("stock-filter", "value"),
        Input("period", "value"),],)

def update_charts(symbol, per):
    period          = periodDict[per]
    filtered_data   = stock[stock['Stock'] == symbol]
    filtered_data   = filtered_data.iloc[-period:]
    
    
    exp1 = filtered_data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = filtered_data['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    exp3 = macd.ewm(span=9, adjust=False).mean()

    
    macd_chart_figure = make_subplots(specs=[[{"secondary_y": True}]])
    macd_chart_figure.add_trace(go.Scatter(x=filtered_data["Date"], y=macd, name= "MACD"), secondary_y=False,)
    macd_chart_figure.add_trace(go.Scatter(x=filtered_data["Date"], y=exp3, name="Signal Line"), secondary_y=False,)
    macd_chart_figure.add_trace(go.Scatter(x=filtered_data["Date"], y=filtered_data["Close"], name=symbol), secondary_y=True,)
    macd_chart_figure.update_layout(title_text=symbol + " -- MACD", template="plotly_white", showlegend=False,)
    #macd_chart_figure.update_xaxes(title_text="xaxis title") 
    macd_chart_figure.update_yaxes(title_text="MACD", secondary_y=False)
    macd_chart_figure.update_yaxes(title_text="Price", secondary_y=True)   
    macd_chart_figure.update_yaxes(showgrid=False)

    
    return macd_chart_figure

