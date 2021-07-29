import dash, json, insight, os, datetime, dash_table
import plotly.graph_objects as go
import pandas as pd
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output 
from app import app
from plotly.subplots import make_subplots


# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
stockdf = pd.read_csv("C:\\Users\\alfre\\trade\\apps\\stockScreen.csv")
symbolList = (insight.stockList("stockSymbols.txt"))
symbolList.sort()
periodDict = {'3 Months': 90,'6 Months': 180,'1 Year': 365,'3 Years': 1095,'5 Years':18250}

#Headers
headerLayout = html.Div(children=[
    html.H1(children="All Stocks at a Glance", className= 'header-content'),
    html.P(children="Screen for Trading Opportunities!", className='header-description')],className='header')

periodFilterLayout = html.Div(children=[
    html.Div(children="Period", className= 'menu-title'),
    dcc.Dropdown(id = "period",
                options=[{'label':period, 'value':period} for period in ('3 Months', '6 Months', '1 Year', '3 Years', '5 Years')],
                value='3 Months', className = 'filter-menus')],
    className= 'filter-menu2')

nextButton= html.Div([
    dbc.Button("Next", id="next-Button", className="mr-2"),
    html.Span(id="next-output", style={"vertical-align": "center"})])

prevButton=html.Div([
    dbc.Button("Previous", id="prev-Button", className="mr-2"),
    html.Span(id="prev-output", style={"vertical-align": "center"})])

holdButton=html.Div([
    dbc.Button("Hold", id="hold-Button", className="mr-2"),
    html.Span(id="hold-output", style={"vertical-align": "center"})])

#menuLayout = html.Div(children=[periodFilterLayout, prevButton, nextButton, holdButton], className='menu')
menuLayout = html.Div(children=[periodFilterLayout, prevButton, nextButton], className='menu')

#Charts/graphs layout
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
        stckSeries=list(stockdf['stock'].unique())
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
        filtered_data = stockdf[stockdf['stock'] == stckSeries[ind%seriesSize]]
        filtered_data = filtered_data.iloc[-per_ :]
        fig = make_subplots(rows=2, cols=1)
        fig.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Low']), row=1, col=1)
        fig.add_trace(go.Scatter(x=filtered_data["Date"], y=[filtered_data['Low'].mean()]*len(filtered_data['Low']), name='avg',line=dict(color='firebrick', width=1.5,dash='dash')),)
        fig.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Volume']), row=2, col=1)
        fig.update_layout(height=1000, width=1000, title_text= str(stckSeries[ind%seriesSize]), template="plotly_white", showlegend=False)
        return fig 
        
        
    x = chartGlobalStocks(nxt, prv, per)
    return(x)
        
        
        
        
        
        
        
        
        
        
        
        
        

