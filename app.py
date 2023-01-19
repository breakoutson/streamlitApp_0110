import re
from collections import Counter
from konlpy.tag import Okt, Komoran #Kkma
import streamlit as st
import urllib.request as req
import urllib.parse as par

from bs4 import BeautifulSoup

okt = Okt()
kom = Komoran()

st.title('BREAKOUT SON 형태소 분석')


# 블로그 에디터 창에서 안보이지만 따라오는 단어들
remove_list = ['대표사진 삭제', '사진 설명을 입력하세요.', '출처 입력', '사진 삭제','이미지 썸네일 삭제', '동영상 정보 상세 보기','동영상 설명을 입력하세요.']

# 줄바꿈 있는 본문을 한번에 입력하기 위해 pyautogui
# str = pyautogui.prompt()

user_input = st.text_input('본문 또는 URL 입력')


if 'blog.naver.com' in user_input:
    url = user_input

    if not 'm.blog.naver.com' in url:
        url = url.replace('blog.naver.com', 'm.blog.naver.com')

    code = req.urlopen(url)
    soup = BeautifulSoup(code, 'html.parser')

    title = soup.select_one('#SE-b28e8031-860b-4891-9f6b-228ccf1c844f')
    str = soup.select_one('div.se-main-container')
    str = str.text
    st.info(str)
    # str = str.text.replace('\n', '').strip()
else:
    str = user_input

if str != '':

    # 따라온 단어들 삭제
    for i in remove_list:
        str = str.replace(i, '')

    # 공백과 줄바꿈 삭제
    str_re = re.sub('\n| ', '', str)
    str_without_line = str.replace('\n','').strip() #줄바꿈만 정리한 것
    # print (str_re)
    # print ('=======================================')
    # print ('공백제외:', len(str_re), '|', '공백포함:', len(str),'자 입니다')

    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)

    emoji_pattern.sub(r'', str_without_line)

    # 형태소 분석
    import time
    with st.spinner('Wait for it...'):
        time.sleep(3)
    word = okt.morphs(str_without_line) # Komoran 으로 공백있는 본문에서 morphs 추출 (조사)
    # word_re = okt.nouns(str_re) # Okt로 공백없는 본문에서 명사추출 (금칙어 조사시)
    word_okt_space = okt.nouns(str_without_line) # Okt로 공백있는 본문에서 명사추출 (형태소추출)
    # word_kkma_space = kkma.nouns(str_without_line) # KKma로 공백있는 본문에서 명사추출 (형태소추출)
    word_kom_space = okt.nouns(str_without_line) # KKma로 공백있는 본문에서 명사추출 (형태소추출)


    # word_cnt = Counter(word)
    # print (word_cnt)

    # 불용어 찾기
    stop_words = []
    for i in word:
        if len(i) == 1:
            stop_words.append(i)

    # 조사 사용빈도
    print ('================= 조사 사용 빈도 ====================================')
    postpositon = ['은','는','이','가','을','를','것','같','있','겠','수'] # 조사 리스트

    postpositon_list = []
    for i in stop_words:
        if i in postpositon:
            postpositon_list.append(i)
    postpositon_cnt = dict(Counter(postpositon_list).most_common())

    num = 0
    for k, v in postpositon_cnt.items():
        print (k, ':', v, '회', ',' , end=' ')
        num += 1
        if num % 6 == 0:
            print ('')
    print ('\n'*1)


    st.write('### 조사 사용빈도')
    st.write('(Tip.조사를 줄이면 메인키워드 집중도가 올라갑니다)')
    st.info(postpositon_cnt)


    # 형태소 추출
    print ('=================== 형태소 추출 ======================================')

    #키워드 카운트
    ########################################################
    print ('komoran 분석')

    # 불용어 제거
    for i in word_kom_space :
        if len(i) == 1:
            word_kom_space .remove(i)

    word_kom_space_cnt = dict(Counter(word_kom_space).most_common(30))
    # num = 0
    # for k , v in word_kom_space_cnt.items():
    #     print (k, ':', v, end=', ')
    #     num += 1
    #     if num % 8 == 0:
    #         print ('')
    # print ('')
    # print ('형태소분석이 완료되었습니다')

    with st.spinner('Wait for it...'):
        time.sleep(2)
    st.write('### 키워드 사용 빈도')
    st.write('(Tip.메인키워드를 가장 많이 쓰되 과다반복을 줄이세요)')
    st.info(word_kom_space_cnt)
else:
    pass
