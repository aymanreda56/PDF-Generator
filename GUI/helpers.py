import sqlite3
from enums import EntryError, EntryErrorCode, ArmyLevels
from datetime import date
import os





with open('db_path.txt', 'r') as f:
    DB_FOLDER_PATH = os.path.abspath(f.read())
    DB_FILE_NAME = 'Soldiers.db'
    DB_PATH = os.path.join(DB_FOLDER_PATH, DB_FILE_NAME)
    DB_PHOTOS = os.path.join(DB_FOLDER_PATH, 'Soldier_Photos')
   

   






def getAbsenceSQL(Level_Index):
    try:
        RefreshVacations()
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()
        Checking_query = f'SELECT Vacations.Soldier_ID, Vacations.Name, Vacations.From_Date, Vacations.To_Date, Vacations.State, Vacations.Summoned FROM Force INNER JOIN Vacations ON Force.Soldier_ID = Vacations.Soldier_ID AND Force.Level {Level_Index};'
        result = cursor.execute(Checking_query).fetchall()
        
        returnedResult = []
        for tup in result:
            if date.fromisoformat(tup[2]) <= date.today() and date.fromisoformat(tup[3]) > date.today():
                returnedResult.append(tup)

        return returnedResult

    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()


def getAbsentOfficers():
    result = getAbsenceSQL('> 5')
    return result


def getAbsentSoldiers():
    result = getAbsenceSQL('= "1"')
    return result

def getAbsentCaps():
    result = getAbsenceSQL('> 1 and Force.Level < 6')
    return result






def AddNewSoldier(soldier_data):
        try:
            CheckIfSoldierExists(soldier_data=soldier_data, Table_Name='Force')
        except EntryError as e:
            raise EntryError(EntryErrorCode.SOLDIER_ALREADY_EXISTING_ERR)
        
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()
        # print('\n\n\n\n')
        # print(soldier_data.values())
        # print('\n\n\n\n')
        insertion_query = ', '.join([f'"{field}"' if type(field) == str else f'{field}' for field in list(soldier_data.values())])
        insertion_query = '(' + insertion_query + ')'
        sql_query_entry = f'''INSERT INTO Force VALUES (?, ?, ?, ?)'''
        try:
            result = cursor.execute(sql_query_entry, (soldier_data['Soldier_ID'], soldier_data['Name'], soldier_data['Level'], soldier_data['Retiring_Date']))
            connection.commit()
        except sqlite3.Error as e:
            print(e)

        finally:
            cursor.close()




def DeleteSoldier(Soldier_ID):
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()
        Deleting_query = f'DELETE FROM Force WHERE Soldier_ID = ?'
        result = cursor.execute(Deleting_query, (Soldier_ID,))
        connection.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()


def CheckIfSoldierExists(soldier_data, Table_Name):
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()
        Checking_query = f'SELECT * FROM {Table_Name} WHERE Soldier_ID = "{soldier_data["Soldier_ID"]}"'
        result = cursor.execute(Checking_query).fetchall()
        # print('\n\n\n\n RESULT OF DOUBLE')
        # print(result)
        # print('\n\n\n\n')
        if(result == []):
            return False
            #
        else:
            print(result)
            raise EntryError(EntryErrorCode.SOLDIER_ALREADY_EXISTING_ERR)

   
    
    except EntryError as e:
        raise EntryError(EntryErrorCode.SOLDIER_ALREADY_EXISTING_ERR)
    
    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()

def fetchSoldiers():
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()
        Checking_query = f'SELECT * FROM Force'
        result = cursor.execute(Checking_query).fetchall()
        print('\n\n\n\n')
        print(result)

        soldiers_dicts = []
        for tupl in result:
            new_dict = {}
            new_dict['Soldier_ID'], new_dict['Name'], new_dict['Level'], new_dict['Retiring_Date'] = tupl
            soldiers_dicts.append(new_dict)

        if(result == []):
            return False
        else:
            print(soldiers_dicts)
            print('\n\n\n\n')

            return soldiers_dicts

    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()



