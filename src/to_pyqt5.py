import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel,QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame

from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QPixmap, QIcon, QColor

import requests
import os
import math
import random

file_path = ""

def transform_json_to_pyqt5(data,output_path,file_id_figma,token_access):
    global file_path
    file_path = os.path.join(output_path+"\\"+"build"+"\\"+"pyqt5.py")
    f = open(file_path, "w", encoding="utf-8")

    f.write("""import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel,
QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame

from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QPixmap, QIcon, QColor""")

    document = data["document"]
    page = document["children"][0]
    frame = page["children"][0]

    f.write("""image_refs = []
            
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle(document["name"])""")

    frame_width = int(frame["absoluteRenderBounds"]["width"])
    frame_height = int(frame["absoluteRenderBounds"]["height"])
    f.write(f'window.setGeometry(100,100",{frame_width},{frame_height}")')
    f.write("\n")

    bg_color = frame.get("backgroundColor", {"r": 1, "g": 1, "b": 1})
    bg_hex = "#%02x%02x%02x" % (int(bg_color["r"] * 255), 
                                int(bg_color["g"] * 255), 
                                int(bg_color["b"] * 255))
    f.write(f'window.setStyleSheet("background-color: {bg_hex};")')
    f.write("\n")
    f.write("\n")


    for element in frame["children"]:
        x = abs(int(element["absoluteBoundingBox"]["x"]))
        y = abs(int(element["absoluteBoundingBox"]["y"]))
        width = int(element["absoluteBoundingBox"]["width"])
        height = int(element["absoluteBoundingBox"]["height"])

        print([element["name"], element["type"], x, y, width, height])

        if element["type"] == "TEXT" or element["name"].lower() == "text":
            text_content = element.get("characters", "")
            font_size = int(element["style"].get("fontSize", 12))
            font_family = element["style"].get("fontFamily", "Arial")
            text_color = element["fills"][0]["color"]
            text_hex = "#%02x%02x%02x" % (int(text_color["r"] * 255),
                                          int(text_color["g"] * 255),
                                          int(text_color["b"] * 255))

            f.write(f"""label = QLabel(text_content, window)
label.setFont(QFont({font_family}, {font_size}))
label.setStyleSheet(f"color: {text_hex};")
label.move({x}, {y})""")

        elif element["name"].lower() == "button":
            button_shape = None
            button_text = None
            
            for child in element["children"]:
                if child["type"] == "TEXT":
                    button_text = child.get("characters", "Button")
                elif child["type"] == "RECTANGLE":
                    button_shape = child

            if button_shape:
                x = abs(int(button_shape["absoluteBoundingBox"]["x"]))
                y = abs(int(button_shape["absoluteBoundingBox"]["y"]))
                width = int(button_shape["absoluteBoundingBox"]["width"])
                height = int(button_shape["absoluteBoundingBox"]["height"])
                print("yes")

                if "fills" in button_shape and button_shape["fills"]:
                    shape_color = button_shape["fills"][0].get("color", {"r": 1, "g": 1, "b": 1})
                    fill_color = "#%02x%02x%02x" % (int(shape_color["r"] * 255),
                                                    int(shape_color["g"] * 255),
                                                    int(shape_color["b"] * 255))

                f.write(f"""
button = QPushButton(
{button_text},
window,
)
button.setStyleSheet(f"color {fill_color};")
button.setGeometry({x},{y},{width},{height})
button.move({x},{y})""")

            f.write("\n")
            f.write("\n")


        elif element["name"].lower() == "entry":
            text_color = element["fills"][0]["color"]
            text_hex = "#%02x%02x%02x" % (int(text_color["r"] * 255),
                                          int(text_color["g"] * 255),
                                          int(text_color["b"] * 255))

            f.write(f"""
text_input = QLineEdit(
window
)

text_input.setPlaceholderText("Write here")  
text_input.setMaxLength(20)
text_input.setFont(QFont("Arial", 14))

text_input.setStyleSheet(f"background-color: {text_hex};")


text_input.setGeometry(x, y, width, height)""")

        elif element["name"].lower() == "image":
            node_id = element["id"]
            file_id = file_id_figma
            access_token = token_access

            url = f"https://api.figma.com/v1/images/{file_id}?ids={node_id}"
            headers = {"X-Figma-Token": access_token}

            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Error: {response.status_code}, Response: {response.text}")
                continue

            image_data = response.json()
            image_url = image_data["images"].get(node_id, "")

            img_data = requests.get(image_url).content
            if not os.path.exists(f"{output_path}/build/image"):
                os.mkdir(f"{output_path}/build/image")

            image_path = f"{output_path}/build/image/{random.randint(1,200)}.png"
            with open(image_path, "wb") as s:
                s.write(img_data)


            f.write(f"""image_label = QLabel(window)
image_label.setPixmap(QPixmap({image_path}))
image_label.setGeometry({x},{y},{width},{height})""")

#         elif element["type"] in ["RECTANGLE", "ELLIPSE"]:
#             x = abs(int(element["absoluteBoundingBox"]["x"]))
#             y = abs(int(element["absoluteBoundingBox"]["y"]))
#             width = int(element["absoluteBoundingBox"]["width"])
#             height = int(element["absoluteBoundingBox"]["height"])

#             fill_color = "#D9D9D9"
#             if "fills" in element and element["fills"]:
#                 shape_color = element["fills"][0].get("color", {"r": 0.85, "g": 0.85, "b": 0.85})
#                 fill_color = "#%02x%02x%02x" % (int(shape_color["r"] * 255),
#                                                 int(shape_color["g"] * 255),
#                                                 int(shape_color["b"] * 255))

#             if element["type"] == "RECTANGLE":
#                 canvas.create_rectangle(x, y, x + width, y + height, fill=fill_color, outline="black")
#                 f.write(f"canvas.create_rectangle({x}, {y}, {x + width}, {y + height}, fill='{fill_color}', outline='black')")
#                 f.write("\n")
#                 f.write("\n")

#             elif element["type"] == "ELLIPSE":
#                 canvas.create_oval(x, y, x + width, y + height, fill=fill_color, outline="black")
#                 f.write(f"""
# canvas.create_oval({x}, {y}, {x + width}, {y + height}, fill='{fill_color}', outline='black')""")
#                 f.write("\n")
#                 f.write("\n")


    f.write("\n")
    f.write("window.show" \
    "sys.exit(app.exec_())")
    f.close()