import time

from bs4 import BeautifulSoup
# import pymysql
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

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
url = "https://www.naturerepublic.com/goods/goods/list?sctg1="
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
wait = WebDriverWait(driver, 10)
cates = soup.select("#category-menu > ul > li > ul.sub-list > li")
category = []
for cate in cates[0:]:
    a = cate.select_one("a")['href']
    b = cate.select_one("a").text
    if "전체보기" in b:
        continue
    else:
        category.append({
            "link": a,
            "name": b
        })

for i in range(len(category)):
    driver.get("https://www.naturerepublic.com/goods/goods/list" + category[i]['link'])
    ins = []
    for k in range(9999):
        try:
            max_view = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     "body > div.content-wrap > section:nth-child(2) > div > div > div > div.category-item-wrap > div.item-list-more > a")))
            max_view.send_keys(Keys.ENTER)
        except ElementNotInteractableException:
            break
        except TimeoutException:
            break
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    count = soup.select_one(
        "body > div > section > div > div > div > div > div > div > p > b").text.replace("개", "")
    for j in range(int(count)):
        img = soup.select_one("#goods-list > li:nth-child(" + str(j + 1) + ") > div.img-slot > img:nth-child(1)")['src']
        img2 = soup.select_one("#goods-list > li:nth-child(" + str(j + 1) + ") > div.img-slot > img:nth-child(2)")[
            'src']
        info_be = soup.select_one("#goods-list > li:nth-child(" + str(j + 1) + ") > div.product-info-slot > a")["href"]
        name = soup.select_one(
            "#goods-list > li:nth-child(" + str(j + 1) + ") > div.product-info-slot > a").text if soup.select_one(
            "#goods-list > li:nth-child(" + str(j + 1) + ") > div.product-info-slot > a") is not None else None
        price = soup.select_one(
            "#goods-list > li:nth-child(" + str(
                j + 1) + ") > div.product-info-slot > div > div > span.price > em").text if soup.select_one(
            "#goods-list > li:nth-child(" + str(
                j + 1) + ") > div.product-info-slot > div > div > span.price > em") is not None else None
        price_be = soup.select_one(
            "#goods-list > li:nth-child(" + str(
                j + 1) + ") > div.product-info-slot > div > div > span.before-sale").text.replace("원",
                                                                                                  "") if soup.select_one(
            "#goods-list > li:nth-child(" + str(
                j + 1) + ") > div.product-info-slot > div > div > span.before-sale") is not None else None

        ins.append({
            "img": img, "img2": img2, "info_be": info_be, "name": name, "price": price, "price_be": price_be
        })

print(ins)