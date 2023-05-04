import time
# import pymysql
import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# conn = { DB 영역}

#  쿼리

# crawling start
now = datetime.datetime.now()
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

# driver_path = ChromeDriverManager().install()
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

url = "https://www.oliveyoung.co.kr/store/main/main.do?oy=0"
driver.get(url)
time.sleep(1)
wait = WebDriverWait(driver, 10)

asd = driver.page_source
so = BeautifulSoup(asd, "html.parser")
sdu2 = so.select("#gnbAllMenu > ul > li:nth-child(1) > div > ul > li")
category = []
for cate in sdu2[0:]:
    a = cate.select_one('a').text
    b = cate.select_one('a')['data-attr']
    c = cate.select_one('a')['href']
    if '더모' not in b:
        category.append({
            'Depth2': b,
            'Depth3': a,
            'run': c
        })
Depth1 = driver.find_element(By.CSS_SELECTOR, "#btnGnbOpen")
Depth1.send_keys(Keys.ENTER)

for i in range(len(category)):
    driver.execute_script(category[i]["run"])
    html = driver.page_source
    so = BeautifulSoup(html, "html.parser")
    cate_depth3 = so.select("#Contents > ul.cate_list_box > li > a")
    #  48개씩 보기 클릭
    max_view = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#Contents > div.cate_align_box > div.count_sort.tx_num > ul > li:nth-child(3) > a")))
    max_view.click()
    for j in range(2, len(cate_depth3)):
        product_type = None
        row = 0
        col = 7
        num = 1
        page = 2
        # depth3 이동
        depth3 = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#Contents > ul.cate_list_box > li:nth-child(" + str(j) + ") > a")))
        depth3.click()
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        product_count = soup.select_one("#Contents > p > span").text
        if '스킨케어' in category[i]['Depth2']:
            if '토너/로션/올인원' in category[i]['Depth3']:
                if '스킨/토너' in cate_depth3[j-1].text:
                    product_type = 'A1'
                elif '스킨케어세트' in cate_depth3[j-1].text:
                    product_type = 'A4'
                else:
                    product_type = 'A2'

            if '에센스/크림' in category[i]['Depth2']:
                if '크림' in cate_depth3[j-1].text:
                    product_type = 'A2'
                else:
                    product_type = 'A3'

            if '미스트/오일' in category[i]['Depth3']:
                product_type = 'A1'

        elif '마스크팩' in category[i]['Depth2']:
            if '시트팩' in cate_depth3[j-1].text:
                product_type = 'H1'

            if '패드' in cate_depth3[j-1].text:
                product_type = 'H2'

            if '페이셜팩' in cate_depth3[j-1].text:
                product_type = 'H1'

            if '코팩/패치' in cate_depth3[j-1].text:
                product_type = 'H1'

        elif '클렌징' in category[i]['Depth2']:
            if '클렌징폼/젤' in cate_depth3[j-1].text:
                product_type = 'B1'

            if '오일/워터/리무버' in cate_depth3[j-1].text:
                product_type = 'B1'

            if '필링/패드' in category[i]['Depth3']:
                if '필링/스크럽' in cate_depth3[j-1].text:
                    product_type = 'B2'
                else:
                    product_type = 'B1'

        elif '선케어' in category[i]['Depth2']:
            if '선블록' in cate_depth3[j-1].text:
                product_type = 'I1'

            if '태닝/애프터선' in cate_depth3[j-1].text:
                product_type = 'I2'

        elif '메이크업' in category[i]['Depth2']:
            if '립메이크업' in category[i]['Depth3']:
                if '립스틱' in cate_depth3[j-1].text:
                    product_type = 'D1'
                else:
                    product_type = 'D2'

            if '베이스메이크업' in category[i]['Depth3']:
                if '블리셔/치크' or '쉐이딩/컨투어링' or '하이라이터' or '픽서' in cate_depth3[j-1].text:
                    product_type = 'E2'
                else:
                    product_type = 'E1'

            if '아이메이크업' in category[i]['Depth3']:
                if '아이라이너' in cate_depth3[j-1].text:
                    product_type = 'C1'
                elif '아이브로우' in cate_depth3[j-1].text:
                    product_type = 'C2'
                elif '마스카라' in cate_depth3[j-1].text:
                    product_type = 'C3'
                else:
                    product_type = 'C4'

        elif '네일' in category[i]['Depth2']:
            if '폴리쉬' in category[i]['Depth3']:
                product_type = 'F1'

            if '팁/스티커' in category[i]['Depth3']:
                product_type = 'F4'

            if '반경화' in category[i]['Depth3']:
                product_type = 'F4'

            if '케어' in category[i]['Depth3']:
                product_type = 'F2'

        elif '바디케어' in category[i]['Depth2']:
            if '샤워/입욕' in category[i]['Depth3']:
                if '입욕제' in cate_depth3[j-1].text:
                    product_type = 'J4'
                elif '바디스크럽' in cate_depth3[j-1].text:
                    product_type = 'J2'
                else:
                    product_type = 'J1'

            if '로션/오일' in category[i]['Depth3']:
                product_type = 'J2'

            if '제모/왁싱' in category[i]['Depth3']:
                product_type = 'J5'

            if '핸드케어' in category[i]['Depth3']:
                product_type = 'J3'

            if '립케어' in category[i]['Depth3']:
                product_type = 'D2'

            if '바디미스트' in category[i]['Depth3']:
                product_type = 'J2'

            if '데오드란트' in category[i]['Depth3']:
                product_type = 'J5'

            if '맘&베이비' in category[i]['Depth3']:
                product_type = 'J6'

            if '선물세트' in category[i]['Depth3']:
                product_type = 'J7'

            if '풋케어' in category[i]['Depth3']:
                product_type = 'J3'

        elif '헤어케어' in category[i]['Depth2']:
            if '샴푸.린스':
                product_type = 'K1'

            if '트리트먼트/팩':
                if '헤어트리트먼트' in cate_depth3[j-1].text:
                    product_type = 'K1'
                else:
                    product_type = 'K2'

            if '헤어에센스' in category[i]['Depth3']:
                product_type = 'K2'

            if '염색약/펌' in category[i]['Depth3']:
                product_type = 'K2'

            if '헤어기기' in category[i]['Depth3']:
                product_type = 'M4'

            if '스타일링' in category[i]['Depth3']:
                product_type = 'K2'

            if '헤어브러쉬' in category[i]['Depth3']:
                product_type = 'K3'

        elif '향수/디퓨저' in category[i]['Depth2']:
            if '여성향수' in category[i]['Depth3']:
                product_type = 'G1'
            if '남성향수' in category[i]['Depth3']:
                product_type = 'G1'
            if '홈프래그런스' in category[i]['Depth3']:
                product_type = 'G2'

            if '선물세트' in category[i]['Depth3']:
                if '향수선물세트' in cate_depth3[j-1].text:
                    product_type = 'G1'
                else:
                    product_type = 'G2'

        elif '미용소품' in category[i]['Depth2']:
            if '메이크업소품' in category[i]['Depth3']:
                if '기타' in cate_depth3[j-1].text:
                    product_type = 'M4'
                else:
                    product_type = 'M1'

            if '스킨케어소품' in category[i]['Depth3']:
                if '기타' in cate_depth3[j-1].text:
                    product_type = 'M4'
                else:
                    product_type = 'M2'

            if '아이소품' in category[i]['Depth3']:
                product_type = 'M1'

            if '헤어/바디소품' in category[i]['Depth3']:
                product_type = 'M5'

            if '미용관리' in category[i]['Depth3']:
                product_type = 'M6'

            if '미용가전' in category[i]['Depth3']:
                product_type = 'M7'

            if '미용잡화' in category[i]['Depth3']:
                product_type = 'M8'

        elif '남성' in category[i]['Depth2']:
            if '스킨케어' in category[i]['Depth3']:
                if '기타' in cate_depth3[j-1].text:
                    product_type = 'L4'
                else:
                    product_type = 'L1'

            if '헤어케어' in category[i]['Depth3']:
                if '샴푸' in cate_depth3[j-1].text:
                    product_type = 'L5'
                else:
                    product_type = 'L7'

            if '쉐이빙' in category[i]['Depth3']:
                product_type = 'L7'

            if '향수/매너용품' in category[i]['Depth3']:
                if '매너용품' in cate_depth3[j-1].text:
                    product_type = 'L4'
                else:
                    product_type = 'L7'

            if '메이크업' in category[i]['Depth3']:
                product_type = 'L8'

            if '바디케어' in category[i]['Depth3']:
                product_type = 'L6'

        for k in range(int(product_count)):
            if row == 4:
                col += 1
                num = 1
                row = 0
            if col > 18:
                if page % 10 == 1:
                    # link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, str(page))))
                    # link.click()
                    link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#Container > div.pageing > a.next")))
                    link.click()
                else:
                    link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, str(page))))
                    link.click()
                    # link = driver.find_element(By.CSS_SELECTOR, "#Container > div.pageing > a.next")
                    # link.click()
                    # link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#Container > div.pageing > a.next")))
                    # link.click()
                page += 1
                col = 7
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
            tag = soup.select("#Contents > ul:nth-child({}) > li:nth-child({})".format(col, num))
            tag = tag[0] if tag else None
            ins = {
                "img_src": tag.select_one("div > a > img")['src'] if tag.select_one("div > a > img") else None,
                "info": tag.select_one("div > a")['href'] if tag.select_one("div > a") else None,
                "brand": tag.select_one("div > div > a > span").text if tag.select_one(
                    "div > div > a > span") else None,
                "product": tag.select_one("div > div > a > p").text if tag.select_one(
                    "div > div > a > p") else None,
                "price": tag.select_one("div > p.prd_price > span.tx_org > span").text if tag.select_one(
                    "div > p.prd_price > span.tx_org > span") else None,
                "sale_price": tag.select_one("div > p.prd_price > span.tx_cur > span").text if tag.select_one(
                    "div > p.prd_price > span.tx_cur > span") else None,
                "sale_yn": tag.select_one("div > p.prd_flag > span.icon_flag.sale").text if tag.select_one(
                    "div > p.prd_flag > span.icon_flag.sale") else None,
                "coupon_yn": tag.select_one("div > p.prd_flag > span.icon_flag.gift").text if tag.select_one(
                    "div > p.prd_flag > span.icon_flag.gift") else None,
                "delivery": tag.select_one("div > p.prd_flag > span.icon_flag.delivery").text if tag.select_one(
                    "div > p.prd_flag > span.icon_flag.delivery") else None
            }
            print(f"ins:{ins}")
            row += 1
            num += 1

now2 = datetime.datetime.now()
print(f"시작시간:{now}")
print(f"종료시간 : {now2}")
driver.quit()
