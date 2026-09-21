import json
import pandas as pd
import argparse
import os
from datetime import datetime

EXPENSES_FILE = "expenses.json"

def generate_id():
    if os.path.exists(EXPENSES_FILE) and os.path.getsize(EXPENSES_FILE) > 0:
        with open(EXPENSES_FILE, "r") as f:
            data = json.load(f)
        value = data[-1].get('id')
        return value + 1
    else:
      return 1 

def check_up():
    if os.path.exists(EXPENSES_FILE) and os.path.getsize(EXPENSES_FILE) > 0:
        with open(EXPENSES_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []
    expenses = data.copy()
    return expenses

def create_expenses_json(data):
    with open(EXPENSES_FILE, "w") as f:
        json.dump(data, f, indent=4)

def expenses_list():
    data = check_up()
    for expense in data:
        print(f"ID: {expense['id']} Date: {expense['date']} Description: {expense['description']} Amount: {expense['amount']}")

def add_expense(description, amount):
    nowtime = datetime.now().strftime("%d.%m.%Y") 
    ex_id = generate_id()

    entry_data = check_up()

    entry_data.append({
        'id': ex_id,
        'date': nowtime,
        'description': description,
        'amount': amount
    }) 

    create_expenses_json(entry_data)    
    print(f"Expense added (ID: {ex_id})")

def update_expense_desc(ex_id, description):
    data_to_update = check_up() 
    for expense in data_to_update:
        if expense["id"] == ex_id:
            expense['description'] = description
    create_expenses_json(data_to_update)

def update_expense_mount(ex_id, amount):
    data_to_update = check_up() 
    for expense in data_to_update:
        if expense["id"] == ex_id:
            expense['amount'] = amount 
    create_expenses_json(data_to_update)   

def delete_expense(ex_id):
    data = check_up()
    expenses = [exp for exp in data if exp['id'] != ex_id]
    create_expenses_json(expenses)

def summary_expenses_all():
    data = check_up()
    summ = 0
    for expense in data:
        summ += expense['amount']
    return summ

def summary_expenses_month(ex_month):
    data = check_up()
    summ = 0
    for expense in data:
        expense_date = datetime.strptime(expense['date'], "%d.%m.%Y")
        if expense_date.month == ex_month:
            summ += expense['amount']
    return summ

def to_csv():
    data = check_up()
    df = pd.DataFrame(data)
    df.to_csv("expenses.csv", index=False)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add expense
    parser_add = subparsers.add_parser("add")
    parser_add.add_argument("description", type=str)
    parser_add.add_argument("amount", type=int)

    #Update expense desc/amount
    parser_add = subparsers.add_parser("update")
    parser_add.add_argument("ex_id", type=int)
    parser_add.add_argument("status", nargs='?', choices=['description', 'amount'], default=None)
    parser_add.add_argument("value")
    
    #Delete expense
    parser_add = subparsers.add_parser("delete")
    parser_add.add_argument("ex_id", type=int)

    #List expenses
    parser_add = subparsers.add_parser("list")

    #Summary expense
    parser_add = subparsers.add_parser("summary")

    #CSV
    parser_add = subparsers.add_parser("csv")

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.description, args.amount)
    elif args.command == "update":
        if args.status == "description":
            update_expense_desc(args.ex_id, args.value)
        else:
            update_expense_mount(args.ex_id, int(args.value))
    elif args.command == "delete":
        delete_expense(args.ex_id)
    elif args.command == "list":
        expenses_list()
    elif args.command == "summary":
        print(summary_expenses_all()) 
    elif args.command == "csv":
        to_csv()

if __name__ == '__main__':
    main()