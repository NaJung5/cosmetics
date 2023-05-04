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

url = "https://www.ableshop.kr/"
driver.get(url)
time.sleep(3)
try:
    bt = driver.find_element(By.CSS_SELECTOR,
                             "#popupEventBanner > div > div.popup-footer > ul > li:nth-child(1) > button")
    bt.click()
except NoSuchElementException:
    pass
cate_bt = driver.find_element(By.CSS_SELECTOR, "#header > div.header-top > div.header-box > div > a > span")
cate_bt.click()
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
#  depth1 = soup.select("#header-cate > div > ul > li > a > strong")
depth1 = soup.select("#header-cate > div > ul > li > div > ul > li ")
# print(depth1)
print(depth1)
print(f"num : {len(depth1)}")
category = []
for cate in depth1[0:]:
    a = cate.select_one("a").text
    b = cate.select_one("a")['href']
    if "javascript" in b:
        category.append({
            'cate_name': a,
            'cate_link': b
        })
print(category)

for i in range(len(category)):
    driver.execute_script(category[i]['cate_link'])
    #
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.select("#goodsList > li:nth-child(1)")
    for tag in tags:
        img = tag.select_one("div.thum > a")['data-imageurl']
        brn = tag.select_one("div.thum > a")['data-brndnm']
        b_info = tag.select_one("div.thum > a")['data-goodsid']
        info = "https://www.ableshop.kr/product/goods//view-goods?goodsId=" + b_info
        product = tag.select_one("div.thum > a")['data-goodsnm']
        sale = tag.select_one("div.info > a > p > span.discount").text if tag.select_one(
            "div.info > a > p > span.discount") else None
        sale_price = tag.select_one("div.info > a > p > strong").text if tag.select_one(
            "div.info > a > p > strong") else None
        price = tag.select_one("div.info > a > p > span.prime").text if tag.select_one(
            "div.info > a > p > span.prime") else None
        ins = {"img": img, "brn": brn, "info": info, "product": product, "sale": sale, "sale_price": sale_price,
               "price": price}
        print(ins)
