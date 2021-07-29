#! python3

import dash, insight, os, datetime
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Output, Input
from app import app
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


csvsList = sorted([ f for f in os.listdir(os.path.abspath('.') + "\\apps") if f.endswith(".csv") ])
datList = [pd.read_csv("C:\\Users\\alfre\\trade\\apps\\" +i) for i in csvsList[:-2]]
odf= pd.concat(datList) 
nameColumn = [longSymbol[:longSymbol.index('_')] for longSymbol in odf['symbol']]
odf['shortSymbol'] = pd.DataFrame(nameColumn)



optionsdf   = pd.read_csv("C:\\Users\\alfre\\trade\\apps\\" + csvsList[:-2][-1])
nameColumn = [longSymbol[:longSymbol.index('_')] for longSymbol in optionsdf['symbol']]
optionsdf['shortSymbol'] = pd.DataFrame(nameColumn)

# print(odf['shortSymbol'])
# 
# print(optionsdf['shortSymbol'])


symbolList  = insight.stockList("stockSymbols.txt")
symbolList.sort()
headerLayout            = html.Div(children=[
    html.H1(children    = "Individual Options", className= 'header-content'),
    html.P(children     = "Screen for Trading Opportunities!", className='header-description')],className='header')

optionFilterLayout = html.Div(children=[
    html.Div(children='StockOption', className='menu-title'),
    dcc.Dropdown(id= 'stockOption-filter', options=[{"label": symbol, "value": symbol} for symbol in symbolList],
                value=symbolList[0], clearable=False, className='filter-menus')], className='filter-menu2')

def makeLayouts(num_of_charts):
    #outList = [do_something_with(item) for i in range(num_of_charts)]
    outList = [html.Div(children=dcc.Graph(id=("chart" + str(i)), config={"displayModeBar": False}), className='card') for i in range(num_of_charts)]
    return outList

menuLayout      = html.Div(children=[optionFilterLayout], className='menu')
graphLayout = html.Div(children=makeLayouts(2), className = 'wrapper')

layout = html.Div(children=[menuLayout, graphLayout])#headerLayout, 

@app.callback(
    [
        Output("chart0", "figure"),
        #Output("GoOI-chart", "figure"),
        
        
        Output("chart1", "figure"),
        ],
        [
        Input("stockOption-filter", "value"),
        #Input("period", "value"),
        ],)

