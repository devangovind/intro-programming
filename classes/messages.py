# Messages Class File
import pandas as pd
import csv
import datetime
class Messages:
    def __init__(self):
        # for Mac
        self.messages_file = 'messages.csv'
        self.messages_data = pd.read_csv(self.messages_file)
        
        # for windows:
        # self.plans_file = 'files\\plan_file.csv'
        # self.plans_filepath = '../files/plans_file.csv'
        # self.plans_data = pd.read_csv(self.plans_filepath)
   
    def get_recieved_messages(self, volunteer):
        self.messages_data = pd.read_csv(self.messages_file)
        return self.messages_data[self.messages_data['volunteer_reciever'] == volunteer]
    def get_sent_messages(self, volunteer):
        self.messages_data = pd.read_csv(self.messages_file)
        return self.messages_data[self.messages_data['volunteer_sender'] == volunteer]
    def get_all(self, volunteer):
        self.messages_data = pd.read_csv(self.messages_file)
        condition_1 = (self.messages_data['volunteer_sender'] == volunteer) | (self.messages_data['volunteer_receiver'] == volunteer)
        return self.messages_data[condition_1]
    def get_all_sender_receiver(self, volunteer1, volunteer2):
        self.messages_data = pd.read_csv(self.messages_file)
        condition_1 = (self.messages_data['volunteer_sender'] == volunteer1) & (self.messages_data['volunteer_receiver'] == volunteer2)
        condition_2 = (self.messages_data['volunteer_sender'] == volunteer2) & (self.messages_data['volunteer_receiver'] == volunteer1)
        filtered_data = self.messages_data[condition_1 | condition_2]
        return filtered_data
    def send_message(self, sender, receiver, time, message):
        new_row = pd.DataFrame({'volunteer_sender': [sender], 'volunteer_receiver': [receiver], 'timestamp': [time], 'message': [message]})
        new_row.to_csv(self.messages_file, mode="a", header=False, index=False)
    def write_data(self, plan_id, new_row):
        camp_index = self.plans_data.index[self.plans_data['plan_id'] == plan_id]
        self.plans_data.iloc[camp_index, :] = new_row
        
        # for mac
        self.plans_data.to_csv(self.plans_file, index=False)
        
        # for windows
        # self.plans_data.to_csv(self.plans_filepath, index=False)
        
        return True


class humanitarian_plan:
    def __init__(self, description, geographical_location, start_date):
        self.description = description
        self.geographical_location = geographical_location
        self.start_date = start_date
    
    def display_plan(self):
        return{
        "Description": self.description,
        "Geographical Location": self.geographical_location,
        "Start Date": self.start_date
        }




       