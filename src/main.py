from tkinter import *
from tkinter import filedialog, messagebox
import requests
import json
import os
import threading
from figma_parser import parse
from tk_transformer import transform_to_tk
from kivy_transformer import transform_to_kivy
from pyqt5_transformer import transform_to_pyqt5
from swing_transformer import transform_to_swing
from cpp_transformer import transform_to_cpp
from preview import show_preview
import utils

active_mode = "figma"  # "figma" or "json"

def on_toggle_mode():
    global active_mode
    if active_mode == "figma":
        
        active_mode = "json"
        mode_label.config(text="Current Mode: Upload JSON File")
        
        # Hide Figma inputs
        file_id_label.place_forget()
        file_id_entry.place_forget()
        token_label.place_forget()
        token_entry.place_forget()
        
        # Show JSON upload
        json_label.place(x=42, y=114)
        json_entry.place(x=45, y=151, width=304, height=30)
        json_browse_btn.place(x=370, y=151, width=30, height=30)
        
    else:
        active_mode = "figma"
        mode_label.config(text="Current Mode: Figma API")
        
        # Show Figma inputs
        file_id_label.place(x=42, y=114)
        file_id_entry.place(x=45, y=151, width=304, height=30)
        token_label.place(x=42, y=213)
        token_entry.place(x=45, y=250, width=355, height=30)
        
        # Hide JSON upload
        json_label.place_forget()
        json_entry.place_forget()
        json_browse_btn.place_forget()

def on_browse_output():
    folder_path = filedialog.askdirectory()
    output_entry.delete(0, END)
    output_entry.insert(0, folder_path)

