#from keywordExtraction import run_keyword_extraction_string
from src.keywordExtraction.keyword_extraction import run_keyword_extraction_api
import time

# https://kugancity.tistory.com/entry/mecab%EC%97%90-%EC%82%AC%EC%9A%A9%EC%9E%90%EC%82%AC%EC%A0%84%EA%B8%B0%EB%B6%84%EC%84%9D-%EC%B6%94%EA%B0%80%ED%95%98%EA%B8%B0
# https://hipster4020.tistory.com/184

# in_string = "Australia, who have now lifted the World Cup six times, won by six wickets with seven overs left to play. The team beat South Africa in the semi-final while India beat New Zealand to make it to the final. The match was played in the world's largest stadium in the western state of Gujarat. Cricket is the most popular sport in India and more than 100,000 fans showed up at the Narendra Modi stadium in Ahmedabad city to cheer on the team. The stadium looked like a sea of blue as spectators sported team jerseys in support of their favourite players. Those who were unable to travel to Ahmedabad tuned in from their homes to watch the match, hoping that India would lift the Cup. India last won the World Cup in 2011. But the hopes of millions of Indians were dashed after Australia defeated India and thousands took to social media to express their disappointment over India's loss. Heartbreak continues for India, wrote one user on X (formerly Twitter), while another said this hurts more than anything. Many of India's top actors and sporting stars also took to X to congratulate the Indian cricket team for their stellar performance throughout the World Cup and to offer support after their loss. It's a sport and there are always a bad day or two. Unfortunately it happened today, but thank you Team India for making us so proud of our sporting legacy in cricket. You bring too much cheer to the whole of India, wrote Bollywood superstar Shah Rukh Khan who was among the spectators in the stadium. Olympic medalist Abhinav Bindra congratulated the Australian cricket team over their win and expressed solidarity with team India. You may not have clinched the final, but your performance was every bit the epitome of champions. Every match, every run, every wicket was a testament to your skill, spirit, and sportsmanship, he wrote. Many fans also expressed hope about India winning the next World Cup. India's World Cup journey might have hit a speed bump, but remember, even the greatest stories have their unexpected chapters. This is just a plot twist, not the end, wrote one X user. This game was an example that hard work doesn't always pay, sometimes luck matters too. Better luck next time team India, wrote another. On Sunday, Australia won the toss and put India in to bat. The Australian pacers were lethal, bowling India out for just 240 runs. It was the first time in the tournament that the Indian side lost all 10 wickets. India put up a brave fight in their bowling attack, with Mohammed Shami and Jasprit Bumrah getting rid of three of Australia's top batters in the first seven overs. But despite India's best efforts, Australia put up a stubborn batting partnership and managed to defeat India with six wickets to spare."

# print('<영어 키 명사 추출 10개>')
# print(run_keyword_extraction_api(in_string, language='eng-adjective', max_num_keywords=10))
# print()

# print('<영어 키 형용사 추출 10개>')
# print(run_keyword_extraction_api(in_string, language='eng-adjective', max_num_keywords=10))
# print()

