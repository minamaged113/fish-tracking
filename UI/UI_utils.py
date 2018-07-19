from tkinter import filedialog


fileTypeTuple = ( ("ARIS files", "*.aris"), ("All files", "*.*"))

def getFilePath(root):
    root.fileName = filedialog.askopenfilename(filetypes = fileTypeTuple)
    return root.fileName

def show_frame():
    pass