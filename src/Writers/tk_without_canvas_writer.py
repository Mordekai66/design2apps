def write(line, output_file):
    if output_file:
        with open(output_file, 'a', encoding="utf-8") as file:
            if line == "close()":
                file.close()
            else:
                file.write(line)
    else:
        print("No output file specified. Line not written.") 