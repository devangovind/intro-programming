import pandas as pd
class Camps:
    def __init__(self):
        self.camps_data = pd.read_csv('files\\camps_file.csv')
    def get_data(self):
        return self.camps_data
    def write_data(self, camp_id, new_row):
        camp_index = self.camps_data.index[self.camps_data['camp_id'] == camp_id]
        self.camps_data.iloc[camp_index, :] = new_row
        self.camps_data.to_csv('files\\camps_file.csv', index=False)
        return True
    def get_resource_data(self, camp_id):
        resource_array = ["0", "0", "0"]
        resource_data = pd.read_csv('files\\camps_file.csv')
        try:
            resource_array[0] = (resource_data['food_pac'][resource_data['Camp_ID'] == camp_id].iloc[0])
            resource_array[1] = (resource_data['medical_sup'][resource_data['Camp_ID'] == camp_id].iloc[0])
            resource_array[2] = (resource_data['tents'][resource_data['Camp_ID'] == camp_id].iloc[0])
        except:
            pass
        return resource_array