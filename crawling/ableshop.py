import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from common import *

driver = start_crawling()

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
category = []
cate_count = soup.select("#header-cate > div > ul > li")

cursor.execute(countProduct, 'AB')
check = cursor.fetchone()
if check['count(*)'] == 0:
    insert = 0
else:
    insert = 1

for i in range(2, len(cate_count)):
    site_depth1 = soup.select_one(f"#header-cate > div > ul > li:nth-child({i}) > a > strong").text
    site_depth2_elements = soup.select(f"#header-cate > div > ul > li:nth-child({i}) > div > ul > li > a")
    category.extend([{
        'site_depth1': site_depth1,
        'site_depth2': site_depth2.text,
        'depth_link': site_depth2['href']
    } for site_depth2 in site_depth2_elements])
for i in range(len(category)):
    driver.execute_script(category[i]['depth_link'])
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    product_count = soup.select_one("#goodsTotalCount").text
    k = 0
    p = 2
    for j in range(int(product_count)):
        if k % 20 == 0 and k > 0:
            try:
                link = soup.select_one(f"#pageing > div.list > a:nth-child({p})")['href']
                driver.execute_script(link)
                k = 0
                p += 1
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
            except NoSuchElementException:
                pass
        tag = soup.select("#goodsList > li ")
        img = tag[k].select_one("div.thum > a > img")['src'] if tag[k].select_one("div.thum > a > img") else None
        brn = tag[k].select_one("div.thum > a")['data-brndnm'] if tag[k].select_one("div.thum > a > img") else None
        info = tag[k].select_one("div.thum > a")['data-goodsid'] if tag[k].select_one("div.thum > a > img") else None
        name = tag[k].select_one("div.thum > a")['data-goodsnm'] if tag[k].select_one("div.thum > a > img") else None
        sale = tag[k].select_one("div.info > a > p > span.discount").text if tag[k].select_one(
            "div.info > a > p > span.discount") else None
        sale_price = tag[k].select_one("div.info > a > p > strong").text if tag[k].select_one(
            "div.info > a > p > strong") else None
        price = tag[k].select_one("div.info > a > p > span.prime").text if tag[k].select_one(
            "div.info > a > p > span.prime") else None
        sold_out = tag[k].select_one("div.thum > a > div > span").text if tag[k].select_one(
            "div.thum > a > div > span") else None
        if price is not None:
            price = re.sub(r"[^0-9]", "", price)
        if sale_price is not None:
            sale_price = re.sub(r"[^0-9]", "", sale_price)
        ins = {"img": img, "img2": "", "brand": brn,
               "info": "https://www.ableshop.kr/product/goods/view-goods?goodsId=" + info, "name": name,
               "sale": sale, "price": sale_price, "site_depth1": category[i]['site_depth1'],
               "site_depth2": category[i]['site_depth2'], "site_depth3": "", "brand_type": 'AB', "be_price": price,
               "pro_code": info, "sold_out": sold_out}
        k += 1
        cursor.execute(findProduct, ins)
        comparison = cursor.fetchone()

        product(ins=ins, comparison=comparison, insert=insert)

end_crawling()
driver.quit()
