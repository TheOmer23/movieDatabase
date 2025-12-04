from passwords import uri, api_key
from pymongo import MongoClient
import bcrypt
import requests


omdb_key = api_key
client = MongoClient(uri)

# Choose a database and collection
db = client["my_database"]
collection = db["users"]
movie_collection = db["movies"]

def find_profile(email):
    return collection.find_one({"email": email})

def signup(email,password):
    if collection.find_one(email):
        raise ValueError(f"{email} user already exists")
    password = hash_password(password)
    collection.insert_one({"email": email,
                           "password": password,
                           "movies": []})

def login(email,password):
    profile = find_profile(email)
    if not profile:
        return None
    hashed_password = profile["password"]
    if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
        return profile
    else:
        return None
    
def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password

def add_movie_to_watchlist(email, movie_name) -> None:
    if not find_profile(email):
        return None
    try:
        response = requests.get(f"http://www.omdbapi.com/?{api_key}&t={movie_name}")
        movie_data = response.json()
        if movie_data["Response"] == "False":
            raise ValueError(f"Movie '{movie_name}' not found!")
        else:
            collection.update_one({"email": email}
                                  ,{"$addToSet": {"movies":movie_name}}) 
            if not movie_collection.find_one({"Title": movie_name}):
                movie_collection.insert_one(movie_data)
    except Exception as e:
        print(f"Error: {e}")
    return None
    
def movie_check(movie_name):
    try:
        response = requests.get(f"http://www.omdbapi.com/?{api_key}&t={movie_name}")
        movie_data = response.json()
        if movie_data["Response"] == "False":
            raise ValueError(f"Movie '{movie_name}' not found!")

    except Exception as e:
        print(f"Error: {e}")
        

if __name__ == "__main__":
    email = input("Enter email:")
    password = input("Enter Password:")
    if login(email,password):
        movie = input("Enter a movie to watchlist:")
        add_movie_to_watchlist(email, movie)
    else:
        signup(email,password)
    # print(login("omer3199@gmail.com", "123456"))
    
