import customtkinter as ctk
import math
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

        screen_width, screen_height = self.first_window_root.winfo_screenwidth(), self.first_window_root.winfo_screenheight()
        width, height = 1200, 600
        self.first_window_root.geometry(f"{width}x{height}+{str(math.floor(screen_width/2 - width/2))}+{str(math.floor(screen_height/2 - height/2))}")  # Set window size


        self.bg_img= ctk.CTkImage(light_image=Image.open('../data/BG_logo.png'), dark_image=Image.open('../data/BG_logo.png'), size=(400,400))
        ImageLBL = ctk.CTkLabel(self.first_window_root, width=self.first_window_root.winfo_width(), height=self.first_window_root.winfo_height(), image=self.bg_img, text='')
        ImageLBL.place(relx=0.92, rely=0.92, anchor=ctk.CENTER)

        # The titel label
        Big_Label = ctk.CTkLabel(self.first_window_root, text="Secretary Assistant", font=('cooper black gothic', 50, 'bold'), text_color=BUTTON_COLOR)
        Big_Label.place(relx = 0.5, rely = 0.2, anchor=ctk.CENTER)


        self.Errors_Lbl = ctk.CTkLabel(self.first_window_root, text= '', text_color=REMOVE_BUTTON_COLOR, fg_color=BG_COLOR, font=('Dubai', 16, 'bold'))
        self.Errors_Lbl.place(relx=0.5, rely=0.8, anchor='center')


        First_Time_question_Label = ctk.CTkLabel(self.first_window_root, text='إذا كانت هذه أول مرة لاستعمالك هذا البرنامج, فنرجو إختيار مكان قاعدة البيانات.' + 'و إعادة فتح البرنامج', font=('cooper black gothic', 30, 'bold'), text_color=BUTTON_COLOR, fg_color=BG_COLOR)
        First_Time_question_Label.place(relx=0.5, rely=0.4, anchor='center')

        Proceed_Button = ctk.CTkButton(self.first_window_root, text='إدخال', command=self.SetDBPath, fg_color=BUTTON_COLOR, font=('Arial', 30, 'bold'), width=150, corner_radius=30)
        Proceed_Button.place(relx=0.5, rely= 0.7, anchor='center')

        # self.first_window_root.bind("<Configure>", lambda x: self.resizeAll())


    def render(self):
        self.first_window_root.mainloop()


    def resizeAll(self):
        self.width = self.first_window_root.winfo_width()
        self.height = self.first_window_root.winfo_height()
        self.bg_img.configure(size=(self.width / 2, self.width / 2))



    def SetDBPath(self):
        db_path = ctk.filedialog.askopenfilename(defaultextension='db', filetypes=[('sqlite.db','*.db'),])
        if(os.path.isfile(db_path) and os.path.splitext(db_path)[1] == '.db'):
            with open('db_path.txt', 'w') as f:
                f.write(os.path.dirname(db_path))
            
            self.first_window_root.destroy()
        
        else:
            self.Errors_Lbl.configure(text='هذا الملف ليس قاعدة البيانات, إذا كنت لا تعرف كيف تستعمل هذا البرنامج, نرجو التواصل مع المهندس أيمن محمد')
            

    
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