def getSoldiers():
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()
        Checking_query = f'SELECT * FROM Force WHERE Level = 1'
        result = cursor.execute(Checking_query).fetchall()

        if(result == []):
            return False
        else:
            return result[0]

    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()

def getNumSoldiers():
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()
        Checking_query = f'SELECT COUNT (*) FROM Force WHERE Level = 1'
        result = cursor.execute(Checking_query).fetchall()

        if(result == []):
            return 0
        else:
            return result[0][0]

    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()


def getOfficers():
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()
        Checking_query = f'SELECT * FROM Force WHERE Level > 5'
        result = cursor.execute(Checking_query).fetchall()

        if(result == []):
            return False
        else:
            return result[0]

    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()

def getNumOfficers():
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()
        Checking_query = f'SELECT COUNT (*) FROM Force WHERE Level > 5'
        result = cursor.execute(Checking_query).fetchall()

        if(result == []):
            return 0
        else:
            return result[0][0]

    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()

def getCaps():
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()
        Checking_query = f'SELECT * FROM Force WHERE Level > 1 AND Level < 5'
        result = cursor.execute(Checking_query).fetchall()

        if(result == []):
            return False
        else:
            return result[0]

    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()


def getNumCaps():
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()
        Checking_query = f'SELECT COUNT (*) FROM Force WHERE Level > 1 AND Level < 5'
        result = cursor.execute(Checking_query).fetchall()

        if(result == []):
            return 0
        else:
            return result[0][0]

    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()



def ArchiveVacation(Soldier_ID, Soldier_Name, From_Date, To_Date, state = '0', summoned = '0', active='1'):
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()
        Checking_query = f'INSERT INTO Vacations_History (Soldier_ID, Name, From_Date, To_Date, State, Summoned, Active) VALUES (?, ?, ?, ?, ?, ?, ?)'
        result = cursor.execute(Checking_query, (Soldier_ID, Soldier_Name, From_Date, To_Date, state, summoned, active))
        connection.commit()

    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()


def RefreshVacations():
    try:
        print('refreshed')
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()
        Checking_query = f'SELECT Soldier_ID, Name, From_Date, To_Date FROM Vacations'
        result = cursor.execute(Checking_query).fetchall()

        for tup in result:
            print(tup)
            if date.today() >= date.fromisoformat(tup[3]):
                ArchiveVacation(Soldier_ID=tup[0], Soldier_Name=tup[1], From_Date=tup[2], To_Date=tup[3], state='0', summoned='0', active='0')
                RemoveVacation(Soldier_ID=tup[0])
                print("removed")

    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()
    




def getLevelFromID(ID):
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()
        Checking_query = f'SELECT Level FROM Force WHERE Soldier_ID = ?'
        result = cursor.execute(Checking_query, (ID,)).fetchall()[0]
        
        if(result == []):
            return False
        else:
            return result[0]

    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()





def getAllDates(with_disabled: bool = False, only_extensions=None) -> list[str]:
    RefreshVacations()
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()
        if with_disabled:
            Checking_query = f'SELECT * FROM Vacations'
        else:
            Checking_query = f'SELECT * FROM Vacations WHERE State = 1'
        
        if(only_extensions):
            if with_disabled:
                Checking_query = f'SELECT * FROM Vacations WHERE Extended = ?'
            else:
                Checking_query = f'SELECT * FROM Vacations WHERE State = 1 AND Extended = ?'
            result = cursor.execute(Checking_query, (only_extensions,)).fetchall()
        else:
            result = cursor.execute(Checking_query).fetchall()
        print('\n\n\n\n')
        print(result)

        if(result == []):
            return []
        else:
            all_dates = [i[2] for i in result]
            return all_dates

    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()


