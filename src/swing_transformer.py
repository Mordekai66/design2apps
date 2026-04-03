import os
import random
import requests
import writer as swinger_writer
import utils

file_path = ""
counters = {'label': 0, 'button': 0, 'entry': 0, 'imgLabel': 0, 'panel': 0, 'linepanel': 0}
def get_var(name):
    counters[name] += 1
    return f'{name}{counters[name]}'

def create_text(element, parent_name, file_path):
    etype = element.get("type", "")
    ename = element.get("name", "").lower()
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    var = get_var('label')
    text_content = element.get("characters", "")
    font_size = int(element.get("style", {}).get("fontSize", 12))
    text_color = utils.rgb_to_rgb_swing(element.get("fills", [{}])[0].get("color", {"r":0, "g":0, "b":0}))
    
    swinger_writer.write(f'        JLabel {var} = new JLabel("{text_content}");\n', file_path)
    swinger_writer.write(f'        {var}.setFont(new Font("Arial", Font.PLAIN, {font_size}));\n', file_path)
    swinger_writer.write(f'        {var}.setForeground({text_color});\n', file_path)
    swinger_writer.write(f'        {var}.setBounds({x}, {y}, {width}, {height});\n', file_path)
    swinger_writer.write(f'        {parent_name}.add({var});\n', file_path)

def create_button(element, parent_name, file_path):
    etype = element.get("type", "")
    ename = element.get("name", "").lower()
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    button_shape = None
    button_text = None
    
    for child in element.get("children", []):
        if child["type"] == "TEXT":
            button_text = child.get("characters", "Button")
        elif child["type"] in ["RECTANGLE", "ELLIPSE", "POLYGON", "STAR", "LINE", "ARROW"]:
            button_shape = child

    if button_shape:
        var = get_var('button')
        bx = abs(int(button_shape["absoluteBoundingBox"]["x"]))
        by = abs(int(button_shape["absoluteBoundingBox"]["y"]))
        bwidth = int(button_shape["absoluteBoundingBox"]["width"])
        bheight = int(button_shape["absoluteBoundingBox"]["height"])
        fill_color = utils.rgb_to_rgb_swing(button_shape.get("fills", [{}])[0].get("color", {"r":1, "g":1, "b":1}))
        swinger_writer.write(f'        JButton {var} = new JButton("{button_text or "Button"}");\n', file_path)
        swinger_writer.write(f'        {var}.setBounds({bx}, {by}, {bwidth+1}, {bheight});\n', file_path)
        swinger_writer.write(f'        {var}.setBackground({fill_color});\n', file_path)
        swinger_writer.write(f'        {parent_name}.add({var});\n', file_path)

def create_entry(element, parent_name, file_path):
    etype = element.get("type", "")
    ename = element.get("name", "").lower()
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    var = get_var('entry')
    swinger_writer.write(f'        JTextField {var} = new JTextField();\n', file_path)
    swinger_writer.write(f'        {var}.setBounds({x}, {y}, {width}, {height});\n', file_path)
    text_color = utils.rgb_to_rgb_swing(element.get("fills", [{}])[0].get("color", {"r":1, "g":1, "b":1}))
    swinger_writer.write(f'        {var}.setBackground({text_color});\n', file_path)
    swinger_writer.write(f'        {parent_name}.add({var});\n', file_path)

def create_image(element, parent_name, file_path, file_id_figma, token_access):
    etype = element.get("type", "")
    ename = element.get("name", "").lower()
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    node_id = element["id"]
    url = f"https://api.figma.com/v1/images/{file_id_figma}?ids={node_id}"
    headers = {"X-Figma-Token": token_access}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        var = get_var('imgLabel')
        image_data = response.json()
        image_url = image_data["images"].get(node_id, "")
        img_data = requests.get(image_url).content
        image_dir = os.path.join(output_path, "build", "image")
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        image_path = os.path.join(image_dir, f"{random.randint(1,200)}.png")
        with open(image_path, "wb") as s:
            s.write(img_data)
        swinger_writer.write(f'        try {{\n', file_path)
        swinger_writer.write(f'            ImageIcon icon = new ImageIcon("{image_path.replace("\\", "/")}");\n', file_path)
        swinger_writer.write(f'            JLabel {var} = new JLabel(icon);\n', file_path)
        swinger_writer.write(f'            {var}.setBounds({x}, {y}, {width}, {height});\n', file_path)
        swinger_writer.write(f'            {parent_name}.add({var});\n', file_path)
        swinger_writer.write(f'        }} catch (Exception e) {{ e.printStackTrace(); }}\n', file_path)

