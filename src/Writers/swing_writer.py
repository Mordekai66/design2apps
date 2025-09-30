def write(line, output_file):
    """
    This function writes a line to the specified output file for Swing code generation.
    """
    if output_file:
        with open(output_file, 'a', encoding="utf-8") as file:
            if line == "close()":
                file.close()
                print(f"File closed: {output_file}")
            else:
                file.write(line)
    else:
        print("No output file specified. Line not written.") 