def write(line, file_path):
    """
    Write a line to a file.

    Args:
        line (str): The line to write.
        file (file object): The file to write to.
    """
    if file_path:

        with open(file_path, 'a', encoding="utf-8") as file:
            if line == "close()":
                file.close()
                print("File closed: kivy_code.py")
            else:
                file.write(line)
    else:
        print("No output file specified. Line not written.")