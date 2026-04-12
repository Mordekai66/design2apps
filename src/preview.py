from tkinter import Toplevel, Button, Frame
from tkinter import ttk
from tkinter import *

def show_preview(data, on_confirm):
    page = data["document"]["children"][0]
    frame = page["children"][0]
    
    preview_win = Toplevel()
    preview_win.title("Design Preview")
    preview_win.geometry("400x500")
    preview_win.config(bg="#0f0e17")
    
    tree = ttk.Treeview(preview_win)
    tree.pack(fill="both", expand=True, padx=10, pady=10)
    
    root_node = tree.insert("", "end", text=f"Frame: {frame['name']}", open=True)
    
    def add_children(parent_node, elements):
        for el in elements:
            label = f"{el['name']}  [{el['type']}]"
            node = tree.insert(parent_node, "end", text=label, open=True)
            if "children" in el:
                add_children(node, el["children"])
    
    add_children(root_node, frame["children"])

    def on_generate():
        preview_win.destroy()
        on_confirm()

    def on_cancel():
        preview_win.destroy()

    btn_frame = Frame(preview_win, bg="#0f0e17")
    btn_frame.pack(pady=10)

    Button(btn_frame, text="Generate", bg='#c34e4e', fg="black", font=("Arial", 12, "bold"), relief="flat", command=on_generate).pack(side=LEFT, padx=5)

    Button(btn_frame, text="Cancel", bg='#875d5d', fg="black", font=("Arial", 12, "bold"), relief="flat", command=on_cancel).pack(side=LEFT, padx=5)

    preview_win.wait_window()