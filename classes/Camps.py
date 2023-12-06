import pandas as pd
class Camps:
    def __init__(self):
        # self.camps_data = pd.read_csv('./files/camps_file.csv')
        #for windows:
        self.camps_filepath = '../files/camps_file.csv'
        self.camps_data = pd.read_csv(self.camps_filepath)
        self.resource_filepath = '../files/resources.csv'
        self.resource_data = pd.read_csv(self.resource_filepath)

    def get_data(self):
        return self.camps_data
    def write_data(self, camp_id, new_row):
        camp_index = self.camps_data.index[self.camps_data['camp_id'] == camp_id]
        self.camps_data.iloc[camp_index, :] = new_row
        self.camps_data.to_csv(self.camps_filepath, index=False)
        return True
    def get_resource_data(self, camp_id):
        resource_array = ["0", "0", "0"]
        resource_data = pd.read_csv(self.resource_filepath)
        try:
            resource_array[0] = (resource_data['food_pac'][resource_data['Camp_ID'] == camp_id].iloc[0])
            resource_array[1] = (resource_data['medical_sup'][resource_data['Camp_ID'] == camp_id].iloc[0])
            resource_array[2] = (resource_data['tents'][resource_data['Camp_ID'] == camp_id].iloc[0])
        except:
            pass
        return resource_array
