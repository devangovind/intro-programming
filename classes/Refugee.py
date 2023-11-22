import pandas as pd
from Camps import Camps

class Refugee:
    def __init__(self) -> None:
        self.refugee_path = "intro-programming/files/refugee.csv"
    
    def generate_refugee_id(self):
        refugee_data = pd.read_csv(self.refugee_path)
        # Extract the numeric part of the Refugee_ID
        last_id_series = refugee_data['Refugee_ID'].str.extract(r'(\d+)', expand=False).astype(int)
        last_id = last_id_series.max()
        new_id = f'R{str(last_id + 1).zfill(3)}'  # Increment and format
        return new_id

    def create_refugee_profile_auto_id(self, camp_id, medical_condition, num_relatives):
        new_refugee_id = self.generate_refugee_id()
        return self.create_refugee_profile(new_refugee_id, camp_id, medical_condition, num_relatives)
    
    def create_refugee_profile(self, camp_id, medical_condition, num_relatives, refugee_id=None):
        refugee_data = pd.read_csv(self.refugee_path)
        
        if refugee_id is None:
            refugee_id = self.generate_refugee_id()
        elif refugee_id in refugee_data['Refugee_ID'].values:
            return "Refugee already exists"
        
        new_refugee = pd.DataFrame({
            'Refugee_ID': [refugee_id],
            'Camp_ID': [camp_id],
            'MedicalCondition': [medical_condition],
            'NumberOfRelatives': [num_relatives]
        })

        refugee_data = pd.concat([refugee_data, new_refugee], ignore_index=True)
        
        try:
            refugee_data.to_csv(self.refugee_path, index=False)
            print(f"Refugee profile for {refugee_id} created and written to CSV successfully.")
            return "Refugee profile created successfully"
        except Exception as e:
            print(f"An error occurred while writing to the CSV: {e}")
            return "Failed to write refugee profile to CSV"
        
   
if __name__ == "__main__":
    refugee = Refugee()
    
    # Example usage of create_refugee_profile_auto_id method
    result = refugee.create_refugee_profile('C24356','Need attention',4)

    print(result)


