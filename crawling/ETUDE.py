from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from common import *


driver = start_crawling()
url = "https://www.etude.com/"
driver.get(url)
wait = WebDriverWait(driver, 10)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
cate = soup.select_one("#mega-menu-item-9221 > a")["href"]
driver.get(cate)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
cate = soup.select("#mega-menu-item-8543 > ul > li > a.mega-menu-link")
depth3 = []

cursor.execute(countProduct, 'AB')
check = cursor.fetchone()
if check['count(*)'] == 0:
    insert = 0
else:
    insert = 1

for cates in cate:
    site_depth1 = cates.text
    dp1 = cates['href']
    depth2_elements = soup.select("#mega-menu-item-8543 > ul > li > ul > li > a")
    for cate2s in depth2_elements:
        site_depth2 = cate2s.text
        site_depth2_link = cate2s['href']
        if site_depth2 != '전체' and dp1 in site_depth2_link:
            depth3.append({
                'site_depth1': site_depth1,
                'site_depth2': site_depth2,
                'depth_link': site_depth2_link
            })
for i in range(len(depth3)):
    driver.get(depth3[i]['depth_link'])
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    productCount = soup.select_one("div.woocommerce-result-count > span").text.split("\n")[1].split(" ")[
        1] if soup.select_one("div.woocommerce-result-count > span") else 0
    p = 2
    k = 0
    for j in range(int(productCount)):
        try:
            if k % 12 == 0 and k > 0:
                link = driver.find_element(By.CSS_SELECTOR,
                                           f"div.wd-loop-footer.products-footer > nav > ul > li:nth-child({p}) > a")
                link.click()
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                k = 0
                p += 1

        except NoSuchElementException:
            pass
        tag = soup.select(
            "body > div > div > div > div > div > section > div > div > div > section"
            " > div > div > div > div > div > div > div > div")
        src = tag[k].select_one("div > div.product-element-top.wd-quick-shop > a > img")['src'] if tag[k].select_one(
            "div > div.product-element-top.wd-quick-shop > a > img") else None

        model_src = tag[k].select_one("div > div.product-element-top.wd-quick-shop > div.hover-img > a > img")[
            'src'] if tag[k].select_one(
            "div > div.product-element-top.wd-quick-shop > div.hover-img > a > img") else None
        info = tag[k].select_one("div > div.product-element-top.wd-quick-shop > a")['href'] if tag[k].select_one(
            "div > div.product-element-top.wd-quick-shop > a") else None
        pro_code = tag[k].select_one("div > div.product-element-top.wd-quick-shop > div > div > a")[
            'data-product_id'] if tag[k].select_one(
            "div > div.product-element-top.wd-quick-shop > div > div > a") else None
        products = tag[k].select_one("div > div.product-element-bottom > h3 > a").text if tag[k].select_one(
            "div > div.product-element-bottom > h3 > a") else None
        price = tag[k].select_one("div > div.product-element-bottom > span > span > bdi").text if tag[k].select_one(
            "div > div.product-element-bottom > span > span > bdi") else None
        if price is not None:
            price = re.sub(r"[^0-9]", "", price)
        # 세일 정보 확인 되는 경우 추가
        # if be_price is not None:
        #     be_price = re.sub(r"[^0-9]", "", be_price)
        ins = {
            'img': src, 'info': info, 'img2': model_src, 'name': products, 'be_price': "", 'price': price,
            "pro_code": pro_code,
            "site_depth1": depth3[i]['site_depth1'], "site_depth2": depth3[i]['site_depth2'],
            "site_depth3": "", "sold_out": "",
            "brand_type": 'ET', "brand": "", "sale": ""
        }
        k += 1
        cursor.execute(findProduct, ins)
        comparison = cursor.fetchone()
        product(ins=ins, comparison=comparison, insert=insert)

end_crawling()
# 31527
