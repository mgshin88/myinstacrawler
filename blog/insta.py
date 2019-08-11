# requests test
import time
import datetime
import sys
import os
import re
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,TimeoutException,ElementNotInteractableException,WebDriverException
from bs4 import BeautifulSoup

class Lets_Crawling:
#https://edmundmartin.com/scraping-instagram-with-python/ request 크롤링 예제
#https://pcmc.tistory.com/72?category=809836
#https://m.blog.naver.com/PostView.nhn?blogId=shino1025&logNo=221305380045&proxyReferer=https%3A%2F%2Fwww.google.com%2F
#https://beomi.github.io/2017/09/28/HowToMakeWebCrawler-Headless-Chrome/
#https://wkdtjsgur100.github.io/selenium-change-ip/
#https://nittaku.tistory.com/139
#https://fifthstory.tistory.com/entry/Python%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%9C-%EC%9D%B8%EC%8A%A4%ED%83%80%EA%B7%B8%EB%9E%A8-%ED%83%9C%EA%B7%B8-%ED%81%AC%EB%A1%A4%EB%A7%81
#https://m.blog.naver.com/PostView.nhn?blogId=kiddwannabe&logNo=221185808375&proxyReferer=https%3A%2F%2Fwww.google.com%2F

    def __init__(self,count):
        self.count = int(count)

    def crawler(self):
        url = "https://www.instagram.com/explore/tags/무신사/"
        # 포스트 내 컨텐츠 담을 리스트 선언
        tagList = [] 
        # 페이지 스크롤 변수
        pagedowns = 0
        # dict(hashtag,cnt)
        hashtag = {}
        # 엑셀 저장 데이터
        feedList = []
        # 리턴 데이터
        returnList = {}
        # 크롤링 결과 데이터
        crawlingList = {}
        # 크롬 옵션 설정
        # options = webdriver.ChromeOptions()
        # print(options)
        # #headless 모드 
        # options.add_argument('headless')
        # options.add_argument('window-size=1920x1080')
        # options.add_argument('disable-gpu')
        # #headless 모드 탐지 방지 언어 및 headless로 보이지 않도록 플러그인 수정
        # options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        # options.add_argument("lang=ko_KR") # 한국어!
        # print(options)
        # driver = webdriver.Chrome('chromedriver',chrome_options=options)
        #네비게이터에 올바른 브라우저 환경처럼 보이도록 세팅해준다
        #driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
        #언어
        #driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
        #위에서 차단한 렌더링 가속 가짜로 넣어서 위장
        #driver.execute_script("const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")
        # 브라우저가 실행되며 해당 url로 이동

        # 파이어폭스 옵션 설정
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.socks", "127.0.0.1")
        profile.set_preference("network.proxy.type", 9150)
        profile.set_preference('general.useragent.override', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0')
        profile.update_preferences()

        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")

        try:
            driver = webdriver.Firefox(executable_path='/crawler/repo/blog/geckodriver.exe',firefox_profile=profile,firefox_options=options)
        except WebDriverException:
            webdriver.close()

        #코드 시작시간
        start = datetime.datetime.now().strftime("%Y_%m_%d %H:%M:%S")
        print(start)

        driver.get(url)
        # 웹자원 대기
        driver.implicitly_wait(1) 
        # 총 게시물 수 태그 클래스이름으로 찾기
        ttlFeed = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,"g47SY"))) 
        print("총 게시물:", ttlFeed.text)
        # body 태그를 태그 이름으로 찾기
        time.sleep(1)
        # 페이지 내 첫번째 게시물 클릭
        driver.find_elements_by_class_name("eLAPa")[0].click()
        # failCnt
        failCnt = 0
        count = self.count
        # 데이터 스크래핑 시작
        while pagedowns < count:
                # 페이지 호출 후 대기
                #driver.implicitly_wait(5) 

            #게시물 본문
            try:
                post = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"C4VMK")))

                try:
                    driver.find_element_by_class_name('XQXOT').send_keys(Keys.HOME)     
                    driver.find_element_by_class_name('XQXOT').find_element_by_xpath("//ul/li/div/button").click()
                    driver.find_element_by_class_name('XQXOT').send_keys(Keys.HOME)  

                except (NoSuchElementException,ElementNotInteractableException):
                    pass
                
                # 게시물 글자수 160자
                # 댓글포함 최대 30개
                # 하나의 해시트그 내 글자수 100자

                #id = driver.execute_script("document.body.getElementsByClassName('C4VMK')[0].getElementsByTagName('a')[0].innerText")
                
                #content = driver.execute_script("document.body.getElementsByClassName('C4VMK')[0].getElementsByTagName('span')[0].innerText")
                
                req = driver.page_source
                soup = BeautifulSoup(req,'html.parser')
                replyCount = soup.find_all("div",class_="C4VMK")
                tagCount = replyCount[0].select('span>a')
                id = replyCount[0].find_all(class_="_6lAjh")[0].select("a")[0].text
                content = replyCount[0].select('span')[0].text
                like = '0'
                tags=[]  
                feedRow = {}        

                try:
                    #like = driver.find_element_by_class_name("Nm9Fw").find_element_by_tag_name("span").text
                    like = soup.find_all("div",class_="Nm9Fw")[0].select("span")[0].text

                except (NoSuchElementException,IndexError):
                    try:
                        like = soup.find_all("span",class_="vcOH2")[0].select("span")[0].text
                    except IndexError:
                        pass
            
                #데이터 가공
                emoji_pattern = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)

                content = emoji_pattern.sub('',content)
                #태그 로직 끝난 후에 긍정,부정 체크 메서드 만들것        
                
                #본문의 해시태그
                if len(tagCount) > 0:

                    for i in range(0,len(tagCount)):
                        tag = tagCount[i].text

                        if "#" in tag:
                            tag = tag.replace("#","").replace(" ","")
                            tags.append(tag)

                #댓글의 해시태그
                if len(replyCount) > 0:

                    for i in range(1,len(replyCount)):
                        #replyid = "document.body.getElementsByClassName('C4VMK')["+i+"].getElementsByTagName('a')[0].innerText"
                        replyid = replyCount[i].find_all("a")[0].text

                        if id == replyid:
                            #replyTagCount = driver.execute_script("document.body.getElementsByClassName('C4VMK')["+i+"].getElementsByTagName('span')[0].getElementsByTagName('a').length")
                            replyTagCount = replyCount[i].find_all("a")

                            if len(replyCount) > 1:

                                for j in range(0,len(replyTagCount)):
                                    #reply =  driver.execute_script("document.body.getElementsByClassName('C4VMK')["+i+"].getElementsByTagName('span')[0].getElementsByTagName('a')["+j+"].innerText")
                                    reply = replyTagCount[j].text

                                    if "#" in reply:
                                        reply = reply.replace("#","").replace(" ","")
                                        tags.append(reply)
                
                #중복제거
                tags = list(set(tags))
                tagList.append(tags)
                print("=======================================================================================")
                print("====================================pagedowns : ",pagedowns,"====================================")
                print("=======================================================================================")
                print("id===============================",id)
                print("content==========================",content)
                print("like=============================",like)
                print("finaltag=========================",tags)
                feedRow["id"] = id
                feedRow["content"] = content
                feedRow["tag"] = tags
                feedRow["like"] = like
                feedList.append(feedRow)

                time.sleep(1)           
                
                #다음 게시물 클릭
                try:
                    driver.find_element_by_class_name("HBoOv").click()

                except NoSuchElementException:
                    # 웹자원 대기
                    driver.get(url)
                    driver.implicitly_wait(1) 

                    for i in range(0,pagedowns):
                        driver.find_elements_by_class_name("eLAPa")[0].click()
                        #html = driver.find_element_by_tag_name("html")
                        #html.send_keys(Keys.DOWN)
                
                pagedowns += 1
                print("=======================================================================================")
                print("=======================================================================================")
            except (NoSuchElementException,StaleElementReferenceException,TimeoutException):
                failCnt += 1
                print("=======================================================================================")
                print("====================================failcount : ",failCnt,"=====================================")
                print("=======================================================================================")
                if failCnt > 3:
                    driver.find_element_by_class_name("HBoOv").click()
                    
                time.sleep(120)
                pass
                
        print("끝!!")
                
        # 해시태그 중복 검사 후 리스트로 재할당
        tagList = list([tuple(set(tag)) for tag in tagList])

        # 해시태그 갯수 구하기
        for htags in tagList:
            for htag in htags:
                # 해시태그 카운트 업
                if not (htag in hashtag):
                    hashtag[htag] = 1
                else:
                    hashtag[htag] += 1

        # 정렬
        keys = sorted(hashtag.items(), key = lambda x:x[1], reverse = True)

        # n순위 까지 출력
        for k, v in keys[:15]:
            print("{}({})".format(k, v))

        end = datetime.datetime.now().strftime("%Y_%m_%d %H:%M:%S")

        print("start======",start)
        print("end======",end)

        print("enddivision=========",datetime.datetime.strptime(end,"%Y_%m_%d %H:%M:%S")-datetime.datetime.strptime(start,"%Y_%m_%d %H:%M:%S"))
        # result = pd.DataFrame(feedList)
        # result.columns = ['id','content','tag','like']
        # result.head()

        #웹자원 종료
        driver.close
        
        crawlingList["ttlfeed"] = ttlFeed.text
        crawlingList["crwfeed"] = len(tagList)
        crawlingList["succnt"] = pagedowns
        crawlingList["failcnt"] = failCnt
        crawlingList["created_at"] = start
        crawlingList["updated_at"] = end
        crawlingList["working_while"] = str(datetime.datetime.strptime(end,"%Y_%m_%d %H:%M:%S")-datetime.datetime.strptime(start,"%Y_%m_%d %H:%M:%S"))

        returnList["crawlingList"] = crawlingList
        returnList["tagList"] = keys
        returnList["excelList"] = feedList

        return returnList 

