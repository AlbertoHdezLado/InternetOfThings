import mysql.connector

iItem = 0
rows = ()

def create_itemlist():
    mydb = mysql.connector.connect(
            host="localhost",
            username="root",
            password="",
    )

    mycursor =  mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS shop")
    
    mycursor.close()
    mydb.close()

    mydb = mysql.connector.connect(
        host="localhost",
        username="root",
        password="",
        database="shop"
    )

    mycursor =  mydb.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS item_list ("
        "id INT(3) UNSIGNED AUTO_INCREMENT PRIMARY KEY,"
        "name VARCHAR(30) NOT NULL,"
        "price FLOAT(6,2) NOT NULL,"
        "amount INT(5) NOT NULL,"
        "image_path VARCHAR(1024) NOT NULL)")
    
    mycursor.close()
    mydb.close()

def search_item_by_id(id):
    mydb = mysql.connector.connect(
        host="localhost",
        username="root",
        password="",
        database="shop"
    )

    mycursor =  mydb.cursor()
    sql = "SELECT * FROM item_list WHERE id=%s"
    mycursor.execute(sql, (id,))

    result=mycursor.fetchall()

    mycursor.close()
    mydb.close()

    return result

def search_item_by_name(name):
    mydb = mysql.connector.connect(
        host="localhost",
        username="root",
        password="",
        database="shop"
    )

    mycursor =  mydb.cursor()
    sql = "SELECT * FROM item_list WHERE name=%s"
    mycursor.execute(sql, (name,))

    result=mycursor.fetchall()

    mycursor.close()
    mydb.close()

    return result

def add_units(id, name, price, amount, image_path):
    result = search_item_by_id(id)
    mydb = mysql.connector.connect(
        host="localhost",
        username="root",
        password="",
        database="shop"
    )

    mycursor =  mydb.cursor()
    if result:
        sql = "UPDATE item_list SET amount=%s WHERE id=%s"
        val = (amount + result[0][3], id)
    else:
        sql = "INSERT INTO item_list (id, name, price, amount, image_path) VALUES (%s, %s, %s, %s, %s)"
        val = (id, name, price, amount, image_path)

    mycursor.execute(sql, val)
    mydb.commit()
    
    mydb.close()

def add_item(name, price, amount, image_path):
    result = search_item_by_name(name)
    mydb = mysql.connector.connect(
        host="localhost",
        username="root",
        password="",
        database="shop"
    )

    mycursor =  mydb.cursor()
    if result:
        sql = "UPDATE item_list SET amount=%s WHERE name=%s"
        val = (amount + result[0][3], name)
    else:
        sql = "INSERT INTO item_list (name, price, amount, image_path) VALUES (%s, %s, %s, %s)"
        val = (name, price, amount, image_path)

    mycursor.execute(sql, val)
    mydb.commit()
    
    mydb.close()

def remove_units(id, amount):
    result = search_item_by_id(id)
    if result:
        mydb = mysql.connector.connect(
            host="localhost",
            username="root",
            password="",
            database="shop"
        )
        mycursor =  mydb.cursor()

        if result[0][3]-amount > 0:
            removed_amount = result[0][3]-amount
            sql = "UPDATE item_list SET amount=%s WHERE id=%s"
            mycursor.execute(sql, (removed_amount,id))
        else:
            removed_amount = result[0][3]
            sql = "DELETE FROM item_list WHERE id=%s"
            mycursor.execute(sql, (id,))

        mydb.commit()

        mycursor.close()
        mydb.close()
        return removed_amount

def get_all_items():
    mydb = mysql.connector.connect(
        host="localhost",
        username="root",
        password="",
        database="shop"
    )

    mycursor =  mydb.cursor()
    sql = "SELECT * FROM item_list"
    mycursor.execute(sql)

    global rows
    rows=mycursor.fetchall()

    mycursor.close()
    mydb.close()

def get_item():
    get_all_items()
    get_item.id = str(rows[iItem][0])
    get_item.name = rows[iItem][1]
    get_item.price = str(rows[iItem][2])
    get_item.amount = str(rows[iItem][3])
    get_item.image_path = rows[iItem][4]

def previous_item():
    global iItem
    if (iItem - 1 >= 0):
        iItem = iItem - 1
    else:
        iItem = len(rows) - 1

def next_item():
    global iItem
    if (iItem + 1 < len(rows)):
        iItem = iItem + 1
    else:
        iItem = 0

#--------------------------------------------------------------

#BASKET
def create_basket():
    mydb = mysql.connector.connect(
        host="localhost",
        username="root",
        password="",
        database="shop"
    )

    mycursor =  mydb.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS basket ("
        "id INT(3) UNSIGNED AUTO_INCREMENT PRIMARY KEY,"
        "name VARCHAR(30) NOT NULL,"
        "price FLOAT(6,2) NOT NULL,"
        "amount INT(5) NOT NULL,"
        "image_path VARCHAR(1024) NOT NULL,"
        "total_price FLOAT(6,2) NOT NULL)")
    
    mycursor.close()
    mydb.close()

