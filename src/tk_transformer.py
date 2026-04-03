import os
import math
import requests
import json
import writer as tk_writer
import utils

file_path = ""

def create_text(element, widget):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    chars = element.get("characters", "")
    font_size = int(element["style"].get("fontSize", 12))
    font_family = element["style"].get("fontFamily", "Arial")
    text_hex = utils.rgb_to_hex(element["fills"][0]["color"])
    alignment_map_x = {"LEFT": "w", "CENTER": "", "RIGHT": "e"}
    alignment_map_y = {"TOP": "n", "CENTER": "", "BOTTOM": "s"}
    text_anchor_x = alignment_map_x.get(element["style"].get("textAlignHorizontal", "LEFT"), "w")
    text_anchor_y = alignment_map_y.get(element["style"].get("textAlignVertical", "TOP"), "n")
    text_anchor_final = text_anchor_y + text_anchor_x

    if str(widget).startswith("frame_"):
        tk_writer.write("\n\n", file_path)
        tk_writer.write(f"""{widget}.create_text({x} - {widget}.winfo_x(), {y} - {widget}.winfo_y(), anchor='{text_anchor_final}', text='{chars}', fill='{text_hex}', font=('{font_family}', {font_size * -1}))""", file_path)
        tk_writer.write("\n\n", file_path)
    else:
        tk_writer.write(f'''{widget}.create_text({x},{y},anchor="{text_anchor_final}", text="{chars}", fill="{text_hex}", font=("{font_family}", {font_size * -1}))''', file_path)
        tk_writer.write("\n\n", file_path)

def create_button(element, widget):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    button_shape = "RECTANGLE" # Default shape of the button.
    button_text = None

    for child in element["children"]:
        # Determine who is text and button shape
        if child["type"] == "TEXT":
            button_text = child.get("characters", "Button")
        elif child["type"] in ["RECTANGLE", "ELLIPSE"]:
            button_shape = child

    x = abs(int(button_shape["absoluteBoundingBox"]["x"]))
    y = abs(int(button_shape["absoluteBoundingBox"]["y"]))
    width = int(button_shape["absoluteBoundingBox"]["width"])
    height = int(button_shape["absoluteBoundingBox"]["height"])
    fill_color = "#FFFFFF"
    if "fills" in button_shape and button_shape["fills"]:
        fill_color = utils.rgb_to_hex(button_shape["fills"][0].get("color", {"r": 1, "g": 1, "b": 1}))
        
    if button_shape["type"] == "RECTANGLE":  
        if str(widget).startswith("frame_"):
            tk_writer.write(f"""{widget}.create_rectangle({x} - {widget}.winfo_x(), {y} - {widget}.winfo_y(), ({x} - {widget}.winfo_x()) + {width}, ({y} - {widget}.winfo_y()) + {height}, fill='{fill_color}', outline="black", tags="button")""", file_path)
            tk_writer.write("\n\n", file_path)
        else:
            tk_writer.write(f"""{widget}.create_rectangle({x}, {y}, {x + width}, {y + height}, fill='{fill_color}', outline="black", tags="button")""", file_path)
            tk_writer.write("\n\n", file_path)
    elif button_shape["type"] == "ELLIPSE":
        if str(widget).startswith("frame_"):
            tk_writer.write(f"""{widget}.create_oval({x} - {widget}.winfo_x() , {y} - {widget}.winfo_y(), ({x} - {widget}.winfo_x()) + {width}, ({y} - {widget}.winfo_y()) + {height}, fill='{fill_color}', outline="black", tags="button")""", file_path)
            tk_writer.write("\n\n", file_path)
        else:
            tk_writer.write(f"""{widget}.create_oval({x}, {y}, {x + width}, {y + height}, fill='{fill_color}', outline="black", tags="button")""", file_path)
            tk_writer.write("\n\n", file_path)

    if button_text:
        if str(widget).startswith("frame_"):
            tk_writer.write(f"""{widget}.create_text({x + width // 2} - {widget}.winfo_x(), {y + height // 2} - {widget}.winfo_y(), text="{button_text}", fill="black", font=("Arial", 12), anchor="center", tags="button")""", file_path)
            tk_writer.write("\n\n", file_path)
        else:
            tk_writer.write(f"""{widget}.create_text({x + width // 2}, {y + height // 2}, text="{button_text}", fill="black", font=("Arial", 12), anchor="center", tags="button")""", file_path)
            tk_writer.write("\n\n", file_path)

