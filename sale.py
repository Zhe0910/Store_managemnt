import mysql.connector
from report import Report
from customer import Customer
from product import Product
from key import HOSTNAME, USER_NAME, PASSWORD
from datetime import date

class Sale:
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

    def create_sale(self):
        while True:
            try:
                customer_id = int(input("Enter customer ID: "))
                employee_id = int(input("Enter employee ID: "))
            except Exception as e:
                print("Invalid input")
                continue
            if Customer(HOSTNAME, USER_NAME, PASSWORD).check_customer(customer_id):
                print("Customer Information:")
                print(Customer(HOSTNAME, USER_NAME, PASSWORD).get_one_customer(customer_id))
                print()
                break
            else:
                print("Customer ID is not in the system")
                
        # insert the invoice info
        with mysql.connector.connect(host = HOSTNAME, user = USER_NAME, password = PASSWORD) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute(f"INSERT INTO invoice (issue_date, customer_id, employee_id) VALUES ('{date.today()}',{customer_id},{employee_id});")
                mysql_connection.commit()
        with mysql.connector.connect(host = HOSTNAME, user = USER_NAME, password = PASSWORD) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute("SELECT MAX(invoice_num) FROM invoice") 
                invoice_num = mysql_cursor.fetchone()[0] # get the invoice's num
        while True:
            Report(HOSTNAME, USER_NAME, PASSWORD).list_all_products()
            try:
                product_id = int(input("Enter product ID: "))
            except Exception as e:
                print("Invalid input")
                continue
            if Product(HOSTNAME, USER_NAME, PASSWORD).check_product_id(product_id) == False:
                print("Product ID is not in the system")
                continue
            product_qty = int(input("Enter quantity: "))
            if Product(HOSTNAME, USER_NAME, PASSWORD).check_product_qty(product_id, product_qty) == False:
                print("Not enough inventory, please try again")
                continue
            price_paid = float(input("Enter the price the customer is paying: "))
            item = (product_id, product_qty, price_paid) # one item
            
            # insert the invoice lines info
            with mysql.connector.connect(host = HOSTNAME, user = USER_NAME, password = PASSWORD) as mysql_connection:
                with mysql_connection.cursor() as mysql_cursor:
                    mysql_cursor.execute(f"USE {self.database_name}")
                    mysql_cursor.execute(f"INSERT INTO invoice_line (invoice_num, product_id, invoice_line_qty, price_paid) VALUES ({invoice_num},{item[0]},{item[1]},{item[2]});")
                    mysql_connection.commit()
            with mysql.connector.connect(host = HOSTNAME, user = USER_NAME, password = PASSWORD) as mysql_connection:
                with mysql_connection.cursor() as mysql_cursor: # update the inventory
                    mysql_cursor.execute(f"USE {self.database_name}")
                    mysql_cursor.execute(f"SELECT product_inventory FROM product WHERE product_id = {item[0]}")
                    product_inventory = mysql_cursor.fetchone()[0]
                    mysql_cursor.execute(f"UPDATE product SET product_inventory = {product_inventory - item[1]} WHERE product_id = {item[0]}")
                    mysql_connection.commit()
           # items.append(item)    a list of products in this sale
            choice = input("Press Y to continue purchasing: ")
            if choice.upper() != "Y":
                 break
                
    def generate_invoice(self):
        with mysql.connector.connect(host = HOSTNAME, user = USER_NAME, password = PASSWORD) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute("SELECT MAX(invoice_num) FROM invoice")                       
                invoice_num = mysql_cursor.fetchone()[0] # the neweset invoice
        with mysql.connector.connect(host = HOSTNAME, user = USER_NAME, password = PASSWORD) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute(f"SELECT * FROM invoice WHERE invoice_num = {invoice_num}")                       
                invoice = mysql_cursor.fetchone() # invoice info                        
        with mysql.connector.connect(host = HOSTNAME, user = USER_NAME, password = PASSWORD) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute(f"SELECT * FROM invoice_line WHERE invoice_num = {invoice_num}")                       
                invoice_lines = mysql_cursor.fetchall() # invoice lines' info
                
        print("-" * 45)
        print("CUSTOMER INVOICE")
        print()
        print(f"Customer ID: {invoice[2]}")
        print(f"Invoice ID: {invoice[0]}")
        print(f"Issue Date: {invoice[1]}")
        print(f"Employee ID: {invoice[3]}")
        print("Product ID         Quantity            Price")
        for i in invoice_lines:
            print(f'{str(i[2]).ljust(20)}{str(i[3]).ljust(20)}{str(i[4]).ljust(20)}')
        print()
        
                
    

    