import hashlib #line:1
import sqlite3 #line:2

DB_PATH = '../db/Soldiers.db'

# def encryptor (O000OO0OOO0000O00 ,OOOOO00OOO0OO00OO ):#line:5
#     OO000000O0O0000O0 ='1a9b00c2478ab95f2184c8'#line:6
#     OO00OO0O000O0O0O0 ='f2184c81d0f3f923a7511c'#line:7
#     OOOO0O0OO000O0000 ='1fa58d744d2f9249483dbd'#line:8
#     O000000000O0O00OO =OO000000O0O0000O0 +O000OO0OOO0000O00 +OO00OO0O000O0O0O0 +OOOOO00OOO0OO00OO +OOOO0O0OO000O0000 #line:9
#     OO000OO0OOO0O00OO =hashlib .sha512 (O000000000O0O00OO .encode ('utf-8',errors ='ignore'),usedforsecurity =True ).hexdigest ()#line:11
#     return OO000OO0OOO0O00OO #line:12
# def insert_new_user (O000OOOO0O0OO0O0O ,OO0O0OOOOOO0O0OO0 ,OOO0O0OO0000OO00O ,OO00OO00O0OOO0O0O ,O0OOO00OO0O00O000 ):#line:15
#     O000OO0O0000O0OO0 =encryptor (OO0O0OOOOOO0O0OO0 ,OOO0O0OO0000OO00O )#line:17
#     try :#line:19
#         OOOO00OOO0OOO0OO0 =sqlite3 .connect ('../db/Soldiers.db')#line:20
#         O0OOOO00OO0O000O0 =OOOO00OOO0OOO0OO0 .cursor ()#line:21
#         O0O000OOO0OO00O00 ='INSERT INTO Accounts VALUES (?, ?, ?, ?)'#line:23
#         O0OOOO00OO0O000O0 .execute (O0O000OOO0OO00O00 ,(OO00OO00O0OOO0O0O ,O0OOO00OO0O00O000 ,O000OO0O0000O0OO0 ,O000OOOO0O0OO0O0O ))#line:24
#         OOOO00OOO0OOO0OO0 .commit ()#line:25
#     except sqlite3 .Error as O0OOOOOO0OO0O00OO :#line:27
#         print (O0OOOOOO0OO0O00OO )#line:28
#     finally :#line:30
#         OOOO00OOO0OOO0OO0 .close ()#line:31
# def fetchUsers ():#line:35
#     O0OO0000O000O0000 =None #line:36
#     try :#line:37
#         OOOOOOO00OO0O000O =sqlite3 .connect ('../db/Soldiers.db')#line:38
#         OO0O0O0O0O000O0O0 =OOOOOOO00OO0O000O .cursor ()#line:39
#         O00000OO00O00O000 ='SELECT * FROM Accounts'#line:40
#         O0OO0000O000O0000 =OO0O0O0O0O000O0O0 .execute (O00000OO00O00O000 ).fetchall ()#line:41
#     except sqlite3 .Error as O0OO00000O0OOO000 :#line:44
#         print (O0OO00000O0OOO000 )#line:45
#     finally :#line:46
#         OOOOOOO00OO0O000O .close ()#line:47
#         return O0OO0000O000O0000 #line:48
# def DeleteUser (O0OO0OOO000O0OO00 ,O0OO0O00000OO00OO ,OOO00OOO0O0000O00 ):#line:51
#     O0OO0OOOOO0000OO0 =encryptor (O0OO0O00000OO00OO ,OOO00OOO0O0000O00 )#line:52
#     try :#line:53
#         OO0OOOOO00OOOOOOO =sqlite3 .connect ('../db/Soldiers.db')#line:54
#         OOO0O0OO0O0O0O0OO =OO0OOOOO00OOOOOOO .cursor ()#line:55
#         O00O0OOO00O0O00O0 ="DELETE FROM Accounts WHERE name = ? AND hash = ?"#line:56
#         OOO0O0OO0O0O0O0OO .execute (O00O0OOO00O0O00O0 ,(O0OO0OOO000O0OO00 ,O0OO0OOOOO0000OO0 ))#line:57
#         OOO0O0OO0O0O0O0OO .commit ()#line:25
#     except sqlite3 .Error as O0O000OOOO000O000 :#line:58
#         print (O0O000OOOO000O000 )#line:59
#     finally :#line:60
#         OO0OOOOO00OOOOOOO .close ()#line:61
# def CheckUser (O0O00OO00OO0OO0O0 ,O00O00O0000OOOOO0 ):#line:65
#     O000O0OOO0O0000OO =fetchUsers ()#line:66
#     OO00O000O000O00O0 =encryptor (O0O00OO00OO0OO0O0 ,O00O00O0000OOOOO0 )#line:67
#     for O000O00O0O0OO0OOO in O000O0OOO0O0000OO :#line:68
#         if OO00O000O000O00O0 ==O000O00O0O0OO0OOO [2 ]:#line:69
#             O0O0OO000OOO00OOO =O000O00O0O0OO0OOO [0 ]#line:70
#             OO0O0O00OOOO0OO00 =O000O00O0O0OO0OOO [1 ]#line:71
#             OOO0OOO00OO0O0OO0 =O000O00O0O0OO0OOO [3 ]#line:72
#             O0O0O0O0O000000OO ={'name':O0O0OO000OOO00OOO ,'level':OO0O0O00OOOO0OO00 ,'is_admin':OOO0OOO00OO0O0OO0 }#line:73
#             return O0O0O0O0O000000OO #line:74
#     return False





# import hashlib
# import sqlite3


def encryptor (username, password):
    otp1 = '1a9b00c2478ab95f2184c8'
    otp2 = 'f2184c81d0f3f923a7511c'
    otp3 = '1fa58d744d2f9249483dbd'
    source_string = otp1 + username + otp2 + password + otp3

    encrypted_string = hashlib.sha512(source_string.encode('utf-8', errors='ignore'), usedforsecurity= True).hexdigest()
    return encrypted_string


def insert_new_user(is_admin, username, password, name, Level):
   
    encrypted_string = encryptor(username=username, password=password)

    try:
        connection = sqlite3.connect('../db/Soldiers.db')
        cursor = connection.cursor()

        query = 'INSERT INTO Accounts VALUES (?, ?, ?, ?)'
        cursor.execute(query, (name, Level, encrypted_string, is_admin))
        connection.commit()

    except sqlite3.Error as e:
        print (e)
    
    finally:
        connection.close()



def fetchUsers():
    result = None
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        query = 'SELECT * FROM Accounts'
        result = cursor.execute(query).fetchall()
        

    except sqlite3.Error as e:
        print(e)
    finally:
        connection.close()
        return result
    

def DeleteUser(name, username, password):
    encrypted_string = encryptor(username=username, password=password)
    try:
        connection = sqlite3.connect('../db/Soldiers.db')
        cursor = connection.cursor()
        query = "DELETE FROM Accounts WHERE name = ? AND hash = ?"
        cursor.execute(query, (name, encrypted_string))
        connection.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        connection.close()



def CheckUser(username, password):
    all_users = fetchUsers()
    hashed_string = encryptor(username=username, password=password)
    for user_data in all_users:
        if hashed_string == user_data[2]:
            name = user_data[0]
            level = user_data[1]
            is_admin = user_data[3]
            returned_dict= {'name': name, 'level': level, 'is_admin': is_admin}
            return returned_dict
    
    return False





# username = 'soldier'
# password = 'soldier'
# insert_new_user('0', username, password, 'Ayman', 'جندي')

# username = 'user1'
# password = 'user1'
# insert_new_user('0', username, password, 'Dev', 'مطور')

