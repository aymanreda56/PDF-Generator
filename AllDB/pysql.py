import sqlite3
import numpy as np
from datetime import date


    #Creating the db tables
try:
    
    # create connection to database 
    connection = sqlite3.connect('Soldiers.db')

    cursor = connection.cursor()

    result = cursor.execute('''CREATE TABLE "Force" (
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





except sqlite3.Error as e:
    print(e)

finally:
    connection.close()




#Trying to add records:
connection = sqlite3.connect('Soldiers.db')
cursor = connection.cursor()

sample_data = [
    ('123451', "أيمن محمد رضا محمد", '1', date(2025, 3, 1).isoformat()),
    ('123452', "محمود صلاح اسماعيل", '1', date(2024, 6, 1).isoformat()),
    ('123453', "خالد محمد هاشم", '1', date(2025, 1, 1).isoformat()),
]


def AddNewSoldier(soldier_data):
    connection = sqlite3.connect('Soldiers.db')
    cursor = connection.cursor()
    print('\n\n\n\n')
    print(soldier_data)
    print('\n\n\n\n')
    insertion_query = ', '.join([f'"{field}"' if type(field) == str else f'{field}' for field in soldier_data])
    insertion_query = '(' + insertion_query + ')'
    sql_query_entry = f'''INSERT INTO "Force" VALUES {insertion_query}'''
    print(sql_query_entry)
    
    try:
        result = cursor.execute(sql_query_entry)
    except sqlite3.Error as e:
        print(e)

    finally:
        connection.commit()
        cursor.close()

for dat in sample_data:
    AddNewSoldier(dat)


# Verifying arabic text:
try:
    result = cursor.execute('SELECT * from Force')

    result_records = result.fetchall()
    print(result_records)
    
except sqlite3.Error as e:
    print(e)

finally:
    cursor.close()


