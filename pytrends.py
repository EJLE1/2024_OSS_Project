#https://github.com/GeneralMills/pytrends?tab=readme-ov-file#related-queries
import time
import pandas as pd
#!pip install pytrends
from pytrends.request import TrendReq
#pytrends API 초기화
pytrends = TrendReq(hl='ko', tz=540)

#키워드들을 검색량 기준으로 우선순위를 정하는 함수
def get_trends_priority(keywords):
    trend_data_list = []

    for keyword in keywords:
        pytrends.build_payload([keyword], cat=0, timeframe='now 1-d', geo='KR', gprop='')
        time.sleep(1)  # 각 키워드 요청 후 5초 대기
        
        trend_data = pytrends.interest_over_time()

        if not trend_data.empty:
            trend_data_list.append(trend_data.mean())  # 평균값 추가

    if not trend_data_list:
        return []

    # 모든 키워드의 평균 검색량을 데이터프레임으로 변환
    trend_data_combined = pd.concat(trend_data_list, axis=1).mean(axis=1)

    # 'isPartial' 컬럼 제거
    if 'isPartial' in trend_data_combined:
        trend_data_combined = trend_data_combined.drop('isPartial')

    # 검색량이 높은 순서대로 정렬
    sorted_trends = trend_data_combined.sort_values(ascending=False)

    return sorted_trends

#입력 키워드 리스트
input_keywords= keyword_list

#출력 우선순위 리스트
output_priority_list = get_trends_priority(input_keywords)

#키워드만 추출
output_priority_list = output_priority_list.index.tolist()
print("키워드만 추출\n",output_priority_list)
