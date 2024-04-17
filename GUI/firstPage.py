import customtkinter as ctk
import re
from datetime import date
import sqlite3
import os
from helpers import CreateDB
# from MainMenu import MainMenu
from EntryPage import EntryPage



class FirstPage():
    def __init__(self):

        self.first_window_root = ctk.CTk()
        self.first_window_root.title("Secretary Assistant")
        self.first_window_root.geometry("1200x600")  # Set window size

        # The titel label
        Big_Label = ctk.CTkLabel(self.first_window_root, text="Secretary Assistant", font=('cooper black gothic', 50, 'bold'))
        Big_Label.pack()


        First_Time_question_Label = ctk.CTkLabel(self.first_window_root, text="اذا كنت أول مرة لإستعمالك هذا البرنامج, فنرجو إدخال بيانات الإدارة من هنا:", font=('cooper black gothic', 20, 'bold'))
        First_Time_question_Label.place(relx=0.5, rely=0.4, anchor='center')

        Proceed_Button = ctk.CTkButton(self.first_window_root, text='Proceed', command=self.render_Entry_Page)
        Proceed_Button.place(relx=0.5, rely= 0.7)

        

        self.first_window_root.mainloop()

    
    def render_Entry_Page(self):
        
        CreateDB()
        self.first_window_root.destroy()
        
        # mm = MainMenu(firstTime=True)
        # ep = EntryPage()
        # self.render_Main_Menu()
        # print('\n\n\nHEREERERE\n\n\n')
        # print(ep)
        # print('\n\n\n\n\n\n')

    
    # def render_Main_Menu(self):
    #     if(self.first_window_root):
    #         self.first_window_root.destroy()
    #     mm = MainMenu()



# fp = FirstPage()