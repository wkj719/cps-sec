from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import time

path = os.getcwd() + "/6th/chromedriver.exe"
driver = webdriver.Chrome(path)

try :
    driver.get("https://search.naver.com/search.naver?where=news&sm=tab_jum&query=")
    time.sleep(1)

    searchWord = "코로나 바이러스"
    element = driver.find_element_by_class_name("box_window")
    element.send_keys(searchWord)
    driver.find_element_by_class_name("bt_search").click()
    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")

    page = int(input("뉴스를 몇 페이지까지 불러올까요? 네이버 뉴스는 최대 400페이지까지 뉴스를 제공합니다. : "))

    newsTitle = []
    newsPublish = []
    newsTime = []
    pages = len(list(range(page)))
    number = pages*10
    nowpage = []

    for i in range(pages) :
        time.sleep(1)
        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")
        conts = bs.find("ul", class_ = "type01").find_all("dl")
        for c in conts :
            newsTitle.append(c.find("a")["title"])
            nt = c.find("dd", class_ = "txt_inline").text
            newsTime.append(nt.split("  ")[1])
        nowpage.append("page"+str(i+1))
        driver.find_element_by_class_name("next").click()

finally :
    for i in range(number) :
        if (i+1)%10 == 1:
            print(nowpage[i//10])
        print("뉴스 제목: " + str(newsTitle[i]) + "ㅣ올라온 시간: " + str(newsTime[i]))

    driver.quit()