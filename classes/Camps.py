import pandas as pd
import matplotlib.pyplot as plt

class Camps:
    def __init__(self):
        # Filepaths for windows
        self.camps_filepath = "../files/camps_file.csv"  # Update to the path where camps.csv is located
        self.resource_filepath = "../files/resources.csv"

        # Filepaths for MAC
        # self.camps_filepath = "intro-programming/files/camps_file.csv"  # Update to the path where camps.csv is located
        # self.resource_filepath = "intro-programming/files/resources.csv"

    def get_data(self):
        self.camps_data = pd.read_csv(self.camps_filepath)
        return self.camps_data
    
    def get_camp_ids(self):
        camps_df = pd.read_csv(self.camps_filepath)
        return camps_df['Camp_ID'].tolist()
        
    def write_data(self, camp_id, new_row):
        self.camps_data = pd.read_csv(self.camps_filepath)  # Ensure the DataFrame is up-to-date
        camp_index = self.camps_data.index[self.camps_data['Camp_ID'] == camp_id].tolist()
        if camp_index:
            self.camps_data.iloc[camp_index[0], :] = new_row
            self.camps_data.to_csv(self.camps_filepath, index=False)
            return True
        else:
            return False
    
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
        

    # def dataVis(self):
    #     # resources_data = pd.read_csv(self.resource_filepath)
    #     # plt.pie(resources_data, autopct="%1.1f%%")

    #     # plt.title("My Tasks")
    #     # plt.axis("equal")

    #     # plt.show()
    #     my_data = [300, 500, 700]
    #     my_labels = ["Tasks Pending", "Tasks Ongoing", "Tasks Completed"]

    #     plt.pie(my_data, labels=my_labels, autopct="%1.1f%%")

    #     plt.title("My Tasks")
    #     plt.axis("equal")

    #     plt.show()

# Testing the Camps class
if __name__ == "__main__":
    camps = Camps()
    
    # # Test getting camp data
    # data = camps.get_data()
    # print("Camp Data:")
    # print(data)
    
    # # Test getting camp IDs
    # camp_ids = camps.get_camp_ids()
    # print("\nCamp IDs:")
    # print(camp_ids)
    
    # # Test writing data
    # # This is a placeholder for new_row which you need to replace with the actual data format you expect.
    # new_row = data.iloc[0].copy()  # Let's just use the first row as a dummy new row for testing
    # new_row['population'] += 1  # Incrementing population for testing
    # write_result = camps.write_data(camp_ids[0], new_row)
    # print("\nWrite Result:")
    # print(write_result)
    
    # # Re-fetch data to confirm write
    # updated_data = camps.get_data()
    # print("\nUpdated Camp Data:")
    # print(updated_data)

    # print(camps.display_camp_resources('C12345'))
    camps.dataVis()