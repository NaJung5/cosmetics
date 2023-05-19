import pymysql
import datetime
import re

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

#  DB 설정영역 ----------------------------------------------------------------------------------------------------------

db = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user='root',
    password='1234567a',
    db='cosmetics',
    charset='utf8',
    autocommit=True,
    cursorclass=pymysql.cursors.DictCursor
)
cursor = db.cursor()

# ----------------------------------------------------------------------------------------------------------------------

# 쿼리 영역  -------------------------------------------------------------------------------------------------------------

insertProduct = """
    INSERT INTO product 
    (img, img2, name, pro_code, be_price, price, sold_out, info, site_depth1, site_depth2, site_depth3,
     brand_type, reg_date, sale)  
    VALUES 
    (%(img)s, %(img2)s, %(name)s, %(pro_code)s, %(be_price)s, %(price)s, %(sold_out)s,%(info)s,
     %(site_depth1)s, %(site_depth2)s, %(site_depth3)s, %(brand_type)s, SYSDATE(), %(sale)s)
"""
findProduct = """
    select img, img2, name, pro_code, be_price, price, sold_out, brand_type, sale
    from product where pro_code = %(pro_code)s
"""
updateProduct = """
    UPDATE product set
    img = %(img)s, img2 = %(img2)s, name = %(name)s, be_price = %(be_price)s, price = %(price)s, mod_date = SYSDATE(),
    sold_out= %(sold_out)s, sale=%(sale)s
    where pro_code = %(pro_code)s and brand_type = %(brand_type)s  
"""
countProduct = """
    select count(*) from product where brand_type = %s
"""
insertProductHis = """
    insert into product_history
    (before_price, after_price, sold_out, link, name, brand_type, pro_code, reg_date)
    values 
    (%(before_price)s, %(after_price)s, %(sold_out)s, %(link)s, %(name)s, %(brand_type)s, %(pro_code)s, SYSDATE())
"""


# ----------------------------------------------------------------------------------------------------------------------

def product(ins, comparison, insert):
    if insert == 0:
        try:
            cursor.execute(insertProduct, ins)
        except pymysql.err.IntegrityError as e:
            if e.args[0] == 1062:
                pass
    elif comparison is None and insert == 1:
        try:
            cursor.execute(insertProduct, ins)
        except pymysql.err.IntegrityError as e:
            if e.args[0] == 1062:
                pass
    else:
        del ins['site_depth1']
        del ins['site_depth2']
        del ins['site_depth3']
        del ins['info']
        del ins['brand']
        print(comparison != ins)
        print(f"ins : {ins}")
        print(f"comparison: {comparison}")
        if comparison != ins:
            his = ({
                'before_price': "", 'after_price': "", 'link': "",
                'brand_type': ins['brand_type'], 'pro_code': ins['pro_code'], 'name': "", "sold_out": ""
            })
            if comparison['price'] != ins['price']:
                his['before_price'] = comparison['price']
                his['after_price'] = ins['price']
                print("가격변동")
            if ins['name'] != comparison['name']:
                his['name'] = ins['name']
            if ins['img'] != comparison['img']:
                his['img'] = ins['img']
            if ins['img2'] != comparison['img2']:
                his['img2'] = ins['img2']
            if ins['sold_out'] != comparison['sold_out']:
                his['sold_out'] = ins['sold_out']
                print("품절")
            cursor.execute(updateProduct, ins)
            cursor.execute(insertProductHis, his)


def start_crawling():
    now = datetime.datetime.now()
    print(f"시작시간 : {now}")
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver


def end_crawling():
    end = datetime.datetime.now()
    print(f"종료시간 : {end}")
    cursor.close()
    db.close()
    start_crawling().quit()