# Admin Class File
import csv
import datetime


class Admin:
  # add functions here
  # remember for functions added the first parameter has to be a self

  def create_humanitarian_plan(self):
    pass




  def __init__(self):
        self.camps_file = 'files/camps.csv'
        self.resources_file = 'files/resources.csv'
        self.camp_id = None
        self.sdate_save = None
        self.date_save = None
        self.month = None
        self.year = None



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
            if 'camp_id' in camp and camp['camp_id'] == self.camp_id:
                return int(camp['population'])
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


if __name__ == "__main__":
    admin = Admin()
    admin.set_camp_id()  # Set camp_id once
    admin.manual_resource_allocation() 

    sdate = Admin().set_valid_sdate()
    edate = Admin().set_valid_eedate(sdate)
    save_date(sdate, edate)
    Admin().read_date()