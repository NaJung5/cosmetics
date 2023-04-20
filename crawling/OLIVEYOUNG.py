import time
import pymysql
import datetime
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# conn = { DB 영역}

#  쿼리

# crawling start

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--disable-gpu')

driver_path = ChromeDriverManager().install()
driver = webdriver.Chrome(executable_path=driver_path, options=options)

url = "https://www.oliveyoung.co.kr/store/main/main.do?oy=0"
driver.get(url)
time.sleep(3)
wait = WebDriverWait(driver, 10)
asd = driver.page_source
so = BeautifulSoup(asd, "html.parser")
# sdu2 = so.select("#gnbAllMenu > ul > li > div > ul > li")
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

for i in range(len(category)):
    Depth1 = driver.find_element(By.CSS_SELECTOR, "#btnGnbOpen")
    Depth1.send_keys(Keys.ENTER)
    time.sleep(1)
    driver.execute_script(category[i]["run"])
    asd = driver.page_source
    so = BeautifulSoup(asd, "html.parser")
    qwe = so.select("#Contents > ul.cate_list_box > li > a")
    for j in range(len(qwe)-1):
        f = 0
        s = 7
        u = 0
        kk = 2
        uu = 0
        qw = 2
        j += 2
        Depth3 = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#Contents > ul.cate_list_box > li:nth-child(" + str(j) + ") > a")))
        Depth3.click()
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        ins = {}
        aa = soup.select_one("#Contents > p > span").text
        for k in range(int(aa)):
            if f == 4:
                s += 1
                u = 0
                f = 0
            if s > 12:
                if kk > 10 and uu == 0:
                    qwer = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                      "#Container > div.pageing > a.next")))
                    qwer.click()
                    time.sleep(3)
                    kk = kk - 8
                    s = 7
                    uu = 1
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                elif kk > 11 and uu == 1:
                    qwer = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                      "#Container > div.pageing > a.next")))
                    qwer.click()
                    kk = kk - 9
                    s = 7
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                else:
                    next_page = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,
                                                        "#Container > div.pageing > a:nth-child(" + str(kk) + ")")))
                    next_page.click()
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    s = 7
                    kk += 1

            tag = soup.select_one("#Contents > ul:nth-child(" + str(s) + ") > li:nth-child(" + str(u + 1) + ")")
            img_src = tag.select_one("div > a > img")['src'] if tag.select_one(" div > a > img") else None
            info = tag.select_one("div > a")['href'] if tag.select_one("div > a") else None
            brand = tag.select_one("div > div > a > span").text if tag.select_one("div > div > a > span") else None
            product = tag.select_one("div > div > a > p").text if tag.select_one("div > div > a > p") else None
            price = tag.select_one("div > p.prd_price > span.tx_org > span").text if tag.select_one(
                "div > p.prd_price > span.tx_org > span") else None
            sale_price = tag.select_one("div > p.prd_price > span.tx_cur > span").text if tag.select_one(
                "div > p.prd_price > span.tx_cur > span") else None
            sale_yn = tag.select_one("div > p.prd_flag > span.icon_flag.sale").text if tag.select_one(
                "div > p.prd_flag > span.icon_flag.sale") else None
            coupon_yn = tag.select_one("div > p.prd_flag > span.icon_flag.gift").text if tag.select_one(
                "div > p.prd_flag > span.icon_flag.gift") else None
            delivery = tag.select_one("div > p.prd_flag > span.icon_flag.delivery").text if tag.select_one(
                "div > p.prd_flag > span.icon_flag.delivery") else None

            ins.update({
                "img_src": img_src,
                "info": info,
                "brand": brand,
                "product": product,
                "price": price,
                "sale_price": sale_price,
                "sale_yn": sale_yn,
                "coupon_yn": coupon_yn,
                "delivery": delivery
            })

            print(f"{k}번째 : {s}  : src : {ins['img_src']}")
            # print(ins)
            # print(i)
            f += 1
            u += 1
