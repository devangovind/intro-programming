# Admin Class File
import pandas as pd
import csv
import datetime

class Admin:
    
    # Combined __init__(self) from multiple sources
    
    def __init__(self):
        self.plans_file = 'intro-programming/files/plans.csv'
        self.camps_file = 'intro-programming/files/camps_file.csv'
        self.resources_file = 'intro-programming/files/resources.csv'
        self.login_file = './files/logindetails.csv'
        self.camp_id = None
        self.users = pd.read_csv(self.login_file)
        
        # from Yan
        with open('C:\\Users\\96249\Desktop\\Python_CW\\intro-programming\\files\\plan_file.csv', 'r', encoding='utf-8') as plan_file:
            read = csv.DictReader(plan_file)
            self.plan_list = []
            for row in read:
                self.plan_list.append(row)


    # FOR (A) CREATE PLANS - GRACIE

    def create_humanitarian_plan(self):
        description = input("Enter the description of the plan: ")
        geographical_location = input("Enter the geographical location of the plan: ")
        start_date = input("Enter the start date of the plan (YYYY/MM/DD): ")
        
        plan = humanitarian_plan(description, geographical_location, start_date)
        plan_data = plan.display_plan()
    
        plan_dict = {'description': description, 'geographical_location': geographical_location, 'start_date': start_date}

        self.write_csv(self.plans_file, plan_data)
        
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

            
    # FOR (B) END DATE - YAN - ALSO INCLUDED - FUNCTIONS FROM YAN FOR A-C GUI INTEGRATION
    
    # This code is for set date of the plan,but still a draft(something need to revise) because without the whole plan table
    def set_valid_sdate(self):
        current_date = datetime.datetime.now()
        cur_year = current_date.year
        cur_month = current_date.month
        cur_day = current_date.day
        self.year = int(input('choose the year of the start date'))
        while self.year < cur_year:
            self.year = int(input('the year is invalid,please choose the year again'))
        self.month = int(input('choose the month of the start date'))
        while self.month < cur_month:
            self.month = int(input('the month is invalid,please choose the year again'))
        self.day = int(input('choose the day of the start date '))
        while self.day < cur_day:
            self.day = int(input('the day is invalid,please choose the year again'))

        date_s = datetime.datetime(self.year, self.month, self.day)

        return date_s

    def set_valid_eedate(self, sdate_):
        current_date = datetime.datetime.now()
        sdate_year = sdate_.year
        sdate_month = sdate_.month
        sdate_day = sdate_.day
        print(sdate_year)
        self.year = int(input('choose the year of the start date'))
        while self.year < sdate_year:
            self.year = int(input(f'the start year of this plan is {sdate_year},please choose the year again'))
        self.month = int(input('choose the month of the start date'))
        while self.month < sdate_month:
            self.month = int(input(f'the start month of this plan is {sdate_month},please choose the month again'))
        self.day = int(input('choose the day of the start date '))
        while self.day < sdate_day:
            self.day = int(input(f'the start day of this plan is {sdate_day},please choose the day again'))

        date_e = datetime.datetime(self.year, self.month, self.day)

        return date_e

    def read_date(self):
        with open('plan_date.CSV', 'r') as date_file:
            read = csv.DictReader(date_file)
            for row in read:
                print(row['start_date'], row['end_date'])

    def save_date(sdate_save, edate_save):
        sdate_save = sdate_save.strftime('%Y-%m-%d')
        edate_save = edate_save.strftime('%Y-%m-%d')
        print(sdate_save)
        print(edate_save)

        with open('plan_date.CSV', 'w') as date_file:
            headers = ['start_date', 'end_date']
            save_date_ = csv.DictWriter(date_file, fieldnames=headers)
            save_date_.writeheader()
            date_dic = {'start_date': sdate_save, 'end_date': edate_save}
            save_date_.writerow(date_dic)

 
    # This is to justify the type of the date input
    def is_date(self, date):
        return isinstance(date, datetime.date)
    
    # This is to make sure the start date
    def check_start_day(self, date):
        today = date.today()
        plan_start_date = date
        if today <= plan_start_date:
            return False
        else:
            return True
    
    # This is to make sure the end date
    def check_end_date(self,end_date,start_day):
        if end_date > start_day:
            return False
        else:
            return True
        
    ## This is to refresh the plan after creating a plan 
    def insert_new_plan(self, new_plan):
        self.plan_list.append(new_plan)
        
    # Change some functions to fit the admin.gui(for admin feature a-c)
    # This is to find the last plan_id, in ortder to achive planid plus one when admin create a new plan 
    def last_plan_id(self):
        plan = pd.read_csv("C:\\Users\\96249\\Desktop\\Python_CW\\intro-programming\\files\plan_file.csv")

        res = plan.sort_values(by='Plan_ID', ascending=False)
        last_plan_id = res.iloc[0]["Plan_ID"]
        # print(res.iloc[0]["Plan_ID"])
        return last_plan_id


    # This is to justify the type of the date input
    def is_date(self, date):
        return isinstance(date, datetime.date)
     
    # FOR (C) DISPLAY PLAN - ELICIA
 
    def check_event_ended(self, plan_id):
        plans = pd.read_csv(self.plans_file)
        plan_details = plans[plans["Plan_ID"]== plan_id]
        plan_end_date_str = plan_details.iloc[0,-1]
        today = date.today()
        plan_end_date = datetime.strptime(plan_end_date_str, "%d/%m/%Y").date()
        #returns True if end date has occured and False if end date has not
        return today > plan_end_date
    
 
    def display_plans(self):
        existing_data = self.read_csv(self.plans_file)

        for row in existing_data:
            print(row)


        if self.check_event_ended(plan_id):
            return "This humanitarian plan has ended."
        else:
            plan_details = camps[camps['Plan_ID']== plan_id]
            if plan_details.empty:
                return "This humanitarian plan does not exist."
            else:
                return plan_details[["Camp_ID","Num_Of_Refugees","Num_Of_Volunteers"]]
          
 
    # FOR (D) EDIT VOLUNTEERS - JUSTIN
 
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
        return "All accounts have been deactivated"


    def delete_account(self, username):
        try:
            if username in self.users['Username'].values:
                self.users = self.users[self.users['Username'] != username]  # Filter out the user to be deleted
                self.save_changes()
                return f"Account {username} deleted"
            else:
                return "Account doesn't exist"
        except KeyError:
            return "Account doesn't exist"

 
    # FOR (E) RESOURCE ALLOCATION - JAY

    def set_camp_id(self):
        self.camp_id = input("Enter camp ID (Not case sensitive)): ").upper()


    def get_camp_population(self):
            try:
                pd_obj = pd.read_csv(self.camps_file)
                # pd_obj is the name for dataframe and we treat it 
                # like array thus result below
                camp = pd_obj[pd_obj['Camp_ID'].str.upper() == self.camp_id]
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
            

    def update_resource_allocation(self, resource_type, quantity):
        try:
            if not isinstance(self.camp_id, str) or not isinstance(resource_type, str):
                raise ValueError("camp_id and resource_type must be strings")

            resources = pd.read_csv(self.resources_file)
            camps = pd.read_csv(self.camps_file)
            if self.camp_id in camps['Camp_ID'].values and self.camp_id in resources['Camp_ID'].values:
                if resource_type in resources.columns:
                    resources.loc[resources['Camp_ID'] == self.camp_id, resource_type] = quantity
                    print(f"Updated {resource_type} for {self.camp_id} to {quantity}.")
                    resources.to_csv(self.resources_file, index=False)
                else:
                    raise ValueError(f"Invalid resource type: {resource_type}")
            else:
                print(f"Camp ID {self.camp_id} does not exist in the resources or camps file.")

        except Exception as e:
            print(f"Error in update_resource_allocation: {e}")


    def suggest_resources(self, duration_days=7):
        population = self.get_camp_population()
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

            return {"food_pac": total_food_needed, "medical_sup": total_medical_kits_needed, "tents": total_tents_needed}
        else:
            print(f"No suggestions for Camp_ID {self.camp_id} with population 0.")
            return {}


    def manual_resource_allocation(self):
        if not self.camp_id:
            self.set_camp_id()
        suggested_resources = self.suggest_resources()
        for resource_type, suggested_quantity in suggested_resources.items():
            print(f"Suggested quantity for {resource_type}: {suggested_quantity}")
            while True:
                user_input = input(f"Enter quantity for {resource_type} (press Enter to accept suggestion): ")
                if not user_input:
                    quantity = suggested_quantity
                    break
                else:
                    try:
                        quantity = int(user_input)
                        if quantity >= 0:
                            break
                        else:
                            print("Please enter a non-negative integer.")
                    except ValueError:
                        print("Invalid input. Please enter a valid integer.")
            self.update_resource_allocation(resource_type, quantity)


if __name__ == "__main__":
    # from resource allocation - E - Jay
    admin = Admin()
    admin.set_camp_id()
    population = admin.get_camp_population()
    print(f"Number of refugees for camp {admin.camp_id}: {population}")
    admin.manual_resource_allocation()
