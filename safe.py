import os, csv
from flask import Flask, render_template, request
from patterns import patterns
import talib #candlestick function
import yfinance as yf
import pandas as pd
import datetime

###41:38 getting a little non-attentive
###could I just get the most recent data in yf.download
###ta-lib prints 0 or non zero value if pattern appears

app = Flask(__name__)

@app.route('/')
def index():
    pattern = request.args.get('pattern', None)##gets the route func value pair and passes pattern string to variable 
    stocks = {} #dictionary symbol and bullish/bearish-signal

    with open('datasets/companies.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'company': row[1]} #splits symbol dict into new dict symbol = {'company': company name}
            print(stocks)                        #stocks index[index[0] of csv.reader] #'PRU': {'company': 'Prudential Financial'},

    if pattern:
        datafiles = os.listdir('datasets/daily') ##get the directory of stock data
        for filename in datafiles:
            df = pd.read_csv('datasets/daily/{}'.format(filename))
            pattern_function = getattr(talib, pattern) #on talib all the functions are named attributes, pass name of function into a variable to call the function
            
            symbol = filename.split('.')[0]#takes CSV filenames and gets 1st element of list
            try:
                result = pattern_function(df['Open'], df['High'], df['Low'], df['Close']) 
                #print (result)
                last = result.tail(1).values ##get's the last pattern I believe
                #print (last)
###bullish/bearish algo 42:09 getting sleepy here
                if last > 0:
                    stocks[symbol][pattern] = 'bullish'
                elif last < 0:
                    stocks[symbol][pattern] = 'bearish'
                else:
                    stocks[symbol][pattern] = None
                    #print("{} triggered {}".format(filename, pattern)) 
            except:
                pass
                   
    return render_template("index.html", patterns=patterns, stocks = stocks, current_pattern = pattern) #inserting into body #late add (42:43)#send pattern name to template and url in line(16)(43:43)
@app.route('/snapshot')
def snapshot():
    path = 'datasets/daily'
    daily_folder = os.listdir(path)
    
    if len(daily_folder) != 0:
        for file in daily_folder:
            os.remove(os.path.join(path, file))

    date = datetime.date.today()
    numdays = 100
    dateList = []
    # for x in range (0, numdays): #from 0 to 100
    #     dateList.append(date - datetime.timedelta(days=x)) #subtract each day from today

    start = input("Enter start date as YYYY-MM-DD  ")
    end = date
    with open('datasets/companies.csv') as f: #get list of company symbols
        companies = f.read().splitlines()
        for company in companies:
            symbol = company.split(',')[0]
            #df = yf.download(symbol, start="2020-07-01", end="2020-11-20") #yf---returns pandas data frame
            df = yf.download(symbol, start, end)
            df.to_csv('datasets/daily/{}.csv'.format(symbol))
    return {
        "code" : "success"
    }