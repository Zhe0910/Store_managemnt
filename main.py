from key import HOSTNAME, USER_NAME, PASSWORD
from user_interface import UserInterface
from report import Report
from customer import Customer
from product import Product
from sale import Sale

def main():
    print("Welcome to Game Snoop!")
    print()
    while True:
        UserInterface().main_menu()
        choice = input("Enter Choice: ")
        if choice == '1':
            Customer(HOSTNAME, USER_NAME, PASSWORD).add_customer()
        elif choice == '2':
            Sale(HOSTNAME, USER_NAME, PASSWORD).create_sale()
            Sale(HOSTNAME, USER_NAME, PASSWORD).generate_invoice()
        elif choice == '3':
            UserInterface().report_menu()
            report_choice = input("Enter choice: ")
            while True:
                if report_choice == '1':
                    Report(HOSTNAME, USER_NAME, PASSWORD).list_all_products()
                    break
                elif report_choice == '2':
                    Report(HOSTNAME, USER_NAME, PASSWORD).list_all_soldout_products()
                    break
                elif report_choice == '3':
                    Report(HOSTNAME, USER_NAME, PASSWORD).list_all_customers_in_one_month()
                    break
                elif report_choice == '0':
                    break
                else:
                    print("Invalid Entry")
        elif choice == '4':
            Product(HOSTNAME, USER_NAME, PASSWORD).update_product()
        elif choice == '0':
            break
        else:
            print("Invalid command please try again")

if __name__ == '__main__':
    main()
                
        