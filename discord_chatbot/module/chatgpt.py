
import os

import openai

import food

# 파일 경로 설정
file_path = '/Users/dryoon04/Documents/GitHub/university-project/discord_chatbot/api key.txt'

# 파일 열기 (읽기 모드로 열기)
with open(file_path, 'r', encoding='utf-8') as file:
    # 파일 내용 읽어오기
    file_content = file.read()
os.environ["OPENAI_API_KEY"] = file_content
openai.api_key = os.getenv("OPENAI_API_KEY")


def chat(user):

    completion = openai.ChatCompletion.create(
    model="gpt-4-1106-preview",
    messages=[
        {"role": "system",
         "content": """사용자의 명령을 인식헤서 분류하는 쳇봇이다. 다음과 같이 무조건 답을 해야한다.(양식 설명의 중괄호는 뺴고 답하기)
                    기숙사 메뉴나 학생식당의 매뉴등을 물어본다면 {식단 장소이름 시간} 이 양식으로 답하면 된다.
                    분류할 수 없는 질문을 하면 {오류} 라고 대답하면 된다."""},
        {"role": "user", "content": f"{user}"},

    ],
    temperature=0,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    )


    ans = completion["choices"][0]["message"]["content"].split()

    if ans[0] == '식단':
        return food.get_menu_data(ans[1])




