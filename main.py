import json
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

def add_expense(description, amount):
    nowtime = datetime.now().isoformat() 
    ex_id = generate_id()

    entry_data = check_up()

    entry_data.append({
        'id': ex_id,
        'date': nowtime,
        'description': description,
        'amount': amount
    }) 

    create_expenses_json(entry_data)    
    print(f"Expense added (ID: {id})")

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

update_expense_desc(1, "haha")
update_expense_mount(1, 3000)