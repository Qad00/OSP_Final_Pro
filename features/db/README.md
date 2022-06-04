#backend
1. elasticsearch.py
  -> elasticsearch 구현해 놓은 것
  -> search_list : 유투브에서 단어를 검색해봤을 때, 나오는 창에 필요한 data들 저장, word는 내가 검색한 단어, dict는 긍정 부정 분석이 완료된 데이터(url_result)들을 저장한 것이다
  -> url_result : url을 검색했을 때 나오는 창에 필요한 데이터들을 저장, 상세한 것은 코드 안에 주석 참조
  -> insert 함수 : 데이터를 넣는 함수이다
  -> search 함수 : 해당 index에 있는 모든 data들을 출력하는데 사용, 나중에 조건을 추가하여 데이터 불러올때 참고하면 좋을 듯
2. data_analysis_with_sampledata
 -> csv파일로 데이터 불러와 단어로 나눈 후 평점을 이용해 긍정 부정 예측한 것
 -> 이거랑 카드리딘이 준 링크를 합쳐서 긍정 부정 만들어 볼 예정
3. movie_data
 -> LSTM 모델로 예측한 예제를 따라해본 것
 -> 우리는 안쓸꺼기 때문에 생략해도 될듯
