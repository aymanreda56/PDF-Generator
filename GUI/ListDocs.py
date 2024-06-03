import customtkinter as ctk
import re, math
from datetime import date
import os
# import GenHelpers
import helpers
from PIL import ImageTk, Image
from style import *
from DocShow import DocShow
# from enc import enc


# from soldData import SoldierData

with open('db_path.txt', 'r') as f:
    DB_FOLDER = os.path.abspath(f.read())
    DB_PHOTOS = os.path.join(DB_FOLDER, 'Soldier_Photos')
    


font_style = 'Dubai'


    



class ListDocs():


        # result['Image_Path'] = result[0][0]
        # result['Name'] = result[0][1]
        # result['BirthDate'] = result[0][2]
        # result['Soldier_ID'] = result[0][3]
        # result['Mobile_Num'] = result[0][4]
        # result['Home_Address'] = result[0][5]
        # result['City'] = result[0][6]
        # result['Governorate'] = result[0][7]
        # result['Home_Number'] = result[0][8]
        # result['Retiring_Date'] = result[0][9]
        # result['Mothers_Mobile_Num'] = result[0][10]
        # result['Function_Inside_Dept'] = result[0][11]
        # result['Date_Of_Join'] = result[0][12]


    def showDoc(self, soldier_ID):
        soldier_data = helpers.retreive_Document(soldier_ID=soldier_ID)
        self.ds = DocShow(
            image_path= soldier_data['Image_Path'],
            name = soldier_data['Name'],
            birth_date= soldier_data['BirthDate'],
            soldier_id= soldier_data['Soldier_ID'],
            retiring_date= soldier_data['Retiring_Date'],
            mobile_number= soldier_data['Mobile_Num'],
            home_number= soldier_data['Home_Number'],
            home_address= soldier_data['Home_Address'],
            city= soldier_data['City'],
            governorate= soldier_data['Governorate'],
            mothers_mob_number= soldier_data['Mothers_Mobile_Num'],
            function_inside_department= soldier_data['Function_Inside_Dept'],
            date_of_join= soldier_data['Date_Of_Join']
        )

        self.ds.render(image_path= soldier_data['Image_Path'],
            name = soldier_data['Name'],
            birth_date= soldier_data['BirthDate'],
            soldier_id= soldier_data['Soldier_ID'],
            retiring_date= soldier_data['Retiring_Date'],
            mobile_number= soldier_data['Mobile_Num'],
            home_number= soldier_data['Home_Number'],
            home_address= soldier_data['Home_Address'],
            city= soldier_data['City'],
            governorate= soldier_data['Governorate'],
            mothers_mob_number= soldier_data['Mothers_Mobile_Num'],
            function_inside_department= soldier_data['Function_Inside_Dept'],
            date_of_join= soldier_data['Date_Of_Join']
        )




    def ShowSpecificSoldierDocument(self, event):
        print(event.widget)
        for (card, soldier_id) in self.cards_array:
            testwidget = event.widget
            if(testwidget.nametowidget(testwidget.winfo_parent())  == card):
                self.showDoc(soldier_ID=soldier_id)
            else:
                itsparent = testwidget.nametowidget(testwidget.winfo_parent())
                if(itsparent.nametowidget(itsparent.winfo_parent())  == card):
                    self.showDoc(soldier_ID=soldier_id)
                else:
                    itsgrandparent = itsparent.nametowidget(itsparent.winfo_parent())
                    if(itsgrandparent.nametowidget(itsgrandparent.winfo_parent())  == card):
                        self.showDoc(soldier_ID=soldier_id)
        


    def Personal_Card(self, first_name, rest_of_name, job_description, soldier_ID, date_of_termination:str, mobile_number, image_path, column_num):
        Card_Frame = ctk.CTkFrame(master=self.Frame_For_List, width=250, height=545, fg_color='#150F30', corner_radius=15, cursor='heart')
        Card_Frame.grid(column = column_num, row=0, padx = 7)


        img= ctk.CTkImage(light_image=Image.open(image_path), dark_image=Image.open(image_path), size=(225,225))
        ImageLBL = ctk.CTkLabel(Card_Frame, width=225, height=226, image=img, text='')
        ImageLBL.grid(row = 0, pady=12, padx=12)

        First_Name_Lbl = ctk.CTkLabel(Card_Frame, text=first_name, font=(font_style, 32, 'bold'), justify='right', text_color=WHITE_TEXT_COLOR)
        First_Name_Lbl.grid(row = 1, pady=0, padx = 12, sticky='e')

        Rest_Of_Name_Lbl = ctk.CTkLabel(Card_Frame, text=rest_of_name, font=(font_style, 20), justify='right', text_color=WHITE_TEXT_COLOR)
        Rest_Of_Name_Lbl.grid(row = 2, pady=0, padx = 12, sticky='e')

        Job_Description_Lbl = ctk.CTkLabel(Card_Frame, text='الوظيفة: ' + job_description , font=(font_style, 20), justify='right', text_color=WHITE_TEXT_COLOR)
        Job_Description_Lbl.grid(row = 3, pady=10, padx = 12, sticky='e')

        Soldier_ID_Lbl = ctk.CTkLabel(Card_Frame, text="الرقم العسكري: "+soldier_ID , font=(font_style, 20), justify='right', text_color=WHITE_TEXT_COLOR)
        Soldier_ID_Lbl.grid(row = 4, pady=10, padx = 12, sticky='e')


        Date_Of_Term_Lbl = ctk.CTkLabel(Card_Frame, text='تاريخ الرديف: ' + date_of_termination , font=(font_style, 20), justify='right', text_color=WHITE_TEXT_COLOR)
        Date_Of_Term_Lbl.grid(row = 5, pady=10, padx = 12, sticky='e')


        Mobile_Number_Lbl = ctk.CTkLabel(Card_Frame, text='موبايل: ' + mobile_number , font=(font_style, 20), justify='right', text_color=WHITE_TEXT_COLOR)
        Mobile_Number_Lbl.grid(row = 6, pady=10, padx = 12, sticky='e')



        Card_Frame.bind('<Button-1>', lambda x: self.ShowSpecificSoldierDocument(x))
        First_Name_Lbl.bind('<Button-1>', lambda x: self.ShowSpecificSoldierDocument(x))
        Rest_Of_Name_Lbl.bind('<Button-1>', lambda x: self.ShowSpecificSoldierDocument(x))
        ImageLBL.bind('<Button-1>', lambda x: self.ShowSpecificSoldierDocument(x))
        Soldier_ID_Lbl.bind('<Button-1>', lambda x: self.ShowSpecificSoldierDocument(x))
        Date_Of_Term_Lbl.bind('<Button-1>', lambda x: self.ShowSpecificSoldierDocument(x))
        Mobile_Number_Lbl.bind('<Button-1>', lambda x: self.ShowSpecificSoldierDocument(x))

        return Card_Frame



    def fillListDocs(self):
        # global SoldierData
        # SoldierData = SoldierData
        SoldierData = helpers.retreive_All_Documents()
        self.cards_array=[]
        for (i,entry) in enumerate(SoldierData):
            tokenized_name = re.split(' ', entry['Name'])
            first_name = tokenized_name[0]
            rest_of_name = ' '.join(tokenized_name[1:])
            job_description = entry['Function_Inside_Dept']
            soldier_ID = entry['Soldier_ID']
            date_of_termination = entry['Retiring_Date']
            mobile_number = entry['Mobile_Num']
            image_path = entry['Image_Path']

            self.cards_array.append((self.Personal_Card(first_name=first_name, rest_of_name=rest_of_name, job_description=job_description , soldier_ID=soldier_ID, date_of_termination=date_of_termination, mobile_number=mobile_number, image_path=image_path, column_num=i), soldier_ID))











    def __init__(self):
        self.root = ctk.CTkToplevel(fg_color=BG_COLOR)
        self.root.iconbitmap("../data/icolog.ico")
        screen_width, screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        width, height = 1360, 775
        self.root.geometry(f"{width}x{height}+{str(math.floor(screen_width/2 - width/2))}+{str(math.floor(screen_height/2 - height/2))}")  # Set window size
        
        self.root.title('عرض وثائق التعارف')
        
        self.ds = False
        self.main_was_active = True

    def renderListDocs(self):
        frame_for_scroll = ctk.CTkFrame(master=self.root, height=570 , width=1200, fg_color=FRAME_DARK_COLOR, border_width=7, border_color=BUTTON_COLOR, corner_radius=20)
        frame_for_scroll.pack(pady=20)
        self.Frame_For_List = ctk.CTkScrollableFrame(master=frame_for_scroll, orientation='horizontal', height=560 , width=1200, fg_color=FRAME_DARK_COLOR, scrollbar_button_color=SCROLL_COLOR, scrollbar_fg_color=BG_COLOR, scrollbar_button_hover_color=SCROLL_HOVER_COLOR)
        self.Frame_For_List.pack(padx=10, pady=20)


        # self.Personal_Card(first_name='أيمن', rest_of_name='محمد رضا عبده', job_description='فريق البحث و التطوير', soldier_ID='12453185132', date_of_termination= date.today().isoformat(), mobile_number='01225838009', image_path='../db/Soldier_Photos/ayman.png')
        self.fillListDocs()

        self.return_button = ctk.CTkButton(master=self.root, width=200, corner_radius=15, fg_color=BUTTON_COLOR, text='العودة للقائمة', font=(font_style, 20, 'bold'), text_color=FG_COLOR, command=self.quit)
        self.return_button.place(relx=0.2, rely=0.9, anchor=ctk.CENTER)
        # self.Frame_For_Buttons = ctk.CTkFrame(self.root)
        # self.Frame_For_Buttons.pack()
        

        self.root.after(1, self.MakeWindowAtTheFront)

        self.root.bind('<Control-q>', lambda x: self.quit())


        self.root.mainloop()



    def MakeWindowAtTheFront(self):
        main_is_active = True
        def helper(wind):
            try:
                    if(not wind.root.children):
                        return False
                    if(self.root.focus_get() == self.root):
                        wind.root.focus_set()
                        self.root.iconify()
                        self.main_was_active = False
                    return True
            except:
                return False
            
            
    
        if(helper(self.ds)):
            main_is_active = False
        else:
            main_is_active = True
            
        if(main_is_active and not self.main_was_active):
            self.root.deiconify()
            self.main_was_active = True
            
        self.root.after(1, self.MakeWindowAtTheFront)




    def quit(self):
        self.root.destroy()



# ld = ListDocs()
# ld.renderListDocs()