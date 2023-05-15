import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
from common import cursor, product, findProduct

# crawling start
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

url = "https://www.innisfree.com/kr/ko/Main.do"
driver.get(url)

start = datetime.datetime.now()
print(f"시작시간: {start}")

category = []

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
# categpry 추출
li_selector = "#headerNew > div.category > div > ul.cateList > li"
depth_selector = "div > ul > li > a"
elements = soup.select(li_selector)

for element in elements:
    depth1 = element.select_one("a").text
    depth2_elements = element.select(depth_selector)
    for depth2_element in depth2_elements:
        depth2 = depth2_element.text
        link = depth2_element["href"]
        if depth2 != depth1:
            category.append({
                "depth1": depth1,
                "depth2": depth2,
                "link": link
            })
ins = []
for i in range(len(category)):
    driver.get("https://www.innisfree.com" + category[i]['link'])
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    p_count = soup.select_one("#lnbSrchFrm > section > div.contWrap > div.sortCon > p > strong.num").text.replace("개",
                                                                                                                  "")
    j = 1
    page = 2
    for k in range(int(p_count)):
        if (j - 1) % 20 == 0 and j - 1 > 0:
            try:
                link = driver.find_element(By.CSS_SELECTOR,
                                           "#prdList > div.paging > span:nth-child(" + str(page) + ") > a")
                link.click()
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                page += 1
                j = 1
            except NoSuchElementException:
                pass
        tag = soup.select_one(f"#prdList > div.prodList > ul > li:nth-child({j})")
        img = tag.select_one("span > a > img:nth-child(3)")['src'] if tag.select_one(
            "span > a > img:nth-child(3)") else None
        img2 = tag.select_one("span > a > img.over")['src'] if tag.select_one("span > a > img.over") else None
        pro_seq = tag.select_one("span > a > span.stikerWrap")['data-stikerwrap']
        name = tag.select_one("a > span.name").text if tag.select_one("a > span") else None
        be_price = tag.select_one("a > p > strong.cost").text if tag.select_one("a > p > strong.cost") else None
        price = tag.select_one("a > p > strong.unit").text if tag.select_one("a > p > strong.unit") else None
        sold_out = tag.select_one("a > p > span.soldOut").text if tag.select_one("a > p > span.soldOut") else None
        info = tag.select_one("a")['href'] if tag.select_one("a") else None
        if img is not None:
            img = img.split("?")[0]
            img2 = img2.split("?")[0]
        if price is not None:
            price = re.sub(r"[^0-9,]", "", price)

        ins = ({
            "img": img, "img2": img2, "name": name, "pro_seq": int(pro_seq), "be_price": be_price, "price": price,
            "info": "https://www.innisfree.com" + info, "site_depth1": category[i]['depth1'],
            "site_depth2": category[i]['depth2'], "brand_type": 'IN', "sold_out": sold_out
        })

        cursor.execute(findProduct, ins)
        comparison = cursor.fetchone()

        product(ins=ins, comparison=comparison)

        j += 1

driver.quit()
cursor.close()
end = datetime.datetime.now()
print(f"종료시간: {end}")
