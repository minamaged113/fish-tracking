"""
This file will handle GUI of Fisher software
Author: Mina Ghobrial
Date: July 19th, 2018

"""
import tkinter as tk
from PIL import Image, ImageTk
import UI_utils as ui 

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

class fisher_main(tk.Tk):
    # class initializer
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self,  *args, **kwargs)
        tk.Tk.wm_title(self, "Fishery")
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}
        self.frames_tuple = (
            welcomeScreen,
            # framePage
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
        im = Image.open("Figures/images.jpeg")
        im = ImageTk.PhotoImage(im)
        
        top = tk.Label( self,
                        font = fonts["title"],
                        text = "Welcome to Fisher",
                        bg = color_codes["background"],
                        fg = color_codes["foreground"]).pack(side = tk.TOP, fill = tk.BOTH)

        middle = tk.Label(  self,
                            bg = color_codes["inActiveBG"]).pack(side = tk.TOP,
                                                                fill = tk.BOTH,
                                                                expand = True)

        openFileBTN = tk.Button(middle,
                                text = "Open File",
                                command = lambda: ui.getFilePath(self)).pack(fill = tk.BOTH, side = tk.TOP )

        bottom = tk.Label(self , bg = color_codes["background"]).pack(  side = tk.TOP, 
                                                                        fill = tk.BOTH)
        
        
# class framePage(tk.Frame):
#     def __init__(self, parent, controller):
        
        


main= fisher_main()
main.mainloop()