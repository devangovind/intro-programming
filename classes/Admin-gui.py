from Admin import Admin
import tkinter as tk
from tkinter import messagebox, END
from tkinter import ttk
from tkcalendar import *
import csv
from datetime import date
from datetime import datetime

class AdminGui:
    def __init__(self, admin):
        self.s_date = None
        self.e_date = None
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Volunteer View")
        self.admin = admin
        # self.volunteer_data = self.volunteer.get_volunteer_data()
        self.create_nav_bar()
        self.welcome_message()
        self.plan_data_ = self.admin.plan_list
        # self.edit_details_button = tk.Button(self.root, text="Edit personal details", font=('Arial', 20))
        # self.root.mainloop()

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
        self.create_plan_btn = tk.Button(self.headerarea, text="Create New Plan", font=('Arial', 16),
                                         command=self.create_new_plan)
        self.create_plan_btn.grid(row=0, column=1)
        self.display_plans_btn = tk.Button(self.headerarea, text="Display Existing Plans", font=('Arial', 16),
                                           command=self.display_plans)
        self.display_plans_btn.grid(row=0, column=2)
        self.manage_camps_btn = tk.Button(self.headerarea, text="Manage Camps", font=('Arial', 16),
                                          command=self.manage_camps)
        self.manage_camps_btn.grid(row=0, column=3)
        self.manage_volunteers_btn = tk.Button(self.headerarea, text="Manage Volunteers", font=('Arial', 16),
                                               command=self.manage_volunteers)
        self.manage_volunteers_btn.grid(row=0, column=4)
        self.logout_btn = tk.Button(self.headerarea, text="Logout", font=('Arial', 16))
        self.logout_btn.grid(row=0, column=5)
        self.headerarea.pack(padx=20)
        self.nav_bar = [self.headerarea, self.home_btn, self.display_plans_btn, self.create_plan_btn,
                        self.manage_camps_btn, self.manage_volunteers_btn, self.logout_btn]

    def welcome_message(self):
        self.clear_content()
        welcome_back = f'Welcome Back, Admin'
        label = tk.Label(self.root, text=welcome_back, font=('Arial', 24))
        label.pack(pady=100)



    def create_new_plan(self):
        self.clear_content()
        # add_plan_window = Toplevel()
        # add_plan_window.geometry('400x400+600+300')
        self.Description = tk.StringVar()
        self.Location = tk.StringVar()

        tk.Label(self.root, text='Add a new plan').place(x=50, y=40)
        tk.Label(self.root, text='Plan_ID:').place(x=50, y=60)
        self.plan_id = self.admin.last_plan_id() + 1
        # print(self.plan_id)
        Plan_Id_butn = tk.Entry(self.root, width=30)
        Plan_Id_butn.place(x=50, y=80)
        Plan_Id_butn.insert(END, self.plan_id)
        Plan_Id_butn.config(state='readonly')
        tk.Label(self.root, text='Description:').place(x=50, y=100)
        self.des_entry = tk.Entry(self.root, width=30, textvariable=self.Description)
        self.des_entry.place(x=50, y=120)
        tk.Label(self.root, text='Location:').place(x=50, y=140)
        self.loc_entry = tk.Entry(self.root, width=30, textvariable=self.Location)
        self.loc_entry.place(x=50, y=160)
        tk.Label(self.root, text='Start_Date:').place(x=50, y=180)
        sdate_button = tk.Button(self.root, text='choose the start date', command=self.pick_sdate).place(x=350, y=160)
        edate_button = tk.Button(self.root, text='choose the end date', command=self.pick_edate).place(x=350, y=200)
        self.start_date = tk.Entry(self.root, width=30)
        self.start_date.place(x=50, y=200)
        # self.start_date.insert(0,'dd/mm/yyyy')
        self.end_date = tk.Entry(self.root, width=30)
        self.end_date.place(x=50, y=250)
        # self.end_date.insert(0,'dd/mm/yyyy')
        self.start_date = tk.Entry(self.root, width=30)
        self.start_date.place(x=50, y=200)
        # self.start_date.insert(0,'dd/mm/yyyy')

        #
        tk.Label(self.root, text='End_Date:').place(x=50, y=220)
        # tk.Entry(self.root, width=30).place(x=50, y=240)
        tk.Button(self.root, text='Save this plan', command=self.save_data).place(x=150, y=300)




    def pick_sdate(self):
        self.date_window = tk.Toplevel()
        self.date_window.grab_set()
        self.date_window.geometry('250x220+590+370')
        self.cal = Calendar(self.date_window, selectmode='day', year=2023, month=11, day=16)
        self.cal.place(x=0, y=0)
        submit_btn = tk.Button(self.date_window, text='submit', command=self.grab_sdate)
        submit_btn.place(x=80, y=190)

    def pick_edate(self):
        if len(self.start_date.get()) == 0:
            messagebox.showwarning(title='Choose start date', message='please choose the start date firstly')
        else:

            self.date_window = tk.Toplevel()
            self.date_window.grab_set()
            self.date_window.geometry('250x220+590+370')
            self.cal = Calendar(self.date_window, selectmode='day', year=2023, month=11, day=16)
            self.cal.place(x=0, y=0)
            submit_btn = tk.Button(self.date_window, text='submit', command=self.grab_edate)
            submit_btn.place(x=80, y=190)

    def grab_sdate(self):
        self.s_date = self.cal.selection_get()
        if self.admin.check_start_day(self.s_date):
            messagebox.showwarning(title='Choose start date', message='The start date cannot before today')
        else:
            self.start_date.delete(0, END)
            self.start_date.insert(0, self.s_date)
            self.date_window.destroy()
            # date = self.cal.get_date()
            print(type(self.s_date))
            print(self.admin.is_date(self.s_date))
            return self.s_date

    def grab_edate(self):

        self.e_date = self.cal.selection_get()
        if self.admin.check_end_date(self.e_date, self.s_date):
            messagebox.showwarning(title='Choose start date', message='The end date cannot before start date')
        else:
            self.end_date.delete(0, END)
            self.end_date.insert(0, self.e_date)
            self.date_window.destroy()
            # date = self.cal.get_date()
            print(type(self.e_date))
            print(self.admin.is_date(self.e_date))
        return self.e_date


    def save_data(self):
        Plan_ID_ = self.plan_id
        Description_ = self.Description.get()
        Location_ = self.Location.get()
        Start_date_ = self.s_date
        End_date_ = self.e_date
        print(Location_)
        print(Description_)
        print(Plan_ID_)
        print(Start_date_)
        print(End_date_)
        if len(self.des_entry.get()) == 0 or len(self.loc_entry.get()) == 0 or len(self.start_date.get())==0 or len(self.end_date.get()) ==0:
            messagebox.showwarning(title='Creat a new plan', message='Please fill in all the entry')
        elif Start_date_ == None or End_date_ == None:
            messagebox.showwarning(title='Creat a new plan', message='Please using take the button to choose the date')
        else:
            Start_date_ = self.s_date.strftime('%d/%m/%Y')
            End_date_  = self.e_date.strftime('%d/%m/%Y')
            plan_dic = {'Plan_ID': Plan_ID_,'Description':Description_,'Location':Location_,'Start Date':Start_date_,'End Date':End_date_}
            plan_list= [{'Plan_ID': Plan_ID_,'Description':Description_,'Location':Location_,'Start Date':Start_date_,'End Date':End_date_}] # 空字典
            header = ['Plan_ID', 'Description', 'Location', 'Start Date', 'End Date']
            print(Start_date_)
            print(End_date_)
            with open('plan_file.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=header)


                writer.writerows(plan_list)
            self.admin.insert_new_plan(plan_dic)



    def display_plans(self):
        self.clear_content()
        # add code here:
        # somewhere in here will be the end button for the individual plans which will maybe go to another function

        header = ['plan_ID', 'Description', 'Location', 'Start Date', 'End Date']
        self.table = ttk.Treeview(self.root)
        self.root.table = self.table
        self.table.configure(columns=header, show='headings')
        for item in header:
            self.table.column(item, width=120, anchor=tk.CENTER)
            self.table.heading(item, text=item)

        self.root.table.pack(fill=tk.BOTH, expand=True)
        # tk.Button(self.root, text='Add a new plan').pack(side='left', pady=20)
        tk.Button(self.root, text='End a plan', command= self.end_plan).pack(side='left', pady=20)
        tk.Button(self.root, text='Refresh plans ').pack(side='left', pady=20)
        # plan_data = PlanData()
        index = 0
        for plan in self.plan_data_:
            # print(plan[-1])
            # print(type(plan[-1]))
            if plan['End Date'] is not None:
                plan_edate_str = plan['End Date']
                plan_end_date = datetime.strptime(plan_edate_str, "%d/%m/%Y").date()
                # print(plan_edate_str)
                # print(plan_end_date)
                # returns True if end date has occured and False if end date has not
                # return today > plan_end_date
                #
                if plan_end_date < date.today():
                    plan['End Date'] = None
            # print(plan['End Date'])
            #
            # # print(plan_edate)
            # # print(plan)
            # # print(plan['End Date'])
            self.root.table.insert('', index + 1, values=(plan['Plan_ID'], plan['Description'],
                                                          plan['Location'], plan['Start Date'], plan['End Date']))



    def end_plan(self):
        # item = self.table.selection()


        # def selectItem(a):
        #     curItem = self.table.focus()
        #     key = self.table.item(curItem)
        #     value = key['values']
        #     date = value[-1]
    #     if item:
    #     isok = messagebox.askyesno(title='提醒', message='您确定要删除此记录么？')
    #     if isok:
    #         self.table.delete(item)
    # else:
    #     messagebox.showinfo(title='提示信息', message='请选择一条记录！！！')
        def update_item():
            item = self.table.selection()
            if item:
                selected = self.table.focus()
                temp = self.table.item(selected, 'values')
                plan_edate = temp[-1]
                if plan_edate is not None and item is not None:
                    isok = messagebox.askyesno(title='提醒', message='Do you want to end this plan？')
                    if isok:
                        end_up = None
                        self.table.item(selected, values=(temp[0], temp[1], temp[2],temp[3],end_up))
                else:
                    messagebox.showwarning(title='End a plan', message='This plan has been ended')

            else:
                messagebox.showinfo(title='Info', message='Please choose a plan！！！')
                # selected = self.table.focus()
                # temp = self.table.item(selected, 'values')
                # plan_edate = temp[-1]
                # if plan_edate is not None and item is not None:
                #     isok = messagebox.askyesno(title='提醒', message='Do you want to end this plan？')
                #     if isok:
                #         end_up = None
                #         self.table.item(selected, values=(temp[0], temp[1], temp[2],temp[3],end_up))
                # else:
                #     messagebox.showwarning(title='End a plan', message='This plan has been ended')

            # self.table.item('curItem', values=(column = 'End date', '下塘西路545号⑤')

            # print(tree.item(curItem))
            # print(value)
            # print(date)
            # return self.date
        # item = self.table.selection()
        self.table.bind('<ButtonRelease-1>', update_item())
        # print(self.date)
        # print(item)
        # if item:
        #     isok = messagebox.askyesno(title='提醒', message='您确定要删除此记录么？')
        #     if isok:
        #         self.table.delete(item)
        # else:
        #     messagebox.showinfo(title='提示信息', message='请选择一条记录！！！')

    def manage_camps(self):
        self.clear_content()
        # code here to manage camp (alllocate resources etc.)

    def manage_volunteers(self):
        self.clear_content()
        # add code here to edit volunteer data

    def clear_content(self):
        for widget in self.root.winfo_children():
            if widget not in self.nav_bar:
                widget.destroy()

    def run(self):

        self.root.mainloop()


dummy = Admin()
VGui = AdminGui(dummy)

VGui.run()