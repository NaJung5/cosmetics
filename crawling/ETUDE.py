import pymysql
import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from common import cursor, product, findProduct

# crawling start
now = datetime.datetime.now()
print(f"시작시간 : {now}")
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
cate = soup.select_one("#mega-menu-item-9221 > a")["href"]
driver.get(cate)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
cate = soup.select("#mega-menu-item-8543 > ul > li > a.mega-menu-link")
depth3 = []

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
        pro_seq = tag[k].select_one("div > div.product-element-top.wd-quick-shop > div > div > a")[
            'data-product_id'] if tag[k].select_one(
            "div > div.product-element-top.wd-quick-shop > div > div > a") else None
        products = tag[k].select_one("div > div.product-element-bottom > h3 > a").text if tag[k].select_one(
            "div > div.product-element-bottom > h3 > a") else None
        price = tag[k].select_one("div > div.product-element-bottom > span > span > bdi").text if tag[k].select_one(
            "div > div.product-element-bottom > span > span > bdi") else None
        ins = {
            'img': src, 'info': info, 'img2': model_src, 'name': products, 'price': price, "pro_seq": pro_seq,
            "site_depth1": depth3[i]['site_depth1'], "site_depth2": depth3[i]['site_depth2'], "sold_out": "",
            "brand_type": 'ET'
        }
        k += 1
        cursor.execute(findProduct, ins)
        comparison = cursor.fetchone()
        product(ins=ins, comparison=comparison)

end = datetime.datetime.now()
print(f"종료시간 : {end}")
