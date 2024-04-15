dicts = [
            {
                'representative_keyword': '형태소 분석기',
                'keywords': [
                    '분석기',
                    '형태소'
                ]
            },
            {
                'representative_keyword': '올리브영',
                'keywords': [
                    '올영',
                    '올리브 영'
                ]
            }
        ]


keyword_data = [('분석', 2), ('형태소 분석기', 1), ('분석기', 1), ('형태소', 1), ('올리브영', 2), ('올영', 1), ('올리브 영', 3)]

# 대표 키워드별 빈도수 계산
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

# 변환된 데이터 확인
print(keyword_data)