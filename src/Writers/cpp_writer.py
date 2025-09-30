def write(line, output_file):
    """
    Writes a line to a file.
    Args:
        line (str): The line to write to the file.
        output_file (str): The path to the file to write to.
    """
    if output_file:
        with open(output_file, 'a', encoding='utf-8') as file:
            if line == "close()":
                file.close()
            else:
                file.write(line)
    else:
        print("No output file specified. Line not written.") 