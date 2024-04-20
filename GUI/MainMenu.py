import customtkinter as ctk
import re
from datetime import date
from EntryPage import EntryPage
from firstPage import FirstPage
import os
from multiprocessing import Pool
from VacationsPage import VacationsPage
import GenHelpers
import helpers
from PIL import ImageTk, Image
from style import *




class MainMenu():
    def render_First_Page(self):
        fp = FirstPage()
        # self.first_window_root.focus_force()
        
        return

    
    def render_Entry_Page(self):
        # self.first_window_root.destroy()
        # self.first_window_root.iconify()
        ep = EntryPage().renderEntryPage()
        # self.first_window_root.deiconify()
        return
    
    def render_Vacations_Page(self):
        # self.first_window_root.iconify()
        vp = VacationsPage()
        # self.first_window_root.deiconify()
        return
    

    def Print_Tamam(self):
        filepath = ctk.filedialog.asksaveasfilename(initialdir = os.path.curdir,
                                          title = "Name the output PDF",
                                          filetypes = (('Pdf Files', '*.pdf*'),))
        GenHelpers.Export_Tamam_PDF(filepath)


    def Print_Vac_Passes(self):
        filepath = ctk.filedialog.asksaveasfilename(initialdir = os.path.curdir,
                                         title = "Name the output PDF",
                                          filetypes = (('Pdf Files', '*.pdf*'),))
        GenHelpers.Export_Vacation_Passes_PDF(filepath)
    


    def __init__(self):
        
        self.initial_visit = False
        self.first_window_root = ctk.CTk(fg_color=BG_COLOR)
        
        self.first_window_root.title("Secretary Assistant")
        self.first_window_root.geometry("1000x600")  # Set window size
        self.first_window_root.iconbitmap("../data/icolog.ico")
        img= ctk.CTkImage(light_image=Image.open('../data/logo_dark.png'), dark_image=Image.open('../data/logo_dark.png'), size=(250,250))
        ImageLBL = ctk.CTkLabel(self.first_window_root, width=self.first_window_root.winfo_width(), height=self.first_window_root.winfo_height(), image=img, text='')
        ImageLBL.place(relx=0.88, rely=0.15, anchor=ctk.CENTER)

        self.bg_img= ctk.CTkImage(light_image=Image.open('../data/BG_logo.png'), dark_image=Image.open('../data/BG_logo.png'), size=(500,500))
        bg_img_lbl = ctk.CTkLabel(self.first_window_root, width=self.first_window_root.winfo_width(), height=self.first_window_root.winfo_height(), image=self.bg_img, text='')
        bg_img_lbl.place(relx=0, rely=0.52, anchor=ctk.CENTER)

        dummy_frame = ctk.CTkFrame(self.first_window_root, width=400, fg_color=BG_COLOR, corner_radius=30)
        dummy_frame.place(relx=0.5, rely=0.1, anchor=ctk.N)

        # The titel label
        Big_Label = ctk.CTkLabel(dummy_frame, text="Secretary Assistant", font=('Arial', 50, 'bold'), text_color=BUTTON_COLOR)
        Big_Label.grid(row=1, pady=30, padx=20)

        #Tammam printing Button
        Tammam_Button = ctk.CTkButton(dummy_frame, text='طباعة تمام اليوم', command=self.Print_Tamam, font=('Arial', 17, 'bold'), fg_color=BUTTON_COLOR)
        Tammam_Button.grid(row=2, pady=30)

        #Vacations Entry Button
        Vacations_Entry_Button = ctk.CTkButton(dummy_frame, text='تسجيل أجازات', command=self.render_Vacations_Page, font=('Arial', 17, 'bold'), fg_color=BUTTON_COLOR)
        Vacations_Entry_Button.grid(row=3, pady=30)

        #Vacations pass printing button
        Vacations_print_Button = ctk.CTkButton(dummy_frame, text='طباعة اجازات', command=self.Print_Vac_Passes, font=('Arial', 17, 'bold'), fg_color=BUTTON_COLOR)
        Vacations_print_Button.grid(row=4, pady=30)

        #Vacations pass printing button
        Vacations_print_Button = ctk.CTkButton(dummy_frame, text='إدخال/تعديل البيانات', command=self.render_Entry_Page, font=('Arial', 17, 'bold'), fg_color=BUTTON_COLOR)
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
        if(not os.path.isfile('../db/Soldiers.db') or (not helpers.fetchSoldiers())):
            self.first_window_root.after(50, self.render_First_Page)



        self.first_window_root.bind("<Configure>", lambda x: self.resizeAll())
        
        self.first_window_root.bind('<Control-q>', lambda x: self.quit())

        self.first_window_root.after(20000, self.RefreshVacations)

        self.first_window_root.mainloop()

    def RefreshVacations(self):
        helpers.RefreshVacations()
        self.first_window_root.after(20000, self.RefreshVacations)
    

    def resizeAll(self):
        self.width = self.first_window_root.winfo_width()
        self.height = self.first_window_root.winfo_height()
        self.bg_img.configure(size=(self.width / 2, self.width / 2))

        # self.big_Entire_Frame.configure(height=self.root.winfo_height()/3)


    def quit(self):
        self.first_window_root.quit()


        












if __name__ == "__main__":
    mm = MainMenu()