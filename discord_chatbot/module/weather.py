from datetime import datetime
import requests

now = datetime.now()
date = now.strftime("20%y%m%d")
key = "JwIEkikJEsIVjZCFDq2zGhNWqyrlUxXXAtFYLz5Jv1cjwzi011MEZbL2szuMIg2z5IbZsp6Y%2FjMzs9%2B%2FU%2BkNCw%3D%3D"

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
params ={'serviceKey' : 'JwIEkikJEsIVjZCFDq2zGhNWqyrlUxXXAtFYLz5Jv1cjwzi011MEZbL2szuMIg2z5IbZsp6Y%2FjMzs9%2B%2FU%2BkNCw%3D%3D', 'pageNo' : '1', 'numOfRows' : '5', 'dataType' : 'JSON', 'base_date' : date, 'base_time' : '0600', 'nx' : '73', 'ny' : '66' }

response = requests.get(url, params=params)
print(response.content)

