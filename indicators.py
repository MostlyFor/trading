from main import binance
import pandas as pd

'''
중심선: 20일 종가 단순 이동 평균선
상단선: 중심선 + 2 * (20일 종가(close) 표준편차)
하단선: 중심선 – 2 * (20일 종가(close) 표준편차)
'''

def bollinger(symbol,timeframe,period):
    coin = binance.fetch_ohlcv(
    symbol=symbol, 
    timeframe=timeframe, 
    since=None, 
    limit=20)
    
    df = pd.DataFrame(coin, columns=['datetime', 'open', 'high', 'low', 'close','volume'])
    df['datetime'] =pd.to_datetime(df['datetime'],unit ='ms')


    middle = df['close'].rolling(period).mean()[19]
    std = df['close'].rolling(period).std()[19]
    upper = middle + 2 * std
    lower = middle - 2 * std
    
    return (upper,middle,lower)
