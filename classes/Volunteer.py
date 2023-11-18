# Volunteer class file
import pandas as pd
import re
from Camps import Camps
class Volunteer:
    def __init__(self, username):
        self.username = username
    def get_volunteer_data(self):
        self.volunteer_file = pd.read_csv('./files/volunteers.csv')
        self.volunteer_data = self.volunteer_file[self.volunteer_file['Username'] == self.username].copy()
        self.volunteer_index = self.volunteer_data.index
        if not self.volunteer_data.empty: return (self.volunteer_data)
        else: return "No volunteer data"
    def edit_volunteer_data(self, fname, sname, phone, age, campID, availability):
        try: 
            self.validate_data(fname, sname, phone, age, campID, availability)
            print("data all good")
            self.volunteer_data['First Name'] = fname
            self.volunteer_data['Last Name'] = sname
            self.volunteer_data['Phone'] = phone
            self.volunteer_data['Age'] = age
            self.volunteer_data['CampID'] = campID
            self.volunteer_data['Availabiltiy'] = availability
            self.volunteer_file.iloc[self.volunteer_index, :] = self.volunteer_data
            self.volunteer_file.to_csv('./files/volunteers.csv', index=False)
        except ValueError as e:
            print(f'errors: {e}')
    

        
    def validate_data(self, fname, sname, phone, age, campID, availability):
        alphabet = "^[a-zA-Z\s]+$"
        def name_validate(name):
            if not bool(re.match(alphabet, name)):
                raise ValueError("Name can only be characters")
            if " " in name:
                raise ValueError("Do not enter spaces in name")
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
        return name_validate(fname), name_validate(sname), phone_validate(), age_validate(), camp_validate()
    def create_refugee_profile(self):
        pass
    def edit_details(self):
        pass

volunteer = Volunteer('volunteer1')
volunteer.get_volunteer_data()
volunteer.edit_volunteer_data("dev", "gov", 1, 3, "camp_01", "01")
# volunteer.edit_volunteer_data("dev2", "A", "3", "cap", "01")
# volunteer.edit_volunteer_data("  ", "sad", "324s2", "cap", "01")

