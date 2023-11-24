import tkinter as tk
from tkinter import messagebox
import csv
import re

class UserRegistration:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("User Registration")

        self.username_label = tk.Label(self.root, text = "Username:\n\nYour username should be between 8 and 16 characters long and only consist of letters a-z and numbers 0-9")
        self.username_entry = tk.Entry(self.root)

        self.first_name_label = tk.Label(self.root, text = "\nFirst Name:")
        self.first_name_entry = tk.Entry(self.root)
    
        self.password_label = tk.Label(self.root, text = "\nPassword:\n\nYour password should contain at least one capital letter, at least one of '?' or '!',\nletters a-z and numbers 0-9 and be between 8 and 16 characters long")
        self.password_entry = tk.Entry(self.root, show = "*")

        self.register_button = tk.Button(self.root, text = "Register", command=self.register)

        self.username_label.pack()
        self.username_entry.pack()

        self.first_name_label.pack()
        self.first_name_entry.pack()

        self.password_label.pack()
        self.password_entry.pack()

        self.register_button.pack()

        self.root.mainloop()

    def register (self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            self.validate_username(username)
            self.validate_password(password)
         
            with open ("intro-programming/files/logindetails.csv", "a") as file:
                file.write(f"{username},{password},{True}\n")
        
            messagebox.showinfo("Success", "Registration successful!")
            self.root.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def validate_username(self,username):
        with open("intro-programming/files/logindetails.csv", "r") as file:
            file_reader = csv.reader(file)
            next(file_reader)
            for row in file_reader:
                if username == row[0]:
                    raise ValueError("This username already exists. Please try an alternative username.")
                else:
                    continue
            
        if " " in username:
            raise ValueError("Do not enter spaces in your username.")
        elif len(username) < 8 or len(username) > 16:
            raise ValueError("Please ensure that your username is between 8 and 16 characters long.")
        elif username.isalnum() == False:
            raise ValueError("Please ensure that your username contains only numbers and letters.")

    def validate_password(self,password):
        pw_chars = r'^[A-Za-z0-9!?]+$'
        punc_chars = r'[!?]'
        if " " in password:
            raise ValueError("Do not enter spaces in your password.")
        elif len(password) < 8 or len(password) > 16:
            raise ValueError("Please ensure that your password is between 8 and 16 characters long.")
        elif not any(c.isupper() for c in password):
            raise ValueError("Please ensure that your password contains at least one capital letter.")
        elif not re.match(pw_chars, password) or not re.search(punc_chars, password):
            raise ValueError("Please ensure that your password contains only letters a-z, numbers 0-9, and at least one of '!' or '?'.")

if __name__ == "__main__":
    registration = UserRegistration()

