from strategy import *


class PositionManager:
    orders = [None] * 3
    
    def __init__(self,symbol):
        self.symbol = symbol
    
    
    def set_TPSL(self,TP,SL):
        self.TP = TP
        self.SL = SL
    
    
    # mode : buy or sell
    def set_position(self,binance,position_size):
        self.binance = binance
        self.position_size = position_size
        
        # market sell
        # 시장가 진입
        self.orders[0] = self.binance.create_order(
            symbol=self.symbol,
            type="MARKET",
            side="sell",
            amount=self.position_size
        )


    def set_range(self,binance,position_size):
        self.binance = binance
        self.position_size = position_size
        
        
        # take profit 
        # 목표가는 전략에 따라 다름
        
        if self.orders[1]!=None:
            self.binance.cancel_order(self.orders[1]['id'], self.orders[1]['symbol'])
        self.orders[1] = self.binance.create_order(
            symbol=self.symbol,
            type="TAKE_PROFIT_MARKET",
            side="buy",
            amount=self.position_size,
            params={'stopPrice': self.TP,
                    "reduceOnly": True}
        )

        # stop loss
        # 목표가는 전략에 따라 다름
        if self.orders[2]!=None:
            self.binance.cancel_order(self.orders[2]['id'], self.orders[2]['symbol'])
        self.orders[2] = self.binance.create_order(
            symbol=self.symbol,
            type="STOP_MARKET",
            side="buy",
            amount=self.position_size,
            params={'stopPrice': self.SL,
                    "reduceOnly": True}
        )
        
    
    
    # 거래 내역 저장
    def save_log(self):
        pass
    
    
    def __del__(self):
        if self.orders[1]!=None:
            self.binance.cancel_order(self.orders[1]['id'], self.orders[1]['symbol'])
        if self.orders[2]!=None:
            self.binance.cancel_order(self.orders[2]['id'], self.orders[2]['symbol'])
        