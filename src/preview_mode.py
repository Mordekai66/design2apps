import tkinter as tk
from tkinter import filedialog, scrolledtext
import subprocess
import os

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            code_area.delete("1.0", tk.END)
            code_area.insert(tk.END, f.read())

def run_preview():
    code = code_area.get("1.0", tk.END)
    with open("temp.py", "w", encoding="utf-8") as f:
        f.write(code)
    subprocess.Popen(["python", "temp.py"], shell=True)

root = tk.Tk()
root.title("Python GUI Preview")
root.geometry("800x600")

btn_frame = tk.Frame(root)
btn_frame.pack(fill="x")

tk.Button(btn_frame, text="Open File", command=open_file).pack(side="left")
tk.Button(btn_frame, text="Run Preview", command=run_preview).pack(side="left")

code_area = scrolledtext.ScrolledText(root, wrap=tk.NONE, font=("Consolas", 12))
code_area.pack(fill="both", expand=True)

root.mainloop()
