# login py file
import csv
# csvfile = open('./files/logindetails.csv', 'w', newline='')
#     # 'w' stands for write mode
#     # 'newline=''': This is important to avoid blank lines between rows in some systems
# csv_writer = csv.writer(csvfile)
# csv_writer.writerow(['Username', 'Password', 'Active'])

# # Writing multiple rows
# csv_writer.writerows([
#     ['admin', "111", True],
#     ['volunteer1', "111", False],
#     ['volunteer2', "111", True],
#     ['volunteer3', "111", True]
# ])
# csvfile.close()
def login(username, password) -> (bool,str):
    '''
    Login function with passed in username and password. 
    Returns a boolean value to determine logged in status
    Returns a message to be displayed to user
    '''
    users_file = open('./files/logindetails.csv', 'r')
    csv_reader = csv.reader(users_file)
    header = next(csv_reader)
    for row in csv_reader:
        if username == row[0] and password == row[1]:
            if row[2] == 'True':
                users_file.close()
                return True, f"Logged in sucessfully. Welcome back {username}"
            users_file.close()
            return False, "Account has been deactivated, contact system administrator"
        elif username == row[0]:
            users_file.close()
            return False, "Incorrect password"
    users_file.close()
    return False, "Account does not exist"

print(login("volunteer1", "111"))
print(login("volunteer2", "111"))
print(login("volunteer5", "111"))
print(login("admin", "111"))