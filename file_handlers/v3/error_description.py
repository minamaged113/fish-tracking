fileReadError = (1, "Error reading file from drive, please check file path.")
frameReadError = (2, "Error reading frame from file.")
jsonData = (3, "Error reading JSON data from the drive.")


def print_error(err_inp_tuple):
    print("Error Code: " + str(err_inp_tuple[0]))
    print(err_inp_tuple[1])
    return