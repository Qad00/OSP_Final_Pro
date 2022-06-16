#backend
1. elasticsearch.py : elasticsearch db 구현해 놓은 것
  - search_list : 유투브에서 단어를 검색해봤을 때, 나오는 창에 필요한 data들 저장
                : word는 내가 검색한 단어, dict는 긍정 부정 분석이 완료된 데이터(url_result)들을 저장한 것이다
  - url_result : url을 검색했을 때 나오는 창에 필요한 데이터들을 저장, 상세한 것은 코드 안에 주석 참조
               : url : 유투브 링크, title : 유투브 제목, image : 썸네일, hits : 조회수, good : 좋아요, num : 분석 결과 개수, pn : 긍정, 부정 판단, p_percent : 긍정 퍼센트, p_word : 긍정 단어, n_word : 부정 단어, file_path : wordcloud 파일 경로
  - insert 함수 : 데이터를 넣는 함수
  - search 함수 : 해당 index에 있는 모든 data들을 출력하는데 사용, 나중에 조건을 추가하여 데이터 불러올때 참고하면 좋을 듯

2.  emtion_analysis.py
 - text_cleaing : 댓글을 정제해주는 함수
 - comment_analysis : 댓글들을 분석하여 1: 긍정, 0: 중립, -1: 부정으로 나눠주는 함수

3. analysis_sample : emtion_analysis의 sample 코드
 - youtube_title.csv라는 파일을 이용해 감정 분석해보는 샘플 코드
 - neg_pol_word.csv/ pos_pol_word.csv : 긍정, 부정 단어
   출처 :  https://github.com/park1200656/KnuSentiLex

4. vader : vader 방식을 이용해 댓글 문장 전체를 긍정, 부정 판단하는 것
 - detScore : -2에서 2까지(강한 부정에서 강한 긍정으로) 분류
 - vader : vader 방식을 이용해 예측, predict에 -2에서 2까지 표시됨

5. sample_vader : vader의 예시 코드, youtube_title.csv를 이용해 예측해 보았다
