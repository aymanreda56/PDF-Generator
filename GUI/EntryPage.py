import customtkinter as ctk
import re
from datetime import date
from enums import EntryError, EntryErrorCode, ArmyLevels
# from MainMenu import MainMenu
import helpers
from style import *





class EntryPage():
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
        if(day not in range(1,30)):
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
        if(len(re.split(' ',text)) < 2):
            raise EntryError(EntryErrorCode.SOLDIER_NAME_TOO_SHORT_ERR)
        if(len(text) > 40):
            raise EntryError(EntryErrorCode.SOLDIER_NAME_TOO_LONG_ERR)
        ############################################################ TODO: this should correctly handle non-arabic characters##################
        for c in text:
            if c in list('abcdefghijklmnopqrstuvwxyz'):
                raise EntryError(EntryErrorCode.SOLDIER_NAME_NOT_ARABIC)
            ################################################################################################
        
        print(text)
        text = re.sub(r'\s+', ' ', text)
        return text



    def submit_text(self, Namebox, IDbox, Level_comboBox, Yearbox, Monthbox, Daybox):
        #making a date object from the date textboxes
        try:
            name = self.validate_name(Namebox.get())
        except EntryError as e:
            self.displayError(e)
            return
        

        try:
            Soldier_ID_string = self.validate_ID(IDbox.get())
        except EntryError as e:
            self.displayError(e)
            return


        (year, month, day) = Yearbox.get(), Monthbox.get(), Daybox.get()
        try:
            self.validate_date(year=year, month=month, day=day)
        except EntryError as e:
            self.displayError(e)
            return
        retiring_date_string = date(year=int(year), month=int(month), day= int(day)).isoformat()
       
        
        
        
        soldierdata = {'Name':name, 'Soldier_ID': Soldier_ID_string, 'Level': str(ArmyLevels.index(Level_comboBox.get())+1),'Retiring_Date': retiring_date_string}            
        # self.Add_Soldier_To_Preview(soldier_data= soldierdata, preview_frame= self.preview_frame, num_entries=self.number_Of_Soldiers)
        try:
            helpers.AddNewSoldier(soldier_data=soldierdata)
        except EntryError as e:
            self.displayError(e)
            return
        # if(not self.Soldiers_previewed_flag):
        #     self.preview_frame = self.Soldiers_Preview_show()
        # else:
        self.Add_Soldier_To_Preview(soldier_data=soldierdata, entries_frame=self.entries_frame, num_entries=self.number_Of_Soldiers)
        

        self.number_Of_Soldiers += 1

        self.errors_Lbl.configure(text='')
        self.return_button_state = True if (helpers.fetchSoldiers()) else False
        self.Back_to_mm_button.configure(state='normal' if self.return_button_state else "disabled", fg_color='#8576FF' if self.return_button_state else '#074173')

        




    def reverse_arabic_text(self, arabicText):
        '''
            this function just takes an arabic sentence, splits it by spaces, then reverses each word.
            this is because tkinter does not support RTL rendering of arabic text.
        '''
        tokens = re.split(r' ',arabicText)
        tokens.reverse()
        # print(tokens)
        return ' '.join(tokens)






    def Soldiers_Preview_show(self):
        #self.Soldiers_previewed_flag = True if helpers.fetchSoldiers() else False
        entire_preview_frame = ctk.CTkScrollableFrame(self.root, label_text="Preview", width=1120, height=self.root.winfo_height()/3)
        self.big_Entire_Frame = entire_preview_frame
        # if(self.Soldiers_previewed_flag):
        self.big_Entire_Frame.pack()
        another_frame = ctk.CTkFrame(self.big_Entire_Frame, width=1000, height=20)
        # if(self.Soldiers_previewed_flag):
        another_frame.pack(pady=5)
        headerLbl = ctk.CTkLabel(another_frame, text="الإسم", font=('Arial', 16, 'bold'))
        headerLbl.place(relx=0.83, rely=0.5, anchor=ctk.CENTER)

        headerLbl = ctk.CTkLabel(another_frame, text="الرقم العسكري", font=('Arial', 16, 'bold'))
        headerLbl.place(relx=0.62, rely=0.5, anchor=ctk.CENTER)

        headerLbl = ctk.CTkLabel(another_frame, text='الرتبة', font=('Arial', 16, 'bold'))
        headerLbl.place(relx=0.4, rely=0.5, anchor=ctk.CENTER)

        headerLbl = ctk.CTkLabel(another_frame, text="تاريخ التسليم", font=('Arial', 16, 'bold'))
        headerLbl.place(relx=0.2, rely=0.5, anchor=ctk.CENTER)


        self.entries_frame = ctk.CTkFrame(self.big_Entire_Frame, width=1120)
        # if(self.Soldiers_previewed_flag):
        self.entries_frame.pack()

        allSoldiers = helpers.fetchSoldiers()
        if(allSoldiers):#) and self.Soldiers_previewed_flag):
            for i, soldier in enumerate(allSoldiers):
                self.Add_Soldier_To_Preview(soldier_data=soldier, entries_frame=self.entries_frame, num_entries=i)


        # self.Soldiers_previewed_flag
        
        return self.entries_frame, entire_preview_frame
    

    # def UpdatePreview(self):
    #     allSoldiers = helpers.fetchSoldiers()
    #     if(allSoldiers and self.Soldiers_previewed_flag):
    #         for i, soldier in enumerate(allSoldiers):
    #             self.Add_Soldier_To_Preview(soldier_data=soldier, entries_frame=entries_frame, num_entries=i)



    def Add_Soldier_To_Preview(self, soldier_data, entries_frame, num_entries: int):
        print(soldier_data)

        new_entry_frame = ctk.CTkFrame(entries_frame, width = 1000, height=30, fg_color=ENTRY_FG_COLOR)
        new_entry_frame.pack(pady=2)

        newEntryLabel = ctk.CTkLabel(new_entry_frame, text=soldier_data['Name'], font=('Arial', 16), width=30 , fg_color=FG_COLOR, text_color=TEXT_COLOR)
        newEntryLabel.place(relx=0.83, rely=0.5, anchor=ctk.CENTER)

        newEntryLabel = ctk.CTkLabel(new_entry_frame, text=soldier_data['Soldier_ID'], font=('Arial', 16), width=30, fg_color=FG_COLOR, text_color=TEXT_COLOR)
        newEntryLabel.place(relx=0.62, rely=0.5, anchor=ctk.CENTER)

        newEntryLabel = ctk.CTkLabel(new_entry_frame, text=ArmyLevels[int(soldier_data["Level"])-1], font=('Arial', 16), width=30, fg_color=FG_COLOR, text_color=TEXT_COLOR)
        newEntryLabel.place(relx=0.4, rely=0.5, anchor=ctk.CENTER)

        newEntryLabel = ctk.CTkLabel(new_entry_frame, text=soldier_data['Retiring_Date'], font=('Arial', 16), width=30, fg_color=FG_COLOR, text_color=TEXT_COLOR)
        newEntryLabel.place(relx=0.2, rely=0.5, anchor=ctk.CENTER)

        #dumFrame = ctk.CTkFrame(new_entry_frame, width=50, height=20)
        #dumFrame.grid(row=num_entries, column=0, sticky='w', padx=0)
        DelButton = ctk.CTkButton(new_entry_frame, text='إزالة', font=('Arial', 16), width=30, fg_color='red', command=lambda frame=new_entry_frame: self.Remove_Soldier_From_Preview(soldier_data['Soldier_ID'], frame))
        DelButton.place(relx=0.1, rely=0.5, anchor=ctk.CENTER)
        self.array_of_entry_frames.append(new_entry_frame)


    def displayError(self, ErrType):
        self.errors_Lbl.configure(text=ErrType)
        return


    def Remove_Soldier_From_Preview(self, Soldier_ID, frame_to_be_destroyed):
        helpers.DeleteSoldier(Soldier_ID=Soldier_ID)
        frame_to_be_destroyed.destroy()
        self.return_button_state = True if (helpers.fetchSoldiers()) else False
        self.Back_to_mm_button.configure(state='normal' if self.return_button_state else "disabled", fg_color='#8576FF' if self.return_button_state else '#074173')
        return



        
    def __init__(self):
        
        self.root = None
        self.errors_Lbl = None
        #self.Soldiers_previewed_flag = True if helpers.fetchSoldiers() else False
        self.number_Of_Soldiers = len(helpers.fetchSoldiers()) if (helpers.fetchSoldiers()) else 0
        self.preview_frame = None
        self.destroyed = False
        self.big_Entire_Frame = None
        self.array_of_entry_frames = []
        self.return_button_state = True if (helpers.fetchSoldiers()) else False
        

                
        

    def BackToMainMenu(self):
        self.destroyed = True
        if(self.destroyed):
            self.root.destroy()
            return
        
        
        # print('\n\n\nHEREERERE\n\n\n')
        
        # print(self)
        # print('\n\n\n\n\n\n')
        # mm = MainMenu()



    def renderEntryPage(self):
        
        self.root = ctk.CTk(fg_color=BG_COLOR)

        #self.Soldiers_previewed_flag = True if helpers.fetchSoldiers() and len(helpers.fetchSoldiers()) > 0 else False
        self.root.title("Secretary PDF-Generator")
        self.root.geometry("1200x600")  # Set window size

        label = ctk.CTkLabel(self.root, text="أدخل بيانات العساكر", font=('Arial', 26), fg_color=FG_COLOR, text_color=TEXT_COLOR)
        label.pack()


        mainframe = ctk.CTkFrame(self.root, width=800, height=400, fg_color= FG_COLOR)
        mainframe.pack(anchor='center', pady=20)
        # mainframe.grid_propagate(False)

        # some labels

        # label.grid_rowconfigure(1, weight=2)


        label = ctk.CTkLabel(mainframe, text="الإسم", font=('Arial', 20, 'bold'), fg_color=FG_COLOR, text_color=TEXT_COLOR)
        label.grid(row= 1, column=3, pady=10)


        label = ctk.CTkLabel(mainframe, text="الرقم العسكري", font=('Arial', 20, 'bold'), fg_color=FG_COLOR, text_color=TEXT_COLOR)
        label.grid(row= 1, column=2, pady=10)

        label = ctk.CTkLabel(mainframe, text="الرتبة", font=('Arial', 20, 'bold'), fg_color=FG_COLOR, text_color=TEXT_COLOR)
        label.grid(row= 1, column=1, pady=10)


        label = ctk.CTkLabel(mainframe, text="تاريخ التسليم", font=('Arial', 20, 'bold'), fg_color=FG_COLOR, text_color=TEXT_COLOR)
        label.grid(row= 1, column=0, pady=10)


        Name_textbox = ctk.CTkEntry(mainframe, font=("Arial", 20), width=200, justify='right', fg_color=FG_COLOR, text_color=TEXT_COLOR)
        Name_textbox.grid(row=2, column=3, pady=10, padx=20)


        Soldier_ID_textbox = ctk.CTkEntry(mainframe, font=("Arial", 20), width=200, justify='right', fg_color=FG_COLOR, text_color=TEXT_COLOR)
        Soldier_ID_textbox.grid(row=2, column=2, pady=10, padx=20)

        Level_DropDown = ctk.CTkComboBox(mainframe, font=("Arial", 20), width=200, values=['عسكري', 'رقيب', 'رقيب أول', 'مساعد', 'مساعد أول', 'ملازم', 'ملازم أول', 'نقيب', 'رائد', 'مقدم', 'عقيد', 'عميد', 'لواء', 'فريق', 'فريق أول', 'مشير'], justify='right', state='readonly')
        Level_DropDown.set("عسكري")
        Level_DropDown.grid(row=2, column=1)


        retiring_date_frame = ctk.CTkFrame(mainframe, width=300, height=100, fg_color=FG_COLOR)
        retiring_date_frame.grid(row=2, column=0, padx=10, pady=20)

        Retiring_Date_day = ctk.CTkEntry(retiring_date_frame, font=("Arial", 15), width=100, placeholder_text='اليوم', justify='right', fg_color=FG_COLOR, text_color=TEXT_COLOR)
        Retiring_Date_day.grid(row=0, column=2, padx=5)

        Retiring_Date_month = ctk.CTkEntry(retiring_date_frame, font=("Arial", 15), width=100, placeholder_text='الشهر', justify='right', fg_color=FG_COLOR, text_color=TEXT_COLOR)
        Retiring_Date_month.grid(row=0, column=1, padx=5)

        Retiring_Date_year = ctk.CTkEntry(retiring_date_frame, font=("Arial", 15), width=100, placeholder_text='السنة', justify='right', fg_color=FG_COLOR, text_color=TEXT_COLOR)
        Retiring_Date_year.grid(row=0, column=0, padx=5)

        submit_button = ctk.CTkButton(mainframe, text="إدخال", font=('Arial', 15, 'bold'), command=lambda: self.submit_text(Name_textbox, Soldier_ID_textbox, Level_DropDown, Retiring_Date_year, Retiring_Date_month, Retiring_Date_day), fg_color=BUTTON_COLOR)
        submit_button.grid(row=3, column=1, pady=20)


        self.Back_to_mm_button = ctk.CTkButton(self.root, text="الرجوع إلى القائمة", font=('Arial', 15, 'bold'), command=lambda: self.BackToMainMenu(), state='normal' if self.return_button_state else 'disabled', fg_color=BUTTON_COLOR if self.return_button_state else '#074173')
        self.Back_to_mm_button.place(relx = 0.1, rely=0.9)
        



        self.errors_Lbl = ctk.CTkLabel(self.root, font=('Arial', 20, 'bold'), text_color='red', text='')
        self.errors_Lbl.place(relx=0.5, rely=0.9, anchor=ctk.CENTER)

        # self.root.bind('enter', command=lambda: self.submit_text(Name_textbox, Soldier_ID_textbox, Level_DropDown, Retiring_Date_year, Retiring_Date_month, Retiring_Date_day))

        self.Soldiers_Preview_show()

        self.root.bind("<Control-q>", lambda x: self.quit())
        self.root.bind("<Configure>", lambda x: self.resizeAll())

        self.root.bind("<Control-Enter>", lambda x: self.submit_text(Name_textbox, Soldier_ID_textbox, Level_DropDown, Retiring_Date_year, Retiring_Date_month, Retiring_Date_day))

        self.root.mainloop()

    def resizeAll(self):
        self.big_Entire_Frame.configure(height=self.root.winfo_height()/3)
    
    def quit(self):
        self.root.destroy()