def create_entry(element, widget):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    text_hex = utils.rgb_to_hex(element["fills"][0]["color"])
    alignment_map_x = {"LEFT": "w", "CENTER": "", "RIGHT": "e"}
    alignment_map_y = {"TOP": "n", "CENTER": "", "BOTTOM": "s"}
    text_anchor_x = alignment_map_x.get(element["constraints"].get("horizontal"), "w")
    text_anchor_y = alignment_map_y.get(element["constraints"].get("vertical"), "n")
    text_anchor_final = text_anchor_y + text_anchor_x

    tk_writer.write(f"entry = Entry(window, bg='{text_hex}')", file_path)
    tk_writer.write("\n", file_path)
    tk_writer.write("entry.insert(0, 'Enter text here')", file_path)
    tk_writer.write("\n", file_path)
    
    if str(widget).startswith("frame_"):
        tk_writer.write(f"""{widget}.create_window({x} - {widget}.winfo_x(),{y} - {widget}.winfo_y(), anchor='{text_anchor_final}', window=entry, width={width}, height={height})""", file_path)
        tk_writer.write("\n\n", file_path)
    else:
        tk_writer.write(f"""{widget}.create_window({x}, {y}, anchor='{text_anchor_final}', window=entry, width={width}, height={height})""", file_path)
        tk_writer.write("\n\n", file_path)

def create_image(element, output_path, file_id_figma, token_access, widget):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    node_id = element["id"]
    alignment_map_x = {"LEFT": "w", "CENTER": "", "RIGHT": "e"}
    alignment_map_y = {"TOP": "n", "CENTER": "", "BOTTOM": "s"}
    text_anchor_x = alignment_map_x.get(element["constraints"].get("horizontal"), "w")
    text_anchor_y = alignment_map_y.get(element["constraints"].get("vertical"), "n")
    text_anchor_final = text_anchor_y + text_anchor_x
    
    file_id = file_id_figma
    access_token = token_access
    url = f"https://api.figma.com/v1/images/{file_id}?ids={node_id}"
    headers = {"X-Figma-Token": access_token}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code}, Response: {response.text}")

    image_data = response.json()
    image_url = image_data["images"].get(node_id, "")
    img_data = requests.get(image_url).content

    if not os.path.exists(os.path.join(f"{os.path.dirname(output_path)}",'image')):
        os.mkdir(os.path.join(f"{os.path.dirname(output_path)}",'image'))
    image_path = os.path.join(f"{os.path.dirname(output_path)}","image",f"{node_id}.png")
    with open(image_path, "wb") as s:
        s.write(img_data)

    tk_writer.write("from PIL import Image, ImageTk", file_path)
    tk_writer.write("\n\n", file_path)
    tk_writer.write("image_refs = []", file_path)
    tk_writer.write("\n", file_path)
    tk_writer.write(f"""image = Image.open(r'{image_path}')
image = image.resize(({width}, {height}))
photo = ImageTk.PhotoImage(image)""", file_path)
    tk_writer.write("\n", file_path)
    tk_writer.write("image_refs.append(photo)", file_path)
    tk_writer.write("\n", file_path)

    if str(widget).startswith("frame_"):
        tk_writer.write(f"""{widget}.create_image({x} - {widget}.winfo_x(), {y} - {widget}.winfo_y(), anchor='{text_anchor_final}', image=photo)""", file_path)
        tk_writer.write("\n\n", file_path)
    else:
        tk_writer.write(f"""{widget}.create_image({x}, {y}, anchor='{text_anchor_final}', image=photo)""", file_path)
        tk_writer.write("\n\n", file_path)

