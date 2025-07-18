dicts = [
            {
                'representative_keyword': '토스페이',
                'keywords': [
                    '토스',
                    '페이'
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

text = "토스페이와 토스와 페이가 들어옵니다. 왜 토스와 페이가 인기가 있을까요?."

keyword_data = [('토스페이', 2), ('토스', 1), ('페이', 1), ('형태소', 1), ('올리브영', 2), ('올영', 1), ('올리브 영', 3)]

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

def detect_language(text):
    k_count = 0
    e_count = 0
    for c in text:
        if ord('가') <= ord(c) <= ord('힣'):
            k_count+=1
        elif ord('a') <= ord(c.lower()) <= ord('z'):
            e_count+=1
    return "Korean" if k_count>e_count else "English"

# 변환된 데이터 확인
print(keyword_data)

print(detect_language(text))