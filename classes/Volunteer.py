# Volunteer class file
import pandas as pd
import re
from Camps import Camps


# need to work on how we are to set this out
# the variables self.volunteer_file and self.volunteer_data i think should be part of the __init__
# also need to think about how this will work in the gui (loops on validation etc.)
class Volunteer:
    def __init__(self, username):
        self.username = username

        # Filepaths for windows
        # self.camp_path = "../files/camps_file.csv"
        # self.resource_path = "../files/resources.csv"
        # self.volunteer_path = '../files/volunteers.csv'


        # Filepaths for MAC
        self.camp_path = "files/camps_file.csv"  
        self.resource_path = "files/resources.csv"  
        self.volunteer_path = "files/volunteers.csv" 

    
    def get_volunteer_data(self):
        self.volunteer_file = pd.read_csv(self.volunteer_path)
        self.volunteer_data = self.volunteer_file[self.volunteer_file['Username'] == self.username].copy()
        self.volunteer_index = self.volunteer_data.index
        
        if not self.volunteer_data.empty: return (self.volunteer_data)
        else: return "No volunteer data"
        
    
    def edit_volunteer_details(self, fname, sname, phone, age, availability):
        if self.validate_personal_details(fname, sname, phone, age):
            self.volunteer_data['First Name'] = fname.strip().capitalize()
            self.volunteer_data['Last Name'] = sname.strip().capitalize()
            self.volunteer_data['Phone'] = int(phone)
            self.volunteer_data['Age'] = int(age)
            self.volunteer_data['Availability'] = int(availability)  # Update availability
            # self.volunteer_data['Camp_ID'] = Camp_ID
            self.volunteer_file.iloc[self.volunteer_index, :] = self.volunteer_data
            self.volunteer_file.to_csv(self.volunteer_path, index=False)
            return True
        else:
            return self.errors
       
    def validate_personal_details(self, fname, sname, phone, age,availability):
        alphabet = "^[a-zA-Z\s]+$"
        self.errors = ["", "", "", ""]
        
        
        def fname_validate():
            if not bool(re.match(alphabet,fname)):
                self.errors[0] = ("Name can only be characters")
            else:
                if " " in fname:
                    self.errors[0] = ("Do not enter spaces in name")
                else:
                    fname.strip()
                    
                    if len(fname)>20 or len(fname) <0:
                        self.errors[0] = ("Name has to be between 0-20 characters")
                    else:
                        self.errors[0] = ""


        def sname_validate():
            if not bool(re.match(alphabet, sname)):
                self.errors[1] = ("Name can only be characters")
            else:
                if " " in sname:
                    self.errors[1] = ("Do not enter spaces in name")
                else:
                    sname.strip()
                    if len(sname)>20 or len(sname) <0:
                        self.errors[1] = ("Name has to be between 0-20 characters")
                    else: self.errors[1] = ""


        def phone_validate():
            if phone.isdigit():
                if 6>len(phone) or len(phone)>15:
                    self.errors[2] = "Phone number must be between 6-15 digits"
                else:
                    self.errors[2] = ""
            else:
                self.errors[2] = ("Phone number must be only numbers")


        def age_validate():
            if age.isdigit():
                if int(age) > 140:
                    self.errors[3] = ("Age too high")
                elif int(age) <= 0:
                    self.errors[3] = ("Age must be positive")
                else:
                    self.errors[3] = ""
            else:
                self.errors[3] = ("Age must be number")
        # def camp_validate():
        #     camp = Camps()
        #     camp_data = camp.get_data()
        #     camps = camp_data['camp_id']
        #     if Camp_ID not in camps.values:
        #         raise ValueError("Camp_ID does not exist")
        def availability_validate():
            if availability.isdigit():
                if int(availability) > 100:  # Assuming availability is a percentage
                    self.errors.append("Availability cannot exceed 100")
                elif int(availability) < 0:
                    self.errors.append("Availability cannot be negative")
                else:
                    self.errors.append("")
            else:
                self.errors.append("Availability must be a number")

        # Call the new validation function
        fname_validate(), sname_validate(), phone_validate(), age_validate(), availability_validate()
        if all(error == "" for error in self.errors):
            return True
        return False


    def edit_camp_details(self, camp_id, availability, capacity):
        if self.validate_camp_details(camp_id, availability, capacity):
           print('v', availability)
           self.volunteer_data['Camp_ID'] = camp_id

           self.volunteer_file.iloc[self.volunteer_index, :] = self.volunteer_data
           self.volunteer_file.to_csv(self.volunteer_path, index=False)
           camps = Camps()
        #    when csv is done maybe change to write_data function definition like this:
        #    write_data(self, Camp_ID, Num_Of_Refugees=None, capacity=None). and then just specify which values are to be changed
        #   call by saying camps.write_data(camp_id, capacity=capacity)
           camps_data = camps.get_data()
           camps_row = camps_data[camps_data['Camp_ID'] == camp_id].copy()
           camps_row['Num_Of_Refugees'] = int(capacity)
           camps.write_data(camp_id, camps_row)
           return True
        else:
           return self.camperrors
           
        
    def validate_camp_details(self, camp_id, availability, capacity):
        self.camperrors = [""] 
        def capacity_validate():
            if capacity.isdigit():
                if int(capacity) > 1000000:
                    self.camperrors[0] = ("Capacity too high")
                elif int(capacity) <= 0:
                    self.camperrors[0] = ("Capacity must be positive")
                else:
                    self.camperrors[0] = ""
            else:
                self.camperrors[0] = ("Capacity must be number")
        capacity_validate()
        if self.camperrors == [""]:
            return True
        return False
    




# if __name__ == "__main__":
#     # Creating an instance of the Volunteer class
#     volunteer = Volunteer("test_user")





# volunteer = Volunteer('volunteer1')
# # need to think about order of functions here. get_vol_data needs to be called before edit so maybe needs to be in __init__
# # if no volunteer data do we then do a create_data function?
# volunteer.get_volunteer_data()
# volunteer.edit_volunteer_data("dev", "gov", 1, 3, "camp_01", "01")
# volunteer.edit_volunteer_data("dev2", "A", "3", "cap", "01")
# volunteer.edit_volunteer_data("  ", "sad", "324s2", "cap", "01")