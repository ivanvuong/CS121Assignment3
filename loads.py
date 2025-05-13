import os, json 

def open_json_file(path):
    try:
        with open(path, 'r', encoding="utf-08") as f:
            data = json.load(f)
            return data
    except Exception as e:
        return "Could not open the json file"

def fetch_data():
    documents = {}
    folder = os.path.join("DEV") 
    for dirpath, dirnames, filenames in os.walk(folder):
        for file in filenames:
            path = os.path.join(dirpath, file)
            data = open_json_file(path)
            if (isinstance(data, dict)):
                url = data["url"]
                content = data["content"]
                documents[url] = content
    return documents 