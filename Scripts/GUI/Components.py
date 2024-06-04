from .Resources import conf, get_font
import tkinter as tk


class CustomButton(tk.Button):
    def __init__(self, parent, text, command, *args, **kwargs):
        self.bg = conf['color']['primary2']
        self.fg = conf['color']['primary1']

        super().__init__(parent, bg=self.bg, fg=self.fg, text=text, command=command, font=get_font(), *args, **kwargs)

        self.pack()


class Header(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, pady=10, *args, **kwargs)

        self.pack(side=tk.TOP, fill=tk.X)

        self.create_buttons()
        self.controller = controller

    def create_buttons(self):
        home_button = CustomButton(self, text="Главная", command=self.__show_home)
        charts_button = CustomButton(self, text="Графики", command=self.__show_charts)
        data_button = CustomButton(self, text="Данные", command=self.__show_data)

        home_button.pack(side=tk.LEFT, padx=10)
        charts_button.pack(side=tk.LEFT, padx=10)
        data_button.pack(side=tk.LEFT, padx=10)

    def __show_page(self, page_name: str):
        page = None
        for frame in self.controller.frames:
            if frame.name == page_name: page = frame
        if page is not None:
            self.controller.show_frame(page)

    def __show_home(self):
        self.__show_page("MainPage")


    def __show_charts(self):
        self.__show_page("ChartPage")

    def __show_data(self):
        self.__show_page("DataPage")
