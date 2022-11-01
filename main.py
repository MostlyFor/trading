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

def make_position(Bot,symbol,position_size):
    coin = binance.fetch_ticker(symbol)
    coin_price = float(coin['info']['lastPrice'])
    
     #거래를 했다면 orders[0]에 거래가 들어감.
    if Bot.orders[0]==None:
       
        #조건에 맞는다면 거래 체결
        if bollinger_upper_short_for_test(symbol,coin_price)[0]:
            
            print('체결됨')
            TP = bollinger_upper_short_for_test(symbol,coin_price)[1]
            SL = bollinger_upper_short_for_test(symbol,coin_price)[2]
            Bot.set_TPSL(TP,SL)
            Bot.set_position(binance,position_size)
    
    
    #있다면 거래 수시로 수정
    else:
            TP = bollinger_upper_short_for_test(symbol,coin_price)[1]
            SL = bollinger_upper_short_for_test(symbol,coin_price)[2]
            Bot.set_TPSL(TP,SL)
        
        
        # 메인 포지션이 끝났다면 끝냄.
        #if Bot.orders[0].
        #   Bot.__del__()
        




if __name__ == "__main__":
    try:
        BTC_M = PositionManager('BTC/USDT')
        ETH_M = PositionManager('ETH/USDT')
        #while에 원하는 전략이 있으면 그걸 클릭하고 그게 실행되게 만들면 좋을 듯
        while True:
            
            #2400 requests per minute
            time.sleep(60/2400)
            
            
            # 지표를 통해 코인 선별 (구현 예정)

            
            # 선별된 코인 전략 기대 수익률에 따라 봇에 자금 분배 (구현 예정)
            # balance = binance.fetch_balance(params={"type": "future"})
            
            
            
            # list에서 Bot 활성화
            make_position(BTC_M,'BTC/USDT',0.001)
            make_position(ETH_M,'ETH/USDT',0.05)
            
        
        
        
        
    except KeyboardInterrupt:
        print('프로그램이 종료되었습니다.')