class Lets_Save:
    def __init__(self,excelList):
        self.excelList = excelList

    def saveCSV(self):
        excelList = self.excelList
        if len(excelList) > 0:
            today = datetime.datetime.now().strftime("%Y_%m_%d")
            filepath = "/Crawler/"+today
            filename = today + "__0"
            if os.path.isdir(filepath):
                while os.path.exists(filepath+"/"+filename):
                    filename = filename[:len(filename)-1] + str(int(filename[len(filename-1)])+ 1)
            else:
                os.makedirs(filepath)
                

            result = pd.DataFrame(excelList)
            result.columns = ['id','content','tag','like']
            print(result.head())
            
            
            result.to_csv(filepath+"/"+filename+".csv", encoding="utf-8") 
            returnMap = {}
            
            returnMap["filename"] = filename
            returnMap["path"] = filepath
            return returnMap

class Lets_Work:
    def __init__(self,tagList,tagFilter):
        self.tagList = tagList
        self.tagFilter = tagFilter

    def ratio_Calculator(self):
        tagList = self.tagList
        tagFilter = self.tagFilter
        ntagCnt = 0
        ptagCnt = 0
        ttlCnt = 0
        ratioMap = {}
        
        if len(tagList) > 0:
            for k,v in tagList:

                if k in tagFilter["ntag"]:
                    ntagCnt += v
                elif k in tagFilter["ptag"]:
                    ptagCnt += v
                ttlCnt += v
        ratioMap["ptagCnt"] = ptagCnt
        ratioMap["ntagCnt"] = ntagCnt
        return ratioMap