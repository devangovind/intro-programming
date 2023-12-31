import pandas as pd
import matplotlib.pyplot as plt
from FileManager import FileManager
from Plans import Plans

class Camps:
    def __init__(self):
        csv_manager = FileManager()
        self.camps_filepath = csv_manager.get_file_path('camps_file.csv')  # Update to the path where camps.csv is located
        self.resource_filepath = csv_manager.get_file_path('resources.csv')
        

    def get_data(self):
        self.camps_data = pd.read_csv(self.camps_filepath)
        return self.camps_data
    
    def get_camp_ids(self):
        camps_df = pd.read_csv(self.camps_filepath)
        return camps_df['Camp_ID'].tolist()
    def valid_camps_ids(self):
        self.camps_data = pd.read_csv(self.camps_filepath)
        self.Plans = Plans()
        valid_plans = self.Plans.valid_plans_ids()
        valid_camps = []
        for index, row in self.camps_data.iterrows():
            if row['Plan_ID'] in valid_plans:
                valid_camps.append(row['Camp_ID'])
        return valid_camps
        
    def write_data(self, camp_id, new_row):
        self.camps_data = pd.read_csv(self.camps_filepath)  # Ensure the DataFrame is up-to-date
        camp_index = self.camps_data.index[self.camps_data['Camp_ID'] == camp_id].tolist()
        if camp_index:
            self.camps_data.iloc[camp_index[0], :] = new_row
            self.camps_data.to_csv(self.camps_filepath, index=False)
            return True
        else:
            return False
    def write_data_frame(self, df):
        df.to_csv(self.camps_filepath, index=False)
    def append_df(self, df):
        df.to_csv(self.camps_filepath, mode="a", index=False, header=False)
    
    def display_camp_resources(self, camp_id):
        # Load the data from both CSV files
        camp_data = pd.read_csv(self.camps_filepath)
        resources_data = pd.read_csv(self.resource_filepath)

        # Merge the two datasets on Camp_ID
        merged_data = pd.merge(camp_data, resources_data, on='Camp_ID', how='inner')
        
        # Filter the merged data for the specified camp_id
        camp_resources = merged_data[merged_data['Camp_ID'] == camp_id]

        if camp_resources.empty:
            return "No data available for the specified camp"
        else:
            # Displaying the merged data
            return camp_resources
    
    def display_all_camp_resources(self):
        try:
            # Load the data from both CSV files
            camp_data = pd.read_csv(self.camps_filepath)
            resources_data = pd.read_csv(self.resource_filepath)

            # Merge the two datasets on Camp_ID
            all_camps_resources = pd.merge(camp_data, resources_data, on='Camp_ID', how='inner')

            # Check if the merged data is empty
            if all_camps_resources.empty:
                return pd.DataFrame()  # Return an empty DataFrame if no data is available
            else:
                # Return the merged data for all camps
                return all_camps_resources
        except Exception as e:
            print(f"An error occurred while trying to display all camp resources: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of error
        
    def get_resource_data(self, camp_id):
        resource_array = ["0", "0", "0"]
        
        # for mac
        resource_data = pd.read_csv(self.resource_filepath)
        
        # for windows
        # resource_data = pd.read_csv(self.resource_filepath)
        try:
            resource_array[0] = (resource_data['food_pac'][resource_data['Camp_ID'] == camp_id].iloc[0])
            resource_array[1] = (resource_data['medical_sup'][resource_data['Camp_ID'] == camp_id].iloc[0])
            resource_array[2] = (resource_data['tents'][resource_data['Camp_ID'] == camp_id].iloc[0])
        except:
            pass
        return resource_array


# Testing the Camps class
if __name__ == "__main__":
    camps = Camps()
    x = camps.display_all_camp_resources()
    print(x)