in_string = '농촌이 도시에 비해 만족스럽지 못한 것은 한두가지가 아니다. 특히 "아이"를 낳고 키우는 것은 몹시 버겁다. 이는 점차 현실이 되어가고 있는 농촌소멸과 직결되는 문제다. 농촌에서 새로 태어나는 아이들은 거의 없고 고령 어르신들만 있어서다. 저출산 문제는 농촌만이 아닌 국가적인 문제가 된 지 오래다. 하지만 농촌은 더더욱 심각하다. 무엇보다 가임여성이 많지 않지만 아이를 출산하기도 힘들다. 집에서 가까운 곳에 분만이 가능한 산부인과가 없어 다른 지역으로 ‘원정 출산’을 가야만 하는 형편이다. 2022년 11월말 기준 전국 226개 시·군·구 가운데 30%에 달하는 68곳은 ‘분만 산부인과’가 단 한곳도 없다. 쉽게 말해 68개 지방자치단체에는 아이를 낳을 병원이 없다는 얘기다. 이들 대부분은 당연히 군단위 농촌지역이다. 인구가 적으니 의사들이 산부인과 개원을 꺼리는 데다 출생아가 많지 않으니 그나마 있던 병원마저도 문을 닫기 때문이다. 게다가 아이를 낳을 수 있는 공공의료기관도 거의 없다. 도시도 예외는 아니다. 인구가 19만명인 경기 안성시에도 분만할 수 있는 병원이 없다고 하니 농촌은 말해 무엇하겠는가. 2004년 전국 1311곳이던 분만 산부인과는 2014년 850곳, 2018년 713곳, 2022년 11월말 기준 584곳으로 쪼그라들었다. 저출산, 전문인력 부족, 인건비 부담, 높은 근무 강도 탓이라고 한다. 여기에 의료사고 분쟁이 다른 과에 비해 높은 영향도 있다. 이런 이유로 분만 산부인과가 더 줄었으면 줄었지 늘기는 어려운 상황이다. 아이를 낳아도 넘어야 할 산이 많다. 보육시설과 학교가 태부족하기 때문이다. 아이를 맡길 곳이 없어 농사에 전념할 수 없고, 자녀가 성장할수록 교육 걱정에 이농을 고민하게 된다. 사정이 이러니 농촌을 등지는 젊은이들이 증가하고 신생아는 줄어드는 악순환이 반복된다. 정부는 분만 인프라가 더이상 붕괴하지 않도록 서둘러 대책을 마련해야 한다. 최근 산부인과 수가를 추가 지원한다고 밝혔지만 이것만으로는 부족하다. 의료인력 확보와 인건비 재정 지원 등도 적극 검토해야 한다. 아울러 농촌지역 보육과 교육시설 확충도 절실하다. 농촌에서도 자녀를 안심하고 출산하고 제대로 양육할 수 있는 시스템 구축에 힘을 쏟아야 한다. 그래야만 농촌에서 아이 울음소리를 들을 수 있을 것이다. 있습니다 없다면서 안녕 하십니까 있습니다 없다면서 안녕 하십니까 있습니다 없다면서 안녕 하십니까 있습니다 없다면서 안녕 하십니까'
# in_string = '버스정류장은, 올리브영, 올리브, 영, 올, 리, 브, ,가, 자, 가지, 버정과 뻐정 사이에 있어요. 정류장은 저쪽에 있고요. 버스는 지금 오고 있습니다. 버저를 눌러주세요. 버는 여기에 있어요, 고터와 고속터미널은 이쪽에 있습니다. 고속터는 저기에 있고 골터는 여기 있어요.'
# in_string = '올리브 영, 올영, 올립영, 올리브 영 먹는 올리브영은 올리브, 아이, 농촌이 아니다.'
# in_string ="안녕하세요. 형태소 분석기입니다. 이것을 써 보세요. 분석기가 형태소를 분석하고 qns석해 줍니다."


# t1=time.time()

# print('<한국어 키 명사 추출 10개>')
# print(run_keyword_extraction_api(in_string, max_num_keywords=30, language='kor', min_length=5))
# print()

# print('<한국어 키 명사 추출 2개>')
# print(run_keyword_extraction_api(in_string, language='kor', max_num_keywords=2))
# print()

# print('<한국어 키 형용사 추출 10개>')
# print(run_keyword_extraction_api(in_string, language='kor-adjective', max_num_keywords=10))
# print()

print('<한국어 키 명사+형용사 추출 10개>')
print(run_keyword_extraction_api(in_string, language='kor-adjective-and-noun', max_num_keywords=10))
print()

# t2=time.time()
# print(f'(default) num_saved_counts_for_prediction (500) {t2-t1}')

# print('<한국어 키 명사 추출 10개>')
# print(run_keyword_extraction_api(in_string, language='kor', max_num_keywords=10, num_saved_counts_for_prediction=5000))
# print()

# print('<한국어 키 명사 추출 2개>')
# print(run_keyword_extraction_api(in_string, language='kor', max_num_keywords=2, num_saved_counts_for_prediction=5000))
# print()

# print('<한국어 키 형용사 추출 10개>')
# print(run_keyword_extraction_api(in_string, language='kor-adjective', max_num_keywords=10, num_saved_counts_for_prediction=5000))
# print()

# print('<한국어 키 명사+형용사 추출 10개>')
# print(run_keyword_extraction_api(in_string, language='kor-adjective-and-noun', max_num_keywords=10, num_saved_counts_for_prediction=5000))
# print()

# t3=time.time()
# print(f'num_saved_counts_for_prediction (5000) {t3-t2}')