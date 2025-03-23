from tkinter import *
from PIL import Image, ImageTk

image_refs = []

app = Tk()
app.title("Page 1")
app.geometry("510x460")
app.config(bg="#0f0e17")

canvas = Canvas(app, width=510, height=460, bg='#0f0e17', highlightthickness=0)
canvas.pack(fill='both', expand=True)

canvas.create_text(133, 32, anchor="w", text="Tk Designer", fill="#fffffe", font=("Inter", -36))

canvas.create_text(23, 123, anchor="w", text="Enter your file id", fill="#ffffff", font=("Inter", -20))

entry = Entry(app, bg='#ff8906')
canvas.create_window(26, 160, anchor="nw", window=entry, width=304, height=30)

canvas.create_text(26, 321, anchor="w", text="Choose the output file path", fill="#ffffff", font=("Inter", -20))

entry = Entry(app, bg='#ff8906')
canvas.create_window(29, 358, anchor="nw", window=entry, width=304, height=30)

canvas.create_text(23, 222, anchor="w", text="Enter your access token", fill="#ffffff", font=("Inter", -20))

entry = Entry(app, bg='#ff8906')
canvas.create_window(26, 259, anchor="nw", window=entry, width=355, height=30)

def change_button_color(event, color):
    canvas.itemconfig("current", fill=color)


button_id = canvas.create_rectangle(351, 358, 381, 388, fill='#875d5d', outline="black", tags="button")



text_id = canvas.create_text(366, 373, text="📁", fill="black", font=("Arial", 12), anchor="center", tags="button")

canvas.tag_bind("button", "<Enter>", lambda event:change_button_color(event, "#87CEEB"))
canvas.tag_bind("button", "<Leave>", lambda event:change_button_color(event, "#875d5d"))

def change_button_color(event, color):
    canvas.itemconfig("current", fill=color)

button_id = canvas.create_oval(101, 408, 197, 459, fill='#c34e4e', outline="black", tags="button")


text_id = canvas.create_text(149, 433, text="Submit", fill="black", font=("Arial", 12), anchor="center", tags="button")

canvas.tag_bind("button", "<Enter>", lambda event:change_button_color(event, "#87CEEB"))
canvas.tag_bind("button", "<Leave>", lambda event:change_button_color(event, "#c34e4e"))

image = Image.open(r'C:/Users/Workstation Shop/OneDrive/Desktop/build/image/78.png')
image = image.resize((138, 105))
photo = ImageTk.PhotoImage(image)
image_refs.append(photo)

canvas.create_image(338, 67, anchor="nw", image=photo)

app.resizable(0,0)
app.mainloop()