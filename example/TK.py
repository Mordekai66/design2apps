from tkinter import *
from PIL import Image, ImageTk

image_refs = []

window = Tk()
window.title("Page 1")
window.geometry("594x423")
window.config(bg="#150606")

canvas = Canvas(window, width=594, height=423, bg='#150606', highlightthickness=0)
canvas.pack(fill='both', expand=True)

canvas.create_text(3, 48, anchor="nw", text="python test", fill="#ffffff", font=("Inter", -12))

entry = Entry(window, bg='#d9d9d9')
canvas.create_window(24, 137, anchor=nw, window=entry, width=539, height=58)

image = Image.open(r'D:/build/image/166.png')
image = image.resize((87, 84))
photo = ImageTk.PhotoImage(image)
image_refs.append(photo)

canvas.create_image(241, 198, anchor=nw, image=photo)


canvas.create_rectangle(39, 326, 152, 347, fill='#d9d9d9', outline="black", tags="button")


canvas.create_text(95, 336, text="ahmed", fill="black", font=("Arial", 12), anchor="center", tags="button")


canvas.create_oval(429, 314, 531, 353, fill='#d9d9d9', outline='black')

window.resizable(0,0)
window.mainloop()