class PositionManager:
    orders = [None] * 3
    
    def __init__(self):
        pass
    
    
    
    # 포지션 3개 한번에 설정
    # mode : buy or sell
    def set_position(self,binance,symbol,position_size):
        self.symbol = symbol
        self.binance = binance
        self.position_size = position_size
        
        # market price (ex: 19500$)
        self.orders[0] = self.binance.create_order(
            symbol=self.symbol,
            type="MARKET",
            side="buy",
            amount=self.position_size
        )

        # take profit 
        # 목표가는 전략에 따라 다름
        # 우선은 퍼센트로 구현함
        
        self.orders[1] = self.binance.create_order(
            symbol=self.symbol,
            type="TAKE_PROFIT_MARKET",
            side="sell",
            amount=self.position_size,
            params={'stopPrice': 20800}
        )

        # stop loss
        # 목표가는 전략에 따라 다름
        
        self.orders[2] = self.binance.create_order(
            symbol=self.symbol,
            type="STOP_MARKET",
            side="sell",
            amount=self.position_size,
            params={'stopPrice': 20600}
        )

    
    #거래 내역 저장
    def __del__(self):
        pass
        

    

#dataframe 매매시각/ 거래 번호 /포지션 사이즈/ 포지션 long/short / 진입근거유형 여부 / 포지션 손실 / 현재 잔고
