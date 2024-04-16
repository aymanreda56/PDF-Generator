import sqlite3

try:
    connection = sqlite3.connect("Soldiers.db")


    cursor = connection.cursor()
    sql_query = """SELECT name FROM sqlite_master
    WHERE type='table';"""
    cursor.execute(sql_query)
    

    result = cursor.fetchall()
    print(type(result))
    print(result)

    for tableName in result:
        delete_db_query = f'''DROP TABLE {tableName[0]}'''
        cursor.execute(delete_db_query)


except sqlite3.Error as e:
    print(e)

finally:
    connection.close()