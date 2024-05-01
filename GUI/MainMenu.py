import customtkinter as ctk

from EntryPage import EntryPage
from firstPage import FirstPage
import os, math
from multiprocessing import Pool, Process, freeze_support
from VacationsPage import VacationsPage
from LoginScreen import LoginScreen
import GenHelpers
import helpers
from PIL import ImageTk, Image
from style import *

which_frame_is_active = None

font_text ='Arial'




class MainMenu():


    def ChangeAllFonts(self):
        
        newFont = FONTS[self.fontindex]
        allTextualWidgets = [self.Big_Label, self.Entry_Button, self.Movement_print_Button, self.Tammam_Button, self.Vacations_print_Button, self.Vacations_Entry_Button]
        for widget in allTextualWidgets:
            wfont = list(widget.cget('font'))
            wfont[0] = newFont
            widget.configure(font=tuple(wfont))
        self.fontindex += 1
        if self.fontindex == len(FONTS): self.fontindex = 0




    def LoadingWindow(self):
        if(not self.LoadingImageLbl):
            print('\n\n\nLOADING Begin')
            Loadingimg= ctk.CTkImage(light_image=Image.open('../data/LoadingScreen2.png'), dark_image=Image.open('../data/LoadingScreen2.png'), size=(600,600))
            self.LoadingImageLbl = ctk.CTkLabel(self.first_window_root, width=self.first_window_root.winfo_width(), height=self.first_window_root.winfo_height(), image=Loadingimg, text='', fg_color=BG_COLOR)
            self.LoadingImageLbl.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
    
    def removeLoadingWindow(self):
        print('\n\n\nLOADING END')
        if(self.LoadingImageLbl):
            self.LoadingImageLbl.destroy()
            self.LoadingImageLbl = None
        

    def render_First_Page(self):
        self.fp = FirstPage()
        self.fp.render()
        # self.first_window_root.focus_force()
        return

    
    def render_Entry_Page(self):
        self.ep = EntryPage()
        self.ep.renderEntryPage()
        return
    
    def render_Vacations_Page(self):
        self.vp = VacationsPage()
        self.vp.renderVacationsPage()
        return
    


    def Print_Tamam(self):
        self.Tmam_Process = Process(target=GenHelpers.Export_Tamam_PDF)
        self.Tmam_Process.start()


        

    
    def Print_Movements(self):
        self.Tmam_Process = Process(target=GenHelpers.Export_Movements_PDF)
        self.Tmam_Process.start()



    def Print_Vac_Passes(self):
        self.Tmam_Process = Process(target=GenHelpers.Export_Vacation_Passes_PDF)
        self.Tmam_Process.start()
    


    def __init__(self):

        if(not os.path.isfile(helpers.DB_PATH) or (not helpers.fetchSoldiers())):
                self.initial_visit = True
        else: self.initial_visit = False
        self.logged_in_flag = False
        self.vp = False
        self.fp = False
        self.ep = False
        self.Tmam_Process = None
        self.LoadingImageLbl = None
        self.fontindex = 0
        
        

        if(self.initial_visit):
            self.logged_in_flag = True
            self.is_admin = 1
        else:
            ls = LoginScreen()
            self.logged_in_flag = ls.logged_in_flag
            self.user_level = ls.level
            self.user_name = ls.name
            self.is_admin = ls.is_admin

        if(self.logged_in_flag):
            self.initial_visit = False
            self.first_window_root = ctk.CTk(fg_color=BG_COLOR)
            self.main_was_active = True

            
            self.first_window_root.title("تنظيم و أفراد مكتب السيد/ مدير الجهاز")
            screen_width, screen_height = self.first_window_root.winfo_screenwidth(), self.first_window_root.winfo_screenheight()
            width, height = 1500, 900
            self.first_window_root.geometry(f"{width}x{height}+{str(math.floor(screen_width/2 - width/2))}+{str(math.floor(screen_height/2 - height/2))}")  # Set window size
            self.first_window_root.iconbitmap("../data/icolog.ico")
            img= ctk.CTkImage(light_image=Image.open('../data/logo_dark.png'), dark_image=Image.open('../data/logo_dark.png'), size=(250,250))
            self.ImageLBL = ctk.CTkLabel(self.first_window_root, width=self.first_window_root.winfo_width(), height=self.first_window_root.winfo_height(), image=img, text='')
            self.ImageLBL.place(relx=0.88, rely=0.15, anchor=ctk.CENTER)


            



            # self.office_img= ctk.CTkImage(light_image=Image.open('../data/office_img.png'), dark_image=Image.open('../data/office_img.png'), size=(200,200))
            # OfficeImageLBL = ctk.CTkLabel(self.first_window_root, width=self.first_window_root.winfo_width(), height=self.first_window_root.winfo_height(), image=self.office_img, text='')
            # OfficeImageLBL.place(relx=0.1, rely=0.18, anchor=ctk.CENTER)

            dummy_frame = ctk.CTkFrame(self.first_window_root, width=400, fg_color=BG_COLOR, corner_radius=30)
            dummy_frame.place(relx=0.5, rely=0.1, anchor=ctk.N)

            # The titel label
            self.Big_Label = ctk.CTkLabel(dummy_frame, text="تنظيم و افراد مكتب السيد/ مدير الجهاز", font=(font_text, 50, 'bold'), text_color=BUTTON_COLOR)
            self.Big_Label.grid(row=1, pady=30, padx=20)

            #Tammam printing Button
            self.Tammam_Button = ctk.CTkButton(dummy_frame, text='طباعة تمام اليوم', command=self.Print_Tamam, font=(font_text, 25, 'bold'), fg_color=BUTTON_COLOR, width=200, corner_radius=30)
            self.Tammam_Button.grid(row=2, pady=30)

            #Vacations Entry Button
            self.Vacations_Entry_Button = ctk.CTkButton(dummy_frame, text='تسجيل أجازات', command=self.render_Vacations_Page, font=(font_text, 25, 'bold'), fg_color=BUTTON_COLOR, width=200, corner_radius=30)
            self.Vacations_Entry_Button.grid(row=3, pady=30)
            if(self.is_admin != '1'):
                self.Vacations_Entry_Button.grid_forget()

            #Movement printing button
            self.Movement_print_Button = ctk.CTkButton(dummy_frame, text='طباعة يومية تحركات', command=self.Print_Movements, font=(font_text, 25, 'bold'), fg_color=BUTTON_COLOR, width=200, corner_radius=30)
            self.Movement_print_Button.grid(row=4, pady=30)

            #Vacations pass printing button
            self.Vacations_print_Button = ctk.CTkButton(dummy_frame, text='طباعة تصاريح الأجازات', command=self.Print_Vac_Passes, font=(font_text, 25, 'bold'), fg_color=BUTTON_COLOR, width=200, corner_radius=30)
            self.Vacations_print_Button.grid(row=5, pady=30)

            #Vacations pass printing button
            self.Entry_Button = ctk.CTkButton(dummy_frame, text='إدخال/ تعديل البيانات', command=self.render_Entry_Page, font=(font_text, 25, 'bold'), fg_color=BUTTON_COLOR, width=200, corner_radius=30)
            self.Entry_Button.grid(row=6, pady=30)



            self.Change_Font_Button = ctk.CTkButton(self.first_window_root, text='تغيير الفونت', command=self.ChangeAllFonts, font=(font_text, 25, 'bold'), fg_color=BUTTON_COLOR, width=200, corner_radius=30)
            self.Change_Font_Button.place(relx=0.8, rely=0.8)



            if(self.is_admin != '1'):
                print('IAMMM')
                self.Entry_Button.grid_forget()


            if(not os.path.isfile(helpers.DB_PATH) or (not helpers.fetchSoldiers())):
                self.first_window_root.after(1, self.render_First_Page)







            self.first_window_root.bind("<Configure>", lambda x: self.resizeAll())
            
            self.first_window_root.bind('<Control-q>', lambda x: self.quit())

            self.first_window_root.after(1, self.MakeWindowAtTheFront)
            


            self.first_window_root.after(20000, self.RefreshVacations)
            self.first_window_root.after(1, self.CheckRunningThreadsForLoadingWindow)



            self.bg_img= ctk.CTkImage(light_image=Image.open('../data/BG_logo.png'), dark_image=Image.open('../data/BG_logo.png'), size=(500,500))
            bg_img_lbl = ctk.CTkLabel(self.first_window_root, width=self.first_window_root.winfo_width(), height=self.first_window_root.winfo_height(), image=self.bg_img, text='')
            bg_img_lbl.place(relx=0, rely=0.52, anchor=ctk.CENTER)
            

            self.first_window_root.mainloop()

    def RefreshVacations(self):
        helpers.RefreshVacations()
        self.first_window_root.after(20000, self.RefreshVacations)
    

    def resizeAll(self):
        self.width = self.first_window_root.winfo_width()
        self.height = self.first_window_root.winfo_height()
        self.bg_img.configure(size=(self.width / 2, self.width / 2))
        # self.office_img.configure(size=(self.width / 5, self.width / 5))

        # self.big_Entire_Frame.configure(height=self.root.winfo_height()/3)

    
    def CheckRunningThreadsForLoadingWindow(self):
        if(self.Tmam_Process):
            if(self.Tmam_Process.is_alive()):
                self.LoadingWindow()
            else:
                self.Tmam_Process = None
                self.removeLoadingWindow()
        
        self.first_window_root.after(1, self.CheckRunningThreadsForLoadingWindow)



    def quit(self):
        self.first_window_root.quit()



    def MakeWindowAtTheFront(self):
        main_is_active = True
        def helper(wind):
            
            try:
                    if(not wind.root.children):
                        return False
                    if(self.first_window_root.focus_get() == self.first_window_root):
                        wind.root.focus_set()
                        self.first_window_root.iconify()
                        self.main_was_active = False
                    return True
            except:
                return False
    
        if(helper(self.vp) or helper(self.ep) or helper(self.fp)):
            main_is_active = False
        else:
            main_is_active = True
            
        if(main_is_active and not self.main_was_active):
            self.first_window_root.deiconify()
            self.main_was_active = True
            
        self.first_window_root.after(1, self.MakeWindowAtTheFront)












if __name__ == "__main__":
    freeze_support()
    mm = MainMenu()