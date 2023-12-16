import re
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup
from html_table_parser import parser_functions


def get_menu_data(user):
    result = []
    now = datetime.now()
    date = now.strftime("%m%d")
    time = now.strftime('%H')
    time = int(time)

    if user == '푸름':
        webpage = requests.get("https://dorm.kumoh.ac.kr/dorm/restaurant_menu01.do#")
        soup = BeautifulSoup(webpage.content, "html.parser")
        data = soup.find('table', {'class': 'smu-table tb-w150'})
        table = parser_functions.make2d(data)
        df = pd.DataFrame(data=table[1:], columns=table[0])
        # 각 칼럼 이름에서 숫자만 추출하여 새로운 칼럼 이름으로 설정
        new_columns = [re.sub("[^0-9]", "", column) for column in df.columns]
        df.columns = new_columns
        df.index = ['중식', '석식']
        for data in df[date]:
            result.append(data.replace('\n', '\n'))
        if 14 < time < 19:
            return result[1]
        else:
            return result[0]

    elif user == '오름1':
        webpage = requests.get("https://dorm.kumoh.ac.kr/dorm/restaurant_menu02.do#")
        soup = BeautifulSoup(webpage.content, "html.parser")
        data = soup.find('table', {'class': 'smu-table tb-w150'})
        table = parser_functions.make2d(data)
        df = pd.DataFrame(data=table[1:], columns=table[0])

        # 각 칼럼 이름에서 숫자만 추출하여 새로운 칼럼 이름으로 설정
        new_columns = [re.sub("[^0-9]", "", column) for column in df.columns]
        df.columns = new_columns

        df.index = ['중식', '석식']
        for data in df[date]:
            result.append(data.replace('\n', '\n'))
        if 14 < time < 19:
            return result[1]
        else:
            return result[0]

    elif user == '오름3':
        webpage = requests.get("https://dorm.kumoh.ac.kr/dorm/restaurant_menu03.do#")
        soup = BeautifulSoup(webpage.content, "html.parser")
        data = soup.find('table', {'class': 'smu-table tb-w150'})
        table = parser_functions.make2d(data)
        df = pd.DataFrame(data=table[1:], columns=table[0])
        # 각 칼럼 이름에서 숫자만 추출하여 새로운 칼럼 이름으로 설정
        new_columns = [re.sub("[^0-9]", "", column) for column in df.columns]
        df.columns = new_columns

        df.index = ['중식', '석식']
        for data in df[date]:
            result.append(data.replace('\n', '\n'))
        if 14 < time < 19:
            return result[1]
        else:
            return result[0]

    elif user == '학생식당':
        webpage = requests.get("https://www.kumoh.ac.kr/ko/restaurant01.do")
        soup = BeautifulSoup(webpage.content, "html.parser")

        data = soup.find('table', {'class': 'smu-table tb-w150'})

        table = parser_functions.make2d(data)

        df = pd.DataFrame(data=table[1:], columns=table[0])

        # 각 칼럼 이름에서 숫자만 추출하여 새로운 칼럼 이름으로 설정
        new_columns = [re.sub("[^0-9]", "", column) for column in df.columns]
        df.columns = new_columns

        df.index = ['조식', '중식']
        for data in df[date]:
            result.append(data.replace('\n', '\n'))
        if 11 < time < 14:
            return result[1]
        else:
            return result[0]


    elif user == '교직원식당':
        webpage = requests.get("https://www.kumoh.ac.kr/ko/restaurant02.do")

        soup = BeautifulSoup(webpage.content, "html.parser")

        data = soup.find('table', {'class': 'smu-table tb-w150'})

        table = parser_functions.make2d(data)

        df = pd.DataFrame(data=table[1:], columns=table[0])

        # 각 칼럼 이름에서 숫자만 추출하여 새로운 칼럼 이름으로 설정
        new_columns = [re.sub("[^0-9]", "", column) for column in df.columns]
        df.columns = new_columns

        df.index = ['중식', '석식']
        for data in df[date]:
            result.append(data.replace('\n', '\n'))
        if 14 < time < 19:
            return result[1]
        else:
            return result[0]


    elif user == '분식당':
        webpage = requests.get("https://www.kumoh.ac.kr/ko/restaurant04.do")

        soup = BeautifulSoup(webpage.content, "html.parser")

        data = soup.find('table', {'class': 'smu-table tb-w150'})

        table = parser_functions.make2d(data)

        df = pd.DataFrame(data=table[1:], columns=table[0])

        # 각 칼럼 이름에서 숫자만 추출하여 새로운 칼럼 이름으로 설정
        new_columns = [re.sub("[^0-9]", "", column) for column in df.columns]
        df.columns = new_columns

        df.index = ['일품요리']
        for data in df[date]:
            result.append(data.replace('\n', '\n'))

        return result[0]

    else:
        return '오류!'



