import mysql.connector
from datetime import date
from key import HOSTNAME, USER_NAME, PASSWORD

class Report:
    def __init__(self, user, password, hostname):
        self.__user = user
        self.__password = password
        self.__hostname = hostname
        self.__database_name = "gamesnoop"
        
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
    
    def list_all_products(self):
        with mysql.connector.connect(host = HOSTNAME, user = USER_NAME, password = PASSWORD) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute("SELECT * FROM product")
                print("Product ID".ljust(20) + "Vendor Number".ljust(20) + "Product Name".ljust(20) + "Product Inventory".ljust(20) + "Product Price".ljust(20))
                for product in mysql_cursor:
                    print(f'{str(product[0]).ljust(20)}{str(product[1]).ljust(20)}{product[2].ljust(20)}{str(product[3]).ljust(20)}{str(product[4]).ljust(20)}')
                print()
    
    def list_all_soldout_products(self):
        with mysql.connector.connect(host = HOSTNAME, user = USER_NAME, password = PASSWORD) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute("SELECT * FROM product WHERE product_inventory = 0")
                print("Product ID".ljust(20) + "Vendor Number".ljust(20) + "Product Name".ljust(20) + "Product Inventory".ljust(20) + "Product Price".ljust(20))
                for product in mysql_cursor:
                    print(f'{str(product[0]).ljust(20)}{str(product[1]).ljust(20)}{product[2].ljust(20)}{str(product[3]).ljust(20)}{str(product[4]).ljust(20)}')
                print()
    
    def list_all_customers_in_one_month(self):
        active_list = []
        today = date.today()
        deadline = date(today.year, today.month - 1, today.day)
        with mysql.connector.connect(host = HOSTNAME, user = USER_NAME, password = PASSWORD) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute(f"SELECT customer_id FROM invoice WHERE issue_date >= '{deadline}'")
                customers = mysql_cursor.fetchall()                    
                print("Customer ID".ljust(20) + "First name".ljust(20) + "Last name".ljust(20) + "Phone number".ljust(20))
                for i in customers:
                    if i[0] not in active_list:
                        mysql_cursor.execute(f"SELECT * FROM customer WHERE customer_id = {i[0]}")
                        customer = mysql_cursor.fetchone()
                        print(f'{str(customer[0]).ljust(20)}{str(customer[1]).ljust(20)}{customer[2].ljust(20)}{str(customer[6]).ljust(20)}')
                        active_list.append(i[0])
                print()