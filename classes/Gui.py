import tkinter as tk
from tkinter import messagebox
import csv
import re

def main():
    register_gui()

def register_gui():
    root = tk.Tk()
    root.title("User Registration")

    username_label = tk.Label(root, text = "Username:")
    username_entry = tk.Entry(root)

    password_label = tk.Label(root, text = "Password:")
    password_entry = tk.Entry(root, show = "*")

    register_button = tk.Button(root, text = "Register", command = lambda: register(username_entry.get(), password_entry.get(), root))

    username_label.pack()
    username_entry.pack()

    register_button.pack()

    root.mainloop()

def register (username, password,root):
    try:
        validate_username(username)
        validate_password(password)
         
        with open ("./files/logindetails.csv", "a") as file:
            file.write(f"{username},{password},{True}\n")
        
        messagebox.showinfo("Success", "Registration successful!")
        root.destroy()

    except ValueError as e:
        messagebox.showerror("Error", str(e))

def validate_username(username):
    pass

def validate_password(password):
    pass

if __name__ == "__main__":
    main()

