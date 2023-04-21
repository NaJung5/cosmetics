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

url = "https://www.etude.com/"
driver.get(url)
wait = WebDriverWait(driver, 10)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
cate = soup.select_one("#mega-menu-item-9221 > a")["href"]  # mega-menu-item-9221 > a
driver.get(cate)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
cate_depth2 = soup.select(
    "body > div > div > div > div > div > section > div > div > div > section > div > div > div > div > div > div > "
    "ul > li> ul > li.cat-parent")
# Depth2
# aaqq = []
# for cc in cate_depth2[0:]:
#     a = cc.select_one('a').text
#     c = cc.select_one('a')['href']
#     aaqq.append({
#         'Depth3': a,
#         'run': c
#     })

# Depth3
cate_depth3 = soup.select(
    "body > div > div > div > div > div > section > div > div > div > section > div > div > div > div > div > div > ul > li > ul > li > ul > li")
depth3 = []
aaq = 0

for cate_depth3s in cate_depth3[0:]:
    a = cate_depth3s.select_one('a').text
    c = cate_depth3s.select_one('a')['href']
    if a != '전체':
        depth3.append({
            'depth_name': a,
            'depth_link': c
        })
for i in range(len(depth3)):
    driver.get(depth3[i]['depth_link'])
    time.sleep(3)
    html = driver.page_source
    product = BeautifulSoup(html, "html.parser")
    productCount = product.select_one("div.woocommerce-result-count > span").text.split("\n")[1].split(" ")[1]
    tag = soup.select(
        "body > div > div > div > div > div > section > div > div > div > section > div > div > div > div > div > div > div > div")
    # print(tag)
    for j in tag[0:]:
        src = j.select_one("div > div.product-element-top.wd-quick-shop > a > img")['src']
        model_src = j.select_one("div > div.product-element-top.wd-quick-shop > div.hover-img > a > img")['src']
        info = j.select_one("div > div.product-element-top.wd-quick-shop > a")['href']
        products = j.select_one("div > div.product-element-bottom > h3 > a").text
        price = j.select_one("div > div.product-element-bottom > span > span > bdi").text
        ins = {
            'src': src, 'info': info, 'model_src': model_src, 'product': products, 'price': price
        }
        print(ins)
    break
# print(f"depth3 : {depth3}")

time.sleep(10)
