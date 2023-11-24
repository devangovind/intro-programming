# Admin Class File

from Plans import humanitarian_plan
import datetime
import csv
import pandas as pd
from Camps import Camps
from datetime import date
from datetime import datetime

class Admin:

    # add functions here
    # remember for functions added the first parameter has to be a self
    def create_humanitarian_plan(self):
        pass
  

    def __init__(self):
        self.plans_file = 'intro-programming/files/plans.csv'
        self.camps_file = 'intro-programming/files/camps_file.csv'
        self.resources_file = 'intro-programming/files/resources.csv'
        self.login_file = './files/logindetails.csv'
        self.volunteer_file = './files/volunteers.csv'
        self.camp_id = None
        self.users = pd.read_csv(self.login_file)


 # FOR (C) DISPLAY PLAN


    def check_event_ended(self, plan_id):
        plans = pd.read_csv(self.plans_file)
        plan_details = plans[plans["Plan_ID"]== plan_id]
        plan_end_date_str = plan_details.iloc[0,-1]
        today = date.today()
        plan_end_date = datetime.strptime(plan_end_date_str, "%d/%m/%Y").date()
        #returns True if end date has occured and False if end date has not
        return today > plan_end_date 
     

    def display_plan(self, plan_id):
        camps = pd.read_csv(self.camps_file)
        plans = pd.read_csv(self.plans_file)

        if self.check_event_ended(plan_id):
            return "This humanitarian plan has ended."
        else:
            plan_details = camps[camps['Plan_ID']== plan_id]
            if plan_details.empty:
                return "This humanitarian plan does not exist."
            else:
                return plan_details[["Camp_ID","Num_Of_Refugees","Num_Of_Volunteers"]]
          
 
 # FOR (D) ACCOUNT ACTIVATION


    def save_changes(self):
        self.users.to_csv(self.login_file, sep=',', index=False, encoding='utf-8')
        return "Saved changes"


    def activate_account(self, username):
        try:
            if username in self.users['Username'].values:
                if self.users.loc[self.users['Username'] == username, 'Active'].iloc[0] != True: # iloc[0] ensures that 'Active' column is selected 
                    self.users.loc[self.users['Username'] == username, 'Active'] = True
                    self.save_changes()
                    return 'Your account has been activated'
                else:
                    return 'Your account has already been activated'
        except KeyError:
            return "Account doesn't exist"


    def activate_all(self):
        self.users['Active'] = True
        self.save_changes()
        return "All accounts have been activated"


    def deactivate_account(self, username):
        try:
            if username in self.users['Username'].values:
                if self.users.loc[self.users['Username'] == username, 'Active'].iloc[0] == True:
                    self.users.loc[self.users['Username'] == username, 'Active'] = False
                    self.save_changes()
                    return "Your account has been deactivated, contact the administrator."
                else:
                    return "Your account has already been deactivated"
        except KeyError:
            return "Account doesn't exist"

    def deactivate_all(self):
        self.users['Active'] = False
        self.save_changes()
        return "All accounts have been deactivated"


    def delete_account(self, username):
        self.volunteer_data = pd.read_csv(self.volunteer_file)
        try:
            if username in self.users['Username'].values:
                self.users = self.users[self.users['Username'] != username]  # Filter out the user to be deleted
                self.volunteer_data = self.volunteer_data[self.volunteer_data['Username'] != username]
                self.volunteer_data.to_csv(self.volunteer_file, sep=',',index=False, encoding='utf-8' )
                self.save_changes()
                return f"Account {username} deleted"
            else:
                return "Account doesn't exist"
        except KeyError:
            return "Account doesn't exist"

 
 # FOR (E) RESOURCE ALLOCATION

    def read_csv(self, filepath):
        try:
            with open(filepath, mode='r', encoding='utf-8-sig') as file:  
                return list(csv.DictReader(file))
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
            return []
          
    
    def write_csv(self, filepath, data):
        try:
            with open(filepath, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=data.keys())

                if file.tell() == 0:
                    writer.writeheader()
                
                writer.writerow(data)
        except Exception as e:
            print(f"Error writing file {filepath}: {e}")


    def create_humanitarian_plan(self):
        description = input("Enter the description of the plan: ")
        geographical_location = input("Enter the geographical location of the plan: ")
        start_date = input("Enter the start date of the plan (YYYY/MM/DD): ")
        
        plan = humanitarian_plan(description, geographical_location, start_date)
        plan_data = plan.display_plan()
    
        plan_dict = {'description': description, 'geographical_location': geographical_location, 'start_date': start_date}

        self.write_csv(self.plans_file, plan_data)

    
    def display_plans(self):
        existing_data = self.read_csv(self.plans_file)

        for row in existing_data:
            print(row)


    def menu(self):
        while True:
            print("1. Create a new humanitarian plan")
            print("2. Display the humanitarian plans")

            a = int(input("Please enter your requirement: "))

            if a == 1:
                self.create_humanitarian_plan()
            elif a == 2:
                self.display_plans()
            else:
                print("Please enter the valid number again!")

                
    def set_camp_id(self):
        self.camp_id = input("Enter camp ID (Not case sensitive)): ").upper()


    def get_camp_population(self, camp_id):
            try:
                camps = Camps()
                camps_data = camps.get_data()
                # pd_obj is the name for dataframe and we treat it 
                # like array thus result below
                camp = camps_data[camps_data['Camp_ID'] == camp_id]
                if not camp.empty:
                    no_ref = int(camp.iloc[0]['Num_Of_Refugees'])
                    no_volunteer = int(camp.iloc[0]['Num_Of_Volunteers'])
                    return no_ref
                else:
                    print(f"Camp ID: {self.camp_id} not found.")
                    return 0
            except Exception as e:
                print(f"Error in get_camp_population: {e}")
                return 0
            

    def update_resource_allocation(self, camp_id, food, medical, tent):
        # try:
        #     if not isinstance(self.camp_id, str) or not isinstance(resource_type, str):
        #         raise ValueError("camp_id and resource_type must be strings")

        #     resources = pd.read_csv(self.resources_file)
        #     camps = pd.read_csv(self.camps_file)
        #     if self.camp_id in camps['Camp_ID'].values and self.camp_id in resources['Camp_ID'].values:
        #         if resource_type in resources.columns:
        #             resources.loc[resources['Camp_ID'] == self.camp_id, resource_type] = quantity
        #             print(f"Updated {resource_type} for {self.camp_id} to {quantity}.")
        #             resources.to_csv(self.resources_file, index=False)
        #         else:
        #             raise ValueError(f"Invalid resource type: {resource_type}")
        #     else:
        #         print(f"Camp ID {self.camp_id} does not exist in the resources or camps file.")
            # resources = pd.read_csv(self.resources_file)
            # camps = pd.read_csv(self.camps_file)
            # if self.camp_id in camps['Camp_ID'].values and self.camp_id in resources['Camp_ID'].values:
            #     if resource_type in resources.columns:
            #         resources.loc[resources['Camp_ID'] == self.camp_id, resource_type] = quantity

            #         print(f"Updated {resource_type} for {self.camp_id} to {quantity}.")
            #         resources.to_csv(self.resources_file, index=False)
            #     else:
            #         raise ValueError(f"Invalid resource type: {resource_type}")
            # else:
            #     print(f"Camp ID {self.camp_id} does not exist in the resources or camps file.")

        # except Exception as e:
        #     print(f"Error in update_resource_allocation: {e}")
        resources_data = pd.read_csv(self.resources_file)
        camp_index = resources_data.index[resources_data['Camp_ID'] == camp_id]
        new_row = [camp_id, food, medical, tent]
        resources_data.iloc[camp_index, :] = new_row
        resources_data.to_csv(self.resources_file, index=False)
        return True

    def suggest_resources(self, camp_id,duration_days=7):
        population = self.get_camp_population(camp_id)
        if population > 0:
            food_per_person_per_day = 3
            medical_kits_per_10_people_per_day = 0.1
            people_per_tent = 5

            total_food_needed = food_per_person_per_day * population * duration_days
            total_medical_kits_needed = medical_kits_per_10_people_per_day * population * duration_days
            total_tents_needed = -(-population // people_per_tent)

            buffer = 1.20
            total_food_needed = int(total_food_needed * buffer)
            total_medical_kits_needed = int(total_medical_kits_needed * buffer)
            total_tents_needed = int(total_tents_needed * buffer)

            return True, {"food": total_food_needed, "medical": total_medical_kits_needed, "tent": total_tents_needed}
        else:
            # print(f"No suggestions for Camp_ID {self.camp_id} with population 0.")
            
            return False, {"food": 0, "medical": 0, "tent": 0}

    def manual_resource_allocation(self, camp_id, food, medical, tent):
        # if not self.camp_id:
        #     self.set_camp_id()
        # suggested_resources = self.suggest_resources()
        # for resource_type, suggested_quantity in suggested_resources.items():
        #     print(f"Suggested quantity for {resource_type}: {suggested_quantity}")
        #     while True:
        #         user_input = input(f"Enter quantity for {resource_type} (press Enter to accept suggestion): ")
        #         if not user_input:
        #             quantity = suggested_quantity
        #             break
        #         else:
        #             try:
        #                 quantity = int(user_input)
        #                 if quantity >= 0:
        #                     break
        #                 else:
        #                     print("Please enter a non-negative integer.")
        #             except ValueError:
        #                 print("Invalid input. Please enter a valid integer.")
        inputted_resources = {"food": food, "medical": medical, "tent": tent}
        self.resource_errors = {"food": "", "medical": "", "tent":""}
        can_allocate, suggest_dict = self.suggest_resources(camp_id)
        if can_allocate == False:
            return False
        def numerical_validate(resource_type, quantity):
            if quantity.isdigit():
                if int(quantity)>(suggest_dict[resource_type]*5):
                    self.resource_errors[resource_type] = f"{resource_type.title()} resource allocation cannot exceed {suggest_dict[resource_type]*5}"
                else:
                    self.resource_errors[resource_type] = ""
            else:
                self.resource_errors[resource_type] = f"{resource_type.title()} resource allocation must be numerical"
        for key, val in inputted_resources.items():
            numerical_validate(key, val)
        if list(self.resource_errors.values()) == ["", "", ""]:
            self.update_resource_allocation(camp_id, food, medical,tent)
            
            return True
        else:
            return self.resource_errors



if __name__ == "__main__":
    admin = Admin()
    admin.set_camp_id()
    population = admin.get_camp_population()
    print(f"Number of refugees for camp {admin.camp_id}: {population}")
    admin.manual_resource_allocation()
    
    test = Admin()
    test.menu()

    #print(admin.users)
    #print(admin.deactivate_all())
    #print(admin.users)
    #print(admin.activate_all())
    #print(admin.users)
    #print(admin.deactivate_account('volunteer1'))
    #print(admin.users)
    #print(admin.activate_account('volunteer1'))
    #print(admin.users)
    #print(admin.delete_account('volunteer3'))
    #print(admin.users)