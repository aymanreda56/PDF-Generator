import os

with open('db_path.txt', 'r') as f:
    DB_FOLDER = os.path.abspath(f.read())
    DB_PHOTOS = os.path.join(DB_FOLDER, 'Soldier_Photos')
    




SoldierData = [ \
    { \
        'Name': 'أيمن محمد رضا',\
        'Function_Inside_Dept': 'فريق البحث و التطوير',\
        'Soldier_ID': '012153133',\
        'Mobile_Num': '01225838009',\
        'Retiring_Date': '01-03-2025',\
        'Image_Path': os.path.join(DB_PHOTOS,'ayman.png'),\
    },\

    {\
        'Name': 'خالد محمد هاشم محمد',\
        'Function_Inside_Dept': 'استلام مكاتبات',\
        'Soldier_ID': '123513213',\
        'Mobile_Num': '01225838009',\
        'Retiring_Date': '01-03-2025',\
        'Image_Path': os.path.join(DB_PHOTOS,'khaled.png'),\
    },\
    
    {
        'Name': 'عبدالرحمن صبري محمد',\
        'Function_Inside_Dept': 'فريق البحث و التطوير',\
        'Soldier_ID': '542312351',\
        'Mobile_Num': '01225838009',\
        'Retiring_Date': '01-03-2025',\
        'Image_Path': os.path.join(DB_PHOTOS,'sabry.png'),\
    },


    {\
        'Name': 'محمد عبدالحليم احمد حامد',\
        'Function_Inside_Dept': 'فريق البحث و التطوير',\
        'Soldier_ID': '753442341',\
        'Mobile_Num': '01225838009',\
        'Retiring_Date': '01-03-2025',\
        'Image_Path': os.path.join(DB_PHOTOS,'halim.png'),\
    },\
    

    {\
        'Name': 'أمجد محمد احمد محمود',\
        'Function_Inside_Dept': 'فريق البحث و التطوير',\
        'Soldier_ID': '123215124',\
        'Mobile_Num': '01225838009',\
        'Retiring_Date': '01-03-2025',\
        'Image_Path': os.path.join(DB_PHOTOS,'amgad.png'),\
    },\
    
    ]