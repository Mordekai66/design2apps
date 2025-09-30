import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from PIL import Image, ImageTk
import json

class AppDesigner:
    def __init__(self, root):
        self.root = root
        self.root.title("App Designer كامل")
        self.root.geometry("1300x750")
        self.root.configure(bg="#1a1a2e")

        self.selected_widget = None
        self.selected_shape = None
        self.drag_data = {"x":0, "y":0, "action": None}
        self.shape_drag_data = {"x":0, "y":0}
        self.widgets_data = []
        self.prop_widgets = []

        # اول ما يفتح يسأل عن حجم الواجهة
        self.frame_width, self.frame_height = self.ask_frame_size()
        
        self.create_toolbox()
        self.create_preview_area()
        self.create_properties_panel()
        self.create_save_button()

    def ask_frame_size(self):
        w = simpledialog.askinteger("حجم الواجهة", "ادخل عرض الواجهة (px):", minvalue=200, maxvalue=1920)
        h = simpledialog.askinteger("حجم الواجهة", "ادخل ارتفاع الواجهة (px):", minvalue=200, maxvalue=1080)
        if not w: w = 800
        if not h: h = 600
        return w, h

    # ---- الواجهة ----
    def create_toolbox(self):
        frame = tk.Frame(self.root, bg="#16213e", width=220)
        frame.pack(side="left", fill="y")
        tk.Label(frame, text="🛠 الأدوات", bg="#16213e", fg="white", font=("Arial", 14, "bold")).pack(pady=10)
        tools = [
            ("زر Button", self.add_button),
            ("عنوان Label", self.add_label),
            ("حقل Entry", self.add_entry),
            ("🖼️ إضافة صورة", self.add_image_widget),
            ("⬛ مستطيل", self.add_rectangle),
            ("⚪ دائرة", self.add_oval),
        ]
        for txt, cmd in tools:
            b = tk.Button(frame, text=txt, command=cmd, bg="#0f3460", fg="white", relief="flat", font=("Arial", 12))
            b.pack(fill="x", pady=5, padx=10)

    def create_preview_area(self):
        self.preview_frame = tk.Frame(self.root, bg="#e0e0e0", width=self.frame_width, height=self.frame_height, relief="ridge", bd=2)
        self.preview_frame.pack(side="left", fill="both", expand=True)
        self.preview_frame.pack_propagate(False)
        tk.Label(self.preview_frame, text="📱 منطقة العرض", bg="#e0e0e0", font=("Arial", 14, "bold")).place(relx=0.5, rely=0.03, anchor="center")

        self.shape_canvas = tk.Canvas(self.preview_frame, bg="#e0e0e0", highlightthickness=0)
        self.shape_canvas.place(x=0, y=40, relwidth=1, relheight=1)
        self.shape_canvas.lower("all")

        self.shape_canvas.bind("<Button-1>", self.on_shape_click)
        self.shape_canvas.bind("<B1-Motion>", self.on_shape_drag)
        self.shape_canvas.bind("<ButtonRelease-1>", self.on_shape_release)

    def create_properties_panel(self):
        self.properties_frame = tk.Frame(self.root, bg="#16213e", width=280)
        self.properties_frame.pack(side="right", fill="y")
        tk.Label(self.properties_frame, text="⚙️ الخصائص", bg="#16213e", fg="white", font=("Arial", 14, "bold")).pack(pady=10)

    def create_save_button(self):
        btn = tk.Button(self.properties_frame, text="💾 حفظ التصميم (JSON)", bg="#f72585", fg="white", font=("Arial", 12, "bold"), command=self.save_to_json)
        btn.pack(side="bottom", pady=20, padx=10, fill="x")

    # ---- إضافة عناصر ----
    def add_button(self):
        btn = tk.Button(self.preview_frame, text="زر جديد", bg="white")
        self.make_draggable_and_resizable(btn)
        btn.place(x=100, y=100)
        self.widgets_data.append({"id": id(btn), "type": "Button", "widget": btn})

    def add_label(self):
        lbl = tk.Label(self.preview_frame, text="عنوان جديد", bg="white")
        self.make_draggable_and_resizable(lbl)
        lbl.place(x=100, y=150)
        self.widgets_data.append({"id": id(lbl), "type": "Label", "widget": lbl})

    def add_entry(self):
        entry = tk.Entry(self.preview_frame)
        self.make_draggable_and_resizable(entry, resizable_y=False)
        entry.place(x=100, y=200, width=150)
        self.widgets_data.append({"id": id(entry), "type": "Entry", "widget": entry})

    def add_image_widget(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        if not path:
            return
        img_orig = Image.open(path)
        img = img_orig.resize((150, 100))
        photo = ImageTk.PhotoImage(img)
        lbl = tk.Label(self.preview_frame, image=photo, bg="white")
        lbl.image = photo
        lbl.img_orig = img_orig
        lbl.image_path = path
        lbl.is_image_widget = True
        self.make_draggable_and_resizable(lbl)
        lbl.place(x=100, y=500, width=150, height=100)
        self.widgets_data.append({"id": id(lbl), "type": "Image", "widget": lbl, "image_path": path})

    def add_rectangle(self):
        rect_id = self.shape_canvas.create_rectangle(50, 50, 150, 100, fill="blue", outline="black", width=2)
        self.widgets_data.append({"id": rect_id, "type": "Rectangle", "coords": [50, 50, 150, 100], "fill": "blue"})
        self.shape_canvas.tag_bind(rect_id, "<Button-1>", self.on_shape_click)
        self.shape_canvas.tag_bind(rect_id, "<B1-Motion>", self.on_shape_drag)
        self.shape_canvas.tag_bind(rect_id, "<ButtonRelease-1>", self.on_shape_release)

    def add_oval(self):
        oval_id = self.shape_canvas.create_oval(50, 150, 150, 250, fill="red", outline="black", width=2)
        self.widgets_data.append({"id": oval_id, "type": "Oval", "coords": [50, 150, 150, 250], "fill": "red"})
        self.shape_canvas.tag_bind(oval_id, "<Button-1>", self.on_shape_click)
        self.shape_canvas.tag_bind(oval_id, "<B1-Motion>", self.on_shape_drag)
        self.shape_canvas.tag_bind(oval_id, "<ButtonRelease-1>", self.on_shape_release)

    # ---- تحريك وتكبير العناصر ----
    def make_draggable_and_resizable(self, widget, resizable_x=True, resizable_y=True):
        widget.bind("<Button-1>", lambda e, w=widget: self.on_widget_click(e, w))
        widget.bind("<B1-Motion>", lambda e, w=widget: self.on_widget_drag(e, w))
        widget.bind("<ButtonRelease-1>", self.on_widget_release)
        widget.bind("<Motion>", lambda e, w=widget: self.on_widget_hover(e, w))
        widget.resizable_x = resizable_x
        widget.resizable_y = resizable_y

    def on_widget_click(self, event, widget):
        self.selected_widget = widget
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.drag_data["action"] = self.get_action(event, widget)
        # نمسح الخصائص القديمة عشان متتراكمش
        for w in self.prop_widgets:
            w.destroy()
        self.prop_widgets.clear()
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

    # تحجيم صورة بدون تشويه
    def resize_image(self, widget, new_w, new_h):
        img_orig = getattr(widget, "img_orig", None)
        if img_orig:
            img_ratio = img_orig.width / img_orig.height
            target_ratio = new_w / new_h
            if target_ratio > img_ratio:
                # عرض أكبر من نسبة الصورة الأصلية
                height = new_h
                width = int(height * img_ratio)
            else:
                width = new_w
                height = int(width / img_ratio)
            img_resized = img_orig.resize((width, height), Image.ANTIALIAS)
            widget.photo = ImageTk.PhotoImage(img_resized)
            widget.config(image=widget.photo)
            widget.place_configure(width=width, height=height)

    # ---- التعامل مع الأشكال الهندسية ----
    def on_shape_click(self, event):
        shape_id = self.shape_canvas.find_closest(event.x, event.y)[0]
        self.selected_shape = shape_id
        self.shape_drag_data["x"] = event.x
        self.shape_drag_data["y"] = event.y

        coords = self.shape_canvas.coords(shape_id)
        x1, y1, x2, y2 = coords
        margin = 10
        if abs(event.x - x2) <= margin and abs(event.y - y2) <= margin:
            self.drag_data["action"] = "resize_shape"
        else:
            self.drag_data["action"] = "move_shape"
        # نمسح الخصائص القديمة عشان متتراكمش
        for w in self.prop_widgets:
            w.destroy()
        self.prop_widgets.clear()
        self.show_shape_properties(shape_id)

    def on_shape_drag(self, event):
        if not self.selected_shape:
            return
        dx = event.x - self.shape_drag_data["x"]
        dy = event.y - self.shape_drag_data["y"]
        action = self.drag_data.get("action")

        coords = self.shape_canvas.coords(self.selected_shape)
        x1, y1, x2, y2 = coords
        if action == "move_shape":
            new_coords = [x1 + dx, y1 + dy, x2 + dx, y2 + dy]
            self.shape_canvas.coords(self.selected_shape, *new_coords)
            # تحديث البيانات
            for item in self.widgets_data:
                if item["id"] == self.selected_shape:
                    item["coords"] = new_coords
                    break
            self.shape_drag_data["x"], self.shape_drag_data["y"] = event.x, event.y
        elif action == "resize_shape":
            new_coords = [x1, y1, max(x2 + dx, x1 + 10), max(y2 + dy, y1 + 10)]
            self.shape_canvas.coords(self.selected_shape, *new_coords)
            # تحديث البيانات
            for item in self.widgets_data:
                if item["id"] == self.selected_shape:
                    item["coords"] = new_coords
                    break
            self.shape_drag_data["x"], self.shape_drag_data["y"] = event.x, event.y

    def on_shape_release(self, event):
        self.drag_data["action"] = None
        self.selected_shape = None

    # ---- عرض الخصائص للعناصر ----
    def show_properties(self, widget):
        # حذف الخصائص القديمة
        for w in self.prop_widgets:
            w.destroy()
        self.prop_widgets.clear()

        text = ""
        try:
            text = widget.cget("text")
        except:
            text = ""

        bg = widget.cget("bg") if "bg" in widget.keys() else "#ffffff"
        fg = widget.cget("fg") if "fg" in widget.keys() else "#000000"
        width = widget.winfo_width()
        height = widget.winfo_height()
        x = widget.winfo_x()
        y = widget.winfo_y()

        def update_text(event=None):
            try:
                widget.config(text=txt_var.get())
            except:
                pass

        def update_bg(event=None):
            widget.config(bg=bg_var.get())

        def update_fg(event=None):
            widget.config(fg=fg_var.get())

        def update_width(event=None):
            w = max(int(width_var.get()), 20)
            widget.place_configure(width=w)
            self.update_widget_size_in_data(widget)

        def update_height(event=None):
            h = max(int(height_var.get()), 20)
            widget.place_configure(height=h)
            self.update_widget_size_in_data(widget)

        def update_x(event=None):
            new_x = int(x_var.get())
            widget.place_configure(x=new_x)
            self.update_widget_position_in_data(widget)

        def update_y(event=None):
            new_y = int(y_var.get())
            widget.place_configure(y=new_y)
            self.update_widget_position_in_data(widget)

        # بناء الخصائص بس للعنصر المحدد (تجنب التكرار)
        tk.Label(self.properties_frame, text="نص:", bg="#16213e", fg="white").pack(anchor="w", padx=10)
        txt_var = tk.StringVar(value=text)
        e_text = tk.Entry(self.properties_frame, textvariable=txt_var)
        e_text.pack(fill="x", padx=10)
        e_text.bind("<KeyRelease>", update_text)
        self.prop_widgets.append(e_text)

        tk.Label(self.properties_frame, text="لون الخلفية:", bg="#16213e", fg="white").pack(anchor="w", padx=10)
        bg_var = tk.StringVar(value=bg)
        e_bg = tk.Entry(self.properties_frame, textvariable=bg_var)
        e_bg.pack(fill="x", padx=10)
        e_bg.bind("<KeyRelease>", update_bg)
        self.prop_widgets.append(e_bg)

        tk.Label(self.properties_frame, text="لون النص:", bg="#16213e", fg="white").pack(anchor="w", padx=10)
        fg_var = tk.StringVar(value=fg)
        e_fg = tk.Entry(self.properties_frame, textvariable=fg_var)
        e_fg.pack(fill="x", padx=10)
        e_fg.bind("<KeyRelease>", update_fg)
        self.prop_widgets.append(e_fg)

        tk.Label(self.properties_frame, text="الموقع (X):", bg="#16213e", fg="white").pack(anchor="w", padx=10)
        x_var = tk.StringVar(value=str(x))
        e_x = tk.Entry(self.properties_frame, textvariable=x_var)
        e_x.pack(fill="x", padx=10)
        e_x.bind("<KeyRelease>", update_x)
        self.prop_widgets.append(e_x)

        tk.Label(self.properties_frame, text="الموقع (Y):", bg="#16213e", fg="white").pack(anchor="w", padx=10)
        y_var = tk.StringVar(value=str(y))
        e_y = tk.Entry(self.properties_frame, textvariable=y_var)
        e_y.pack(fill="x", padx=10)
        e_y.bind("<KeyRelease>", update_y)
        self.prop_widgets.append(e_y)

        tk.Label(self.properties_frame, text="العرض:", bg="#16213e", fg="white").pack(anchor="w", padx=10)
        width_var = tk.StringVar(value=str(width))
        e_width = tk.Entry(self.properties_frame, textvariable=width_var)
        e_width.pack(fill="x", padx=10)
        e_width.bind("<KeyRelease>", update_width)
        self.prop_widgets.append(e_width)

        tk.Label(self.properties_frame, text="الارتفاع:", bg="#16213e", fg="white").pack(anchor="w", padx=10)
        height_var = tk.StringVar(value=str(height))
        e_height = tk.Entry(self.properties_frame, textvariable=height_var)
        e_height.pack(fill="x", padx=10)
        e_height.bind("<KeyRelease>", update_height)
        self.prop_widgets.append(e_height)

    # ---- عرض خصائص الأشكال ----
    def show_shape_properties(self, shape_id):
        for w in self.prop_widgets:
            w.destroy()
        self.prop_widgets.clear()

        shape_item = None
        for item in self.widgets_data:
            if item["id"] == shape_id:
                shape_item = item
                break
        if not shape_item:
            return

        coords = shape_item.get("coords", [0,0,0,0])
        fill = shape_item.get("fill", "#000000")
        x1, y1, x2, y2 = coords
        width = x2 - x1
        height = y2 - y1

        def update_fill(event=None):
            color = fill_var.get()
            shape_item["fill"] = color
            self.shape_canvas.itemconfig(shape_id, fill=color)

        def update_x1(event=None):
            try:
                new_x1 = int(x1_var.get())
                shape_item["coords"][0] = new_x1
                self.shape_canvas.coords(shape_id, new_x1, coords[1], coords[2], coords[3])
            except: pass

        def update_y1(event=None):
            try:
                new_y1 = int(y1_var.get())
                shape_item["coords"][1] = new_y1
                self.shape_canvas.coords(shape_id, coords[0], new_y1, coords[2], coords[3])
            except: pass

        def update_x2(event=None):
            try:
                new_x2 = int(x2_var.get())
                shape_item["coords"][2] = new_x2
                self.shape_canvas.coords(shape_id, coords[0], coords[1], new_x2, coords[3])
            except: pass

        def update_y2(event=None):
            try:
                new_y2 = int(y2_var.get())
                shape_item["coords"][3] = new_y2
                self.shape_canvas.coords(shape_id, coords[0], coords[1], coords[2], new_y2)
            except: pass

        tk.Label(self.properties_frame, text="لون التعبئة:", bg="#16213e", fg="white").pack(anchor="w", padx=10)
        fill_var = tk.StringVar(value=fill)
        e_fill = tk.Entry(self.properties_frame, textvariable=fill_var)
        e_fill.pack(fill="x", padx=10)
        e_fill.bind("<KeyRelease>", update_fill)
        self.prop_widgets.append(e_fill)

        tk.Label(self.properties_frame, text="x1:", bg="#16213e", fg="white").pack(anchor="w", padx=10)
        x1_var = tk.StringVar(value=str(x1))
        e_x1 = tk.Entry(self.properties_frame, textvariable=x1_var)
        e_x1.pack(fill="x", padx=10)
        e_x1.bind("<KeyRelease>", update_x1)
        self.prop_widgets.append(e_x1)

        tk.Label(self.properties_frame, text="y1:", bg="#16213e", fg="white").pack(anchor="w", padx=10)
        y1_var = tk.StringVar(value=str(y1))
        e_y1 = tk.Entry(self.properties_frame, textvariable=y1_var)
        e_y1.pack(fill="x", padx=10)
        e_y1.bind("<KeyRelease>", update_y1)
        self.prop_widgets.append(e_y1)

        tk.Label(self.properties_frame, text="x2:", bg="#16213e", fg="white").pack(anchor="w", padx=10)
        x2_var = tk.StringVar(value=str(x2))
        e_x2 = tk.Entry(self.properties_frame, textvariable=x2_var)
        e_x2.pack(fill="x", padx=10)
        e_x2.bind("<KeyRelease>", update_x2)
        self.prop_widgets.append(e_x2)

        tk.Label(self.properties_frame, text="y2:", bg="#16213e", fg="white").pack(anchor="w", padx=10)
        y2_var = tk.StringVar(value=str(y2))
        e_y2 = tk.Entry(self.properties_frame, textvariable=y2_var)
        e_y2.pack(fill="x", padx=10)
        e_y2.bind("<KeyRelease>", update_y2)
        self.prop_widgets.append(e_y2)

    # ---- حفظ التصميم كملف JSON بنفس هيكلة Figma ----
    def save_to_json(self):
        def rgb_to_figma_color(hex_color):
            hex_color = hex_color.lstrip('#')
            lv = len(hex_color)
            try:
                r, g, b = tuple(int(hex_color[i:i+lv//3], 16)/255.0 for i in range(0, lv, lv//3))
            except:
                r, g, b = 0, 0, 0
            return {"r": r, "g": g, "b": b}

        children = []
        frame_id = "0:0"
        frame_name = "Frame 1"
        frame_x, frame_y = 0, 0
        frame_w, frame_h = self.frame_width, self.frame_height  # استخدم أبعاد المستخدم

        for item in self.widgets_data:
            wid_type = item.get("type")
            node_id = str(item.get("id"))
            if wid_type in ("Button", "Label", "Entry", "Image"):
                w = item["widget"]
                x, y = w.winfo_x(), w.winfo_y()
                wdt, hgt = w.winfo_width(), w.winfo_height()
                fill_color = "#ffffff"
                try:
                    fill_color = w.cget("bg")
                except:
                    pass
                fill_rgb = rgb_to_figma_color(fill_color)

                node = {
                    "id": node_id,
                    "name": wid_type,
                    "type": "RECTANGLE" if wid_type != "Entry" else "FRAME",
                    "absoluteBoundingBox": {
                        "x": x,
                        "y": y,
                        "width": wdt,
                        "height": hgt
                    },
                    "fills": [{"type": "SOLID", "color": fill_rgb}],
                }
                if wid_type in ("Button", "Label"):
                    try:
                        node["type"] = "TEXT"
                        node["characters"] = w.cget("text")
                    except:
                        pass
                elif wid_type == "Image":
                    node["type"] = "IMAGE"
                    node["imageRef"] = item.get("image_path", "")
                children.append(node)

            elif wid_type in ("Rectangle", "Oval"):
                coords = item.get("coords", [0,0,0,0])
                x1, y1, x2, y2 = coords
                wdt = x2 - x1
                hgt = y2 - y1
                fill_rgb = rgb_to_figma_color(item.get("fill", "#000000"))
                node = {
                    "id": node_id,
                    "name": wid_type,
                    "type": "RECTANGLE" if wid_type == "Rectangle" else "ELLIPSE",
                    "absoluteBoundingBox": {
                        "x": x1,
                        "y": y1,
                        "width": wdt,
                        "height": hgt
                    },
                    "fills": [{"type": "SOLID", "color": fill_rgb}],
                }
                children.append(node)

        figma_json = {
            "document": {
                "id": frame_id,
                "name": frame_name,
                "type": "FRAME",
                "absoluteBoundingBox": {
                    "x": frame_x,
                    "y": frame_y,
                    "width": frame_w,
                    "height": frame_h
                },
                "children": children
            }
        }

        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(figma_json, f, indent=4, ensure_ascii=False)

        messagebox.showinfo("تم", f"تم حفظ التصميم بنفس هيكلة فيجما في الملف:\n{path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppDesigner(root)
    root.mainloop()
