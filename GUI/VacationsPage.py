import customtkinter as ctk
import re
from datetime import date
from enums import EntryError, EntryErrorCode, ArmyLevels
# from MainMenu import MainMenu
import helpers




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
        if(len(re.split(' ',text)) < 3):
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





    def Soldiers_Preview_show(self):
        #self.Soldiers_previewed_flag = True if helpers.fetchSoldiers() else False
        entire_preview_frame = ctk.CTkScrollableFrame(self.root, label_text="Preview", width=1120)
        self.big_Entire_Frame = entire_preview_frame
        # if(self.Soldiers_previewed_flag):
        self.big_Entire_Frame.pack()
        another_frame = ctk.CTkFrame(self.big_Entire_Frame, width=1120)
        # if(self.Soldiers_previewed_flag):
        another_frame.pack()
        headerLbl = ctk.CTkLabel(another_frame, text="الإسم", font=('Arial', 16, 'bold'))
        headerLbl.grid(row=0, column=3, sticky='e', padx=1120/12)

        headerLbl = ctk.CTkLabel(another_frame, text="الرقم العسكري", font=('Arial', 16, 'bold'))
        headerLbl.grid(row=0, column=2, padx=1120/12)

        headerLbl = ctk.CTkLabel(another_frame, text='الرتبة', font=('Arial', 16, 'bold'))
        headerLbl.grid(row=0, column=1, padx=1120/12)

        headerLbl = ctk.CTkLabel(another_frame, text="تاريخ التسليم", font=('Arial', 16, 'bold'))
        headerLbl.grid(row=0, column=0, sticky='w', padx=1120/12)


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

        new_entry_frame = ctk.CTkFrame(entries_frame, width = 1120, height=30)
        new_entry_frame.pack()

        newEntryLabel = ctk.CTkLabel(new_entry_frame, text=soldier_data['Name'], font=('Arial', 14), width=30)
        newEntryLabel.grid(row=num_entries, column=4, sticky='e', padx=1120/12)

        newEntryLabel = ctk.CTkLabel(new_entry_frame, text=soldier_data['Soldier_ID'], font=('Arial', 14), width=30)
        newEntryLabel.grid(row=num_entries, column=3, padx=1120/12, sticky='e')

        newEntryLabel = ctk.CTkLabel(new_entry_frame, text=ArmyLevels[int(soldier_data["Level"])-1], font=('Arial', 14), width=30)
        newEntryLabel.grid(row=num_entries, column=2, padx=1120/12, sticky='e')

        newEntryLabel = ctk.CTkLabel(new_entry_frame, text=soldier_data['Retiring_Date'], font=('Arial', 14), width=30)
        newEntryLabel.grid(row=num_entries, column=1, sticky='e', padx=1120/12)

        dumFrame = ctk.CTkFrame(new_entry_frame, width=50, height=20)
        dumFrame.grid(row=num_entries, column=0, sticky='w', padx=0)
        DelButton = ctk.CTkButton(dumFrame, text='إزالة', font=('Arial', 14), width=30, fg_color='red', command=lambda frame=new_entry_frame: self.Remove_Soldier_From_Preview(soldier_data['Soldier_ID'], frame))
        DelButton.place(relx=0.5, rely=0.5, anchor='center')
        self.array_of_entry_frames.append(new_entry_frame)


    def displayError(self, ErrType):
        self.errors_Lbl.configure(text=ErrType)
        return


    def Remove_Soldier_From_Preview(self, Soldier_ID, frame_to_be_destroyed):
        helpers.DeleteSoldier(Soldier_ID=Soldier_ID)
        frame_to_be_destroyed.destroy()
        return



        
    def __init__(self):
        
        self.root = None
        self.errors_Lbl = None
        self.number_Of_Soldiers = len(helpers.fetchSoldiers()) if (helpers.fetchSoldiers()) else 0
        self.preview_frame = None
        self.destroyed = False
        self.big_Entire_Frame = None
        self.array_of_entry_frames = []
        self.renderEntryPage()
    

    def BackToMainMenu(self):
        self.destroyed = True
        if(self.destroyed):
            self.root.destroy()
            return
        
        
        # print('\n\n\nHEREERERE\n\n\n')
        
        # print(self)
        # print('\n\n\n\n\n\n')
        # mm = MainMenu()


    def ChangePlaceHoldersWithComboBox(self, event):
        self.Level_textbox.configure(text=helpers.getSoldierLevelFromID(helpers.getSoldierIDFromName(self.Name_ComboBox.get())))
        self.Soldier_ID_textbox.configure(text=helpers.getSoldierIDFromName(self.Name_ComboBox.get()))



    def renderEntryPage(self):
        
        self.root = ctk.CTk()

        #self.Soldiers_previewed_flag = True if helpers.fetchSoldiers() and len(helpers.fetchSoldiers()) > 0 else False
        self.root.title("Secretary PDF-Generator")
        self.root.geometry("1800x600")  # Set window size

        label = ctk.CTkLabel(self.root, text="أدخل بيانات العساكر", font=('Arial', 26))
        label.pack()


        mainframe = ctk.CTkFrame(self.root, width=800, height=400)
        mainframe.pack(anchor='center', pady=20)
        # mainframe.grid_propagate(False)

        # some labels

        # label.grid_rowconfigure(1, weight=2)


        label = ctk.CTkLabel(mainframe, text="الإسم", font=('Arial', 20, 'bold'))
        label.grid(row= 1, column=4, pady=10)


        label = ctk.CTkLabel(mainframe, text="الرقم العسكري", font=('Arial', 20, 'bold'))
        label.grid(row= 1, column=3, pady=10)

        label = ctk.CTkLabel(mainframe, text="الرتبة", font=('Arial', 20, 'bold'))
        label.grid(row= 1, column=2, pady=10)

        label = ctk.CTkLabel(mainframe, text="من", font=('Arial', 20, 'bold'))
        label.grid(row= 1, column=1, pady=10)

        label = ctk.CTkLabel(mainframe, text="إلى", font=('Arial', 20, 'bold'))
        label.grid(row= 1, column=0, pady=10)


