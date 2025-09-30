import json
from tk_writer import write
import os

def color_to_hex(color):
    r = int(color.get('r', 1) * 255)
    g = int(color.get('g', 1) * 255)
    b = int(color.get('b', 1) * 255)
    return f'#{r:02x}{g:02x}{b:02x}'

def generate_tk(json_path, output_py):
    if os.path.exists(output_py):
        os.remove(output_py)
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    write('from tkinter import *\n', output_py)
    write('root = Tk()\n', output_py)
    
    counters = {'label': 0, 'button': 0, 'entry': 0, 'frame': 0}
    def get_var(name):
        counters[name] += 1
        return f'{name}{counters[name]}'
    
    def handle_element(element, parent_name, parent_bbox=None):
        etype = element.get('type', '')
        ename = element.get('name', '').lower()
        bbox = element.get('absoluteBoundingBox')
        if not bbox:
            return
        px = parent_bbox['x'] if parent_bbox else 0
        py = parent_bbox['y'] if parent_bbox else 0
        x = int(bbox['x'] - px)
        y = int(bbox['y'] - py)
        width = int(bbox['width'])
        height = int(bbox['height'])
        
        if etype == 'TEXT' or ename == 'text':
            var = get_var('label')
            text = element.get('characters', '')
            font_size = int(element.get('style', {}).get('fontSize', 12))
            text_color = color_to_hex(element.get('fills', [{}])[0].get('color', {'r':0, 'g':0, 'b':0}))
            write(f'{var} = Label({parent_name}, text="{text}", font=("Arial", {font_size}), fg="{text_color}")\n', output_py)
            write(f'{var}.place(x={x}, y={y}, width={width}, height={height})\n', output_py)
        elif ename == 'button' or etype == 'BUTTON':
            var = get_var('button')
            btn_text = 'Button'
            for child in element.get('children', []):
                if child['type'] == 'TEXT':
                    btn_text = child.get('characters', 'Button')
            write(f'{var} = Button({parent_name}, text="{btn_text}")\n', output_py)
            write(f'{var}.place(x={x}, y={y}, width={width}, height={height})\n', output_py)
        elif ename == 'entry' or etype == 'ENTRY':
            var = get_var('entry')
            write(f'{var} = Entry({parent_name})\n', output_py)
            write(f'{var}.place(x={x}, y={y}, width={width}, height={height})\n', output_py)
        elif etype == 'FRAME' or ename == 'frame':
            var = get_var('frame')
            write(f'{var} = Frame({parent_name}, bg="{color_to_hex(element.get("backgroundColor", {"r":1,"g":1,"b":1}))}")\n', output_py)
            write(f'{var}.place(x={x}, y={y}, width={width}, height={height})\n', output_py)
            for child in element.get('children', []):
                handle_element(child, var, bbox)
        elif etype == 'GROUP' or ename == 'group':
            for child in element.get('children', []):
                handle_element(child, parent_name, parent_bbox)
    
    doc = data['document']
    page = doc['children'][0]
    for element in page['children']:
        if element['type'] == 'FRAME':
            handle_element(element, 'root', element['absoluteBoundingBox'])
    write('root.mainloop()\n', output_py)
    write('close()', output_py)

# Example usage:
# generate_tk('build/json.json', 'build/tk_generated.py') 