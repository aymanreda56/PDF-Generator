import customtkinter as ctk
import math
import os, shutil
from PIL import ImageTk, Image
from style import *
import SoldierModel
from tkcalendar import Calendar
from datetime import date
import re
from time import sleep
import helpers
from enums import EntryError, SoldierModelErrorCode, EntryErrorCode
import cropper

with open('db_path.txt', 'r') as f:
    DB_FOLDER = os.path.abspath(f.read())
    DB_PATH = os.path.abspath(os.path.join(DB_FOLDER, 'Soldiers.db'))
    DB_PHOTOS = os.path.join(os.path.abspath(DB_FOLDER),'Soldier_Photos')




font_style = 'Dubai'
guide_font_size = 20




def validate_date(year, month, day):
    try:
        year = int(year)
        month = int(month)
        day = int(day)
    except:
        raise EntryError(EntryErrorCode.RETIRING_DATE_INTEGER_ERR)
   
    if(month not in range(1,13)):
        raise EntryError(EntryErrorCode.RETIRING_DATE_MONTH_ERR)
    if(day not in range(1,32)):
        raise EntryError(EntryErrorCode.RETIRING_DATE_DAY_ERR)
    try:
        date(year=year, month=month, day= day)
    except:
        raise EntryError(EntryErrorCode.RETIRING_DATE_GENERAL_ERR)


def validate_ID(ID_string, error_code):
    if ((not ID_string) or ID_string == '' or re.sub('\s+','', ID_string) == '' ):
        raise EntryError(error_code)

    for c in ID_string:
        if ord(c) not in range (48,58):
            raise EntryError(error_code)
        
    for c in ID_string:
        if c not in list('1234567890'):
            raise EntryError(error_code)

    return ID_string


def validate_name(text):
    if ((not text) or text == '' or re.sub('\s+','', text) == '' ):
        raise EntryError(EntryErrorCode.SOLDIER_NAME_MISSING)
    if(len(re.split(' ',text)) < 3):
        raise EntryError(EntryErrorCode.SOLDIER_NAME_TOO_SHORT_ERR)
    if(len(text) > 70):
        raise EntryError(EntryErrorCode.SOLDIER_NAME_TOO_LONG_ERR)
    ############################################################ TODO: this should correctly handle non-arabic characters##################
    for c in text:
        if c in list('abcdefghijklmnopqrstuvwxyz0123456789'):
            raise EntryError(EntryErrorCode.SOLDIER_NAME_NOT_ARABIC)
        ################################################################################################
    
    print(text)
    text = re.sub(r'\s+', ' ', text)
    return text






