import customtkinter as ctk

from EntryPage import EntryPage
from firstPage import FirstPage
import os, math
from multiprocessing import Pool, Process, freeze_support
from VacationsPage import VacationsPage
from Vacations_Group_Page import Vacations_Group_Page
from LoginScreen import LoginScreen
import GenHelpers
import helpers
from PIL import ImageTk, Image
from style import *
from DocumentEntryPage import DocumentEntryPage
from ListDocs import ListDocs
import auto_updater
import VacationsHistory
from SettingsPage import SettingsPage

which_frame_is_active = None

font_text ='Dubai'




def global_updater():
    auto_updater.download_update(username='aymanreda56', reponame='secretary-assistant', versionfile='ver.txt', url=f'http://github.com/aymanreda56/secretary-assistant/archive/main.zip')





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
        self.initial_visit = False
        # self.first_window_root.focus_force()
        return

    
    def render_Entry_Page(self):
        self.ep = EntryPage()
        self.ep.renderEntryPage()
        return
    
    def render_Settings_Page(self):
        self.sp = SettingsPage()
        self.sp.renderSettingsPage()
        return
    
    def render_Vacations_Page(self):
        try:
            self.vp.quit()
        except:
            pass
        self.vp = VacationsPage(self.render_Group_Vacations_Page)
        self.vp.renderVacationsPage()
        return
    
    def render_Group_Vacations_Page(self):
        try:
            self.vp.quit()
        except:
            pass
        self.vp = Vacations_Group_Page(self.render_Vacations_Page)
        self.vp.render()
        return
    

    def EnterNewDocument(self):
        self.dep = DocumentEntryPage()
        self.dep.renderDocumentsEntryPage()
        return
    

    def ShowAllDocuments(self):
        self.ld = ListDocs()
        self.ld.renderListDocs()
        return
    


    def Print_Tamam(self):
        self.Tmam_Process = Process(target=GenHelpers.Export_Tamam_PDF)
        self.Tmam_Process.start()

    
    def Print_Vacations_History(self):
        self.Tmam_Process = Process(target=VacationsHistory.ExportVacationsHistory)
        self.Tmam_Process.start()


        

    
    def Print_Movements(self):
        self.Tmam_Process = Process(target=GenHelpers.Export_Movements_PDF)
        self.Tmam_Process.start()



    def Print_Vac_Passes(self):
        self.Tmam_Process = Process(target=GenHelpers.Export_Vacation_Passes_PDF)
        self.Tmam_Process.start()




    def ConfirmPage(self):
        self.ConfirmPageRoot = ctk.CTk(fg_color='#3C415E')
        screen_width, screen_height = self.ConfirmPageRoot.winfo_screenwidth(), self.ConfirmPageRoot.winfo_screenheight()


        width, height = 600, 200
        self.ConfirmPageRoot.geometry(f"{width}x{height}+{str(math.floor(screen_width/2 - width/2))}+{str(math.floor(screen_height/2 - height/2))}")  # Set window size
        self.ConfirmPageRoot.iconbitmap("../data/icolog.ico")
        self.ConfirmPageRoot.title(f"تحديث؟")


        text = 'التحديث يستغرق تقريبا 20 دقيقة,\nهل تريد التحديث الآن؟'
        text = text + '\nبرجاء إعادة فتح البرنامج بعد التحميل'
        confirmlbl = ctk.CTkLabel(master=self.ConfirmPageRoot, text=text, font=(font_text, 30, 'bold'))
        confirmlbl.pack(pady=10)
        
        confirmbutton = ctk.CTkButton(master=self.ConfirmPageRoot, text= 'تأكيد التحديث', fg_color=WARNING_COLOR, font=(font_text, 30, 'bold'), corner_radius=15, command=self.ConfirmUpdate, text_color='Black')
        confirmbutton.pack(pady=10)

        self.ConfirmPageRoot.bind('<Control-q>', lambda x: self.ConfirmPageRoot.destroy())

        self.ConfirmPageRoot.mainloop()

    
    def ConfirmUpdate(self):
        self.ConfirmPageRoot.destroy()
        self.Update()
        


    def Update(self):
        self.Tmam_Process = Process(target=global_updater)
        self.Tmam_Process.start()


    def __init__(self):

        if(not os.path.isfile(helpers.DB_PATH)):
                self.initial_visit = True
        else: self.initial_visit = False
        self.logged_in_flag = False
        self.vp = False
        self.fp = False
        self.ep = False
        self.dep = False
        self.ld = False
        self.sp = False
        self.Tmam_Process = None
        self.update_process = None
        self.LoadingImageLbl = None
        self.fontindex = 0


        is_update_available, new_version, new_version_str = auto_updater.check_For_Updates(username='aymanreda56', reponame='secretary-assistant', versionfile='ver.txt')
        if(is_update_available):
            update_color = WARNING_COLOR
            update_text = 'اضغط للتحديث'
            update_text_color = "Black"
        else:
            update_color = ACCEPT_COLOR
            update_text = 'هذه هي أحدث نسخة'
            update_text_color = TEXT_COLOR
        
        

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
            width, height = 1800, 900
            self.first_window_root.geometry(f"{width}x{height}+{str(math.floor(screen_width/2 - width/2))}+{str(math.floor(screen_height/2 - height/2))}")  # Set window size
            self.first_window_root.iconbitmap("../data/icolog.ico")
            img= ctk.CTkImage(light_image=Image.open(PROJ_LOGO), dark_image=Image.open(PROJ_LOGO), size=(250, 312.5 if CHOSEN_PRESET else 250))
            self.ImageLBL = ctk.CTkLabel(self.first_window_root, width=self.first_window_root.winfo_width(), height=self.first_window_root.winfo_height(), image=img, text='')
            self.ImageLBL.place(relx=0.88, rely=0.2, anchor=ctk.CENTER)

            self.bg_img= ctk.CTkImage(light_image=Image.open(BG_LOGO), dark_image=Image.open(BG_LOGO), size=(600,600))
            bg_img_lbl = ctk.CTkLabel(self.first_window_root, width=self.first_window_root.winfo_width(), height=self.first_window_root.winfo_height(), image=self.bg_img, text='')
            bg_img_lbl.place(relx=0, rely=0.52, anchor=ctk.CENTER)



            grass_img= ctk.CTkImage(light_image=Image.open(GRASS), dark_image=Image.open(GRASS), size=(1700,120))
            bottom_navbar = ctk.CTkLabel(self.first_window_root, width=self.first_window_root.winfo_width(), height=60, image=grass_img, text='')
            bottom_navbar.place(relx=0.5, rely=1, anchor='s')


            



            # self.office_img= ctk.CTkImage(light_image=Image.open('../data/office_img.png'), dark_image=Image.open('../data/office_img.png'), size=(200,200))
            # OfficeImageLBL = ctk.CTkLabel(self.first_window_root, width=self.first_window_root.winfo_width(), height=self.first_window_root.winfo_height(), image=self.office_img, text='')
            # OfficeImageLBL.place(relx=0.1, rely=0.18, anchor=ctk.CENTER)

            dummy_frame = ctk.CTkFrame(self.first_window_root, width=400, fg_color=BG_COLOR, corner_radius=30)
            dummy_frame.place(relx=0.5, rely=0.1, anchor=ctk.N)

            # The titel label
            self.Big_Label = ctk.CTkLabel(dummy_frame, text="تنظيم و أفراد مكتب السيد/ مدير الجهاز", font=(font_text, 70, 'bold'), text_color=BUTTON_COLOR)
            self.Big_Label.grid(row=1, columnspan=8,pady=70, padx=20)

            #Tammam printing Button
            self.Tammam_Button = ctk.CTkButton(dummy_frame, text='طباعة تمام اليوم', command=self.Print_Tamam, font=(font_text, 25, 'bold'), fg_color=BUTTON_COLOR, width=200, corner_radius=30)
            self.Tammam_Button.grid(row=2, column=4, pady=30)


            #Movement printing button
            self.Movement_print_Button = ctk.CTkButton(dummy_frame, text='طباعة يومية تحركات', command=self.Print_Movements, font=(font_text, 25, 'bold'), fg_color=BUTTON_COLOR, width=200, corner_radius=30)
            self.Movement_print_Button.grid(row=2, column=3, pady=30)

            #Vacations pass printing button
            self.Vacations_print_Button = ctk.CTkButton(dummy_frame, text='طباعة تصاريح الأجازات', command=self.Print_Vac_Passes, font=(font_text, 25, 'bold'), fg_color=BUTTON_COLOR, width=200, corner_radius=30)
            self.Vacations_print_Button.grid(row=3, column=4, pady=30)


    
            #Vacations Entry Button
            self.Vacations_Entry_Button = ctk.CTkButton(dummy_frame, text='تسجيل أجازات', command=self.render_Vacations_Page, font=(font_text, 25, 'bold'), fg_color=BUTTON_COLOR, width=200, corner_radius=30)
            self.Vacations_Entry_Button.grid(row=3, column=3, pady=30)
            


            #Vacations pass printing button
            self.Entry_Button = ctk.CTkButton(dummy_frame, text='إدخال/ تعديل البيانات', command=self.render_Entry_Page, font=(font_text, 25, 'bold'), fg_color=BUTTON_COLOR, width=200, corner_radius=30)
            self.Entry_Button.grid(row=5, column =4, columnspan=1, pady=30)


            #Vacations History printing button
            self.Vac_History_Button = ctk.CTkButton(dummy_frame, text='تاريخ الأجازات', command=self.Print_Vacations_History, font=(font_text, 25, 'bold'), fg_color=BUTTON_COLOR, width=200, corner_radius=30)
            self.Vac_History_Button.grid(row=5, column =3, columnspan=1, pady=30)


            # #All Documents Show Button
            self.AllDocs_Show_Button = ctk.CTkButton(dummy_frame, text="إظهار كل وثائق التعارف", command=self.ShowAllDocuments, font=(font_text, 25, 'bold'), fg_color=BUTTON_COLOR, width=200, corner_radius=30)
            self.AllDocs_Show_Button.grid(row=4, column=3, pady=30)


            #Document Entry Button
            self.Doc_Entry_Button = ctk.CTkButton(dummy_frame, text='إدخال وثيقة تعارف جديدة', command=self.EnterNewDocument, font=(font_text, 25, 'bold'), fg_color=BUTTON_COLOR, width=200, corner_radius=30)
            self.Doc_Entry_Button.grid(row=4, column=4, pady=30)


            # self.Change_Font_Button = ctk.CTkButton(self.first_window_root, text='تغيير الفونت', command=self.ChangeAllFonts, font=(font_text, 25, 'bold'), fg_color=BUTTON_COLOR, width=200, corner_radius=30)
            # self.Change_Font_Button.place(relx=0.8, rely=0.8)


            self.Settings_Button = ctk.CTkButton(self.first_window_root, text='إعدادات', command=self.render_Settings_Page, font=(font_text, 25, 'bold'), fg_color=BUTTON_COLOR, width=200, corner_radius=30)
            self.Settings_Button.place(relx=0.8, rely=0.8)

            

            self.Update_Button = ctk.CTkButton(self.first_window_root, text=update_text, command=self.ConfirmPage, font=(font_text, 25, 'bold'), fg_color=update_color, width=200, corner_radius=30, text_color=update_text_color)
            if(is_update_available):
                self.Update_Button.place(relx=0.8, rely=0.7)






            if(not os.path.isfile(helpers.DB_PATH)):
                self.render_First_Page()







            # self.first_window_root.bind("<Configure>", lambda x: self.resizeAll())
            
            self.first_window_root.bind('<Control-q>', lambda x: self.quit())

            self.first_window_root.after(1, self.MakeWindowAtTheFront)
            


            self.first_window_root.after(20000, self.RefreshVacations)
            self.first_window_root.after(1, self.CheckRunningThreadsForLoadingWindow)




            if(self.is_admin != '1'):
                # self.Vacations_Entry_Button.grid_forget()
                self.Doc_Entry_Button.grid_forget()
                self.AllDocs_Show_Button.grid_forget()
                self.Entry_Button.grid_forget()
                self.Vac_History_Button.grid_forget()



            
            

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
            
            
    
        if(helper(self.vp) or helper(self.ep) or helper(self.fp) or helper(self.dep) or helper(self.ld) or helper(self.sp)):
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