import os, json

def load_item(file):
    with open(file, "r") as f:
        return json.load(f)

def save_item(file, item):
    with open(file, "w") as f:
        json.dump(item, f, indent=4)
        
def get_host(url: str):
    return url.split(":")[-1]