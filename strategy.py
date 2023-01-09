from indicators import *



# 1분봉 볼린져 밴드 상단으로 일정 만큼 위로 올라오고 5분봉 상단에 있다면 short
# tp : 볼린져 밴드 중단
# sp : 볼린져 

def bollinger_upper_short(symbol,price,period):
    upper,middle,lower=bollinger(symbol,'1m',period)
    
    gap = upper-lower
    
    
    Upper,Middle,Lower = bollinger(symbol,'5m',period)
    
    if price > (gap/100 *5 + upper) and price > Upper:
        return (True,middle,upper+ gap/100 * 15)
                
    return (False,0,0)



def bollinger_upper_short_for_test2(symbol,price,period):
    upper,middle,lower=bollinger(symbol,'1m',period)
    
    gap = upper-lower
    
    if price >  + upper:
        return (True,middle,upper+ gap/100 * 15)
                
    return (False,0,0)


buy_price = None

def bollinger_upper_short_for_test(symbol,price,period):
    upper,middle,lower=bollinger(symbol,'1m',period)
    
    if price < lower:
        buy_price = price
        return (True,middle,buy_price*99%100)
                
    return (False,0,0)