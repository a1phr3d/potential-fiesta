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
    html.H1(children="RSI", className= 'header-content'),],className='header')
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

graphLayout = html.Div(children=makeLayouts(1, 'rsi'), className = 'wrapper')

layout = html.Div(children=[headerLayout, menuLayout, graphLayout])


@app.callback(
#     [
        Output("rsi0", "figure"),
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
    
    rsi_fd  = filtered_data.copy(deep=True)
    delta   = rsi_fd['Close'].diff()
    up      = delta.clip(lower=0)
    down    = -1*delta.clip(upper=0)
    ema_up  = up.ewm(com=13, adjust=False).mean()
    ema_down = down.ewm(com=13, adjust=False).mean()
    rs = ema_up/ema_down
    rsi_fd['RSI'] = 100 - (100/(1 + rs))
    # Skip first 14 **15** days to have real values
    rsi_fd = rsi_fd.iloc[14:]
    

    rsi_chart_figure = make_subplots(specs=[[{"secondary_y": True}]])     
    rsi_chart_figure.add_trace(go.Scatter(x=rsi_fd["Date"], y=rsi_fd['RSI'], name="RSI"), secondary_y=False,)
    rsi_chart_figure.add_trace(go.Scatter(x=rsi_fd["Date"], y=[30]*len(rsi_fd['RSI']), name='Underbought',line=dict(color='firebrick', width=1.5,dash='dash')), secondary_y=False,)
    rsi_chart_figure.add_trace(go.Scatter(x=rsi_fd["Date"], y=[70]*len(rsi_fd['RSI']), name='Overbought',line=dict(color='firebrick', width=1.5,dash='dash')), secondary_y=False,)
    rsi_chart_figure.update_layout(title_text=symbol + "-- RSI", template="plotly_white", showlegend=False,)
    rsi_chart_figure.update_xaxes(showgrid=False)
    rsi_chart_figure.update_yaxes(showgrid=False)

    
    return rsi_chart_figure
