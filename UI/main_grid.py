"""
This file will handle GUI of Fisher software
Author: Mina Ghobrial
Date: July 19th, 2018

"""
import tkinter as tk
from PIL import Image, ImageTk
import UI_utils as ui 
from tkinter import ttk

color_codes = {
    "foreground" : "#999999",
    "comment" : "#777777",
    "lightInActiveBG": "#333333" ,
    "inActiveBG": "#222222",
    "background" : "#111111"
}
fonts = {
    "normalText": ("Century Gothic", 12),
    "title": ("Times New Roman", 26, "bold"),
    "subtitle": ("Time New Roman", 18, "italic"),
    "heading1": ("Century Gothic", 20),
    "heading2": ("Century Gothic", 17),
    "heading3": ("Century Gothic", 14)
}
frames = {}

class fisher_main(tk.Tk):
    # class initializer
    HOLDING_VARIABLE = None
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self,  *args, **kwargs)
        tk.Tk.wm_title(self, "Fishery")
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.HOLDING_VARIABLE = container
        self.frames_tuple = (
            welcomeScreen,
        )
        for frame in self.frames_tuple:
            handle = frame(container, self)
            frames[frame] = handle
            handle.grid(row = 0, column = 0, sticky = "nsew")
        self.show_frame(welcomeScreen)

    def show_frame(self, controller):
        frame = frames[controller]
        frame.tkraise()

    def showFramesScreen(self, filePath):
        handle = framePage(self.HOLDING_VARIABLE,  self, filePath = filePath)
        frames[framePage] = handle
        frame = handle
        frame.tkraise()
        

class welcomeScreen(tk.Frame):
    # this will be the first page loaded when the application
    # is launched for the first time
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.bg = color_codes["background"]
        self.cursor = "circle"
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)



        topLabel = tk.Label( self,
                        font = fonts["title"],
                        text = "Welcome to Fisher",
                        bg = color_codes["background"],
                        fg = color_codes["foreground"]).grid(in_=self, sticky = "NEWS")

        # self.grid_rowconfigure(1, weight = 0)
        # self.grid_columnconfigure(0, weight = 1)
        middle = tk.Frame(self, bg = color_codes["inActiveBG"])
        openFileBTN = tk.Button(self,
                                text = "Open File",
                                relief = tk.FLAT,
                                command = lambda: controller.showFramesScreen(filePath = ui.openFile(self))).grid(row = 2, in_ = self)

        
        
class framePage(tk.Frame):
    def __init__(self, parent, controller, filePath):
        tk.Frame.__init__(self, parent)
        self.bg = color_codes["background"]
        self.cursor = "circle"
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        print(filePath)
        canvas = tk.Canvas(self)

        


main= fisher_main()
main.mainloop()