def on_browse_json():
    file_path = filedialog.askopenfilename(
        title="Select JSON File",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    if file_path:
        json_entry.delete(0, END)
        json_entry.insert(0, file_path)

def run_transformer(func, *args, message="File created successfully!"):
    try:
        func(*args)
        messagebox.showinfo("Success", message)
    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")

def on_submit():
    global current_mode
    
    # Check if at least one framework is selected
    if not any([tk_var.get(), kivy_var.get(), pyqt5_var.get(), swing_var.get(), cpp_var.get()]):
        messagebox.showerror("Error", "Please select at least one framework")
        return
    
    output_dir = output_entry.get().strip()
    
    if output_dir.startswith(("\"", "'")) and output_dir.endswith(("\"", "'")):
        output_dir = output_dir[1:-1]

    if not utils.validate_output_dir(output_dir):
        return

    if active_mode == "figma":
        # Figma API mode
        token_access = token_entry.get().strip()
        file_id = file_id_entry.get().strip()

        if not utils.validate_figma_fields(token_access, file_id):
            return

        if not utils.validate_figma_token(token_access, file_id):
            return

        try:
            data = parse(token_access, file_id, output_dir)
            if data is None:
                messagebox.showerror("Error", "Failed to fetch data from Figma")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Error parsing data: {e}")
            return

    else:
        # JSON file mode
        json_file_path = json_entry.get().strip()
        if not json_file_path:
            messagebox.showerror("Error", "Please select a JSON file")
            return
        
        if not os.path.exists(json_file_path):
            messagebox.showerror("Error", "JSON file does not exist")
            return

        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Save a copy to build directory for consistency
            build_dir = os.path.join(output_dir, "build")
            os.makedirs(build_dir, exist_ok=True)
            
            with open(os.path.join(build_dir, "json.json"), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading JSON file: {e}")
            return

    # Generate selected UI files
    file_id_figma = file_id_entry.get().strip() if active_mode == "figma" else "local_json"
    token_access = token_entry.get().strip() if active_mode == "figma" else "local_json"

    def do_generate():
        if tk_var.get():
            threading.Thread(target=run_transformer, args=(transform_to_tk, data, output_dir, file_id_figma, token_access), kwargs={"message": "Tk file created successfully!"}).start()
        if kivy_var.get():
            threading.Thread(target=run_transformer, args=(transform_to_kivy, data, output_dir, file_id_figma, token_access), kwargs={"message": "Kivy file created successfully!"}).start()
        if pyqt5_var.get():
            threading.Thread(target=run_transformer, args=(transform_to_pyqt5, data, output_dir, file_id_figma, token_access), kwargs={"message": "PyQt5 file created successfully!"}).start()
        if swing_var.get():
            threading.Thread(target=run_transformer, args=(transform_to_swing, data, output_dir, file_id_figma, token_access), kwargs={"message": "Swing file created successfully!"}).start()
        if cpp_var.get():
            threading.Thread(target=run_transformer, args=(transform_to_cpp, data, output_dir, file_id_figma, token_access), kwargs={"message": "C++ file created successfully!"}).start()
    show_preview(data, on_confirm=do_generate)

app = Tk()
app.title("design2apps")
app.geometry("570x550")
app.config(bg="#0f0e17")
app.resizable(0, 0)

tk_var = IntVar(value=1)
kivy_var = IntVar(value=1)
pyqt5_var = IntVar(value=1)
swing_var = IntVar(value=1)
cpp_var = IntVar(value=1)

canvas = Canvas(app, width=562, height=550, bg='#0f0e17', highlightthickness=0)
canvas.pack(fill='both', expand=True)

# Title
canvas.create_text(281, 30, anchor="center", text="design2apps", fill="#fffffe", font=("Inter", 36, "bold"))

# Mode toggle section
canvas.create_text(42, 70, anchor="w", text="Data Source:", fill="#ffffff", font=("Inter", 14))

# Mode toggle button
toggle_btn = Button(app, text="Switch to JSON Upload", bg='#ff8906', fg="black", font=("Arial", 10), command=on_toggle_mode, relief="flat")
canvas.create_window(200, 70, anchor="w", window=toggle_btn)

# Current mode label
mode_label = Label(app, text="Current Mode: Figma API", bg="#0f0e17", fg="#ffffff", font=("Inter", 10))
canvas.create_window(400, 70, anchor="w", window=mode_label)

# Figma API input fields (initially visible)
file_id_label = Label(app, text="Enter your file id", bg="#0f0e17", fg="#ffffff", font=("Inter", 14))
file_id_label.place(x=42, y=114)

# Figma File ID entry field
file_id_entry = Entry(app, bg='#ff8906', fg="black", font=("Arial", 10))
file_id_entry.place(x=45, y=151, width=304, height=30)

# Figma Token entry field
token_label = Label(app, text="Enter your token access", bg="#0f0e17", fg="#ffffff", font=("Inter", 14))
token_label.place(x=42, y=213)

# Figma Token entry field
token_entry = Entry(app, bg='#ff8906', fg="black", font=("Arial", 10))
token_entry.place(x=45, y=250, width=355, height=30)

# JSON upload fields (initially hidden)
json_label = Label(app, text="Select JSON File", bg="#0f0e17", fg="#ffffff", font=("Inter", 14))

# JSON file path entry field (initially hidden)
json_entry = Entry(app, bg='#ff8906', fg="black", font=("Arial", 10))
json_browse_btn = Button(app, text="📁", bg='#875d5d', fg="black", font=("Arial", 10), command=on_browse_json, relief="flat")

# Framework selection label
framework_label = Label(app, text="Select Frameworks:", bg="#0f0e17", fg="#ffffff", font=("Inter", 14))
framework_label.place(x=42, y=290)

# Framework checkboxes
tk_check = Checkbutton(app, text="Tkinter", variable=tk_var, bg="#0f0e17", fg="#ffffff", selectcolor="#0f0e17", activebackground="#0f0e17", font=("Inter", 12))
tk_check.place(x=42, y=320)

kivy_check = Checkbutton(app, text="Kivy", variable=kivy_var, bg="#0f0e17", fg="#ffffff", selectcolor="#0f0e17", activebackground="#0f0e17", font=("Inter", 12))
kivy_check.place(x=150, y=320)

pyqt5_check = Checkbutton(app, text="PyQt5", variable=pyqt5_var, bg="#0f0e17", fg="#ffffff", selectcolor="#0f0e17", activebackground="#0f0e17", font=("Inter", 12))
pyqt5_check.place(x=250, y=320)

swing_check = Checkbutton(app, text="Swing", variable=swing_var, bg="#0f0e17", fg="#ffffff", selectcolor="#0f0e17", activebackground="#0f0e17", font=("Inter", 12))
swing_check.place(x=350, y=320)

cpp_check = Checkbutton(app, text="C++", variable=cpp_var, bg="#0f0e17", fg="#ffffff", selectcolor="#0f0e17", activebackground="#0f0e17", font=("Inter", 12))
cpp_check.place(x=450, y=320)

# Output directory selection
output_label = Label(app, text="Choose the output file path", bg="#0f0e17", fg="#ffffff", font=("Inter", 14))
output_label.place(x=42, y=360)

# Output directory entry field
output_entry = Entry(app, bg='#ff8906', fg="black", font=("Arial", 10))
output_entry.place(x=45, y=397, width=304, height=30)

# Output directory browse button
output_browse_btn = Button(app, text="📁", bg='#875d5d', fg="black", font=("Arial", 10), command=on_browse_output, relief="flat")
output_browse_btn.place(x=370, y=397, width=30, height=30)

# Submit button
submit_btn = Button(app, text="Submit", bg='#c34e4e', fg="black", font=("Arial", 14, "bold"), command=on_submit, relief="flat", width=15, height=2)
canvas.create_window(281, 470, anchor="center", window=submit_btn)

app.mainloop()