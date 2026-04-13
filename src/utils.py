import os
import requests
import json
from tkinter import messagebox

def validate_output_dir(output_path):
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

def validate_figma_fields(token, fileID):
    if not fileID:
        messagebox.showerror("Error", "File ID is empty")
        return False
    if not token:
        messagebox.showerror("Error", "Token is empty")
        return False
    return True

def validate_figma_token(token, file_id):
    url = f"https://api.figma.com/v1/files/{file_id}"
    headers = {"X-Figma-Token": token}

    try:
        response = requests.get(url, headers=headers, timeout=10)
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
    if response.status_code == 401:
        messagebox.showerror("Error", "Unauthorized access - check your token")
        return False
    if response.status_code == 429:
        messagebox.showerror("Error", "Rate limit exceeded - please try again later")
        return False

    messagebox.showerror("Error", f"Unexpected error: {response.status_code}")
    return False

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % (int(rgb['r'] * 255), int(rgb['g'] * 255), int(rgb['b'] * 255))
def rgb_to_rgb_swing(rgb):
    return f"new Color({int(rgb['r'] * 255)}, {int(rgb['g'] * 255)}, {int(rgb['b'] * 255)})"
def rgb_to_rgb_cpp(rgb):
    return f"QColor({int(rgb['r'] * 255)}, {int(rgb['g'] * 255)}, {int(rgb['b'] * 255)})"