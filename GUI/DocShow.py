import customtkinter as ctk
import re, math
from datetime import date
# import os
import GenHelpers, helpers
# import helpers
from PIL import ImageTk, Image
from style import *
from soldData import SoldierData
from DocumentEntryPage import DocumentEntryPage
from SoldierModel import SoldierModel
# from enc import enc



font_style = 'Dubai'
font_size = 18


    




class DocShow():


    def ConfirmPage(self):
        self.ConfirmPageRoot = ctk.CTk(fg_color='#3C415E')
        screen_width, screen_height = self.ConfirmPageRoot.winfo_screenwidth(), self.ConfirmPageRoot.winfo_screenheight()


        width, height = 600, 150
        self.ConfirmPageRoot.geometry(f"{width}x{height}+{str(math.floor(screen_width/2 - width/2))}+{str(math.floor(screen_height/2 - height/2))}")  # Set window size
        self.ConfirmPageRoot.iconbitmap("../data/icolog.ico")
        self.ConfirmPageRoot.title(f'مسح وثيقة تعارف {self.name}')

        confirmlbl = ctk.CTkLabel(master=self.ConfirmPageRoot, text='هل أنت متأكد من مسح وثيقة التعارف؟', font=(font_style, 30, 'bold'))
        confirmlbl.pack(pady=10)
        
        confirmbutton = ctk.CTkButton(master=self.ConfirmPageRoot, text= 'تأكيد', fg_color=REMOVE_BUTTON_COLOR, font=(font_style, 30, 'bold'), corner_radius=15, command=self.ConfirmDeletion)
        confirmbutton.pack(pady=10)

        self.ConfirmPageRoot.bind('<Control-q>', lambda x: self.ConfirmPageRoot.destroy())

        self.ConfirmPageRoot.mainloop()

    
    def ConfirmDeletion(self):
        helpers.delete_Document(soldier_ID=self.soldier_id)
        self.ConfirmPageRoot.destroy()
        self.root.destroy()




    def addFields(self, image_path, name, birth_date, soldier_id, retiring_date, mobile_number, home_number, home_address=None, city=None, governorate=None, mothers_mob_number=None, function_inside_department=None, date_of_join=None):
        i = 0

        img= ctk.CTkImage(light_image=Image.open(image_path), dark_image=Image.open(image_path), size=(225,225))
        ImageLBL = ctk.CTkLabel(self.frame_for_grid, width=225, height=226, image=img, text='')
        ImageLBL.grid(column = 1, row = i, pady=12, padx=20, sticky='e')
        i += 1
        
        nameLbl = ctk.CTkLabel(master=self.frame_for_grid, text='الإسم: '+name, text_color=TEXT_COLOR, fg_color=FRAME_DARK_COLOR, font=(font_style, font_size, 'bold'))
        nameLbl.grid(column = 1, row=i, pady=12, padx=20, sticky='e')
        i += 1

        birth_dateLbl = ctk.CTkLabel(master=self.frame_for_grid, text='تاريخ الميلاد: '+GenHelpers.translate_all_numbers_to_arabic(birth_date), text_color=TEXT_COLOR, fg_color=FRAME_DARK_COLOR, font=(font_style, font_size, 'bold'))
        birth_dateLbl.grid(column = 1, row=i, pady=12, padx=20, sticky='e')
        i += 1


        soldier_id_Lbl = ctk.CTkLabel(master=self.frame_for_grid, text='الرقم العسكري:  '+GenHelpers.translate_all_numbers_to_arabic(soldier_id), text_color=TEXT_COLOR, fg_color=FRAME_DARK_COLOR, font=(font_style, font_size, 'bold'))
        soldier_id_Lbl.grid(column = 1, row=i, pady=12, padx=20, sticky='e')
        i += 1


        retiring_dateLbl = ctk.CTkLabel(master=self.frame_for_grid, text='تاريخ الرديف:  '+GenHelpers.translate_all_numbers_to_arabic(retiring_date), text_color=TEXT_COLOR, fg_color=FRAME_DARK_COLOR, font=(font_style, font_size, 'bold'))
        retiring_dateLbl.grid(column = 1, row=i, pady=12, padx=20, sticky='e')
        i += 1

        mobile_numberLbl = ctk.CTkLabel(master=self.frame_for_grid, text='رقم الموبايل:  '+GenHelpers.translate_all_numbers_to_arabic(mobile_number), text_color=TEXT_COLOR, fg_color=FRAME_DARK_COLOR, font=(font_style, font_size, 'bold'))
        mobile_numberLbl.grid(column = 1, row=i, pady=12, padx=20, sticky='e')
        i += 1


        home_numberLbl = ctk.CTkLabel(master=self.frame_for_grid, text='رقم المنزل:  '+GenHelpers.translate_all_numbers_to_arabic(home_number), text_color=TEXT_COLOR, fg_color=FRAME_DARK_COLOR, font=(font_style, font_size, 'bold'))
        home_numberLbl.grid(column = 1, row=i, pady=12, padx=20, sticky='e')
        i += 1


        home_addressLbl = ctk.CTkLabel(master=self.frame_for_grid, text='عنوان المنزل:  '+GenHelpers.translate_all_numbers_to_arabic(home_address), text_color=TEXT_COLOR, fg_color=FRAME_DARK_COLOR, font=(font_style, font_size, 'bold'))
        home_addressLbl.grid(column = 1, row=i, pady=12, padx=20, sticky='e')
        i += 1

        cityLbl = ctk.CTkLabel(master=self.frame_for_grid, text='المدينة:  '+city, text_color=TEXT_COLOR, fg_color=FRAME_DARK_COLOR, font=(font_style, font_size, 'bold'))
        cityLbl.grid(column = 1, row=i, pady=12, padx=20, sticky='e')
        i += 1

        governorateLbl = ctk.CTkLabel(master=self.frame_for_grid, text='المحافظة:  '+governorate, text_color=TEXT_COLOR, fg_color=FRAME_DARK_COLOR, font=(font_style, font_size, 'bold'))
        governorateLbl.grid(column = 1, row=i, pady=12, padx=20, sticky='e')
        i += 1


        mothers_mob_number = ctk.CTkLabel(master=self.frame_for_grid, text='رقم هاتف ولي الأمر:  '+GenHelpers.translate_all_numbers_to_arabic(mothers_mob_number), text_color=TEXT_COLOR, fg_color=FRAME_DARK_COLOR, font=(font_style, font_size, 'bold'))
        mothers_mob_number.grid(column = 1, row=i, pady=12, padx=20, sticky='e')
        i += 1



        i = 1

        function_inside_departmentLbl = ctk.CTkLabel(master=self.frame_for_grid, text="الوظيفة داخل الإدارة:  "+function_inside_department, text_color=TEXT_COLOR, fg_color=FRAME_DARK_COLOR, font=(font_style, font_size, 'bold'))
        function_inside_departmentLbl.grid(column = 0, row=i, pady=12, padx=30, sticky='e')
        i += 1

        date_of_joinLbl = ctk.CTkLabel(master=self.frame_for_grid, text='تاريخ الإنضمام للإدارة:  '+date_of_join, text_color=TEXT_COLOR, fg_color=FRAME_DARK_COLOR, font=(font_style, font_size, 'bold'))
        date_of_joinLbl.grid(column = 0, row=i, pady=12, padx=30, sticky='e')
        i += 1






    def __init__(self, image_path, name, birth_date, soldier_id, retiring_date, mobile_number, home_number, home_address, city=None, governorate=None, mothers_mob_number=None, function_inside_department=None, date_of_join=None):
        
        self.image_path = image_path
        self.soldier_id = soldier_id
        self.name = name
        self.birth_date = birth_date
        self.retiring_date = retiring_date
        self.mobile_number = mobile_number
        self.home_number = home_number
        self.home_address = home_address
        self.city = city
        self.governorate = governorate
        self.mothers_mob_number = mothers_mob_number
        self.function_inside_department = function_inside_department
        self.date_of_join = date_of_join


        
        self.root = ctk.CTkToplevel(fg_color=BG_COLOR)


        
        screen_width, screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()


        width, height = 1000, 900
        self.root.geometry(f"{width}x{height}+{str(math.floor(screen_width/2 - width/2))}+{str(math.floor(screen_height/2 - height/2))}")  # Set window size
        self.root.iconbitmap("../data/icolog.ico")
        self.root.title(f'عرض وثيقة تعارف {name}')
    
    def render(self, image_path, name, birth_date, soldier_id, retiring_date, mobile_number, home_number, home_address, city=None, governorate=None, mothers_mob_number=None, function_inside_department=None, date_of_join=None):

        self.frame_for_grid = ctk.CTkFrame(master=self.root, width=2000 , height=1000, fg_color=FRAME_DARK_COLOR, border_width=7, border_color=BUTTON_COLOR, corner_radius=20)
        self.frame_for_grid.pack(expand=True)
        self.frame_for_grid.pack_propagate(False)
    

        # self.Personal_Card(first_name='أيمن', rest_of_name='محمد رضا عبده', job_description='فريق البحث و التطوير', soldier_ID='12453185132', date_of_termination= date.today().isoformat(), mobile_number='01225838009', image_path='../db/Soldier_Photos/ayman.png')
        self.addFields(image_path=image_path, name=name, birth_date=birth_date, soldier_id=soldier_id, retiring_date=retiring_date, mobile_number=mobile_number, home_number=home_number, home_address=home_address, city=city, governorate=governorate, mothers_mob_number=mothers_mob_number, function_inside_department=function_inside_department, date_of_join=date_of_join)

        self.return_button = ctk.CTkButton(master=self.frame_for_grid, width=200, corner_radius=15, fg_color=BUTTON_COLOR, text='العودة للقائمة', font=(font_style, 20, 'bold'), text_color=FG_COLOR, command=self.quit)
        self.return_button.place(relx=0.2, rely=0.9, anchor=ctk.CENTER)

        self.DeleteButton = ctk.CTkButton(master=self.frame_for_grid, width=150, corner_radius=15, fg_color=REMOVE_BUTTON_COLOR, text='مسح الوثيقة', font=(font_style, 20, 'bold'), text_color=FG_COLOR, command=self.ConfirmPage)
        self.DeleteButton.place(relx=0.18, rely=0.84, anchor=ctk.CENTER)

        self.EditButton = ctk.CTkButton(master=self.frame_for_grid, width=150, corner_radius=15, fg_color=ACCEPT_COLOR, text='تعديل الوثيقة', font=(font_style, 20, 'bold'), text_color=FG_COLOR, command=self.edit_document)
        self.EditButton.place(relx=0.18, rely=0.78, anchor=ctk.CENTER)
        # self.Frame_For_Buttons = ctk.CTkFrame(self.root)
        # self.Frame_For_Buttons.pack()



        self.root.bind('<Control-q>', lambda x: self.quit())

        self.root.mainloop()



    
    def edit_document(self):
        self.root.destroy()

        SoldModel = SoldierModel(image_path= self.image_path,
            name = self.name,
            birth_date= self.birth_date,
            soldier_id= self.soldier_id,
            retiring_date= self.retiring_date,
            mobile_number= self.mobile_number,
            home_number= self.home_number,
            home_address= self.home_address,
            city= self.city,
            governorate= self.governorate,
            mothers_mob_number= self.mothers_mob_number,
            function_inside_department= self.function_inside_department,
            date_of_join= self.date_of_join)
        
        dep = DocumentEntryPage(edit_mode=True, Sold_Model=SoldModel)


        dep.renderDocumentsEntryPage()

        
        

        # self.ds = DocShow(
        #     image_path= self.image_path,
        #     name = self.name,
        #     birth_date= self.birth_date,
        #     soldier_id= self.soldier_id,
        #     retiring_date= self.retiring_date,
        #     mobile_number= self.mobile_number,
        #     home_number= self.home_number,
        #     home_address= self.home_address,
        #     city= self.city,
        #     governorate= self.governorate,
        #     mothers_mob_number= self.mothers_mob_number,
        #     function_inside_department= self.function_inside_department,
        #     date_of_join= self.date_of_join
        # )

        # self.ds.render(
        #     image_path= self.image_path,
        #     name = self.name,
        #     birth_date= self.birth_date,
        #     soldier_id= self.soldier_id,
        #     retiring_date= self.retiring_date,
        #     mobile_number= self.mobile_number,
        #     home_number= self.home_number,
        #     home_address= self.home_address,
        #     city= self.city,
        #     governorate= self.governorate,
        #     mothers_mob_number= self.mothers_mob_number,
        #     function_inside_department= self.function_inside_department,
        #     date_of_join= self.date_of_join
        # )




    def quit(self):
        self.root.destroy()






        # 'Name': 
        # 'Function': 'فريق البحث و التطوير',\
        # 'Soldier_ID': '012153133',\
        # 'Mobile_Num': '01225838009',\
        # 'Retiring_Date': '01-03-2025',\
        # 'Picture_Path': r'D:\PDF_Generator\db\Soldier_Photos\ayman.png',\






# ds = DocShow(image_path=r'D:\PDF_Generator\db\Soldier_Photos\ayman.png',\
#         name='أيمن محمد رضا',\
#         birth_date='11-11-2000',
#         soldier_id='1231241231',
#         retiring_date='1-3-2025',
#         mobile_number='01225838009',
#         home_number='28080080',
#         home_address='20ش مصطفى فهمي على شارع خسرو, حلوان, القاهرة',
#         city='حلوان', 
#         governorate='القاهرة',
#         mothers_mob_number='01225838009',
#         function_inside_department='فريق البحث و التطوير',
#         date_of_join='28-3-2025'
#         )

# ds.render(image_path=r'D:\PDF_Generator\db\Soldier_Photos\ayman.png',\
#         name='أيمن محمد رضا',\
#         birth_date='11-11-2000',
#         soldier_id='1231241231',
#         retiring_date='1-3-2025',
#         mobile_number='01225838009',
#         home_number='28080080',
#         home_address='20ش مصطفى فهمي على شارع خسرو, حلوان, القاهرة',
#         city='حلوان', 
#         governorate='القاهرة',
#         mothers_mob_number='01225838009',
#         function_inside_department='فريق البحث و التطوير',
#         date_of_join='28-3-2025'
#         )
