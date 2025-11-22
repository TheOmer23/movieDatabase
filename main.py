from passwords import uri
from pymongo import MongoClient

# uri =  "mongodb+srv://omer3199_db_user:Aa123456@users.qdpzz3w.mongodb.net/"

client = MongoClient(uri)

# Choose a database and collection
db = client["my_database"]
collection = db["users"]

#insert an example
doc = {"username": "Alex123",
       "password": "123456",
       "email": "alex@gmail.com",
       "movies": []}
# collection.insert_one(doc)

# print("Inserted one document!")

def findprofile(email):
    return collection.find_one({"email": email})

def signup(email,password):
    collection.insert_one({"email": email,
                           "password": password,
                           "movies": []})

def login(email,password):
    return collection.find_one({"email": email,
                                "password": password})

if __name__ == "__main__":
    if findprofile("jane@affbc.com"):
        print("False")
    else:
        print("True")
