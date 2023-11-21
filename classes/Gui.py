import tkinter as tk
from tkinter import messagebox
import csv
import re

# draft (have some errors and haven't been defined as a class.)

def main():
    register_gui()

def register_gui():
    root = tk.Tk()
    root.title("User Registration")

    username_label = tk.Label(root, text = "Your username should be between 8 and 16 characters long and only consist of letters a-z and numbers 0-9.\n\nPlease enter a username:")
    username_entry = tk.Entry(root)

    password_label = tk.Label(root, text = "\nYour password should contain at least one capital letter, at least one of '?' or '!', letters a-z and numbers 0-9 and be between 8 and 16 characters long.\n\nPlease enter a password: ")
    password_entry = tk.Entry(root, show = "*")

    register_button = tk.Button(root, text = "Register", command = lambda: register(username_entry.get(), password_entry.get(), root))

    username_label.pack()
    username_entry.pack()

    password_label.pack()
    password_entry.pack()

    register_button.pack()

    root.mainloop()

def register (username, password,root):
    try:
        validate_username(username)
        validate_password(password)
         
        with open ("../files/logindetails.csv", "a") as file:
            file.write(f"{username},{password},{True}\n")
        
        messagebox.showinfo("Success", "Registration successful!")
        root.destroy()

    except ValueError as e:
        messagebox.showerror("Error", str(e))

def validate_username(username):
    with open("../files/logindetails.csv", "r") as file:
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

def validate_password(password):
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
    main()

