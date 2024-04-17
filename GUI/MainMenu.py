import customtkinter as ctk
import re
from datetime import date
from EntryPage import EntryPage
from firstPage import FirstPage
import os
from multiprocessing import Pool
from VacationsPage import VacationsPage


class MainMenu():
    def render_First_Page(self):
        fp = FirstPage()
        return

    
    def render_Entry_Page(self):
        # self.first_window_root.destroy()
        ep = EntryPage().renderEntryPage()
        return
    
    def render_Vacations_Page(self):
        vp = VacationsPage()
        return
    


    def __init__(self):
        
        self.initial_visit = False
        self.first_window_root = ctk.CTk()
        self.first_window_root.title("Secretary Assistant")
        self.first_window_root.geometry("1000x600")  # Set window size

        dummy_frame = ctk.CTkFrame(self.first_window_root, width=400)
        dummy_frame.place(relx=0.5, rely=0.03, anchor=ctk.N)

        # The titel label
        Big_Label = ctk.CTkLabel(dummy_frame, text="Secretary Assistant", font=('cooper black gothic', 50, 'bold'))
        Big_Label.grid(row=1, pady=30)

        #Tammam printing Button
        Tammam_Button = ctk.CTkButton(dummy_frame, text='طباعة تمام اليوم', command=self.render_Entry_Page, font=('Arial', 17, 'bold'))
        Tammam_Button.grid(row=2, pady=30)

        #Vacations Entry Button
        Vacations_Entry_Button = ctk.CTkButton(dummy_frame, text='تسجيل أجازات', command=self.render_Entry_Page, font=('Arial', 17, 'bold'))
        Vacations_Entry_Button.grid(row=3, pady=30)

        #Vacations pass printing button
        Vacations_print_Button = ctk.CTkButton(dummy_frame, text='طباعة اجازات', command=self.render_Entry_Page, font=('Arial', 17, 'bold'))
        Vacations_print_Button.grid(row=4, pady=30)

        #Vacations pass printing button
        Vacations_print_Button = ctk.CTkButton(dummy_frame, text='إدخال/تعديل البيانات', command=self.render_Entry_Page, font=('Arial', 17, 'bold'))
        Vacations_print_Button.grid(row=5, pady=30)

        # if(not self.firstTime):
        #     self.first_window_root.mainloop()
        #     pass
        # else:
        #     self.render_Entry_Page()

        # FirstPage()
        
        # FirstPage()
            # th = threading.Thread(target=lambda:FirstPage(), daemon=True)
            # th.start()
        if(not os.path.isfile('../db/Soldiers.db')):
            self.first_window_root.after(50, self.render_First_Page)
        self.first_window_root.mainloop()

        


        













mm = MainMenu()