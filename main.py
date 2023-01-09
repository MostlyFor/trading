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


def make_position(Bot,symbol,position_size,best_st):
    coin = binance.fetch_ticker(symbol)
    coin_price = float(coin['info']['lastPrice'])
    period = int(best_st[-2:]) -10
    
    # 봇이 활성화 되지 않은 경우
    if Bot.orders[0]==None:
       
        # 전략에 맞으면 거래 체결
        if bollinger_upper_short_for_test(symbol,coin_price,period)[0]:
            
            print('체결됨')
            TP = bollinger_upper_short_for_test(symbol,coin_price,period)[1]
            SL = bollinger_upper_short_for_test(symbol,coin_price,period)[2]
            Bot.set_TPSL(TP,SL)
            Bot.set_position(binance,position_size)
    
    
    # 봇이 활성화 된 경우 변동하는 가격에 맞게 TP와 SL 수정
    else:
            TP = bollinger_upper_short_for_test(symbol,coin_price,period)[1]
            SL = bollinger_upper_short_for_test(symbol,coin_price,period)[2]
            Bot.set_TPSL(TP,SL)
            Bot.set_range(Binance,0.091)
        




if __name__ == "__main__":
    try:
        BTC_M = PositionManager('BTC/USDT')
        ETH_M = PositionManager('ETH/USDT')
        
        #while에 원하는 전략이 있으면 그걸 클릭하고 그게 실행되게 만들면 좋을 듯
        while True:
            
           
            
            
            # 지표를 통해 코인 선별 (구현 예정)

            
            # 선별된 코인 전략 기대 수익률에 따라 봇에 자금 분배 (구현 예정)
            # balance = binance.fetch_balance(params={"type": "future"})
           
            # 시그널 탐지 주기
            time.sleep(60/2400) 
            signal = True
            
            if signal:
                # 백테스팅으로 현재 상황에서 가장 유리한 전략 뽑아냄
                import backTesting
                
                best_st=backTesting.best_st
                
                # 그게 net이 양수라면 진행
                # 그리고 확률 값도 뽑아냄
                # 10000개 정도에서 수익률 집계도 함.
                # list에서 Bot 활성화
                make_position(BTC_M,'BTC/USDT',0.001,best_st)
                make_position(ETH_M,'ETH/USDT',0.05,best_st)
            
        
        
        
        
    except KeyboardInterrupt:
        print('프로그램이 종료되었습니다.')
