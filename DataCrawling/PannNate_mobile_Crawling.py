## 네이트판 모바일버전 특정 게시물 댓글 전부 긁기 by.현빈 ##

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
        url = 'https://m.pann.nate.com/talk/reply/view?pann_id=359474472&currMenu=cranking&stndDt=20210626&vPage=16&gb=d&order=R&rankingType=total&page='

        url_tmp = url + str(i)
        driver.get(url_tmp)
        time.sleep(delay_time)

        html = driver.page_source
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')
        
        if (i > 2) :
            contents = soup.select('dd.userText')
            contents = [content.text.strip() for content in contents]
            List1 = contents[k:]

        else : 
            contents = soup.select('dd.userText')
            contents = [content.text.strip() for content in contents]
            List1 = contents


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
        #if (i == 4 ) :break # 검사용


    #robot = driver.find_element_by_css_selector('a.u_cbox_cleanbot_setbutton is_highlight')
    #robot.click()

    # 기사에서 댓글 더보는 창을 클릭해서 들어가게 만드는 코드...!
    # 핵심은 로딩될 수 있게 딜레이를 사이사이에 잘 주는 것이다..^^

    # time.sleep(delay_time)
    # 다음댓글창 = driver.find_element_by_css_selector('div.paging panel_last a[href]')
    # 다음댓글창.click()
    # time.sleep(delay_time)

    # while True:
    #     try:
    #         더보기 = driver.find_element_by_css_selector('a.u_cbox_btn_more')
    #         더보기.click()
    #         time.sleep(delay_time)
    #     except:
    #         break
        
#    html = driver.page_source
#    print(html)

    # 모듈 참조
#   from bs4 import BeautifulSoup
    # maximum = 0
    # page = 1

#   soup = BeautifulSoup(html, 'lxml')  # 파서 : 누가 분석할 것인지 고르는 것! 이거 속도빠름!

    # while 1:
    #     page_list = soup.findAll("a", {"class": "NP=r:" + str(page)})
    #     if not page_list:
    #         maximum = page - 1
    #         break
    #     page = page + 1
    # print("총 " + str(maximum) + " 개의 페이지가 확인 됬습니다.")

    #다음 댓글목록
    # time.sleep(delay_time)
    # nextcomment = driver.find_element_by_css_selector('div.paginate-reple > a > page-num > 2페이지') 
    # print(nextcomment)
    # nextcomment.click()
    # time.sleep(delay_time)

#모바일 버전
    # 댓글추출
    # contents = soup.select('dd.userText')
    # contents = [content.text for content in contents]

    # # 작성자
    # nicks = soup.select('dl > dt > span') #그런데 클래스이름이 두개라 짝수꺼만 가져와야함..
    # nicks = [nick.text for nick in nicks]

    # #날짜
    # dates = soup.select('dl > dt > em') #얘는 반대로 클래스 이름 두개라 홀수꺼만 가져와야함..
    # dates = [date.text for date in dates]


    # zip함수 및 개체 취합
    replys = List3
    #driver.quit() #전체 창 x누르는 것
    return replys

