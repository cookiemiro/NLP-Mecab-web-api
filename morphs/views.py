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

def read_csv_file(request):
    if request.method == "POST":
        print(request.body)
        json_data = json.loads(request.body)
        print(json_data)
        
        extractAdjectives = json_data["extractAdjectives"]
        keywordExtraction = json_data["keywordExtraction"]
        ignoreOneWord = json_data["ignoreOneWord"]
        text = json_data["text"]
        dicts = json_data["dicts"] if "dicts" in json_data else None
        print(extractAdjectives)
        print(ignoreOneWord)
        print(keywordExtraction)
        print(text)
        print(dicts)
        
        if extractAdjectives:
           language = "kor-adjective"
        elif extractAdjectives and keywordExtraction:
            language = "kor-adjective-and-noun"
        else:
            language = "kor"
        
        print(language)
        
        if json_data["type"] == "고유명사":

            # # 기존 CSV 파일 불러오기
            # existing_data = []
            # with open('existing_data.csv', 'r', newline='', encoding='utf-8') as csvfile:
            #     reader = csv.reader(csvfile)
            #     existing_data = list(reader)

            # # CSV 파일에 데이터 추가
            # with open('existing_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
            #     writer = csv.writer(csvfile)
            #     for row in converted_data:
            #         writer.writerow(row)

            # # 기존 데이터에 새로운 데이터 추가
            # existing_data.extend(converted_data)

            # # 결과 확인을 위해 출력
            # for row in existing_data:
            #     print(row)
                
            
            # print(request.FILES)

            # file = request.FILES["csv"]
            # # 파일 내용을 읽어옴
            # file_content = file.read().decode("utf-8")
            # # CSV 파싱

            # print(file_content)
            # # csv_reader = csv.reader(file_content.splitlines(), delimiter=',')
            # # for row in csv_reader:
            # #     print(row)
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
            keyword_data = run_keyword_extraction_api(text, language=language, max_num_keywords=30, min_length=1 if ignoreOneWord else 0)
            print(keywords)
            
            response = []
            
            for item in dicts:
                representative_keyword = item['representative_keyword']
                keywords = item['keywords']
                representative_count = 0
                
                # 대표 키워드와 해당하는 키워드들의 빈도수 합산
                for i, (keyword, count) in enumerate(keyword_data):
                    if keyword == representative_keyword or keyword in keywords:
                        representative_count += count
                
                # 키워드 개수를 대표 키워드로 통합
                for i, (keyword, count) in enumerate(keyword_data):
                    if keyword == representative_keyword or keyword in keywords:
                        keyword_data[i] = (representative_keyword, representative_count)

            # 중복된 튜플 제거
            keyword_data = list(set(keyword_data))
                        
            response = {
                "keywords" : keyword_data,
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