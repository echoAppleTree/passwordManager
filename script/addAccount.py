"""
Author : David-Alexandre Guenette <da.guenette@icloud.com>
Date   : 2021-01-18
Purpose: Password Manager
"""

from cryptography.fernet import Fernet
import argparse
import pymongo
import dns # required for connecting with SRV
# import credentials.py


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


def main():
    """ Main Function"""
        
    args = get_args()
    email = args.email
    pwd = args.pwd
    url = args.url
    service = args.service

    # Generate encoded password
    key = Fernet.generate_key()
    f = Fernet(key)
    encoded_pwd = f.encrypt(pwd.encode('utf-8'))
    
    # Connection to MangoDB
    client = pymongo.MongoClient("mongodb+srv://root:wBZ7KvWpajhUTbt8@passwordmanager.njg0o.mongodb.net/passwordManager?retryWrites=true&w=majority")
    db = client["passwordManager"]
    col = db["accounts"]

    mydict = {"email": email, "pwd": encoded_pwd, "url": url, "service": service, "key": key}
    x = col.insert_one(mydict)
    print(x.inserted_id)

        
if __name__ == '__main__':
    main()
    
         

    
   
