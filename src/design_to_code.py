import tkinter as tk
from tkinter import simpledialog

def create_main_window():
    """Create the main application window."""
    root = tk.Tk()
    root.title("Tkinter GUI")
    root.geometry("800x600")

    # Create the main frames (side frame and center frame)
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    side_frame = create_side_frame(main_frame)
    side_frame.pack(side=tk.LEFT, fill=tk.Y)

    center_frame = create_center_frame(main_frame)
    center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    return root, center_frame


def create_side_frame(parent):
    """Create the side frame with buttons."""
    side_frame = tk.Frame(parent, bg="lightyellow", width=200)
    side_frame.pack_propagate(False)  # Prevent resizing

    # Add buttons to the side frame
    button_data = [
        ("Button", "button"),
        ("Entry", "entry"),
        ("Label", "label"),
        ("Text", "text"),
        ("Checkbutton", "checkbutton"),
        ("Radiobutton", "radiobutton"),
        ("Scale", "scale"),
        ("Listbox", "listbox"),
        ("Frame", "frame")
    ]
    for label, item_name in button_data:
        button = tk.Button(side_frame, text=label, command=lambda name=item_name: place_item(name))
        button.pack(pady=10)

    return side_frame


def create_center_frame(parent):
    """Create the center frame for placing items."""
    center_frame = tk.Canvas(parent, bg="lightgreen")
    center_frame.pack(fill=tk.BOTH, expand=True)
    center_frame.bind("<ButtonRelease-1>", on_drop)
    return center_frame


def place_item(item_name):
    """Place an item in the center frame."""
    item = None
    if item_name == "button":
        item = tk.Button(center_frame, text="Button")
    elif item_name == "entry":
        item = tk.Entry(center_frame)
    elif item_name == "label":
        item = tk.Label(center_frame, text="Label")
    elif item_name == "text":
        item = tk.Text(center_frame, width=20, height=5)
    elif item_name == "checkbutton":
        item = tk.Checkbutton(center_frame, text="Checkbutton")
    elif item_name == "radiobutton":
        item = tk.Radiobutton(center_frame, text="Radiobutton", value=1)
    elif item_name == "scale":
        item = tk.Scale(center_frame, from_=0, to=100, orient=tk.HORIZONTAL)
    elif item_name == "listbox":
        item = tk.Listbox(center_frame, height=5)
        for i in range(10):
            item.insert(tk.END, f"Item {i+1}")
    elif item_name == "frame":
        item = tk.Frame(center_frame, bg="lightblue", width=100, height=100)
        item.pack_propagate(False)  # Prevent resizing
    

    # Bind the drag event to the item
    if item:
        item.place(x=100, y=100)  # Set initial position
        item.bind("<Button-1>", lambda event, widget=item: on_drag_start(event, widget))
        item.bind("<B1-Motion>", lambda event, widget=item: on_drag_motion(event, widget))
        item.bind("<ButtonRelease-1>", lambda event, widget=item: on_drop(event, widget))
        item.bind("<Double-1>", lambda event, widget=item: show_property_window(event, widget))  # Double-click event


def on_drag_start(event, widget):
    """Start dragging the widget."""
    widget.drag_data = {'x': event.x, 'y': event.y}


def on_drag_motion(event, widget):
    """Move the widget while dragging."""
    delta_x = event.x - widget.drag_data['x']
    delta_y = event.y - widget.drag_data['y']
    new_x = widget.winfo_x() + delta_x
    new_y = widget.winfo_y() + delta_y
    widget.place(x=new_x, y=new_y)


def on_drop(event, widget=None):
    """Handle drop event (no action needed here)."""
    pass


def show_property_window(event, widget):
    """Show a property window to edit widget properties."""
    # Create a new window for editing properties
    prop_window = tk.Toplevel(root)
    prop_window.title("Edit Properties")

    if isinstance(widget, tk.Button):
        label_text = tk.Label(prop_window, text="Enter new text for Button:")
        label_text.grid(row=0, column=0, padx=10, pady=10)
        entry_text = tk.Entry(prop_window)
        entry_text.insert(0, widget.cget("text"))
        entry_text.grid(row=0, column=1, padx=10, pady=10)

        # Save button
        save_btn = tk.Button(prop_window, text="Save", command=lambda: save_properties(widget, entry_text.get()))
        save_btn.grid(row=1, columnspan=2, pady=10)
    
    elif isinstance(widget, tk.Label):
        label_text = tk.Label(prop_window, text="Enter new text for Label:")
        label_text.grid(row=0, column=0, padx=10, pady=10)
        entry_text = tk.Entry(prop_window)
        entry_text.insert(0, widget.cget("text"))
        entry_text.grid(row=0, column=1, padx=10, pady=10)

        # Save button
        save_btn = tk.Button(prop_window, text="Save", command=lambda: save_properties(widget, entry_text.get()))
        save_btn.grid(row=1, columnspan=2, pady=10)
    
    elif isinstance(widget, tk.Entry):
        label_text = tk.Label(prop_window, text="Enter new text for Entry:")
        label_text.grid(row=0, column=0, padx=10, pady=10)
        entry_text = tk.Entry(prop_window)
        entry_text.insert(0, widget.get())
        entry_text.grid(row=0, column=1, padx=10, pady=10)

        # Save button
        save_btn = tk.Button(prop_window, text="Save", command=lambda: save_properties(widget, entry_text.get()))
        save_btn.grid(row=1, columnspan=2, pady=10)


def save_properties(widget, new_value):
    """Save the updated value to the widget."""
    if isinstance(widget, tk.Button):
        widget.config(text=new_value)
    elif isinstance(widget, tk.Label):
        widget.config(text=new_value)
    elif isinstance(widget, tk.Entry):
        widget.delete(0, tk.END)
        widget.insert(0, new_value)


if __name__ == "__main__":
    root, center_frame = create_main_window()
    root.mainloop()