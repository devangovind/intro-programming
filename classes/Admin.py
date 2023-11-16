# Admin Class File
import csv


class Admin:
  # add functions here
  # remember for functions added the first parameter has to be a self
  def create_humanitarian_plan(self):
    pass

  def __init__(self):
      self.camps_file = '/Users/jiaxinhe/Library/Mobile Documents/com~apple~CloudDocs/UCL CS/Term 1/COMP0066 Introductory to programming/Groupwork/github_location/intro-programming/files/camps.csv'
      self.resources_file = '/Users/jiaxinhe/Library/Mobile Documents/com~apple~CloudDocs/UCL CS/Term 1/COMP0066 Introductory to programming/Groupwork/github_location/intro-programming/files/resources.csv'

  def read_csv(self, filepath):
      with open(filepath, mode='r') as file:
          return list(csv.DictReader(file))

  def write_csv(self, filepath, data):
      with open(filepath, mode='w', newline='') as file:
          writer = csv.DictWriter(file, fieldnames=data[0].keys())
          writer.writeheader()
          writer.writerows(data)

  def get_camp_population(self, camp_id):
    camps = self.read_csv(self.camps_file)
    for camp in camps:
        if 'camp_id' in camp and camp['camp_id'] == camp_id:
            return int(camp['population'])
    return 0

  def update_resource_allocation(self, camp_id, resource_type, quantity):
    if not isinstance(camp_id, str) or not isinstance(resource_type, str):
        raise ValueError("camp_id and resource_type must be strings")

    resources = self.read_csv(self.resources_file)
    updated = False
    for column in resources:
        if column.get('camp_id') == camp_id:
            if resource_type in column:
                column[resource_type] = quantity
                updated = True
            else:
                raise ValueError(f"Invalid resource type: {resource_type}")

    if updated:
        print(f"Updated resources for {camp_id}: {resources}")
        self.write_csv(self.resources_file, resources)
    else:
        print(f"No changes made for {camp_id}. Camp ID may not exist in the file.")



  def allocate_resources(self, camp_id, duration_days=7):
    population = self.get_camp_population(camp_id)
    
    if population > 0:
        # Define basic needs
        food_per_person_per_day = 3  # 3 food packets per person per day
        medical_kits_per_10_people_per_day = 0.1  # 1 kit per 10 people per day
        people_per_tent = 5  # Assuming 5 people per tent

        # Calculate total needs
        total_food_needed = food_per_person_per_day * population * duration_days
        total_medical_kits_needed = medical_kits_per_10_people_per_day * population * duration_days
        total_tents_needed = -(-population // people_per_tent)  # Ceiling division for tents

        # Add a buffer (e.g., 20%)
        buffer = 1.20
        total_food_needed = int(total_food_needed * buffer)
        total_medical_kits_needed = int(total_medical_kits_needed * buffer)
        total_tents_needed = int(total_tents_needed * buffer)

        # Update resource allocation
        self.update_resource_allocation(camp_id, 'food_packets', total_food_needed)
        self.update_resource_allocation(camp_id, 'medical_kits', total_medical_kits_needed)
        self.update_resource_allocation(camp_id, 'tents', total_tents_needed)

        return {"food_packets": total_food_needed, "medical_kits": total_medical_kits_needed, "tents": total_tents_needed}

if __name__ == "__main__":
    admin = Admin()
    camp_id = 'camp_01'
    print(f"Allocating resources for {camp_id}:")
    admin.allocate_resources(camp_id)
    admin.update_resource_allocation(camp_id, 'tents',10)
    print(f"Resources allocated successfully for {camp_id}.")
