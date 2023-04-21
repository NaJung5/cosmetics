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
    bt = driver.find_element(By.CSS_SELECTOR, "#popupEventBanner > div > div.popup-footer > ul > li:nth-child(1) > button")
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
time.sleep(10)
