import customtkinter as ctk
from tkinter import ttk
import re, math
from datetime import date, timedelta
from enums import EntryError, EntryErrorCode, ArmyLevels
# from MainMenu import MainMenu
import helpers
from style import *
from tkcalendar import Calendar
from PIL import Image, ImageTk
# from VacationsPage import VacationsPage

FONT_STYLE = 'Dubai'








class Vacations_Group_Page ():

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



    def Add_Row(self, master_frame, data:tuple):
        New_Row_Frame = ctk.CTkFrame(master=master_frame, width = 1380, height=35, fg_color=ENTRY_FG_COLOR)
        New_Row_Frame.pack(pady=3, fill=ctk.X)


        service_days = data[2]
        if(data[1] == 'غير محسوب بعد'):
                service_days = 'لم يحسب بعد'


        Last_Date_Lbl = ctk.CTkLabel(master=New_Row_Frame, text= data[1], font=(FONT_STYLE, 16, 'bold'), justify = 'right', width=30, text_color=TEXT_COLOR)
        Last_Date_Lbl.place(relx=0.6, rely=0.5, anchor='center')


        Name_Lbl = ctk.CTkLabel(master=New_Row_Frame, text= data[0], font=(FONT_STYLE, 16, 'bold'), justify = 'right', width=30, text_color=TEXT_COLOR)
        Name_Lbl.place(relx=0.88, rely=0.5, anchor='center')

        if(data[2] >= 0):
            Service_Days_Lbl = ctk.CTkLabel(master=New_Row_Frame, text= service_days, font=(FONT_STYLE, 16, 'bold'), justify = 'right', width=30, text_color=TEXT_COLOR)
            Service_Days_Lbl.place(relx=0.3, rely=0.5, anchor='center')

            
            Enter_Vacation_Button = ctk.CTkButton(master=New_Row_Frame, text= 'نزول', fg_color=BUTTON_LIGHT_COLOR, font=(FONT_STYLE, 16, 'bold'))
            Enter_Vacation_Button.configure(command=lambda: self.add_Vacation(name=data[0], Soldier_ID_string=data[3], FromYearbox=self.Date_Year_Entry, FromMonthbox=self.Date_Month_Entry, FromDaybox=self.Date_Day_Entry, duration=self.Duration_Textbox, frame_to_be_destroyed=New_Row_Frame, master_frame=master_frame))
            Enter_Vacation_Button.place(relx=0.1, rely=0.5, anchor='center')
            
        else:
            Extension_Button = ctk.CTkButton(master=New_Row_Frame, text= 'مد', fg_color=ACCEPT_COLOR, font=(FONT_STYLE, 16, 'bold'), width=50)
            Extension_Button.configure(command=lambda: self.show_extension_entry(New_Row_Frame, Extension_Button, Soldier_ID=data[3]))
            Extension_Button.grid(row=0, column=2, sticky='E', padx=20)


            # Summon_Button = ctk.CTkButton(master=New_Row_Frame, text= 'إستدعاء', fg_color=REMOVE_BUTTON_COLOR, font=(FONT_STYLE, 16, 'bold'))
            # Summon_Button.grid(row=0, column=0, sticky='E', padx=20)



    def show_extension_entry(self, frame, Extension_Button, Soldier_ID):
        extension_duration_entry= ctk.CTkEntry(frame, font=(FONT_STYLE, 14), width=50, justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR, placeholder_text='المدة')
        extension_duration_entry.grid(row=0, column=1, sticky='E', padx=20)

        

        Extension_Button.configure(text='تأكيد', command=lambda: self.Extend(frame= frame, Soldier_ID=Soldier_ID, Duration_Box=extension_duration_entry, Extension_Button=Extension_Button))


    def Extend(self, frame, Soldier_ID, Duration_Box, Extension_Button):

        try:
            Duration = Duration_Box.get()
            if(not Duration):
                self.displayError('المدة غير صالحة')
                return
            Duration = int(Duration)
        except:
            self.displayError('المدة غير صالحة')
            return
        if(Duration== '' and Duration <=0):
            self.displayError('المدة غير صالحة')
            return
        
        to_date = helpers.GetToDateFromVacation(Soldier_ID=Soldier_ID)
        new_date_string = date.fromisoformat(to_date) + timedelta(days=Duration)
        new_date_string = new_date_string.isoformat()
        helpers.ExtendVacation(Soldier_ID=Soldier_ID, new_to_date=new_date_string)
        # Extension_Button.configure(text='تأكيد', command=lambda: self.destroy_extension_entry(frame= frame, extension_entry=Duration_Box, extension_button=Extension_Button))

        Duration_Box.destroy()
        Extension_Button.configure(text='مد', command= lambda: self.show_extension_entry(frame, Extension_Button, Soldier_ID=Soldier_ID))




    def add_Vacation(self, name, Soldier_ID_string, FromYearbox, FromMonthbox, FromDaybox, duration, frame_to_be_destroyed, master_frame):

        
        (from_year, from_month, from_day) = FromYearbox.get(), FromMonthbox.get(), FromDaybox.get()
        try:
            self.validate_date(year=from_year, month=from_month, day=from_day)
        except EntryError as e:
            self.displayError(e)
            return
        
        
        From_date_string = date(year=int(from_year), month=int(from_month), day= int(from_day)).isoformat()


        try:
            duration = duration.get()
            duration = int(duration)
            if(duration and duration <= 0):
                self.displayError('برجاء إدخال مدة أجازة صالحة')
                return
        except:
            self.displayError('برجاء إدخال مدة أجازة صالحة')
            return

        
        
        to_date_string = date.fromisoformat(From_date_string) + timedelta(days=duration)
        to_date_string = to_date_string.isoformat()
      
        
        soldierdata = {'Name':name, 'Soldier_ID': Soldier_ID_string,'From_Date': From_date_string, 'To_Date': to_date_string}            
        
        
        try:
            helpers.CheckIfSoldierExists(soldier_data=soldierdata, Table_Name='Vacations')
        except:
            self.displayError(EntryErrorCode.VACATION_ALREADY_EXISTING.value)
            return
        
        try:
            helpers.AddVacation(Soldier_ID=Soldier_ID_string, FromDate=From_date_string, ToDate=to_date_string, State=1, Summoned=0)
        except EntryError as e:
            self.displayError(e)
            return

        self.errors_Lbl.configure(text='')
        frame_to_be_destroyed.pack_forget()

        
        last_vac_date = helpers.getLastReturnFromID(Soldier_ID=Soldier_ID_string)
        service_days = helpers.getServiceDays(last_vac_date)
        data = (name, last_vac_date, service_days, Soldier_ID_string)
        self.Add_Row(master_frame=master_frame, data=data)


    def Soldiers_Showing_Frame(self):
        all_present_soldiers = helpers.fetchSoldiers()
        data_to_be_displayed = []
        for soldier in all_present_soldiers:
            Soldier_ID = soldier['Soldier_ID']
            Soldier_Name = soldier['Name']
            last_vac_date = helpers.getLastReturnFromID(Soldier_ID=Soldier_ID)
            service_days = helpers.getServiceDays(last_vac_date)
            

            data_to_be_displayed.append((Soldier_Name, last_vac_date, service_days, Soldier_ID))
        
        # all_absent_soldiers = helpers.getActiveVacations(with_disabled=True)
        # for soldier in all_absent_soldiers:
        #     Soldier_ID = soldier[0]
        #     Soldier_Name = soldier[1]
        #     last_vac_date = helpers.getLastReturnFromID(Soldier_ID=Soldier_ID)
        #     service_days = helpers.getServiceDays(last_vac_date)
        #     data_to_be_displayed.append((Soldier_Name, last_vac_date, service_days, Soldier_ID))


        data_to_be_displayed.sort(key=lambda x: x[2], reverse= True) #sort according to service days


        frame_for_scrollable_frame = ctk.CTkFrame(self.root, width=1460,fg_color=FRAME_DARK_COLOR, border_color=BUTTON_COLOR, border_width=5, corner_radius=15)
        frame_for_scrollable_frame.pack()
        
        Header_Frame = ctk.CTkFrame(master=frame_for_scrollable_frame, fg_color=FRAME_LIGHT_COLOR, width=1460, height=30, corner_radius=5)
        Header_Frame.pack(pady=8, padx=8)
        
        
        Master_Frame = ctk.CTkScrollableFrame(frame_for_scrollable_frame, label_text="", width=1430, height=500,fg_color=FRAME_DARK_COLOR, label_fg_color=FRAME_DARK_COLOR, scrollbar_button_color=BUTTON_COLOR)
        # self.big_Entire_Frame = entire_preview_frame

        # Master_Frame = ctk.CTkScrollableFrame(master=self.root, width=1000, height=500)
        Master_Frame.pack(padx=10)

        

        Service_Days_Lbl = ctk.CTkLabel(master=Header_Frame, text= 'عدد أيام الخدمة', font=(FONT_STYLE, 16, 'bold'), justify = ctk.RIGHT, text_color=FG_COLOR)
        Service_Days_Lbl.place(relx=0.3, rely=0.5, anchor='center')

        Last_Date_Lbl = ctk.CTkLabel(master=Header_Frame, text= 'تاريخ آخر عودة', font=(FONT_STYLE, 16, 'bold'), justify = ctk.RIGHT, text_color=FG_COLOR)
        Last_Date_Lbl.place(relx=0.6, rely=0.5, anchor='center')


        Name_Lbl = ctk.CTkLabel(master=Header_Frame, text= 'الإسم', font=(FONT_STYLE, 16, 'bold'), justify = ctk.RIGHT, text_color=FG_COLOR)
        Name_Lbl.place(relx=0.88, rely=0.5, anchor='center')


        for soldier in data_to_be_displayed:
            self.Add_Row(Master_Frame, soldier)









    def showCalendar(self):
        self.calenndar = Calendar(self.date_frame, font=('Comic Sans MS', 12), borderwidth=10, background = CALENDAR_BG, foreground=CALENDAR_FG, 
                             bordercolor = '#F5F5F5', normalbackground='#FFFFFF', disabledbackground = '#F5F5F5', disabledforeground = '#F5F5F5', selectforeground = '#F5F5F5',
                             selectbackground = '#0047FF',
                             headerforeground='#749BC2',
                             cursor='heart', showweeknumbers = False
                             ,weekendbackground='#F5F5F5')
        

        for child in self.date_frame.winfo_children():
            child_widget = self.date_frame.nametowidget(child)
            child_widget.grid_forget()
        self.calenndar.grid(row=0, column=0, columnspan=3, padx=10, pady=20)

        self.calendar_button.configure(text='اختيار', command=self.hideCalendar)


    def hideCalendar(self ):

        chosen_date = self.calenndar.get_date() #returned as 4/25/24 for 2024/March/25th
        month, day, year = re.split('/',chosen_date)
        year = "20"+year

        self.calenndar.destroy()


        self.Date_Day_Entry = ctk.CTkEntry(self.date_frame, font=("Arial", 15), width=100, placeholder_text='اليوم', justify='right', fg_color=FG_COLOR, text_color=TEXT_COLOR)
        self.Date_Day_Entry.grid(row=0, column=2, padx=5)

        self.Date_Month_Entry = ctk.CTkEntry(self.date_frame, font=("Arial", 15), width=100, placeholder_text='الشهر', justify='right', fg_color=FG_COLOR, text_color=TEXT_COLOR)
        self.Date_Month_Entry.grid(row=0, column=1, padx=5)

        self.Date_Year_Entry = ctk.CTkEntry(self.date_frame, font=("Arial", 15), width=100, placeholder_text='السنة', justify='right', fg_color=FG_COLOR, text_color=TEXT_COLOR)
        self.Date_Year_Entry.grid(row=0, column=0, padx=5)

        self.Date_Day_Entry.insert(0, day)
        self.Date_Month_Entry.insert(0, month)
        self.Date_Year_Entry.insert (0, year)


        self.calendar_button.configure(text='التقويم', command= self.showCalendar)
    

    def control_panel(self):
        dummy_frame = ctk.CTkFrame(master=self.root, width=700, height=50, fg_color=BG_COLOR)
        dummy_frame.pack(pady=30, padx=10)
        # dummy_frame2 = ctk.CTkFrame(master=dummy_frame, width=700, height=50, fg_color=BG_COLOR)
        # dummy_frame2.place(relx=0.5, rely=0.5, anchor='center')

        label = ctk.CTkLabel(dummy_frame, text='المدة', font=('Arial', 20, 'bold'), fg_color=FG_COLOR, text_color=TEXT_COLOR)
        label.pack(side=ctk.RIGHT)
        self.Duration_Textbox = ctk.CTkEntry(dummy_frame, font=("Arial", 20), width=50, justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR, placeholder_text='7')
        self.Duration_Textbox.pack(side=ctk.RIGHT, padx=10)


        self.calendar_button = ctk.CTkButton(master=dummy_frame, text='التقويم', font=(FONT_STYLE, 16, 'bold'), fg_color=BUTTON_COLOR, text_color=WHITE_TEXT_COLOR, command=self.showCalendar)
        self.calendar_button.pack(side=ctk.LEFT)

        self.date_frame = ctk.CTkFrame(dummy_frame, width=200, fg_color=TEXT_BOX_FG_COLOR)
        self.date_frame.pack(side=ctk.LEFT)
        self.AddVacationDatePlaceHolder(self.date_frame)

        label = ctk.CTkLabel(dummy_frame, text="تاريخ النزول", font=('Arial', 20, 'bold'), fg_color=FG_COLOR, text_color=TEXT_COLOR)
        label.pack(side=ctk.LEFT, padx=10)



    def AddVacationDatePlaceHolder(self, date_frame):
        
        self.Date_Day_Entry = ctk.CTkEntry(date_frame, font=(FONT_STYLE, 15), width=100, placeholder_text='اليوم', justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR)
        self.Date_Day_Entry.grid(row=0, column=2, padx=5)

        self.Date_Month_Entry = ctk.CTkEntry(date_frame, font=(FONT_STYLE, 15), width=100, placeholder_text='الشهر', justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR)
        self.Date_Month_Entry.grid(row=0, column=1, padx=5)

        self.Date_Year_Entry = ctk.CTkEntry(date_frame, font=(FONT_STYLE, 15), width=100, placeholder_text='السنة', justify='right', fg_color=TEXT_BOX_FG_COLOR, text_color=TEXT_COLOR)
        self.Date_Year_Entry.grid(row=0, column=0, padx=5)

        # self.retiringdcalendarshowbutton = ctk.CTkButton(date_frame, text='التقويم', font=(FONT_STYLE, 15), width=30, command= lambda: self.showCalendar('retire'))
        # self.retiringdcalendarshowbutton.grid(row=0, column=0, sticky='n')



    def __init__(self, func_to_other_window):
        self.func_to_other_window = func_to_other_window
        self.root = ctk.CTk(fg_color=BG_COLOR)

        self.root.title("تسجيل أجازات")
        screen_width, screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        width, height = 1700, 900
        self.root.geometry(f"{width}x{height}+{str(math.floor(screen_width/2 - width/2))}+{str(math.floor(screen_height/2 - height/2))}")  # Set window size
        self.root.iconbitmap("../data/icolog.ico")

        BigLabel = ctk.CTkLabel(master=self.root, text="تسجيل أجازات", font=(FONT_STYLE, 60, 'bold'),text_color=TEXT_COLOR)
        BigLabel.pack()

        self.control_panel()


        self.Soldiers_Showing_Frame()


        return_Button = ctk.CTkButton(master=self.root, text='العودة للقائمة', font=(FONT_STYLE, 16, 'bold'), fg_color=BUTTON_COLOR, text_color=WHITE_TEXT_COLOR, command=self.quit)
        return_Button.pack(side='left', padx=50, expand=True)


        individual_Vac_Button = ctk.CTkButton(master=self.root, text='تسجيل أجازات فردية', font=(FONT_STYLE, 16, 'bold'), fg_color=BUTTON_COLOR, text_color=WHITE_TEXT_COLOR, command=self.func_to_other_window)
        individual_Vac_Button.pack(side = 'left', padx=50, anchor='center', pady=10, expand=True)


        self.errors_Lbl = ctk.CTkLabel(self.root, font=('Arial', 20, 'bold'), text_color='red', text='')
        self.errors_Lbl.place(relx=0.5, rely=0.9, anchor=ctk.CENTER)









    def render(self):
        self.root.mainloop()

    def quit(self):
        self.root.destroy()

    def displayError(self, ErrType):
        self.errors_Lbl.configure(text=ErrType)
        return
    


# def open_individual_vac_page(prev_root):
#     prev_root.destroy()
#     vp = VacationsPage()
#     vp.renderVacationsPage()



# vgp = Vacations_Group_Page()
# vgp.render()