# Volunteer class file
import pandas as pd
import re
from Camps import Camps
import csv
from datetime import date
from datetime import datetime


# need to work on how we are to set this out
# the variables self.volunteer_file and self.volunteer_data i think should be part of the __init__
# also need to think about how this will work in the gui (loops on validation etc.)
class Volunteer:
    def __init__(self, username):
        self.username = username

        # Filepaths for MAC
        # self.camp_path = "files\\camps_file.csv"
        # self.resource_path = "files\\resources.csv"
        # self.volunteer_path = 'files\\volunteers.csv'
        # self.resource_req_path = "files\\resource_request.csv"
        # self.volunteer_file = None

        # Filepaths for windows
        self.camp_path = "../files/camps_file.csv"  
        self.resource_path = "../files/resources.csv"  
        self.volunteer_path = "../files/volunteers.csv" 
        self.resource_req_path = "../files/resource_request.csv"
        self.volunteer_file = None

    
    def get_volunteer_data(self):
        self.volunteer_file = pd.read_csv(self.volunteer_path)
        self.volunteer_data = self.volunteer_file[self.volunteer_file['Username'] == self.username].copy()
        self.volunteer_index = self.volunteer_data.index
        
        if not self.volunteer_data.empty: return (self.volunteer_data)
        else: return "No volunteer data"
        
    
    def edit_volunteer_details(self, fname, sname, phone, age, availability):
        
        if self.validate_personal_details(fname, sname, phone, age, availability):
            self.volunteer_data['First Name'] = fname.strip().capitalize()
            self.volunteer_data['Last Name'] = sname.strip().capitalize()
            self.volunteer_data['Phone'] = int(phone)
            self.volunteer_data['Age'] = int(age)
            # self.volunteer_data['Camp_ID'] = Camp_ID
            self.volunteer_data['Availability'] = availability
            self.volunteer_file.iloc[self.volunteer_index, :] = self.volunteer_data
            self.volunteer_file.to_csv(self.volunteer_path, index=False)
            return True
        else:
            return self.errors


    def validate_personal_details(self, fname, sname, phone, age, availability):
        alphabet = "^[a-zA-Z\s]+$"
        self.errors = ["", "", "", "", ""]
        
        
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

        def availability_validate():
            if "1" not in str(availability):
                self.errors[4] = "Availability must be at least one day per week."


        fname_validate(), sname_validate(), phone_validate(), age_validate(), availability_validate()
        if self.errors == ["", "", "", "", ""]:
            return True
        return False


    def switch_volunteer_camp(self, new_camp_id):
        # Load the volunteer's current data if not already loaded
        if self.volunteer_file is None:
            self.get_volunteer_data()

        # Retrieve the volunteer's row using their username
        volunteer_row = self.volunteer_file[self.volunteer_file['Username'] == self.username]

        # Check if volunteer data exists
        if volunteer_row.empty:
            return False

        # Retrieve the original CampID before updating
        original_camp_id = volunteer_row['CampID'].iloc[0]

        # Update the camps data
        camps = Camps()
        camps_data = camps.get_data()

        # Decrease Num_Of_Volunteers in the original camp if it's not the same as the new camp
        if original_camp_id != new_camp_id:
            original_camp_index = camps_data.index[camps_data['Camp_ID'] == original_camp_id].tolist()
            if original_camp_index:
                camps_data.loc[original_camp_index[0], 'Num_Of_Volunteers'] -= 1

            # Increase Num_Of_Volunteers in the new camp
            new_camp_index = camps_data.index[camps_data['Camp_ID'] == new_camp_id].tolist()
            if new_camp_index:
                camps_data.loc[new_camp_index[0], 'Num_Of_Volunteers'] += 1

            # Write the changes back to the CSV file
            camps_data.to_csv(camps.camps_filepath, index=False)

        # Update the volunteer's camp ID
        self.volunteer_file.loc[self.volunteer_file['Username'] == self.username, 'CampID'] = new_camp_id

        # Write the changes back to the CSV file
        self.volunteer_file.to_csv(self.volunteer_path, index=False)

        return True


    def edit_camp_details(self, camp_id, capacity):
        camps = Camps()
        self.camps_data = camps.get_data()
        if self.validate_camp_details(camp_id, capacity):
           self.volunteer_data['Camp_ID'] = camp_id
           self.volunteer_file.iloc[self.volunteer_index, :] = self.volunteer_data
           self.volunteer_file.to_csv(self.volunteer_path, index=False)
        #    when csv is done maybe change to write_data function definition like this:
        #    write_data(self, Camp_ID, Num_Of_Refugees=None, capacity=None). and then just specify which values are to be changed
        #   call by saying camps.write_data(camp_id, capacity=capacity)
           
           camps_row = self.camps_data[self.camps_data['Camp_ID'] == camp_id].copy()
           camps_row['Capacity'] = int(capacity)
           camps_row = camps_row.values.tolist()[0]
           camps.write_data(camp_id, camps_row)
           return True
        else:
           return self.camperrors


    def validate_camp_details(self, camp_id, capacity):
        print(self.camps_data[self.camps_data['Camp_ID'] == camp_id])
        print(self.camps_data[self.camps_data['Camp_ID'] == camp_id]['Num_Of_Refugees'])
        print(self.camps_data[self.camps_data['Camp_ID'] == camp_id].loc[:,'Num_Of_Refugees'].values[0])
        curr_num_refugees = self.camps_data[self.camps_data['Camp_ID'] == camp_id].loc[:,'Num_Of_Refugees'].values[0]
        self.camperrors = [""] 
        def capacity_validate():
            if capacity.isdigit():
                if int(capacity) > 10000:
                    self.camperrors[0] = ("Capacity too high")
                elif int(capacity) <= 0:
                    self.camperrors[0] = ("Capacity must be positive")
                elif int(capacity) < int(curr_num_refugees):
                    self.camperrors[0] = (f'Capacity cannot be less than the current number of refugees ({curr_num_refugees})')
                else:
                    self.camperrors[0] = ""
            else:
                self.camperrors[0] = ("Capacity must be number")
        capacity_validate()
        if self.camperrors == [""]:
            return True
        return False
        
    
    def edit_resources_req_details(self, username, camp_id, food, medical_supplies, tents):
        volunteer_username = username
        volunteer_camp = camp_id
        food_entry = food
        medical_supplies_entry = medical_supplies
        tents_entry = tents
        today = str(date.today())
        today = datetime.strptime(today, "%Y-%m-%d").strftime("%d/%m/%Y")
        
        def validate_entries(food, medical_supplies, tents):
            errors = ["", "", ""]
            if food.isdigit():
                errors[0] = ""
            else:
                errors[0] = ("Resource must be a number")

            if medical_supplies.isdigit():
                errors[1] = ""
            else:
                errors[1] = ("Resource must be a number")

            if tents.isdigit():
                errors[2] = ""
            else:
                errors[2] = ("Resource must be a number")
            return errors
        
        self.errors = validate_entries(food_entry, medical_supplies_entry, tents_entry) 
        if self.errors == ["", "", ""]:
            print("inputs were integers")
            input_food = int(food_entry)
            input_medical_supplies = int(medical_supplies_entry)
            input_tents = int(tents_entry)
            responded = 'False'

            # if volunteer alrd in camp with previous request, overwrite the previous request
            # if camp had not made previous request, write to csv
            req_df = pd.read_csv(self.resource_req_path)

            if volunteer_camp in req_df.iloc[:,1].values:
                req_df = req_df[req_df['Camp_ID'] != str(volunteer_camp)]
                # print(req_df)
                req_df.to_csv(self.resource_req_path, index=False)

            with open(self.resource_req_path, "a") as file:
                file.write(f"{volunteer_username},{volunteer_camp},{input_food},{input_medical_supplies},{input_tents},{today},{responded}\n")

            return True
        else:
            print("inputs were not integers")
            return self.errors


# def main():
#     # Example setup for testing
#     volunteer_username = "volunteer3"  # Replace with a valid username
#     new_camp_id = "C67890"      # Replace with a valid new camp ID

#     # Create a Volunteer instance
#     volunteer = Volunteer(username=volunteer_username)
    
#     # Call the method to switch the volunteer's camp
#     success = volunteer.switch_volunteer_camp(new_camp_id)

#     # Print the result
#     if success:
#         print(f"Successfully switched to camp {new_camp_id}.")
#     else:
#         print("Failed to switch camps.")

# if __name__ == "__main__":
#     main()