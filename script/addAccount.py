"""
Author : David-Alexandre Guenette <da.guenette@icloud.com>
Date   : 2021-01-18
Purpose: Password Manager
"""

from cryptography.fernet import Fernet
import argparse
import pymongo
import dns # required for connecting with SRV
import credential
import ui


def get_args():
    """ Get command-line arguments """
    
    parser = argparse.ArgumentParser(
        description='Password Manager',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        
    parser.add_argument('email',
                        metavar='str',
                        help='Your email')
                      
    parser.add_argument('pwd',
                        metavar='str',
                        help='Your password')
                        
    parser.add_argument('url',
                        metavar='str',
                        help="Site's URL")

    parser.add_argument('service',
                        metavar='str',
                        help='The service')


    return parser.parse_args()


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


def main():
    """ Main Function"""
        
    # 01 - Declare arguements from argparse
    args = get_args()
    email = args.email
    pwd = args.pwd
    url = args.url
    service = args.service

    # 02 - Declare user1 from credentials
    user1 = credential.u1

    # 03 - Generate encoded password & key
    secure_pwd, secure_key = encode_password(pwd)
    
    # 04 - Connection to MangoDB
    collections = connection_to_db(user1.name, user1.password, user1.db)
    mydict = {"email": email, "pwd": secure_pwd, "url": url, "service": service, "key": secure_key}
    x = collections.insert_one(mydict)

    # 05 - Print confirmation
    confirmation_message(mydict['email'], mydict['url'], x.inserted_id)
        
if __name__ == '__main__':
    main()
    
         

    
   
