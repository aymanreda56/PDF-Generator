import sqlite3
from enums import EntryError, EntryErrorCode








def AddNewSoldier(soldier_data):
        try:
            CheckIfSoldierExists(soldier_data=soldier_data, Table_Name='Force')
        except:
            raise EntryError(EntryErrorCode.SOLDIER_ALREADY_EXISTING_ERR)
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



def CheckIfSoldierExists(soldier_data, Table_Name):
    try:
        connection = sqlite3.connect('../db/Soldiers.db')
        cursor = connection.cursor()
        Checking_query = f'SELECT * FROM {Table_Name} WHERE Soldier_ID = "{soldier_data["Soldier_ID"]}"'
        result = cursor.execute(Checking_query).fetchall()
        print('\n\n\n\n')
        print(result)
        print('\n\n\n\n')
        if(result == []):
            return False
            #
        else:
            raise EntryError(EntryErrorCode.SOLDIER_ALREADY_EXISTING_ERR)
            return True

    except sqlite3.Error as e:
        print(e)
    
    except EntryError as e:
        raise EntryError(EntryErrorCode.SOLDIER_ALREADY_EXISTING_ERR)
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
            new_dict['Name'], new_dict['Soldier_ID'], new_dict['Level'], new_dict['Retiring_Date'] = tupl
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