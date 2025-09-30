from tkinter import *
import requests
import json
import os
from collect_parse_json_file import parse
from to_tk import transform_json_to_tk
from to_kivy import transform_json_to_kivy
from to_pyqt5 import transform_json_to_pyqt5
from tkinter import filedialog, messagebox
from to_swing import transform_json_to_swing
from to_cpp import transform_json_to_cpp
import threading
# only shapes
# 7W HakZ aG3 8u6br 2Bw3 92Lv
# f i g d_ w -iI LLhME Oqtf XI0 Orz N9 nVi   m7v5wD D5HXzI7--I

# general test
# G 6hQ7h n1 nsJY yrN qFC e k39
# fi g d_w-iILLhMEOqtf XI0 OrzN 9nVim7 v5wDD5HXzI7--   I

# calc test
# HEWUrIrqS9Or3L8OHmWIqj
# fi gd _w-iILLhMEOq    tfXI0 O rz N 9 n Vi m7v5wDD5HXzI7--I

# Compare login test with real world wxample
# VhBqxbkrjSDMKX U U C 70 MLX
# f ig d_w-iILLhMEOqtfXI0OrzN9nVim7v5wDD5HX z I 7 --I

def select_file(event):
    folder_path = filedialog.askdirectory()
    entry_3.delete(0,END)
    entry_3.insert(0,folder_path)


def run_with_message(func, *args, message="Done!"):
        func(*args)
        messagebox.showinfo("Success", message)

def call_data(event):
    token_access = entry_2.get().strip()
    file_id = entry_1.get().strip()
    output_file_path = os.path.dirname(entry_3.get().strip())
    print(output_file_path)

    if output_file_path.startswith(("\"", "'")) and output_file_path.endswith(("\"", "'")):
        output_file_path = output_file_path[1:-1]

    if validate_inputs(token_access, file_id, output_file_path) and check_figma_access(token_access, file_id):
        print(output_file_path)
        try:
            data = parse(token_access, file_id, output_file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error parsing data: {e}")
            return

        threading.Thread(target=run_with_message, args=(transform_json_to_tk, data, output_file_path, file_id, token_access), kwargs={"message": "Tk file created successfully!"}).start()
        threading.Thread(target=run_with_message, args=(transform_json_to_kivy, data, output_file_path, file_id, token_access), kwargs={"message": "Kivy file created successfully!"}).start()
        threading.Thread(target=run_with_message, args=(transform_json_to_pyqt5, data, output_file_path, file_id, token_access), kwargs={"message": "PyQt5 file created successfully!"}).start()
        threading.Thread(target=run_with_message, args=(transform_json_to_swing, data, output_file_path, file_id, token_access), kwargs={"message": "Swing file created successfully!"}).start()
        threading.Thread(target=run_with_message, args=(transform_json_to_cpp, data, output_file_path, file_id, token_access), kwargs={"message": "C++ file created successfully!"}).start()

    else:
        messagebox.showerror("Error", "Check your entries!")

def validate_inputs(token, fileID, output_path):
    if not fileID:
        messagebox.showerror("Error", "File ID is empty")
        return False
    if not token:
        messagebox.showerror("Error", "Token is empty")
        return False
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

def check_figma_access(token, file_id):
    url = f"https://api.figma.com/v1/files/{file_id}"
    headers = {"X-Figma-Token": token}

    try:
        response = requests.get(url, headers=headers, timeout=5)
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

    messagebox.showerror("Error", f"Unexpected error: {response.status_code}")
    return False


app = Tk()
app.title("Figma API Integration")
app.geometry("562x450")
app.config(bg="#0f0e17")

canvas = Canvas(app, width=562, height=450, bg='#0f0e17', highlightthickness=0)
canvas.pack(fill='both', expand=True)

canvas.create_text(167, 23, anchor="w", text="Tk Designer", fill="#fffffe", font=("Inter", -36))

canvas.create_text(42, 114, anchor="w", text="Enter your file id", fill="#ffffff", font=("Inter", -20))

entry_1 = Entry(app, bg='#ff8906')
canvas.create_window(45, 151, anchor="nw", window=entry_1, width=304, height=30)

canvas.create_text(42, 213, anchor="w", text="Enter your token access", fill="#ffffff", font=("Inter", -20))

entry_2 = Entry(app, bg='#ff8906')
canvas.create_window(45, 250, anchor="nw", window=entry_2, width=355, height=30)

canvas.create_text(45, 312, anchor="w", text="Choose the output file path", fill="#ffffff", font=("Inter", -20))

entry_3 = Entry(app, bg='#ff8906')
canvas.create_window(48, 349, anchor="nw", window=entry_3, width=304, height=30)


button_id = canvas.create_rectangle(370, 349, 400, 379, fill='#875d5d', outline="black", tags="browse")

text_id = canvas.create_text(385, 364, text="📁", fill="black", font=("Arial", 12), anchor="center", tags="browse")


button_id = canvas.create_oval(120, 399, 294, 451, fill="#c34e4e", outline="black", tags="button")


text_id = canvas.create_text(207, 425, text="Submit", fill="black", font=("Arial", 12), anchor="center", tags="button")

canvas.tag_bind("browse", "<Button-1>", select_file)
canvas.tag_bind("button", "<Button-1>", call_data)

app.resizable(0,0)
app.mainloop()