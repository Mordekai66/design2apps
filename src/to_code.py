from tkinter import Tk, Canvas, Entry, Button, Toplevel
import requests
from PIL import Image, ImageTk
import os
import math
import random

file_path = ""
def transform_json_to_app(data,output_path,file_id_figma,token_access):
    global file_path
    file_path = os.path.join(output_path+"\\"+"build"+"\\"+"output.py")
    f = open(file_path, "w", encoding="utf-8")
    f.write("from tkinter import *")
    f.write("\n")
    f.write("from PIL import Image, ImageTk")
    f.write("\n")
    f.write("\n")

    document = data["document"]
    page = document["children"][0]
    frame = page["children"][0]

    app = Toplevel()
    app.title(page["name"])
    f.write("image_refs = []")
    f.write("\n")
    f.write("\n")
    f.write("app = Tk()")
    f.write("\n")
    f.write(f'app.title("{page["name"]}")')
    f.write("\n")

    frame_width = int(frame["absoluteRenderBounds"]["width"])
    frame_height = int(frame["absoluteRenderBounds"]["height"])
    app.geometry(f"{frame_width}x{frame_height}")
    f.write(f'app.geometry("{frame_width}x{frame_height}")')
    f.write("\n")

    bg_color = frame.get("backgroundColor", {"r": 1, "g": 1, "b": 1})
    bg_hex = "#%02x%02x%02x" % (int(bg_color["r"] * 255), 
                                int(bg_color["g"] * 255), 
                                int(bg_color["b"] * 255))
    f.write(f'app.config(bg="{bg_hex}")')
    f.write("\n")
    f.write("\n")

    canvas = Canvas(app, width=frame_width, height=frame_height, bg=bg_hex, highlightthickness=0)
    f.write(f"canvas = Canvas(app, width={frame_width}, height={frame_height}, bg='{bg_hex}', highlightthickness=0)")
    f.write("\n")
    f.write("canvas.pack(fill='both', expand=True)")
    f.write("\n")
    f.write("\n")
    canvas.pack(fill="both", expand=True)
    image_refs = []

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
            alignment_map = {"LEFT": "w", "CENTER": "center", "RIGHT": "e"}
            text_anchor = alignment_map.get(element["style"].get("textAlignHorizontal"), "w")

            canvas.create_text(x, y, anchor=text_anchor, text=text_content, fill=text_hex, font=(font_family, font_size * -1))

            f.write(f'canvas.create_text({x}, {y}, anchor="{text_anchor}", text="{text_content}", fill="{text_hex}", font=("{font_family}", {font_size * -1}))')
            f.write("\n")
            f.write("\n")

        elif element["name"].lower() == "button":
            f.write("def change_button_color(event, color):")
            f.write("\n")
            f.write('    canvas.itemconfig("current", fill=color)')
            f.write("\n")
            f.write("\n")
            def change_button_color(event, color):
                canvas.itemconfig("current", fill=color)
            button_shape = None
            button_text = None
            

            # البحث عن الشكل والنص داخل الزر
            for child in element["children"]:
                if child["type"] == "TEXT":
                    button_text = child.get("characters", "Button")
                elif child["type"] in ["RECTANGLE", "ELLIPSE", "POLYGON", "STAR", "LINE", "ARROW"]:
                    button_shape = child

            if button_shape:
                x = abs(int(button_shape["absoluteBoundingBox"]["x"]))
                y = abs(int(button_shape["absoluteBoundingBox"]["y"]))
                width = int(button_shape["absoluteBoundingBox"]["width"])
                height = int(button_shape["absoluteBoundingBox"]["height"])
                print("yes")

                fill_color = "#FFFFFF"
                if "fills" in button_shape and button_shape["fills"]:
                    shape_color = button_shape["fills"][0].get("color", {"r": 1, "g": 1, "b": 1})
                    fill_color = "#%02x%02x%02x" % (int(shape_color["r"] * 255),
                                                    int(shape_color["g"] * 255),
                                                    int(shape_color["b"] * 255))

                # إنشاء الزر داخل `Canvas`
                if button_shape["type"] == "RECTANGLE":
                    button_id = canvas.create_rectangle(x, y, x + width, y + height, fill=fill_color, outline="black", tags="button")
                    f.write(f"""
button_id = canvas.create_rectangle({x}, {y}, {x + width}, {y + height}, fill='{fill_color}', outline="black", tags="button")
""")
                    f.write("\n")
                    f.write("\n")
                elif button_shape["type"] == "ELLIPSE":
                    button_id = canvas.create_oval(x, y, x + width, y + height, fill=fill_color, outline="black", tags="button")
                    f.write(f"""button_id = canvas.create_oval({x}, {y}, {x + width}, {y + height}, fill='{fill_color}', outline="black", tags="button")""")
                    f.write("\n")
                    f.write("\n")
                elif button_shape["type"] == "POLYGON":
                    button_id = canvas.create_polygon([
                        (x + width * 0.5, y),
                        (x + width, y + height * 0.4),
                        (x + width * 0.75, y + height),
                        (x + width * 0.25, y + height),
                        (x, y + height * 0.4),
                    ], fill=fill_color, outline="black", tags="button")
                
                # إضافة النص
                if button_text:
                    text_id = canvas.create_text(x + width // 2, y + height // 2, text=button_text, fill="black", font=("Arial", 12), anchor="center", tags="button")
                    f.write(f"""
text_id = canvas.create_text({x + width // 2}, {y + height // 2}, text="{button_text}", fill="black", font=("Arial", 12), anchor="center", tags="button")""")
                f.write("\n")
                f.write("\n")
            canvas.tag_bind("button", "<Enter>", lambda event:change_button_color(event, "#87CEEB"))
            canvas.tag_bind(f"'button', '<Leave>', lambda event:change_button_color(event, '{fill_color}'")
            f.write(f"""canvas.tag_bind("button", "<Enter>", lambda event:change_button_color(event, "#87CEEB"))
canvas.tag_bind("button", "<Leave>", lambda event:change_button_color(event, "{fill_color}"))""")
            f.write("\n")
            f.write("\n")


        elif element["name"].lower() == "entry":
            text_color = element["fills"][0]["color"]
            text_hex = "#%02x%02x%02x" % (int(text_color["r"] * 255),
                                          int(text_color["g"] * 255),
                                          int(text_color["b"] * 255))
            entry = Entry(app, bg=text_hex)
            canvas.create_window(x, y, anchor="nw", window=entry, width=width, height=height)
            f.write(f"entry = Entry(app, bg='{text_hex}')")
            f.write("\n")
            f.write(f"""canvas.create_window({x}, {y}, anchor="nw", window=entry, width={width}, height={height})""")
            f.write("\n")
            f.write("\n")

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

            image = Image.open(image_path)
            image = image.resize((width, height))
            photo = ImageTk.PhotoImage(image)
            f.write(f"""image = Image.open(r'{image_path}')
image = image.resize(({width}, {height}))
photo = ImageTk.PhotoImage(image)""")
            f.write("\n")
            image_refs.append(photo)
            f.write("image_refs.append(photo)")
            f.write("\n")
            print(photo)
            canvas.create_image(x, y, anchor="nw", image=photo)
            f.write(f"""
canvas.create_image({x}, {y}, anchor="nw", image=photo)""")
            f.write("\n")
            f.write("\n")

        elif element["type"] in ["RECTANGLE", "ELLIPSE", "VECTOR"]:
            x = abs(int(element["absoluteBoundingBox"]["x"]))
            y = abs(int(element["absoluteBoundingBox"]["y"]))
            width = int(element["absoluteBoundingBox"]["width"])
            height = int(element["absoluteBoundingBox"]["height"])

            fill_color = "#D9D9D9"
            if "fills" in element and element["fills"]:
                shape_color = element["fills"][0].get("color", {"r": 0.85, "g": 0.85, "b": 0.85})
                fill_color = "#%02x%02x%02x" % (int(shape_color["r"] * 255),
                                                int(shape_color["g"] * 255),
                                                int(shape_color["b"] * 255))

            if element["type"] == "RECTANGLE":
                canvas.create_rectangle(x, y, x + width, y + height, fill=fill_color, outline="black")
                f.write(f"canvas.create_rectangle({x}, {y}, {x + width}, {y + height}, fill='{fill_color}', outline='black')")
                f.write("\n")
                f.write("\n")

            elif element["type"] == "ELLIPSE":
                canvas.create_oval(x, y, x + width, y + height, fill=fill_color, outline="black")
                f.write(f"""
canvas.create_oval({x}, {y}, {x + width}, {y + height}, fill='{fill_color}', outline='black')""")
                f.write("\n")
                f.write("\n")

                canvas.create_polygon([
                    (x + width * 0.5, y),
                    (x + width, y + height * 0.4),
                    (x + width * 0.75, y + height),
                    (x + width * 0.25, y + height),
                    (x, y + height * 0.4),
                ], fill=fill_color, outline="black")
                f.write(f"canvas.create_polygon([({x + width * 0.5}, {y}), ({x + width}, {y + height * 0.4}), ({x + width * 0.75}, {y + height}), ({x + width * 0.25}, {y + height}), ({x}, {y + height * 0.4})], fill='{fill_color}', outline='black')")
                f.write("\n")
                f.write("\n")

            elif element["type"] == "VECTOR":
                if "absoluteRenderBounds" in element:
                    x = abs(int(element["absoluteRenderBounds"]["x"]))
                    y = abs(int(element["absoluteRenderBounds"]["y"]))
                    width = int(element["absoluteRenderBounds"]["width"])
                    height = int(element["absoluteRenderBounds"]["height"])

                def detect_arrow_position(data):
                    bbox = data["absoluteBoundingBox"]
                    rotation_radians = data.get("rotation", 0)
                    rotation_degrees = math.degrees(rotation_radians)

                    start_x, start_y = bbox["x"], bbox["y"]
                    end_x, end_y = start_x + bbox["width"], start_y + bbox["height"]

                    if -10 <= rotation_degrees <= 10:  
                        return "last" if start_x < end_x else "first"
                    elif 170 <= abs(rotation_degrees) <= 190:  
                        return "first" if start_x < end_x else "last"
                    elif 80 <= rotation_degrees <= 100:  
                        return "last" if start_y < end_y else "first"
                    elif -100 <= rotation_degrees <= -80:  
                        return "first" if start_y < end_y else "last"
                    elif 30 <= rotation_degrees <= 60:  
                        return "last"
                    elif -60 <= rotation_degrees <= -30:  
                        return "last"
                    elif 120 <= rotation_degrees <= 150: 
                        return "first"
                    elif -150 <= rotation_degrees <= -120:
                        return "first"
                    else:
                        return "last" 

                arrow_position = detect_arrow_position(element)

                canvas.create_line(x, y, x + width, y + height, fill="black", arrow=arrow_position, width=2)
                f.write(f"""
canvas.create_line({x}, {y}, {x + width}, {y + height}, fill='black', arrow='{arrow_position}', width=2)""")
                f.write("\n")
                f.write("\n")
    f.write("app.resizable(0,0)")
    f.write("\n")
    f.write("app.mainloop()")
    f.close()
    app.mainloop()