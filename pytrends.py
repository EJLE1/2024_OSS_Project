#https://github.com/GeneralMills/pytrends?tab=readme-ov-file#related-queries

#!pip install pytrends
from pytrends.request import TrendReq
#pytrends API 초기화
pytrends = TrendReq(hl='ko', tz=540)

#키워드들을 검색량 기준으로 우선순위를 정하는 함수
def get_trends_priority(keywords):
  #전체 카테고리에서 오늘기준 24시간 동안 한국지역에서 검색된 검색량 가져오기
  pytrends.build_payload(keywords, cat=0, timeframe='now 1-d', geo='KR', gprop='')
  trend_data = pytrends.interest_over_time()
  #parameter 설명/ .build_payload(키워드 리스트, 카테고리, 검색날짜, 지역, 그룹세분화(이미지,유튜브등))
  #카테고리 추가 시 참고/ Economy News: 1164, Economics: 520
  #trend_data의 date는 UTC-0 기준(+9시간 시 한국시간)

  if trend_data.empty:
      return []

  #24시간 동안 평균 검색량을 우선순위의 기준
  trend_data = trend_data.mean()    

  # 'isPartial' 컬럼 제거
  if 'isPartial' in trend_data:
    trend_data = trend_data.drop('isPartial')

  # 검색량이 높은 순서대로 정렬
  sorted_trends = trend_data.sort_values(ascending=False)

  return sorted_trends

#입력 키워드 리스트
#test
input_keywords= ["금리","sk하이닉스","예금","나스닥"]
#출력 우선순위 리스트
output_priority_list = get_trends_priority(input_keywords)

#test
print("키워드 우선순위\n",output_priority_list)
