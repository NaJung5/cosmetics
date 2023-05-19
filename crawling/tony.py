import pprint
import sys
import time
from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from common import *

url = "https://www.tonystreet.com/"
driver = start_crawling()
driver.get(url)
wait = WebDriverWait(driver, 10)
try:
    popup = driver.find_element(By.CSS_SELECTOR, "#todayClosePop")
    popup.click()
except NoSuchElementException:
    pass

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
cursor.execute(countProduct, 'TO')
check = cursor.fetchone()
if check['count(*)'] == 0:
    insert = 0
else:
    insert = 1
category = []
depth1_element = soup.select("ul.depth-ul > li > a > em")
depth2_element = soup.select("ul.depth-ul > li > a.ctgr2_pc")
for depth1 in depth1_element:
    site_depth1 = depth1.text
    for depth2 in depth2_element:
        site_depth2 = depth2.text
        site_link = depth2['href']
        if site_depth1 in site_link and site_depth2 != site_depth1:
            category.append({
                'site_depth1': site_depth1,
                'site_depth2': site_depth2,
                'site_link': site_link
            })

category = [item for item in category if not (item['site_depth1'] == '메이크업' and item['site_depth2'] == '메이크업소품')]

ins = []
for site_depth in category:
    driver.get("https://www.tonystreet.com" + site_depth['site_link'])
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='ctgr_box']")))

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    depth3 = soup.find_all("a", class_='ctgr_box')
    del depth3[0]
    for site_depth3 in depth3:
        url = "https://www.tonystreet.com" + site_depth3['href']
        driver.get(url)

        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='ctgr_box']")))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        count = soup.select_one("#ctgrcnt").text
        p = 1
        page = 2
        for k in range(int(count)):
            if p > 20:
                try:
                    link = driver.find_element(By.LINK_TEXT, str(page))
                    link.click()
                    p = 1
                    page += 1
                    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='ctgr_box']")))
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                except NoSuchElementException:
                    pass
            tag = soup.select_one("#productWrapper > ul > li:nth-child({})".format(p))
            img = tag.select_one("div > a > img:nth-child(1)")['src'] if tag.select_one(
                "div > a > img:nth-child(1)") else None
            img2 = tag.select_one("div > a > img.over")['src'] if tag.select_one("div > a > img.over") else None
            brand = tag.select_one("span.brand-name").text if tag.select_one("span.brand-name") else None
            pro_code = tag.select_one("div > div > div > input[type=hidden]:nth-child(1)")['value'] if tag.select_one(
                "div > div > div > input[type=hidden]:nth-child(3)") else None
            name = tag.select_one("span.prod-name").text if tag.select_one("span.prod-name") else None
            sale = tag.select_one("em.price-percent").text if tag.select_one("em.price-percent") else None
            be_price = tag.select_one("em.price-before > span").text if tag.select_one(
                "em.price-before > span") else None
            price = tag.select_one("em.price-after > span").text if tag.select_one(
                "em.price-after > span") else None
            sold_out = tag.select_one("div > a > span > span").text if tag.select_one("div > a > span > span") else None
            if be_price is not None:
                be_price = re.sub(r"[^0-9]", "", be_price)
            if price is not None:
                price = re.sub(r"[^0-9]", "", price)

            if sale is not None:
                sale = re.sub(r"[^0-9%]", "", sale)
            ins = {"img": img, "img2": img2, "brand": brand,
                   "info": "https://tonystreet.com/shop/prod/shop_prod_product_view.do?i_sProductcd=" + pro_code,
                   "name": name,
                   "sale": sale, "price": price, "site_depth1": site_depth['site_depth1'],
                   "site_depth2": site_depth['site_depth2'], "site_depth3": site_depth3.text, "brand_type": 'TO',
                   "be_price": price, "pro_code": pro_code, "sold_out": sold_out}
            cursor.execute(findProduct, ins)
            comparison = cursor.fetchone()

            product(ins=ins, comparison=comparison, insert=insert)
            p += 1

end_crawling()
