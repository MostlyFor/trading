# trading

![image](https://user-images.githubusercontent.com/106165619/199129183-970b8c4b-af0f-41bd-9d82-7ee27a25d862.png)


![image](https://user-images.githubusercontent.com/106165619/199129198-12c9f838-1efa-4bf3-abec-9f0ef446cdb0.png)


![image](https://user-images.githubusercontent.com/106165619/199129220-9862e3b2-d248-4816-b8dd-da79e09792d7.png)


![image](https://user-images.githubusercontent.com/106165619/199129235-9ec5ee8a-c996-427d-acb8-a2cbedea51c2.png)



프로그램 전반적인 구조

while(button 누를 때 까지){  
      코인 봇 생성(BTC, ETH 등)   
      현재 가격 받아옴  
      관심있는 코인 1에 대해 다음을 적용  
      {  1. 현재 사용하고 있는 전략에 대해 진입 조건에 맞는지 확인  
      2. 진입 조건이 맞으면 포지션 관리자 진입  
      3. 사용하고 있는 전략에 현재 가격을 대입하여 TP/SL 값 다시 수정  
      4. 거래가 체결 되었다면 코인 봇 초기화  }   
      관심있는 코인 2에 대해 위와 같이 적용 {}  
}



1. 봇(포지션 관리자) – 여러 개의 봇이 필요하므로 클래스로 구현
(비트코인, 이더리움 등등 거래하는 코인마다 객체 하나가 담당함)


 - 주된 역할 : 
  
  
              1. 거리 내역 저장


              2. 포지션 진입
                
                
              3. 포지션 TP(목표가) / SL(손절라인) 지정

              
              
2. 전략 관리자 (백테스팅을 담당하는 함수 및 클래스..?)


3. 잔고 관리자 (잔고를 관리하고 현금화하거나 할 때 사용)
              
