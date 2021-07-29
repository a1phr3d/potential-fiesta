import pandas as pd
import pandas_datareader.data as web
import datetime

start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2020, 1, 27)
SP500 = web.DataReader(['sp500'], 'fred', start, end)
