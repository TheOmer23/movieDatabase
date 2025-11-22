from passwords import uri
from pymongo import MongoClient

# uri =  "mongodb+srv://omer3199_db_user:Aa123456@users.qdpzz3w.mongodb.net/"

client = MongoClient(uri)

# Choose a database and collection
db = client["my_database"]
collection = db["users"]

#insert an example
doc = {"name": "Omer", "age": 26}
collection.insert_one(doc)

print("Inserted one document!")
