# Admin Class File
import datetime
import csv
import pandas as pd
from datetime import date
from datetime import datetime
import csv


class Admin:
  # add functions here
  # remember for functions added the first parameter has to be a self
  def create_humanitarian_plan(self):
    pass

  def __init__(self):
      self.camps_file = '../files/camps_file.csv'
      self.plans_file = '../files/plans_file.csv'
      self.resources_file = '../files/resources.csv'
      self.camp_id = None

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

  # FOR RESOURCE ALLOCATION
  def read_csv(self, filepath):
    try:
        with open(filepath, mode='r', encoding='utf-8-sig') as file:  # 'utf-8-sig' handles the BOM
            return list(csv.DictReader(file))
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return []

  def write_csv(self, filepath, data):
      try:
          with open(filepath, mode='w', newline='') as file:
              writer = csv.DictWriter(file, fieldnames=data[0].keys())
              writer.writeheader()
              writer.writerows(data)
      except Exception as e:
          print(f"Error writing file {filepath}: {e}")

  def set_camp_id(self):
      self.camp_id = input("Enter camp ID: ")

  def get_camp_population(self):
    try:
        camps = self.read_csv(self.camps_file)
        for camp in camps:
            # print(f"Checking camp: {camp}")  # Debugging print
            if 'camp_id' in camp and camp['camp_id'] == self.camp_id:
                population = int(camp['population'])
                # print(f"Population of {self.camp_id}: {population}")  # Show population
                return population
        print(f"Camp ID: {self.camp_id} not found.")
        return 0
    except Exception as e:
        print(f"Error in get_camp_population: {e}")
        return 0

  def update_resource_allocation(self, resource_type, quantity):
    try:
        if not isinstance(self.camp_id, str) or not isinstance(resource_type, str):
            raise ValueError("camp_id and resource_type must be strings")

        resources = self.read_csv(self.resources_file)
        camp_exists = False
        for column in resources:
            if column.get('camp_id') == self.camp_id:
                camp_exists = True
                if resource_type in column:
                    column[resource_type] = quantity
                    print(f"Updated {resource_type} for {self.camp_id} to {quantity}.")
                    self.write_csv(self.resources_file, resources)
                    return
                else:
                    raise ValueError(f"Invalid resource type: {resource_type}")

        if not camp_exists:
            print(f"Camp ID {self.camp_id} does not exist in the file.")

    except Exception as e:
        print(f"Error in update_resource_allocation: {e}")


  def suggest_resources(self, duration_days=7):
    population = self.get_camp_population()
    if population > 0:
        # Define basic needs
        food_per_person_per_day = 3  # e.g., 3 food packets per person per day
        medical_kits_per_10_people_per_day = 0.1  # e.g., 1 kit per 10 people per day
        people_per_tent = 5  # e.g., Assuming 5 people per tent

        # Calculate total needs
        total_food_needed = food_per_person_per_day * population * duration_days
        total_medical_kits_needed = medical_kits_per_10_people_per_day * population * duration_days
        total_tents_needed = -(-population // people_per_tent)  # Ceiling division for tents

        # Add a buffer (e.g., 20%)
        buffer = 1.20
        total_food_needed = int(total_food_needed * buffer)
        total_medical_kits_needed = int(total_medical_kits_needed * buffer)
        total_tents_needed = int(total_tents_needed * buffer)

        return {"food_pac": total_food_needed, "medical_sup": total_medical_kits_needed, "tents": total_tents_needed}
    else:
        print(f"No suggestions for camp_id {self.camp_id} with population 0.")
        return {}


  def manual_resource_allocation(self):
      if not self.camp_id:
          self.set_camp_id()
      suggested_resources = self.suggest_resources()
      for resource_type, suggested_quantity in suggested_resources.items():
          print(f"Suggested quantity for {resource_type}: {suggested_quantity}")
          user_input = input(f"Enter quantity for {resource_type} (press Enter to accept suggestion): ")
          quantity = int(user_input) if user_input else suggested_quantity
          self.update_resource_allocation(resource_type, quantity)

if __name__ == "__main__":
    admin = Admin()
    admin.set_camp_id()  # Set camp_id once
    x = admin.get_camp_population()
    print(f"Population of {admin.camp_id}: {x}")
    admin.manual_resource_allocation() 

