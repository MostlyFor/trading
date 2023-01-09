import backtrader as bt
import ccxt
from LAB import key
import pandas as pd
import datetime

import plotly.express as px

binance = ccxt.binance(config = {
    'apiKey': key.api_key, 
    'secret': key.secret_key,
    'enableRateLimit' : True,
    'options': {
        'defaultType': 'future'
    }
})
global graph_log
graph_log = pd.DataFrame(columns={'STRA NAME','NET PNL','WinRate'})



class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', [15]),
    )
    # 출력해주는 함수
    def log(self, txt, doprint=False):
        
        #파라미터만 간단히 바꿀 땐 로그 안띄움.
        if  doprint or self.printall:
            dt = self.datas[0].datetime.date(0)
            dt_time = self.datas[0].datetime.time()
            
            #시스템에도 로그 띄움
            print('%s, %s, %s' % (dt.isoformat(),dt_time, txt))
            
            
            #파일에 로그 씀
            # 파일 열기
            if self.printall:
                f= open('./log/strategy.txt', 'a',encoding='UTF-8')
                
            else : 
                f = open('./log/what_strategy.txt', 'a',encoding='UTF-8')

            # 파일에 텍스트 쓰기
            f.write('%s, %s, %s' % (dt.isoformat(),dt_time, txt))
            f.write('\n')
            
            # 파일 닫기
            f.close()

    #초기화 함수
    def __init__(self,params=None):
        self.printall = False;
        
        if params!=None:
            for name, val in params.items():
                setattr(self.params, name, val)
            
            self.printall = self.params.printall
            
        
        #항상 종가로 계산 !
        self.dataclose = self.datas[0].close

        # 주문 현황과 거래된 가격, 그리고 수수료 기록
        self.order = None
        self.buyprice = None
        self.buycomm = None
        
        # 전략 우위 판별을 위해 승률 기록
        self.trade_count =0
        self.trade_win_count = 0

        # 이평선 전략을 위해 그려봄
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)

        # 볼린져
        self.boll = bt.indicators.BollingerBands(period= self.params.maperiod-10,devfactor = 2)
        
    # order 바뀔때마다 작동
    def notify_order(self, order):
        
        #거래 대기 중이면 그냥 가만히 있음
        if order.status in [order.Submitted, order.Accepted]:
            return

        
        # 거래 됨 -> 기록해야함.
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'long 전부 체결됨, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                # 수수료도 따로 저장해둠 어딘가에 쓰겠지뭐
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            
            #팔았다고 반대로 기록
            else:  # Sell
                self.log('short 전부 체결됨, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
            # 이건 지금은 필요 없는데 몇개 뒤에 팔건지를 위해 해놓은거
            # self.bar_executed = len(self)

        # 거래 취소되거나 돈 없었으면
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('거래 취소됨')

        # 거래 되거나 취소 된 경우 대기 중 거래 없으므로 none 넣어줌
        self.order = None

    # trade 바뀔떄마다 작동
    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log(f'trade 됨 , 거래 수익 : {trade.pnl}, 거래 순수익 : {trade.pnlcomm}')
        
        
        # 결국 수익이 났는지 확인, pnlcomm 은 거래 수익 - 거래 순수익
        if trade.pnlcomm  > 0:
            self.trade_win_count+=1

    def next(self):
        # 다음 신호로 넘어왔으면 이제 계속 기록
        # self.log('현재종가, %.2f' % self.dataclose[0])
    
        # 거래 대기 중인지 확인
        if self.order:
            return

        # 거래 돼서 포지션에 들어가있는지 확인
        if not self.position:

            if self.params.maperiod <=25:
                # 사는 조건
                if self.dataclose[0] > self.sma[0]:
                
                    # BUY, BUY, BUY!!! (with all possible default parameters)
                    self.log('long 주문 들어감, %.2f' % self.dataclose[0])

                    # Keep track of the created order to avoid a 2nd order
                    self.order = self.buy()
                    self.trade_count +=1
            #볼린저 사는 조건
            else:
                if self.dataclose[0] < self.boll.lines.bot[0]:
                    
                    # BUY, BUY, BUY!!! (with all possible default parameters)
                    self.log('long 주문 들어감, %.2f' % self.dataclose[0])

                    self.order = self.buy(price=self.boll.lines.bot[0])
                    self.trade_count +=1
                

        else:
            if self.params.maperiod <=25:
                # 파는 조건
                if self.dataclose[0] < self.buyprice*90 % 100 or self.dataclose[0] > self.buyprice *99 % 100:
                    #print(self.dataclose[0],self.buyprice)
                    # SELL, SELL, SELL!!! (with all possible default parameters)
                    self.log('short 주문 들어감, %.2f' % self.dataclose[0])

                    # Keep track of the created order to avoid a 2nd order
                    self.order = self.sell()
            else:
                if self.dataclose[0] > self.boll.lines.mid[0] or self.dataclose[0] < self.buyprice *99 % 100:
                    self.log('short 주문 들어감, %.2f' % self.dataclose[0])
                    self.order = self.sell(price = self.boll.lines.mid[0])
                
                    
                
    # 이건 여러 개 전략 검토할 때 쓰는 함수로서 발동 조건은 : 내가볼 떄 함수 끝까지 왔을 때인듯
    def stop(self):
        global graph_log
        Ending_value=self.broker.getvalue()
        if self.params.maperiod<=25:
            self.log('(MA Period %2d) 순수익 %.2f' %
                     (self.params.maperiod, Ending_value-Start_Value), doprint=True)
            data = {'STRA NAME': f'MA Period {self.params.maperiod}',
                              'NET PNL': Ending_value-Start_Value, 
                              'WinRate': round(self.trade_win_count/self.trade_count*100)}
            graph_log = graph_log.append(data,ignore_index=True)


        else:
            self.log('(Bolinger Period %2d) 순수익 %.2f' %
                     (self.params.maperiod - 10, Ending_value-Start_Value), doprint=True)
            data = {'STRA NAME': 'Bolinger Period {}'.format(self.params.maperiod - 10),
                              'NET PNL': Ending_value-Start_Value, 
                              'WinRate': round(self.trade_win_count/self.trade_count*100)}
            graph_log = graph_log.append(data,ignore_index=True)
        print('승률', round(self.trade_win_count/self.trade_count*100),'%', '이긴 횟수 : ', self.trade_win_count, '전체 거래 횟수 : ', self.trade_count)
        


btc_ohlcv = binance.fetch_ohlcv("BTC/USDT", '1m')
df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
df['datetime'] =  pd.to_datetime(df['datetime'], unit='ms')
df.set_index('datetime', inplace=True)
data = bt.feeds.PandasData(dataname=df)



# Create a cerebro entity
cerebro = bt.Cerebro()
# Add a strategy
strats = cerebro.optstrategy(
    TestStrategy,
    maperiod=range(15, 45))

cerebro.adddata(data)
Start_Value = 20000
cerebro.broker.setcash(Start_Value)
cerebro.addsizer(bt.sizers.FixedSize, stake=1)
cerebro.broker.setcommission(commission=0.001)
cerebro.run(maxcpus=1)

fig = px.bar(graph_log,
                 x= 'WinRate',
                 y='NET PNL',
                 hover_name = 'STRA NAME',
                 )#symbol = 'STRA NAME')

now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
fig.write_image('./log/지금.png')


graph_log.sort_values('NET PNL',inplace=True,ascending=False)

best_st = graph_log.iloc[0]['STRA NAME']




# 여러 전략 중 최선의 전략 자세히 기록 여기에 기록 true 저장 해야함.

cerebro_real = bt.Cerebro()
start_params = {'maperiod': int(best_st[-2:])+10, 'printall' : True}
cerebro_real.addstrategy(TestStrategy, start_params)
cerebro_real.adddata(data)
Start_Value = 20000
cerebro_real.broker.setcash(Start_Value)
cerebro_real.addsizer(bt.sizers.FixedSize, stake=1)
cerebro_real.broker.setcommission(commission=0.001)
cerebro_real.run()
#cerebro_real.plot(style="candle", barup="red", bardown="blue",)
