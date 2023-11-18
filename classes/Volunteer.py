# Volunteer class file
import pandas as pd
import re
from Camps import Camps
class Volunteer:
    def __init__(self, username):
        self.username = username
        
    def get_volunteer_data(self):
        volunteer_file = pd.read_csv('./files/volunteers.csv')
        self.volunteer_data = volunteer_file[volunteer_file['Username'] == self.username]
        if not self.volunteer_data.empty: return (self.volunteer_data)
        else: return "No volunteer data"
    def edit_volunteer_data(self, name, phone, age, campID, availability):
        try: 
            self.validate_data(name, phone, age, campID, availability)
            print("data all good")
        except ValueError as e:
            print(f'errors: {e}')
    

        
    def validate_data(self, name, phone, age, campID, availability):
        alphabet = "^[a-zA-Z\s]+$"
        def name_validate():
            if not bool(re.match(alphabet, name)):
                raise ValueError("Name can only be characters")
        def phone_validate():
            try:
                int(phone)
            except:
                raise ValueError("Phone number must be only numbers")
        def age_validate():
            try:
                int(age)
                if age > 140:
                    raise ValueError("Age too high")
                elif age < 0:
                    raise ValueError("Age must be positive")
            except:
                raise ValueError("Age must be number")
        def camp_validate():
            camp = Camps()
            camp_data = camp.get_data()
            camps = camp_data['camp_id']
            if campID not in camps.values:
                raise ValueError("CampID does not exist")
        return name_validate(), phone_validate(), age_validate(), camp_validate()
    def create_refugee_profile(self):
        pass
    def edit_details(self):
        pass

volunteer = Volunteer('volunteer1')
volunteer.get_volunteer_data()
volunteer.edit_volunteer_data("dev", 1, 3, "cap", "01")
volunteer.edit_volunteer_data("dev2", "A", "3", "cap", "01")
volunteer.edit_volunteer_data("  ", "sad", "324s2", "cap", "01")

