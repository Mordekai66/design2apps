import os
import math
import random
import requests
import json
from Writers import tk_writer

file_path = ""

# Create a function to add text to the canvas
def create_text_element(element, widget):
    # Getting text element info
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))

    text_content = element.get("characters", "")
    font_size = int(element["style"].get("fontSize", 12))
    font_family = element["style"].get("fontFamily", "Arial")
    text_color = element["fills"][0]["color"]
    # Convert text_color to hex color code
    text_hex = "#%02x%02x%02x" % (int(text_color["r"] * 255),
                                int(text_color["g"] * 255),
                                int(text_color["b"] * 255))
    # Determine anchor of element
    alignment_map_x = {"LEFT": "w", "CENTER": "", "RIGHT": "e"}
    alignment_map_y = {"TOP": "n", "CENTER": "", "BOTTOM": "s"}

    text_anchor_x = alignment_map_x.get(element["style"].get("textAlignHorizontal", "LEFT"), "w")
    text_anchor_y = alignment_map_y.get(element["style"].get("textAlignVertical", "TOP"), "n")
    text_anchor_final = text_anchor_y + text_anchor_x
    print(f'widget: {widget}, type: {type(widget)}')

    # Check if this canvas is frame or window canvas
    if str(widget).startswith("frame_"):
        # This element is inside a Frame, so (x, y) coordinates
        # should be adjusted relative to the frame, not the main canvas/window
        tk_writer.write("\n\n", file_path)
        tk_writer.write(f"""{widget.replace(":", "_")}.create_text({x} - {widget.replace(":","_")}.winfo_x(), {y} - {widget.replace(":","_")}.winfo_y(), anchor='{text_anchor_final}', text='{text_content}', fill='{text_hex}', font=('{font_family}', {font_size * -1}))""", file_path)
        tk_writer.write("\n\n", file_path)
    else:
        # This element is on the main window canvas,
        # so no need to convert (x, y) – they are already correct
        tk_writer.write(f'''{widget}.create_text({x},{y},anchor="{text_anchor_final}", text="{text_content}", fill="{text_hex}", font=("{font_family}", {font_size * -1}))''', file_path)
        tk_writer.write("\n\n", file_path)

def create_button_element(element, widget):
    # Get button element info
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])

    # Button shape and text are initialized with default values
    button_shape = "RECTANGLE"
    button_text = None

    for child in element["children"]:
        # Determine who is text and button shape
        if child["type"] == "TEXT":
            button_text = child.get("characters", "Button")
        elif child["type"] in ["RECTANGLE", "ELLIPSE"]:
            button_shape = child

    if button_shape:
        # Get button_shape coordinates
        x = abs(int(button_shape["absoluteBoundingBox"]["x"]))
        y = abs(int(button_shape["absoluteBoundingBox"]["y"]))
        width = int(button_shape["absoluteBoundingBox"]["width"])
        height = int(button_shape["absoluteBoundingBox"]["height"])

        fill_color = "#FFFFFF"
        if "fills" in button_shape and button_shape["fills"]:
            shape_color = button_shape["fills"][0].get("color", {"r": 1, "g": 1, "b": 1})
            # Convert shape color to hex color code
            fill_color = "#%02x%02x%02x" % (int(shape_color["r"] * 255),
                                            int(shape_color["g"] * 255),
                                            int(shape_color["b"] * 255))
            if button_shape["type"] == "RECTANGLE":  
                
                if str(widget).startswith("frame_"):
                    # This element is inside a Frame, so (x, y) coordinates
                    # should be adjusted relative to the frame, not the main canvas/window
                    tk_writer.write(f"""
{widget.replace(":","_")}.create_rectangle({x} - {widget.replace(":","_")}.winfo_x(), {y} - {widget.replace(":","_")}.winfo_y(), ({x} - {widget.replace(":","_")}.winfo_x()) + {width}, ({y} - {widget.replace(":","_")}.winfo_y()) + {height}, fill='{fill_color}', outline="black", tags="button")""", file_path)
                    tk_writer.write("\n\n", file_path)
                else:
                    # This element is on the main window canvas,
                    # so no need to convert (x, y) – they are already correct
                    tk_writer.write(f"""
{widget}.create_rectangle({x}, {y}, {x + width}, {y + height}, fill='{fill_color}', outline="black", tags="button")""", file_path)
                    tk_writer.write("\n\n", file_path)


            elif button_shape["type"] == "ELLIPSE":
                if str(widget).startswith("frame_"):
                    # This element is inside a Frame, so (x, y) coordinates
                    # should be adjusted relative to the frame, not the main canvas/window
                    tk_writer.write(f"""
{widget.replace(":","_")}.create_oval({x} - {widget.replace(":","_")}.winfo_x() , {y} - {widget.replace(":","_")}.winfo_y(), ({x} - {widget.replace(":","_")}.winfo_x()) + {width}, ({y} - {widget.replace(":","_")}.winfo_y()) + {height}, fill='{fill_color}', outline="black", tags="button")""", file_path)
                    tk_writer.write("\n\n", file_path)
                else:
                    # This element is on the main window canvas,
                    # so no need to convert (x, y) – they are already correct
                    tk_writer.write(f"""{widget}.create_oval({x}, {y}, {x + width}, {y + height}, fill='{fill_color}', outline="black", tags="button")""", file_path)
                    tk_writer.write("\n\n", file_path)

            if button_text:
                if str(widget).startswith("frame_"):
                    # This element is inside a Frame, so (x, y) coordinates
                    # should be adjusted relative to the frame, not the main canvas/window
                    tk_writer.write(f"""
{widget.replace(":","_")}.create_text({x + width // 2} - {widget.replace(":","_")}.winfo_x(), {y + height // 2} - {widget.replace(":","_")}.winfo_y(), text="{button_text}", fill="black", font=("Arial", 12), anchor="center", tags="button")""", file_path)
                    tk_writer.write("\n\n", file_path)
                else:
                    # This element is on the main window canvas,
                    # so no need to convert (x, y) – they are already correct
                    tk_writer.write(f"""{widget}.create_text({x + width // 2}, {y + height // 2}, text="{button_text}", fill="black", font=("Arial", 12), anchor="center", tags="button")""", file_path)
                    tk_writer.write("\n\n", file_path)

