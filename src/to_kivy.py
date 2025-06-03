import requests
import os
import math
import random
from Writers import kivy_writer

file_path = ""

def create_text(element,frame_width, frame_height):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    text_content = element.get("characters", "")
    font_size = int(element["style"].get("fontSize", 12))
    font_family = "Arial"
    text_color = element["fills"][0]["color"]


    kivy_writer.write(f"""
        label = Label(
        text = '{text_content}',
        font_name = '{font_family}',
        font_size = {font_size},
        size_hint=(None, None),
        size = ({width}, {height}),
        pos = ({x}, Window.size[1]-({y+height})),
        )

        layout.add_widget(label)""", file_path)
    kivy_writer.write("\n\n", file_path)


def create_button(element,frame_width, frame_height):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    button_shape = "RECTANGLE"
    button_text = "Button"
    for child in element["children"]:
        if child["type"] == "TEXT":
                    button_text = child.get("characters", "Button")
        elif child["type"]  == "RECTANGLE":
                    button_shape = child

    if button_shape:
        x = abs(int(button_shape["absoluteBoundingBox"]["x"]))
        y = abs(int(button_shape["absoluteBoundingBox"]["y"]))
        width = int(button_shape["absoluteBoundingBox"]["width"])
        height = int(button_shape["absoluteBoundingBox"]["height"])

    if "fills" in button_shape and button_shape["fills"]:
        shape_color = button_shape["fills"][0].get("color", {"r": 1, "g": 1, "b": 1})

    if button_shape["type"] == "RECTANGLE":
                        
        kivy_writer.write(f"""
        btn = Button(
        text='{button_text}',
        size_hint=(None, None),
        size = ({width}, {height}),
        pos = ({x}, Window.size[1]-({y+height})),
        )
        layout.add_widget(btn)""", file_path)
        kivy_writer.write("\n", file_path)
        kivy_writer.write("\n", file_path)


def create_entry(element,frame_width, frame_height):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    text_color = element["fills"][0]["color"]

    kivy_writer.write(f"""
        entry = TextInput(
        hint_text="Enter text here",
        size_hint=(None, None),
        size = ({width}, {height}),
        pos = ({x}, Window.size[1]-({y+height})),
        background_color={text_color['r'], text_color['g'],text_color['b'],1},
        font_size=14)

        layout.add_widget(entry)
""", file_path)
    kivy_writer.write("\n\n", file_path)


def create_image(element,frame_width, frame_height, output_path, file_id_figma, token_access):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    node_id = element["id"]
    file_id = file_id_figma
    access_token = token_access

    url = f"https://api.figma.com/v1/images/{file_id}?ids={node_id}"
    headers = {"X-Figma-Token": access_token}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error:{response.status_code}, Response: {response.text}")

    image_data = response.json()
    image_url = image_data["images"].get(node_id, "")

    img_data = requests.get(image_url).content
    if not os.path.exists(f"{output_path}/build/image"):
        os.mkdir(f"{output_path}/build/image")

    image_path = f"{output_path}/build/image/{random.randint(1, 200)}.png"
    with open(image_path, "wb") as s:
        s.write(img_data)

    kivy_writer.write(f"""
        img = Image(
        source=r'{image_path}',
        size_hint=(None, None),
        size = ({width}, {height}),
        pos = ({x}, Window.size[1]-({y+height})))

        layout.add_widget(img)
""", file_path)
    kivy_writer.write("\n\n", file_path)

def create_rectangle(element):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])

    if "fills" in element and element["fills"]:
        shape_color = element["fills"][0].get("color", {"r": 0.85, "g": 0.85, "b": 0.85})
    kivy_writer.write(f"""
        with layout.canvas:
            Color({shape_color['r']},{shape_color['g']},{shape_color['b']})
            Rectangle(pos=({x}, Window.size[1]-({y+height})),
            size=({width}, {height}))
""", file_path)
    kivy_writer.write("\n\n", file_path)

def create_ellipse(element):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])

    if "fills" in element and element["fills"]:
        shape_color = element["fills"][0].get("color", {"r": 0.85, "g": 0.85, "b": 0.85})
    kivy_writer.write(f"""
        with layout.canvas:
            Color({shape_color['r']},{shape_color['g']},{shape_color['b']})
            Ellipse(pos=({x}, Window.size[1]-({y+height})),
            size=({width}, {height}))
    """, file_path)
    kivy_writer.write("\n\n", file_path)



def transform_json_to_kivy(data, output_path, file_id_figma, token_access):
    global file_path
    file_path = os.path.join(output_path+"\\"+"build"+"\\"+"kivy_code.py")
    
    if os.path.exists(file_path):
        os.remove(file_path)
    
    document = data["document"]
    page = document["children"][0]
    frame = page["children"][0]
    frame_width = int(frame["absoluteRenderBounds"]["width"])
    frame_height = int(frame["absoluteRenderBounds"]["height"])



    kivy_writer.write(f"""from kivy.config import Config
Config.set('graphics', 'width', '{int(frame_width - (frame_width*0.20))}')
Config.set('graphics', 'height', '{int(frame_height - (frame_height*0.20))}')
Config.set('graphics', 'resizable', 0)
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Ellipse, Color
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
""", file_path)
    kivy_writer.write("from kivy.app import App", file_path)
    kivy_writer.write("\n", file_path)
    kivy_writer.write("from kivy.core.window import Window", file_path)
    kivy_writer.write("\n", file_path)
    kivy_writer.write("\n", file_path)
    kivy_writer.write("\n", file_path)



    kivy_writer.write("image_ref = []", file_path)
    kivy_writer.write("\n", file_path)
    kivy_writer.write("\n", file_path)

    bg_color = frame.get("backgroundColor", {"r": 1, "g": 1, "b": 1})
    kivy_writer.write(
        f'Window.clearcolor = ({bg_color["r"]}, {bg_color["g"]}, {bg_color["b"]})', file_path)
    kivy_writer.write("\n", file_path)
    kivy_writer.write("\n", file_path)
    print(f"bg_color done: {bg_color}")


    kivy_writer.write("""class Kivy_app(App):
    def build(self):""", file_path)
    kivy_writer.write("\n\n", file_path)
    print("class created")


    kivy_writer.write("        layout = FloatLayout()", file_path)
    kivy_writer.write("\n\n", file_path)

    for element in frame["children"]:
        print(f'{element["name"]}, {element["type"]} was created in Kivy')

        if element["type"] == "TEXT" or element["name"].lower() == "text":
            create_text(element,frame_width,frame_height)

        elif element["name"].lower() == "button":
            create_button(element,frame_width,frame_height)

        elif element["name"].lower() == "entry":
            create_entry(element,frame_width,frame_height)


        elif element["name"].lower() == "image":
            create_image(element,frame_width, frame_height, output_path, file_id_figma, token_access)

        elif element["type"] == "RECTANGLE":
            create_rectangle(element)
                

        elif element["type"] == "ELLIPSE":
            create_ellipse(element)
            
    kivy_writer.write("""
        return layout""", file_path)
    kivy_writer.write("\n\n", file_path)
    kivy_writer.write("Kivy_app().run()", file_path)
    kivy_writer.write("close()", file_path)