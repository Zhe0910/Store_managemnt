import mysql.connector
from report import Report 
from key import HOSTNAME, USER_NAME, PASSWORD

class Product:
    def __init__(self, user, password, hostname):
        self.__user_name = user
        self.__password = password
        self.__hostname = hostname
        self.__database_name = 'gamesnoop'
        self.__table_name = 'product'
    
    @property
    def user(self):
        return self.__user
    @property
    def password(self):
        return self.__password
    @property
    def hostname(self):
        return self.__hostname
    @property
    def database_name(self):
        return self.__database_name
    @property
    def table_name(self):
        return self.__table_name
    
    def update_product(self):
        while True:
            Report(HOSTNAME, USER_NAME, PASSWORD).list_all_products()
            product_id = int(input("Which product would you want to update?(Enter ID): "))
            with mysql.connector.connect(host = HOSTNAME, user = USER_NAME, password = PASSWORD) as mysql_connection:
                with mysql_connection.cursor() as mysql_cursor:
                    mysql_cursor.execute(f"USE {self.database_name}")
                    mysql_cursor.execute(f"SELECT product_inventory FROM {self.table_name} where product_id = '{product_id}'")
                    product_inventory = mysql_cursor.fetchone()[0]
            print(f"Currently {product_inventory} items are in stock")
            try:
                update_inventory = int(input("How many you want to add?(Enter int) "))
            except Exception as e:
                print("Invalid input please try again")
            with mysql.connector.connect(host = HOSTNAME, user = USER_NAME, password = PASSWORD) as mysql_connection:
                with mysql_connection.cursor() as mysql_cursor:
                    mysql_cursor.execute(f"USE {self.database_name}")
                    mysql_cursor.execute(f"UPDATE product SET product_inventory = {update_inventory + product_inventory} WHERE product_id = {product_id}")
                    mysql_connection.commit()
            print(f"Inventory has been updated, {update_inventory + product_inventory} available")
            choice = input("Do you want to continue?(Y)")
            if choice.upper() == "Y":
                continue
            else:
                print()
                break
            
    def check_product_id(self, input_product_id):
        with mysql.connector.connect(host = HOSTNAME, user = USER_NAME, password = PASSWORD) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute(f"SELECT * FROM {self.table_name} WHERE product_id = {input_product_id}")
                result = mysql_cursor.fetchone()
                if result == None:
                    return False
                else:
                    return True
    
    def check_product_qty(self, input_product_id, input_product_qty):
        with mysql.connector.connect(host = HOSTNAME, user = USER_NAME, password = PASSWORD) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute(f"SELECT * FROM {self.table_name} WHERE product_id = '{input_product_id}'")
                product_qty = mysql_cursor.fetchone()[3]
                if input_product_qty > product_qty:
                    return False
                else:
                    return True
                
        
                
    
    
    