def update_charts(symbol):
    def chartOpenInterest(symbol):
        filtered_data   = optionsdf[optionsdf['shortSymbol'] == symbol]
        callFilter      = filtered_data[filtered_data['putCall'] == "CALL"]
        putFilter       = filtered_data[filtered_data['putCall'] == "PUT"]
        binFilter       = filtered_data[filtered_data['openInterest'] > 0]
        binStart        = max(binFilter['openInterest'])
        x1, x2, y1, y2  = (callFilter['strikePrice'], putFilter['strikePrice'], 
                          callFilter['openInterest'], putFilter['openInterest'])
        fig             = make_subplots(rows=2, cols=1, subplot_titles=("Calls", "Puts"))
        fig.add_trace(go.Histogram2d(x = x1, y = y1, coloraxis = "coloraxis",), 1,1)
        fig.add_trace(go.Histogram2d(x = x2, y = y2, coloraxis = "coloraxis", ybins = {'end':binStart}), 2,1)
        #fig.update_xaxes(title_text="Strike Price", row=1, col=1)
        fig.update_xaxes(title_text="Strike Price", row=2, col=1)
        fig.update_yaxes(title_text="Open Interest", row=1, col=1)
        fig.update_yaxes(title_text="Open Interest", row=2, col=1)
        fig.update_layout(title_text="Call/Put Open Interest")
        return fig
    
    
    def chartGlobalOpenInterest():
        #optionsdf = odf
        def computeSum(call_put):
            filterObj = odf[odf['putCall'] == call_put]
            filterObj = filterObj[['shortSymbol', 'openInterest', 'totalVolume']]
            filterObj = filterObj.groupby(['shortSymbol']).sum().reset_index()
            return filterObj
             
        callFilter      = computeSum("CALL")
        putFilter       = computeSum("PUT")
        fig = go.Figure()
        fig.add_trace(go.Bar(x = callFilter['shortSymbol'], y = callFilter['openInterest'], name = 'Calls'))
        fig.add_trace(go.Bar(x = putFilter['shortSymbol'], y = putFilter['openInterest'], name = 'Puts'))
        fig.update_layout(height=500, width=800, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        return fig
    
    x = chartOpenInterest(symbol)
    y = chartGlobalOpenInterest()
    


#     f1OIsum = dftempc.groupby(['shortSymbol']).sum().reset_index()
#     f1TVsum = dftempc.groupby(['totalVolume']).sum().reset_index()
#     
#     dftempp = optionsdf[optionsdf['putCall'] == 'PUT']
#     dftempp = dftempp[['shortSymbol', 'openInterest', 'totalVolume']]
#     f2OIsum = dftempp.groupby(['shortSymbol']).sum().reset_index()
#     f2TVsum = dftempp.groupby(['totalVolume']).sum().reset_index()
#     
#     GoOIfig = go.Figure()
#     GoOIfig.add_trace(go.Bar(x = f1OIsum['shortSymbol'], y = f1OIsum['openInterest'], name = 'Calls'))
#     GoOIfig.add_trace(go.Bar(x = f2OIsum['shortSymbol'], y = f2OIsum['openInterest'], name = 'Puts'))
#     GoOIfig.update_layout(height=600, width=1000, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
#     
#     GoTVfig = go.Figure()
#     GoTVfig.add_trace(go.Bar(x = f1TVsum['shortSymbol'], y = f1TVsum['totalVolume'], name = 'Calls'))
#     GoTVfig.add_trace(go.Bar(x = f2TVsum['shortSymbol'], y = f2TVsum['totalVolume'], name = 'Puts'))
#     GoTVfig.update_layout(height=600, width=1000, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

    return x, y

    
    

#     fig = go.Figure()
#     fig.add_trace(go.Bar(x=f1['strikePrice'],
#                          y=f1['bidSize'],
#                          name='Calls',
#                          marker_color='rgb(55, 83, 109)'))
#     fig.add_trace(go.Bar(x=f2['strikePrice'], 
#                          y=f2['openInterest'],
#                          name='Puts',
#                          marker_color='rgb(26, 118, 255)'
#                 ))
# 
#     fig.update_layout(
#         title='US Export of Plastic Scrap',
#         xaxis_tickfont_size=14,
#         yaxis=dict(
#             title='USD (millions)',
#             titlefont_size=16,
#             tickfont_size=14,
#         ),
#         legend=dict(
#             x=0,
#             y=1.0,
#             bgcolor='rgba(255, 255, 255, 0)',
#             bordercolor='rgba(255, 255, 255, 0)'
#         ),
#         barmode='group',
#         bargap=0.15, # gap between bars of adjacent location coordinates.
#         bargroupgap=0.1 # gap between bars of the same location coordinate.
#     )
#     #fig.show()
#     return fig










# 
#     pOIfig = go.Figure()
#     pOIfig.add_trace(go.Scatter(x=f1['strikePrice'], y=f1['openInterest'],
#                                 mode='markers',
#                                 marker=dict(size=f1norm*15),
# #                                 marker=dict(size=f1norm*15),
#                                 name='Calls'))
#     pOIfig.add_trace(go.Scatter(x=f2['strikePrice'], y=f2['openInterest'],
#                                 mode='markers',
#                                 marker=dict(size=f2norm*15),
#                                 name='Puts'))
#     pOIfig.update_layout(height=1000, width=1000)
#     return pOIfig
#     pOIfig.update_layout(height=1000, width=1000, title_text= str(stckSeries[ind%seriesSize]), template="plotly_white", showlegend=False)
    
    
#     x=f1['Bid'] * f1['BidSize']
#     x=x.sum()
#     y=f2['Bid'] * f2['BidSize']
#     y=y.sum()
#     z=x/y
# #     fig = go.Figure()
# # #     fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[0, 2, 3, 5], fill='tozeroy')) # fill down to xaxis
# # #     fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[3, 5, 1, 7], fill='tonexty')) # fill to trace0 y
# #     fig.add_trace(go.Histogram(x=optionsdf['Bid'][:100], y=optionsdf['BidSize'][:100], fill='tozeroy'))
# 
# 
#     print(z)
#     relativecallvolumefig = go.Figure()
#     relativecallvolumefig.add_trace(go.Histogram(x=z))
# #                                                  y=f1['TotalVolume']))
# #     relativecallvolumefig.add_trace(go.Histogram(x=f2['StrikePrice'],
# #                                                  y=f2['TotalVolume']))
    
    
#     
#     
#     
#     
#     f1norm=f1['OpenInterest']/1000
# 
#     
#     
#     f2norm=f2['OpenInterest']/1000
# 
#     
#     
#     
#     
# #     bidfig = go.Figure(data=[go.Histogram(x = f1['StrikePrice'],
# #                                           y = f1['BidSize'])])
#     
#     bidfig = go.Figure()
#     bidfig.add_trace(go.Histogram(x = f1['Bid'],
#                                   y = f1['BidSize']))
#     bidfig.add_trace(go.Histogram(x = f2['Bid'],
#                                   y = f2['BidSize']))
#     
#     # Overlay both histograms
#     bidfig.update_layout(barmode='overlay')
#     # Reduce opacity to see both histograms
#     bidfig.update_traces(opacity=0.75)
#     
#     
#     
# #     
# #     
# #     go.Figure(data=[go.Histogram(x = f1['StrikePrice'],
# #                                            y = f1['BidSize'])])
#     
#     
#     
#     
#     
# #     auxfig = go.Figure()
# #     auxfig.add_trace(go.Scatter(x=f1['StrikePrice'], y=f1['BidSize'],
# #                     mode='markers',
# #                     marker=dict(size=f1norm*15),
# #                     name='Calls'))
# #     
# #     auxfig.add_trace(go.Scatter(x=f2['StrikePrice'], y=f2['BidSize'],
# #                     mode='markers',
# #                     marker=dict(size=f2norm*15),
# #                     name='Puts'))
# 
#     auxfig = go.Figure()
#     auxfig.add_trace(go.Scatter(x=f1['StrikePrice'], 
#                                 y=f1['Bid'],
#                     mode='markers',
#                     marker=dict(size=f1norm),
#                     name='Calls'))
#     
#     auxfig.add_trace(go.Scatter(x=f2['StrikePrice'], 
#                                 y=f2['Bid'],
#                     mode='markers',
#                     marker=dict(size=f2norm),
#                     name='Puts'))   
#     return auxfig, bidfig
#     
#     
    
    
    
    
    
    
    

#     filtered_data = filtered_data.iloc[-period:]
    

#     
#     price_chart_figure = {
#         "data": [{
#                 "x": filtered_data["date"],
#                 "y": filtered_data["low"],
#                 "type": "lines",
#                 "hovertemplate": "$%{y:.2f}<extra></extra>",},],
#         "layout": {
#             "title": {"text": str(symbol),"x": 0.05,"xanchor": "left"},
#             "xaxis": {"fixedrange": True},
#             "yaxis": {"tickprefix": "$", "fixedrange": True},
#             "colorway": ["#17B897"],},}
# 
#     volume_chart_figure = {
#         "data": [{
#                 "x": filtered_data["date"],
#                 "y": filtered_data["volume"],
#                 "type": "lines",},],
#         "layout": {
#             "title": {"text": str(symbol), "x": 0.05, "xanchor": "left"},
#             "xaxis": {"fixedrange": True},
#             "yaxis": {"fixedrange": True},
#             "colorway": ["#E12D39"],},}



# Basic Radar Chart with go.Scatterpolar
# import plotly.graph_objects as go
# 
# fig = go.Figure(data=go.Scatterpolar(
#   r=[1, 5, 2, 2, 3],
#   theta=['processing cost','mechanical properties','chemical stability', 'thermal stability',
#            'device integration'],
#   fill='toself'
# ))
# 
# fig.update_layout(
#   polar=dict(
#     radialaxis=dict(
#       visible=True
#     ),
#   ),
#   showlegend=False
# )
# 
# fig.show()

#Multiple Trace Radar Chart
# import plotly.graph_objects as go
# 
# categories = ['processing cost','mechanical properties','chemical stability',
#               'thermal stability', 'device integration']
# 
# fig = go.Figure()
# 
# fig.add_trace(go.Scatterpolar(
#       r=[1, 5, 2, 2, 3],
#       theta=categories,
#       fill='toself',
#       name='Product A'
# ))
# fig.add_trace(go.Scatterpolar(
#       r=[4, 3, 2.5, 1, 2],
#       theta=categories,
#       fill='toself',
#       name='Product B'
# ))
# 
# fig.update_layout(
#   polar=dict(
#     radialaxis=dict(
#       visible=True,
#       range=[0, 5]
#     )),
#   showlegend=False
# )
# 
# fig.show()


#     
#     aux_chart_figure = make_subplots(specs=[[{"secondary_y": True}]])
#     aux_chart_figure.add_trace(
#         go.Scatter(x=filtered_data["date"], y=macd, name= symbol + " MACD"),
#         secondary_y=False,)
#     aux_chart_figure.add_trace(
#         go.Scatter(x=filtered_data["date"], y=exp3, name="Signal Line"),
#         secondary_y=False,)
#     aux_chart_figure.add_trace(
#         go.Scatter(x=filtered_data["date"], y=filtered_data["adj-close"], name=symbol),
#         secondary_y=True,)
#     aux_chart_figure.update_layout(
#         title_text=symbol + "-- MACD",
#         template="plotly_white",
#         showlegend=False,)
#     # Set x-axis title
#     #macd_chart_figure.update_xaxes(title_text="xaxis title") 
#     #Set y-axes titles
#     macd_chart_figure.update_yaxes(title_text="MACD", secondary_y=False)
#     macd_chart_figure.update_yaxes(title_text="Price", secondary_y=True)   
# #     macd_chart_figure.update_yaxes(showgrid=False)
#     aux_chart_figure = go.Figure()
#     aux_chart_figure.add_trace(go.Scatterpolar(
#     r=[1, 5, 2, 2, 3],
# #     theta=categories,
# #     fill='toself',
# #     name='Product A'
#     ))






##if __name__ == "__main__":
##    app.run_server(host = '127.0.0.1', debug=True)