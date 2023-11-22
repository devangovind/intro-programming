# Admin Class File
import pandas as pd


class Admin:
  # add functions here
  # remember for functions added the first parameter has to be a self
    def create_humanitarian_plan(self):
        pass

    def __init__(self):
        self.login_file = './files/logindetails.csv'
        self.users = pd.read_csv(self.login_file)


    def save_changes(self):
        self.users.to_csv(self.login_file, sep=',', index=False, encoding='utf-8')
        return "Saved changes"


    def activate_account(self, username):
        try:
            if username in self.users['Username'].values:
                if self.users.loc[self.users['Username'] == username, 'Active'].iloc[0] != True: # iloc[0] ensures that 'Active' column is selected 
                    self.users.loc[self.users['Username'] == username, 'Active'] = True
                    self.save_changes()
                    return 'Your account has been activated'
                else:
                    return 'Your account has already been activated'
        except KeyError:
            return "Account doesn't exist"


    def activate_all(self):
        self.users['Active'] = True
        return "All accounts have been activated"


    def deactivate_account(self, username):
        try:
            if username in self.users['Username'].values:
                if self.users.loc[self.users['Username'] == username, 'Active'].iloc[0] == True:
                    self.users.loc[self.users['Username'] == username, 'Active'] = False
                    self.save_changes()
                    return "Your account has been deactivated, contact the administrator."
                else:
                    return "Your account has already been deactivated"
        except KeyError:
            return "Account doesn't exist"

    def deactivate_all(self):
        self.users['Active'] = False
        return "All accounts have been deactivated"


    def delete_account(self, username):
        try:
            if username in self.users['Username'].values:
                self.users = self.users[self.users['Username'] != username]  # Filter out the user to be deleted
                self.save_changes()
                return f"Account {username} deleted"
            else:
                return "Account doesn't exist"
        except KeyError:
            return "Account doesn't exist"

if __name__ == "__main__":
    admin = Admin()
    print(admin.users)

    print(admin.deactivate_all())
    print(admin.users)

    
    print(admin.activate_all())
    print(admin.users)
    
    print(admin.deactivate_account('volunteer1'))
    print(admin.users)
    
    print(admin.activate_account('volunteer1'))
    print(admin.users)

    #print(admin.delete_account('volunteer3'))
    #print(admin.users)
