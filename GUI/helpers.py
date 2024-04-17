import sqlite3
from enums import EntryError, EntryErrorCode, ArmyLevels


def AddNewSoldier(soldier_data):
        try:
            CheckIfSoldierExists(soldier_data=soldier_data, Table_Name='Force')
        except EntryError as e:
            raise EntryError(EntryErrorCode.SOLDIER_ALREADY_EXISTING_ERR)
        
        connection = sqlite3.connect('../db/Soldiers.db')
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
        connection = sqlite3.connect('../db/Soldiers.db')
        cursor = connection.cursor()
        Deleting_query = f'DELETE FROM Force WHERE Soldier_ID = ?'
        result = cursor.execute(Deleting_query, (Soldier_ID))
        connection.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()


def CheckIfSoldierExists(soldier_data, Table_Name):
    try:
        connection = sqlite3.connect('../db/Soldiers.db')
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
            raise EntryError(EntryErrorCode.SOLDIER_ALREADY_EXISTING_ERR)

   
    
    except EntryError as e:
        raise EntryError(EntryErrorCode.SOLDIER_ALREADY_EXISTING_ERR)
    
    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()

def fetchSoldiers():
    try:
        connection = sqlite3.connect('../db/Soldiers.db')
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




def RefreshVacations():
    pass




def getActiveVacations():
    try:
        connection = sqlite3.connect('../db/Soldiers.db')
        cursor = connection.cursor()
        Checking_query = f'SELECT * FROM Vacations WHERE State = 1'
        result = cursor.execute(Checking_query).fetchall()
        print('\n\n\n\n')
        print(result)

        if(result == []):
            return False
        else:
            print(result)
            print('\n\n\n\n')

            return result

    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()




def AddVacation(Soldier_ID, FromDate, ToDate):
    try:
        connection = sqlite3.connect('../db/Soldiers.db')
        cursor = connection.cursor()

        search_query = "SELECT Name FROM Force WHERE Soldier_ID = ?"
        result = cursor.execute(search_query, (Soldier_ID)).fetchall()
        Soldier_Name = result[0]
    except sqlite3.Error as e:
        print(e)
        return False
    try:
        connection = sqlite3.connect('../db/Soldiers.db')
        cursor = connection.cursor()

        insertion_query = "INSERT INTO Vacations VALUES (?, ?, ?, ?)"
        cursor.execute(insertion_query, (Soldier_ID, Soldier_Name, FromDate, ToDate))
        connection.commit()

    except sqlite3.Error as e:
        print(e)
        return False


def RemoveVacation(Soldier_ID):
    try:
        connection = sqlite3.connect('../db/Soldiers.db')
        cursor = connection.cursor()

        search_query = "DELETE FROM Vacations WHERE Soldier_ID = ?"
        result = cursor.execute(search_query, (Soldier_ID))
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


def CreateDB():
    try:
        # create connection to database 
        connection = sqlite3.connect('../db/Soldiers.db')

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
            FOREIGN KEY("Soldier_ID")  REFERENCES Force ("Soldier_ID")
        );''')

        result = cursor.execute('''CREATE TABLE "Missions" (
        "Soldier_ID"	TEXT NOT NULL UNIQUE,
        "Name"	TEXT NOT NULL,
        "From_Date"	TEXT NOT NULL,
        "To_Date"	TEXT NOT NULL,
        "Place"	TEXT,
        FOREIGN KEY("Soldier_ID") REFERENCES Force ("Soldier_ID")
        )''')


        connection.commit()


    except sqlite3.Error as e:
        print(e)

    finally:
        cursor.close()








    