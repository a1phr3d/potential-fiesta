import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from app import app




data = pd.read_csv("stockScreen.csv")
symbols = pd.unique(data['stock'])






headerLayout = html.Div(children=[
    html.H1(children="Individual Stock", className= 'header-content'),
    html.P(children="Screen for Trading Opportunities!", className='header-description')],className='header')

stockFilterLayout = html.Div(children=[
    html.Div(children='Stock', className='menu-title'),
    dcc.Dropdown(id= 'stock-filter',
                options=[{"label": symbol, "value": symbol} for symbol in symbols],
                value=symbols[0], clearable=False, className='filter-menus')], className='filter-menu2')

def makeLayouts(num_of_charts):
    #outList = [do_something_with(item) for i in range(num_of_charts)]
    outList = [html.Div(children=dcc.Graph(id=("stockchart" + str(i)), config={"displayModeBar": False}), className='card') for i in range(num_of_charts)]
    return outList

menuLayout  = html.Div(children=[stockFilterLayout], className='menu')
graphLayout = html.Div(children=makeLayouts(1), className = 'wrapper')

layout = html.Div(children=[headerLayout, menuLayout, graphLayout])


@app.callback(
    Output("stockchart0", "figure"),
    [Input("stock-filter", "value"),
#         Input("date-range", "start_date"),
#         Input("date-range", "end_date"),
    ],
)

def update_charts(symbol):
    filtered_data = data[data['stock'] == symbol]
    filtered_data = filtered_data.iloc[-60:]
    
    
    price_chart_figure = {
        "data": [
{
                "x": filtered_data["Date"],
                "y": filtered_data["Close"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        
        "layout": {"title": {"text": str(symbol),"x": 0.05,"xanchor": "left"},
                   "xaxis": {"fixedrange": True}, 
                   "yaxis": {"tickprefix": "$", "fixedrange": True}, "colorway": ["#17B897"],},}
        

    return price_chart_figure


# if __name__ == "__main__":
#     app.run_server(debug=True)