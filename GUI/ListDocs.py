import customtkinter as ctk
import re
from datetime import date
import os
import GenHelpers
import helpers
from PIL import ImageTk, Image
from style import *
from enc import enc



font_style = 'Dubai'





class ListDocs():

    def Personal_Card(self, first_name, rest_of_name, job_description, soldier_ID, date_of_termination:str, mobile_number, image_path):
        Card_Frame = ctk.CTkFrame(master=self.Frame_For_List, width=250, height=545, fg_color='#150F30')
        Card_Frame.grid(column = 0)


        img= ctk.CTkImage(light_image=Image.open(image_path), dark_image=Image.open(image_path), size=(225,225))
        ImageLBL = ctk.CTkLabel(Card_Frame, width=225, height=226, image=img, text='')
        ImageLBL.grid(row = 0, pady=12, padx=12)

        First_Name_Lbl = ctk.CTkLabel(Card_Frame, text=first_name, font=(font_style, 32, 'bold'), justify='right', text_color=WHITE_TEXT_COLOR)
        First_Name_Lbl.grid(row = 1, pady=0, padx = 12, sticky='e')

        Rest_Of_Name_Lbl = ctk.CTkLabel(Card_Frame, text=rest_of_name, font=(font_style, 20), justify='right', text_color=WHITE_TEXT_COLOR)
        Rest_Of_Name_Lbl.grid(row = 2, pady=0, padx = 12, sticky='e')

        Job_Description_Lbl = ctk.CTkLabel(Card_Frame, text='الوظيفة: ' + job_description , font=(font_style, 20), justify='right', text_color=WHITE_TEXT_COLOR)
        Job_Description_Lbl.grid(row = 3, pady=10, padx = 12, sticky='e')

        Soldier_ID_Lbl = ctk.CTkLabel(Card_Frame, text=soldier_ID , font=(font_style, 20), justify='right', text_color=WHITE_TEXT_COLOR)
        Soldier_ID_Lbl.grid(row = 4, pady=10, padx = 12, sticky='e')


        Date_Of_Term_Lbl = ctk.CTkLabel(Card_Frame, text='تاريخ الرديف: ' + date_of_termination , font=(font_style, 20), justify='right', text_color=WHITE_TEXT_COLOR)
        Date_Of_Term_Lbl.grid(row = 5, pady=10, padx = 12, sticky='e')


        Mobile_Number_Lbl = ctk.CTkLabel(Card_Frame, text='موبايل: ' + mobile_number , font=(font_style, 20), justify='right', text_color=WHITE_TEXT_COLOR)
        Mobile_Number_Lbl.grid(row = 6, pady=10, padx = 12, sticky='e')











    def __init__(self):
        self.root = ctk.CTk(fg_color=BG_COLOR)
        self.root.geometry('1360x775')
        self.root.title(font_style)
        self.Frame_For_List = ctk.CTkScrollableFrame(master=self.root, height=1000 , width=1000, orientation='horizontal', fg_color=BG_COLOR)
        self.Frame_For_List.pack()


        self.Personal_Card(first_name='أيمن', rest_of_name='محمد رضا عبده', job_description='فريق البحث و التطوير', soldier_ID='12453185132', date_of_termination= date.today().isoformat(), mobile_number='01225838009', image_path='../db/Soldier_Photos/ayman.png')

        # self.Frame_For_Buttons = ctk.CTkFrame(self.root)
        # self.Frame_For_Buttons.pack()



        self.root.mainloop()




ListDocs()