import os, json 

def open_json_file(path):
    try:
        with open(path, 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data
    except Exception as e:
        return "Could not open the json file"

def fetch_data():
    path = os.path.join("DEV")
    for folder in os.listdir(path):
        dir_path = os.path.join(path, folder)
        if os.path.isdir(dir_path):  
            for file in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file)
                data = open_json_file(file_path)
                if (isinstance(data, dict)):
                    url = data["url"]
                    content = data["content"]
                    if url and content:
                        yield url, content