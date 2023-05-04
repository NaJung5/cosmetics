import time
# import pymysql
import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# conn = { DB 영역}

#  쿼리

# crawling start
# now = datetime.datetime.now()
# print(f"시작시간 : {now}")
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

url = "https://www.innisfree.com/kr/ko/Main.do"
driver.get(url)
wait = WebDriverWait(driver, 10)
time.sleep(3)
category = []
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
depth1 = soup.select("#headerNew > div.category > div > ul.cateList > li > div > ul > li > a")
# cmenu1QW > a:nth-child(2)
# cmenu1QW#smenuQW
# headerNew > div.category > div > ul.cateList
# headerNew > div.category > div > ul.cateList > li:nth-child(6)
# cmenu1UK > a:nth-child(1)
# cmenu1UA > a:nth-child(1)
# smenuUA
# headerNew > div.category > div > ul.cateList > li:nth-child(2)
for cate in depth1[0:]:
    a = cate['href']
    b = cate.text
    if a is not None:
        category.append({
            "link": a,
            "name": b
        })
ins = []
print(category[0]['link'])
for i in range(len(category)):
    driver.get("https://www.innisfree.com" + category[i]['link'])
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    p_count = soup.select_one("#lnbSrchFrm > section > div.contWrap > div.sortCon > p > strong.num").text.replace("개", "")
    for j in range(len(p_count)):
        tag = soup.select_one("#prdList > div.prodList > ul > li:nth-child(" + str(j + 1) + ") ")
        img = tag.select_one("span > a > img:nth-child(3)")['src'] if tag.select_one(
            "span > a > img:nth-child(3)") else None
        img2 = tag.select_one("span > a > img.over")['src'] if tag.select_one("span > a > img.over") else None
        name = soup.select_one(
            "#prdList > div.prodList > ul > li:nth-child(" + str(j + 1) + ") > a > span").text if soup.select_one(
            "#prdList > div.prodList > ul > li:nth-child(" + str(j + 1) + ") > a > span") else None
        price = tag.select_one("a > p > strong.cost").text if tag.select_one("a > p > strong.cost") else None
        be_price = tag.select_one("a > p > strong.unit").text if tag.select_one("a > p > strong.unit") else None
        info = tag.select_one("a").text if tag.select_one("a") else None

        ins.append({
            "img": img, "img2": img2, "name": name, "price": price, "be_price": be_price, "info": info
        })
        print(f"ins: {ins}")
