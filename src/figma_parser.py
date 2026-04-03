import requests
import json
import os

def parse(token, file_id, output_dir):
    url = f"https://api.figma.com/v1/files/{file_id}"
    headers = {"X-Figma-Token": token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if not os.path.exists(os.path.join(output_dir, "build")):
            os.makedirs(os.path.join(output_dir, "build"))
        with open(os.path.join(output_dir, "build", "json.json"), "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)
            return data
    else:
        print(f"Failed: {response.status_code}, {response.text}")
        return None

def load_local_json(json_path, output_dir):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not os.path.exists(os.path.join(output_dir, "build")):
            os.makedirs(os.path.join(output_dir, "build"))
        with open(os.path.join(output_dir, "build", "json.json"), "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)
        return data
    except Exception as e:
        print(f"Error loading local JSON: {e}")
        return None