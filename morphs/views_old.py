from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from src.keywordExtraction.keyword_extraction import run_keyword_extraction_api
import os
import csv
import sys
import subprocess


def run_test_script(request):
    # test_script.py 실행
    in_string = '버스정류장은 버정과 뻐정 사이에 있어요. 정류장은 저쪽에 있고요. 버스는 지금 오고 있습니다. 버저를 눌러주세요. 버는 여기에 있어요'
    print(settings.BASE_DIR)
    a = run_keyword_extraction_api(in_string, language='kor', max_num_keywords=10)
    print(a)
    response = {
        "noun" : a,
        "message": 'Test script executed successfully!',
    }

    return JsonResponse(response)

def read_csv_file(request):
    print(request.POST)
    if request.POST["type"] == "고유명사":
        print(request.FILES)

        file = request.FILES["csv"]
        # 파일 내용을 읽어옴
        file_content = file.read().decode("utf-8")
        # CSV 파싱

        print(file_content)
        # csv_reader = csv.reader(file_content.splitlines(), delimiter=',')
        # for row in csv_reader:
        #     print(row)

        file_path = '/home/xodml/keyword-extraction-master/mecab-ko-dic-2.1.1-20180720/user-dic/nnp.csv'

        commands = [
            "/home/xodml/keyword-extraction-master/mecab-ko-dic-2.1.1-20180720/tools/add-userdic.sh",
            "/home/xodml/keyword-extraction-master/user-dic.sh",
        ]
        
        sudo_password = "Idea1004!!"
        
        for cmd in commands:
            run_bash_command(cmd, sudo_password)

        with open(file_path, 'w', encoding='utf-8') as f:
            # 파일에 내용 쓰기
            f.write(file_content)

    return JsonResponse({"message": "사용자 사전이 저장되었습니다."})

def run_bash_command(command, password):
    try:
        # sudo로 실행하려면 shell=True와 함께 subprocess.Popen을 사용하십시오.
        process = subprocess.Popen(['sudo', '-S', 'bash', '-c', command], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=(password + '\n').encode())
        if process.returncode != 0:
            # 에러 처리
            print(f"에러 발생: {stderr.decode()}")
        else:
            # 성공적으로 실행된 경우
            print(f"출력: {stdout.decode()}")
    except Exception as e:
        # 예외 처리
        print(f"에러 발생: {str(e)}")