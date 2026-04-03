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

def run_transformer(func, *args, message="Done!"):
    try:
        func(*args)
        messagebox.showinfo("Success", message)
    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")

def on_submit():
    global current_mode
    
    output_dir = output_entry.get().strip()
    
    if output_dir.startswith(("\"", "'")) and output_dir.endswith(("\"", "'")):
        output_dir = output_dir[1:-1]

    if not validate_output_dir(output_dir):
        return

    if active_mode == "figma":
        # Figma API mode
        token_access = token_entry.get().strip()
        file_id = file_id_entry.get().strip()

        if not validate_figma_fields(token_access, file_id):
            return

        if not validate_figma_token(token_access, file_id):
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

    # Generate all UI files
    file_id_figma = entry_1.get().strip() if active_mode == "figma" else "local_json"
    token_access = entry_2.get().strip() if active_mode == "figma" else "local_json"

    threading.Thread(target=run_transformer, args=(transform_to_tk, data, output_dir, file_id_figma, token_access), kwargs={"message": "Tk file created successfully!"}).start()
    threading.Thread(target=run_transformer, args=(transform_to_kivy, data, output_dir, file_id_figma, token_access), kwargs={"message": "Kivy file created successfully!"}).start()
    threading.Thread(target=run_transformer, args=(transform_to_pyqt5, data, output_dir, file_id_figma, token_access), kwargs={"message": "PyQt5 file created successfully!"}).start()
    threading.Thread(target=run_transformer, args=(transform_to_swing, data, output_dir, file_id_figma, token_access), kwargs={"message": "Swing file created successfully!"}).start()
    threading.Thread(target=run_transformer, args=(transform_to_cpp, data, output_dir, file_id_figma, token_access), kwargs={"message": "C++ file created successfully!"}).start()

def validate_output_dir(output_path):
    if not output_path:
        messagebox.showerror("Error", "Output path is empty")
        return False
    if not os.path.exists(output_path):
        messagebox.showerror("Error", "Path does not exist")
        return False
    if not os.path.isdir(output_path):
        messagebox.showerror("Error", "Path is not a directory")
        return False
    return True

def validate_figma_fields(token, fileID):
    if not fileID:
        messagebox.showerror("Error", "File ID is empty")
        return False
    if not token:
        messagebox.showerror("Error", "Token is empty")
        return False
    return True

def validate_figma_token(token, file_id):
    url = f"https://api.figma.com/v1/files/{file_id}"
    headers = {"X-Figma-Token": token}

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Figma API error: {e}")
        return False

    if response.status_code == 200:
        return True
    if response.status_code == 403:
        messagebox.showerror("Error", "Invalid token or insufficient permissions")
        return False
    if response.status_code == 404:
        messagebox.showerror("Error", "File not found")
        return False
    if response.status_code == 401:
        messagebox.showerror("Error", "Unauthorized access - check your token")
        return False
    if response.status_code == 429:
        messagebox.showerror("Error", "Rate limit exceeded - please try again later")
        return False

    messagebox.showerror("Error", f"Unexpected error: {response.status_code}")
    return False

app = Tk()
app.title("Figma API Integration")
app.geometry("562x500")
app.config(bg="#0f0e17")
app.resizable(0, 0)

canvas = Canvas(app, width=562, height=500, bg='#0f0e17', highlightthickness=0)
canvas.pack(fill='both', expand=True)

# Title
canvas.create_text(281, 30, anchor="center", text="Tk Designer", fill="#fffffe", font=("Inter", 36, "bold"))

# Mode toggle section
canvas.create_text(42, 70, anchor="w", text="Data Source:", fill="#ffffff", font=("Inter", 14))

# Mode toggle button
toggle_btn = Button(app, text="Switch to JSON Upload", bg='#ff8906', fg="black", font=("Arial", 10), command=on_toggle_mode, relief="flat")
canvas.create_window(200, 70, anchor="w", window=toggle_btn)

mode_label = Label(app, text="Current Mode: Figma API", bg="#0f0e17", fg="#ffffff", font=("Inter", 10))
canvas.create_window(400, 70, anchor="w", window=mode_label)

file_id_label = Label(app, text="Enter your file id", bg="#0f0e17", fg="#ffffff", font=("Inter", 14))
file_id_label.place(x=42, y=114)

file_id_entry = Entry(app, bg='#ff8906', fg="black", font=("Arial", 10))
file_id_entry.place(x=45, y=151, width=304, height=30)

token_label = Label(app, text="Enter your token access", bg="#0f0e17", fg="#ffffff", font=("Inter", 14))
token_label.place(x=42, y=213)

token_entry = Entry(app, bg='#ff8906', fg="black", font=("Arial", 10))
token_entry.place(x=45, y=250, width=355, height=30)

json_label = Label(app, text="Select JSON File", bg="#0f0e17", fg="#ffffff", font=("Inter", 14))

json_entry = Entry(app, bg='#ff8906', fg="black", font=("Arial", 10))
json_browse_btn = Button(app, text="📁", bg='#875d5d', fg="black", 
                        font=("Arial", 10), command=on_browse_json, relief="flat")

output_label = Label(app, text="Choose the output file path", bg="#0f0e17", fg="#ffffff", font=("Inter", 14))
output_label.place(x=42, y=312)

output_entry = Entry(app, bg='#ff8906', fg="black", font=("Arial", 10))
output_entry.place(x=45, y=349, width=304, height=30)

output_browse_btn = Button(app, text="📁", bg='#875d5d', fg="black", font=("Arial", 10), command=on_browse_output, relief="flat")
output_browse_btn.place(x=370, y=349, width=30, height=30)

# Submit button
submit_btn = Button(app, text="Submit", bg='#c34e4e', fg="black", font=("Arial", 14, "bold"), command=on_submit, relief="flat", width=15, height=2)
canvas.create_window(281, 420, anchor="center", window=submit_btn)

app.mainloop()