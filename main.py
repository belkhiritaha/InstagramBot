from cmath import log
from time import sleep
import logging
import json
from random import randint
import os
from os.path import exists

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import multiprocessing

from logic import *


with open(r".\database.json" , "r") as file:
    database = json.load(file)

#close file
file.close()

print(database["comment_list"])

numberOfAccounts = len(database['accounts'])
account_info = [database['accounts'][i] + [database['hashtags'][i]] for i in range(numberOfAccounts)]

frame_styles = {"relief": "groove",
                "bd": 3, "bg": "#BEB2A7",
                "fg": "#073bb3", "font": ("Arial", 9, "bold")}

last_info = "Starting up... (logs will be saved to logs.txt)"

multiprocessing.freeze_support()

######################################GUI#############################################


class LoginPage(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        main_frame = tk.Frame(self, bg="#708090", height=431, width=626)  # this is the background
        main_frame.pack(fill="both", expand="true")

        self.geometry("626x431")  # Sets window size to 626w x 431h pixels
        self.resizable(0, 0)  # This prevents any resizing of the screen
        title_styles = {"font": ("Trebuchet MS Bold", 16), "background": "blue"}

        text_styles = {"font": ("Verdana", 14),
                       "background": "blue",
                       "foreground": "#E1FFFF"}

        frame_login = tk.Frame(main_frame, bg="blue", relief="groove", bd=2)  # this is the frame that holds all the login details and buttons
        frame_login.place(rely=0.30, relx=0.17, height=130, width=400)

        label_title = tk.Label(frame_login, title_styles, text="Login Page")
        label_title.grid(row=0, column=1, columnspan=1)

        label_user = tk.Label(frame_login, text_styles, text="Username:")
        label_user.grid(row=1, column=0)

        label_pw = tk.Label(frame_login, text_styles, text="Password:")
        label_pw.grid(row=2, column=0)

        entry_user = ttk.Entry(frame_login, width=45, cursor="xterm")
        entry_user.grid(row=1, column=1)

        entry_pw = ttk.Entry(frame_login, width=45, cursor="xterm", show="*")
        entry_pw.grid(row=2, column=1)

        button = ttk.Button(frame_login, text="Login", command=lambda: getlogin())
        button.place(rely=0.70, relx=0.50)

        def getlogin():
            username = entry_user.get()
            password = entry_pw.get()
            # if your want to run the script as it is set validation = True
            validation = validate(username, password)
            if validation:
                tk.messagebox.showinfo("Login Successful",
                                       "Welcome {}".format(username))
                root.deiconify()
                top.destroy()
            else:
                tk.messagebox.showerror("Information", "The Username or Password you have entered are incorrect ")

        def validate(username, password):
            # Checks the text file for a username/password combination.
            if password=="admin" and username=="admin":
                return True
            return False


class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        main_frame = tk.Frame(self, bg="#84CEEB", height=600, width=1024)
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        # self.resizable(0, 0) prevents the app from being resized
        # self.geometry("1024x600") fixes the applications size
        self.frames = {}
        F = Some_Widgets
        frame = F(main_frame, self)
        self.frames[F] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Some_Widgets)

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def OpenNewWindow(self):
        OpenNewWindow()

    def Quit_application(self):
        self.destroy()


class GUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.main_frame = tk.Frame(self, bg="#BEB2A7", height=600, width=1024)
        # self.main_frame.pack_propagate(0)
        self.main_frame.pack(fill="both", expand="true")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)


