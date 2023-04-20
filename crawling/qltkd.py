# import time
# import pymysql
# import datetime
# import sys
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.select import Select
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.keys import Keys
# from bs4 import BeautifulSoup
#
# # conn = { DB 영역}
#
# #  쿼리
#
# # crawling start
#
# options = webdriver.ChromeOptions()
# # options.add_argument('--headless')
# # options.add_argument('--no-sandbox')
# # options.add_argument('--disable-dev-shm-usage')
# # options.add_argument('--disable-gpu')
#
# driver_path = ChromeDriverManager().install()
# driver = webdriver.Chrome(executable_path=driver_path, options=options)
#
# url = "https://www.oliveyoung.co.kr/store/main/main.do?oy=0"
# driver.get(url)
# time.sleep(3)
# wait = WebDriverWait(driver, 10)
# Depth1 = driver.find_element(By.CSS_SELECTOR, "#btnGnbOpen")
# Depth1.send_keys(Keys.ENTER)
#
# asd = driver.page_source
# so = BeautifulSoup(asd, "html.parser")
# Depth2 = wait.until(
#     EC.presence_of_element_located((By.CSS_SELECTOR,
#                                     "#gnbAllMenu > ul > li:nth-child(1) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(1) > a")))
# Depth2.click()
# Depth3 = wait.until(
#     EC.presence_of_element_located((By.CSS_SELECTOR, "#Contents > ul.cate_list_box > li:nth-child(2) > a")))
# Depth3.click()
#
# #Contents > ul.cate_list_box
# time.sleep(3)
# html = driver.page_source
# soup = BeautifulSoup(html, "html.parser")
# qwe = soup.select("#Contents > ul.cate_list_box > li")
# print(len(qwe))
# ab = []
# for qwes in qwe[1:]:
#     a = qwes.select_one("a")
#     print(a)
#     if a is not None:
#         ab.append({'asdasd': a})
# print(f"avbb : {ab}")
# print(f"avbb : {len(ab)}")
# # aav = driver.find_element(By.CLASS_NAME, ab[2]['class'])
# print(ab[2]['class'])
# ins = {}
# aa = soup.select_one("#Contents > p > span").text
# f = 0
# s = 7
# u = 0
# k = 2
# uu = 0
# # # 1. 스킨케어
# # for i in range(int(aa)):
# #     if f == 4:
# #         s += 1
# #         u = 0
# #         f = 0
# #     if s > 12:
# #         try:
# #             if k > 10 and uu == 0:
# #                 qwer = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
# #                                                                   "#Container > div.pageing > a.next")))
# #                 qwer.click()
# #                 time.sleep(3)
# #                 k = k - 8
# #                 s = 7
# #                 uu = 1
# #                 print(f"초기화된 k : {k}")
# #                 html = driver.page_source
# #                 soup = BeautifulSoup(html, "html.parser")
# #             elif k > 12 and uu == 1:
# #                 qwer = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
# #                                                                   "#Container > div.pageing > a.next")))
# #                 qwer.click()
# #                 time.sleep(3)
# #                 k = k - 8
# #                 s = 7
# #                 html = driver.page_source
# #                 soup = BeautifulSoup(html, "html.parser")
# #             else:
# #                 next_page = wait.until(
# #                     EC.presence_of_element_located((By.CSS_SELECTOR,
# #                                                     "#Container > div.pageing > a:nth-child(" + str(k) + ")")))
# #                 next_page.click()
# #                 time.sleep(3)
# #                 html = driver.page_source
# #                 soup = BeautifulSoup(html, "html.parser")
# #                 s = 7
# #                 k += 1
# #         except TimeoutException:
# #             pass
# #
# #     tag = soup.select_one("#Contents > ul:nth-child(" + str(s) + ") > li:nth-child(" + str(u + 1) + ")")
# #     img_src = tag.select_one("div > a > img")['src'] if tag.select_one(" div > a > img") else None
# #     info = tag.select_one("div > a")['href'] if tag.select_one("div > a") else None
# #     brand = tag.select_one("div > div > a > span").text if tag.select_one("div > div > a > span") else None
# #     product = tag.select_one("div > div > a > p").text if tag.select_one("div > div > a > p") else None
# #     price = tag.select_one("div > p.prd_price > span.tx_org > span").text if tag.select_one(
# #         "div > p.prd_price > span.tx_org > span") else None
# #     sale_price = tag.select_one("div > p.prd_price > span.tx_cur > span").text if tag.select_one(
# #         "div > p.prd_price > span.tx_cur > span") else None
# #     sale_yn = tag.select_one("div > p.prd_flag > span.icon_flag.sale").text if tag.select_one(
# #         "div > p.prd_flag > span.icon_flag.sale") else None
# #     coupon_yn = tag.select_one("div > p.prd_flag > span.icon_flag.gift").text if tag.select_one(
# #         "div > p.prd_flag > span.icon_flag.gift") else None
# #     delivery = tag.select_one("div > p.prd_flag > span.icon_flag.delivery").text if tag.select_one(
# #         "div > p.prd_flag > span.icon_flag.delivery") else None
# #
# #     ins.update({
# #         "img_src": img_src,
# #         "info": info,
# #         "brand": brand,
# #         "product": product,
# #         "price": price,
# #         "sale_price": sale_price,
# #         "sale_yn": sale_yn,
# #         "coupon_yn": coupon_yn,
# #         "delivery": delivery
# #
# #     })
# #     # print(ins)
# #     # print(i)
# #     f += 1
# #     u += 1
# #
# # # 2. 마스크팩
# # # Container > div.pageing > a.next
# # # 3. 클렌징
# #
# # # 4. 선케어
# #
# # # 5. 더모 코스메틱
# #
# # # 6. 메이크업
# #
# # # 7. 네일
# #
# # # 8. 바디케어
# #
# # # 9. 헤어케어
# #
# # # 10. 향수/디퓨저
# #
# # # 11. 미용소품
# #
# # # 12. 남성
