import requests
import json
import os
def parse(token, file_id,output_file_path):
    access_token = token
    # file_id = "Xi5mvUCmU48YtGxJf3yplN"
    # access_token = "figd_nchgLbfRxprBUHGmCelEv8wYojZm-8klyU9yeL9B"

    url = f"https://api.figma.com/v1/files/{file_id}"
    headers = {"X-Figma-Token": access_token}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        with open(os.path.join(output_file_path+"//"+"build"+"//"+"json.json"), "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)

            return data
    else:
        print(f"Failed: {response.status_code}, {response.text}")
        return 