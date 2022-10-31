from asyncio.windows_events import NULL
from LAB import key
import ccxt
import pprint
import time
import pandas as pd
from strategy import *
from PositionManager import *
from indicators import *




binance = ccxt.binance(config = {
    'apiKey': key.api_key, 
    'secret': key.secret_key,
    'enableRateLimit' : True,
    'options': {
        'defaultType': 'future'
    }
})






if __name__ == "__main__":
    try:
        cnt = 1
        while True:
            BTC_M = PositionManager('BTC/USDT')
            
            #2400 requests per minute
            time.sleep(60/2400)
            
            
            # 잔고 조회
            balance = binance.fetch_balance(params={"type": "future"})
            #print(balance['USDT'])
            
            
            
            #btc가 진입조건에 맞는다면 포지션 진입
            btc = binance.fetch_ticker('BTC/USDT')
            if sample1() and BTC_M.orders[0]==None:
                BTC_M.set_position(binance,0.001)
                
            
            
            #btc 모든 포지션이 종료되었으면 BTC_M 초기화
            #if BTC_M.orders[0]
            
            
                
                
                
            #eth가 진입조건에 맞는다면
            eth = binance.fetch_ticker('ETH/USDT')
            pass
        
        
        
        
    except KeyboardInterrupt:
        print('프로그램이 종료되었습니다.')