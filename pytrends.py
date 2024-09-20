{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyNqcejOgMjb1HvohMFdysje",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/EJLE1/2024_OSS_Project/blob/main/pytrends.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#https://github.com/GeneralMills/pytrends?tab=readme-ov-file#related-queries\n",
        "\n",
        "#!pip install pytrends\n",
        "from pytrends.request import TrendReq\n",
        "#pytrends API 초기화\n",
        "pytrends = TrendReq(hl='ko', tz=540)\n",
        "\n",
        "#키워드들을 검색량 기준으로 우선순위를 정하는 함수\n",
        "def get_trends_priority(keywords):\n",
        "  #전체 카테고리에서 오늘기준 24시간 동안 한국지역에서 검색된 검색량 가져오기\n",
        "  pytrends.build_payload(keywords, cat=0, timeframe='now 1-d', geo='KR', gprop='')\n",
        "  trend_data = pytrends.interest_over_time()\n",
        "  #parameter 설명/ .build_payload(키워드 리스트, 카테고리, 검색날짜, 지역, 그룹세분화(이미지,유튜브등))\n",
        "  #카테고리 추가 시 참고/ Economy News: 1164, Economics: 520\n",
        "  #trend_data의 date는 UTC-0 기준(+9시간 시 한국시간)\n",
        "\n",
        "  if trend_data.empty:\n",
        "      return []\n",
        "\n",
        "  #24시간 동안 평균 검색량을 우선순위의 기준\n",
        "  trend_data = trend_data.mean()\n",
        "\n",
        "  # 'isPartial' 컬럼 제거\n",
        "  if 'isPartial' in trend_data:\n",
        "    trend_data = trend_data.drop('isPartial')\n",
        "\n",
        "  # 검색량이 높은 순서대로 정렬\n",
        "  sorted_trends = trend_data.sort_values(ascending=False)\n",
        "\n",
        "  return sorted_trends\n",
        "\n",
        "#입력 키워드 리스트\n",
        "#test\n",
        "input_keywords= [\"금리\",\"sk하이닉스\",\"예금\",\"나스닥\"]\n",
        "#출력 우선순위 리스트\n",
        "output_priority_list = get_trends_priority(input_keywords)\n",
        "\n",
        "#test\n",
        "print(\"키워드 우선순위\\n\",output_priority_list)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "S1SA3xMLhaNi",
        "outputId": "e4b05982-1125-4875-b28b-aa4a0c03c6c9"
      },
      "execution_count": 58,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "키워드 우선순위\n",
            " 금리        34.372222\n",
            "나스닥       19.922222\n",
            "sk하이닉스     6.938889\n",
            "예금         5.850000\n",
            "dtype: float64\n"
          ]
        }
      ]
    }
  ]
}