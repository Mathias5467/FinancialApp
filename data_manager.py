import json
import os
from datetime import datetime
from functional_components import *

FILE_NAME = "data.json"

def save_data(financial_components):
    data_to_save = [comp.to_dict() for comp in financial_components]
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, indent=4)

def load_data():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            raw_data = json.loads(content)
    except (json.JSONDecodeError, IOError):
        return []

    loaded_components = []
    for item in raw_data:
        
        img_name = item.get("image_name", "money")
        
        if item["type"] == "Savings":
            obj = Savings(item["name"], item.get("target_amount", 0), img_name, item["current_amount"])
        else:
            obj = Budget(item["name"], img_name, item["current_amount"])

        
        for t in item["transactions"]:
            trans = Transaction(
                amount=t["amount"],
                type=TransactionType(t["type"]), 
                current_amount=t["current_amount"],
                date=datetime.fromisoformat(t["date"]),
                note=t["note"]
            )
            obj.transactions.append(trans)
        
        loaded_components.append(obj)
    
    return loaded_components