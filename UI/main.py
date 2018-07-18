"""
This file will handle GUI of Fisher software
Author: Mina Ghobrial
Date: July 19th, 2018

"""
import tkinter as tk
from PIL import Image, ImageTk

color_codes = {
    "foreground" : "#999999",
    "comment" : "#777777",
    "lightInActiveBG": "#333333" ,
    "inActiveBG": "#222222",
    "background" : "#111111"
}

class fisher_main(tk.Tk):
    # class initializer
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self,  *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}
        self.frames_tuple = (
            welcomeScreen,
        )
        for frame in self.frames_tuple:
            handle = frame(container, self)
            self.frames[frame] = handle
            handle.grid(row = 0, column = 0, sticky = "nsew")
        self.show_frame(welcomeScreen)

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()

class welcomeScreen(tk.Frame):
    # this will be the first page loaded when the application
    # is launched for the first time
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        frame = tk.Frame(self)
        frame.grid_rowconfigure(0, weight = 1)
        frame.grid_columnconfigure(0, weight = 1)
        # frame.grid(row = 0, column = 0, sticky = "nsew")
        im = Image.open("Figures/images.jpeg")
        im = ImageTk.PhotoImage(im)
        topBar = tk.Label(self ,text = "\t\t\t\t\t\t", bg = color_codes["background"]).grid(row = 0 ,column = 0,sticky = "w", columnspan =5 )
        leftSideBar = tk.Label(self , bg = color_codes["inActiveBG"]).grid(row = 1 ,column = 0,sticky = "w" )

        rightSideBar = tk.Label(self , bg = color_codes["lightInActiveBG"]).grid(row = 1 ,column = 1,sticky = "w" )
        




main= fisher_main()
main.mainloop()