if __name__ == '__main__':
    from datetime import datetime  # 속도측정
    start = datetime.now()
    url = 'https://m.pann.nate.com/talk/reply/view?pann_id=359474472&currMenu=cranking&stndDt=20210626&vPage=16&gb=d&order=R&rankingType=total&page='

    #게시글 경로 : 20대 이야기 - 톡체널 - 명예의 전당 (2021.06.26~2021.04.24)
    #ETC
    #https://m.pann.nate.com/talk/360041215?currMenu=cranking&order=R&page=9
    #https://m.pann.nate.com/talk/reply/view?pann_id=359935415&currMenu=cranking&stndDt=20210626&vPage=10&gb=d&order=R&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=359698336&currMenu=cranking&stndDt=20210626&vPage=13&gb=d&order=R&rankingType=total&page=
    #https://m.pann.nate.com/talk/reply/view?pann_id=359512345&currMenu=cranking&stndDt=20210626&vPage=15&gb=d&order=R&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=359474472&currMenu=cranking&stndDt=20210626&vPage=16&gb=d&order=R&rankingType=total&page=
    #https://m.pann.nate.com/talk/reply/view?pann_id=359280108&currMenu=cranking&stndDt=20210626&vPage=20&gb=d&order=R&rankingType=total
    
    #현빈 / 개
    #https://m.pann.nate.com/talk/reply/view?pann_id=360691181&currMenu=cranking&stndDt=20210626&vPage=1&gb=d&order=R&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=360659176&currMenu=cranking&stndDt=20210626&vPage=1&gb=d&order=R&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=360499237&currMenu=cranking&stndDt=20210626&vPage=2&gb=d&order=R&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=360453859&currMenu=cranking&stndDt=20210626&vPage=3&gb=d&order=R&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=360433763&currMenu=cranking&stndDt=20210626&vPage=3&gb=d&order=R&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=360289456&currMenu=cranking&stndDt=20210626&vPage=5&gb=d&order=R&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=360201414&currMenu=cranking&stndDt=20210626&vPage=6&gb=d&order=R&rankingType=total
    #


    #게시글 경로  : 톡톡 - 명예의 전당 - 연간 - 2018 - 번 페이지
    #준용 / 4067개
    #https://m.pann.nate.com/talk/reply/view?pann_id=360132535&order=N&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=359198374&order=N&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=359309607&order=N&rankingType=total&
    #https://m.pann.nate.com/talk/reply/view?pann_id=359764232&order=N&rankingType=total 이거 500만 한 것!
    #
    #
    #
    #
    #
    #


    #상민 / 1739개 
    #https://m.pann.nate.com/talk/reply/view?pann_id=344854205&currMenu=ranking&stndDt=2019&vPage=1&gb=y&order=N&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=345921538&currMenu=ranking&stndDt=2019&vPage=3&gb=y&order=N&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=345954624&currMenu=ranking&stndDt=2019&vPage=3&gb=y&order=N&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=347686393&currMenu=ranking&stndDt=2019&vPage=5&gb=y&order=N&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=347070645&currMenu=ranking&stndDt=2019&vPage=9&gb=y&order=N&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=348395720&currMenu=ranking&stndDt=2019&vPage=9&gb=y&order=N&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=344771050&currMenu=ranking&stndDt=2019&vPage=9&gb=y&order=N&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=347584085&currMenu=ranking&stndDt=2019&vPage=10&gb=y&order=N&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=343741598&currMenu=ranking&stndDt=2018&vPage=1&gb=y&order=N&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=341509035&currMenu=ranking&stndDt=2018&vPage=2&gb=y&order=N&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=344027534&currMenu=ranking&stndDt=2018&vPage=3&gb=y&order=N&rankingType=total
    
    #의진 / 1757개
    #https://m.pann.nate.com/talk/reply/view?pann_id=356165309&currMenu=ranking&stndDt=2020&vPage=2&gb=y&order=N&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=352080620&currMenu=ranking&stndDt=2020&vPage=5&gb=y&order=N&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=349912554&currMenu=ranking&stndDt=2020&vPage=5&gb=y&order=N&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=352237941&currMenu=ranking&stndDt=2020&vPage=5&gb=y&order=N&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=349721221&currMenu=ranking&stndDt=2020&vPage=9&gb=y&order=N&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=348337297&currMenu=ranking&stndDt=2019&vPage=5&gb=y&order=N&rankingType=total
    #https://m.pann.nate.com/talk/reply/view?pann_id=352027086&currMenu=ranking&stndDt=2020&vPage=10&gb=y&order=N&rankingType=total

  
    #
    #
    #https://m.pann.nate.com/talk/reply/view?pann_id=360050531&currMenu=today&stndDt=20210528&vPage=1&gb=d&order=N&rankingType=total
    print(get_replys(url),5,0.1)
    reply_data = get_replys(url)

    import pandas as pd
    col =['내용']
    data_frame = pd.DataFrame(reply_data,columns=col)
    data_frame.to_excel('추가_네이트판_실험_개-라벨링x.xlsx',sheet_name='기사제목',startrow=0,header=True)

    end = datetime.now()
    print(end-start)