############################################################################# WE MUST DISABLE EDITING THE COMBOBOX
        self.Name_ComboBox = ctk.CTkComboBox(mainframe, font=("Arial", 20), width=200, justify='right', values=helpers.getNamesFromDB(), command=self.ChangePlaceHoldersWithComboBox)
        self.Name_ComboBox.grid(row=2, column=4, pady=10, padx=20)

##################################################################################################################
        
        self.Soldier_ID_textbox = ctk.CTkLabel(mainframe, font=("Arial", 20), width=200, justify='right', text=helpers.getSoldierIDFromName(Name_ComboBox=self.Name_ComboBox.get()))
        self.Soldier_ID_textbox.grid(row=2, column=3, pady=10, padx=20)

        self.Level_textbox = ctk.CTkLabel(mainframe, font=("Arial", 20), width=200, justify='right', text=helpers.getSoldierLevelFromID(Soldier_ID=self.Soldier_ID_textbox.cget('text')))
        self.Level_textbox.grid(row=2, column=2, pady=10, padx=20)


        From_date_frame = ctk.CTkFrame(mainframe, width=300, height=100)
        From_date_frame.grid(row=2, column=1, padx=10, pady=20)

        From_Date_day = ctk.CTkEntry(From_date_frame, font=("Arial", 15), width=40, placeholder_text='اليوم', justify='right')
        From_Date_day.grid(row=0, column=2, padx=5)

        From_Date_month = ctk.CTkEntry(From_date_frame, font=("Arial", 15), width=40, placeholder_text='الشهر', justify='right')
        From_Date_month.grid(row=0, column=1, padx=5)

        From_Date_year = ctk.CTkEntry(From_date_frame, font=("Arial", 15), width=70, placeholder_text='السنة', justify='right')
        From_Date_year.grid(row=0, column=0, padx=5)

        To_date_frame = ctk.CTkFrame(mainframe, width=300, height=100)
        To_date_frame.grid(row=2, column=0, padx=10, pady=20)


        to_Date_day = ctk.CTkEntry(To_date_frame, font=("Arial", 15), width=40, placeholder_text='اليوم', justify='right')
        to_Date_day.grid(row=0, column=2, padx=5)

        to_Date_month = ctk.CTkEntry(To_date_frame, font=("Arial", 15), width=40, placeholder_text='الشهر', justify='right')
        to_Date_month.grid(row=0, column=1, padx=5)

        to_Date_year = ctk.CTkEntry(To_date_frame, font=("Arial", 15), width=70, placeholder_text='السنة', justify='right')
        to_Date_year.grid(row=0, column=0, padx=5)

        Back_to_mm_button = ctk.CTkButton(self.root, text="الرجوع إلى القائمة", font=('Arial', 15, 'bold'), command=lambda: self.BackToMainMenu())
        Back_to_mm_button.place(relx = 0.1, rely=0.9)
        



        self.errors_Lbl = ctk.CTkLabel(self.root, font=('Arial', 20, 'bold'), text_color='red', text='')
        self.errors_Lbl.place(relx=0.5, rely=0.9, anchor=ctk.CENTER)

        # self.root.bind('enter', command=lambda: self.submit_text(Name_textbox, Soldier_ID_textbox, Level_DropDown, Retiring_Date_year, Retiring_Date_month, Retiring_Date_day))

        self.Soldiers_Preview_show()

        self.root.mainloop()

    









def ShowVacationHistory():
    pass


def AddVacation():
    pass

def RemoveVacation():
    pass



def RefreshVacations_And_PushToHistory():
    pass


VacationsPage()