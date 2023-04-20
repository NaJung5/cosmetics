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
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

# driver_path = ChromeDriverManager().install()
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

url = "https://www.oliveyoung.co.kr/store/main/main.do?oy=0"
driver.get(url)
time.sleep(3)
wait = WebDriverWait(driver, 10)

asd = driver.page_source
so = BeautifulSoup(asd, "html.parser")
sdu2 = so.select("#gnbAllMenu > ul > li:nth-child(1) > div > ul > li")
category = []
for cate in sdu2[0:]:
    a = cate.select_one('a').text
    b = cate.select_one('a')['data-attr']
    c = cate.select_one('a')['href']
    category.append({
        'Depth2': b,
        'Depth3': a,
        'run': c
    })

Depth1 = driver.find_element(By.CSS_SELECTOR, "#btnGnbOpen")
Depth1.send_keys(Keys.ENTER)
now = datetime.datetime.now()
print(f"시작시간 : {now}")
for i in range(len(category)):
    driver.execute_script(category[i]["run"])
    asd = driver.page_source
    so = BeautifulSoup(asd, "html.parser")
    qwe = so.select("#Contents > ul.cate_list_box > li > a")
    for j in range(2, len(qwe)):
        row = 0
        col = 7
        num = 0
        page = 2
        Depth3 = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#Contents > ul.cate_list_box > li:nth-child(" + str(j) + ") > a")))
        Depth3.click()
        max_view = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#Contents > div.cate_align_box > div.count_sort.tx_num > ul > li:nth-child(3) > a")))
        max_view.click()
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        cate_count = soup.select_one("#Contents > p > span").text
        print(f"count: {cate_count}")
        for k in range(int(cate_count)):
            if row == 4:
                col += 1
                num = 0
                row = 0
            if col > 18:
                try:
                    link = driver.find_element(By.LINK_TEXT, str(page))
                    link.click()
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    page += 1
                    col = 7
                except NoSuchElementException:
                    link = driver.find_element(By.CSS_SELECTOR, "#Container > div.pageing > a.next")
                    link.click()
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    page += 1
                    col = 7
            tag = soup.select_one("#Contents > ul:nth-child(" + str(col) + ") > li:nth-child(" + str(num + 1) + ")")
            ins = {
                "img_src": tag.select_one("div > a > img")['src'] if tag.select_one("div > a > img") else None,
                "info": tag.select_one("div > a")['href'] if tag.select_one("div > a") else None,
                "brand": tag.select_one("div > div > a > span").text if tag.select_one(
                    "div > div > a > span") else None,
                "product": tag.select_one("div > div > a > p").text if tag.select_one("div > div > a > p") else None,
                "price": tag.select_one("div > p.prd_price > span.tx_org > span").text if tag.select_one(
                    "div > p.prd_price > span.tx_org > span") else None,
                "sale_price": tag.select_one("div > p.prd_price > span.tx_cur > span").text if tag.select_one(
                    "div > p.prd_price > span.tx_cur > span") else None,
                "sale_yn": tag.select_one("div > p.prd_flag > span.icon_flag.sale").text if tag.select_one(
                    "div > p.prd_flag > span.icon_flag.sale") else None,
                "coupon_yn": tag.select_one("div > p.prd_flag > span.icon_flag.gift").text if tag.select_one(
                    "div > p.prd_flag > span.icon_flag.gift") else None,
                "delivery": tag.select_one("div > p.prd_flag > span.icon_flag.delivery").text if tag.select_one(
                    "div > p.prd_flag > span.icon_flag.delivery") else None
            }
            row += 1
            num += 1
now2 = datetime.datetime.now()
print(f"종료시간 : {now2}")
driver.quit()
