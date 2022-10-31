from asyncio.windows_events import NULL
from sqlite3 import Timestamp
from LAB import key
import ccxt
import pprint
import time
import pandas as pd
from strategy import *
from PositionManager import *




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
        #while에 원하는 전략이 있으면 그걸 클릭하고 그게 실행되게 만들면 좋을 듯
        while True:
            BTC_M = PositionManager('BTC/USDT')
            
            #2400 requests per minute
            time.sleep(60/2400)
            
            
            # 잔고 조회
            balance = binance.fetch_balance(params={"type": "future"})
            #print(balance['USDT'])
            
            
            
            #btc가 진입조건에 맞는다면 포지션 진입, 각 종목당 봇은 하나만 운영
            btc = binance.fetch_ticker("BTC/USDT")
            btc_price = float(btc['info']['lastPrice'])
            
            print('진행중')
            
            #거래를 했다면 orders[0]에 거래가 들어감.
            if BTC_M.orders[0]==None:
               
                if bollinger_upper_short("BTC/USDT",btc_price)[0]:
                    TP = bollinger_upper_short("BTC/USDT",btc_price)[1]
                    SL = bollinger_upper_short("BTC/USDT",btc_price)[2]
                    BTC_M.set_TPSL(TP,SL)
                    BTC_M.set_position(binance,0.001)
            
            #있다면 거래 수시로 수정
            else:
                TP = bollinger_upper_short("BTC/USDT",btc_price)[1]
                SL = bollinger_upper_short("BTC/USDT",btc_price)[2]
                BTC_M.set_TPSL(TP,SL)
                
                
            
            
            #btc TP 또는 SL이 발동되었다면 종료
            #if BTC_M.orders[0]
            
            
                
                
                
            #eth가 진입조건에 맞는다면
            eth = binance.fetch_ticker('ETH/USDT')
            pass
        
        
        
        
    except KeyboardInterrupt:
        print('프로그램이 종료되었습니다.')