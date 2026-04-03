import json
from pydoc import Doc
from this import d
import writer as cpp_writer
import os
import utils

file_path = ""
counters = {'label': 0, 'button': 0, 'entry': 0, 'frame': 0}
def get_var(name):
    counters[name] += 1
    return f'{name}{counters[name]}'

def create_text(element, parent, parent_bbox=None):
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
    var = get_var('label')
    text = element.get('characters', '')
    font_size = int(element.get('style', {}).get('fontSize', 12))
    color = utils.rgb_to_rgb_cpp(element.get('fills', [{}])[0].get('color', {'r':0, 'g':0, 'b':0}))
    cpp_writer.write(f'    QLabel* {var} = new QLabel({parent});\n', file_path)
    cpp_writer.write(f'    {var}->setText("{text}");\n', file_path)
    cpp_writer.write(f'    {var}->setGeometry({x}, {y}, {width}, {height});\n', file_path)
    cpp_writer.write(f'    {var}->setStyleSheet("color: {color}; font-size: {font_size}px;");\n', file_path)

def create_button(element, parent, parent_bbox=None):
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
    var = get_var('button')
    btn_text = 'Button'
    for child in element.get('children', []):
        if child['type'] == 'TEXT':
            btn_text = child.get('characters', 'Button')
    cpp_writer.write(f'    QPushButton* {var} = new QPushButton({parent});\n', file_path)
    cpp_writer.write(f'    {var}->setText("{btn_text}");\n', file_path)
    cpp_writer.write(f'    {var}->setGeometry({x}, {y}, {width}, {height});\n', file_path)

def create_entry(element, parent, parent_bbox=None):
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
    var = get_var('entry')
    cpp_writer.write(f'    QLineEdit* {var} = new QLineEdit({parent});\n', file_path)
    cpp_writer.write(f'    {var}->setGeometry({x}, {y}, {width}, {height});\n', file_path)

def create_frame(element, parent, parent_bbox=None):
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
    var = get_var('frame')
    color = utils.rgb_to_rgb_cpp(element.get('backgroundColor', {'r':1,'g':1,'b':1}))
    cpp_writer.write(f'    QWidget* {var} = new QWidget({parent});\n', file_path)
    cpp_writer.write(f'    {var}->setStyleSheet("background-color: {color};");\n', file_path)
    cpp_writer.write(f'    {var}->setGeometry({x}, {y}, {width}, {height});\n', file_path)

    for child in element.get('children', []):
        if child['type'] == 'TEXT' or child['name'].lower() == 'text':
            create_text(child, var)
        elif child['type'] == 'BUTTON':
            create_button(child, var)
        elif child['type'] == 'ENTRY':
            create_entry(child, var)
        elif child['type'] == 'FRAME':
            create_frame(child, var)

def transform_to_cpp(data, output_path, file_id_figma, token_access):
    global file_path
    file_path = os.path.join(output_path +"\\build" + "\\cpp.cpp")

    if os.path.exists(file_path):
        os.remove(file_path)
    doc = data['document']
    page = doc['children'][0]
    frame = page['children'][0]
    frame_width = int(frame['absoluteBoundingBox']['width'])
    frame_height = int(frame['absoluteBoundingBox']['height'])
    cpp_writer.write('#include <QApplication>\n#include <QWidget>\n#include <QLabel>\n#include <QPushButton>\n#include <QLineEdit>\n\nint main(int argc, char *argv[]) {\n    QApplication app(argc, argv);\n    QWidget root;\n    root.setGeometry(100, 100, 800, 600);\n', file_path)
    for element in frame['children']:
        if element['type'] == 'TEXT' or element['name'].lower() == 'text':
            create_text(element, 'root')
        elif element["name"].lower() == "button":
            create_button(element, 'root')
        elif element["name"].lower() == "entry":
            create_entry(element, 'root')
        elif element['type'] == 'FRAME':
            create_frame(element, 'root')
        print(f"Processed element {element['name']} of type {element['type']}")
    cpp_writer.write('    root.show();\n    return app.exec();\n}\n', file_path)