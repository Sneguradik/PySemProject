import tkinter as tk
from .Components import CustomButton, Header
from .Resources import conf


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=conf['color']['background'])
        Header(self, controller)
        CustomButton(self, text="Click", command=lambda: controller.show_frame(ChartPage))

    name = "MainPage"


class ChartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        Header(self, controller)

        button = tk.Button(self, text="Back to Start Page",
                           command=lambda: controller.show_frame(StartPage))
        button.pack()

    name = "ChartPage"


class DataPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        Header(self, controller)

        button = tk.Button(self, text="Back to Starddt Page",
                           command=lambda: controller.show_frame(StartPage))
        button.pack()

    name = "DataPage"
