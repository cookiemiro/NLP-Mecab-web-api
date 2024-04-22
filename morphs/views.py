from django.http import HttpResponse, JsonResponse
from django.conf import settings
import src.keywordExtraction.keyword_extraction
from src.keywordExtraction.keyword_extraction import run_keyword_extraction_api
import json
from importlib import reload
import subprocess


def run_test_script(request):
    # test_script.py 실행
    if request.method == "POST":
        json_data = json.loads(request.body)
        in_string = json_data["text"]
        print(in_string)
        
        # 모듈 reload를 통하여 함수가 새롭게 로딩될 수 있도록 함.
        reload(src.keywordExtraction.keyword_extraction)
        a = run_keyword_extraction_api(in_string, language='kor-adjective-and-noun', max_num_keywords=10)
        print(a)
        response = {
            "noun" : a,
            "message": 'Test script executed successfully!',
        }

        return JsonResponse(response)
    else:
        return HttpResponse("POST 요청만 허용됩니다.", status=405)

# wsl port-forwarding: https://thenicesj.tistory.com/775
# https://codeac.tistory.com/118
def read_csv_file(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        
        extractAdjectives = json_data["extractAdjectives"]
        keywordExtraction = json_data["keywordExtraction"]
        ignoreOneWord = json_data["ignoreOneWord"]
        text = json_data["text"]
        dicts = json_data["dicts"] if "dicts" in json_data else None 
        
        if json_data["type"] == "고유명사":
            # 사용자 사전에 대한 폴더 설명 및 우선 순위 적용(윈도우지만 설명이 잘 되어 있음): https://luminitworld.tistory.com/104
            # 사용자 사전 적용 우선순위: https://mondayus.tistory.com/46
            # 종성 추가에 문제가 생기면 보고 적용하기: https://hipster4020.tistory.com/184
            # 사용자 사전의 형식: https://joyhong.tistory.com/128
            if dicts:
                file_path = '/home/xodml/keyword-extraction-master/mecab-ko-dic-2.1.1-20180720/user-dic/nnp.csv'

                for i in range(len(dicts)):
                    dict_item = dicts[i]
                    representative_keyword = dict_item["representative_keyword"]
                    keywords = dict_item["keywords"]
                
                    with open(file_path, 'a', encoding='utf-8') as f:
                        
                        # csv 파일에 첫 번째에 빈줄이 있으면 사전 적용이 잘 되지 않음.
                        if i == 0:
                            f.seek(0)  # 파일의 처음으로 이동
                            f.truncate()  # 파일 내용을 지움

                            # 파일에 내용 쓰기
                            f.write(f"{representative_keyword},,,,NNP,*,T,{representative_keyword},*,*,*,*,*")

                        else:
                            f.write(f"\n{representative_keyword},,,,NNP,*,T,{representative_keyword},*,*,*,*,*")
                    
                        for keyword in keywords:   
                            # 파일에 내용 쓰기
                            f.write(f"\n{keyword},,,,NNP,*,T,{keyword},*,*,*,*,*")

                commands = [
                    "/home/xodml/keyword-extraction-master/mecab-ko-dic-2.1.1-20180720/tools/add-userdic.sh",
                    "/home/xodml/keyword-extraction-master/user-dic.sh",
                ]
                
                sudo_password = settings.SUPERUSER_KEY
            
                for cmd in commands:
                    run_bash_command(cmd, sudo_password)
                    # time.sleep(1)
                    
            reload(src.keywordExtraction.keyword_extraction)
            
            keyword_response = []
            
            for text_data in text:  # 각 텍스트 데이터에 대해 처리
                person = text_data["person"]
                answers = text_data["answer"]
                
                str_txt = ""
            
                for answer in answers:  # 각 답변에 대해 형태소 분석 적용  
                    if answer.endswith("."):
                        str_txt += answer + " "
                    else:
                        str_txt += answer + ". "
                
                print(str_txt)  
                    
                sentence_language = detect_language(str_txt)
                
                if sentence_language == "Korean":
                    if extractAdjectives:
                        language = "kor-adjective"
                    elif extractAdjectives and keywordExtraction:
                        language = "kor-adjective-and-noun"
                    else:
                        language = "kor"
                elif sentence_language == "English":
                    if extractAdjectives:
                        language = "eng-adjective"
                    elif extractAdjectives and keywordExtraction:
                        language = "eng"
                    else:
                        language = "eng"
                    
                keyword_data =  run_keyword_extraction_api(str_txt, language=language, max_num_keywords=30, min_length=1 if ignoreOneWord else 0)
        
                for item in dicts:
                    representative_keyword = item['representative_keyword']
                    keywords = item['keywords']
                    representative_count = 0
                    
                    # 대표 키워드와 해당하는 키워드들의 빈도수 합산
                    for i, (keyword, count) in enumerate(keyword_data):
                        if keyword == representative_keyword or keyword in keywords:
                            representative_count += count
                    
                    # 키워드 개수를 대표 키워드로 통합
                    # 하위 키워드들을 대표 키워드로 변경
                    for i, (keyword, count) in enumerate(keyword_data):
                        if keyword == representative_keyword or keyword in keywords:
                            # 각 인덱스의 값들을 튜플로 변환
                            keyword_data[i] = (representative_keyword, representative_count)

                # 중복된 튜플 제거
                # 집합({})을 사용해서 중복된 데이터(튜플)들을 제거
                keyword_data = list(set(keyword_data))
                    
                keyword_response.append({
                    "person": person,
                    "analyzed_answer": keyword_data
                })
                      
            response = {
                "keywords" : keyword_response,
                # "text_language" : sentence_language,
                "message": {
                    "dict": "사용자 사전이 저장되었습니다.",
                    "keywords": "키워드 추출이 완료 되었습니다."
                },
            }

        return JsonResponse(response, status=200)
    else:
        return HttpResponse("POST 요청만 허용됩니다.", status=405)

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

# 요약문에 대한 요구사항을 확인하고 추가
# 요약문 전부 한국어와 영문이 들어옴.
def detect_language(text):
    k_count = 0
    e_count = 0
    for c in text:
        if ord('가') <= ord(c) <= ord('힣'):
            k_count+=1
        elif ord('a') <= ord(c.lower()) <= ord('z'):
            e_count+=1
    return "Korean" if k_count>e_count else "English"