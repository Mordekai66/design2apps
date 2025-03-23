# Convert Figma Designs to Tkinter Code

This project aims to automatically convert Figma designs into Tkinter lib code, helping developers save time and effort when building graphical user interfaces for their applications.

---

## Project Goal

The project is designed to assist developers in converting ready-made designs into Python code using Tkinter without manual coding. Whether you're a beginner or an experienced developer, this tool can significantly speed up the development process.

---

## How It Works

1. **Enter the Design File ID from Figma**: Provide the file ID of your design from the workspace.  
2. **Enter the Access Token**: The access token is required to access the design for conversion.
3. **Specify the Output File Path**: Enter the path where you want to save the generated Python file.  
4. **Analyze the Design**: The script reads the design and extracts elements, colors, fonts, and layouts.  
5. **Generate the Code**: The tool generates Tkinter code based on the extracted data.  
6. **Final Output**: A Python file with ready-to-use Tkinter code is generated.  

---

## Features

- Fast conversion from Figma to Tkinter with minimal manual intervention.
- Supports colors, fonts, buttons, and layouts exactly as in the original design.
- Produces clean, well-structured, and easily readable code.
- Easy to modify and extend the generated output.

---
## Use Cases

This tool is useful for:  

- **Developers & Startups** – Quickly prototyping Tkinter-based applications.  
- **Students & Learners** – Understanding how GUI elements in Figma translate into Python code.  
- **GUI Designers** – Experimenting with Tkinter-based designs without deep Python knowledge.  

---

## Future Development Plans
- Support for other GUI libraries such as PyQt and Kivy.
- Improved handling of complex layouts.

---

# Repository Structure

```plaintext
figma2tkinter
│── src         # Source code directory
│   ├── main.py                            # Entry point for the application
│   ├── to_code.py                         # Logic to convert Figma design to Tkinter code
│   ├── collect_parse_json_file.py         # Fetches JSON data from Figma
│
│──  examples             # Sample designs and generated outputs
│   ├──  jsom.json        # Example Figma JSON file
│   ├──  output.py        # Generated Tkinter code
│
│──  requirements.txt      # Dependencies list
│──  LICENSE               # License information (e.g., MIT, GPL)
```
