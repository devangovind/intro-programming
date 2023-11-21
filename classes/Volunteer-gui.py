import tkinter as tk
from tkinter import messagebox
from Volunteer import Volunteer
from Camps import Camps
# UPDATE FOR ADMIN DASHBOARD
class VolunteerGui:
    def __init__(self, volunteer):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Volunteer View")
        self.volunteer = volunteer
        self.volunteer_data = self.volunteer.get_volunteer_data()
        self.create_nav_bar()
        self.welcome_message()
        # self.edit_details_button = tk.Button(self.root, text="Edit personal details", font=('Arial', 20))
    def create_nav_bar(self):
        # update nav bar with approariate button names
        self.headerarea = tk.Frame(self.root)
        self.headerarea.columnconfigure(0, weight=1)
        self.headerarea.columnconfigure(1, weight=1)
        self.headerarea.columnconfigure(2, weight=1)
        self.headerarea.columnconfigure(3, weight=1)
        self.headerarea.columnconfigure(4, weight=1)
        self.headerarea.columnconfigure(5, weight=1)
        self.home_btn = tk.Button(self.headerarea, text="Home", font=('Arial', 16), command=self.welcome_message)
        self.home_btn.grid(row=0, column=0)
        self.edit_details_btn = tk.Button(self.headerarea, text="Edit Personal Details", font=('Arial', 16), command=self.edit_details)
        self.edit_details_btn.grid(row=0, column=1)
        self.edit_camp_btn = tk.Button(self.headerarea, text="Edit Camp Details", font=('Arial', 16), command=self.edit_camp)
        self.edit_camp_btn.grid(row=0, column=2)
        self.view_camp_btn = tk.Button(self.headerarea, text="View Camp Details", font=('Arial', 16))
        self.view_camp_btn.grid(row=0, column=3)
        self.add_refugee_btn = tk.Button(self.headerarea, text="Create Refugee Profile", font=('Arial', 16))
        self.add_refugee_btn.grid(row=0, column=4)
        self.logout_btn = tk.Button(self.headerarea, text="Logout", font=('Arial', 16))
        self.logout_btn.grid(row=0, column=5)
        self.headerarea.pack(padx=20)
        self.nav_bar = [self.headerarea, self.home_btn,self.edit_camp_btn, self.edit_details_btn, self.view_camp_btn, self.add_refugee_btn, self.logout_btn]
    def welcome_message(self):
        self.clear_content()
        welcome_back = f'Welcome Back, {self.volunteer.username}'
        label = tk.Label(self.root, text=welcome_back, font=('Arial', 24))
        label.pack(pady=100)
    def edit_details(self):
        self.clear_content()
        # edit function name and add code here
    def submit_details(self):
        # validation of data from previous function
        pass
    def edit_camp(self):
        pass
    # add fuuunction here

    def submit_camp(self):
        # add code here
        pass

    def clear_content(self):
        for widget in self.root.winfo_children():
            if widget not in self.nav_bar:
                widget.destroy()
    def run(self):
    
        self.root.mainloop()

dummy = Volunteer("volunteer1")
VGui = VolunteerGui(dummy)
VGui.run()