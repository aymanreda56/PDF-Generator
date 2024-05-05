from enum import Enum










class EntryError(Exception):
    def __init__(self, entry_err_code):
        message = entry_err_code.value
        self.message = message
        super().__init__(self.message)



class EntryErrorCode(Enum):
    SOLDIER_ID_ERR = "يوجد خطأ في الرقم العسكري"
    SOLDIER_ID_INTEGER_ERR = "برجاء عدم إدخال حروف, مسموح فقط بالأرقام الإنجليزية"

    SOLDIER_ID_MISSING = "من فضلك أدخل الرقم العسكري"

    SOLDIER_NAME_ERR = "يوجد خطأ في الإسم"
    SOLDIER_NAME_MISSING = "من فضلك أدخل الإسم"
    SOLDIER_NAME_NOT_ARABIC = "الإسم يجب ان يكون باللغة العربية تماماً"
    SOLDIER_NAME_TOO_SHORT_ERR = "الإسم قصير للغاية, برجاء ادخال الإسم رباعي بالكامل"
    SOLDIER_NAME_TOO_LONG_ERR = 'الإسم طويل للغاية, برجاء إدخال الإسم بشكل صحيح'

    RETIRING_DATE_DAY_ERR = "خطأ في تاريخ التسليم, برجاء إدخال رقم من 1 إلى 30"
    RETIRING_DATE_MONTH_ERR = "خطأ في شهر التسليم, برجاء إدخاء رقم من 1 إالى 12"
    RETIRING_DATE_YEAR_ERR = "خطأ في سنة التسليم, برجاء إدخال رقم من 2024 إلى 2100"

    RETIRING_DATE_INTEGER_ERR = "برجاء إدخال ارقام إنجليزية في خانة التاريخ و ليس كلمات"
    RETIRING_DATE_GENERAL_ERR = "خطأ في تاريخ التسليم, برجاء مراجعة البيانات و ادخال الأرقام بالإنجليزية"

    VACATIONS_DATES_ARE_NEGATIVE = "خطأ في التواريخ, يجب ان يكون تاريخ النزول قبل تاريخ العودة و ليس العكس"

    VACATION_ALREADY_EXISTING = 'الشخص بالفعل مسجل في الأجازات\nإذا كنت تريد تعديلها فبرجاء مسحها و إدخالها مرة أخرى'


    SOLDIER_ALREADY_EXISTING_ERR = "الشخص بالفعل مسجل, برجاء تعديل البيانات او مسح الشخص المسجل و إدخاله مرة أخرى"






class SoldierModelErrorCode(Enum):
    IMAGE_EMPTY = 'برجاء إدخال صورة شخصية'
    IMAGE_NOT_PARSEABLE = 'برجاء إدخال صورة سليمة و ليست فايل غير مفهوم'

    NAME_EMPTY = 'برجاء إدخال اسم الشخص'

    BIRTHDATE_EMPTY = 'برجاء إدخال تاريخ ميلاد الشخص'

    SOLDIER_ID_EMPTY = 'برجاء إدخال الرقم العسكري للشخص'

    RETIRING_DATE_EMPTY = 'برجاء إدخال تاريخ الرديف للشخص'

    MOBILE_NUMBER_EMPTY = 'برجاء إدخال رقم موبايل الشخص'
    
    HOME_ADDRESS_EMPTY = 'برجاء إدخال عنوان الشخص'

    CITY_EMPTY = 'برجاء إدخال المدينة'

    GOVERNORATE_EMPTY = 'برحاء إدخال المحافظة'

    HOME_NUMBER_EMPTY = 'برجاء إدخال رقم هاتف المنزل'

    MOTHERS_MOBILE_NUMBER_EMPTY = 'برجاء إدخال رقم ولي الأمر'

    FUNCTION_EMPTY = 'برجاء إدخال الوظيفة داخل الإدارة'

    JOIN_DATE_EMPTY = 'برجاء إدخال تاريخ الإنضمام للإدارة'






ArmyLevels=[
    'جندي',
    'رقيب',
    'رقيب أول',
    'مساعد',
    'مساعد أول',
    'ملازم',
    'ملازم أول',
    'نقيب',
    'رائد',
    'مقدم',
    'عقيد',
    'عميد',
    'لواء',
    'فريق',
    'فريق أول',
    'مشير'
]

