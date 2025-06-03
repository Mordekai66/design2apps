import requests
import os
import random
from Writers import pyqt5_writer


def create_text(element):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    text_content = element.get("characters", "")
    font_size = int(element["style"].get("fontSize", 12))
    font_family = element["style"].get("fontFamily", "Arial")
    text_color = element["fills"][0]["color"]
    text_hex = "#%02x%02x%02x" % (int(text_color["r"] * 255),
                                  int(text_color["g"] * 255),
                                  int(text_color["b"] * 255))

    pyqt5_writer.write(f"""
        label = QLabel("{text_content}", self)
        label.setFont(QFont("{font_family}", {font_size}))
        label.setStyleSheet("color: {text_hex};")
        label.move({x}, {y})
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
            shape_color = button_shape["fills"][0].get("color", {"r": 1, "g": 1, "b": 1})
            fill_color = "#%02x%02x%02x" % (int(shape_color["r"] * 255),
                                            int(shape_color["g"] * 255),
                                            int(shape_color["b"] * 255))

        pyqt5_writer.write(f"""
        button = QPushButton("{button_text}", self)
        button.setGeometry({x}, {y}, {width}, {height})
        button.setStyleSheet("border-radius: {radius}px; background-color: {fill_color};")
""", file_path)


def create_entry(element):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    text_color = element["fills"][0]["color"]
    entry_hex = "#%02x%02x%02x" % (int(text_color["r"] * 255),
                                   int(text_color["g"] * 255),
                                   int(text_color["b"] * 255))
    radius = int(element.get("cornerRadius", 0))

    pyqt5_writer.write(f"""
        text_input = QLineEdit(self)
        text_input.setPlaceholderText("Write here")
        text_input.setMaxLength(20)
        text_input.setFont(QFont("Arial", 14))
        text_input.setStyleSheet("background-color: {entry_hex}; border-radius: {radius}px;")
        text_input.setGeometry({x}, {y}, {width}, {height})
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
        image_label = QLabel(self)
        image_label.setPixmap(QPixmap(r"{image_path}"))
        image_label.setGeometry({x}, {y}, {width}, {height})
        image_label.setStyleSheet("border-radius: {corner_radius}px;")
""", file_path)


def create_rectangle(element):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    fill_color = "#D9D9D9"
    if "fills" in element and element["fills"]:
        shape_color = element["fills"][0].get("color", {"r": 0.85, "g": 0.85, "b": 0.85})
        fill_color = "#%02x%02x%02x" % (
            int(shape_color["r"] * 255),
            int(shape_color["g"] * 255),
            int(shape_color["b"] * 255)
        )
    radius = int(element.get("cornerRadius", 0))
    pyqt5_writer.write(f"""
        painter = QPainter(self)
        painter.setBrush(QColor("{fill_color}"))
        painter.setPen(QColor("black"))
        painter.drawRoundedRect({x}, {y}, {width}, {height}, {radius}, {radius})
""", file_path)


def create_ellipse(element):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    fill_color = "#D9D9D9"
    if "fills" in element and element["fills"]:
        shape_color = element["fills"][0].get("color", {"r": 0.85, "g": 0.85, "b": 0.85})
        fill_color = "#%02x%02x%02x" % (
            int(shape_color["r"] * 255),
            int(shape_color["g"] * 255),
            int(shape_color["b"] * 255)
        )
    radius = int(element.get("cornerRadius", 0))
    pyqt5_writer.write(f"""
        painter = QPainter(self)
        painter.setBrush(QColor("{fill_color}"))
        painter.setPen(QColor("black"))
        painter.drawEllipse({x}, {y}, {width}, {height})
""", file_path)

def transform_json_to_pyqt5(data, output_path, file_id_figma, token_access):
    global file_path
    file_path = os.path.join(output_path,"\\", "build", "pyqt5.py")
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

    document = data["document"]
    page = document["children"][0]
    frame = page["children"][0]
    frame_width = int(frame["absoluteRenderBounds"]["width"])
    frame_height = int(frame["absoluteRenderBounds"]["height"])
    bg_color = frame.get("backgroundColor", {"r": 1, "g": 1, "b": 1})
    bg_hex = "#%02x%02x%02x" % (int(bg_color["r"] * 255),
                int(bg_color["g"] * 255),
                int(bg_color["b"] * 255))

    pyqt5_writer.write(f"""
        self.setWindowTitle('{page["name"]}')
        self.setGeometry(100, 100, {frame_width}, {frame_height})
        self.setStyleSheet("background-color: {bg_hex};")
""", file_path)

    for element in frame["children"]:
        print(f'{element["name"]}, {element["type"]} was created in PyQt5')
            
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

    pyqt5_writer.write("""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PyQt5App()
    window.show()
    sys.exit(app.exec_())
""", file_path)
    pyqt5_writer.write("close()", file_path)