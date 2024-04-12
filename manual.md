# Installation

    ./mecab.sh
    pip3 install .

# User Guide

## Getting Started

    python test_script.py

## Daglo (Input: google result)

    from keywordExtraction import runKeywordExtraction
    runKeywordExtraction('korean_sample.json', language='kor')
    runKeywordExtraction('english_sample.json', language='eng')

## String (Input: string)

    from keywordExtraction import runKeywordExtractionString
    korean_string = '샘플 텍스트 샘플'
    english_string = 'sample text in lowercase, if english text, convert it to lowercase'
    candidate_num = 50
    target_keywords_num = 10
    runKeywordExtractionString(korean_string, candidate_num, target_keywords_num, language='kor')
    runKeywordExtractionString(english_string, candidate_num, target_keywords_num, language='eng')

## run_keyword_extraction_api

| args | default | description |
|--|--|--|
| in_string || 입력 string |
| language | `kor` | 언어 (`kor`:한국어 명사, `kor-adjective`:한국어 형용사, `eng`:영어 명사, `eng-adjective`:영어 형용사) |
| max_num_keywords | `10` | 출력 키워드 개수 |
