import re
import time
from bs4 import BeautifulSoup
from tqdm.notebook import tqdm
import matplotlib.pyplot as plt
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


nickname = input('op.gg 사이트에서 검색할 닉네임을 입력해주세요 : \n')
url = f'https://www.op.gg/summoners/kr/{nickname}'

# Chrome 드라이버 경로 설정
driver = webdriver.Chrome()

# op.gg 웹 사이트로 이동
print('로딩중...')
driver.get(url)

look = driver.find_element(By.CSS_SELECTOR, ".css-n9kjrp .header-profile-info .info > .last-update").text
print(look)

if re.search(r'(\d+)+(시간|일)\s+전', look):
    driver.find_element(By.CSS_SELECTOR, ".css-1ki6o6m.e18vylim0").click()
    print('데이터 최신화 중...')
    new = tqdm(range(5),desc='5초 소요',leave=False)
    for i in new:
        time.sleep(1)
    new.close()
        

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(0.5)

for i in range(1, 7):
    try:
        more_button = driver.find_element(By.CSS_SELECTOR, '.css-1s9fubg .more')
        more_button.click()
        print('게임 로드중...')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    except:
        print("더이상 찾을 데이터가 없습니다.")
        break
# details = driver.find_elements(By.XPATH, ("//div[contains(@class,'StatsButton')]"))
# for i in details:
#     i.click()
#     time.sleep(1)


    
print('완료')

html = driver.page_source
# print('파일저장중')
# f = open('/Users/dryoon/Documents/schoolproject/all.html','w')
# f.write(html)
# f.close() 
# print('저장완료!')
# driver.quit()


# # 파일 열기 (읽기 모드)
# file_path = "/Users/dryoon/Documents/schoolproject/all.html"  # 파일 경로를 지정합니다.
# file = open(file_path, "r")


# BeautifulSoup을 사용하여 HTML 파싱
# soup = BeautifulSoup(file, 'html.parser')

soup = BeautifulSoup(html, 'html.parser')
# "game-content" 클래스 선택
game_content = soup.select('div.game-content')

#가져온 게임수 세기
recent_game_len = len(game_content)
print(f'가져온 게임의 판수는 {recent_game_len}판 입니다')

# 승패가져와서 데이터프레임으로 저장
result_all = soup.find_all(class_="result")
result_values = [result.get_text() for result in result_all]
df_result = pd.DataFrame({'결과': result_values})

#승리와 패베 개수샘
result_num = df_result['결과'].value_counts()

#kda 가져와서 데이터프레임으로 저장
result_kda = soup.find_all(class_="k-d-a")
kda_values = [kdaresult.get_text() for kdaresult in result_kda]
del kda_values[0]
df_kda = pd.DataFrame({'k/d/a': kda_values})

print(f"승리{result_num['승리']}판")
print(f"패배{result_num['패배']}판")
winrate = "%0.2f"%((result_num["승리"]/recent_game_len)*100)
print(f'승률 : {winrate}%')
print(df_result)
# ratio = [result_num['승리'],result_num['패배']]
# labels = ['승리', '패배']

# plt.pie(ratio, labels=labels, autopct='%.1f%%')
# plt.show()
# file.close()
# 승리기록이 없을시 오류발생