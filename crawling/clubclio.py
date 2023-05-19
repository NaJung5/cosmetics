import pprint
import sys

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common import *
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

url = "https://clubclio.co.kr/"
driver = start_crawling()
wait = WebDriverWait(driver, 10)
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

category = []
depth1_elements = soup.select("div.sub_menu__area > ul:nth-child(1) > li > a")
depth2_elements = soup.select("div.maxWidth > div.sub_menu__area > ul[id]")

for depth1 in depth1_elements:
    site_depth1 = depth1.text
    b = depth1['id']
    ch = re.sub("r[0-9]]", "", b)
    for depth2 in depth2_elements:
        c = depth2['id']
        ch2 = c.replace("depth2", "")
        for site in depth2:
            asd = site.find("a")
            if asd != -1:
                site_depth2 = asd.text
                site_link = asd['href']
                if ch == ch2 and site_depth1 != '이너뷰티':
                    category.append({
                        "site_depth1": site_depth1,
                        "site_depth2": site_depth2,
                        "site_link": site_link
                    })
pattern = r'background-image:url\((.*?)\)'

for cate in category:
    url = "https://clubclio.co.kr" + cate['site_link']
    driver.get(url)
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='devTotalProduct']")))
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    count = soup.find("span", id='devTotalProduct').text
    p = 1
    page = 2
    for i in range(int(count)):
        if p > 24:
            try:
                link = driver.find_element(By.LINK_TEXT, str(page))
                link.click()
                # wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='devListContents']/div")))
                time.sleep(3)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                p = 1
                page += 1
            except NoSuchElementException:
                pass
        tag = soup.select_one("#devListContents > div:nth-child({}) > dl".format(p))
        img = tag.select_one("dd.details_thumb > a")['style'] if tag.select_one("dd.details_thumb > a") else None
        info = tag.select_one("dd.details_thumb > a")['href'] if tag.select_one("dd.details_thumb > a") else None
        brand = tag.select_one("div.details_brand_name").text if tag.select_one("div.details_brand_name") else None
        name = tag.select_one("div.details_title").text if tag.select_one("div.details_title") else None
        be_price = tag.select_one("div.details_price > span").text if tag.select_one(
            "div.details_price > span") else None
        price = tag.select_one("div.details_price > strong:nth-child(1)").text if tag.select_one(
            "div.details_price > strong:nth-child(1)") else None
        sale = tag.select_one("div.details_price > strong.percent").text if tag.select_one(
            "div.details_price > strong.percent") else None
        pro_code = tag.select_one("dd.details_thumb")['data-pid'] if tag.select_one("dd.details_thumb") else None

        if img is not None:
            match = re.search(pattern, img)
            img = match.group(1)

        ins = {"img": img, "img2": "", "brand": brand,
               "info": "https://clubclio.co.kr/shop/goodsView/" + pro_code,
               "name": name,
               "sale": sale, "price": price, "site_depth1": cate['site_depth1'],
               "site_depth2": cate['site_depth2'], "site_depth3": "", "brand_type": 'CL',
               "be_price": price, "pro_code": pro_code, "sold_out": "sold_out"}
        pprint.pprint(ins)
        p += 1
end_crawling()
