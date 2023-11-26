from Admin import Admin
import tkinter as tk
from tkinter import messagebox, END
from tkinter import ttk
from tkcalendar import *
import csv
import datetime
import time
from datetime import date
import pandas as pd # 引入pandas



# from datetime import datetime

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

    ## Admin feature a-c

    def create_new_plan(self):
        self.clear_content()
        # Get the value by admin using entry
        self.Description = tk.StringVar()
        self.Location = tk.StringVar()
        # Build the label
        tk.Label(self.root, text='Add a new plan').place(x=50, y=40)
        tk.Label(self.root, text='Plan_ID:').place(x=50, y=60)
        tk.Label(self.root, text='Description:').place(x=50, y=100)
        tk.Label(self.root, text='Location:').place(x=50, y=140)
        tk.Label(self.root, text='Start_Date:').place(x=50, y=180)
        tk.Label(self.root, text='End_Date:').place(x=50, y=220)
        # Get the plan_ID automatically
        self.plan_id = self.admin.last_plan_id() + 1
        # print(self.plan_id)--> just for testing during coding
        # The plan_ID can be shown in the window and admin can not edit
        self.plan_id_label = tk.Label(self.root, text=self.plan_id)
        # Build the entry
        self.plan_id_label.place(x=50, y=80)
        self.des_entry = tk.Entry(self.root, width=30, textvariable=self.Description)
        self.des_entry.place(x=50, y=120)
        self.loc_entry = tk.Entry(self.root, width=30, textvariable=self.Location)
        self.loc_entry.place(x=50, y=160)
        # Build the button
        sdate_button = tk.Button(self.root, text='choose the start date', command=self.pick_sdate).place(x=350, y=160)
        edate_button = tk.Button(self.root, text='choose the end date', command=self.pick_edate).place(x=350, y=200)
        tk.Button(self.root, text='Save this plan', command=self.save_data).place(x=150, y=300)

        # When admin click the entry date, admin will be informed that they need to use calendar
        def stest(content, reason, name):
            if self.start_date.get() is not None:
                messagebox.showwarning(title='Creat a new plan',
                                       message='Please using take the button to choose the date')
                # return False

        self.valid_input_sdate = tk.StringVar()
        sCMD = self.root.register(stest)
        self.start_date = tk.Entry(self.root, textvariable=self.valid_input_sdate, validate='focusin',
                                   validatecommand=(sCMD, '%P', '%V', '%W'))
        self.start_date.place(x=50, y=200)

        def etest(content, reason, name):
            if self.end_date.get() is not None:
                messagebox.showwarning(title='Creat a new plan',
                                       message='Please using take the button to choose the date')

        self.valid_input_edate = tk.StringVar()
        eCMD = self.root.register(etest)
        self.end_date = tk.Entry(self.root, textvariable=self.valid_input_edate, validate='focusin',
                                 validatecommand=(eCMD, '%P', '%V', '%W'))
        self.end_date.place(x=50, y=250)

    #  This method is to get the date using calendar and judge whether it is valid or not

    def pick_sdate(self):
        self.date_window = tk.Toplevel()
        self.date_window.grab_set()
        self.date_window.geometry('250x220+590+370')
        self.cal = Calendar(self.date_window, selectmode='day', year=2023, month=11, day=16)
        self.cal.place(x=0, y=0)
        submit_btn = tk.Button(self.date_window, text='submit', command=self.grab_sdate)
        submit_btn.place(x=80, y=190)

    def pick_edate(self):
        if len(self.start_date.get()) == 0 or self.s_date is None:
            messagebox.showwarning(title='Choose start date',
                                   message='please choose the start date firstly using calendar')
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

    ## This is to save the recoding and it can be show directly later
    def save_data(self):
        Plan_ID_ = self.plan_id
        Description_ = self.Description.get()
        Location_ = self.Location.get()
        Start_date_ = self.s_date
        End_date_ = self.e_date
        var_start_day = self.valid_input_sdate.get()
        var_end_day = self.valid_input_edate.get()
        print(Location_)
        print(Description_)
        print(Plan_ID_)
        print(Start_date_)
        print(End_date_)
        print("test:" + var_start_day)
        print("test:" + var_end_day)
        if len(self.des_entry.get()) == 0 or len(self.loc_entry.get()) == 0 or len(self.start_date.get()) == 0 or len(
                self.end_date.get()) == 0:
            messagebox.showwarning(title='Creat a new plan', message='Please fill in all the entry')
        elif Start_date_ == None or End_date_ == None:
            messagebox.showwarning(title='Creat a new plan', message='Please using take the button to choose the date')
            self.start_date.delete(0, END)
            self.end_date.delete(0, END)
            self.e_date = None
            self.s_date = None
        elif Start_date_ is not None or End_date_ is not None:
            Start_date_ = self.s_date.strftime('%Y-%m-%d')
            End_date_ = self.e_date.strftime('%Y-%m-%d')
            # print(End_date_)
            # print(var_start_day==Start_date_)
            # print(self.admin.check_end_date(self.e_date, self.s_date))
            if var_start_day == Start_date_ and var_end_day == End_date_ and not (
            self.admin.check_end_date(self.e_date, self.s_date)):
                if self.s_date == date.today():

                    Start_date_ = self.s_date.strftime('%d/%m/%Y')
                    End_date_ = self.e_date.strftime('%d/%m/%Y')
                    plan_dic = {'Plan_ID': Plan_ID_, 'Description': Description_, 'Location': Location_,
                                'Start Date': Start_date_, 'End Date': End_date_,'Status':'Ongoing'}
                    plan_list = [
                        {'Plan_ID': Plan_ID_, 'Description': Description_, 'Location': Location_, 'Start Date': Start_date_,
                         'End Date': End_date_,'Status':'Ongoing'}]  # 空字典
                    header = ['Plan_ID', 'Description', 'Location', 'Start Date', 'End Date','Status']
                    with open('C:\\Users\\96249\\Desktop\Python_CW\\intro-programming\\files\\plan_file.csv', 'a', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=header)

                        writer.writerows(plan_list)
                    self.admin.insert_new_plan(plan_dic)
                    messagebox.showinfo('infor', 'Create a plan successfully')
                    # self.plan_id = self.plan_id + 1
                    # self.Plan_Id_entry.insert(END, self.plan_id)
                    self.Description.set('')
                    self.Location.set('')
                    self.start_date.delete(0, END)
                    self.end_date.delete(0, END)
                    self.e_date = None
                    self.s_date = None
                    self.plan_id = self.plan_id + 1
                    self.plan_id_label.destroy()
                    self.plan_id_label = tk.Label(self.root, text=self.plan_id)
                    self.plan_id_label.place(x=50, y=80)
                elif self.s_date > date.today():
                    Start_date_ = self.s_date.strftime('%d/%m/%Y')
                    End_date_ = self.e_date.strftime('%d/%m/%Y')
                    plan_dic = {'Plan_ID': Plan_ID_, 'Description': Description_, 'Location': Location_,
                                'Start Date': Start_date_, 'End Date': End_date_,'Status':'Future'}
                    plan_list = [
                        {'Plan_ID': Plan_ID_, 'Description': Description_, 'Location': Location_, 'Start Date': Start_date_,
                         'End Date': End_date_,'Status':'Future'}]  # 空字典
                    header = ['Plan_ID', 'Description', 'Location', 'Start Date', 'End Date','Status']
                    print(Start_date_)
                    print(End_date_)
                    with open('C:\\Users\\96249\\Desktop\\Python_CW\\intro-programming\\files\\plan_file.csv', 'a', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=header)

                        writer.writerows(plan_list)
                    self.admin.insert_new_plan(plan_dic)
                    messagebox.showinfo('infor', 'Create a plan successfully')
                    # self.plan_id = self.plan_id + 1
                    # self.Plan_Id_entry.insert(END, self.plan_id)
                    self.Description.set('')
                    self.Location.set('')
                    self.start_date.delete(0, END)
                    self.end_date.delete(0, END)
                    self.e_date = None
                    self.s_date = None
                    self.plan_id = self.plan_id + 1
                    self.plan_id_label.destroy()
                    self.plan_id_label = tk.Label(self.root, text=self.plan_id)
                    self.plan_id_label.place(x=50, y=80)
            elif self.admin.check_end_date(self.e_date, self.s_date):
                messagebox.showwarning(title='Choose start date', message='The end date cannot before start date')
                self.start_date.delete(0, END)
                self.end_date.delete(0, END)
                self.e_date = None
                self.s_date = None
            else:
                # print(var_start_day!=Start_date_)
                self.admin.is_date(var_start_day)
                messagebox.showwarning(title='Creat a new plan',
                                       message='Please reuse the button to enter the date using calendar ')
                self.start_date.delete(0, END)
                self.end_date.delete(0, END)
                self.e_date = None
                self.s_date = None

    ## This is to show the plan by table

    def display_plans(self):
        self.clear_content()
        # add code here:
        # somewhere in here will be the end button for the individual plans which will maybe go to another function

        header = ['plan_ID', 'Description', 'Location', 'Start Date', 'End Date','Status']
        self.table = ttk.Treeview(self.root)
        self.root.table = self.table
        self.table.configure(columns=header, show='headings')
        for item in header:
            self.table.column(item, width=120, anchor=tk.CENTER)
            self.table.heading(item, text=item)

        self.root.table.pack(fill=tk.BOTH, expand=True)
        tk.Button(self.root, text='End a plan', command=self.end_plan).pack(side='left', pady=20)
        # tk.Button(self.root, text='refresh', command= self.refresh_plan).pack(side='left', pady=20)
        # plan_data = PlanData()
        # this is to show if the end date in the plan has arrived, this End date will show "None"
        index = 0
        # 如果开始时间到了今天 创建的计划自动变为ongoing
        # 如果结束时间到了今天 创建的计划自动变为 finished
        df = pd.read_csv("C:\\Users\\96249\\Desktop\\Python_CW\\intro-programming\\files\\plan_file.csv")
        df.set_index("Plan_ID", inplace=True)  # 日期列设置为index
        # df.loc[(df["高温"] >= 0) & (df["强度"] == "2级"), "风向"] = "【一朵】"
        today_str = time.strftime("%d/%m/%Y", time.localtime(time.time()))
        df.loc[(df["Start Date"] == today_str) & (df['Status'] =='Future'), "Status"] = "Ongoing"
        df.loc[(df["End Date"] == today_str) & (df['Status'] == 'Ongoing'), "Status"] = "Finshed"
        # print(df) # just for test
        df.to_csv("C:\\Users\\96249\\Desktop\\Python_CW\\intro-programming\\files\plan_file.csv")
        # 将上面自动更新之后的显示在表中
        index = 0
        with open('C:\\Users\\96249\\Desktop\\Python_CW\\intro-programming\\files\\plan_file.csv', 'r', encoding='utf-8') as plan_file:
            read = csv.DictReader(plan_file)
            self.plan_update_list = []
            for row in read:
                self.plan_update_list.append(row)
        print(self.plan_update_list)
        for plan in self.plan_update_list:
            self.root.table.insert('', index + 1, values=(plan['Plan_ID'], plan['Description'],
                                                          plan['Location'], plan['Start Date'], plan['End Date'],plan['Status']))

    def end_plan(self):
        item = self.table.selection()
        if item:
            def valid_item_():
                item = self.table.selection()
                selected = self.table.focus()
                temp = self.table.item(selected, 'values')
                self.plan_sdate = temp[-3]
                self.plan_edate = temp[-2]
                self.status = temp[-1]
                print('test:' + self.plan_edate)
                self.plan_sdate_date = datetime.datetime.strptime(self.plan_sdate, '%d/%m/%Y').date()
                # self.plan_edate_date = datetime.datetime.strptime(self.plan_edate,'%d/%m/%Y').date()

            self.table.bind('<ButtonRelease-1>', valid_item_())
            print(self.plan_sdate)
            if self.plan_sdate_date > date.today():
                messagebox.showinfo(title='Info', message='This plan has not started! It cannot be ended')
            elif self.status == 'Ongoing':
                print(self.status)
                print('test2')
                isok = messagebox.askyesno(title='infor', message='Do you want to end this plan？')
                if isok:
                    def update_item():
                        item = self.table.selection()
                        selected = self.table.focus()
                        temp = self.table.item(selected, 'values')
                        plan_edate = temp[-2]
                        end_up = 'Finished'
                        print(temp[0])
                        print(temp[1])
                        print(temp[2])
                        print(temp[3])
                        print(temp[4])
                        end_date_today = time.strftime("%d/%m/%Y",time.localtime(time.time()))
                        print('今天是'+ end_date_today)
                        # 显示变化
                        self.table.item(selected, values=(temp[0], temp[1], temp[2], temp[3], end_date_today,end_up))
                        #储存新的变化后的计划进去
                        plan_end_dic = {'Plan_ID': temp[0], 'Description': temp[1], 'Location': temp[2],
                                        'Start Date': temp[3], 'End Date': end_date_today,'Status':end_up}
                        plan_end_list = [
                            {'Plan_ID': temp[0], 'Description': temp[1], 'Location': temp[2], 'Start Date': temp[3],
                             'End Date': end_date_today,'Status':end_up}]
                        header = ['Plan_ID', 'Description', 'Location', 'Start Date', 'End Date','Status']
                        # 先加入
                        with open('C:\\Users\\96249\\Desktop\\Python_CW\\intro-programming\\files\\plan_file.csv', 'a',
                                  newline='', encoding='utf-8') as f:
                            writer = csv.DictWriter(f, fieldnames=header)
                            writer.writerows(plan_end_list)
                        self.admin.insert_new_plan(plan_end_dic)

                        print(plan_end_list)
                        # 然后删除
                        print('test2 change')
                        print(temp[0])
                        print(temp[1])
                        print(temp[2])
                        print(temp[3])
                        print(temp[4])
                        header = ['Plan_ID', 'Description', 'Location', 'Start Date', 'End Date','Status']
                        for x in self.plan_data_:
                            print('>>>>====', x)
                            if temp[0] == x['Plan_ID'] and temp[1] == x['Description'] and temp[2] == x['Location'] and \
                                    temp[4] == x['End Date'] and temp[5] == 'Ongoing':
                                yy = self.plan_data_.remove(x)
                            elif int(temp[0]) == x['Plan_ID'] and temp[1] == x['Description'] and temp[2] == x['Location'] and \
                                    temp[4] == x['End Date'] and temp[5] == 'Ongoing':

                                    yy = self.plan_data_.remove(x)
                                    print('yes or not')
                        print(self.plan_data_)

                        with open('C:\\Users\\96249\\Desktop\\Python_CW\\intro-programming\\files\\plan_file.csv', 'w', newline='') as csvfile:
                            fields = ['Plan_ID', 'Description', 'Location', 'Start Date', 'End Date', 'Status']
                            writer = csv.DictWriter(csvfile, fieldnames=fields)
                            writer.writeheader()
                            for row in self.plan_data_:
                                writer.writerow(row)

                    self.table.bind('<ButtonRelease-1>', update_item())

            elif self.status == 'Finished':
                print(self.plan_edate)

                messagebox.showinfo(title='Info', message='This plan has aready ended')
        elif not item:
            messagebox.showinfo(title='Info', message='Please choose a plan！！！')

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