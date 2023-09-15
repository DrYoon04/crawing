import requests
from bs4 import BeautifulSoup
from html_table_parser import parser_functions
import pandas as pd
from datetime import datetime
import re

user = input('동이름을 적어주세요(오름1, 오름3, 푸름)') #동이름 선택
result = []
now = datetime.now()
date = now.strftime("%m%d") #오늘 날짜를 구함
time = now.strftime('%H') # 오늘 시간을 구함
time = int(time) #str에서 int로 변환

if user == '푸름':
    webpage = requests.get("https://dorm.kumoh.ac.kr/dorm/restaurant_menu01.do#")
elif user== '오름1':
    webpage = requests.get("https://dorm.kumoh.ac.kr/dorm/restaurant_menu02.do#")
elif user == '오름3':
    webpage = requests.get("https://dorm.kumoh.ac.kr/dorm/restaurant_menu03.do#")


soup = BeautifulSoup(webpage.content, "html.parser") 

data = soup.find('table', {'class': 'smu-table tb-w150'}) #html에서 class에 해당하는 테이블을 찾음

table = parser_functions.make2d(data) #찾은 테이블을 table에 저장

df = pd.DataFrame(data=table[1:], columns=table[0]) #데이터 프레임에 저장

# 각 칼럼 이름에서 숫자만 추출하여 새로운 칼럼 이름으로 설정
new_columns = [re.sub("[^0-9]", "", column) for column in df.columns]
df.columns = new_columns

df.index = ['중식', '석식']
for data in df[date]: #띄어쓰기 정리
    result.append(data.replace('\n', '\n'))

if 14<time<19: #현제 시간에 따라 중식 식단이나 석식 식단이 출력됨
    print(result[1])
else:
    print(result[0])