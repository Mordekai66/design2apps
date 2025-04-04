
import requests
import os
import math
import random

file_path = ""


def transform_json_to_kivy(data, output_path, file_id_figma, token_access):
    global file_path
    file_path = os.path.join(output_path+"\\"+"build"+"\\"+"kivy_code.py")
    f = open(file_path, "w", encoding="utf-8")

    f.write("from kivy.app import App")
    f.write("\n")
    f.write("from kivy.core.window import Window")
    f.write("\n")
    f.write("""from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Ellipse, Color
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
""")
    f.write("\n")
    f.write("\n")

    document = data["document"]
    page = document["children"][0]
    frame = page["children"][0]

    f.write("image_ref = []")
    f.write("\n")
    f.write("\n")

    frame_width = int(frame["absoluteRenderBounds"]["width"])
    frame_height = int(frame["absoluteRenderBounds"]["height"])

    f.write(f"Window.size = ({frame_width},{frame_height})")
    f.write("\n")

    bg_color = frame.get("backgroundColor", {"r": 1, "g": 1, "b": 1})
    f.write(
        f'Window.clearcolor = ({bg_color["r"]}, {bg_color["g"]}, {bg_color["b"]})')
    f.write("\n")
    f.write("\n")
    print(f"bg_color done: {bg_color}")


    f.write("""class Kivy_app(App):
    def build(self):""")
    f.write("\n\n")
    print("class created")


    f.write("        layout = FloatLayout()")
    f.write("\n\n")

    for element in frame["children"]:
        x = abs(int(element["absoluteBoundingBox"]["x"]))
        y = abs(int(element["absoluteBoundingBox"]["y"]))
        width = int(element["absoluteBoundingBox"]["width"])
        height = int(element["absoluteBoundingBox"]["height"])

        print([element["name"], element["type"], x, y, width, height])

        if element["type"] == "TEXT" or element["name"].lower() == "text":
            text_content = element.get("characters", "")
            font_size = int(element["style"].get("fontSize", 12))
            font_family = "Arial"
            text_color = element["fills"][0]["color"]


            f.write(f"""        label = Label(
        text = '{text_content}',
        font_name = '{font_family}',
        font_size = {font_size},
        size_hint = (None, None),
        pos_hint = {{'x': {x / frame_width}, 'y': {1 - (y / frame_height)}}},
        halign="left",  
        valign="top"
        )

        layout.add_widget(label)""")
            f.write("\n\n")

        elif element["name"].lower() == "button":
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
                        
                        f.write(f"""
        btn = Button(
        text='{button_text}',
        size_hint=({width} / {frame_width}, {height} / {frame_height}),
        pos_hint={{'x': {x} / {frame_width}, 'y': 1 - ({y} / {frame_height})}}
        )
        layout.add_widget(btn)""")
                        f.write("\n")
                        f.write("\n")


        elif element["name"].lower() == "entry":
            text_color = element["fills"][0]["color"]

            f.write(f"""
        entry = TextInput(
        hint_text="Enter text here",
        pos_hint={{'x': {x / frame_width}, 'y': 1 - ({y} / {frame_height})}},
        size_hint=({width / frame_width}, {height / frame_height}),
        background_color={text_color['r'], text_color['g'],text_color['b'],1},
        font_size=14)

        layout.add_widget(entry)
""")
            f.write("\n\n")


        elif element["name"].lower() == "image":
            node_id = element["id"]
            file_id = file_id_figma
            access_token = token_access

            url = f"https://api.figma.com/v1/images/{file_id}?ids={node_id}"
            headers = {"X-Figma-Token": access_token}

            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Error:{response.status_code}, Response: {response.text}")
                continue

            image_data = response.json()
            image_url = image_data["images"].get(node_id, "")

            img_data = requests.get(image_url).content
            if not os.path.exists(f"{output_path}/build/image"):
                os.mkdir(f"{output_path}/build/image")

            image_path = f"{output_path}/build/image/{random.randint(1, 200)}.png"
            with open(image_path, "wb") as s:
                s.write(img_data)

            f.write(f"""
        img = Image(
        source=r'{image_path}',
        pos_hint={{'x': {x / frame_width}, 'y': {1 - ((y + height / 2) / frame_height)}}},
        size_hint=(87 / 594, 84 / 423))

        layout.add_widget(img)
""")
            f.write("\n\n")

                    
        elif element["type"] in ["RECTANGLE", "ELLIPSE"]:
            x = abs(int(element["absoluteBoundingBox"]["x"]))
            y = abs(int(element["absoluteBoundingBox"]["y"]))
            width = int(element["absoluteBoundingBox"]["width"])
            height = int(element["absoluteBoundingBox"]["height"])

            if "fills" in element and element["fills"]:
                shape_color = element["fills"][0].get("color", {"r": 0.85, "g": 0.85, "b": 0.85})

            if element["type"] == "RECTANGLE":
                x = x
                y = frame_height - y -height
                width = width
                height = height
                f.write(f"""
        with layout.canvas:
            Color({shape_color['r']},{shape_color['g']},{shape_color['b']})
            Rectangle(pos=({x}, {y}),
            size=({width}, {height}))
""")
                f.write("\n\n")

            elif element["type"] == "ELLIPSE":
                x = x
                y = frame_height - y - height
                width = width
                height = height
                f.write(f"""
        with layout.canvas:
            Color({shape_color['r']},{shape_color['g']},{shape_color['b']})
            Ellipse(pos=({x}, {y}),
            size=({width}, {height}))
    """)
                f.write("\n\n")
            
    f.write(f"        return layout")
    f.write("\n\n")
    f.write("Kivy_app().run()")
    f.close()