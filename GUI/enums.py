from enum import Enum



class EntryError(Exception):
    def __init__(self, entry_err_code):
        message = entry_err_code.value
        self.message = message
        super().__init__(self.message)



class EntryErrorCode(Enum):
    SOLDIER_ID_ERR = "يوجد خطأ في الرقم العسكري"
    SOLDIER_NAME_ERR = "يوجد خطأ في الإسم"
    RETIRING_DATE_DAY_ERR = "خطأ في تاريخ التسليم, برجاء إدخال رقم من 1 إلى 30"
    RETIRING_DATE_MONTH_ERR = "خطأ في شهر التسليم, برجاء إدخاء رقم من 1 إالى 12"
    RETIRING_DATE_YEAR_ERR = "خطأ في سنة التسليم, برجاء إدخال رقم من 2024 إلى 2100"

    RETIRING_DATE_INTEGER_ERR = "برجاء إدخال ارقام إنجليزية في خانة التاريخ و ليس كلمات"
    RETIRING_DATE_GENERAL_ERR = "خطأ في تاريخ التسليم, برجاء مراجعة البيانات و ادخال الأرقام بالإنجليزية"

    SOLDIER_ALREADY_EXISTING_ERR = "الشخص بالفعل مسجل, برجاء تعديل البيانات او مسح الشخص المسجل و إدخاله مرة أخرى"