def search_in_basket_by_id(id):
    mydb = mysql.connector.connect(
        host="localhost",
        username="root",
        password="",
        database="shop"
    )

    mycursor =  mydb.cursor()
    sql = "SELECT * FROM basket WHERE id=%s"
    mycursor.execute(sql, (id,))

    result=mycursor.fetchall()

    mycursor.close()
    mydb.close()

    return result

def search_in_basket_by_name(name):
    mydb = mysql.connector.connect(
        host="localhost",
        username="root",
        password="",
        database="shop"
    )

    mycursor =  mydb.cursor()
    sql = "SELECT * FROM basket WHERE name=%s"
    mycursor.execute(sql, (name,))

    result=mycursor.fetchall()

    mycursor.close()
    mydb.close()

    return result

def add_to_basket(id, name, price, amount, image_path):
    result = search_in_basket_by_name(id)
    mydb = mysql.connector.connect(
        host="localhost",
        username="root",
        password="",
        database="shop"
    )
    
    removed_amount = remove_units(id, amount)

    mycursor =  mydb.cursor()

    if result:
        sql = "UPDATE basket SET amount=%s, total_price=%s WHERE id=%s"
        val = (removed_amount + result[0][3], price*(removed_amount + result[0][3]), id)
    else:
        sql = "INSERT INTO basket (id, name, price, amount, image_path, total_price) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (id, name, price, removed_amount, image_path, price*removed_amount)

    mycursor.execute(sql, val)
    mydb.commit()
    
    mydb.close()

def remove_from_basket(id, name, price, amount, image_path):
    result = search_in_basket_by_id(id)
    if result:
        add_units(id, name, price, amount, image_path)

        mydb = mysql.connector.connect(
            host="localhost",
            username="root",
            password="",
            database="shop"
        )
        mycursor =  mydb.cursor()
        if result[0][3]-amount > 0:
            sql = "UPDATE basket SET amount=%s WHERE id=%s"
            mycursor.execute(sql, (result[0][3]-amount,id))
        else:
            sql = "DELETE FROM basket WHERE id=%s"
            mycursor.execute(sql, (id,))

        mydb.commit()

        mycursor.close()
        mydb.close()

def get_all_from_basket():
    mydb = mysql.connector.connect(
        host="localhost",
        username="root",
        password="",
        database="shop"
    )

    mycursor =  mydb.cursor()
    sql = "SELECT * FROM basket"
    mycursor.execute(sql)

    global rows
    rows=mycursor.fetchall()

    mycursor.close()
    mydb.close()

def get_from_basket():
    get_all_from_basket()
    get_from_basket.id = str(rows[iItem][0])
    get_from_basket.name = rows[iItem][1]
    get_from_basket.price = str(rows[iItem][2])
    get_from_basket.amount = str(rows[iItem][3])
    get_from_basket.image_path = rows[iItem][4]
    get_from_basket.total_price = str(rows[iItem][5])

def previous_from_basket():
    global iItem
    if (iItem - 1 >= 0):
        iItem = iItem - 1
    else:
        iItem = len(rows) - 1

def next_from_basket():
    global iItem
    if (iItem + 1 < len(rows)):
        iItem = iItem + 1
    else:
        iItem = 0

def get_total_price_basket():
    mydb = mysql.connector.connect(
        host="localhost",
        username="root",
        password="",
        database="shop"
    )
    mycursor =  mydb.cursor()

    sql = "SELECT SUM('total_price') FROM basket"
    mycursor.execute(sql)

    final_price = mycursor.fetchall()

    mycursor.close()
    mydb.close()
    return final_price


#--------------------------------------------------------------

#main
def reset_iterator():
    global iItem
    iItem = 0

create_itemlist()
create_basket()

#add_item("Villa", 13.4, 10, "./Item_images/villa.jpg")
#add_item("Porsche Panamera", 2.1, 50, "./Item_images/panamera.jpg")
#add_item("Private Island", 100.6, 2, "./Item_images/private_island.jpg")
#add_item("Yacht", 10.4, 7, "./Item_images/yacht.jpg")
#add_item("Jet", 15.7, 8, "./Item_images/jet.jpg")
#add_item("Patek Philippe", 1.4, 20, "./Item_images/patek_philippe.jpg")

#add_to_basket("Patek Philippe", 1.4, 5, "./Item_images/patek_philippe.jpg")
#remove_from_basket("Patek Philippe", 1.4, 5, "./Item_images/patek_philippe.jpg")
