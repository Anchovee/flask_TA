import os, csv
optionsList = ['SPY','SPX','AAPL','QQQ','EEM','IWM','TSLA','SLV','VIX','XLF','GE','BAC','HYG','EFA','GLD','WFC','AAL','NIO','BABA','F','MSFT','GDX','USO','T','EWZ','XLE','FXI','AMD','INTC','FB','PFE','C','XOM','PBR','VALE','XOP','CCL','PLTR','NOK','UBER','CSCO','MU','SNAP','VXX','JPM','GOLD','BA','DIS','PCG','GM']
def trim(optionsList):
    stocks = {}
    rows = ['SPY', 'AAPL', 'SPX']
    with open('datasets/companies.csv') as f:
        for row in csv.reader(f):
            if row[0] in optionsList:
                print (row[0] +','+row[1])
    # for row in rows:
    #     if row in optionsList:
    #         # stocks[row[0]] = {'company': row[1]}
    #         print (row)

if __name__ == "__main__":
    optionsList = ['SPY','SPX','AAPL','QQQ','EEM','IWM','TSLA','SLV','VIX','XLF','GE','BAC','HYG','EFA','GLD','WFC','AAL','NIO','BABA','F','MSFT','GDX','USO','T','EWZ','XLE','FXI','AMD','INTC','FB','PFE','C','XOM','PBR','VALE','XOP','CCL','PLTR','NOK','UBER','CSCO','MU','SNAP','VXX','JPM','GOLD','BA','DIS','PCG','GM']
    trim(optionsList)     


