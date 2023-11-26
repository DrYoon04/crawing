from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup
from html_table_parser import parser_functions

now = datetime.now()
date = now.strftime("%Y")
time = str(date)
print("공지사항 로딩중")

url1 = "https://www.kumoh.ac.kr/ko/sub06_01_01_01.do?mode=list&&articleLimit=500&article.offset=0" #학사안내
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}

html = requests.get(url1, headers=headers)
soup = BeautifulSoup(html.content, 'html.parser')
data = soup.find('div', {'class': 'board-list01'})

table = data.find('table')
p = parser_functions.make2d(table)
#판다스 데이터프레임으로 변환
df = pd.DataFrame(p[1:], columns=p[0])


#번호 없는 행 개수 세기
count = 0
for i in df['번호']:
    if i == '':
        count += 1
#count만큼 행 삭제
df = df.drop(df.index[0:count])

#필요없는 데이터 삭제
df = df.reset_index(drop=True)
df = df.drop(['조회'], axis=1)
df = df.drop(['첨부'], axis=1)
df = df.drop(['작성자'], axis=1)


#제목만 남기고 나머지 삭제
for i in df['제목']:
    pretreatment = i.split('\n')
    clean_text = pretreatment[0]
    #판다스 제목행 수정
    df['제목'] = df['제목'].replace(i, clean_text)

#title left 클레스 안의 href 가져오기
title = data.find_all('td', {'class': 'title left'})
main_url = "https://www.kumoh.ac.kr/ko/sub06_01_01_01.do"
for i in range(len(title)):
    title[i] = title[i].find('a')
    title[i] = title[i]['href']
    title[i] = main_url+title[i]
title = title[count:]
#link 열 추가 후 title리스트에 있는 href값 넣기
df['link'] = title

df.to_csv("/Users/dryoon04/Documents/GitHub/university-project/discord_chatbot/data/notice.csv")
print("공지사항 로딩완료")

