"""
Author : David-Alexandre Guenette <da.guenette@icloud.com>
Date   : 2021-01-18
Purpose: Interface Functions for Password Manager
"""

import tkinter as tk
import account as acc

def label(window, txtType, fontSpecs):
    """Label Object for Interface"""
    label = tk.Label(window, text=txtType, font=fontSpecs)
    return label


def entry(window, txtType, fontSpecs, display=None):
    """Entry Object for Interface"""
    entry = tk.Entry(window, text=txtType, font=fontSpecs, show=display)
    return entry


def button(window, txtType, func):
    """Button Object for Interface"""
    btn = tk.Button(window, text = txtType, command = func)
    return btn


def text(window, width_num, height_num):
    """Text Field Object for Interface"""
    textWidget = tk.Text(window, width=width_num, height=height_num)
    scrollBard = tk.Scrollbar(window)
    scrollBard.config(command=textWidget.yview)
    textWidget.config(yscrollcommand=scrollBard.set)
    return textWidget


def grid(obj, row_num, column_num, padx_num=None, pady_num=None):
    """Grid Object for Interface"""
    obj.grid(row=row_num, column=column_num, padx=padx_num, pady=pady_num)
    return obj


def build_itf():
    """Build interface"""

    root = tk.Tk()

    # Setting the window's size
    root.geometry("600x400")

    # Add Account - Variables Input
    global_email = tk.StringVar()
    global_pwd = tk.StringVar()
    global_url = tk.StringVar()
    global_service = tk.StringVar()


    # Find Password - Variables Input
    global_email_find = tk.StringVar()
    global_service_find = tk.StringVar()


    # Create instance of file like object
    display_add = text(root, 30, 5)
    display_find = text(root, 30, 5)


    # Submit Function to send data to db
    def submit():
        """
        Defining a function that will get the name and password and print them on the screen
        """

        # 01 - Defining variables
        email = entry(root, global_email, ('calibre', 10, 'normal')).get()
        pwd = entry(root, global_pwd, ('calibre', 10, 'normal'), '*').get()
        url = entry(root, global_url, ('calibre', 10, 'normal')).get()
        service = entry(root, global_service, ('calibre', 10, 'normal')).get()

        # 02 - Display on widget
        display_add.delete('1.0', tk.END)
        quote = "Your email: {}.\nFor: {}\n".format(email, service)
        display_add.insert(tk.END, quote)


        # 03 - add account to db
        acc.add_account(pwd, email, url, service)

        # 04 - Reset entries
        global_email.set("")
        global_pwd.set("")
        global_url.set("")
        global_service.set("")


    # Find Function to retrieve password from db
    def find():
        # 01 - Defining variables
        email = entry(root, global_email_find, ('calibre', 10, 'normal')).get()
        service = entry(root, global_service_find, ('calibre', 10, 'normal')).get()

        # 03 - Find account
        pwd = acc.find_password(email, service)

        # 02 - Display on widge
        display_find.delete('1.0', tk.END)
        quote = "Your password for {} is:\n  {}".format(service, pwd)
        display_find.insert(tk.END, quote)

        # 04 - Reset entries
        global_email_find.set("")
        global_service_find.set("")


    # Label / Entry - Grid Positioning - Add Account
    grid(label(root, 'Email', ('calibre', 10, 'bold')), 0, 0)
    grid(entry(root, global_email, ('calibre', 10, 'normal')), 0, 1)
    grid(label(root, 'Password', ('calibre', 10, 'bold')), 1, 0)
    grid(entry(root, global_pwd, ('calibre', 10, 'normal'), '*'), 1, 1)
    grid(label(root, 'URL', ('calibre', 10, 'bold')), 2, 0)
    grid(entry(root, global_url, ('calibre', 10, 'normal')), 2, 1)
    grid(label(root, 'Service', ('calibre', 10, 'bold')), 3, 0)
    grid(entry(root, global_service, ('calibre', 10, 'normal')), 3, 1)

    grid(button(root, 'Submit', submit), 4, 1, 20, 5)

    grid(display_add, 5, 1, 5, 20)

    # Label / Entry - Grid Positioning - Find Password
    grid(label(root, 'Email', ('calibre', 10, 'bold')), 6, 0)
    grid(entry(root, global_email_find, ('calibre', 10, 'normal')), 6, 1)
    grid(label(root, 'Service', ('calibre', 10, 'bold')), 7, 0)
    grid(entry(root, global_service_find, ('calibre', 10, 'normal')), 7, 1)

    grid(button(root, 'Find', find), 8, 1, 20, 20)

    grid(display_find, 9, 1, 5, 20)

    # Performing an infinite loop for the window to display
    root.mainloop() 