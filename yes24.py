# CPS Practice(4주차)
# 원하는 순위를 입력하면 해당 순위까지의 베스트셀러 목록을 불러와 순위, 책 명, 가격, 저자 및 출판사 정보를 표 파일로 제공하는 웹 크롤러.

import requests
from bs4 import BeautifulSoup
import csv

rank = int(input("몇 위 까지 보겠습니까?"))
if rank > 10000:
    print("불러올 수 있는 최대는 10000위까지입니다.")

# 입력받은 순위를 계산하여 불러올 페이지 수를 정하는 함수
def pageCnt(rank):
    if rank%40 != 0:
        page = rank//40 + 1
    else:
        page = rank//40
    return page

page = int(pageCnt(rank))

class Scraper():
    def __init__(self):
        self.url = "http://www.yes24.com/24/category/bestseller?CategoryNumber=001&sumgb=06&fetchSize=40&PageNumber="
        self.bookinfo = []

    def getHTML(self, cnt):
        res = requests.get(self.url + str(cnt+1))
        if res.status_code !=200:
            print("Request Error : ", res.status_code)
        html = res.text
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def getInfo(self, rankLimit, soup, cnt):
        books = soup.find_all("td", class_ = "goodsTxtInfo")
        bookRank = []
        bookName = []
        bookPrice = []
        bookWriter = []

        for b in books:
            bookName.append(b.find("a").text)
            bookPrice.append(b.find("span").text)
            bookWriter.append(b.find("div", class_ ="aupu").text)
            bookRank = range(len(bookName))

        self.writeCSV(rankLimit, bookRank, bookName, bookPrice, bookWriter, cnt)
    
    def writeCSV(self, rankLimit, rank, name, price, writer, cnt):
        file = open("yes24.csv", "a", newline = "", encoding = "UTF-8")

        wr = csv.writer(file)
        for i in range(len(name)):
            wr.writerow([rank[i]+1+((cnt)*40), name[i], price[i], writer[i]])
            # 리스트의 순위 값이 입력받은 순위 값과 같아지면 반복을 중단하는 조건문
            if rank[i]+1+((cnt)*40) == rankLimit:
                break

        file.close()

    def scrap(self, rankLimit):        
        file = open("yes24.csv", "w", newline="", encoding = "UTF-8")
        wr = csv.writer(file)
        wr.writerow(["순위", "책 명", "가격", "저자 및 출판사"])
        file.close()

        for i in range(page):
            soupInfo = self.getHTML(i)
            self.getInfo(rankLimit, soupInfo, i)
            print(i+1, "번째 페이지 완료")


if __name__ == "__main__":
    s=Scraper()
    s.scrap(rank)