def create_entry_element(element, widget):
    # Get entry element info
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    text_color = element["fills"][0]["color"]
    text_hex = "#%02x%02x%02x" % (int(text_color["r"] * 255),
                                    int(text_color["g"] * 255),
                                    int(text_color["b"] * 255))
    alignment_map_x = {"LEFT": "w", "CENTER": "", "RIGHT": "e"}
    alignment_map_y = {"TOP": "n", "CENTER": "", "BOTTOM": "s"}
    # Get anchor of element
    text_anchor_x = alignment_map_x.get(element["constraints"].get("horizontal"), "w")
    text_anchor_y = alignment_map_y.get(element["constraints"].get("vertical"), "n")

    text_anchor_final = text_anchor_y + text_anchor_x

    tk_writer.write(f"entry = Entry(window, bg='{text_hex}')", file_path)
    tk_writer.write("\n", file_path)
    tk_writer.write("entry.insert(0, 'Enter text here')", file_path)
    tk_writer.write("\n", file_path)
    if str(widget).startswith("frame_"):
            # This element is inside a Frame, so (x, y) coordinates
            # should be adjusted relative to the frame, not the main canvas/window
        tk_writer.write(f"""{widget.replace(":","_")}.create_window({x} - {widget.replace(":","_")}.winfo_x(),{y} - {widget.replace(":","_")}.winfo_y(), anchor='{text_anchor_final}', window=entry, width={width}, height={height})""", file_path)
        tk_writer.write("\n\n", file_path)

    else:
        # This element is on the main window canvas,
        # so no need to convert (x, y) – they are already correct
        tk_writer.write(f"""{widget}.create_window({x}, {y}, anchor='{text_anchor_final}', window=entry, width={width}, height={height})""", file_path)
        tk_writer.write("\n\n", file_path)


