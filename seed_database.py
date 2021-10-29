import os 
import json
from random import choice, randint
from datetime import datetime 
import model, server, crud 

os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

# Load movie data from JSON file
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    release = movie["release_date"]
    format = "%Y-%m-%d"
    date = datetime.strptime(release, format)

    movie_added = crud.create_movie(title = movie["title"], overview = movie["overview"], release_date = date,
                        poster_path = movie["poster_path"])
    movies_in_db.append(movie_added)


for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    user = crud.create_user(email, password)
    
    movie = choice(movies_in_db)
    score = randint(1,5)
    crud.create_rating(user, movie, score)
    