import json
import os
from datetime import datetime
from functional_components import * # This must contain your resource_path function

# This is the path to the persistent file (next to the .exe)
LOCAL_FILE = "data.json"

def save_data(financial_components):
    """Always saves to the local folder next to the EXE."""
    data_to_save = [comp.to_dict() for comp in financial_components]
    with open(LOCAL_FILE, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, indent=4)

def load_data():
    """Tries to load local data; if missing, loads the bundled template."""
    raw_data = []
    
    # 1. Check if user has a local data file
    if os.path.exists(LOCAL_FILE):
        path_to_load = LOCAL_FILE
    else:
        # 2. If no local file, try to find the one bundled inside the EXE
        path_to_load = resource_path("data.json")
    
    # Check if we actually found a file at either location
    if not os.path.exists(path_to_load):
        return []

    try:
        with open(path_to_load, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            raw_data = json.loads(content)
    except (json.JSONDecodeError, IOError):
        return []

    # --- Reconstructing objects (Your existing logic) ---
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