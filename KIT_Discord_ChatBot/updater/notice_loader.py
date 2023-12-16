import os
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

df = pd.read_csv("module/data/notice.csv")

#제목과 url을 딕셔너리로 만들기
title_url = {}
for i in range(len(df)):
    title_url[df['제목'][i]] = df['url'][i]

    from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}

for title, url in tqdm(title_url.items()):
    clean_title =  re.sub('[^a-zA-Z0-9가-힣\s]', '', title)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    board_contents = soup.find('div', class_='board-contents')
    
    # 공지사항의 내용을 가져옴
    text_content = board_contents.get_text(separator='\n', strip=True)
    text_content = re.sub(r'\n','', text_content)

    file_name = f"module/data/notice_txt/{clean_title}.txt"
    #데이터 프레임에 본문 내용 추가
    df.loc[df['제목'] == title, '본문'] = text_content
    #파일로 저장

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(f"url : {url}\n{text_content}")
    