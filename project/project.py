from expenses import Expenses
from expenses import Otheroptions
from manage import summary
import manage
from datetime import datetime
import sys
from tabulate import tabulate
from collections import defaultdict
import csv
import pyfiglet


categories = ['🥕 Groceries','🔧 Utilities','🍕 Food','📶 Subscription','🏠 Rent','🚗 Transport','💰 Miscellaneous ']
def main():
    f = pyfiglet.figlet_format("Welcome", font="slant")
    print(f)
    while True:
        menu_options = [
        ["1.", "💵", "Add new Expense"],
        ["2.", "💻", "View Expenses"],
        ["3.", "📉", "Analyse Expenses"],
        ["4.", "🔧", "Other Options"],
        ["5.", "❌", "Exit"]
        ]
        print("\n" + tabulate(menu_options, tablefmt="rounded_grid"))
        ans = int(input("Enter Choice: "))

        match ans:
            case 1:
                get_expenses()

            case 2:
                show_expenses()

            case 3:
                summary()
                
            case 4:
                manage.otherfunction()
                
            case 5:
                sys.exit("Exiting now...")
            case _:
                print("Enter Valid choice")
       

def check_balance():
    balance = 0.0
    with open("ledger.csv",'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            last_row = row
    balance = float(last_row['balance'])
    return balance


def get_expenses():
    bal = check_balance()
    bal_update = Otheroptions()
    while True:
        try:
            desc = input("Enter description/Name: ").title()
            
            for i,_ in enumerate(categories):
                print(f"{i+1}. {_}")
            idx = int(input("Enter category:"))
            if idx <= len(categories) and idx >= 1:
                catgry = categories[idx-1]
            else:
                sys.exit("Invalid category index entered")
            
            amt = float(input("Enter amount: "))
            if amt > bal:
                print("FAILED: Insufficient Balance")
                break
            else:
                bal = bal-amt
        
            ch = str(input("Input today's date? (y/n): "))
            while True:
                if ch.lower() == 'y':
                    exp = Expenses(category=catgry, desc=desc, amount=amt)
                    bal_update.update_balance(bal)
                    exp.write_to_file()
                    return

                elif ch.lower() == 'n':
                    date = str(input("Enter date in (YYY-MM-DD): "))
                    exp = Expenses(category=catgry, desc=desc, amount=amt, exp_date=date)
                    bal_update.update_balance(bal)
                    exp.write_to_file()
                    return

                else:
                    print("Enter valid date")

        except ValueError:
            print("Invalid input")
            pass
    

def print_by_catgry(des):
    total_amount = 0.0
    total = defaultdict(float)
    with open('expenses.csv', 'r', encoding='utf-8') as read_file:
        reader = csv.DictReader(read_file)
        for row in reader:
            total[row["category"]] += float(row["amount"])
            total_amount += float(row["amount"])
    total = sorted(total.items(),key=lambda x:x[1], reverse=des)

    print("\n--------- Expenses (by Categories) --------")
    table_data = [[category, f"${tt:.2f}"] for category, tt in total]
    print("\n" + tabulate(table_data, headers=["Category", "Total Spent"], tablefmt="grid"))
    print(f"Grand Total Spent = ${total_amount}")


def print_by_date(start,end):
    total_amount = 0.0
    table_data = []
    with open("expenses.csv",'r',encoding='utf-8') as read_date_file:
        reader = csv.DictReader(read_date_file)
        for row in reader:
            row_date = datetime.strptime(row['date'], "%Y-%m-%d")
            if start <= row_date <= end:
                table_data.append([row['date'],row['category'],row['description'],row['amount']])
                total_amount += float(row["amount"])
    if table_data:
        print(f"\n----------Expenses from {start} to {end}----------")
        print("\n" + tabulate(table_data, headers=["Date", "Category","Description","Amount"], tablefmt="grid"))
        print(f"Grand Total Spent = ${total_amount}")
    else:
        print(f"No expenses found between {start} to {end}")

    
def print_by_amount(min_amount):
    total_amount = 0.0
    table_data = []
    print(f"\n----------Expenses above {min_amount}----------")
    with open("expenses.csv",'r', encoding="utf-8") as read_amt_file:
        reader = csv.DictReader(read_amt_file)
        for row in reader:
            if float(row["amount"]) > min_amount:
                table_data.append([row['date'],row['category'],row['description'],row['amount']])
                total_amount += float(row["amount"])
    if table_data:
        print("\n" + tabulate(table_data, headers=["Date", "Category","Description","Amount"], tablefmt="grid"))
        print(f"Grand Total Spent = {total_amount}")
    else:
        print(f"No expenses found above ${min_amount}")


def print_by_name(name):
    table_data = []
    total_amount = 0
    with open("expenses.csv",'r', encoding="utf-8") as read_amt_file:
        reader = csv.DictReader(read_amt_file)
        for row in reader:
            if name in row["description"]:
                table_data.append([row['date'],row['description'],row['amount']])
                total_amount += float(row["amount"])
    if table_data:
        print(f"\n----------Expenses with '{name}'----------")
        print("\n" + tabulate(table_data, headers=["Date","Description","Amount"], tablefmt="grid"))
        print(f"Grand Total Spent = ${total_amount}")
    else:
        print(f"No expenses found with '{name}'")


def show_expenses():
    print("1.🛒 Expenses by category\n2.🗓️ Expenses by date\n3.📊 Expenses by Amount\n4.🍎 Expenses by Name")
    choice = int(input("Enter choice: "))

    match choice:
        case 1:
            option = int(input("1-> Descending 2-> Ascending: "))
            if option == 1:
                descending = True
                print_by_catgry(descending)

            elif option == 2:
                descending = False
                print_by_catgry(descending)

            else:
               raise ValueError("Invalid input")
        
        case 2:
            start = str(input("Enter date (YYY-MM-DD): "))
            end = str(input("Enter date (YYY-MM-DD): "))
            start = datetime.strptime(start, "%Y-%m-%d")
            end = datetime.strptime(end, "%Y-%m-%d")
            print_by_date(start,end)
        
        case 3:
            amt = float(input("Enter amount: "))
            print_by_amount(amt)

        case 4:
            name = str(input("Enter name: ")).title()
            print_by_name(name)
        
        case _:
            sys.exit("Invalid choice")


if __name__ == "__main__":
    main()