#! python3

import dash, insight
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Output, Input
from app import app
import plotly.graph_objects as go
from plotly.subplots import make_subplots


stockdf = pd.read_csv("C:\\Users\\alfre\\trade\\apps\\stockScreen.csv")

symbolList = insight.stockList("stockSymbols.txt")
symbolList.sort()
periodDict = {'3 Months': 90,'6 Months': 180,'1 Year': 365,'3 Years': 1095,'5 Years':18250}
#print(stockdf.to_string())

headerLayout = html.Div(children=[
    html.H1(children="Individual Stock", className= 'header-content'),
    html.P(children="Screen for Trading Opportunities!", className='header-description')],className='header')

stockFilterLayout = html.Div(children=[
    html.Div(children='Stock', className='menu-title'),
    dcc.Dropdown(id= 'stock-filter',
                options=[{"label": symbol, "value": symbol} for symbol in symbolList],
                value=symbolList[0], clearable=False, className='filter-menus')], className='filter-menu2')
periodFilterLayout = html.Div(children=[
    html.Div(children="Period", className= 'menu-title'),
    dcc.Dropdown(id = "period",
                options=[{'label':period, 'value':period} for period in ('3 Months', '6 Months', '1 Year', '3 Years', '5 Years')],
                value='3 Months', className = 'filter-menus')], className='filter-menu2')



def makeLayouts(num_of_charts):
    #outList = [do_something_with(item) for i in range(num_of_charts)]
    outList = [html.Div(children=dcc.Graph(id=("stockchart" + str(i)), config={"displayModeBar": False}), className='card') for i in range(num_of_charts)]
    return outList

menuLayout  = html.Div(children=[stockFilterLayout, periodFilterLayout], className='menu')
graphLayout = html.Div(children=makeLayouts(4), className = 'wrapper')





# priceChartLayout    = html.Div(children=dcc.Graph(id="price-chart", config={"displayModeBar": False}), className='card')
# volumeChartLayout   = html.Div(children=dcc.Graph(id="volume-chart", config={"displayModeBar": False}), className='card')
# macdChartLayout     = html.Div(children=dcc.Graph(id="macd-chart", config={"displayModeBar": False}), className='card')
# rsiChartLayout      = html.Div(children=dcc.Graph(id="rsi-chart", config={"displayModeBar": False}), className='card')

# menuLayout  = html.Div(children=[stockFilterLayout, periodFilterLayout], className='menu')
# graphLayout = html.Div(children=[priceChartLayout, volumeChartLayout, macdChartLayout, rsiChartLayout], className = 'wrapper')

layout = html.Div(children=[headerLayout, menuLayout, graphLayout])


@app.callback([
        Output("stockchart0", "figure"),
        Output("stockchart1", "figure"),
        Output("stockchart2", "figure"),
        Output("stockchart3", "figure"),
        ],
    [
        Input("stock-filter", "value"),
        Input("period", "value"),],)

def update_charts(symbol, per):
    period          = periodDict[per]
    filtered_data   =stockdf[stockdf['stock'] == symbol]
    filtered_data   = filtered_data.iloc[-period:]
    
    exp1 = filtered_data['Adj Close'].ewm(span=12, adjust=False).mean()
    exp2 = filtered_data['Adj Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    exp3 = macd.ewm(span=9, adjust=False).mean()
    """
    exp3, AKA the 'Signal Line' is a nine-day EMA of the MACD. 
    When the signal line (red one) crosses the MACD (green) line: 
        * it is time to sell if the MACD (green) line is below 
        * it is time to buy if the MACD (green) line is above.
    """
    
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
    
    price_chart_figure = {
        "data": [{"x": filtered_data["Date"],
                  "y": filtered_data["Low"],
                "type": "lines", "hovertemplate": "$%{y:.2f}<extra></extra>",},],
        "layout": {"title": {"text": str(symbol),"x": 0.05,"xanchor": "left"},
                   "xaxis": {"fixedrange": True}, 
                   "yaxis": {"tickprefix": "$", "fixedrange": True}, "colorway": ["#17B897"],},}
    volume_chart_figure = {
        "data": [{"x": filtered_data["Date"],
                "y": filtered_data["Volume"],
                "type": "lines",},],
        "layout": {"title": {"text": str(symbol), "x": 0.05, "xanchor": "left"},
                   "xaxis": {"fixedrange": True},
                   "yaxis": {"fixedrange": True}, "colorway": ["#E12D39"],},}
    
    macd_chart_figure = make_subplots(specs=[[{"secondary_y": True}]])
    macd_chart_figure.add_trace(go.Scatter(x=filtered_data["Date"], y=macd, name= "MACD"), secondary_y=False,)
    macd_chart_figure.add_trace(go.Scatter(x=filtered_data["Date"], y=exp3, name="Signal Line"), secondary_y=False,)
    macd_chart_figure.add_trace(go.Scatter(x=filtered_data["Date"], y=filtered_data["Adj Close"], name=symbol), secondary_y=True,)
    macd_chart_figure.update_layout(title_text=symbol + " -- MACD", template="plotly_white", showlegend=False,)
    #macd_chart_figure.update_xaxes(title_text="xaxis title") 
    macd_chart_figure.update_yaxes(title_text="MACD", secondary_y=False)
    macd_chart_figure.update_yaxes(title_text="Price", secondary_y=True)   
    macd_chart_figure.update_yaxes(showgrid=False)

    rsi_chart_figure = make_subplots(specs=[[{"secondary_y": True}]])     
    rsi_chart_figure.add_trace(go.Scatter(x=rsi_fd["Date"], y=rsi_fd['RSI'], name="RSI"), secondary_y=False,)
    rsi_chart_figure.add_trace(go.Scatter(x=rsi_fd["Date"], y=[30]*len(rsi_fd['RSI']), name='Underbought',line=dict(color='firebrick', width=1.5,dash='dash')), secondary_y=False,)
    rsi_chart_figure.add_trace(go.Scatter(x=rsi_fd["Date"], y=[70]*len(rsi_fd['RSI']), name='Overbought',line=dict(color='firebrick', width=1.5,dash='dash')), secondary_y=False,)
    rsi_chart_figure.update_layout(title_text=symbol + "-- RSI", template="plotly_white", showlegend=False,)
    rsi_chart_figure.update_xaxes(showgrid=False)
    rsi_chart_figure.update_yaxes(showgrid=False)
    """
    An asset is usually considered overbought when the RSI is above 70% and undersold when it is below 30%.
    RSI is usually calculated over 14 intervals (mostly days) and you will see it represented as RSI14
    """

    
    return price_chart_figure, volume_chart_figure, macd_chart_figure, rsi_chart_figure



##if __name__ == "__main__":
##    app.run_server(host = '127.0.0.1', debug=True)