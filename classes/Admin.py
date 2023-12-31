# Admin Class File

from Plans import humanitarian_plan
from Plans import Plans
from FileManager import FileManager
import datetime
import csv
import pandas as pd
from Camps import Camps
from Plans import Plans
# from datetime import date
# from datetime import datetime


class Admin:
    def __init__(self, username):
        self.username = username
        csv_manager = FileManager()
        self.resources_file = csv_manager.get_file_path("resources.csv")
        self.login_file = csv_manager.get_file_path('logindetails.csv')
        self.volunteer_file = csv_manager.get_file_path('volunteers.csv')
        self.Plans = Plans()
        self.Camps = Camps()
        self.users = pd.read_csv(self.login_file)
        self.plans_data = self.Plans.get_data()
        self.plan_list = self.Plans.get_plan_ids()


 # FOR (A)(B)(C) DISPLAY PLAN AND END A PLAN


    def check_event_ended(self, plan_id):
        plans = self.Plans.get_data()
        plan_details = plans[plans["Plan_ID"]== plan_id]
        plan_end_date_str = plan_details.iloc[0,-1]
        today = datetime.date.today()
        plan_end_date = datetime.strptime(plan_end_date_str, "%d/%m/%Y").date()
        #returns True if end date has occured and False if end date has not
        return today > plan_end_date 
          
    def get_data(self):
        
        return self.Plans.get_data()
    
## Change some functions to fit the admin.gui(for admin feature a-c and adding a new camp)
## This is to find the last plan_id, in ortder to achive planid plus one when admin create a new plan 
    def last_plan_id(self):
        plan = self.Plans.get_data()
        plan['Numeric_ID'] = plan['Plan_ID'].str.extract(r'(\d+)').astype(int)
        last_plan = plan.loc[plan['Numeric_ID'].idxmax()]
        last_plan_id = last_plan['Plan_ID']
        num_ = int(last_plan_id[1:])
        return num_
    
    def last_camp_id(self):
        camps = self.Camps.get_data()
        camps['Numeric_ID'] = camps['Camp_ID'].str.extract(r'(\d+)').astype(int)
        last_plan = camps.loc[camps['Numeric_ID'].idxmax()]
        last_plan_id = last_plan['Camp_ID']
        num_ = int(last_plan_id[1:])
        return num_

## This is to justify the type of the date input
    def is_date(self, date):
        return isinstance(date, datetime.date)
## This is to make sure the start date
    def check_start_day(self, date):
        today = date.today()
        plan_start_date = date
        if today <= plan_start_date:
            return False
        else:
            return True
## This is to make sure the end date
    def check_end_date(self,end_date,start_day):
        if end_date > start_day:
            return False
        else:
            return True

## This is to refresh the plan after creating a plan 
    def insert_new_plan(self, new_plan):
        self.plan_list.append(new_plan)
    def insert_empty_resource(self, df):
        df.to_csv(self.resources_file, mode="a", index=False, header=False)

## This is to choose the plan which can be added a new camp 
    def valid_plan(self):
        return self.Plans.valid_plans_ids()

        
    
    def valid_camp(self):
        return self.Camps.valid_camps_ids()
       
    
# FOR (D) ACCOUNT ACTIVATION
    def save_changes(self):
        self.users.to_csv(self.login_file, sep=',', index=False, encoding='utf-8')
        return "Saved changes"

    def activate_account(self, username):
        if username in self.users['Username'].values:
            self.users.loc[self.users['Username'] == username, 'Active'] = True
            self.save_changes()
   
    def activate_all(self):
        self.users.loc[self.users['Account Type'] == "Volunteer", 'Active'] = True
        self.save_changes()
        return "All accounts have been activated"


    def deactivate_account(self, username):
        if username in self.users['Username'].values:
            self.users.loc[self.users['Username'] == username, 'Active'] = False
            self.save_changes()
               


    def deactivate_all(self):
        self.users.loc[self.users['Account Type'] == "Volunteer", 'Active'] = False
        self.save_changes()
        return "All accounts have been deactivated"


    def delete_account(self, username, camp_id):
        self.volunteer_data = pd.read_csv(self.volunteer_file)
        try:
            if username in self.users['Username'].values:
                self.volunteer_data = self.volunteer_data[self.volunteer_data['Username'] != username]
                # this line does not work: # self.volunteer_data.to_csv(self.volunteer_file, sep=',',index=False, encoding='utf-8')
                self.volunteer_data.to_csv(self.volunteer_file,index=False)
                self.users = self.users[self.users['Username'] != username]  # Filter out the user to be deleted
                self.save_changes()
                # update camps_file.csv to decrement volunteers
                self.camp_df = self.Camps.get_data()
                self.camp_data = self.camp_df[self.camp_df['Camp_ID'] == camp_id].copy()
                self.camp_index = self.camp_data.index
                self.camp_data['Num_Of_Volunteers'] -= 1
                self.camp_df.iloc[self.camp_index, :] = self.camp_data
                self.Camps.write_data_frame(self.camp_df)
                return f"Account {username} deleted"
            else:
                return "Account doesn't exist"
        except KeyError:
            return "Account doesn't exist"

 
 # FOR (E) RESOURCE ALLOCATION

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
                    return no_ref + no_volunteer
                else:
                    return 0
            except Exception as e:
                return 0
            

    def update_resource_allocation(self, camp_id, food, medical, tent):
        resources_data = pd.read_csv(self.resources_file)
        if camp_id in resources_data['Camp_ID'].values:
            camp_index = resources_data.index[resources_data['Camp_ID'] == camp_id]
            new_row = [camp_id, int(food), int(medical), int(tent)]
            resources_data.iloc[camp_index, :] = new_row
            resources_data.to_csv(self.resources_file, index=False)
        else:
            new_row = {'Camp_ID': camp_id, 'food_pac': food, 'medical_sup': medical, 'tents': tent}
            resources_data.loc[len(resources_data)] = new_row
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

            
            return False, {"food": 0, "medical": 0, "tent": 0}

    def manual_resource_allocation(self, camp_id, food, medical, tent):

        inputted_resources = {"food": food, "medical": medical, "tent": tent}
        self.resource_errors = {"food": "", "medical": "", "tent":""}
        can_allocate, suggest_dict = self.suggest_resources(camp_id)
        if can_allocate == False:
            return False
        def numerical_validate(resource_type, quantity):
            if quantity.isdigit():
              
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
   