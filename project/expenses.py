from datetime import date
import os
import csv


class Expenses:
    def __init__(self, desc, category, amount, exp_date=date.today()):
        self.date = exp_date
        self.desc = desc
        self.category = category
        self.amount = amount


    def write_to_file(self):
        fieldnames = ["date", "category", "description", "amount"]
        # filepath = os.path.abspath('expenses.csv')
        # print(f"Writing to: {filepath}")
        with open('expenses.csv', 'a', newline='', encoding='utf-8') as write_file:
            writer = csv.DictWriter(write_file,fieldnames=fieldnames)
            new_row = {
                "date":self.date,
                "category":self.category,
                "description":self.desc,
                "amount":self.amount
            }
            writer.writerow(new_row)
            write_file.flush()
        print(f"date={self.date}, category={self.category}, desc={self.desc}, amount={self.amount}")
        print("Expense Added Successfully")


class Analyse:
    def __init__(self,st_date = date.today()):
        self.date = st_date

        
    def writestock(self,name,nshares):
        fieldnames = ["date", "name", "nshares", "lastprice"]
        lastprice = float(input("Price: "))
        with open("stocks.csv", 'a', newline='',encoding="utf-8") as stockfile:
            writer = csv.DictWriter(stockfile,fieldnames=fieldnames)
            new_stocks = {
                "date":self.date,
                "name":name,
                "nshares":nshares,
                "lastprice":lastprice
            }
            writer.writerow(new_stocks)
            stockfile.flush()
        print(f'Total = {lastprice*nshares}')
        print(f"{name} Addded Successfully")

    
    def removestock(self, name, nshares_to_remove):
        rows = []
        name = name.upper()  
        remaining_to_remove = int(nshares_to_remove)
        # 1. Read existing data
        try:
            with open('stocks.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                for row in reader:
                    # 2. Check if this is the stock we want to reduce
                    if row['name'].upper() == name and remaining_to_remove > 0:
                        current_shares = int(row['nshares'])
                        
                        if current_shares <= remaining_to_remove:
                            # Remove this entire row's shares
                            remaining_to_remove -= current_shares
                            row['nshares'] = 0 
                        else:
                            # This row has more than we need to remove
                            row['nshares'] = current_shares - remaining_to_remove
                            remaining_to_remove = 0
                    
                    rows.append(row)
        except FileNotFoundError:
            raise FileNotFoundError("stocks.csv not found.")

        if remaining_to_remove > 0:
            print(f"Warning: Only removed partial shares. {remaining_to_remove} shares not found.")

        with open('stocks.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                if int(row['nshares']) > 0:
                    writer.writerow(row)
            f.flush()


class Otheroptions: 
    def __init__(self,td_day = date.today()):
        self.date = td_day


    def update_balance(self,balance):
        fieldnames = ["date",'balance','savings','other_assets']
        with open("ledger.csv","r") as f:
            last_row = None
            reader = csv.DictReader(f)
            for row in reader:
                last_row = row

        with open("ledger.csv", 'a', newline='',encoding="utf-8") as stockfile:
            writer = csv.DictWriter(stockfile,fieldnames=fieldnames)
            savings = last_row['savings']
            assets = last_row['other_assets']
            new_bal = {
                "date":self.date,
                "balance":balance,
                "savings":savings,
                "other_assets":assets
            }
            writer.writerow(new_bal)
            stockfile.flush()
        print(f"Balance Updated Successfully")


    def update_savings(self,savings):
        fieldnames = ["date",'balance','savings','other_assets']
        with open("ledger.csv","r") as f:
            last_row = None
            reader = csv.DictReader(f)
            for row in reader:
                last_row = row

        with open("ledger.csv", 'a', newline='',encoding="utf-8") as stockfile:
            writer = csv.DictWriter(stockfile,fieldnames=fieldnames)
            balance = last_row['balance']
            assets = last_row['other_assets']
            new_sav = {
                "date":self.date,
                "balance":balance,
                "savings":savings,
                "other_assets":assets
            }
            writer.writerow(new_sav)
            stockfile.flush()
        print(f"Savings Updated Successfully")

    
    def update_assets(self,assets):
        fieldnames = ["date",'balance','savings','other_assets']
        with open("ledger.csv","r") as f:
            last_row = None
            reader = csv.DictReader(f)
            for row in reader:
                last_row = row

        with open("ledger.csv", 'a', newline='',encoding="utf-8") as stockfile:
            writer = csv.DictWriter(stockfile,fieldnames=fieldnames)
            savings = last_row['savings']
            balance = last_row['balance']
            new_ast = {
                "date":self.date,
                "balance":balance,
                "savings":savings,
                "other_assets":assets
            }
            writer.writerow(new_ast)
            stockfile.flush()
        print(f"Assets Updated Successfully")
