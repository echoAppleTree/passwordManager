import argparse
from cryptography.fernet import Fernet
import pymongo
import dns # required for connecting with SRV
import credential


def get_args():
    """ Get command-line arguments """
    
    parser = argparse.ArgumentParser(
        description='Password Manager',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        
    parser.add_argument('email',
                        metavar='str',
                        help='Your email')
    
    parser.add_argument('service',
                        metavar='str',
                        help='The service')

    return parser.parse_args()


def connection_to_db(username, password, database):
    """Create connection to db"""
    client = pymongo.MongoClient("mongodb+srv://{}:{}@passwordmanager.njg0o.mongodb.net/{}?retryWrites=true&w=majority".format(username, password, database))
    db = client["passwordManager"]
    col = db["accounts"]

    return col


def main():

    # 01 - Declare arguements from argparse
    args = get_args()
    service = args.service
    email = args.email

    # 02 - Declare user1 from credentials
    user1 = credential.u1

    # 03 - Connection to MangoDB
    collections = connection_to_db(user1.name, user1.password, user1.db)

    # 04 - Give password to user
    for x in collections.find({},{"email": 1, "pwd": 1, "url": 1, "service": 1, "key": 1}):
        if x['email'] == email and x['service'] == service:
            key = x['key']
            f = Fernet(key)
            token = x['pwd']
            decoded_pwd = f.decrypt(token).decode('utf-8')

            print("Hello {}, here's your password for {}.".format(x['email'], x['url']))
            print("Password: {}".format(decoded_pwd))


if __name__ == '__main__':
    main()
    