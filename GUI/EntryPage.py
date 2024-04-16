import customtkinter as ctk
import re
from datetime import date
from enums import EntryError, EntryErrorCode, ArmyLevels
import sqlite3
from MainMenu import MainMenu







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
        (year, month, day) = Yearbox.get(), Monthbox.get(), Daybox.get()
        try:
            self.validate_date(year=year, month=month, day=day)
        except EntryError as e:
            self.displayError(e)
            return
        retiring_date_string = date(year=int(year), month=int(month), day= int(day)).isoformat()
        try:
            Soldier_ID_string = self.validate_ID(IDbox.get())
        except EntryError as e:
            self.displayError(e)
            return
        
        try:
            name = self.validate_name(Namebox.get())
        except EntryError as e:
            self.displayError(e)
            return
        
        soldierdata = {'Name':name, 'Soldier_ID': Soldier_ID_string, 'Level': str(ArmyLevels.index(Level_comboBox.get())+1),'Retiring_Date': retiring_date_string}
        
        if(not self.Soldiers_previewed_flag):
            self.preview_frame = self.Soldiers_Preview_show()

        
        self.AddNewSoldier(soldier_data=soldierdata)

        self.Add_Soldier_To_Preview(soldier_data= soldierdata, preview_frame= self.preview_frame, num_entries=self.number_Of_Soldiers)
        self.number_Of_Soldiers += 1

        self.errors_Lbl.configure(text='')




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
        self.preview_frame = ctk.CTkScrollableFrame(self.root, label_text="Preview", width=self.root.winfo_width() - 80)
        self.preview_frame.pack()
        another_frame = ctk.CTkFrame(self.preview_frame, width=self.root.winfo_width() - 80)
        another_frame.pack()
        headerLbl = ctk.CTkLabel(another_frame, text="الإسم", font=('Arial', 16, 'bold'))
        headerLbl.grid(row=0, column=3, sticky='e', padx=self.root.winfo_width()/12)

        headerLbl = ctk.CTkLabel(another_frame, text="الرقم العسكري", font=('Arial', 16, 'bold'))
        headerLbl.grid(row=0, column=2, padx=self.root.winfo_width()/12)

        headerLbl = ctk.CTkLabel(another_frame, text='الرتبة', font=('Arial', 16, 'bold'))
        headerLbl.grid(row=0, column=1, padx=self.root.winfo_width()/12)

        headerLbl = ctk.CTkLabel(another_frame, text="تاريخ التسليم", font=('Arial', 16, 'bold'))
        headerLbl.grid(row=0, column=0, sticky='w', padx=self.root.winfo_width()/12)


        entries_frame = ctk.CTkFrame(self.preview_frame, width=self.root.winfo_width() - 80)
        entries_frame.pack()

        allSoldiers = self.fetchSoldiers()
        if(allSoldiers):
            for i, soldier in enumerate(allSoldiers):
                self.Add_Soldier_To_Preview(soldier_data=soldier, preview_frame=entries_frame, num_entries=i)

        # self.Soldiers_previewed_flag
        self.Soldiers_previewed_flag = True
        return entries_frame
    



    def Add_Soldier_To_Preview(self, soldier_data, preview_frame, num_entries: int):
        newEntryLabel = ctk.CTkLabel(preview_frame, text=soldier_data['Name'], font=('Arial', 14))
        newEntryLabel.grid(row=num_entries, column=3, sticky='e', padx=self.root.winfo_width()/12)

        newEntryLabel = ctk.CTkLabel(preview_frame, text=soldier_data['Soldier_ID'], font=('Arial', 14))
        newEntryLabel.grid(row=num_entries, column=2, padx=self.root.winfo_width()/12)

        print('\n\n\n')
        print(soldier_data["Level"])
        print('\n\n\n')
        newEntryLabel = ctk.CTkLabel(preview_frame, text=ArmyLevels[int(soldier_data["Level"])-1], font=('Arial', 14))
        newEntryLabel.grid(row=num_entries, column=1, padx=self.root.winfo_width()/12)

        newEntryLabel = ctk.CTkLabel(preview_frame, text=soldier_data['Retiring_Date'], font=('Arial', 14))
        newEntryLabel.grid(row=num_entries, column=0, sticky='w', padx=self.root.winfo_width()/12)



    def displayError(self, ErrType):
        self.errors_Lbl.configure(text=ErrType)
        return





        
    def __init__(self):
        
        self.root = None
        self.errors_Lbl = None
        self.Soldiers_previewed_flag = False
        self.number_Of_Soldiers = (not self.fetchSoldiers() ==False) and len(self.fetchSoldiers())
        self.preview_frame = None

        self.root = ctk.CTk()
        self.root.title("Secretary PDF-Generator")
        self.root.geometry("1200x600")  # Set window size

        label = ctk.CTkLabel(self.root, text="أدخل بيانات العساكر", font=('Arial', 26))
        label.pack()


        mainframe = ctk.CTkFrame(self.root, width=800, height=400)
        mainframe.pack(anchor='center', pady=20)
        # mainframe.grid_propagate(False)

        # some labels

        # label.grid_rowconfigure(1, weight=2)


        label = ctk.CTkLabel(mainframe, text="الإسم", font=('Arial', 20, 'bold'))
        label.grid(row= 1, column=3, pady=10)


        label = ctk.CTkLabel(mainframe, text="الرقم العسكري", font=('Arial', 20, 'bold'))
        label.grid(row= 1, column=2, pady=10)

        label = ctk.CTkLabel(mainframe, text="الرتبة", font=('Arial', 20, 'bold'))
        label.grid(row= 1, column=1, pady=10)


        label = ctk.CTkLabel(mainframe, text="تاريخ التسليم", font=('Arial', 20, 'bold'))
        label.grid(row= 1, column=0, pady=10)


        Name_textbox = ctk.CTkEntry(mainframe, font=("Arial", 20), width=200, justify='right')
        Name_textbox.grid(row=2, column=3, pady=10, padx=20)


        Soldier_ID_textbox = ctk.CTkEntry(mainframe, font=("Arial", 20), width=200, justify='right')
        Soldier_ID_textbox.grid(row=2, column=2, pady=10, padx=20)

