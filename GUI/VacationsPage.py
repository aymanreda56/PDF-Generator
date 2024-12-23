import customtkinter as ctk
from tkinter import ttk
import re, math
from datetime import date
from enums import EntryError, EntryErrorCode, ArmyLevels
# from MainMenu import MainMenu
import helpers
from style import *
from tkcalendar import Calendar
from PIL import Image, ImageTk

def reverse_Arabic_Words(string):
    words = re.split(' ', string)
    words.reverse()
    return ' '.join(words)



class VacationsPage():
    def validate_date(self, year, month, day):
        try:
            year = int(year)
            month = int(month)
            day = int(day)
        except:
            raise EntryError(EntryErrorCode.RETIRING_DATE_INTEGER_ERR)
        if(year < 2023):
            raise EntryError(EntryErrorCode.RETIRING_DATE_YEAR_ERR)
        if(month not in range(1,13)):
            raise EntryError(EntryErrorCode.RETIRING_DATE_MONTH_ERR)
        if(day not in range(1,32)):
            raise EntryError(EntryErrorCode.RETIRING_DATE_DAY_ERR)
        try:
            date(year=year, month=month, day= day)
        except:
            raise EntryError(EntryErrorCode.RETIRING_DATE_GENERAL_ERR)




    def validate_ID(self, ID_string):
        if ((not ID_string) or ID_string == '' or re.sub('\s+','', ID_string) == '' ):
            raise EntryError(EntryErrorCode.SOLDIER_ID_MISSING)

        for c in ID_string:
            if ord(c) not in range (48,58):
                raise EntryError(EntryErrorCode.SOLDIER_ID_INTEGER_ERR)
            
        for c in ID_string:
            if c not in list('1234567890'):
                raise EntryError(EntryErrorCode.SOLDIER_ID_ERR)

        return ID_string
    



    def validate_name(self, text):
        if ((not text) or text == '' or re.sub('\s+','', text) == '' ):
            raise EntryError(EntryErrorCode.SOLDIER_NAME_MISSING)
        if(len(re.split(' ',text)) < 3):
            raise EntryError(EntryErrorCode.SOLDIER_NAME_TOO_SHORT_ERR)
        if(len(text) > 70):
            raise EntryError(EntryErrorCode.SOLDIER_NAME_TOO_LONG_ERR)
        ############################################################ TODO: this should correctly handle non-arabic characters##################
        for c in text:
            if c in list('abcdefghijklmnopqrstuvwxyz'):
                raise EntryError(EntryErrorCode.SOLDIER_NAME_NOT_ARABIC)
            ################################################################################################
        
        #print(text)
        text = re.sub(r'\s+', ' ', text)
        return text



    def submit_text(self, Namebox, IDbox, Level_comboBox, FromYearbox, FromMonthbox, FromDaybox, ToYearbox, ToMonthbox, ToDaybox):

        print(FromYearbox.get())
        print(FromMonthbox.get())
        print(FromDaybox.get())
        print(type(FromYearbox.get()))

        #making a date object from the date textboxes
        try:
            name = self.validate_name(Namebox.get())
        except EntryError as e:
            self.displayError(e)
            return
        

        try:
            Soldier_ID_string = self.validate_ID(IDbox.cget('text'))
        except EntryError as e:
            self.displayError(e)
            return


        (from_year, from_month, from_day) = FromYearbox.get(), FromMonthbox.get(), FromDaybox.get()
        try:
            self.validate_date(year=from_year, month=from_month, day=from_day)
        except EntryError as e:
            self.displayError(e)
            return
        From_date_string = date(year=int(from_year), month=int(from_month), day= int(from_day)).isoformat()


        (to_year, to_month, to_day) = ToYearbox.get(), ToMonthbox.get(), ToDaybox.get()
        try:
            self.validate_date(year=to_year, month=to_month, day=to_day)
        except EntryError as e:
            self.displayError(e)
            return
        to_date_string = date(year=int(to_year), month=int(to_month), day= int(to_day)).isoformat()
       
        try:
            if(date.fromisoformat(From_date_string) > date.fromisoformat(to_date_string)):
                raise EntryError(EntryErrorCode.VACATIONS_DATES_ARE_NEGATIVE)
        except EntryError as e:
            self.displayError(e)
            return
        
        soldierdata = {'Name':name, 'Soldier_ID': Soldier_ID_string, 'Level': str(ArmyLevels.index(Level_comboBox.cget('text'))+1),'From_Date': From_date_string, 'To_Date': to_date_string}            
        
        extended = False
        try:
            helpers.CheckIfSoldierExists(soldier_data=soldierdata, Table_Name='Vacations')
        except:
            to_date_of_existing_vac = helpers.GetToDateFromVacation(Soldier_ID_string)
            if(date.fromisoformat(From_date_string) != date.fromisoformat(to_date_of_existing_vac)):
                self.displayError(EntryErrorCode.VACATION_ALREADY_EXISTING.value)
                return
            else:
                extended = True
        

        try:
            if(extended):
                helpers.ExtendVacation(Soldier_ID=Soldier_ID_string, new_to_date=to_date_string)
            else:
                helpers.AddVacation(Soldier_ID=Soldier_ID_string, FromDate=From_date_string, ToDate=to_date_string, State=1, Summoned=0, Extended=0)
        except EntryError as e:
            self.displayError(e)
            return

        self.Add_Soldier_To_Preview(soldier_data=soldierdata, entries_frame=self.entries_frame, num_entries=self.number_Of_Vacations)
        

        self.number_Of_Vacations += 1

        self.errors_Lbl.configure(text='')





    def Soldiers_Preview_show(self):
        #self.Soldiers_previewed_flag = True if helpers.fetchSoldiers() else False
        self.frame_for_scrollable_frame = ctk.CTkFrame(self.root, width=1460, fg_color=FRAME_DARK_COLOR, border_color=BUTTON_COLOR, border_width=5, corner_radius=15)
        self.frame_for_scrollable_frame.pack()
        entire_preview_frame = ctk.CTkScrollableFrame(self.frame_for_scrollable_frame, label_text="", width=1440, fg_color=FRAME_DARK_COLOR, label_fg_color=FRAME_DARK_COLOR, scrollbar_button_color=BUTTON_COLOR)
        self.big_Entire_Frame = entire_preview_frame
        # if(self.Soldiers_previewed_flag):
        self.big_Entire_Frame.pack(padx=10, pady=10)
        another_frame = ctk.CTkFrame(self.big_Entire_Frame, width=1350, height=20, fg_color=FRAME_DARK_COLOR)
        # if(self.Soldiers_previewed_flag):
        another_frame.pack(pady=5)
        headerLbl = ctk.CTkLabel(another_frame, text="الإسم", font=('Arial', 18, 'bold'), text_color=TEXT_COLOR)
        headerLbl.place(relx=0.93, rely=0.5, anchor=ctk.CENTER)

        headerLbl = ctk.CTkLabel(another_frame, text="الرقم العسكري", font=('Arial', 18, 'bold'), text_color=TEXT_COLOR)
        headerLbl.place(relx=0.7, rely=0.5, anchor=ctk.CENTER)

        headerLbl = ctk.CTkLabel(another_frame, text='الرتبة', font=('Arial', 18, 'bold'), text_color=TEXT_COLOR)
        headerLbl.place(relx=0.47, rely=0.5, anchor=ctk.CENTER)

        headerLbl = ctk.CTkLabel(another_frame, text="من", font=('Arial', 18, 'bold'), text_color=TEXT_COLOR)
        headerLbl.place(relx=0.26, rely=0.5, anchor=ctk.CENTER)


        headerLbl = ctk.CTkLabel(another_frame, text="إلى", font=('Arial', 18, 'bold'), text_color=TEXT_COLOR)
        headerLbl.place(relx=0.1, rely=0.5, anchor=ctk.CENTER)


        self.entries_frame = ctk.CTkFrame(self.big_Entire_Frame, width=1380)
        # if(self.Soldiers_previewed_flag):
        self.entries_frame.pack()

        allSoldiers = helpers.getActiveVacations(with_disabled= True)
        if(allSoldiers):#) and self.Soldiers_previewed_flag):
            for i, soldier in enumerate(allSoldiers):
                soldier_dict = {'Soldier_ID': soldier[0], 'Name': soldier[1], 'Level': helpers.getLevelFromID(soldier[0]),'From_Date': soldier[2], 'To_Date': soldier[3], 'State': soldier[4], 'Summoned': soldier[5]}
                self.Add_Soldier_To_Preview(soldier_data=soldier_dict, entries_frame=self.entries_frame, num_entries=i)


        # self.Soldiers_previewed_flag
        
        return self.entries_frame, entire_preview_frame
    


    def Add_Soldier_To_Preview(self, soldier_data, entries_frame, num_entries: int):
        #print(soldier_data)

        new_entry_frame = ctk.CTkFrame(entries_frame, width = 1380, height=35, fg_color=ENTRY_FG_COLOR)
        new_entry_frame.pack(padx= 2, pady=2)

        newEntryLabel = ctk.CTkLabel(new_entry_frame, text=soldier_data['Name'], font=('Arial', 20, 'bold'), width=30, text_color=TEXT_COLOR)
        newEntryLabel.place(relx=0.92, rely=0.5, anchor=ctk.CENTER)

        newEntryLabel = ctk.CTkLabel(new_entry_frame, text=soldier_data['Soldier_ID'], font=('Arial', 20, 'bold'), width=30, text_color=TEXT_COLOR)
        newEntryLabel.place(relx=0.7, rely=0.5, anchor=ctk.CENTER)

        newEntryLabel = ctk.CTkLabel(new_entry_frame, text=ArmyLevels[int(soldier_data["Level"])-1], font=('Arial', 20, 'bold'), width=30, text_color=TEXT_COLOR)
        newEntryLabel.place(relx=0.47, rely=0.5, anchor=ctk.CENTER)

        newEntryLabel = ctk.CTkLabel(new_entry_frame, text=soldier_data['From_Date'], font=('Arial', 20, 'bold'), width=30, text_color=TEXT_COLOR)
        newEntryLabel.place(relx=0.26, rely=0.5, anchor=ctk.CENTER)

        newEntryLabel = ctk.CTkLabel(new_entry_frame, text=soldier_data['To_Date'], font=('Arial', 20, 'bold'), width=30, text_color=TEXT_COLOR)
        newEntryLabel.place(relx=0.1, rely=0.5, anchor=ctk.CENTER)

        newCheckBox = ctk.CTkCheckBox(master=new_entry_frame, text='')

        if(helpers.CheckStateOfVacation(soldier_data['Soldier_ID'])[0] == 1):
            newCheckBox.select()
        else:
            newCheckBox.deselect()

        newCheckBox.configure(command= lambda: self.Change_Printable_State(Soldier_ID=soldier_data['Soldier_ID'], checkbox=newCheckBox))
        
        newCheckBox.place(relx=0.8, rely=0.5, anchor=ctk.CENTER)

        DelButton = ctk.CTkButton(new_entry_frame, text='إزالة', font=('Arial', 20, 'bold'), width=30, height=30,fg_color=REMOVE_BUTTON_COLOR, command=lambda frame=new_entry_frame: self.Remove_Soldier_From_Preview(soldier_data['Soldier_ID'], frame))
        DelButton.place(relx=0.02, rely=0.5, anchor='center')
        self.array_of_entry_frames.append(new_entry_frame)


    def displayError(self, ErrType):
        self.errors_Lbl.configure(text=ErrType)
        return


    def Remove_Soldier_From_Preview(self, Soldier_ID, frame_to_be_destroyed):
        helpers.RemoveVacation(Soldier_ID=Soldier_ID, delete_from_history=True)
        frame_to_be_destroyed.destroy()
        return
    

    def Change_Printable_State(self, Soldier_ID, checkbox):
        new_state = '1' if (checkbox.get() == 1) else '0'
        helpers.UpdateVacationState(Soldier_ID=Soldier_ID, new_state=new_state)
        return



        
    def __init__(self, func_to_other_window):

        self.func_to_other_window = func_to_other_window
        
        self.root = None
        self.errors_Lbl = None
        self.number_Of_Vacations = len(helpers.getActiveVacations(with_disabled=True)) if (helpers.getActiveVacations(with_disabled=True)) else 0
        self.preview_frame = None
        self.destroyed = False
        self.big_Entire_Frame = None
        self.array_of_entry_frames = []
        
        # self.renderVacationsPage()
    

    def BackToMainMenu(self):
        self.destroyed = True
        if(self.destroyed):
            self.root.destroy()
            return


    def ChangePlaceHoldersWithComboBox(self, event):
        chosenName = self.Name_ComboBox.get()
        self.Level_textbox.configure(text=helpers.getSoldierLevelFromID(helpers.getSoldierIDFromName(chosenName)))
        self.Soldier_ID_textbox.configure(text=helpers.getSoldierIDFromName(chosenName))

        
        # self.Name_ComboBox.configure(text = chosenName)



    
    def showCalendar(self, is_from_date):


        
        calenndar = Calendar(self.mainframe, font=('Comic Sans MS', 12), borderwidth=10, background = CALENDAR_BG, foreground=CALENDAR_FG, 
                             bordercolor = '#F5F5F5', normalbackground='#FFFFFF', disabledbackground = '#F5F5F5', disabledforeground = '#F5F5F5', selectforeground = '#F5F5F5',
                             selectbackground = '#0047FF',
                             headerforeground='#749BC2',
                             cursor='heart', showweeknumbers = False
                             ,weekendbackground='#F5F5F5')
        assert(is_from_date == 0 or is_from_date == 1)
        calenndar.grid(row=2, column=is_from_date, padx=10, pady=20)

        if(is_from_date):
            calling_button = self.From_Date_Calendar_Show_Button
            self.from_date_calendar = calenndar
        else:
            calling_button = self.To_Date_Calendar_Show_Button
            self.to_date_calendar = calenndar

        calling_button.configure(text='اختيار', command= lambda: self.hideCalendar(is_from_date))


    def hideCalendar(self, is_from_date ):

        if(is_from_date):
            calling_button = self.From_Date_Calendar_Show_Button
            calenndar = self.from_date_calendar
            date_frame = self.From_date_frame
            day_box, month_box, year_box = self.From_Date_day, self.From_Date_month, self.From_Date_year
        else:
            calling_button = self.To_Date_Calendar_Show_Button
            calenndar = self.to_date_calendar
            date_frame = self.To_date_frame
            day_box, month_box, year_box = self.to_Date_day, self.to_Date_month, self.to_Date_year

        chosen_date = calenndar.get_date() #returned as 4/25/24 for 2024/March/25th
        month, day, year = re.split('/',chosen_date)
        year = "20"+year

        calenndar.destroy()

        date_frame = ctk.CTkFrame(self.mainframe, width=300, height=100, fg_color=FG_COLOR)
        date_frame.grid(row=2, column=is_from_date, padx=10, pady=20)

        day_box = ctk.CTkEntry(date_frame, font=("Arial", 15), width=100, placeholder_text='اليوم', justify='right', fg_color=FG_COLOR, text_color=TEXT_COLOR)
        day_box.grid(row=0, column=2, padx=5)

        month_box = ctk.CTkEntry(date_frame, font=("Arial", 15), width=100, placeholder_text='الشهر', justify='right', fg_color=FG_COLOR, text_color=TEXT_COLOR)
        month_box.grid(row=0, column=1, padx=5)

        year_box = ctk.CTkEntry(date_frame, font=("Arial", 15), width=100, placeholder_text='السنة', justify='right', fg_color=FG_COLOR, text_color=TEXT_COLOR)
        year_box.grid(row=0, column=0, padx=5)

        day_box.insert(0, day)
        month_box.insert(0, month)
        year_box.insert (0, year)

        if(is_from_date):
            self.From_Date_Calendar_Show_Button = calling_button
            self.from_date_calendar = calenndar
            self.From_date_frame = date_frame
            self.From_Date_day, self.From_Date_month, self.From_Date_year = day_box, month_box, year_box
        else:
            self.To_Date_Calendar_Show_Button = calling_button
            self.to_date_calendar = calenndar
            self.To_date_frame = date_frame
            self.to_Date_day, self.to_Date_month, self.to_Date_year = day_box, month_box, year_box

        calling_button.configure(text='التقويم', command= lambda x = calling_button: self.showCalendar(is_from_date))




    def renderVacationsPage(self):
        
        self.root = ctk.CTkToplevel(fg_color=BG_COLOR)

        self.root.title("تنظيم وأفراد مكتب السيد/ مدير الجهاز")
        

        screen_width, screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        width, height = 1600, 1000
        self.root.geometry(f"{width}x{height}+{str(math.floor(screen_width/2 - width/2))}+{str(math.floor(screen_height/2 - height/2))}")  # Set window size

        self.root.iconbitmap("../data/icolog.ico")

        label = ctk.CTkLabel(self.root, text="أدخل بيانات العساكر",  font=('Arial', 35, 'bold'), text_color=TEXT_COLOR)
        label.pack(pady=20)

        img= ctk.CTkImage(light_image=Image.open('../data/logo_dark.png'), dark_image=Image.open('../data/logo_dark.png'), size=(250,312.5))
        ImageLBL = ctk.CTkLabel(self.root, width=self.root.winfo_width(), height=self.root.winfo_height(), image=img, text='')
        ImageLBL.place(relx=0.93, rely=0.2, anchor=ctk.CENTER)

        bg_img= ctk.CTkImage(light_image=Image.open('../data/bg_logo_semi_transparent.png'), dark_image=Image.open('../data/bg_logo_semi_transparent.png'), size=(1000,1000))
        ImageLBL = ctk.CTkLabel(self.root, image=bg_img, text='')
        ImageLBL.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)


        house_img= ctk.CTkImage(light_image=Image.open('../data/house.png'), dark_image=Image.open('../data/house.png'), size=(200,200))
        house_img_lbl = ctk.CTkLabel(self.root, width=200, height=200, image=house_img, text='')
        house_img_lbl.place(relx=0.85, rely=0.8, anchor=ctk.CENTER)


        self.mainframe = ctk.CTkFrame(self.root, width=800, height=400, fg_color=BG_COLOR)
        self.mainframe.pack(anchor='center', pady=20)
        

        label = ctk.CTkLabel(self.mainframe, text="الإسم", font=('Arial', 20, 'bold'), text_color=TEXT_COLOR)
        label.grid(row= 1, column=4, pady=10)


        label = ctk.CTkLabel(self.mainframe, text="الرقم العسكري", font=('Arial', 20, 'bold'), text_color=TEXT_COLOR)
        label.grid(row= 1, column=3, pady=10)

        label = ctk.CTkLabel(self.mainframe, text="الرتبة", font=('Arial', 20, 'bold'), text_color=TEXT_COLOR)
        label.grid(row= 1, column=2, pady=10)

        label = ctk.CTkLabel(self.mainframe, text="من", font=('Arial', 20, 'bold'), text_color=TEXT_COLOR)
        label.grid(row= 1, column=1, pady=10)

        label = ctk.CTkLabel(self.mainframe, text="إلى", font=('Arial', 20, 'bold'), text_color=TEXT_COLOR)
        label.grid(row= 1, column=0, pady=10)


        self.Name_ComboBox = ctk.CTkComboBox(self.mainframe, font=("Arial", 20), width=200, justify=ctk.RIGHT, values=helpers.getNamesFromDB(), command=self.ChangePlaceHoldersWithComboBox, state='readonly', dropdown_font=("Arial", 16, 'bold'), dropdown_fg_color=DROPDOWN_FG_COLOR, dropdown_text_color=DROPDOWN_TEXT_COLOR, fg_color=DROPDOWN_FG_COLOR, bg_color=FG_COLOR, text_color=DROPDOWN_TEXT_COLOR, button_color=BUTTON_COLOR, dropdown_hover_color='#51C4D3', border_width=3)
        
        self.Name_ComboBox.grid(row=2, column=4, pady=10, padx=20)

        
        self.Soldier_ID_textbox = ctk.CTkLabel(self.mainframe, font=("Arial", 20), width=200, justify='right', text=helpers.getSoldierIDFromName(Name_ComboBox=self.Name_ComboBox.get()), text_color=TEXT_COLOR)
        self.Soldier_ID_textbox.grid(row=2, column=3, pady=10, padx=20)

        self.Level_textbox = ctk.CTkLabel(self.mainframe, font=("Arial", 20), width=200, justify='right', text=helpers.getSoldierLevelFromID(Soldier_ID=self.Soldier_ID_textbox.cget('text')), text_color=TEXT_COLOR)
        self.Level_textbox.grid(row=2, column=2, pady=10, padx=20)


        self.From_date_frame = ctk.CTkFrame(self.mainframe, width=300, height=100, fg_color=BG_COLOR)
        self.From_date_frame.grid(row=2, column=1, padx=10, pady=20)

        self.From_Date_day = ctk.CTkEntry(self.From_date_frame, font=("Arial", 15), width=40, placeholder_text='اليوم', justify='right', fg_color=TEXT_BOX_FG_COLOR, border_color=TEXT_COLOR, text_color=TEXT_COLOR)
        self.From_Date_day.grid(row=0, column=2, padx=5)

        self.From_Date_month = ctk.CTkEntry(self.From_date_frame, font=("Arial", 15), width=40, placeholder_text='الشهر', justify='right', fg_color=TEXT_BOX_FG_COLOR, border_color=TEXT_COLOR, text_color=TEXT_COLOR)
        self.From_Date_month.grid(row=0, column=1, padx=5)

        self.From_Date_year = ctk.CTkEntry(self.From_date_frame, font=("Arial", 15), width=70, placeholder_text='السنة', justify='right', fg_color=TEXT_BOX_FG_COLOR, border_color=TEXT_COLOR, text_color=TEXT_COLOR)
        self.From_Date_year.grid(row=0, column=0, padx=5)

        self.From_Date_Calendar_Show_Button = ctk.CTkButton(self.mainframe, text='التقويم')
        self.From_Date_Calendar_Show_Button.configure(command= lambda: self.showCalendar(1))
        self.From_Date_Calendar_Show_Button.grid(row=3, column=1, padx=10)

        self.To_date_frame = ctk.CTkFrame(self.mainframe, width=300, height=100, fg_color=BG_COLOR)
        self.To_date_frame.grid(row=2, column=0, padx=10, pady=20)


        self.to_Date_day = ctk.CTkEntry(self.To_date_frame, font=("Arial", 15), width=40, placeholder_text='اليوم', justify='right', fg_color=TEXT_BOX_FG_COLOR, border_color=TEXT_COLOR, text_color=TEXT_COLOR)
        self.to_Date_day.grid(row=0, column=2, padx=5)

        self.to_Date_month = ctk.CTkEntry(self.To_date_frame, font=("Arial", 15), width=40, placeholder_text='الشهر', justify='right', fg_color=TEXT_BOX_FG_COLOR, border_color=TEXT_COLOR, text_color=TEXT_COLOR)
        self.to_Date_month.grid(row=0, column=1, padx=5)

        self.to_Date_year = ctk.CTkEntry(self.To_date_frame, font=("Arial", 15), width=70, placeholder_text='السنة', justify='right', fg_color=TEXT_BOX_FG_COLOR, border_color=TEXT_COLOR, text_color=TEXT_COLOR)
        self.to_Date_year.grid(row=0, column=0, padx=5)

        self.To_Date_Calendar_Show_Button = ctk.CTkButton(self.mainframe, text='التقويم')
        self.To_Date_Calendar_Show_Button.configure(command= lambda :self.showCalendar(0))
        self.To_Date_Calendar_Show_Button.grid(row=3, column=0, padx=10)

        submit_button = ctk.CTkButton(self.mainframe, text="إدخال",width=90, corner_radius=20, font=('Arial', 25, 'bold'), command=lambda: self.submit_text(self.Name_ComboBox, self.Soldier_ID_textbox, self.Level_textbox, self.From_Date_year, self.From_Date_month, self.From_Date_day, self.to_Date_year, self.to_Date_month, self.to_Date_day), fg_color=BUTTON_COLOR, text_color=BUTTON_TEXT_COLOR)
        submit_button.grid(row=4, column=2, pady=20)

        Back_to_mm_button = ctk.CTkButton(self.root, text="الرجوع إلى القائمة",width = 70, corner_radius=20, font=('Arial', 20, 'bold'), command=lambda: self.BackToMainMenu(), fg_color=BUTTON_COLOR, text_color=BUTTON_TEXT_COLOR)
        Back_to_mm_button.place(relx = 0.1, rely=0.9)


        Back_to_mm_button = ctk.CTkButton(self.root, text="شيفتات",width = 70, corner_radius=20, font=('Arial', 40, 'bold'), command=self.func_to_other_window, fg_color=BUTTON_COLOR, text_color=BUTTON_TEXT_COLOR)
        Back_to_mm_button.place(relx = 0.5, rely=0.9)
        



        self.errors_Lbl = ctk.CTkLabel(self.root, font=('Arial', 20, 'bold'), text_color='red', text='')
        self.errors_Lbl.place(relx=0.5, rely=0.9, anchor=ctk.CENTER)


        
        self.root.bind("<Control-q>", lambda x: self.quit())
        # self.root.bind("<Configure>", lambda x: self.resizeAll())

        self.root.bind("<Control-Enter>", lambda x: self.submit_text(self.Name_ComboBox, self.Soldier_ID_textbox, self.Level_textbox, self.From_Date_year, self.From_Date_month, self.From_Date_day, self.to_Date_year, self.to_Date_month, self.to_Date_day))


        # self.root.bind('enter', command=lambda: self.submit_text(Name_textbox, Soldier_ID_textbox, Level_DropDown, Retiring_Date_year, Retiring_Date_month, Retiring_Date_day))

        self.Soldiers_Preview_show()

        self.root.mainloop()

    




    def resizeAll(self):
        self.big_Entire_Frame.configure(height=self.root.winfo_height()/3)
    
    def quit(self):
        self.root.destroy()





def ShowVacationHistory():
    pass


def AddVacation():
    pass

def RemoveVacation():
    pass



def RefreshVacations_And_PushToHistory():
    pass


# VacationsPage()