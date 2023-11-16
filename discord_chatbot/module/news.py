import requests
from bs4 import BeautifulSoup
import re
import pandas as pd



url = "https://news.daum.net/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}

html = requests.get(url, headers=headers)
soup = BeautifulSoup(html.content, 'html.parser')
news_block = soup.find(class_="box_g box_news_issue")
news_main = news_block.find_all(class_="tit_g")

news_block_len = len(news_main)

news_content_link = []
news_content_headline = []

for i in range(news_block_len):
    link_element = news_main[i].find('a', class_='link_txt')
    if link_element and 'href' in link_element.attrs:
        news_content_link.append(link_element['href'])
    else:
        news_content_link.append("N/A")  
        
    # 기사 제목을 추출합니다.
    headline_element = news_main[i].find('a')
    if headline_element:
        news_content_headline.append(headline_element.text)
    else:
        news_content_headline.append("N/A")
        # 기사 제목을 찾을 수 없는 경우 처리

cleaned_data = []
for item in news_content_headline:
    # 공백 제거 및 제목 부분 추출
    cleaned_item = re.sub(r'\n\s*', '', item.strip())
    cleaned_data.append(cleaned_item)


# 가져온 내용 출력
print(f'가져온 뉴스의 해드라인은 {news_block_len}개 입니다')
for i in range(news_block_len):
    print(f"{i+1} 기사 제목: {cleaned_data[i]}")
    print(f"링크: {news_content_link[i]}")

for selected_news_link in news_content_link:
    # 선택한 뉴스 링크의 내용을 가져옵니다
    html = requests.get(selected_news_link, headers=headers)
    soup = BeautifulSoup(html.content, 'html.parser')

    # 뉴스 기사의 텍스트 내용을 추출하고 처리합니다
    news_text = []
    for p in soup.find_all('p', {'dmcf-ptype': 'general'}):
        add_text = []
        extracted_text = p.get_text()
        print(extracted_text)
        add_text.append(extracted_text)

    add_text = ' '.join(add_text)
    news_text.append(add_text)

print(len(news_text))
        
# 판다스 데이터 프레임 생성
df = pd.DataFrame({'기사 제목': cleaned_data, '본문': news_text})
#csv로 저장
df.to_csv('news.csv', index=False)