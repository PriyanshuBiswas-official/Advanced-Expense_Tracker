from expenses import Analyse
from expenses import Otheroptions
import csv
from tabulate import tabulate
from collections import defaultdict


def get_stock():
    symbol = input("Symbol: ").upper().strip()
    nshares = float(input("No. of shares: "))
    return symbol,nshares


def show_portfolio():
    portfolio_totals = {}
    table_data = []
    total = 0.0
    with open("stocks.csv", 'r', newline='',encoding="utf-8") as stockfile:
        reader = csv.DictReader(stockfile)
        for row in reader:
            symbol = row["name"]
            share = float(row['nshares'])
            price = float(row['lastprice'])

            investment = share*price
            total += investment
            portfolio_totals[symbol] = portfolio_totals.get(symbol, 0) + investment

            table_data = [[symbol, f"${total:,.2f}"] for symbol, total in portfolio_totals.items()]

    # Print as a nice table
    print("\n--- Portfolio Summary ---")
    print(tabulate(table_data, headers=["Ticker", "Total Invested"], tablefmt="heavy_grid"))
    # print(f"Total invested = {total}")
    return total


def calculate_income_assets():
    balance = 0.0
    savings = 0.0
    assets = 0.0
    with open('ledger.csv','r') as savings_file:
        last_row = None
        reader = csv.DictReader(savings_file)
        for row in reader:
            last_row = row

    if last_row is None:
        raise ValueError("Ledger is empty or contains no data rows.")

    else:
        balance = last_row['balance']
        savings = last_row['savings']
        assets = last_row['other_assets']
        return balance,savings,assets


def top5_expenses():
    total_amount = 0.0
    total = defaultdict(float)
    with open('expenses.csv', 'r', encoding='utf-8') as read_file:
        reader = csv.DictReader(read_file)
        for row in reader:
            total[row["category"]] += float(row["amount"])
            total_amount += float(row["amount"])
    total = sorted(total.items(),key=lambda x:x[1], reverse=True)

    top5 = total[:5]

    print("\n------ Top 5 Categories -----")
    table_data = [[category, f"${tt:.2f}"] for category, tt in top5]
    print("\n" + tabulate(table_data, headers=["Category", "Total Spent"], tablefmt="heavy_grid"))
    print(f"Total = {total_amount}")


def summary():
    bal,sav,ast = calculate_income_assets()
    top5_expenses()
    invest = show_portfolio()
    table_data = [["Balance",bal],["Savings",sav],["Other Assets",ast],["Total Invested",invest]]
    print(tabulate(table_data,headers=["Financial Snapshot","Total"],tablefmt="heavy_grid"))
    while True:
        choice = str(input("Enter q to quit to main menu: "))
        if choice.lower() == 'q':
            return
        else:
            print("Invalid input")


def otherfunction():
    update = Otheroptions()
    while True:
        menu_options = [
        ["1.", "💵", "Update Balance"],
        ["2.", "💻", "Update Savings"],
        ["3.", "💰", "Update Assets"],
        ["4.", "📈", "Add stock to portfolio"],
        ["5.", "📉", "Remove stock from portfolio"],
        ["6.", "❌", "Exit to main menu"]
    ]
        print("\n" + tabulate(menu_options, tablefmt="rounded_grid"))
        ch = int(input("Enter your choice:"))
        match ch:
            case 1:
                bal = float(input("Enter new Balance: "))
                update.update_balance(bal)

            case 2:
                sav = float(input("Enter new Savings: "))
                update.update_savings(sav)

            case 3:
                ast = float(input("Enter Value of new Assets: "))
                update.update_assets(ast)

            case 4:
                stock = Analyse()
                symbol,n = get_stock()
                stock.writestock(name=symbol,nshares=n)

            case 5:
                stock = Analyse()
                symbol,n = get_stock()
                stock.removestock(name=symbol,nshares_to_remove=n)

            case 6:
                print("Exiting to main menu...")
                return

            case _:
                print("Invalid choice entered")


if __name__ == "__main__":
    summary()
