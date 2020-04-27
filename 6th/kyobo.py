from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import time

# Keys 모듈 추가됨: 검색을 위해 사용

path = os.getcwd() + "/6th/chromedriver.exe"
driver = webdriver.Chrome(path)

try :
    driver.get("http://www.kyobobook.co.kr/index.laf")
    time.sleep(1)

    searchIndex = "파이썬"
    element = driver.find_element_by_class_name("main_input") # 
    element.send_keys(searchIndex) # 괄호 안에는 검색할 검색어 넣음(넣기만 함)
    driver.find_element_by_class_name("btn_search").click()
    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")

    pages = int(bs.find("span", id = "totalpage").text)
    print(pages)
    title = []
    for i in range(3) :
        time.sleep(1)

        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")
        # url을 입력하기는 복잡하니까 다음 버튼 누르는걸로 페이지 이동
        conts = bs.find("div", class_ = "list_search_result").find_all("td", class_ = "detail")

        title.append("page" + str(i + 1)) # 현재 불러온 목록이 몇 페이지인지 title[]의 첫 번째 자리에 넣음

        for c in conts :
            title.append(c.find("div", class_ = "title").find("strong").text)
        driver.find_element_by_xpath('//*[@id="contents_section"]/div[9]/div[1]/a[3]/img').click()
finally :
    for t in title :
        if t.find("page") != -1 : # 리스트 t에서 page라는 값을 찾고, 그것이 존재하면(-1값이 아니면) 실행
            print() # 공백 한 줄 띄우기
            print(t)
        else :
            print(t)
    driver.quit()