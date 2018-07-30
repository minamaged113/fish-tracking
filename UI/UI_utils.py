from tkinter import filedialog


fileTypeTuple = ( ("ARIS files", "*.aris"), ("All files", "*.*"))

def openFile(root):
    root.fileName = filedialog.askopenfilename(filetypes = fileTypeTuple)
    # root.show_frame[]
    return root.fileName

def show_frame():
    pass