def getActiveVacations(with_disabled: bool = False, only_extensions=None) -> list:
    RefreshVacations()
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()
        if with_disabled:
            Checking_query = f'SELECT * FROM Vacations'
        else:
            Checking_query = f'SELECT * FROM Vacations WHERE State = 1'

        if(only_extensions):
            if with_disabled:
                Checking_query = f'SELECT * FROM Vacations WHERE Extended = ?'
            else:
                Checking_query = f'SELECT * FROM Vacations WHERE State = 1 AND Extended = ?'
        
            result = cursor.execute(Checking_query, (only_extensions,)).fetchall()
        else:
            result = cursor.execute(Checking_query).fetchall()
        
        
        print('\n\n\n\n')
        print(result)

        if(result == []):
            return []
        else:
            return result

    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()





def UpdateVacationState(Soldier_ID, new_state):
    RefreshVacations()
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()

        update_query = 'UPDATE Vacations SET "State" = ? WHERE "Soldier_ID" = ?'
        result = cursor.execute(update_query, [new_state, Soldier_ID])

        connection.commit()
        
    except sqlite3.Error as e:
        print(e)
        return False
    finally:
        cursor.close()


def GetNameFromID(Soldier_ID):
    result=' '
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()
       
        query = f'SELECT Name FROM Force WHERE Soldier_ID = ?'
        result = cursor.execute(query, (Soldier_ID,)).fetchall()
    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()
        return result[0][0]


def ExtendVacation(Soldier_ID, new_to_date):
    RefreshVacations()
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()

        update_query = 'UPDATE Vacations SET "To_Date" = ?, "Extended" = 1 WHERE "Soldier_ID" = ?'
        result = cursor.execute(update_query, [new_to_date, Soldier_ID])

        connection.commit()


        from_date = getLastReturnFromID(Soldier_ID=Soldier_ID)
        Soldier_Name = GetNameFromID(Soldier_ID=Soldier_ID)
        ArchiveVacation(Soldier_ID=Soldier_ID, Soldier_Name=Soldier_Name, From_Date=from_date, To_Date=new_to_date, state='1', summoned=0, active=1)
        
    except sqlite3.Error as e:
        print(e)
        return False
    finally:
        cursor.close()


def GetToDateFromVacation(Soldier_ID):
    RefreshVacations()
    result = ['']
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()

        query = 'SELECT "To_Date" FROM Vacations WHERE "Soldier_ID" = ?'
        result = cursor.execute(query, (Soldier_ID,)).fetchall()
        
    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()
        return result[0][0]



def GetAllFromDatesOfExtensions():
    allVacations = getActiveVacations(with_disabled=True, only_extensions=1)
    allIDS = []
    for tup in allVacations:
        allIDS.append(tup[0])
    
    allExtensionFromDates = []
    for id in allIDS:
        allExtensionFromDates.append(GetExtensionFromDate(id))

    return allExtensionFromDates



def CheckStateOfVacation(Soldier_ID):
    RefreshVacations()
    try:
        result = None
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()

        select_query = 'SELECT State FROM Vacations WHERE "Soldier_ID" = ?'
        result = cursor.execute(select_query, (Soldier_ID,)).fetchall()[0]

        connection.commit()
        
    except sqlite3.Error as e:
        print(e)

    finally:
        cursor.close()
        return result



def AddVacation(Soldier_ID, FromDate, ToDate, State, Summoned, Extended:int=0):
    RefreshVacations()
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()

        search_query = "SELECT Name FROM Force WHERE Soldier_ID = ?"
        result = cursor.execute(search_query, [Soldier_ID]).fetchall()
        Soldier_Name = result[0][0]
        
    except sqlite3.Error as e:
        print(e)
        return False
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()

        insertion_query = '''INSERT INTO Vacations VALUES (?, ?, ?, ?, ?, ?, ?)'''
        cursor.execute(insertion_query, (Soldier_ID, Soldier_Name, FromDate, ToDate, State, Summoned, Extended))
        connection.commit()

        
        if date.today() >= date.fromisoformat(ToDate):
            isActive = '0'
        else:
            isActive = '1'
        ArchiveVacation(Soldier_ID=Soldier_ID, Soldier_Name=Soldier_Name, From_Date=FromDate, To_Date=ToDate, state='0', summoned=Summoned, active=isActive)

    except sqlite3.Error as e:
        print(e)
        return False
    finally:
        connection.close()
        RefreshVacations()


