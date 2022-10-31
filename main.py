from LAB import key
import ccxt
import pprint
import time
import pandas as pd



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
        while True:
            #2400 requests per minute
            time.sleep(0.025)
            
            
            # 잔고 조회
            balance = binance.fetch_balance(params={"type": "future"})
            #print(balance['USDT'])
            
            
            #가격정보 받아오기
            btc = binance.fetch_ticker('BTC/USDT')
            pprint.pprint(btc)

            
            
            
            #btc가 조건에 맞는다면
            
            #eth가 조건에 맞는다면
            pass
    except KeyboardInterrupt:
        print('프로그램이 종료되었습니다.')