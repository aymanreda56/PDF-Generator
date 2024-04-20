import customtkinter as ctk
import re
from datetime import date
import sqlite3
import os
from helpers import CreateDB
# from MainMenu import MainMenu
from EntryPage import EntryPage
from PIL import Image, ImageTk
from style import *




class FirstPage():
    def __init__(self):

        self.first_window_root = ctk.CTkToplevel(fg_color=BG_COLOR)
        self.first_window_root.title("Secretary Assistant")
        self.first_window_root.geometry("1200x600")  # Set window size

        self.bg_img= ctk.CTkImage(light_image=Image.open('../data/BG_logo.png'), dark_image=Image.open('../data/BG_logo.png'), size=(400,400))
        ImageLBL = ctk.CTkLabel(self.first_window_root, width=self.first_window_root.winfo_width(), height=self.first_window_root.winfo_height(), image=self.bg_img, text='')
        ImageLBL.place(relx=0.92, rely=0.92, anchor=ctk.CENTER)

        # The titel label
        Big_Label = ctk.CTkLabel(self.first_window_root, text="Secretary Assistant", font=('cooper black gothic', 50, 'bold'), text_color=BUTTON_COLOR)
        Big_Label.place(relx = 0.5, rely = 0.2, anchor=ctk.CENTER)


        First_Time_question_Label = ctk.CTkLabel(self.first_window_root, text=": اذا كنت أول مرة لإستعمالك هذا البرنامج, فنرجو إدخال بيانات الإدارة من هنا", font=('cooper black gothic', 30, 'bold'), text_color=BUTTON_COLOR, fg_color=BG_COLOR)
        First_Time_question_Label.place(relx=0.5, rely=0.4, anchor='center')

        Proceed_Button = ctk.CTkButton(self.first_window_root, text='Proceed', command=self.render_Entry_Page, fg_color=BUTTON_COLOR, font=('Arial', 30, 'bold'), width=150, corner_radius=30)
        Proceed_Button.place(relx=0.5, rely= 0.7, anchor='center')

        self.first_window_root.bind("<Configure>", lambda x: self.resizeAll())

        self.first_window_root.mainloop()


    def resizeAll(self):
        self.width = self.first_window_root.winfo_width()
        self.height = self.first_window_root.winfo_height()
        self.bg_img.configure(size=(self.width / 2, self.width / 2))

    
    def render_Entry_Page(self):
        
        CreateDB()
        self.first_window_root.destroy()
        
        # mm = MainMenu(firstTime=True)
        ep = EntryPage().renderEntryPage()
        # self.render_Main_Menu()
        # print('\n\n\nHEREERERE\n\n\n')
        # print(ep)
        # print('\n\n\n\n\n\n')

    
    # def render_Main_Menu(self):
    #     if(self.first_window_root):
    #         self.first_window_root.destroy()
    #     mm = MainMenu()