class Some_Widgets(GUI):  # inherits from the GUI class
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)

        title_styles = {"font": ("Trebuchet MS Bold", 16), "background": "blue"}

        text_styles = {"font": ("Verdana", 10),
                       "background": "#BEB2A7",
                       "foreground": "black"}

        frame1 = tk.LabelFrame(self, frame_styles, text="Accounts")
        frame1.place(rely=0.05, relx=0.02, height=250, width=1000)

        frame2 = tk.LabelFrame(self, frame_styles, text="Bot Control")
        frame2.place(rely=0.35, relx=0.02, height=350, width=1000)

        # input username
        input1 = tk.Entry(frame2, width=45, cursor="xterm")
        input1.pack()
        input2 = tk.Entry(frame2, width=45, cursor="xterm")
        input2.pack()
        input3 = tk.Entry(frame2, width=45, cursor="xterm")
        input3.pack()

        # input password
        label_user = tk.Label(frame2, text_styles, text="username:")
        label_user.place(height=20, width=150, rely=0, relx=0.1)
        label_pw = tk.Label(frame2, text_styles, text="password:")
        label_pw.place(height=20, width=150, rely=0.1, relx=0.1)
        label_hashtag = tk.Label(frame2, text_styles, text="hashtag:")
        label_hashtag.place(height=20, width=150, rely=0.2, relx=0.1)

        button2 = ttk.Button(frame2, text="add account", command=lambda: add_account())
        button2.pack()

        #comment
        #add margin top
        
        input4 = tk.Entry(frame2, width=45, cursor="xterm")
        input4.place(rely=0.4, relx=0.295)

        label_comment = tk.Label(frame2, text_styles, text="comment:")
        label_comment.place(height=20, width=150, rely=0.4, relx=0.1)
        
        button3 = ttk.Button(frame2, text="add comment", command=lambda: add_comment())
        button3.place(rely=0.48, relx=0.45)


        # number of comments
        input5 = tk.Entry(frame2, width=45, cursor="xterm")
        input5.place(rely=0.6, relx=0.295)

        label_number = tk.Label(frame2, text_styles, text="number of comments:")
        label_number.place(height=20, width=150, rely=0.6, relx=0.1)

        button4 = ttk.Button(frame2, text="start bot", command=lambda: update_number_of_comments())
        button4.place(rely=0.68, relx=0.45)

        # print last info
        label_last_info = tk.Label(frame2, text_styles, text="update:")
        label_last_info.place(height=20, width=150, rely=0.8, relx=0.1)
        label_last_info_value = tk.Label(frame2, text_styles, text=last_info)
        label_last_info_value.place(height=20, width=500, rely=0.8, relx=0.295)



        # This is a treeview.
        tv1 = ttk.Treeview(frame1)
        column_list_account = ["username", "password", "hashtag"]
        tv1['columns'] = column_list_account
        tv1["show"] = "headings"  # removes empty column
        for column in column_list_account:
            tv1.heading(column, text=column)
            tv1.column(column, width=50)
        tv1.place(relheight=0.7, relwidth=0.995)
        treescroll = tk.Scrollbar(frame1)
        treescroll.configure(command=tv1.yview)
        tv1.configure(yscrollcommand=treescroll.set)
        treescroll.pack(side="right", fill="y")
        
        tv2 = ttk.Treeview(frame2)
        column_list_comment = ["comments"]
        tv2['columns'] = column_list_comment
        tv2["show"] = "headings"  # removes empty column
        for column in column_list_comment:
            tv2.heading(column, text=column)
            tv2.column(column, width=150, anchor="center")
        tv2.place(relheight=1, relwidth=0.3, rely=0, relx=0.7)
        treescroll2 = tk.Scrollbar(frame2)
        treescroll2.configure(command=tv2.yview)
        tv2.configure(yscrollcommand=treescroll2.set)
        treescroll2.pack(side="right", fill="y")
        

        def Load_AccData():
            for row in account_info:
                tv1.insert("", "end", values=row)

        def Load_CommentData():
            for comment in database["comment_list"]:
                tv2.insert("", "end", values=(comment,))

        def add_account():
            # Deletes the data in the current treeview and reinserts it.
            account_info.append([input1.get(), input2.get(), input3.get()])
            # write into database.json
            database["accounts"].append([input1.get(), input2.get()])
            database["hashtags"].append(input3.get())
            #write into new file
            with open(r".\database.json" , 'w+') as f:
                json.dump(database, f)
            
            tv1.delete(*tv1.get_children())  # *=splat operator
            Load_AccData()

        def add_comment():
            database["comment_list"].append(input4.get())
            #write into new file
            with open(r".\database.json" , 'w+') as f:
                json.dump(database, f)

            tv2.delete(*tv2.get_children())  # *=splat operator
            Load_CommentData()

        def update_number_of_comments():
            database["number_of_comments"] = input5.get()
            #write into new file
            with open(r".\database.json" , 'w+') as f:
                json.dump(database, f)
            numberOfAccounts = len(account_info)
            parentBot(numberOfAccounts)
            
        Load_AccData()
        Load_CommentData()

if __name__ == "__main__":
    top = LoginPage()
    top.title("login")
    root = MyApp()
    root.withdraw()
    root.title("instagram comment bot")
    root.mainloop()