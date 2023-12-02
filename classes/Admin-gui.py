from Admin import Admin
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from Camps import Camps
from Plans import Plans
from Resource_requests import Resource_requests
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
        self.requests = Resource_requests()
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
        info_lbl = tk.Label(self.root, text="Click on Allocate Resources to allocate to specific camp", font=('Arial', 16))
        info_lbl.pack()
        camp_columns = ["Camp ID", "Plan ID", "No. of Volunteers", "No. of Refugees", "Capacity", "Food Packages", "Medical Supplies", "Tents", "Action (Click) ⬇"]
        column_widths = [60, 60, 100, 100, 60, 110, 110, 60, 130]
        tree_view_frame= tk.Frame(self.root)
        tree_view_frame.pack()
        tree_view_frame.columnconfigure(0, weight=8)
        tree_view_frame.columnconfigure(1, weight=1)
        self.camps_tree = ttk.Treeview(tree_view_frame, columns=camp_columns, show="headings")
        for i in range(len(camp_columns)):
            col = camp_columns[i]
            self.camps_tree.heading(col, text=col)
            self.camps_tree.column(col, stretch=False, width=column_widths[i])
        self.camps_tree.bind("<ButtonRelease-1>", self.can_allocate)        
        scrollbar = ttk.Scrollbar(tree_view_frame, orient="vertical", command=self.camps_tree.yview)
        # Configure the Treeview to use the scrollbar
        self.camps_tree.configure(yscrollcommand=scrollbar.set)
        # Place the scrollbar on the right side of the Treeview
        self.camps_tree.grid(row=0, column=0, sticky='nsew')
        
        # label.grid(row=0,column=1)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.unresolved = self.requests.get_unresolved()
        request_btn_text = f'Resource Requests ({len(self.unresolved)})'
        request_btn = tk.Button(self.root, text=request_btn_text, font= ("Arial", 16), command=self.resource_requests_list)
        request_btn.pack(pady=50)
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
    
    def resource_requests_list(self):
        self.clear_content()
        self.unresolved = self.requests.get_unresolved()
        request_title = tk.Label(self.root, text="Resource Requests", font=('Arial', 24))
        request_title.pack(pady=20)
        unresolved_title = tk.Label(self.root, text="Unresolved Requests", font=('Arial', 20))
        unresolved_title.pack(pady=5)
        unresolved_frame = tk.Frame(self.root)
        unresolved_frame.columnconfigure(0, weight=8)
        unresolved_frame.columnconfigure(1, weight=1)
        unresolved_columns = ["Camp ID", "Requester", "Food Packages Requested", "Medical Supplies Requested", "Tents Requested", "Time Requested"]
        column_widths = [60, 120, 170, 170, 140, 100]
        grant_requests = tk.Button(self.root, text="Allocate all requested resources", command=self.grant_all_requests)
        grant_requests.pack()
        self.requests_tree = ttk.Treeview(unresolved_frame, columns=unresolved_columns, show="headings")
        self.requests_tree.grid(row=0, column=0)
        request_scrollbar = ttk.Scrollbar(unresolved_frame, orient="vertical", command=self.requests_tree.yview)
        # Configure the Treeview to use the scrollbar
        self.requests_tree.configure(yscrollcommand=request_scrollbar.set)
        request_scrollbar.grid(row=0, column=1)
        unresolved_frame.pack()
        for i in range(len(unresolved_columns)):
            col = unresolved_columns[i]
            self.requests_tree.heading(col, text=col)
            self.requests_tree.column(col, stretch=False, width=column_widths[i])
        for index, row in (self.unresolved[::-1].iterrows()):
            values = [row['Camp_ID'], row['Volunteer'], row['food_pac'], row['medical_sup'], row['tents'], row['date']]
            self.requests_tree.insert("", "end", values=values)
        self.requests_tree.bind("<ButtonRelease-1>", self.grant_specific_request)
  
        # completed requests
        self.resolved = self.requests.get_resolved()
        resolved_title = tk.Label(self.root, text="Resolved Requests", font=('Arial', 20))
        resolved_title.pack(pady=20)
        resolved_frame = tk.Frame(self.root)
        resolved_frame.columnconfigure(0, weight=8)
        resolved_frame.columnconfigure(1, weight=1)
        resolved_columns = ["Camp ID", "Requester", "Food Packages Requested", "Medical Supplies Requested", "Tents Requested", "Time Requested"]
        column_widths = [60, 120, 170, 170, 140, 100]
        self.resolved_tree = ttk.Treeview(resolved_frame, columns=resolved_columns, show="headings")
        self.resolved_tree.grid(row=0, column=0)
        resolved_scrollbar = ttk.Scrollbar(resolved_frame, orient="vertical", command=self.resolved_tree.yview)
        # Configure the Treeview to use the scrollbar
        self.resolved_tree.configure(yscrollcommand=resolved_scrollbar.set)
        self.resolved_tree.configure(height=5)
        
        resolved_scrollbar.grid(row=0, column=1)
        resolved_frame.pack()
        for i in range(len(resolved_columns)):
            col = resolved_columns[i]
            self.resolved_tree.heading(col, text=col)
            self.resolved_tree.column(col, stretch=False, width=column_widths[i])
        for index, row in (self.resolved[::-1].iterrows()):
            
            values = [row['Camp_ID'], row['Volunteer'], row['food_pac'], row['medical_sup'], row['tents'], row['date']]
            self.resolved_tree.insert("", "end", values=values)
        
    def grant_all_requests(self):
        self.requests.write_all()
        for index, row in (self.unresolved.iterrows()):
            self.admin.manual_resource_allocation(row['Camp_ID'], str(row['food_pac']), str(row['medical_sup']), str(row['tents']))
        messagebox.showinfo("Success", "All Requested Resources Successfully Allocated!")
        self.resource_requests_list()
    
    def grant_specific_request(self, event):
        item_id = self.requests_tree.selection()
        if item_id:
            row = (self.requests_tree.item(item_id, "values"))
            requested_resources = [row[2], row[3], row[4]]
            camp_id = row[0]
        
            can_allocate, suggest_resources_dict = self.admin.suggest_resources(row[0])
            if can_allocate == False:
                messagebox.showinfo("Error", "Chosen camp has 0 population and thus no resources can be allocated")
                self.manage_camps()
            else:
               
                resources = self.camps.get_resource_data(camp_id)
                if resources == []:
                    resources = [0, 0, 0]
                self.allocate_resources(camp_id, resources, suggest_resources_dict, requested_resources)

    def can_allocate(self, event):
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
                request_data = self.requests.get_unresolved()
                if camp_id in request_data['Camp_ID'].values:
                    row = request_data[request_data['Camp_ID']==camp_id].values[0]
                    requested_resources = [row[3], row[4], row[5]]
                    self.allocate_resources(camp_id, curr_resources, suggest_resources_dict, requested_resources)
                else:
                    self.allocate_resources(camp_id, curr_resources, suggest_resources_dict)
    def allocate_resources(self, camp_id, curr_resources, suggest_resources_dict, requested_resources=None):
            self.clear_content()
           
            if requested_resources != None:
                requested_strings = [f'Requested Food: {requested_resources[0]}', f'Requested Medical: {requested_resources[1]}', f'Requested Tents: {requested_resources[2]}']
            else:
                requested_strings = ["", "", ""]
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
            requested_food_lbl = tk.Label(self.root, text=requested_strings[0], font=('Arial', 16))
            self.food_error = tk.Label(self.root, text="", fg="red", font=('Arial', 16))
            food_lbl.pack()
            self.food_inp.pack()
            requested_food_lbl.pack()
            suggest_food_lbl.pack()
            
            self.food_error.pack(pady=(0,10))
            med_lbl = tk.Label(self.root, text="Edit medical supplies:", font=('Arial', 18))
            self.med_inp = tk.Entry(self.root)
            self.med_inp.insert(0, curr_resources[1])
            suggest_med_lbl = tk.Label(self.root, text=suggest_med_text, font=('Arial', 16))
            requested_med_lbl = tk.Label(self.root, text=requested_strings[1], font=('Arial', 16))
            self.med_error = tk.Label(self.root, text="", fg="red", font=('Arial', 16))
            med_lbl.pack()
            self.med_inp.pack()
            requested_med_lbl.pack()
            suggest_med_lbl.pack()
            self.med_error.pack(pady=(0,10))
            tents_lbl = tk.Label(self.root, text="Edit tents:", font=('Arial', 18))
            self.tents_inp = tk.Entry(self.root)
            self.tents_inp.insert(0, curr_resources[2])
            suggest_tents_lbl = tk.Label(self.root, text=suggest_tents_text, font=('Arial', 16))
            requested_tents_lbl = tk.Label(self.root, text=requested_strings[2], font=('Arial', 16))
            self.tents_error = tk.Label(self.root, text="", fg="red", font=('Arial', 16))
            tents_lbl.pack()
            self.tents_inp.pack()
            requested_tents_lbl.pack()
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
        info_lbl  = tk.Label(self.root, text="Click on a State or Delete column to edit an individual volunteer", font=('Arial', 16))
        info_lbl.pack()
        camp_columns = ["Camp ID", "Username", "First Name", "Surname", "Phone", "Age", "Availability", "State", "Delete"]
        column_widths = [70, 80, 80, 80, 80, 40, 220, 70, 70]
        tree_view_frame= tk.Frame(self.root)
        tree_view_frame.pack()
        tree_view_frame.columnconfigure(0, weight=8)
        tree_view_frame.columnconfigure(1, weight=1)
        self.volun_tree = ttk.Treeview(tree_view_frame, columns=camp_columns, show="headings")
        for i in range(len(camp_columns)):
            col = camp_columns[i]
            self.volun_tree.heading(col, text=col)
            self.volun_tree.column(col, stretch=False, width=column_widths[i])
        self.volun_tree.bind("<ButtonRelease-1>", self.individual_volunteer)
        scrollbar = ttk.Scrollbar(tree_view_frame, orient="vertical", command=self.volun_tree.yview)
        # Configure the Treeview to use the scrollbar
        self.volun_tree.configure(yscrollcommand=scrollbar.set)
        # Place the scrollbar on the right side of the Treeview
        self.volun_tree.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1)
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

