fileReadError = (1, "Error reading file from drive, please check file path.")

def print_error(err_inp_tuple):
    print("Error Code: " + str(err_inp_tuple[0]))
    print(err_inp_tuple[1])
    return