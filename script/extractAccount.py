import argparse
from cryptography.fernet import Fernet
import pymongo
import dns # required for connecting with SRV


def get_args():
    """ Get command-line arguments """
    
    parser = argparse.ArgumentParser(
        description='Password Manager',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        
    parser.add_argument('service',
                        metavar='str',
                        help='The service')

    return parser.parse_args()




def main():
    args = get_args()
    service = args.service
 
    # Connection to MangoDB
    client = pymongo.MongoClient("mongodb+srv://root:wBZ7KvWpajhUTbt8@passwordmanager.njg0o.mongodb.net/passwordManager?retryWrites=true&w=majority")
    db = client["passwordManager"]
    col = db["accounts"]

    for x in col.find({},{"pwd": 1, "service": 1, "key": 1}):
        if x['service'] == service:
            key = x['key']
            f = Fernet(key)
            token = x['pwd']
            print(f.decrypt(token))

if __name__ == '__main__':
    main()
    