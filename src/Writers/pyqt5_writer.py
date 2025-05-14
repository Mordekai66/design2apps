def write(line, file_path):
    """Writes the given line to the specified file.
    Args:
        line (_type_):  _description_
        file_path (_type_): _description_   
    """
    if file_path:
        with open(file_path, "a", encoding="utf-8") as file:
            if line == "close()":
                file.close()
                print("File closed: pyqt5.py")
            else:
                file.write(line)
    else:
        print("File path is empty. Cannot write to file.")