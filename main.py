from passwords import uri
from pymongo import MongoClient
import bcrypt
import requests

omdb_key = "http://www.omdbapi.com/?apikey=641cb94e&"
# uri =  "mongodb+srv://omer3199_db_user:Aa123456@users.qdpzz3w.mongodb.net/"

client = MongoClient(uri)

# Choose a database and collection
db = client["my_database"]
collection = db["users"]
movie_collection = db["movies"]

def signup(email,password):
    password = hash_password(password)
    collection.insert_one({"email": email,
                           "password": password,
                           "movie names": []})

def login(email,password):
    profile = collection.find_one({"email": email})
    if not profile:
        return None
    hashed_password = profile["password"]
    print(hashed_password)
    if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
        return profile
    else:
        return None
    
def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password



# if __name__ == "__main__":
    
