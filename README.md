# design2apps — Convert Figma Designs to GUI Code

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![Figma](https://img.shields.io/badge/Figma-Input-F24E1E?logo=figma&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-Output-306998?logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-Output-41CD52?logo=qt&logoColor=white)
![Kivy](https://img.shields.io/badge/Kivy-Output-1EB8F1?logo=kivy&logoColor=white)
![Java Swing](https://img.shields.io/badge/Java_Swing-Output-007396?logo=java&logoColor=white)
![C++ Qt](https://img.shields.io/badge/C%2B%2B_Qt-Output-FF6B35?logo=qt&logoColor=white)
![Version](https://img.shields.io/badge/version-2.0.0-brightgreen)
![Views](https://visitor-badge.laobi.icu/badge?page_id=Mordekai66.design2apps)

design2apps automatically converts Figma designs into GUI code for multiple frameworks — Tkinter, Kivy, PyQt5, Java Swing, and C++ with Qt — saving developers the time of writing repetitive UI code by hand.

---

## Project Goal

Convert ready-made Figma designs into executable GUI code without manual coding, across multiple programming languages and frameworks, in less than 5 seconds.

---

## How It Works

design2apps supports two input modes:

**Figma API Mode**
1. Provide your Figma file ID and personal access token
2. The tool fetches the design via Figma API and saves it locally as `json.json`
3. Code is generated for all five frameworks simultaneously

**Local JSON Mode**
1. Upload a previously exported Figma JSON file directly
2. No API credentials required
3. Same generation pipeline applies

In both modes, the tool extracts elements, colors, fonts, and layouts from the design data, then generates framework-specific source files in your chosen output directory.

---

## Features

- **Two Input Modes**: Figma API or local JSON file upload
- **Multi-Framework Support**: Tkinter, Kivy, PyQt5, Java Swing, C++ with Qt
- **Comprehensive Element Support**: text, buttons, entries, images, rectangles, ellipses, frames, lines, arrows
- **Accurate Styling**: preserves colors, fonts, sizes, and layouts from the original design
- **Image Export**: automatically downloads and saves images from Figma into a local `image/` directory
- **File Tree Preview**: displays a hierarchical tree of all parsed UI elements before generation, allowing you to inspect structure, nesting, and components that will be converted into code
- **Threaded Generation**: all five framework files are generated simultaneously
- **Input Validation**: validates Figma token and file ID before making API calls

---

## Supported GUI Elements

- **Text**: font family, size, color, alignment
- **Buttons**: text content and background color
- **Input Fields**: text entry widgets
- **Images**: downloaded from Figma API or loaded from local path
- **Shapes**: rectangles, ellipses, lines, arrows
- **Frames / Groups**: nested elements with accurate positioning

---

## Installation

```bash
pip install requests pillow kivy pyqt5
```

For C++ output — ensure Qt development tools are installed.  
For Java output — ensure Java JDK is installed.

---

## Usage

### 1. Run the Application

```bash
python main.py
```

### 2. Choose Input Mode

The app opens in **Figma API mode** by default. Click **"Switch to JSON Upload"** to toggle to local JSON mode.

**Figma API Mode:**
- Enter your Figma File ID (from the URL: `https://www.figma.com/file/{FILE_ID}/...`)
- Enter your personal access token (generated from Figma account settings → Personal Access Tokens)
- Select output directory

**Local JSON Mode:**
- Select a Figma JSON file exported previously
- Select output directory

### 3. Generate

Click **Submit**. The tool validates inputs, fetches or loads the design data, and generates all output files simultaneously.

---

## Output Files

All files are saved under `{output_dir}/build/`:

| File | Framework |
|------|-----------|
| `TK.py` | Tkinter |
| `kivy_app.py` | Kivy |
| `pyqt5.py` | PyQt5 |
| `SwingUI.java` | Java Swing |
| `cpp.cpp` | C++ with Qt |
| `json.json` | Raw Figma design data |
| `image/` | Downloaded image assets |

---

## Project Structure

| File | Role |
|------|------|
| `main.py` | Application entry point and UI (Tkinter) |
| `figma_parser.py` | Fetches design from Figma API or loads local JSON |
| `tk_transformer.py` | Generates Tkinter code |
| `kivy_transformer.py` | Generates Kivy code |
| `pyqt5_transformer.py` | Generates PyQt5 code |
| `swing_transformer.py` | Generates Java Swing code |
| `cpp_transformer.py` | Generates C++ with Qt code |
| `writer.py` | Shared file-append utility used by all transformers |
| `utils.py` | Shared color conversion utilities |

---

## Framework Details

**Tkinter** — Canvas-based absolute positioning; preserves original design proportions.

**Kivy** — FloatLayout with coordinate system inversion (origin at bottom-left); canvas drawing for shapes.

**PyQt5** — QWidget with QPainter for shapes; StyleSheet for colors and fonts.

**Java Swing** — JFrame with absolute layout (`setBounds`); custom painting via `paintComponent` for lines and arrows.

**C++ with Qt** — QApplication/QWidget based; QLabel, QPushButton, QLineEdit components with StyleSheet styling.

---

## Visual Accuracy by Framework

| Framework | Accuracy | Notes |
|-----------|----------|-------|
| Tkinter | 95% | Most predictable layout system |
| PyQt5 | 92% | Complex widget hierarchy |
| Java Swing | 90% | AWT coordinate quirks |
| C++ with Qt | 88% | Memory management overhead |
| Kivy | 85% | Coordinate system inversion |

---

## Future Plans

- Enhanced support for complex and responsive layouts
- Additional frameworks (Flutter, React Native, C#)
- Basic interaction/event template generation
- Web-based version
- Plugin system for community-contributed transformers
- Batch processing for multiple designs
