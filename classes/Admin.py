# Admin Class File
import pandas as pd
import csv
import datetime 

class Admin:
    def __init__(self):
            with open('C:\\Users\\96249\Desktop\\Python_CW\\intro-programming\\files\\plan_file.csv', 'r', encoding='utf-8') as plan_file:
                read = csv.DictReader(plan_file)
                self.plan_list = []
                for row in read:
                    self.plan_list.append(row)
            # print(plan_list)
            self.camps_file = 'intro-programming/files/camps_file.csv'
            self.resources_file = 'intro-programming/files/resources.csv'
            self.camp_id = None




## Change some functions to fit the admin.gui(for admin feature a-c)
## This is to find the last plan_id, in ortder to achive planid plus one when admin create a new plan 
    def last_plan_id(self):
        plan = pd.read_csv("C:\\Users\\96249\\Desktop\\Python_CW\\intro-programming\\files\plan_file.csv")

        res = plan.sort_values(by='Plan_ID', ascending=False)
        last_plan_id = int(res.iloc[0]["Plan_ID"])
        # print(res.iloc[0]["Plan_ID"])
        return last_plan_id

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
    # def plan_id_plus_1(self):
    #     self.plan_id  = self.plan_id + 1
    #     return str(self.plan_id)

## This is to refresh the plan after creating a plan 
    def insert_new_plan(self, new_plan):
        self.plan_list.append(new_plan)

    






    
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
    admin = Admin()
    admin.set_camp_id()
    population = admin.get_camp_population()
    print(f"Number of refugees for camp {admin.camp_id}: {population}")
    admin.manual_resource_allocation()