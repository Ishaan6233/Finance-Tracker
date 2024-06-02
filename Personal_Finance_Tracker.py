import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

DB_FILE = 'finance_manager.db'

class FinanceManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS income (
                                    id INTEGER PRIMARY KEY,
                                    amount REAL NOT NULL,
                                    category TEXT NOT NULL,
                                    description TEXT,
                                    date TEXT NOT NULL
                                );''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS expense (
                                    id INTEGER PRIMARY KEY,
                                    amount REAL NOT NULL,
                                    category TEXT NOT NULL,
                                    description TEXT,
                                    date TEXT NOT NULL
                                );''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS budget (
                                    id INTEGER PRIMARY KEY,
                                    category TEXT NOT NULL,
                                    amount REAL NOT NULL,
                                    date TEXT NOT NULL
                                );''')

    def add_income(self, amount, category, description):
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with self.conn:
            self.conn.execute("INSERT INTO income (amount, category, description, date) VALUES (?, ?, ?, ?)",
                              (amount, category, description, date))
        print(f"Income of {amount} added in category {category}.")

    def add_expense(self, amount, category, description):
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with self.conn:
            self.conn.execute("INSERT INTO expense (amount, category, description, date) VALUES (?, ?, ?, ?)",
                              (amount, category, description, date))
        print(f"Expense of {amount} added in category {category}.")

    def view_income(self):
        cursor = self.conn.execute("SELECT * FROM income")
        print("Income:")
        for row in cursor:
            print(row)

    def view_expenses(self):
        cursor = self.conn.execute("SELECT * FROM expense")
        print("Expenses:")
        for row in cursor:
            print(row)

    def set_budget(self, category, amount):
        date = datetime.now().strftime('%Y-%m-%d')
        with self.conn:
            self.conn.execute("INSERT INTO budget (category, amount, date) VALUES (?, ?, ?)",
                              (category, amount, date))
        print(f"Budget of {amount} set for category {category}.")

    def view_budget(self):
        cursor = self.conn.execute("SELECT * FROM budget")
        print("Budgets:")
        for row in cursor:
            print(row)

    def generate_report(self):
        cursor = self.conn.execute("SELECT category, SUM(amount) FROM expense GROUP BY category")
        print("Expense Report by Category:")
        for row in cursor:
            print(f"Category: {row[0]}, Total Expense: {row[1]}")

        cursor = self.conn.execute("SELECT category, SUM(amount) FROM income GROUP BY category")
        print("\nIncome Report by Category:")
        for row in cursor:
            print(f"Category: {row[0]}, Total Income: {row[1]}")

    def visualize_data(self):
        categories = []
        amounts = []

        cursor = self.conn.execute("SELECT category, SUM(amount) FROM expense GROUP BY category")
        for row in cursor:
            categories.append(row[0])
            amounts.append(row[1])

        plt.figure(figsize=(10, 5))

        plt.subplot(1, 2, 1)
        plt.bar(categories, amounts)
        plt.xlabel('Categories')
        plt.ylabel('Amount')
        plt.title('Expenses by Category')

        plt.subplot(1, 2, 2)
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title('Expense Distribution')

        plt.tight_layout()
        plt.show()

def main():
    manager = FinanceManager()

    while True:
        print("\nPersonal Finance Management System")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Income")
        print("4. View Expenses")
        print("5. Set Budget")
        print("6. View Budget")
        print("7. Generate Report")
        print("8. Visualize Data")
        print("9. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            description = input("Enter description: ")
            manager.add_income(amount, category, description)
        elif choice == '2':
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            description = input("Enter description: ")
            manager.add_expense(amount, category, description)
        elif choice == '3':
            manager.view_income()
        elif choice == '4':
            manager.view_expenses()
        elif choice == '5':
            category = input("Enter category: ")
            amount = float(input("Enter amount: "))
            manager.set_budget(category, amount)
        elif choice == '6':
            manager.view_budget()
        elif choice == '7':
            manager.generate_report()
        elif choice == '8':
            manager.visualize_data()
        elif choice == '9':
            print("Exiting the Personal Finance Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == '__main__':
    main()
