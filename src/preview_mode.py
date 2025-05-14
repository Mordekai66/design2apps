import tkinter as tk
import subprocess
import os

def run_script():
    # تشغيل ملف بايثون باستخدام subprocess
    command = "D:\VS code\Python-Projects\Tkinter - Figma API integration\to_kivy.py"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output_label.config(text=result.stdout)  # عرض المخرجات داخل label

root = tk.Tk()
root.title("Main Application")

# إنشاء Frame لعرض المحتوى داخل نافذة Tkinter
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

# Button لتشغيل الكود
run_button = tk.Button(root, text="Run Python Script", command=run_script)
run_button.pack()

# Label لعرض النتيجة
output_label = tk.Label(root, text="Output will appear here...")
output_label.pack()

root.mainloop()
