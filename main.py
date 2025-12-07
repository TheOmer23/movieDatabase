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
    if not email or not password:
        raise ValueError("Email and password are required")
    # Correct check: look for a document with {'email': email}
    if collection.find_one({"email": email}):
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
        response = requests.get(f"http://www.omdbapi.com/?{api_key}&s={movie_name}")
        movie_data = response.json()
        if movie_data["Response"] == "False":
            raise ValueError(f"Movie '{movie_name}' not found!")
        return movie_data
    except Exception as e:
        print(f"Error: {e}")
        return None
        
def get_movie_poster(movie_name):
    try:
        response = requests.get(f"http://www.omdbapi.com/?{api_key}&s={movie_name}")
        movie_data = response.json()
        if movie_data["Response"] == "False":
            raise ValueError(f"Movie '{movie_name}' not found!")
        else:
            posters = []
            for movie in movie_data["Search"]:
                if movie_name.lower() in movie["Title"].lower():
                    posters.append(movie["Poster"])
            return posters
    except Exception as e:
        print(f"Error: {e}")
        return None
        

if __name__ == "__main__":
    # email = input("Enter email:")
    # password = input("Enter Password:")
    # print(signup(email,password))
    print(get_movie_poster("ted"))
    # print(movie_check("batman"))
    # print(login("omer3199@gmail.com", "123456"))
    
