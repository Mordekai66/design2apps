# Convert Figma Designs to GUI Code

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![Figma](https://img.shields.io/badge/Figma-Input-F24E1E?logo=figma&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-Output-306998?logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-Output-41CD52?logo=qt&logoColor=white)
![Kivy](https://img.shields.io/badge/Kivy-Output-1EB8F1?logo=kivy&logoColor=white)
![Java Swing](https://img.shields.io/badge/Java_Swing-Output-007396?logo=java&logoColor=white)
![C++ Qt](https://img.shields.io/badge/C%2B%2B_Qt-Output-FF6B35?logo=qt&logoColor=white)

This project automatically converts Figma designs into GUI code for multiple frameworks including Tkinter, Kivy, PyQt5, Java Swing, and C++ with Qt, helping developers save time and effort when building graphical user interfaces.

---

## Project Goal

The project assists developers in converting ready-made Figma designs into executable GUI code without manual coding. Whether you're a beginner or an experienced developer, this tool can significantly speed up the development process across multiple programming languages and frameworks.

---

## How It Works

1. **Enter the Design File ID from Figma**: Provide the file ID of your design from the workspace.  
2. **Enter the Access Token**: The access token is required to access the design for conversion.  
3. **Specify the Output File Path**: Enter the directory path where you want to save the generated code files.  
4. **Analyze the Design**: The script fetches the Figma design via API and extracts elements, colors, fonts, and layouts.  
5. **Generate Code for All Frameworks**: The tool automatically generates GUI code for Tkinter, Kivy, PyQt5, Java Swing, and C++ with Qt.  
6. **Final Output**: Multiple code files with ready-to-use GUI code are generated in the specified output directory.  

---

## Features

- **Multi-Framework Support**: Convert to Tkinter, Kivy, PyQt5, Java Swing, and C++ with Qt
- **Comprehensive Element Support**: Handles text, buttons, entries, images, rectangles, ellipses, frames, lines, and arrows
- **Accurate Styling**: Preserves colors, fonts, sizes, and layouts from the original design
- **Image Export**: Automatically downloads and embeds images from Figma designs
- **Clean Code Generation**: Produces well-structured, readable, and executable code
- **Threaded Processing**: Generates code for all frameworks simultaneously for better performance
- **Input Validation**: Validates Figma access tokens and file IDs before processing

---

## Supported GUI Elements

- **Text Elements**: With proper font family, size, color, and alignment
- **Buttons**: With text content and styling
- **Input Fields**: Text entry fields
- **Images**: Automatically downloaded from Figma
- **Shapes**: Rectangles, ellipses, lines, and arrows
- **Containers**: Frames and groups with nested elements
- **Layouts**: Accurate positioning and sizing of all elements

---

## Use Cases

This tool is useful for:  

- **Developers & Startups** – Quickly prototyping GUI-based applications across multiple technologies
- **Students & Learners** – Understanding how GUI designs translate into different programming frameworks
- **GUI Designers** – Experimenting with different GUI frameworks without deep coding knowledge
- **Cross-Platform Development** – Generating UI code for multiple platforms from a single design

---

## Installation & Setup

1. **Install Python Dependencies**:
```bash
pip install requests pillow
```
For C++ Output: Ensure you have Qt development tools installed

For Java Output: Ensure you have Java JDK installed

2. **Run the Application**:

```bash
python main.py
```

## How to Use

### 1. Get Figma Credentials

**Obtain Figma File ID:**
- Go to your Figma design file
- Copy the file ID from the URL:
https://www.figma.com/file/{FILE_ID}/your-design-name

**Generate Access Token:**
1. Go to Figma account settings
2. Navigate to "Personal Access Tokens" section
3. Generate a new token with read access
4. Copy the generated token

### 2. Run the Application

**Launch the Application:**
```bash
python main.py
```
Application Steps:

1. Enter Figma File ID - Paste your Figma file ID in the first input field

2. Enter Access Token - Paste your Figma personal access token in the second input field

3. Select Output Directory - Click the folder icon to choose where to save generated files

4. Generate Code - Click the "Submit" button to start the conversion process

### 3. Generated Files
Output Location:

- All files are saved in the build subdirectory of your chosen output path

#### Generated Files:

TK.py - Tkinter Python code

kivy_code.py - Kivy Python code

pyqt5.py - PyQt5 Python code

SwingUI.java - Java Swing code

cpp.cpp - C++ with Qt code

json.json - Raw Figma design data

image/ - Directory containing downloaded images from the design

## Framework Details
**Tkinter**:
- Uses Canvas for precise element positioning

- Supports all basic GUI elements

- Maintains original design proportions

**Kivy**:
- FloatLayout for flexible positioning

- Canvas drawing for shapes

- Responsive design considerations

**PyQt5**:
- QWidget-based implementation

- QPainter for custom shapes

- StyleSheet support for styling

**Java Swing:**
- JFrame with absolute positioning

- Support for images and custom painting

- Standard Swing components

**C++ with Qt**:
- QApplication and QWidget based

- QLabel, QPushButton, QLineEdit components

- StyleSheet implementation for colors

## Future Development Plans
- Enhanced support for complex layouts and responsive designs

- Additional GUI frameworks support (Flutter, React Native, etc.)

- Improved error handling and user feedback

- More customization options for generated code

- Batch processing for multiple designs

- Plugin system for extending functionality
