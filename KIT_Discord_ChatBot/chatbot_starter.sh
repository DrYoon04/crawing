#!/bin/bash

conda activate discord
sleep 1
echo "Discord ChatBot Starter"
sleep 1

sudo service elasticsearch start
echo "Elasticsearch started"
sleep 1
# 몇초동안 입력이 없으면 자동 실행

echo "Starting..."
#기다리기
sleep 1


# 파이썬 파일이 있는 디렉터리 경로
directory_path="/home/dryoon/KIT_Discord_ChatBot"

# Git 저장소로 이동
cd "$directory_path"
echo "Git repository: $directory_path"
echo "-----------------------"
echo "변경사항 확인중..."
echo "github에서 pull을 이용해서 변경사항을 확인합니다"
sleep 1

# Git 저장소에서 최신 변경사항 가져오기
git pull
echo "확인완료"
echo "-----------------------"
# 실행할 파이썬 파일 이름
python_file="main.py"

# 파이썬 파일 실행
python "$python_file"
echo "실행중..."
sleep 1