def GetExtensionFromDate(Soldier_ID):
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()

        search_query = "SELECT To_Date FROM Vacations_History WHERE Soldier_ID = ? AND State = 0"
        result = cursor.execute(search_query, (Soldier_ID,)).fetchall()
        


        if(result == []):
            return 'غير محسوب بعد'
        
        latest_date = date.fromisoformat('2000-01-01') #dummy very old date to compare with
        for res in result:
            vac_final_date = date.fromisoformat(res[0])
            
            if (vac_final_date > latest_date):
                latest_date = vac_final_date

        
        

        cursor.close()
        print('DEBUGGG\n')
        print(latest_date.isoformat())
        return latest_date.isoformat()

    except sqlite3.Error as e:
        print(e)
    
    finally:
        cursor.close()


def RemoveVacation(Soldier_ID, delete_from_history:bool = False):
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()

        search_query = "DELETE FROM Vacations WHERE Soldier_ID = ?"
        
        result = cursor.execute(search_query, (Soldier_ID,))

        if(delete_from_history):
            history_deletion_query = 'DELETE FROM Vacations_History WHERE Soldier_ID = ? AND To_Date = ?'
            result = cursor.execute(history_deletion_query, (Soldier_ID, getLastReturnFromID(Soldier_ID=Soldier_ID)))
            
        connection.commit()
    except sqlite3.Error as e:
        print(e)
        return False
    


def getSoldierIDFromName(Name_ComboBox)->str:
    allSoldiers = fetchSoldiers()
    for soldier in allSoldiers:
        if soldier['Name'] == Name_ComboBox:
            return soldier['Soldier_ID']
    return False


def getSoldierLevelFromID(Soldier_ID)->str:
    allSoldiers = fetchSoldiers()
    for soldier in allSoldiers:
        if soldier['Soldier_ID'] == Soldier_ID:
            return ArmyLevels[soldier['Level']-1]
    return False


def getNamesFromDB() -> list:
    allSoldiers = fetchSoldiers()
    SoldierNames = []
    for soldier in allSoldiers:
        SoldierNames.append(soldier['Name'])
    return SoldierNames



def getIDsFromDB() -> list:
    allSoldiers = fetchSoldiers()
    SoldierIDs = []
    for soldier in allSoldiers:
        SoldierIDs.append(soldier['Soldier_ID'])
    return SoldierIDs




def getLastReturnFromID(Soldier_ID:str) -> str:
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()

        search_query = "SELECT To_Date FROM Vacations_History WHERE Soldier_ID = ?"
        result = cursor.execute(search_query, (Soldier_ID,)).fetchall()
        


        if(result == []):
            return 'غير محسوب بعد'
        
        latest_date = date.fromisoformat('2000-01-01') #dummy very old date to compare with
        for res in result:
            vac_final_date = date.fromisoformat(res[0])
            
            if (vac_final_date > latest_date):
                latest_date = vac_final_date

        
        

        cursor.close()
        return latest_date.isoformat()

    except sqlite3.Error as e:
        print(e)
    
    finally:
        cursor.close()
        # return 'لم يحسب بعد'
    


def getServiceDays(last_vac_date:str)->int:
    try:
        delta_date = date.today() - date.fromisoformat(last_vac_date)
        return delta_date.days
    except:
        return 0