def create_rectangle(element, widget):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    fill_color = "#D9D9D9"
    if "fills" in element and element["fills"]:
        fill_color = utils.rgb_to_hex(element["fills"][0].get("color", {"r": 0.85, "g": 0.85, "b": 0.85}))

    if str(widget).startswith("frame_"):
        tk_writer.write(f"{widget}.create_rectangle({x} - {widget}.winfo_x(), {y} - {widget}.winfo_y(), ({x} - {widget}.winfo_x()) + {width}, ({y} - {widget}.winfo_y()) + {height}, fill='{fill_color}', outline='black')", file_path)
        tk_writer.write("\n\n", file_path)
    else:
        tk_writer.write(f"{widget}.create_rectangle({x}, {y}, {x + width}, {y + height}, fill='{fill_color}', outline='black')", file_path)
        tk_writer.write("\n\n", file_path)

def create_ellipse(element, widget):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    fill_color = "#D9D9D9"
    if "fills" in element and element["fills"]:
            fill_color = utils.rgb_to_hex(element["fills"][0].get("color", {"r": 0.85, "g": 0.85, "b": 0.85}))

    if str(widget).startswith("frame_"):
        tk_writer.write(f"{widget}.create_oval({x} - {widget}.winfo_x(), {y} - {widget}.winfo_y(), ({x} - {widget}.winfo_x()) + {width}, ({y} - {widget}.winfo_y()) + {height}, fill='{fill_color}', outline='black')", file_path)
        tk_writer.write("\n\n", file_path)
    else:
        tk_writer.write(f"{widget}.create_oval({x}, {y}, {x + width}, {y + height}, fill='{fill_color}', outline='black')", file_path)
        tk_writer.write("\n\n", file_path)

def create_arrow(element, widget):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    def detect_arrow_position(data):
        bbox = data["absoluteBoundingBox"]
        rotation_radians = data.get("rotation", 0)
        rotation_degrees = math.degrees(rotation_radians)
        start_x, start_y = bbox["x"], bbox["y"]
        end_x = start_x + bbox["width"] * math.cos(rotation_radians)
        end_y = start_y - bbox["height"] * math.sin(rotation_radians)
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

    if str(widget).startswith("frame_"):
        tk_writer.write(f"""{widget}.create_line({x} - {widget}.winfo_x(), {y} - {widget}.winfo_y(), ({x} - {widget}.winfo_x()) + {width}, ({y} - {widget}.winfo_y()) + {height}, fill='black', arrow='{arrow_position}', width=2)""", file_path)
        tk_writer.write("\n\n", file_path)
    else:
        tk_writer.write(f"""{widget}.create_line({x}, {y}, {x + width}, {y + height}, fill='black', arrow='{arrow_position}', width=2)""", file_path)
        tk_writer.write("\n\n", file_path)

def create_line(element, widget):
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])

    if str(widget).startswith("frame_"):
        tk_writer.write(f"""{widget}.create_line({x} - {widget}.winfo_x(), {y} - {widget}.winfo_y(), ({x} - {widget}.winfo_x()) + {width}, ({y} - {widget}.winfo_y()) + {height}, fill='black', width=2)""", file_path)
        tk_writer.write("\n\n", file_path)
    else:
        tk_writer.write(f"""{widget}.create_line({x}, {y}, {x + width}, {y + height}, fill='black', width=2)""", file_path)
        tk_writer.write("\n\n", file_path)


