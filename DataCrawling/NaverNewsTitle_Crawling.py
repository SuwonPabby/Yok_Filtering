## 네이버 뉴스 제목 긁는 크롤링 by.현빈 ##

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
# 크롬 드라e이버를 다운받고 크롬 드라이버를 실행하는 것이다.
# 이 드라이버에서 크롬이 열리게 된다.
#from bs4 import BeautifulSoup
#from urllib.request import urlopen
import time

def get_replys(url,inp_time=5,delay_time=0.2):
    #driver = webdriver.Chrome()
    #driver.implicitly_wait(inp_time)
    #driver.get(url)

    ##USB: usb_device_handle_win.cc:1054 Failed 
    #to read descriptor from node connection: 시스템에 부착된 장치가 작동하지 않습니다. (0x1F)
    # 위의 코드에서 이 error를 해결하기 위해 이 코드로 사용하였다.(구글 서칭)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(inp_time)   
    driver.get(url)

    List2 = []
    List3 = []

    i = 1
    while True:
        url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EB%93%B1%EC%8B%A0&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=11&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start='
        url_tmp = url + str(i)
        driver.get(url_tmp)
        time.sleep(delay_time)              

        html = driver.page_source
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')

        time.sleep(delay_time)           
        time.sleep(delay_time)
        time.sleep(delay_time)
        time.sleep(delay_time)

        if (i > 11) :
            contents = soup.select('a.news_tit')
            contents = [content.text.strip() for content in contents]
            List1 = contents

        else : 
            contents = soup.select('a.news_tit')
            contents = [content.text.strip() for content in contents]
            print(contents)
            List1 = contents


        #List2 = List1
        if List2 == List1:
            break
        else:
            if ( i == 51): 
                k = 0
                for j in range(min(len(List2), len(List1))):
                    if List2[j] == List1[j]: k += 1
                    else : 
                        List1 = List1[k:]
                        break
            List2 = List1
            print(List1)
            List3 += List1 

        i += 10
        if (i == 2011 ) :break # 검사용

    # zip함수 및 개체 취합
    replys = List3
    #driver.quit() #전체 창 x누르는 것
    return replys

if __name__ == '__main__':
    from datetime import datetime  # 속도측정
    start = datetime.now()
    url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EB%93%B1%EC%8B%A0&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=11&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=1'

# "등신" 검색 주소
#https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EB%93%B1%EC%8B%A0&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=11&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=1

# "새끼" 검색 주소
#https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EC%83%88%EB%81%BC&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=30&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=1

#"시발점" 검색 주소
#https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EC%8B%9C%EB%B0%9C%EC%A0%90&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=12&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=1

#"개년" 검색 주소 -> 18페이지가 최대
#https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EA%B0%9C%EB%85%84&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=12&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=1

    print(get_replys(url),5,0.1)
    reply_data = get_replys(url)

    import pandas as pd
    col =['내용']
    data_frame = pd.DataFrame(reply_data,columns=col)
    data_frame.to_excel('네이버뉴스제목_등신_0009개-라벨링x.xlsx',sheet_name='기사제목',startrow=0,header=True)

    end = datetime.now()
    print(end-start)
