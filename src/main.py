from tkinter import *
import requests
import json
import os
from collect_parse_json_file import parse
from to_code import transform_json_to_app
from tkinter import filedialog


def select_file(event):
    folder_path = filedialog.askdirectory()
    entry_3.delete(0,END)
    entry_3.insert(0,folder_path)

def call_data(event):
    data = parse(entry_2.get().strip(), entry_1.get().strip(),entry_3.get().strip())
    output_file_path = entry_3.get()
    if output_file_path[0] == "\"" and output_file_path[-1] == "\"":
        output_file_path = output_file_path[1:-1]
    print(output_file_path)
    transform_json_to_app(data,output_file_path.strip(),entry_1.get().strip(),entry_2.get().strip())

app = Tk()
app.title("Figma API Integration")
app.geometry("562x460")
app.config(bg="#0f0e17")

canvas = Canvas(app, width=562, height=460, bg='#0f0e17', highlightthickness=0)
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


button_id = canvas.create_oval(120, 399, 294, 451, fill='#c34e4e', outline="black", tags="button")


text_id = canvas.create_text(207, 425, text="Submit", fill="black", font=("Arial", 12), anchor="center", tags="button")

canvas.tag_bind("browse", "<Button-1>", select_file)
canvas.tag_bind("button", "<Button-1>", call_data)

app.resizable(0,0)
app.mainloop()