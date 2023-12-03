import pandas as pd
from Camps import Camps

class Refugee:
    def __init__(self) -> None:
        # Filepaths for windows
        self.refugee_path = "./files/refugee.csv"
        self.camps_path = "./files/camps_file.csv"
        self.medical_conditions_path = "./files/medical_conditions.csv"

        # Filepaths for MAC
        # self.refugee_path = "intro-programming/files/refugee.csv"
        # self.camps_file = "intro-programming/files/camps_file.csv"
        # self.medical_conditions = "intro-programming/files/medical_conditions.csv"
    
    def generate_refugee_id(self):
        refugee_data = pd.read_csv(self.refugee_path)
        # Extract the numeric part of the Refugee_ID
        last_id_series = refugee_data['Refugee_ID'].str.extract(r'(\d+)', expand=False).astype(int)
        last_id = last_id_series.max()
        new_id = f'R{str(last_id + 1).zfill(3)}'  # Increment and format
        return new_id

    def create_refugee_profile_auto_id(self, camp_id, medical_status, medical_condition, medical_description, num_relatives):
        new_refugee_id = self.generate_refugee_id()
        return self.create_refugee_profile(new_refugee_id, camp_id, medical_status, medical_condition, medical_description, num_relatives)
    
    def create_refugee_profile(self, camp_id, medical_status, medical_condition, medical_description, num_relatives, refugee_id=None):
        refugee_data = pd.read_csv(self.refugee_path)
        
        if refugee_id is None:
            refugee_id = self.generate_refugee_id()
        elif refugee_id in refugee_data['Refugee_ID'].values:
            return "Refugee already exists"
    
        

        new_refugee = pd.DataFrame({
            'Refugee_ID': [refugee_id],
            'Camp_ID': [camp_id],
            'MedicalStatus': [medical_status],
            'MedicalCondition': [medical_condition],
            'MedicalDescription': [medical_description],
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

    def update_camp_info(self, refugee_id):
        refugee_data = pd.read_csv(self.refugee_path)
        selected_refugee = refugee_data.loc[refugee_data['Refugee_ID'] == refugee_id]
        if selected_refugee.empty:
            return "Refugee not found"

        camp_id = selected_refugee['Camp_ID'].values[0]
        num_relatives = selected_refugee['NumberOfRelatives'].values[0]

        camp_info = pd.read_csv(self.camps_path)
        camp = camp_info.loc[camp_info['Camp_ID'] == camp_id]

        if camp.empty:
            return "Camp not found"

        camp_capacity = camp['Capacity'].values[0]
        current_num_refugees = camp['Num_Of_Refugees'].values[0]

        if current_num_refugees + num_relatives + 1 < camp_capacity:
            camp_info.loc[camp_info['Camp_ID'] == camp_id, 'Num_Of_Refugees'] += (num_relatives + 1)
            try:
                camp_info.to_csv(self.camps_path, index=False)
                print(f"Number of refugees for {camp_id} updated and written to CSV successfully.")
                return "Camp information updated successfully"
            except Exception as e:
                print(f"An error occurred while writing to the CSV: {e}")
                return "Failed to update camp information"
        elif current_num_refugees + num_relatives + 1 == camp_capacity:
            camp_info.loc[camp_info['Camp_ID'] == camp_id, 'Num_Of_Refugees'] += (num_relatives + 1)
            try:
                camp_info.to_csv(self.camps_path, index=False)
                print(f"Number of refugees for {camp_id} updated and written to CSV successfully. Camp is now full.")
                return "Camp information updated successfully, camp is now full."
            except Exception as e:
                print(f"An error occurred while writing to the CSV: {e}")
                return "Failed to update camp information"
        else:
            return "Camp is full"

    def get_medical_conditions(self):
        medical_conditions = pd.read_csv(self.medical_conditions_path)
        return medical_conditions['NameOfCondition'].tolist()
   
if __name__ == "__main__":
    refugee = Refugee()
    
    # Example usage of create_refugee_profile_auto_id method
    result = refugee.create_refugee_profile('C12345','Healthy', None, None,4)
    refugee.update_camp_info("R001")
    print(result)