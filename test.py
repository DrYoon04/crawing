from selenium import webdriver
from selenium.webdriver.common.by import By
import time
nickname = input('검색하고 싶은 소환사이름을 입력해주세요!')
url = f'https://www.op.gg/summoners/kr/{nickname}'
# Chrome 드라이버 경로 설정
driver = webdriver.Chrome()
# op.gg 웹 사이트로 이동
driver.get(url)

element = driver.find_element(By.CSS_SELECTOR, '.css-1s9fubg .more')
element.click()
time.sleep(30)
driver.quit()