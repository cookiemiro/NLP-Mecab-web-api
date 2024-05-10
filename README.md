# NLP-Mecab-web-api
형태소 분석기를 웹 api 형식으로 만들었습니다.

## 리눅스 환경에서만 가능합니다.

### 1. 프로젝트 디렉토리에 한국어 형태소 분석기 mecab-ko를 설치합니다.

### 2. 사용자 사전 적용을 위해 프로젝트 경로에 bash 파일을 생성해서 다음의 코드를 넣어줍니다.

```
#!/bin/bash

cd {home directory}/keyword-extraction-master/mecab-ko-dic-2.1.1-20180720

sudo make install
```

※ 관리자 권한으로 컴파일이 필요하기 때문에 환경변수에 sudo password가 필요함.

### 3. /analyzer/dict/에 다음과 같은 형태로 api 요청을 보냅니다.
```
{
    "extractAdjectives" : true,
    "keywordExtraction" : true,
    "ignoreOneWord" : false,
    "text" : [
        {
            "person" : "테스터1",
            "answer" : ["버스정거장에 버정과 버스 사이", "버스정거와 버스는 버쩡 옆에 있어요."]
        },{
            "person" : "테스터2",
            "answer" : ["버스정거장1에 버정1과 버스1 사이", "버스정거1와 버스1는 버쩡1 옆에 있어요."]
        }
    ], 
    "type" : "고유명사",
    "dicts" : [
        {
            "representative_keyword" : "버스정거장", 
            "keywords" : [
                "버정",
                "버스",
                "버쩡",
                "버스정거"
             ]
         },
        {
            "representative_keyword" : "버스정거장1", 
            "keywords" : [
                 "버정1",
                 "버스1",
                 "버쩡1",
                 "버스정거1"
            ]
        }
    ]
}
```

### 4. 위에서부터 키값은
- extractAdjectives: 형용사 추출여부

- keywordExtraction: 명사 추출여부

- ignoreOneWord: 1개의 단어 제외 여부

- text: 저희 프로젝트의 형식에 맞게 만들었습니다. 원하시면 string으로 사용하시면 됩니다. 처음에 string으로 개발하고 이후에 바꿨습니다.

- type: 나중에 단어 타입에 따라 분기처리 하기 위해 추가

- dicts: 저희 프로젝트 형식에 맞췄습니다. 모두 사용자 사전으로 등록됩니다.

### 5. 서버 배포 방법
nohup gunicorn --bind=127.0.0.1:8000 --timeout=120 --workers=9 analyzer.wsgi:application &

### 6. 깃헙 레포 토큰 등록
https://tomatohj.tistory.com/20

### ※ api 서버로 사용했기 때문에 데이터 베이스는 사용하지 않았습니다.