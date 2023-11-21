import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import ttkbootstrap as tb
import csv

# these functions are NOT in class because they are used in different classes to validate admin and volunteers
def user_valid(username, acct_type):
    with open("../files/logindetails.csv", "r") as file:
        file_reader = csv.reader(file)
        for row in file_reader:
            if username == row[0]:
                # check if account is active first and is of correct account type
                if row[2] == 'TRUE' and row[3] == acct_type:
                    return row
                else:
                    return ""
            else:
                continue
        return ""
    
def password_valid(password, credentials):
    if credentials[1] == password:
        return True
    else:
        return False

# class Login for Login page
class Login:
    # Login page configuration
    def __init__(self, master):
        self.root = master
        self.root.geometry("1000x600")
        self.root.title("Welcome to the Humanitarian Management System")

        #each tab is in a notebook and each tab is its own frame
        self.notebook = ttk.Notebook(master)
        self.notebook.pack()

        # Admin Tab
        self.admin_frame = Frame(self.notebook, pady=150, padx=200)
        self.admin_frame.pack(fill="both", expand=1)
        self.notebook.add(self.admin_frame, text="Admin")
        self.admin_caption = Label(self.admin_frame, text="Welcome to the Humanitarian Management System Portal", font=20)
        self.admin_caption.grid(row=0, column=0)
        self.admin_caption2 = Label(self.admin_frame, text="Login as Admin. Please enter your username and password.")
        self.admin_caption2.grid(row=1, column=0, pady=20)

             # Admin - username
        self.admin_username = Label(self.admin_frame, text="Admin Username:")
        self.admin_username.grid(row=2, column=0)
        self.username_entry = Entry(self.admin_frame, width= 30)
        self.username_entry.grid(row=3, column=0)

             # Admin - password
        self.admin_password = Label(self.admin_frame, text="Admin Password:")
        self.admin_password.grid(row=4, column=0)
        self.password_entry = Entry(self.admin_frame, width= 30)
        self.password_entry.grid(row=5, column=0)

        self.admin_sign_in = Button(self.admin_frame, text="Sign In", command=self.admin_validate)
        self.admin_sign_in.grid(row=6, column=0, pady=20)

        # Volunteer Tab
        self.volunteer_frame = Frame(self.notebook, pady=150, padx=200)
        self.volunteer_frame.pack(fill="both", expand=1)
        self.notebook.add(self.volunteer_frame, text="Volunteer")
        self.volunteer_caption = Label(self.volunteer_frame, text="Welcome to the Humanitarian Management System Portal", font=20)
        self.volunteer_caption.grid(row=0, column=0)
        self.volunteer_caption2 = Label(self.volunteer_frame, text="Sign in as a Volunteer, or register your details if you do not have an account yet.")
        self.volunteer_caption2.grid(row=1, column=0, pady=20)
        self.volunteer_sign_in = Button(self.volunteer_frame, text="Sign In", command=self.volunteer_login_page, width=20)
        self.volunteer_sign_in.grid(row=2, column=0, pady=10)
        self.volunteer_register = Button(self.volunteer_frame, text="Register as Volunteer", command=self.volunteer_register_page, width=20)
        self.volunteer_register.grid(row=3, column=0, pady=10)

    def admin_validate(self):
        # Validate if admin username and pw is correct
        user_type = 'Admin'
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()
        if entered_username != "" and entered_password != "":
            if user_valid(entered_username, user_type) != "":
                correct_credentials = user_valid(entered_username, user_type) 
                if password_valid(entered_password, correct_credentials): # shows admin menu if login is valid
                    Admin_Menu()
                else:
                    messagebox.showerror("Error", "Password is incorrect!")
            else:
                messagebox.showerror("Error", "Username is invalid or User is inactive!")
        else:
            messagebox.showerror("Error", "You have not entered a username or password!")

    def volunteer_login_page(self):
        # display volunteer log in window
        Volunteer_Login()

    def volunteer_register_page(self):
        # display volunteer registration window
        Volunteer_Register()

# class Admin_Menu for Admin page after successful login
class Admin_Menu:
    # Yan's portion
    def __init__(self):
        print("Test admin sign in button")

# class Volunteer_Login for volunteer login page when they select sign in
class Volunteer_Login:
    def __init__(self):
        self.log_in_window = Toplevel()
        self.log_in_window.geometry("500x200+300+300")
        self.log_in_window.resizable(False, False)
        self.log_in_window.title("Login to your Volunteer account")
        self.caption = Label(self.log_in_window, text="Login as Volunteer. Please enter your username and password.")
        self.caption.pack(pady=10)
        self.username = Label(self.log_in_window, text="Volunteer Username:")
        self.username.pack()
        self.username_entry = Entry(self.log_in_window, width= 30)
        self.username_entry.pack()
        self.password = Label(self.log_in_window, text="Volunteer Password:")
        self.password.pack()
        self.password_entry = Entry(self.log_in_window, width= 30)
        self.password_entry.pack()


        sign_in = Button(self.log_in_window, text="Sign In", command= self.volunteer_validate)
        sign_in.pack(pady=20)

    def volunteer_validate(self): # Validate if volunteer username and pw is correct
        user_type = "Volunteer"
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()
        if entered_username != "" and entered_password != "":
            if user_valid(entered_username, user_type) != "":
                correct_credentials = user_valid(entered_username, user_type) 
                if password_valid(entered_password, correct_credentials): #if login is valid
                    self.log_in_window.destroy()
                    Volunteer_Menu()
                else:
                    messagebox.showerror("Error", "Password is incorrect!")
                    self.log_in_window.lift()
            else:
                messagebox.showerror("Error", "Username is invalid or User is inactive!")
                self.log_in_window.lift()
        else:
            messagebox.showerror("Error", "You have not entered a username or password!")
            self.log_in_window.lift()

        
# class Volunteer_Register for volunteer registration page when they select register
class Volunteer_Register: 
    # Gracie's portion
    def __init__(self):
        print("test volunteer register button")

# class Volunteer_Menu for Volunteer page after successful login
class Volunteer_Menu:
    def __init__(self):
        # Devin's portion
        print("This will change the original window to volunteer menu")
        

if __name__ == '__main__':
    root = Tk()
    login_menu = Login(root)
    root.mainloop()