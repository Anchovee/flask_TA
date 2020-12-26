import os, pandas


def is_consolidating(df, percentage = 2.5):
    recent_candlesticks = df[-15:]
    
    #Use pandas to get max/min closes
    close = recent_candlesticks['Close']
    max_close = close.max()
    min_close = close.min()

    #Use pandas to get max/mean volumes
    vol = recent_candlesticks['Volume']
    max_vol = vol.max()
    avg_vol = vol.mean()
    
    #Get a threshold for min from 15 days not exceeding a % of max
    threshold = 1 - percentage/100
    if min_close > max_close * threshold and max_vol > (avg_vol + avg_vol * 0.60):
        return True
    return False
def is_breaking_out(df, percentage = 2.5):
    
    last_close = df[-1:]['Close'].max()

    #Pandas Close col. for -n up to but not equal last day
    if is_consolidating(df[:-1], percentage = percentage):
        recent_closes = df[-16:-1]["Close"].max()

        if last_close > recent_closes:
            return True
    return False

for filename in os.listdir('datasets/daily'):
    stock = filename.split('.')[0]
    df = pandas.read_csv(f"datasets/daily/{filename}")
    
    if is_consolidating(df):
        print(f'{stock} chubbin up')
    
    if is_breaking_out(df):
        print(f'{stock} full chubs')
   