def create_frame(element, parent_name, file_path):
    etype = element.get("type", "")
    ename = element.get("name", "").lower()
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    var = get_var('panel')
    swinger_writer.write(f'        JPanel {var} = new JPanel();\n', file_path)
    swinger_writer.write(f'        {var}.setLayout(null);\n', file_path)
    swinger_writer.write(f'        {var}.setBounds({x}, {y}, {width}, {height});\n', file_path)
    fill_color = utils.rgb_to_rgb_swing(element.get("fills", [{}])[0].get("color", {"r":0.85, "g":0.85, "b":0.85}))
    swinger_writer.write(f'        {var}.setBackground({fill_color});\n', file_path)
    for child in element.get("children", []):
        if child["type"] == "TEXT" or child["name"].lower() == "text":
            create_text(child, var, file_path)
        elif child['name'].lower() == 'button':
            create_button(child, var, file_path)
        elif child["name"].lower() == "entry":
            create_entry(child, var, file_path)
        elif child["name"].lower() == "image":
            create_image(child, var, file_path, file_id_figma, token_access)
        elif child["type"] == "RECTANGLE":
            create_frame(child, var, file_path)
        elif child["type"] == "ELLIPSE":
            create_frame(child, var, file_path)
        elif child["type"] == "FRAME":
            create_frame(child, var, file_path)
        elif child["type"] == "LINE":
            create_line(child, var, file_path)
        elif child["type"] in "ARROW":
            create_line(child, var, file_path)
    swinger_writer.write(f'        {parent_name}.add({var});\n', file_path)

def create_line(element, parent_name, file_path):
    etype = element.get("type", "")
    ename = element.get("name", "").lower()
    x = abs(int(element["absoluteBoundingBox"]["x"]))
    y = abs(int(element["absoluteBoundingBox"]["y"]))
    width = int(element["absoluteBoundingBox"]["width"])
    height = int(element["absoluteBoundingBox"]["height"])
    var = get_var('linepanel')
    swinger_writer.write(f'        JPanel {var} = new JPanel() {{\n', file_path)
    swinger_writer.write(f'            protected void paintComponent(Graphics g) {{\n', file_path)
    swinger_writer.write(f'                super.paintComponent(g);\n', file_path)
    swinger_writer.write(f'                g.setColor(Color.BLACK);\n', file_path)
    swinger_writer.write(f'                g.drawLine(0, 0, {width}, {height});\n', file_path)
    swinger_writer.write(f'            }}\n', file_path)
    swinger_writer.write(f'        }};\n', file_path)
    swinger_writer.write(f'        {var}.setOpaque(false);\n', file_path)
    swinger_writer.write(f'        {var}.setBounds({x}, {y}, {width}, {height});\n', file_path)
    swinger_writer.write(f'        {parent_name}.add({var});\n', file_path)


def transform_to_swing(data, output_path, file_id_figma, token_access):
    global file_path
    page = data["document"]["children"][0]
    frame_node = page["children"][0]
    frame_width = int(frame_node["absoluteRenderBounds"]["width"])
    frame_height = int(frame_node["absoluteRenderBounds"]["height"])
    bg_color = utils.rgb_to_rgb_swing(frame_node.get("backgroundColor", {"r": 1, "g": 1, "b": 1}))
    file_path = os.path.join(output_path + "\\build" + "\\SwingUI.java")
    if os.path.exists(file_path):
        os.remove(file_path)
    
    swinger_writer.write("import javax.swing.*;\n", file_path)
    swinger_writer.write("import java.awt.*;\n", file_path)
    swinger_writer.write("import java.awt.image.*;\n", file_path)
    swinger_writer.write("import javax.imageio.ImageIO;\n", file_path)
    swinger_writer.write("import java.io.*;\n\n", file_path)
    swinger_writer.write("public class SwingUI {\n", file_path)
    swinger_writer.write("    public static void main(String[] args) {\n", file_path)
    swinger_writer.write("        JFrame frame = new JFrame();\n", file_path)
    swinger_writer.write(f'        frame.setTitle("{page["name"]}");\n', file_path)
    swinger_writer.write(f'        frame.setSize({frame_width}, {frame_height});\n', file_path)
    swinger_writer.write(f'        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);\n', file_path)
    swinger_writer.write(f'        frame.setLayout(null);\n', file_path)
    swinger_writer.write(f'        frame.getContentPane().setBackground({bg_color});\n', file_path)

    for element in frame_node["children"]:
        if element["type"] == "TEXT" or element["name"].lower() == "text":
            create_text(element, "frame", file_path)
        elif element['name'].lower() == 'button':
            create_button(element, "frame", file_path)
        elif element["name"].lower() == "entry":
            create_entry(element, "frame", file_path)
        elif element["name"].lower() == "image":
            create_image(element, "frame", file_path, file_id_figma, token_access)
        elif element["type"] == "RECTANGLE":
            create_frame(element, "frame", file_path)
        elif element["type"] == "ELLIPSE":
            create_frame(element, "frame", file_path)
        elif element["type"] == "FRAME":
            create_frame(element, "frame", file_path)
        elif element["type"] == "LINE":
            create_line(element, "frame", file_path)
        elif element["type"] in "ARROW":
            create_line(element, "frame", file_path)
            
    swinger_writer.write("        frame.setVisible(true);\n", file_path)
    swinger_writer.write("    }\n", file_path)
    swinger_writer.write("}\n", file_path)