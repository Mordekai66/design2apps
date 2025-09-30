import json
from pydoc import Doc
from this import d
from Writers.cpp_writer import write
import os

def color_to_qcolor(color):
    r = int(color.get('r', 1) * 255)
    g = int(color.get('g', 1) * 255)
    b = int(color.get('b', 1) * 255)
    return f'QColor({r},{g},{b})'

def transform_json_to_cpp(data, output_path, file_id_figma, token_access):
    file_path = os.path.join(output_path +"\\build" + "\\cpp.cpp")

    if os.path.exists(file_path):
        os.remove(file_path)

    write('#include <QApplication>\n#include <QWidget>\n#include <QLabel>\n#include <QPushButton>\n#include <QLineEdit>\n\nint main(int argc, char *argv[]) {\n    QApplication app(argc, argv);\n    QWidget root;\n    root.setGeometry(100, 100, 800, 600);\n', file_path)
    counters = {'label': 0, 'button': 0, 'entry': 0, 'frame': 0}
    def get_var(name):
        counters[name] += 1
        return f'{name}{counters[name]}'
    def handle_element(element, parent, parent_bbox=None):
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
            color = color_to_qcolor(element.get('fills', [{}])[0].get('color', {'r':0, 'g':0, 'b':0}))
            write(f'    QLabel* {var} = new QLabel({parent});\n', file_path)
            write(f'    {var}->setText("{text}");\n', file_path)
            write(f'    {var}->setGeometry({x}, {y}, {width}, {height});\n', file_path)
            write(f'    {var}->setStyleSheet("color: {color}; font-size: {font_size}px;");\n', file_path)
        elif ename == 'button' or etype == 'BUTTON':
            var = get_var('button')
            btn_text = 'Button'
            for child in element.get('children', []):
                if child['type'] == 'TEXT':
                    btn_text = child.get('characters', 'Button')
            write(f'    QPushButton* {var} = new QPushButton({parent});\n', file_path)
            write(f'    {var}->setText("{btn_text}");\n', file_path)
            write(f'    {var}->setGeometry({x}, {y}, {width}, {height});\n', file_path)
        elif ename == 'entry' or etype == 'ENTRY':
            var = get_var('entry')
            write(f'    QLineEdit* {var} = new QLineEdit({parent});\n', file_path)
            write(f'    {var}->setGeometry({x}, {y}, {width}, {height});\n', file_path)
        elif etype == 'FRAME' or ename == 'frame':
            var = get_var('frame')
            color = color_to_qcolor(element.get('backgroundColor', {'r':1,'g':1,'b':1}))
            write(f'    QWidget* {var} = new QWidget({parent});\n', file_path)
            write(f'    {var}->setStyleSheet("background-color: {color};");\n', file_path)
            write(f'    {var}->setGeometry({x}, {y}, {width}, {height});\n', file_path)
            for child in element.get('children', []):
                handle_element(child, var, bbox)
        elif etype == 'GROUP' or ename == 'group':
            for child in element.get('children', []):
                handle_element(child, parent, parent_bbox)
    doc = data['document']
    page = doc['children'][0]
    for element in page['children']:
        if element['type'] == 'FRAME':
            handle_element(element, '&root', element['absoluteBoundingBox'])
    write('    root.show();\n    return app.exec();\n}\n', file_path)
    write('close()', file_path)

# Example usage:
# generate_cpp('build/json.json', 'cpp_generated.cpp') 