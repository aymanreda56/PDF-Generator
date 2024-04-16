import customtkinter as ctk
import re
from datetime import date
from EntryPage import *
import sqlite3
import os




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

        Proceed_Button = ctk.CTkButton(self.first_window_root, text='Proceed', command=lambda: self.render_Entry_Page(create_db_flag=True))
        Proceed_Button.place(relx=0.5, rely= 0.7)

        if(os.path.isfile('../db/Soldiers.db')):
            self.render_Entry_Page(create_db_flag=False)

        self.first_window_root.mainloop()

    
    def render_Entry_Page(self, create_db_flag):
        
        if(create_db_flag):
            CreateDB()
        self.first_window_root.withdraw()
        ep = EntryPage()
        print('\n\n\nHEREERERE\n\n\n')
        print(ep)
        print('\n\n\n\n\n\n')





def CreateDB():
    try:
        # create connection to database 
        connection = sqlite3.connect('../db/Soldiers.db')

        cursor = connection.cursor()

        result = cursor.execute('''CREATE TABLE Force (
            "Soldier_ID"	TEXT NOT NULL UNIQUE,
            "Name"	TEXT NOT NULL,
            "Level"	INTEGER NOT NULL,
            "Retiring_Date"	TEXT,
            PRIMARY KEY("Soldier_ID")
        );''')

        result = cursor.execute('''CREATE TABLE "Vacations" (
            "Soldier_ID"	TEXT NOT NULL UNIQUE,
            "Name"	TEXT NOT NULL,
            "From_Date"	TEXT NOT NULL,
            "To_Date"	TEXT NOT NULL,
            FOREIGN KEY("Soldier_ID")  REFERENCES Force ("Soldier_ID")
        );''')

        result = cursor.execute('''CREATE TABLE "Missions" (
        "Soldier_ID"	TEXT NOT NULL UNIQUE,
        "Name"	TEXT NOT NULL,
        "From_Date"	TEXT NOT NULL,
        "To_Date"	TEXT NOT NULL,
        "Place"	TEXT,
        FOREIGN KEY("Soldier_ID") REFERENCES Force ("Soldier_ID")
        )''')


        connection.commit()


    except sqlite3.Error as e:
        print(e)

    finally:
        cursor.close()





fp = FirstPage()