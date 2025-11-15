# design to json.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import json
import math

class AppDesigner:
    def __init__(self, root):
        self.root = root
        self.root.title("App Designer to Figma Exporter")
        self.root.geometry("1400x850")
        self.root.configure(bg="#1a202c")
        
        # Initialize variables
        self.selected_widget = None
        self.selected_shape = None
        self.drag_data = {"x":0, "y":0, "action": None}
        self.shape_drag_data = {"x":0, "y":0}
        self.widgets_data = []
        self.prop_widgets = []
        self.zoom_level = 1.0
        self.history = []
        self.history_index = -1
        self.frames = []
        self.current_frame_index = 0
        self.grid_visible = True
        
        # Frame dimensions
        self.frame_width_var = tk.IntVar(value=800)
        self.frame_height_var = tk.IntVar(value=600)
        
        # Create UI components
        self.create_frame_settings()
        self.create_toolbar()
        self.create_toolbox()
        self.create_preview_area()
        self.create_properties_panel()
        self.create_frame_management()
        
        # Initialize with one frame
        self.add_frame()
        
        # Save initial state
        self.save_state()

    # ---- UI Creation Methods ----
    def create_frame_settings(self):
        settings_frame = tk.Frame(self.root, bg="#1a202c", height=40)
        settings_frame.pack(side="top", fill="x")
        
        # Frame dimensions
        tk.Label(settings_frame, text="Frame:", bg="#1a202c", fg="#ffffff", 
                 font=("Segoe UI", 10)).pack(side="left", padx=10)
        
        width_entry = tk.Entry(settings_frame, textvariable=self.frame_width_var, width=5)
        width_entry.pack(side="left", padx=2)
        
        tk.Label(settings_frame, text="×", bg="#1a202c", fg="#ffffff", 
                 font=("Segoe UI", 10)).pack(side="left")
        
        height_entry = tk.Entry(settings_frame, textvariable=self.frame_height_var, width=5)
        height_entry.pack(side="left", padx=2)
        
        # Apply button
        apply_btn = tk.Button(settings_frame, text="Apply", command=self.update_frame_dimensions,
                             bg="#4a5568", fg="#ffffff", relief="flat", cursor="hand2")
        apply_btn.pack(side="left", padx=10)
        
        # Preset sizes
        presets_frame = tk.Frame(settings_frame, bg="#1a202c")
        presets_frame.pack(side="left", padx=20)
        
        tk.Label(presets_frame, text="Presets:", bg="#1a202c", fg="#ffffff", 
                 font=("Segoe UI", 10)).pack(side="left")
        
        presets = [
            ("Desktop", 1920, 1080),
            ("Tablet", 768, 1024),
            ("Mobile", 375, 667)
        ]
        
        for name, w, h in presets:
            btn = tk.Button(presets_frame, text=name, 
                           command=lambda w=w, h=h: self.set_frame_dimensions(w, h),
                           bg="#4a5568", fg="#ffffff", relief="flat", cursor="hand2")
            btn.pack(side="left", padx=2)
        
        # Grid toggle
        grid_btn = tk.Button(settings_frame, text="Toggle Grid", command=self.toggle_grid,
                            bg="#4a5568", fg="#ffffff", relief="flat", cursor="hand2")
        grid_btn.pack(side="right", padx=10)

    def create_toolbar(self):
        toolbar_frame = tk.Frame(self.root, bg="#2d3748", height=40)
        toolbar_frame.pack(side="top", fill="x")
        
        # Undo/Redo buttons
        self.undo_button = tk.Button(toolbar_frame, text="↶ Undo", command=self.undo,
                                    bg="#4a5568", fg="#ffffff", relief="flat", cursor="hand2")
        self.undo_button.pack(side="left", padx=5)
        
        self.redo_button = tk.Button(toolbar_frame, text="↷ Redo", command=self.redo,
                                    bg="#4a5568", fg="#ffffff", relief="flat", cursor="hand2")
        self.redo_button.pack(side="left", padx=5)
        
        # Save button
        save_btn = tk.Button(toolbar_frame, text="💾 Save to Figma JSON", command=self.save_to_figma_json,
                            bg="#38a169", fg="#ffffff", relief="flat", cursor="hand2", font=("Segoe UI", 10, "bold"))
        save_btn.pack(side="right", padx=10)

    def create_toolbox(self):
        frame = tk.Frame(self.root, bg="#2d3748", width=220, relief="flat", highlightthickness=0)
        frame.pack(side="left", fill="y")
        
        # Header with gradient effect
        header_frame = tk.Frame(frame, bg="#1a202c", height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        tk.Label(header_frame, text="🛠 Tools", bg="#1a202c", fg="#ffffff", 
                 font=("Segoe UI", 14, "bold")).pack(expand=True)
        
        # Tool categories
        categories = {
            "Basic": [
                ("Button", self.add_button), 
                ("Label", self.add_label), 
                ("Entry", self.add_entry),
                ("Text Area", self.add_textarea),
                ("Checkbox", self.add_checkbox),
                ("Radio Button", self.add_radiobutton)
            ],
            "Media": [
                ("Image", self.add_image_widget),
                ("Video Player", self.add_video_player)
            ],
            "Shapes": [
                ("Rectangle", self.add_rectangle), 
                ("Oval", self.add_oval),
                ("Triangle", self.add_triangle),
                ("Line", self.add_line),
                ("Polygon", self.add_polygon)
            ],
            "Containers": [
                ("Frame", self.add_container),
                ("Card", self.add_card)
            ],
            "Navigation": [
                ("Menu", self.add_menu),
                ("Tabs", self.add_tabs)
            ]
        }
        
        for category, items in categories.items():
            # Category header
            cat_frame = tk.Frame(frame, bg="#2d3748")
            cat_frame.pack(fill="x", padx=10, pady=(10, 5))
            tk.Label(cat_frame, text=category, bg="#2d3748", fg="#a0aec0", 
                     font=("Segoe UI", 10, "bold")).pack(anchor="w")
            
            # Category items
            for txt, cmd in items:
                btn_frame = tk.Frame(frame, bg="#2d3748")
                btn_frame.pack(fill="x", padx=10, pady=2)
                
                btn = tk.Button(btn_frame, text=txt, command=cmd, bg="#4a5568", fg="#ffffff", 
                               relief="flat", font=("Segoe UI", 10), cursor="hand2",
                               activebackground="#718096", activeforeground="#ffffff")
                btn.pack(fill="x", pady=1)
                
                # Hover effect
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#718096"))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#4a5568"))

    def create_preview_area(self):
        # Main container with padding
        preview_container = tk.Frame(self.root, bg="#1a202c", padx=10, pady=10)
        preview_container.pack(side="left", fill="both", expand=True)
        
        # Header with controls
        header_frame = tk.Frame(preview_container, bg="#1a202c", height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📱 Design Area", bg="#1a202c", fg="#ffffff", 
                 font=("Segoe UI", 14, "bold")).pack(side="left", padx=10)
        
        # Zoom controls
        zoom_frame = tk.Frame(header_frame, bg="#1a202c")
        zoom_frame.pack(side="right", padx=10)
        
        tk.Button(zoom_frame, text="-", command=self.zoom_out, bg="#4a5568", fg="#ffffff", 
                 relief="flat", width=2).pack(side="left", padx=2)
        
        self.zoom_label = tk.Label(zoom_frame, text="100%", bg="#1a202c", fg="#ffffff", 
                                  font=("Segoe UI", 10), width=5)
        self.zoom_label.pack(side="left", padx=2)
        
        tk.Button(zoom_frame, text="+", command=self.zoom_in, bg="#4a5568", fg="#ffffff", 
                 relief="flat", width=2).pack(side="left", padx=2)
        
        # Canvas with frame border
        canvas_frame = tk.Frame(preview_container, bg="#2d3748", relief="solid", bd=1)
        canvas_frame.pack(fill="both", expand=True)
        
        self.preview_frame = tk.Frame(canvas_frame, bg="#f7fafc", width=750, height=700)
        self.preview_frame.pack(expand=True)
        
        # Add grid background
        self.shape_canvas = tk.Canvas(self.preview_frame, bg="#f7fafc", highlightthickness=0)
        self.shape_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.shape_canvas.lower("all")
        
        # Bind canvas events
        self.shape_canvas.bind("<Button-1>", self.on_canvas_click)
        self.shape_canvas.bind("<B1-Motion>", self.on_shape_drag)
        self.shape_canvas.bind("<ButtonRelease-1>", self.on_shape_release)
        
        # Add grid background
        self.add_grid_background()

    def create_properties_panel(self):
        self.properties_frame = tk.Frame(self.root, bg="#2d3748", width=280)
        self.properties_frame.pack(side="right", fill="y")
        
        # Header
        header_frame = tk.Frame(self.properties_frame, bg="#1a202c", height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        tk.Label(header_frame, text="⚙️ Properties", bg="#1a202c", fg="#ffffff", 
                 font=("Segoe UI", 14, "bold")).pack(expand=True)
        
        # Content area with scrollbar
        self.properties_canvas = tk.Canvas(self.properties_frame, bg="#2d3748", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.properties_frame, orient="vertical", command=self.properties_canvas.yview)
        self.properties_scrollable_frame = tk.Frame(self.properties_canvas, bg="#2d3748")
        
        self.properties_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.properties_canvas.configure(scrollregion=self.properties_canvas.bbox("all"))
        )
        
        self.properties_canvas.create_window((0, 0), window=self.properties_scrollable_frame, anchor="nw")
        self.properties_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.properties_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_frame_management(self):
        # Frame management panel
        frame_mgmt_frame = tk.Frame(self.root, bg="#1a202c", height=40)
        frame_mgmt_frame.pack(side="bottom", fill="x")
        
        # Previous frame button
        self.prev_frame_btn = tk.Button(
            frame_mgmt_frame, text="◀", command=self.prev_frame,
            bg="#4a5568", fg="#ffffff", relief="flat", width=3
        )
        self.prev_frame_btn.pack(side="left", padx=5)
        
        # Frame selector
        self.frame_selector = ttk.Combobox(frame_mgmt_frame, state="readonly", width=15)
        self.frame_selector.pack(side="left", padx=5)
        self.frame_selector.bind("<<ComboboxSelected>>", self.on_frame_selected)
        
        # Add frame button
        add_frame_btn = tk.Button(
            frame_mgmt_frame, text="+", command=self.add_frame,
            bg="#4a5568", fg="#ffffff", relief="flat", width=3
        )
        add_frame_btn.pack(side="left", padx=5)
        
        # Delete frame button
        self.del_frame_btn = tk.Button(
            frame_mgmt_frame, text="-", command=self.delete_frame,
            bg="#4a5568", fg="#ffffff", relief="flat", width=3
        )
        self.del_frame_btn.pack(side="left", padx=5)
        
        # Next frame button
        self.next_frame_btn = tk.Button(
            frame_mgmt_frame, text="▶", command=self.next_frame,
            bg="#4a5568", fg="#ffffff", relief="flat", width=3
        )
        self.next_frame_btn.pack(side="left", padx=5)

    # ---- Widget Creation Methods ----
    def add_button(self):
        btn = tk.Button(self.preview_frame, text="Button", bg="#ffffff", relief="flat")
        self.make_draggable_and_resizable(btn)
        btn.place(x=100, y=100)
        self.widgets_data.append({"id": id(btn), "type": "Button", "widget": btn})
        self.save_state()

    def add_label(self):
        lbl = tk.Label(self.preview_frame, text="Label", bg="#ffffff")
        self.make_draggable_and_resizable(lbl)
        lbl.place(x=100, y=150)
        self.widgets_data.append({"id": id(lbl), "type": "Label", "widget": lbl})
        self.save_state()

    def add_entry(self):
        entry = tk.Entry(self.preview_frame, relief="flat")
        self.make_draggable_and_resizable(entry, resizable_y=False)
        entry.place(x=100, y=200, width=150)
        self.widgets_data.append({"id": id(entry), "type": "Entry", "widget": entry})
        self.save_state()

    def add_textarea(self):
        textarea = tk.Text(self.preview_frame, height=4, width=20, relief="flat", wrap=tk.WORD)
        self.make_draggable_and_resizable(textarea)
        textarea.place(x=100, y=250, width=200, height=80)
        self.widgets_data.append({"id": id(textarea), "type": "Textarea", "widget": textarea})
        self.save_state()

    def add_checkbox(self):
        var = tk.IntVar()
        cb = tk.Checkbutton(self.preview_frame, text="Checkbox", variable=var, bg="#ffffff")
        self.make_draggable_and_resizable(cb)
        cb.place(x=100, y=350)
        self.widgets_data.append({"id": id(cb), "type": "Checkbox", "widget": cb, "variable": var})
        self.save_state()

    def add_radiobutton(self):
        var = tk.IntVar()
        rb = tk.Radiobutton(self.preview_frame, text="Radio Button", variable=var, value=1, bg="#ffffff")
        self.make_draggable_and_resizable(rb)
        rb.place(x=100, y=400)
        self.widgets_data.append({"id": id(rb), "type": "Radiobutton", "widget": rb, "variable": var})
        self.save_state()

    def add_image_widget(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        if not path:
            return
        img_orig = Image.open(path)
        img = img_orig.resize((150, 100))
        photo = ImageTk.PhotoImage(img)
        lbl = tk.Label(self.preview_frame, image=photo, bg="#ffffff")
        lbl.image = photo
        lbl.img_orig = img_orig
        lbl.image_path = path
        lbl.is_image_widget = True
        self.make_draggable_and_resizable(lbl)
        lbl.place(x=100, y=500, width=150, height=100)
        self.widgets_data.append({"id": id(lbl), "type": "Image", "widget": lbl, "image_path": path})
        self.save_state()

    def add_video_player(self):
        # Create a placeholder for video player
        frame = tk.Frame(self.preview_frame, bg="#000000", relief="solid", bd=2)
        self.make_draggable_and_resizable(frame)
        frame.place(x=100, y=620, width=200, height=120)
        
        # Add play icon
        play_label = tk.Label(frame, text="▶", bg="#000000", fg="#ffffff", font=("Arial", 24))
        play_label.place(relx=0.5, rely=0.5, anchor="center")
        
        self.widgets_data.append({"id": id(frame), "type": "Video", "widget": frame})
        self.save_state()

    def add_rectangle(self):
        rect_id = self.shape_canvas.create_rectangle(50, 50, 150, 100, fill="#4299e1", outline="#2b6cb0", width=2)
        self.widgets_data.append({"id": rect_id, "type": "Rectangle", "coords": [50, 50, 150, 100], "fill": "#4299e1"})
        self.shape_canvas.tag_bind(rect_id, "<Button-1>", self.on_shape_click)
        self.shape_canvas.tag_bind(rect_id, "<B1-Motion>", self.on_shape_drag)
        self.shape_canvas.tag_bind(rect_id, "<ButtonRelease-1>", self.on_shape_release)
        self.save_state()

    def add_oval(self):
        oval_id = self.shape_canvas.create_oval(50, 150, 150, 250, fill="#ed64a6", outline="#b83280", width=2)
        self.widgets_data.append({"id": oval_id, "type": "Oval", "coords": [50, 150, 150, 250], "fill": "#ed64a6"})
        self.shape_canvas.tag_bind(oval_id, "<Button-1>", self.on_shape_click)
        self.shape_canvas.tag_bind(oval_id, "<B1-Motion>", self.on_shape_drag)
        self.shape_canvas.tag_bind(oval_id, "<ButtonRelease-1>", self.on_shape_release)
        self.save_state()

    def add_triangle(self):
        points = [100, 50, 50, 150, 150, 150]
        triangle_id = self.shape_canvas.create_polygon(points, fill="#48bb78", outline="#2f855a", width=2)
        self.widgets_data.append({"id": triangle_id, "type": "Triangle", "points": points, "fill": "#48bb78"})
        self.shape_canvas.tag_bind(triangle_id, "<Button-1>", self.on_shape_click)
        self.shape_canvas.tag_bind(triangle_id, "<B1-Motion>", self.on_shape_drag)
        self.shape_canvas.tag_bind(triangle_id, "<ButtonRelease-1>", self.on_shape_release)
        self.save_state()

    def add_line(self):
        line_id = self.shape_canvas.create_line(50, 300, 200, 300, fill="#000000", width=3)
        self.widgets_data.append({"id": line_id, "type": "Line", "coords": [50, 300, 200, 300], "width": 3})
        self.shape_canvas.tag_bind(line_id, "<Button-1>", self.on_shape_click)
        self.shape_canvas.tag_bind(line_id, "<B1-Motion>", self.on_shape_drag)
        self.shape_canvas.tag_bind(line_id, "<ButtonRelease-1>", self.on_shape_release)
        self.save_state()

    def add_polygon(self):
        # Create a hexagon
        points = []
        cx, cy, r = 100, 400, 40
        for i in range(6):
            angle = 2 * math.pi * i / 6
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            points.extend([x, y])
        
        polygon_id = self.shape_canvas.create_polygon(points, fill="#9f7aea", outline="#6b46c1", width=2)
        self.widgets_data.append({"id": polygon_id, "type": "Polygon", "points": points, "fill": "#9f7aea"})
        self.shape_canvas.tag_bind(polygon_id, "<Button-1>", self.on_shape_click)
        self.shape_canvas.tag_bind(polygon_id, "<B1-Motion>", self.on_shape_drag)
        self.shape_canvas.tag_bind(polygon_id, "<ButtonRelease-1>", self.on_shape_release)
        self.save_state()

    def add_container(self):
        container = tk.Frame(self.preview_frame, bg="#e2e8f0", relief="solid", bd=1)
        self.make_draggable_and_resizable(container)
        container.place(x=300, y=100, width=300, height=200)
        
        # Add a label to identify it
        label = tk.Label(container, text="Container", bg="#e2e8f0")
        label.place(relx=0.5, rely=0.1, anchor="center")
        
        self.widgets_data.append({"id": id(container), "type": "Container", "widget": container})
        self.save_state()

    def add_card(self):
        card = tk.Frame(self.preview_frame, bg="#ffffff", relief="solid", bd=1)
        self.make_draggable_and_resizable(card)
        card.place(x=300, y=350, width=250, height=150)
        
        # Add a shadow effect
        shadow = tk.Frame(card, bg="#cbd5e0", height=5)
        shadow.pack(side="bottom", fill="x")
        
        # Add a label to identify it
        label = tk.Label(card, text="Card", bg="#ffffff", font=("Arial", 12, "bold"))
        label.place(relx=0.5, rely=0.3, anchor="center")
        
        # Add some sample text
        text = tk.Label(card, text="This is a sample card", bg="#ffffff")
        text.place(relx=0.5, rely=0.6, anchor="center")
        
        self.widgets_data.append({"id": id(card), "type": "Card", "widget": card})
        self.save_state()

    def add_menu(self):
        menu_frame = tk.Frame(self.preview_frame, bg="#4a5568", relief="flat")
        self.make_draggable_and_resizable(menu_frame, resizable_y=False)
        menu_frame.place(x=300, y=550, width=300, height=40)
        
        # Add menu items
        menu_items = ["Home", "About", "Services", "Contact"]
        for i, item in enumerate(menu_items):
            btn = tk.Button(menu_frame, text=item, bg="#4a5568", fg="#ffffff", 
                           relief="flat", font=("Arial", 10))
            btn.pack(side="left", padx=10, pady=5)
        
        self.widgets_data.append({"id": id(menu_frame), "type": "Menu", "widget": menu_frame})
        self.save_state()

    def add_tabs(self):
        tabs_frame = tk.Frame(self.preview_frame, bg="#ffffff", relief="solid", bd=1)
        self.make_draggable_and_resizable(tabs_frame)
        tabs_frame.place(x=650, y=100, width=300, height=200)
        
        # Tab headers
        headers_frame = tk.Frame(tabs_frame, bg="#e2e8f0", height=30)
        headers_frame.pack(side="top", fill="x")
        
        # Tab buttons
        tab1 = tk.Button(headers_frame, text="Tab 1", bg="#cbd5e0", relief="flat", font=("Arial", 10))
        tab1.pack(side="left", padx=5, pady=2)
        
        tab2 = tk.Button(headers_frame, text="Tab 2", bg="#e2e8f0", relief="flat", font=("Arial", 10))
        tab2.pack(side="left", padx=5, pady=2)
        
        tab3 = tk.Button(headers_frame, text="Tab 3", bg="#e2e8f0", relief="flat", font=("Arial", 10))
        tab3.pack(side="left", padx=5, pady=2)
        
        # Tab content
        content_frame = tk.Frame(tabs_frame, bg="#ffffff")
        content_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        
        content_label = tk.Label(content_frame, text="Tab 1 Content", bg="#ffffff")
        content_label.pack()
        
        self.widgets_data.append({"id": id(tabs_frame), "type": "Tabs", "widget": tabs_frame})
        self.save_state()

    # ---- Drag and Resize Functionality ----
    def make_draggable_and_resizable(self, widget, resizable_x=True, resizable_y=True):
        widget.bind("<Button-1>", lambda e, w=widget: self.on_widget_click(e, w))
        widget.bind("<B1-Motion>", lambda e, w=widget: self.on_widget_drag(e, w))
        widget.bind("<ButtonRelease-1>", self.on_widget_release)
        widget.bind("<Motion>", lambda e, w=widget: self.on_widget_hover(e, w))
        widget.resizable_x = resizable_x
        widget.resizable_y = resizable_y

    def on_widget_click(self, event, widget):
        self.selected_widget = widget
        self.selected_shape = None  # Clear shape selection
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.drag_data["action"] = self.get_action(event, widget)
        self.show_properties(widget)

    def on_widget_drag(self, event, widget):
        action = self.drag_data["action"]
        if action == "move":
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            widget.place_configure(x=widget.winfo_x() + dx, y=widget.winfo_y() + dy)
            self.update_widget_position_in_data(widget)
        elif action == "resize":
            new_w = widget.winfo_width()
            new_h = widget.winfo_height()
            if widget.resizable_x:
                new_w = max(widget.winfo_width() + (event.x - self.drag_data["x"]), 20)
            if widget.resizable_y:
                new_h = max(widget.winfo_height() + (event.y - self.drag_data["y"]), 20)
            widget.place_configure(width=new_w, height=new_h)
            if getattr(widget, "is_image_widget", False):
                self.resize_image(widget, new_w, new_h)
            self.drag_data["x"], self.drag_data["y"] = event.x, event.y
            self.update_widget_size_in_data(widget)

    def on_widget_release(self, event):
        self.drag_data["action"] = None
        self.save_state()

    def on_widget_hover(self, event, widget):
        if (widget.resizable_x and abs(event.x - widget.winfo_width()) <= 5) and (widget.resizable_y and abs(event.y - widget.winfo_height()) <= 5):
            widget.config(cursor="size_nw_se")
        else:
            widget.config(cursor="fleur")

    def get_action(self, event, widget):
        if (widget.resizable_x and abs(event.x - widget.winfo_width()) <= 5) and (widget.resizable_y and abs(event.y - widget.winfo_height()) <= 5):
            return "resize"
        return "move"

    def update_widget_position_in_data(self, widget):
        for item in self.widgets_data:
            if item.get("widget") == widget:
                item["x"] = widget.winfo_x()
                item["y"] = widget.winfo_y()
                break

    def update_widget_size_in_data(self, widget):
        for item in self.widgets_data:
            if item.get("widget") == widget:
                item["width"] = widget.winfo_width()
                item["height"] = widget.winfo_height()
                break

    def resize_image(self, widget, new_w, new_h):
        img_orig = widget.img_orig
        img_resized = img_orig.resize((int(new_w), int(new_h)), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img_resized)
        widget.config(image=photo)
        widget.image = photo

    # ---- Shape Manipulation ----
    def on_canvas_click(self, event):
        # Check if we clicked on empty space (not on a widget or shape)
        # find_overlapping is more reliable than find_closest for detecting empty space
        clicked_items = self.shape_canvas.find_overlapping(event.x-1, event.y-1, event.x+1, event.y+1)
        
        if not clicked_items:
            # Clear any current selection
            self.selected_widget = None
            self.selected_shape = None
            # Show page properties
            self.show_page_properties()
        else:
            # If a shape was clicked, the existing on_shape_click will handle it
            pass

    def on_shape_click(self, event):
        shape_id = self.shape_canvas.find_closest(event.x, event.y)[0]
        self.selected_shape = shape_id
        self.selected_widget = None  # Clear widget selection
        self.shape_drag_data["x"] = event.x
        self.shape_drag_data["y"] = event.y

        # Determine action based on shape type
        shape_type = None
        for item in self.widgets_data:
            if item["id"] == shape_id:
                shape_type = item["type"]
                break
        
        if shape_type == "Line":
            # For lines, check if near either endpoint
            coords = self.shape_canvas.coords(shape_id)
            x1, y1, x2, y2 = coords
            margin = 10
            
            if abs(event.x - x1) <= margin and abs(event.y - y1) <= margin:
                self.drag_data["action"] = "resize_line_start"
            elif abs(event.x - x2) <= margin and abs(event.y - y2) <= margin:
                self.drag_data["action"] = "resize_line_end"
            else:
                self.drag_data["action"] = "move_shape"
        else:
            # For other shapes, check if near the bottom-right corner for resizing
            coords = self.shape_canvas.coords(shape_id)
            if shape_type in ("Rectangle", "Oval"):
                x1, y1, x2, y2 = coords
                margin = 10
                if abs(event.x - x2) <= margin and abs(event.y - y2) <= margin:
                    self.drag_data["action"] = "resize_shape"
                else:
                    self.drag_data["action"] = "move_shape"
            elif shape_type in ("Triangle", "Polygon"):
                # For polygons, check if near any point
                points = coords
                margin = 10
                for i in range(0, len(points), 2):
                    if abs(event.x - points[i]) <= margin and abs(event.y - points[i+1]) <= margin:
                        self.drag_data["action"] = f"resize_point_{i//2}"
                        break
                else:
                    self.drag_data["action"] = "move_shape"
        
        self.show_shape_properties(shape_id)

    def on_shape_drag(self, event):
        if self.selected_shape is None:
            return
        action = self.drag_data.get("action")
        dx = event.x - self.shape_drag_data["x"]
        dy = event.y - self.shape_drag_data["y"]

        # Get shape type
        shape_type = None
        for item in self.widgets_data:
            if item["id"] == self.selected_shape:
                shape_type = item["type"]
                break
        
        if action == "move_shape":
            self.shape_canvas.move(self.selected_shape, dx, dy)
        elif action == "resize_shape" and shape_type in ("Rectangle", "Oval"):
            coords = self.shape_canvas.coords(self.selected_shape)
            x1, y1, x2, y2 = coords
            new_x2 = max(x2 + dx, x1 + 10)
            new_y2 = max(y2 + dy, y1 + 10)
            self.shape_canvas.coords(self.selected_shape, x1, y1, new_x2, new_y2)
        elif action == "resize_line_start" and shape_type == "Line":
            coords = self.shape_canvas.coords(self.selected_shape)
            x1, y1, x2, y2 = coords
            self.shape_canvas.coords(self.selected_shape, x1 + dx, y1 + dy, x2, y2)
        elif action == "resize_line_end" and shape_type == "Line":
            coords = self.shape_canvas.coords(self.selected_shape)
            x1, y1, x2, y2 = coords
            self.shape_canvas.coords(self.selected_shape, x1, y1, x2 + dx, y2 + dy)
        elif action and action.startswith("resize_point_") and shape_type in ("Triangle", "Polygon"):
            point_index = int(action.split("_")[-1])
            coords = self.shape_canvas.coords(self.selected_shape)
            # Update the specific point
            coords[point_index * 2] += dx
            coords[point_index * 2 + 1] += dy
            self.shape_canvas.coords(self.selected_shape, *coords)
            
            # Update the data
            for item in self.widgets_data:
                if item["id"] == self.selected_shape:
                    item["points"] = coords.copy()
                    break

        self.shape_drag_data["x"] = event.x
        self.shape_drag_data["y"] = event.y

        # Update data
        for item in self.widgets_data:
            if item["id"] == self.selected_shape:
                if shape_type in ("Rectangle", "Oval"):
                    item["coords"] = self.shape_canvas.coords(self.selected_shape)
                elif shape_type == "Line":
                    item["coords"] = self.shape_canvas.coords(self.selected_shape)
                break

    def on_shape_release(self, event):
        self.selected_shape = None
        self.drag_data["action"] = None
        self.save_state()

    # ---- Properties Panel ----
    def clear_properties_panel(self):
        """Clear all widgets from the properties panel"""
        for widget in self.properties_scrollable_frame.winfo_children():
            widget.destroy()
        self.prop_widgets.clear()

    def show_page_properties(self):
        # Clear previous properties
        self.clear_properties_panel()
        
        # Get current frame data
        current_frame = self.frames[self.current_frame_index]
        
        # Page properties
        self.create_property_field("Page Name:", current_frame["name"], 
                              lambda e: self.update_page_property("name", e.widget.get()))
        
        self.create_property_field("Width:", current_frame["width"], 
                              lambda e: self.update_page_property("width", int(e.widget.get())))
        
        self.create_property_field("Height:", current_frame["height"], 
                              lambda e: self.update_page_property("height", int(e.widget.get())))
        
        self.create_property_field("Background:", current_frame["background"], 
                              lambda e: self.update_page_property("background", e.widget.get()))

    def update_page_property(self, property_name, value):
        try:
            # Update frame data
            self.frames[self.current_frame_index][property_name] = value
            
            # Apply changes to UI
            if property_name == "name":
                # Update frame selector
                frame_names = [f["name"] for f in self.frames]
                self.frame_selector['values'] = frame_names
                self.frame_selector.current(self.current_frame_index)
            elif property_name == "width":
                self.frame_width_var.set(value)
                self.update_frame_dimensions()
            elif property_name == "height":
                self.frame_height_var.set(value)
                self.update_frame_dimensions()
            elif property_name == "background":
                self.preview_frame.configure(bg=value)
                self.shape_canvas.configure(bg=value)
            
            self.save_state()
        except:
            pass

    def show_properties(self, widget):
        # Clear previous properties
        self.clear_properties_panel()
        
        # Get widget type
        widget_type = None
        for item in self.widgets_data:
            if item.get("widget") == widget:
                widget_type = item["type"]
                break
        
        # Common properties
        x = widget.winfo_x()
        y = widget.winfo_y()
        width = widget.winfo_width()
        height = widget.winfo_height()
        
        # Position and size properties
        self.create_property_field("X Position:", x, 
                                  lambda e: self.update_widget_position(widget, "x", int(e.widget.get())))
        
        self.create_property_field("Y Position:", y, 
                                  lambda e: self.update_widget_position(widget, "y", int(e.widget.get())))
        
        self.create_property_field("Width:", width, 
                                  lambda e: self.update_widget_size(widget, "width", int(e.widget.get())))
        
        self.create_property_field("Height:", height, 
                                  lambda e: self.update_widget_size(widget, "height", int(e.widget.get())))
        
        # Type-specific properties
        if widget_type == "Button":
            text = widget.cget("text")
            bg = widget.cget("bg")
            fg = widget.cget("fg")
            
            self.create_property_field("Text:", text, 
                                      lambda e: self.update_widget_property(widget, "text", e.widget.get()))
            
            self.create_property_field("Background:", bg, 
                                      lambda e: self.update_widget_property(widget, "bg", e.widget.get()))
            
            self.create_property_field("Text Color:", fg, 
                                      lambda e: self.update_widget_property(widget, "fg", e.widget.get()))
        
        elif widget_type == "Label":
            text = widget.cget("text")
            bg = widget.cget("bg")
            fg = widget.cget("fg")
            
            self.create_property_field("Text:", text, 
                                      lambda e: self.update_widget_property(widget, "text", e.widget.get()))
            
            self.create_property_field("Background:", bg, 
                                      lambda e: self.update_widget_property(widget, "bg", e.widget.get()))
            
            self.create_property_field("Text Color:", fg, 
                                      lambda e: self.update_widget_property(widget, "fg", e.widget.get()))
        
        elif widget_type == "Entry":
            bg = widget.cget("bg")
            fg = widget.cget("fg")
            
            self.create_property_field("Background:", bg, 
                                      lambda e: self.update_widget_property(widget, "bg", e.widget.get()))
            
            self.create_property_field("Text Color:", fg, 
                                      lambda e: self.update_widget_property(widget, "fg", e.widget.get()))
        
        elif widget_type == "Textarea":
            bg = widget.cget("bg")
            fg = widget.cget("fg")
            
            self.create_property_field("Background:", bg, 
                                      lambda e: self.update_widget_property(widget, "bg", e.widget.get()))
            
            self.create_property_field("Text Color:", fg, 
                                      lambda e: self.update_widget_property(widget, "fg", e.widget.get()))
        
        elif widget_type == "Checkbox":
            text = widget.cget("text")
            bg = widget.cget("bg")
            fg = widget.cget("fg")
            
            self.create_property_field("Text:", text, 
                                      lambda e: self.update_widget_property(widget, "text", e.widget.get()))
            
            self.create_property_field("Background:", bg, 
                                      lambda e: self.update_widget_property(widget, "bg", e.widget.get()))
            
            self.create_property_field("Text Color:", fg, 
                                      lambda e: self.update_widget_property(widget, "fg", e.widget.get()))
        
        elif widget_type == "Radiobutton":
            text = widget.cget("text")
            bg = widget.cget("bg")
            fg = widget.cget("fg")
            
            self.create_property_field("Text:", text, 
                                      lambda e: self.update_widget_property(widget, "text", e.widget.get()))
            
            self.create_property_field("Background:", bg, 
                                      lambda e: self.update_widget_property(widget, "bg", e.widget.get()))
            
            self.create_property_field("Text Color:", fg, 
                                      lambda e: self.update_widget_property(widget, "fg", e.widget.get()))
        
        elif widget_type == "Image":
            path = getattr(widget, "image_path", "")
            self.create_property_field("Image Path:", path, 
                                      lambda e: self.update_image_path(widget, e.widget.get()))
        
        elif widget_type in ("Container", "Card", "Menu", "Tabs", "Video"):
            bg = widget.cget("bg")
            self.create_property_field("Background:", bg, 
                                      lambda e: self.update_widget_property(widget, "bg", e.widget.get()))

    def create_property_field(self, label_text, initial_value, update_func):
        """Create a property field with label and entry"""
        frame = tk.Frame(self.properties_scrollable_frame, bg="#2d3748")
        frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(frame, text=label_text, bg="#2d3748", fg="#ffffff", 
                 font=("Segoe UI", 10)).pack(anchor="w")
        
        var = tk.StringVar(value=str(initial_value))
        entry = tk.Entry(frame, textvariable=var, bg="#4a5568", fg="#ffffff", 
                         relief="flat", font=("Segoe UI", 10))
        entry.pack(fill="x", pady=(2, 0))
        
        # Bind to update function
        entry.bind("<KeyRelease>", update_func)
        
        # Add to prop_widgets list for tracking
        self.prop_widgets.append(entry)
        
        return var

    def update_widget_property(self, widget, property_name, value):
        """Update a widget property and save state"""
        try:
            widget.config(**{property_name: value})
            self.save_state()
        except:
            pass

    def update_widget_position(self, widget, axis, value):
        """Update widget position and save state"""
        try:
            if axis == "x":
                widget.place_configure(x=value)
            else:
                widget.place_configure(y=value)
            self.update_widget_position_in_data(widget)
            self.save_state()
        except:
            pass

    def update_widget_size(self, widget, dimension, value):
        """Update widget size and save state"""
        try:
            if dimension == "width":
                widget.place_configure(width=max(value, 20))
            else:
                widget.place_configure(height=max(value, 20))
            
            # Update image if needed
            if getattr(widget, "is_image_widget", False):
                self.resize_image(widget, widget.winfo_width(), widget.winfo_height())
            
            self.update_widget_size_in_data(widget)
            self.save_state()
        except:
            pass

    def update_image_path(self, widget, path):
        """Update image path and reload image"""
        try:
            if path:
                img_orig = Image.open(path)
                img = img_orig.resize((widget.winfo_width(), widget.winfo_height()))
                photo = ImageTk.PhotoImage(img)
                widget.config(image=photo)
                widget.image = photo
                widget.img_orig = img_orig
                widget.image_path = path
                
                # Update data
                for item in self.widgets_data:
                    if item.get("widget") == widget:
                        item["image_path"] = path
                        break
                
                self.save_state()
        except:
            pass

    def show_shape_properties(self, shape_id):
        # Clear previous properties
        self.clear_properties_panel()
        
        shape_item = None
        for item in self.widgets_data:
            if item["id"] == shape_id:
                shape_item = item
                break
        if not shape_item:
            return

        shape_type = shape_item["type"]
        
        # Common properties
        self.create_property_field("Fill Color:", shape_item.get("fill", "#000000"), 
                                  lambda e: self.update_shape_property(shape_id, "fill", e.widget.get()))
        
        # Type-specific properties
        if shape_type == "Rectangle":
            coords = shape_item.get("coords", [0,0,0,0])
            x1, y1, x2, y2 = coords
            
            self.create_property_field("X1:", x1, 
                                      lambda e: self.update_shape_coord(shape_id, 0, int(e.widget.get())))
            
            self.create_property_field("Y1:", y1, 
                                      lambda e: self.update_shape_coord(shape_id, 1, int(e.widget.get())))
            
            self.create_property_field("X2:", x2, 
                                      lambda e: self.update_shape_coord(shape_id, 2, int(e.widget.get())))
            
            self.create_property_field("Y2:", y2, 
                                      lambda e: self.update_shape_coord(shape_id, 3, int(e.widget.get())))
        
        elif shape_type == "Oval":
            coords = shape_item.get("coords", [0,0,0,0])
            x1, y1, x2, y2 = coords
            
            self.create_property_field("X1:", x1, 
                                      lambda e: self.update_shape_coord(shape_id, 0, int(e.widget.get())))
            
            self.create_property_field("Y1:", y1, 
                                      lambda e: self.update_shape_coord(shape_id, 1, int(e.widget.get())))
            
            self.create_property_field("X2:", x2, 
                                      lambda e: self.update_shape_coord(shape_id, 2, int(e.widget.get())))
            
            self.create_property_field("Y2:", y2, 
                                      lambda e: self.update_shape_coord(shape_id, 3, int(e.widget.get())))
        
        elif shape_type == "Triangle":
            points = shape_item.get("points", [0,0,0,0,0,0])
            
            self.create_property_field("Point 1 X:", points[0], 
                                      lambda e: self.update_shape_point(shape_id, 0, int(e.widget.get())))
            
            self.create_property_field("Point 1 Y:", points[1], 
                                      lambda e: self.update_shape_point(shape_id, 1, int(e.widget.get())))
            
            self.create_property_field("Point 2 X:", points[2], 
                                      lambda e: self.update_shape_point(shape_id, 2, int(e.widget.get())))
            
            self.create_property_field("Point 2 Y:", points[3], 
                                      lambda e: self.update_shape_point(shape_id, 3, int(e.widget.get())))
            
            self.create_property_field("Point 3 X:", points[4], 
                                      lambda e: self.update_shape_point(shape_id, 4, int(e.widget.get())))
            
            self.create_property_field("Point 3 Y:", points[5], 
                                      lambda e: self.update_shape_point(shape_id, 5, int(e.widget.get())))
        
        elif shape_type == "Line":
            coords = shape_item.get("coords", [0,0,0,0])
            x1, y1, x2, y2 = coords
            width = shape_item.get("width", 3)
            
            self.create_property_field("X1:", x1, 
                                      lambda e: self.update_shape_coord(shape_id, 0, int(e.widget.get())))
            
            self.create_property_field("Y1:", y1, 
                                      lambda e: self.update_shape_coord(shape_id, 1, int(e.widget.get())))
            
            self.create_property_field("X2:", x2, 
                                      lambda e: self.update_shape_coord(shape_id, 2, int(e.widget.get())))
            
            self.create_property_field("Y2:", y2, 
                                      lambda e: self.update_shape_coord(shape_id, 3, int(e.widget.get())))
            
            self.create_property_field("Width:", width, 
                                      lambda e: self.update_line_width(shape_id, int(e.widget.get())))
        
        elif shape_type == "Polygon":
            points = shape_item.get("points", [])
            for i in range(0, len(points), 2):
                point_num = i // 2 + 1
                self.create_property_field(f"Point {point_num} X:", points[i], 
                                          lambda e, idx=i: self.update_shape_point(shape_id, idx, int(e.widget.get())))
                
                self.create_property_field(f"Point {point_num} Y:", points[i+1], 
                                          lambda e, idx=i+1: self.update_shape_point(shape_id, idx, int(e.widget.get())))

    def update_shape_property(self, shape_id, property_name, value):
        """Update a shape property and save state"""
        try:
            for item in self.widgets_data:
                if item["id"] == shape_id:
                    item[property_name] = value
                    self.shape_canvas.itemconfig(shape_id, fill=value)
                    self.save_state()
                    break
        except:
            pass

    def update_shape_coord(self, shape_id, coord_index, value):
        """Update a shape coordinate and save state"""
        try:
            for item in self.widgets_data:
                if item["id"] == shape_id:
                    coords = item["coords"].copy()
                    coords[coord_index] = value
                    self.shape_canvas.coords(shape_id, *coords)
                    item["coords"] = coords
                    self.save_state()
                    break
        except:
            pass

    def update_shape_point(self, shape_id, point_index, value):
        """Update a polygon/triangle point and save state"""
        try:
            for item in self.widgets_data:
                if item["id"] == shape_id:
                    points = item["points"].copy()
                    points[point_index] = value
                    self.shape_canvas.coords(shape_id, *points)
                    item["points"] = points
                    self.save_state()
                    break
        except:
            pass

    def update_line_width(self, shape_id, width):
        """Update line width and save state"""
        try:
            for item in self.widgets_data:
                if item["id"] == shape_id:
                    item["width"] = width
                    self.shape_canvas.itemconfig(shape_id, width=width)
                    self.save_state()
                    break
        except:
            pass

    # ---- Frame Management ----
    def add_frame(self):
        frame_index = len(self.frames)
        frame_name = f"Frame {frame_index + 1}"
        
        # Create new frame data
        new_frame = {
            "id": f"frame_{frame_index}",
            "name": frame_name,
            "width": self.frame_width_var.get(),
            "height": self.frame_height_var.get(),
            "widgets": [],
            "background": "#ffffff"
        }
        
        # Add to frames list
        self.frames.append(new_frame)
        
        # Update selector
        frame_names = [f["name"] for f in self.frames]
        self.frame_selector['values'] = frame_names
        self.frame_selector.current(frame_index)
        
        # Switch to new frame
        self.current_frame_index = frame_index
        self.load_frame(frame_index)
        
        # Update buttons
        self.update_frame_buttons()

    def delete_frame(self):
        if len(self.frames) <= 1:
            messagebox.showwarning("Cannot Delete", "You must have at least one frame.")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Delete frame '{self.frames[self.current_frame_index]['name']}'?"):
            return
        
        # Remove current frame
        self.frames.pop(self.current_frame_index)
        
        # Adjust current frame index
        if self.current_frame_index >= len(self.frames):
            self.current_frame_index = len(self.frames) - 1
        
        # Update selector
        frame_names = [f["name"] for f in self.frames]
        self.frame_selector['values'] = frame_names
        self.frame_selector.current(self.current_frame_index)
        
        # Load frame
        self.load_frame(self.current_frame_index)
        
        # Update buttons
        self.update_frame_buttons()

    def prev_frame(self):
        if self.current_frame_index > 0:
            self.save_current_frame()
            self.current_frame_index -= 1
            self.frame_selector.current(self.current_frame_index)
            self.load_frame(self.current_frame_index)
            self.update_frame_buttons()

    def next_frame(self):
        if self.current_frame_index < len(self.frames) - 1:
            self.save_current_frame()
            self.current_frame_index += 1
            self.frame_selector.current(self.current_frame_index)
            self.load_frame(self.current_frame_index)
            self.update_frame_buttons()

    def on_frame_selected(self, event):
        self.save_current_frame()
        self.current_frame_index = self.frame_selector.current()
        self.load_frame(self.current_frame_index)
        self.update_frame_buttons()

    def load_frame(self, frame_index):
        # Clear current widgets
        for item in self.widgets_data:
            if "widget" in item:
                item["widget"].destroy()
            elif item["type"] in ("Rectangle", "Oval", "Triangle", "Line", "Polygon"):
                self.shape_canvas.delete(item["id"])
        
        self.widgets_data.clear()
        
        # Clear properties panel
        self.clear_properties_panel()
        
        # Load frame data
        frame = self.frames[frame_index]
        
        # Set frame dimensions
        self.frame_width_var.set(frame["width"])
        self.frame_height_var.set(frame["height"])
        self.update_frame_dimensions()
        
        # Set background color
        self.preview_frame.configure(bg=frame["background"])
        self.shape_canvas.configure(bg=frame["background"])
        
        # Load widgets
        for widget_data in frame["widgets"]:
            widget_type = widget_data["type"]
            
            if widget_type == "Button":
                btn = tk.Button(self.preview_frame, text=widget_data.get("text", "Button"), 
                               bg=widget_data.get("bg", "#ffffff"), 
                               fg=widget_data.get("fg", "#000000"), relief="flat")
                self.make_draggable_and_resizable(btn)
                btn.place(x=widget_data["x"], y=widget_data["y"], 
                         width=widget_data["width"], height=widget_data["height"])
                self.widgets_data.append({"id": id(btn), "type": "Button", "widget": btn})
            
            elif widget_type == "Label":
                lbl = tk.Label(self.preview_frame, text=widget_data.get("text", "Label"), 
                              bg=widget_data.get("bg", "#ffffff"), 
                              fg=widget_data.get("fg", "#000000"))
                self.make_draggable_and_resizable(lbl)
                lbl.place(x=widget_data["x"], y=widget_data["y"], 
                         width=widget_data["width"], height=widget_data["height"])
                self.widgets_data.append({"id": id(lbl), "type": "Label", "widget": lbl})
            
            elif widget_type == "Entry":
                entry = tk.Entry(self.preview_frame, bg=widget_data.get("bg", "#ffffff"), 
                                fg=widget_data.get("fg", "#000000"), relief="flat")
                self.make_draggable_and_resizable(entry, resizable_y=False)
                entry.place(x=widget_data["x"], y=widget_data["y"], 
                           width=widget_data["width"])
                self.widgets_data.append({"id": id(entry), "type": "Entry", "widget": entry})
            
            elif widget_type == "Textarea":
                textarea = tk.Text(self.preview_frame, bg=widget_data.get("bg", "#ffffff"), 
                                  fg=widget_data.get("fg", "#000000"), relief="flat", wrap=tk.WORD)
                self.make_draggable_and_resizable(textarea)
                textarea.place(x=widget_data["x"], y=widget_data["y"], 
                              width=widget_data["width"], height=widget_data["height"])
                self.widgets_data.append({"id": id(textarea), "type": "Textarea", "widget": textarea})
            
            elif widget_type == "Checkbox":
                var = tk.IntVar()
                cb = tk.Checkbutton(self.preview_frame, text=widget_data.get("text", "Checkbox"), 
                                   variable=var, bg=widget_data.get("bg", "#ffffff"), 
                                   fg=widget_data.get("fg", "#000000"))
                self.make_draggable_and_resizable(cb)
                cb.place(x=widget_data["x"], y=widget_data["y"], 
                         width=widget_data["width"], height=widget_data["height"])
                self.widgets_data.append({"id": id(cb), "type": "Checkbox", "widget": cb, "variable": var})
            
            elif widget_type == "Radiobutton":
                var = tk.IntVar()
                rb = tk.Radiobutton(self.preview_frame, text=widget_data.get("text", "Radio Button"), 
                                   variable=var, value=1, bg=widget_data.get("bg", "#ffffff"), 
                                   fg=widget_data.get("fg", "#000000"))
                self.make_draggable_and_resizable(rb)
                rb.place(x=widget_data["x"], y=widget_data["y"], 
                         width=widget_data["width"], height=widget_data["height"])
                self.widgets_data.append({"id": id(rb), "type": "Radiobutton", "widget": rb, "variable": var})
            
            elif widget_type == "Image":
                path = widget_data.get("image_path", "")
                if path:
                    try:
                        img_orig = Image.open(path)
                        img = img_orig.resize((widget_data["width"], widget_data["height"]))
                        photo = ImageTk.PhotoImage(img)
                        lbl = tk.Label(self.preview_frame, image=photo, bg=widget_data.get("bg", "#ffffff"))
                        lbl.image = photo
                        lbl.img_orig = img_orig
                        lbl.image_path = path
                        lbl.is_image_widget = True
                        self.make_draggable_and_resizable(lbl)
                        lbl.place(x=widget_data["x"], y=widget_data["y"], 
                                 width=widget_data["width"], height=widget_data["height"])
                        self.widgets_data.append({"id": id(lbl), "type": "Image", "widget": lbl, "image_path": path})
                    except:
                        pass
            
            elif widget_type == "Video":
                frame = tk.Frame(self.preview_frame, bg=widget_data.get("bg", "#000000"), relief="solid", bd=2)
                self.make_draggable_and_resizable(frame)
                frame.place(x=widget_data["x"], y=widget_data["y"], 
                           width=widget_data["width"], height=widget_data["height"])
                
                # Add play icon
                play_label = tk.Label(frame, text="▶", bg="#000000", fg="#ffffff", font=("Arial", 24))
                play_label.place(relx=0.5, rely=0.5, anchor="center")
                
                self.widgets_data.append({"id": id(frame), "type": "Video", "widget": frame})
            
            elif widget_type == "Rectangle":
                rect_id = self.shape_canvas.create_rectangle(
                    widget_data["coords"][0], widget_data["coords"][1], 
                    widget_data["coords"][2], widget_data["coords"][3], 
                    fill=widget_data.get("fill", "#4299e1"), outline="#2b6cb0", width=2)
                self.widgets_data.append({"id": rect_id, "type": "Rectangle", "coords": widget_data["coords"], "fill": widget_data.get("fill", "#4299e1")})
                self.shape_canvas.tag_bind(rect_id, "<Button-1>", self.on_shape_click)
                self.shape_canvas.tag_bind(rect_id, "<B1-Motion>", self.on_shape_drag)
                self.shape_canvas.tag_bind(rect_id, "<ButtonRelease-1>", self.on_shape_release)
            
            elif widget_type == "Oval":
                oval_id = self.shape_canvas.create_oval(
                    widget_data["coords"][0], widget_data["coords"][1], 
                    widget_data["coords"][2], widget_data["coords"][3], 
                    fill=widget_data.get("fill", "#ed64a6"), outline="#b83280", width=2)
                self.widgets_data.append({"id": oval_id, "type": "Oval", "coords": widget_data["coords"], "fill": widget_data.get("fill", "#ed64a6")})
                self.shape_canvas.tag_bind(oval_id, "<Button-1>", self.on_shape_click)
                self.shape_canvas.tag_bind(oval_id, "<B1-Motion>", self.on_shape_drag)
                self.shape_canvas.tag_bind(oval_id, "<ButtonRelease-1>", self.on_shape_release)
            
            elif widget_type == "Triangle":
                triangle_id = self.shape_canvas.create_polygon(
                    widget_data["points"], fill=widget_data.get("fill", "#48bb78"), outline="#2f855a", width=2)
                self.widgets_data.append({"id": triangle_id, "type": "Triangle", "points": widget_data["points"], "fill": widget_data.get("fill", "#48bb78")})
                self.shape_canvas.tag_bind(triangle_id, "<Button-1>", self.on_shape_click)
                self.shape_canvas.tag_bind(triangle_id, "<B1-Motion>", self.on_shape_drag)
                self.shape_canvas.tag_bind(triangle_id, "<ButtonRelease-1>", self.on_shape_release)
            
            elif widget_type == "Line":
                line_id = self.shape_canvas.create_line(
                    widget_data["coords"][0], widget_data["coords"][1], 
                    widget_data["coords"][2], widget_data["coords"][3], 
                    fill="#000000", width=widget_data.get("width", 3))
                self.widgets_data.append({"id": line_id, "type": "Line", "coords": widget_data["coords"], "width": widget_data.get("width", 3)})
                self.shape_canvas.tag_bind(line_id, "<Button-1>", self.on_shape_click)
                self.shape_canvas.tag_bind(line_id, "<B1-Motion>", self.on_shape_drag)
                self.shape_canvas.tag_bind(line_id, "<ButtonRelease-1>", self.on_shape_release)
            
            elif widget_type == "Polygon":
                polygon_id = self.shape_canvas.create_polygon(
                    widget_data["points"], fill=widget_data.get("fill", "#9f7aea"), outline="#6b46c1", width=2)
                self.widgets_data.append({"id": polygon_id, "type": "Polygon", "points": widget_data["points"], "fill": widget_data.get("fill", "#9f7aea")})
                self.shape_canvas.tag_bind(polygon_id, "<Button-1>", self.on_shape_click)
                self.shape_canvas.tag_bind(polygon_id, "<B1-Motion>", self.on_shape_drag)
                self.shape_canvas.tag_bind(polygon_id, "<ButtonRelease-1>", self.on_shape_release)
            
            elif widget_type == "Container":
                container = tk.Frame(self.preview_frame, bg=widget_data.get("bg", "#e2e8f0"), relief="solid", bd=1)
                self.make_draggable_and_resizable(container)
                container.place(x=widget_data["x"], y=widget_data["y"], 
                               width=widget_data["width"], height=widget_data["height"])
                
                # Add a label to identify it
                label = tk.Label(container, text="Container", bg=widget_data.get("bg", "#e2e8f0"))
                label.place(relx=0.5, rely=0.1, anchor="center")
                
                self.widgets_data.append({"id": id(container), "type": "Container", "widget": container})
            
            elif widget_type == "Card":
                card = tk.Frame(self.preview_frame, bg=widget_data.get("bg", "#ffffff"), relief="solid", bd=1)
                self.make_draggable_and_resizable(card)
                card.place(x=widget_data["x"], y=widget_data["y"], 
                           width=widget_data["width"], height=widget_data["height"])
                
                # Add a shadow effect
                shadow = tk.Frame(card, bg="#cbd5e0", height=5)
                shadow.pack(side="bottom", fill="x")
                
                # Add a label to identify it
                label = tk.Label(card, text="Card", bg=widget_data.get("bg", "#ffffff"), font=("Arial", 12, "bold"))
                label.place(relx=0.5, rely=0.3, anchor="center")
                
                # Add some sample text
                text = tk.Label(card, text="This is a sample card", bg=widget_data.get("bg", "#ffffff"))
                text.place(relx=0.5, rely=0.6, anchor="center")
                
                self.widgets_data.append({"id": id(card), "type": "Card", "widget": card})
            
            elif widget_type == "Menu":
                menu_frame = tk.Frame(self.preview_frame, bg=widget_data.get("bg", "#4a5568"), relief="flat")
                self.make_draggable_and_resizable(menu_frame, resizable_y=False)
                menu_frame.place(x=widget_data["x"], y=widget_data["y"], 
                                width=widget_data["width"], height=widget_data["height"])
                
                # Add menu items
                menu_items = ["Home", "About", "Services", "Contact"]
                for i, item in enumerate(menu_items):
                    btn = tk.Button(menu_frame, text=item, bg=widget_data.get("bg", "#4a5568"), fg="#ffffff", 
                                   relief="flat", font=("Arial", 10))
                    btn.pack(side="left", padx=10, pady=5)
                
                self.widgets_data.append({"id": id(menu_frame), "type": "Menu", "widget": menu_frame})
            
            elif widget_type == "Tabs":
                tabs_frame = tk.Frame(self.preview_frame, bg=widget_data.get("bg", "#ffffff"), relief="solid", bd=1)
                self.make_draggable_and_resizable(tabs_frame)
                tabs_frame.place(x=widget_data["x"], y=widget_data["y"], 
                                width=widget_data["width"], height=widget_data["height"])
                
                # Tab headers
                headers_frame = tk.Frame(tabs_frame, bg="#e2e8f0", height=30)
                headers_frame.pack(side="top", fill="x")
                
                # Tab buttons
                tab1 = tk.Button(headers_frame, text="Tab 1", bg="#cbd5e0", relief="flat", font=("Arial", 10))
                tab1.pack(side="left", padx=5, pady=2)
                
                tab2 = tk.Button(headers_frame, text="Tab 2", bg="#e2e8f0", relief="flat", font=("Arial", 10))
                tab2.pack(side="left", padx=5, pady=2)
                
                tab3 = tk.Button(headers_frame, text="Tab 3", bg="#e2e8f0", relief="flat", font=("Arial", 10))
                tab3.pack(side="left", padx=5, pady=2)
                
                # Tab content
                content_frame = tk.Frame(tabs_frame, bg=widget_data.get("bg", "#ffffff"))
                content_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
                
                content_label = tk.Label(content_frame, text="Tab 1 Content", bg=widget_data.get("bg", "#ffffff"))
                content_label.pack()
                
                self.widgets_data.append({"id": id(tabs_frame), "type": "Tabs", "widget": tabs_frame})
        
        # Save state after loading
        self.save_state()

    def save_current_frame(self):
        # Save current widgets to frame data
        frame = self.frames[self.current_frame_index]
        frame["widgets"] = []
        
        for item in self.widgets_data:
            widget_data = {"type": item["type"]}
            
            if "widget" in item:
                widget = item["widget"]
                widget_data["x"] = widget.winfo_x()
                widget_data["y"] = widget.winfo_y()
                widget_data["width"] = widget.winfo_width()
                widget_data["height"] = widget.winfo_height()
                
                if item["type"] in ("Button", "Label", "Entry", "Textarea", "Checkbox", "Radiobutton"):
                    widget_data["bg"] = widget.cget("bg")
                    widget_data["fg"] = widget.cget("fg")
                    
                    if item["type"] in ("Button", "Label", "Checkbox", "Radiobutton"):
                        widget_data["text"] = widget.cget("text")
                
                elif item["type"] == "Image":
                    widget_data["image_path"] = getattr(widget, "image_path", "")
                    widget_data["bg"] = widget.cget("bg")
                
                elif item["type"] in ("Container", "Card", "Menu", "Tabs", "Video"):
                    widget_data["bg"] = widget.cget("bg")
            
            elif item["type"] in ("Rectangle", "Oval"):
                widget_data["coords"] = item["coords"]
                widget_data["fill"] = item.get("fill", "#000000")
            
            elif item["type"] in ("Triangle", "Polygon"):
                widget_data["points"] = item["points"]
                widget_data["fill"] = item.get("fill", "#000000")
            
            elif item["type"] == "Line":
                widget_data["coords"] = item["coords"]
                widget_data["width"] = item.get("width", 3)
            
            frame["widgets"].append(widget_data)

    def update_frame_buttons(self):
        # Update button states based on current frame index
        self.prev_frame_btn.config(state="normal" if self.current_frame_index > 0 else "disabled")
        self.next_frame_btn.config(state="normal" if self.current_frame_index < len(self.frames) - 1 else "disabled")
        self.del_frame_btn.config(state="normal" if len(self.frames) > 1 else "disabled")

    # ---- Utility Methods ----
    def set_frame_dimensions(self, width, height):
        self.frame_width_var.set(width)
        self.frame_height_var.set(height)
        self.update_frame_dimensions()

    def update_frame_dimensions(self):
        width = self.frame_width_var.get()
        height = self.frame_height_var.get()
        
        # Update frame data
        self.frames[self.current_frame_index]["width"] = width
        self.frames[self.current_frame_index]["height"] = height
        
        # Update UI
        self.preview_frame.config(width=width, height=height)
        self.save_state()

    def toggle_grid(self):
        self.grid_visible = not self.grid_visible
        if self.grid_visible:
            self.add_grid_background()
        else:
            self.shape_canvas.delete("grid_line")

    def add_grid_background(self):
        if not self.grid_visible:
            return
            
        # Delete existing grid
        self.shape_canvas.delete("grid_line")
        
        # Get canvas dimensions
        width = self.preview_frame.winfo_width()
        height = self.preview_frame.winfo_height()
        
        # Draw grid lines
        grid_size = 20
        
        # Vertical lines
        for i in range(0, width, grid_size):
            self.shape_canvas.create_line(i, 0, i, height, fill="#e2e8f0", tags="grid_line")
        
        # Horizontal lines
        for i in range(0, height, grid_size):
            self.shape_canvas.create_line(0, i, width, i, fill="#e2e8f0", tags="grid_line")
        
        # Move grid to background
        self.shape_canvas.tag_lower("grid_line")

    def zoom_in(self):
        self.zoom_level = min(self.zoom_level + 0.1, 2.0)
        self.update_zoom()

    def zoom_out(self):
        self.zoom_level = max(self.zoom_level - 0.1, 0.5)
        self.update_zoom()

    def update_zoom(self):
        # Update zoom label
        self.zoom_label.config(text=f"{int(self.zoom_level * 100)}%")
        
        # Scale canvas
        self.shape_canvas.scale("all", 0, 0, self.zoom_level, self.zoom_level)
        
        # Redraw grid if visible
        if self.grid_visible:
            self.add_grid_background()

    # ---- History Management ----
    def save_state(self):
        # Save current state to history
        self.save_current_frame()
        
        # Remove any states after current index
        self.history = self.history[:self.history_index + 1]
        
        # Add new state
        self.history.append(json.dumps(self.frames))
        self.history_index += 1
        
        # Limit history size
        if len(self.history) > 50:
            self.history.pop(0)
            self.history_index -= 1
        
        # Update button states
        self.undo_button.config(state="normal" if self.history_index > 0 else "disabled")
        self.redo_button.config(state="normal" if self.history_index < len(self.history) - 1 else "disabled")

    def undo(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.frames = json.loads(self.history[self.history_index])
            self.load_frame(self.current_frame_index)
            
            # Update button states
            self.undo_button.config(state="normal" if self.history_index > 0 else "disabled")
            self.redo_button.config(state="normal")

    def redo(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.frames = json.loads(self.history[self.history_index])
            self.load_frame(self.current_frame_index)
            
            # Update button states
            self.redo_button.config(state="normal" if self.history_index < len(self.history) - 1 else "disabled")
            self.undo_button.config(state="normal")

    # ---- Export to Figma JSON ----
    def save_to_figma_json(self):
        # Save current frame
        self.save_current_frame()
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return
        
        # Create Figma-like JSON structure
        figma_data = {
            "document": {
                "id": "0:0",
                "name": "App Design",
                "type": "DOCUMENT",
                "children": []
            }
        }
        
        # Add frames as pages
        for frame_data in self.frames:
            page = {
                "id": f"1:{len(figma_data['document']['children'])}",
                "name": frame_data["name"],
                "type": "CANVAS",
                "children": []
            }
            
            # Add frame container
            frame_node = {
                "id": f"2:{len(page['children'])}",
                "name": "Frame",
                "type": "FRAME",
                "x": 0,
                "y": 0,
                "width": frame_data["width"],
                "height": frame_data["height"],
                "children": [],
                "backgroundColor": self._hex_to_rgba(frame_data.get("background", "#ffffff"))
            }
            
            # Add widgets to frame
            for widget_data in frame_data["widgets"]:
                widget_node = self._widget_to_figma_node(widget_data)
                if widget_node:
                    frame_node["children"].append(widget_node)
            
            page["children"].append(frame_node)
            figma_data["document"]["children"].append(page)
        
        # Save to file
        with open(file_path, 'w') as f:
            json.dump(figma_data, f, indent=2)
        
        messagebox.showinfo("Export Successful", f"Design exported to {file_path}")

    def _widget_to_figma_node(self, widget_data):
        widget_type = widget_data["type"]
        
        if widget_type == "Button":
            return {
                "id": f"3:{widget_data['x']}{widget_data['y']}",
                "name": "Button",
                "type": "RECTANGLE",
                "x": widget_data["x"],
                "y": widget_data["y"],
                "width": widget_data["width"],
                "height": widget_data["height"],
                "fills": [{"type": "SOLID", "color": self._hex_to_rgba(widget_data.get("bg", "#ffffff"))}],
                "strokes": [],
                "strokeWeight": 1,
                "children": [
                    {
                        "id": f"4:{widget_data['x']}{widget_data['y']}",
                        "name": "Text",
                        "type": "TEXT",
                        "x": 0,
                        "y": 0,
                        "width": widget_data["width"],
                        "height": widget_data["height"],
                        "fills": [{"type": "SOLID", "color": self._hex_to_rgba(widget_data.get("fg", "#000000"))}],
                        "characters": widget_data.get("text", "Button"),
                        "fontSize": 14,
                        "textAlignHorizontal": "CENTER",
                        "textAlignVertical": "CENTER"
                    }
                ]
            }
        
        elif widget_type == "Label":
            return {
                "id": f"3:{widget_data['x']}{widget_data['y']}",
                "name": "Label",
                "type": "TEXT",
                "x": widget_data["x"],
                "y": widget_data["y"],
                "width": widget_data["width"],
                "height": widget_data["height"],
                "fills": [{"type": "SOLID", "color": self._hex_to_rgba(widget_data.get("fg", "#000000"))}],
                "characters": widget_data.get("text", "Label"),
                "fontSize": 14,
                "textAlignHorizontal": "LEFT",
                "textAlignVertical": "TOP"
            }
        
        elif widget_type == "Entry":
            return {
                "id": f"3:{widget_data['x']}{widget_data['y']}",
                "name": "Entry",
                "type": "RECTANGLE",
                "x": widget_data["x"],
                "y": widget_data["y"],
                "width": widget_data["width"],
                "height": widget_data["height"],
                "fills": [{"type": "SOLID", "color": self._hex_to_rgba(widget_data.get("bg", "#ffffff"))}],
                "strokes": [{"type": "SOLID", "color": self._hex_to_rgba("#000000")}],
                "strokeWeight": 1
            }
        
        elif widget_type == "Textarea":
            return {
                "id": f"3:{widget_data['x']}{widget_data['y']}",
                "name": "Textarea",
                "type": "RECTANGLE",
                "x": widget_data["x"],
                "y": widget_data["y"],
                "width": widget_data["width"],
                "height": widget_data["height"],
                "fills": [{"type": "SOLID", "color": self._hex_to_rgba(widget_data.get("bg", "#ffffff"))}],
                "strokes": [{"type": "SOLID", "color": self._hex_to_rgba("#000000")}],
                "strokeWeight": 1
            }
        
        elif widget_type == "Checkbox":
            return {
                "id": f"3:{widget_data['x']}{widget_data['y']}",
                "name": "Checkbox",
                "type": "GROUP",
                "x": widget_data["x"],
                "y": widget_data["y"],
                "width": widget_data["width"],
                "height": widget_data["height"],
                "children": [
                    {
                        "id": f"4:{widget_data['x']}{widget_data['y']}",
                        "name": "Box",
                        "type": "RECTANGLE",
                        "x": 0,
                        "y": 0,
                        "width": 20,
                        "height": 20,
                        "fills": [{"type": "SOLID", "color": self._hex_to_rgba(widget_data.get("bg", "#ffffff"))}],
                        "strokes": [{"type": "SOLID", "color": self._hex_to_rgba("#000000")}],
                        "strokeWeight": 1
                    },
                    {
                        "id": f"5:{widget_data['x']}{widget_data['y']}",
                        "name": "Text",
                        "type": "TEXT",
                        "x": 25,
                        "y": 0,
                        "width": widget_data["width"] - 25,
                        "height": widget_data["height"],
                        "fills": [{"type": "SOLID", "color": self._hex_to_rgba(widget_data.get("fg", "#000000"))}],
                        "characters": widget_data.get("text", "Checkbox"),
                        "fontSize": 14,
                        "textAlignHorizontal": "LEFT",
                        "textAlignVertical": "CENTER"
                    }
                ]
            }
        
        elif widget_type == "Radiobutton":
            return {
                "id": f"3:{widget_data['x']}{widget_data['y']}",
                "name": "Radio Button",
                "type": "GROUP",
                "x": widget_data["x"],
                "y": widget_data["y"],
                "width": widget_data["width"],
                "height": widget_data["height"],
                "children": [
                    {
                        "id": f"4:{widget_data['x']}{widget_data['y']}",
                        "name": "Circle",
                        "type": "ELLIPSE",
                        "x": 0,
                        "y": 0,
                        "width": 20,
                        "height": 20,
                        "fills": [{"type": "SOLID", "color": self._hex_to_rgba(widget_data.get("bg", "#ffffff"))}],
                        "strokes": [{"type": "SOLID", "color": self._hex_to_rgba("#000000")}],
                        "strokeWeight": 1
                    },
                    {
                        "id": f"5:{widget_data['x']}{widget_data['y']}",
                        "name": "Text",
                        "type": "TEXT",
                        "x": 25,
                        "y": 0,
                        "width": widget_data["width"] - 25,
                        "height": widget_data["height"],
                        "fills": [{"type": "SOLID", "color": self._hex_to_rgba(widget_data.get("fg", "#000000"))}],
                        "characters": widget_data.get("text", "Radio Button"),
                        "fontSize": 14,
                        "textAlignHorizontal": "LEFT",
                        "textAlignVertical": "CENTER"
                    }
                ]
            }
        
        elif widget_type == "Image":
            return {
                "id": f"3:{widget_data['x']}{widget_data['y']}",
                "name": "Image",
                "type": "RECTANGLE",
                "x": widget_data["x"],
                "y": widget_data["y"],
                "width": widget_data["width"],
                "height": widget_data["height"],
                "fills": [{"type": "IMAGE", "imageRef": widget_data.get("image_path", ""), "scaleMode": "FILL"}]
            }
        
        elif widget_type == "Video":
            return {
                "id": f"3:{widget_data['x']}{widget_data['y']}",
                "name": "Video Player",
                "type": "RECTANGLE",
                "x": widget_data["x"],
                "y": widget_data["y"],
                "width": widget_data["width"],
                "height": widget_data["height"],
                "fills": [{"type": "SOLID", "color": self._hex_to_rgba(widget_data.get("bg", "#000000"))}]
            }
        
        elif widget_type == "Rectangle":
            x1, y1, x2, y2 = widget_data["coords"]
            return {
                "id": f"3:{x1}{y1}",
                "name": "Rectangle",
                "type": "RECTANGLE",
                "x": x1,
                "y": y1,
                "width": x2 - x1,
                "height": y2 - y1,
                "fills": [{"type": "SOLID", "color": self._hex_to_rgba(widget_data.get("fill", "#4299e1"))}]
            }
        
        elif widget_type == "Oval":
            x1, y1, x2, y2 = widget_data["coords"]
            return {
                "id": f"3:{x1}{y1}",
                "name": "Oval",
                "type": "ELLIPSE",
                "x": x1,
                "y": y1,
                "width": x2 - x1,
                "height": y2 - y1,
                "fills": [{"type": "SOLID", "color": self._hex_to_rgba(widget_data.get("fill", "#ed64a6"))}]
            }
        
        elif widget_type == "Triangle":
            # Find bounding box
            points = widget_data["points"]
            x_coords = [points[i] for i in range(0, len(points), 2)]
            y_coords = [points[i] for i in range(1, len(points), 2)]
            x1, y1 = min(x_coords), min(y_coords)
            x2, y2 = max(x_coords), max(y_coords)
            
            return {
                "id": f"3:{x1}{y1}",
                "name": "Triangle",
                "type": "VECTOR",
                "x": x1,
                "y": y1,
                "width": x2 - x1,
                "height": y2 - y1,
                "fills": [{"type": "SOLID", "color": self._hex_to_rgba(widget_data.get("fill", "#48bb78"))}],
                "vectorNetwork": {
                    "vertices": [
                        {"x": points[0] - x1, "y": points[1] - y1},
                        {"x": points[2] - x1, "y": points[3] - y1},
                        {"x": points[4] - x1, "y": points[5] - y1}
                    ],
                    "segments": [
                        {"start": 0, "end": 1},
                        {"start": 1, "end": 2},
                        {"start": 2, "end": 0}
                    ]
                }
            }
        
        elif widget_type == "Line":
            x1, y1, x2, y2 = widget_data["coords"]
            return {
                "id": f"3:{x1}{y1}",
                "name": "Line",
                "type": "LINE",
                "x": x1,
                "y": y1,
                "width": x2 - x1,
                "height": y2 - y1,
                "strokes": [{"type": "SOLID", "color": self._hex_to_rgba("#000000")}],
                "strokeWeight": widget_data.get("width", 3)
            }
        
        elif widget_type == "Polygon":
            # Find bounding box
            points = widget_data["points"]
            x_coords = [points[i] for i in range(0, len(points), 2)]
            y_coords = [points[i] for i in range(1, len(points), 2)]
            x1, y1 = min(x_coords), min(y_coords)
            x2, y2 = max(x_coords), max(y_coords)
            
            # Create vertices and segments
            vertices = []
            segments = []
            for i in range(0, len(points), 2):
                vertices.append({"x": points[i] - x1, "y": points[i+1] - y1})
                if i < len(points) - 2:
                    segments.append({"start": i // 2, "end": (i // 2) + 1})
            segments.append({"start": len(vertices) - 1, "end": 0})
            
            return {
                "id": f"3:{x1}{y1}",
                "name": "Polygon",
                "type": "VECTOR",
                "x": x1,
                "y": y1,
                "width": x2 - x1,
                "height": y2 - y1,
                "fills": [{"type": "SOLID", "color": self._hex_to_rgba(widget_data.get("fill", "#9f7aea"))}],
                "vectorNetwork": {
                    "vertices": vertices,
                    "segments": segments
                }
            }
        
        elif widget_type == "Container":
            return {
                "id": f"3:{widget_data['x']}{widget_data['y']}",
                "name": "Container",
                "type": "FRAME",
                "x": widget_data["x"],
                "y": widget_data["y"],
                "width": widget_data["width"],
                "height": widget_data["height"],
                "fills": [{"type": "SOLID", "color": self._hex_to_rgba(widget_data.get("bg", "#e2e8f0"))}],
                "children": [
                    {
                        "id": f"4:{widget_data['x']}{widget_data['y']}",
                        "name": "Label",
                        "type": "TEXT",
                        "x": widget_data["width"] / 2 - 40,
                        "y": widget_data["height"] * 0.1 - 10,
                        "width": 80,
                        "height": 20,
                        "fills": [{"type": "SOLID", "color": self._hex_to_rgba("#000000")}],
                        "characters": "Container",
                        "fontSize": 14,
                        "textAlignHorizontal": "CENTER",
                        "textAlignVertical": "CENTER"
                    }
                ]
            }
        
        elif widget_type == "Card":
            return {
                "id": f"3:{widget_data['x']}{widget_data['y']}",
                "name": "Card",
                "type": "FRAME",
                "x": widget_data["x"],
                "y": widget_data["y"],
                "width": widget_data["width"],
                "height": widget_data["height"],
                "fills": [{"type": "SOLID", "color": self._hex_to_rgba(widget_data.get("bg", "#ffffff"))}],
                "strokes": [{"type": "SOLID", "color": self._hex_to_rgba("#cbd5e0")}],
                "strokeWeight": 1,
                "children": [
                    {
                        "id": f"4:{widget_data['x']}{widget_data['y']}",
                        "name": "Shadow",
                        "type": "RECTANGLE",
                        "x": 0,
                        "y": widget_data["height"] - 5,
                        "width": widget_data["width"],
                        "height": 5,
                        "fills": [{"type": "SOLID", "color": self._hex_to_rgba("#cbd5e0")}]
                    },
                    {
                        "id": f"5:{widget_data['x']}{widget_data['y']}",
                        "name": "Title",
                        "type": "TEXT",
                        "x": widget_data["width"] / 2 - 30,
                        "y": widget_data["height"] * 0.3 - 10,
                        "width": 60,
                        "height": 20,
                        "fills": [{"type": "SOLID", "color": self._hex_to_rgba("#000000")}],
                        "characters": "Card",
                        "fontSize": 12,
                        "fontWeight": 700,
                        "textAlignHorizontal": "CENTER",
                        "textAlignVertical": "CENTER"
                    },
                    {
                        "id": f"6:{widget_data['x']}{widget_data['y']}",
                        "name": "Text",
                        "type": "TEXT",
                        "x": widget_data["width"] / 2 - 70,
                        "y": widget_data["height"] * 0.6 - 10,
                        "width": 140,
                        "height": 20,
                        "fills": [{"type": "SOLID", "color": self._hex_to_rgba("#000000")}],
                        "characters": "This is a sample card",
                        "fontSize": 10,
                        "textAlignHorizontal": "CENTER",
                        "textAlignVertical": "CENTER"
                    }
                ]
            }
        
        elif widget_type == "Menu":
            return {
                "id": f"3:{widget_data['x']}{widget_data['y']}",
                "name": "Menu",
                "type": "FRAME",
                "x": widget_data["x"],
                "y": widget_data["y"],
                "width": widget_data["width"],
                "height": widget_data["height"],
                "fills": [{"type": "SOLID", "color": self._hex_to_rgba(widget_data.get("bg", "#4a5568"))}],
                "children": [
                    {
                        "id": f"4:{widget_data['x']}{widget_data['y']}",
                        "name": "Home",
                        "type": "TEXT",
                        "x": 10,
                        "y": 10,
                        "width": 50,
                        "height": 20,
                        "fills": [{"type": "SOLID", "color": self._hex_to_rgba("#ffffff")}],
                        "characters": "Home",
                        "fontSize": 10,
                        "textAlignHorizontal": "CENTER",
                        "textAlignVertical": "CENTER"
                    },
                    {
                        "id": f"5:{widget_data['x']}{widget_data['y']}",
                        "name": "About",
                        "type": "TEXT",
                        "x": 70,
                        "y": 10,
                        "width": 50,
                        "height": 20,
                        "fills": [{"type": "SOLID", "color": self._hex_to_rgba("#ffffff")}],
                        "characters": "About",
                        "fontSize": 10,
                        "textAlignHorizontal": "CENTER",
                        "textAlignVertical": "CENTER"
                    },
                    {
                        "id": f"6:{widget_data['x']}{widget_data['y']}",
                        "name": "Services",
                        "type": "TEXT",
                        "x": 130,
                        "y": 10,
                        "width": 60,
                        "height": 20,
                        "fills": [{"type": "SOLID", "color": self._hex_to_rgba("#ffffff")}],
                        "characters": "Services",
                        "fontSize": 10,
                        "textAlignHorizontal": "CENTER",
                        "textAlignVertical": "CENTER"
                    },
                    {
                        "id": f"7:{widget_data['x']}{widget_data['y']}",
                        "name": "Contact",
                        "type": "TEXT",
                        "x": 200,
                        "y": 10,
                        "width": 60,
                        "height": 20,
                        "fills": [{"type": "SOLID", "color": self._hex_to_rgba("#ffffff")}],
                        "characters": "Contact",
                        "fontSize": 10,
                        "textAlignHorizontal": "CENTER",
                        "textAlignVertical": "CENTER"
                    }
                ]
            }
        
        elif widget_type == "Tabs":
            return {
                "id": f"3:{widget_data['x']}{widget_data['y']}",
                "name": "Tabs",
                "type": "FRAME",
                "x": widget_data["x"],
                "y": widget_data["y"],
                "width": widget_data["width"],
                "height": widget_data["height"],
                "fills": [{"type": "SOLID", "color": self._hex_to_rgba(widget_data.get("bg", "#ffffff"))}],
                "strokes": [{"type": "SOLID", "color": self._hex_to_rgba("#e2e8f0")}],
                "strokeWeight": 1,
                "children": [
                    {
                        "id": f"4:{widget_data['x']}{widget_data['y']}",
                        "name": "Tab Headers",
                        "type": "FRAME",
                        "x": 0,
                        "y": 0,
                        "width": widget_data["width"],
                        "height": 30,
                        "fills": [{"type": "SOLID", "color": self._hex_to_rgba("#e2e8f0")}],
                        "children": [
                            {
                                "id": f"5:{widget_data['x']}{widget_data['y']}",
                                "name": "Tab 1",
                                "type": "TEXT",
                                "x": 5,
                                "y": 5,
                                "width": 50,
                                "height": 20,
                                "fills": [{"type": "SOLID", "color": self._hex_to_rgba("#000000")}],
                                "characters": "Tab 1",
                                "fontSize": 10,
                                "textAlignHorizontal": "CENTER",
                                "textAlignVertical": "CENTER"
                            },
                            {
                                "id": f"6:{widget_data['x']}{widget_data['y']}",
                                "name": "Tab 2",
                                "type": "TEXT",
                                "x": 65,
                                "y": 5,
                                "width": 50,
                                "height": 20,
                                "fills": [{"type": "SOLID", "color": self._hex_to_rgba("#000000")}],
                                "characters": "Tab 2",
                                "fontSize": 10,
                                "textAlignHorizontal": "CENTER",
                                "textAlignVertical": "CENTER"
                            },
                            {
                                "id": f"7:{widget_data['x']}{widget_data['y']}",
                                "name": "Tab 3",
                                "type": "TEXT",
                                "x": 125,
                                "y": 5,
                                "width": 50,
                                "height": 20,
                                "fills": [{"type": "SOLID", "color": self._hex_to_rgba("#000000")}],
                                "characters": "Tab 3",
                                "fontSize": 10,
                                "textAlignHorizontal": "CENTER",
                                "textAlignVertical": "CENTER"
                            }
                        ]
                    },
                    {
                        "id": f"8:{widget_data['x']}{widget_data['y']}",
                        "name": "Tab Content",
                        "type": "FRAME",
                        "x": 10,
                        "y": 40,
                        "width": widget_data["width"] - 20,
                        "height": widget_data["height"] - 50,
                        "fills": [{"type": "SOLID", "color": self._hex_to_rgba(widget_data.get("bg", "#ffffff"))}],
                        "children": [
                            {
                                "id": f"9:{widget_data['x']}{widget_data['y']}",
                                "name": "Content",
                                "type": "TEXT",
                                "x": (widget_data["width"] - 20) / 2 - 50,
                                "y": (widget_data["height"] - 50) / 2 - 10,
                                "width": 100,
                                "height": 20,
                                "fills": [{"type": "SOLID", "color": self._hex_to_rgba("#000000")}],
                                "characters": "Tab 1 Content",
                                "fontSize": 10,
                                "textAlignHorizontal": "CENTER",
                                "textAlignVertical": "CENTER"
                            }
                        ]
                    }
                ]
            }
        
        return None

    def _hex_to_rgba(self, color_input):
        """
        Converts a color string (hex code or Tkinter color name) to an RGBA dictionary.
        Handles invalid inputs gracefully by returning a default black color.
        """
        # Ensure the input is a string
        if not isinstance(color_input, str):
            # Return a default color (black) if the input is not a string
            return {"r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0}

        # Default to black in case of any conversion errors
        default_color = {"r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0}
        
        try:
            # If it's a hex code, process it directly
            if color_input.startswith('#'):
                hex_color = color_input.lstrip('#')
                if len(hex_color) == 3:
                    hex_color = ''.join([c * 2 for c in hex_color])
                elif len(hex_color) != 6:
                    # Invalid hex length
                    return default_color

                r = int(hex_color[0:2], 16) / 255.0
                g = int(hex_color[2:4], 16) / 255.0
                b = int(hex_color[4:6], 16) / 255.0
                a = 1.0
                
                return {"r": r, "g": g, "b": b, "a": a}
            
            else:
                # If it's not a hex code, assume it's a color name (e.g., "SystemButtonFace", "white")
                # Use a temporary widget to leverage Tkinter's color name resolution
                # We create a dummy widget because winfo_rgb needs a widget context.
                # We use self.root which should be available in the class.
                if not self.root.winfo_exists():
                    return default_color

                # winfo_rgb returns a tuple of (r, g, b) values in the range 0-65535
                r, g, b = self.root.winfo_rgb(color_input)
                
                # Convert to 0-1 range
                r = r / 65535.0
                g = g / 65535.0
                b = b / 65535.0
                a = 1.0
                
                return {"r": r, "g": g, "b": b, "a": a}

        except (ValueError, TclError):
            # Catch errors from invalid hex literals or unknown color names
            # TclError can be raised by winfo_rgb for invalid color names
            return default_color


if __name__ == "__main__":
    root = tk.Tk()
    app = AppDesigner(root)
    root.mainloop()