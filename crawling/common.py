import pymysql

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
    (img, img2, name, pro_seq, be_price, price, sold_out, info, site_depth1, site_depth2, brand_type, reg_date)  
    VALUES 
    (%(img)s, %(img2)s, %(name)s, %(pro_seq)s, %(be_price)s, %(price)s, %(sold_out)s,%(info)s,
     %(site_depth1)s, %(site_depth2)s, %(brand_type)s, SYSDATE())
"""
findProduct = """
    select img, img2, name, pro_seq, be_price, price, sold_out, brand_type 
    from product where pro_seq = %(pro_seq)s
"""
updateProduct = """
    UPDATE product set
    img = %(img)s, img2 = %(img2)s, name = %(name)s, be_price = %(be_price)s, price = %(price)s, mod_date = SYSDATE(),
    sold_out= %(sold_out)s
    where pro_seq = %(pro_seq)s and brand_type = %(brand_type)s  
"""
countProduct = """
    select count(*) from product where brand_type = %s
"""
insertProductHis = """
    insert into product_history
    (before_price, after_price, sold_out, link, name, brand_type, pro_seq, reg_date)
    values 
    (%(before_price)s, %(after_price)s, %(sold_out)s, %(link)s, %(name)s, %(brand_type)s, %(pro_seq)s, SYSDATE())
"""


# ----------------------------------------------------------------------------------------------------------------------

def product(ins, comparison):
    cursor.execute(countProduct, ins)
    check = cursor.fetchone()
    if check['count(*)'] == 0:
        insert = 0
    else:
        insert = 1
    if insert == 0:
        cursor.execute(insertProduct, ins)

    elif comparison is None and insert == 1:
        cursor.execute(insertProduct, ins)
    else:
        del ins['site_depth1']
    del ins['site_depth2']
    del ins['info']
    if comparison != ins:
        his = ({
            'before_price': "", 'after_price': "", 'link': "",
            'brand_type': ins['brand_type'], 'pro_seq': ins['pro_seq'], 'name': "", "sold_out": ""
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