def create_image_element(element, output_path, file_id_figma, token_access, widget):
    # Getting image info
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    node_id = element["id"]
    file_id = file_id_figma
    access_token = token_access

    # Get image from figma API
    url = f"https://api.figma.com/v1/images/{file_id}?ids={node_id}"
    headers = {"X-Figma-Token": access_token}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code}, Response: {response.text}")

    image_data = response.json()
    image_url = image_data["images"].get(node_id, "")

    # Store data od image
    img_data = requests.get(image_url).content


    if not os.path.exists(os.path.join(f"{os.path.dirname(output_path)}",'image')):
        os.mkdir(os.path.join(f"{os.path.dirname(output_path)}",'image'))

    # Write image data in PNG file
    image_path = os.path.join(f"{os.path.dirname(output_path)}","image",f"{random.randint(1,200)}.png")
    
    with open(image_path, "wb") as s:
        s.write(img_data)
    
    # Determine anchor of element
    alignment_map_x = {"LEFT": "w", "CENTER": "", "RIGHT": "e"}
    alignment_map_y = {"TOP": "n", "CENTER": "", "BOTTOM": "s"}
    text_anchor_x = alignment_map_x.get(element["constraints"].get("horizontal"), "w")
    text_anchor_y = alignment_map_y.get(element["constraints"].get("vertical"), "n")

    text_anchor_final = text_anchor_y + text_anchor_x

    tk_writer.write(f"""image = Image.open(r'{image_path}')
image = image.resize(({width}, {height}))
photo = ImageTk.PhotoImage(image)""", file_path)
    tk_writer.write("\n", file_path)
    tk_writer.write("image_refs.append(photo)", file_path)
    tk_writer.write("\n", file_path)

    if str(widget).startswith("frame_"):
        # This element is inside a Frame, so (x, y) coordinates
        # should be adjusted relative to the frame, not the main canvas/window
        tk_writer.write(f"""
{widget.replace(":","_")}.create_image({x} - {widget.replace(":","_")}.winfo_x(), {y} - {widget.replace(":","_")}.winfo_y(), anchor='{text_anchor_final}', image=photo)""", file_path)
        tk_writer.write("\n\n", file_path)

    else:
        # This element is on the main window canvas,
        # so no need to convert (x, y) – they are already correct
        tk_writer.write(f"""
{widget}.create_image({x}, {y}, anchor='{text_anchor_final}', image=photo)""", file_path)
        tk_writer.write("\n\n", file_path)

def create_rectangle(element, widget):
    # Getting rectangle element info
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
        
    if str(widget).startswith("frame_"):
        # This element is inside a Frame, so (x, y) coordinates
        # should be adjusted relative to the frame, not the main canvas/window
        tk_writer.write(f"{widget.replace(':','_')}.create_rectangle({x} - {widget.replace(":","_")}.winfo_x(), {y} - {widget.replace(":","_")}.winfo_y(), ({x} - {widget.replace(":","_")}.winfo_x()) + {width}, ({y} - {widget.replace(":","_")}.winfo_y()) + {height}, fill='{fill_color}', outline='black')", file_path)
        tk_writer.write("\n\n", file_path)
    else:
        # This element is on the main window canvas,
        # so no need to convert (x, y) – they are already correct
        tk_writer.write(f"{widget}.create_rectangle({x}, {y}, {x + width}, {y + height}, fill='{fill_color}', outline='black')", file_path)
        tk_writer.write("\n\n", file_path)

def create_ellipse(element, widget):
    # Getting ellipse element info
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
            
    if str(widget).startswith("frame_"):
        # This element is inside a Frame, so (x, y) coordinates
        # should be adjusted relative to the frame, not the main canvas/window
        tk_writer.write(f"{widget.replace(':','_')}.create_oval({x} - {widget.replace(":","_")}.winfo_x(), {y} - {widget.replace(":","_")}.winfo_y(), ({x} - {widget.replace(":","_")}.winfo_x()) + {width}, ({y} - {widget.replace(":","_")}.winfo_y()) + {height}, fill='{fill_color}', outline='black')", file_path)
        tk_writer.write("\n\n", file_path)
    else:
        # This element is on the main window canvas,
        # so no need to convert (x, y) – they are already correct
        tk_writer.write(f"{widget}.create_oval({x}, {y}, {x + width}, {y + height}, fill='{fill_color}', outline='black')", file_path)
        tk_writer.write("\n\n", file_path)

def create_arrow(element, widget):
    # Getting arrow element info
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
        # This element is inside a Frame, so (x, y) coordinates
        # should be adjusted relative to the frame, not the main canvas/window
        tk_writer.write(f"""
{widget.replace(":","_")}.create_line({x} - {widget.replace(":","_")}.winfo_x(), {y} - {widget.replace(":","_")}.winfo_y(), ({x} - {widget.replace(":","_")}.winfo_x()) + {width}, ({y} - {widget.replace(":","_")}.winfo_y()) + {height}, fill='black', arrow='{arrow_position}', width=2)""", file_path)
        tk_writer.write("\n\n", file_path)

    else:
        # This element is on the main window canvas,
        # so no need to convert (x, y) – they are already correct
        tk_writer.write(f"""
{widget}.create_line({x}, {y}, {x + width}, {y + height}, fill='black', arrow='{arrow_position}', width=2)""", file_path)
        tk_writer.write("\n\n", file_path)

