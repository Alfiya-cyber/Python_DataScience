import csv
import threading
import time

class Customer:
    def __init__(self, customer_id, name, balance, salary, account_type):
        self.customer_id = customer_id
        self.name = name
        self.balance = balance
        self.salary = salary
        self.account_type = account_type
        self.transactions = []
        self.lock = threading.Lock()

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be more than zero")
            return
        with self.lock:
            self.balance += amount
            self.transactions.append({"type": "Deposited", "amount": amount})
        print(amount, "deposited successfully to", self.name + "'s account.")

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be more than zero")
            return
        with self.lock:
            if amount > self.balance:
                print("Balance is not sufficient")
                return
            self.balance -= amount
            self.transactions.append({"type": "Withdrawn", "amount": amount})
        print(amount, "withdrawn successfully from", self.name + "'s account.")

    def show_transactions(self):
        with self.lock:
            return self.transactions

    def apply_interest(self):
        with self.lock:
            if self.account_type == "savings":
                interest = self.balance * 15 
                self.balance += interest
                self.transactions.append({"type": "Interest", "amount": interest})
            print("Interest of", interest, "applied successfully to", self.name + "'s account.")

def read_customers(file_name):
    customers = {}
    with open(file_name, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            customer_id = int(row["CustomerID"])
            name = row["Name"]
            balance = float(row["AccountBalance"])
            salary = float(row["Salary"])
            account_type = row["AccountType"]
            customers[customer_id] = Customer(customer_id, name, balance, salary, account_type)
    return customers

def periodic_interest_application(customers, stop_event):
    while not stop_event.is_set():
        time.sleep(100)  # Apply interest every 10 seconds
        for customer in customers.values():
            customer.apply_interest()

# Read customers from CSV
customers = read_customers("C:/Users/AlfiyaTamboli/Documents/GitHub/Python_DataScience/CASE STUDY/Data.csv")

# Event to stop the periodic interest application thread
stop_event = threading.Event()

# Start a daemon thread to apply interest periodically
interest_thread = threading.Thread(target=periodic_interest_application, args=(customers, stop_event), daemon=True)
interest_thread.start()

def main():
    while True:
        print("\n1. Deposit")
        print("2. Withdraw")
        print("3. Show Transactions")
        print("4. Apply Interest")
        print("5. Exit")

        try:
            choice = int(input("\nEnter your choice: "))
        except ValueError:
            print("Invalid input, please enter a number.")
            continue

        if choice == 1:
            try:
                customer_id = int(input("Enter Customer ID: "))
                amount = float(input("Enter amount to deposit: "))
                customers[customer_id].deposit(amount)
            except ValueError:
                print("Invalid input, please enter valid numbers.")
            except KeyError:
                print("Customer ID not found, please try again.")

        elif choice == 2:
            try:
                customer_id = int(input("Enter Customer ID: "))
                amount = float(input("Enter amount to withdraw: "))
                customers[customer_id].withdraw(amount)
            except ValueError:
                print("Invalid input, please enter valid numbers.")
            except KeyError:
                print("Customer ID not found, please try again.")

        elif choice == 3:
            try:
                customer_id = int(input("Enter Customer ID: "))
                print(customers[customer_id].show_transactions())
            except ValueError:
                print("Invalid input, please enter a valid Customer ID.")
            except KeyError:
                print("Customer ID not found, please try again.")

        elif choice == 4:
            try:
                customer_id = int(input("Enter Customer ID: "))
                customers[customer_id].apply_interest()
            except ValueError:
                print("Invalid input, please enter a valid Customer ID.")
            except KeyError:
                print("Customer ID not found, please try again.")

        elif choice == 5:
            stop_event.set()  # Set the stop event to stop the interest application thread
            interest_thread.join()  # Wait for the interest application thread to finish
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
