import customtkinter as ctk
import re
from datetime import date
import os
import GenHelpers
import helpers
from PIL import ImageTk, Image
from style import *


def doSomething(LoginScreen):
    def prime_generator():
        """Generate prime numbers indefinitely."""
        primes = []  # List to store generated prime numbers
        num = 2      # Start with the first prime number
        while True:
            is_prime = True
            for prime in primes:
                if num % prime == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(num)
                yield num
            num += 1


    def generate_prime_greater_than(number:int):
        prime_gen = prime_generator()
        returned_number = 1
        while returned_number < number:
            returned_number = next(prime_gen)
        return returned_number



    big_number = 100000
    num = generate_prime_greater_than(100000)
    LoginScreen.logged_in_flag = True
    LoginScreen.root.destroy()








class LoginScreen():


    def resizeAll(self):
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        self.bg_img.configure(size=(width / 2, width / 2))

        # self.big_Entire_Frame.configure(height=self.self.root.winfo_height()/3)


    def __init__(self):
        self.logged_in_flag = False
        self.root = ctk.CTk(fg_color=BG_COLOR)
        self.root.title("تنظيم وأفراد مكتب السيد مدير الجهاز")
        self.root.geometry("1500x600")  # Set window size
        self.root.iconbitmap("../data/icolog.ico")


        img= ctk.CTkImage(light_image=Image.open('../data/logo_dark.png'), dark_image=Image.open('../data/logo_dark.png'), size=(250,250))
        ImageLBL = ctk.CTkLabel(self.root, width=self.root.winfo_width(), height=self.root.winfo_height(), image=img, text='')
        ImageLBL.place(relx=0.88, rely=0.15, anchor=ctk.CENTER)

        self.bg_img= ctk.CTkImage(light_image=Image.open('../data/BG_logo.png'), dark_image=Image.open('../data/BG_logo.png'), size=(500,500))
        self.bg_img_lbl = ctk.CTkLabel(self.root, width=self.root.winfo_width(), height=self.root.winfo_height(), image=self.bg_img, text='')
        self.bg_img_lbl.place(relx=0, rely=0.52, anchor=ctk.CENTER)



        # The titel label
        Big_Label = ctk.CTkLabel(self.root, text="تنظيم وأفراد مكتب السيد مدير الجهاز", font=('Arial', 50, 'bold'), text_color=BUTTON_COLOR)
        Big_Label.place(relx = 0.5, rely= 0.1, anchor = ctk.CENTER)


        username_Entry = ctk.CTkEntry(self.root, placeholder_text='اسم المستخدم', font=('Arial', 30, 'bold'), justify='right', width=300)
        username_Entry.place(relx = 0.5, rely=0.35, anchor=ctk.CENTER)

        password_Entry = ctk.CTkEntry(self.root, placeholder_text='كلمة السر', font=('Arial', 30, 'bold'), justify='right', width=300)
        password_Entry.place(relx = 0.5, rely=0.45, anchor=ctk.CENTER)



        sumbit_Button =ctk.CTkButton(self.root, text='إدخال', font=('Arial', 30, 'bold'), width=100, command=lambda: doSomething(self))
        sumbit_Button.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)



        self.root.bind("<Configure>", lambda x: self.resizeAll())

        self.root.bind('<Control-q>', lambda: self.root.quit)


        self.root.mainloop()
        