def getPresentSoldiers():
    result = []
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()

        query = 'SELECT * FROM Force WHERE NOT EXISTS ( SELECT Soldier_ID FROM Vacations WHERE Force.Soldier_ID = Vacations.Soldier_ID);'
        result = cursor.execute(query).fetchall()
        
    except sqlite3.Error as e:
        print(e)
    
    finally:
        cursor.close()
        return result
    




def CreateDB():
    try:
        # create connection to database 
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")

        cursor = connection.cursor()

        result = cursor.execute('''CREATE TABLE Force (
            "Soldier_ID"	TEXT NOT NULL UNIQUE,
            "Name"	TEXT NOT NULL,
            "Level"	INTEGER NOT NULL,
            "Retiring_Date"	TEXT,
            PRIMARY KEY("Soldier_ID")
        );''')

        result = cursor.execute('''CREATE TABLE "Vacations" (
            "Soldier_ID"	TEXT NOT NULL UNIQUE,
            "Name"	TEXT NOT NULL,
            "From_Date"	TEXT NOT NULL,
            "To_Date"	TEXT NOT NULL,
            "State"     INTEGER NOT NULL,
            "Summoned"  INTEGER NOT NULL,
            "Extended"  INTEGER,
            FOREIGN KEY("Soldier_ID")  REFERENCES Force ("Soldier_ID")  ON DELETE CASCADE
        );''')

        result = cursor.execute('''CREATE TABLE "Missions" (
        "Soldier_ID"	TEXT NOT NULL UNIQUE,
        "Name"	TEXT NOT NULL,
        "From_Date"	TEXT NOT NULL,
        "To_Date"	TEXT NOT NULL,
        "Place"	TEXT,
        FOREIGN KEY("Soldier_ID") REFERENCES Force ("Soldier_ID")  ON DELETE CASCADE
        )''')


        result = cursor.execute('''CREATE TABLE "Vacations_History" (
            "ID"	INTEGER,
            "Soldier_ID"	TEXT,
            "Name"	TEXT,
            "From_Date"	TEXT,
            "To_Date"	TEXT,
            "State"	INTEGER,
            "Summoned"	INTEGER,
            PRIMARY KEY("ID" AUTOINCREMENT)
        );''')

        result = cursor.execute('''CREATE TABLE "Accounts" (
            "name"	TEXT NOT NULL,
            "level"	TEXT NOT NULL,
            "hash"	TEXT NOT NULL UNIQUE,
            "is_admin"	TEXT NOT NULL,
            PRIMARY KEY("hash")
        );''')


        result = cursor.execute('''CREATE TABLE "Documents" (
            "Image_Path"	TEXT NOT NULL,
            "Name"	TEXT NOT NULL,
            "BirthDate"	TEXT NOT NULL,
            "Soldier_ID"	TEXT NOT NULL UNIQUE,
            "Mobile_Num"	TEXT NOT NULL,
            "Home_Address"	TEXT NOT NULL,
            "City"	TEXT NOT NULL,
            "Governorate"	TEXT NOT NULL,
            "Home_Number"	TEXT NOT NULL,
            "Retiring_Date"	TEXT NOT NULL,
            "Mothers_Mobile_Num"	TEXT NOT NULL,
            "Function_Inside_Dept"	TEXT NOT NULL,
            "Date_Of_Join"	TEXT NOT NULL,
            PRIMARY KEY("Soldier_ID")
        );''')


        connection.commit()


    except sqlite3.Error as e:
        print(e)

    finally:
        cursor.close()




