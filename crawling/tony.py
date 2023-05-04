import time

from bs4 import BeautifulSoup
# import pymysql
from selenium import webdriver
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# conn = { DB 영역}

#  쿼리

# crawling start
# now = datetime.datetime.now()
# print(f"시작시간 : {now}")
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
url = "https://www.tonystreet.com/"
driver.get(url)
wait = WebDriverWait(driver, 10)
try:
    popup = driver.find_element(By.CSS_SELECTOR, "#todayClosePop")
    popup.click()
except ElementClickInterceptedException:
    pass
click = wait.until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "body > header > div.nav > div > nav > ul > li.all_menu > a > i")))
click.click()

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

depth1 = soup.find_all("body > header > div > div > section > div > div > div > div > ul > li")
category = []
depth11 = soup.find_all("a", class_='ctgr2_pc')
print(depth11[0])
for i in range(len(depth11)):
    a = depth11[i]['href']
    b = depth11[i].text
    # a = depth11[i]
    category.append({
        'link': a,
        'name': b
    })

print(category)
ins = []
for i in range(len(category)):
    driver.get("https://www.tonystreet.com" + category[i]['link'])
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    depth_count = soup.find_all("a", class_='ctgr_box')
    for j in range(2, len(depth_count)):
        print(f"j: {j}")
        Depth3 = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "#frmCtgr > div > section.product-depth.p_ver > div > div > ul > li:nth-child(" + str(j) + ") > a")))
        # L01M01S01
        Depth3.click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        count = soup.select_one("#ctgrcnt").text
        for k in range(len(count)):
            tag = ()
#productWrapper > ul > li:nth-child(1) > div > a > img:nth-child(1) -> src
#productWrapper > ul > li:nth-child(1) > div > a > img.over -> ['src']
