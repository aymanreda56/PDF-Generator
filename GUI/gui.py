import customtkinter as ctk
import re
from datetime import date
from enums import EntryError, EntryErrorCode
Soldiers_previewed_flag = False

number_Of_Soldiers = 0
preview_frame = None



def validate_date(year, month, day):
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



def submit_text(Namebox, IDbox, Yearbox, Monthbox, Daybox):
    global number_Of_Soldiers
    global Soldiers_previewed_flag
    global preview_frame

    
    #making a date object from the date textboxes
    (year, month, day) = Yearbox.get(), Monthbox.get(), Daybox.get()
    try:
        validate_date(year=year, month=month, day=day)
    except EntryError as e:
        displayError(e)
        return
    retiring_date_string = date(year=year, month=month, day= day).isoformat()
    
    soldierdata = {'Name':Namebox.get(), 'Soldier_ID': IDbox.get(), 'Retiring_Date': retiring_date_string}
    
    if(not Soldiers_previewed_flag):
        preview_frame = Soldiers_Preview_show()

    
    Add_Soldier_To_Preview(soldier_data= soldierdata, preview_frame= preview_frame, num_entries=number_Of_Soldiers)
    number_Of_Soldiers += 1



def reverse_arabic_text(arabicText):
    '''
        this function just takes an arabic sentence, splits it by spaces, then reverses each word.
        this is because tkinter does not support RTL rendering of arabic text.
    '''
    tokens = re.split(r' ',arabicText)
    tokens.reverse()
    # print(tokens)
    return ' '.join(tokens)




def Soldiers_Preview_show():
    preview_frame = ctk.CTkScrollableFrame(root, label_text="Preview", width=root.winfo_width() - 80)
    preview_frame.pack()
    another_frame = ctk.CTkFrame(preview_frame, width=root.winfo_width() - 80)
    another_frame.pack()
    headerLbl = ctk.CTkLabel(another_frame, text="الإسم", font=('Arial', 16, 'bold'))
    headerLbl.grid(row=0, column=2, sticky='e', padx=root.winfo_width()/12)

    headerLbl = ctk.CTkLabel(another_frame, text="الرقم العسكري", font=('Arial', 16, 'bold'))
    headerLbl.grid(row=0, column=1, padx=root.winfo_width()/12)

    headerLbl = ctk.CTkLabel(another_frame, text="تاريخ التسليم", font=('Arial', 16, 'bold'))
    headerLbl.grid(row=0, column=0, sticky='w', padx=root.winfo_width()/12)


    entries_frame = ctk.CTkFrame(preview_frame, width=root.winfo_width() - 80)
    entries_frame.pack()

    global Soldiers_previewed_flag
    Soldiers_previewed_flag = True
    return entries_frame




def Add_Soldier_To_Preview(soldier_data, preview_frame, num_entries: int):
    newEntryLabel = ctk.CTkLabel(preview_frame, text=soldier_data['Name'], font=('Arial', 14))
    newEntryLabel.grid(row=num_entries, column=2, sticky='e', padx=root.winfo_width()/12)

    newEntryLabel = ctk.CTkLabel(preview_frame, text=soldier_data['Soldier_ID'], font=('Arial', 14))
    newEntryLabel.grid(row=num_entries, column=1, padx=root.winfo_width()/12)

    newEntryLabel = ctk.CTkLabel(preview_frame, text=soldier_data['Retiring_Date'], font=('Arial', 14))
    newEntryLabel.grid(row=num_entries, column=0, sticky='w', padx=root.winfo_width()/12)



def displayError(ErrType):
    errors_Lbl.configure(text=ErrType)
    return










    

root = ctk.CTk()
root.title("Secretary PDF-Generator")
root.geometry("1000x600")  # Set window size

label = ctk.CTkLabel(root, text="أدخل بيانات العساكر", font=('Arial', 26))
label.pack()


mainframe = ctk.CTkFrame(root, width=800, height=400)
mainframe.pack(anchor='center', pady=20)
# mainframe.grid_propagate(False)

# some labels

# label.grid_rowconfigure(1, weight=2)


label = ctk.CTkLabel(mainframe, text="الإسم", font=('Arial', 20, 'bold'))
label.grid(row= 1, column=2, pady=10)


label = ctk.CTkLabel(mainframe, text="الرقم العسكري", font=('Arial', 20, 'bold'))
label.grid(row= 1, column=1, pady=10)


label = ctk.CTkLabel(mainframe, text="تاريخ التسليم", font=('Arial', 20, 'bold'))
label.grid(row= 1, column=0, pady=10)


Name_textbox = ctk.CTkEntry(mainframe, font=("Arial", 20), width=200)
Name_textbox.grid(row=2, column=2, pady=10, padx=20)


Soldier_ID_textbox = ctk.CTkEntry(mainframe, font=("Arial", 20), width=200)
Soldier_ID_textbox.grid(row=2, column=1, pady=10, padx=20)


retiring_date_frame = ctk.CTkFrame(mainframe, width=300, height=100)
retiring_date_frame.grid(row=2, column=0, padx=10, pady=20)

Retiring_Date_day = ctk.CTkEntry(retiring_date_frame, font=("Arial", 15), width=100, placeholder_text='اليوم')
Retiring_Date_day.grid(row=0, column=2, padx=5)

Retiring_Date_month = ctk.CTkEntry(retiring_date_frame, font=("Arial", 15), width=100, placeholder_text='الشهر')
Retiring_Date_month.grid(row=0, column=1, padx=5)

Retiring_Date_year = ctk.CTkEntry(retiring_date_frame, font=("Arial", 15), width=100, placeholder_text='السنة')
Retiring_Date_year.grid(row=0, column=0, padx=5)

submit_button = ctk.CTkButton(mainframe, text="إدخال", command=lambda: submit_text(Name_textbox, Soldier_ID_textbox, Retiring_Date_year, Retiring_Date_month, Retiring_Date_day))
submit_button.grid(row=3, column=1, pady=20)



errors_Lbl = ctk.CTkLabel(root, font=('Arial', 20, 'bold'), text_color='red', text='')
errors_Lbl.place(relx=0.5, rely=0.9, anchor=ctk.CENTER)




root.mainloop()