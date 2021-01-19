# Program to make a simple
# login screen

import tkinter as tk
from cryptography.fernet import Fernet
import argparse
import pymongo
import dns # required for connecting with SRV
import credential
import addAccount

def encode_password(password):
    """ Encode password with Fernet"""
    key = Fernet.generate_key()
    f = Fernet(key)
    encoded_pwd = f.encrypt(password.encode('utf-8'))

    return encoded_pwd, key


def connection_to_db(username, password, database):
    """Create connection to db"""
    client = pymongo.MongoClient("mongodb+srv://{}:{}@passwordmanager.njg0o.mongodb.net/{}?retryWrites=true&w=majority".format(username, password, database))
    db = client["passwordManager"]
    col = db["accounts"]

    return col


def confirmation_message(email, url, _id):
    """Confirmation message after registering new information."""

    print("Thank you {} for registering your information for {}.".format(email, url))
    print("Here's your ID: {}".format(_id))
    print("---------------------------------")
    print("In order to extract your password, call 'extractAccount.py <service>'.")


def add_account(a_pwd, a_email, a_url, a_service):
    # 01 - Declare user1 from credentials
    user1 = credential.u1

    # 04 - Generate encoded password & key
    secure_pwd, secure_key = encode_password(a_pwd)

    #05 - Connection to MangoDB
    collections = connection_to_db(user1.name, user1.password, user1.db)
    mydict = {"email": a_email, "pwd": secure_pwd, "url": a_url, "service": a_service, "key": secure_key}
    x = collections.insert_one(mydict) 

    # 06 - Print confirmation
    confirmation_message(mydict['email'], mydict['url'], x.inserted_id)   


def build_ui():

    root = tk.Tk()

    # Setting the window's size
    root.geometry("600x400")

    # Declaring string variable for name and pwd
    global_email = tk.StringVar()
    global_pwd = tk.StringVar()
    global_url = tk.StringVar()
    global_service = tk.StringVar()

    def submit():
        """
        Defining a function that will get the name and password and print them on the screen
        """

        # 01 - Defining variables
        email = email_entry.get()
        pwd = pwd_entry.get()
        url = url_entry.get()
        service = service_entry.get()

        # 02 - Test to console
        print("The name is : " + email)
        print("The password is : " + pwd)
        print("The url is : " + url)
        print("The service is : " + service)

        add_account(pwd, email, url, service)

        global_email.set("")
        global_pwd.set("")
        global_url.set("")
        global_service.set("")


    # Email Label
    email_label = tk.Label(root, text = 'Username', font=('calibre', 10, 'bold'))

    # Email Entry
    email_entry = tk.Entry(root, text = global_email, font=('calibre', 10, 'normal'))

    # Password Label
    pwd_label = tk.Label(root, text = 'Password', font = ('calibre', 10, 'bold'))

    # Password Entry
    pwd_entry = tk.Entry(root, textvariable = global_pwd, font = ('calibre', 10, 'normal'), show = '*')

    # URL Label
    url_label = tk.Label(root, text = 'URL', font = ('calibre', 10, 'bold'))

    # URL Entry
    url_entry = tk.Entry(root, textvariable = global_url, font = ('calibre', 10, 'normal'))

    # Service Label
    service_label = tk.Label(root, text = 'Service', font = ('calibre', 10, 'bold'))

    # Service Entry
    service_entry = tk.Entry(root, textvariable = global_service, font = ('calibre', 10, 'normal'))


    # Submit
    sub_btn = tk.Button(root, text = 'Submit', command = submit)

    # Placing the label and entry in the required position using grid method
    email_label.grid(row=0, column=0)
    email_entry.grid(row=0, column=1)
    pwd_label.grid(row=1, column=0)
    pwd_entry.grid(row=1, column=1)
    url_label.grid(row=2, column=0)
    url_entry.grid(row=2, column=1)
    service_label.grid(row=3, column=0)
    service_entry.grid(row=3, column=1)

    sub_btn.grid(row=4, column=0)

    # Performing an infinite loop for the window to display
    root.mainloop() 

def main():
    build_ui()

if __name__ == '__main__':
    main()