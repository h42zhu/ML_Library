import nmf
import urllib2
import pandas

from pandas.io.data import DataReader
from datetime import datetime
from numpy import *



def read_stock_data(tickers, start_date, end_date = datetime.now(), source = 'yahoo', field = 'Volume', out = 'matrix'):
    if out == 'matrix':
        stock_data = DataReader(tickers, source , start_date, end_date)
        stock_data_frame = pandas.DataFrame(stock_data.ix[field]).values
        
        date_data_values = pandas.DataFrame(stock_data.ix[field]).index
        
        return date_data_values, stock_data_frame
        
        
    # other output methods = (csv) ... to do
    
    
def display_feature(w, h, tickers, dates, top_disp_dates = 30):
    # loop over all possible features
    for i in range(shape(h)[0]):
        print "Feature {0}".format(i)
        # get the top stocks for this feature
        ol = [(h[i,j], tickers[j]) for j in range(shape(h)[1])]
        ol.sort(reverse = True)
        
        for j in range(len(tickers)):
            print ol[j]
        print
              
        # show the top dates for this feature
        porder = [(w[d, i], d) for d in range(top_disp_dates)]
        porder.sort(reverse = True)
        print [(p[0], dates[p[1]]) for p in porder[0:3]]








# script
tickers = ('YHOO', 'AVP', 'AAPL', 'PG', 'XOM', 'BP', 'AMGN')

dates, l1 = read_stock_data(tickers, datetime(2014,1,1))

# print dates

w, h = nmf.factorize(l1)
display_feature(w, h, tickers, dates)


#for t in tickers:
    #rows = urllib2.urlopen('http://ichart.finance.yahoo.com/table.csv?' + 
                           #'s=%s&d=11&e=26&f=2006&g=d&a=3&b=12&c=1996'%t + 
                           #'&ignore=.csv').readlines()
    #print rows

#stock_data = DataReader(tickers,  "yahoo", datetime(2000,1,1), datetime(2012,1,1))
#stock_data_frame = pandas.DataFrame(stock_data.ix['Volume']).values
#print stock_data_frame

#stock_data_frame = pandas.DataFrame(stock_data)
#print stock_data_frame
