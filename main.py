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
    id = generate_id()

    entry_data = check_up()

    entry_data.append({
        'id': id,
        'date': nowtime,
        'description': description,
        'amount': amount
    }) 

    create_expenses_json(entry_data)    

add_expense("jopa2", 20)