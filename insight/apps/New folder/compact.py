import dash, json, insight, os, datetime, dash_table
import plotly.graph_objects as go
import pandas as pd
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output 
from app import app
from plotly.subplots import make_subplots
from time import strptime


def makeLayouts(num_of_charts):
    #outList = [do_something_with(item) for i in range(num_of_charts)]
    outList = [html.Div(children=dcc.Graph(id=("compactChart" + str(i)), config={"displayModeBar": False}), className='card') for i in range(num_of_charts)]
    return outList


#options
csvsList = sorted([ f for f in os.listdir(os.path.abspath('.') + "\\apps") if f.endswith(".csv") ])
datList = [pd.read_csv("C:\\Users\\alfre\\trade\\apps\\" +i) for i in csvsList[:-2]]
optionsdf= pd.concat(datList) 
nameColumn = [longSymbol[:longSymbol.index('_')] for longSymbol in optionsdf['symbol']]
optionsdf['shortSymbol'] = pd.DataFrame(nameColumn)

#stock
stockdf = pd.read_csv("C:\\Users\\alfre\\trade\\apps\\stockScreen.csv")
symbolList = sorted(insight.stockList("stockSymbols.txt"))
periodDict = {'3 Months': 90,'6 Months': 180,'1 Year': 365,'3 Years': 1095,'5 Years':18250}

#Headers
compactheaderLayout = html.Div(children=[
    html.H1(children="All Stocks at a Glance", className= 'header-content'),
    html.P(children="Screen for Trading Opportunities!", className='header-description')],className='header')

#menus
nextButton= html.Div([
    dbc.Button("Next", id="next-Button", className="mr-2"),
    html.Span(id="next-output", style={"vertical-align": "center"})])
prevButton=html.Div([
    dbc.Button("Previous", id="prev-Button", className="mr-2"),
    html.Span(id="prev-output", style={"vertical-align": "center"})])
compactperiodFilterLayout = html.Div(children=[
    html.Div(children="Period", className= 'menu-title'),
    dcc.Dropdown(id = "period",
                options=[{'label':period, 'value':period} for period in ('3 Months', '6 Months', '1 Year', '3 Years', '5 Years')],
                value='3 Months',clearable=False, className = 'filter-menus')],
    className= 'filter-menu2')
compactstockFilterLayout = html.Div(children=[
    html.Div(children='Stock', className='menu-title'),
    dcc.Dropdown(id= 'stock-filter',
                options=[{"label": symbol, "value": symbol} for symbol in symbolList],
                value=symbolList[0],  
                className='filter-menus')], className='filter-menu2')

c_menuLayout = html.Div(children=[compactstockFilterLayout, compactperiodFilterLayout, prevButton, nextButton], className='menu')
c_GraphLayout = html.Div(children=makeLayouts(1), className = 'wrapper')

layout = html.Div(children=[compactheaderLayout, c_menuLayout, c_GraphLayout])



@app.callback(
    #[
        Output('compactChart0', 'figure'),
        #Output('compactChart1', 'figure'),
        #Output('compactChart2', 'figure'),
        #Output('compactChart3', 'figure'),
        #Output('compactChart4', 'figure'),
       # Output('compactChart5', 'figure'),
    #],
    [
        Input("stock-filter", "value"),
        Input("next-Button", "n_clicks"),
        Input("prev-Button", "n_clicks"),
        Input("period", "value"),
        ],
    )
# .mean()
def update_charts(symbol, nxt, prv, per):
    def plot_table(symbol, nxt, prv, per):
        period          = periodDict[per]
        filtered_data   =stockdf[stockdf['stock'] == symbol]
        filtered_data   = filtered_data.iloc[-period:]
        
        c=[]
        decayVal = []
        close = list(filtered_data['Close'])
        open = list(filtered_data['Open'])
        for i in range(len(filtered_data)):
            c.append(i+1)
            if i < 89:
                decayVal.append(open[i] * (close[i+1]/close[i]))

        macd_chart_figure = make_subplots(specs=[[{"secondary_y": True}]])
        #macd_chart_figure.add_trace(go.Scatter(x=filtered_data["Date"], y=macd, name= "MACD"), secondary_y=False,)
        macd_chart_figure.add_trace(go.Scatter(x=c[:89], y=decayVal, name= "MACD"), secondary_y=True,)
        macd_chart_figure.add_trace(go.Scatter(x=filtered_data["Date"], y=filtered_data["High"], name='adjclose'), secondary_y=False,)
        macd_chart_figure.update_layout(title_text=symbol + " -- MACD", template="plotly_white", showlegend=False,)

        
        
        
        
        

        
        
        #fig = go.Figure()
    
   
        
        return macd_chart_figure
    
    a = plot_table(symbol, nxt, prv, per)
    return a