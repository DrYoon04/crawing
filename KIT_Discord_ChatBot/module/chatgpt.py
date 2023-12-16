import os
from datetime import datetime
import base64
from openai import OpenAI
from module import elasticsearch_engine as ese
from module import food

now = datetime.now()
date = now.strftime("%Y-%m-%d")

file_path = "gpt_key_base64.txt"
with open(file_path, 'r') as file:
    # 파일 내용 읽기
    encoded_content = file.read()
    # base64 디코딩
    decoded_content = base64.b64decode(encoded_content)
    decoded_string = decoded_content.decode('utf-8')

os.environ["OPENAI_API_KEY"] = decoded_string
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=decoded_string,
)

def chat(user):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system",
             "content": f"오늘 날짜 : {date}"
                        "마크다운언어를 이용해서 깔끔하게 보여준다."
                        "사용자의 명령을 인식헤서 분류하는 쳇봇이다. 다음과 같이 무조건 답을 해야한다.(양식 설명의 중괄호는 뺴고 답하기)"
                        "기숙사 메뉴나 학생식당의 매뉴등을 물어본다면 {식단 장소이름 시간} 이 양식으로 답하면 된다."
                        "학교 공지사항을 물어본다면 {공지사항 물어본내용 오늘날짜는(오늘날짜)이다}이 양식으로 답하면 된다"
                        "그외는 알아서 답해준다."
                        "분류할 수 없는 질문을 하면 잘모르겠다 라고 대답하면 된다."},
            {"role": "user", "content": f"{user}"},
        ],
        model="gpt-4-1106-preview",
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # content 추출
    content = chat_completion.choices[0].message.content.split()

    if content[0] == '식단':

        return food.get_menu_data(content[1])
    elif content[0] == "공지사항":
        combined_string = ' '.join(content[1:])
        school = ese.elasticsearch_finder(combined_string)
        return school
    else:
        return content[0]