class DocumentEntryPage():



    
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


    def Submit(self, NameBox, BirthDate_Day_Box, BirthDate_Month_Box, BirthDate_Year_Box, Soldier_ID_Box, Mobile_Num_Box, City_Box,
               Home_Address_Box, Governorate_Box, Home_Num_Box, Retiring_Date_Day_Box, Retiring_Date_Month_Box, Retiring_Date_Year_Box, MothersMobileNum_Box,
               FunctionBox, Date_Of_Join_Box):
        

        try:
            if(self.image_path =='' or (not self.image_path)):
                raise EntryError(SoldierModelErrorCode.IMAGE_EMPTY)
        except EntryError as e:
            self.displayError(e)
            return
        

        try:
            Soldier_ID = validate_ID(Soldier_ID_Box.get(), error_code=EntryErrorCode.SOLDIER_ID_ERR)
        except EntryError as e:
            self.displayError(e)
            return
        
        
        try:
            Name = validate_name(NameBox.get())
        except EntryError as e:
            self.displayError(e)
            return
        

        bday = BirthDate_Day_Box.get()
        bmonth = BirthDate_Month_Box.get()
        byear = BirthDate_Year_Box.get()

        try:
            
            validate_date(byear, bmonth, bday)
            bdate = date(int(byear), int(bmonth), int(bday))
            bdate_string = bdate.isoformat()
        except EntryError as e:
            self.displayError(e)
            return
        

        
        try:
            Mobile_Number = validate_ID(Mobile_Num_Box.get(), error_code=SoldierModelErrorCode.MOBILE_NUMBER_EMPTY)
        except EntryError as e:
            self.displayError(e)
            return


        
        City = City_Box.get()
        if (City =='' or (not City)):
            self.displayError(SoldierModelErrorCode.CITY_EMPTY)
            return


        Home_Address = Home_Address_Box.get()
        if (Home_Address =='' or (not Home_Address)):
            self.displayError(SoldierModelErrorCode.HOME_ADDRESS_EMPTY)
            return

        Governorate = Governorate_Box.get()
        if (Governorate =='' or (not Governorate)):
            self.displayError(SoldierModelErrorCode.GOVERNORATE_EMPTY)
            return

        
        try:
            Home_Num = validate_ID(Home_Num_Box.get(), error_code=SoldierModelErrorCode.HOME_NUMBER_EMPTY)
        except EntryError as e:
            self.displayError(e)
            return

        rday = Retiring_Date_Day_Box.get()
        rmonth = Retiring_Date_Month_Box.get()
        ryear = Retiring_Date_Year_Box.get()

        try:
            validate_date(ryear, rmonth, rday)
            retiring_date = date(int(ryear), int(rmonth), int(rday))
            retiring_date_string = retiring_date.isoformat()
        except EntryError as e:
            self.displayError(e)
            return
        

        try:
            MothersMobileNum = validate_ID(MothersMobileNum_Box.get(), error_code=SoldierModelErrorCode.MOTHERS_MOBILE_NUMBER_EMPTY)
        except EntryError as e:
            self.displayError(e)
            return

        Function_dept = FunctionBox.get()
        if (Function_dept =='' or (not Function_dept)):
            self.displayError(SoldierModelErrorCode.FUNCTION_EMPTY)
            return


        Date_Of_Join = Date_Of_Join_Box.get()
        if (Date_Of_Join =='' or (not Date_Of_Join)):
            self.displayError(SoldierModelErrorCode.JOIN_DATE_EMPTY)
            return



        


        # image_file_name, image_file_path = os.path.split(Image_Path)
        fullpath, extension = os.path.splitext(self.image_path)
        dstImage = os.path.join(os.path.abspath(DB_PHOTOS), Soldier_ID+extension)
        
        if(self.image_path != dstImage):
            shutil.copy2(self.image_path, dstImage)

        if(self.edit_mode):
            helpers.Edit_Document(image_path=Soldier_ID+extension, name=Name, birth_date=bdate_string, soldier_id=Soldier_ID, retiring_date=retiring_date_string
                        , mobile_number=Mobile_Number, home_number=Home_Num, home_address=Home_Address, city=City, governorate=Governorate,
                        mothers_mob_number=MothersMobileNum, function_inside_department=Function_dept, date_of_join=Date_Of_Join)
        else:
            helpers.insert_Document(image_path=Soldier_ID+extension, name=Name, birth_date=bdate_string, soldier_id=Soldier_ID, retiring_date=retiring_date_string
                                , mobile_number=Mobile_Number, home_number=Home_Num, home_address=Home_Address, city=City, governorate=Governorate,
                                mothers_mob_number=MothersMobileNum, function_inside_department=Function_dept, date_of_join=Date_Of_Join)
        

        self.ErrorLabel.configure(text='')















    def showCalendar(self, type_of_date):

        if(type_of_date == 'retire'):
            master = self.RetiringDate_Frame
            day_entry = self.RetiringDate_Day_Entry
            month_entry = self.RetiringDate_Month_Entry
            year_entry = self.RetiringDate_Year_Entry
            calendarButton = self.retiringdcalendarshowbutton
        else:
            master = self.BirthDate_Frame
            day_entry = self.BirthDate_Day_Entry
            month_entry = self.BirthDate_Month_Entry
            year_entry = self.BirthDate_Year_Entry
            calendarButton = self.birthdcalendarshowbutton

        self.calenndar = Calendar(master, font=('Comic Sans MS', 12), borderwidth=10, background = CALENDAR_BG, foreground=CALENDAR_FG, 
                             bordercolor = '#F5F5F5', normalbackground='#FFFFFF', disabledbackground = '#F5F5F5', disabledforeground = '#F5F5F5', selectforeground = '#F5F5F5',
                             selectbackground = '#0047FF',
                             headerforeground='#749BC2',
                             cursor='heart', showweeknumbers = False
                             ,weekendbackground='#F5F5F5')
        
        day_entry.destroy()
        month_entry.destroy()
        year_entry.destroy()

        self.calenndar.grid(row=0, column=1, padx=10, pady=20)

        calendarButton.configure(text='اختيار', command= lambda: self.hideCalendar(type_of_date = type_of_date))


    def hideCalendar(self, type_of_date):

        if(type_of_date == 'retire'):
            master = self.RetiringDate_Frame
            day_entry = self.RetiringDate_Day_Entry
            month_entry = self.RetiringDate_Month_Entry
            year_entry = self.RetiringDate_Year_Entry
            calendarButton = self.retiringdcalendarshowbutton
        else:
            master = self.BirthDate_Frame
            day_entry = self.BirthDate_Day_Entry
            month_entry = self.BirthDate_Month_Entry
            year_entry = self.BirthDate_Year_Entry
            calendarButton = self.birthdcalendarshowbutton

        chosen_date = self.calenndar.get_date() #returned as 4/25/24 for 2024/March/25th
        month, day, year = re.split('/',chosen_date)
        year = "20"+year

        self.calenndar.destroy()

        day_entry = ctk.CTkEntry(master, font=(font_style, 15), width=100, placeholder_text='اليوم', justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR)
        day_entry.grid(row=0, column=3, padx=5)

        month_entry = ctk.CTkEntry(master, font=(font_style, 15), width=100, placeholder_text='الشهر', justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR)
        month_entry.grid(row=0, column=2, padx=5)

        year_entry = ctk.CTkEntry(master, font=(font_style, 15), width=100, placeholder_text='السنة', justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR)
        year_entry.grid(row=0, column=1, padx=5)

        day_entry.insert(0, day)
        month_entry.insert(0, month)
        year_entry.insert (0, year)

        calendarButton.configure(text='التقويم', command= lambda: self.showCalendar (type_of_date= type_of_date))

        if(type_of_date == 'retire'):
            self.RetiringDate_Frame = master
            self.RetiringDate_Day_Entry = day_entry
            self.RetiringDate_Month_Entry = month_entry
            self.RetiringDate_Year_Entry = year_entry
            self.retiringdcalendarshowbutton = calendarButton
        else:
            self.BirthDate_Frame = master
            self.BirthDate_Day_Entry = day_entry
            self.BirthDate_Month_Entry = month_entry
            self.BirthDate_Year_Entry = year_entry
            self.birthdcalendarshowbutton = calendarButton




    def deleteImage(self):
        self.ImageLBL.destroy()
        self.Delete_Image_Button.destroy()
        self.Image_Entry_Button = ctk.CTkButton(master=self.Image_Frame, text='إدخال صورة', fg_color=BUTTON_COLOR, font=(font_style, 16, 'bold'), command=self.addImage)
        self.Image_Entry_Button.place(relx=0.5, rely=0.9, anchor=ctk.CENTER)



    def addImage(self, image_path=''):
        try:
            if(not image_path):
                self.image_path = ctk.filedialog.askopenfilename(defaultextension='.png', filetypes=[('images, *.png'), ('images, *.jpg'), ('images, *.jpeg')])
                if(self.image_path):
                    
                    temp_img_path = os.path.join(DB_PHOTOS,'temp.png')
                    try:
                        ic = cropper.ImageCropper(image_path=self.image_path, output_path=temp_img_path)
                        self.root.wait_window(ic.root)
                    except Exception as e:
                        print(f'something occured here {e}')
                        raise(EntryError(SoldierModelErrorCode.IMAGE_NOT_PARSEABLE))
                    self.image_path = os.path.abspath(temp_img_path)
           
            self.img= ctk.CTkImage(light_image=Image.open(self.image_path), dark_image=Image.open(self.image_path), size=(225,225))
            try:
                self.ImageLBL = ctk.CTkLabel(self.Image_Frame, width=225, height=226, image=self.img, text='')
                self.ImageLBL.pack()
            except Exception as e:
                print(f'here is the error {e}')
        except:
            self.displayError(SoldierModelErrorCode.IMAGE_NOT_PARSEABLE)
            return

        self.Image_Entry_Button.destroy()
        self.Delete_Image_Button = ctk.CTkButton(master=self.ImageLBL, text='مسح', fg_color=REMOVE_BUTTON_COLOR, font=(font_style, 14, 'bold'), command=self.deleteImage, width=50)
        self.Delete_Image_Button.place(relx=0.5, rely=0.85, anchor=ctk.CENTER)


    def AddImagePlaceHolder(self, image_path = ''):
        self.Image_Frame = ctk.CTkFrame(master=self.big_scrollable_frame, width=225, height=225, fg_color=EMPTY_IMAGE_PLACEHOLDER, border_color=BUTTON_COLOR, border_width=5)
        self.Image_Frame.grid(pady=20, columnspan = 2, row=0, column=0, padx=20)

        self.Image_Entry_Button = ctk.CTkButton(master=self.Image_Frame, text='إدخال صورة', fg_color=BUTTON_COLOR, font=(font_style, 16, 'bold'), command=self.addImage)
        self.Image_Entry_Button.place(relx=0.5, rely=0.8, anchor=ctk.CENTER)

        if(image_path):
            self.addImage(image_path=image_path)






    def AddBirthDatePlaceHolder(self):


        self.BirthDate_Frame = ctk.CTkFrame(self.big_scrollable_frame, width=300, height=100, fg_color=FG_COLOR)
        self.BirthDate_Frame.grid(row=2, column=0, padx=20)

        self.BirthDate_Day_Entry = ctk.CTkEntry(self.BirthDate_Frame, font=(font_style, 15), width=100, placeholder_text='اليوم', justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR)
        self.BirthDate_Day_Entry.grid(row=0, column=3, padx=5)

        self.BirthDate_Month_Entry = ctk.CTkEntry(self.BirthDate_Frame, font=(font_style, 15), width=100, placeholder_text='الشهر', justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR)
        self.BirthDate_Month_Entry.grid(row=0, column=2, padx=5)

        self.BirthDate_Year_Entry = ctk.CTkEntry(self.BirthDate_Frame, font=(font_style, 15), width=100, placeholder_text='السنة', justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR)
        self.BirthDate_Year_Entry.grid(row=0, column=1, padx=5)


        self.birthdcalendarshowbutton = ctk.CTkButton(self.BirthDate_Frame, text='التقويم', font=(font_style, 15), width=30, command=lambda: self.showCalendar('birth'))
        self.birthdcalendarshowbutton.grid(row=0, column=0, sticky='n')


    def AddRetiringDatePlaceHolder(self):
        self.RetiringDate_Frame = ctk.CTkFrame(self.big_scrollable_frame, width=300, height=100, fg_color=FG_COLOR)
        self.RetiringDate_Frame.grid(row=4, column=0, padx=20)

        self.RetiringDate_Day_Entry = ctk.CTkEntry(self.RetiringDate_Frame, font=(font_style, 15), width=100, placeholder_text='اليوم', justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR)
        self.RetiringDate_Day_Entry.grid(row=0, column=3, padx=5)

        self.RetiringDate_Month_Entry = ctk.CTkEntry(self.RetiringDate_Frame, font=(font_style, 15), width=100, placeholder_text='الشهر', justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR)
        self.RetiringDate_Month_Entry.grid(row=0, column=2, padx=5)

        self.RetiringDate_Year_Entry = ctk.CTkEntry(self.RetiringDate_Frame, font=(font_style, 15), width=100, placeholder_text='السنة', justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR)
        self.RetiringDate_Year_Entry.grid(row=0, column=1, padx=5)

        self.retiringdcalendarshowbutton = ctk.CTkButton(self.RetiringDate_Frame, text='التقويم', font=(font_style, 15), width=30, command= lambda: self.showCalendar('retire'))
        self.retiringdcalendarshowbutton.grid(row=0, column=0, sticky='n')


    def displayError(self, ErrType):
        self.ErrorLabel.configure(text=ErrType)
        return



    def __init__(self, edit_mode = False, Sold_Model = None):

        self.Soldier_Model = Sold_Model
        if not Sold_Model:
            self.Soldier_Model = SoldierModel.SoldierModel()

        if(self.Soldier_Model):
            self.image_path = self.Soldier_Model.image_path
            self.soldier_id = self.Soldier_Model.soldier_id
            self.name = self.Soldier_Model.name
            self.birth_date = self.Soldier_Model.birth_date
            self.retiring_date = self.Soldier_Model.retiring_date
            self.mobile_number = self.Soldier_Model.mobile_number
            self.home_number = self.Soldier_Model.home_number
            self.home_address = self.Soldier_Model.home_address
            self.city = self.Soldier_Model.city
            self.governorate = self.Soldier_Model.governorate
            self.mothers_mob_number = self.Soldier_Model.mothers_mob_number
            self.function_inside_department = self.Soldier_Model.function_inside_department
            self.date_of_join = self.Soldier_Model.date_of_join


        self.edit_mode = edit_mode
        





        self.root = ctk.CTkToplevel(fg_color=BG_COLOR)
        
        screen_width, screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()

        width, height = 1360, 1000
        self.root.geometry(f"{width}x{height}+{str(math.floor(screen_width/2 - width/2))}+{str(math.floor(screen_height/2 - height/2)-20)}")  # Set window size
        self.root.iconbitmap("../data/icolog.ico")
        self.root.title('إدخال وثيقة تعارف')
        



    def renderDocumentsEntryPage(self):


        BigLabel = ctk.CTkLabel(master=self.root, text='إدخال وثيقة تعارف', font=(font_style, 50, 'bold'), text_color=TEXT_COLOR)
        BigLabel.pack(pady=30)

        self.big_scrollable_frame = ctk.CTkScrollableFrame(master=self.root, width=700, height=700, fg_color=FRAME_DARK_COLOR)
        self.big_scrollable_frame.pack()


        self.AddImagePlaceHolder()

        self.Name_Entry = ctk.CTkEntry(self.big_scrollable_frame, font=(font_style, 20), width=200, justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR, placeholder_text='الإسم رباعي باللغة العربية')
        self.Name_Entry.grid(row = 1, column = 0, pady=20, padx=20)
        name_lbl = ctk.CTkLabel (self.big_scrollable_frame, text='الإسم:  ', font=(font_style, guide_font_size, 'bold'), text_color=TEXT_COLOR)
        name_lbl.grid(row=1, column = 1, sticky= 'e', padx=20)
        


        name_lbl = ctk.CTkLabel (self.big_scrollable_frame, text='تاريخ الميلاد:  ', font=(font_style, guide_font_size, 'bold'), text_color=TEXT_COLOR)
        name_lbl.grid(row=2, column = 1, sticky= 'e', pady=20, padx=20)
        self.AddBirthDatePlaceHolder()


        name_lbl = ctk.CTkLabel (self.big_scrollable_frame, text='الرقم العسكري:  ', font=(font_style, guide_font_size, 'bold'), text_color=TEXT_COLOR)
        name_lbl.grid(row=3, column = 1, sticky= 'e', pady=20, padx=20)
        self.Soldier_ID_Entry = ctk.CTkEntry(self.big_scrollable_frame, font=(font_style, 20), width=200, justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR, placeholder_text='الرقم العسكري')
        self.Soldier_ID_Entry.grid(row = 3, column = 0, padx=20)


        name_lbl = ctk.CTkLabel (self.big_scrollable_frame, text='تاريخ الرديف:  ', font=(font_style, guide_font_size, 'bold'), text_color=TEXT_COLOR)
        name_lbl.grid(row=4, column = 1, sticky= 'e', pady=20, padx=20)
        self.AddRetiringDatePlaceHolder()


        name_lbl = ctk.CTkLabel (self.big_scrollable_frame, text='رقم الهاتف الشخصي:  ', font=(font_style, guide_font_size, 'bold'), text_color=TEXT_COLOR)
        name_lbl.grid(row=5, column = 1, sticky= 'e', pady=20, padx=20)
        self.MobileNumber_Entry = ctk.CTkEntry(self.big_scrollable_frame, font=(font_style, 20), width=200, justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR, placeholder_text='رقم الموبايل الشخصي')
        self.MobileNumber_Entry.grid(row=5, column=0, padx=20)



        name_lbl = ctk.CTkLabel (self.big_scrollable_frame, text='عنوان الإقامة', font=(font_style, guide_font_size, 'bold'), text_color=TEXT_COLOR)
        name_lbl.grid(row=6, column = 1, sticky= 'e', pady=20, padx=20)
        self.HomeAddress_Entry = ctk.CTkEntry(self.big_scrollable_frame, font=(font_style, 20), width=200, justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR, placeholder_text='عنوان الإقامة')
        self.HomeAddress_Entry.grid(row=6, column=0, padx=20)


        name_lbl = ctk.CTkLabel (self.big_scrollable_frame, text='المدينة', font=(font_style, guide_font_size, 'bold'), text_color=TEXT_COLOR)
        name_lbl.grid(row=7, column = 1, sticky= 'e', pady=20, padx=20)
        self.City_Entry = ctk.CTkEntry(self.big_scrollable_frame, font=(font_style, 20), width=200, justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR, placeholder_text='المدينة')
        self.City_Entry.grid(row=7, column=0, padx=20)



        name_lbl = ctk.CTkLabel (self.big_scrollable_frame, text='المحافظة', font=(font_style, guide_font_size, 'bold'), text_color=TEXT_COLOR)
        name_lbl.grid(row=8, column = 1, sticky= 'e', pady=20, padx=20)
        self.Governorate_Entry = ctk.CTkEntry(self.big_scrollable_frame, font=(font_style, 20), width=200, justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR, placeholder_text='المحافظة')
        self.Governorate_Entry.grid(row=8, column=0, padx=20)


        name_lbl = ctk.CTkLabel (self.big_scrollable_frame, text='رقم الهاتف المنزلي', font=(font_style, guide_font_size, 'bold'), text_color=TEXT_COLOR)
        name_lbl.grid(row=9, column = 1, sticky= 'e', pady=20, padx=20)
        self.HomeNumber_Entry = ctk.CTkEntry(self.big_scrollable_frame, font=(font_style, 20), width=200, justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR, placeholder_text='رقم الهاتف المنزلي')
        self.HomeNumber_Entry.grid(row=9, column=0, padx=20)


        name_lbl = ctk.CTkLabel (self.big_scrollable_frame, text='رقم الهاتف الشخصي لولي الأمر', font=(font_style, guide_font_size, 'bold'), text_color=TEXT_COLOR)
        name_lbl.grid(row=10, column = 1, sticky= 'e', pady=20, padx=20)
        self.MothersMobileNum_Entry = ctk.CTkEntry(self.big_scrollable_frame, font=(font_style, 20), width=200, justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR, placeholder_text='رقم الهاتف الشخصي لولي الأمر')
        self.MothersMobileNum_Entry.grid(row=10, column=0, padx=20)



        name_lbl = ctk.CTkLabel (self.big_scrollable_frame, text='الوظيفة داخل الإدارة', font=(font_style, guide_font_size, 'bold'), text_color=TEXT_COLOR)
        name_lbl.grid(row=11, column = 1, sticky= 'e', pady=20, padx=20)
        self.Function_Entry = ctk.CTkEntry(self.big_scrollable_frame, font=(font_style, 20), width=200, justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR, placeholder_text='الوظيفة داخل الإدارة')
        self.Function_Entry.grid(row=11, column=0, padx=20)



        name_lbl = ctk.CTkLabel (self.big_scrollable_frame, text='تاريخ الإنضمام للإدارة', font=(font_style, guide_font_size, 'bold'), text_color=TEXT_COLOR)
        name_lbl.grid(row=12, column = 1, sticky= 'e', pady=20, padx=20)
        self.DateOfJoin_Entry = ctk.CTkEntry(self.big_scrollable_frame, font=(font_style, 20), width=200, justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR, placeholder_text='تاريخ الإنضمام للإدارة')
        self.DateOfJoin_Entry.grid(row=12, column=0, padx=20)










        self.ErrorLabel = ctk.CTkLabel(self.root, text = '', fg_color=BG_COLOR, font=(font_style, 20, 'bold'), corner_radius=10, text_color=REMOVE_BUTTON_COLOR)
        self.ErrorLabel.pack(pady=30)



        self.SubmitButton = ctk.CTkButton(self.root, text = 'إدخال', fg_color=BUTTON_COLOR, font=(font_style, 20, 'bold'), corner_radius=10, command= lambda: self.Submit(NameBox=self.Name_Entry, BirthDate_Day_Box=self.BirthDate_Day_Entry, BirthDate_Month_Box=self.BirthDate_Month_Entry,
                            BirthDate_Year_Box=self.BirthDate_Year_Entry, Soldier_ID_Box=self.Soldier_ID_Entry, Mobile_Num_Box=self.MobileNumber_Entry, City_Box=self.City_Entry,
                            Home_Address_Box=self.HomeAddress_Entry, Governorate_Box=self.Governorate_Entry, Home_Num_Box=self.HomeNumber_Entry, Retiring_Date_Day_Box=self.RetiringDate_Day_Entry,
                            Retiring_Date_Month_Box=self.RetiringDate_Month_Entry, Retiring_Date_Year_Box=self.RetiringDate_Year_Entry, MothersMobileNum_Box=self.MothersMobileNum_Entry, FunctionBox=self.Function_Entry, Date_Of_Join_Box=self.DateOfJoin_Entry))
        self.SubmitButton.pack()


        self.returnButton = ctk.CTkButton(self.root, fg_color=BUTTON_COLOR, text='الرجوع للقائمة', command=self.quit, font=(font_style, 20, 'bold'), corner_radius=10)
        self.returnButton.place(relx=0.1, rely=0.9, anchor=ctk.CENTER)



        self.root.bind('<Control-q>', lambda x: self.quit())

        if (self.edit_mode):
            self.edit_doc(image_path= self.image_path, name = self.name, birth_date= self.birth_date, soldier_id= self.soldier_id, retiring_date= self.retiring_date, mobile_number= self.mobile_number, home_number= self.home_number, home_address= self.home_address, city= self.city, governorate= self.governorate, mothers_mob_number= self.mothers_mob_number, function_inside_department= self.function_inside_department, date_of_join= self.date_of_join)






        self.root.mainloop()




    def edit_doc(self, image_path= '../data/unknown_image.png', name =  'لا يوجد', birth_date= date(1970, 1, 1).isoformat(), soldier_id= 'لا يوجد', retiring_date= date(1970, 1, 1).isoformat(), mobile_number= 'لا يوجد', home_number= 'لا يوجد', home_address= 'لا يوجد', city= 'لا يوجد', governorate= 'لا يوجد', mothers_mob_number= 'لا يوجد', function_inside_department= 'لا يوجد', date_of_join= 'لا يوجد'):
        if(self.edit_mode):
            if(not image_path): image_path = '../data/unknown_image.png'
            # self.img= ctk.CTkImage(light_image=Image.open(os.path.abspath(image_path)), dark_image=Image.open(os.path.abspath(image_path)), size=(225,225))
            # self.ImageLBL = ctk.CTkLabel(self.Image_Frame, width=225, height=226, image=self.img, text='')
            # self.ImageLBL.pack()
            self.AddImagePlaceHolder(image_path=image_path)
            self.Name_Entry.insert(0, name)
            self.Soldier_ID_Entry.insert(0, soldier_id)
            self.MobileNumber_Entry.insert(0, mobile_number)
            self.HomeAddress_Entry.insert(0, home_address)
            self.City_Entry.insert(0, city)
            self.Governorate_Entry.insert(0, governorate)
            self.HomeNumber_Entry.insert(0, home_number)
            self.MothersMobileNum_Entry.insert(0, mothers_mob_number)
            self.Function_Entry.insert(0, function_inside_department)
            self.DateOfJoin_Entry.insert(0, date_of_join)


            self.RetiringDate_Day_Entry.insert(0, str(date.fromisoformat(retiring_date).day))
            self.RetiringDate_Month_Entry.insert(0, str(date.fromisoformat(retiring_date).month))
            self.RetiringDate_Year_Entry.insert(0, str(date.fromisoformat(retiring_date).year))


            self.BirthDate_Day_Entry.insert(0, str(date.fromisoformat(birth_date).day))
            self.BirthDate_Month_Entry.insert(0, str(date.fromisoformat(birth_date).month))
            self.BirthDate_Year_Entry.insert(0, str(date.fromisoformat(birth_date).year))
    


    def quit(self):
        self.root.destroy()
















# dp = DocumentEntryPage()
# dp.renderDocumentsEntryPage()
