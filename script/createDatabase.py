import pymongo
import dns # required for connecting with SRV



client = pymongo.MongoClient("mongodb+srv://root:wBZ7KvWpajhUTbt8@passwordmanager.njg0o.mongodb.net/passwordManager?retryWrites=true&w=majority")
db = client["passwordManager"]

col = db["accounts"]

mydict = {"email": "test@gmail.com", "pwd": "pwd123", "url": "test.com", "service": "test", "key": "tAeST"}

x = col.insert_one(mydict)

print(x.inserted_id)