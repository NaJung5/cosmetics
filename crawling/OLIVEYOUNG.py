import sys
import time
import pprint

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from common import *

driver = start_crawling()

url = "https://www.oliveyoung.co.kr/store/main/main.do?oy=0"
driver.get(url)
wait = WebDriverWait(driver, 10)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
depth1_elements = soup.select("#gnbAllMenu > ul > li:nth-child(1) > div > p > a")
depth2_elements = soup.select("#gnbAllMenu > ul > li:nth-child(1) > div > ul > li > a")
category = []
cursor.execute(countProduct, 'OL')
check = cursor.fetchone()
if check['count(*)'] == 0:
    insert = 0
else:
    insert = 1
for depth1 in depth1_elements:
    site_depth1 = depth1.text
    check1 = depth1['data-attr']
    for depth2 in depth2_elements:
        site_depth2 = depth2.text
        check2 = depth2['data-attr']
        site_link = depth2['href']
        if check1 in check2:
            category.append({'site_depth1': site_depth1,
                             'site_depth2': site_depth2,
                             'site_link': site_link})

for site_depth in category:
    driver.execute_script(site_depth["site_link"])
    html = driver.page_source
    so = BeautifulSoup(html, "html.parser")
    cate_depth3 = so.select("#Contents > ul.cate_list_box > li > a")
    del cate_depth3[0]
    max_view = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#Contents > div.cate_align_box > div.count_sort.tx_num > ul > li:nth-child(3) > a")))
    max_view.click()
    for site_depth3 in cate_depth3:
        row = 0
        col = 7
        num = 1
        page = 2
        element = driver.find_element(By.XPATH, '//a[@data-attr="{}"]'.format(site_depth3['data-attr']))
        element.click()
        site_depth3 = site_depth3.text
        wait.until(EC.presence_of_element_located((By.XPATH, "//p[@class='cate_info_tx']/span")))
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        product_count = soup.select_one("p.cate_info_tx > span").text
        for k in range(int(product_count)):
            if row == 4:
                col += 1
                num = 1
                row = 0
            if col > 18:
                try:
                    link = driver.find_element(By.LINK_TEXT, str(page))
                    link.click()
                    wait.until(EC.presence_of_element_located((By.XPATH, "//p[@class='cate_info_tx']/span")))
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                except NoSuchElementException:
                    pass
                page += 1
                col = 7
            tag = soup.select_one("#Contents > ul:nth-child({}) > li:nth-child({})".format(col, num))
            img = tag.select_one("div > a > img")['src'] if tag.select_one("div > a > img") else None
            info = tag.select_one("a.prd_thumb")['href'] if tag.select_one("a.prd_thumb") else None
            pro_code = tag.select_one("a.prd_thumb")['data-ref-goodsno'] if tag.select_one("a.prd_thumb") else None
            brand = tag.select_one("span.tx_brand").text if tag.select_one("span.tx_brand") else None
            name = tag.select_one("p.tx_name").text if tag.select_one("p.tx_name") else None
            be_price = tag.select_one("span.tx_org > span").text if tag.select_one("span.tx_org > span") else None
            price = tag.select_one("span.tx_cur > span").text if tag.select_one("span.tx_cur > span") else None
            sold_out = tag.select_one("span.soldout").text if tag.select_one("span.soldout") else None

            if be_price is not None:
                be_price = re.sub(r"[^0-9]", "", be_price)
            if price is not None:
                price = re.sub(r"[^0-9]", "", price)

            ins = ({
                "img": img, "img2": "", "info": info, "brand": brand, "name": name, "be_price": be_price,
                "price": price, "pro_code": pro_code, "site_depth1": site_depth['site_depth1'],
                "site_depth2": site_depth['site_depth2'], "site_depth3": site_depth3, "brand_type": 'OL',
                "sold_out": sold_out, "sale": ""

            })
            cursor.execute(findProduct, ins)
            comparison = cursor.fetchone()

            product(ins=ins, comparison=comparison, insert=insert)
            row += 1
            num += 1

end_crawling()
