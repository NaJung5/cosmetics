from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from common import *

driver = start_crawling()

url = "https://www.innisfree.com/kr/ko/Main.do"
driver.get(url)

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

cursor.execute(countProduct, 'IN')
check = cursor.fetchone()
if check['count(*)'] == 0:
    insert = 0
else:
    insert = 1

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
        pro_code = tag.select_one("span > a > span.stikerWrap")['data-stikerwrap']
        name = tag.select_one("a > span.name").text if tag.select_one("a > span") else None
        be_price = tag.select_one("a > p > strong.cost").text if tag.select_one("a > p > strong.cost") else None
        price = tag.select_one("a > p > strong.unit").text if tag.select_one("a > p > strong.unit") else None
        sold_out = tag.select_one("a > p > span.soldOut").text if tag.select_one("a > p > span.soldOut") else None
        info = tag.select_one("a")['href'] if tag.select_one("a") else None
        sale = tag.select_one("a > p > span").text if tag.select_one("a > p > span") else None
        if img is not None:
            img = img.split("?")[0]
            img2 = img2.split("?")[0]
        if be_price is not None:
            be_price = re.sub(r"[^0-9]", "", be_price)
        if price is not None:
            price = re.sub(r"[^0-9]", "", price)
        else:
            sale = 0
        ins = ({
            "img": img, "img2": img2, "name": name, "pro_code": pro_code, "be_price": be_price, "price": price,
            "info": "https://www.innisfree.com" + info, "site_depth1": category[i]['depth1'],
            "site_depth2": category[i]['depth2'], "brand_type": 'IN', "sold_out": sold_out,
            "site_depth3": "", "brand": "", "sale": sale
        })

        cursor.execute(findProduct, ins)
        comparison = cursor.fetchone()

        product(ins=ins, comparison=comparison, insert=insert)

        j += 1

end_crawling()
