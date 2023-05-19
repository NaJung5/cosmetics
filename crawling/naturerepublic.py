import pprint
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from common import *

driver = start_crawling()
url = "https://www.naturerepublic.com/goods/goods/list?sctg1="
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
wait = WebDriverWait(driver, 10)
cate = soup.select("body > header > div.gnb > div.center > ul > li.all-category > div.gnb-sub-menu > ul > li")

category = []

cursor.execute(countProduct, 'NA')
check = cursor.fetchone()
if check['count(*)'] == 0:
    insert = 0
else:
    insert = 1

for element in cate:
    site_depth1 = element.select_one("a").text
    depth2_elements = element.select("ul > li > a")
    for depth2_element in depth2_elements:
        site_depth2 = depth2_element.text
        site_link = depth2_element['href']
        if site_depth1 != site_depth2:
            category.append({
                'site_depth1': site_depth1,
                'site_depth2': site_depth2,
                'site_link': site_link
            })

for i in range(len(category)):
    driver.get("https://www.naturerepublic.com/goods/goods/list" + category[i]['site_link'])
    ins = []
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    count = soup.select_one(
        "body > div > section > div > div > div > div > div > div > p > b").text.replace("개", "")
    if int(count) > 20:
        try:
            select_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.drop-down > a")))
            select_list.send_keys(Keys.ENTER)
            select_count = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "ul.sort-menu.select > li > div > ul > li:nth-child(3) > a")))
            select_count.send_keys(Keys.ENTER)
            time.sleep(1)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
        except ElementNotInteractableException:
            pass
    if int(count) > 60:
        page = True
    else:
        page = False
    for j in range(int(count)):
        while page:
            try:
                next_page = driver.find_element(By.CSS_SELECTOR,
                                                "body > div.content-wrap > section:nth-child(2) > div > div > div > "
                                                "div.category-item-wrap > div.item-list-more > a")
                next_page.send_keys(Keys.ENTER)
            except ElementNotInteractableException:
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                page = False
        tag = soup.select_one(f"#goods-list > li:nth-child({j + 1})")
        img = tag.select_one("div.img-slot > img:nth-child(1)")['src'] if tag.select_one(
            "div.img-slot > img:nth-child(1)") else None
        img2 = tag.select_one("div.img-slot > img:nth-child(2)")['src'] if tag.select_one(
            "div.img-slot > img:nth-child(2)") else None
        info = tag.select_one("div.product-info-slot > a")["href"] if tag.select_one(
            "div.product-info-slot > a") is not None else None
        name = tag.select_one("div.product-info-slot > a").text if tag.select_one(
            "div.product-info-slot > a") is not None else None
        pro_code = tag.select_one("div.img-slot > div.quick-btns > ul > li:nth-child(1) > a")[
            'data-no'] if tag.select_one("div.img-slot > div.quick-btns > ul > li:nth-child(1) > a") else None
        price = tag.select_one("div.product-info-slot > div > div > span.price > em").text if tag.select_one(
            "div.product-info-slot > div > div > span.price > em") is not None else None
        price_be = tag.select_one(
            "div.product-info-slot > div > div > span.before-sale").text.replace("원", "") if tag.select_one(
            "div.product-info-slot > div > div > span.before-sale") is not None else None
        sale = tag.select_one("div.tag-wrap > ul > li:nth-child(1) > div").text if tag.select_one(
            "div.tag-wrap > ul > li:nth-child(1) > div") else None
        sale_check = tag.select_one("div.tag-wrap > ul > li:nth-child(1).hidden") if tag.select_one(
            "div.tag-wrap > ul > li:nth-child(1)") else None
        sold_out = tag['class']
        try:
            sold_out[3]
            sold_out = '품절되었습니다.'
        except IndexError:
            sold_out = ''
        if sale_check is not None:
            sale = ''
        if price is not None:
            price = re.sub(r"[^0-9]", "", price)
        if price_be is not None:
            price_be = re.sub(r"[^0-9]", "", price_be)
        ins = ({
            "img": img, "img2": img2, "info": "https://www.naturerepublic.com/" + info, "name": name, "price": price,
            "be_price": price_be, "pro_code": pro_code, "site_depth1": category[i]['site_depth1'],
            "sold_out": sold_out,
            "site_depth2": category[i]['site_depth2'], "site_depth3": "", "brand": "", "sale": sale, "brand_type": "NA"
        })

        cursor.execute(findProduct, ins)
        comparison = cursor.fetchone()

        product(ins=ins, comparison=comparison, insert=insert)

end_crawling()
