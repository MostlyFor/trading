from indicators import *

def sample1():
    return True


# 1분봉 볼린져 밴드 상단으로 일정 만큼 위로 올라오고 5분봉 상단에 있다면 short
# tp : 볼린져 밴드 중단
# sp : 볼린져 

def bollinger_upper_short(symbol,price):
    upper,middle,lower=bollinger(symbol,'1m')
    
    gap = upper-lower
    
    
    Upper,Middle,Lower = bollinger(symbol,'5m')
    
    if price > (gap/100 *5 + upper) and price > Upper:
        return (True,middle,upper+ gap/100 * 15)
                
    return (False,0,0)



bollinger_upper_short('BTC/USDT',1)