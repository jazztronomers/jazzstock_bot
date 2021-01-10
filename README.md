## Summary

1. 웹페이지: 일단위로 수급정보를 가공하여 시각화하는 서비스
    - <a>jazzstock.net</a> 
    
2. 탤래그램알람봇: 기관외인도합 수급상위 400종목의 체결정보를 실시간으로 긁어서, 특정조건에 일치하면 Alerting 하는 서비스 
    - <a>t.me/joinchat/AAAAAEnGDPwp4RD50hrvSg</a> 

3. 개발블로그: 일상 및 개발 관련 잡담
    - <a>blog.naver.com/rubenchu</a>
    
4.  1:1 카톡: 
    - <a>open.kakao.com/o/sSgGeFnc</a>
    
5. 재즈스탁 오픈카톡방: 
    - <a>open.kakao.com/o/ge5OuYhb</a>   ## 입장코드 jazz



## FAQ

알람조건은 어떻게 되나요 ?<br>
config/condition.py 에 PROD_COND dictionary를 기반으로 운영되고 있습니다 
  

Q: 개발에 직접 참여할 수 있나요?<br>
A: 본 프로젝트를 clone하여 직접 서버(혹은 개인피씨) 로 소스구동하여 자신만의 룰로 알람봇을 구현하실 수 있습니다.
룰 구현 및 테스트 교육은 막연히 준비하고 있습니다.
3) 현재 제 채널은 기관 외인 5거래일 수급 기준으로 480종목 정렬하여 돌리고 있습니다, 조건식은 거래량 주가의 동반 상향이평괴리 발생시를 수식화하였습니다.



## Detail

재즈스탁 알람봇은 네이버증권페이지에서 1분단위 체결정보를 크롤링하여, 5분봉을 생성합니다.

생성된 5분봉이 <u>사전에 json으로 정의된 매매조건</u>과 일치 하는경우: 

* Telegram bot 을 통해서 사용자에게 메시지를 전송할 수 있습니다.

* 더 나아가서 증권사 API와 연동된 서버로 메세지를 전달하여 자동매매를 구현할 수 있습니다.

본 프로젝트를 실행하기 위해서는 Jazzstock DB와 연동되어 있어야 합니다, Jazzstock DB에는 상장종목 3년치 OHLCV 데이터 및 기관, 거래원 수급데이터가 일단위로, 재무데이터가 분기별로 수집되고 있습니다, 따라서 일봉기준 지표를 번거롭게 가공하지 않고 바로 불러올 수 있습니다. 

DB접속계정 발급관련 문의는 이메일로 보내주세요, Standalone 버전은 아직은 만들 생각없습니다



## Requirement



0. Python 3.6.x 문법을 사용합니다.

1. 사용되는 python 패키지는 requirements.txt 에서 확인합니다.

2. config/config_template.py 을 참고하여 발급받은 db접속정보를 입력하고, config.py 로 renaming합니다.

3. main/main_crawlnaver_debug.py 을 실행하여 , 전반적으로 어떻게 작동하는지 확인합니다.

   

아직은 개발단계로, 클래스구조 변화가 자주 발생합니다.

7월말까지 객체구조를 freezing 하고,  사용자가 매매조건 및 simulation만 진행할 수 있도록하는것을 목표로 삼고있습니다.



## Why Crawling ?

증권사 api의 경우 시간당 Request수가 제한되어 취급할 수 있는 종목수가 제한적입니다,

<center>5 request / 1 sec & 100 request / 1 min</center>

해당 제약사항을 해결하기 위해서 분봉생성을 자체 Crawling으로 진행하는 방법을 선택했습니다.

CSP에서 제공하는 저렴한 Instance(t2.micro 등)를 사용하면 매일매일 새로운 퍼블릭IP를 할당 받을 수 있고, 인스턴스당 1분에 100종목의 1분단위 체결정보를 20초안에 수집해올 수 있으며, 장종료시점 까지 문제없이 실행됩니다.

온디맨드 t2.nano 인스턴스기준 시간당 0.0072 USD으로, 인스턴스당 월 비용은 다음과 같다.



<center> 0.0072 USD X 7hour X 22 days = 1.1088 USD </center>.

   

인스턴스당 수집할 수 있는 종목수는 100개 까지만 테스트해봤으므로, 어느정도 버퍼가 존재합니다.


##

Pycharm 개발환경세팅: 작성예정
Ubuntu - Jupyter lab 개발환경세팅: 작성예정

## Sample

#### 

<img src="https://blogfiles.pstatic.net/MjAyMDA2MjVfMTQ0/MDAxNTkzMDU3MzM0OTAx.DtsNmIT8z0RZqM15z-0pjOXhD4h4YQ-7_PcoO6REhcMg.3qRYfKP6bScMMRbPIgCGPSWe2T0vJB9XEibitLfG7DMg.PNG.rubenchu/image.png">



보시다 시피, 인간이 직관적으로 5분봉 차트를 바라볼때 확인하는 지표들을 (볼린저밴드, stochastic slow 등)를 수집과 동시에 생성할 수 있도록 함수로 작성해두었습니다.



