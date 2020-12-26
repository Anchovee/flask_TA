import os, pandas
import plotly.graph_objects as go

symbols = ['TRV']
for filename in os.listdir('datasets/daily'):
    symbol = filename.split('.')[0]
    df = pandas.read_csv(f"datasets/daily/{filename}")
    if df.empty:
        continue
    
    #rolling mean calcs mean price for given preceding period
    df['20sma'] =  df['Close'].rolling(window=20).mean()
    df['stdev'] = df['Close'].rolling(window=20).std()
    df['upper_band'] = df['20sma'] + (2 * df['stdev'])
    df['lower_band'] = df['20sma'] - (2 * df['stdev'])

    df['TR'] = abs(df['High'] - df['Low'])
    df['ATR'] = df['TR'].rolling(window=20).mean()

    df['lower_keltner'] = df['20sma'] - (df['ATR'] * 1.5)
    df['upper_keltner'] = df['20sma'] + (df['ATR'] * 1.5)

    def in_squeeze(df):
        return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner']

    df['squeeze_on'] = df.apply(in_squeeze, axis=1)

    #get last idx of df (iloc|last|tail function)
    if df.iloc[-3]['squeeze_on'] and not df.iloc[-1]['squeeze_on']:
        print(symbol)

'''Chart It with Squeeze Lines in Plotly'''
if symbol == 'ROST':
    print(df)
    aapl_df = df 
    candlestick = go.Candlestick(x=aapl_df['Date'], open = aapl_df['Open'], high = aapl_df['High'], low = aapl_df['Low'],close = aapl_df['Close']) 
    upper_band = go.Scatter(x=aapl_df['Date'], y=aapl_df['upper_band'], name="Upper_BB", line={'color':'red'})
    lower_band = go.Scatter(x=aapl_df['Date'], y=aapl_df['lower_band'], name="Lower_BB", line={'color':'red'})
    upper_kelt = go.Scatter(x=aapl_df['Date'], y=aapl_df['upper_keltner'], name="Upper_Kelt", line={'color':'gray'})
    lower_kelt = go.Scatter(x=aapl_df['Date'], y=aapl_df['lower_keltner'], name="Lower_Kelt", line={'color':'gray'})


    fig = go.Figure(data=[candlestick, upper_band, lower_band, upper_kelt, lower_kelt])
    fig.layout.xaxis.type = 'category'
    fig.layout.xaxis.rangeslider.visible = False
    fig.update_layout(title = "Symbol", template="plotly_white")
    fig.update_xaxes(showgrid=False)

    fig.show()

##track performance on watch list
#df[-1]['High'] - df[-2]['High']