############################################################## DOCUMENT SPECIFIC FUNCTIONS ########################################################
def insert_Document(image_path, name, birth_date, soldier_id, retiring_date, mobile_number, home_number, home_address, city, governorate, mothers_mob_number, function_inside_department, date_of_join):
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()

        insertion_query = '''INSERT INTO Documents (Image_Path, Name, BirthDate, Soldier_ID, Mobile_Num, Home_Address, City, Governorate, Home_Number, Retiring_Date, Mothers_Mobile_Num, Function_Inside_Dept, Date_Of_Join) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        cursor.execute(insertion_query, (image_path, name, birth_date, soldier_id, mobile_number, home_address, city, governorate, home_number, retiring_date, mothers_mob_number, function_inside_department, date_of_join))
        connection.commit()

    except sqlite3.Error as e:
        print(e)
        return False
    

def Edit_Document(image_path, name, birth_date, soldier_id, retiring_date, mobile_number, home_number, home_address, city, governorate, mothers_mob_number, function_inside_department, date_of_join):
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()

        insertion_query = '''UPDATE Documents SET Image_Path = ?, Name = ?, BirthDate = ?, Soldier_ID = ?, Mobile_Num = ?, Home_Address = ?, City = ?, Governorate = ?, Home_Number = ?, Retiring_Date = ?, Mothers_Mobile_Num = ?, Function_Inside_Dept = ?, Date_Of_Join = ? WHERE Soldier_ID = ?'''
        cursor.execute(insertion_query, (image_path, name, birth_date, soldier_id, mobile_number, home_address, city, governorate, home_number, retiring_date, mothers_mob_number, function_inside_department, date_of_join, soldier_id))
        connection.commit()

    except sqlite3.Error as e:
        print(e)
        return False
    




def retreive_Document(soldier_ID):
    returned_result = False

    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()
        Checking_query = f'SELECT * FROM Documents WHERE Soldier_ID = ?'
        result = cursor.execute(Checking_query, (str(soldier_ID),)).fetchall()
        
        returned_result = {}
        returned_result['Image_Path'] = os.path.join(DB_PHOTOS,result[0][0])
        returned_result['Name'] = result[0][1]
        returned_result['BirthDate'] = result[0][2]
        returned_result['Soldier_ID'] = result[0][3]
        returned_result['Mobile_Num'] = result[0][4]
        returned_result['Home_Address'] = result[0][5]
        returned_result['City'] = result[0][6]
        returned_result['Governorate'] = result[0][7]
        returned_result['Home_Number'] = result[0][8]
        returned_result['Retiring_Date'] = result[0][9]
        returned_result['Mothers_Mobile_Num'] = result[0][10]
        returned_result['Function_Inside_Dept'] = result[0][11]
        returned_result['Date_Of_Join'] = result[0][12]


    except sqlite3.Error as e:
        print(e)
        returned_result = False
    finally:
        cursor.close()
        return returned_result


def retreive_All_Documents():
    final_result = False

    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()
        Checking_query = f'SELECT * FROM Documents'
        allresults = cursor.execute(Checking_query).fetchall()

        final_result = []
        for result in allresults:
            entry_result = {}
            entry_result['Image_Path'] = os.path.abspath(os.path.join(DB_PHOTOS, result[0]))
            entry_result['Name'] = result[1]
            entry_result['BirthDate'] = result[2]
            entry_result['Soldier_ID'] = result[3]
            entry_result['Mobile_Num'] = result[4]
            entry_result['Home_Address'] = result[5]
            entry_result['City'] = result[6]
            entry_result['Governorate'] = result[7]
            entry_result['Home_Number'] = result[8]
            entry_result['Retiring_Date'] = result[9]
            entry_result['Mothers_Mobile_Num'] = result[10]
            entry_result['Function_Inside_Dept'] = result[11]
            entry_result['Date_Of_Join'] = result[12]

            final_result.append(entry_result)


    except sqlite3.Error as e:
        print(e)
        final_result = False
    finally:
        cursor.close()
        return final_result





def delete_Document(soldier_ID):
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = 1")
        cursor = connection.cursor()

        search_query = "DELETE FROM Documents WHERE Soldier_ID = ?"
        result = cursor.execute(search_query, (soldier_ID,))
        connection.commit()
    except sqlite3.Error as e:
        print(e)
        return False
    
