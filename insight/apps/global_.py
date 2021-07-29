import dash, json, os, datetime, dash_table
import plotly.graph_objects as go
import pandas as pd
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output 
from app import app
from plotly.subplots import make_subplots
from plotly.validators.layout import _hoverdistance


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




#Headers
headerLayout = html.Div(children=[
    html.H1(children="All Stocks at a Glance", className= 'header-content'),],className='header')

periodFilterLayout = html.Div(children=[
    html.Div(children="Period", className= 'menu-title'),
    dcc.Dropdown(id = "period",
                options=[{'label':period, 'value':period} for period in ('2 Months', '3 Months', '6 Months', '1 Year', '2 Years', '3 Years')],
                value='2 Months', className = 'filter-menus')], className='filter-menu2')

nextButton= html.Div([
    dbc.Button("Next", id="next-Button", className="mr-2"),
    html.Span(id="next-output", style={"vertical-align": "center"})])

prevButton=html.Div([
    dbc.Button("Previous", id="prev-Button", className="mr-2"),
    html.Span(id="prev-output", style={"vertical-align": "center"})])

holdButton=html.Div([
    dbc.Button("Hold", id="hold-Button", className="mr-2"),
    html.Span(id="hold-output", style={"vertical-align": "center"})])

menuLayout = html.Div(children=[periodFilterLayout, prevButton, nextButton], className='menu')

priceVolumeChartLayout = html.Div(children=dcc.Graph(id="priceVolume-chart", config={"displayModeBar": False}), className='card')
graphLayout = html.Div(children=[priceVolumeChartLayout], className = 'wrapper')

layout = html.Div(children=[headerLayout, menuLayout, graphLayout])



@app.callback(Output('priceVolume-chart', 'figure'),
    [
        Input("next-Button", "n_clicks"),
        Input("prev-Button", "n_clicks"),
        #Input("hold-Button", "n_clicks"),
        Input("period", "value"),],)

def update_graph(nxt, prv, per):
    def chartGlobalStocks(nxt, prv, per):
         
         
        stckSeries=symbols
        seriesSize = len(stckSeries)
        ind=0
        try:
            ind += nxt
        except TypeError:
            pass
        try:
            ind -= prv
        except TypeError:
            pass
        symb = stckSeries[ind%seriesSize]
        per_ = periodDict[per]
        filtered_data = stock[stock['Stock'] == stckSeries[ind%seriesSize]]
        print(filtered_data)
        filtered_data = filtered_data.iloc[-per_ :]
        fig = make_subplots(rows=2, cols=1)
        fig.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Low']), row=1, col=1)
        fig.add_trace(go.Scatter(x=filtered_data["Date"], y=[filtered_data['Low'].mean()]*len(filtered_data['Low']), name='avg',line=dict(color='firebrick', width=1.5,dash='dash')),)
        fig.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Volume']), row=2, col=1)
        fig.add_trace(go.Bar(x=filtered_data['Date'], y=filtered_data['Volume']), row=2, col=1)
        fig.update_layout(
            #hoverdistance = 0,
            height=800, 
            #width=1000, 
            title_text= str(stckSeries[ind%seriesSize]), template="plotly_white", showlegend=False)
#         fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False,
#                  showspikes=True, spikemode='across', spikesnap='cursor', showline=False, spikedash='solid')
# 
#         fig.update_xaxes(showgrid=False, zeroline=False, rangeslider_visible=False, showticklabels=False,
#                          showspikes=True, spikemode='across', spikesnap='cursor', showline=False, spikedash='solid')
        return fig 
          
    x = chartGlobalStocks(nxt, prv, per)
    return(x)


 
        
        
        
        
        
        
    
