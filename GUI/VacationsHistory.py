import customtkinter as ctk
import re, math
from datetime import date
from enums import EntryError, EntryErrorCode, ArmyLevels
# from MainMenu import MainMenu
import helpers
from style import *

FONT_STYLE = 'Dubai'


class VacationsHistory():
    def __init__(self):
        self.root = ctk.CTk(fg_color=BG_COLOR)

        self.root.title("تنظيم و أفراد مكتب السيد/ مدير الجهاز")
        screen_width, screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        width, height = 1700, 900
        self.root.geometry(f"{width}x{height}+{str(math.floor(screen_width/2 - width/2))}+{str(math.floor(screen_height/2 - height/2))}")  # Set window size
        self.root.iconbitmap("../data/icolog.ico")

        BigLabel = ctk.CTkLabel(master=self.root, text='عرض كل الأجازات', font=(FONT_STYLE, 60, 'bold'),text_color=TEXT_COLOR)
        BigLabel.pack()

        self.root.mainloop()




VacationsHistory()