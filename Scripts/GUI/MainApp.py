import tkinter as tk
from .Pages import StartPage, ChartPage, DataPage
from .Components import Header



class SomeApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Multi-Screen Tkinter App")
        self.geometry("800x600")

        # A container that will contain all the frames
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)



        # Dictionary to hold the frames
        self.frames = {}

        for F in (StartPage, ChartPage, DataPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)



    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
