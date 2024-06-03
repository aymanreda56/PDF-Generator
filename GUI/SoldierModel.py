from enums import SoldierModelErrorCode, EntryError
from datetime import date

class SoldierModel():
    def __init__(self
        , image_path= '', name =  'لا يوجد', birth_date= date(1970, 1, 1).isoformat(), soldier_id= 'لا يوجد', retiring_date= date(1970, 1, 1).isoformat(), mobile_number= 'لا يوجد', home_number= 'لا يوجد', home_address= 'لا يوجد', city= 'لا يوجد', governorate= 'لا يوجد', mothers_mob_number= 'لا يوجد', function_inside_department= 'لا يوجد', date_of_join= 'لا يوجد'):

        
        
        self.name = name
        self.birth_date = birth_date
        self.soldier_id = soldier_id
        self.retiring_date = retiring_date
        self.image_path = image_path
        self.mobile_number = mobile_number
        self.home_address = home_address
        self.home_number = home_number
        self.city = city
        self.governorate = governorate
        self.mothers_mob_number = mothers_mob_number
        self.function_inside_department = function_inside_department
        self.date_of_join = date_of_join

    
    def __eq__(self, value: object) -> bool:
        return self.soldier_id == value.soldier_id
    
    
    def __repr__(self) -> str:
        constructed_string = f'\n\nname:\t{self.name}\nbirthdate:\t{self.birthdate}\nsoldier id:\t{self.soldier_id}\nretiring date:\t{self.retiring_date}\nimage_path:\t{self.image_path}\n'
        constructed_string = constructed_string + f"mobile number:\t{self.mobile_number}\nhome address:\t{self.home_address}\ncity:\t{self.city}\ngovernorate:\t{self.governorate}\n"
        constructed_string = constructed_string + f"home number:\t{self.home_number}\nmother's mobile number:\t{self.mothers_mobile_number}\nfunction inside the department:\t{self.function_inside_department}\n"
        constructed_string = constructed_string + f'date of joining:\t{self.date_of_join}\n\n'
        return constructed_string
    

    def nameIsEmpty(self):
        return self.name == None
    
    def birthdateIsEmpty(self):
        return self.birthdate == None
    
    def soldierIDIsEmpty(self):
        return self.soldier_id == None
    
    def retiringDateIsEmpty(self):
        return self.retiring_date == None
    
    def imagePathIsEmpty(self):
        return self.image_path == None
    
    def mobileNumberIsEmpty(self):
        return self.mobile_number == None
    
    def homeAddressIsEmpty(self):
        return self.home_address == None
    
    def cityIsEmpty(self):
        return self.city == None
    
    def governorateIsEmpty(self):
        return self.governorate == None
    
    def homeNumberIsEmpty(self):
        return self.homeNumberIsEmpty == None
    
    def mothersMobileNumberIsEmpty(self):
        return self.mothers_mobile_number == None
    
    def functionIsEmpty(self):
        return self.function_inside_department == None
    
    def joinDateIsEmpty(self):
        return self.joinDateIsEmpty == None
    


    def is_complete(self):
        if(self.imagePathIsEmpty):
            raise EntryError(SoldierModelErrorCode.IMAGE_EMPTY)
        if(self.nameIsEmpty):
            raise EntryError(SoldierModelErrorCode.NAME_EMPTY)
        if(self.birthdateIsEmpty):
            raise EntryError(SoldierModelErrorCode.BIRTHDATE_EMPTY)
        if(self.soldierIDIsEmpty):
            raise EntryError(SoldierModelErrorCode.SOLDIER_ID_EMPTY)
        if(self.retiringDateIsEmpty):
            raise EntryError(SoldierModelErrorCode.RETIRING_DATE_EMPTY)
        if(self.mobileNumberIsEmpty):
            raise EntryError(SoldierModelErrorCode.MOBILE_NUMBER_EMPTY)
        if(self.homeAddressIsEmpty):
            raise EntryError(SoldierModelErrorCode.HOME_ADDRESS_EMPTY)
        if(self.cityIsEmpty):
            raise EntryError(SoldierModelErrorCode.CITY_EMPTY)
        if(self.governorateIsEmpty):
            raise EntryError(SoldierModelErrorCode.GOVERNORATE_EMPTY)
        if(self.mothersMobileNumberIsEmpty):
            raise EntryError(SoldierModelErrorCode.MOTHERS_MOBILE_NUMBER_EMPTY)
        if(self.homeNumberIsEmpty):
            raise EntryError(SoldierModelErrorCode.HOME_NUMBER_EMPTY)
        if(self.functionIsEmpty):
            raise EntryError(SoldierModelErrorCode.FUNCTION_EMPTY)
        if(self.joinDateIsEmpty):
            raise EntryError(SoldierModelErrorCode.JOIN_DATE_EMPTY)
        

        return True