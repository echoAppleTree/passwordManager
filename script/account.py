"""
Author : David-Alexandre Guenette <da.guenette@icloud.com>
Date   : 2021-01-18
Purpose: Account Functions for Password Manager
"""

from cryptography.fernet import Fernet
import pymongo
import dns # required for connecting with SRV
import credential



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
    """Add an account to db with encoded password."""

    # 01 - Declare user1 from credentials
    user1 = credential.dbManager01

    # 02 - Generate encoded password & key
    secure_pwd, secure_key = encode_password(a_pwd)

    # 03 - Connection to MangoDB
    collections = connection_to_db(user1.name, user1.password, user1.db)
    mydict = {"email": a_email, "pwd": secure_pwd, "url": a_url, "service": a_service, "key": secure_key}
    x = collections.insert_one(mydict)
    

def find_password(f_email, f_service):
    """Find and decode password"""
    # 01 - Declare user1 from credentials
    user1 = credential.dbManager01

    # 02 - Connection to MangoDB
    collections = connection_to_db(user1.name, user1.password, user1.db)

    # 04 - Give password to user
    for x in collections.find({},{"email": 1, "pwd": 1, "url": 1, "service": 1, "key": 1}):
        if x['email'] == f_email and x['service'] == f_service:
            key = x['key']
            f = Fernet(key)
            token = x['pwd']
            decoded_pwd = f.decrypt(token).decode('utf-8')
            
            return decoded_pwd


    
   