def create_line(element, widget):
    # Getting line element info
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])

    if str(widget).startswith("frame_"):
        # This element is inside a Frame, so (x, y) coordinates
        # should be adjusted relative to the frame, not the main canvas/window
        tk_writer.write(f"""
{widget.replace(":","_")}.create_line({x} - {widget.replace(":","_")}.winfo_x(), {y} - {widget.replace(":","_")}.winfo_y(), ({x} - {widget.replace(":","_")}.winfo_x()) + {width}, ({y} - {widget.replace(":","_")}.winfo_y()) + {height}, fill='black', width=2)""", file_path)
        tk_writer.write("\n\n", file_path)

    else:
        # This element is on the main window canvas,
        # so no need to convert (x, y) – they are already correct
        tk_writer.write(f"""
{widget}.create_line({x}, {y}, {x + width}, {y + height}, fill='black', width=2)""", file_path)
        tk_writer.write("\n\n", file_path)


def create_frame(element, widget, file_id_figma, token_access):
    # Dict was created to store incoming frames,
    # so I can reference them later as variables in the new pyth file
    frames = {}

    # Getting frame element info
    frame_id = element["id"]
    frame_name = f"Frame_{frame_id}"
    frames[frame_name] = element

    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    bg_color = element.get("backgroundColor", {"r": 1, "g": 1, "b": 1})
    bg_hex = "#%02x%02x%02x" % (int(bg_color["r"] * 255),
                                    int(bg_color["g"] * 255),
                                    int(bg_color["b"] * 255))

    tk_writer.write(f"""
frame_{frame_id.replace(":","_")} = Canvas(window, width={width}, height={height}, bg='{bg_hex}', highlightthickness=0)
{widget.replace(":","_")}.create_window({x}, {y}, anchor='nw', window=frame_{frame_id.replace(":","_")})
""", file_path)
    tk_writer.write(f"{widget.replace(":","_")}.update()", file_path)
    tk_writer.write("\n\n", file_path)

    for frame_element in element["children"]:
            if frame_element["type"] == "TEXT" or frame_element["name"].lower() == "text":
                create_text_element(frame_element, 'frame_' + frame_id)

            elif frame_element["name"].lower() == "button":
                create_button_element(frame_element, 'frame_' + frame_id)

            elif frame_element["name"].lower() == "entry":
                create_entry_element(frame_element, 'frame_' + frame_id)

            elif frame_element["name"].lower() == "image":
                create_image_element(frame_element, file_path, file_id_figma, token_access, 'frame_' + frame_id)

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


    return frames


def transform_json_to_tk(data, output_path, file_id_figma, token_access):
    global file_path
    """ This function reads JSON data from Figma and loops through each element in the frame, converting them into Canvas elements in a new Python file named TK.py"""

    # Store parameters in variables to use them into another func
    file_id_figma = file_id_figma
    token_access = token_access
    # Check if the output file path exists, delete it if it does, otherwise create it

    file_path = os.path.join(output_path +"\\build" + "\\TK.py")

    if os.path.exists(file_path):
        os.remove(file_path)

    print(f"Creating {file_path} file")

    # Importing required libraries
    tk_writer.write("from tkinter import *", file_path)
    tk_writer.write("\n\n", file_path)
    tk_writer.write("from PIL import Image, ImageTk", file_path)
    tk_writer.write("\n\n", file_path)
    tk_writer.write('image_refs = []', file_path)
    tk_writer.write("\n\n", file_path)

    document = data["document"]
    page = document["children"][0]
    frame = page["children"][0]

    tk_writer.write("window = Tk()", file_path)
    tk_writer.write("\n", file_path)
    tk_writer.write(f'window.title("{page["name"]}")', file_path)
    tk_writer.write("\n", file_path)

    frame_width = int(frame["absoluteRenderBounds"]["width"])
    frame_height = int(frame["absoluteRenderBounds"]["height"])
    tk_writer.write(f'window.geometry("{frame_width}x{frame_height}")', file_path)
    tk_writer.write("\n", file_path)

    bg_color = frame.get("backgroundColor", {"r": 1, "g": 1, "b": 1})
    bg_hex = "#%02x%02x%02x" % (int(bg_color["r"] * 255), 
                                int(bg_color["g"] * 255), 
                                int(bg_color["b"] * 255))
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

        print(f'{element["name"]}, {element["type"]} was created in  Tkinter')

        if element["type"] == "TEXT" or element["name"].lower() == "text":
            create_text_element(element, 'canvas')


        elif element["name"].lower() == "button":
            create_button_element(element, 'canvas')


        elif element["name"].lower() == "entry":
            create_entry_element(element, 'canvas')

        elif element["name"].lower() == "image":
            create_image_element(element, output_path, file_id_figma, token_access, 'canvas')


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

    tk_writer.write("window.resizable(0,0)", file_path)
    tk_writer.write("\n", file_path)
    tk_writer.write("window.mainloop()", file_path)
    tk_writer.write("close()", file_path)