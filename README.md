# Convert Figma Designs to GUI Code (Tkinter, Kivy, PyQt5)

This project aims to automatically convert Figma designs into GUI code for Tkinter, Kivy, and PyQt5, helping developers save time and effort when building graphical user interfaces for their applications.

---

## Project Goal

The project is designed to assist developers in converting ready-made designs into Python code using Tkinter, Kivy, and PyQt5 without manual coding. Whether you're a beginner or an experienced developer, this tool can significantly speed up the development process.

---

## How It Works

1. **Enter the Design File ID from Figma**: Provide the file ID of your design from the workspace.  
2. **Enter the Access Token**: The access token is required to access the design for conversion.  
3. **Specify the Output File Path**: Enter the path where you want to save the generated Python file.  
4. **Analyze the Design**: The script reads the design and extracts elements, colors, fonts, and layouts.  
5. **Choose Output Framework**: Select whether you want the output in Tkinter, Kivy, or PyQt5.  
6. **Generate the Code**: The tool generates GUI code based on the extracted data.  
7. **Final Output**: A Python file with ready-to-use GUI code is generated.  

---

## Features

- Fast conversion from Figma to Tkinter, Kivy, and PyQt5 with minimal manual intervention.
- Supports colors, fonts, buttons, and layouts exactly as in the original design.
- Produces clean, well-structured, and easily readable code.
- Supports multiple GUI frameworks, allowing developers to choose their preferred one.
- Easy to modify and extend the generated output.

---

## Use Cases

This tool is useful for:  

- **Developers & Startups** – Quickly prototyping GUI-based applications.  
- **Students & Learners** – Understanding how GUI elements in Figma translate into Python code.  
- **GUI Designers** – Experimenting with different Python GUI frameworks without deep coding knowledge.  

---

## Future Development Plans

- Enhanced support for complex layouts and advanced GUI components.
- Additional support for more GUI frameworks like PySide and Dear PyGui.
- Improved error handling and customization options.

---

# Repository Structure

```plaintext
figma2gui
│── src         # Source code directory
│   ├── main.py                            # Entry point for the application
│   ├── collect_parse_json_file.py         # Fetches JSON data from Figma
│   ├── to_tk.py                # Converts design to Tkinter
│   ├── to_kivy.py              # Converts design to Kivy
│   ├── to_pyqt5.py             # Converts design to PyQt5
│
│──  examples              # Sample designs and generated outputs
│   ├──  sample.json       # Example Figma JSON file
│   ├──  output_tkinter.py # Generated Tkinter code
│   ├──  output_kivy.py    # Generated Kivy code
│   ├──  output_pyqt5.py   # Generated PyQt5 code
│
│──  requirements.txt      # Dependencies list
│──  LICENSE               # License information
```