def create_frame(element, widget, file_id_figma, token_access):
    frames = {}
    frame_id = element["id"].replace(":", "_")
    frames[frame_name] = f"frame_{frame_id}"

    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    bg_hex = utils.rgb_to_hex(element.get("backgroundColor", {"r": 1, "g": 1, "b": 1}))

    tk_writer.write(f"""frame_{frame_id} = Canvas(window, width={width}, height={height}, bg='{bg_hex}', highlightthickness=0)
{widget}.create_window({x}, {y}, anchor='nw', window=frame_{frame_id})
""", file_path)
    tk_writer.write(f"{widget}.update()", file_path)
    tk_writer.write("\n\n", file_path)

    for frame_element in element["children"]:
        if frame_element["type"] == "TEXT" or frame_element["name"].lower() == "text":
            create_text(frame_element, 'frame_' + frame_id)
        elif frame_element["name"].lower() == "button":
            create_button(frame_element, 'frame_' + frame_id)
        elif frame_element["name"].lower() == "entry":
            create_entry(frame_element, 'frame_' + frame_id)
        elif frame_element["name"].lower() == "image":
            create_image(frame_element, file_path, file_id_figma, token_access, 'frame_' + frame_id)
        elif frame_element["type"] == "RECTANGLE":
            create_rectangle(frame_element, 'frame_' + frame_id)
        elif frame_element["type"] == "ELLIPSE":
            create_ellipse(frame_element, 'frame_' + frame_id)
        elif frame_element["name"].lower() == "arrow":
            create_arrow(frame_element, 'frame_' + frame_id)
        elif frame_element["name"].lower() == "line":
            create_line(frame_element, 'frame_' + frame_id)
        elif frame_element["type"] == "FRAME":
            create_frame(frame_element, 'frame_' + frame_id, file_id_figma, token_access)

def transform_json_to_tk(data, output_path, file_id_figma, token_access):
    global file_path
    """ This function reads JSON data from Figma and loops through each element in the frame, converting them into Canvas elements in a new Python file named TK.py"""
    page = data["document"]["children"][0]
    frame = page["children"][0]
    frame_width = int(frame["absoluteRenderBounds"]["width"])
    frame_height = int(frame["absoluteRenderBounds"]["height"])
    bg_hex = utils.rgb_to_hex(frame.get("backgroundColor", {"r": 1, "g": 1, "b": 1}))
    file_id_figma = file_id_figma
    token_access = token_access
    
    file_path = os.path.join(output_path + "\\build" + "\\TK.py")
    if os.path.exists(file_path):
        os.remove(file_path)

    tk_writer.write("from tkinter import *", file_path)
    tk_writer.write("\n\n", file_path)
    tk_writer.write("\n\n", file_path)
    tk_writer.write("window = Tk()", file_path)
    tk_writer.write("\n", file_path)
    tk_writer.write(f'window.title("{page["name"]}")', file_path)
    tk_writer.write("\n", file_path)
    tk_writer.write(f'window.geometry("{frame_width}x{frame_height}")', file_path)
    tk_writer.write("\n", file_path)
    tk_writer.write(f'window.config(bg="{bg_hex}")', file_path)
    tk_writer.write("\n", file_path)
    tk_writer.write("\n", file_path)
    tk_writer.write(f"canvas = Canvas(window, width={frame_width}, height={frame_height}, bg='{bg_hex}', highlightthickness=0)", file_path)
    tk_writer.write("\n", file_path)
    tk_writer.write("canvas.pack(fill='both', expand=True)", file_path)
    tk_writer.write("\n", file_path)
    tk_writer.write("\n", file_path)

    for element in frame["children"]:
        """Looping through elements in the parent frame, extracting each one, and converting it into code"""
        if element["type"] == "TEXT" or element["name"].lower() == "text":
            create_text(element, 'canvas')
        elif element["name"].lower() == "button":
            create_button(element, 'canvas')
        elif element["name"].lower() == "entry":
            create_entry(element, 'canvas')
        elif element["name"].lower() == "image":
            create_image(element, output_path, file_id_figma, token_access, 'canvas')
        elif element["type"] == "RECTANGLE":
            create_rectangle(element, 'canvas')
        elif element["type"] == "ELLIPSE":
            create_ellipse(element, 'canvas')
        elif element["name"].lower() == "arrow":
            create_arrow(element, 'canvas')
        elif element["name"].lower() == "line":
            create_line(element, 'canvas')
        elif element["type"] == "FRAME":
            create_frame(element, "canvas", file_id_figma, token_access)
        print(f'{element["name"]}, {element["type"]} was created in  Tkinter')

    tk_writer.write("window.resizable(0,0)", file_path)
    tk_writer.write("\n", file_path)
    tk_writer.write("window.mainloop()", file_path)