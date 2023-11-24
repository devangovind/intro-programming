from Admin import Admin
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from Camps import Camps
from Plans import Plans
import pandas as pd

class AdminGui:
    def __init__(self, admin):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Admin View")
        self.admin = admin
        # self.volunteer_data = self.volunteer.get_volunteer_data()
        self.create_nav_bar()
        self.welcome_message()
        self.camps = Camps()
        self.plans = Plans()
        self.camps_data = self.camps.get_data()
        
        # self.edit_details_button = tk.Button(self.root, text="Edit personal details", font=('Arial', 20))
    def create_nav_bar(self):
        self.headerarea = tk.Frame(self.root)
        self.headerarea.columnconfigure(0, weight=1)
        self.headerarea.columnconfigure(1, weight=1)
        self.headerarea.columnconfigure(2, weight=1)
        self.headerarea.columnconfigure(3, weight=1)
        self.headerarea.columnconfigure(4, weight=1)
        self.headerarea.columnconfigure(5, weight=1)
        self.home_btn = tk.Button(self.headerarea, text="Home", font=('Arial', 16), command=self.welcome_message)
        self.home_btn.grid(row=0, column=0)
        self.create_plan_btn = tk.Button(self.headerarea, text="Create New Plan", font=('Arial', 16), command=self.create_new_plan)
        self.create_plan_btn.grid(row=0, column=1)
        self.display_plans_btn = tk.Button(self.headerarea, text="Display Existing Plans", font=('Arial', 16), command=self.display_plans)
        self.display_plans_btn.grid(row=0, column=2)
        self.manage_camps_btn = tk.Button(self.headerarea, text="Manage Camps", font=('Arial', 16), command=self.manage_camps)
        self.manage_camps_btn.grid(row=0, column=3)
        self.manage_volunteers_btn = tk.Button(self.headerarea, text="Manage Volunteers", font=('Arial', 16), command=self.manage_volunteers)
        self.manage_volunteers_btn.grid(row=0, column=4)
        self.logout_btn = tk.Button(self.headerarea, text="Logout", font=('Arial', 16))
        self.logout_btn.grid(row=0, column=5)
        self.headerarea.pack(padx=20)
        self.nav_bar = [self.headerarea, self.home_btn,self.display_plans_btn, self.create_plan_btn, self.manage_camps_btn, self.manage_volunteers_btn, self.logout_btn]
    def welcome_message(self):
        self.clear_content()
        welcome_back = f'Welcome Back, Admin'
        label = tk.Label(self.root, text=welcome_back, font=('Arial', 24))
        label.pack(pady=100)
    def create_new_plan(self):
        self.clear_content()
        # add the code for creating a new plan here
    def display_plans(self):
        self.clear_content()
        # add code here:
        # somewhere in here will be the end button for the individual plans which will maybe go to another function 

    def manage_camps(self):
        # when data visualisation is ready. we can have each camp name be clickable to bring up a new screen with the data visualised
        self.clear_content()
        title = tk.Label(self.root, text="Manage Camps", font=('Arial', 24))
        title.pack(pady=20)
        plans_data = self.plans.get_data()
        plans_ids = ["All Plans"]
        for val in plans_data['Plan_ID']:
            if val in plans_ids:
                continue
            plans_ids.append(val)
        self.selected_plan = tk.StringVar(self.root)
        self.selected_plan.set(plans_ids[0])
        plans_menu_lbl = tk.Label(self.root, text="Filter By Plan:", font=('Arial', 18))
        plans_menu = tk.OptionMenu(self.root, self.selected_plan, *plans_ids, command=self.filter_camps)
        plans_menu_lbl.pack()
        plans_menu.pack()
        camp_columns = ["Camp ID", "Plan ID", "No. of Volunteers", "No. of Refugees", "Capacity", "Food Packages", "Medical Supplies", "Tents", "Action (Click) ⬇"]
        column_widths = [60, 60, 100, 100, 60, 110, 110, 60, 130]
        self.camps_tree = ttk.Treeview(self.root, columns=camp_columns, show="headings")
        for i in range(len(camp_columns)):
            col = camp_columns[i]
            self.camps_tree.heading(col, text=col)
            self.camps_tree.column(col, stretch=False, width=column_widths[i])
        self.camps_tree.bind("<ButtonRelease-1>", self.allocate_resources)
        self.camps_tree.pack(pady=20)
        self.filter_camps()

    def filter_camps(self, event=None):
        for item in self.camps_tree.get_children():
            self.camps_tree.delete(item)
        selected_plan = self.selected_plan.get()
        if selected_plan == "All Plans": filtered_data = self.camps_data
        else:
            filtered_data = self.camps_data[self.camps_data["Plan_ID"] == selected_plan]
        for index, row in (filtered_data.iterrows()):
            resources = self.camps.get_resource_data(row['Camp_ID'])
            values=[row['Camp_ID'], row['Plan_ID'], row['Num_Of_Volunteers'],row['Num_Of_Refugees'], 50, resources[0], resources[1], resources[2], "Allocate Resources"]
            self.camps_tree.insert("", "end", values=values)
            
    def allocate_resources(self, event):
        item_id = self.camps_tree.selection()
        column = self.camps_tree.identify_column(event.x)
        if item_id and column == "#9":
            row = (self.camps_tree.item(item_id, "values"))
            camp_id = row[0]
            curr_resources = [row[5], row[6], row[7]]
            can_allocate, suggest_resources_dict = self.admin.suggest_resources(camp_id)
            if can_allocate == False:
                messagebox.showinfo("Error", "Chosen camp has 0 population and thus no resources can be allocated")
                self.manage_camps()
            else:
                self.clear_content()
                title_txt = f'Allocate Resources for Camp {camp_id}'
                title = tk.Label(self.root, text=title_txt, font=('Arial', 24))
                title.pack(pady=20)
                suggest_food_text = f'Suggested food supplies: {suggest_resources_dict["food"]}'
                suggest_med_text = f'Suggested medical supplies: {suggest_resources_dict["medical"]}'
                suggest_tents_text = f'Suggested tents: {suggest_resources_dict["tent"]}'
                food_lbl = tk.Label(self.root, text="Edit food supplies:", font=('Arial', 18))
                self.food_inp = tk.Entry(self.root)
                self.food_inp.insert(0, curr_resources[0])
                suggest_food_lbl = tk.Label(self.root, text=suggest_food_text, font=('Arial', 16))
                self.food_error = tk.Label(self.root, text="", fg="red", font=('Arial', 16))
                food_lbl.pack()
                self.food_inp.pack()
                suggest_food_lbl.pack()
                self.food_error.pack(pady=(0,10))
                med_lbl = tk.Label(self.root, text="Edit medical supplies:", font=('Arial', 18))
                self.med_inp = tk.Entry(self.root)
                self.med_inp.insert(0, curr_resources[1])
                suggest_med_lbl = tk.Label(self.root, text=suggest_med_text, font=('Arial', 16))
                self.med_error = tk.Label(self.root, text="", fg="red", font=('Arial', 16))
                med_lbl.pack()
                self.med_inp.pack()
                suggest_med_lbl.pack()
                self.med_error.pack(pady=(0,10))
                tents_lbl = tk.Label(self.root, text="Edit tents:", font=('Arial', 18))
                self.tents_inp = tk.Entry(self.root)
                self.tents_inp.insert(0, curr_resources[2])
                suggest_tents_lbl = tk.Label(self.root, text=suggest_tents_text, font=('Arial', 16))
                self.tents_error = tk.Label(self.root, text="", fg="red", font=('Arial', 16))
                tents_lbl.pack()
                self.tents_inp.pack()
                suggest_tents_lbl.pack()
                self.tents_error.pack(pady=(0,10))
                self.submitframe = tk.Frame(self.root)
                self.submitframe.columnconfigure(0, weight=1)
                self.submitframe.columnconfigure(1, weight=1)
                self.submitframe.columnconfigure(2, weight=1)
                cancel_btn = tk.Button(self.submitframe, text="Cancel", font=('Arial', 20), command=self.manage_camps)
                cancel_btn.grid(row=0, column=0)
                submit_suggest_btn = tk.Button(self.submitframe, text="Allocate Suggested Resources", font=('Arial', 20), command=lambda: self.submit_resources(camp_id, str(suggest_resources_dict["food"]), str(suggest_resources_dict["medical"]), str(suggest_resources_dict["tent"])))
                submit_suggest_btn.grid(row=0, column=1)
                submit_btn = tk.Button(self.submitframe, text="Allocate Edited Resourece", font=('Arial', 20), command=lambda: self.submit_resources(camp_id, self.food_inp.get(), self.med_inp.get(), self.tents_inp.get()))
                submit_btn.grid(row=0, column=2)
                self.submitframe.pack()

    def submit_resources(self, camp_id, food_sup, med_sup, tents):
        res = self.admin.manual_resource_allocation(camp_id, food_sup, med_sup, tents)
        if res == True:
            self.food_inp.delete(0, tk.END)  # Clear the current content
            self.food_inp.insert(0, food_sup)
            self.med_inp.delete(0, tk.END)
            self.med_inp.insert(0, med_sup)
            self.tents_inp.delete(0, tk.END)
            self.tents_inp.insert(0,tents)
            self.food_error.config(text="Food supplies saved", fg="green")
            self.med_error.config(text="Medical supplies saved", fg="green")
            self.tents_error.config(text="Tents saved", fg="green")
            self.root.update_idletasks()
            messagebox.showinfo("Success", "Resources Successfully Allocated!")
            self.manage_camps()
        else:
            self.food_error.config(text=res['food'])
            self.med_error.config(text=res['medical'])
            self.tents_error.config(text=res['tent'])


        # code here to manage camp (alllocate resources etc.)

    def manage_volunteers(self):
        self.clear_content()
        # add code here to edit volunteer data
        self.volunteer_data = pd.read_csv("./files/volunteers.csv")
        self.users = pd.read_csv("./files/logindetails.csv")
        title = tk.Label(self.root, text="Manage Volunteers", font=('Arial', 24))
        title.pack(pady=20)
        camps_ids = ["All Camps"]
        for val in self.camps_data['Camp_ID']:
            if val in camps_ids:
                continue
            camps_ids.append(val)
        self.selected_camp = tk.StringVar(self.root)
        self.selected_camp.set(camps_ids[0])
        camps_menu_lbl = tk.Label(self.root, text="Filter By Camp:", font=('Arial', 18))
        camps_menu = tk.OptionMenu(self.root, self.selected_camp, *camps_ids, command=self.filter_volunteers)
        camps_menu_lbl.pack()
        camps_menu.pack()
        all_buttons = tk.Frame(self.root)
       
        all_buttons.columnconfigure(1, weight=1)
        all_buttons.columnconfigure(2, weight=1)
        activate_all_btn = tk.Button(all_buttons, text="Activate All", font=('Arial', 16), command=self.activate_all)
        deactivate_all_btn = tk.Button(all_buttons, text="Deactivate All", font=('Arial', 16), command=self.deactivate_all)
        activate_all_btn.grid(row=0, column=0)
        deactivate_all_btn.grid(row=0, column=1)
        all_buttons.pack()
        camp_columns = ["Camp ID", "Username", "First Name", "Surname", "Phone", "Age", "Availability", "State", "Delete"]
        column_widths = [70, 80, 80, 80, 80, 40, 220, 70, 70]
        self.volun_tree = ttk.Treeview(self.root, columns=camp_columns, show="headings")
        for i in range(len(camp_columns)):
            col = camp_columns[i]
            self.volun_tree.heading(col, text=col)
            self.volun_tree.column(col, stretch=False, width=column_widths[i])
        self.volun_tree.bind("<ButtonRelease-1>", self.individual_volunteer)
        self.volun_tree.pack(pady=20)
        self.filter_volunteers()
    def activate_all(self):
        self.admin.activate_all()
        self.manage_volunteers()
    def deactivate_all(self):
        self.admin.deactivate_all()
        self.manage_volunteers()
    def filter_volunteers(self, event=None):
        for item in self.volun_tree.get_children():
            self.volun_tree.delete(item)
        selected_camp = self.selected_camp.get()
        if selected_camp == "All Camps": filtered_data = self.volunteer_data
        else:
            filtered_data = self.volunteer_data[self.volunteer_data["Camp_ID"] == selected_camp]
        if not filtered_data.empty:
            for index, row in (filtered_data.iterrows()):
                days = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
                availability_array = []
                availability =  str(row['Availability']).zfill(7)
                for i in range(len(availability)):
                    if availability[i] == "1":
                        availability_array.append(days[i])
                if len(availability_array) == 7:
                    availability_string = "All Days"
                elif len(availability_array) == 0:
                    availability_string = "No Days"
                else:
                    if len(availability_array) == 2:
                        availability_string = f'{availability_array[0]} and {availability_array[1]}'
                    else:
                        availability_string = ", ".join(availability_array)
                state = self.users[self.users["Username"] == row["Username"]]["Active"].values[0]
                if state: state = "Active"
                else: state = "Deactive"
                values=[row['Camp_ID'], row['Username'], row['First Name'], row['Last Name'],row['Phone'], row['Age'], availability_string, state, "Delete?"]
                self.volun_tree.insert("", "end", values=values)

    def individual_volunteer(self, event):
        item_id = self.volun_tree.selection()
        column = self.volun_tree.identify_column(event.x)
        if item_id and column == "#8":
            row = (self.volun_tree.item(item_id, "values"))
            self.activate_deactivate(row)
        elif item_id and column == "#9":
            row = (self.volun_tree.item(item_id, "values"))
            self.delete_volunteer(row[1])

    def activate_deactivate(self, row):
        username = row[1]
        if row[-2] == "Active":
            volunteer_choice = messagebox.askyesno(title="Manage Volunteer", message=f"Deactivate {username}'s Account:\n")
            if volunteer_choice == True:
                self.admin.deactivate_account(username)
                self.root.update_idletasks()
                self.manage_volunteers()
        else:
            volunteer_choice = messagebox.askyesno(title="Manage Volunteer", message=f"Activate {username}'s Account:\n")
            if volunteer_choice == True:
                self.admin.activate_account(username)
                self.root.update_idletasks()
                self.manage_volunteers()
            
    def delete_volunteer(self, username):
        volunteer_choice = messagebox.askyesno(title="Manage Volunteer", message=f"Delete {username}'s Account:\n" )
        if volunteer_choice == True:
            self.admin.delete_account(username)
            self.root.update_idletasks()
            self.manage_volunteers()
    
    def clear_content(self):
        for widget in self.root.winfo_children():
            if widget not in self.nav_bar:
                widget.destroy()
    def run(self):
    
        self.root.mainloop()

dummy = Admin()
VGui = AdminGui(dummy)
VGui.run()