############################################################################# WE MUST DISABLE EDITING THE COMBOBOX
        Level_DropDown = ctk.CTkComboBox(mainframe, font=("Arial", 20), width=200, values=['عسكري', 'رقيب', 'رقيب أول', 'مساعد', 'مساعد أول', 'ملازم', 'ملازم أول', 'نقيب', 'رائد', 'مقدم', 'عقيد', 'عميد', 'لواء', 'فريق', 'فريق أول', 'مشير'], justify='right')
##################################################################################################################
        Level_DropDown.set("عسكري")
        Level_DropDown.grid(row=2, column=1)


        retiring_date_frame = ctk.CTkFrame(mainframe, width=300, height=100)
        retiring_date_frame.grid(row=2, column=0, padx=10, pady=20)

        Retiring_Date_day = ctk.CTkEntry(retiring_date_frame, font=("Arial", 15), width=100, placeholder_text='اليوم', justify='right')
        Retiring_Date_day.grid(row=0, column=2, padx=5)

        Retiring_Date_month = ctk.CTkEntry(retiring_date_frame, font=("Arial", 15), width=100, placeholder_text='الشهر', justify='right')
        Retiring_Date_month.grid(row=0, column=1, padx=5)

        Retiring_Date_year = ctk.CTkEntry(retiring_date_frame, font=("Arial", 15), width=100, placeholder_text='السنة', justify='right')
        Retiring_Date_year.grid(row=0, column=0, padx=5)

        submit_button = ctk.CTkButton(mainframe, text="إدخال", command=lambda: self.submit_text(Name_textbox, Soldier_ID_textbox, Level_DropDown, Retiring_Date_year, Retiring_Date_month, Retiring_Date_day))
        submit_button.grid(row=3, column=1, pady=20)


        Back_to_mm_button = ctk.CTkButton(self.root, text="الرجوع إلى القائمة", command=lambda: self.renderMainMenu())
        Back_to_mm_button.place(relx = 0.1, rely=0.9)
        



        self.errors_Lbl = ctk.CTkLabel(self.root, font=('Arial', 20, 'bold'), text_color='red', text='')
        self.errors_Lbl.place(relx=0.5, rely=0.9, anchor=ctk.CENTER)

        # self.root.bind('enter', command=lambda: self.submit_text(Name_textbox, Soldier_ID_textbox, Level_DropDown, Retiring_Date_year, Retiring_Date_month, Retiring_Date_day))
        self.root.mainloop()



    def renderMainMenu(self):
        self.root.withdraw()
        print('\n\n\nHEREERERE\n\n\n')
        print(self)
        print('\n\n\n\n\n\n')
        mm = MainMenu()
        




    def AddNewSoldier(self, soldier_data):
        try:
            if(not self.CheckIfSoldierExists(soldier_data=soldier_data, Table_Name='Force')):
                raise EntryError(EntryErrorCode.SOLDIER_ALREADY_EXISTING_ERR)
        except EntryError as e:
            self.displayError(ErrType=e)
            return False
        connection = sqlite3.connect('../db/Soldiers.db')
        cursor = connection.cursor()
        # print('\n\n\n\n')
        # print(soldier_data.values())
        # print('\n\n\n\n')
        insertion_query = ', '.join([f'"{field}"' if type(field) == str else f'{field}' for field in list(soldier_data.values())])
        insertion_query = '(' + insertion_query + ')'
        sql_query_entry = f'''INSERT INTO "Force" VALUES {insertion_query}'''
        print(sql_query_entry)
        
        try:
            result = cursor.execute(sql_query_entry)
            connection.commit()
        except sqlite3.Error as e:
            print(e)

        finally:
            cursor.close()



    def CheckIfSoldierExists(self, soldier_data, Table_Name):
        try:
            connection = sqlite3.connect('../db/Soldiers.db')
            cursor = connection.cursor()
            Checking_query = f'SELECT * FROM {Table_Name} WHERE Soldier_ID = {soldier_data["Soldier_ID"]}'
            result = cursor.execute(Checking_query).fetchall()
            print('\n\n\n\n')
            print(result)
            print('\n\n\n\n')
            if(result == []):
                return False
                #raise EntryError(EntryErrorCode.SOLDIER_ALREADY_EXISTING_ERR)
            else:
                return True

        except sqlite3.Error as e:
            print(e)
        finally:
            cursor.close()

    def fetchSoldiers(self):
        try:
            connection = sqlite3.connect('../db/Soldiers.db')
            cursor = connection.cursor()
            Checking_query = f'SELECT * FROM Force'
            result = cursor.execute(Checking_query).fetchall()
            print('\n\n\n\n')
            print(result)
            print('\n\n\n\n')

            soldiers_dicts = []
            for tupl in result:
                new_dict = {}
                new_dict['Name'], new_dict['Soldier_ID'], new_dict['Level'], new_dict['Retiring_Date'] = tupl
                soldiers_dicts.append(new_dict)

            if(result == []):
                return False
            else:
                return soldiers_dicts

        except sqlite3.Error as e:
            print(e)
        finally:
            cursor.close()