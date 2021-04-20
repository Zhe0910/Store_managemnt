import mysql.connector
from datetime import date
from key import HOSTNAME, USER_NAME, PASSWORD


class Customer:
    def __init__(self, user, password, hostname):
        self.__user = user
        self.__password = password
        self.__hostname = hostname
        self.__database_name = "gamesnoop"
        self.__table_name = "customer"
    
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
    
    def add_customer(self):
        while True:
            try:
                with mysql.connector.connect(host = HOSTNAME, user = USER_NAME, password = PASSWORD) as mysql_connection:
                        with mysql_connection.cursor() as mysql_cursor:
                            mysql_cursor.execute(f"USE {self.database_name}")
                            customer_fname = input("Enter customer's first name: ")
                            customer_lname = input("Enter customer's last name: ")
                            customer_street_num = input("Enter customer's street number: ")
                            customer_street_name = input("Enter customer's street name: ")
                            customer_city = input("Enter customer's city: ")
                            customer_phone = input("Enter customer's phone nmber: ")
                            insert_query = f'insert into customer (customer_fname, customer_lname, customer_street_num,\
                                            customer_street_name, customer_city, customer_phone) values ("{customer_fname}", \
                                            "{customer_lname}", "{customer_street_num}", "{customer_street_name}",\
                                            "{customer_city}", "{customer_phone}");'
                            mysql_cursor.execute(insert_query)
                            mysql_connection.commit()
            except Exception as e:
                print(e)
            else:
                print("The customer has been added")
                print()
                break
    
    def get_one_customer(self, input_customer_id):
        customer = []
        with mysql.connector.connect(host = HOSTNAME, user = USER_NAME, password = PASSWORD) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute(f"SELECT * FROM {self.table_name} WHERE customer_id = '{input_customer_id}'")
                customer_info = mysql_cursor.fetchone()
        return customer_info
    
    def check_customer(self, input_customer_id):
        with mysql.connector.connect(host = HOSTNAME, user = USER_NAME, password = PASSWORD) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute(f"SELECT * FROM {self.table_name} WHERE customer_id = {input_customer_id}")
                result = mysql_cursor.fetchone()
                if result == None:
                    return False
                else:
                    return True
    
        
