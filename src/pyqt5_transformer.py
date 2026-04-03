import requests
import os
import random
import writer as pyqt5_writer
import utils

file_path = ""

def create_text(element):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    text_content = element.get("characters", "")
    font_size = int(element["style"].get("fontSize", 12))
    font_family = element["style"].get("fontFamily", "Arial")
    text_hex = utils.rgb_to_hex(element["fills"][0]["color"])

    pyqt5_writer.write(f"""
        label_{element['id'].replace(":", "_")} = QLabel("{text_content}", self)
        label_{element['id'].replace(":", "_")}.setFont(QFont("{font_family}", {font_size}))
        label_{element['id'].replace(":", "_")}.setStyleSheet("color: {text_hex};")
        label_{element['id'].replace(":", "_")}.move({x}, {y})
""", file_path)

def create_button(element):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
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
        radius = int(button_shape.get("cornerRadius", 0))

        if "fills" in button_shape and button_shape["fills"]:
            fill_color = utils.rgb_to_hex(button_shape["fills"][0].get("color", {"r": 1, "g": 1, "b": 1}))

        pyqt5_writer.write(f"""
        button_{element['id'].replace(":", "_")} = QPushButton("{button_text}", self)
        button_{element['id'].replace(":", "_")}.setGeometry({x}, {y}, {width}, {height})
        button_{element['id'].replace(":", "_")}.setStyleSheet("border-radius: {radius}px; background-color: {fill_color};")
""", file_path)

def create_entry(element):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    entry_hex = utils.rgb_to_hex(element["fills"][0]["color"])
    radius = int(element.get("cornerRadius", 0))

    pyqt5_writer.write(f"""
        text_input_{element['id'].replace(":", "_")} = QLineEdit(self)
        text_input_{element['id'].replace(":", "_")}.setPlaceholderText("Write here")
        text_input_{element['id'].replace(":", "_")}.setMaxLength(20)
        text_input_{element['id'].replace(":", "_")}.setFont(QFont("Arial", 14))
        text_input_{element['id'].replace(":", "_")}.setStyleSheet("background-color: {entry_hex}; border-radius: {radius}px;")
        text_input_{element['id'].replace(":", "_")}.setGeometry({x}, {y}, {width}, {height})
""", file_path)

def create_image(element,output_path, file_id_figma,token_access):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    node_id = element["id"]
    file_id = file_id_figma
    access_token = token_access
    corner_radius = element.get("cornerRadius", 0)

    url = f"https://api.figma.com/v1/images/{file_id}?ids={node_id}"
    headers = {"X-Figma-Token": access_token}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.status_code}, Response: {response.text}")
        return

    image_data = response.json()
    image_url = image_data["images"].get(node_id, "")

    img_data = requests.get(image_url).content
    image_dir = os.path.join(output_path, "build", "image")
    os.makedirs(image_dir, exist_ok=True)
    image_path = os.path.join(image_dir, f"{random.randint(1, 200)}.png")
    with open(image_path, "wb") as s:
        s.write(img_data)

    pyqt5_writer.write(f"""
        image_label_{element['id'].replace(":", "_")} = QLabel(self)
        image_label_{element['id'].replace(":", "_")}.setPixmap(QPixmap(r"{image_path}"))
        image_label_{element['id'].replace(":", "_")}.setGeometry({x}, {y}, {width}, {height})
        image_label_{element['id'].replace(":", "_")}.setStyleSheet("border-radius: {corner_radius}px;")
""", file_path)


def create_rectangle(element):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    fill_color = "#D9D9D9"
    if "fills" in element and element["fills"]:
        fill_color = utils.rgb_to_hex(element["fills"][0].get("color", {"r": 0.85, "g": 0.85, "b": 0.85}))
    radius = int(element.get("cornerRadius", 0))
    pyqt5_writer.write(f"""
        painter_{element['id'].replace(":", "_")} = QPainter(self)
        painter_{element['id'].replace(":", "_")}.setBrush(QColor("{fill_color}"))
        painter_{element['id'].replace(":", "_")}.setPen(QColor("black"))
        painter_{element['id'].replace(":", "_")}.drawRoundedRect({x}, {y}, {width}, {height}, {radius}, {radius})
""", file_path)

def create_ellipse(element):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    fill_color = "#D9D9D9"
    if "fills" in element and element["fills"]:
        fill_color = utils.rgb_to_hex(element["fills"][0].get("color", {"r": 0.85, "g": 0.85, "b": 0.85}))
    radius = int(element.get("cornerRadius", 0))
    pyqt5_writer.write(f"""
        painter_{element['id'].replace(":", "_")} = QPainter(self)
        painter_{element['id'].replace(":", "_")}.setBrush(QColor("{fill_color}"))
        painter_{element['id'].replace(":", "_")}.setPen(QColor("black"))
        painter_{element['id'].replace(":", "_")}.drawEllipse({x}, {y}, {width}, {height})
""", file_path)

def transform_to_pyqt5(data, output_path, file_id_figma, token_access):
    global file_path
    file_path = os.path.join(output_path + "\\build" + "\\pyqt5.py")
    if os.path.exists(file_path):
        os.remove(file_path)

    pyqt5_writer.write("""import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QFrame
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QPixmap, QIcon, QColor
import requests
import os
import random

class PyQt5App(QWidget):
    def __init__(self):
        super().__init__()
""", file_path)


    page = data['document']["children"][0]
    frame = page["children"][0]
    frame_width = int(frame["absoluteRenderBounds"]["width"])
    frame_height = int(frame["absoluteRenderBounds"]["height"])
    bg_hex = utils.rgb_to_hex(frame.get("backgroundColor", {"r": 1, "g": 1, "b": 1}))

    pyqt5_writer.write(f"""
        self.setWindowTitle('{page["name"]}')
        self.setGeometry(100, 100, {frame_width}, {frame_height})
        self.setStyleSheet("background-color: {bg_hex};")
""", file_path)

    for element in frame["children"]:
        if element["type"] == "TEXT" or element["name"].lower() == "text":
            create_text(element)
        elif element["name"].lower() == "button":
            create_button(element)
        elif element["name"].lower() == "entry":
            create_entry(element)
        elif element["name"].lower() == "image":
            create_image(element,output_path, file_id_figma,token_access)
        elif element["type"] =="RECTANGLE":
            create_rectangle(element)
        elif element["type"] == "ELLIPSE":
            create_ellipse(element)

        print(f'{element["name"]}, {element["type"]} was created in PyQt5')
        
    pyqt5_writer.write("""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PyQt5App()
    window.show()
    sys.exit(app.exec_())
""", file_path)