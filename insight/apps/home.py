import dash_html_components as html
import dash_bootstrap_components as dbc




table_header = [html.Thead(html.Tr([html.Th("Analysis")
                                    , html.Th("Notes")]))]

row1 = html.Tr([html.Td(dbc.Button("Fibonacci", href="/fibonacci", color="primary", className="mt-3")), 
                html.Td("""The retracement levels can be used in a situation where you wanted to buy a particular stock but 
                you have not been able to because of a sharp run-up in the stock price. In such a situation, wait 
                for the price to correct to Fibonacci retracement levels such as 23.6%, 38.2%, and 61.8% and then buy the stock.
                The Fibonacci retracement trading strategy is more effective over a longer time interval """)])
row2 = html.Tr([html.Td(dbc.Button("Global Screen", href="/global_", color="primary", className="mt-3")), 
                html.Td("Prefect")])
row3 = html.Tr([html.Td(dbc.Button("MACD", href="/macd", color="primary", className="mt-3")), 
                html.Td("""exp3, AKA the 'Signal Line' is a nine-day EMA of the MACD. 
                When the signal line (red one) crosses the MACD (green) line: 
                * it is time to sell if the MACD (green) line is below 
                * it is time to buy if the MACD (green) line is above.""")])
row4 = html.Tr([html.Td(dbc.Button("RSI", href="/rsi", color="primary", className="mt-3")), 
                html.Td("""An asset is usually considered overbought when the RSI is above 70% and undersold when it is below 30%.
                RSI is usually calculated over 14 intervals (mostly days) and you will see it represented as RSI14""")])

#row4 = html.Tr([html.Td("Trillian"), html.Td("Astra")])
table_body = [html.Tbody([row1, row2, row3, row4])]
table = dbc.Table(table_header + table_body, bordered=True)


layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Welcome to the In$ight dashboard!", className="text-center")
                    , className="mb-5 mt-5")]),
        dbc.Row([
            dbc.Col(html.H1(children="Analyses I'm Working On", className="text-center")
                    , className="mb-5 mt-5")]),
#         dbc.Row([
#             dbc.Col(html.H5(children='It consists of two main pages: Global, which gives an overview of the COVID-19 cases and deaths around the world, '
#                                      'Singapore, which gives an overview of the situation in Singapore after different measures have been implemented by the local government.')
#                     , className="mb-5")
#         ]),
#         dbc.Row([
#             dbc.Col(dbc.Card(children=[html.H3(children='Get the original datasets used in this dashboard',
#                                                className="text-center"),
#                                        dbc.Row([dbc.Col(dbc.Button("Global", href="https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863",
#                                                                    color="primary"),
#                                                         className="mt-3"),
#                                                 dbc.Col(dbc.Button("Singapore", href="https://data.world/hxchua/covid-19-singapore",
#                                                                    color="primary"),
#                                                         className="mt-3")], justify="center")],
#                              body=True, color="dark", outline=True)
#                     , width=4, className="mb-4"),
#             dbc.Col(dbc.Card(children=[html.H3(children='Access the code used to build this dashboard',
#                                                className="text-center"),
#                                        dbc.Button("GitHub",
#                                                   href="https://github.com/meredithwan/covid-dash-app",
#                                                   color="primary",
#                                                   className="mt-3"),
#                                        ],
#                              body=True, color="dark", outline=True)
#                     , width=4, className="mb-4"),
#             dbc.Col(dbc.Card(children=[html.H3(children='Analyses Im working on', className="text-center"),
#                                        dbc.Button("Fibonacci", href="/fibonacci", color="primary", className="mt-3"),],
#                                        body=True, color="dark", outline=True), width=4, className="mb-4")], className="mb-5"),
        
        
        
        table,

    ])

])

