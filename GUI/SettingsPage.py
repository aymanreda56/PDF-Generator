import customtkinter as ctk
import math
import os
import re
from PIL import ImageTk, Image
from style import *
from enc import enc



class SettingsPage():
    # def Validate(self, username_box, password_box):
    #     username = username_box.get()
    #     password = password_box.get()
    #     if(not username):
    #         self.displayError('برجاء إدخال اسم المستخدم')
    #         return False, False
    #     if(not password):
    #         self.displayError('برجاء إدخال كلمة السر')
    #         return False, False
    #     return username, password
    


    # def autoJustify(self, isusername):
    #     if(isusername):
    #         entrybox = self.username_Entry
    #     else:
    #         entrybox = self.password_Entry
    #     text = entrybox.get()
    #     if(text):
    #         if(ord(text[0]) in range(65, 90) or ord(text[0]) in range(97, 122) or ord(text[0]) in range(48, 57)):
    #             entrybox.configure(justify='left')
    #         else:
    #             entrybox.configure(justify='right')


    # def Login(self, username_box, password_box):
    #     username, password = self.Validate(username_box=username_box, password_box=password_box)
    #     if(username and password):
    #         self.Error_Label.configure(text='')
    #         login_result = enc.CheckUser(username, password)
    #         if(login_result):
    #             self.logged_in_flag = True
    #             self.level = login_result['level']
    #             self.name = login_result['name']
    #             self.is_admin = login_result['is_admin']
    #             self.root.destroy()
    #             return login_result
    #         else:
    #             self.displayError('المستخدم ليس موجود')


    # def resizeAll(self):
    #     width = self.root.winfo_width()
    #     height = self.root.winfo_height()
    #     self.bg_img.configure(size=(width / 2, width / 2))

        # self.big_Entire_Frame.configure(height=self.self.root.winfo_height()/3)

    def displayError(self, error_mes:str):
        self.Error_Label.configure(text = error_mes)
    

    def ChangeOutputFolder(self):
        new_output_folder_path = ctk.filedialog.askdirectory()
        if(not new_output_folder_path): return
        if(os.path.isdir(new_output_folder_path)):
            with open('config.txt', 'r') as f:
                config_text = f.readlines()
            config_text[1] = os.path.abspath(new_output_folder_path) + '\n'
            with open('config.txt', 'w') as f:
                f.writelines(config_text)

            self.displayError('تمت العملية بنجاح, يجب إعادة فتح البرنامج لثبات التأثير')
            self.Prepopulate()
            self.output_folder_lbl.configure(text=self.output_folder)
        else:
            self.displayError('الفولدر ليس موجود, او نوعه ليس فولدر')


    def ChangeTheme(self):
        
        with open('config.txt', 'r') as f:
            config_text = f.readlines()

        Theme_Code = int(re.sub('[\n\s]', '', config_text[0]))
        Theme_Code = 0 if Theme_Code else 1

        config_text[0] = str(Theme_Code) + '\n'

        with open('config.txt', 'w') as f:
            f.writelines(config_text)
        
        self.displayError('تمت العملية بنجاح, يجب إعادة فتح البرنامج لثبات التأثير')

        self.Prepopulate()
        self.theme_name_lbl.configure(text=self.theme_name)
    

    def ChangeDBFolder(self):
        new_output_folder_path = ctk.filedialog.askopenfilename(defaultextension='db')
        if(not new_output_folder_path): return
        if(os.path.isfile(new_output_folder_path) and os.path.splitext(new_output_folder_path)[1] == '.db'):
            with open('db_path.txt', 'w') as f:
                f.write(os.path.dirname(new_output_folder_path))

            self.displayError('تمت العملية بنجاح, يجب إعادة فتح البرنامج لثبات التأثير')
            self.Prepopulate()
            self.db_path_lbl.configure(text=self.db_path)

        else:
            self.displayError('الفولدر ليس موجود, او نوعه ليس فولدر')



    def Prepopulate(self):
        with open ('config.txt', 'r') as f:
            config_text = f.readlines()

        self.output_folder = re.sub('[\n\s]', '', config_text[1])
        self.theme_name = 'ورق مشجر' if int(re.sub('[\n\s]', '', config_text[0])) else 'كلاسيكي'

        with open ('db_path.txt', 'r') as f:
            db_patth = f.read()
        self.db_path = db_patth


    def __init__(self):
        
        self.root = ctk.CTkToplevel(fg_color=BG_COLOR)
        self.root.title("تنظيم وأفراد مكتب السيد/ مدير الجهاز")

        self.Prepopulate()


        screen_width, screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        width, height = 1500, 800
        self.root.geometry(f"{width}x{height}+{str(math.floor(screen_width/2 - width/2))}+{str(math.floor(screen_height/2 - height/2))}")  # Set window size


        self.root.iconbitmap("../data/icolog.ico")


        img= ctk.CTkImage(light_image=Image.open(PROJ_LOGO), dark_image=Image.open(PROJ_LOGO), size=(250,312.5 if CHOSEN_PRESET else 250))
        ImageLBL = ctk.CTkLabel(self.root, width=self.root.winfo_width(), height=self.root.winfo_height(), image=img, text='')
        ImageLBL.place(relx=0.88, rely=0.2, anchor=ctk.CENTER)

        self.bg_img= ctk.CTkImage(light_image=Image.open(BG_LOGO), dark_image=Image.open(BG_LOGO), size=(700,700))
        self.bg_img_lbl = ctk.CTkLabel(self.root, width=self.root.winfo_width(), height=self.root.winfo_height(), image=self.bg_img, text='')
        self.bg_img_lbl.place(relx=0, rely=0.52, anchor=ctk.CENTER)


        wheatimg= ctk.CTkImage(light_image=Image.open(WHEAT_LEAVES), dark_image=Image.open(WHEAT_LEAVES), size=(630,200))
        botNavbar = ctk.CTkLabel(self.root, width=self.root.winfo_width(), height=self.root.winfo_height(), image=wheatimg, text='')
        botNavbar.place(relx=0.5, rely=1, anchor='s')



        # The titel label
        Big_Label = ctk.CTkLabel(self.root, text="تنظيم وأفراد مكتب السيد/ مدير الجهاز", font=('Arial', 50, 'bold'), text_color=BUTTON_COLOR)
        Big_Label.pack()



        self.BigFrame = ctk.CTkFrame(self.root, width=400, fg_color=BG_COLOR, corner_radius=30)
        self.BigFrame.pack(pady=100)



        self.Change_Output_Folder_Button = ctk.CTkButton(self.BigFrame, text='تغيير مكان الصحف المنتجة', font=('Dubai', 30, 'bold'), width=100, command=self.ChangeOutputFolder)
        self.Change_Output_Folder_Button.grid(row = 0, column=1)

        self.output_folder_lbl = ctk.CTkLabel(self.BigFrame, text=self.output_folder, font=('Dubai', 30, 'bold'), width=100, text_color=TEXT_COLOR)
        self.output_folder_lbl.grid(row = 0, column = 0)


        self.Change_Theme_Button = ctk.CTkButton(self.BigFrame, text='تغيير ألوان البرنامج', font=('Dubai', 30, 'bold'), width=100, command=self.ChangeTheme)
        self.Change_Theme_Button.grid(row = 1, column=1)

        self.theme_name_lbl = ctk.CTkLabel(self.BigFrame, text=self.theme_name, font=('Dubai', 30, 'bold'), width=100, text_color=TEXT_COLOR)
        self.theme_name_lbl.grid(row = 1, column = 0)


        self.Change_DB_Path_Button = ctk.CTkButton(self.BigFrame, text='تغيير مكان قاعدة البيانات', font=('Dubai', 30, 'bold'), width=100, command=self.ChangeDBFolder)
        self.Change_DB_Path_Button.grid(row = 2, column=1)


        self.db_path_lbl = ctk.CTkLabel(self.BigFrame, text=self.db_path, font=('Dubai', 30, 'bold'), width=100, text_color=TEXT_COLOR)
        self.db_path_lbl.grid(row = 2, column = 0)


        # self.username_Entry = ctk.CTkEntry(self.root, placeholder_text='اسم المستخدم', font=('Dubai', 30, 'bold'), justify='right', width=300)
        # self.username_Entry.place(relx = 0.5, rely=0.35, anchor=ctk.CENTER)
        # self.username_Entry.bind("<Key>", lambda x:self.autoJustify(1))

        # self.password_Entry = ctk.CTkEntry(self.root, placeholder_text='كلمة السر', font=('Dubai', 30, 'bold'), justify='right', width=300)
        # self.password_Entry.place(relx = 0.5, rely=0.45, anchor=ctk.CENTER)
        # self.password_Entry.bind("<Key>", lambda x:self.autoJustify(0))


        self.Error_Label = ctk.CTkLabel(self.root, font=('Arial', 30, 'bold'), justify='right', fg_color=FG_COLOR, text_color=REMOVE_BUTTON_COLOR, text='')
        self.Error_Label.place(relx= 0.5, rely=0.8, anchor=ctk.CENTER)

        # sumbit_Button =ctk.CTkButton(self.root, text='إدخال', font=('Dubai', 30, 'bold'), width=100, command=lambda: self.Login(username_box=self.username_Entry, password_box=self.password_Entry))
        # sumbit_Button.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

        # self.root.bind("<Configure>", lambda x: self.resizeAll())

        self.root.bind('<Control-q>', lambda: self.root.quit)
        self.root.bind('<Control-e>', lambda x: self.Login(username_box=self.username_Entry, password_box=self.password_Entry))



    def renderSettingsPage(self):

        self.root.mainloop()


