import os
import random
import requests
from Writers.swing_writer import write

def color_from_figma(color):
    r = int(color.get('r', 1) * 255)
    g = int(color.get('g', 1) * 255)
    b = int(color.get('b', 1) * 255)
    return f'new Color({r}, {g}, {b})'

def transform_json_to_swing(data, output_path, file_id_figma, token_access):
    file_path = os.path.join(output_path + "\\build" + "\\SwingUI.java")
    if os.path.exists(file_path):
        os.remove(file_path)
    
    write("import javax.swing.*;\n", file_path)
    write("import java.awt.*;\n", file_path)
    write("import java.awt.image.*;\n", file_path)
    write("import javax.imageio.ImageIO;\n", file_path)
    write("import java.io.*;\n\n", file_path)
    write("public class SwingUI {\n", file_path)
    write("    public static void main(String[] args) {\n", file_path)
    write("        JFrame frame = new JFrame();\n", file_path)
    
    document = data["document"]
    page = document["children"][0]
    frame_node = page["children"][0]
    
    frame_width = int(frame_node["absoluteRenderBounds"]["width"])
    frame_height = int(frame_node["absoluteRenderBounds"]["height"])
    bg_color = frame_node.get("backgroundColor", {"r": 1, "g": 1, "b": 1})
    
    write(f'        frame.setTitle("{page["name"]}");\n', file_path)
    write(f'        frame.setSize({frame_width}, {frame_height});\n', file_path)
    write(f'        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);\n', file_path)
    write(f'        frame.setLayout(null);\n', file_path)
    write(f'        frame.getContentPane().setBackground({color_from_figma(bg_color)});\n', file_path)
    
    # Counters for unique variable names
    counters = {
        'label': 0,
        'button': 0,
        'entry': 0,
        'imgLabel': 0,
        'panel': 0,
        'linepanel': 0
    }
    def get_var(name):
        counters[name] += 1
        return f'{name}{counters[name]}'
    
    def handle_element(element, parent_name):
        etype = element.get("type", "")
        ename = element.get("name", "").lower()
        x = abs(int(element["absoluteBoundingBox"]["x"]))
        y = abs(int(element["absoluteBoundingBox"]["y"]))
        width = int(element["absoluteBoundingBox"]["width"])
        height = int(element["absoluteBoundingBox"]["height"])
        
        if etype == "TEXT" or ename == "text":
            var = get_var('label')
            text_content = element.get("characters", "")
            font_size = int(element.get("style", {}).get("fontSize", 12))
            text_color = element.get("fills", [{}])[0].get("color", {"r":0, "g":0, "b":0})
            write(f'        JLabel {var} = new JLabel("{text_content}");\n', file_path)
            write(f'        {var}.setFont(new Font("Arial", Font.PLAIN, {font_size}));\n', file_path)
            write(f'        {var}.setForeground({color_from_figma(text_color)});\n', file_path)
            write(f'        {var}.setBounds({x}, {y}, {width}, {height});\n', file_path)
            write(f'        {parent_name}.add({var});\n', file_path)
        elif ename == "button":
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
                fill_color = button_shape.get("fills", [{}])[0].get("color", {"r":1, "g":1, "b":1})
                write(f'        JButton {var} = new JButton("{button_text or "Button"}");\n', file_path)
                write(f'        {var}.setBounds({bx}, {by}, {bwidth+1}, {bheight});\n', file_path)
                write(f'        {var}.setBackground({color_from_figma(fill_color)});\n', file_path)
                write(f'        {parent_name}.add({var});\n', file_path)
        elif ename == "entry":
            var = get_var('entry')
            write(f'        JTextField {var} = new JTextField();\n', file_path)
            write(f'        {var}.setBounds({x}, {y}, {width}, {height});\n', file_path)
            text_color = element.get("fills", [{}])[0].get("color", {"r":1, "g":1, "b":1})
            write(f'        {var}.setBackground({color_from_figma(text_color)});\n', file_path)
            write(f'        {parent_name}.add({var});\n', file_path)
        elif ename == "image":
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
                write(f'        try {{\n', file_path)
                write(f'            ImageIcon icon = new ImageIcon("{image_path.replace("\\", "/")}");\n', file_path)
                write(f'            JLabel {var} = new JLabel(icon);\n', file_path)
                write(f'            {var}.setBounds({x}, {y}, {width}, {height});\n', file_path)
                write(f'            {parent_name}.add({var});\n', file_path)
                write(f'        }} catch (Exception e) {{ e.printStackTrace(); }}\n', file_path)
        elif etype in ["RECTANGLE", "ELLIPSE", "FRAME"] or ename == "frame":
            var = get_var('panel')
            write(f'        JPanel {var} = new JPanel();\n', file_path)
            write(f'        {var}.setLayout(null);\n', file_path)
            write(f'        {var}.setBounds({x}, {y}, {width}, {height});\n', file_path)
            fill_color = element.get("fills", [{}])[0].get("color", {"r":0.85, "g":0.85, "b":0.85})
            write(f'        {var}.setBackground({color_from_figma(fill_color)});\n', file_path)
            for child in element.get("children", []):
                handle_element(child, var)
            write(f'        {parent_name}.add({var});\n', file_path)
        elif etype in ["LINE", "ARROW"] or ename in ["line", "arrow"]:
            var = get_var('linepanel')
            write(f'        JPanel {var} = new JPanel() {{\n', file_path)
            write(f'            protected void paintComponent(Graphics g) {{\n', file_path)
            write(f'                super.paintComponent(g);\n', file_path)
            write(f'                g.setColor(Color.BLACK);\n', file_path)
            write(f'                g.drawLine(0, 0, {width}, {height});\n', file_path)
            write(f'            }}\n', file_path)
            write(f'        }};\n', file_path)
            write(f'        {var}.setOpaque(false);\n', file_path)
            write(f'        {var}.setBounds({x}, {y}, {width}, {height});\n', file_path)
            write(f'        {parent_name}.add({var});\n', file_path)
    
    for element in frame_node["children"]:
        handle_element(element, "frame")
    
    write("        frame.setVisible(true);\n", file_path)
    write("    }\n", file_path)
    write("}\n", file_path)
    write("close()", file_path) 