##  DC인사이드 게시판 특정 단어 연속 크롤링 ##

from selenium import webdriver
import time
#from selenium.webdriver.common.keys import Keys
# 크롬 드라e이버를 다운받고 크롬 드라이버를 실행하는 것이다.
# 이 드라이버에서 크롬이 열리게 된다.
#from bs4 import BeautifulSoup
#from urllib.request import urlopen


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
        url = 'https://search.dcinside.com/post/p/'
        url2 = '/sort/accuracy/q/.EB.93.B1.EC.8B.A0'
        url_tmp = url + str(i) + url2
        driver.get(url_tmp)
        time.sleep(delay_time)

        html = driver.page_source
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')

        time.sleep(delay_time)
        time.sleep(delay_time)
        time.sleep(delay_time)
        time.sleep(delay_time)        
        
        if (i > 2) :
            contents = soup.select('ul.sch_result_list > li > a.tit_txt')
            contents = [content.text.strip() for content in contents]
            List1 = contents[k:]

        else : 
            contents = soup.select('ul.sch_result_list > li > a.tit_txt')
            contents = [content.text.strip() for content in contents]
            List1 = contents
            print(contents)


        #List2 = List1
        if List2 == List1:
            break
        else:
            if ( i == 2): 
                k = 0
                for j in range(min(len(List2), len(List1))):
                    if List2[j] == List1[j]: k += 1
                    else : 
                        List1 = List1[k:]
                        break
            List2 = List1
            print(List1)
            List3 += List1 

        i += 1
        if (i == 81 ) :break # 검사용

    replys = List3
    return replys

if __name__ == '__main__':
    from datetime import datetime  # 속도측정
    start = datetime.now()
    url = 'https://search.dcinside.com/post/p/1/sort/accuracy/q/.EB.93.B1.EC.8B.A0'

 
    print(get_replys(url),5,0.1)
    reply_data = get_replys(url)

    import pandas as pd
    col =['내용']
    data_frame = pd.DataFrame(reply_data,columns=col)
    data_frame.to_excel('디씨_등신_0000개-라벨링x.xlsx',sheet_name='기사제목',startrow=0,header=True)

    end = datetime.now()
    print(end-start)
